"""User preferences and state management."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class UserPreferences:
    """Manage user preferences and state."""

    def __init__(self, user_id: str):
        """Initialize user preferences.

        Args:
            user_id: User identifier
        """
        self.user_id = user_id
        self.preferences: dict[str, Any] = {}
        self.recent_tools: list[str] = []
        self.favorite_tools: list[str] = []
        self.tool_usage_stats: dict[str, int] = {}

    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get user preference.

        Args:
            key: Preference key
            default: Default value if not set

        Returns:
            Preference value or default
        """
        return self.preferences.get(key, default)

    def set_preference(self, key: str, value: Any) -> None:
        """Set user preference.

        Args:
            key: Preference key
            value: Preference value
        """
        self.preferences[key] = value

    def add_recent_tool(self, tool_name: str) -> None:
        """Add tool to recent tools list.

        Args:
            tool_name: Name of the tool
        """
        if tool_name in self.recent_tools:
            self.recent_tools.remove(tool_name)
        self.recent_tools.insert(0, tool_name)
        self.recent_tools = self.recent_tools[:20]

        self.tool_usage_stats[tool_name] = self.tool_usage_stats.get(tool_name, 0) + 1

    def get_recent_tools(self, limit: int = 5) -> list[str]:
        """Get recently used tools.

        Args:
            limit: Maximum number of tools to return

        Returns:
            List of recent tool names
        """
        return self.recent_tools[:limit]

    def get_most_used_tools(self, limit: int = 5) -> list[str]:
        """Get most frequently used tools.

        Args:
            limit: Maximum number of tools to return

        Returns:
            List of most used tool names
        """
        sorted_tools = sorted(
            self.tool_usage_stats.items(),
            key=lambda x: x[1],
            reverse=True,
        )
        return [tool_name for tool_name, _ in sorted_tools[:limit]]


class UserPreferencesManager:
    """Manage user preferences for multiple users."""

    def __init__(self):
        """Initialize preferences manager."""
        self.preferences: dict[str, UserPreferences] = {}

    def get_user_preferences(self, user_id: str) -> UserPreferences:
        """Get or create user preferences.

        Args:
            user_id: User identifier

        Returns:
            User preferences instance
        """
        if user_id not in self.preferences:
            self.preferences[user_id] = UserPreferences(user_id)
        return self.preferences[user_id]

    def get_preference(self, user_id: str, key: str, default: Any = None) -> Any:
        """Get user preference.

        Args:
            user_id: User identifier
            key: Preference key
            default: Default value

        Returns:
            Preference value or default
        """
        prefs = self.get_user_preferences(user_id)
        return prefs.get_preference(key, default)

    def set_preference(self, user_id: str, key: str, value: Any) -> None:
        """Set user preference.

        Args:
            user_id: User identifier
            key: Preference key
            value: Preference value
        """
        prefs = self.get_user_preferences(user_id)
        prefs.set_preference(key, value)


_global_preferences_manager: UserPreferencesManager | None = None


def get_user_preferences_manager() -> UserPreferencesManager:
    """Get global user preferences manager.

    Returns:
        UserPreferencesManager instance
    """
    global _global_preferences_manager
    if _global_preferences_manager is None:
        _global_preferences_manager = UserPreferencesManager()
    return _global_preferences_manager

