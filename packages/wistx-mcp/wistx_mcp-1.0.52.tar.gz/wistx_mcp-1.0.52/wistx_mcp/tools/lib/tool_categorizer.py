"""Tool categorizer for organizing and discovering tools."""

from typing import Any

from wistx_mcp.tools.lib.tool_categories import (
    get_all_categories,
    get_category_info,
    get_category_tools,
    get_tool_category,
    search_tools_by_keyword,
)


class ToolCategorizer:
    """Categorize and organize MCP tools for efficient discovery."""

    @staticmethod
    def get_tool_category(tool_name: str) -> str | None:
        """Get category for a tool.

        Args:
            tool_name: Name of the tool

        Returns:
            Category name or None if not found
        """
        return get_tool_category(tool_name)

    @staticmethod
    def get_tools_by_category(category: str) -> list[str]:
        """Get all tools in a category.

        Args:
            category: Category name

        Returns:
            List of tool names in the category
        """
        return get_category_tools(category)

    @staticmethod
    def get_all_categories() -> dict[str, dict[str, Any]]:
        """Get all categories with metadata.

        Returns:
            Dictionary mapping category names to category metadata
        """
        return get_all_categories()

    @staticmethod
    def search_tools(query: str, category: str | None = None) -> list[str]:
        """Search for tools by query and optionally filter by category.

        Args:
            query: Search query (keyword or tool name)
            category: Optional category filter

        Returns:
            List of matching tool names
        """
        if category:
            category_tools = get_category_tools(category)
            matching = [t for t in category_tools if query.lower() in t.lower()]
            keyword_matches = search_tools_by_keyword(query)
            matching.extend([t for t in keyword_matches if t in category_tools])
            return list(set(matching))

        return search_tools_by_keyword(query)

    @staticmethod
    def get_category_summary() -> dict[str, Any]:
        """Get summary of all categories.

        Returns:
            Dictionary with category summaries
        """
        categories = get_all_categories()
        summary = {}

        for category_id, category_info in categories.items():
            summary[category_id] = {
                "name": category_info["name"],
                "description": category_info["description"],
                "tool_count": len(category_info.get("tools", [])),
                "tools": category_info.get("tools", []),
            }

        return summary

