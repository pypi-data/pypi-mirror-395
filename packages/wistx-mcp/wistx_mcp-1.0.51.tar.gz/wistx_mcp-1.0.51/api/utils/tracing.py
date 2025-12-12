"""Distributed tracing with OpenTelemetry."""

import logging
import uuid
import contextvars
from contextlib import contextmanager
from typing import Any, Iterator

correlation_id: contextvars.ContextVar[str | None] = contextvars.ContextVar("correlation_id", default=None)

try:
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.instrumentation.pymongo import PymongoInstrumentor
    from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
    from opentelemetry.trace import Status, StatusCode

    TRACING_AVAILABLE = True
except ImportError:
    TRACING_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("OpenTelemetry not installed. Tracing will be disabled.")

from api.config import settings

logger = logging.getLogger(__name__)

_tracer_provider: Any = None
_tracer: Any = None


def initialize_tracing(
    service_name: str = "wistx-api",
    otlp_endpoint: str | None = None,
    enabled: bool = True,
) -> None:
    """Initialize OpenTelemetry tracing.

    Args:
        service_name: Service name for traces
        otlp_endpoint: OTLP endpoint URL (e.g., http://localhost:4317)
        enabled: Whether tracing is enabled
    """
    global _tracer_provider, _tracer

    if not TRACING_AVAILABLE:
        logger.warning("OpenTelemetry not available, tracing disabled")
        return

    if not enabled:
        logger.info("Tracing disabled by configuration")
        return

    try:
        resource = Resource.create({
            "service.name": service_name,
            "service.version": settings.api_version,
        })

        tracer_provider = TracerProvider(resource=resource)
        trace.set_tracer_provider(tracer_provider)

        if otlp_endpoint:
            otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
            span_processor = BatchSpanProcessor(otlp_exporter)
            tracer_provider.add_span_processor(span_processor)
            logger.info("Tracing initialized with OTLP endpoint: %s", otlp_endpoint)
        else:
            logger.info("Tracing initialized (no OTLP endpoint, spans will be no-op)")

        _tracer_provider = tracer_provider
        _tracer = trace.get_tracer(__name__)

        FastAPIInstrumentor().instrument()
        PymongoInstrumentor().instrument()
        HTTPXClientInstrumentor().instrument()

        logger.info("OpenTelemetry tracing initialized successfully")
    except Exception as e:
        logger.error("Failed to initialize tracing: %s", e, exc_info=True)


def get_tracer() -> Any:
    """Get OpenTelemetry tracer instance.

    Returns:
        Tracer instance or None if tracing is not available
    """
    if not TRACING_AVAILABLE or _tracer is None:
        return None

    return _tracer


@contextmanager
def trace_span(
    name: str,
    attributes: dict[str, Any] | None = None,
) -> Iterator[Any]:
    """Create a trace span context manager.

    Args:
        name: Span name
        attributes: Optional span attributes

    Yields:
        Span instance
    """
    tracer = get_tracer()
    if not tracer:
        yield None
        return

    with tracer.start_as_current_span(name, attributes=attributes) as span:
        try:
            yield span
        except Exception as e:
            if span:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
            raise


def add_span_attribute(key: str, value: Any) -> None:
    """Add attribute to current span.

    Args:
        key: Attribute key
        value: Attribute value
    """
    span = trace.get_current_span()
    if span and span.is_recording():
        span.set_attribute(key, value)


def add_span_event(name: str, attributes: dict[str, Any] | None = None) -> None:
    """Add event to current span.

    Args:
        name: Event name
        attributes: Optional event attributes
    """
    span = trace.get_current_span()
    if span and span.is_recording():
        span.add_event(name, attributes=attributes or {})


def get_correlation_id() -> str:
    """Get or create correlation ID.

    Returns:
        Correlation ID string
    """
    cid = correlation_id.get()
    if not cid:
        cid = str(uuid.uuid4())
        correlation_id.set(cid)
    return cid


def set_correlation_id(cid: str) -> None:
    """Set correlation ID.

    Args:
        cid: Correlation ID string
    """
    correlation_id.set(cid)

