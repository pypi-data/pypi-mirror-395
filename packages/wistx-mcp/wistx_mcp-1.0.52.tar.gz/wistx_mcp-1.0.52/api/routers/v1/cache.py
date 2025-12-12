"""Predictive cache endpoints."""

import logging
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import get_current_user
from api.models.predictive_cache import CacheEntryType
from api.services.predictive_cache_service import predictive_cache_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/cache", tags=["cache"])


@router.post(
    "/prefetch",
    status_code=status.HTTP_200_OK,
    summary="Prefetch predicted files",
    description="Predict likely next accesses and pre-cache them",
)
async def prefetch_context(
    resource_id: str,
    path: str,
    access_type: str = "read",
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Prefetch predicted files.

    Args:
        resource_id: Resource ID
        path: Current file path
        access_type: Access type (read, search, list)
        current_user: Current authenticated user

    Returns:
        Dictionary with prefetched paths

    Raises:
        HTTPException: If validation fails
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    if not resource_id or not path:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="resource_id and path are required",
        )

    valid_access_types = ["read", "search", "list"]
    if access_type not in valid_access_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"access_type must be one of: {', '.join(valid_access_types)}",
        )

    try:
        prefetched = await predictive_cache_service.predict_and_prefetch(
            user_id=user_id,
            resource_id=resource_id,
            path=path,
            access_type=access_type,
        )

        return {
            "data": {
                "prefetched_paths": prefetched,
                "count": len(prefetched),
            }
        }

    except Exception as e:
        logger.error("Error prefetching: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to prefetch",
        ) from e


@router.get(
    "/status",
    status_code=status.HTTP_200_OK,
    summary="Get cache status",
    description="Get cache statistics",
)
async def get_cache_status(
    resource_id: Optional[str] = None,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Get cache status.

    Args:
        resource_id: Resource ID (optional)
        current_user: Current authenticated user

    Returns:
        Dictionary with cache statistics

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
        cache_status = await predictive_cache_service.get_cache_status(
            user_id=user_id,
            resource_id=resource_id,
        )

        return {"data": cache_status}

    except Exception as e:
        logger.error("Error getting cache status: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get cache status",
        ) from e


@router.delete(
    "",
    status_code=status.HTTP_200_OK,
    summary="Invalidate cache",
    description="Invalidate cache entries",
)
async def invalidate_cache(
    resource_id: Optional[str] = None,
    key: Optional[str] = None,
    entry_type: Optional[str] = None,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Invalidate cache entries.

    Args:
        resource_id: Resource ID (optional)
        key: Cache key (optional)
        entry_type: Entry type (optional)
        current_user: Current authenticated user

    Returns:
        Dictionary with invalidation results

    Raises:
        HTTPException: If validation fails
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    entry_type_enum = None
    if entry_type:
        try:
            entry_type_enum = CacheEntryType(entry_type)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid entry_type: {entry_type}",
            ) from None

    try:
        invalidated_count = await predictive_cache_service.invalidate_cache(
            user_id=user_id,
            resource_id=resource_id,
            key=key,
            entry_type=entry_type_enum,
        )

        return {
            "data": {
                "invalidated_count": invalidated_count,
            }
        }

    except Exception as e:
        logger.error("Error invalidating cache: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to invalidate cache",
        ) from e


@router.post(
    "/dependencies",
    status_code=status.HTTP_201_CREATED,
    summary="Record dependency",
    description="Record a dependency relationship",
)
async def record_dependency(
    resource_id: str,
    source_path: str,
    target_path: str,
    dependency_type: str,
    strength: float = 1.0,
    metadata: Optional[dict[str, Any]] = None,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Record a dependency relationship.

    Args:
        resource_id: Resource ID
        source_path: Source file path
        target_path: Target file path
        dependency_type: Dependency type (direct, transitive, reverse, related)
        strength: Dependency strength (0.0-1.0)
        metadata: Additional metadata
        current_user: Current authenticated user

    Returns:
        Dictionary with dependency entry

    Raises:
        HTTPException: If validation fails
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    if not resource_id or not source_path or not target_path:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="resource_id, source_path, and target_path are required",
        )

    if strength < 0.0 or strength > 1.0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="strength must be between 0.0 and 1.0",
        )

    from api.models.predictive_cache import DependencyType

    try:
        dependency_type_enum = DependencyType(dependency_type)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid dependency_type: {dependency_type}",
        ) from None

    try:
        entry = await predictive_cache_service.record_dependency(
            resource_id=resource_id,
            source_path=source_path,
            target_path=target_path,
            dependency_type=dependency_type_enum,
            strength=strength,
            metadata=metadata,
        )

        return {"data": entry.model_dump()}

    except Exception as e:
        logger.error("Error recording dependency: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to record dependency",
        ) from e

