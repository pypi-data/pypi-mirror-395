"""Admin RBAC models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


ADMIN_PERMISSIONS = {
    "users.read": "View users",
    "users.write": "Edit users",
    "users.delete": "Delete users",
    "users.suspend": "Suspend/activate users",
    "activity.read": "View activity feed",
    "security.view": "View security events",
    "security.audit": "View audit logs",
    "security.api_keys": "Manage API keys",
    "analytics.view": "View analytics",
    "system.view": "View system health",
    "system.manage": "Manage system settings",
    "admin.invite": "Invite admins",
    "admin.manage": "Manage admin roles/permissions",
    "admin.delete": "Remove admins",
}

ADMIN_ROLES = {
    "super_admin": ["*"],
    "admin": [
        "users.read",
        "users.write",
        "users.suspend",
        "activity.read",
        "security.view",
        "security.audit",
        "security.api_keys",
        "analytics.view",
        "system.view",
    ],
    "support": [
        "users.read",
        "activity.read",
        "security.view",
        "analytics.view",
    ],
}

VALID_ADMIN_ROLES = list(ADMIN_ROLES.keys())
VALID_PERMISSIONS = list(ADMIN_PERMISSIONS.keys())


class AdminInvitationCreateRequest(BaseModel):
    """Request model for creating admin invitation."""

    email: str = Field(..., description="Email to invite")
    role: str = Field(..., description="Admin role")
    permissions: Optional[list[str]] = Field(None, description="Custom permissions (optional)")
    expires_in_days: int = Field(default=7, ge=1, le=30, description="Invitation expiration in days")

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        if v not in VALID_ADMIN_ROLES:
            raise ValueError(f"Invalid role. Must be one of: {', '.join(VALID_ADMIN_ROLES)}")
        return v

    @field_validator("permissions")
    @classmethod
    def validate_permissions(cls, v: Optional[list[str]]) -> Optional[list[str]]:
        if v is None:
            return v
        invalid_perms = [p for p in v if p not in VALID_PERMISSIONS and p != "*"]
        if invalid_perms:
            raise ValueError(f"Invalid permissions: {', '.join(invalid_perms)}")
        return v


class AdminInvitationResponse(BaseModel):
    """Response model for admin invitation."""

    invitation_id: str = Field(..., description="Invitation ID")
    email: str = Field(..., description="Email invited")
    role: str = Field(..., description="Admin role")
    permissions: list[str] = Field(default_factory=list, description="Custom permissions")
    token: str = Field(..., description="Invitation token")
    expires_at: datetime = Field(..., description="Invitation expiration")
    status: str = Field(..., description="Invitation status")
    invited_by: str = Field(..., description="Admin user ID who created invitation")
    invited_by_email: Optional[str] = Field(None, description="Admin email who created invitation")
    accepted_at: Optional[datetime] = Field(None, description="When invitation was accepted")
    accepted_by: Optional[str] = Field(None, description="User ID who accepted")
    created_at: datetime = Field(..., description="Invitation creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class AdminInvitationListResponse(BaseModel):
    """Response model for admin invitation list."""

    invitations: list[AdminInvitationResponse] = Field(..., description="List of invitations")
    total: int = Field(..., description="Total number of invitations")
    limit: int = Field(..., description="Limit used")
    offset: int = Field(..., description="Offset used")


class AdminInvitationAcceptRequest(BaseModel):
    """Request model for accepting admin invitation."""

    token: str = Field(..., description="Invitation token")


class AdminRoleUpdateRequest(BaseModel):
    """Request model for updating admin role."""

    role: str = Field(..., description="New admin role")

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        if v not in VALID_ADMIN_ROLES:
            raise ValueError(f"Invalid role. Must be one of: {', '.join(VALID_ADMIN_ROLES)}")
        return v


class AdminPermissionsUpdateRequest(BaseModel):
    """Request model for updating admin permissions."""

    permissions: list[str] = Field(..., description="List of permissions")

    @field_validator("permissions")
    @classmethod
    def validate_permissions(cls, v: list[str]) -> list[str]:
        invalid_perms = [p for p in v if p not in VALID_PERMISSIONS and p != "*"]
        if invalid_perms:
            raise ValueError(f"Invalid permissions: {', '.join(invalid_perms)}")
        return v


class AdminInfoResponse(BaseModel):
    """Response model for admin information."""

    user_id: str = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    full_name: Optional[str] = Field(None, description="User's full name")
    admin_role: Optional[str] = Field(None, description="Admin role")
    admin_permissions: list[str] = Field(default_factory=list, description="Admin permissions")
    is_super_admin: bool = Field(default=False, description="Is super admin")
    admin_status: Optional[str] = Field(None, description="Admin status")
    admin_invited_by: Optional[str] = Field(None, description="Admin who invited")
    admin_invited_at: Optional[datetime] = Field(None, description="When invitation was accepted")
    created_at: Optional[datetime] = Field(None, description="Account creation timestamp")


class AdminListResponse(BaseModel):
    """Response model for admin list."""

    admins: list[AdminInfoResponse] = Field(..., description="List of admins")
    total: int = Field(..., description="Total number of admins")
    limit: int = Field(..., description="Limit used")
    offset: int = Field(..., description="Offset used")

