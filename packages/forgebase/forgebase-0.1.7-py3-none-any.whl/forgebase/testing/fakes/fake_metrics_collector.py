"""
In-memory metrics collector for testing.

Provides a fake metrics collector that captures metrics without overhead
for testing instrumentation and observability. Compatible with TrackMetrics
interface.

Philosophy:
    Production code should be instrumented with metrics, but tests shouldn't
    require a full metrics backend. FakeMetricsCollector provides zero-overhead
    metric collection that can be inspected programmatically in tests.

    Benefits:
    1. Zero overhead - no aggregation complexity
    2. Inspectable - query collected metrics
    3. Assertion helpers - built-in test utilities
    4. Compatible with TrackMetrics interface

Use Cases:
    - Verifying metrics are being collected
    - Testing @track_metrics decorators
    - Validating UseCase instrumentation
    - Checking metric values and labels

Example::

    from forgebase.testing.fakes.fake_metrics_collector import FakeMetricsCollector

    def test_usecase_metrics():
        # Setup
        metrics = FakeMetricsCollector()
        usecase = CreateUserUseCase(metrics=metrics)

        # Execute
        user = usecase.execute(data)

        # Verify metrics
        assert metrics.was_incremented('usecase.create_user.count')
        assert metrics.get_counter('usecase.create_user.success') == 1
        assert metrics.get_histogram_count('usecase.create_user.duration_ms') == 1

:author: ForgeBase Development Team
:since: 2025-11-03
"""

from contextlib import contextmanager
from typing import Any


