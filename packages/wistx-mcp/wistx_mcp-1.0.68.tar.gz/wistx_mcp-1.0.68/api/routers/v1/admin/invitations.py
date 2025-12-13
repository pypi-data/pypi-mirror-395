"""Admin invitation endpoints."""

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.dependencies.auth import get_current_user, require_admin, require_permission, require_super_admin
from api.models.admin.rbac import (
    AdminInvitationAcceptRequest,
    AdminInvitationCreateRequest,
    AdminInvitationListResponse,
    AdminInvitationResponse,
)
from api.services.admin.invitation_service import admin_invitation_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/invitations", tags=["admin"])


@router.post("/", response_model=AdminInvitationResponse, status_code=status.HTTP_201_CREATED, summary="Create admin invitation")
async def create_invitation(
    request: AdminInvitationCreateRequest,
    current_user: dict[str, Any] = Depends(require_super_admin),
) -> AdminInvitationResponse:
    """Create admin invitation (super admin only).

    Args:
        request: Invitation creation request
        current_user: Current super admin user

    Returns:
        Created invitation response

    Raises:
        HTTPException: If invitation creation fails
    """
    try:
        return await admin_invitation_service.create_invitation(
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
        logger.error("Error creating invitation: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create invitation",
        ) from e


@router.get("/", response_model=AdminInvitationListResponse, summary="List admin invitations")
async def list_invitations(
    limit: int = Query(default=50, ge=1, le=100, description="Maximum number of results"),
    offset: int = Query(default=0, ge=0, description="Offset for pagination"),
    status_filter: str | None = Query(None, alias="status", description="Filter by status"),
    current_user: dict[str, Any] = Depends(require_admin),
) -> AdminInvitationListResponse:
    """List admin invitations.

    Args:
        limit: Result limit
        offset: Result offset
        status_filter: Status filter
        current_user: Current admin user

    Returns:
        Invitation list response
    """
    try:
        return await admin_invitation_service.list_invitations(limit, offset, status_filter)
    except Exception as e:
        logger.error("Error listing invitations: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list invitations",
        ) from e


@router.get("/{invitation_id}", response_model=AdminInvitationResponse, summary="Get invitation")
async def get_invitation(
    invitation_id: str,
    current_user: dict[str, Any] = Depends(require_admin),
) -> AdminInvitationResponse:
    """Get invitation by ID.

    Args:
        invitation_id: Invitation ID
        current_user: Current admin user

    Returns:
        Invitation response

    Raises:
        HTTPException: If invitation not found
    """
    try:
        return await admin_invitation_service.get_invitation(invitation_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error getting invitation: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get invitation",
        ) from e


@router.post("/accept", response_model=AdminInvitationResponse, summary="Accept invitation")
async def accept_invitation(
    request: AdminInvitationAcceptRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> AdminInvitationResponse:
    """Accept admin invitation.

    Args:
        request: Invitation acceptance request with token
        current_user: Current authenticated user

    Returns:
        Updated invitation response

    Raises:
        HTTPException: If invitation acceptance fails
    """
    from api.dependencies.auth import get_current_user

    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )

    try:
        return await admin_invitation_service.accept_invitation(request.token, user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error accepting invitation: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to accept invitation",
        ) from e


@router.delete("/{invitation_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Revoke invitation")
async def revoke_invitation(
    invitation_id: str,
    current_user: dict[str, Any] = Depends(require_super_admin),
) -> None:
    """Revoke admin invitation (super admin only).

    Args:
        invitation_id: Invitation ID
        current_user: Current super admin user

    Raises:
        HTTPException: If revocation fails
    """
    try:
        await admin_invitation_service.revoke_invitation(
            invitation_id,
            current_user.get("user_id"),
            current_user.get("email", ""),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error revoking invitation: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to revoke invitation",
        ) from e

