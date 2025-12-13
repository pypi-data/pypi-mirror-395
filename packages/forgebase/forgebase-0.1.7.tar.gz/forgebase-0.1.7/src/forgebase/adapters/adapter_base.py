"""
Base class for all adapters in ForgeBase.

Adapters implement ports, providing concrete connections to external systems.
Following Hexagonal Architecture, adapters isolate infrastructure concerns
from the application core.

Author: Jorge, The Forge
Created: 2025-11-03
"""

from abc import ABC, abstractmethod
from typing import Any


class AdapterBase(ABC):
    """
    Abstract base class for all adapters.

    Adapters are concrete implementations of ports. They handle communication
    with external systems (databases, HTTP APIs, file systems, etc.) while
    keeping the application core independent of these details.

    Two types of adapters:
        - Driving adapters (primary): Drive the application (e.g., CLI, HTTP server)
        - Driven adapters (secondary): Driven by the application (e.g., Repository, Email)

    Design Decisions:
        - Introspection via name() and module() for debugging and logging
        - info() method for runtime metadata
        - _instrument() hook for observability integration

    :Example:

        class JSONUserRepository(AdapterBase, UserRepositoryPort):
            def __init__(self, file_path: str):
                self.file_path = file_path

            def name(self) -> str:
                return "JSONUserRepository"

            def module(self) -> str:
                return "infrastructure.repository"

            def save(self, user: User) -> None:
                # Implementation
                pass

            def find_by_id(self, user_id: str) -> Optional[User]:
                # Implementation
                pass

    .. seealso::
        :class:`PortBase` - Defines adapter contracts
    """

    @abstractmethod
    def name(self) -> str:
        """
        Return the adapter's name.

        Used for logging, debugging, and introspection.

        :return: Adapter name
        :rtype: str

        :Example:

            def name(self) -> str:
                return self.__class__.__name__
        """
        pass

    @abstractmethod
    def module(self) -> str:
        """
        Return the adapter's module path.

        Used for categorization and introspection.

        :return: Module path (e.g., "infrastructure.repository")
        :rtype: str

        :Example:

            def module(self) -> str:
                return "infrastructure.repository"
        """
        pass

    def info(self) -> dict[str, Any]:
        """
        Return metadata about this adapter.

        Provides information useful for debugging, logging, and documentation.

        :return: Dictionary with adapter metadata
        :rtype: Dict[str, Any]

        :Example:

            def info(self) -> dict:
                return {
                    "name": self.name(),
                    "module": self.module(),
                    "type": "driven",  # or "driving"
                    "description": "JSON-based user repository"
                }
        """
        return {
            "name": self.name(),
            "module": self.module(),
            "type": "adapter"
        }

    @abstractmethod
    def _instrument(self) -> None:
        """
        Hook for instrumentation and observability setup.

        Override this to add metrics collection, logging, or tracing to the
        adapter. Called during adapter initialization.

        :Example:

            def _instrument(self) -> None:
                self.metrics_collector.register_adapter(self.name())
                self.logger.info(f"Adapter {self.name()} initialized")
        """
        pass

    def __str__(self) -> str:
        """
        String representation of the adapter.

        :return: Human-readable adapter description
        :rtype: str
        """
        return f"{self.name()} ({self.module()})"

    def __repr__(self) -> str:
        """
        Developer-friendly representation.

        :return: Representation string
        :rtype: str
        """
        return f"{self.__class__.__name__}()"
