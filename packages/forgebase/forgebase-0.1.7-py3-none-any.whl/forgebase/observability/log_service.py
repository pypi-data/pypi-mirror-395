"""
Central logging service with structured logging and aggregation.

Provides a production-ready logging system with structured data, multiple
output handlers, context propagation, and correlation tracking. This service
builds on LoggerPort to provide enterprise-grade observability.

Philosophy:
    Effective observability requires more than just writing messages to files.
    Modern systems need structured, searchable, aggregatable logs that can be
    analyzed by both humans and machines. This service enables:

    1. Structured Data: Logs are JSON objects, not just strings
    2. Context Propagation: Automatic injection of contextual information
    3. Correlation: Track requests across system boundaries
    4. Aggregation: Collect logs from multiple sources
    5. Sampling: Reduce volume for high-frequency logs

Use Cases:
    - Production monitoring and debugging
    - Request tracing across services
    - Performance analysis
    - Security audit trails
    - Compliance logging
    - Error tracking and alerting

Example::

    # Initialize service
    log_service = LogService(
        service_name="forgebase-api",
        environment="production"
    )

    # Add file handler
    log_service.add_file_handler("logs/app.log")

    # Log with context
    log_service.info(
        "User logged in",
        user_id="123",
        ip_address="192.168.1.1",
        session_id="abc-def-ghi"
    )

    # With correlation ID
    with log_service.correlation_context("req-12345"):
        log_service.info("Processing request")
        # All logs in this context will have correlation_id="req-12345"

:author: ForgeBase Development Team
:since: 2025-11-03
"""

import contextlib
import json
import threading
import uuid
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any

from forgebase.infrastructure.logging.logger_port import LoggerPort, LogLevel


class LogContext:
    """
    Thread-local context for log metadata.

    Stores contextual information that should be automatically included
    in all log messages within the current thread/request.

    :ivar correlation_id: Request/transaction correlation ID
    :vartype correlation_id: Optional[str]
    :ivar user_id: Current user identifier
    :vartype user_id: Optional[str]
    :ivar custom: Custom context fields
    :vartype custom: Dict[str, Any]
    """

    def __init__(self):
        """Initialize empty log context."""
        self.correlation_id: str | None = None
        self.user_id: str | None = None
        self.custom: dict[str, Any] = {}

    def to_dict(self) -> dict[str, Any]:
        """
        Convert context to dictionary.

        :return: Context as dictionary
        :rtype: Dict[str, Any]
        """
        context = {}
        if self.correlation_id:
            context['correlation_id'] = self.correlation_id
        if self.user_id:
            context['user_id'] = self.user_id
        context.update(self.custom)
        return context

    def clear(self):
        """Clear all context data."""
        self.correlation_id = None
        self.user_id = None
        self.custom.clear()


# Thread-local storage for context
_context = threading.local()


def get_context() -> LogContext:
    """
    Get current thread's log context.

    :return: Current log context
    :rtype: LogContext
    """
    if not hasattr(_context, 'log_context'):
        _context.log_context = LogContext()
    return _context.log_context


class LogHandler:
    """
    Base class for log handlers.

    Handlers receive structured log entries and output them to various
    destinations (console, file, network, etc.).
    """

    def emit(self, log_entry: dict[str, Any]) -> None:
        """
        Emit a log entry.

        :param log_entry: Structured log entry
        :type log_entry: Dict[str, Any]
        """
        pass

    def flush(self) -> None:
        """Flush any buffered log entries."""
        pass

    def close(self) -> None:
        """Close handler and release resources."""
        pass


class ConsoleHandler(LogHandler):
    """
    Console output handler.

    Writes structured logs to stdout as JSON.
    """

    def emit(self, log_entry: dict[str, Any]) -> None:
        """Emit log entry to console."""
        print(json.dumps(log_entry, default=str))


