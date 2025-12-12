"""Tool usage tracking for analytics and recommendations."""

import logging
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any

logger = logging.getLogger(__name__)


class ToolUsageTracker:
    """Track tool usage for analytics and recommendations."""

    def __init__(self):
        """Initialize usage tracker."""
        self.usage_history: list[dict[str, Any]] = []
        self.tool_counts: dict[str, int] = defaultdict(int)
        self.tool_sequences: list[list[str]] = []
        self.user_tool_history: dict[str, list[str]] = defaultdict(list)

    def track_usage(
        self,
        tool_name: str,
        user_id: str | None = None,
        success: bool = True,
        duration_ms: int | None = None,
    ) -> None:
        """Track tool usage.

        Args:
            tool_name: Name of the tool used
            user_id: User ID (optional)
            success: Whether tool call was successful
            duration_ms: Duration in milliseconds (optional)
        """
        usage_entry = {
            "tool_name": tool_name,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "success": success,
            "duration_ms": duration_ms,
        }

        self.usage_history.append(usage_entry)
        self.tool_counts[tool_name] += 1

        if user_id:
            self.user_tool_history[user_id].append(tool_name)
            if len(self.user_tool_history[user_id]) > 20:
                self.user_tool_history[user_id] = self.user_tool_history[user_id][-20:]

        if len(self.usage_history) > 10000:
            self.usage_history = self.usage_history[-10000:]

    def track_sequence(self, tool_sequence: list[str], user_id: str | None = None) -> None:
        """Track a sequence of tool calls.

        Args:
            tool_sequence: List of tool names in sequence
            user_id: User ID (optional)
        """
        if len(tool_sequence) > 1:
            self.tool_sequences.append(tool_sequence)
            if len(self.tool_sequences) > 1000:
                self.tool_sequences = self.tool_sequences[-1000:]

    def get_recently_used_tools(self, user_id: str | None = None, limit: int = 5) -> list[str]:
        """Get recently used tools.

        Args:
            user_id: User ID (optional, for user-specific history)
            limit: Maximum number of tools to return

        Returns:
            List of recently used tool names
        """
        if user_id and user_id in self.user_tool_history:
            return self.user_tool_history[user_id][-limit:]

        recent_usage = sorted(
            self.usage_history[-100:],
            key=lambda x: x["timestamp"],
            reverse=True,
        )
        tool_names = [u["tool_name"] for u in recent_usage]
        seen = set()
        unique_tools = []
        for tool in tool_names:
            if tool not in seen:
                seen.add(tool)
                unique_tools.append(tool)
                if len(unique_tools) >= limit:
                    break
        return unique_tools

    def get_tool_statistics(self, tool_name: str) -> dict[str, Any]:
        """Get statistics for a tool.

        Args:
            tool_name: Name of the tool

        Returns:
            Dictionary with tool statistics
        """
        tool_usages = [u for u in self.usage_history if u["tool_name"] == tool_name]

        if not tool_usages:
            return {
                "tool_name": tool_name,
                "total_uses": 0,
                "success_rate": 0.0,
                "average_duration_ms": None,
            }

        successful = sum(1 for u in tool_usages if u.get("success", True))
        durations = [u["duration_ms"] for u in tool_usages if u.get("duration_ms")]

        return {
            "tool_name": tool_name,
            "total_uses": len(tool_usages),
            "success_rate": successful / len(tool_usages) if tool_usages else 0.0,
            "average_duration_ms": sum(durations) / len(durations) if durations else None,
        }

    def get_common_sequences(self, tool_name: str, limit: int = 5) -> list[list[str]]:
        """Get common tool sequences starting with a tool.

        Args:
            tool_name: Starting tool name
            limit: Maximum number of sequences to return

        Returns:
            List of tool sequences
        """
        sequences_starting_with = [
            seq for seq in self.tool_sequences if seq and seq[0] == tool_name
        ]

        sequence_counts: dict[tuple, int] = defaultdict(int)
        for seq in sequences_starting_with:
            sequence_counts[tuple(seq)] += 1

        sorted_sequences = sorted(
            sequence_counts.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        return [list(seq) for seq, count in sorted_sequences[:limit]]

    def get_popular_tools(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get most popular tools.

        Args:
            limit: Maximum number of tools to return

        Returns:
            List of tool statistics sorted by usage
        """
        tool_stats = []
        for tool_name, count in sorted(
            self.tool_counts.items(),
            key=lambda x: x[1],
            reverse=True,
        ):
            stats = self.get_tool_statistics(tool_name)
            stats["total_uses"] = count
            tool_stats.append(stats)

        return tool_stats[:limit]


_usage_tracker: ToolUsageTracker | None = None


def get_usage_tracker() -> ToolUsageTracker:
    """Get global usage tracker instance.

    Returns:
        ToolUsageTracker instance
    """
    global _usage_tracker
    if _usage_tracker is None:
        _usage_tracker = ToolUsageTracker()
    return _usage_tracker

