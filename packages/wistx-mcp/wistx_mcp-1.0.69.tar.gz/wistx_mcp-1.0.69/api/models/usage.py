"""Usage tracking models."""

from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class QueryMetrics(BaseModel):
    """Query usage metrics."""

    compliance_queries: int = Field(default=0, ge=0, description="Number of compliance queries")
    knowledge_queries: int = Field(default=0, ge=0, description="Number of knowledge base queries")
    total_queries: int = Field(default=0, ge=0, description="Total number of queries")


class IndexMetrics(BaseModel):
    """Indexing usage metrics."""

    repositories_indexed: int = Field(default=0, ge=0, description="Number of repositories indexed")
    documents_indexed: int = Field(default=0, ge=0, description="Number of documents indexed")
    total_indexes: int = Field(default=0, ge=0, description="Total number of indexes")
    storage_mb: float = Field(default=0.0, ge=0.0, description="Storage used in MB")


class PerformanceMetrics(BaseModel):
    """Performance metrics."""

    total_time_ms: int = Field(default=0, ge=0, description="Total request time in milliseconds")
    query_time_ms: Optional[int] = Field(default=None, ge=0, description="Query processing time")
    vector_search_time_ms: Optional[int] = Field(default=None, ge=0, description="Vector search time")


class APIUsageRequest(BaseModel):
    """API usage tracking request."""

    request_id: str = Field(..., description="Unique request ID")
    user_id: str = Field(..., description="User ID")
    api_key_id: str = Field(..., description="API key ID")
    organization_id: Optional[str] = Field(default=None, description="Organization ID")
    plan: str = Field(default="professional", description="User plan")
    endpoint: str = Field(..., description="API endpoint")
    method: str = Field(default="POST", description="HTTP method")
    operation_type: str = Field(..., description="Operation type: query, index, or other")
    operation_details: dict = Field(default_factory=dict, description="Operation-specific details")
    performance: Optional[PerformanceMetrics] = Field(default=None, description="Performance metrics")
    status_code: int = Field(default=200, description="HTTP status code")
    success: bool = Field(default=True, description="Request success status")
    ip_address: Optional[str] = Field(default=None, description="Client IP address")
    user_agent: Optional[str] = Field(default=None, description="User agent")


class UsageSummary(BaseModel):
    """Usage summary for a time period."""

    user_id: str = Field(..., description="User ID")
    start_date: datetime = Field(..., description="Start date")
    end_date: datetime = Field(..., description="End date")
    total_requests: int = Field(default=0, ge=0, description="Total requests")
    queries: QueryMetrics = Field(..., description="Query metrics")
    indexes: IndexMetrics = Field(..., description="Index metrics")
    requests_by_endpoint: dict[str, int] = Field(default_factory=dict, description="Requests by endpoint")
    requests_by_status: dict[int, int] = Field(default_factory=dict, description="Requests by status code")
    average_response_time_ms: Optional[float] = Field(default=None, ge=0, description="Average response time")


class DailyUsageSummary(BaseModel):
    """Daily usage summary."""

    date: datetime = Field(..., description="Date")
    total_requests: int = Field(default=0, ge=0, description="Total requests")
    queries: QueryMetrics = Field(..., description="Query metrics")
    indexes: IndexMetrics = Field(..., description="Index metrics")
