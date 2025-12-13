"""
Base class for repository pattern implementation.

Provides abstract interface for entity persistence following
Repository Pattern from Domain-Driven Design.

Author: Jorge, The Forge
Created: 2025-11-03
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from forgebase.domain.entity_base import EntityBase

T = TypeVar('T', bound=EntityBase)


class RepositoryBase(ABC, Generic[T]):
    """
    Abstract base class for all repositories.

    Implements the Repository Pattern, providing a collection-like interface
    for entity persistence. Repositories abstract away storage details,
    allowing the domain layer to remain independent of infrastructure.

    Design Decisions:
        - Generic typing ensures type safety
        - Returns Optional for find operations (None = not found)
        - Separates "not found" (None) from errors (exceptions)
        - CRUD operations as minimal contract

    :Example:

        class UserRepository(RepositoryBase[User]):
            def __init__(self, db_connection):
                self.db = db_connection

            def save(self, entity: User) -> None:
                self.db.upsert('users', entity.to_dict())

            def find_by_id(self, id: str) -> Optional[User]:
                data = self.db.get('users', id)
                return User.from_dict(data) if data else None

            def find_all(self) -> List[User]:
                return [User.from_dict(d) for d in self.db.all('users')]

            def delete(self, id: str) -> None:
                self.db.delete('users', id)

            def exists(self, id: str) -> bool:
                return self.db.exists('users', id)

    .. note::
        save() should be idempotent - calling multiple times with same ID
        should update, not create duplicates.

    .. seealso::
        :class:`EntityBase` - Entities managed by repositories
    """

    @abstractmethod
    def save(self, entity: T) -> None:
        """
        Persist an entity.

        Should be idempotent - saving the same entity (by ID) multiple times
        should update the existing record, not create duplicates.

        :param entity: Entity to persist
        :type entity: T
        :raises RepositoryError: When persistence fails

        :Example:

            user = User("user-123", "Alice", "alice@example.com")
            repository.save(user)

            # Update - not duplicate
            user.name = "Alice Smith"
            repository.save(user)  # Updates existing
        """
        pass

    @abstractmethod
    def find_by_id(self, id: str) -> T | None:
        """
        Find entity by ID.

        Returns None if not found (not an exception), allowing caller to
        decide how to handle absence.

        :param id: Entity ID
        :type id: str
        :return: Entity if found, None otherwise
        :rtype: Optional[T]
        :raises RepositoryError: When retrieval fails (not when entity absent)

        :Example:

            user = repository.find_by_id("user-123")
            if user:
                print(f"Found: {user.name}")
            else:
                print("User not found")
        """
        pass

    @abstractmethod
    def find_all(self) -> list[T]:
        """
        Retrieve all entities.

        :return: List of all entities (empty list if none)
        :rtype: List[T]
        :raises RepositoryError: When retrieval fails

        :Example:

            users = repository.find_all()
            print(f"Total users: {len(users)}")
        """
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        """
        Delete entity by ID.

        Should be idempotent - deleting a non-existent entity should not fail.

        :param id: Entity ID to delete
        :type id: str
        :raises RepositoryError: When deletion fails

        :Example:

            repository.delete("user-123")
            repository.delete("user-123")  # Idempotent - doesn't fail
        """
        pass

    @abstractmethod
    def exists(self, id: str) -> bool:
        """
        Check if entity exists by ID.

        :param id: Entity ID
        :type id: str
        :return: True if entity exists, False otherwise
        :rtype: bool
        :raises RepositoryError: When check fails

        :Example:

            if repository.exists("user-123"):
                print("User exists")
        """
        pass


class RepositoryError(Exception):
    """
    Raised when repository operations fail.

    Use this for infrastructure errors (database down, file not accessible),
    not for "entity not found" (which returns None).

    :ivar context: Additional error context information
    :vartype context: dict
    """

    def __init__(self, message: str, context: dict[str, Any] | None = None):
        """
        Initialize repository error.

        :param message: Error description
        :type message: str
        :param context: Additional context information
        :type context: Optional[dict]
        """
        super().__init__(message)
        self.context = context or {}
