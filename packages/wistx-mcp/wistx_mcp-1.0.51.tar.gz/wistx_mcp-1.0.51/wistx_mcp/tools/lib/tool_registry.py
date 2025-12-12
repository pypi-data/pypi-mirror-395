"""MCP tool registry for versioning and deprecation."""

import logging
from typing import Any

logger = logging.getLogger(__name__)

TOOL_VERSIONS: dict[str, dict[str, Any]] = {
    "wistx_get_compliance_requirements": {
        "current_version": "v1",
        "available_versions": ["v1"],
        "deprecated_versions": [],
        "deprecation_dates": {},
        "sunset_dates": {},
    },
    "wistx_calculate_infrastructure_cost": {
        "current_version": "v1",
        "available_versions": ["v1"],
        "deprecated_versions": [],
        "deprecation_dates": {},
        "sunset_dates": {},
    },
    "wistx_get_devops_infra_code_examples": {
        "current_version": "v1",
        "available_versions": ["v1"],
        "deprecated_versions": [],
        "deprecation_dates": {},
        "sunset_dates": {},
    },
    "wistx_research_knowledge_base": {
        "current_version": "v1",
        "available_versions": ["v1"],
        "deprecated_versions": [],
        "deprecation_dates": {},
        "sunset_dates": {},
    },
    "wistx_index_repository": {
        "current_version": "v1",
        "available_versions": ["v1"],
        "deprecated_versions": [],
        "deprecation_dates": {},
        "sunset_dates": {},
    },
    "wistx_index_resource": {
        "current_version": "v1",
        "available_versions": ["v1"],
        "deprecated_versions": [],
        "deprecation_dates": {},
        "sunset_dates": {},
    },
    "wistx_search_codebase": {
        "current_version": "v1",
        "available_versions": ["v1"],
        "deprecated_versions": [],
        "deprecation_dates": {},
        "sunset_dates": {},
    },
    "wistx_web_search": {
        "current_version": "v1",
        "available_versions": ["v1"],
        "deprecated_versions": [],
        "deprecation_dates": {},
        "sunset_dates": {},
    },
    "wistx_design_architecture": {
        "current_version": "v1",
        "available_versions": ["v1"],
        "deprecated_versions": [],
        "deprecation_dates": {},
        "sunset_dates": {},
    },
    "wistx_troubleshoot_issue": {
        "current_version": "v1",
        "available_versions": ["v1"],
        "deprecated_versions": [],
        "deprecation_dates": {},
        "sunset_dates": {},
    },
    "wistx_generate_documentation": {
        "current_version": "v1",
        "available_versions": ["v1"],
        "deprecated_versions": [],
        "deprecation_dates": {},
        "sunset_dates": {},
    },
    "wistx_manage_integration": {
        "current_version": "v1",
        "available_versions": ["v1"],
        "deprecated_versions": [],
        "deprecation_dates": {},
        "sunset_dates": {},
    },
    "wistx_manage_infrastructure": {
        "current_version": "v1",
        "available_versions": ["v1"],
        "deprecated_versions": [],
        "deprecation_dates": {},
        "sunset_dates": {},
    },
    "wistx_search_packages": {
        "current_version": "v1",
        "available_versions": ["v1"],
        "deprecated_versions": [],
        "deprecation_dates": {},
        "sunset_dates": {},
    },
    "wistx_regex_search": {
        "current_version": "v1",
        "available_versions": ["v1"],
        "deprecated_versions": [],
        "deprecation_dates": {},
        "sunset_dates": {},
    },
}


def get_tool_versions() -> dict[str, dict[str, Any]]:
    """Get all tool version information.

    Returns:
        Dictionary mapping tool names to version information
    """
    return TOOL_VERSIONS


def get_tool_version(tool_name: str) -> dict[str, Any] | None:
    """Get version information for a specific tool.

    Args:
        tool_name: Tool name (with or without version suffix)

    Returns:
        Version information or None if not found
    """
    base_name = _get_base_tool_name(tool_name)
    return TOOL_VERSIONS.get(base_name)


def is_tool_deprecated(tool_name: str) -> bool:
    """Check if a tool version is deprecated.

    Args:
        tool_name: Tool name (with or without version suffix)

    Returns:
        True if deprecated, False otherwise
    """
    version_info = get_tool_version(tool_name)
    if not version_info:
        return False

    base_name = _get_base_tool_name(tool_name)
    version = _extract_version_from_tool_name(tool_name) or version_info["current_version"]

    return version in version_info.get("deprecated_versions", [])


def get_deprecation_warning(tool_name: str) -> str | None:
    """Get deprecation warning message for a tool.

    Args:
        tool_name: Tool name (with or without version suffix)

    Returns:
        Deprecation warning message or None
    """
    if not is_tool_deprecated(tool_name):
        return None

    version_info = get_tool_version(tool_name)
    if not version_info:
        return None

    base_name = _get_base_tool_name(tool_name)
    version = _extract_version_from_tool_name(tool_name) or version_info["current_version"]
    current_version = version_info["current_version"]

    deprecation_date = version_info.get("deprecation_dates", {}).get(version)
    sunset_date = version_info.get("sunset_dates", {}).get(version)

    warning = f"Tool '{base_name}' version '{version}' is deprecated."
    if current_version:
        warning += f" Please migrate to version '{current_version}'."
    if sunset_date:
        warning += f" This version will be removed on {sunset_date}."

    return warning


def _get_base_tool_name(tool_name: str) -> str:
    """Extract base tool name without version suffix.

    Args:
        tool_name: Tool name (e.g., "wistx_get_compliance_requirements_v2")

    Returns:
        Base tool name (e.g., "wistx_get_compliance_requirements")
    """
    if "_v" in tool_name:
        parts = tool_name.rsplit("_v", 1)
        if parts[1][0].isdigit():
            return parts[0]
    return tool_name


def _extract_version_from_tool_name(tool_name: str) -> str | None:
    """Extract version from tool name.

    Args:
        tool_name: Tool name (e.g., "wistx_get_compliance_requirements_v2")

    Returns:
        Version string (e.g., "v2") or None
    """
    if "_v" in tool_name:
        parts = tool_name.rsplit("_v", 1)
        if parts[1][0].isdigit():
            return f"v{parts[1].split('_')[0]}"
    return None


def resolve_tool_name(tool_name: str) -> str:
    """Resolve tool name to actual versioned tool name.

    If base name is provided, resolves to current version.
    If versioned name is provided, returns as-is.

    Args:
        tool_name: Tool name (base or versioned)

    Returns:
        Resolved tool name (versioned)
    """
    base_name = _get_base_tool_name(tool_name)
    version_info = TOOL_VERSIONS.get(base_name)
    
    if not version_info:
        return tool_name
    
    version = _extract_version_from_tool_name(tool_name)
    current_version = version_info.get("current_version", "v1")
    
    if version:
        return tool_name
    
    if current_version == "v1":
        return base_name
    
    return f"{base_name}_{current_version}"

