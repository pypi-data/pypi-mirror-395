"""MCP tools package - lazy loading to prevent segfaults during import."""

import importlib

# NOTE: Lazy imports to prevent segmentation faults during module loading
# The tools are imported on-demand rather than at module load time
# This prevents circular imports and garbage collection issues

__all__ = [
    "mcp_tools",
    "user_indexing",
    "web_search",
    "search_codebase",
    "regex_search",
    "package_search",
    "design_architecture",
    "troubleshoot_issue",
    "generate_documentation",
    "manage_integration",
    "manage_infrastructure",
    "get_github_file_tree",
    "visualize_infra_flow",
    "infrastructure_context",
    "virtual_filesystem",
    "intelligent_context",
]

def __getattr__(name):
    """Lazy load tools on demand."""
    if name == "mcp_tools":
        return importlib.import_module("wistx_mcp.tools.mcp_tools")
    elif name == "user_indexing":
        return importlib.import_module("wistx_mcp.tools.user_indexing")
    elif name == "web_search":
        return importlib.import_module("wistx_mcp.tools.web_search")
    elif name == "search_codebase":
        return importlib.import_module("wistx_mcp.tools.search_codebase")
    elif name == "regex_search":
        return importlib.import_module("wistx_mcp.tools.regex_search")
    elif name == "package_search":
        return importlib.import_module("wistx_mcp.tools.package_search")
    elif name == "design_architecture":
        return importlib.import_module("wistx_mcp.tools.design_architecture")
    elif name == "troubleshoot_issue":
        return importlib.import_module("wistx_mcp.tools.troubleshoot_issue")
    elif name == "generate_documentation":
        return importlib.import_module("wistx_mcp.tools.generate_documentation")
    elif name == "manage_integration":
        return importlib.import_module("wistx_mcp.tools.manage_integration")
    elif name == "manage_infrastructure":
        return importlib.import_module("wistx_mcp.tools.manage_infrastructure")
    elif name == "get_github_file_tree":
        return importlib.import_module("wistx_mcp.tools.get_github_file_tree")
    elif name == "virtual_filesystem":
        return importlib.import_module("wistx_mcp.tools.virtual_filesystem")
    elif name == "intelligent_context":
        return importlib.import_module("wistx_mcp.tools.intelligent_context")
        return importlib.import_module("wistx_mcp.tools.get_github_file_tree")
    elif name == "visualize_infra_flow":
        return importlib.import_module("wistx_mcp.tools.visualize_infra_flow")
    elif name == "infrastructure_context":
        return importlib.import_module("wistx_mcp.tools.infrastructure_context")
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

