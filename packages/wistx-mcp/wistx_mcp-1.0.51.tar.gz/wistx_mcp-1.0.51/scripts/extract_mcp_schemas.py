"""Extract MCP tool schemas from wistx_mcp/server.py and generate documentation."""

import ast
import json
import re
from pathlib import Path
from typing import Any, Dict, List


class MCPToolExtractor(ast.NodeVisitor):
    """AST visitor to extract Tool definitions."""

    def __init__(self) -> None:
        self.tools: List[Dict[str, Any]] = []

    def visit_Call(self, node: ast.Call) -> None:
        """Extract Tool() calls."""
        if isinstance(node.func, ast.Name) and node.func.id == "Tool":
            tool_info = self._extract_tool_info(node)
            if tool_info:
                self.tools.append(tool_info)
        self.generic_visit(node)

    def _extract_tool_info(self, node: ast.Call) -> Dict[str, Any] | None:
        """Extract tool information from Tool() call."""
        tool_info: Dict[str, Any] = {}

        for keyword in node.keywords:
            if keyword.arg == "name":
                tool_info["name"] = self._extract_string_value(keyword.value)
            elif keyword.arg == "description":
                tool_info["description"] = self._extract_string_value(keyword.value)
            elif keyword.arg == "inputSchema":
                tool_info["inputSchema"] = self._extract_dict_value(keyword.value)

        return tool_info if tool_info else None

    def _extract_string_value(self, node: ast.AST) -> str:
        """Extract string value from AST node."""
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        elif isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.JoinedStr):
            parts = []
            for value in node.values:
                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                    parts.append(value.value)
                elif isinstance(value, ast.Str):
                    parts.append(value.s)
            return "".join(parts)
        return ""

    def _extract_dict_value(self, node: ast.AST) -> Dict[str, Any]:
        """Extract dictionary value from AST node."""
        if isinstance(node, ast.Dict):
            result: Dict[str, Any] = {}
            for key, value in zip(node.keys, node.values):
                key_str = self._extract_string_value(key) if key else None
                if key_str:
                    result[key_str] = self._extract_ast_value(value)
            return result
        return {}

    def _extract_ast_value(self, node: ast.AST) -> Any:
        """Recursively extract value from AST node."""
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.Dict):
            return self._extract_dict_value(node)
        elif isinstance(node, ast.List):
            return [self._extract_ast_value(item) for item in node.elts]
        elif isinstance(node, ast.NameConstant):
            return node.value
        elif isinstance(node, ast.Name):
            if node.id == "True":
                return True
            elif node.id == "False":
                return False
            elif node.id == "None":
                return None
        return None


def extract_mcp_tools() -> List[Dict[str, Any]]:
    """Extract MCP tool definitions from server.py."""
    server_file = Path("wistx_mcp/server.py")

    if not server_file.exists():
        print(f"❌ File not found: {server_file}")
        return []

    with open(server_file, "r") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
        extractor = MCPToolExtractor()
        extractor.visit(tree)
        return extractor.tools
    except SyntaxError as e:
        print(f"❌ Syntax error parsing {server_file}: {e}")
        return []


def generate_example_arguments(schema: Dict[str, Any]) -> Dict[str, Any]:
    """Generate example arguments from schema."""
    example: Dict[str, Any] = {}

    if "properties" in schema:
        required = schema.get("required", [])
        for param_name, param_info in schema["properties"].items():
            param_type = param_info.get("type")
            default = param_info.get("default")

            if default is not None:
                example[param_name] = default
            elif param_name in required:
                if param_type == "string":
                    example[param_name] = f"example_{param_name}"
                elif param_type == "array":
                    example[param_name] = []
                elif param_type == "object":
                    example[param_name] = {}
                elif param_type == "boolean":
                    example[param_name] = True
                elif param_type == "integer":
                    example[param_name] = 1

    return example


def generate_tool_markdown(tool: Dict[str, Any], docs_dir: Path) -> None:
    """Generate markdown documentation for a single tool."""
    tool_name = tool["name"].replace("wistx_", "")
    description = tool.get("description", "")
    input_schema = tool.get("inputSchema", {})

    content = f"""---
title: {tool_name.replace('_', ' ').title()}
description: {description.split('.')[0] if description else ''}
---

# {tool_name.replace('_', ' ').title()}

{description}

"""

    if "properties" in input_schema:
        content += "## Parameters\n\n"
        content += "| Parameter | Type | Required | Description |\n"
        content += "|-----------|------|----------|-------------|\n"

        required_params = input_schema.get("required", [])

        for param_name, param_info in input_schema["properties"].items():
            param_type = param_info.get("type", "unknown")
            if param_type == "array":
                items = param_info.get("items", {})
                item_type = items.get("type", "any")
                param_type = f"array<{item_type}>"
            elif param_type == "object":
                param_type = "object"
            is_required = param_name in required_params
            param_desc = param_info.get("description", "").replace("\n", " ")

            content += f"| `{param_name}` | {param_type} | {'Yes' if is_required else 'No'} | {param_desc} |\n"

        content += "\n"

    example_args = generate_example_arguments(input_schema)
    content += "## Example\n\n"
    content += "```json\n"
    content += json.dumps(
        {
            "tool": tool["name"],
            "arguments": example_args,
        },
        indent=2,
    )
    content += "\n```\n"

    output_file = docs_dir / f"{tool_name}.mdx"
    output_file.write_text(content)
    print(f"✅ Generated: {output_file}")


