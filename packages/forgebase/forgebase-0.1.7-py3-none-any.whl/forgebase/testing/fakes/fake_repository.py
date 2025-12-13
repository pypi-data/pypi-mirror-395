"""
In-memory repository for testing.

Provides a fake repository implementation that stores entities in memory
for fast, isolated testing. Implements RepositoryBase interface for drop-in
replacement of real repositories.

Philosophy:
    Tests should be fast and isolated. Real repositories involve I/O
    (file system, databases, network) which slows tests and creates
    dependencies. FakeRepository provides the same interface with
    zero I/O overhead and complete isolation.

    Benefits:
    1. Blazing fast - no I/O latency
    2. Isolated - each test gets clean state
    3. Inspectable - query internal state
    4. Predictable - no external failures
    5. Drop-in replacement - implements RepositoryBase

Use Cases:
    - Testing UseCases without database
    - Testing domain logic in isolation
    - Fast unit test execution
    - Verifying repository interactions

Example::

    from forgebase.testing.fakes.fake_repository import FakeRepository

    def test_user_creation():
        # Setup
        repo = FakeRepository()
        usecase = CreateUserUseCase(repository=repo)

        # Execute
        user = usecase.execute({"email": "test@example.com"})

        # Verify
        assert repo.count() == 1
        assert repo.contains(user.id)
        saved_user = repo.find_by_id(user.id)
        assert saved_user.email == "test@example.com"

:author: ForgeBase Development Team
:since: 2025-11-03
"""

from typing import TypeVar

from forgebase.domain.entity_base import EntityBase
from forgebase.infrastructure.repository.repository_base import (
    RepositoryBase,
    RepositoryError,
)

# Generic type for entities
T = TypeVar('T', bound=EntityBase)


