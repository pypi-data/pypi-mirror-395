"""OAuth routers for Google and GitHub authentication."""

import logging
import time
from urllib.parse import quote

import httpx
from fastapi import APIRouter, HTTPException, Request, Query
from fastapi.responses import RedirectResponse

from api.auth.users import (
    jwt_authentication,
    google_oauth_client,
    github_oauth_client,
    UserManager,
)
from api.auth.database import MongoDBUserDatabase
from api.database.async_mongodb import async_mongodb_adapter
from api.config import settings

logger = logging.getLogger(__name__)


def _validate_oauth_config() -> None:
    """Validate OAuth configuration and warn about misconfigurations.
    
    Checks for common issues like DEBUG=true in production or missing production URLs.
    """
    if settings.debug:
        backend_url = settings.oauth_backend_callback_url_dev
        frontend_url = settings.oauth_frontend_redirect_url_dev
        
        if "api.wistx.ai" in str(backend_url) or "wistx.ai" in str(frontend_url):
            logger.critical(
                "SECURITY WARNING: DEBUG=true but production URLs detected! "
                "This will cause OAuth redirects to fail. "
                "Set DEBUG=false in production or use development URLs.",
                extra={
                    "event": "oauth_config_mismatch",
                    "debug": settings.debug,
                    "backend_url": str(backend_url),
                    "frontend_url": str(frontend_url),
                },
            )
    else:
        backend_url = settings.oauth_backend_callback_url_prod
        frontend_url = settings.oauth_frontend_redirect_url_prod
        
        if "localhost" in str(backend_url) or "localhost" in str(frontend_url):
            logger.critical(
                "SECURITY WARNING: DEBUG=false but localhost URLs detected! "
                "This will cause OAuth redirects to fail in production. "
                "Check OAUTH_BACKEND_CALLBACK_URL_PROD and OAUTH_FRONTEND_REDIRECT_URL_PROD.",
                extra={
                    "event": "oauth_config_mismatch",
                    "debug": settings.debug,
                    "backend_url": str(backend_url),
                    "frontend_url": str(frontend_url),
                },
            )


def get_oauth_backend_callback_url(provider: str, request: Request | None = None) -> str:
    """Get backend OAuth callback URL for provider.

    This is where the OAuth provider (Google/GitHub) redirects to after authorization.
    Prioritizes hostname detection over DEBUG flag to prevent misconfiguration.
    Make sure this URI is registered in the OAuth provider's console.

    Args:
        provider: OAuth provider name (google, github)
        request: Optional request object to detect production from hostname

    Returns:
        Backend callback URL
    """
    prod_url = str(settings.oauth_backend_callback_url_prod).format(provider=provider)
    dev_url = str(settings.oauth_backend_callback_url_dev).format(provider=provider)
    
    is_production_host = False
    hostname = None
    if request:
        hostname = request.url.hostname if hasattr(request.url, 'hostname') else None
        if hostname:
            is_production_host = (
                'api.wistx.ai' in hostname or 
                'wistx.ai' in hostname or 
                '.run.app' in hostname or
                hostname.endswith('.a.run.app')
            )
    
    if is_production_host:
        callback_url = prod_url
        if settings.debug:
            logger.critical(
                "CRITICAL MISCONFIGURATION: DEBUG=true but running on production hostname! "
                "Using production backend callback URL despite DEBUG flag. Hostname: %s, DEBUG=%s",
                hostname or 'unknown',
                settings.debug,
            )
        else:
            logger.info(
                "Using PRODUCTION backend callback URL (production hostname detected): %s",
                callback_url,
            )
    elif settings.debug:
        callback_url = dev_url
        logger.warning(
            "Using DEVELOPMENT backend callback URL (DEBUG=true, non-production hostname): %s",
            callback_url,
        )
    else:
        callback_url = prod_url
        logger.info(
            "Using PRODUCTION backend callback URL (DEBUG=false): %s",
            callback_url,
        )
    
    logger.info(
        "Backend OAuth callback URL for %s: %s (hostname=%s, debug=%s). "
        "Ensure this URI is registered in %s OAuth console.",
        provider,
        callback_url,
        hostname or 'unknown',
        settings.debug,
        provider.capitalize(),
    )
    return callback_url


