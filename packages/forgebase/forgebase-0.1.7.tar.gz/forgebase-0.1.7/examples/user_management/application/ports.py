"""
Application Ports for User Management.

Defines the contracts that external systems must implement.

:author: ForgeBase Development Team
:since: 2025-11-03
"""

from abc import abstractmethod

from examples.user_management.domain.user import User
from forgebase.application.port_base import PortBase


class UserRepositoryPort(PortBase):
    """
    Port (interface) for user repository.

    This port defines the contract for persisting and retrieving users.
    Concrete implementations can use any storage mechanism (JSON, SQL, etc.)
    without affecting the application layer.

    This follows the Hexagonal Architecture pattern: the application defines
    what it needs (the port), and infrastructure provides implementations (adapters).

    Example::

        # Application layer uses the port
        class CreateUserUseCase:
            def __init__(self, user_repository: UserRepositoryPort):
                self.user_repository = user_repository

            def execute(self, name: str, email: str):
                user = User(name=name, email=Email(email))
                self.user_repository.save(user)
                return user

        # Infrastructure provides concrete implementation
        class JSONUserRepository(UserRepositoryPort):
            def save(self, user: User) -> None:
                # Save to JSON file
                ...
    """

    @abstractmethod
    def save(self, user: User) -> None:
        """
        Save user to repository.

        :param user: User entity to save
        :type user: User
        """
        pass

    @abstractmethod
    def find_by_id(self, user_id: str) -> User | None:
        """
        Find user by ID.

        :param user_id: User identifier
        :type user_id: str
        :return: User if found, None otherwise
        :rtype: Optional[User]
        """
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User | None:
        """
        Find user by email address.

        :param email: Email address
        :type email: str
        :return: User if found, None otherwise
        :rtype: Optional[User]
        """
        pass

    @abstractmethod
    def delete(self, user_id: str) -> None:
        """
        Delete user from repository.

        :param user_id: User identifier
        :type user_id: str
        """
        pass

    @abstractmethod
    def exists(self, user_id: str) -> bool:
        """
        Check if user exists.

        :param user_id: User identifier
        :type user_id: str
        :return: True if user exists
        :rtype: bool
        """
        pass

    def info(self) -> dict:
        """
        Get port information.

        :return: Port metadata
        :rtype: dict
        """
        return {
            'port': 'UserRepositoryPort',
            'type': 'driven',
            'module': 'user_management.application.ports',
            'description': 'User persistence contract'
        }
