"""
Distributed tracing interface (OpenTelemetry-compatible).

Provides abstract interface for distributed tracing, enabling request tracking
across service boundaries. Compatible with OpenTelemetry standards for
interoperability with existing tracing backends (Jaeger, Zipkin, etc.).

Philosophy:
    In distributed systems, understanding a single request often requires
    following it across multiple services, databases, and external APIs.
    Distributed tracing provides this visibility by:

    1. Creating spans for each operation
    2. Propagating context across boundaries
    3. Linking spans into complete traces
    4. Recording timing and metadata

    This enables answering questions like:
    - Where is time being spent?
    - Which service is causing errors?
    - How do requests flow through the system?

Use Cases:
    - Performance debugging in microservices
    - Understanding service dependencies
    - Identifying bottlenecks
    - Troubleshooting distributed failures
    - Capacity planning

Example::

    # Initialize tracer
    tracer = NoOpTracer()  # Or JaegerTracer(), ZipkinTracer(), etc.

    # Create span
    with tracer.start_span("process_request") as span:
        span.set_attribute("user_id", "123")
        span.set_attribute("endpoint", "/api/users")

        # Do work
        result = process_request()

        # Nested span
        with tracer.start_span("database_query") as db_span:
            db_span.set_attribute("query", "SELECT * FROM users")
            data = db.query("SELECT * FROM users")

:author: ForgeBase Development Team
:since: 2025-11-03
"""

import time
import uuid
from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class SpanKind(Enum):
    """
    Span kind enumeration.

    Defines the role of a span in a trace.
    """
    INTERNAL = "INTERNAL"  # Internal operation
    SERVER = "SERVER"  # Server handling a request
    CLIENT = "CLIENT"  # Client making a request
    PRODUCER = "PRODUCER"  # Message producer
    CONSUMER = "CONSUMER"  # Message consumer


class SpanStatus(Enum):
    """
    Span status enumeration.

    Indicates whether the span completed successfully.
    """
    UNSET = "UNSET"  # Status not set
    OK = "OK"  # Completed successfully
    ERROR = "ERROR"  # Completed with error


@dataclass
class Span:
    """
    Represents a single operation in a distributed trace.

    A span represents a unit of work or operation. It tracks:
    - When it started and ended
    - What operation it represents
    - Any errors that occurred
    - Metadata about the operation

    :ivar span_id: Unique span identifier
    :vartype span_id: str
    :ivar trace_id: Trace identifier (groups related spans)
    :vartype trace_id: str
    :ivar parent_span_id: Parent span identifier (if nested)
    :vartype parent_span_id: Optional[str]
    :ivar name: Operation name
    :vartype name: str
    :ivar kind: Span kind
    :vartype kind: SpanKind
    :ivar start_time: Start timestamp (seconds since epoch)
    :vartype start_time: float
    :ivar end_time: End timestamp (seconds since epoch)
    :vartype end_time: Optional[float]
    :ivar status: Span status
    :vartype status: SpanStatus
    :ivar attributes: Span attributes/tags
    :vartype attributes: Dict[str, Any]
    :ivar events: Span events (logs within span)
    :vartype events: List[Dict[str, Any]]
    """

    span_id: str
    trace_id: str
    name: str
    parent_span_id: str | None = None
    kind: SpanKind = SpanKind.INTERNAL
    start_time: float = field(default_factory=time.time)
    end_time: float | None = None
    status: SpanStatus = SpanStatus.UNSET
    attributes: dict[str, Any] = field(default_factory=dict)
    events: list[dict[str, Any]] = field(default_factory=list)

    def set_attribute(self, key: str, value: Any) -> None:
        """
        Set span attribute.

        Attributes are key-value pairs that provide context about the operation.

        :param key: Attribute name
        :type key: str
        :param value: Attribute value
        :type value: Any

        Example::

            span.set_attribute("http.method", "GET")
            span.set_attribute("http.status_code", 200)
            span.set_attribute("user.id", "123")
        """
        self.attributes[key] = value

    def add_event(self, name: str, attributes: dict[str, Any] | None = None) -> None:
        """
        Add event to span.

        Events represent significant points in the span's lifetime.

        :param name: Event name
        :type name: str
        :param attributes: Event attributes
        :type attributes: Optional[Dict[str, Any]]

        Example::

            span.add_event("cache_miss")
            span.add_event("retry_attempt", {"attempt": 2})
        """
        event = {
            'name': name,
            'timestamp': time.time(),
            'attributes': attributes or {}
        }
        self.events.append(event)

    def set_status(self, status: SpanStatus, description: str | None = None) -> None:
        """
        Set span status.

        :param status: Span status
        :type status: SpanStatus
        :param description: Optional status description
        :type description: Optional[str]
        """
        self.status = status
        if description:
            self.set_attribute("status.description", description)

    def end(self) -> None:
        """End the span and record end time."""
        if self.end_time is None:
            self.end_time = time.time()

    def duration_ms(self) -> float:
        """
        Get span duration in milliseconds.

        :return: Duration in milliseconds
        :rtype: float
        """
        if self.end_time is None:
            return (time.time() - self.start_time) * 1000
        return (self.end_time - self.start_time) * 1000


