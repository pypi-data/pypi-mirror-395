"""
Logging Port Interface for ForgeBase.

This module defines the abstract interface for logging in ForgeBase. By defining
logging as a Port, we enable multiple implementations (stdout, file, remote services)
while keeping the application layer independent of specific logging libraries.

Philosophy:
    Logging is not just about writing text to files. It's about structured data
    collection that enables observability, debugging, and understanding system behavior.
    Good logging supports both human readers and machine parsing, includes context,
    and follows consistent levels of severity.

    This Port supports structured logging with context propagation, allowing rich
    metadata to be attached to log messages. This enables powerful filtering, search,
    and aggregation in production systems.

Logging Levels (from lowest to highest severity):
    - DEBUG: Detailed diagnostic information, typically only enabled during development
    - INFO: General informational messages about system operation
    - WARNING: Indication that something unexpected happened, but system continues
    - ERROR: Serious problem that caused a specific operation to fail
    - CRITICAL: Very serious error that may prevent the system from continuing

Example::

    # Using a concrete implementation
    logger = StdoutLogger(level=LogLevel.INFO)

    # Basic logging
    logger.info("Application started")

    # Structured logging with context
    logger.info("User logged in", user_id="12345", ip="192.168.1.1")

    # Error logging with context
    try:
        risky_operation()
    except Exception as e:
        logger.error("Operation failed", error=str(e), operation="risky_operation")

:author: ForgeBase Development Team
:since: 2025-11-03
"""

import json
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, TextIO


class LogLevel(Enum):
    """
    Log level enumeration.

    Defines the severity levels for log messages in ascending order of importance.
    """

    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

    def __lt__(self, other):
        """Compare log levels by severity."""
        if isinstance(other, LogLevel):
            return self.value < other.value
        return NotImplemented

    def __le__(self, other):
        """Compare log levels by severity (less than or equal)."""
        if isinstance(other, LogLevel):
            return self.value <= other.value
        return NotImplemented

    def __gt__(self, other):
        """Compare log levels by severity (greater than)."""
        if isinstance(other, LogLevel):
            return self.value > other.value
        return NotImplemented

    def __ge__(self, other):
        """Compare log levels by severity (greater than or equal)."""
        if isinstance(other, LogLevel):
            return self.value >= other.value
        return NotImplemented


class LoggerPort(ABC):
    """
    Abstract interface for logging implementations.

    This Port defines the contract that all logger implementations must follow.
    By programming against this interface rather than concrete implementations,
    we enable flexibility in logging backends without changing application code.

    All methods accept a message string plus optional context keyword arguments.
    Context is structured data that provides additional information about the
    log event. This enables powerful filtering and aggregation in log analysis tools.

    Implementations should:
        - Format messages consistently
        - Include timestamps
        - Preserve context information
        - Handle errors gracefully
        - Be thread-safe

    Example Implementation::

        class FileLogger(LoggerPort):
            def __init__(self, file_path: str):
                self.file = open(file_path, 'a')

            def info(self, message: str, **context) -> None:
                timestamp = datetime.utcnow().isoformat()
                log_entry = {
                    'timestamp': timestamp,
                    'level': 'INFO',
                    'message': message,
                    'context': context
                }
                self.file.write(json.dumps(log_entry) + '\\n')
                self.file.flush()

            # ... other methods
    """

    @abstractmethod
    def debug(self, message: str, **context: Any) -> None:
        """
        Log a debug message.

        Debug messages provide detailed diagnostic information useful during
        development and troubleshooting. They are typically disabled in production.

        :param message: Human-readable log message
        :type message: str
        :param context: Additional structured context data
        :type context: Any

        Example::

            logger.debug("Database query executed", query="SELECT * FROM users", duration_ms=45)
        """
        pass

    @abstractmethod
    def info(self, message: str, **context: Any) -> None:
        """
        Log an informational message.

        Info messages document normal system operation and significant events.
        They provide a high-level view of what the system is doing.

        :param message: Human-readable log message
        :type message: str
        :param context: Additional structured context data
        :type context: Any

        Example::

            logger.info("User login successful", user_id="12345", ip="192.168.1.1")
        """
        pass

    @abstractmethod
    def warning(self, message: str, **context: Any) -> None:
        """
        Log a warning message.

        Warnings indicate that something unexpected happened or might cause
        problems in the future, but the system continues to operate normally.

        :param message: Human-readable log message
        :type message: str
        :param context: Additional structured context data
        :type context: Any

        Example::

            logger.warning("API rate limit approaching", current_usage=950, limit=1000)
        """
        pass

    @abstractmethod
    def error(self, message: str, **context: Any) -> None:
        """
        Log an error message.

        Errors indicate that a specific operation failed due to a problem.
        The system continues to run, but the operation could not be completed.

        :param message: Human-readable log message
        :type message: str
        :param context: Additional structured context data
        :type context: Any

        Example::

            logger.error("Failed to save user data", user_id="12345", error="Database connection timeout")
        """
        pass

    @abstractmethod
    def critical(self, message: str, **context: Any) -> None:
        """
        Log a critical message.

        Critical messages indicate serious errors that may prevent the system
        from continuing to operate. These require immediate attention.

        :param message: Human-readable log message
        :type message: str
        :param context: Additional structured context data
        :type context: Any

        Example::

            logger.critical("Database connection lost", retry_attempts=3, last_error="Connection refused")
        """
        pass


