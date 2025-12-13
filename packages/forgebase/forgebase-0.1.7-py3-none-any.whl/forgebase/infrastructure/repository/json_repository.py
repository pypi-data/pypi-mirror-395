"""
JSON-based repository implementation.

Provides simple file-based persistence using JSON format.
Suitable for development, testing, and small-scale applications.

Author: Jorge, The Forge
Created: 2025-11-03
"""

import json
import threading
from collections.abc import Callable
from pathlib import Path
from typing import Any, Generic, TypeVar

from forgebase.domain.entity_base import EntityBase
from forgebase.infrastructure.repository.repository_base import (
    RepositoryBase,
    RepositoryError,
)

T = TypeVar('T', bound=EntityBase)


class JSONRepository(RepositoryBase[T], Generic[T]):
    """
    JSON file-based repository implementation.

    Persists entities as JSON in a single file. Provides thread-safe operations
    via file locking. Suitable for development and small datasets.

    Design Decisions:
        - Single JSON file with dict of entities (keyed by ID)
        - File locking for thread safety
        - Automatic file/directory creation
        - Loads entire file into memory (not suitable for large datasets)

    Limitations:
        - Not suitable for >10k entities (performance)
        - Not suitable for distributed systems (local file)
        - No transaction support across multiple operations
        - No query optimization (full scan)

    :param file_path: Path to JSON file
    :param entity_class: Entity class for deserialization
    :param to_dict: Function to convert entity to dict (optional)
    :param from_dict: Function to create entity from dict (optional)

    :Example:

        class User(EntityBase):
            def __init__(self, id, name, email):
                super().__init__(id)
                self.name = name
                self.email = email

            def validate(self):
                if not self.name:
                    raise ValueError("Name required")

            def to_dict(self):
                return {"id": self.id, "name": self.name, "email": self.email}

            @classmethod
            def from_dict(cls, data):
                return cls(data["id"], data["name"], data["email"])

        # Usage
        repo = JSONRepository("data/users.json", User)
        user = User(None, "Alice", "alice@example.com")
        repo.save(user)

        found = repo.find_by_id(user.id)
        print(found.name)  # "Alice"

    .. warning::
        Not suitable for production use with large datasets or high concurrency.

    .. seealso::
        :class:`RepositoryBase` - Abstract interface
    """

    def __init__(
        self,
        file_path: str,
        entity_class: type[T],
        to_dict: Callable[[T], dict[str, Any]] | None = None,
        from_dict: Callable[[dict[str, Any]], T] | None = None
    ):
        """
        Initialize JSON repository.

        Creates file and parent directories if they don't exist.

        :param file_path: Path to JSON file
        :param entity_class: Entity class for type checking
        :param to_dict: Optional custom serializer (defaults to entity.to_dict())
        :param from_dict: Optional custom deserializer (defaults to entity_class.from_dict())
        """
        self.file_path = Path(file_path)
        self.entity_class = entity_class
        self._to_dict = to_dict or (lambda e: e.to_dict())  # type: ignore[attr-defined]
        self._from_dict = from_dict or entity_class.from_dict  # type: ignore[attr-defined]
        self._lock = threading.Lock()
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Create file and parent directories if they don't exist."""
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            if not self.file_path.exists():
                self._write_data({})
        except OSError as e:
            raise RepositoryError(f"Failed to create file {self.file_path}: {e}") from e

    def _read_data(self) -> dict[str, Any]:
        """Read and parse JSON file."""
        try:
            with open(self.file_path, encoding='utf-8') as f:
                return json.load(f)  # type: ignore[no-any-return]
        except json.JSONDecodeError as e:
            raise RepositoryError(f"Invalid JSON in {self.file_path}: {e}") from e
        except OSError as e:
            raise RepositoryError(f"Failed to read {self.file_path}: {e}") from e

    def _write_data(self, data: dict[str, Any]) -> None:
        """Write data to JSON file."""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except OSError as e:
            raise RepositoryError(f"Failed to write {self.file_path}: {e}") from e

    def save(self, entity: T) -> None:
        """
        Save entity to JSON file.

        Thread-safe via locking. Idempotent - updates if ID exists.

        :param entity: Entity to save
        :raises RepositoryError: If save fails
        """
        if not isinstance(entity, self.entity_class):
            raise RepositoryError(
                f"Expected {self.entity_class.__name__}, got {type(entity).__name__}"
            )

        with self._lock:
            data = self._read_data()
            data[entity.id] = self._to_dict(entity)
            self._write_data(data)

    def find_by_id(self, id: str) -> T | None:
        """
        Find entity by ID.

        :param id: Entity ID
        :return: Entity if found, None otherwise
        :raises RepositoryError: If read fails
        """
        with self._lock:
            data = self._read_data()
            entity_data = data.get(id)
            return self._from_dict(entity_data) if entity_data else None

    def find_all(self) -> list[T]:
        """
        Retrieve all entities.

        :return: List of all entities
        :raises RepositoryError: If read fails
        """
        with self._lock:
            data = self._read_data()
            return [self._from_dict(entity_data) for entity_data in data.values()]

    def delete(self, id: str) -> None:
        """
        Delete entity by ID.

        Idempotent - doesn't fail if entity doesn't exist.

        :param id: Entity ID
        :raises RepositoryError: If deletion fails
        """
        with self._lock:
            data = self._read_data()
            data.pop(id, None)  # Idempotent - no error if missing
            self._write_data(data)

    def exists(self, id: str) -> bool:
        """
        Check if entity exists.

        :param id: Entity ID
        :return: True if exists
        :raises RepositoryError: If check fails
        """
        with self._lock:
            data = self._read_data()
            return id in data

    def count(self) -> int:
        """
        Count total entities.

        :return: Total number of entities
        :raises RepositoryError: If count fails
        """
        with self._lock:
            data = self._read_data()
            return len(data)

    def clear(self) -> None:
        """
        Delete all entities.

        :raises RepositoryError: If clear fails
        """
        with self._lock:
            self._write_data({})
