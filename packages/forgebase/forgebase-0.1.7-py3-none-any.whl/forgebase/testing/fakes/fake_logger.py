"""
In-memory logger for testing.

Provides a fake logger implementation that stores log entries in memory
for inspection during tests. Implements LoggerPort interface for drop-in
replacement of real loggers.

Philosophy:
    Tests shouldn't produce log spam, but they should verify that important
    events are being logged. FakeLogger enables this by capturing logs
    in memory, allowing assertions about what was logged without cluttering
    test output.

    Benefits:
    1. Zero overhead - no I/O during tests
    2. Inspectable - query logs programmatically
    3. Thread-safe - works with concurrent tests
    4. Drop-in replacement - implements LoggerPort

Use Cases:
    - Verifying error logging in failure scenarios
    - Checking audit trail creation
    - Testing log context propagation
    - Validating log levels in different conditions

Example::

    from forgebase.testing.fakes.fake_logger import FakeLogger

    def test_user_creation_logs_event():
        # Setup
        logger = FakeLogger()
        usecase = CreateUserUseCase(logger=logger)

        # Execute
        user = usecase.execute({"email": "test@example.com"})

        # Verify logging
        assert logger.has_logged("User created", level="INFO")
        assert logger.get_log_count(level="ERROR") == 0

        # Inspect details
        logs = logger.get_logs(level="INFO")
        assert logs[0]['message'] == "User created"
        assert logs[0]['context']['user_id'] == user.id

:author: ForgeBase Development Team
:since: 2025-11-03
"""

import threading
from typing import Any

from forgebase.infrastructure.logging.logger_port import LoggerPort, LogLevel


