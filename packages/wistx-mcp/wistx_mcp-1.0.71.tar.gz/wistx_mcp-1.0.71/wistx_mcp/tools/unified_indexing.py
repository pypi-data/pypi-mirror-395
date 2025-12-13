"""Unified indexing and resource management tool.

This module merges indexing and resource management into one unified interface:
- index_repository (index GitHub repos)
- index_content (index documentation/documents)
- list_resources, check_resource_status, delete_resource (manage_resources)

Usage:
    # Index a GitHub repository
    result = await wistx_index(action="repository", repo_url="https://github.com/org/repo", ...)

    # Index documentation website
    result = await wistx_index(action="content", content_url="https://docs.example.com", ...)

    # List indexed resources
    result = await wistx_index(action="list", ...)

    # Check indexing status
    result = await wistx_index(action="status", resource_id="res_xxx", ...)

    # Delete a resource
    result = await wistx_index(action="delete", resource_type="repository", identifier="...", ...)
"""

import logging
from typing import Any

from wistx_mcp.tools.lib.plan_enforcement import require_query_quota

logger = logging.getLogger(__name__)

# Valid actions
INDEX_ACTIONS = ["repository", "content"]
MANAGE_ACTIONS = ["list", "status", "delete"]
ALL_VALID_ACTIONS = INDEX_ACTIONS + MANAGE_ACTIONS


@require_query_quota
async def wistx_index(
    # REQUIRED
    action: str,

    # API KEY (optional - uses context or MCP initialization)
    api_key: str | None = None,

    # === INDEX REPOSITORY (action="repository") ===
    repo_url: str | None = None,
    branch: str = "main",
    github_token: str | None = None,
    
    # === INDEX CONTENT (action="content") ===
    content_url: str | None = None,
    file_path: str | None = None,
    content_type: str | None = None,
    
    # === COMMON FOR INDEXING ===
    name: str | None = None,
    description: str | None = None,
    tags: list[str] | None = None,
    include_patterns: list[str] | None = None,
    exclude_patterns: list[str] | None = None,
    
    # === RESOURCE MANAGEMENT (action="list", "status", "delete") ===
    resource_type: str | None = None,
    resource_id: str | None = None,
    identifier: str | None = None,
    status_filter: str | None = None,
    include_ai_analysis: bool = True,
    deduplicate: bool = True,
    show_duplicates: bool = False,
) -> dict[str, Any]:
    """Unified indexing and resource management.

    **Actions:**

    INDEXING:
    - "repository": Index a GitHub repository (public or private)
    - "content": Index documentation website or document file

    RESOURCE MANAGEMENT:
    - "list": List all indexed resources
    - "status": Check indexing status for a specific resource
    - "delete": Delete an indexed resource

    Args:
        action: Operation to perform (required)
        api_key: WISTX API key for authentication (required)

        For repository:
        - repo_url: GitHub repository URL (required)
        - branch: Branch to index (default: "main")
        - github_token: Personal access token (optional, OAuth used if available)
        - name: Custom name for the resource
        - description: Resource description
        - tags: Tags for categorization
        - include_patterns: File patterns to include (glob)
        - exclude_patterns: File patterns to exclude (glob)

        For content:
        - content_url: Documentation website URL or document URL
        - file_path: Local file path (alternative to content_url)
        - content_type: "documentation", "pdf", "docx", "markdown" (auto-detected if omitted)
        - name: Custom name for the resource
        - description: Resource description
        - tags: Tags for categorization
        - include_patterns: URL patterns to include (for docs)
        - exclude_patterns: URL patterns to exclude (for docs)

        For list:
        - resource_type: Filter by type (repository, documentation, document)
        - status_filter: Filter by status (pending, indexing, completed, failed)
        - include_ai_analysis: Include AI insights (default: True)
        - deduplicate: Show only latest per repo (default: True)
        - show_duplicates: Include duplicate info (default: False)

        For status:
        - resource_id: Resource ID (required)

        For delete:
        - resource_type: Type of resource (required)
        - identifier: Resource identifier - URL, owner/repo, or resource_id (required)

    Returns:
        Dictionary with results specific to the action

    Raises:
        ValueError: If invalid action or missing required parameters
        RuntimeError: If operation fails
    """
    if action not in ALL_VALID_ACTIONS:
        raise ValueError(
            f"Invalid action: {action}. "
            f"Valid actions: {', '.join(ALL_VALID_ACTIONS)}"
        )
    
    logger.info("Unified indexing: action=%s", action)
    
    # Route to appropriate handler
    if action == "repository":
        return await _handle_index_repository(
            repo_url=repo_url,
            branch=branch,
            name=name,
            description=description,
            tags=tags,
            github_token=github_token,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
            api_key=api_key,
        )
    
    elif action == "content":
        return await _handle_index_content(
            content_url=content_url,
            file_path=file_path,
            content_type=content_type,
            name=name,
            description=description,
            tags=tags,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
            api_key=api_key,
        )
    
    elif action == "list":
        return await _handle_list_resources(
            resource_type=resource_type,
            status=status_filter,
            api_key=api_key,
            include_ai_analysis=include_ai_analysis,
            deduplicate=deduplicate,
            show_duplicates=show_duplicates,
        )

    elif action == "status":
        return await _handle_check_status(
            resource_id=resource_id,
            api_key=api_key,
        )

    elif action == "delete":
        return await _handle_delete_resource(
            resource_type=resource_type,
            identifier=identifier,
            api_key=api_key,
        )


