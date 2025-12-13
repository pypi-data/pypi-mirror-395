"""
Error handling utilities for the application layer.

Provides standardized error handling, guards, and error context propagation.

Author: Jorge, The Forge
Created: 2025-11-03
"""

from collections.abc import Callable
from functools import wraps
from typing import Any

from forgebase.domain.exceptions import DomainException


class ApplicationError(Exception):
    """
    Base exception for application layer errors.

    Use this for errors that occur during use case execution,
    distinct from domain or infrastructure errors.
    """
    pass


class UseCaseExecutionError(ApplicationError):
    """Raised when use case execution fails."""
    pass


class InvalidInputError(ApplicationError):
    """Raised when use case receives invalid input."""
    pass


def handle_domain_errors(domain_exception: type[DomainException],
                        application_exception: type[ApplicationError]) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to convert domain exceptions to application exceptions.

    Useful for maintaining layer boundaries - catch domain errors and
    re-raise as application errors with additional context.

    :param domain_exception: Domain exception type to catch
    :param application_exception: Application exception type to raise
    :return: Decorator function

    :Example:

        @handle_domain_errors(ValidationError, InvalidInputError)
        def execute(self, dto):
            entity = Entity(dto.value)
            entity.validate()  # May raise ValidationError
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except domain_exception as e:
                raise application_exception(str(e)) from e
        return wrapper
    return decorator


def guard_not_none(value: Any | None, error_message: str) -> Any:
    """
    Guard that ensures value is not None.

    :param value: Value to check
    :param error_message: Error message if None
    :return: The value if not None
    :raises ApplicationError: If value is None

    :Example:

        user = repository.find_by_id(user_id)
        user = guard_not_none(user, f"User {user_id} not found")
    """
    if value is None:
        raise ApplicationError(error_message)
    return value


def guard_condition(condition: bool, error_message: str) -> None:
    """
    Guard that ensures a condition is True.

    :param condition: Condition to check
    :param error_message: Error message if False
    :raises ApplicationError: If condition is False

    :Example:

        guard_condition(
            user.is_active,
            "Cannot perform operation: user is inactive"
        )
    """
    if not condition:
        raise ApplicationError(error_message)
