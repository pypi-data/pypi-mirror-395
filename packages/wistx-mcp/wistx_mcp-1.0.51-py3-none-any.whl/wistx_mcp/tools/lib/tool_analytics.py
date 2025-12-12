"""Tool usage analytics and performance tracking."""

import logging
import time
from collections import defaultdict
from typing import Any

logger = logging.getLogger(__name__)


class ToolAnalytics:
    """Track and analyze tool usage patterns and performance."""

    def __init__(self):
        """Initialize tool analytics."""
        self.tool_calls = defaultdict(int)
        self.tool_successes = defaultdict(int)
        self.tool_failures = defaultdict(int)
        self.tool_execution_times = defaultdict(list)
        self.tool_errors = defaultdict(list)
        self.last_reset = time.time()

    def record_tool_call(self, tool_name: str, success: bool = True, 
                        execution_time: float = 0.0, error: str | None = None) -> None:
        """Record a tool call.
        
        Args:
            tool_name: Name of the tool
            success: Whether the call succeeded
            execution_time: Time taken to execute in seconds
            error: Error message if failed
        """
        self.tool_calls[tool_name] += 1
        
        if success:
            self.tool_successes[tool_name] += 1
        else:
            self.tool_failures[tool_name] += 1
            if error:
                self.tool_errors[tool_name].append({
                    "error": error,
                    "timestamp": time.time(),
                })
        
        if execution_time > 0:
            self.tool_execution_times[tool_name].append(execution_time)
        
        logger.debug(f"Recorded call for {tool_name}: success={success}, time={execution_time}s")

    def get_tool_stats(self, tool_name: str) -> dict[str, Any]:
        """Get statistics for a specific tool.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Dictionary with tool statistics
        """
        total_calls = self.tool_calls.get(tool_name, 0)
        successes = self.tool_successes.get(tool_name, 0)
        failures = self.tool_failures.get(tool_name, 0)
        execution_times = self.tool_execution_times.get(tool_name, [])
        
        success_rate = (successes / total_calls * 100) if total_calls > 0 else 0
        avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
        
        return {
            "tool_name": tool_name,
            "total_calls": total_calls,
            "successes": successes,
            "failures": failures,
            "success_rate": success_rate,
            "avg_execution_time": avg_execution_time,
            "min_execution_time": min(execution_times) if execution_times else 0,
            "max_execution_time": max(execution_times) if execution_times else 0,
            "recent_errors": self.tool_errors.get(tool_name, [])[-5:],  # Last 5 errors
        }

    def get_all_stats(self) -> dict[str, Any]:
        """Get statistics for all tools.
        
        Returns:
            Dictionary with statistics for all tools
        """
        stats = {}
        for tool_name in self.tool_calls:
            stats[tool_name] = self.get_tool_stats(tool_name)
        
        return {
            "total_tools": len(stats),
            "tools": stats,
            "summary": self._get_summary_stats(),
        }

    def _get_summary_stats(self) -> dict[str, Any]:
        """Get summary statistics across all tools."""
        total_calls = sum(self.tool_calls.values())
        total_successes = sum(self.tool_successes.values())
        total_failures = sum(self.tool_failures.values())
        
        all_execution_times = []
        for times in self.tool_execution_times.values():
            all_execution_times.extend(times)
        
        overall_success_rate = (total_successes / total_calls * 100) if total_calls > 0 else 0
        avg_execution_time = sum(all_execution_times) / len(all_execution_times) if all_execution_times else 0
        
        return {
            "total_calls": total_calls,
            "total_successes": total_successes,
            "total_failures": total_failures,
            "overall_success_rate": overall_success_rate,
            "avg_execution_time": avg_execution_time,
            "uptime_seconds": time.time() - self.last_reset,
        }

    def get_top_tools(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get top tools by usage.
        
        Args:
            limit: Maximum number of tools to return
            
        Returns:
            List of top tools sorted by usage
        """
        tools = [(name, self.tool_calls[name]) for name in self.tool_calls]
        tools.sort(key=lambda x: x[1], reverse=True)
        
        return [
            {
                "tool_name": name,
                "calls": calls,
                "stats": self.get_tool_stats(name),
            }
            for name, calls in tools[:limit]
        ]

    def get_failing_tools(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get tools with highest failure rates.
        
        Args:
            limit: Maximum number of tools to return
            
        Returns:
            List of failing tools sorted by failure rate
        """
        tools = []
        for tool_name in self.tool_calls:
            stats = self.get_tool_stats(tool_name)
            if stats["total_calls"] > 0:
                tools.append((tool_name, stats["success_rate"]))
        
        tools.sort(key=lambda x: x[1])  # Sort by success rate (ascending)
        
        return [
            {
                "tool_name": name,
                "stats": self.get_tool_stats(name),
            }
            for name, _ in tools[:limit]
        ]

    def get_slowest_tools(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get slowest tools by average execution time.
        
        Args:
            limit: Maximum number of tools to return
            
        Returns:
            List of slowest tools sorted by execution time
        """
        tools = []
        for tool_name in self.tool_execution_times:
            times = self.tool_execution_times[tool_name]
            if times:
                avg_time = sum(times) / len(times)
                tools.append((tool_name, avg_time))
        
        tools.sort(key=lambda x: x[1], reverse=True)
        
        return [
            {
                "tool_name": name,
                "avg_execution_time": avg_time,
                "stats": self.get_tool_stats(name),
            }
            for name, avg_time in tools[:limit]
        ]

    def reset_stats(self) -> None:
        """Reset all statistics."""
        self.tool_calls.clear()
        self.tool_successes.clear()
        self.tool_failures.clear()
        self.tool_execution_times.clear()
        self.tool_errors.clear()
        self.last_reset = time.time()
        logger.info("Analytics statistics reset")

    def export_stats(self) -> dict[str, Any]:
        """Export all statistics for external storage.
        
        Returns:
            Dictionary with all statistics
        """
        return {
            "timestamp": time.time(),
            "uptime_seconds": time.time() - self.last_reset,
            "all_stats": self.get_all_stats(),
            "top_tools": self.get_top_tools(20),
            "failing_tools": self.get_failing_tools(10),
            "slowest_tools": self.get_slowest_tools(10),
        }

