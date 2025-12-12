"""Virtual filesystem endpoints for infrastructure-aware file navigation."""

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import get_current_user
from api.models.v1_responses import ErrorResponse
from api.services.virtual_filesystem_service import virtual_filesystem_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/filesystem", tags=["filesystem"])


@router.post(
    "/{resource_id}/list",
    status_code=status.HTTP_200_OK,
    summary="List directory contents",
    description="List directory contents in virtual filesystem with infrastructure-aware views",
)
async def list_filesystem(
    resource_id: str,
    path: str = "/",
    view_mode: str = "standard",
    include_metadata: bool = False,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """List directory contents in virtual filesystem.

    Args:
        resource_id: Resource ID to list filesystem for
        path: Directory path to list (default: '/')
        view_mode: View mode ('standard', 'infrastructure', 'compliance', 'costs', 'security')
        include_metadata: Include full infrastructure metadata
        current_user: Current authenticated user

    Returns:
        Dictionary with directory listing

    Raises:
        HTTPException: If resource not found or access denied
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    if view_mode not in ["standard", "infrastructure", "compliance", "costs", "security", "section"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid view_mode: {view_mode}. Must be one of: standard, infrastructure, compliance, costs, security, section",
        )

    try:
        if view_mode == "section":
            from api.services.section_organizer import section_organizer

            sections = await section_organizer.get_sections_for_resource(
                resource_id=resource_id,
                user_id=user_id,
            )

            return {
                "data": {
                    "resource_id": resource_id,
                    "view_mode": "section",
                    "sections": [s.model_dump() for s in sections],
                    "total": len(sections),
                }
            }

        entries = await virtual_filesystem_service.list_directory(
            resource_id=resource_id,
            path=path,
            user_id=user_id,
            view_mode=view_mode,
            include_metadata=include_metadata,
        )

        return {
            "data": {
                "resource_id": resource_id,
                "path": path,
                "entries": entries,
                "total": len(entries),
            }
        }

    except ValueError as e:
        logger.warning("Invalid request for list_filesystem: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error listing filesystem: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list filesystem",
        ) from e


@router.post(
    "/{resource_id}/read",
    status_code=status.HTTP_200_OK,
    summary="Read file with context",
    description="Read file from virtual filesystem with optional context (dependencies, compliance, costs, security)",
)
async def read_file_with_context(
    resource_id: str,
    path: str,
    start_line: int | None = None,
    end_line: int | None = None,
    include_dependencies: bool = False,
    include_compliance: bool = False,
    include_costs: bool = False,
    include_security: bool = False,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Read file from virtual filesystem with optional context.

    Args:
        resource_id: Resource ID
        path: Virtual filesystem path to file
        start_line: Start line number (1-based, inclusive)
        end_line: End line number (1-based, inclusive)
        include_dependencies: Include file dependencies
        include_compliance: Include compliance controls
        include_costs: Include cost estimates
        include_security: Include security issues
        current_user: Current authenticated user

    Returns:
        Dictionary with file content and context

    Raises:
        HTTPException: If file not found or access denied
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    if start_line is not None and start_line < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_line must be >= 1",
        )
    if end_line is not None and end_line < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="end_line must be >= 1",
        )
    if start_line is not None and end_line is not None and start_line > end_line:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_line must be <= end_line",
        )

    try:
        entry = await virtual_filesystem_service.get_entry(
            resource_id=resource_id,
            path=path,
            user_id=user_id,
        )

        if not entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File not found: {path}",
            )

        result = entry.model_dump()

        if include_dependencies and entry.infrastructure_metadata:
            result["dependencies"] = {
                "direct": entry.infrastructure_metadata.dependencies or [],
                "dependents": entry.infrastructure_metadata.dependents or [],
            }

        if include_compliance and entry.infrastructure_metadata:
            result["compliance"] = {
                "standards": entry.infrastructure_metadata.compliance_standards or [],
            }

        if include_costs and entry.infrastructure_metadata:
            if entry.infrastructure_metadata.estimated_monthly_cost_usd:
                result["costs"] = {
                    "monthly_usd": entry.infrastructure_metadata.estimated_monthly_cost_usd,
                }

        if include_security and entry.infrastructure_metadata:
            if entry.infrastructure_metadata.security_score is not None:
                result["security"] = {
                    "score": entry.infrastructure_metadata.security_score,
                }

        try:
            from api.services.predictive_cache_service import predictive_cache_service

            await predictive_cache_service.track_access(
                user_id=user_id,
                resource_id=resource_id,
                path=path,
                access_type="read",
            )

            await predictive_cache_service.predict_and_prefetch(
                user_id=user_id,
                resource_id=resource_id,
                path=path,
                access_type="read",
            )
        except Exception as e:
            logger.debug("Error in predictive caching: %s", e)

        return {"data": result}

    except HTTPException:
        raise
    except ValueError as e:
        logger.warning("Invalid request for read_file_with_context: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error reading file with context: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to read file",
        ) from e


@router.post(
    "/{resource_id}/tree",
    status_code=status.HTTP_200_OK,
    summary="Get filesystem tree",
    description="Get filesystem tree structure with multiple view modes",
)
async def get_filesystem_tree(
    resource_id: str,
    root_path: str = "/",
    max_depth: int = 10,
    view_mode: str = "standard",
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Get filesystem tree structure.

    Args:
        resource_id: Resource ID
        root_path: Root path for tree (default: '/')
        max_depth: Maximum depth to traverse (default: 10)
        view_mode: View mode ('standard', 'infrastructure', 'compliance', 'costs', 'security')
        current_user: Current authenticated user

    Returns:
        Dictionary with tree structure

    Raises:
        HTTPException: If resource not found or access denied
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    if view_mode not in ["standard", "infrastructure", "compliance", "costs", "security", "section"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid view_mode: {view_mode}. Must be one of: standard, infrastructure, compliance, costs, security, section",
        )

    if max_depth < 1 or max_depth > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="max_depth must be between 1 and 50",
        )

    try:
        tree = await virtual_filesystem_service.get_tree(
            resource_id=resource_id,
            root_path=root_path,
            max_depth=max_depth,
            user_id=user_id,
            view_mode=view_mode,
        )

        return {"data": tree}

    except ValueError as e:
        logger.warning("Invalid request for get_filesystem_tree: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error getting filesystem tree: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get filesystem tree",
        ) from e


@router.post(
    "/{resource_id}/glob",
    status_code=status.HTTP_200_OK,
    summary="Glob pattern search",
    description="Find filesystem entries matching glob pattern with infrastructure filters",
)
async def glob_infrastructure(
    resource_id: str,
    pattern: str,
    entry_type: str | None = None,
    code_type: str | None = None,
    cloud_provider: str | None = None,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Find filesystem entries matching glob pattern.

    Args:
        resource_id: Resource ID
        pattern: Glob pattern (e.g., '**/*.tf', '/infrastructure/**')
        entry_type: Filter by entry type
        code_type: Filter by code type
        cloud_provider: Filter by cloud provider
        current_user: Current authenticated user

    Returns:
        Dictionary with matching entries

    Raises:
        HTTPException: If resource not found or access denied
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    if not pattern:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="pattern is required",
        )

    try:
        from api.models.virtual_filesystem import FilesystemEntryType

        entry_type_enum = None
        if entry_type:
            try:
                entry_type_enum = FilesystemEntryType(entry_type)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid entry_type: {entry_type}",
                ) from None

        matches = await virtual_filesystem_service.glob(
            resource_id=resource_id,
            pattern=pattern,
            user_id=user_id,
            entry_type=entry_type_enum,
            code_type=code_type,
            cloud_provider=cloud_provider,
        )

        return {
            "data": {
                "resource_id": resource_id,
                "pattern": pattern,
                "matches": matches,
                "total": len(matches),
            }
        }

    except HTTPException:
        raise
    except ValueError as e:
        logger.warning("Invalid request for glob_infrastructure: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error globbing infrastructure: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to glob infrastructure",
        ) from e