class TracerPort(ABC):
    """
    Abstract interface for distributed tracing.

    This port defines the contract for tracing implementations. By programming
    against this interface, applications can switch between different tracing
    backends (Jaeger, Zipkin, OpenTelemetry, etc.) without code changes.

    Interface Design:
        - Compatible with OpenTelemetry Tracing API
        - Context propagation (inject/extract)
        - Span lifecycle management
        - Baggage support for cross-service data

    Implementations should:
        - Be thread-safe
        - Support context propagation
        - Handle errors gracefully (don't break application)
        - Export spans to tracing backend

    Example Implementation::

        class JaegerTracer(TracerPort):
            def __init__(self, service_name: str, jaeger_endpoint: str):
                self.service_name = service_name
                self.endpoint = jaeger_endpoint
                self.current_span = None

            def start_span(self, name: str, **attributes) -> Span:
                span = Span(
                    span_id=str(uuid.uuid4()),
                    trace_id=self.current_trace_id or str(uuid.uuid4()),
                    name=name
                )
                for key, value in attributes.items():
                    span.set_attribute(key, value)
                return span

            # ... other methods
    """

    @abstractmethod
    def start_span(
        self,
        name: str,
        kind: SpanKind = SpanKind.INTERNAL,
        **attributes: Any
    ) -> Span:
        """
        Start a new span.

        :param name: Span name (operation name)
        :type name: str
        :param kind: Span kind
        :type kind: SpanKind
        :param attributes: Initial span attributes
        :type attributes: Any
        :return: Started span
        :rtype: Span

        Example::

            span = tracer.start_span(
                "http_request",
                kind=SpanKind.CLIENT,
                http_method="GET",
                http_url="/api/users"
            )
        """
        pass

    @abstractmethod
    def current_span(self) -> Span | None:
        """
        Get current active span.

        :return: Current span or None
        :rtype: Optional[Span]
        """
        pass

    @abstractmethod
    def inject_context(self) -> dict[str, str]:
        """
        Inject trace context for propagation.

        Returns a dictionary of headers/metadata that should be propagated
        to downstream services to maintain trace context.

        :return: Context headers for propagation
        :rtype: Dict[str, str]

        Example::

            # Inject context into HTTP headers
            context = tracer.inject_context()
            headers = {
                'X-Trace-Id': context['traceparent'],
                # ... other headers
            }
            response = requests.get(url, headers=headers)
        """
        pass

    @abstractmethod
    def extract_context(self, carrier: dict[str, str]) -> None:
        """
        Extract trace context from propagated metadata.

        Reads trace context from incoming headers/metadata to continue
        an existing trace.

        :param carrier: Context carrier (headers, metadata)
        :type carrier: Dict[str, str]

        Example::

            # Extract context from HTTP headers
            tracer.extract_context(request.headers)
            # Now spans will be part of the incoming trace
        """
        pass


