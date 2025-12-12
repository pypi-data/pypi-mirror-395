"""Waitlist models for pre-launch signups."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class WaitlistSignupRequest(BaseModel):
    """Request model for waitlist signup."""

    email: EmailStr = Field(..., description="User email address")
    name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="User's name (optional)"
    )


class WaitlistSignupResponse(BaseModel):
    """Response model for waitlist signup."""

    success: bool = Field(..., description="Whether signup was successful")
    message: str = Field(..., description="Response message")
    position: Optional[int] = Field(
        None, description="Position in waitlist (if available)"
    )


class WaitlistStatusResponse(BaseModel):
    """Response model for waitlist status check."""

    enabled: bool = Field(..., description="Whether waitlist mode is enabled")
    message: Optional[str] = Field(
        None, description="Optional message about waitlist status"
    )

