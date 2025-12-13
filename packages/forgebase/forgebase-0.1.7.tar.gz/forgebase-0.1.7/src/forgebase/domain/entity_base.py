"""
Base class for all domain entities in ForgeBase.

This module provides EntityBase, the foundational abstract class for all
domain entities following Domain-Driven Design principles. Entities are
objects with unique identity that persists through state changes.

An entity is defined by its ID, not by its attributes. Two entities with
the same ID are considered equal, even if their attributes differ.

This implementation enforces Clean Architecture by keeping the domain layer
completely independent of infrastructure concerns. Entities know nothing
about databases, HTTP, or any external systems.

Philosophy:
    The decision to use an abstract base class (instead of protocols or duck
    typing) enforces explicit contracts and enables validation at development
    time. This reflects ForgeBase's Autonomy principle: modules with clearly
    defined contracts.

Example::

    from forgebase.domain import EntityBase

    class User(EntityBase):
        def __init__(self, id: str, name: str, email: str):
            super().__init__(id)
            self.name = name
            self.email = email

        def validate(self) -> None:
            if not self.name:
                raise ValueError("User name cannot be empty")
            if "@" not in self.email:
                raise ValueError("Invalid email format")

    # Usage
    user = User(None, "Alice", "alice@example.com")
    user.validate()  # OK
    print(user.id)  # Auto-generated UUID

Author: Jorge, The Forge
Created: 2025-11-03
"""

import uuid
from abc import ABC, abstractmethod
from typing import Any