class StdoutLogger(LoggerPort):
    """
    Simple logger implementation that writes to stdout.

    This is a reference implementation of LoggerPort that demonstrates the expected
    behavior. It writes structured JSON logs to stdout, making it suitable for
    containerized environments where logs are collected from standard output.

    Features:
        - Structured JSON output
        - Configurable minimum log level
        - ISO 8601 timestamps
        - Context preservation
        - Thread-safe (uses stdout which is thread-safe in Python)

    Example::

        # Create logger with INFO level (debug messages will be ignored)
        logger = StdoutLogger(level=LogLevel.INFO)

        # Log some messages
        logger.info("Application started", version="1.0.0")
        logger.debug("This won't appear")  # Below configured level
        logger.error("Something failed", error="Network timeout")

    :ivar level: Minimum log level to output
    :vartype level: LogLevel
    :ivar output: Output stream for log messages
    :vartype output: TextIO
    """

    def __init__(self, level: LogLevel = LogLevel.INFO, output: TextIO = sys.stdout):
        """
        Initialize stdout logger.

        :param level: Minimum log level to output
        :type level: LogLevel
        :param output: Output stream (default: sys.stdout)
        :type output: TextIO
        """
        self.level = level
        self.output = output

    def _should_log(self, level: LogLevel) -> bool:
        """Check if message at given level should be logged."""
        return level >= self.level

    def _format_log(self, level: LogLevel, message: str, context: dict[str, Any]) -> str:
        """
        Format log entry as JSON.

        :param level: Log level
        :type level: LogLevel
        :param message: Log message
        :type message: str
        :param context: Context data
        :type context: Dict[str, Any]
        :return: Formatted JSON string
        :rtype: str
        """
        log_entry = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': level.name,
            'message': message
        }

        # Add context if present
        if context:
            log_entry['context'] = context

        return json.dumps(log_entry, default=str)

    def _write_log(self, level: LogLevel, message: str, context: dict[str, Any]) -> None:
        """
        Write log entry to output stream.

        :param level: Log level
        :type level: LogLevel
        :param message: Log message
        :type message: str
        :param context: Context data
        :type context: Dict[str, Any]
        """
        if self._should_log(level):
            formatted = self._format_log(level, message, context)
            self.output.write(formatted + '\n')
            self.output.flush()

    def debug(self, message: str, **context: Any) -> None:
        """Log debug message to stdout."""
        self._write_log(LogLevel.DEBUG, message, context)

    def info(self, message: str, **context: Any) -> None:
        """Log info message to stdout."""
        self._write_log(LogLevel.INFO, message, context)

    def warning(self, message: str, **context: Any) -> None:
        """Log warning message to stdout."""
        self._write_log(LogLevel.WARNING, message, context)

    def error(self, message: str, **context: Any) -> None:
        """Log error message to stdout."""
        self._write_log(LogLevel.ERROR, message, context)

    def critical(self, message: str, **context: Any) -> None:
        """Log critical message to stdout."""
        self._write_log(LogLevel.CRITICAL, message, context)

    def set_level(self, level: LogLevel) -> None:
        """
        Change the minimum log level.

        :param level: New minimum log level
        :type level: LogLevel

        Example::

            logger = StdoutLogger(level=LogLevel.INFO)
            logger.set_level(LogLevel.DEBUG)  # Now debug messages will appear
        """
        self.level = level

    def __repr__(self) -> str:
        """String representation of logger."""
        return f"<StdoutLogger level={self.level.name}>"


class NoOpLogger(LoggerPort):
    """
    No-operation logger that discards all log messages.

    Useful for testing or when logging should be completely disabled.
    This implements the Null Object pattern for logging.

    Example::

        # In tests where logging is noise
        logger = NoOpLogger()
        logger.info("This message is discarded")
        logger.error("This too")
    """

    def debug(self, message: str, **context: Any) -> None:
        """Discard debug message."""
        pass

    def info(self, message: str, **context: Any) -> None:
        """Discard info message."""
        pass

    def warning(self, message: str, **context: Any) -> None:
        """Discard warning message."""
        pass

    def error(self, message: str, **context: Any) -> None:
        """Discard error message."""
        pass

    def critical(self, message: str, **context: Any) -> None:
        """Discard critical message."""
        pass

    def __repr__(self) -> str:
        """String representation of no-op logger."""
        return "<NoOpLogger>"
