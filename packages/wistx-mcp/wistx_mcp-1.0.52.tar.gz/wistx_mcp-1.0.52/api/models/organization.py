"""Organization models for team management."""

from datetime import datetime
from typing import Any, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class Organization(BaseModel):
    """Organization model."""

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., alias="_id", description="Organization ID")
    name: str = Field(..., min_length=1, max_length=100, description="Organization name")
    slug: str = Field(..., description="Organization slug (unique)")
    plan_id: str = Field(..., description="Plan ID (team or enterprise)")
    stripe_customer_id: Optional[str] = Field(default=None, description="Stripe customer ID")
    stripe_subscription_id: Optional[str] = Field(default=None, description="Stripe subscription ID")
    subscription_status: str = Field(
        default="inactive",
        description="Subscription status (active, canceled, past_due, inactive)",
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    created_by: str = Field(..., description="User ID who created organization")
    status: str = Field(default="active", description="Organization status (active, suspended, canceled)")
    deleted_at: Optional[datetime] = Field(default=None, description="Soft delete timestamp")
    version: int = Field(default=1, description="Version for optimistic locking")
    settings: dict[str, Any] = Field(
        default_factory=lambda: {
            "allowed_domains": [],
            "require_domain_match": False,
            "billing_email": None,
            "notification_preferences": {},
        },
        description="Organization settings",
    )
    metadata: dict[str, Any] = Field(default_factory=dict, description="Custom metadata fields")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for MongoDB storage.

        Returns:
            Dictionary representation
        """
        data = self.model_dump(exclude={"id"}, by_alias=True)
        data["_id"] = ObjectId(self.id)
        data["created_by"] = ObjectId(self.created_by) if self.created_by else None
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Organization":
        """Create from MongoDB document.

        Args:
            data: MongoDB document

        Returns:
            Organization instance
        """
        data_copy = data.copy()
        if "_id" in data_copy:
            data_copy["id"] = str(data_copy["_id"])
            del data_copy["_id"]
        if "created_by" in data_copy and isinstance(data_copy["created_by"], ObjectId):
            data_copy["created_by"] = str(data_copy["created_by"])
        if "settings" not in data_copy:
            data_copy["settings"] = {
                "allowed_domains": [],
                "require_domain_match": False,
                "billing_email": None,
                "notification_preferences": {},
            }
        return cls(**data_copy)


class OrganizationMember(BaseModel):
    """Organization member model."""

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., alias="_id", description="Member ID")
    organization_id: str = Field(..., description="Organization ID")
    user_id: str = Field(..., description="User ID")
    role: str = Field(..., description="Member role (owner, admin, member, viewer)")
    invited_by: str = Field(..., description="User ID who invited this member")
    joined_at: datetime = Field(default_factory=datetime.utcnow, description="Join timestamp")
    status: str = Field(default="active", description="Member status (active, pending, removed)")
    permissions: list[str] = Field(default_factory=list, description="Granular permissions")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for MongoDB storage.

        Returns:
            Dictionary representation
        """
        data = self.model_dump(exclude={"id"}, by_alias=True)
        data["_id"] = ObjectId(self.id)
        data["organization_id"] = ObjectId(self.organization_id) if self.organization_id else None
        data["user_id"] = ObjectId(self.user_id) if self.user_id else None
        data["invited_by"] = ObjectId(self.invited_by) if self.invited_by else None
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "OrganizationMember":
        """Create from MongoDB document.

        Args:
            data: MongoDB document

        Returns:
            OrganizationMember instance
        """
        data_copy = data.copy()
        if "_id" in data_copy:
            data_copy["id"] = str(data_copy["_id"])
            del data_copy["_id"]
        if "organization_id" in data_copy and isinstance(data_copy["organization_id"], ObjectId):
            data_copy["organization_id"] = str(data_copy["organization_id"])
        if "user_id" in data_copy and isinstance(data_copy["user_id"], ObjectId):
            data_copy["user_id"] = str(data_copy["user_id"])
        if "invited_by" in data_copy and isinstance(data_copy["invited_by"], ObjectId):
            data_copy["invited_by"] = str(data_copy["invited_by"])
        return cls(**data_copy)


class OrganizationInvitation(BaseModel):
    """Organization invitation model."""

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., alias="_id", description="Invitation ID")
    organization_id: str = Field(..., description="Organization ID")
    email: str = Field(..., description="Email address to invite")
    role: str = Field(..., description="Member role (admin, member, viewer)")
    invited_by: str = Field(..., description="User ID who sent invitation")
    token: str = Field(..., description="Unique invitation token")
    expires_at: datetime = Field(..., description="Expiration timestamp")
    status: str = Field(default="pending", description="Invitation status (pending, accepted, expired, revoked)")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for MongoDB storage.

        Returns:
            Dictionary representation
        """
        data = self.model_dump(exclude={"id"}, by_alias=True)
        data["_id"] = ObjectId(self.id)
        data["organization_id"] = ObjectId(self.organization_id) if self.organization_id else None
        data["invited_by"] = ObjectId(self.invited_by) if self.invited_by else None
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "OrganizationInvitation":
        """Create from MongoDB document.

        Args:
            data: MongoDB document

        Returns:
            OrganizationInvitation instance
        """
        data_copy = data.copy()
        if "_id" in data_copy:
            data_copy["id"] = str(data_copy["_id"])
            del data_copy["_id"]
        if "organization_id" in data_copy and isinstance(data_copy["organization_id"], ObjectId):
            data_copy["organization_id"] = str(data_copy["organization_id"])
        if "invited_by" in data_copy and isinstance(data_copy["invited_by"], ObjectId):
            data_copy["invited_by"] = str(data_copy["invited_by"])
        return cls(**data_copy)


class CreateOrganizationRequest(BaseModel):
    """Request to create organization."""

    name: str = Field(..., min_length=1, max_length=100, description="Organization name")
    plan_id: str = Field(default="team", description="Plan ID (team or enterprise)")


class InviteMemberRequest(BaseModel):
    """Request to invite member."""

    email: str = Field(..., description="Email address to invite")
    role: str = Field(default="member", description="Member role (admin, member, viewer)")


class UpdateMemberRoleRequest(BaseModel):
    """Request to update member role."""

    role: str = Field(..., description="New role (owner, admin, member, viewer)")


class UpdateOrganizationRequest(BaseModel):
    """Request to update organization."""

    name: Optional[str] = Field(default=None, min_length=1, max_length=100, description="Organization name")
    settings: Optional[dict[str, Any]] = Field(default=None, description="Organization settings")
    metadata: Optional[dict[str, Any]] = Field(default=None, description="Custom metadata")


class UpdateAllowedDomainsRequest(BaseModel):
    """Request to update allowed email domains."""

    allowed_domains: list[str] = Field(..., description="List of allowed email domains")
    require_domain_match: bool = Field(default=False, description="Require domain match for invitations")
