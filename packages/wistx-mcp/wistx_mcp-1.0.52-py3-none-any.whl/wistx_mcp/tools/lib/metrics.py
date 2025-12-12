"""Metrics and observability for MCP tools."""

import logging
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from functools import wraps
from typing import Any, Callable

logger = logging.getLogger(__name__)


@dataclass
class ToolMetrics:
    """Metrics for a single tool."""

    tool_name: str
    call_count: int = 0
    success_count: int = 0
    error_count: int = 0
    total_duration: float = 0.0
    min_duration: float = float("inf")
    max_duration: float = 0.0
    last_call_time: datetime | None = None
    errors: list[dict[str, Any]] = field(default_factory=list)

    @property
    def average_duration(self) -> float:
        """Calculate average duration."""
        if self.call_count == 0:
            return 0.0
        return self.total_duration / self.call_count

    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.call_count == 0:
            return 0.0
        return self.success_count / self.call_count

    def record_call(self, duration: float, success: bool, error: Exception | None = None) -> None:
        """Record a tool call."""
        self.call_count += 1
        self.total_duration += duration
        self.min_duration = min(self.min_duration, duration)
        self.max_duration = max(self.max_duration, duration)
        self.last_call_time = datetime.now()

        if success:
            self.success_count += 1
        else:
            self.error_count += 1
            if error:
                self.errors.append({
                    "timestamp": datetime.now().isoformat(),
                    "error_type": type(error).__name__,
                    "error_message": str(error),
                })


class MetricsCollector:
    """Collector for tool metrics."""

    def __init__(self):
        """Initialize metrics collector."""
        self.metrics: dict[str, ToolMetrics] = defaultdict(lambda: ToolMetrics(tool_name=""))

    def get_metrics(self, tool_name: str) -> ToolMetrics:
        """Get metrics for a tool."""
        if tool_name not in self.metrics:
            self.metrics[tool_name] = ToolMetrics(tool_name=tool_name)
        return self.metrics[tool_name]

    def record_tool_call(
        self,
        tool_name: str,
        duration: float,
        success: bool,
        error: Exception | None = None,
    ) -> None:
        """Record a tool call."""
        metrics = self.get_metrics(tool_name)
        metrics.record_call(duration, success, error)

    def get_all_metrics(self) -> dict[str, ToolMetrics]:
        """Get all metrics."""
        return dict(self.metrics)

    def reset(self) -> None:
        """Reset all metrics."""
        self.metrics.clear()


_global_collector = MetricsCollector()


def track_tool_metrics(tool_name: str | None = None):
    """Decorator to track tool metrics.

    Args:
        tool_name: Name of the tool (defaults to function name)

    Returns:
        Decorated function
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        name = tool_name or func.__name__

        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            error: Exception | None = None
            success = False

            try:
                result = await func(*args, **kwargs)
                success = True
                return result
            except Exception as e:
                error = e
                raise
            finally:
                duration = time.time() - start_time
                _global_collector.record_tool_call(name, duration, success, error)

                logger.debug(
                    "Tool %s: duration=%.3fs, success=%s",
                    name,
                    duration,
                    success,
                )

        return wrapper

    return decorator


def get_metrics() -> dict[str, ToolMetrics]:
    """Get all collected metrics.

    Returns:
        Dictionary of tool metrics
    """
    return _global_collector.get_all_metrics()


def get_tool_metrics(tool_name: str) -> ToolMetrics:
    """Get metrics for a specific tool.

    Args:
        tool_name: Name of the tool

    Returns:
        Tool metrics
    """
    return _global_collector.get_metrics(tool_name)


def reset_metrics() -> None:
    """Reset all metrics."""
    _global_collector.reset()

