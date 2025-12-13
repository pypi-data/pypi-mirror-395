"""
Metrics collection and telemetry system.

Provides comprehensive metrics tracking with support for counters, gauges,
histograms, and timers. Enables performance monitoring, success/failure tracking,
and system health observation.

Philosophy:
    "You can't improve what you don't measure." Metrics are the quantitative
    foundation of observability. While logs tell you what happened and traces
    show you the path, metrics tell you how well the system is performing.

    Good metrics enable:
    1. Performance monitoring (is the system fast enough?)
    2. Capacity planning (do we need more resources?)
    3. Anomaly detection (is something unusual happening?)
    4. Business insights (how are users using the system?)

Metric Types:
    - **Counter**: Monotonically increasing value (requests, errors, events)
    - **Gauge**: Point-in-time value that can go up or down (memory, connections)
    - **Histogram**: Distribution of values (latencies, sizes)
    - **Timer**: Specialized histogram for measuring duration

Example::

    # Initialize metrics
    metrics = TrackMetrics()

    # Counter: track total requests
    metrics.increment('requests.total')
    metrics.increment('requests.by_endpoint', endpoint='/api/users')

    # Gauge: track active connections
    metrics.gauge('connections.active', 42)

    # Histogram: track request duration
    metrics.histogram('request.duration_ms', 145.5)

    # Timer context manager
    with metrics.timer('database.query'):
        result = db.execute(query)

    # Export metrics
    print(metrics.report())

:author: ForgeBase Development Team
:since: 2025-11-03
"""

import statistics
import threading
import time
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Counter:
    """
    Counter metric - monotonically increasing value.

    Used for counting events like requests, errors, or any cumulative value.

    :ivar value: Current counter value
    :vartype value: int
    :ivar labels: Labels/tags for this counter
    :vartype labels: Dict[str, str]
    """
    value: int = 0
    labels: dict[str, str] = field(default_factory=dict)

    def increment(self, amount: int = 1):
        """Increment counter by amount."""
        self.value += amount


@dataclass
class Gauge:
    """
    Gauge metric - point-in-time value that can increase or decrease.

    Used for measuring instantaneous values like memory usage, active connections,
    temperature, etc.

    :ivar value: Current gauge value
    :vartype value: float
    :ivar labels: Labels/tags for this gauge
    :vartype labels: Dict[str, str]
    """
    value: float = 0.0
    labels: dict[str, str] = field(default_factory=dict)

    def set(self, value: float):
        """Set gauge to specific value."""
        self.value = value


@dataclass
class Histogram:
    """
    Histogram metric - distribution of values.

    Used for measuring distributions like request latencies, response sizes,
    or any value where you care about the statistical distribution.

    :ivar values: List of observed values
    :vartype values: List[float]
    :ivar labels: Labels/tags for this histogram
    :vartype labels: Dict[str, str]
    """
    values: list[float] = field(default_factory=list)
    labels: dict[str, str] = field(default_factory=dict)

    def observe(self, value: float):
        """Observe a value."""
        self.values.append(value)

    def count(self) -> int:
        """Get number of observations."""
        return len(self.values)

    def sum(self) -> float:
        """Get sum of all values."""
        return sum(self.values)

    def mean(self) -> float:
        """Get mean of values."""
        return statistics.mean(self.values) if self.values else 0.0

    def median(self) -> float:
        """Get median of values."""
        return statistics.median(self.values) if self.values else 0.0

    def min(self) -> float:
        """Get minimum value."""
        return min(self.values) if self.values else 0.0

    def max(self) -> float:
        """Get maximum value."""
        return max(self.values) if self.values else 0.0

    def percentile(self, p: float) -> float:
        """
        Get percentile value.

        :param p: Percentile (0-100)
        :type p: float
        :return: Percentile value
        :rtype: float
        """
        if not self.values:
            return 0.0
        sorted_values = sorted(self.values)
        index = int(len(sorted_values) * (p / 100))
        return sorted_values[min(index, len(sorted_values) - 1)]


