"""Prometheus metrics for hybrid retrieval services.

Provides observability for:
- Search latency and throughput
- Cache hit/miss rates
- Reranking performance
- Query routing decisions
- Research session metrics
"""

import logging
import time
from contextlib import contextmanager
from functools import wraps
from typing import Any, Callable

logger = logging.getLogger(__name__)

try:
    from prometheus_client import Counter, Gauge, Histogram, Summary
    PROMETHEUS_AVAILABLE = True
except ImportError:
    logger.warning("prometheus_client not installed. Metrics will be disabled.")
    PROMETHEUS_AVAILABLE = False
    Counter = None
    Gauge = None
    Histogram = None
    Summary = None


# =============================================================================
# Hybrid Retrieval Metrics
# =============================================================================

if PROMETHEUS_AVAILABLE:
    # Search metrics
    SEARCH_REQUESTS = Counter(
        "retrieval_search_requests_total",
        "Total search requests",
        ["search_type", "user_scope"],
    )
    SEARCH_LATENCY = Histogram(
        "retrieval_search_latency_seconds",
        "Search latency in seconds",
        ["search_type", "user_scope"],
        buckets=[0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
    )
    SEARCH_RESULTS_COUNT = Histogram(
        "retrieval_search_results_count",
        "Number of results returned",
        ["search_type"],
        buckets=[0, 1, 5, 10, 20, 50, 100],
    )
    
    # Cache metrics
    CACHE_HITS = Counter(
        "retrieval_cache_hits_total",
        "Total cache hits",
        ["cache_type"],
    )
    CACHE_MISSES = Counter(
        "retrieval_cache_misses_total",
        "Total cache misses",
        ["cache_type"],
    )
    CACHE_SIZE = Gauge(
        "retrieval_cache_size",
        "Current cache size",
        ["cache_type"],
    )
    
    # Reranking metrics
    RERANK_REQUESTS = Counter(
        "retrieval_rerank_requests_total",
        "Total reranking requests",
    )
    RERANK_LATENCY = Histogram(
        "retrieval_rerank_latency_seconds",
        "Reranking latency in seconds",
        buckets=[0.1, 0.25, 0.5, 1.0, 2.0, 5.0],
    )
    RERANK_INPUT_SIZE = Histogram(
        "retrieval_rerank_input_size",
        "Number of results sent for reranking",
        buckets=[1, 5, 10, 20, 50],
    )
    
    # Query routing metrics
    ROUTING_DECISIONS = Counter(
        "retrieval_routing_decisions_total",
        "Total routing decisions",
        ["target"],
    )
    
    # Research session metrics
    RESEARCH_SESSIONS = Counter(
        "retrieval_research_sessions_total",
        "Total research sessions created",
        ["status"],
    )
    RESEARCH_DURATION = Histogram(
        "retrieval_research_duration_seconds",
        "Research session duration in seconds",
        buckets=[1, 5, 10, 30, 60, 120, 300],
    )
    RESEARCH_SOURCES_FETCHED = Histogram(
        "retrieval_research_sources_fetched",
        "Number of sources fetched per research session",
        buckets=[1, 3, 5, 10, 20],
    )
    RESEARCH_CHUNKS_CREATED = Histogram(
        "retrieval_research_chunks_created",
        "Number of chunks created per research session",
        buckets=[10, 50, 100, 500, 1000],
    )
    
    # Evaluation metrics
    FEEDBACK_RECORDED = Counter(
        "retrieval_feedback_recorded_total",
        "Total relevance feedback recorded",
        ["relevance_score"],
    )
    
    # Error metrics
    RETRIEVAL_ERRORS = Counter(
        "retrieval_errors_total",
        "Total retrieval errors",
        ["error_type", "service"],
    )


def record_search(search_type: str, user_scope: str, latency: float, result_count: int):
    """Record search metrics."""
    if not PROMETHEUS_AVAILABLE:
        return
    SEARCH_REQUESTS.labels(search_type=search_type, user_scope=user_scope).inc()
    SEARCH_LATENCY.labels(search_type=search_type, user_scope=user_scope).observe(latency)
    SEARCH_RESULTS_COUNT.labels(search_type=search_type).observe(result_count)


def record_cache_hit(cache_type: str):
    """Record cache hit."""
    if not PROMETHEUS_AVAILABLE:
        return
    CACHE_HITS.labels(cache_type=cache_type).inc()


def record_cache_miss(cache_type: str):
    """Record cache miss."""
    if not PROMETHEUS_AVAILABLE:
        return
    CACHE_MISSES.labels(cache_type=cache_type).inc()


def set_cache_size(cache_type: str, size: int):
    """Set current cache size."""
    if not PROMETHEUS_AVAILABLE:
        return
    CACHE_SIZE.labels(cache_type=cache_type).set(size)


def record_rerank(latency: float, input_size: int):
    """Record reranking metrics."""
    if not PROMETHEUS_AVAILABLE:
        return
    RERANK_REQUESTS.inc()
    RERANK_LATENCY.observe(latency)
    RERANK_INPUT_SIZE.observe(input_size)


def record_routing_decision(target: str):
    """Record routing decision."""
    if not PROMETHEUS_AVAILABLE:
        return
    ROUTING_DECISIONS.labels(target=target).inc()


def record_research_session(status: str, duration: float = 0, sources: int = 0, chunks: int = 0):
    """Record research session metrics."""
    if not PROMETHEUS_AVAILABLE:
        return
    RESEARCH_SESSIONS.labels(status=status).inc()
    if duration > 0:
        RESEARCH_DURATION.observe(duration)
    if sources > 0:
        RESEARCH_SOURCES_FETCHED.observe(sources)
    if chunks > 0:
        RESEARCH_CHUNKS_CREATED.observe(chunks)


def record_feedback(relevance_score: int):
    """Record relevance feedback."""
    if not PROMETHEUS_AVAILABLE:
        return
    FEEDBACK_RECORDED.labels(relevance_score=str(relevance_score)).inc()


def record_error(error_type: str, service: str):
    """Record retrieval error."""
    if not PROMETHEUS_AVAILABLE:
        return
    RETRIEVAL_ERRORS.labels(error_type=error_type, service=service).inc()


@contextmanager
def timed_operation(metric_name: str, **labels):
    """Context manager for timing operations.

    Usage:
        with timed_operation("search", search_type="hybrid"):
            # do search
    """
    start = time.time()
    try:
        yield
    finally:
        duration = time.time() - start
        if metric_name == "search" and PROMETHEUS_AVAILABLE:
            SEARCH_LATENCY.labels(**labels).observe(duration)
        elif metric_name == "rerank" and PROMETHEUS_AVAILABLE:
            RERANK_LATENCY.observe(duration)


def track_latency(metric_name: str, **default_labels):
    """Decorator for tracking function latency.

    Usage:
        @track_latency("search", search_type="hybrid")
        async def search(self, query: str):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                duration = time.time() - start
                if metric_name == "search" and PROMETHEUS_AVAILABLE:
                    SEARCH_LATENCY.labels(**default_labels).observe(duration)
                elif metric_name == "rerank" and PROMETHEUS_AVAILABLE:
                    RERANK_LATENCY.observe(duration)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start = time.time()
            try:
                return func(*args, **kwargs)
            finally:
                duration = time.time() - start
                if metric_name == "search" and PROMETHEUS_AVAILABLE:
                    SEARCH_LATENCY.labels(**default_labels).observe(duration)
                elif metric_name == "rerank" and PROMETHEUS_AVAILABLE:
                    RERANK_LATENCY.observe(duration)

        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    return decorator


class RetrievalMetricsCollector:
    """Collector for retrieval metrics with structured logging."""

    def __init__(self, service_name: str):
        """Initialize collector.

        Args:
            service_name: Name of the service for logging context
        """
        self.service_name = service_name
        self.logger = logging.getLogger(f"retrieval.{service_name}")

    def log_search(
        self,
        query: str,
        search_type: str,
        user_id: str | None,
        result_count: int,
        latency_ms: float,
        cache_hit: bool = False,
    ):
        """Log search operation with structured data."""
        self.logger.info(
            "Search completed",
            extra={
                "event": "search",
                "query_length": len(query),
                "search_type": search_type,
                "user_id": user_id,
                "result_count": result_count,
                "latency_ms": latency_ms,
                "cache_hit": cache_hit,
            },
        )

        # Record Prometheus metrics
        user_scope = "user" if user_id else "global"
        record_search(search_type, user_scope, latency_ms / 1000, result_count)
        if cache_hit:
            record_cache_hit("results")
        else:
            record_cache_miss("results")

    def log_rerank(
        self,
        input_count: int,
        output_count: int,
        latency_ms: float,
    ):
        """Log reranking operation."""
        self.logger.info(
            "Reranking completed",
            extra={
                "event": "rerank",
                "input_count": input_count,
                "output_count": output_count,
                "latency_ms": latency_ms,
            },
        )
        record_rerank(latency_ms / 1000, input_count)

    def log_routing(self, query: str, target: str, reason: str):
        """Log routing decision."""
        self.logger.info(
            "Query routed",
            extra={
                "event": "routing",
                "query_length": len(query),
                "target": target,
                "reason": reason,
            },
        )
        record_routing_decision(target)

    def log_error(self, error_type: str, message: str, **context):
        """Log error with context."""
        self.logger.error(
            f"Retrieval error: {message}",
            extra={
                "event": "error",
                "error_type": error_type,
                **context,
            },
        )
        record_error(error_type, self.service_name)

