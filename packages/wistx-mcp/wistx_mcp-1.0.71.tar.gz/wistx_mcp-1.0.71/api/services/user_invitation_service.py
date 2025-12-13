"""User invitation service for B2B account creation."""

import logging
import secrets
from datetime import datetime, timedelta
from typing import Any, Optional

from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from api.database.mongodb import mongodb_manager
from api.models.audit_log import AuditEventType, AuditLogSeverity
from api.services.audit_log_service import audit_log_service
from api.exceptions import ValidationError

logger = logging.getLogger(__name__)

INVITATION_TOKEN_LENGTH = 32
INVITATION_EXPIRY_DAYS = 7


class UserInvitationService:
    """Service for managing user invitations (B2B account creation)."""

    def __init__(self):
        """Initialize user invitation service."""
        self._db = None

    @property
    def db(self):
        """Get database connection (lazy initialization)."""
        if self._db is None:
            self._db = mongodb_manager.get_database()
        return self._db

    def _generate_token(self) -> str:
        """Generate secure invitation token.

        Returns:
            URL-safe token string
        """
        return secrets.token_urlsafe(INVITATION_TOKEN_LENGTH)

    async def create_user_with_invitation(
        self,
        email: str,
        plan: str,
        created_by: str,
        full_name: Optional[str] = None,
        organization_name: Optional[str] = None,
        send_invitation: bool = True,
        skip_non_critical: bool = False,
    ) -> dict[str, Any]:
        """Create user account with invitation.

        Args:
            email: User email address
            plan: Plan ID (professional, team, enterprise)
            created_by: Admin/sales user ID who created the account
            full_name: Optional full name (pre-fills onboarding)
            organization_name: Optional organization name (pre-fills onboarding)
            send_invitation: Whether to send invitation email

        Returns:
            Created user and invitation details

        Raises:
            ValueError: If user already exists or invalid plan
        """
        email_lower = email.lower().strip()

        existing_user = self.db.users.find_one({"email": email_lower})
        if existing_user:
            user_id = str(existing_user.get("_id", ""))
            created_at = existing_user.get("created_at")
            
            if created_at:
                if isinstance(created_at, str):
                    try:
                        created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    except (ValueError, AttributeError):
                        created_at = None
                elif not isinstance(created_at, datetime):
                    created_at = None
                
                if created_at:
                    time_diff = (datetime.utcnow() - created_at).total_seconds()
                    if time_diff < 10:
                        logger.info(
                            "User %s was created %.2f seconds ago, returning existing user (idempotent operation)",
                            email_lower,
                            time_diff,
                        )
                        existing_token = existing_user.get("invitation_token")
                        existing_expires = existing_user.get("invitation_expires_at")
                        invitation_sent = existing_user.get("invitation_sent_at") is not None
                        
                        from api.config import settings
                        frontend_url_raw = (
                            str(settings.oauth_frontend_redirect_url_prod).replace("/auth/callback/{provider}", "")
                            if not settings.debug
                            else str(settings.oauth_frontend_redirect_url_dev).replace("/auth/callback/{provider}", "")
                        )
                        if not frontend_url_raw.endswith("/"):
                            frontend_url_raw = frontend_url_raw.rstrip("/")
                        if frontend_url_raw.startswith("http://") and not settings.debug:
                            frontend_url_raw = frontend_url_raw.replace("http://", "https://", 1)
                        invitation_url = f"{frontend_url_raw}/auth?invite_token={existing_token}" if existing_token else ""
                        
                        return {
                            "user_id": user_id,
                            "email": email_lower,
                            "plan": existing_user.get("plan", plan),
                            "invitation_token": existing_token,
                            "invitation_url": invitation_url,
                            "expires_at": existing_expires.isoformat() if existing_expires else (datetime.utcnow() + timedelta(days=INVITATION_EXPIRY_DAYS)).isoformat(),
                            "invitation_sent": invitation_sent,
                        }
            
            if existing_user.get("invitation_token") and not existing_user.get("invitation_accepted_at"):
                expires_at = existing_user.get("invitation_expires_at")
                if expires_at and expires_at > datetime.utcnow():
                    raise ValidationError(
                        message=f"User with email {email} already exists with a pending invitation",
                        user_message=f"User with email {email} already has a pending invitation. Use the resend invitation endpoint to send a new invitation.",
                        error_code="USER_PENDING_INVITATION",
                        details={"email": email, "user_id": user_id, "expires_at": expires_at.isoformat() if expires_at else None}
                    )
                else:
                    raise ValidationError(
                        message=f"User with email {email} already exists with an expired invitation",
                        user_message=f"User with email {email} already has an expired invitation. Use the resend invitation endpoint to send a new invitation.",
                        error_code="USER_EXPIRED_INVITATION",
                        details={"email": email, "user_id": user_id}
                    )
            else:
                raise ValidationError(
                    message=f"User with email {email} already exists",
                    user_message=f"User with email {email} already exists. This user may have already completed onboarding.",
                    error_code="USER_ALREADY_EXISTS",
                    details={"email": email, "user_id": user_id}
                )

        valid_plans = ["professional", "team", "enterprise"]
        if plan not in valid_plans:
            raise ValidationError(
                message=f"Invalid plan: {plan}",
                user_message=f"Invalid plan. Valid plans: {', '.join(valid_plans)}",
                error_code="INVALID_PLAN",
                details={"plan": plan, "valid_plans": valid_plans}
            )

        token = self._generate_token()
        expires_at = datetime.utcnow() + timedelta(days=INVITATION_EXPIRY_DAYS)

        user_dict = {
            "_id": ObjectId(),
            "email": email_lower,
            "plan": plan,
            "subscription_status": "inactive",
            "is_active": False,
            "profile_completed": False,
            "onboarding_completed": False,
            "full_name": full_name,
            "organization_name": organization_name,
            "referral_source": "Demo Call",
            "invitation_token": token,
            "invitation_expires_at": expires_at,
            "invitation_sent_at": None,
            "invitation_accepted_at": None,
            "created_by_admin": ObjectId(created_by),
            "account_type": "b2b",
            "allow_self_serve_checkout": True,
            "money_back_guarantee_start": None,
            "money_back_guarantee_end": None,
            "money_back_guarantee_used": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        try:
            self.db.users.insert_one(user_dict)
            user_id = str(user_dict["_id"])
        except DuplicateKeyError:
            existing_user = self.db.users.find_one({"email": email_lower})
            if existing_user:
                user_id = str(existing_user.get("_id", ""))
                created_recently = existing_user.get("created_at")
                
                if created_recently:
                    if isinstance(created_recently, str):
                        try:
                            created_recently = datetime.fromisoformat(created_recently.replace("Z", "+00:00"))
                        except (ValueError, AttributeError):
                            created_recently = None
                    elif not isinstance(created_recently, datetime):
                        created_recently = None
                    
                    if created_recently:
                        time_diff = (datetime.utcnow() - created_recently).total_seconds()
                        if time_diff < 5:
                            logger.info(
                                "User %s was created by concurrent request %.2f seconds ago, returning existing user",
                                email_lower,
                                time_diff,
                            )
                        existing_token = existing_user.get("invitation_token")
                        existing_expires = existing_user.get("invitation_expires_at")
                        invitation_sent = existing_user.get("invitation_sent_at") is not None
                        
                        if not existing_token or (existing_expires and existing_expires <= datetime.utcnow()):
                            new_token = self._generate_token()
                            new_expires = datetime.utcnow() + timedelta(days=INVITATION_EXPIRY_DAYS)
                            self.db.users.update_one(
                                {"_id": existing_user["_id"]},
                                {
                                    "$set": {
                                        "invitation_token": new_token,
                                        "invitation_expires_at": new_expires,
                                        "invitation_sent_at": None,
                                        "invitation_accepted_at": None,
                                    }
                                },
                            )
                            existing_token = new_token
                            existing_expires = new_expires
                            invitation_sent = False
                            
                            if send_invitation:
                                from api.config import settings as config_settings
                                frontend_url_resend_raw = (
                                    str(config_settings.oauth_frontend_redirect_url_prod).replace("/auth/callback/{provider}", "")
                                    if not config_settings.debug
                                    else str(config_settings.oauth_frontend_redirect_url_dev).replace("/auth/callback/{provider}", "")
                                )
                                if not frontend_url_resend_raw.endswith("/"):
                                    frontend_url_resend_raw = frontend_url_resend_raw.rstrip("/")
                                if frontend_url_resend_raw.startswith("http://") and not config_settings.debug:
                                    frontend_url_resend_raw = frontend_url_resend_raw.replace("http://", "https://", 1)
                                invitation_url_resend = f"{frontend_url_resend_raw}/auth?invite_token={new_token}"
                                
                                await self._send_invitation_email(
                                    email=email_lower,
                                    full_name=full_name,
                                    token=new_token,
                                    expires_at=new_expires,
                                    plan=plan,
                                    invitation_url=invitation_url_resend,
                                )
                                self.db.users.update_one(
                                    {"_id": existing_user["_id"]},
                                    {"$set": {"invitation_sent_at": datetime.utcnow()}},
                                )
                                invitation_sent = True
                        
                        from api.config import settings
                        frontend_url_raw = (
                            str(settings.oauth_frontend_redirect_url_prod).replace("/auth/callback/{provider}", "")
                            if not settings.debug
                            else str(settings.oauth_frontend_redirect_url_dev).replace("/auth/callback/{provider}", "")
                        )
                        if frontend_url_raw.startswith("http://") and not settings.debug:
                            frontend_url_raw = frontend_url_raw.replace("http://", "https://", 1)
                        frontend_url = frontend_url_raw
                        if not frontend_url.endswith("/"):
                            frontend_url = frontend_url.rstrip("/")
                        invitation_url = f"{frontend_url}/auth?invite_token={existing_token}"
                        
                        return {
                            "user_id": user_id,
                            "email": email_lower,
                            "plan": existing_user.get("plan", plan),
                            "invitation_token": existing_token,
                            "invitation_url": invitation_url,
                            "expires_at": existing_expires.isoformat() if existing_expires else (datetime.utcnow() + timedelta(days=INVITATION_EXPIRY_DAYS)).isoformat(),
                            "invitation_sent": invitation_sent,
                        }
                
                if existing_user.get("invitation_token") and not existing_user.get("invitation_accepted_at"):
                    expires_at_check = existing_user.get("invitation_expires_at")
                    if expires_at_check and expires_at_check > datetime.utcnow():
                        raise ValidationError(
                            message=f"User with email {email} already exists with a pending invitation",
                            user_message=f"User with email {email} already has a pending invitation. Use the resend invitation endpoint to send a new invitation.",
                            error_code="USER_PENDING_INVITATION",
                            details={"email": email, "user_id": user_id}
                        )
                    else:
                        raise ValidationError(
                            message=f"User with email {email} already exists with an expired invitation",
                            user_message=f"User with email {email} already has an expired invitation. Use the resend invitation endpoint to send a new invitation.",
                            error_code="USER_EXPIRED_INVITATION",
                            details={"email": email, "user_id": user_id}
                        )
                else:
                    raise ValidationError(
                        message=f"User with email {email} already exists",
                        user_message=f"User with email {email} already exists. This user may have already completed onboarding.",
                        error_code="USER_ALREADY_EXISTS",
                        details={"email": email, "user_id": user_id}
                    )
            else:
                raise ValueError(f"User with email {email} already exists (duplicate key error - user may have been created by another request)")

        user_id = str(user_dict["_id"])

        if plan in ["team", "enterprise"] and organization_name:
            try:
                from api.services.organization_service import organization_service
                from fastapi import Request

                org_dict = await organization_service.create_organization(
                    user_id=user_id,
                    name=organization_name,
                    plan_id=plan,
                    request=None,
                )
                logger.info(
                    "Organization '%s' auto-created for user %s (plan: %s)",
                    organization_name,
                    user_id,
                    plan,
                )
            except Exception as e:
                logger.warning(
                    "Failed to auto-create organization for user %s: %s. User can create it manually later.",
                    user_id,
                    e,
                )

        from api.config import settings

        frontend_url = (
            settings.oauth_frontend_redirect_url_prod.replace("/auth/callback/{provider}", "")
            if not settings.debug
            else settings.oauth_frontend_redirect_url_dev.replace("/auth/callback/{provider}", "")
        )
        if not frontend_url.endswith("/"):
            frontend_url = frontend_url.rstrip("/")
        invitation_url = f"{frontend_url}/auth?invite_token={token}"

        if send_invitation and not skip_non_critical:
            try:
                await self._send_invitation_email(
                    email=email_lower,
                    full_name=full_name,
                    token=token,
                    expires_at=expires_at,
                    plan=plan,
                    invitation_url=invitation_url,
                )
                self.db.users.update_one(
                    {"_id": ObjectId(user_id)},
                    {"$set": {"invitation_sent_at": datetime.utcnow()}},
                )
            except Exception as e:
                logger.warning(
                    "Failed to send invitation email for user %s: %s. User was created successfully.",
                    user_id,
                    e,
                )

        if not skip_non_critical:
            try:
                audit_log_service.log_event(
                    event_type=AuditEventType.USER_CREATED,
                    user_id=created_by,
                    severity=AuditLogSeverity.LOW,
                    details={
                        "created_user_id": user_id,
                        "created_user_email": email_lower,
                        "plan": plan,
                        "invitation_sent": send_invitation,
                        "organization_auto_created": plan in ["team", "enterprise"] and organization_name is not None,
                    },
                )
            except Exception as e:
                logger.warning(
                    "Failed to log audit event for user creation %s: %s. User was created successfully.",
                    user_id,
                    e,
                )

        from api.config import settings

        frontend_url = (
            settings.oauth_frontend_redirect_url_prod.replace("/auth/callback/{provider}", "")
            if not settings.debug
            else settings.oauth_frontend_redirect_url_dev.replace("/auth/callback/{provider}", "")
        )
        if not frontend_url.endswith("/"):
            frontend_url = frontend_url.rstrip("/")
        invitation_url = f"{frontend_url}/auth?invite_token={token}"

        logger.info("User account created with invitation: %s (plan: %s)", email_lower, plan)

        return {
            "user_id": user_id,
            "email": email_lower,
            "plan": plan,
            "invitation_token": token,
            "invitation_url": invitation_url,
            "expires_at": expires_at.isoformat(),
            "invitation_sent": send_invitation,
        }

    def get_pending_invitation_by_email(self, email: str) -> Optional[dict[str, Any]]:
        """Check if user has pending invitation by email.

        Args:
            email: User email address

        Returns:
            User document with pending invitation if found, None otherwise
        """
        email_lower = email.lower().strip()
        user = self.db.users.find_one({"email": email_lower})
        
        if not user:
            return None
        
        invitation_token = user.get("invitation_token")
        invitation_accepted_at = user.get("invitation_accepted_at")
        invitation_expires_at = user.get("invitation_expires_at")
        
        if not invitation_token:
            return None
        
        if invitation_accepted_at:
            return None
        
        if invitation_expires_at and invitation_expires_at < datetime.utcnow():
            return None
        
        return user

    async def _send_invitation_email(
        self,
        email: str,
        full_name: Optional[str],
        token: str,
        expires_at: datetime,
        plan: str,
        invitation_url: str,
    ) -> None:
        """Send invitation email to user.

        Args:
            email: User email
            full_name: User full name (if provided)
            token: Invitation token
            expires_at: Token expiration date
            plan: Plan name
            invitation_url: Full invitation URL
        """
        try:
            from api.services.email import email_service

            user_name = full_name or email.split("@")[0]

            await email_service.send_template(
                template_name="user_invitation",
                to=email,
                subject=f"Welcome to WISTX - Complete Your {plan.capitalize()} Plan Setup",
                context={
                    "user_name": user_name,
                    "user_email": email,
                    "plan_name": plan.capitalize(),
                    "invitation_url": invitation_url,
                    "expires_at": expires_at.strftime("%B %d, %Y at %I:%M %p UTC"),
                    "current_year": datetime.now().year,
                },
                tags=["user_invitation", "b2b", "onboarding"],
                metadata={
                    "plan": plan,
                    "invitation_token": token,
                },
            )
            logger.info("User invitation email sent to %s", email)
        except Exception as e:
            logger.warning("Failed to send user invitation email to %s: %s", email, e)
            raise

    async def send_invitation_email_background(
        self,
        user_id: str,
        invitation_token: str,
    ) -> None:
        """Send invitation email in background (for BackgroundTasks).

        Args:
            user_id: User ID
            invitation_token: Invitation token
        """
        try:
            user = self.db.users.find_one({"_id": ObjectId(user_id)})
            if not user:
                logger.error("User not found for background email send: %s", user_id)
                return

            email = user.get("email")
            full_name = user.get("full_name")
            plan = user.get("plan", "professional")
            expires_at = user.get("invitation_expires_at")

            if not email or not expires_at:
                logger.error("Missing required fields for background email send: user_id=%s", user_id)
                return

            if isinstance(expires_at, str):
                try:
                    expires_at = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
                except (ValueError, AttributeError):
                    logger.error("Invalid expiration date format: %s", expires_at)
                    return
            elif not isinstance(expires_at, datetime):
                logger.error("Invalid expiration date type: %s", type(expires_at))
                return

            from api.config import settings

            frontend_url_raw = (
                str(settings.oauth_frontend_redirect_url_prod).replace("/auth/callback/{provider}", "")
                if not settings.debug
                else str(settings.oauth_frontend_redirect_url_dev).replace("/auth/callback/{provider}", "")
            )
            if not frontend_url_raw.endswith("/"):
                frontend_url_raw = frontend_url_raw.rstrip("/")
            
            if frontend_url_raw.startswith("http://") and not settings.debug:
                frontend_url_raw = frontend_url_raw.replace("http://", "https://", 1)
                logger.warning(
                    "Converted HTTP to HTTPS for background invitation URL",
                    extra={"original_url": frontend_url_raw, "user_id": user_id},
                )
            
            invitation_url = f"{frontend_url_raw}/auth?invite_token={invitation_token}"

            await self._send_invitation_email(
                email=email,
                full_name=full_name,
                token=invitation_token,
                expires_at=expires_at,
                plan=plan,
                invitation_url=invitation_url,
            )

            self.db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"invitation_sent_at": datetime.utcnow()}},
            )
            logger.info("Background invitation email sent successfully for user %s", user_id)
        except Exception as e:
            logger.error(
                "Failed to send background invitation email for user %s: %s",
                user_id,
                e,
                exc_info=True,
            )

    async def log_audit_event_background(
        self,
        created_by: str,
        user_id: str,
        email: str,
        plan: str,
        organization_auto_created: bool = False,
        invitation_sent: bool = False,
    ) -> None:
        """Log audit event in background (for BackgroundTasks).

        Args:
            created_by: Admin user ID who created the account
            user_id: Created user ID
            email: Created user email
            plan: User plan
            organization_auto_created: Whether organization was auto-created
            invitation_sent: Whether invitation was sent
        """
        try:
            audit_log_service.log_event(
                event_type=AuditEventType.USER_CREATED,
                user_id=created_by,
                severity=AuditLogSeverity.LOW,
                details={
                    "created_user_id": user_id,
                    "created_user_email": email,
                    "plan": plan,
                    "invitation_sent": invitation_sent,
                    "organization_auto_created": organization_auto_created,
                },
            )
            logger.debug("Background audit log event created successfully for user %s", user_id)
        except Exception as e:
            logger.error(
                "Failed to log background audit event for user creation %s: %s",
                user_id,
                e,
                exc_info=True,
            )

    async def validate_invitation_token(self, token: str) -> dict[str, Any]:
        """Validate invitation token.

        Args:
            token: Invitation token

        Returns:
            User document if token is valid

        Raises:
            ValueError: If token is invalid or expired
        """
        user = self.db.users.find_one({"invitation_token": token})
        if not user:
            raise ValidationError(
                message="Invalid invitation token",
                user_message="Invalid invitation token. Please check your invitation link.",
                error_code="INVALID_INVITATION_TOKEN",
                details={"token_prefix": token[:8] if token else None}
            )

        user_id = str(user["_id"])

        if user.get("invitation_accepted_at"):
            raise ValidationError(
                message="Invitation has already been accepted",
                user_message="This invitation has already been accepted",
                error_code="INVITATION_ALREADY_ACCEPTED",
                details={"user_id": user_id}
            )

        expires_at = user.get("invitation_expires_at")
        if expires_at and expires_at < datetime.utcnow():
            raise ValidationError(
                message="Invitation has expired",
                user_message="This invitation has expired. Please request a new invitation.",
                error_code="INVITATION_EXPIRED",
                details={"user_id": user_id}
            )

        return user

    async def accept_invitation(self, token: str, user_id: str) -> None:
        """Mark invitation as accepted and create organization if needed.

        Args:
            token: Invitation token
            user_id: User ID who accepted the invitation
        """
        user = self.db.users.find_one({"invitation_token": token})
        if not user:
            raise ValidationError(
                message="Invalid invitation token",
                user_message="Invalid invitation token. Please check your invitation link.",
                error_code="INVALID_INVITATION_TOKEN",
                details={"token_prefix": token[:8] if token else None}
            )

        if str(user["_id"]) != user_id:
            raise ValidationError(
                message="Invitation token does not match user ID",
                user_message="Invitation token does not match your account. Please use the correct invitation link.",
                error_code="TOKEN_USER_MISMATCH",
                details={"user_id": user_id, "token_prefix": token[:8] if token else None}
            )

        plan = user.get("plan", "professional")
        organization_name = user.get("organization_name")
        existing_org_id = user.get("organization_id")

        if plan in ["team", "enterprise"] and organization_name and not existing_org_id:
            try:
                from api.services.organization_service import organization_service

                org_dict = await organization_service.create_organization(
                    user_id=user_id,
                    name=organization_name,
                    plan_id=plan,
                    request=None,
                )
                logger.info(
                    "Organization '%s' auto-created during invitation acceptance for user %s (plan: %s)",
                    organization_name,
                    user_id,
                    plan,
                )
            except Exception as e:
                logger.error(
                    "Failed to auto-create organization during invitation acceptance for user %s: %s",
                    user_id,
                    e,
                    exc_info=True,
                )

        self.db.users.update_one(
            {"invitation_token": token},
            {
                "$set": {
                    "invitation_accepted_at": datetime.utcnow(),
                    "invitation_token": None,
                    "updated_at": datetime.utcnow(),
                }
            },
        )
        logger.info("Invitation accepted by user %s", user_id)

    async def resend_invitation(self, user_id: str) -> dict[str, Any]:
        """Resend invitation email to user.

        Args:
            user_id: User ID

        Returns:
            Invitation details

        Raises:
            ValueError: If user not found or invitation already accepted
        """
        user = self.db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            from api.exceptions import NotFoundError
            raise NotFoundError(
                message=f"User not found: {user_id}",
                user_message="User not found",
                error_code="USER_NOT_FOUND",
                details={"user_id": user_id}
            )

        if user.get("invitation_accepted_at"):
            raise ValidationError(
                message="Invitation has already been accepted",
                user_message="This invitation has already been accepted",
                error_code="INVITATION_ALREADY_ACCEPTED",
                details={"user_id": user_id}
            )

        if not user.get("invitation_token"):
            token = self._generate_token()
            expires_at = datetime.utcnow() + timedelta(days=INVITATION_EXPIRY_DAYS)
            self.db.users.update_one(
                {"_id": ObjectId(user_id)},
                {
                    "$set": {
                        "invitation_token": token,
                        "invitation_expires_at": expires_at,
                    }
                },
            )
        else:
            token = user["invitation_token"]
            expires_at = user.get("invitation_expires_at", datetime.utcnow() + timedelta(days=INVITATION_EXPIRY_DAYS))

        from api.config import settings as config_settings
        frontend_url_resend_raw = (
            str(config_settings.oauth_frontend_redirect_url_prod).replace("/auth/callback/{provider}", "")
            if not config_settings.debug
            else str(config_settings.oauth_frontend_redirect_url_dev).replace("/auth/callback/{provider}", "")
        )
        if not frontend_url_resend_raw.endswith("/"):
            frontend_url_resend_raw = frontend_url_resend_raw.rstrip("/")
        
        if frontend_url_resend_raw.startswith("http://") and not config_settings.debug:
            frontend_url_resend_raw = frontend_url_resend_raw.replace("http://", "https://", 1)
            logger.warning(
                "Converted HTTP to HTTPS for resend invitation URL",
                extra={"original_url": frontend_url_resend_raw, "user_id": user_id},
            )
        
        invitation_url_resend = f"{frontend_url_resend_raw}/auth?invite_token={token}"

        await self._send_invitation_email(
            email=user["email"],
            full_name=user.get("full_name"),
            token=token,
            expires_at=expires_at,
            plan=user.get("plan", "professional"),
            invitation_url=invitation_url_resend,
        )

        self.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"invitation_sent_at": datetime.utcnow()}},
        )

        from api.config import settings

        frontend_url = (
            settings.oauth_frontend_redirect_url_prod.replace("/auth/callback/{provider}", "")
            if not settings.debug
            else settings.oauth_frontend_redirect_url_dev.replace("/auth/callback/{provider}", "")
        )
        if not frontend_url.endswith("/"):
            frontend_url = frontend_url.rstrip("/")
        invitation_url = f"{frontend_url}/auth?invite_token={token}"

        return {
            "invitation_token": token,
            "invitation_url": invitation_url,
            "expires_at": expires_at.isoformat(),
        }


user_invitation_service = UserInvitationService()

