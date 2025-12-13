"""Waitlist API endpoints."""

import logging
from datetime import datetime
from typing import Any

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_users import FastAPIUsers

from api.config import settings
from api.database.mongodb import mongodb_manager
from api.models.waitlist import (
    WaitlistSignupRequest,
    WaitlistSignupResponse,
    WaitlistStatusResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/waitlist", tags=["waitlist"])


@router.get(
    "/status",
    response_model=WaitlistStatusResponse,
    summary="Get waitlist status",
    description="Check if waitlist mode is enabled",
)
async def get_waitlist_status() -> WaitlistStatusResponse:
    """Get waitlist status.

    Returns:
        Waitlist status information
    """
    logger.info("Waitlist status check: enabled=%s", settings.enable_waitlist)
    return WaitlistStatusResponse(
        enabled=settings.enable_waitlist,
        message="Waitlist mode is enabled" if settings.enable_waitlist else None,
    )


@router.post(
    "/signup",
    response_model=WaitlistSignupResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Join waitlist",
    description="Sign up for the waitlist",
)
async def join_waitlist(
    request: WaitlistSignupRequest,
) -> WaitlistSignupResponse:
    """Join the waitlist.

    Args:
        request: Waitlist signup request

    Returns:
        Waitlist signup response

    Raises:
        HTTPException: If signup fails
    """
    try:
        db = mongodb_manager.get_database()
        waitlist_collection = db.waitlist

        existing_entry = waitlist_collection.find_one({"email": request.email.lower()})

        if existing_entry:
            logger.info("Waitlist signup attempt for existing email: %s", request.email)
            return WaitlistSignupResponse(
                success=True,
                message="You're already on the waitlist! We'll notify you when access is available.",
            )

        total_count = waitlist_collection.count_documents({})
        position = total_count + 1

        waitlist_entry = {
            "email": request.email.lower(),
            "name": request.name,
            "created_at": datetime.utcnow(),
            "status": "pending",
        }

        waitlist_collection.insert_one(waitlist_entry)

        logger.info(
            "New waitlist signup: %s (position: %d)", request.email, position
        )

        try:
            from api.services.email import email_service
            from api.config import settings

            user_name = request.name or request.email.split("@")[0] or "there"

            email_response = await email_service.send_template(
                template_name="waitlist_confirmation",
                to=request.email,
                subject="You're on the WISTX Waitlist! 🎉",
                context={
                    "user_name": user_name,
                    "position": str(position),
                    "current_year": str(datetime.utcnow().year),
                },
                tags=["waitlist", "confirmation"],
            )

            if email_response.success:
                logger.info(
                    "Waitlist confirmation email sent to %s (provider: %s, message_id: %s)",
                    request.email,
                    email_response.provider.value,
                    email_response.message_id or "unknown",
                )
            else:
                logger.warning(
                    "Failed to send waitlist confirmation email to %s: %s (provider: %s)",
                    request.email,
                    email_response.error,
                    email_response.provider.value if email_response.provider else "unknown",
                )
        except Exception as e:
            logger.error(
                "Exception sending waitlist confirmation email to %s: %s",
                request.email,
                e,
                exc_info=True,
            )

        return WaitlistSignupResponse(
            success=True,
            message="Successfully joined the waitlist! We'll notify you when access is available.",
            position=position,
        )

    except Exception as e:
        logger.error("Error joining waitlist: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to join waitlist. Please try again later.",
        ) from e

