"""Tool categorization system for organizing MCP tools by domain."""

from typing import Any

TOOL_CATEGORIES = {
    "compliance": {
        "name": "Compliance",
        "description": "Tools for compliance requirements, standards, and verification",
        "keywords": ["compliance", "standards", "PCI-DSS", "HIPAA", "SOC2", "NIST", "controls", "remediation"],
        "tools": [
            "wistx_get_compliance_requirements",
        ],
    },
    "pricing": {
        "name": "Pricing & Cost",
        "description": "Tools for infrastructure cost calculation and optimization",
        "keywords": ["cost", "pricing", "FinOps", "cost optimization", "budget", "expenses"],
        "tools": [
            "wistx_calculate_infrastructure_cost",
        ],
    },
    "code": {
        "name": "Code Examples",
        "description": "Tools for finding and searching infrastructure code examples",
        "keywords": ["code", "examples", "templates", "snippets", "reference implementation"],
        "tools": [
            "wistx_get_devops_infra_code_examples",
        ],
    },
    "infrastructure": {
        "name": "Infrastructure Management",
        "description": "Tools for designing, managing, and troubleshooting infrastructure",
        "keywords": ["infrastructure", "kubernetes", "cluster", "design", "architecture", "troubleshoot"],
        "tools": [
            "wistx_design_architecture",
            "wistx_troubleshoot_issue",
            "wistx_manage_infrastructure",
            "wistx_manage_integration",
            "wistx_get_existing_infrastructure",
        ],
    },
    "knowledge": {
        "name": "Knowledge & Research",
        "description": "Tools for researching best practices, patterns, and strategies",
        "keywords": ["research", "knowledge", "best practices", "patterns", "strategies", "guides"],
        "tools": [
            "wistx_research_knowledge_base",
            "wistx_web_search",
        ],
    },
    "indexing": {
        "name": "Indexing & Search",
        "description": "Tools for indexing and searching repositories, documentation, and codebases",
        "keywords": ["index", "search", "repository", "codebase", "documentation", "crawl"],
        "tools": [
            "wistx_index_repository",
            "wistx_index_resource",
            "wistx_list_resources",
            "wistx_check_resource_status",
            "wistx_delete_resource",
            "wistx_search_codebase",
            "wistx_regex_search",
        ],
    },
    "documentation": {
        "name": "Documentation",
        "description": "Tools for generating documentation and reports",
        "keywords": ["documentation", "reports", "runbook", "architecture docs"],
        "tools": [
            "wistx_generate_documentation",
        ],
    },
    "packages": {
        "name": "Package Search",
        "description": "Tools for searching DevOps and infrastructure packages",
        "keywords": ["packages", "registry", "PyPI", "NPM", "Terraform Registry", "Helm"],
        "tools": [
            "wistx_search_packages",
        ],
    },
}

TOOL_CATEGORY_MAP: dict[str, str] = {
    "wistx_get_compliance_requirements": "compliance",
    "wistx_calculate_infrastructure_cost": "pricing",
    "wistx_get_devops_infra_code_examples": "code",
    "wistx_research_knowledge_base": "knowledge",
    "wistx_web_search": "knowledge",
    "wistx_index_repository": "indexing",
    "wistx_index_resource": "indexing",
    "wistx_list_resources": "indexing",
    "wistx_check_resource_status": "indexing",
    "wistx_delete_resource": "indexing",
    "wistx_search_codebase": "indexing",
    "wistx_regex_search": "indexing",
    "wistx_design_architecture": "infrastructure",
    "wistx_troubleshoot_issue": "infrastructure",
    "wistx_generate_documentation": "documentation",
    "wistx_manage_integration": "infrastructure",
    "wistx_manage_infrastructure": "infrastructure",
    "wistx_search_packages": "packages",
    "wistx_get_existing_infrastructure": "infrastructure",
}


def get_tool_category(tool_name: str) -> str | None:
    """Get category for a tool.

    Args:
        tool_name: Name of the tool

    Returns:
        Category name or None if not found
    """
    return TOOL_CATEGORY_MAP.get(tool_name)


def get_category_tools(category: str) -> list[str]:
    """Get all tools in a category.

    Args:
        category: Category name

    Returns:
        List of tool names in the category
    """
    category_info = TOOL_CATEGORIES.get(category)
    if category_info:
        return category_info.get("tools", [])
    return []


def get_all_categories() -> dict[str, dict[str, Any]]:
    """Get all categories with metadata.

    Returns:
        Dictionary mapping category names to category metadata
    """
    return TOOL_CATEGORIES


def get_category_info(category: str) -> dict[str, Any] | None:
    """Get category information.

    Args:
        category: Category name

    Returns:
        Category information dictionary or None if not found
    """
    return TOOL_CATEGORIES.get(category)


def search_tools_by_keyword(keyword: str) -> list[str]:
    """Search tools by keyword across categories.

    Args:
        keyword: Keyword to search for

    Returns:
        List of tool names matching the keyword
    """
    keyword_lower = keyword.lower()
    matching_tools: list[str] = []

    for category_info in TOOL_CATEGORIES.values():
        keywords = category_info.get("keywords", [])
        if any(keyword_lower in kw.lower() for kw in keywords):
            matching_tools.extend(category_info.get("tools", []))

    for tool_name, category in TOOL_CATEGORY_MAP.items():
        if keyword_lower in tool_name.lower():
            if tool_name not in matching_tools:
                matching_tools.append(tool_name)

    return list(set(matching_tools))