def generate_category_page(
    category: str, tools: List[Dict[str, Any]], docs_dir: Path
) -> None:
    """Generate documentation page for a tool category."""
    category_name = category.replace("_", " ").title()

    content = f"""---
title: {category_name} Tools
description: WISTX MCP tools for {category_name.lower()}
---

# {category_name} Tools

"""

    for tool in tools:
        tool_name = tool["name"].replace("wistx_", "")
        description = tool.get("description", "")
        input_schema = tool.get("inputSchema", {})

        content += f"## {tool_name.replace('_', ' ').title()}\n\n"
        content += f"{description}\n\n"

        if "properties" in input_schema:
            content += "### Parameters\n\n"
            content += "| Parameter | Type | Required | Description |\n"
            content += "|-----------|------|----------|-------------|\n"

            required_params = input_schema.get("required", [])

            for param_name, param_info in input_schema["properties"].items():
                param_type = param_info.get("type", "unknown")
                is_required = param_name in required_params
                param_desc = param_info.get("description", "").replace("\n", " ")

                content += f"| `{param_name}` | {param_type} | {'Yes' if is_required else 'No'} | {param_desc} |\n"

            content += "\n"

        example_args = generate_example_arguments(input_schema)
        content += "### Example\n\n"
        content += "```json\n"
        content += json.dumps(
            {
                "tool": tool["name"],
                "arguments": example_args,
            },
            indent=2,
        )
        content += "\n```\n\n"
        content += "---\n\n"

    output_file = docs_dir / f"{category}.mdx"
    output_file.write_text(content)
    print(f"✅ Generated: {output_file}")


def generate_overview_page(tools: List[Dict[str, Any]], docs_dir: Path) -> None:
    """Generate MCP tools overview page."""
    content = """---
title: MCP Tools Overview
description: Complete list of WISTX MCP tools
---

# MCP Tools Overview

WISTX provides a comprehensive set of MCP tools for DevOps, compliance, and infrastructure management.

## Available Tools

"""

    tool_categories = {
        "Compliance & Pricing": [
            "wistx_get_compliance_requirements",
            "wistx_calculate_infrastructure_cost",
        ],
        "Indexing": [
            "wistx_index_repository",
            "wistx_index_resource",
            "wistx_list_resources",
            "wistx_check_resource_status",
            "wistx_delete_resource",
        ],
        "Knowledge & Search": [
            "wistx_research_knowledge_base",
            "wistx_web_search",
            "wistx_search_codebase",
        ],
        "Development Tools": [
            "wistx_design_architecture",
            "wistx_troubleshoot_issue",
            "wistx_generate_documentation",
            "wistx_manage_integration",
            "wistx_manage_infrastructure",
        ],
    }

    for category_name, tool_names in tool_categories.items():
        content += f"### {category_name}\n\n"
        for tool in tools:
            if tool["name"] in tool_names:
                tool_display_name = tool["name"].replace("wistx_", "").replace("_", " ").title()
                description = tool.get("description", "").split(".")[0]
                content += f"- **{tool_display_name}**: {description}\n"
        content += "\n"

    output_file = docs_dir / "overview.mdx"
    output_file.write_text(content)
    print(f"✅ Generated: {output_file}")


def main() -> None:
    """Main function to extract and generate MCP tool documentation."""
    print("Extracting MCP tool schemas...")
    tools = extract_mcp_tools()
    print(f"Found {len(tools)} tools")

    if not tools:
        print("❌ No tools found. Check wistx_mcp/server.py")
        return

    docs_dir = Path("docs/mcp-tools")
    docs_dir.mkdir(parents=True, exist_ok=True)

    print("Generating documentation...")
    generate_overview_page(tools, docs_dir)

    tool_categories = {
        "compliance": ["wistx_get_compliance_requirements"],
        "pricing": ["wistx_calculate_infrastructure_cost"],
        "indexing": [
            "wistx_index_repository",
            "wistx_index_resource",
            "wistx_list_resources",
            "wistx_check_resource_status",
            "wistx_delete_resource",
        ],
        "knowledge": ["wistx_research_knowledge_base"],
        "search": [
            "wistx_web_search",
            "wistx_search_codebase",
        ],
        "architecture": ["wistx_design_architecture"],
        "troubleshooting": ["wistx_troubleshoot_issue"],
        "documentation": ["wistx_generate_documentation"],
        "integration": ["wistx_manage_integration"],
        "infrastructure": ["wistx_manage_infrastructure"],
    }

    for category, tool_names in tool_categories.items():
        category_tools = [t for t in tools if t["name"] in tool_names]
        if category_tools:
            generate_category_page(category, category_tools, docs_dir)

    print("✅ Documentation generation complete")


if __name__ == "__main__":
    main()

