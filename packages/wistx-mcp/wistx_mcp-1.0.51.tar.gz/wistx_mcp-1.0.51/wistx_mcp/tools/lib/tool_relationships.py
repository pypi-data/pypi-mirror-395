"""Tool relationship mapping for documenting workflows and dependencies."""

from typing import Any

TOOL_RELATIONSHIPS: dict[str, dict[str, Any]] = {
    "wistx_get_compliance_requirements": {
        "prerequisites": [],
        "commonly_followed_by": [
            "wistx_design_architecture",
            "wistx_manage_infrastructure",
            "wistx_get_devops_infra_code_examples",
            "wistx_generate_documentation",
        ],
        "workflows": [
            {
                "name": "Compliance-First Architecture Design",
                "steps": [
                    "wistx_get_compliance_requirements",
                    "wistx_design_architecture",
                    "wistx_calculate_infrastructure_cost",
                    "wistx_generate_documentation",
                ],
                "description": "Design infrastructure with compliance requirements from the start",
            },
            {
                "name": "Compliance Audit & Remediation",
                "steps": [
                    "wistx_get_compliance_requirements",
                    "wistx_search_codebase",
                    "wistx_regex_search",
                    "wistx_troubleshoot_issue",
                ],
                "description": "Audit existing infrastructure for compliance violations and fix issues",
            },
        ],
    },
    "wistx_calculate_infrastructure_cost": {
        "prerequisites": [],
        "commonly_followed_by": [
            "wistx_design_architecture",
            "wistx_manage_infrastructure",
            "wistx_generate_documentation",
        ],
        "workflows": [
            {
                "name": "Cost-Optimized Architecture",
                "steps": [
                    "wistx_design_architecture",
                    "wistx_calculate_infrastructure_cost",
                    "wistx_research_knowledge_base",
                    "wistx_design_architecture",
                ],
                "description": "Design architecture, calculate costs, research optimizations, redesign",
            },
            {
                "name": "Existing Infrastructure Cost Analysis",
                "steps": [
                    "wistx_get_existing_infrastructure",
                    "wistx_calculate_infrastructure_cost",
                    "wistx_generate_documentation",
                ],
                "description": "Analyze costs of existing infrastructure and generate cost report",
            },
        ],
    },
    "wistx_get_devops_infra_code_examples": {
        "prerequisites": [],
        "commonly_followed_by": [
            "wistx_design_architecture",
            "wistx_manage_infrastructure",
            "wistx_search_codebase",
        ],
        "workflows": [
            {
                "name": "Find & Apply Code Examples",
                "steps": [
                    "wistx_get_devops_infra_code_examples",
                    "wistx_search_codebase",
                    "wistx_design_architecture",
                ],
                "description": "Find public examples, search your codebase, then design solution",
            },
        ],
    },
    "wistx_index_repository": {
        "prerequisites": [],
        "commonly_followed_by": [
            "wistx_search_codebase",
            "wistx_regex_search",
            "wistx_get_existing_infrastructure",
            "wistx_troubleshoot_issue",
        ],
        "workflows": [
            {
                "name": "Index & Search Workflow",
                "steps": [
                    "wistx_index_repository",
                    "wistx_check_resource_status",
                    "wistx_search_codebase",
                ],
                "description": "Index repository, wait for completion, then search",
            },
            {
                "name": "Security Audit Workflow",
                "steps": [
                    "wistx_index_repository",
                    "wistx_check_resource_status",
                    "wistx_regex_search",
                    "wistx_troubleshoot_issue",
                ],
                "description": "Index repo, search for security issues, troubleshoot findings",
            },
        ],
    },
    "wistx_search_codebase": {
        "prerequisites": ["wistx_index_repository"],
        "commonly_followed_by": [
            "wistx_get_devops_infra_code_examples",
            "wistx_troubleshoot_issue",
            "wistx_design_architecture",
        ],
        "workflows": [
            {
                "name": "Code Discovery & Implementation",
                "steps": [
                    "wistx_search_codebase",
                    "wistx_get_devops_infra_code_examples",
                    "wistx_design_architecture",
                ],
                "description": "Search your codebase, find public examples, implement solution",
            },
        ],
    },
    "wistx_design_architecture": {
        "prerequisites": [
            "wistx_get_compliance_requirements",
            "wistx_research_knowledge_base",
        ],
        "commonly_followed_by": [
            "wistx_calculate_infrastructure_cost",
            "wistx_manage_infrastructure",
            "wistx_generate_documentation",
            "wistx_get_devops_infra_code_examples",
        ],
        "workflows": [
            {
                "name": "Complete Architecture Design",
                "steps": [
                    "wistx_get_compliance_requirements",
                    "wistx_research_knowledge_base",
                    "wistx_design_architecture",
                    "wistx_calculate_infrastructure_cost",
                    "wistx_generate_documentation",
                ],
                "description": "Full architecture design workflow from requirements to documentation",
            },
        ],
    },
    "wistx_troubleshoot_issue": {
        "prerequisites": [
            "wistx_search_codebase",
            "wistx_research_knowledge_base",
        ],
        "commonly_followed_by": [
            "wistx_get_devops_infra_code_examples",
            "wistx_manage_infrastructure",
        ],
        "workflows": [
            {
                "name": "Issue Resolution Workflow",
                "steps": [
                    "wistx_troubleshoot_issue",
                    "wistx_get_devops_infra_code_examples",
                    "wistx_search_codebase",
                ],
                "description": "Troubleshoot issue, find examples, search codebase for fixes",
            },
        ],
    },
    "wistx_manage_infrastructure": {
        "prerequisites": [
            "wistx_get_compliance_requirements",
            "wistx_get_existing_infrastructure",
        ],
        "commonly_followed_by": [
            "wistx_calculate_infrastructure_cost",
            "wistx_generate_documentation",
            "wistx_troubleshoot_issue",
        ],
        "workflows": [
            {
                "name": "Infrastructure Lifecycle Management",
                "steps": [
                    "wistx_get_existing_infrastructure",
                    "wistx_get_compliance_requirements",
                    "wistx_manage_infrastructure",
                    "wistx_calculate_infrastructure_cost",
                ],
                "description": "Manage infrastructure with compliance and cost considerations",
            },
        ],
    },
    "wistx_generate_documentation": {
        "prerequisites": [
            "wistx_design_architecture",
            "wistx_get_compliance_requirements",
            "wistx_calculate_infrastructure_cost",
        ],
        "commonly_followed_by": [],
        "workflows": [
            {
                "name": "Documentation Generation",
                "steps": [
                    "wistx_design_architecture",
                    "wistx_get_compliance_requirements",
                    "wistx_calculate_infrastructure_cost",
                    "wistx_generate_documentation",
                ],
                "description": "Generate comprehensive documentation from architecture, compliance, and cost data",
            },
        ],
    },
    "wistx_research_knowledge_base": {
        "prerequisites": [],
        "commonly_followed_by": [
            "wistx_design_architecture",
            "wistx_troubleshoot_issue",
            "wistx_get_devops_infra_code_examples",
        ],
        "workflows": [
            {
                "name": "Research & Design",
                "steps": [
                    "wistx_research_knowledge_base",
                    "wistx_design_architecture",
                    "wistx_get_devops_infra_code_examples",
                ],
                "description": "Research best practices, design architecture, find code examples",
            },
        ],
    },
}


