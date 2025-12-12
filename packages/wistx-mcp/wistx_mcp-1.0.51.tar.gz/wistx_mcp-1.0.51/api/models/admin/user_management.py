"""Admin user management models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserListQuery(BaseModel):
    """Query parameters for listing users."""

    search: Optional[str] = Field(None, description="Search by email, name, or user ID")
    plan: Optional[str] = Field(None, description="Filter by plan")
    is_active: Optional[bool] = Field(None, description="Filter by active status")
    is_verified: Optional[bool] = Field(None, description="Filter by verified status")
    profile_completed: Optional[bool] = Field(None, description="Filter by profile completion")
    organization_id: Optional[str] = Field(None, description="Filter by organization ID")
    start_date: Optional[datetime] = Field(None, description="Filter by creation date (start)")
    end_date: Optional[datetime] = Field(None, description="Filter by creation date (end)")
    limit: int = Field(default=50, ge=1, le=100, description="Maximum number of results")
    offset: int = Field(default=0, ge=0, description="Offset for pagination")
    sort_by: str = Field(default="created_at", description="Field to sort by")
    sort_order: str = Field(default="desc", description="Sort order (asc or desc)")


class UserUpdateRequest(BaseModel):
    """Request model for updating user."""

    plan: Optional[str] = Field(None, description="User plan")
    is_active: Optional[bool] = Field(None, description="User active status")
    is_verified: Optional[bool] = Field(None, description="User verified status")
    full_name: Optional[str] = Field(None, min_length=2, max_length=100, description="User's full name")
    role: Optional[str] = Field(None, description="User's role")
    organization_name: Optional[str] = Field(None, min_length=2, max_length=200, description="Organization name")
    organization_id: Optional[str] = Field(None, description="Organization ID")


class AdminUserResponse(BaseModel):
    """Admin user response model."""

    user_id: str = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    full_name: Optional[str] = Field(None, description="User's full name")
    role: Optional[str] = Field(None, description="User's role")
    organization_name: Optional[str] = Field(None, description="Organization name")
    organization_id: Optional[str] = Field(None, description="Organization ID")
    plan: str = Field(..., description="User plan")
    is_active: bool = Field(..., description="User active status")
    is_verified: bool = Field(..., description="User verified status")
    is_admin: bool = Field(..., description="User admin status")
    profile_completed: bool = Field(..., description="Profile completion status")
    github_connected: bool = Field(..., description="GitHub connection status")
    created_at: Optional[datetime] = Field(None, description="Account creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    last_active_at: Optional[datetime] = Field(None, description="Last active timestamp")


class UserListResponse(BaseModel):
    """User list response model."""

    users: list[AdminUserResponse] = Field(..., description="List of users")
    total: int = Field(..., description="Total number of users matching filters")
    limit: int = Field(..., description="Limit used")
    offset: int = Field(..., description="Offset used")


class UserSuspendRequest(BaseModel):
    """Request model for suspending user."""

    reason: Optional[str] = Field(None, max_length=500, description="Suspension reason")


class UserStatsResponse(BaseModel):
    """User statistics response model."""

    user_id: str = Field(..., description="User ID")
    total_api_requests: int = Field(default=0, description="Total API requests")
    total_queries: int = Field(default=0, description="Total queries")
    total_indexing_operations: int = Field(default=0, description="Total indexing operations")
    storage_mb: float = Field(default=0.0, description="Storage used in MB")
    api_keys_count: int = Field(default=0, description="Number of API keys")
    active_api_keys_count: int = Field(default=0, description="Number of active API keys")


class CreateUserWithInvitationRequest(BaseModel):
    """Request model for creating user with invitation (B2B)."""

    email: str = Field(..., description="User email address")
    plan: str = Field(..., description="Plan ID (professional, team, enterprise)")
    full_name: Optional[str] = Field(None, min_length=2, max_length=100, description="User's full name (pre-fills onboarding)")
    organization_name: Optional[str] = Field(None, min_length=2, max_length=200, description="Organization name (pre-fills onboarding)")
    send_invitation: bool = Field(default=True, description="Whether to send invitation email immediately")


class CreateUserWithInvitationResponse(BaseModel):
    """Response model for creating user with invitation."""

    user_id: str = Field(..., description="Created user ID")
    email: str = Field(..., description="User email")
    plan: str = Field(..., description="Assigned plan")
    invitation_token: str = Field(..., description="Invitation token")
    invitation_url: str = Field(..., description="Invitation URL")
    expires_at: str = Field(..., description="Invitation expiration date (ISO format)")
    invitation_sent: bool = Field(..., description="Whether invitation email was sent")

