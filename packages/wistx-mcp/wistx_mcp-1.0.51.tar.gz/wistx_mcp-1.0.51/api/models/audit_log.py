"""Pydantic models for security audit logging."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AuditEventType(str, Enum):
    """Security audit event types."""

    AUTHENTICATION_SUCCESS = "authentication_success"
    AUTHENTICATION_FAILURE = "authentication_failure"
    AUTHENTICATION_LOGOUT = "authentication_logout"
    API_KEY_CREATED = "api_key_created"
    API_KEY_DELETED = "api_key_deleted"
    API_KEY_ROTATED = "api_key_rotated"
    API_KEY_USED = "api_key_used"
    OAUTH_CONNECTED = "oauth_connected"
    OAUTH_DISCONNECTED = "oauth_disconnected"
    TOKEN_REFRESHED = "token_refreshed"
    TOKEN_REVOKED = "token_revoked"
    AUTHORIZATION_GRANTED = "authorization_granted"
    AUTHORIZATION_DENIED = "authorization_denied"
    PERMISSION_CHANGED = "permission_changed"
    ROLE_ASSIGNED = "role_assigned"
    ROLE_REVOKED = "role_revoked"
    DATA_ACCESSED = "data_accessed"
    DATA_MODIFIED = "data_modified"
    DATA_DELETED = "data_deleted"
    CONFIGURATION_CHANGED = "configuration_changed"
    PLAN_CHANGED = "plan_changed"
    SETTINGS_MODIFIED = "settings_modified"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    UNAUTHORIZED_ACCESS_ATTEMPT = "unauthorized_access_attempt"
    SECURITY_ALERT = "security_alert"
    ORGANIZATION_CREATED = "organization_created"
    ORGANIZATION_UPDATED = "organization_updated"
    ORGANIZATION_DELETED = "organization_deleted"
    ORGANIZATION_MEMBER_INVITED = "organization_member_invited"
    ORGANIZATION_MEMBER_ACCEPTED = "organization_member_accepted"
    ORGANIZATION_MEMBER_REMOVED = "organization_member_removed"
    ORGANIZATION_MEMBER_ROLE_CHANGED = "organization_member_role_changed"
    ORGANIZATION_INVITATION_REVOKED = "organization_invitation_revoked"
    ORGANIZATION_API_KEY_CREATED = "organization_api_key_created"
    ORGANIZATION_API_KEY_DELETED = "organization_api_key_deleted"


class AuditLogSeverity(str, Enum):
    """Audit log severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AuditLog(BaseModel):
    """Security audit log entry."""

    event_id: str = Field(..., description="Unique event ID")
    event_type: AuditEventType = Field(..., description="Type of audit event")
    severity: AuditLogSeverity = Field(..., description="Event severity")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Event timestamp")
    user_id: str | None = Field(None, description="User ID (if applicable)")
    api_key_id: str | None = Field(None, description="API key ID (if applicable)")
    organization_id: str | None = Field(None, description="Organization ID (if applicable)")
    ip_address: str | None = Field(None, description="Client IP address")
    user_agent: str | None = Field(None, description="User agent string")
    request_id: str | None = Field(None, description="Request ID for correlation")
    endpoint: str | None = Field(None, description="API endpoint or MCP tool name")
    method: str | None = Field(None, description="HTTP method (for API)")
    status_code: int | None = Field(None, description="HTTP status code")
    success: bool = Field(..., description="Whether operation was successful")
    message: str = Field(..., description="Human-readable event message")
    details: dict[str, Any] = Field(default_factory=dict, description="Additional event details")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    compliance_tags: list[str] = Field(default_factory=list, description="Compliance tags (PCI-DSS, HIPAA, etc.)")


class AuditLogQuery(BaseModel):
    """Query parameters for audit log retrieval."""

    event_types: list[AuditEventType] | None = Field(None, description="Filter by event types")
    severity: AuditLogSeverity | None = Field(None, description="Filter by severity")
    user_id: str | None = Field(None, description="Filter by user ID")
    api_key_id: str | None = Field(None, description="Filter by API key ID")
    organization_id: str | None = Field(None, description="Filter by organization ID")
    ip_address: str | None = Field(None, description="Filter by IP address")
    start_date: datetime | None = Field(None, description="Start date filter")
    end_date: datetime | None = Field(None, description="End date filter")
    limit: int = Field(default=100, ge=1, le=1000, description="Maximum number of results")
    offset: int = Field(default=0, ge=0, description="Offset for pagination")


class AuditLogResponse(BaseModel):
    """Audit log query response."""

    logs: list[AuditLog] = Field(..., description="List of audit log entries")
    total: int = Field(..., description="Total number of matching entries")
    limit: int = Field(..., description="Limit used")
    offset: int = Field(..., description="Offset used")

