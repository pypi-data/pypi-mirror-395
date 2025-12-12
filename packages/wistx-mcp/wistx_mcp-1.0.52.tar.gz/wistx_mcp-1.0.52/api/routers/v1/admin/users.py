"""Admin user management endpoints."""

import logging
from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.dependencies.auth import require_admin
from api.models.admin.user_management import (
    AdminUserResponse,
    CreateUserWithInvitationRequest,
    CreateUserWithInvitationResponse,
    UserListQuery,
    UserListResponse,
    UserStatsResponse,
    UserSuspendRequest,
    UserUpdateRequest,
)
from api.services.admin.user_service import admin_user_service
from api.services.user_invitation_service import user_invitation_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["admin"])


@router.get("/", response_model=UserListResponse, summary="List users")
async def list_users(
    search: str | None = Query(None, description="Search by email, name, or user ID"),
    plan: str | None = Query(None, description="Filter by plan"),
    is_active: bool | None = Query(None, description="Filter by active status"),
    is_verified: bool | None = Query(None, description="Filter by verified status"),
    profile_completed: bool | None = Query(None, description="Filter by profile completion"),
    organization_id: str | None = Query(None, description="Filter by organization ID"),
    start_date: datetime | None = Query(None, description="Filter by creation date (start)"),
    end_date: datetime | None = Query(None, description="Filter by creation date (end)"),
    limit: int = Query(default=50, ge=1, le=100, description="Maximum number of results"),
    offset: int = Query(default=0, ge=0, description="Offset for pagination"),
    sort_by: str = Query(default="created_at", description="Field to sort by"),
    sort_order: str = Query(default="desc", description="Sort order (asc or desc)"),
    current_user: dict[str, Any] = Depends(require_admin),
) -> UserListResponse:
    """List users with filters and pagination.

    Args:
        search: Search term
        plan: Plan filter
        is_active: Active status filter
        is_verified: Verified status filter
        profile_completed: Profile completion filter
        organization_id: Organization ID filter
        start_date: Start date filter
        end_date: End date filter
        limit: Result limit
        offset: Result offset
        sort_by: Sort field
        sort_order: Sort order
        current_user: Current admin user

    Returns:
        User list response
    """
    query = UserListQuery(
        search=search,
        plan=plan,
        is_active=is_active,
        is_verified=is_verified,
        profile_completed=profile_completed,
        organization_id=organization_id,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    try:
        return await admin_user_service.list_users(query)
    except Exception as e:
        logger.error("Error listing users: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list users",
        ) from e


@router.get("/{user_id}", response_model=AdminUserResponse, summary="Get user details")
async def get_user(
    user_id: str,
    current_user: dict[str, Any] = Depends(require_admin),
) -> AdminUserResponse:
    """Get user details.

    Args:
        user_id: User ID
        current_user: Current admin user

    Returns:
        Admin user response

    Raises:
        HTTPException: If user not found
    """
    try:
        return await admin_user_service.get_user(user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error getting user: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user",
        ) from e


@router.patch("/{user_id}", response_model=AdminUserResponse, summary="Update user")
async def update_user(
    user_id: str,
    updates: UserUpdateRequest,
    current_user: dict[str, Any] = Depends(require_admin),
) -> AdminUserResponse:
    """Update user.

    Args:
        user_id: User ID
        updates: Update data
        current_user: Current admin user

    Returns:
        Updated admin user response

    Raises:
        HTTPException: If user not found
    """
    try:
        return await admin_user_service.update_user(user_id, updates, current_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error updating user: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user",
        ) from e


@router.post("/{user_id}/suspend", response_model=AdminUserResponse, summary="Suspend user")
async def suspend_user(
    user_id: str,
    request: UserSuspendRequest,
    current_user: dict[str, Any] = Depends(require_admin),
) -> AdminUserResponse:
    """Suspend user.

    Args:
        user_id: User ID
        request: Suspend request
        current_user: Current admin user

    Returns:
        Updated admin user response

    Raises:
        HTTPException: If user not found
    """
    try:
        return await admin_user_service.suspend_user(user_id, request, current_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error suspending user: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to suspend user",
        ) from e


@router.post("/{user_id}/activate", response_model=AdminUserResponse, summary="Activate user")
async def activate_user(
    user_id: str,
    current_user: dict[str, Any] = Depends(require_admin),
) -> AdminUserResponse:
    """Activate suspended user.

    Args:
        user_id: User ID
        current_user: Current admin user

    Returns:
        Updated admin user response

    Raises:
        HTTPException: If user not found
    """
    try:
        return await admin_user_service.activate_user(user_id, current_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error activating user: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to activate user",
        ) from e


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete user")
async def delete_user(
    user_id: str,
    current_user: dict[str, Any] = Depends(require_admin),
) -> None:
    """Delete user permanently.

    Args:
        user_id: User ID
        current_user: Current admin user

    Raises:
        HTTPException: If user not found
    """
    try:
        await admin_user_service.delete_user(user_id, current_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error deleting user: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user",
        ) from e


@router.get("/{user_id}/stats", response_model=UserStatsResponse, summary="Get user statistics")
async def get_user_stats(
    user_id: str,
    current_user: dict[str, Any] = Depends(require_admin),
) -> UserStatsResponse:
    """Get user statistics.

    Args:
        user_id: User ID
        current_user: Current admin user

    Returns:
        User statistics response

    Raises:
        HTTPException: If user not found
    """
    try:
        return await admin_user_service.get_user_stats(user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error getting user stats: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user stats",
        ) from e


@router.post("/create", response_model=CreateUserWithInvitationResponse, status_code=status.HTTP_201_CREATED, summary="Create user with invitation")
async def create_user_with_invitation(
    request: CreateUserWithInvitationRequest,
    current_user: dict[str, Any] = Depends(require_admin),
) -> CreateUserWithInvitationResponse:
    """Create user account with invitation (B2B post-demo).

    Args:
        request: User creation request
        current_user: Current admin user

    Returns:
        Created user and invitation details

    Raises:
        HTTPException: If user creation fails
    """
    try:
        result = await user_invitation_service.create_user_with_invitation(
            email=request.email,
            plan=request.plan,
            created_by=current_user.get("user_id"),
            full_name=request.full_name,
            organization_name=request.organization_name,
            send_invitation=request.send_invitation,
        )
        return CreateUserWithInvitationResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error creating user with invitation: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user with invitation",
        ) from e


@router.post("/{user_id}/resend-invitation", response_model=CreateUserWithInvitationResponse, summary="Resend invitation")
async def resend_invitation(
    user_id: str,
    current_user: dict[str, Any] = Depends(require_admin),
) -> CreateUserWithInvitationResponse:
    """Resend invitation email to user.

    Args:
        user_id: User ID
        current_user: Current admin user

    Returns:
        Invitation details

    Raises:
        HTTPException: If user not found or invitation already accepted
    """
    try:
        result = await user_invitation_service.resend_invitation(user_id)
        from api.database.mongodb import mongodb_manager
        from bson import ObjectId
        db = mongodb_manager.get_database()
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise ValueError("User not found")
        return CreateUserWithInvitationResponse(
            user_id=user_id,
            email=user.get("email", ""),
            plan=user.get("plan", "professional"),
            invitation_token=result["invitation_token"],
            invitation_url=result["invitation_url"],
            expires_at=result["expires_at"],
            invitation_sent=True,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error resending invitation: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to resend invitation",
        ) from e

