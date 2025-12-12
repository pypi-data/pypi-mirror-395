"""Tool description builder for consistent, agent-optimized tool descriptions."""

from typing import Any


class ToolDescriptionBuilder:
    """Builder for creating standardized tool descriptions optimized for AI agents."""

    def __init__(self, tool_name: str, one_line_purpose: str):
        """Initialize tool description builder.

        Args:
            tool_name: Name of the tool
            one_line_purpose: One-line description of tool purpose
        """
        self.tool_name = tool_name
        self.one_line_purpose = one_line_purpose
        self.when_to_use: list[str] = []
        self.when_not_to_use: list[str] = []
        self.returns: list[str] = []
        self.example: dict[str, Any] | None = None
        self.common_workflows: list[str] = []
        self.related_tools: list[str] = []
        self.trigger_keywords: list[str] = []

    def add_when_to_use(self, scenario: str) -> "ToolDescriptionBuilder":
        """Add a 'when to use' scenario.

        Args:
            scenario: Scenario description

        Returns:
            Self for chaining
        """
        self.when_to_use.append(scenario)
        return self

    def add_when_not_to_use(self, scenario: str) -> "ToolDescriptionBuilder":
        """Add a 'when NOT to use' scenario.

        Args:
            scenario: Scenario description

        Returns:
            Self for chaining
        """
        self.when_not_to_use.append(scenario)
        return self

    def add_returns(self, output_description: str) -> "ToolDescriptionBuilder":
        """Add return value description.

        Args:
            output_description: Description of return value

        Returns:
            Self for chaining
        """
        self.returns.append(output_description)
        return self

    def set_example(self, example: dict[str, Any]) -> "ToolDescriptionBuilder":
        """Set example invocation.

        Args:
            example: Example parameter dictionary

        Returns:
            Self for chaining
        """
        self.example = example
        return self

    def add_common_workflow(self, workflow: str) -> "ToolDescriptionBuilder":
        """Add common workflow description.

        Args:
            workflow: Workflow description (e.g., "Tool A → Tool B → This tool")

        Returns:
            Self for chaining
        """
        self.common_workflows.append(workflow)
        return self

    def add_related_tool(self, tool_name: str, relationship: str) -> "ToolDescriptionBuilder":
        """Add related tool.

        Args:
            tool_name: Name of related tool
            relationship: Relationship description (e.g., "Use before this tool to check compliance")

        Returns:
            Self for chaining
        """
        self.related_tools.append(f"- `{tool_name}`: {relationship}")
        return self

    def add_trigger_keywords(self, keywords: list[str]) -> "ToolDescriptionBuilder":
        """Add trigger keywords for agent recognition.

        Args:
            keywords: List of keywords agents should recognize

        Returns:
            Self for chaining
        """
        self.trigger_keywords.extend(keywords)
        return self

    def build(self) -> str:
        """Build the complete tool description.

        Returns:
            Formatted tool description string
        """
        import json

        parts: list[str] = []

        parts.append(f"{self.tool_name}: {self.one_line_purpose}")

        if self.trigger_keywords:
            keywords_str = ", ".join(self.trigger_keywords)
            parts.append(f"\n**Keywords:** {keywords_str}")

        if self.when_to_use:
            parts.append("\n**When to Use:**")
            for scenario in self.when_to_use:
                parts.append(f"- {scenario}")

        if self.when_not_to_use:
            parts.append("\n**When NOT to Use:**")
            for scenario in self.when_not_to_use:
                parts.append(f"- {scenario}")

        if self.returns:
            parts.append("\n**Returns:**")
            for ret in self.returns:
                parts.append(f"- {ret}")

        if self.example:
            example_json = json.dumps(self.example, indent=2)
            parts.append("\n**Example:**")
            parts.append("```json")
            parts.append(example_json)
            parts.append("```")

        if self.common_workflows:
            parts.append("\n**Common Workflows:**")
            for i, workflow in enumerate(self.common_workflows, 1):
                parts.append(f"{i}. {workflow}")

        if self.related_tools:
            parts.append("\n**Related Tools:**")
            parts.extend(self.related_tools)

        return "\n".join(parts)

    def validate(self) -> list[str]:
        """Validate description completeness.

        Returns:
            List of validation errors (empty if valid)
        """
        errors: list[str] = []

        if not self.when_to_use:
            errors.append("Missing 'When to Use' scenarios")

        if not self.returns:
            errors.append("Missing 'Returns' descriptions")

        if not self.example:
            errors.append("Missing example invocation")

        return errors

