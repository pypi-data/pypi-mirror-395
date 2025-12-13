"""
ForgeBase Core Initialization & Bootstrap.

Provides cognitive initialization sequence for the ForgeBase framework,
handling dependency injection, configuration, observability, and lifecycle.

:author: ForgeBase Development Team
:since: 2025-11-03
"""

import atexit
import signal
import sys
from typing import Any

from forgebase.application.usecase_base import UseCaseBase
from forgebase.infrastructure.configuration.config_loader import ConfigLoader
from forgebase.infrastructure.logging.logger_port import LoggerPort, StdoutLogger
from forgebase.observability.feedback_manager import FeedbackManager
from forgebase.observability.log_service import LogService
from forgebase.observability.tracer_port import NoOpTracer, TracerPort
from forgebase.observability.track_metrics import TrackMetrics


class DependencyContainer:
    """
    Lightweight dependency injection container.

    Manages component lifecycle and dependency resolution without
    heavy framework dependencies.
    """

    def __init__(self):
        """Initialize empty container."""
        self._services: dict[str, Any] = {}
        self._singletons: dict[str, Any] = {}

    def register(self, name: str, instance: Any, singleton: bool = True) -> None:
        """
        Register a service.

        :param name: Service identifier
        :type name: str
        :param instance: Service instance or factory
        :type instance: Any
        :param singleton: Whether to cache as singleton
        :type singleton: bool
        """
        if singleton:
            self._singletons[name] = instance
        else:
            self._services[name] = instance

    def get(self, name: str) -> Any:
        """
        Retrieve a service.

        :param name: Service identifier
        :type name: str
        :return: Service instance
        :rtype: Any
        :raises KeyError: If service not found
        """
        if name in self._singletons:
            return self._singletons[name]
        if name in self._services:
            return self._services[name]
        msg = f"Service '{name}' not found in container"
        raise KeyError(msg)

    def has(self, name: str) -> bool:
        """
        Check if service exists.

        :param name: Service identifier
        :type name: str
        :return: True if service registered
        :rtype: bool
        """
        return name in self._singletons or name in self._services

    def clear(self) -> None:
        """Clear all registered services."""
        self._services.clear()
        self._singletons.clear()


