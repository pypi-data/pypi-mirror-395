"""Organization service for team management."""

import logging
import secrets
from datetime import datetime, timedelta
from typing import Any

from bson import ObjectId
from fastapi import Request

from api.database.mongodb import mongodb_manager
from api.exceptions import NotFoundError, AuthorizationError, ValidationError
from api.models.audit_log import AuditEventType, AuditLogSeverity
from api.models.organization import (
    CreateOrganizationRequest,
    InviteMemberRequest,
    Organization,
    OrganizationInvitation,
    OrganizationMember,
    UpdateMemberRoleRequest,
    UpdateOrganizationRequest,
)
from api.services.audit_log_service import audit_log_service
from api.utils.slug import generate_slug, generate_unique_slug

logger = logging.getLogger(__name__)

INVITATION_TOKEN_LENGTH = 32
INVITATION_EXPIRY_DAYS = 7


class OrganizationService:
    """Service for managing organizations and team members."""

    def __init__(self):
        """Initialize organization service."""
        self._db = None

    @property
    def db(self):
        """Get database connection."""
        if self._db is None:
            mongodb_manager.connect()
            self._db = mongodb_manager.get_database()
        return self._db

    async def create_organization(
        self,
        user_id: str,
        name: str,
        plan_id: str = "team",
        request: Request | None = None,
    ) -> dict[str, Any]:
        """Create new organization.

        **CRITICAL**: Only Team and Enterprise plans can create organizations.
        Professional plan users cannot create organizations.

        Args:
            user_id: User ID creating the organization
            name: Organization name
            plan_id: Plan ID (team or enterprise)
            request: FastAPI request object for audit logging

        Returns:
            Created organization document

        Raises:
            HTTPException: If user plan doesn't support organizations
        """
        user = self.db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise NotFoundError(
                message=f"User not found: {user_id}",
                user_message="User not found",
                error_code="USER_NOT_FOUND",
                details={"user_id": user_id}
            )

        user_plan = user.get("plan")

        if user_plan not in ["team", "enterprise"]:
            raise AuthorizationError(
                message=f"Organization features require Team or Enterprise plan. Current plan: {user_plan}",
                user_message=f"Organization features require Team or Enterprise plan. Your current plan: {user_plan}. Professional plan ($99/month) is for individual use only.",
                error_code="PLAN_NOT_SUPPORTED",
                details={"user_plan": user_plan, "required_plans": ["team", "enterprise"]}
            )

        if plan_id != user_plan:
            raise ValidationError(
                message=f"Organization plan ({plan_id}) must match user plan ({user_plan})",
                user_message=f"Organization plan must match your current plan. Your plan: {user_plan}, requested plan: {plan_id}",
                error_code="PLAN_MISMATCH",
                details={"user_plan": user_plan, "requested_plan": plan_id}
            )

        base_slug = generate_slug(name)
        existing_slugs = [
            org["slug"]
            for org in self.db.organizations.find({"slug": {"$regex": f"^{base_slug}"}}, {"slug": 1})
        ]
        slug = generate_unique_slug(base_slug, existing_slugs)

        now = datetime.utcnow()
        org_id = str(ObjectId())
        organization = Organization.model_validate({
            "id": org_id,
            "name": name,
            "slug": slug,
            "plan_id": plan_id,
            "created_by": user_id,
            "created_at": now,
            "updated_at": now,
        })

        org_dict = organization.to_dict()
        self.db.organizations.insert_one(org_dict)

        member_id = str(ObjectId())
        member = OrganizationMember.model_validate({
            "id": member_id,
            "organization_id": organization.id,
            "user_id": user_id,
            "role": "owner",
            "invited_by": user_id,
            "joined_at": now,
        })

        member_dict = member.to_dict()
        self.db.organization_members.insert_one(member_dict)

        self.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"organization_id": ObjectId(organization.id)}},
        )

        audit_log_service.log_event(
            event_type=AuditEventType.ORGANIZATION_CREATED,
            severity=AuditLogSeverity.LOW,
            message=f"Organization '{name}' created",
            success=True,
            user_id=user_id,
            organization_id=organization.id,
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None,
            details={
                "organization_name": name,
                "organization_slug": slug,
                "plan_id": plan_id,
            },
            compliance_tags=["SOC2-CC6.1", "ISO-27001-A.9.2"],
        )

        logger.info("Organization created: %s by user %s", organization.id, user_id)
        return org_dict

    async def get_organization(self, organization_id: str) -> dict[str, Any] | None:
        """Get organization by ID.

        Args:
            organization_id: Organization ID

        Returns:
            Organization document or None
        """
        org = self.db.organizations.find_one({"_id": ObjectId(organization_id), "status": "active"})
        return org

    async def list_user_organizations(self, user_id: str) -> list[dict[str, Any]]:
        """List organizations user is a member of.

        Args:
            user_id: User ID

        Returns:
            List of organization documents
        """
        user = self.db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return []

        org_ids = set()

        user_org_id = user.get("organization_id")
        if user_org_id:
            org_ids.add(ObjectId(user_org_id) if isinstance(user_org_id, str) else user_org_id)

        memberships = list(
            self.db.organization_members.find(
                {"user_id": ObjectId(user_id), "status": "active"},
                {"organization_id": 1},
            )
        )

        for membership in memberships:
            org_id = membership.get("organization_id")
            if org_id:
                org_ids.add(ObjectId(org_id) if isinstance(org_id, str) else org_id)

        if not org_ids:
            return []

        organizations = list(
            self.db.organizations.find(
                {"_id": {"$in": list(org_ids)}, "status": "active"},
            )
        )

        return organizations

    async def update_organization(
        self,
        organization_id: str,
        updates: UpdateOrganizationRequest,
        updated_by: str,
        request: Request | None = None,
    ) -> dict[str, Any]:
        """Update organization.

        Args:
            organization_id: Organization ID
            updates: Update request
            updated_by: User ID making the update
            request: FastAPI request object for audit logging

        Returns:
            Updated organization document

        Raises:
            HTTPException: If organization not found or user lacks permission
        """
        org = await self.get_organization(organization_id)
        if not org:
            raise NotFoundError(
                message=f"Organization not found: {organization_id}",
                user_message="Organization not found",
                error_code="ORGANIZATION_NOT_FOUND",
                details={"organization_id": organization_id}
            )

        member = self.db.organization_members.find_one(
            {
                "organization_id": ObjectId(organization_id),
                "user_id": ObjectId(updated_by),
                "status": "active",
            }
        )

        if not member or member.get("role") not in ["owner", "admin"]:
            raise AuthorizationError(
                message="Admin or owner role required to update organization",
                user_message="You must be an admin or owner to update this organization",
                error_code="INSUFFICIENT_PERMISSIONS",
                details={"organization_id": organization_id, "user_id": updated_by, "required_roles": ["owner", "admin"]}
            )

        update_data: dict[str, Any] = {"updated_at": datetime.utcnow()}

        if updates.name:
            base_slug = generate_slug(updates.name)
            existing_slugs = [
                o["slug"]
                for o in self.db.organizations.find(
                    {"slug": {"$regex": f"^{base_slug}"}, "_id": {"$ne": ObjectId(organization_id)}},
                    {"slug": 1},
                )
            ]
            slug = generate_unique_slug(base_slug, existing_slugs)
            update_data["name"] = updates.name
            update_data["slug"] = slug

        if updates.settings:
            update_data["settings"] = updates.settings

        if updates.metadata:
            update_data["metadata"] = updates.metadata

        self.db.organizations.update_one(
            {"_id": ObjectId(organization_id)},
            {"$set": update_data},
        )

        audit_log_service.log_event(
            event_type=AuditEventType.ORGANIZATION_UPDATED,
            severity=AuditLogSeverity.LOW,
            message=f"Organization '{organization_id}' updated",
            success=True,
            user_id=updated_by,
            organization_id=organization_id,
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None,
            details=update_data,
            compliance_tags=["SOC2-CC6.1", "ISO-27001-A.9.2"],
        )

        return await self.get_organization(organization_id)

    async def validate_invitation_token(self, token: str) -> dict[str, Any]:
        """Validate invitation token and return invitation details.

        Args:
            token: Invitation token

        Returns:
            Dictionary with invitation details including organization name and inviter name

        Raises:
            HTTPException: If invitation not found, expired, or invalid
        """
        invitation = self.db.organization_invitations.find_one({"token": token})

        if not invitation:
            raise NotFoundError(
                message=f"Invitation not found for token: {token[:8]}...",
                user_message="Invitation not found or invalid",
                error_code="INVITATION_NOT_FOUND",
                details={"token_prefix": token[:8]}
            )

        if invitation.get("status") != "pending":
            raise ValidationError(
                message=f"Invitation already {invitation.get('status')}",
                user_message=f"This invitation has already been {invitation.get('status')}",
                error_code="INVITATION_ALREADY_PROCESSED",
                details={"status": invitation.get("status")}
            )

        if invitation.get("expires_at") < datetime.utcnow():
            self.db.organization_invitations.update_one(
                {"_id": invitation["_id"]},
                {"$set": {"status": "expired"}},
            )
            raise ValidationError(
                message="Invitation has expired",
                user_message="This invitation has expired. Please request a new invitation.",
                error_code="INVITATION_EXPIRED",
                details={"expires_at": invitation.get("expires_at").isoformat() if invitation.get("expires_at") else None}
            )

        organization_id = str(invitation["organization_id"])
        org = await self.get_organization(organization_id)
        if not org:
            raise NotFoundError(
                message=f"Organization not found: {organization_id}",
                user_message="Organization not found",
                error_code="ORGANIZATION_NOT_FOUND",
                details={"organization_id": organization_id}
            )

        inviter = self.db.users.find_one({"_id": ObjectId(invitation["invited_by"])})
        inviter_name = (
            inviter.get("full_name") or inviter.get("email", "").split("@")[0]
            if inviter
            else "Team Admin"
        )

        return {
            "organization_name": org.get("name", "Unknown Organization"),
            "invited_by_name": inviter_name,
            "role": invitation.get("role", "member"),
            "expires_at": invitation.get("expires_at").isoformat()
            if invitation.get("expires_at")
            else None,
            "email": invitation.get("email"),
        }

    async def invite_member(
        self,
        organization_id: str,
        email: str,
        role: str,
        invited_by: str,
        request: Request | None = None,
    ) -> dict[str, Any]:
        """Invite member to organization.

        Args:
            organization_id: Organization ID
            email: Email address to invite
            role: Member role (admin, member, viewer)
            invited_by: User ID sending invitation
            request: FastAPI request object for audit logging

        Returns:
            Created invitation document

        Raises:
            HTTPException: If organization not found or user lacks permission
        """
        org = await self.get_organization(organization_id)
        if not org:
            raise NotFoundError(
                message=f"Organization not found: {organization_id}",
                user_message="Organization not found",
                error_code="ORGANIZATION_NOT_FOUND",
                details={"organization_id": organization_id}
            )

        member = self.db.organization_members.find_one(
            {
                "organization_id": ObjectId(organization_id),
                "user_id": ObjectId(invited_by),
                "status": "active",
            }
        )

        if not member or member.get("role") not in ["owner", "admin"]:
            raise AuthorizationError(
                message="Admin or owner role required to invite members",
                user_message="You must be an admin or owner to invite members to this organization",
                error_code="INSUFFICIENT_PERMISSIONS",
                details={"organization_id": organization_id, "user_id": invited_by, "required_roles": ["owner", "admin"]}
            )

        if role == "owner":
            raise ValidationError(
                message="Cannot invite members as owner",
                user_message="Cannot invite members as owner. Owner role can only be assigned during organization creation.",
                error_code="INVALID_ROLE",
                details={"role": role}
            )

        org_settings = org.get("settings", {})
        require_domain_match = org_settings.get("require_domain_match", False)
        allowed_domains = org_settings.get("allowed_domains", [])

        if require_domain_match and allowed_domains:
            email_domain = email.split("@")[-1].lower()
            if email_domain not in [d.lower() for d in allowed_domains]:
                raise ValidationError(
                    message=f"Email domain '{email_domain}' is not allowed",
                    user_message=f"Email domain '{email_domain}' is not allowed. Allowed domains: {', '.join(allowed_domains)}",
                    error_code="EMAIL_DOMAIN_NOT_ALLOWED",
                    details={"email_domain": email_domain, "allowed_domains": allowed_domains}
                )

        existing_invitation = self.db.organization_invitations.find_one(
            {
                "organization_id": ObjectId(organization_id),
                "email": email,
                "status": "pending",
            }
        )

        if existing_invitation:
            logger.info("Pending invitation already exists for %s, returning existing invitation", email)
            existing_invitation_model = OrganizationInvitation.from_dict(existing_invitation)
            return existing_invitation_model.to_dict()

        token = secrets.token_urlsafe(INVITATION_TOKEN_LENGTH)
        expires_at = datetime.utcnow() + timedelta(days=INVITATION_EXPIRY_DAYS)

        invitation_id = str(ObjectId())
        invitation = OrganizationInvitation.model_validate({
            "id": invitation_id,
            "organization_id": organization_id,
            "email": email,
            "role": role,
            "invited_by": invited_by,
            "token": token,
            "expires_at": expires_at,
        })

        invitation_dict = invitation.to_dict()
        self.db.organization_invitations.insert_one(invitation_dict)

        try:
            from api.services.email import email_service
            from api.config import settings

            inviter = self.db.users.find_one({"_id": ObjectId(invited_by)})
            inviter_name = (
                inviter.get("full_name") or inviter.get("email", "").split("@")[0]
                if inviter
                else "Team Admin"
            )
            inviter_email = inviter.get("email", "") if inviter else ""

            frontend_url = (
                settings.oauth_frontend_redirect_url_prod.replace("/auth/callback/{provider}", "")
                if not settings.debug
                else settings.oauth_frontend_redirect_url_dev.replace("/auth/callback/{provider}", "")
            )
            invitation_url = f"{frontend_url}/accept-invitation?token={token}"

            await email_service.send_template(
                template_name="organization_invitation",
                to=email,
                subject=f"Invitation to join {org.get('name')} on WISTX",
                context={
                    "organization_name": org.get("name"),
                    "invited_by_name": inviter_name,
                    "invited_by_email": inviter_email,
                    "role": role,
                    "expires_at": expires_at.strftime("%B %d, %Y at %I:%M %p UTC"),
                    "invitation_url": invitation_url,
                    "invited_email": email,
                    "current_year": datetime.now().year,
                },
                tags=["organization_invitation", "team"],
                metadata={
                    "organization_id": organization_id,
                    "invitation_id": str(invitation_dict["_id"]),
                    "role": role,
                },
            )
            logger.info("Organization invitation email sent to %s", email)
        except Exception as e:
            logger.warning("Failed to send organization invitation email to %s: %s", email, e)

        audit_log_service.log_event(
            event_type=AuditEventType.ORGANIZATION_MEMBER_INVITED,
            severity=AuditLogSeverity.LOW,
            message=f"Member {email} invited to organization",
            success=True,
            user_id=invited_by,
            organization_id=organization_id,
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None,
            details={
                "invited_email": email,
                "role": role,
                "invitation_token": token,
            },
            compliance_tags=["SOC2-CC6.1", "ISO-27001-A.9.2"],
        )

        logger.info("Member invited: %s to organization %s", email, organization_id)
        return invitation_dict

    async def accept_invitation(
        self,
        token: str,
        user_id: str,
        request: Request | None = None,
    ) -> dict[str, Any]:
        """Accept organization invitation.

        Args:
            token: Invitation token
            user_id: User ID accepting invitation
            request: FastAPI request object for audit logging

        Returns:
            Created membership document

        Raises:
            HTTPException: If invitation not found, expired, or invalid
        """
        invitation = self.db.organization_invitations.find_one({"token": token})

        if not invitation:
            logger.warning("Invitation not found", {"token": token[:20] + "...", "user_id": user_id})
            raise NotFoundError(
                message=f"Invitation not found for token: {token[:8]}...",
                user_message="Invitation not found or invalid",
                error_code="INVITATION_NOT_FOUND",
                details={"token_prefix": token[:8], "user_id": user_id}
            )

        invitation_status = invitation.get("status")
        if invitation_status != "pending":
            logger.warning(
                "Attempt to accept non-pending invitation",
                {"token": token[:20] + "...", "user_id": user_id, "status": invitation_status},
            )
            raise ValidationError(
                message=f"Invitation already {invitation_status}",
                user_message=f"This invitation has already been {invitation_status}",
                error_code="INVITATION_ALREADY_PROCESSED",
                details={"status": invitation_status, "user_id": user_id}
            )

        expires_at = invitation.get("expires_at")
        if expires_at and expires_at < datetime.utcnow():
            self.db.organization_invitations.update_one(
                {"_id": invitation["_id"]},
                {"$set": {"status": "expired"}},
            )
            logger.warning(
                "Attempt to accept expired invitation",
                {
                    "token": token[:20] + "...",
                    "user_id": user_id,
                    "expires_at": expires_at.isoformat() if expires_at else None,
                    "now": datetime.utcnow().isoformat(),
                },
            )
            raise ValidationError(
                message="Invitation has expired",
                user_message="This invitation has expired. Please request a new invitation.",
                error_code="INVITATION_EXPIRED",
                details={"expires_at": expires_at.isoformat() if expires_at else None, "user_id": user_id}
            )

        user = self.db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            logger.error("User not found when accepting invitation", {"user_id": user_id, "token": token})
            raise NotFoundError(
                message=f"User not found: {user_id}",
                user_message="User not found",
                error_code="USER_NOT_FOUND",
                details={"user_id": user_id}
            )

        user_email_raw = user.get("email") or ""
        invitation_email_raw = invitation.get("email") or ""
        user_email = user_email_raw.lower().strip()
        invitation_email = invitation_email_raw.lower().strip()

        logger.debug(
            "Email comparison for invitation acceptance",
            {
                "user_id": user_id,
                "token": token[:20] + "...",
                "user_email_raw": user_email_raw,
                "invitation_email_raw": invitation_email_raw,
                "user_email_normalized": user_email,
                "invitation_email_normalized": invitation_email,
                "match": user_email == invitation_email,
            },
        )

        if user_email != invitation_email:
            logger.warning(
                "Email mismatch when accepting invitation",
                {
                    "user_id": user_id,
                    "token": token[:20] + "...",
                    "user_email": user_email_raw,
                    "invitation_email": invitation_email_raw,
                    "user_email_normalized": user_email,
                    "invitation_email_normalized": invitation_email,
                },
            )
            raise AuthorizationError(
                message=f"Invitation email ({invitation_email_raw}) does not match user email ({user_email_raw})",
                user_message=f"Invitation email ({invitation_email_raw}) does not match your account email ({user_email_raw})",
                error_code="EMAIL_MISMATCH",
                details={
                    "invitation_email": invitation_email_raw,
                    "user_email": user_email_raw,
                    "user_id": user_id
                }
            )

        organization_id = str(invitation["organization_id"])
        org = await self.get_organization(organization_id)
        if not org:
            raise NotFoundError(
                message=f"Organization not found: {organization_id}",
                user_message="Organization not found",
                error_code="ORGANIZATION_NOT_FOUND",
                details={"organization_id": organization_id}
            )

        existing_member = self.db.organization_members.find_one(
            {
                "organization_id": ObjectId(organization_id),
                "user_id": ObjectId(user_id),
            }
        )

        if existing_member:
            if existing_member.get("status") == "active":
                raise ValidationError(
                    message="User is already a member of this organization",
                    user_message="You are already a member of this organization",
                    error_code="ALREADY_MEMBER",
                    details={"organization_id": organization_id, "user_id": user_id}
                )
            self.db.organization_members.update_one(
                {"_id": existing_member["_id"]},
                {
                    "$set": {
                        "status": "active",
                        "role": invitation.get("role"),
                        "joined_at": datetime.utcnow(),
                    }
                },
            )
        else:
            member_id = str(ObjectId())
            member = OrganizationMember.model_validate({
                "id": member_id,
                "organization_id": organization_id,
                "user_id": user_id,
                "role": invitation.get("role", "member"),
                "invited_by": str(invitation["invited_by"]),
                "joined_at": datetime.utcnow(),
            })

            member_dict = member.to_dict()
            self.db.organization_members.insert_one(member_dict)

        org_plan = org.get("plan_id", "professional")
        update_fields = {
            "organization_id": ObjectId(organization_id),
        }

        if org_plan in ["team", "enterprise"]:
            update_fields["plan"] = org_plan
            logger.info(
                "Updating user plan to match organization plan",
                {
                    "user_id": user_id,
                    "organization_id": organization_id,
                    "old_plan": user.get("plan"),
                    "new_plan": org_plan,
                },
            )

        self.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_fields},
        )

        self.db.organization_invitations.update_one(
            {"_id": invitation["_id"]},
            {"$set": {"status": "accepted"}},
        )

        audit_log_service.log_event(
            event_type=AuditEventType.ORGANIZATION_MEMBER_ACCEPTED,
            severity=AuditLogSeverity.LOW,
            message=f"Member {user.get('email')} accepted invitation to organization",
            success=True,
            user_id=user_id,
            organization_id=organization_id,
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None,
            details={
                "invited_email": invitation.get("email"),
                "role": invitation.get("role"),
            },
            compliance_tags=["SOC2-CC6.1", "ISO-27001-A.9.2"],
        )

        logger.info("Invitation accepted: user %s joined organization %s", user_id, organization_id)
        return await self.list_members(organization_id)

    async def list_invitations(
        self, organization_id: str, status: str = "pending"
    ) -> list[dict[str, Any]]:
        """List organization invitations.

        Args:
            organization_id: Organization ID
            status: Invitation status filter (default: pending)

        Returns:
            List of invitation documents with inviter details
        """
        invitations = list(
            self.db.organization_invitations.find(
                {
                    "organization_id": ObjectId(organization_id),
                    "status": status,
                }
            ).sort("created_at", -1)
        )

        if not invitations:
            return []

        inviter_ids = [inv["invited_by"] for inv in invitations if inv.get("invited_by")]
        inviters = {}
        if inviter_ids:
            inviters = {
                str(u["_id"]): u
                for u in self.db.users.find(
                    {"_id": {"$in": inviter_ids}}, {"email": 1, "full_name": 1}
                )
            }

        result = []
        for inv in invitations:
            inviter = inviters.get(str(inv.get("invited_by", ""))) if inv.get("invited_by") else None
            result.append({
                "id": str(inv["_id"]),
                "email": inv.get("email"),
                "role": inv.get("role", "member"),
                "status": inv.get("status", "pending"),
                "created_at": inv.get("created_at"),
                "expires_at": inv.get("expires_at"),
                "invited_by": str(inv["invited_by"]) if inv.get("invited_by") else None,
                "invited_by_name": (
                    inviter.get("full_name") or inviter.get("email", "").split("@")[0]
                    if inviter
                    else "Unknown"
                ),
            })

        return result

    async def list_members(self, organization_id: str) -> list[dict[str, Any]]:
        """List organization members.

        Args:
            organization_id: Organization ID

        Returns:
            List of member documents with user details
        """
        members = list(
            self.db.organization_members.find(
                {"organization_id": ObjectId(organization_id), "status": "active"},
            )
        )

        if not members:
            return []

        user_ids = [m["user_id"] for m in members]
        users = {
            str(u["_id"]): u
            for u in self.db.users.find({"_id": {"$in": user_ids}}, {"email": 1, "full_name": 1})
        }

        result = []
        for member in members:
            user_id_str = str(member["user_id"])
            user = users.get(user_id_str, {})
            result.append(
                {
                    "id": str(member["_id"]),
                    "organization_id": organization_id,
                    "user_id": user_id_str,
                    "role": member.get("role"),
                    "invited_by": str(member.get("invited_by", "")),
                    "joined_at": member.get("joined_at"),
                    "status": member.get("status", "active"),
                    "permissions": member.get("permissions", []),
                    "user_email": user.get("email", "unknown"),
                    "user_name": user.get("full_name"),
                }
            )

        return result

    async def remove_member(
        self,
        organization_id: str,
        user_id: str,
        removed_by: str,
        request: Request | None = None,
    ) -> None:
        """Remove member from organization.

        Args:
            organization_id: Organization ID
            user_id: User ID to remove
            removed_by: User ID removing the member
            request: FastAPI request object for audit logging

        Raises:
            HTTPException: If organization not found, user lacks permission, or cannot remove owner
        """
        org = await self.get_organization(organization_id)
        if not org:
            raise NotFoundError(
                message=f"Organization not found: {organization_id}",
                user_message="Organization not found",
                error_code="ORGANIZATION_NOT_FOUND",
                details={"organization_id": organization_id}
            )

        member_to_remove = self.db.organization_members.find_one(
            {
                "organization_id": ObjectId(organization_id),
                "user_id": ObjectId(user_id),
                "status": "active",
            }
        )

        if not member_to_remove:
            raise NotFoundError(
                message=f"Member not found: {user_id}",
                user_message="Member not found in this organization",
                error_code="MEMBER_NOT_FOUND",
                details={"organization_id": organization_id, "user_id": user_id}
            )

        if member_to_remove.get("role") == "owner":
            raise ValidationError(
                message="Cannot remove organization owner",
                user_message="Cannot remove the organization owner. Please transfer ownership first.",
                error_code="CANNOT_REMOVE_OWNER",
                details={"organization_id": organization_id, "user_id": user_id}
            )

        remover = self.db.organization_members.find_one(
            {
                "organization_id": ObjectId(organization_id),
                "user_id": ObjectId(removed_by),
                "status": "active",
            }
        )

        if not remover or remover.get("role") not in ["owner", "admin"]:
            raise AuthorizationError(
                message="Admin or owner role required to remove members",
                user_message="You must be an admin or owner to remove members from this organization",
                error_code="INSUFFICIENT_PERMISSIONS",
                details={"organization_id": organization_id, "user_id": removed_by, "required_roles": ["owner", "admin"]}
            )

        self.db.organization_members.update_one(
            {"_id": member_to_remove["_id"]},
            {"$set": {"status": "removed"}},
        )

        self.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$unset": {"organization_id": ""}},
        )

        user = self.db.users.find_one({"_id": ObjectId(user_id)}, {"email": 1})

        audit_log_service.log_event(
            event_type=AuditEventType.ORGANIZATION_MEMBER_REMOVED,
            severity=AuditLogSeverity.LOW,
            message=f"Member {user.get('email') if user else user_id} removed from organization",
            success=True,
            user_id=removed_by,
            organization_id=organization_id,
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None,
            details={
                "removed_user_id": user_id,
                "removed_user_email": user.get("email") if user else None,
            },
            compliance_tags=["SOC2-CC6.1", "ISO-27001-A.9.2"],
        )

        logger.info("Member removed: user %s from organization %s", user_id, organization_id)

    async def update_member_role(
        self,
        organization_id: str,
        user_id: str,
        role: str,
        updated_by: str,
        request: Request | None = None,
    ) -> None:
        """Update member role.

        Args:
            organization_id: Organization ID
            user_id: User ID to update
            role: New role (owner, admin, member, viewer)
            updated_by: User ID making the update
            request: FastAPI request object for audit logging

        Raises:
            HTTPException: If organization not found, user lacks permission, or invalid role
        """
        org = await self.get_organization(organization_id)
        if not org:
            raise NotFoundError(
                message=f"Organization not found: {organization_id}",
                user_message="Organization not found",
                error_code="ORGANIZATION_NOT_FOUND",
                details={"organization_id": organization_id}
            )

        if role not in ["owner", "admin", "member", "viewer"]:
            raise ValidationError(
                message=f"Invalid role: {role}",
                user_message=f"Invalid role: {role}. Must be one of: owner, admin, member, viewer",
                error_code="INVALID_ROLE",
                details={"role": role, "valid_roles": ["owner", "admin", "member", "viewer"]}
            )

        member = self.db.organization_members.find_one(
            {
                "organization_id": ObjectId(organization_id),
                "user_id": ObjectId(user_id),
                "status": "active",
            }
        )

        if not member:
            raise NotFoundError(
                message=f"Member not found: {user_id}",
                user_message="Member not found in this organization",
                error_code="MEMBER_NOT_FOUND",
                details={"organization_id": organization_id, "user_id": user_id}
            )

        updater = self.db.organization_members.find_one(
            {
                "organization_id": ObjectId(organization_id),
                "user_id": ObjectId(updated_by),
                "status": "active",
            }
        )

        if not updater or updater.get("role") != "owner":
            raise AuthorizationError(
                message="Owner role required to update member roles",
                user_message="Only organization owners can update member roles",
                error_code="OWNER_ROLE_REQUIRED",
                details={"organization_id": organization_id, "user_id": updated_by, "required_role": "owner"}
            )

        if role == "owner" and member.get("role") != "owner":
            old_owner = self.db.organization_members.find_one(
                {
                    "organization_id": ObjectId(organization_id),
                    "role": "owner",
                    "status": "active",
                }
            )

            if old_owner and str(old_owner["user_id"]) != user_id:
                self.db.organization_members.update_one(
                    {"_id": old_owner["_id"]},
                    {"$set": {"role": "admin"}},
                )

        self.db.organization_members.update_one(
            {"_id": member["_id"]},
            {"$set": {"role": role}},
        )

        user = self.db.users.find_one({"_id": ObjectId(user_id)}, {"email": 1})

        audit_log_service.log_event(
            event_type=AuditEventType.ORGANIZATION_MEMBER_ROLE_CHANGED,
            severity=AuditLogSeverity.LOW,
            message=f"Member {user.get('email') if user else user_id} role changed to {role}",
            success=True,
            user_id=updated_by,
            organization_id=organization_id,
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None,
            details={
                "updated_user_id": user_id,
                "updated_user_email": user.get("email") if user else None,
                "old_role": member.get("role"),
                "new_role": role,
            },
            compliance_tags=["SOC2-CC6.1", "ISO-27001-A.9.2"],
        )

        logger.info("Member role updated: user %s to role %s in organization %s", user_id, role, organization_id)


organization_service = OrganizationService()