def get_oauth_frontend_redirect_url(provider: str, request: Request | None = None) -> str:
    """Get frontend redirect URL for provider.

    This is where the backend redirects to after processing OAuth callback.
    Prioritizes hostname detection over DEBUG flag to prevent misconfiguration.
    
    Logic:
    1. If request hostname indicates production (api.wistx.ai, wistx.ai, or *.run.app), use production URL
    2. Otherwise, use DEBUG flag to determine dev vs prod
    3. Warns if DEBUG=true on production hostname or DEBUG=false with localhost URLs

    Args:
        provider: OAuth provider name (google, github)
        request: Optional request object to detect production from hostname

    Returns:
        Frontend redirect URL
    """
    prod_url = str(settings.oauth_frontend_redirect_url_prod).format(provider=provider)
    dev_url = str(settings.oauth_frontend_redirect_url_dev).format(provider=provider)
    
    is_production_host = False
    hostname = None
    if request:
        hostname = request.url.hostname if hasattr(request.url, 'hostname') else None
        if hostname:
            is_production_host = (
                'api.wistx.ai' in hostname or 
                'wistx.ai' in hostname or 
                '.run.app' in hostname or
                hostname.endswith('.a.run.app')
            )
    
    if is_production_host:
        frontend_url = prod_url
        
        if settings.debug:
            logger.critical(
                "CRITICAL MISCONFIGURATION: DEBUG=true but running on production hostname! "
                "Using production URL despite DEBUG flag. Hostname: %s, DEBUG=%s",
                hostname or 'unknown',
                settings.debug,
                extra={
                    "event": "oauth_debug_on_production_host",
                    "debug": settings.debug,
                    "hostname": hostname,
                    "provider": provider,
                    "url": frontend_url,
                },
            )
        else:
            logger.info(
                "Using PRODUCTION frontend redirect URL (production hostname detected): %s",
                frontend_url,
                extra={
                    "event": "oauth_using_prod_url_hostname",
                    "debug": settings.debug,
                    "hostname": hostname,
                    "provider": provider,
                    "url": frontend_url,
                },
            )
        
        if "localhost" in frontend_url:
            logger.critical(
                "CRITICAL: Production hostname detected but OAUTH_FRONTEND_REDIRECT_URL_PROD contains localhost! "
                "This will cause OAuth failures. Hostname: %s, URL=%s",
                hostname or 'unknown',
                frontend_url,
                extra={
                    "event": "oauth_localhost_in_production_config",
                    "debug": settings.debug,
                    "hostname": hostname,
                    "frontend_url": frontend_url,
                    "provider": provider,
                    "config_value": str(settings.oauth_frontend_redirect_url_prod),
                },
            )
    elif settings.debug:
        frontend_url = dev_url
        
        logger.warning(
            "Using DEVELOPMENT frontend redirect URL (DEBUG=true, non-production hostname): %s",
            frontend_url,
            extra={
                "event": "oauth_using_dev_url",
                "debug": settings.debug,
                "hostname": hostname,
                    "provider": provider,
                    "url": frontend_url,
                },
            )
    else:
        frontend_url = prod_url
        
        if "localhost" in frontend_url:
            logger.critical(
                "CRITICAL: Production mode (DEBUG=false) but localhost URL in OAUTH_FRONTEND_REDIRECT_URL_PROD! "
                "This will cause OAuth failures. URL=%s, DEBUG=%s, Hostname=%s",
                frontend_url,
                settings.debug,
                hostname or 'unknown',
                extra={
                    "event": "oauth_localhost_in_production_config",
                    "debug": settings.debug,
                    "hostname": hostname,
                    "frontend_url": frontend_url,
                    "provider": provider,
                    "config_value": str(settings.oauth_frontend_redirect_url_prod),
                },
            )
        else:
            logger.info(
                "Using PRODUCTION frontend redirect URL (DEBUG=false): %s",
                frontend_url,
                extra={
                    "event": "oauth_using_prod_url",
                    "debug": settings.debug,
                    "hostname": hostname,
                    "provider": provider,
                    "url": frontend_url,
                },
            )
    
    return frontend_url