class EntityBase(ABC):
    """
    Abstract base class for all domain entities.

    This class implements the identity pattern for entities according to
    Domain-Driven Design. Each entity has a unique ID that defines its
    identity, independent of other attributes.

    The decision to use an abstract base class enforces explicit contracts
    and facilitates validation at development time. This reflects the
    Autonomy principle of ForgeBase: modules with well-defined contracts.

    Design Decisions:
        - UUID4 for IDs: Ensures global uniqueness without central coordination,
          aligned with the Autonomy principle
        - Lazy ID generation: ID can be provided or auto-generated, supporting
          both new entities and reconstitution from persistence
        - Abstract validate(): Forces subclasses to explicitly define their
          invariants, making business rules visible and enforceable

    :ivar id: Unique identifier of the entity
    :vartype id: str

    Example::

        class Product(EntityBase):
            def __init__(self, id: Optional[str], name: str, price: float):
                super().__init__(id)
                self.name = name
                self.price = price

            def validate(self) -> None:
                if not self.name:
                    raise ValueError("Product name is required")
                if self.price < 0:
                    raise ValueError("Price cannot be negative")

        # New entity with auto-generated ID
        product = Product(None, "Laptop", 1500.00)
        print(product.id)  # e.g., "a1b2c3d4-..."

        # Reconstituted entity with existing ID
        existing = Product("product-123", "Mouse", 25.00)

    Note::

        Subclasses MUST implement the validate() method to enforce their
        specific invariants. Validation should raise appropriate exceptions
        (preferably from domain.exceptions module) when rules are violated.

    Warning::

        Do not use EntityBase for objects without their own identity. For
        those cases, use ValueObjectBase instead.

    See Also::

        :class:`ValueObjectBase` : Base for objects without identity
        :mod:`domain.exceptions` : Domain-specific exceptions
        :class:`UseCaseBase` : Orchestration using entities
    """

    def __init__(self, id: str | None = None):
        """
        Initialize the entity with a unique ID.

        If no ID is provided, a UUID4 is automatically generated. The choice
        of UUID4 ensures global uniqueness without central coordination,
        aligned with ForgeBase's Autonomy principle.

        Design rationale:
            - Optional ID supports both new entity creation and reconstitution
              from persistence
            - UUID4 (not UUID1) avoids leaking machine/time information
            - String ID (not UUID object) for better serialization compatibility

        :param id: Unique identifier for the entity (optional, auto-generated if None)
        :type id: Optional[str]

        Example::

            # New entity - ID auto-generated
            entity1 = EntityBase(None)
            print(entity1.id)  # "f47ac10b-58cc-4372-a567-0e02b2c3d479"

            # Reconstituted entity - ID provided
            entity2 = EntityBase("existing-id-123")
            print(entity2.id)  # "existing-id-123"

        Note::

            ID generation happens at construction time, not lazily. This ensures
            the entity always has a valid ID from the moment it's created.
        """
        self._id: str = id or str(uuid.uuid4())

    @property
    def id(self) -> str:
        """
        Get entity ID (read-only).

        The ID is immutable after entity creation to maintain identity integrity.
        This prevents entities from breaking when used in sets or as dict keys.

        :return: Entity identifier
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        """
        Prevent ID modification after entity creation.

        Entity identity must remain stable throughout the entity's lifetime.
        Attempting to change the ID will raise an AttributeError.

        :param value: Attempted new ID value
        :raises AttributeError: Always - ID is immutable
        """
        raise AttributeError(
            "Entity ID is immutable and cannot be changed after creation. "
            "Entity identity must remain stable to ensure correct behavior "
            "in sets, dictionaries, and equality comparisons."
        )

    @abstractmethod
    def validate(self) -> None:
        """
        Validate the entity's invariants.

        This abstract method must be implemented by all subclasses to enforce
        their specific business rules. Validation should raise exceptions when
        invariants are violated.

        Design rationale:
            The decision to use an explicit method (instead of automatic
            validation in __init__) provides fine-grained control over when
            validation occurs. This is useful in scenarios like:
            - Reconstituting entities from database (already validated)
            - Gradual entity construction in builders
            - Performance optimization in bulk operations

        :raises InvariantViolation: When a business rule is violated
        :raises ValidationError: When data is invalid

        Example::

            class Order(EntityBase):
                def __init__(self, id, items, total):
                    super().__init__(id)
                    self.items = items
                    self.total = total

                def validate(self) -> None:
                    if not self.items:
                        raise ValueError("Order must have at least one item")
                    if self.total < 0:
                        raise ValueError("Total cannot be negative")
                    if sum(item.price for item in self.items) != self.total:
                        raise ValueError("Total doesn't match items sum")

            # Usage
            order = Order(None, [item1, item2], 100.00)
            order.validate()  # Will raise if invariants violated

        Note::

            Consider calling validate() at the end of __init__() if you want
            "fail-fast" behavior, or call it explicitly before persistence.

        See Also::

            :mod:`domain.validators` : Reusable validation functions
            :mod:`domain.exceptions` : Domain-specific exceptions
        """
        pass

    def __eq__(self, other: Any) -> bool:
        """
        Compare entities by identity (ID), not by attributes.

        Two entities are considered equal if they have the same ID, regardless
        of their other attributes. This is the fundamental principle of entity
        equality in Domain-Driven Design.

        Design rationale:
            - ID-based equality ensures entities maintain identity through state
              changes
            - Type check prevents false positives with non-entity objects
            - Supports polymorphism (subclass entities can be compared)

        :param other: Object to compare with
        :type other: Any
        :return: True if both entities have the same ID, False otherwise
        :rtype: bool

        Example::

            user1 = User("user-123", "Alice", "alice@example.com")
            user2 = User("user-123", "Alice Smith", "alice.smith@example.com")
            user3 = User("user-456", "Alice", "alice@example.com")

            print(user1 == user2)  # True (same ID)
            print(user1 == user3)  # False (different ID)
            print(user1 == "user-123")  # False (not an entity)

        Note::

            This is identity equality, not structural equality. For comparing
            entity attributes, implement custom comparison methods.
        """
        if not isinstance(other, EntityBase):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        """
        Generate hash based on entity ID.

        Allows entities to be used in sets and as dictionary keys. The hash
        is based solely on ID, maintaining consistency with __eq__.

        Design rationale:
            - Hash based on ID ensures hash stability even when attributes change
            - Consistent with __eq__ implementation (objects that compare equal
              must have the same hash)
            - Enables using entities in sets and dict keys

        :return: Hash value based on entity ID
        :rtype: int

        Example::

            users = {
                User("user-1", "Alice", "alice@example.com"),
                User("user-2", "Bob", "bob@example.com"),
                User("user-1", "Alice Updated", "new@example.com")  # Won't be added
            }
            print(len(users))  # 2 (user-1 considered duplicate)

            user_index = {
                user1: "Active",
                user2: "Inactive"
            }

        Warning::

            Entities used as dict keys or in sets should not have their ID
            modified after insertion. Doing so will break the collection.

        Note::

            The hash is computed from the string ID, which is immutable.
            This ensures hash stability.
        """
        return hash(self._id)

    def __repr__(self) -> str:
        """
        Return developer-friendly string representation of the entity.

        Provides a clear representation showing the entity's class name and ID,
        useful for debugging and logging.

        :return: String representation in format ClassName(id='...')
        :rtype: str

        Example::

            user = User("user-123", "Alice", "alice@example.com")
            print(repr(user))  # "User(id='user-123')"

            print(f"Processing {user!r}")  # Uses __repr__
        """
        return f"{self.__class__.__name__}(id='{self.id}')"

    def __str__(self) -> str:
        """
        Return user-friendly string representation of the entity.

        By default, returns the same as __repr__. Subclasses can override
        to provide more meaningful string representations.

        :return: String representation of the entity
        :rtype: str

        Example::

            user = User("user-123", "Alice", "alice@example.com")
            print(str(user))  # "User(id='user-123')"
            print(user)       # Same as str(user)

        Note::

            Override this method in subclasses to provide domain-specific
            string representations.
        """
        return self.__repr__()
