"""Intelligent context endpoints for multi-resource context storage."""

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import get_current_user
from api.models.intelligent_context import ContextSaveRequest, ContextStatus, ContextType
from api.models.v1_responses import ErrorResponse
from api.services.intelligent_context_service import intelligent_context_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/contexts", tags=["contexts"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Save context with automatic analysis",
    description="Save context with automatic infrastructure analysis (compliance, costs, security)",
)
async def save_context_with_analysis(
    request: ContextSaveRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Save context with automatic analysis.

    Args:
        request: Context save request
        current_user: Current authenticated user

    Returns:
        Dictionary with saved context

    Raises:
        HTTPException: If validation fails
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    try:
        context_type_enum = ContextType(request.context_type)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid context_type: {request.context_type}",
        ) from None

    organization_id = current_user.get("organization_id")

    try:
        context = await intelligent_context_service.save_context_with_analysis(
            user_id=user_id,
            context_type=context_type_enum,
            title=request.title,
            summary=request.summary,
            description=request.description,
            conversation_history=request.conversation_history,
            code_snippets=request.code_snippets,
            plans=request.plans,
            decisions=request.decisions,
            infrastructure_resources=request.infrastructure_resources,
            linked_resources=request.linked_resources,
            tags=request.tags,
            workspace=request.workspace,
            organization_id=organization_id,
            auto_analyze=request.auto_analyze,
        )

        return {"data": context.model_dump()}

    except ValueError as e:
        logger.warning("Invalid request for save_context_with_analysis: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error saving context: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save context",
        ) from e


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    summary="Intelligent context search",
    description="Search contexts intelligently with infrastructure awareness",
)
async def search_contexts_intelligently(
    query: str,
    context_type: str | None = None,
    compliance_standard: str | None = None,
    cost_range: dict[str, float] | None = None,
    security_score_min: float | None = None,
    limit: int = 50,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Search contexts intelligently.

    Args:
        query: Search query
        context_type: Filter by context type
        compliance_standard: Filter by compliance standard
        cost_range: Filter by cost range
        security_score_min: Minimum security score
        limit: Maximum results
        current_user: Current authenticated user

    Returns:
        Dictionary with search results

    Raises:
        HTTPException: If validation fails
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    if not query or len(query) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query must be at least 3 characters",
        )

    if limit < 1 or limit > 500:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="limit must be between 1 and 500",
        )

    context_type_enum = None
    if context_type:
        try:
            context_type_enum = ContextType(context_type)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid context_type: {context_type}",
            ) from None

    organization_id = current_user.get("organization_id")

    try:
        results = await intelligent_context_service.search_contexts_intelligently(
            user_id=user_id,
            query=query,
            context_type=context_type_enum,
            compliance_standard=compliance_standard,
            cost_range=cost_range,
            security_score_min=security_score_min,
            limit=limit,
            organization_id=organization_id,
            include_organization=True if organization_id else False,
        )

        return {
            "data": {
                "query": query,
                "results": results,
                "total": len(results),
            }
        }

    except ValueError as e:
        logger.warning("Invalid request for search_contexts_intelligently: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error searching contexts: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search contexts",
        ) from e


@router.get(
    "/{context_id}",
    status_code=status.HTTP_200_OK,
    summary="Get context by ID",
    description="Retrieve context by ID with full analysis",
)
async def get_context(
    context_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Get context by ID.

    Args:
        context_id: Context ID
        current_user: Current authenticated user

    Returns:
        Dictionary with context details

    Raises:
        HTTPException: If context not found
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    try:
        context = await intelligent_context_service.get_context(
            context_id=context_id,
            user_id=user_id,
        )

        if not context:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Context not found: {context_id}",
            )

        return {"data": context.model_dump()}

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting context: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get context",
        ) from e


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="List contexts",
    description="List contexts with filtering",
)
async def list_contexts(
    context_type: str | None = None,
    status: str | None = None,
    workspace: str | None = None,
    tags: list[str] | None = None,
    limit: int = 100,
    offset: int = 0,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """List contexts with filtering.

    Args:
        context_type: Filter by context type
        status: Filter by status
        workspace: Filter by workspace
        tags: Filter by tags
        limit: Maximum results
        offset: Offset for pagination
        current_user: Current authenticated user

    Returns:
        Dictionary with contexts list

    Raises:
        HTTPException: If validation fails
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    if limit < 1 or limit > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="limit must be between 1 and 1000",
        )
    if offset < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="offset must be >= 0",
        )

    context_type_enum = None
    if context_type:
        try:
            context_type_enum = ContextType(context_type)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid context_type: {context_type}",
            ) from None

    status_enum = None
    if status:
        try:
            status_enum = ContextStatus(status)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status: {status}",
            ) from None

    organization_id = current_user.get("organization_id")

    try:
        contexts = await intelligent_context_service.list_contexts(
            user_id=user_id,
            context_type=context_type_enum,
            status=status_enum,
            workspace=workspace,
            tags=tags,
            limit=limit,
            offset=offset,
            organization_id=organization_id,
            include_organization=True if organization_id else False,
        )

        return {
            "data": {
                "contexts": contexts,
                "total": len(contexts),
                "limit": limit,
                "offset": offset,
            }
        }

    except HTTPException:
        raise
    except ValueError as e:
        logger.warning("Invalid request for list_contexts: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error listing contexts: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list contexts",
        ) from e


@router.post(
    "/{context_id}/links",
    status_code=status.HTTP_201_CREATED,
    summary="Link contexts",
    description="Link contexts with semantic relationship",
)
async def link_contexts(
    context_id: str,
    target_context_id: str,
    relationship_type: str,
    strength: float = 1.0,
    metadata: dict[str, Any] | None = None,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Link contexts.

    Args:
        context_id: Source context ID
        target_context_id: Target context ID
        relationship_type: Relationship type
        strength: Relationship strength
        metadata: Additional metadata
        current_user: Current authenticated user

    Returns:
        Dictionary with link information

    Raises:
        HTTPException: If validation fails
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    if not target_context_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="target_context_id is required",
        )

    if context_id == target_context_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="source_context_id and target_context_id must be different",
        )

    if strength < 0.0 or strength > 1.0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="strength must be between 0.0 and 1.0",
        )

    try:
        link = await intelligent_context_service.link_contexts(
            source_context_id=context_id,
            target_context_id=target_context_id,
            relationship_type=relationship_type,
            strength=strength,
            metadata=metadata,
        )

        return {"data": link.model_dump()}

    except ValueError as e:
        logger.warning("Invalid request for link_contexts: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error linking contexts: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to link contexts",
        ) from e


@router.get(
    "/{context_id}/graph",
    status_code=status.HTTP_200_OK,
    summary="Get context graph",
    description="Get context dependency graph showing relationships",
)
async def get_context_graph(
    context_id: str,
    depth: int = 2,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Get context dependency graph.

    Args:
        context_id: Root context ID
        depth: Maximum depth to traverse
        current_user: Current authenticated user

    Returns:
        Dictionary with graph structure

    Raises:
        HTTPException: If validation fails
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    if depth < 1 or depth > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="depth must be between 1 and 10",
        )

    try:
        graph = await intelligent_context_service.get_context_graph(
            context_id=context_id,
            depth=depth,
            user_id=user_id,
        )

        return {"data": graph}

    except ValueError as e:
        logger.warning("Invalid request for get_context_graph: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error getting context graph: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get context graph",
        ) from e

