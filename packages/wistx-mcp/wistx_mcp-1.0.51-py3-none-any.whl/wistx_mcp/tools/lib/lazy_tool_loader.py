"""Lazy tool loading for progressive tool discovery."""

import logging
from typing import Any

from wistx_mcp.tools.lib.tool_categorizer import ToolCategorizer
from wistx_mcp.tools.lib.tool_descriptions import ToolDescriptionManager

logger = logging.getLogger(__name__)


class LazyToolLoader:
    """Load tools progressively based on category and usage patterns."""

    # Essential tools that should always be loaded
    ESSENTIAL_TOOLS = {
        "wistx_get_recommended_tools",
        "wistx_list_tools_by_category",
        "wistx_get_tool_documentation",
        "wistx_research_knowledge_base",
        "wistx_web_search",
    }

    # Tools by category for on-demand loading
    CATEGORY_TOOLS = {
        "compliance": [
            "wistx_get_compliance_requirements",
        ],
        "pricing": [
            "wistx_calculate_infrastructure_cost",
        ],
        "code": [
            "wistx_get_devops_infra_code_examples",
            "wistx_search_codebase",
            "wistx_regex_search",
        ],
        "filesystem": [
            "wistx_list_filesystem",
            "wistx_read_file_with_context",
        ],
        "context": [
            "wistx_save_context_with_analysis",
            "wistx_search_contexts_intelligently",
        ],
        "infrastructure": [
            "wistx_manage_infrastructure",
            "wistx_get_existing_infrastructure",
        ],
        "knowledge": [
            "wistx_research_knowledge_base",
        ],
        "indexing": [
            "wistx_index_repository",
        ],
        "documentation": [
            "wistx_generate_documentation",
            "wistx_design_architecture",
            "wistx_troubleshoot_issue",
        ],
        "packages": [
            "wistx_search_packages",
        ],
        "integration": [
            "wistx_manage_integration",
        ],
    }

    def __init__(self):
        """Initialize lazy tool loader."""
        self.categorizer = ToolCategorizer()
        self.loaded_categories = set()
        self.loaded_tools = set(self.ESSENTIAL_TOOLS)

    def get_essential_tools(self) -> list[str]:
        """Get essential tools that should always be loaded."""
        return list(self.ESSENTIAL_TOOLS)

    def load_category(self, category: str) -> list[str]:
        """Load all tools in a category.
        
        Args:
            category: Category name
            
        Returns:
            List of tool names in category
        """
        if category in self.loaded_categories:
            return self.CATEGORY_TOOLS.get(category, [])
        
        tools = self.CATEGORY_TOOLS.get(category, [])
        self.loaded_categories.add(category)
        self.loaded_tools.update(tools)
        
        logger.info(f"Loaded category '{category}' with {len(tools)} tools")
        return tools

    def load_tools_for_query(self, query: str) -> list[str]:
        """Load tools relevant to a query.
        
        Args:
            query: Search query or task description
            
        Returns:
            List of relevant tool names
        """
        matching_tools = self.categorizer.search_tools(query)
        self.loaded_tools.update(matching_tools)
        
        logger.info(f"Loaded {len(matching_tools)} tools for query: {query}")
        return matching_tools

    def get_loaded_tools(self) -> set[str]:
        """Get all currently loaded tools."""
        return self.loaded_tools.copy()

    def is_tool_loaded(self, tool_name: str) -> bool:
        """Check if a tool is loaded."""
        return tool_name in self.loaded_tools

    def load_all_tools(self) -> None:
        """Load all tools (for backward compatibility)."""
        for category in self.CATEGORY_TOOLS:
            self.load_category(category)
        logger.info(f"Loaded all {len(self.loaded_tools)} tools")

    def get_loading_stats(self) -> dict[str, Any]:
        """Get statistics about tool loading."""
        total_tools = sum(len(tools) for tools in self.CATEGORY_TOOLS.values())
        total_tools += len(self.ESSENTIAL_TOOLS)
        
        return {
            "essential_tools": len(self.ESSENTIAL_TOOLS),
            "loaded_tools": len(self.loaded_tools),
            "total_tools": total_tools,
            "loaded_categories": len(self.loaded_categories),
            "total_categories": len(self.CATEGORY_TOOLS),
            "loading_percentage": (len(self.loaded_tools) / total_tools * 100) if total_tools > 0 else 0,
        }

    def get_unloaded_categories(self) -> list[str]:
        """Get categories that haven't been loaded yet."""
        return [cat for cat in self.CATEGORY_TOOLS if cat not in self.loaded_categories]

    def get_category_for_tool(self, tool_name: str) -> str | None:
        """Get category for a tool."""
        return self.categorizer.get_tool_category(tool_name)

