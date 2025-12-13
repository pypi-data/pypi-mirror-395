"""Performance utilities and benchmarking."""

import asyncio
import logging
import time
from functools import wraps
from typing import Any, Callable

logger = logging.getLogger(__name__)


def benchmark(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to benchmark function execution time.

    Args:
        func: Function to benchmark

    Returns:
        Decorated function with benchmarking
    """

    @wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(
                "Function %s executed in %.3f seconds",
                func.__name__,
                duration,
            )
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.warning(
                "Function %s failed after %.3f seconds: %s",
                func.__name__,
                duration,
                e,
            )
            raise

    @wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(
                "Function %s executed in %.3f seconds",
                func.__name__,
                duration,
            )
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.warning(
                "Function %s failed after %.3f seconds: %s",
                func.__name__,
                duration,
                e,
            )
            raise

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper


async def measure_execution_time(coro: Callable[..., Any], *args: Any, **kwargs: Any) -> tuple[Any, float]:
    """Measure execution time of a coroutine.

    Args:
        coro: Coroutine to measure
        *args: Positional arguments
        **kwargs: Keyword arguments

    Returns:
        Tuple of (result, duration_in_seconds)
    """
    start_time = time.time()
    result = await coro(*args, **kwargs)
    duration = time.time() - start_time
    return result, duration


def get_performance_summary(metrics: dict[str, Any]) -> dict[str, Any]:
    """Generate performance summary from metrics.

    Args:
        metrics: Dictionary of metrics

    Returns:
        Performance summary dictionary
    """
    summary = {
        "total_tools": len(metrics),
        "total_calls": sum(m.call_count for m in metrics.values()),
        "total_errors": sum(m.error_count for m in metrics.values()),
        "average_duration": sum(m.average_duration for m in metrics.values()) / len(metrics) if metrics else 0.0,
        "slowest_tool": max(metrics.items(), key=lambda x: x[1].average_duration)[0] if metrics else None,
        "fastest_tool": min(metrics.items(), key=lambda x: x[1].average_duration)[0] if metrics else None,
        "most_called_tool": max(metrics.items(), key=lambda x: x[1].call_count)[0] if metrics else None,
    }
    return summary

