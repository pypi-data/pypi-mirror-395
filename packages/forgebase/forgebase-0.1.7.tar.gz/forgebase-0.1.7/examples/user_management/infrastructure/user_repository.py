"""
In-Memory User Repository Implementation.

Concrete implementation of UserRepositoryPort using in-memory storage.
Perfect for examples and testing.

:author: ForgeBase Development Team
:since: 2025-11-03
"""

from examples.user_management.application.ports import UserRepositoryPort
from examples.user_management.domain.user import User


class InMemoryUserRepository(UserRepositoryPort):
    """
    In-memory implementation of user repository.

    Stores users in a dictionary for fast access. Perfect for examples,
    testing, and prototyping.

    In production, you would swap this with a SQL/NoSQL implementation
    without changing any application code (thanks to the Port/Adapter pattern).

    Example::

        # Create repository
        repository = InMemoryUserRepository()

        # Save user
        user = User(name="John", email=Email("john@example.com"))
        repository.save(user)

        # Find by ID
        found = repository.find_by_id(user.id)
        assert found == user

        # Find by email
        found = repository.find_by_email("john@example.com")
        assert found == user

    :ivar _storage: Internal storage dictionary
    :vartype _storage: Dict[str, User]
    :ivar _email_index: Email to user ID index
    :vartype _email_index: Dict[str, str]
    """

    def __init__(self):
        """Initialize empty repository."""
        self._storage: dict[str, User] = {}
        self._email_index: dict[str, str] = {}  # email -> user_id mapping

    def save(self, user: User) -> None:
        """
        Save user to repository.

        :param user: User entity to save
        :type user: User
        """
        user.validate()  # Ensure user is valid before saving

        self._storage[user.id] = user
        self._email_index[str(user.email)] = user.id

    def find_by_id(self, user_id: str) -> User | None:
        """
        Find user by ID.

        :param user_id: User identifier
        :type user_id: str
        :return: User if found, None otherwise
        :rtype: Optional[User]
        """
        return self._storage.get(user_id)

    def find_by_email(self, email: str) -> User | None:
        """
        Find user by email address.

        :param email: Email address
        :type email: str
        :return: User if found, None otherwise
        :rtype: Optional[User]
        """
        user_id = self._email_index.get(email)
        if user_id:
            return self._storage.get(user_id)
        return None

    def delete(self, user_id: str) -> None:
        """
        Delete user from repository.

        :param user_id: User identifier
        :type user_id: str
        """
        user = self._storage.get(user_id)
        if user:
            # Remove from email index
            del self._email_index[str(user.email)]
            # Remove from storage
            del self._storage[user_id]

    def exists(self, user_id: str) -> bool:
        """
        Check if user exists.

        :param user_id: User identifier
        :type user_id: str
        :return: True if user exists
        :rtype: bool
        """
        return user_id in self._storage

    def count(self) -> int:
        """
        Get total number of users.

        :return: User count
        :rtype: int
        """
        return len(self._storage)

    def find_all(self) -> list[User]:
        """
        Get all users.

        :return: List of all users
        :rtype: List[User]
        """
        return list(self._storage.values())

    def clear(self) -> None:
        """Clear all users from repository."""
        self._storage.clear()
        self._email_index.clear()

    def info(self) -> dict:
        """
        Get repository information.

        :return: Repository metadata
        :rtype: dict
        """
        return {
            'adapter': 'InMemoryUserRepository',
            'type': 'repository',
            'storage_type': 'in-memory',
            'user_count': self.count()
        }
