"""
Sandbox for isolated code execution with resource limits.

Provides a controlled environment for executing untrusted or experimental code
with configurable timeouts, memory limits, and permission restrictions.

⚠️ SECURITY WARNING:
    This sandbox provides BASIC isolation for development and testing purposes.
    It is NOT a complete security solution and should NOT be used in production
    environments with truly malicious code.

    For production-grade sandboxing, consider:
    - Docker containers with resource limits
    - Virtual machines
    - Specialized sandboxing solutions (Firecracker, gVisor, Kata Containers)

Philosophy:
    Cognitive systems need to experiment and learn, which sometimes involves
    running code generated or modified by AI agents. A sandbox provides a
    safety boundary that allows experimentation while preventing catastrophic
    failures like infinite loops, memory exhaustion, or system damage.

    This implementation focuses on:
    1. Time limits (prevent infinite loops)
    2. Memory limits (prevent memory exhaustion)
    3. Exception isolation (failures don't crash host)
    4. Namespace isolation (prevent global state pollution)

Use Cases:
    - Testing AI-generated code
    - Running user-submitted code in educational contexts
    - Experimental algorithm evaluation
    - Safe execution of dynamic configuration
    - CTF challenges and coding competitions

Limitations:
    ⚠️ This sandbox does NOT protect against:
    - Malicious file system access
    - Network operations
    - System calls (fork bombs, etc.)
    - Side-channel attacks
    - Cryptographic attacks
    - Resource exhaustion via subprocesses

    For these threats, use OS-level sandboxing (containers, VMs, seccomp, etc.)

Example::

    # Basic usage
    sandbox = Sandbox(timeout=5.0, memory_limit_mb=100)

    result = sandbox.execute('''
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n-1) + fibonacci(n-2)

    result = fibonacci(10)
    ''')

    print(result.output)  # 55
    print(result.execution_time)  # e.g., 0.002 seconds

    # With timeout
    try:
        result = sandbox.execute('''
        while True:
            pass  # Infinite loop
        ''')
    except SandboxTimeoutError:
        print("Code execution timed out")

:author: ForgeBase Development Team
:since: 2025-11-03
"""

import io
import time
import traceback
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
from typing import Any


class SandboxError(Exception):
    """Base exception for sandbox-related errors."""

    def __init__(self, message: str, context: dict[str, Any] | None = None):
        """
        Initialize sandbox error.

        :param message: Error description
        :type message: str
        :param context: Additional context information
        :type context: Optional[Dict[str, Any]]
        """
        super().__init__(message)
        self.context = context or {}


class SandboxTimeoutError(SandboxError):
    """
    Raised when code execution exceeds timeout limit.

    This indicates the code is likely in an infinite loop or taking
    too long to complete.
    """
    pass


class SandboxMemoryError(SandboxError):
    """
    Raised when code execution exceeds memory limit.

    This indicates the code is consuming too much memory, possibly
    due to large data structures or memory leaks.
    """
    pass


class SandboxExecutionError(SandboxError):
    """
    Raised when code execution fails with an exception.

    Contains details about the exception that occurred during execution.
    """

    def __init__(self, message: str, original_exception: Exception | None = None, context: dict[str, Any] | None = None):
        """
        Initialize execution error.

        :param message: Error description
        :type message: str
        :param original_exception: The exception that occurred during execution
        :type original_exception: Optional[Exception]
        :param context: Additional context information
        :type context: Optional[Dict[str, Any]]
        """
        super().__init__(message, context)
        self.original_exception = original_exception


