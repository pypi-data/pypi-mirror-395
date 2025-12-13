"""Admin management endpoints."""

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.dependencies.auth import require_admin, require_super_admin
from api.models.admin.rbac import (
    AdminInfoResponse,
    AdminListResponse,
    AdminPermissionsUpdateRequest,
    AdminRoleUpdateRequest,
)
from api.services.admin.admin_management_service import admin_management_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admins", tags=["admin"])


@router.get("/", response_model=AdminListResponse, summary="List all admins")
async def list_admins(
    limit: int = Query(default=50, ge=1, le=100, description="Maximum number of results"),
    offset: int = Query(default=0, ge=0, description="Offset for pagination"),
    role: str | None = Query(None, description="Filter by role"),
    status_filter: str | None = Query(None, alias="status", description="Filter by status"),
    show_internal_only: bool = Query(False, description="Show only @wistx.ai users"),
    current_user: dict[str, Any] = Depends(require_admin),
) -> AdminListResponse:
    """List all admins.

    Args:
        limit: Result limit
        offset: Result offset
        role: Role filter
        status_filter: Status filter
        show_internal_only: Show only @wistx.ai users
        current_user: Current admin user

    Returns:
        Admin list response
    """
    try:
        return await admin_management_service.list_admins(limit, offset, role, status_filter, show_internal_only)
    except Exception as e:
        logger.error("Error listing admins: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list admins",
        ) from e


@router.get("/{user_id}", response_model=AdminInfoResponse, summary="Get admin details")
async def get_admin(
    user_id: str,
    current_user: dict[str, Any] = Depends(require_admin),
) -> AdminInfoResponse:
    """Get admin details.

    Args:
        user_id: User ID
        current_user: Current admin user

    Returns:
        Admin info response

    Raises:
        HTTPException: If admin not found
    """
    try:
        return await admin_management_service.get_admin(user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error getting admin: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get admin",
        ) from e


@router.patch("/{user_id}/role", response_model=AdminInfoResponse, summary="Update admin role")
async def update_admin_role(
    user_id: str,
    request: AdminRoleUpdateRequest,
    current_user: dict[str, Any] = Depends(require_super_admin),
) -> AdminInfoResponse:
    """Update admin role (super admin only).

    Args:
        user_id: User ID
        request: Role update request
        current_user: Current super admin user

    Returns:
        Updated admin info response

    Raises:
        HTTPException: If update fails
    """
    try:
        return await admin_management_service.update_admin_role(
            user_id,
            request,
            current_user.get("user_id"),
            current_user.get("email", ""),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error updating admin role: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update admin role",
        ) from e


@router.patch("/{user_id}/permissions", response_model=AdminInfoResponse, summary="Update admin permissions")
async def update_admin_permissions(
    user_id: str,
    request: AdminPermissionsUpdateRequest,
    current_user: dict[str, Any] = Depends(require_super_admin),
) -> AdminInfoResponse:
    """Update admin permissions (super admin only).

    Args:
        user_id: User ID
        request: Permissions update request
        current_user: Current super admin user

    Returns:
        Updated admin info response

    Raises:
        HTTPException: If update fails
    """
    try:
        return await admin_management_service.update_admin_permissions(
            user_id,
            request,
            current_user.get("user_id"),
            current_user.get("email", ""),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error updating admin permissions: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update admin permissions",
        ) from e


@router.post("/{user_id}/suspend", response_model=AdminInfoResponse, summary="Suspend admin")
async def suspend_admin(
    user_id: str,
    current_user: dict[str, Any] = Depends(require_super_admin),
) -> AdminInfoResponse:
    """Suspend admin (super admin only).

    Args:
        user_id: User ID
        current_user: Current super admin user

    Returns:
        Updated admin info response

    Raises:
        HTTPException: If suspension fails
    """
    try:
        return await admin_management_service.suspend_admin(
            user_id,
            current_user.get("user_id"),
            current_user.get("email", ""),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error suspending admin: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to suspend admin",
        ) from e


@router.post("/{user_id}/activate", response_model=AdminInfoResponse, summary="Activate admin")
async def activate_admin(
    user_id: str,
    current_user: dict[str, Any] = Depends(require_super_admin),
) -> AdminInfoResponse:
    """Activate suspended admin (super admin only).

    Args:
        user_id: User ID
        current_user: Current super admin user

    Returns:
        Updated admin info response

    Raises:
        HTTPException: If activation fails
    """
    try:
        return await admin_management_service.activate_admin(
            user_id,
            current_user.get("user_id"),
            current_user.get("email", ""),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error activating admin: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to activate admin",
        ) from e


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remove admin")
async def remove_admin(
    user_id: str,
    current_user: dict[str, Any] = Depends(require_super_admin),
) -> None:
    """Remove admin (super admin only).

    Args:
        user_id: User ID
        current_user: Current super admin user

    Raises:
        HTTPException: If removal fails
    """
    try:
        await admin_management_service.remove_admin(
            user_id,
            current_user.get("user_id"),
            current_user.get("email", ""),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error removing admin: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove admin",
        ) from e

