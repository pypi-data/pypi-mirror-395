"""User profile models for signup and profile management."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


VALID_ROLES = [
    "DevOps Engineer",
    "Platform Engineer",
    "SRE",
    "Developer",
    "Manager",
    "Other",
]

VALID_REFERRAL_SOURCES = [
    "Google Search",
    "Twitter/X",
    "LinkedIn",
    "GitHub",
    "Friend/Colleague",
    "Conference/Event",
    "Blog/Article",
    "Demo Call",
    "Other",
]


class ProfileCompletionRequest(BaseModel):
    """Request model for completing user profile during signup."""

    full_name: str = Field(..., min_length=2, max_length=100, description="User's full name")
    role: str = Field(..., description="User's role/job title")
    organization_name: Optional[str] = Field(
        None, min_length=2, max_length=200, description="Organization/company name"
    )
    referral_source: str = Field(..., description="How user discovered WISTX")

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Validate role is from predefined list."""
        if v not in VALID_ROLES:
            raise ValueError(f"Role must be one of: {', '.join(VALID_ROLES)}")
        return v

    @field_validator("referral_source")
    @classmethod
    def validate_referral_source(cls, v: str) -> str:
        """Validate referral source is from predefined list."""
        if v not in VALID_REFERRAL_SOURCES:
            raise ValueError(f"Referral source must be one of: {', '.join(VALID_REFERRAL_SOURCES)}")
        return v


class ProfileUpdateRequest(BaseModel):
    """Request model for updating user profile."""

    full_name: Optional[str] = Field(None, min_length=2, max_length=100, description="User's full name")
    role: Optional[str] = Field(None, description="User's role/job title")
    organization_name: Optional[str] = Field(
        None, min_length=2, max_length=200, description="Organization/company name"
    )
    referral_source: Optional[str] = Field(None, description="How user discovered WISTX")

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: Optional[str]) -> Optional[str]:
        """Validate role is from predefined list if provided."""
        if v is not None and v not in VALID_ROLES:
            raise ValueError(f"Role must be one of: {', '.join(VALID_ROLES)}")
        return v

    @field_validator("referral_source")
    @classmethod
    def validate_referral_source(cls, v: Optional[str]) -> Optional[str]:
        """Validate referral source is from predefined list if provided."""
        if v is not None and v not in VALID_REFERRAL_SOURCES:
            raise ValueError(f"Referral source must be one of: {', '.join(VALID_REFERRAL_SOURCES)}")
        return v


class UserProfileResponse(BaseModel):
    """Response model for user profile."""

    user_id: str = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    full_name: Optional[str] = Field(None, description="User's full name")
    role: Optional[str] = Field(None, description="User's role/job title")
    organization_name: Optional[str] = Field(None, description="Organization/company name")
    organization_id: Optional[str] = Field(None, description="Organization ID for multi-tenancy")
    organization_role: Optional[str] = Field(None, description="User's role in organization (owner, admin, member)")
    referral_source: Optional[str] = Field(None, description="How user discovered WISTX")
    profile_completed: bool = Field(..., description="Whether profile is complete")
    github_connected: bool = Field(..., description="Whether GitHub repository OAuth is connected")
    plan: str = Field(..., description="User's subscription plan")
    is_verified: bool = Field(..., description="Whether email is verified")
    is_admin: bool = Field(default=False, description="Whether user has admin privileges")
    is_super_admin: bool = Field(default=False, description="Whether user is a super admin")
    admin_role: Optional[str] = Field(None, description="Admin role if user is an admin")
    admin_status: Optional[str] = Field(None, description="Admin status if user is an admin")
    created_at: Optional[datetime] = Field(None, description="Account creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")


class ProfileCompletionStatusResponse(BaseModel):
    """Response model for profile completion status."""

    profile_completed: bool = Field(..., description="Whether profile is complete")
    missing_fields: list[str] = Field(..., description="List of missing required fields")
    completed_fields: list[str] = Field(..., description="List of completed fields")


class ProfileOptionsResponse(BaseModel):
    """Response model for profile form options."""

    roles: list[str] = Field(..., description="Available role options")
    referral_sources: list[str] = Field(..., description="Available referral source options")

