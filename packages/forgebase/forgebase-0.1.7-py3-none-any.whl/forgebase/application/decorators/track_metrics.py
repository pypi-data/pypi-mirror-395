"""
Decorator for automatic metrics instrumentation.

Provides decorators for automatic tracking of UseCase and Port executions,
capturing metrics like duration, success/failure rates, and invocation counts
without cluttering business logic.

Philosophy:
    Observability should be effortless. Rather than manually instrumenting
    every method with metrics collection code, decorators enable automatic
    tracking that:

    1. Doesn't clutter business logic
    2. Is consistent across the codebase
    3. Can be toggled on/off easily
    4. Reduces boilerplate

    This follows the principle of aspect-oriented programming, separating
    cross-cutting concerns like metrics from core functionality.

Example::

    from forgebase.application.decorators.track_metrics import track_metrics
    from forgebase.observability.track_metrics import TrackMetrics

    # Initialize metrics system
    metrics = TrackMetrics()

    # Decorate UseCase
    @track_metrics(metrics, name="create_user")
    def execute(self, user_data: dict) -> User:
        user = User(**user_data)
        self.repository.save(user)
        return user

    # Metrics are automatically collected:
    # - usecase.execution.count
    # - usecase.execution.duration
    # - usecase.execution.errors

:author: ForgeBase Development Team
:since: 2025-11-03
"""

import functools
import inspect
import time
from collections.abc import Callable
from typing import Any

from forgebase.observability.track_metrics import TrackMetrics


