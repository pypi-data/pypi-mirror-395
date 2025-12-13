"""Unified context management tool - filesystem navigation and conversation context.

This module merges filesystem and context tools into one unified interface:
- wistx_list_filesystem (list directory contents)
- wistx_read_file_with_context (read file with analysis)
- wistx_save_context_with_analysis (save conversation context)
- wistx_search_contexts_intelligently (search saved contexts)
- wistx_get_context (get context by ID)
- wistx_list_contexts (list saved contexts)

Usage:
    # List files in indexed repository
    result = await wistx_context(action="list_files", resource_id="res_xxx", path="/", ...)

    # Read file with context
    result = await wistx_context(action="read_file", resource_id="res_xxx", path="/main.tf", ...)

    # Save context
    result = await wistx_context(action="save", context_type="conversation", title="...", ...)

    # Search contexts
    result = await wistx_context(action="search", query="terraform vpc", ...)
"""

import logging
from typing import Any

from wistx_mcp.tools.lib.plan_enforcement import require_query_quota

logger = logging.getLogger(__name__)

# Valid actions
FILESYSTEM_ACTIONS = ["list_files", "read_file"]
CONTEXT_ACTIONS = ["save", "search", "get", "list_saved"]
ALL_VALID_ACTIONS = FILESYSTEM_ACTIONS + CONTEXT_ACTIONS