class NoOpTracer(TracerPort):
    """
    No-operation tracer that discards all spans.

    Useful for testing or when tracing should be completely disabled.
    Implements the Null Object pattern for tracing.

    Example::

        # Disable tracing in tests
        tracer = NoOpTracer()
        with tracer.start_span("operation") as span:
            # Span is created but discarded
            do_work()
    """

    def start_span(
        self,
        name: str,
        kind: SpanKind = SpanKind.INTERNAL,
        **attributes: Any
    ) -> Span:
        """Create span that will be discarded."""
        return Span(
            span_id=str(uuid.uuid4()),
            trace_id=str(uuid.uuid4()),
            name=name,
            kind=kind,
            attributes=attributes
        )

    def current_span(self) -> Span | None:
        """No current span in NoOp tracer."""
        return None

    def inject_context(self) -> dict[str, str]:
        """Return empty context."""
        return {}

    def extract_context(self, carrier: dict[str, str]) -> None:
        """Ignore context extraction."""
        pass

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        pass


class InMemoryTracer(TracerPort):
    """
    In-memory tracer for testing and development.

    Stores spans in memory for inspection. Useful for:
    - Testing trace generation
    - Development without tracing backend
    - Debugging trace structure

    :ivar spans: List of completed spans
    :vartype spans: List[Span]
    :ivar _current_span: Currently active span
    :vartype _current_span: Optional[Span]
    :ivar _trace_id: Current trace ID
    :vartype _trace_id: Optional[str]

    Example::

        tracer = InMemoryTracer()

        with tracer.start_span("operation") as span:
            do_work()

        # Inspect collected spans
        for span in tracer.get_spans():
            print(f"{span.name}: {span.duration_ms()}ms")
    """

    def __init__(self):
        """Initialize in-memory tracer."""
        self.spans: list[Span] = []
        self._current_span: Span | None = None
        self._trace_id: str | None = None

    def start_span(
        self,
        name: str,
        kind: SpanKind = SpanKind.INTERNAL,
        **attributes: Any
    ) -> Span:
        """Start new span and track it."""
        # Generate or reuse trace ID
        if not self._trace_id:
            self._trace_id = str(uuid.uuid4())

        # Create span
        span = Span(
            span_id=str(uuid.uuid4()),
            trace_id=self._trace_id,
            name=name,
            kind=kind,
            parent_span_id=self._current_span.span_id if self._current_span else None,
            attributes=attributes
        )

        # Set as current span
        self._current_span = span

        return span

    @contextmanager
    def span(
        self,
        name: str,
        kind: SpanKind = SpanKind.INTERNAL,
        **attributes: Any
    ):
        """
        Context manager for automatic span lifecycle.

        :param name: Span name
        :type name: str
        :param kind: Span kind
        :type kind: SpanKind
        :param attributes: Span attributes
        :type attributes: Any
        :yield: Span

        Example::

            with tracer.span("database_query", operation="SELECT"):
                result = db.query("SELECT * FROM users")
        """
        span = self.start_span(name, kind, **attributes)
        try:
            yield span
        except Exception as e:
            span.set_status(SpanStatus.ERROR, str(e))
            span.set_attribute("exception.type", type(e).__name__)
            span.set_attribute("exception.message", str(e))
            raise
        finally:
            span.end()
            self.spans.append(span)
            # Restore parent as current
            self._current_span = None  # Simplified for in-memory

    def current_span(self) -> Span | None:
        """Get current active span."""
        return self._current_span

    def inject_context(self) -> dict[str, str]:
        """Inject current trace context."""
        if not self._trace_id:
            return {}

        # W3C Trace Context format
        return {
            'traceparent': f"00-{self._trace_id}-{self._current_span.span_id if self._current_span else '0' * 16}-01"
        }

    def extract_context(self, carrier: dict[str, str]) -> None:
        """Extract trace context from carrier."""
        traceparent = carrier.get('traceparent')
        if traceparent:
            # Parse W3C Trace Context: version-trace_id-span_id-flags
            parts = traceparent.split('-')
            if len(parts) >= 2:
                self._trace_id = parts[1]

    def get_spans(self) -> list[Span]:
        """
        Get all collected spans.

        :return: List of spans
        :rtype: List[Span]
        """
        return self.spans.copy()

    def clear(self) -> None:
        """Clear all collected spans."""
        self.spans.clear()
        self._current_span = None
        self._trace_id = None

    def __repr__(self) -> str:
        """String representation."""
        return f"<InMemoryTracer spans={len(self.spans)}>"
