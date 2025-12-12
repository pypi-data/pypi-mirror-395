"""Admin security endpoints."""

import logging
from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.dependencies.auth import require_admin, require_permission_factory
from api.models.admin.security import (
    APIKeyListQuery,
    APIKeyListResponse,
    APIKeyRevokeRequest,
    IPMonitoringResponse,
    SecurityEventsQuery,
    SecurityEventsSummaryResponse,
)
from api.models.audit_log import AuditLogSeverity
from api.services.admin.security_service import admin_security_service
from api.services.audit_log_service import audit_log_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/security", tags=["admin"])


@router.get("/events", summary="Get security events summary")
async def get_security_events_summary(
    severity: AuditLogSeverity | None = Query(None, description="Filter by severity"),
    start_date: datetime | None = Query(None, description="Start date filter"),
    end_date: datetime | None = Query(None, description="End date filter"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of results"),
    offset: int = Query(default=0, ge=0, description="Offset for pagination"),
    current_user: dict[str, Any] = Depends(require_admin),
) -> SecurityEventsSummaryResponse:
    """Get security events summary.

    Args:
        severity: Severity filter
        start_date: Start date filter
        end_date: End date filter
        limit: Result limit
        offset: Result offset
        current_user: Current admin user

    Returns:
        Security events summary response
    """
    query = SecurityEventsQuery(
        severity=severity,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset,
    )

    try:
        return await admin_security_service.get_security_events_summary(query)
    except Exception as e:
        logger.error("Error getting security events summary: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get security events summary",
        ) from e


@router.get("/audit-logs", summary="Get audit logs")
async def get_audit_logs(
    event_types: list[str] | None = Query(None, description="Filter by event types"),
    severity: AuditLogSeverity | None = Query(None, description="Filter by severity"),
    user_id: str | None = Query(None, description="Filter by user ID"),
    api_key_id: str | None = Query(None, description="Filter by API key ID"),
    organization_id: str | None = Query(None, description="Filter by organization ID"),
    ip_address: str | None = Query(None, description="Filter by IP address"),
    start_date: datetime | None = Query(None, description="Start date filter"),
    end_date: datetime | None = Query(None, description="End date filter"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of results"),
    offset: int = Query(default=0, ge=0, description="Offset for pagination"),
    current_user: dict[str, Any] = Depends(require_permission_factory("security.audit")),
) -> dict[str, Any]:
    """Get audit logs with filters.

    Args:
        event_types: Event types filter
        severity: Severity filter
        user_id: User ID filter
        api_key_id: API key ID filter
        organization_id: Organization ID filter
        ip_address: IP address filter
        start_date: Start date filter
        end_date: End date filter
        limit: Result limit
        offset: Result offset
        current_user: Current admin user

    Returns:
        Audit logs response
    """
    from api.models.audit_log import AuditEventType, AuditLogQuery

    event_type_enums = None
    if event_types:
        event_type_enums = [AuditEventType(et) for et in event_types]

    query = AuditLogQuery(
        event_types=event_type_enums,
        severity=severity,
        user_id=user_id,
        api_key_id=api_key_id,
        organization_id=organization_id,
        ip_address=ip_address,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset,
    )

    try:
        response = audit_log_service.query_logs(query)
        return {
            "logs": [log.model_dump() for log in response.logs],
            "total": response.total,
            "limit": response.limit,
            "offset": response.offset,
        }
    except Exception as e:
        logger.error("Error getting audit logs: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get audit logs",
        ) from e


@router.get("/api-keys", response_model=APIKeyListResponse, summary="List all API keys")
async def list_api_keys(
    user_id: str | None = Query(None, description="Filter by user ID"),
    organization_id: str | None = Query(None, description="Filter by organization ID"),
    is_active: bool | None = Query(None, description="Filter by active status"),
    plan: str | None = Query(None, description="Filter by plan"),
    search: str | None = Query(None, description="Search by key prefix or name"),
    limit: int = Query(default=50, ge=1, le=100, description="Maximum number of results"),
    offset: int = Query(default=0, ge=0, description="Offset for pagination"),
    current_user: dict[str, Any] = Depends(require_permission_factory("security.api_keys")),
) -> APIKeyListResponse:
    """List all API keys with filters.

    Args:
        user_id: User ID filter
        organization_id: Organization ID filter
        is_active: Active status filter
        plan: Plan filter
        search: Search term
        limit: Result limit
        offset: Result offset
        current_user: Current admin user

    Returns:
        API key list response
    """
    query = APIKeyListQuery(
        user_id=user_id,
        organization_id=organization_id,
        is_active=is_active,
        plan=plan,
        search=search,
        limit=limit,
        offset=offset,
    )

    try:
        return await admin_security_service.list_api_keys(query)
    except Exception as e:
        logger.error("Error listing API keys: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list API keys",
        ) from e


@router.post("/api-keys/{api_key_id}/revoke", summary="Revoke API key (admin override)")
async def revoke_api_key_admin(
    api_key_id: str,
    request: APIKeyRevokeRequest,
    current_user: dict[str, Any] = Depends(require_permission_factory("security.api_keys")),
) -> dict[str, Any]:
    """Revoke API key (admin override).

    Args:
        api_key_id: API key ID
        request: Revoke request
        current_user: Current admin user

    Returns:
        Revoked API key response

    Raises:
        HTTPException: If API key not found
    """
    try:
        revoked_key = await admin_security_service.revoke_api_key_admin(
            api_key_id, request.reason, current_user
        )
        return revoked_key.model_dump()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error revoking API key: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to revoke API key",
        ) from e


@router.get("/ip-monitoring", response_model=IPMonitoringResponse, summary="Get IP monitoring data")
async def get_ip_monitoring(
    days: int = Query(default=7, ge=1, le=90, description="Number of days to analyze"),
    current_user: dict[str, Any] = Depends(require_admin),
) -> IPMonitoringResponse:
    """Get IP address monitoring data.

    Args:
        days: Number of days to analyze
        current_user: Current admin user

    Returns:
        IP monitoring response
    """
    try:
        return await admin_security_service.get_ip_monitoring(days=days)
    except Exception as e:
        logger.error("Error getting IP monitoring: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get IP monitoring",
        ) from e

