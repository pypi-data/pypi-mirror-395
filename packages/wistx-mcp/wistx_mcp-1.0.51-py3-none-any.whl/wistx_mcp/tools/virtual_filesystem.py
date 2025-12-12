"""Virtual filesystem tools for infrastructure-aware file navigation."""

import logging
from typing import Any

from wistx_mcp.tools.lib.api_client import WISTXAPIClient
from wistx_mcp.tools.lib.auth_context import validate_api_key_and_get_user_id
from wistx_mcp.tools.lib.plan_enforcement import require_query_quota

logger = logging.getLogger(__name__)

api_client = WISTXAPIClient()


@require_query_quota
async def wistx_list_filesystem(
    resource_id: str,
    api_key: str,
    path: str = "/",
    view_mode: str = "standard",
    include_metadata: bool = False,
) -> dict[str, Any]:
    """List directory contents in virtual filesystem with infrastructure-aware views.

    Args:
        resource_id: Resource ID to list filesystem for
        api_key: WISTX API key for authentication
        path: Directory path to list (default: '/')
        view_mode: View mode - 'standard', 'infrastructure', 'compliance', 'costs', 'security'
        include_metadata: Include full infrastructure metadata in response

    Returns:
        Dictionary with directory listing:
        {
            "resource_id": "...",
            "path": "/",
            "entries": [
                {
                    "entry_id": "fs_abc123",
                    "name": "infrastructure",
                    "type": "directory",
                    "path": "/infrastructure",
                    "children_count": 5,
                    ...
                }
            ],
            "total": 10
        }
    """
    user_id = await validate_api_key_and_get_user_id(api_key)
    if not user_id:
        raise ValueError("Authentication required - api_key is invalid")

    if view_mode not in ["standard", "infrastructure", "compliance", "costs", "security"]:
        raise ValueError(
            f"Invalid view_mode: {view_mode}. "
            "Must be one of: standard, infrastructure, compliance, costs, security"
        )

    try:
        response = await api_client.list_filesystem(
            resource_id=resource_id,
            path=path,
            view_mode=view_mode,
            include_metadata=include_metadata,
            api_key=api_key,
        )

        return response.get("data") or response

    except Exception as e:
        logger.error("Error in wistx_list_filesystem: %s", e, exc_info=True)
        raise


@require_query_quota
async def wistx_read_file_with_context(
    resource_id: str,
    path: str,
    api_key: str,
    start_line: int | None = None,
    end_line: int | None = None,
    include_dependencies: bool = False,
    include_compliance: bool = False,
    include_costs: bool = False,
    include_security: bool = False,
) -> dict[str, Any]:
    """Read file from virtual filesystem with optional context (dependencies, compliance, costs, security).

    Args:
        resource_id: Resource ID
        path: Virtual filesystem path to file
        api_key: WISTX API key for authentication
        start_line: Start line number (1-based, inclusive)
        end_line: End line number (1-based, inclusive)
        include_dependencies: Include file dependencies (direct/transitive/reverse)
        include_compliance: Include compliance controls and violations
        include_costs: Include cost estimates and breakdown
        include_security: Include security issues and recommendations

    Returns:
        Dictionary with file content and context:
        {
            "entry_id": "fs_abc123",
            "path": "/infrastructure/terraform/modules/vpc/main.tf",
            "name": "main.tf",
            "content": "...",
            "line_count": 150,
            "language": "terraform",
            "dependencies": {...},  # If include_dependencies=True
            "compliance": {...},     # If include_compliance=True
            "costs": {...},          # If include_costs=True
            "security": {...}        # If include_security=True
        }
    """
    user_id = await validate_api_key_and_get_user_id(api_key)
    if not user_id:
        raise ValueError("Authentication required - api_key is invalid")

    if start_line is not None and start_line < 1:
        raise ValueError("start_line must be >= 1")
    if end_line is not None and end_line < 1:
        raise ValueError("end_line must be >= 1")
    if start_line is not None and end_line is not None and start_line > end_line:
        raise ValueError("start_line must be <= end_line")

    try:
        response = await api_client.read_file_with_context(
            resource_id=resource_id,
            path=path,
            start_line=start_line,
            end_line=end_line,
            include_dependencies=include_dependencies,
            include_compliance=include_compliance,
            include_costs=include_costs,
            include_security=include_security,
            api_key=api_key,
        )

        return response.get("data") or response

    except Exception as e:
        logger.error("Error in wistx_read_file_with_context: %s", e, exc_info=True)
        raise