def track_metrics(
    metrics: TrackMetrics,
    name: str | None = None,
    track_errors: bool = True,
    track_duration: bool = True,
    track_count: bool = True,
    **labels: str
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator for automatic metrics tracking.

    Automatically instruments a function to collect metrics about:
    - Execution count
    - Execution duration
    - Success/failure rate
    - Exception types

    :param metrics: TrackMetrics instance
    :type metrics: TrackMetrics
    :param name: Metric name (defaults to function name)
    :type name: Optional[str]
    :param track_errors: Whether to track errors
    :type track_errors: bool
    :param track_duration: Whether to track duration
    :type track_duration: bool
    :param track_count: Whether to track invocation count
    :type track_count: bool
    :param labels: Additional labels for metrics
    :type labels: str
    :return: Decorated function
    :rtype: Callable

    Example::

        metrics = TrackMetrics()

        @track_metrics(metrics, name="process_order")
        def process_order(order_id: str):
            # ... business logic ...
            return result

        # Or with custom labels
        @track_metrics(
            metrics,
            name="api_call",
            service="payment_gateway"
        )
        def call_payment_api():
            # ... API call ...
            pass

        # Async functions supported
        @track_metrics(metrics, name="async_operation")
        async def async_operation():
            # ... async logic ...
            pass
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """Inner decorator function."""
        metric_name = name or func.__name__
        metric_labels = labels

        # Check if function is async
        is_async = inspect.iscoroutinefunction(func)

        if is_async:
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                """Async wrapper for instrumented function."""
                # Increment invocation count
                if track_count:
                    metrics.increment(
                        f"{metric_name}.count",
                        amount=1,
                        **metric_labels
                    )

                # Track duration
                start_time = time.time()

                try:
                    result = await func(*args, **kwargs)

                    # Track success
                    if track_count:
                        metrics.increment(
                            f"{metric_name}.success",
                            amount=1,
                            **metric_labels
                        )

                    return result

                except Exception as e:
                    # Track errors
                    if track_errors:
                        metrics.increment(
                            f"{metric_name}.errors",
                            amount=1,
                            error_type=type(e).__name__,
                            **metric_labels
                        )

                    raise

                finally:
                    # Track duration
                    if track_duration:
                        duration_ms = (time.time() - start_time) * 1000
                        metrics.histogram(
                            f"{metric_name}.duration_ms",
                            duration_ms,
                            **metric_labels
                        )

            return async_wrapper

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            """Sync wrapper for instrumented function."""
            # Increment invocation count
            if track_count:
                metrics.increment(
                    f"{metric_name}.count",
                    amount=1,
                    **metric_labels
                )

            # Track duration
            start_time = time.time()

            try:
                result = func(*args, **kwargs)

                # Track success
                if track_count:
                    metrics.increment(
                        f"{metric_name}.success",
                        amount=1,
                        **metric_labels
                    )

                return result

            except Exception as e:
                # Track errors
                if track_errors:
                    metrics.increment(
                        f"{metric_name}.errors",
                        amount=1,
                        error_type=type(e).__name__,
                        **metric_labels
                    )

                raise

            finally:
                # Track duration
                if track_duration:
                    duration_ms = (time.time() - start_time) * 1000
                    metrics.histogram(
                        f"{metric_name}.duration_ms",
                        duration_ms,
                        **metric_labels
                    )

        return sync_wrapper

    return decorator


def track_usecase(
    metrics: TrackMetrics,
    name: str | None = None,
    **labels: str
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator specifically for UseCase instrumentation.

    Convenience wrapper around track_metrics with UseCase-specific naming.

    :param metrics: TrackMetrics instance
    :type metrics: TrackMetrics
    :param name: UseCase name (defaults to class name)
    :type name: Optional[str]
    :param labels: Additional labels
    :type labels: str
    :return: Decorated function
    :rtype: Callable

    Example::

        metrics = TrackMetrics()

        class CreateUserUseCase(UseCaseBase):
            @track_usecase(metrics, name="create_user")
            def execute(self, user_data: dict) -> User:
                # ... business logic ...
                return user

        # Metrics generated:
        # - create_user.count
        # - create_user.duration_ms
        # - create_user.success
        # - create_user.errors
    """
    return track_metrics(
        metrics=metrics,
        name=f"usecase.{name}" if name else None,
        track_errors=True,
        track_duration=True,
        track_count=True,
        **labels
    )


def track_port(
    metrics: TrackMetrics,
    name: str | None = None,
    **labels: str
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator specifically for Port instrumentation.

    Convenience wrapper around track_metrics with Port-specific naming.

    :param metrics: TrackMetrics instance
    :type metrics: TrackMetrics
    :param name: Port name (defaults to class name)
    :type name: Optional[str]
    :param labels: Additional labels
    :type labels: str
    :return: Decorated function
    :rtype: Callable

    Example::

        metrics = TrackMetrics()

        class UserRepositoryPort(PortBase):
            @track_port(metrics, name="user_repository")
            def find_by_email(self, email: str) -> Optional[User]:
                # ... implementation ...
                return user

        # Metrics generated:
        # - port.user_repository.count
        # - port.user_repository.duration_ms
        # - port.user_repository.success
        # - port.user_repository.errors
    """
    return track_metrics(
        metrics=metrics,
        name=f"port.{name}" if name else None,
        track_errors=True,
        track_duration=True,
        track_count=True,
        **labels
    )


def track_adapter(
    metrics: TrackMetrics,
    name: str | None = None,
    **labels: str
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator specifically for Adapter instrumentation.

    Convenience wrapper around track_metrics with Adapter-specific naming.

    :param metrics: TrackMetrics instance
    :type metrics: TrackMetrics
    :param name: Adapter name (defaults to class name)
    :type name: Optional[str]
    :param labels: Additional labels
    :type labels: str
    :return: Decorated function
    :rtype: Callable

    Example::

        metrics = TrackMetrics()

        class HTTPAdapter(AdapterBase):
            @track_adapter(metrics, name="http_request")
            def handle_request(self, request: Request) -> Response:
                # ... implementation ...
                return response

        # Metrics generated:
        # - adapter.http_request.count
        # - adapter.http_request.duration_ms
        # - adapter.http_request.success
        # - adapter.http_request.errors
    """
    return track_metrics(
        metrics=metrics,
        name=f"adapter.{name}" if name else None,
        track_errors=True,
        track_duration=True,
        track_count=True,
        **labels
    )