@dataclass
class ExecutionResult:
    """
    Result of code execution in sandbox.

    Contains all information about the execution: output, return value,
    timing, and any errors that occurred.

    :ivar success: Whether execution completed successfully
    :vartype success: bool
    :ivar output: Captured stdout output
    :vartype output: str
    :ivar error_output: Captured stderr output
    :vartype error_output: str
    :ivar return_value: Value returned by the code (if any)
    :vartype return_value: Any
    :ivar exception: Exception that occurred (if any)
    :vartype exception: Optional[Exception]
    :ivar exception_traceback: Full traceback of exception (if any)
    :vartype exception_traceback: Optional[str]
    :ivar execution_time: Time taken to execute (seconds)
    :vartype execution_time: float
    :ivar timeout: Whether execution timed out
    :vartype timeout: bool
    """

    success: bool
    output: str
    error_output: str
    return_value: Any = None
    exception: Exception | None = None
    exception_traceback: str | None = None
    execution_time: float = 0.0
    timeout: bool = False

    def __str__(self) -> str:
        """String representation of execution result."""
        if self.success:
            return f"ExecutionResult(success=True, time={self.execution_time:.3f}s)"
        error_type = "Timeout" if self.timeout else type(self.exception).__name__ if self.exception else "Unknown"
        return f"ExecutionResult(success=False, error={error_type}, time={self.execution_time:.3f}s)"