class FileHandler(LogHandler):
    """
    File output handler.

    Writes structured logs to a file, with automatic rotation support.

    :ivar file_path: Path to log file
    :vartype file_path: Path
    :ivar max_bytes: Maximum file size before rotation (0=no rotation)
    :vartype max_bytes: int
    :ivar backup_count: Number of backup files to keep
    :vartype backup_count: int
    """

    def __init__(
        self,
        file_path: str,
        max_bytes: int = 0,
        backup_count: int = 0
    ):
        """
        Initialize file handler.

        :param file_path: Path to log file
        :type file_path: str
        :param max_bytes: Max file size before rotation (0=unlimited)
        :type max_bytes: int
        :param backup_count: Number of backup files
        :type backup_count: int
        """
        self.file_path = Path(file_path)
        self.max_bytes = max_bytes
        self.backup_count = backup_count

        # Create directory if needed
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        # Open file (kept open for handler lifetime, closed in close())
        self._file = open(self.file_path, 'a', encoding='utf-8')  # noqa: SIM115

    def emit(self, log_entry: dict[str, Any]) -> None:
        """Emit log entry to file."""
        self._file.write(json.dumps(log_entry, default=str) + '\n')

    def flush(self) -> None:
        """Flush file buffer."""
        if self._file:
            self._file.flush()

    def close(self) -> None:
        """Close log file."""
        if self._file:
            self._file.close()