@require_query_quota
async def wistx_get_filesystem_tree(
    resource_id: str,
    api_key: str,
    root_path: str = "/",
    max_depth: int = 10,
    view_mode: str = "standard",
) -> dict[str, Any]:
    """Get filesystem tree structure with multiple view modes.

    Args:
        resource_id: Resource ID
        api_key: WISTX API key for authentication
        root_path: Root path for tree (default: '/')
        max_depth: Maximum depth to traverse (default: 10)
        view_mode: View mode - 'standard', 'infrastructure', 'compliance', 'costs', 'security'

    Returns:
        Dictionary with tree structure:
        {
            "path": "/",
            "name": "/",
            "type": "directory",
            "children": [
                {
                    "path": "/infrastructure",
                    "name": "infrastructure",
                    "type": "directory",
                    "children": [...]
                }
            ]
        }
    """
    user_id = await validate_api_key_and_get_user_id(api_key)
    if not user_id:
        raise ValueError("Authentication required - api_key is invalid")

    if view_mode not in ["standard", "infrastructure", "compliance", "costs", "security"]:
        raise ValueError(
            f"Invalid view_mode: {view_mode}. "
            "Must be one of: standard, infrastructure, compliance, costs, security"
        )

    if max_depth < 1 or max_depth > 50:
        raise ValueError("max_depth must be between 1 and 50")

    try:
        response = await api_client.get_filesystem_tree(
            resource_id=resource_id,
            root_path=root_path,
            max_depth=max_depth,
            view_mode=view_mode,
            api_key=api_key,
        )

        return response.get("data") or response

    except Exception as e:
        logger.error("Error in wistx_get_filesystem_tree: %s", e, exc_info=True)
        raise


@require_query_quota
async def wistx_glob_infrastructure(
    resource_id: str,
    pattern: str,
    api_key: str,
    entry_type: str | None = None,
    code_type: str | None = None,
    cloud_provider: str | None = None,
) -> dict[str, Any]:
    """Find filesystem entries matching glob pattern with infrastructure filters.

    Args:
        resource_id: Resource ID
        pattern: Glob pattern (e.g., '**/*.tf', '/infrastructure/**')
        api_key: WISTX API key for authentication
        entry_type: Filter by entry type ('file', 'directory', 'terraform_module', etc.)
        code_type: Filter by code type ('terraform', 'kubernetes', 'docker', etc.)
        cloud_provider: Filter by cloud provider ('aws', 'gcp', 'azure')

    Returns:
        Dictionary with matching entries:
        {
            "resource_id": "...",
            "pattern": "**/*.tf",
            "matches": [
                {
                    "entry_id": "fs_abc123",
                    "path": "/infrastructure/terraform/modules/vpc/main.tf",
                    "name": "main.tf",
                    ...
                }
            ],
            "total": 5
        }
    """
    user_id = await validate_api_key_and_get_user_id(api_key)
    if not user_id:
        raise ValueError("Authentication required - api_key is invalid")

    if not pattern:
        raise ValueError("pattern is required")

    try:
        response = await api_client.glob_infrastructure(
            resource_id=resource_id,
            pattern=pattern,
            entry_type=entry_type,
            code_type=code_type,
            cloud_provider=cloud_provider,
            api_key=api_key,
        )

        return response.get("data") or response

    except Exception as e:
        logger.error("Error in wistx_glob_infrastructure: %s", e, exc_info=True)
        raise