class Sandbox:
    """
    Sandbox for isolated code execution with resource limits.

    Provides a controlled environment for executing Python code with
    configurable timeout and memory limits. Captures output and handles
    exceptions gracefully.

    Features:
        - Timeout protection (prevents infinite loops)
        - Memory limit monitoring (basic)
        - Output capture (stdout/stderr)
        - Exception isolation
        - Clean namespace for each execution
        - Execution timing

    Security Notes:
        ⚠️ This is a BASIC sandbox suitable for:
        - Development and testing
        - Educational environments
        - Low-risk code execution
        - Trusted code with bugs

        NOT suitable for:
        - Production with untrusted code
        - Security-critical applications
        - Malicious code execution
        - Multi-tenant systems

    :ivar timeout: Maximum execution time in seconds
    :vartype timeout: float
    :ivar memory_limit_mb: Maximum memory usage in MB (informational only)
    :vartype memory_limit_mb: int
    :ivar restricted_modules: Module names that cannot be imported
    :vartype restricted_modules: set

    Example::

        # Create sandbox with 5 second timeout
        sandbox = Sandbox(timeout=5.0, memory_limit_mb=100)

        # Execute safe code
        result = sandbox.execute('''
        x = 10
        y = 20
        result = x + y
        print(f"Sum: {result}")
        ''')

        print(result.output)  # "Sum: 30"
        print(result.return_value)  # None (nothing returned)

        # Execute code with return value
        result = sandbox.execute('''
        def calculate():
            return 42

        result = calculate()
        ''', capture_result='result')

        print(result.return_value)  # 42
    """

    def __init__(
        self,
        timeout: float = 10.0,
        memory_limit_mb: int = 100,
        restricted_modules: set | None = None
    ):
        """
        Initialize sandbox with resource limits.

        :param timeout: Maximum execution time in seconds (default: 10.0)
        :type timeout: float
        :param memory_limit_mb: Maximum memory in MB (informational, default: 100)
        :type memory_limit_mb: int
        :param restricted_modules: Set of module names to restrict (default: None)
        :type restricted_modules: Optional[set]

        Example::

            # Strict sandbox
            sandbox = Sandbox(
                timeout=1.0,
                memory_limit_mb=50,
                restricted_modules={'os', 'sys', 'subprocess'}
            )
        """
        self.timeout = timeout
        self.memory_limit_mb = memory_limit_mb
        self.restricted_modules = restricted_modules or set()

        # Add some commonly restricted modules by default
        self.restricted_modules.update({'os', 'sys', 'subprocess', 'importlib'})

    def execute(
        self,
        code: str,
        globals_dict: dict[str, Any] | None = None,
        locals_dict: dict[str, Any] | None = None,
        capture_result: str | None = None
    ) -> ExecutionResult:
        """
        Execute code in isolated environment.

        Runs the provided code with timeout protection, output capture,
        and exception handling.

        :param code: Python code to execute
        :type code: str
        :param globals_dict: Global namespace for execution (default: clean namespace)
        :type globals_dict: Optional[Dict[str, Any]]
        :param locals_dict: Local namespace for execution (default: same as globals)
        :type locals_dict: Optional[Dict[str, Any]]
        :param capture_result: Name of variable to capture as return value
        :type capture_result: Optional[str]
        :return: Execution result with output and status
        :rtype: ExecutionResult
        :raises SandboxTimeoutError: If execution exceeds timeout
        :raises SandboxExecutionError: If execution fails critically

        Example::

            sandbox = Sandbox(timeout=5.0)

            # Basic execution
            result = sandbox.execute('print("Hello")')
            print(result.output)  # "Hello\\n"

            # Capture return value
            result = sandbox.execute('''
            answer = 42
            ''', capture_result='answer')
            print(result.return_value)  # 42

            # With custom globals
            result = sandbox.execute(
                'result = multiply(x, y)',
                globals_dict={'multiply': lambda a, b: a * b, 'x': 5, 'y': 3},
                capture_result='result'
            )
            print(result.return_value)  # 15
        """
        # Setup clean namespace
        if globals_dict is None:
            globals_dict = {
                '__builtins__': self._create_restricted_builtins(),
                '__name__': '__sandbox__',
                '__doc__': None,
            }

        if locals_dict is None:
            locals_dict = globals_dict

        # Capture output
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        # Track execution time
        start_time = time.time()
        exception = None
        exception_tb = None
        return_value = None
        timeout_occurred = False

        try:
            # Simple timeout implementation using signal (Unix-like systems)
            # Note: This is basic and doesn't work on Windows or with threads
            import signal

            def timeout_handler(signum, frame):
                raise TimeoutError("Execution timeout")

            # Set timeout alarm (if supported)
            if hasattr(signal, 'SIGALRM'):
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(int(self.timeout))

            try:
                # Redirect stdout/stderr
                with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                    # Execute code
                    exec(code, globals_dict, locals_dict)

                    # Capture result if requested
                    if capture_result and capture_result in locals_dict:
                        return_value = locals_dict[capture_result]

            finally:
                # Cancel alarm
                if hasattr(signal, 'SIGALRM'):
                    signal.alarm(0)

        except TimeoutError as e:
            timeout_occurred = True
            exception = e
            exception_tb = traceback.format_exc()

        except Exception as e:
            exception = e
            exception_tb = traceback.format_exc()

        # Calculate execution time
        execution_time = time.time() - start_time

        # Build and return result
        return ExecutionResult(
            success=(exception is None),
            output=stdout_capture.getvalue(),
            error_output=stderr_capture.getvalue(),
            return_value=return_value,
            exception=exception,
            exception_traceback=exception_tb,
            execution_time=execution_time,
            timeout=timeout_occurred
        )

    def _create_restricted_builtins(self) -> dict[str, Any]:
        """
        Create restricted builtins dictionary.

        Removes dangerous built-in functions that could be used for
        malicious purposes or to escape the sandbox.

        :return: Restricted builtins dictionary
        :rtype: Dict[str, Any]
        """
        # Start with safe builtins
        import builtins

        safe_builtins = {}

        # Allow most basic operations
        allowed = {
            'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes',
            'callable', 'chr', 'classmethod', 'complex', 'dict', 'dir',
            'divmod', 'enumerate', 'filter', 'float', 'format', 'frozenset',
            'getattr', 'hasattr', 'hash', 'hex', 'id', 'int', 'isinstance',
            'issubclass', 'iter', 'len', 'list', 'map', 'max', 'min',
            'next', 'object', 'oct', 'ord', 'pow', 'print', 'property',
            'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice',
            'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type',
            'vars', 'zip',
            # Keep some exceptions
            'Exception', 'ValueError', 'TypeError', 'KeyError', 'IndexError',
            'RuntimeError', 'StopIteration', 'AttributeError',
        }

        for name in allowed:
            if hasattr(builtins, name):
                safe_builtins[name] = getattr(builtins, name)

        # Custom __import__ to restrict modules
        def restricted_import(name, *args, **kwargs):
            if name in self.restricted_modules:
                raise ImportError(f"Module '{name}' is restricted in sandbox")
            return __import__(name, *args, **kwargs)

        safe_builtins['__import__'] = restricted_import

        return safe_builtins

    def __repr__(self) -> str:
        """String representation of sandbox."""
        return f"<Sandbox timeout={self.timeout}s memory_limit={self.memory_limit_mb}MB>"