class ForgeBaseCore:
    """
    Core initialization and bootstrap system for ForgeBase.

    Orchestrates the cognitive initialization sequence, ensuring all
    components are properly configured, instrumented, and ready for use.

    This class embodies the "Reflexividade" principle by providing
    complete introspection of the initialized system.

    Example::

        core = ForgeBaseCore(config_path="config.yaml")
        core.bootstrap()

        # Use the framework
        usecase = core.get_usecase("my_usecase")
        result = usecase.execute(data=input_data)

        # Graceful shutdown
        core.shutdown()
    """

    def __init__(self, config_path: str | None = None):
        """
        Initialize ForgeBase core.

        :param config_path: Optional path to configuration file
        :type config_path: Optional[str]
        """
        self.config_path = config_path
        self.container = DependencyContainer()
        self._usecases: dict[str, UseCaseBase] = {}
        self._adapters: dict[str, Any] = {}
        self._initialized = False
        self._shutdown_handlers: list = []

    def bootstrap(self) -> None:
        """
        Execute complete bootstrap sequence.

        Phases:
        1. Load Configuration
        2. Setup Logging
        3. Initialize Observability
        4. Discover & Register UseCases
        5. Initialize Adapters
        6. Health Check
        7. Ready

        :raises RuntimeError: If bootstrap fails
        """
        if self._initialized:
            msg = "ForgeBase already initialized"
            raise RuntimeError(msg)

        try:
            # Phase 1: Load Configuration
            self._load_configuration()

            # Phase 2: Setup Logging
            self._setup_logging()

            # Phase 3: Initialize Observability
            self._initialize_observability()

            # Phase 4: Register UseCases
            self._discover_usecases()

            # Phase 5: Initialize Adapters
            self._initialize_adapters()

            # Phase 6: Health Check
            health = self.health_check()
            if not health['healthy']:
                msg = f"Health check failed: {health}"
                raise RuntimeError(msg)

            # Phase 7: Ready
            self._register_shutdown_handlers()
            self._initialized = True

            logger = self.container.get('logger')
            logger.info(
                "ForgeBase initialized successfully",
                usecases=len(self._usecases),
                adapters=len(self._adapters)
            )

        except Exception as e:
            error_msg = f"Bootstrap failed: {e}"
            if self.container.has('logger'):
                logger = self.container.get('logger')
                logger.error(error_msg, error=str(e))
            raise RuntimeError(error_msg) from e

    def _load_configuration(self) -> None:
        """Load configuration from file or defaults."""
        # Create config loader with defaults
        config_loader = ConfigLoader(defaults={
            'app.name': 'ForgeBase',
            'app.debug': False,
            'log.level': 'INFO'
        })

        # Load from file if specified
        if self.config_path:
            config_loader.load_from_file(self.config_path)

        # Load from environment variables
        config_loader.load_from_env(prefix='FORGEBASE')

        self.container.register('config_loader', config_loader)
        self.container.register('config', config_loader.get_all())

    def _setup_logging(self) -> None:
        """Setup logging infrastructure."""
        # Use StdoutLogger as default
        logger: LoggerPort = StdoutLogger()
        self.container.register('logger', logger)

        # Initialize LogService
        log_service = LogService(
            service_name="forgebase",
            environment="development"
        )
        # Add console handler
        log_service.add_console_handler()
        self.container.register('log_service', log_service)

    def _initialize_observability(self) -> None:
        """Initialize observability components."""
        # Initialize metrics
        metrics = TrackMetrics()
        self.container.register('metrics', metrics)

        # Initialize tracer (default: NoOp)
        tracer: TracerPort = NoOpTracer()
        self.container.register('tracer', tracer)

        # Initialize feedback manager
        feedback = FeedbackManager()
        self.container.register('feedback', feedback)

    def _discover_usecases(self) -> None:
        """
        Discover and register UseCases.

        Scans for UseCase implementations and registers them
        in the internal registry.
        """
        # For now, UseCases must be registered manually
        # Future: implement auto-discovery via package scanning
        pass

    def _initialize_adapters(self) -> None:
        """Initialize registered adapters."""
        # Adapters are initialized on-demand when added
        pass

    def _register_shutdown_handlers(self) -> None:
        """Register graceful shutdown handlers."""
        # Register atexit handler
        atexit.register(self._cleanup)

        # Register signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame) -> None:  # noqa: ARG002
        """
        Handle shutdown signals.

        :param signum: Signal number
        :param frame: Current stack frame
        """
        logger = self.container.get('logger')
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.shutdown()
        sys.exit(0)

    def _cleanup(self) -> None:
        """Execute cleanup tasks."""
        if self.container.has('logger'):
            logger = self.container.get('logger')
            logger.debug("Executing cleanup handlers...")

        for handler in self._shutdown_handlers:
            try:
                handler()
            except Exception as e:
                if self.container.has('logger'):
                    logger = self.container.get('logger')
                    logger.error(f"Cleanup handler failed: {e}")

    def shutdown(self) -> None:
        """
        Execute graceful shutdown.

        Stops all adapters, flushes observability data,
        and releases resources.
        """
        if not self._initialized:
            return

        logger = self.container.get('logger')
        logger.info("Shutting down ForgeBase...")

        # Stop adapters
        for name, adapter in self._adapters.items():
            try:
                if hasattr(adapter, 'stop'):
                    adapter.stop()
                logger.debug(f"Stopped adapter: {name}")
            except Exception as e:
                logger.error(f"Failed to stop adapter {name}: {e}")

        # Flush metrics
        if self.container.has('metrics'):
            metrics = self.container.get('metrics')
            report = metrics.report()
            logger.info("Final metrics report", metrics=report)

        # Execute cleanup
        self._cleanup()

        self._initialized = False
        logger.info("ForgeBase shutdown complete")

    def register_usecase(self, name: str, usecase: UseCaseBase) -> None:
        """
        Register a UseCase.

        :param name: UseCase identifier
        :type name: str
        :param usecase: UseCase instance
        :type usecase: UseCaseBase
        """
        self._usecases[name] = usecase

        if self.container.has('logger'):
            logger = self.container.get('logger')
            logger.debug(f"Registered UseCase: {name}")

    def get_usecase(self, name: str) -> UseCaseBase:
        """
        Retrieve a UseCase by name.

        :param name: UseCase identifier
        :type name: str
        :return: UseCase instance
        :rtype: UseCaseBase
        :raises KeyError: If UseCase not found
        """
        if name not in self._usecases:
            msg = f"UseCase '{name}' not found"
            raise KeyError(msg)
        return self._usecases[name]

    def list_usecases(self) -> list[str]:
        """
        List all registered UseCases.

        :return: List of UseCase names
        :rtype: List[str]
        """
        return list(self._usecases.keys())

    def register_adapter(self, name: str, adapter: Any) -> None:
        """
        Register an adapter.

        :param name: Adapter identifier
        :type name: str
        :param adapter: Adapter instance
        :type adapter: Any
        """
        self._adapters[name] = adapter

        if self.container.has('logger'):
            logger = self.container.get('logger')
            logger.debug(f"Registered adapter: {name}")

    def get_adapter(self, name: str) -> Any:
        """
        Retrieve an adapter by name.

        :param name: Adapter identifier
        :type name: str
        :return: Adapter instance
        :rtype: Any
        :raises KeyError: If adapter not found
        """
        if name not in self._adapters:
            msg = f"Adapter '{name}' not found"
            raise KeyError(msg)
        return self._adapters[name]

    def add_shutdown_handler(self, handler) -> None:
        """
        Add custom shutdown handler.

        :param handler: Callable to execute on shutdown
        :type handler: Callable
        """
        self._shutdown_handlers.append(handler)

    def health_check(self) -> dict[str, Any]:
        """
        Execute health check on all components.

        :return: Health status report
        :rtype: Dict[str, Any]
        """
        health = {
            'healthy': True,
            'components': {},
            'timestamp': None
        }

        # Check configuration
        health['components']['config'] = {
            'status': 'ok' if self.container.has('config') else 'missing'
        }

        # Check logging
        health['components']['logging'] = {
            'status': 'ok' if self.container.has('logger') else 'missing'
        }

        # Check observability
        health['components']['metrics'] = {
            'status': 'ok' if self.container.has('metrics') else 'missing'
        }

        health['components']['tracer'] = {
            'status': 'ok' if self.container.has('tracer') else 'missing'
        }

        # Check UseCases
        health['components']['usecases'] = {
            'status': 'ok',
            'count': len(self._usecases),
            'registered': list(self._usecases.keys())
        }

        # Check Adapters
        health['components']['adapters'] = {
            'status': 'ok',
            'count': len(self._adapters),
            'registered': list(self._adapters.keys())
        }

        # Determine overall health
        health['healthy'] = all(
            comp.get('status') == 'ok'
            for comp in health['components'].values()
            if 'status' in comp
        )

        return health

    def info(self) -> dict[str, Any]:
        """
        Get system information and introspection data.

        :return: System information
        :rtype: Dict[str, Any]
        """
        return {
            'initialized': self._initialized,
            'config_path': self.config_path,
            'usecases': {
                'count': len(self._usecases),
                'names': list(self._usecases.keys())
            },
            'adapters': {
                'count': len(self._adapters),
                'names': list(self._adapters.keys())
            },
            'services': {
                'registered': (
                    list(self.container._singletons.keys()) +
                    list(self.container._services.keys())
                )
            }
        }