async def _handle_index_repository(
    repo_url: str | None,
    branch: str,
    name: str | None,
    description: str | None,
    tags: list[str] | None,
    github_token: str | None,
    include_patterns: list[str] | None,
    exclude_patterns: list[str] | None,
    api_key: str,
) -> dict[str, Any]:
    """Handle repository action - delegates to index_repository."""
    if not repo_url:
        raise ValueError("repo_url is required for action='repository'")

    from wistx_mcp.tools.user_indexing import index_repository

    return await index_repository(
        repo_url=repo_url,
        branch=branch,
        name=name,
        description=description,
        tags=tags,
        github_token=github_token,
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
        api_key=api_key,
    )


async def _handle_index_content(
    content_url: str | None,
    file_path: str | None,
    content_type: str | None,
    name: str | None,
    description: str | None,
    tags: list[str] | None,
    include_patterns: list[str] | None,
    exclude_patterns: list[str] | None,
    api_key: str,
) -> dict[str, Any]:
    """Handle content action - delegates to index_content."""
    if not content_url and not file_path:
        raise ValueError("content_url or file_path is required for action='content'")

    from wistx_mcp.tools.user_indexing import index_content

    return await index_content(
        content_url=content_url,
        file_path=file_path,
        content_type=content_type,
        name=name,
        description=description,
        tags=tags,
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
        api_key=api_key,
    )


async def _handle_list_resources(
    resource_type: str | None,
    status: str | None,
    api_key: str,
    include_ai_analysis: bool,
    deduplicate: bool,
    show_duplicates: bool,
) -> dict[str, Any]:
    """Handle list action - delegates to list_resources."""
    from wistx_mcp.tools.user_indexing import list_resources

    return await list_resources(
        resource_type=resource_type,
        status=status,
        api_key=api_key,
        include_ai_analysis=include_ai_analysis,
        deduplicate=deduplicate,
        show_duplicates=show_duplicates,
    )


async def _handle_check_status(
    resource_id: str | None,
    api_key: str,
) -> dict[str, Any]:
    """Handle status action - delegates to check_resource_status."""
    if not resource_id:
        raise ValueError("resource_id is required for action='status'. Use action='list' first to get resource IDs.")

    from wistx_mcp.tools.user_indexing import check_resource_status

    return await check_resource_status(
        resource_id=resource_id,
        api_key=api_key,
    )


async def _handle_delete_resource(
    resource_type: str | None,
    identifier: str | None,
    api_key: str,
) -> dict[str, Any]:
    """Handle delete action - delegates to delete_resource."""
    if not resource_type:
        raise ValueError("resource_type is required for action='delete'")
    if not identifier:
        raise ValueError("identifier is required for action='delete'")

    from wistx_mcp.tools.user_indexing import delete_resource

    return await delete_resource(
        resource_type=resource_type,
        identifier=identifier,
        api_key=api_key,
    )