def create_oauth_router(provider: str, oauth_client):
    """Create OAuth router with custom frontend redirect.

    Args:
        provider: OAuth provider name (google, github)
        oauth_client: OAuth client instance

    Returns:
        APIRouter with OAuth routes
    """
    router = APIRouter()

    @router.get("/callback")
    async def custom_callback(
        code: str = Query(...),
        state: str = Query(None),
        request: Request = None,
    ) -> RedirectResponse:
        """Custom OAuth callback that redirects to frontend with token.
        
        Handles two flows:
        1. Main OAuth flow (login/signup) - no state or state without encoded user_id
        2. V1 OAuth flow (connecting GitHub to existing user) - state contains encoded user_id
        
        Args:
            code: OAuth authorization code
            state: OAuth state parameter (may contain encoded user_id for v1 flow)
            request: FastAPI request object
        """
        try:
            logger.info(
                "OAuth callback received for %s",
                provider,
                extra={"event": "oauth_callback_start", "provider": provider, "has_state": bool(state)},
            )
            
            if state and provider == "github":
                from api.routers.v1.oauth import decode_user_state
                user_id, _ = decode_user_state(state)
                if user_id:
                    logger.info(
                        "Detected v1 OAuth flow for user %s, routing to v1 handler",
                        user_id,
                        extra={"event": "oauth_v1_flow_detected", "provider": provider, "user_id": str(user_id)},
                    )
                    from api.routers.v1.oauth import github_oauth_callback as v1_callback
                    return await v1_callback(code=code, state=state)
            
            redirect_uri = get_oauth_backend_callback_url(provider, request)
            logger.debug("Getting access token with redirect_uri: %s", redirect_uri)
            
            access_token_response = await oauth_client.get_access_token(code, redirect_uri)
            logger.debug("Access token received for %s", provider)
            
            if provider == "google":
                try:
                    user_info = await oauth_client.get_id_email(access_token_response["access_token"])
                except Exception as google_error:
                    logger.warning("Google People API failed, trying userinfo endpoint: %s", google_error)
                    async with httpx.AsyncClient() as client:
                        response = await client.get(
                            "https://www.googleapis.com/oauth2/v2/userinfo",
                            headers={"Authorization": f"Bearer {access_token_response['access_token']}"},
                        )
                        response.raise_for_status()
                        user_data = response.json()
                        user_id = user_data.get("id")
                        user_email = user_data.get("email")
                        if not user_id or not user_email:
                            raise ValueError("Missing id or email in Google userinfo response") from google_error
                        user_info = (user_id, user_email)
            else:
                user_info = await oauth_client.get_id_email(access_token_response["access_token"])
            
            logger.debug("User info received: %s", user_info)
            
            if isinstance(user_info, tuple) and len(user_info) == 2:
                user_id, user_email = user_info
            else:
                logger.error("Unexpected user_info format from %s: %s", provider, type(user_info))
                raise ValueError(f"Unexpected user_info format: {user_info}")

            await async_mongodb_adapter.connect()
            db = async_mongodb_adapter.get_database()
            collection = db.users
            user_db = MongoDBUserDatabase(collection)
            user_manager = UserManager(user_db)

            expires_at = None
            if "expires_in" in access_token_response:
                expires_at = int(time.time()) + access_token_response["expires_in"]

            account_id_str = str(user_id)
            logger.debug("Calling oauth_callback for %s with account_id: %s (type: %s), email: %s", provider, account_id_str, type(user_id).__name__, user_email)
            
            existing_user_by_email = await user_db.get_by_email(user_email)
            existing_user_by_oauth = await user_db.get_by_oauth_account(provider, account_id_str)
            
            if existing_user_by_email:
                user_dict = await user_db.collection.find_one({"email": user_email})
                oauth_accounts = user_dict.get("oauth_accounts", []) if user_dict else []
                stored_account_ids = [
                    str(acc.get("account_id", "")) 
                    for acc in oauth_accounts 
                    if acc.get("oauth_name") == provider
                ]
                logger.info(
                    "OAuth account lookup results",
                    extra={
                        "provider": provider,
                        "account_id_from_google": account_id_str,
                        "account_id_type": type(user_id).__name__,
                        "email": user_email,
                        "existing_by_email": str(existing_user_by_email.id) if existing_user_by_email else None,
                        "existing_by_oauth": str(existing_user_by_oauth.id) if existing_user_by_oauth else None,
                        "stored_account_ids": stored_account_ids,
                        "account_id_match": account_id_str in stored_account_ids,
                    },
                )
            else:
                logger.info(
                    "OAuth account lookup results",
                    extra={
                        "provider": provider,
                        "account_id": account_id_str,
                        "email": user_email,
                        "existing_by_email": None,
                        "existing_by_oauth": str(existing_user_by_oauth.id) if existing_user_by_oauth else None,
                    },
                )
            
            if existing_user_by_email and not existing_user_by_oauth:
                logger.info(
                    "User exists by email but not by OAuth account - merging OAuth account to existing user",
                    extra={
                        "existing_user_id": str(existing_user_by_email.id),
                        "provider": provider,
                        "account_id": str(user_id),
                        "email": user_email,
                    },
                )
                
                oauth_account = {
                    "oauth_name": provider,
                    "account_id": account_id_str,
                    "account_email": user_email,
                    "access_token": access_token_response["access_token"],
                    "expires_at": expires_at,
                    "refresh_token": access_token_response.get("refresh_token"),
                }
                
                existing_user_by_email = await user_db.add_oauth_account(existing_user_by_email, oauth_account)
                user = existing_user_by_email
                logger.info(
                    "OAuth account merged successfully to existing user",
                    extra={
                        "user_id": str(user.id),
                        "email": user.email,
                        "provider": provider,
                    },
                )
            else:
                if not existing_user_by_email and not existing_user_by_oauth:
                    from api.auth.admin import is_internal_admin_domain, can_signup_as_admin
                    
                    invite_token = None
                    if request:
                        invite_token = request.query_params.get("invite_token")
                    
                    can_signup, admin_error = can_signup_as_admin(user_email)
                    
                    if is_internal_admin_domain(user_email):
                        if not can_signup:
                            logger.warning(
                                "Admin signup blocked for %s: %s",
                                user_email,
                                admin_error,
                                extra={
                                    "event": "admin_signup_blocked",
                                    "email": user_email,
                                    "provider": provider,
                                },
                            )
                            frontend_url = get_oauth_frontend_redirect_url(provider, request)
                            error_url = f"{frontend_url}?error=admin_signup_blocked&message={admin_error.replace(' ', '%20') if admin_error else 'Admin%20signup%20requires%20an%20invitation.'}"
                            return RedirectResponse(url=error_url)
                    else:
                        from api.services.user_invitation_service import user_invitation_service
                        pending_invitation = user_invitation_service.get_pending_invitation_by_email(user_email)
                        
                        if not invite_token and not pending_invitation:
                            logger.warning(
                                "Signup blocked for %s: No invitation found",
                                user_email,
                                extra={
                                    "event": "signup_blocked_no_invitation",
                                    "email": user_email,
                                    "provider": provider,
                                },
                            )
                            frontend_url = get_oauth_frontend_redirect_url(provider, request)
                            error_url = f"{frontend_url}?error=invitation_required&message=Signup%20requires%20an%20invitation.%20Please%20contact%20Founder%20at%20hi@wistx.ai%20or%20use%20your%20invitation%20link."
                            return RedirectResponse(url=error_url)
                
                try:
                    user = await user_manager.oauth_callback(
                        oauth_name=provider,
                        access_token=access_token_response["access_token"],
                        account_id=account_id_str,
                        account_email=user_email,
                        expires_at=expires_at,
                        refresh_token=access_token_response.get("refresh_token"),
                        request=request,
                    )
                except ValueError as e:
                    error_msg = str(e)
                    if "invitation" in error_msg.lower() or "admin" in error_msg.lower():
                        logger.warning(
                            "Admin signup blocked for %s: %s",
                            user_email,
                            error_msg,
                        )
                        frontend_url = get_oauth_frontend_redirect_url(provider, request)
                        error_url = f"{frontend_url}?error=admin_signup_blocked&message={error_msg.replace(' ', '%20')}"
                        return RedirectResponse(url=error_url)
                    raise
            logger.info(
                "SECURITY: User created/updated via OAuth: %s (email: %s)",
                user.id,
                user.email,
                extra={
                    "event": "oauth_user_created",
                    "provider": provider,
                    "user_id": str(user.id),
                    "email": user_email,
                },
            )

            from api.auth.admin import is_internal_admin_domain
            from api.database.mongodb import mongodb_manager
            from api.services.user_invitation_service import user_invitation_service
            from api.services.organization_service import organization_service
            from bson import ObjectId
            from datetime import datetime

            db = mongodb_manager.get_database()
            user_doc = db.users.find_one({"_id": ObjectId(str(user.id))})

            if user_doc and user_doc.get("invitation_token"):
                try:
                    await user_invitation_service.accept_invitation(
                        token=user_doc["invitation_token"],
                        user_id=str(user.id),
                    )
                    logger.info(
                        "User invitation accepted during OAuth for user %s",
                        user.id,
                    )
                except Exception as invite_error:
                    logger.warning(
                        "Failed to accept user invitation during OAuth: %s",
                        invite_error,
                    )

            pending_org_invitations = list(
                db.organization_invitations.find(
                    {
                        "email": {"$regex": f"^{user_email}$", "$options": "i"},
                        "status": "pending",
                    }
                )
            )

            if pending_org_invitations:
                for pending_invitation in pending_org_invitations:
                    expires_at = pending_invitation.get("expires_at")
                    if expires_at and expires_at < datetime.utcnow():
                        continue

                    invitation_token = pending_invitation.get("token")
                    if invitation_token:
                        try:
                            await organization_service.accept_invitation(
                                token=invitation_token,
                                user_id=str(user.id),
                                request=request,
                            )
                            logger.info(
                                "Organization invitation auto-accepted during OAuth for user %s (org: %s)",
                                user.id,
                                pending_invitation.get("organization_id"),
                            )
                            user_doc = db.users.find_one({"_id": ObjectId(str(user.id))})
                            break
                        except HTTPException as org_invite_error:
                            if org_invite_error.status_code == 403:
                                logger.debug(
                                    "Organization invitation email mismatch during OAuth (expected): %s",
                                    org_invite_error.detail,
                                )
                            else:
                                logger.warning(
                                    "Failed to auto-accept organization invitation during OAuth: %s",
                                    org_invite_error,
                                )
                        except Exception as org_invite_error:
                            logger.warning(
                                "Failed to auto-accept organization invitation during OAuth: %s",
                                org_invite_error,
                            )

            if is_internal_admin_domain(user_email):
                if user_doc:
                    update_fields = {}
                    if user_doc.get("plan") != "enterprise":
                        update_fields["plan"] = "enterprise"
                        logger.info(
                            "Updating plan to enterprise for internal admin: %s",
                            user_email,
                        )
                    if not user_doc.get("is_super_admin") and not user_doc.get("admin_role"):
                        if not db.users.find_one({"is_super_admin": True}):
                            update_fields["is_super_admin"] = True
                            update_fields["admin_role"] = "super_admin"
                            update_fields["admin_status"] = "active"
                            update_fields["admin_permissions"] = ["*"]
                            logger.info(
                                "Promoting to super admin (first admin): %s",
                                user_email,
                            )
                    
                    if update_fields:
                        update_fields["updated_at"] = datetime.utcnow()
                        db.users.update_one(
                            {"_id": ObjectId(str(user.id))},
                            {"$set": update_fields},
                        )
                        user_dict = user.to_dict()
                        user_dict.update(update_fields)
                        from api.auth.users import User
                        user = User.from_dict(user_dict)
                        logger.info(
                            "User updated with new fields: %s",
                            list(update_fields.keys()),
                        )

            jwt_strategy = jwt_authentication.get_strategy()
            jwt_token = await jwt_strategy.write_token(user)

            if not jwt_token or not isinstance(jwt_token, str):
                logger.error("Invalid token generated for OAuth user: %s", user.id)
                raise ValueError("Failed to generate authentication token")
            
            import jwt
            from datetime import datetime
            try:
                decoded = jwt.decode(jwt_token, options={"verify_signature": False})
                exp_timestamp = decoded.get("exp")
                if exp_timestamp:
                    exp_time = datetime.fromtimestamp(exp_timestamp)
                    now = datetime.utcnow()
                    lifetime_minutes = (exp_time - now).total_seconds() / 60
                    logger.info(
                        "JWT token created: exp=%s (UTC), lifetime_minutes=%.1f, configured_expire_minutes=%d",
                        exp_time,
                        lifetime_minutes,
                        settings.access_token_expire_minutes,
                    )
            except Exception as decode_error:
                logger.debug("Could not decode JWT for expiration logging: %s", decode_error)

            from api.models.audit_log import AuditEventType, AuditLogSeverity
            from api.services.audit_log_service import audit_log_service

            ip_address = request.client.host if request.client else None
            user_agent = request.headers.get("user-agent") if request else None

            from datetime import datetime
            is_new_user = not user.is_verified
            
            audit_log_service.log_event(
                event_type=AuditEventType.AUTHENTICATION_SUCCESS,
                severity=AuditLogSeverity.LOW,
                message=f"User {user.id} authenticated via OAuth ({provider})",
                success=True,
                user_id=str(user.id),
                organization_id=str(user.organization_id) if user.organization_id else None,
                ip_address=ip_address,
                user_agent=user_agent,
                endpoint=f"/oauth/{provider}/callback",
                method="GET",
                details={
                    "auth_method": "oauth",
                    "provider": provider,
                    "is_signup": is_new_user,
                    "token_size": len(jwt_token),
                },
                compliance_tags=["PCI-DSS-10", "SOC2"],
            )

            frontend_url = get_oauth_frontend_redirect_url(provider, request)
            
            logger.info(
                "OAuth callback redirecting to frontend: %s (debug=%s, provider=%s)",
                frontend_url,
                settings.debug,
                provider,
                extra={
                    "event": "oauth_redirect_url_determined",
                    "frontend_url": frontend_url,
                    "debug": settings.debug,
                    "provider": provider,
                    "oauth_frontend_redirect_url_dev": str(settings.oauth_frontend_redirect_url_dev),
                    "oauth_frontend_redirect_url_prod": str(settings.oauth_frontend_redirect_url_prod),
                },
            )
            
            from api.utils.cookies import set_auth_cookie_safe
            
            cookie_success = False
            if settings.debug:
                sync_url = f"{frontend_url}?token={quote(jwt_token)}"
                logger.info(
                    "Development mode: Redirecting to frontend with token for sync (user: %s)",
                    user.id,
                )
                response = RedirectResponse(url=sync_url)
                cookie_success = True
            else:
                response = RedirectResponse(url=frontend_url)
                cookie_success, _ = set_auth_cookie_safe(
                    response, jwt_token, fallback_to_header=False
                )
                
                if cookie_success:
                    logger.info(
                        "Cookie set successfully for OAuth callback (user: %s)",
                        user.id,
                    )
                else:
                    logger.error(
                        "Failed to set cookie for OAuth callback (user: %s). "
                        "User will need to authenticate again.",
                        user.id,
                    )
                    error_url = f"{frontend_url}?error=token_failed&message=Cookie%20authentication%20failed.%20Please%20try%20again."
                    response = RedirectResponse(url=error_url)

            logger.info(
                "OAuth callback successful for %s, redirecting to frontend",
                provider,
                extra={
                    "event": "oauth_callback_success",
                    "provider": provider,
                    "user_id": str(user.id),
                    "cookie_set": cookie_success,
                    "token_size": len(jwt_token),
                },
            )
            
            if not cookie_success:
                logger.warning(
                    "Cookie not set for OAuth callback - requests will fail without authentication",
                    extra={
                        "provider": provider,
                        "user_id": str(user.id),
                    },
                )
            
            return response
        except Exception as e:
            logger.error(
                "SECURITY: OAuth callback error for %s: %s",
                provider,
                e,
                exc_info=True,
                extra={"event": "oauth_callback_error", "provider": provider},
            )
            frontend_url = get_oauth_frontend_redirect_url(provider, request)
            error_message = quote(str(e))
            error_url = f"{frontend_url}?error=oauth_failed&message={error_message}"
            logger.error("Redirecting to frontend with error: %s", error_url)
            return RedirectResponse(url=error_url)

    @router.get("/authorize")
    async def oauth_authorize(request: Request) -> RedirectResponse:
        """Get OAuth authorization URL."""
        redirect_uri = get_oauth_backend_callback_url(provider, request)
        authorization_url = await oauth_client.get_authorization_url(
            redirect_uri=redirect_uri,
            state=None,
        )
        return RedirectResponse(url=authorization_url)

    return router


google_oauth_router = create_oauth_router("google", google_oauth_client)
github_oauth_router = create_oauth_router("github", github_oauth_client)
