"""Security audit log endpoints."""

import logging
from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.dependencies.auth import get_current_user
from api.models.audit_log import (
    AuditEventType,
    AuditLogQuery,
    AuditLogResponse,
    AuditLogSeverity,
)
from api.services.audit_log_service import audit_log_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/audit-logs", tags=["audit-logs"])


@router.get("", response_model=AuditLogResponse)
async def query_audit_logs(
    event_types: list[AuditEventType] | None = Query(None, description="Filter by event types"),
    severity: AuditLogSeverity | None = Query(None, description="Filter by severity"),
    user_id: str | None = Query(None, description="Filter by user ID"),
    api_key_id: str | None = Query(None, description="Filter by API key ID"),
    organization_id: str | None = Query(None, description="Filter by organization ID"),
    ip_address: str | None = Query(None, description="Filter by IP address"),
    start_date: datetime | None = Query(None, description="Start date filter"),
    end_date: datetime | None = Query(None, description="End date filter"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of results"),
    offset: int = Query(default=0, ge=0, description="Offset for pagination"),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> AuditLogResponse:
    """Query security audit logs.

    Requires admin permissions or access to own organization's logs.

    Returns:
        Audit log response with matching entries
    """
    user_info = current_user
    user_plan = user_info.get("plan", "professional")

    if user_plan not in ("enterprise", "admin"):
        if organization_id and organization_id != user_info.get("organization_id"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Cannot query other organization's audit logs",
            )

        if user_id and user_id != user_info.get("user_id"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Cannot query other user's audit logs",
            )

        if not organization_id:
            organization_id = user_info.get("organization_id")

    query = AuditLogQuery(
        event_types=event_types,
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

    return audit_log_service.query_logs(query)


@router.get("/security-events", response_model=AuditLogResponse)
async def get_security_events(
    severity: AuditLogSeverity | None = Query(None, description="Filter by severity"),
    start_date: datetime | None = Query(None, description="Start date filter"),
    end_date: datetime | None = Query(None, description="End date filter"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of results"),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> AuditLogResponse:
    """Get security-related events.

    Returns security events like authentication failures, unauthorized access,
    rate limit violations, and suspicious activity.

    Returns:
        Audit log response with security events
    """
    user_info = current_user
    user_plan = user_info.get("plan", "professional")

    if user_plan not in ("enterprise", "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Security events require admin permissions",
        )

    logs = audit_log_service.get_security_events(
        start_date=start_date,
        end_date=end_date,
        severity=severity,
        limit=limit,
    )

    return AuditLogResponse(logs=logs, total=len(logs), limit=limit, offset=0)


@router.get("/user/{user_id}", response_model=AuditLogResponse)
async def get_user_audit_trail(
    user_id: str,
    start_date: datetime | None = Query(None, description="Start date filter"),
    end_date: datetime | None = Query(None, description="End date filter"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of results"),
    offset: int = Query(default=0, ge=0, description="Offset for pagination"),
    event_types: list[AuditEventType] | None = Query(None, description="Filter by event types"),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> AuditLogResponse:
    """Get audit trail for a specific user.

    Users can only view their own audit trail unless they have admin permissions.

    Returns:
        Audit log response with user's audit trail
    """
    user_info = current_user
    current_user_id = user_info.get("user_id")
    user_plan = user_info.get("plan", "professional")

    if user_plan not in ("enterprise", "admin") and user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot view other user's audit trail",
        )

    logger.debug(
        "Fetching user audit trail: user_id=%s, event_types=%s, offset=%d, limit=%d",
        user_id,
        [et.value if isinstance(et, AuditEventType) else et for et in (event_types or [])],
        offset,
        limit,
    )

    query = AuditLogQuery(
        user_id=user_id,
        event_types=event_types if event_types else None,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset,
    )

    response = audit_log_service.query_logs(query)
    
    logger.debug(
        "User audit trail response: total=%d, returned=%d, event_types_filter=%s",
        response.total,
        len(response.logs),
        [et.value if isinstance(et, AuditEventType) else et for et in (event_types or [])],
    )
    
    return response


@router.get("/compliance/{compliance_tag}", response_model=AuditLogResponse)
async def get_compliance_audit_trail(
    compliance_tag: str,
    start_date: datetime | None = Query(None, description="Start date filter"),
    end_date: datetime | None = Query(None, description="End date filter"),
    limit: int = Query(default=1000, ge=1, le=10000, description="Maximum number of results"),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> AuditLogResponse:
    """Get audit trail for compliance requirements.

    Returns audit logs tagged with specific compliance standards (PCI-DSS, HIPAA, SOC2, etc.).

    Returns:
        Audit log response with compliance audit trail
    """
    user_info = current_user
    user_plan = user_info.get("plan", "professional")

    if user_plan not in ("enterprise", "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Compliance audit trails require admin permissions",
        )

    logs = audit_log_service.get_compliance_audit_trail(
        compliance_tag=compliance_tag,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
    )

    return AuditLogResponse(logs=logs, total=len(logs), limit=limit, offset=0)

