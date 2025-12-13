"""User profile management endpoints."""

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import get_current_user
from api.models.user_profile import (
    ProfileCompletionRequest,
    ProfileCompletionStatusResponse,
    ProfileOptionsResponse,
    ProfileUpdateRequest,
    UserProfileResponse,
    VALID_REFERRAL_SOURCES,
    VALID_ROLES,
)
from api.services.user_profile_service import user_profile_service
from api.services.user_invitation_service import user_invitation_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/profile/complete",
    response_model=UserProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Complete user profile",
    description="Complete user profile during signup. This endpoint is called after OAuth authentication.",
)
async def complete_profile(
    request: ProfileCompletionRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> UserProfileResponse:
    """Complete user profile during signup.

    Args:
        request: Profile completion data
        current_user: Current authenticated user

    Returns:
        Updated user profile

    Raises:
        HTTPException: If profile already completed or validation fails
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )

    try:
        profile = await user_profile_service.complete_profile(str(user_id), request)
        logger.info("Profile completed for user: %s", user_id)
        return profile
    except ValueError as e:
        error_msg = str(e)
        if "already completed" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=error_msg,
            ) from e
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_msg,
        ) from e
    except Exception as e:
        logger.error("Error completing profile: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to complete profile",
        ) from e


@router.get(
    "/me",
    response_model=UserProfileResponse,
    summary="Get current user profile",
    description="Get the current authenticated user's profile information.",
)
async def get_current_user_profile(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> UserProfileResponse:
    """Get current user profile.

    Args:
        current_user: Current authenticated user

    Returns:
        User profile

    Raises:
        HTTPException: If user not found
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )

    try:
        profile = await user_profile_service.get_profile(str(user_id))
        return profile
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error getting profile: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve profile",
        ) from e


@router.patch(
    "/me",
    response_model=UserProfileResponse,
    summary="Update user profile",
    description="Update the current authenticated user's profile information.",
)
async def update_user_profile(
    request: ProfileUpdateRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> UserProfileResponse:
    """Update user profile.

    Args:
        request: Profile update data (partial update)
        current_user: Current authenticated user

    Returns:
        Updated user profile

    Raises:
        HTTPException: If user not found or validation fails
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )

    try:
        profile = await user_profile_service.update_profile(str(user_id), request)
        logger.info("Profile updated for user: %s", user_id)
        return profile
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error updating profile: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile",
        ) from e


@router.get(
    "/profile/status",
    response_model=ProfileCompletionStatusResponse,
    summary="Check profile completion status",
    description="Check if the current user's profile is complete and which fields are missing.",
)
async def get_profile_completion_status(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> ProfileCompletionStatusResponse:
    """Check profile completion status.

    Args:
        current_user: Current authenticated user

    Returns:
        Profile completion status

    Raises:
        HTTPException: If user not found
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )

    try:
        status_response = await user_profile_service.check_completion_status(str(user_id))
        return status_response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error checking profile status: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to check profile status",
        ) from e


@router.get(
    "/profile/options",
    response_model=ProfileOptionsResponse,
    summary="Get profile form options",
    description="Get available options for role and referral source dropdowns.",
)
async def get_profile_options() -> ProfileOptionsResponse:
    """Get profile form options.

    Returns:
        Available options for profile form
    """
    return ProfileOptionsResponse(
        roles=VALID_ROLES,
        referral_sources=VALID_REFERRAL_SOURCES,
    )


@router.get(
    "/signup/next-step",
    summary="Get next step in signup flow",
    description="Get the next step the user should complete in the signup flow. "
    "Returns guidance on whether profile completion or GitHub connection is needed.",
)
async def get_signup_next_step(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Get next step in signup flow.

    Args:
        current_user: Current authenticated user

    Returns:
        Next step guidance with redirect information
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )

    try:
        from api.database.mongodb import mongodb_manager
        from api.services.oauth_service import oauth_service
        from bson import ObjectId

        status_response = await user_profile_service.check_completion_status(str(user_id))
        has_github = await oauth_service.has_github_token(str(user_id))

        def find_user_sync():
            db = mongodb_manager.get_database()
            return db.users.find_one({"_id": ObjectId(user_id)})
        
        loop = asyncio.get_event_loop()
        try:
            user_doc = await asyncio.wait_for(
                loop.run_in_executor(ThreadPoolExecutor(max_workers=1), find_user_sync),
                timeout=3.0
            )
        except asyncio.TimeoutError:
            logger.error("get_signup_next_step: MongoDB query timed out for user: %s", user_id)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database query timeout",
            )
        
        if not user_doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        onboarding_completed = user_doc.get("onboarding_completed", False)
        profile_completed = user_doc.get("profile_completed", False)

        if profile_completed and not onboarding_completed:
            from datetime import datetime
            
            def update_user_sync():
                db = mongodb_manager.get_database()
                db.users.update_one(
                    {"_id": ObjectId(user_id)},
                    {"$set": {"onboarding_completed": True, "updated_at": datetime.utcnow()}},
                )
            
            try:
                await asyncio.wait_for(
                    loop.run_in_executor(ThreadPoolExecutor(max_workers=1), update_user_sync),
                    timeout=3.0
                )
            except asyncio.TimeoutError:
                logger.warning("get_signup_next_step: Failed to update onboarding_completed flag (timeout)")
            
            onboarding_completed = True

        if not status_response.profile_completed:
            return {
                "next_step": "profile",
                "message": "Please complete your profile to continue",
                "required": True,
                "endpoint": "/v1/users/profile/complete",
                "status_endpoint": "/v1/users/profile/status",
            }

        if onboarding_completed:
            return {
                "next_step": "complete",
                "message": "Welcome back to WISTX",
                "required": False,
                "redirect": "/dashboard",
            }

        if profile_completed and not has_github and not onboarding_completed:
            return {
                "next_step": "github",
                "message": "Connect GitHub to enable repository indexing (optional)",
                "required": False,
                "endpoint": "/v1/oauth/github/authorize",
                "status_endpoint": "/v1/oauth/github/status",
            }

        return {
            "next_step": "complete",
            "message": "Signup complete! Welcome to WISTX",
            "required": False,
            "redirect": "/dashboard",
        }
    except Exception as e:
        logger.error("Error getting signup next step: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get signup next step",
        ) from e


@router.get("/invitation/validate", summary="Validate invitation token")
async def validate_invitation_token(
    token: str,
) -> dict[str, Any]:
    """Validate invitation token and return associated email.

    Args:
        token: Invitation token

    Returns:
        Email and plan associated with the invitation

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        user_doc = await user_invitation_service.validate_invitation_token(token)
        return {
            "email": user_doc.get("email"),
            "plan": user_doc.get("plan", "professional"),
            "full_name": user_doc.get("full_name"),
            "organization_name": user_doc.get("organization_name"),
            "expires_at": user_doc.get("invitation_expires_at").isoformat() if user_doc.get("invitation_expires_at") else None,
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error validating invitation token: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to validate invitation token",
        ) from e

