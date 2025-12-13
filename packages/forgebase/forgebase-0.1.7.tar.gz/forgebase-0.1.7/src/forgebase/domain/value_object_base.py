"""
Base class for value objects in ForgeBase.

Value objects are immutable objects defined by their attributes, not by identity.
Unlike entities, two value objects with the same attributes are considered equal.

Author: Jorge, The Forge
Created: 2025-11-03
"""

from abc import ABC, abstractmethod
from typing import Any


class ValueObjectBase(ABC):
    """
    Abstract base class for all value objects.

    Value objects are immutable objects without identity. They are defined
    solely by their attributes, and two value objects with identical attributes
    are considered equal.

    Design Decisions:
        - Immutability enforced via __setattr__: Prevents accidental modification
        - Structural equality: Based on all attributes, not identity
        - Hashable: Can be used in sets and as dict keys
        - Abstract validate(): Forces explicit validation logic

    :Example:

        class Email(ValueObjectBase):
            def __init__(self, address: str):
                self.address = address
                self._freeze()  # Enforce immutability

            def validate(self) -> None:
                if "@" not in self.address:
                    raise ValueError("Invalid email format")

        email1 = Email("test@example.com")
        email2 = Email("test@example.com")
        assert email1 == email2  # Same attributes = equal

    .. note::
        Call `_freeze()` at the end of __init__() to enforce immutability.

    .. seealso::
        :class:`EntityBase` - For objects with identity
    """

    def __init__(self) -> None:
        """Initialize the value object."""
        self._frozen = False

    def _freeze(self) -> None:
        """Freeze the object to prevent further modifications."""
        object.__setattr__(self, '_frozen', True)

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Prevent attribute modification after freezing.

        :param name: Attribute name
        :param value: Attribute value
        :raises AttributeError: If object is frozen
        """
        if hasattr(self, '_frozen') and self._frozen:
            raise AttributeError(f"Cannot modify immutable {self.__class__.__name__}")
        object.__setattr__(self, name, value)

    @abstractmethod
    def validate(self) -> None:
        """
        Validate the value object's constraints.

        :raises ValidationError: When validation fails
        """
        pass

    def to_dict(self) -> dict[str, Any]:
        """
        Convert value object to dictionary.

        :return: Dictionary representation
        :rtype: Dict[str, Any]
        """
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

    def __eq__(self, other: Any) -> bool:
        """
        Structural equality based on all attributes.

        :param other: Object to compare
        :return: True if all attributes match
        """
        if not isinstance(other, self.__class__):
            return False
        return self.to_dict() == other.to_dict()

    def __hash__(self) -> int:
        """
        Hash based on all attribute values.

        :return: Hash value
        """
        items = tuple(sorted(self.to_dict().items()))
        return hash(items)

    def __repr__(self) -> str:
        """
        String representation.

        :return: Representation string
        """
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.to_dict().items())
        return f"{self.__class__.__name__}({attrs})"
