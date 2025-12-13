"""Unified packages tool - search and read DevOps resources.

This module merges package search and file reading into one unified interface:
- search_devops_resources (search packages, tools, services, documentation)
- read_package_file (read specific file sections from packages)

Usage:
    # Search packages and tools
    result = await wistx_packages(action="search", query="kubernetes deployment", ...)

    # Read a file from a package
    result = await wistx_packages(action="read_file", registry="pypi", package_name="boto3", ...)
"""

import logging
from typing import Any

from wistx_mcp.tools.lib.plan_enforcement import require_query_quota

logger = logging.getLogger(__name__)

# Valid actions
VALID_ACTIONS = ["search", "read_file"]


@require_query_quota
async def wistx_packages(
    # REQUIRED
    action: str,

    # API KEY (optional - uses context or MCP initialization)
    api_key: str | None = None,

    # === SEARCH (action="search") ===
    query: str | None = None,
    resource_types: list[str] | None = None,
    pattern: str | None = None,
    template: str | None = None,
    search_type: str = "semantic",
    domain: str | None = None,
    category: str | None = None,
    package_name: str | None = None,
    limit: int = 1000,

    # === READ FILE (action="read_file") ===
    registry: str | None = None,
    filename_sha256: str | None = None,
    start_line: int = 1,
    end_line: int = 100,
    version: str | None = None,
) -> dict[str, Any]:
    """Unified packages and DevOps resources tool.

    **Actions:**

    - "search": Search packages, CLI tools, services, and documentation
    - "read_file": Read specific file section from package source

    Args:
        action: Operation to perform (required)
        api_key: WISTX API key for authentication (required)

        For search:
        - query: Natural language search query (required for semantic search)
        - resource_types: Filter by types (package, tool, service, documentation, all)
        - pattern: Regex pattern (for regex search on packages)
        - template: Pre-built template name (alternative to pattern)
        - search_type: Search type (semantic, regex, hybrid)
        - registry: Filter by registry (pypi, npm, terraform, etc.)
        - domain: Filter by domain (devops, infrastructure, compliance, etc.)
        - category: Filter by category (infrastructure-as-code, kubernetes, etc.)
        - package_name: Search specific package
        - limit: Maximum results per resource type

        For read_file:
        - registry: Registry name (required) - pypi, npm, terraform
        - package_name: Package name (required)
        - filename_sha256: SHA256 hash of filename (required, from search results)
        - start_line: Starting line, 1-based (default: 1)
        - end_line: Ending line (default: 100, max 200 lines from start)
        - version: Optional package version

    Returns:
        For search:
        - packages: List of packages
        - tools: List of CLI tools
        - services: List of services/integrations
        - documentation: List of documentation
        - unified_results: Cross-type ranked results
        - total: Total results

        For read_file:
        - file_path: Path to file in package
        - content: File content for specified line range
        - start_line: Actual start line
        - end_line: Actual end line
        - total_lines: Total lines in file

    Raises:
        ValueError: If invalid action or missing required parameters
        RuntimeError: If operation fails
    """
    if action not in VALID_ACTIONS:
        raise ValueError(
            f"Invalid action: {action}. "
            f"Valid actions: {', '.join(VALID_ACTIONS)}"
        )

    logger.info("Unified packages: action=%s", action)

    # Route to appropriate handler
    if action == "search":
        return await _handle_search(
            query=query,
            resource_types=resource_types,
            pattern=pattern,
            template=template,
            search_type=search_type,
            registry=registry,
            domain=domain,
            category=category,
            package_name=package_name,
            limit=limit,
            api_key=api_key,
        )

    elif action == "read_file":
        return await _handle_read_file(
            registry=registry,
            package_name=package_name,
            filename_sha256=filename_sha256,
            start_line=start_line,
            end_line=end_line,
            version=version,
        )


async def _handle_search(
    query: str | None,
    resource_types: list[str] | None,
    pattern: str | None,
    template: str | None,
    search_type: str,
    registry: str | None,
    domain: str | None,
    category: str | None,
    package_name: str | None,
    limit: int,
    api_key: str,
) -> dict[str, Any]:
    """Handle search action - delegates to search_devops_resources."""
    if not query and not pattern and not template and not package_name:
        raise ValueError("query, pattern, template, or package_name is required for action='search'")

    from wistx_mcp.tools.package_search import search_devops_resources

    return await search_devops_resources(
        query=query or "",
        resource_types=resource_types,
        pattern=pattern,
        template=template,
        search_type=search_type,
        registry=registry,
        domain=domain,
        category=category,
        package_name=package_name,
        limit=limit,
        api_key=api_key,
    )


async def _handle_read_file(
    registry: str | None,
    package_name: str | None,
    filename_sha256: str | None,
    start_line: int,
    end_line: int,
    version: str | None,
) -> dict[str, Any]:
    """Handle read_file action - delegates to read_package_file."""
    if not registry:
        raise ValueError("registry is required for action='read_file'")
    if not package_name:
        raise ValueError("package_name is required for action='read_file'")
    if not filename_sha256:
        raise ValueError(
            "filename_sha256 is required for action='read_file'. "
            "Use action='search' first to get the filename_sha256 from search results."
        )

    from wistx_mcp.tools.lib.package_read_file import read_package_file

    return await read_package_file(
        registry=registry,
        package_name=package_name,
        filename_sha256=filename_sha256,
        start_line=start_line,
        end_line=end_line,
        version=version,
    )
