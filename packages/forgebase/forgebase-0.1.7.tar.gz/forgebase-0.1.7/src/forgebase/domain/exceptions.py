"""
Domain-specific exceptions for ForgeBase.

This module defines the exception hierarchy for domain layer errors.
All domain exceptions inherit from DomainException for easy catching.

Author: Jorge, The Forge
Created: 2025-11-03
"""


class DomainException(Exception):  # noqa: N818
    """
    Base exception for all domain-level errors.

    Use this as base for all domain-specific exceptions to maintain
    clear separation between domain and infrastructure errors.

    :Example:

        try:
            user.validate()
        except DomainException as e:
            # Handle all domain errors
            logger.error(f"Domain error: {e}")
    """
    pass


class ValidationError(DomainException):
    """
    Raised when entity or value object validation fails.

    Use this when data doesn't meet format or type requirements.

    :Example:

        if not email_address or "@" not in email_address:
            raise ValidationError("Email must contain @")
    """
    pass


class InvariantViolation(DomainException):
    """
    Raised when a business rule (invariant) is violated.

    Use this for business logic violations, not just data format issues.

    :Example:

        if order.total < 0:
            raise InvariantViolation("Order total cannot be negative")
    """
    pass


class BusinessRuleViolation(DomainException):
    """
    Raised when a business rule prevents an operation.

    Use this for domain rules that prevent specific operations.

    :Example:

        if not user.is_active:
            raise BusinessRuleViolation("Cannot place order: user inactive")
    """
    pass


class EntityNotFoundError(DomainException):
    """
    Raised when an expected entity doesn't exist.

    :Example:

        user = repository.find_by_id(user_id)
        if not user:
            raise EntityNotFoundError(f"User {user_id} not found")
    """
    pass


class DuplicateEntityError(DomainException):
    """
    Raised when attempting to create a duplicate entity.

    :Example:

        if repository.find_by_email(email):
            raise DuplicateEntityError(f"User with email {email} already exists")
    """
    pass
