"""
Base class for Data Transfer Objects in ForgeBase.

DTOs transfer data between layers (e.g., from adapter to use case).
They provide validation and serialization capabilities.

Author: Jorge, The Forge
Created: 2025-11-03
"""

from abc import ABC, abstractmethod
from typing import Any, TypeVar

T = TypeVar('T', bound='DTOBase')


class DTOBase(ABC):
    """
    Abstract base class for all Data Transfer Objects.

    DTOs are simple data containers that transfer information between
    architectural layers. They provide validation and serialization.

    Design Decisions:
        - Explicit validate() method for clear validation timing
        - to_dict()/from_dict() for serialization
        - No business logic - purely data transfer

    :Example:

        class CreateUserDTO(DTOBase):
            def __init__(self, email: str, name: str):
                self.email = email
                self.name = name

            def validate(self) -> None:
                if not self.email or "@" not in self.email:
                    raise ValidationError("Invalid email")
                if not self.name:
                    raise ValidationError("Name is required")

            def to_dict(self) -> dict:
                return {"email": self.email, "name": self.name}

            @classmethod
            def from_dict(cls, data: dict) -> "CreateUserDTO":
                return cls(data["email"], data["name"])

    .. note::
        DTOs are mutable (unlike value objects) for ease of construction.
    """

    @abstractmethod
    def validate(self) -> None:
        """
        Validate the DTO's data.

        Should raise ValidationError when data is invalid.

        :raises ValidationError: When validation fails

        :Example:

            def validate(self) -> None:
                errors = []
                if not self.email:
                    errors.append("Email is required")
                if self.age < 0:
                    errors.append("Age must be positive")
                if errors:
                    raise ValidationError("; ".join(errors))
        """
        pass

    def to_dict(self) -> dict[str, Any]:
        """
        Convert DTO to dictionary.

        Default implementation returns all public attributes.
        Override for custom serialization.

        :return: Dictionary representation
        :rtype: Dict[str, Any]
        """
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

    @classmethod
    def from_dict(cls: type[T], data: dict[str, Any]) -> T:
        """
        Create DTO from dictionary.

        Default implementation passes dict as kwargs to constructor.
        Override for custom deserialization.

        :param data: Dictionary data
        :type data: Dict[str, Any]
        :return: DTO instance
        :rtype: T

        :Example:

            data = {"email": "test@example.com", "name": "Test"}
            dto = CreateUserDTO.from_dict(data)
        """
        return cls(**data)