class FakeMetricsCollector:
    """
    In-memory metrics collector for testing.

    Captures counters, gauges, and histogram values without overhead.
    Provides inspection methods for test assertions.

    Features:
        - Compatible with TrackMetrics interface
        - Assertion helpers
        - Label tracking
        - Reset between tests

    :ivar _counters: Counter values storage
    :vartype _counters: Dict[str, int]
    :ivar _gauges: Gauge values storage
    :vartype _gauges: Dict[str, float]
    :ivar _histograms: Histogram values storage
    :vartype _histograms: Dict[str, List[float]]

    Example::

        metrics = FakeMetricsCollector()

        # Increment counter
        metrics.increment('requests.total')
        metrics.increment('requests.total')

        # Set gauge
        metrics.gauge('memory.used_mb', 512.5)

        # Record histogram
        metrics.histogram('request.duration_ms', 123.4)

        # Query
        assert metrics.get_counter('requests.total') == 2
        assert metrics.get_gauge('memory.used_mb') == 512.5
        assert metrics.get_histogram_count('request.duration_ms') == 1
    """

    def __init__(self):
        """Initialize empty metrics storage."""
        self._counters: dict[str, int] = {}
        self._gauges: dict[str, float] = {}
        self._histograms: dict[str, list[float]] = {}
        self._labels: dict[str, dict[str, Any]] = {}

    def increment(self, name: str, amount: int = 1, **labels: str) -> None:
        """
        Increment a counter.

        :param name: Counter name
        :type name: str
        :param amount: Amount to increment (default: 1)
        :type amount: int
        :param labels: Optional labels
        :type labels: str

        Example::

            metrics.increment('requests.total')
            metrics.increment('bytes.sent', amount=1024)
            metrics.increment('requests', endpoint='/api/users', method='GET')
        """
        key = self._make_key(name, labels)
        self._counters[key] = self._counters.get(key, 0) + amount

        if labels:
            self._labels[key] = labels

    def gauge(self, name: str, value: float, **labels: str) -> None:
        """
        Set a gauge value.

        :param name: Gauge name
        :type name: str
        :param value: Gauge value
        :type value: float
        :param labels: Optional labels
        :type labels: str

        Example::

            metrics.gauge('memory.used_mb', 512.5)
            metrics.gauge('connections', 42, pool='primary')
        """
        key = self._make_key(name, labels)
        self._gauges[key] = value

        if labels:
            self._labels[key] = labels

    def histogram(self, name: str, value: float, **labels: str) -> None:
        """
        Record a value in a histogram.

        :param name: Histogram name
        :type name: str
        :param value: Observed value
        :type value: float
        :param labels: Optional labels
        :type labels: str

        Example::

            metrics.histogram('request.duration_ms', 145.3)
            metrics.histogram('response.size_bytes', 4096)
        """
        key = self._make_key(name, labels)

        if key not in self._histograms:
            self._histograms[key] = []

        self._histograms[key].append(value)

        if labels:
            self._labels[key] = labels

    @contextmanager
    def timer(self, name: str, **labels: str):
        """
        Context manager for timing operations.

        :param name: Metric name
        :type name: str
        :param labels: Optional labels
        :type labels: str
        :yields: None

        Example::

            with metrics.timer('database.query'):
                result = db.execute(query)
        """
        import time

        start_time = time.time()
        try:
            yield
        finally:
            duration_ms = (time.time() - start_time) * 1000
            self.histogram(name, duration_ms, **labels)

    def _make_key(self, name: str, labels: dict[str, str]) -> str:
        """
        Create unique key for metric with labels.

        :param name: Metric name
        :type name: str
        :param labels: Labels dictionary
        :type labels: Dict[str, str]
        :return: Unique key
        :rtype: str
        """
        if not labels:
            return name

        label_str = ','.join(f'{k}={v}' for k, v in sorted(labels.items()))
        return f"{name}{{{label_str}}}"

    # Test assertion helpers

    def get_counter(self, name: str, **labels: str) -> int | None:
        """
        Get counter value.

        :param name: Counter name
        :type name: str
        :param labels: Optional labels to match
        :type labels: str
        :return: Counter value or None if not found
        :rtype: Optional[int]

        Example::

            count = metrics.get_counter('requests.total')
            assert count == 5

            labeled = metrics.get_counter('requests', endpoint='/api/users')
            assert labeled == 3
        """
        key = self._make_key(name, labels)
        return self._counters.get(key)

    def get_gauge(self, name: str, **labels: str) -> float | None:
        """
        Get gauge value.

        :param name: Gauge name
        :type name: str
        :param labels: Optional labels to match
        :type labels: str
        :return: Gauge value or None if not found
        :rtype: Optional[float]

        Example::

            memory = metrics.get_gauge('memory.used_mb')
            assert memory == 512.5
        """
        key = self._make_key(name, labels)
        return self._gauges.get(key)

    def get_histogram_values(self, name: str, **labels: str) -> list[float] | None:
        """
        Get histogram values.

        :param name: Histogram name
        :type name: str
        :param labels: Optional labels to match
        :type labels: str
        :return: List of values or None if not found
        :rtype: Optional[List[float]]

        Example::

            values = metrics.get_histogram_values('request.duration_ms')
            assert len(values) == 10
            assert max(values) < 1000  # All under 1s
        """
        key = self._make_key(name, labels)
        return self._histograms.get(key)

    def get_histogram_count(self, name: str, **labels: str) -> int:
        """
        Get count of histogram observations.

        :param name: Histogram name
        :type name: str
        :param labels: Optional labels to match
        :type labels: str
        :return: Number of observations
        :rtype: int

        Example::

            count = metrics.get_histogram_count('request.duration_ms')
            assert count == 10
        """
        values = self.get_histogram_values(name, **labels)
        return len(values) if values else 0

    def was_incremented(self, name: str, **labels: str) -> bool:
        """
        Check if counter was incremented (exists and > 0).

        :param name: Counter name
        :type name: str
        :param labels: Optional labels to match
        :type labels: str
        :return: True if counter was incremented
        :rtype: bool

        Example::

            assert metrics.was_incremented('requests.total')
            assert metrics.was_incremented('requests', method='POST')
        """
        value = self.get_counter(name, **labels)
        return value is not None and value > 0

    def was_recorded(self, name: str, **labels: str) -> bool:
        """
        Check if histogram had values recorded.

        :param name: Histogram name
        :type name: str
        :param labels: Optional labels to match
        :type labels: str
        :return: True if values were recorded
        :rtype: bool

        Example::

            assert metrics.was_recorded('request.duration_ms')
        """
        return self.get_histogram_count(name, **labels) > 0

    def assert_counter_equals(self, name: str, expected: int, **labels: str) -> None:
        """
        Assert counter has specific value.

        :param name: Counter name
        :type name: str
        :param expected: Expected value
        :type expected: int
        :param labels: Optional labels to match
        :type labels: str
        :raises AssertionError: If value doesn't match

        Example::

            metrics.assert_counter_equals('requests.total', 5)
            metrics.assert_counter_equals('errors', 0, severity='critical')
        """
        actual = self.get_counter(name, **labels)

        if actual is None:
            msg = f"Counter '{name}' was not incremented"
            if labels:
                msg += f" with labels {labels}"
            raise AssertionError(msg)

        if actual != expected:
            msg = f"Counter '{name}' expected {expected}, got {actual}"
            if labels:
                msg += f" (labels: {labels})"
            raise AssertionError(msg)

    def assert_counter_greater(self, name: str, threshold: int, **labels: str) -> None:
        """
        Assert counter is greater than threshold.

        :param name: Counter name
        :type name: str
        :param threshold: Minimum value (exclusive)
        :type threshold: int
        :param labels: Optional labels to match
        :type labels: str
        :raises AssertionError: If value is not greater

        Example::

            metrics.assert_counter_greater('requests.total', 0)
        """
        actual = self.get_counter(name, **labels)

        if actual is None:
            raise AssertionError(f"Counter '{name}' was not incremented")

        if actual <= threshold:
            raise AssertionError(
                f"Counter '{name}' expected > {threshold}, got {actual}"
            )

    def clear(self) -> None:
        """
        Clear all collected metrics.

        Example::

            def setUp(self):
                self.metrics = FakeMetricsCollector()

            def tearDown(self):
                self.metrics.clear()
        """
        self._counters.clear()
        self._gauges.clear()
        self._histograms.clear()
        self._labels.clear()

    def reset(self) -> None:
        """Alias for clear()."""
        self.clear()

    def report(self) -> dict[str, Any]:
        """
        Generate metrics report.

        Compatible with TrackMetrics.report() interface.

        :return: Metrics report
        :rtype: Dict[str, Any]

        Example::

            report = metrics.report()
            print(f"Counters: {report['counters']}")
            print(f"Gauges: {report['gauges']}")
        """
        return {
            'counters': dict(self._counters),
            'gauges': dict(self._gauges),
            'histograms': {
                name: {
                    'count': len(values),
                    'sum': sum(values),
                    'mean': sum(values) / len(values) if values else 0,
                    'min': min(values) if values else 0,
                    'max': max(values) if values else 0,
                }
                for name, values in self._histograms.items()
            }
        }

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"<FakeMetricsCollector "
            f"counters={len(self._counters)} "
            f"gauges={len(self._gauges)} "
            f"histograms={len(self._histograms)}>"
        )
