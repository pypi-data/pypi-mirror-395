"""Admin analytics models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ActivityFeedQuery(BaseModel):
    """Query parameters for activity feed."""

    user_id: Optional[str] = Field(None, description="Filter by user ID")
    endpoint: Optional[str] = Field(None, description="Filter by endpoint")
    operation_type: Optional[str] = Field(None, description="Filter by operation type")
    success: Optional[bool] = Field(None, description="Filter by success status")
    start_date: Optional[datetime] = Field(None, description="Start date filter")
    end_date: Optional[datetime] = Field(None, description="End date filter")
    limit: int = Field(default=100, ge=1, le=1000, description="Maximum number of results")
    offset: int = Field(default=0, ge=0, description="Offset for pagination")


class ActivityEntry(BaseModel):
    """Activity feed entry."""

    request_id: str = Field(..., description="Request ID")
    user_id: str = Field(..., description="User ID")
    email: Optional[str] = Field(None, description="User email")
    api_key_id: Optional[str] = Field(None, description="API key ID")
    organization_id: Optional[str] = Field(None, description="Organization ID")
    plan: str = Field(..., description="User plan")
    timestamp: datetime = Field(..., description="Activity timestamp")
    endpoint: str = Field(..., description="API endpoint")
    method: str = Field(..., description="HTTP method")
    operation_type: str = Field(..., description="Operation type")
    status_code: int = Field(..., description="HTTP status code")
    success: bool = Field(..., description="Success status")
    ip_address: Optional[str] = Field(None, description="IP address")
    user_agent: Optional[str] = Field(None, description="User agent")
    response_time_ms: Optional[int] = Field(None, description="Response time in milliseconds")


class ActivityFeedResponse(BaseModel):
    """Activity feed response."""

    activities: list[ActivityEntry] = Field(..., description="List of activities")
    total: int = Field(..., description="Total number of activities matching filters")
    limit: int = Field(..., description="Limit used")
    offset: int = Field(..., description="Offset used")


class UsageOverviewResponse(BaseModel):
    """Usage overview response."""

    total_users: int = Field(..., description="Total number of users")
    active_users_24h: int = Field(..., description="Active users in last 24 hours")
    active_users_7d: int = Field(..., description="Active users in last 7 days")
    active_users_30d: int = Field(..., description="Active users in last 30 days")
    total_api_requests: int = Field(..., description="Total API requests")
    total_api_requests_24h: int = Field(..., description="API requests in last 24 hours")
    total_api_requests_7d: int = Field(..., description="API requests in last 7 days")
    total_api_requests_30d: int = Field(..., description="API requests in last 30 days")
    total_queries: int = Field(..., description="Total queries")
    total_indexing_operations: int = Field(..., description="Total indexing operations")
    total_storage_mb: float = Field(..., description="Total storage used in MB")
    average_response_time_ms: Optional[float] = Field(None, description="Average response time")
    error_rate: float = Field(..., description="Error rate percentage")


class UsageByPlanResponse(BaseModel):
    """Usage statistics by plan."""

    plan: str = Field(..., description="Plan name")
    user_count: int = Field(..., description="Number of users")
    total_requests: int = Field(..., description="Total requests")
    total_queries: int = Field(..., description="Total queries")
    total_indexing: int = Field(..., description="Total indexing operations")
    total_storage_mb: float = Field(..., description="Total storage MB")
    average_requests_per_user: float = Field(..., description="Average requests per user")


class UsageByPlanListResponse(BaseModel):
    """Usage by plan list response."""

    plans: list[UsageByPlanResponse] = Field(..., description="Usage by plan")


class UsageTrendsQuery(BaseModel):
    """Query parameters for usage trends."""

    days: int = Field(default=30, ge=1, le=365, description="Number of days")
    group_by: str = Field(default="day", description="Group by (day, week, month)")


class UsageTrendPoint(BaseModel):
    """Usage trend data point."""

    date: str = Field(..., description="Date")
    total_requests: int = Field(..., description="Total requests")
    total_queries: int = Field(..., description="Total queries")
    total_indexing: int = Field(..., description="Total indexing operations")
    unique_users: int = Field(..., description="Unique active users")
    error_count: int = Field(..., description="Error count")
    average_response_time_ms: Optional[float] = Field(None, description="Average response time")


class UsageTrendsResponse(BaseModel):
    """Usage trends response."""

    trends: list[UsageTrendPoint] = Field(..., description="Usage trend data points")
    period_days: int = Field(..., description="Period in days")


class TopEndpointResponse(BaseModel):
    """Top endpoint response."""

    endpoint: str = Field(..., description="Endpoint path")
    request_count: int = Field(..., description="Request count")
    average_response_time_ms: Optional[float] = Field(None, description="Average response time")
    error_count: int = Field(..., description="Error count")
    error_rate: float = Field(..., description="Error rate percentage")


class TopEndpointsResponse(BaseModel):
    """Top endpoints response."""

    endpoints: list[TopEndpointResponse] = Field(..., description="Top endpoints")
    period_days: int = Field(..., description="Period in days")


class TopUserResponse(BaseModel):
    """Top user response."""

    user_id: str = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    plan: str = Field(..., description="User plan")
    request_count: int = Field(..., description="Request count")
    query_count: int = Field(..., description="Query count")
    indexing_count: int = Field(..., description="Indexing count")
    storage_mb: float = Field(..., description="Storage MB")


class TopUsersResponse(BaseModel):
    """Top users response."""

    users: list[TopUserResponse] = Field(..., description="Top users")
    period_days: int = Field(..., description="Period in days")
    limit: int = Field(..., description="Limit used")

