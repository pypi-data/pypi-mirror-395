"""Admin security models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from api.models.audit_log import AuditEventType, AuditLogSeverity


class SecurityEventsQuery(BaseModel):
    """Query parameters for security events."""

    severity: Optional[AuditLogSeverity] = Field(None, description="Filter by severity")
    start_date: Optional[datetime] = Field(None, description="Start date filter")
    end_date: Optional[datetime] = Field(None, description="End date filter")
    limit: int = Field(default=100, ge=1, le=1000, description="Maximum number of results")
    offset: int = Field(default=0, ge=0, description="Offset for pagination")


class SecurityEventSummary(BaseModel):
    """Security event summary."""

    event_type: AuditEventType = Field(..., description="Event type")
    count: int = Field(..., description="Event count")
    severity: AuditLogSeverity = Field(..., description="Event severity")


class SecurityEventsSummaryResponse(BaseModel):
    """Security events summary response."""

    total_events: int = Field(..., description="Total security events")
    events_by_type: list[SecurityEventSummary] = Field(..., description="Events grouped by type")
    events_by_severity: dict[str, int] = Field(..., description="Events grouped by severity")
    period_days: int = Field(..., description="Period in days")


class IPMonitoringEntry(BaseModel):
    """IP monitoring entry."""

    ip_address: str = Field(..., description="IP address")
    request_count: int = Field(..., description="Request count")
    failed_auth_count: int = Field(..., description="Failed authentication count")
    rate_limit_violations: int = Field(..., description="Rate limit violations")
    last_seen: datetime = Field(..., description="Last seen timestamp")
    user_ids: list[str] = Field(default_factory=list, description="User IDs using this IP")


class IPMonitoringResponse(BaseModel):
    """IP monitoring response."""

    ips: list[IPMonitoringEntry] = Field(..., description="IP monitoring entries")
    total_unique_ips: int = Field(..., description="Total unique IP addresses")
    period_days: int = Field(..., description="Period in days")


class APIKeyListQuery(BaseModel):
    """Query parameters for listing API keys."""

    user_id: Optional[str] = Field(None, description="Filter by user ID")
    organization_id: Optional[str] = Field(None, description="Filter by organization ID")
    is_active: Optional[bool] = Field(None, description="Filter by active status")
    plan: Optional[str] = Field(None, description="Filter by plan")
    search: Optional[str] = Field(None, description="Search by key prefix or name")
    limit: int = Field(default=50, ge=1, le=100, description="Maximum number of results")
    offset: int = Field(default=0, ge=0, description="Offset for pagination")


class AdminAPIKeyResponse(BaseModel):
    """Admin API key response."""

    api_key_id: str = Field(..., description="API key ID")
    key_prefix: str = Field(..., description="Key prefix")
    name: Optional[str] = Field(None, description="Key name")
    user_id: str = Field(..., description="User ID")
    user_email: Optional[str] = Field(None, description="User email")
    organization_id: Optional[str] = Field(None, description="Organization ID")
    plan: str = Field(..., description="Plan")
    is_active: bool = Field(..., description="Active status")
    is_test_key: bool = Field(..., description="Test key flag")
    usage_count: int = Field(..., description="Usage count")
    last_used_at: Optional[datetime] = Field(None, description="Last used timestamp")
    last_used_ip: Optional[str] = Field(None, description="Last used IP")
    created_at: datetime = Field(..., description="Created timestamp")
    expires_at: Optional[datetime] = Field(None, description="Expiration timestamp")
    revoked_at: Optional[datetime] = Field(None, description="Revocation timestamp")


class APIKeyListResponse(BaseModel):
    """API key list response."""

    api_keys: list[AdminAPIKeyResponse] = Field(..., description="List of API keys")
    total: int = Field(..., description="Total number of API keys matching filters")
    limit: int = Field(..., description="Limit used")
    offset: int = Field(..., description="Offset used")


class APIKeyRevokeRequest(BaseModel):
    """Request model for revoking API key."""

    reason: Optional[str] = Field(None, max_length=500, description="Revocation reason")

