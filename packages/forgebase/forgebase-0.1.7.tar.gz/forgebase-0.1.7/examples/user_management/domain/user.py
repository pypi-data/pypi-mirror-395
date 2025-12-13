"""
User Entity for User Management Example.

Demonstrates a proper Entity implementation with business logic.

:author: ForgeBase Development Team
:since: 2025-11-03
"""

import uuid
from datetime import datetime

from examples.user_management.domain.email import Email
from forgebase.domain.entity_base import EntityBase
from forgebase.domain.exceptions import BusinessRuleViolation, ValidationError


class User(EntityBase):
    """
    User entity with email and name.

    Represents a user in the system. Demonstrates the Entity pattern:
    identity-based equality, business rules, and domain logic.

    Business Rules:
        - Name must not be empty
        - Email must be valid
        - User can be activated/deactivated
        - Deactivated users cannot be reactivated (business rule example)

    Example::

        # Create user
        user = User(
            id=str(uuid.uuid4()),
            name="John Doe",
            email=Email(address="john@example.com")
        )

        # Activate user
        user.activate()
        assert user.is_active

        # Business rule violation
        user.deactivate()
        try:
            user.activate()  # Cannot reactivate
        except BusinessRuleViolation:
            print("Cannot reactivate user")

    :ivar name: User's full name
    :vartype name: str
    :ivar email: User's email address
    :vartype email: Email
    :ivar is_active: Whether user is active
    :vartype is_active: bool
    :ivar created_at: When user was created
    :vartype created_at: datetime
    :ivar deactivated_at: When user was deactivated
    :vartype deactivated_at: Optional[datetime]
    """

    def __init__(
        self,
        id: str | None = None,
        name: str = "",
        email: Email | None = None
    ):
        """
        Initialize user entity.

        :param id: User identifier (auto-generated if not provided)
        :type id: Optional[str]
        :param name: User's full name
        :type name: str
        :param email: User's email address
        :type email: Optional[Email]
        """
        super().__init__(id=id or str(uuid.uuid4()))
        self.name = name
        self.email = email
        self.is_active = True
        self.created_at = datetime.utcnow()
        self.deactivated_at: datetime | None = None

    def validate(self) -> None:
        """
        Validate user entity.

        :raises ValidationError: If validation fails
        """
        if not self.name or not self.name.strip():
            raise ValidationError("User name cannot be empty")

        if self.email is None:
            raise ValidationError("User email is required")

        # Validate email value object
        self.email.validate()

    def activate(self) -> None:
        """
        Activate user account.

        :raises BusinessRuleViolation: If user was previously deactivated
        """
        if self.deactivated_at is not None:
            raise BusinessRuleViolation(
                f"Cannot reactivate user {self.id} that was deactivated at {self.deactivated_at.isoformat()}"
            )

        self.is_active = True

    def deactivate(self) -> None:
        """
        Deactivate user account.

        This is a one-way operation - users cannot be reactivated
        once deactivated (demonstrates a business rule).
        """
        self.is_active = False
        self.deactivated_at = datetime.utcnow()

    def change_email(self, new_email: Email) -> None:
        """
        Change user's email address.

        :param new_email: New email address
        :type new_email: Email
        :raises ValidationError: If email is invalid
        """
        new_email.validate()
        self.email = new_email

    def change_name(self, new_name: str) -> None:
        """
        Change user's name.

        :param new_name: New name
        :type new_name: str
        :raises ValidationError: If name is empty
        """
        if not new_name or not new_name.strip():
            raise ValidationError("Name cannot be empty")

        self.name = new_name.strip()

    def to_dict(self) -> dict:
        """
        Convert user to dictionary.

        Useful for serialization and API responses.

        :return: User data as dictionary
        :rtype: dict
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': str(self.email),
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'deactivated_at': self.deactivated_at.isoformat() if self.deactivated_at else None
        }

    def __repr__(self) -> str:
        """String representation of user."""
        return f"<User id={self.id} name='{self.name}' email={self.email}>"
