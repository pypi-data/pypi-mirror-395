"""
Base class for ports (interface contracts) in ForgeBase.

Ports define contracts for external communication following Hexagonal
Architecture. They are implemented by adapters in the infrastructure layer.

Author: Jorge, The Forge
Created: 2025-11-03
"""

from abc import ABC, abstractmethod
from typing import Any


class PortBase(ABC):
    """
    Abstract base class for all ports.

    Ports are interfaces that define contracts between the application core
    and external systems. Following Hexagonal Architecture, ports allow the
    core to remain independent of implementation details.

    Two types of ports:
        - Driving ports (primary): Called BY the application (e.g., CLI, HTTP)
        - Driven ports (secondary): Called FROM the application (e.g., Repository)

    :Example:

        class UserRepositoryPort(PortBase):
            @abstractmethod
            def save(self, user: User) -> None:
                pass

            @abstractmethod
            def find_by_id(self, user_id: str) -> Optional[User]:
                pass

            def info(self) -> dict:
                return {
                    "name": "UserRepositoryPort",
                    "type": "driven",
                    "methods": ["save", "find_by_id"]
                }

    .. seealso::
        :class:`AdapterBase` - Implements ports
    """

    @abstractmethod
    def info(self) -> dict[str, Any]:
        """
        Return metadata about this port for introspection.

        Provides information about the port's purpose, type, and contract.
        Useful for documentation, debugging, and runtime introspection.

        :return: Dictionary with port metadata
        :rtype: Dict[str, Any]

        :Example:

            def info(self) -> dict:
                return {
                    "name": self.__class__.__name__,
                    "type": "driven",  # or "driving"
                    "methods": ["method1", "method2"],
                    "description": "Port for X functionality"
                }
        """
        pass

    def __str__(self) -> str:
        """
        String representation of the port.

        :return: Human-readable port description
        :rtype: str
        """
        info = self.info()
        return f"{info.get('name', self.__class__.__name__)} ({info.get('type', 'unknown')} port)"
