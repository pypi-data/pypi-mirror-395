"""Tool discovery and recommendation tools for agents."""

import logging
from typing import Any

from wistx_mcp.tools.lib.tool_recommender import ToolRecommender
from wistx_mcp.tools.lib.tool_categorizer import ToolCategorizer
from wistx_mcp.tools.lib.tool_descriptions import ToolDescriptionManager

logger = logging.getLogger(__name__)


async def get_recommended_tools(
    task_description: str,
    category: str | None = None,
    max_results: int = 10,
) -> dict[str, Any]:
    """Get recommended tools for a specific task.
    
    Args:
        task_description: Description of the task or goal
        category: Optional category filter (compliance, pricing, code, infrastructure, etc.)
        max_results: Maximum number of recommendations (default: 10)
    
    Returns:
        Dictionary with recommended tools and explanations
    """
    try:
        recommender = ToolRecommender()
        recommendations = recommender.recommend_tools(
            query=task_description,
            category=category,
        )
        
        # Limit results
        recommendations = recommendations[:max_results]
        
        # Add short descriptions
        for rec in recommendations:
            tool_name = rec["tool"]
            rec["short_description"] = ToolDescriptionManager.get_short_description(tool_name)
            rec["category"] = ToolCategorizer().get_tool_category(tool_name)
        
        return {
            "task": task_description,
            "category_filter": category,
            "recommendations": recommendations,
            "count": len(recommendations),
            "guidance": (
                "Use the recommended tools in the order shown. "
                "Each tool has a score (0-1) indicating relevance. "
                "Use wistx_get_tool_documentation for detailed information about any tool."
            ),
        }
    except Exception as e:
        logger.error(f"Error getting recommended tools: {e}", exc_info=True)
        return {
            "error": str(e),
            "task": task_description,
            "recommendations": [],
            "count": 0,
        }


async def list_tools_by_category(
    category: str,
    include_descriptions: bool = True,
) -> dict[str, Any]:
    """List all tools in a specific category.
    
    Args:
        category: Category name (compliance, pricing, code, infrastructure, knowledge, indexing, documentation, packages)
        include_descriptions: Whether to include short descriptions
    
    Returns:
        Dictionary with tools in category
    """
    try:
        categorizer = ToolCategorizer()
        
        # Get all tools in category
        tools_in_category = categorizer.get_tools_by_category(category)
        
        if not tools_in_category:
            return {
                "category": category,
                "tools": [],
                "count": 0,
                "available_categories": categorizer.get_all_categories(),
            }
        
        tools_data = []
        for tool_name in tools_in_category:
            tool_info = {
                "name": tool_name,
            }
            if include_descriptions:
                tool_info["short_description"] = ToolDescriptionManager.get_short_description(tool_name)
            tools_data.append(tool_info)
        
        return {
            "category": category,
            "tools": tools_data,
            "count": len(tools_data),
            "available_categories": categorizer.get_all_categories(),
        }
    except Exception as e:
        logger.error(f"Error listing tools by category: {e}", exc_info=True)
        return {
            "error": str(e),
            "category": category,
            "tools": [],
            "count": 0,
        }


async def get_tool_documentation(
    tool_name: str,
) -> dict[str, Any]:
    """Get detailed documentation for a specific tool.
    
    Args:
        tool_name: Name of the tool
    
    Returns:
        Dictionary with tool documentation
    """
    try:
        short_desc = ToolDescriptionManager.get_short_description(tool_name)
        detailed_desc = ToolDescriptionManager.get_detailed_description(tool_name)
        category = ToolCategorizer().get_tool_category(tool_name)
        
        return {
            "tool_name": tool_name,
            "category": category,
            "short_description": short_desc,
            "detailed_description": detailed_desc or "Detailed description not available yet.",
            "guidance": "Use this tool when you need detailed information about what a tool does and how to use it.",
        }
    except Exception as e:
        logger.error(f"Error getting tool documentation: {e}", exc_info=True)
        return {
            "error": str(e),
            "tool_name": tool_name,
        }

