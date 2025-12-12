"""Organization usage analytics models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from api.models.usage import IndexMetrics, QueryMetrics


class MemberUsageBreakdown(BaseModel):
    """Member-level usage breakdown."""

    user_id: str = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    full_name: Optional[str] = Field(default=None, description="User full name")
    role: str = Field(..., description="Member role (owner, admin, member, viewer)")
    queries: int = Field(default=0, ge=0, description="Number of queries")
    indexes: int = Field(default=0, ge=0, description="Number of indexes")
    storage_mb: float = Field(default=0.0, ge=0.0, description="Storage used in MB")
    total_requests: int = Field(default=0, ge=0, description="Total API requests")
    success_rate: float = Field(default=0.0, ge=0.0, le=100.0, description="Success rate percentage")
    average_response_time_ms: Optional[float] = Field(default=None, ge=0, description="Average response time")


class OrganizationUsageSummary(BaseModel):
    """Organization-level usage summary."""

    organization_id: str = Field(..., description="Organization ID")
    organization_name: str = Field(..., description="Organization name")
    plan_id: str = Field(..., description="Organization plan")
    start_date: datetime = Field(..., description="Start date")
    end_date: datetime = Field(..., description="End date")
    total_requests: int = Field(default=0, ge=0, description="Total requests")
    successful_requests: int = Field(default=0, ge=0, description="Successful requests")
    failed_requests: int = Field(default=0, ge=0, description="Failed requests")
    success_rate: float = Field(default=0.0, ge=0.0, le=100.0, description="Success rate percentage")
    queries: QueryMetrics = Field(..., description="Query metrics")
    indexes: IndexMetrics = Field(..., description="Index metrics")
    total_members: int = Field(default=0, ge=0, description="Total active members")
    active_members: int = Field(default=0, ge=0, description="Members with usage in period")
    requests_by_endpoint: dict[str, int] = Field(default_factory=dict, description="Requests by endpoint")
    requests_by_status: dict[int, int] = Field(default_factory=dict, description="Requests by status code")
    average_response_time_ms: Optional[float] = Field(default=None, ge=0, description="Average response time")
    member_breakdown: list[MemberUsageBreakdown] = Field(default_factory=list, description="Per-member usage breakdown")


class DailyOrganizationUsage(BaseModel):
    """Daily organization usage."""

    date: str = Field(..., description="Date (YYYY-MM-DD)")
    total_requests: int = Field(default=0, ge=0, description="Total requests")
    queries: QueryMetrics = Field(..., description="Query metrics")
    indexes: IndexMetrics = Field(..., description="Index metrics")
    active_members: int = Field(default=0, ge=0, description="Active members on this day")


class OrganizationUsageTrends(BaseModel):
    """Organization usage trends over time."""

    organization_id: str = Field(..., description="Organization ID")
    period_days: int = Field(..., ge=1, le=365, description="Number of days in period")
    daily_usage: list[DailyOrganizationUsage] = Field(default_factory=list, description="Daily usage data")
    total_queries: int = Field(default=0, ge=0, description="Total queries in period")
    total_indexes: int = Field(default=0, ge=0, description="Total indexes in period")
    total_storage_mb: float = Field(default=0.0, ge=0.0, description="Total storage in MB")
    peak_usage_day: Optional[str] = Field(default=None, description="Date with peak usage")
    peak_usage_requests: int = Field(default=0, ge=0, description="Peak usage requests")


class OrganizationQuotaStatus(BaseModel):
    """Organization quota status with member breakdown."""

    organization_id: str = Field(..., description="Organization ID")
    plan_id: str = Field(..., description="Organization plan")
    queries: dict[str, int | float] = Field(..., description="Query quota status (current, limit, percentage)")
    indexes: dict[str, int | float] = Field(..., description="Index quota status (current, limit, percentage)")
    storage: dict[str, float] = Field(..., description="Storage quota status (current, limit, percentage)")
    member_breakdown: list[MemberUsageBreakdown] = Field(default_factory=list, description="Per-member usage breakdown")