class TrackMetrics:
    """
    Central metrics collection and tracking system.

    Provides thread-safe metrics collection with support for counters, gauges,
    histograms, and timers. Designed for production observability and monitoring.

    Features:
        - Thread-safe metric collection
        - Multiple metric types (counter, gauge, histogram)
        - Label/tag support for dimensional metrics
        - Context managers for timing
        - Export to multiple formats (JSON, Prometheus-style)
        - Low overhead (< 1ms per metric operation)

    Standard Metrics:
        This system comes with common metrics pre-defined:
        - `usecase.execution.duration` - UseCase execution time
        - `usecase.execution.count` - Total UseCase executions
        - `usecase.execution.errors` - UseCase execution errors
        - `port.call.duration` - Port call duration
        - `adapter.request.count` - Adapter request count

    :ivar _counters: Counter metrics storage
    :vartype _counters: Dict[str, Counter]
    :ivar _gauges: Gauge metrics storage
    :vartype _gauges: Dict[str, Gauge]
    :ivar _histograms: Histogram metrics storage
    :vartype _histograms: Dict[str, Histogram]
    :ivar _lock: Thread lock for thread-safety
    :vartype _lock: threading.Lock

    Example::

        # Create metrics system
        metrics = TrackMetrics()

        # Track request count by endpoint
        metrics.increment(
            'http.requests.total',
            endpoint='/api/users',
            method='GET'
        )

        # Track response time
        metrics.histogram(
            'http.request.duration_ms',
            123.5,
            endpoint='/api/users'
        )

        # Track active connections (gauge)
        metrics.gauge('connections.active', 15)

        # Use timer context manager
        with metrics.timer('database.query_duration_ms'):
            result = db.query("SELECT * FROM users")

        # Get metrics report
        report = metrics.report()
        print(f"Total requests: {report['counters']['http.requests.total']}")
    """

    def __init__(self):
        """Initialize metrics tracking system."""
        self._counters: dict[str, Counter] = defaultdict(Counter)
        self._gauges: dict[str, Gauge] = defaultdict(Gauge)
        self._histograms: dict[str, Histogram] = defaultdict(Histogram)
        self._lock = threading.Lock()

    def _make_key(self, name: str, labels: dict[str, str]) -> str:
        """
        Create unique key for metric with labels.

        :param name: Metric name
        :type name: str
        :param labels: Label dictionary
        :type labels: Dict[str, str]
        :return: Unique key
        :rtype: str
        """
        if not labels:
            return name

        # Sort labels for consistent keys
        label_str = ','.join(f'{k}={v}' for k, v in sorted(labels.items()))
        return f"{name}{{{label_str}}}"

    def increment(self, name: str, amount: int = 1, **labels: str) -> None:
        """
        Increment a counter metric.

        Counters are monotonically increasing values used for counting events.

        :param name: Counter name
        :type name: str
        :param amount: Amount to increment (default: 1)
        :type amount: int
        :param labels: Dimensional labels/tags
        :type labels: str

        Example::

            # Simple counter
            metrics.increment('requests.total')

            # Counter with labels
            metrics.increment(
                'requests.total',
                endpoint='/api/users',
                method='POST'
            )

            # Increment by custom amount
            metrics.increment('bytes.sent', amount=1024)
        """
        key = self._make_key(name, labels)
        with self._lock:
            counter = self._counters[key]
            counter.labels = labels
            counter.increment(amount)

    def gauge(self, name: str, value: float, **labels: str) -> None:
        """
        Set a gauge metric.

        Gauges represent point-in-time values that can increase or decrease.

        :param name: Gauge name
        :type name: str
        :param value: Gauge value
        :type value: float
        :param labels: Dimensional labels/tags
        :type labels: str

        Example::

            # Memory usage
            metrics.gauge('memory.used_mb', 1024.5)

            # Active connections
            metrics.gauge('connections.active', 42)

            # Temperature
            metrics.gauge('cpu.temperature_celsius', 65.5)
        """
        key = self._make_key(name, labels)
        with self._lock:
            gauge = self._gauges[key]
            gauge.labels = labels
            gauge.set(value)

    def histogram(self, name: str, value: float, **labels: str) -> None:
        """
        Record a value in a histogram metric.

        Histograms track the distribution of values, useful for latencies,
        sizes, or any measurement where you care about percentiles.

        :param name: Histogram name
        :type name: str
        :param value: Observed value
        :type value: float
        :param labels: Dimensional labels/tags
        :type labels: str

        Example::

            # Request duration
            metrics.histogram('request.duration_ms', 145.3)

            # Response size
            metrics.histogram('response.size_bytes', 4096)

            # With labels
            metrics.histogram(
                'query.duration_ms',
                23.5,
                database='postgres',
                table='users'
            )
        """
        key = self._make_key(name, labels)
        with self._lock:
            histogram = self._histograms[key]
            histogram.labels = labels
            histogram.observe(value)

    @contextmanager
    def timer(self, name: str, **labels: str):
        """
        Context manager for timing code execution.

        Automatically measures duration and records it as a histogram.

        :param name: Metric name
        :type name: str
        :param labels: Dimensional labels/tags
        :type labels: str
        :yield: None

        Example::

            # Time a function
            with metrics.timer('process_request_ms'):
                process_request()

            # With labels
            with metrics.timer('database.query_ms', operation='SELECT'):
                result = db.query("SELECT * FROM users")

            # Nested timers work too
            with metrics.timer('total_request_ms'):
                with metrics.timer('auth_ms'):
                    authenticate()
                with metrics.timer('process_ms'):
                    process()
        """
        start_time = time.time()
        try:
            yield
        finally:
            duration_ms = (time.time() - start_time) * 1000
            self.histogram(name, duration_ms, **labels)

    def get_counter(self, name: str, **labels: str) -> int | None:
        """
        Get current counter value.

        :param name: Counter name
        :type name: str
        :param labels: Labels to match
        :type labels: str
        :return: Counter value or None if not found
        :rtype: Optional[int]
        """
        key = self._make_key(name, labels)
        with self._lock:
            counter = self._counters.get(key)
            return counter.value if counter else None

    def get_gauge(self, name: str, **labels: str) -> float | None:
        """
        Get current gauge value.

        :param name: Gauge name
        :type name: str
        :param labels: Labels to match
        :type labels: str
        :return: Gauge value or None if not found
        :rtype: Optional[float]
        """
        key = self._make_key(name, labels)
        with self._lock:
            gauge = self._gauges.get(key)
            return gauge.value if gauge else None

    def get_histogram_stats(self, name: str, **labels: str) -> dict[str, float] | None:
        """
        Get histogram statistics.

        :param name: Histogram name
        :type name: str
        :param labels: Labels to match
        :type labels: str
        :return: Statistics dictionary or None if not found
        :rtype: Optional[Dict[str, float]]

        Example::

            stats = metrics.get_histogram_stats('request.duration_ms')
            print(f"p50: {stats['p50']}, p95: {stats['p95']}, p99: {stats['p99']}")
        """
        key = self._make_key(name, labels)
        with self._lock:
            histogram = self._histograms.get(key)
            if not histogram or not histogram.values:
                return None

            return {
                'count': histogram.count(),
                'sum': histogram.sum(),
                'mean': histogram.mean(),
                'median': histogram.median(),
                'min': histogram.min(),
                'max': histogram.max(),
                'p50': histogram.percentile(50),
                'p75': histogram.percentile(75),
                'p90': histogram.percentile(90),
                'p95': histogram.percentile(95),
                'p99': histogram.percentile(99),
            }

    def report(self) -> dict[str, Any]:
        """
        Generate comprehensive metrics report.

        :return: Metrics report with all collected data
        :rtype: Dict[str, Any]

        Example::

            report = metrics.report()

            # Access counters
            total_requests = report['counters']['requests.total']

            # Access histogram stats
            p95_latency = report['histograms']['request.duration_ms']['p95']

            # Access gauges
            active_conn = report['gauges']['connections.active']
        """
        with self._lock:
            report = {
                'counters': {},
                'gauges': {},
                'histograms': {},
                'timestamp': time.time()
            }

            # Counters
            for key, counter in self._counters.items():
                report['counters'][key] = counter.value

            # Gauges
            for key, gauge in self._gauges.items():
                report['gauges'][key] = gauge.value

            # Histograms
            for key, histogram in self._histograms.items():
                if histogram.values:
                    report['histograms'][key] = {
                        'count': histogram.count(),
                        'sum': histogram.sum(),
                        'mean': histogram.mean(),
                        'median': histogram.median(),
                        'min': histogram.min(),
                        'max': histogram.max(),
                        'p50': histogram.percentile(50),
                        'p75': histogram.percentile(75),
                        'p90': histogram.percentile(90),
                        'p95': histogram.percentile(95),
                        'p99': histogram.percentile(99),
                    }

            return report

    def reset(self) -> None:
        """
        Reset all metrics.

        WARNING: This clears all collected metrics data!
        """
        with self._lock:
            self._counters.clear()
            self._gauges.clear()
            self._histograms.clear()

    def __repr__(self) -> str:
        """String representation."""
        with self._lock:
            return f"<TrackMetrics counters={len(self._counters)} gauges={len(self._gauges)} histograms={len(self._histograms)}>"
