"""Metrics export for monitoring integration."""

import logging
from typing import Any

from wistx_mcp.tools.lib.metrics import get_metrics, get_tool_metrics

logger = logging.getLogger(__name__)


def export_prometheus_metrics() -> str:
    """Export metrics in Prometheus format.

    Returns:
        Prometheus metrics string
    """
    lines = []
    all_metrics = get_metrics()

    for tool_name, metrics in all_metrics.items():
        name_safe = tool_name.replace("-", "_").replace(".", "_")

        lines.append(f'# HELP wistx_tool_calls_total Total number of tool calls')
        lines.append(f'# TYPE wistx_tool_calls_total counter')
        lines.append(f'wistx_tool_calls_total{{tool="{tool_name}"}} {metrics.call_count}')

        lines.append(f'# HELP wistx_tool_success_total Total number of successful tool calls')
        lines.append(f'# TYPE wistx_tool_success_total counter')
        lines.append(f'wistx_tool_success_total{{tool="{tool_name}"}} {metrics.success_count}')

        lines.append(f'# HELP wistx_tool_errors_total Total number of failed tool calls')
        lines.append(f'# TYPE wistx_tool_errors_total counter')
        lines.append(f'wistx_tool_errors_total{{tool="{tool_name}"}} {metrics.error_count}')

        lines.append(f'# HELP wistx_tool_duration_seconds Tool execution duration in seconds')
        lines.append(f'# TYPE wistx_tool_duration_seconds histogram')
        lines.append(f'wistx_tool_duration_seconds_sum{{tool="{tool_name}"}} {metrics.total_duration}')
        lines.append(f'wistx_tool_duration_seconds_count{{tool="{tool_name}"}} {metrics.call_count}')

        if metrics.call_count > 0:
            lines.append(f'wistx_tool_duration_seconds_avg{{tool="{tool_name}"}} {metrics.average_duration}')
            lines.append(f'wistx_tool_duration_seconds_min{{tool="{tool_name}"}} {metrics.min_duration}')
            lines.append(f'wistx_tool_duration_seconds_max{{tool="{tool_name}"}} {metrics.max_duration}')

        lines.append(f'# HELP wistx_tool_success_rate Tool success rate (0.0-1.0)')
        lines.append(f'# TYPE wistx_tool_success_rate gauge')
        lines.append(f'wistx_tool_success_rate{{tool="{tool_name}"}} {metrics.success_rate}')

    return "\n".join(lines)


def export_json_metrics() -> dict[str, Any]:
    """Export metrics as JSON.

    Returns:
        Dictionary with metrics data
    """
    all_metrics = get_metrics()
    return {
        "tools": {
            tool_name: {
                "call_count": metrics.call_count,
                "success_count": metrics.success_count,
                "error_count": metrics.error_count,
                "total_duration": metrics.total_duration,
                "average_duration": metrics.average_duration,
                "min_duration": metrics.min_duration if metrics.min_duration != float("inf") else None,
                "max_duration": metrics.max_duration,
                "success_rate": metrics.success_rate,
                "last_call_time": metrics.last_call_time.isoformat() if metrics.last_call_time else None,
                "error_count_recent": len(metrics.errors),
            }
            for tool_name, metrics in all_metrics.items()
        }
    }


def export_summary_metrics() -> dict[str, Any]:
    """Export summary metrics.

    Returns:
        Dictionary with summary statistics
    """
    all_metrics = get_metrics()

    total_calls = sum(m.call_count for m in all_metrics.values())
    total_success = sum(m.success_count for m in all_metrics.values())
    total_errors = sum(m.error_count for m in all_metrics.values())
    total_duration = sum(m.total_duration for m in all_metrics.values())

    return {
        "summary": {
            "total_tools": len(all_metrics),
            "total_calls": total_calls,
            "total_success": total_success,
            "total_errors": total_errors,
            "overall_success_rate": total_success / total_calls if total_calls > 0 else 0.0,
            "average_duration": total_duration / total_calls if total_calls > 0 else 0.0,
        },
        "by_tool": {
            tool_name: {
                "calls": metrics.call_count,
                "success_rate": metrics.success_rate,
                "avg_duration": metrics.average_duration,
            }
            for tool_name, metrics in all_metrics.items()
        },
    }

