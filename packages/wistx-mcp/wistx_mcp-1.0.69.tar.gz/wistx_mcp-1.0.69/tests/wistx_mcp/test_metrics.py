"""Unit tests for metrics collection."""

import pytest
from datetime import datetime

from wistx_mcp.tools.lib.metrics import (
    MetricsCollector,
    ToolMetrics,
    get_metrics,
    get_tool_metrics,
    reset_metrics,
)


def test_tool_metrics_initialization():
    """Test ToolMetrics initialization."""
    metrics = ToolMetrics(tool_name="test_tool")

    assert metrics.tool_name == "test_tool"
    assert metrics.call_count == 0
    assert metrics.success_count == 0
    assert metrics.error_count == 0
    assert metrics.total_duration == 0.0
    assert metrics.average_duration == 0.0
    assert metrics.success_rate == 0.0


def test_tool_metrics_record_call_success():
    """Test recording successful call."""
    metrics = ToolMetrics(tool_name="test_tool")

    metrics.record_call(duration=1.5, success=True)

    assert metrics.call_count == 1
    assert metrics.success_count == 1
    assert metrics.error_count == 0
    assert metrics.total_duration == 1.5
    assert metrics.min_duration == 1.5
    assert metrics.max_duration == 1.5
    assert metrics.average_duration == 1.5
    assert metrics.success_rate == 1.0


def test_tool_metrics_record_call_error():
    """Test recording failed call."""
    metrics = ToolMetrics(tool_name="test_tool")
    error = ValueError("Test error")

    metrics.record_call(duration=0.5, success=False, error=error)

    assert metrics.call_count == 1
    assert metrics.success_count == 0
    assert metrics.error_count == 1
    assert len(metrics.errors) == 1
    assert metrics.errors[0]["error_type"] == "ValueError"
    assert metrics.success_rate == 0.0


def test_tool_metrics_average_duration():
    """Test average duration calculation."""
    metrics = ToolMetrics(tool_name="test_tool")

    metrics.record_call(duration=1.0, success=True)
    metrics.record_call(duration=2.0, success=True)
    metrics.record_call(duration=3.0, success=True)

    assert metrics.average_duration == 2.0
    assert metrics.min_duration == 1.0
    assert metrics.max_duration == 3.0


def test_metrics_collector_get_metrics():
    """Test MetricsCollector get_metrics."""
    collector = MetricsCollector()

    metrics = collector.get_metrics("test_tool")

    assert metrics.tool_name == "test_tool"
    assert collector.metrics["test_tool"] == metrics


def test_metrics_collector_record_tool_call():
    """Test MetricsCollector record_tool_call."""
    collector = MetricsCollector()

    collector.record_tool_call("test_tool", duration=1.0, success=True)
    collector.record_tool_call("test_tool", duration=0.5, success=False)

    metrics = collector.get_metrics("test_tool")

    assert metrics.call_count == 2
    assert metrics.success_count == 1
    assert metrics.error_count == 1


def test_metrics_collector_reset():
    """Test MetricsCollector reset."""
    collector = MetricsCollector()

    collector.record_tool_call("test_tool", duration=1.0, success=True)
    assert len(collector.metrics) == 1

    collector.reset()
    assert len(collector.metrics) == 0


def test_get_tool_metrics():
    """Test get_tool_metrics function."""
    reset_metrics()

    metrics = get_tool_metrics("test_tool")
    metrics.record_call(duration=1.0, success=True)

    all_metrics = get_metrics()
    assert "test_tool" in all_metrics
    assert all_metrics["test_tool"].call_count == 1


def test_reset_metrics():
    """Test reset_metrics function."""
    metrics = get_tool_metrics("test_tool")
    metrics.record_call(duration=1.0, success=True)

    assert len(get_metrics()) > 0

    reset_metrics()

    assert len(get_metrics()) == 0