@require_query_quota
async def wistx_context(
    # REQUIRED
    action: str,

    # API KEY (optional - uses context or MCP initialization)
    api_key: str | None = None,

    # === FILESYSTEM OPERATIONS (list_files, read_file) ===
    resource_id: str | None = None,
    path: str = "/",
    view_mode: str = "standard",
    include_metadata: bool = False,
    start_line: int | None = None,
    end_line: int | None = None,
    include_dependencies: bool = False,
    include_compliance: bool = False,
    include_costs: bool = False,
    include_security: bool = False,

    # === CONTEXT SAVE (save) ===
    context_type: str | None = None,
    title: str | None = None,
    summary: str | None = None,
    description: str | None = None,
    conversation_history: list[dict[str, Any]] | None = None,
    code_snippets: list[dict[str, Any]] | None = None,
    plans: list[dict[str, Any]] | None = None,
    decisions: list[dict[str, Any]] | None = None,
    infrastructure_resources: list[dict[str, Any]] | None = None,
    linked_resources: list[str] | None = None,
    tags: list[str] | None = None,
    workspace: str | None = None,
    auto_analyze: bool = True,

    # === CONTEXT SEARCH (search) ===
    query: str | None = None,
    compliance_standard: str | None = None,
    cost_range: dict[str, float] | None = None,
    security_score_min: float | None = None,

    # === GET/LIST SAVED (get, list_saved) ===
    context_id: str | None = None,
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    """Unified context management - filesystem navigation and conversation context.

    **Actions:**

    FILESYSTEM:
    - "list_files": List directory contents in indexed repository
    - "read_file": Read file with optional analysis context

    CONTEXT MANAGEMENT:
    - "save": Save conversation/design context with analysis
    - "search": Search saved contexts intelligently
    - "get": Get specific saved context by ID
    - "list_saved": List all saved contexts

    Args:
        action: Operation to perform (required)
        api_key: WISTX API key for authentication (required)

        For list_files:
        - resource_id: Resource ID (required)
        - path: Directory path (default: "/")
        - view_mode: standard, infrastructure, compliance, costs, security
        - include_metadata: Include full metadata

        For read_file:
        - resource_id: Resource ID (required)
        - path: File path (required)
        - start_line: Start line (1-based)
        - end_line: End line (1-based)
        - include_dependencies: Include dependency analysis
        - include_compliance: Include compliance controls
        - include_costs: Include cost estimates
        - include_security: Include security issues

        For save:
        - context_type: conversation, architecture_design, code_review, etc. (required)
        - title: Context title (required)
        - summary: Context summary (required)
        - description: Detailed description
        - conversation_history: Conversation messages
        - code_snippets: Referenced code
        - plans: Plans or workflows
        - decisions: Decisions made
        - infrastructure_resources: Infrastructure resource refs
        - linked_resources: Linked resource IDs
        - tags: Tags for categorization
        - workspace: Workspace identifier
        - auto_analyze: Auto-analyze infrastructure (default: True)

        For search:
        - query: Search query (required)
        - context_type: Filter by type
        - compliance_standard: Filter by standard (PCI-DSS, HIPAA)
        - cost_range: {"min": 0.0, "max": 1000.0}
        - security_score_min: Minimum security score (0-100)
        - limit: Max results

        For get:
        - context_id: Context ID (required)

        For list_saved:
        - context_type: Filter by type
        - status: Filter by status (active, archived)
        - workspace: Filter by workspace
        - tags: Filter by tags
        - limit: Max results
        - offset: Pagination offset

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

    logger.info("Unified context: action=%s", action)

    # Route to appropriate handler
    if action == "list_files":
        return await _handle_list_files(
            resource_id=resource_id,
            api_key=api_key,
            path=path,
            view_mode=view_mode,
            include_metadata=include_metadata,
        )

    elif action == "read_file":
        return await _handle_read_file(
            resource_id=resource_id,
            path=path,
            api_key=api_key,
            start_line=start_line,
            end_line=end_line,
            include_dependencies=include_dependencies,
            include_compliance=include_compliance,
            include_costs=include_costs,
            include_security=include_security,
        )

    elif action == "save":
        return await _handle_save_context(
            api_key=api_key,
            context_type=context_type,
            title=title,
            summary=summary,
            description=description,
            conversation_history=conversation_history,
            code_snippets=code_snippets,
            plans=plans,
            decisions=decisions,
            infrastructure_resources=infrastructure_resources,
            linked_resources=linked_resources,
            tags=tags,
            workspace=workspace,
            auto_analyze=auto_analyze,
        )

    elif action == "search":
        return await _handle_search_contexts(
            query=query,
            api_key=api_key,
            context_type=context_type,
            compliance_standard=compliance_standard,
            cost_range=cost_range,
            security_score_min=security_score_min,
            limit=limit,
        )

    elif action == "get":
        return await _handle_get_context(
            context_id=context_id,
            api_key=api_key,
        )

    elif action == "list_saved":
        return await _handle_list_contexts(
            api_key=api_key,
            context_type=context_type,
            status=status,
            workspace=workspace,
            tags=tags,
            limit=limit,
            offset=offset,
        )


async def _handle_list_files(
    resource_id: str | None,
    api_key: str,
    path: str,
    view_mode: str,
    include_metadata: bool,
) -> dict[str, Any]:
    """Handle list_files action - delegates to wistx_list_filesystem."""
    if not resource_id:
        raise ValueError("resource_id is required for action='list_files'")

    from wistx_mcp.tools.virtual_filesystem import wistx_list_filesystem

    return await wistx_list_filesystem(
        resource_id=resource_id,
        api_key=api_key,
        path=path,
        view_mode=view_mode,
        include_metadata=include_metadata,
    )


async def _handle_read_file(
    resource_id: str | None,
    path: str,
    api_key: str,
    start_line: int | None,
    end_line: int | None,
    include_dependencies: bool,
    include_compliance: bool,
    include_costs: bool,
    include_security: bool,
) -> dict[str, Any]:
    """Handle read_file action - delegates to wistx_read_file_with_context."""
    if not resource_id:
        raise ValueError("resource_id is required for action='read_file'")
    if not path or path == "/":
        raise ValueError("path must be specified for action='read_file'")

    from wistx_mcp.tools.virtual_filesystem import wistx_read_file_with_context

    return await wistx_read_file_with_context(
        resource_id=resource_id,
        path=path,
        api_key=api_key,
        start_line=start_line,
        end_line=end_line,
        include_dependencies=include_dependencies,
        include_compliance=include_compliance,
        include_costs=include_costs,
        include_security=include_security,
    )



async def _handle_save_context(
    api_key: str,
    context_type: str | None,
    title: str | None,
    summary: str | None,
    description: str | None,
    conversation_history: list[dict[str, Any]] | None,
    code_snippets: list[dict[str, Any]] | None,
    plans: list[dict[str, Any]] | None,
    decisions: list[dict[str, Any]] | None,
    infrastructure_resources: list[dict[str, Any]] | None,
    linked_resources: list[str] | None,
    tags: list[str] | None,
    workspace: str | None,
    auto_analyze: bool,
) -> dict[str, Any]:
    """Handle save action - delegates to wistx_save_context_with_analysis."""
    if not context_type:
        raise ValueError("context_type is required for action='save'")
    if not title:
        raise ValueError("title is required for action='save'")
    if not summary:
        raise ValueError("summary is required for action='save'")

    from wistx_mcp.tools.intelligent_context import wistx_save_context_with_analysis

    return await wistx_save_context_with_analysis(
        context_type=context_type,
        title=title,
        summary=summary,
        api_key=api_key,
        description=description,
        conversation_history=conversation_history,
        code_snippets=code_snippets,
        plans=plans,
        decisions=decisions,
        infrastructure_resources=infrastructure_resources,
        linked_resources=linked_resources,
        tags=tags,
        workspace=workspace,
        auto_analyze=auto_analyze,
    )


async def _handle_search_contexts(
    query: str | None,
    api_key: str,
    context_type: str | None,
    compliance_standard: str | None,
    cost_range: dict[str, float] | None,
    security_score_min: float | None,
    limit: int,
) -> dict[str, Any]:
    """Handle search action - delegates to wistx_search_contexts_intelligently."""
    if not query:
        raise ValueError("query is required for action='search'")

    from wistx_mcp.tools.intelligent_context import wistx_search_contexts_intelligently

    return await wistx_search_contexts_intelligently(
        query=query,
        api_key=api_key,
        context_type=context_type,
        compliance_standard=compliance_standard,
        cost_range=cost_range,
        security_score_min=security_score_min,
        limit=limit,
    )


async def _handle_get_context(
    context_id: str | None,
    api_key: str,
) -> dict[str, Any]:
    """Handle get action - delegates to wistx_get_context."""
    if not context_id:
        raise ValueError("context_id is required for action='get'")

    from wistx_mcp.tools.intelligent_context import wistx_get_context

    return await wistx_get_context(
        context_id=context_id,
        api_key=api_key,
    )


async def _handle_list_contexts(
    api_key: str,
    context_type: str | None,
    status: str | None,
    workspace: str | None,
    tags: list[str] | None,
    limit: int,
    offset: int,
) -> dict[str, Any]:
    """Handle list_saved action - delegates to wistx_list_contexts."""
    from wistx_mcp.tools.intelligent_context import wistx_list_contexts

    return await wistx_list_contexts(
        api_key=api_key,
        context_type=context_type,
        status=status,
        workspace=workspace,
        tags=tags,
        limit=limit,
        offset=offset,
    )