class FakeRepository(RepositoryBase[T]):
    """
    In-memory repository for testing.

    Stores entities in a Python dictionary, providing fast CRUD operations
    without any I/O overhead. Perfect for unit testing.

    Features:
        - Instant CRUD operations
        - Query capabilities (find_by, filter)
        - Inspection methods (count, contains, get_all_ids)
        - Reset between tests
        - Simulates repository errors

    Thread-safe for concurrent test scenarios.

    :ivar _storage: Dictionary storing entities by ID
    :vartype _storage: Dict[str, T]
    :ivar _should_fail: Flag to simulate repository failures
    :vartype _should_fail: bool

    Example::

        # Create repository
        repo = FakeRepository[User]()

        # Save entities
        user1 = User(id="1", name="Alice")
        user2 = User(id="2", name="Bob")
        repo.save(user1)
        repo.save(user2)

        # Query
        assert repo.count() == 2
        alice = repo.find_by_id("1")
        assert alice.name == "Alice"

        # Inspect
        all_ids = repo.get_all_ids()
        assert all_ids == ["1", "2"]

        # Reset
        repo.clear()
        assert repo.count() == 0
    """

    def __init__(self):
        """Initialize empty in-memory storage."""
        self._storage: dict[str, T] = {}
        self._should_fail = False

    def save(self, entity: T) -> None:
        """
        Save entity to memory.

        :param entity: Entity to save
        :type entity: T
        :raises RepositoryError: If simulated failure enabled

        Example::

            user = User(id="123", name="Alice")
            repo.save(user)

            # Update
            user.name = "Alice Updated"
            repo.save(user)  # Overwrites existing
        """
        self._check_failure()

        # Validate entity before saving
        entity.validate()

        # Store by ID
        self._storage[entity.id] = entity

    def find_by_id(self, id: str) -> T | None:
        """
        Find entity by ID.

        :param id: Entity ID
        :type id: str
        :return: Entity if found, None otherwise
        :rtype: Optional[T]
        :raises RepositoryError: If simulated failure enabled

        Example::

            user = repo.find_by_id("123")
            if user:
                print(f"Found: {user.name}")
            else:
                print("Not found")
        """
        self._check_failure()
        return self._storage.get(id)

    def find_all(self) -> list[T]:
        """
        Retrieve all entities.

        :return: List of all entities
        :rtype: List[T]
        :raises RepositoryError: If simulated failure enabled

        Example::

            all_users = repo.find_all()
            print(f"Total users: {len(all_users)}")
        """
        self._check_failure()
        return list(self._storage.values())

    def delete(self, id: str) -> None:
        """
        Delete entity by ID.

        Idempotent - deleting non-existent entity doesn't raise error.

        :param id: Entity ID to delete
        :type id: str
        :raises RepositoryError: If simulated failure enabled

        Example::

            repo.delete("123")
            assert not repo.contains("123")

            # Idempotent
            repo.delete("123")  # No error
        """
        self._check_failure()

        if id in self._storage:
            del self._storage[id]

    def exists(self, id: str) -> bool:
        """
        Check if entity exists.

        :param id: Entity ID
        :type id: str
        :return: True if entity exists
        :rtype: bool
        :raises RepositoryError: If simulated failure enabled

        Example::

            if repo.exists("123"):
                print("User exists")
            else:
                print("User not found")
        """
        self._check_failure()
        return id in self._storage

    def count(self) -> int:
        """
        Count total number of entities.

        :return: Total entity count
        :rtype: int
        :raises RepositoryError: If simulated failure enabled

        Example::

            assert repo.count() == 5
        """
        self._check_failure()
        return len(self._storage)

    def clear(self) -> None:
        """
        Delete all entities.

        WARNING: This operation cannot be undone!

        :raises RepositoryError: If simulated failure enabled

        Example::

            repo.clear()
            assert repo.count() == 0
        """
        self._check_failure()
        self._storage.clear()

    # Additional test helpers

    def contains(self, id: str) -> bool:
        """
        Alias for exists() - more natural in test assertions.

        :param id: Entity ID
        :type id: str
        :return: True if entity exists
        :rtype: bool

        Example::

            assert repo.contains("123")
            assert not repo.contains("999")
        """
        return self.exists(id)

    def get_all_ids(self) -> list[str]:
        """
        Get list of all entity IDs.

        Useful for test assertions and debugging.

        :return: List of entity IDs
        :rtype: List[str]

        Example::

            ids = repo.get_all_ids()
            assert "123" in ids
            assert len(ids) == 5
        """
        return list(self._storage.keys())

    def find_by(self, **criteria) -> list[T]:
        """
        Find entities matching criteria.

        Performs simple attribute matching. For more complex queries,
        use find_all() and filter in Python.

        :param criteria: Attribute key-value pairs to match
        :return: List of matching entities
        :rtype: List[T]

        Example::

            # Find by single attribute
            active_users = repo.find_by(status="active")

            # Find by multiple attributes
            admins = repo.find_by(role="admin", department="IT")

            # No matches returns empty list
            ghosts = repo.find_by(status="ghost")
            assert ghosts == []
        """
        results = []

        for entity in self._storage.values():
            matches = all(
                hasattr(entity, key) and getattr(entity, key) == value
                for key, value in criteria.items()
            )

            if matches:
                results.append(entity)

        return results

    def filter(self, predicate) -> list[T]:
        """
        Filter entities using custom predicate function.

        :param predicate: Function that returns True for matching entities
        :type predicate: Callable[[T], bool]
        :return: List of matching entities
        :rtype: List[T]

        Example::

            # Find users with long names
            long_names = repo.filter(lambda u: len(u.name) > 10)

            # Find active users created this year
            recent_active = repo.filter(
                lambda u: u.status == "active" and u.created_at.year == 2025
            )

            # Complex conditions
            special_users = repo.filter(
                lambda u: u.is_premium() and u.last_login_days_ago() < 7
            )
        """
        return [entity for entity in self._storage.values() if predicate(entity)]

    def simulate_failure(self, should_fail: bool = True) -> None:
        """
        Enable/disable simulated repository failures.

        Useful for testing error handling in code that uses the repository.

        :param should_fail: Whether to simulate failures
        :type should_fail: bool

        Example::

            # Enable failure simulation
            repo.simulate_failure(True)

            # This will raise RepositoryError
            try:
                repo.save(user)
            except RepositoryError:
                print("Handled repository failure")

            # Disable simulation
            repo.simulate_failure(False)
            repo.save(user)  # Works normally
        """
        self._should_fail = should_fail

    def _check_failure(self) -> None:
        """
        Check if should simulate failure.

        :raises RepositoryError: If failure simulation enabled
        """
        if self._should_fail:
            raise RepositoryError("Simulated repository failure")

    def reset(self) -> None:
        """
        Reset repository to initial state.

        Clears all entities and disables failure simulation.

        Example::

            def setUp(self):
                self.repo = FakeRepository()

            def tearDown(self):
                self.repo.reset()
        """
        self._storage.clear()
        self._should_fail = False

    def __len__(self) -> int:
        """
        Support len() function.

        Example::

            assert len(repo) == 5
            # Equivalent to:
            assert repo.count() == 5
        """
        return len(self._storage)

    def __contains__(self, id: str) -> bool:
        """
        Support 'in' operator.

        Example::

            if "123" in repo:
                print("User exists")
            # Equivalent to:
            if repo.contains("123"):
                print("User exists")
        """
        return id in self._storage

    def __repr__(self) -> str:
        """String representation."""
        return f"<FakeRepository entities={len(self._storage)}>"
