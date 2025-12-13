"""Tool recommendation system for suggesting relevant tools based on context."""

from typing import Any

from wistx_mcp.tools.lib.tool_categorizer import ToolCategorizer
from wistx_mcp.tools.lib.tool_relationships import (
    get_all_workflows,
    get_commonly_followed_by,
    get_prerequisites,
    get_tool_relationships,
)


class ToolRecommender:
    """Recommend tools based on context, usage patterns, and relationships."""

    def __init__(self):
        """Initialize tool recommender."""
        self.categorizer = ToolCategorizer()

    def recommend_tools(
        self,
        query: str | None = None,
        current_tool: str | None = None,
        category: str | None = None,
        recently_used: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Recommend tools based on context.

        Args:
            query: Search query or user intent
            current_tool: Currently used tool (for workflow continuation)
            category: Preferred category filter
            recently_used: List of recently used tool names

        Returns:
            List of recommended tools with scores and reasons
        """
        recommendations: list[dict[str, Any]] = []

        if current_tool:
            recommendations.extend(self._recommend_by_workflow(current_tool))

        if query:
            recommendations.extend(self._recommend_by_query(query, category))

        if recently_used:
            recommendations.extend(self._recommend_by_history(recently_used))

        recommendations = self._deduplicate_and_score(recommendations)
        return sorted(recommendations, key=lambda x: x["score"], reverse=True)[:10]

    def _recommend_by_workflow(self, current_tool: str) -> list[dict[str, Any]]:
        """Recommend tools based on workflow relationships.

        Args:
            current_tool: Currently used tool

        Returns:
            List of recommendations
        """
        recommendations = []

        commonly_followed_by = get_commonly_followed_by(current_tool)
        for tool_name in commonly_followed_by:
            recommendations.append(
                {
                    "tool": tool_name,
                    "score": 0.8,
                    "reason": f"Commonly used after {current_tool}",
                    "type": "workflow",
                }
            )

        workflows = get_workflows(current_tool)
        for workflow in workflows:
            steps = workflow.get("steps", [])
            if current_tool in steps:
                current_index = steps.index(current_tool)
                if current_index < len(steps) - 1:
                    next_tool = steps[current_index + 1]
                    recommendations.append(
                        {
                            "tool": next_tool,
                            "score": 0.9,
                            "reason": f"Next step in workflow: {workflow.get('name', 'Workflow')}",
                            "type": "workflow",
                        }
                    )

        return recommendations

    def _recommend_by_query(self, query: str, category: str | None = None) -> list[dict[str, Any]]:
        """Recommend tools based on search query.

        Args:
            query: Search query
            category: Optional category filter

        Returns:
            List of recommendations
        """
        recommendations = []
        query_lower = query.lower()

        matching_tools = self.categorizer.search_tools(query, category)
        for tool_name in matching_tools[:5]:
            score = 0.7
            if category:
                tool_category = self.categorizer.get_tool_category(tool_name)
                if tool_category == category:
                    score = 0.8

            recommendations.append(
                {
                    "tool": tool_name,
                    "score": score,
                    "reason": f"Matches query: {query}",
                    "type": "search",
                }
            )

        return recommendations

    def _recommend_by_history(self, recently_used: list[str]) -> list[dict[str, Any]]:
        """Recommend tools based on usage history.

        Args:
            recently_used: List of recently used tools

        Returns:
            List of recommendations
        """
        recommendations = []

        for tool_name in recently_used[-3:]:
            commonly_followed_by = get_commonly_followed_by(tool_name)
            for next_tool in commonly_followed_by[:3]:
                if next_tool not in recently_used:
                    recommendations.append(
                        {
                            "tool": next_tool,
                            "score": 0.6,
                            "reason": f"Commonly used after {tool_name}",
                            "type": "history",
                        }
                    )

        return recommendations

    def _deduplicate_and_score(self, recommendations: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Deduplicate recommendations and combine scores.

        Args:
            recommendations: List of recommendations

        Returns:
            Deduplicated list with combined scores
        """
        tool_scores: dict[str, dict[str, Any]] = {}

        for rec in recommendations:
            tool_name = rec["tool"]
            if tool_name not in tool_scores:
                tool_scores[tool_name] = {
                    "tool": tool_name,
                    "score": rec["score"],
                    "reasons": [rec["reason"]],
                    "types": [rec["type"]],
                }
            else:
                tool_scores[tool_name]["score"] = min(1.0, tool_scores[tool_name]["score"] + rec["score"] * 0.2)
                tool_scores[tool_name]["reasons"].append(rec["reason"])
                tool_scores[tool_name]["types"].append(rec["type"])

        return list(tool_scores.values())

    def get_workflow_suggestions(self, goal: str) -> list[dict[str, Any]]:
        """Suggest workflows based on goal.

        Args:
            goal: User goal or task description

        Args:
            goal: User goal or task description

        Returns:
            List of suggested workflows
        """
        goal_lower = goal.lower()
        suggested_workflows = []

        all_workflows = get_all_workflows()
        for workflow in all_workflows:
            workflow_name = workflow.get("name", "").lower()
            workflow_desc = workflow.get("description", "").lower()

            if goal_lower in workflow_name or goal_lower in workflow_desc:
                suggested_workflows.append(workflow)

        return suggested_workflows[:5]