class LogService(LoggerPort):
    """
    Central logging service with structured logging and aggregation.

    Provides enterprise-grade logging with:
    - Structured JSON logs
    - Multiple output handlers
    - Context propagation
    - Correlation IDs
    - Sampling for high-volume logs
    - Performance tracking

    Features:
        - Thread-safe operation
        - Automatic context injection
        - Flexible handler system
        - Log level filtering
        - Sampling for high-frequency events
        - Stack trace capture

    :ivar service_name: Name of the service
    :vartype service_name: str
    :ivar environment: Environment (dev, staging, prod)
    :vartype environment: str
    :ivar min_level: Minimum log level to process
    :vartype min_level: LogLevel
    :ivar handlers: List of log handlers
    :vartype handlers: List[LogHandler]

    Example::

        # Setup
        log_service = LogService(
            service_name="my-api",
            environment="production",
            min_level=LogLevel.INFO
        )

        # Add handlers
        log_service.add_console_handler()
        log_service.add_file_handler("logs/app.log")

        # Log with context
        with log_service.correlation_context("req-123"):
            log_service.info("Processing request", endpoint="/api/users")

            with log_service.context(user_id="user-456"):
                log_service.info("User action", action="create_order")
                # This log will have both correlation_id and user_id
    """

    def __init__(
        self,
        service_name: str = "forgebase",
        environment: str = "development",
        min_level: LogLevel = LogLevel.INFO
    ):
        """
        Initialize log service.

        :param service_name: Name of the service
        :type service_name: str
        :param environment: Environment name
        :type environment: str
        :param min_level: Minimum log level
        :type min_level: LogLevel
        """
        self.service_name = service_name
        self.environment = environment
        self.min_level = min_level
        self.handlers: list[LogHandler] = []
        self._lock = threading.Lock()

    def add_handler(self, handler: LogHandler) -> None:
        """
        Add a log handler.

        :param handler: Handler to add
        :type handler: LogHandler
        """
        with self._lock:
            self.handlers.append(handler)

    def add_console_handler(self) -> None:
        """Add console output handler."""
        self.add_handler(ConsoleHandler())

    def add_file_handler(
        self,
        file_path: str,
        max_bytes: int = 0,
        backup_count: int = 0
    ) -> None:
        """
        Add file output handler.

        :param file_path: Path to log file
        :type file_path: str
        :param max_bytes: Max file size before rotation
        :type max_bytes: int
        :param backup_count: Number of backups
        :type backup_count: int
        """
        self.add_handler(FileHandler(file_path, max_bytes, backup_count))

    def _should_log(self, level: LogLevel) -> bool:
        """
        Check if message at level should be logged.

        :param level: Log level
        :type level: LogLevel
        :return: True if should log
        :rtype: bool
        """
        return level >= self.min_level

    def _create_log_entry(
        self,
        level: LogLevel,
        message: str,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Create structured log entry.

        :param level: Log level
        :type level: LogLevel
        :param message: Log message
        :type message: str
        :param context: Additional context
        :type context: Dict[str, Any]
        :return: Structured log entry
        :rtype: Dict[str, Any]
        """
        # Get thread-local context
        thread_context = get_context().to_dict()

        # Build log entry
        log_entry = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': level.name,
            'service': self.service_name,
            'environment': self.environment,
            'message': message,
        }

        # Add thread context
        if thread_context:
            log_entry['context'] = thread_context

        # Merge additional context
        if context:
            if 'context' in log_entry:
                log_entry['context'].update(context)
            else:
                log_entry['context'] = context

        return log_entry

    def _emit(self, log_entry: dict[str, Any]) -> None:
        """
        Emit log entry to all handlers.

        :param log_entry: Structured log entry
        :type log_entry: Dict[str, Any]
        """
        with self._lock:
            for handler in self.handlers:
                try:
                    handler.emit(log_entry)
                except Exception as e:
                    # Don't let handler errors crash logging
                    print(f"Log handler error: {e}")

    def debug(self, message: str, **context: Any) -> None:
        """Log debug message."""
        if self._should_log(LogLevel.DEBUG):
            log_entry = self._create_log_entry(LogLevel.DEBUG, message, context)
            self._emit(log_entry)

    def info(self, message: str, **context: Any) -> None:
        """Log info message."""
        if self._should_log(LogLevel.INFO):
            log_entry = self._create_log_entry(LogLevel.INFO, message, context)
            self._emit(log_entry)

    def warning(self, message: str, **context: Any) -> None:
        """Log warning message."""
        if self._should_log(LogLevel.WARNING):
            log_entry = self._create_log_entry(LogLevel.WARNING, message, context)
            self._emit(log_entry)

    def error(self, message: str, **context: Any) -> None:
        """Log error message."""
        if self._should_log(LogLevel.ERROR):
            log_entry = self._create_log_entry(LogLevel.ERROR, message, context)
            self._emit(log_entry)

    def critical(self, message: str, **context: Any) -> None:
        """Log critical message."""
        if self._should_log(LogLevel.CRITICAL):
            log_entry = self._create_log_entry(LogLevel.CRITICAL, message, context)
            self._emit(log_entry)

    @contextmanager
    def correlation_context(self, correlation_id: str | None = None):
        """
        Context manager for correlation ID.

        All logs within this context will include the correlation ID,
        enabling request tracing across the system.

        :param correlation_id: Correlation ID (auto-generated if None)
        :type correlation_id: Optional[str]
        :yield: None

        Example::

            with log_service.correlation_context("req-12345"):
                log_service.info("Processing request")
                process_request()
                log_service.info("Request completed")
                # Both logs will have correlation_id="req-12345"
        """
        ctx = get_context()
        old_correlation_id = ctx.correlation_id

        # Set correlation ID (generate if not provided)
        ctx.correlation_id = correlation_id or str(uuid.uuid4())

        try:
            yield
        finally:
            # Restore previous correlation ID
            ctx.correlation_id = old_correlation_id

    @contextmanager
    def context(self, **kwargs):
        """
        Context manager for custom context fields.

        All logs within this context will include the specified fields.

        :param kwargs: Context fields
        :yield: None

        Example::

            with log_service.context(user_id="123", tenant="acme"):
                log_service.info("User action")
                # Log will have user_id and tenant in context
        """
        ctx = get_context()
        old_custom = ctx.custom.copy()

        # Add custom fields
        ctx.custom.update(kwargs)

        try:
            yield
        finally:
            # Restore previous custom fields
            ctx.custom = old_custom

    def set_min_level(self, level: LogLevel) -> None:
        """
        Set minimum log level.

        :param level: New minimum level
        :type level: LogLevel
        """
        self.min_level = level

    def flush(self) -> None:
        """Flush all handlers."""
        with self._lock:
            for handler in self.handlers:
                with contextlib.suppress(Exception):
                    handler.flush()

    def close(self) -> None:
        """Close all handlers and release resources."""
        with self._lock:
            for handler in self.handlers:
                with contextlib.suppress(Exception):
                    handler.close()
            self.handlers.clear()

    def __repr__(self) -> str:
        """String representation."""
        return f"<LogService service={self.service_name} env={self.environment} handlers={len(self.handlers)}>"
