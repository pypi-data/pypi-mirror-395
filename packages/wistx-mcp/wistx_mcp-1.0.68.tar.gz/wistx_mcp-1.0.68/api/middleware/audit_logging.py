"""Security audit logging middleware."""

import asyncio
import logging
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from api.models.audit_log import AuditEventType, AuditLogSeverity
from api.services.audit_log_service import audit_log_service
from api.services.security_monitor_service import security_monitor_service
from api.utils.client_ip import get_real_client_ip

logger = logging.getLogger(__name__)


class AuditLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for security audit logging."""

    def __init__(self, app):
        """Initialize audit logging middleware.

        Args:
            app: ASGI application
        """
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and log security events.

        Args:
            request: FastAPI request object
            call_next: Next middleware/handler

        Returns:
            Response object
        """
        user_info = getattr(request.state, "user_info", None)
        user_id = user_info.get("user_id") if user_info else None
        api_key_id = user_info.get("api_key_id") if user_info else None
        organization_id = user_info.get("organization_id") if user_info else None

        ip_address = get_real_client_ip(request)
        user_agent = request.headers.get("user-agent")
        request_id = getattr(request.state, "request_id", None)

        if (
            request.url.path.startswith("/health")
            or request.url.path.startswith("/docs")
            or request.url.path.startswith("/openapi.json")
            or request.url.path.startswith("/redoc")
        ):
            return await call_next(request)

        response = await call_next(request)

        if user_info:
            status_code = response.status_code

            if status_code == 401:
                audit_log_service.log_event(
                    event_type=AuditEventType.AUTHENTICATION_FAILURE,
                    severity=AuditLogSeverity.MEDIUM,
                    message=f"Authentication failed for endpoint: {request.url.path}",
                    success=False,
                    user_id=user_id,
                    api_key_id=api_key_id,
                    organization_id=organization_id,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    request_id=request_id,
                    endpoint=request.url.path,
                    method=request.method,
                    status_code=status_code,
                    details={
                        "reason": "Invalid or missing credentials",
                        "path": request.url.path,
                    },
                    compliance_tags=["PCI-DSS-10", "SOC2"],
                )
                # Track for suspicious activity detection (OWASP brute force)
                try:
                    await security_monitor_service.track_failed_auth(
                        ip_address=ip_address,
                        user_id=user_id,
                        user_agent=user_agent,
                    )
                except Exception as e:
                    logger.debug("Security monitor tracking failed: %s", e)

            elif status_code == 403:
                audit_log_service.log_event(
                    event_type=AuditEventType.AUTHORIZATION_DENIED,
                    severity=AuditLogSeverity.HIGH,
                    message=f"Authorization denied for user {user_id} on endpoint: {request.url.path}",
                    success=False,
                    user_id=user_id,
                    api_key_id=api_key_id,
                    organization_id=organization_id,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    request_id=request_id,
                    endpoint=request.url.path,
                    method=request.method,
                    status_code=status_code,
                    details={
                        "reason": "Insufficient permissions",
                        "path": request.url.path,
                    },
                    compliance_tags=["PCI-DSS-10", "SOC2"],
                )
                # Track for suspicious activity detection (OWASP authorization probing)
                try:
                    await security_monitor_service.track_forbidden(
                        ip_address=ip_address,
                        endpoint=request.url.path,
                        user_id=user_id,
                        user_agent=user_agent,
                    )
                except Exception as e:
                    logger.debug("Security monitor tracking failed: %s", e)

            elif status_code == 404:
                # Track for suspicious activity detection (OWASP API scanning)
                try:
                    await security_monitor_service.track_not_found(
                        ip_address=ip_address,
                        endpoint=request.url.path,
                        user_agent=user_agent,
                    )
                except Exception as e:
                    logger.debug("Security monitor tracking failed: %s", e)

            elif status_code >= 200 and status_code < 300:
                sensitive_modification_endpoints = [
                    "/v1/compliance",
                    "/v1/pricing",
                    "/v1/users",
                    "/v1/billing",
                    "/v1/budget",
                    "/v1/api-keys",
                    "/v1/auth",
                    "/v1/oauth",
                    "/v1/reports",
                    "/v1/indexing",
                ]

                if request.method == "DELETE":
                    if any(request.url.path.startswith(ep) for ep in sensitive_modification_endpoints):
                        audit_log_service.log_event(
                            event_type=AuditEventType.DATA_DELETED,
                            severity=AuditLogSeverity.HIGH,
                            message=f"Sensitive data deleted: {request.url.path}",
                            success=True,
                            user_id=user_id,
                            api_key_id=api_key_id,
                            organization_id=organization_id,
                            ip_address=ip_address,
                            user_agent=user_agent,
                            request_id=request_id,
                            endpoint=request.url.path,
                            method=request.method,
                            status_code=status_code,
                            details={
                                "operation": "delete",
                                "path": request.url.path,
                                "data_type": "sensitive",
                            },
                            compliance_tags=["PCI-DSS-10", "SOC2", "GDPR"],
                        )
                elif request.method in ("POST", "PUT", "PATCH"):
                    if any(request.url.path.startswith(ep) for ep in sensitive_modification_endpoints):
                        audit_log_service.log_event(
                            event_type=AuditEventType.DATA_MODIFIED,
                            severity=AuditLogSeverity.MEDIUM,
                            message=f"Sensitive data modified via {request.method} {request.url.path}",
                            success=True,
                            user_id=user_id,
                            api_key_id=api_key_id,
                            organization_id=organization_id,
                            ip_address=ip_address,
                            user_agent=user_agent,
                            request_id=request_id,
                            endpoint=request.url.path,
                            method=request.method,
                            status_code=status_code,
                            details={
                                "operation": request.method,
                                "path": request.url.path,
                                "data_type": "sensitive",
                            },
                            compliance_tags=["PCI-DSS-10", "SOC2"],
                        )
                elif request.method == "GET":
                    sensitive_access_endpoints = [
                        "/v1/compliance",
                        "/v1/pricing",
                        "/v1/code-examples",
                        "/v1/knowledge",
                        "/v1/users",
                        "/v1/billing",
                        "/v1/budget",
                        "/v1/api-keys",
                        "/v1/audit-logs",
                        "/v1/indexing",
                    ]
                    if any(request.url.path.startswith(ep) for ep in sensitive_access_endpoints):
                        audit_log_service.log_event(
                            event_type=AuditEventType.DATA_ACCESSED,
                            severity=AuditLogSeverity.LOW,
                            message=f"Sensitive data accessed: {request.url.path}",
                            success=True,
                            user_id=user_id,
                            api_key_id=api_key_id,
                            organization_id=organization_id,
                            ip_address=ip_address,
                            user_agent=user_agent,
                            request_id=request_id,
                            endpoint=request.url.path,
                            method=request.method,
                            status_code=status_code,
                            details={
                                "data_type": "sensitive",
                                "path": request.url.path,
                            },
                            compliance_tags=["PCI-DSS-10", "HIPAA", "SOC2"],
                        )
        else:
            # Track unauthenticated suspicious activity (API scanning, probing)
            status_code = response.status_code
            if status_code == 404:
                try:
                    await security_monitor_service.track_not_found(
                        ip_address=ip_address,
                        endpoint=request.url.path,
                        user_agent=user_agent,
                    )
                except Exception as e:
                    logger.debug("Security monitor tracking failed: %s", e)
            elif status_code == 403:
                try:
                    await asyncio.wait_for(
                        security_monitor_service.track_forbidden(
                            ip_address=ip_address,
                            endpoint=request.url.path,
                            user_agent=user_agent,
                        ),
                        timeout=0.5,
                    )
                except asyncio.TimeoutError:
                    logger.debug("Security monitor tracking timed out (non-critical)")
                except Exception as e:
                    logger.debug("Security monitor tracking failed (non-critical): %s", e)

        return response

