"""
Email ValueObject for User Management Example.

Demonstrates a proper ValueObject implementation with validation.

:author: ForgeBase Development Team
:since: 2025-11-03
"""

import re

from forgebase.domain.exceptions import ValidationError
from forgebase.domain.value_object_base import ValueObjectBase


class Email(ValueObjectBase):
    """
    Email address value object.

    Represents an immutable email address with validation.
    This demonstrates the ValueObject pattern: immutable, validated,
    and compared by value rather than identity.

    Example::

        # Valid email
        email = Email(address="user@example.com")
        print(email.address)  # user@example.com

        # Invalid email raises ValidationError
        try:
            invalid = Email(address="not-an-email")
        except ValidationError as e:
            print(f"Invalid: {e}")

        # Equality based on value
        email1 = Email(address="test@example.com")
        email2 = Email(address="test@example.com")
        assert email1 == email2

    :ivar address: Email address string
    :vartype address: str
    """

    def __init__(self, address: str):
        """
        Initialize email value object.

        :param address: Email address
        :type address: str
        :raises ValidationError: If email is invalid
        """
        super().__init__()
        self.address = address
        self.validate()
        self._freeze()

    def validate(self) -> None:
        """
        Validate email format.

        :raises ValidationError: If email format is invalid
        """
        address = self.address

        if not address:
            raise ValidationError("Email address cannot be empty")

        # Basic email validation pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, address):
            raise ValidationError(f"Invalid email format: {address}")

        # Additional validation: length check
        if len(address) > 254:  # RFC 5321
            raise ValidationError(
                f"Email address too long (max 254 characters): {len(address)} chars"
            )

    @property
    def domain(self) -> str:
        """
        Get email domain.

        :return: Domain part of email
        :rtype: str
        """
        return self.address.split('@')[1]

    @property
    def local_part(self) -> str:
        """
        Get local part of email.

        :return: Local part (before @)
        :rtype: str
        """
        return self.address.split('@')[0]

    def __str__(self) -> str:
        """String representation of email."""
        return self.address