def get_tool_relationships(tool_name: str) -> dict[str, Any] | None:
    """Get relationships for a tool.

    Args:
        tool_name: Name of the tool

    Returns:
        Relationship dictionary or None if not found
    """
    return TOOL_RELATIONSHIPS.get(tool_name)


def get_prerequisites(tool_name: str) -> list[str]:
    """Get prerequisite tools for a tool.

    Args:
        tool_name: Name of the tool

    Returns:
        List of prerequisite tool names
    """
    relationships = get_tool_relationships(tool_name)
    if relationships:
        return relationships.get("prerequisites", [])
    return []


def get_commonly_followed_by(tool_name: str) -> list[str]:
    """Get tools commonly used after this tool.

    Args:
        tool_name: Name of the tool

    Returns:
        List of tool names commonly used after this tool
    """
    relationships = get_tool_relationships(tool_name)
    if relationships:
        return relationships.get("commonly_followed_by", [])
    return []


def get_workflows(tool_name: str) -> list[dict[str, Any]]:
    """Get workflows involving this tool.

    Args:
        tool_name: Name of the tool

    Returns:
        List of workflow dictionaries
    """
    relationships = get_tool_relationships(tool_name)
    if relationships:
        return relationships.get("workflows", [])
    return []


def get_all_workflows() -> list[dict[str, Any]]:
    """Get all documented workflows.

    Returns:
        List of all workflow dictionaries
    """
    all_workflows = []
    for tool_name, relationships in TOOL_RELATIONSHIPS.items():
        workflows = relationships.get("workflows", [])
        for workflow in workflows:
            workflow["primary_tool"] = tool_name
            all_workflows.append(workflow)
    return all_workflows


def find_workflow_by_name(workflow_name: str) -> dict[str, Any] | None:
    """Find a workflow by name.

    Args:
        workflow_name: Name of the workflow

    Returns:
        Workflow dictionary or None if not found
    """
    for workflow in get_all_workflows():
        if workflow.get("name") == workflow_name:
            return workflow
    return None