class FakeLogger(LoggerPort):
    """
    In-memory logger for testing.

    Implements LoggerPort by storing all log entries in memory.
    Provides inspection methods for test assertions.

    Thread-safe implementation allows use in concurrent test scenarios.

    Features:
        - Captures all log levels
        - Stores full context
        - Queryable by level, message, context
        - Resettable between tests
        - No I/O overhead

    :ivar _logs: List of captured log entries
    :vartype _logs: List[Dict[str, Any]]
    :ivar _lock: Thread lock for concurrent access
    :vartype _lock: threading.Lock

    Example::

        logger = FakeLogger()

        # Log some events
        logger.info("User logged in", user_id="123")
        logger.error("Payment failed", amount=100.0, reason="insufficient funds")

        # Query logs
        assert logger.has_logged("User logged in")
        assert logger.get_log_count(level="ERROR") == 1

        # Inspect details
        error_logs = logger.get_logs(level="ERROR")
        assert error_logs[0]['context']['amount'] == 100.0

        # Reset for next test
        logger.clear()
    """

    def __init__(self):
        """Initialize empty in-memory log storage."""
        self._logs: list[dict[str, Any]] = []
        self._lock = threading.Lock()

    def debug(self, message: str, **context: Any) -> None:
        """
        Log debug message.

        :param message: Log message
        :type message: str
        :param context: Additional context
        :type context: Any
        """
        self._log(LogLevel.DEBUG, message, context)

    def info(self, message: str, **context: Any) -> None:
        """
        Log info message.

        :param message: Log message
        :type message: str
        :param context: Additional context
        :type context: Any
        """
        self._log(LogLevel.INFO, message, context)

    def warning(self, message: str, **context: Any) -> None:
        """
        Log warning message.

        :param message: Log message
        :type message: str
        :param context: Additional context
        :type context: Any
        """
        self._log(LogLevel.WARNING, message, context)

    def error(self, message: str, **context: Any) -> None:
        """
        Log error message.

        :param message: Log message
        :type message: str
        :param context: Additional context
        :type context: Any
        """
        self._log(LogLevel.ERROR, message, context)

    def critical(self, message: str, **context: Any) -> None:
        """
        Log critical message.

        :param message: Log message
        :type message: str
        :param context: Additional context
        :type context: Any
        """
        self._log(LogLevel.CRITICAL, message, context)

    def _log(self, level: LogLevel, message: str, context: dict[str, Any]) -> None:
        """
        Internal logging method that stores entry.

        :param level: Log level
        :type level: LogLevel
        :param message: Log message
        :type message: str
        :param context: Log context
        :type context: Dict[str, Any]
        """
        entry = {
            'level': level,
            'message': message,
            'context': context
        }

        with self._lock:
            self._logs.append(entry)

    def get_logs(
        self,
        level: str | LogLevel | None = None,
        message_contains: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get captured log entries, optionally filtered.

        :param level: Filter by log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        :type level: Optional[Union[str, LogLevel]]
        :param message_contains: Filter by message substring
        :type message_contains: Optional[str]
        :return: List of matching log entries
        :rtype: List[Dict[str, Any]]

        Example::

            # Get all logs
            all_logs = logger.get_logs()

            # Get only errors
            errors = logger.get_logs(level="ERROR")
            errors = logger.get_logs(level=LogLevel.ERROR)  # or use enum

            # Search by message
            auth_logs = logger.get_logs(message_contains="authentication")

            # Combine filters
            auth_errors = logger.get_logs(
                level="ERROR",
                message_contains="authentication"
            )
        """
        with self._lock:
            logs = self._logs.copy()

        # Filter by level
        if level:
            if isinstance(level, str):
                level = LogLevel[level.upper()]
            logs = [log for log in logs if log['level'] == level]

        # Filter by message
        if message_contains:
            logs = [
                log for log in logs
                if message_contains.lower() in log['message'].lower()
            ]

        return logs

    def has_logged(
        self,
        message: str,
        level: str | LogLevel | None = None,
        **context_match: Any
    ) -> bool:
        """
        Check if a specific message was logged.

        :param message: Message to search for (substring match)
        :type message: str
        :param level: Optional level filter
        :type level: Optional[Union[str, LogLevel]]
        :param context_match: Optional context values to match
        :type context_match: Any
        :return: True if message was logged
        :rtype: bool

        Example::

            # Simple message check
            assert logger.has_logged("User created")

            # Check with level
            assert logger.has_logged("Payment failed", level="ERROR")

            # Check with context
            assert logger.has_logged(
                "User action",
                user_id="123",
                action="login"
            )
        """
        logs = self.get_logs(level=level, message_contains=message)

        # If no context match required, return if any logs found
        if not context_match:
            return len(logs) > 0

        # Check context match
        for log in logs:
            log_context = log['context']
            if all(
                key in log_context and log_context[key] == value
                for key, value in context_match.items()
            ):
                return True

        return False

    def get_log_count(self, level: str | LogLevel | None = None) -> int:
        """
        Get count of log entries.

        :param level: Optional level filter
        :type level: Optional[Union[str, LogLevel]]
        :return: Number of log entries
        :rtype: int

        Example::

            # Total logs
            total = logger.get_log_count()

            # Errors only
            error_count = logger.get_log_count(level="ERROR")

            # Assert no errors
            assert logger.get_log_count(level="ERROR") == 0
        """
        return len(self.get_logs(level=level))

    def assert_logged(
        self,
        message: str,
        level: str | LogLevel | None = None,
        **context_match: Any
    ) -> None:
        """
        Assert that a message was logged (raises if not).

        Convenience method for test assertions.

        :param message: Message to check for
        :type message: str
        :param level: Optional level filter
        :type level: Optional[Union[str, LogLevel]]
        :param context_match: Optional context values to match
        :type context_match: Any
        :raises AssertionError: If message wasn't logged

        Example::

            # Will pass
            logger.info("User created")
            logger.assert_logged("User created")

            # Will fail
            logger.assert_logged("User deleted")  # AssertionError
        """
        if not self.has_logged(message, level=level, **context_match):
            level_str = f" at {level} level" if level else ""
            context_str = f" with context {context_match}" if context_match else ""

            msg = f"Message '{message}'{level_str}{context_str} was not logged"
            raise AssertionError(msg)

    def assert_not_logged(
        self,
        message: str,
        level: str | LogLevel | None = None
    ) -> None:
        """
        Assert that a message was NOT logged (raises if it was).

        :param message: Message to check for absence
        :type message: str
        :param level: Optional level filter
        :type level: Optional[Union[str, LogLevel]]
        :raises AssertionError: If message was logged

        Example::

            # Ensure sensitive data not logged
            logger.assert_not_logged("password")
            logger.assert_not_logged("credit card", level="ERROR")
        """
        if self.has_logged(message, level=level):
            level_str = f" at {level} level" if level else ""
            msg = f"Message '{message}'{level_str} was logged but shouldn't be"
            raise AssertionError(msg)

    def clear(self) -> None:
        """
        Clear all captured logs.

        Useful for resetting between tests or test sections.

        Example::

            def setUp(self):
                self.logger = FakeLogger()

            def tearDown(self):
                self.logger.clear()

            def test_something(self):
                # Test code
                pass
                # Logs automatically cleared in tearDown
        """
        with self._lock:
            self._logs.clear()

    def get_last_log(
        self,
        level: str | LogLevel | None = None
    ) -> dict[str, Any] | None:
        """
        Get the most recent log entry.

        :param level: Optional level filter
        :type level: Optional[Union[str, LogLevel]]
        :return: Last log entry or None
        :rtype: Optional[Dict[str, Any]]

        Example::

            logger.info("First message")
            logger.error("Last message")

            last = logger.get_last_log()
            assert last['message'] == "Last message"

            last_error = logger.get_last_log(level="ERROR")
            assert last_error['message'] == "Last message"
        """
        logs = self.get_logs(level=level)
        return logs[-1] if logs else None

    def __repr__(self) -> str:
        """String representation."""
        return f"<FakeLogger logs={len(self._logs)}>"
