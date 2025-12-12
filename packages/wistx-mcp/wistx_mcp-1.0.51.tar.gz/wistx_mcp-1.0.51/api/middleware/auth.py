"""Authentication middleware for FastAPI.

Extracts and validates authentication tokens (API keys or JWT) from requests
and sets user information in request.state for use by route handlers.
"""

import logging
from typing import Callable

from fastapi import Request, Response, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware

from api.auth.api_keys import get_user_from_api_key
from api.auth.users import jwt_authentication
from api.auth.admin import is_internal_admin

logger = logging.getLogger(__name__)


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Authentication middleware that extracts and validates API keys or JWT tokens.

    Sets user information in request.state.user_info for use by route handlers.
    Does not enforce authentication - routes can use get_current_user dependency
    to require authentication.
    """

    def __init__(self, app, enforce_auth: bool = False):
        """Initialize authentication middleware.

        Args:
            app: ASGI application
            enforce_auth: If True, require authentication for all routes (except excluded)
        """
        super().__init__(app)
        self.enforce_auth = enforce_auth
        self.excluded_paths = {
            "/health",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/auth/",
        }

    def _is_excluded_path(self, path: str) -> bool:
        """Check if path is excluded from authentication.

        Args:
            path: Request path

        Returns:
            True if path is excluded, False otherwise
        """
        return any(path.startswith(excluded) for excluded in self.excluded_paths)

    async def _extract_api_key_user(self, authorization: str) -> dict | None:
        """Extract user info from API key.

        Args:
            authorization: Authorization header value

        Returns:
            User info dictionary or None if invalid
        """
        if not authorization or not authorization.startswith("Bearer "):
            return None

        api_key_value = authorization.replace("Bearer ", "").strip()
        if not api_key_value:
            return None

        try:
            user_info = await get_user_from_api_key(api_key_value)
            return user_info
        except (ValueError, RuntimeError, ConnectionError) as e:
            logger.warning("Failed to verify API key: %s", e)
            return None
        except Exception as e:
            logger.warning("Unexpected error verifying API key: %s", e)
            return None

    async def _extract_jwt_user(
        self, authorization: str | None = None, token: str | None = None
    ) -> dict | None:
        """Extract user info from JWT token.

        Args:
            authorization: Authorization header value (optional)
            token: Direct token string (optional, takes precedence)

        Returns:
            User info dictionary or None if invalid
        """
        if token:
            jwt_token = token
        elif authorization and authorization.startswith("Bearer "):
            jwt_token = authorization.replace("Bearer ", "").strip()
        else:
            return None

        if not jwt_token:
            return None

        try:
            from api.database.async_mongodb import async_mongodb_adapter
            from api.auth.database import MongoDBUserDatabase
            from api.auth.users import UserManager

            logger.info("Connecting to async MongoDB adapter for JWT validation")
            try:
                await async_mongodb_adapter.connect()
                logger.info("Async MongoDB adapter connected successfully")
            except Exception as conn_error:
                logger.error(
                    "Failed to connect to async MongoDB adapter for JWT validation: %s (type: %s)",
                    str(conn_error),
                    type(conn_error).__name__,
                    exc_info=True,
                )
                raise
            
            db = async_mongodb_adapter.get_database()
            collection = db.users
            user_db = MongoDBUserDatabase(collection)
            user_manager = UserManager(user_db)

            strategy = jwt_authentication.get_strategy()
            
            import jwt
            from datetime import datetime
            try:
                decoded = jwt.decode(jwt_token, options={"verify_signature": False})
                exp_timestamp = decoded.get("exp")
                if exp_timestamp:
                    exp_time = datetime.fromtimestamp(exp_timestamp)
                    now = datetime.utcnow()
                    if now > exp_time:
                        logger.warning(
                            "JWT token expired: exp=%s (UTC), now=%s (UTC), expired_by=%s",
                            exp_time,
                            now,
                            now - exp_time,
                        )
                    else:
                        logger.info(
                            "JWT token not expired: exp=%s (UTC), now=%s (UTC), expires_in=%s",
                            exp_time,
                            now,
                            exp_time - now,
                        )
            except Exception as decode_error:
                logger.warning("Could not decode JWT for expiration check: %s", decode_error)
            
            logger.info("Calling strategy.read_token() for JWT validation")
            try:
                user = await strategy.read_token(jwt_token, user_manager)
                logger.info("strategy.read_token() completed: user=%s", "found" if user else "None")
            except Exception as read_error:
                logger.error(
                    "strategy.read_token() raised exception: %s (type: %s)",
                    str(read_error),
                    type(read_error).__name__,
                    exc_info=True,
                )
                raise
            if user:
                from api.database.mongodb import mongodb_manager
                from api.auth.admin import get_admin_info
                from bson import ObjectId

                email = getattr(user, "email", "")
                db = mongodb_manager.get_database()
                user_doc = db.users.find_one({"_id": ObjectId(str(user.id))})
                
                admin_info = {}
                if user_doc:
                    admin_info = get_admin_info(user_doc)
                else:
                    from api.auth.admin import is_internal_admin_domain
                    admin_info = {
                        "is_admin": is_internal_admin_domain(email),
                        "admin_role": None,
                        "admin_permissions": [],
                        "is_super_admin": False,
                        "admin_status": None,
                    }

                organization_id = None
                organization_role = None
                if user_doc:
                    organization_id = str(user_doc.get("organization_id")) if user_doc.get("organization_id") else None
                    if organization_id:
                        member = db.organization_members.find_one(
                            {
                                "organization_id": ObjectId(organization_id),
                                "user_id": ObjectId(str(user.id)),
                                "status": "active",
                            }
                        )
                        if member:
                            organization_role = member.get("role")

                return {
                    "user_id": str(user.id),
                    "email": email,
                    "plan": getattr(user, "plan", "professional"),
                    "rate_limits": getattr(user, "limits", {}),
                    "organization_id": organization_id,
                    "organization_role": organization_role,
                    **admin_info,
                }
            else:
                logger.error(
                    "JWT token validation returned None (token may be expired or invalid). Token length: %d, first 20 chars: %s",
                    len(jwt_token),
                    jwt_token[:20] if len(jwt_token) > 20 else jwt_token,
                )
        except ValueError as e:
            logger.error("JWT token validation failed (ValueError): %s", e, exc_info=True)
        except RuntimeError as e:
            logger.error("JWT token validation failed (RuntimeError): %s", e, exc_info=True)
        except AttributeError as e:
            logger.error("JWT token validation failed (AttributeError): %s", e, exc_info=True)
        except Exception as e:
            logger.error("Unexpected error validating JWT token: %s", e, exc_info=True)

        return None

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and extract authentication.

        Args:
            request: FastAPI request object
            call_next: Next middleware/handler

        Returns:
            Response object

        Raises:
            HTTPException: If authentication is required but missing/invalid
        """
        if request.method == "OPTIONS":
            return await call_next(request)
        
        if self._is_excluded_path(request.url.path):
            return await call_next(request)

        authorization = request.headers.get("Authorization", "") or request.headers.get("authorization", "")
        cookie_token = request.cookies.get("auth_token")

        all_header_names = list(request.headers.keys())
        auth_header_present = "Authorization" in all_header_names or "authorization" in [h.lower() for h in all_header_names]

        logger.debug(
            "Auth middleware check: has_authorization_header=%s, has_cookie=%s, path=%s, auth_header_value_length=%d, all_headers=%s",
            bool(authorization),
            bool(cookie_token),
            request.url.path,
            len(authorization) if authorization else 0,
            ", ".join(all_header_names[:10]),
        )

        user_info = None

        if cookie_token:
            logger.info(
                "Cookie token detected. Starting JWT validation. Path: %s, token_length: %d",
                request.url.path,
                len(cookie_token) if cookie_token else 0,
            )
            try:
                logger.info(
                    "Attempting cookie-based JWT validation. Path: %s, token_length: %d, token_preview: %s",
                    request.url.path,
                    len(cookie_token) if cookie_token else 0,
                    cookie_token[:50] if cookie_token and len(cookie_token) > 50 else cookie_token,
                )
                user_info = await self._extract_jwt_user(token=cookie_token)
                logger.info(
                    "_extract_jwt_user returned: %s",
                    "user_info" if user_info else "None",
                )
                if user_info:
                    logger.info(
                        "Authenticated user via cookie: %s",
                        user_info.get("user_id"),
                    )
                else:
                    import jwt
                    from datetime import datetime
                    try:
                        decoded = jwt.decode(cookie_token, options={"verify_signature": False})
                        exp_timestamp = decoded.get("exp")
                        if exp_timestamp:
                            exp_time = datetime.fromtimestamp(exp_timestamp)
                            now = datetime.utcnow()
                            if now > exp_time:
                                logger.warning(
                                    "Cookie token expired: exp=%s (UTC), now=%s (UTC), expired_by=%s. Path: %s",
                                    exp_time,
                                    now,
                                    now - exp_time,
                                    request.url.path,
                                )
                            else:
                                logger.warning(
                                    "Cookie token present but JWT validation failed (returned None). Token not expired: exp=%s (UTC), now=%s (UTC), expires_in=%s. Path: %s, token_length: %d",
                                    exp_time,
                                    now,
                                    exp_time - now,
                                    request.url.path,
                                    len(cookie_token) if cookie_token else 0,
                                )
                        else:
                            logger.warning(
                                "Cookie token present but JWT validation failed (returned None). Token missing 'exp' claim. Path: %s, token_length: %d, token_preview: %s",
                                request.url.path,
                                len(cookie_token) if cookie_token else 0,
                                cookie_token[:50] if cookie_token and len(cookie_token) > 50 else cookie_token,
                            )
                    except Exception as decode_error:
                        logger.warning(
                            "Cookie token present but JWT validation failed (returned None). Could not decode token for expiration check: %s. Path: %s, token_length: %d",
                            decode_error,
                            request.url.path,
                            len(cookie_token) if cookie_token else 0,
                        )
            except Exception as e:
                logger.error(
                    "Cookie auth failed with exception, falling back to header. Path: %s, error_type: %s, error: %s",
                    request.url.path,
                    type(e).__name__,
                    str(e),
                    exc_info=True,
                )

        if not user_info and authorization:
            logger.debug(
                "Attempting header-based auth: authorization_header_length=%d",
                len(authorization),
            )
            user_info = await self._extract_api_key_user(authorization)
            if not user_info:
                user_info = await self._extract_jwt_user(authorization=authorization)
                if user_info:
                    logger.debug(
                        "Authenticated user via Authorization header: %s",
                        user_info.get("user_id"),
                    )
                else:
                    logger.warning(
                        "JWT validation failed for Authorization header: path=%s, header_length=%d",
                        request.url.path,
                        len(authorization),
                    )

        if user_info:
            request.state.user_info = user_info
            logger.info("Authenticated user: %s", user_info.get("user_id"))
        else:
            logger.warning(
                "No user_info set by middleware. Path: %s, has_cookie: %s, has_authorization: %s, enforce_auth: %s",
                request.url.path,
                bool(cookie_token),
                bool(authorization),
                self.enforce_auth,
            )
            if self.enforce_auth:
                from api.models.audit_log import AuditEventType, AuditLogSeverity
                from api.services.audit_log_service import audit_log_service
                from api.services.security_monitor_service import security_monitor_service

                ip_address = request.client.host if request.client else None
                user_agent = request.headers.get("user-agent")
                request_id = getattr(request.state, "request_id", None)

                audit_log_service.log_event(
                    event_type=AuditEventType.AUTHENTICATION_FAILURE,
                    severity=AuditLogSeverity.MEDIUM,
                    message="Authentication required but not provided",
                    success=False,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    request_id=request_id,
                    endpoint=request.url.path,
                    method=request.method,
                    details={
                        "reason": "Missing authentication",
                        "path": request.url.path,
                    },
                    compliance_tags=["PCI-DSS-10", "SOC2"],
                )

                # Track failed auth for suspicious activity detection (OWASP)
                try:
                    await security_monitor_service.track_failed_auth(
                        ip_address=ip_address,
                        user_agent=user_agent,
                    )
                except Exception as e:
                    logger.debug("Security monitor tracking failed: %s", e)

                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        response = await call_next(request)

        # Note: Removed redundant cookie re-sending on every request
        # Cookies are only set during login/sync endpoints, not on every authenticated request
        # This reduces overhead and prevents potential cookie conflicts

        return response
