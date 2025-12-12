"""Response models for v1 API."""

from typing import Any, Optional

from pydantic import BaseModel, Field


class ComplianceControlResponse(BaseModel):
    """Response model for a single compliance control."""

    control_id: str = Field(..., description="Unique control identifier")
    standard: str = Field(..., description="Compliance standard")
    title: str = Field(..., description="Control title")
    description: str = Field(..., description="Control description")
    severity: str = Field(..., description="Severity level")
    category: str | None = Field(default=None, description="Category")
    subcategory: str | None = Field(default=None, description="Subcategory")
    applies_to: list[str] = Field(default_factory=list, description="Applicable resources")
    remediation: dict[str, Any] | None = Field(default=None, description="Remediation guidance")
    verification: dict[str, Any] | None = Field(default=None, description="Verification procedures")
    references: list[dict[str, Any]] = Field(default_factory=list, description="External references")
    source_url: str | None = Field(default=None, description="Source URL")


class ComplianceRequirementsSummary(BaseModel):
    """Summary statistics for compliance requirements."""

    total: int = Field(..., description="Total number of controls")
    by_severity: dict[str, int] = Field(default_factory=dict, description="Count by severity")
    by_standard: dict[str, int] = Field(default_factory=dict, description="Count by standard")


class ComplianceRequirementsResponse(BaseModel):
    """Response model for compliance requirements query."""

    controls: list[ComplianceControlResponse] = Field(default_factory=list, description="List of compliance controls")
    summary: ComplianceRequirementsSummary = Field(..., description="Summary statistics")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Query metadata")


class KnowledgeArticleResponse(BaseModel):
    """Response model for a single knowledge article."""

    article_id: str = Field(..., description="Unique article identifier")
    domain: str = Field(..., description="Knowledge domain")
    subdomain: str = Field(..., description="Subdomain")
    content_type: str = Field(..., description="Content type")
    title: str = Field(..., description="Article title")
    summary: str = Field(..., description="Article summary")
    content: str | None = Field(default=None, description="Full content (if requested)")
    tags: list[str] = Field(default_factory=list, description="Tags")
    categories: list[str] = Field(default_factory=list, description="Categories")
    industries: list[str] = Field(default_factory=list, description="Applicable industries")
    cloud_providers: list[str] = Field(default_factory=list, description="Cloud providers")
    services: list[str] = Field(default_factory=list, description="Services")
    cross_domain_impacts: dict[str, Any] | None = Field(
        default=None,
        description="Cross-domain impacts (compliance, cost, security)",
    )
    source_url: str | None = Field(default=None, description="Source URL")
    quality_score: float | None = Field(default=None, description="Quality score")


class KnowledgeResearchSummary(BaseModel):
    """Summary statistics for knowledge research."""

    total_found: int = Field(..., description="Total number of articles found")
    domains_covered: list[str] = Field(default_factory=list, description="Domains covered in results")
    key_insights: list[str] = Field(default_factory=list, description="Key insights")


class KnowledgeResearchResponse(BaseModel):
    """Response model for knowledge research query."""

    results: list[KnowledgeArticleResponse] = Field(default_factory=list, description="Search results")
    research_summary: KnowledgeResearchSummary = Field(..., description="Research summary")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Query metadata")


class APIResponse(BaseModel):
    """Standard API response wrapper."""

    data: dict[str, Any] | list[Any] = Field(..., description="Response data")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Response metadata")


class APIError(BaseModel):
    """Standard API error response."""

    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: str | dict[str, Any] | None = Field(default=None, description="Error details (can be string, dict, or null)")


class ErrorResponse(BaseModel):
    """Error response wrapper."""

    error: APIError = Field(..., description="Error information")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Response metadata")


class BudgetResponse(BaseModel):
    """Response model for infrastructure budget."""

    budget_id: str = Field(..., description="Budget ID")
    name: str = Field(..., description="Budget name")
    description: Optional[str] = Field(default=None, description="Budget description")
    scope: dict[str, Any] = Field(..., description="Budget scope")
    monthly_limit_usd: float = Field(..., description="Monthly budget limit")
    alert_threshold_percent: float = Field(..., description="Alert threshold")
    critical_threshold_percent: float = Field(..., description="Critical threshold")
    status: str = Field(..., description="Budget status")
    enforcement_mode: str = Field(..., description="Enforcement mode")
    current_period_start: str = Field(..., description="Period start (ISO format)")
    current_period_end: str = Field(..., description="Period end (ISO format)")
    created_at: str = Field(..., description="Creation timestamp (ISO format)")
    updated_at: str = Field(..., description="Update timestamp (ISO format)")


class BudgetStatusResponse(BaseModel):
    """Response model for budget status."""

    budget_id: str = Field(..., description="Budget ID")
    period: str = Field(..., description="Period (YYYY-MM)")
    total_spent_usd: float = Field(..., description="Total spending")
    budget_limit_usd: float = Field(..., description="Budget limit")
    remaining_usd: float = Field(..., description="Remaining budget")
    utilization_percent: float = Field(..., description="Utilization percentage")
    status: str = Field(..., description="Budget status")
    by_cloud_provider: dict[str, float] = Field(default_factory=dict, description="Spending by cloud")
    by_service: dict[str, float] = Field(default_factory=dict, description="Spending by service")
    projected_monthly_spend: Optional[float] = Field(default=None, description="Projected spending")
    projected_exceed: bool = Field(default=False, description="Projected to exceed")
    days_until_exceed: Optional[int] = Field(default=None, description="Days until exceed")


class SpendingSummaryResponse(BaseModel):
    """Response model for spending summary."""

    period: str = Field(..., description="Period (YYYY-MM)")
    total_spent_usd: float = Field(..., description="Total spending")
    by_cloud_provider: dict[str, float] = Field(default_factory=dict, description="Spending by cloud")
    by_service: dict[str, float] = Field(default_factory=dict, description="Spending by service")
    by_environment: dict[str, float] = Field(default_factory=dict, description="Spending by environment")
    component_count: int = Field(default=0, description="Number of components")


class CodebaseSearchResult(BaseModel):
    """Response model for a single codebase search result."""

    article_id: str = Field(..., description="Article ID")
    resource_id: str = Field(..., description="Resource ID")
    title: str = Field(..., description="Title")
    content: str = Field(..., description="Content")
    source_url: Optional[str] = Field(default=None, description="Source URL")
    file_path: Optional[str] = Field(default=None, description="File path")
    tags: list[str] = Field(default_factory=list, description="Tags")
    similarity_score: Optional[float] = Field(default=None, description="Similarity score")


class FreshnessInfo(BaseModel):
    """Freshness metadata for search results."""

    index_last_updated: Optional[str] = Field(
        default=None,
        description="ISO timestamp when index was last updated",
    )
    latest_commit_sha: Optional[str] = Field(
        default=None,
        description="SHA of latest commit in repository",
    )
    indexed_commit_sha: Optional[str] = Field(
        default=None,
        description="SHA of commit when index was last updated",
    )
    commits_behind: int = Field(
        default=0,
        description="Number of commits behind latest",
    )
    stale_files_count: int = Field(
        default=0,
        description="Number of files that have changed since indexing",
    )
    stale_files: list[str] = Field(
        default_factory=list,
        description="List of files that have changed (limited to first 10)",
    )
    fresh_content_fetched: bool = Field(
        default=False,
        description="Whether fresh content was fetched for stale files",
    )
    freshness_check_performed: bool = Field(
        default=False,
        description="Whether freshness check was performed",
    )
    freshness_check_error: Optional[str] = Field(
        default=None,
        description="Error message if freshness check failed",
    )


class CodebaseSearchResponse(BaseModel):
    """Response model for codebase search."""

    results: list[CodebaseSearchResult] = Field(default_factory=list, description="Search results")
    resources: list[dict[str, Any]] = Field(default_factory=list, description="Resource information")
    total: int = Field(..., description="Total results count")
    highlights: list[dict[str, Any]] = Field(default_factory=list, description="Code highlights")
    ai_analysis: Optional[dict[str, Any]] = Field(default=None, description="AI analysis")
    grouped_by_section: Optional[dict[str, Any]] = Field(
        default=None,
        description="Results grouped by documentation section (if group_by_section=true)",
    )
    freshness: Optional[FreshnessInfo] = Field(
        default=None,
        description="Freshness metadata (if check_freshness=true or include_fresh_content=true)",
    )


class PackageFileReference(BaseModel):
    """Reference to a package source file."""

    file_path: str = Field(..., description="File path within package")
    filename_sha256: str = Field(..., description="SHA256 hash of filename (for reading file content)")


class PackageSearchResult(BaseModel):
    """Response model for a single package search result."""

    package_id: str = Field(..., description="Package ID")
    name: str = Field(..., description="Package name")
    registry: str = Field(..., description="Registry name")
    version: Optional[str] = Field(default=None, description="Version")
    description: Optional[str] = Field(default=None, description="Description")
    domain: Optional[str] = Field(default=None, description="Domain")
    category: Optional[str] = Field(default=None, description="Category")
    github_url: Optional[str] = Field(default=None, description="GitHub URL")
    download_count: Optional[int] = Field(default=None, description="Download count")
    stars: Optional[int] = Field(default=None, description="GitHub stars")
    similarity_score: Optional[float] = Field(default=None, description="Similarity score")
    source_files: Optional[list[PackageFileReference]] = Field(
        default=None,
        description="Key source files with SHA256 hashes (for reading file content via wistx_read_package_file)",
    )


class PackageSearchResponse(BaseModel):
    """Response model for package search."""

    results: list[PackageSearchResult] = Field(default_factory=list, description="Search results")
    matches: list[PackageSearchResult] = Field(default_factory=list, description="Regex matches")
    total: int = Field(..., description="Total results")
    semantic_count: Optional[int] = Field(default=None, description="Semantic results count")
    regex_count: Optional[int] = Field(default=None, description="Regex results count")
    search_type: str = Field(..., description="Search type used")


class ArchitectureDesignResponse(BaseModel):
    """Response model for architecture design."""

    action: str = Field(..., description="Action performed")
    project_name: Optional[str] = Field(default=None, description="Project name")
    architecture: dict[str, Any] = Field(..., description="Architecture design")
    templates: list[dict[str, Any]] = Field(default_factory=list, description="Templates used")
    compliance_context: Optional[dict[str, Any]] = Field(default=None, description="Compliance context")
    security_context: Optional[dict[str, Any]] = Field(default=None, description="Security context")
    best_practices: list[dict[str, Any]] = Field(default_factory=list, description="Best practices")
    recommendations: list[str] = Field(default_factory=list, description="Recommendations")
    output_files: list[dict[str, Any]] = Field(default_factory=list, description="Generated files")


class InfrastructureInventoryResponse(BaseModel):
    """Response model for infrastructure inventory."""

    repository_url: Optional[str] = Field(default=None, description="Repository URL")
    environment_name: Optional[str] = Field(default=None, description="Environment name")
    status: str = Field(..., description="Status (indexed, not_indexed)")
    resource_id: Optional[str] = Field(default=None, description="Resource ID")
    resources: list[dict[str, Any]] = Field(default_factory=list, description="Infrastructure resources")
    resources_count: int = Field(default=0, description="Total resources count")
    total_monthly_cost: float = Field(default=0.0, description="Total monthly cost")
    total_annual_cost: float = Field(default=0.0, description="Total annual cost")
    cost_breakdown: dict[str, Any] = Field(default_factory=dict, description="Cost breakdown")
    cost_optimizations: list[dict[str, Any]] = Field(default_factory=list, description="Cost optimizations")
    compliance_summary: dict[str, Any] = Field(default_factory=dict, description="Compliance summary")
    compliance_status: str = Field(default="unknown", description="Overall compliance status")
    recommendations: list[str] = Field(default_factory=list, description="Recommendations")
    context_for_agents: Optional[str] = Field(default=None, description="Context for coding agents")


class InfrastructureManageResponse(BaseModel):
    """Response model for infrastructure management."""

    resource_id: str = Field(..., description="Resource identifier")
    status: str = Field(..., description="Current status")
    endpoints: list[str] = Field(default_factory=list, description="Access endpoints")
    compliance_status: Optional[dict[str, Any]] = Field(default=None, description="Compliance status")
    cost_summary: Optional[dict[str, Any]] = Field(default=None, description="Cost information")
    recommendations: list[str] = Field(default_factory=list, description="Optimization recommendations")
    action_performed: str = Field(..., description="Action that was performed")


class ServiceStatusResponse(BaseModel):
    """Response model for individual service status."""

    status: str = Field(..., description="Service status (operational, degraded, down, not_configured)")
    latency_ms: Optional[float] = Field(default=None, description="Service latency in milliseconds")
    error: Optional[str] = Field(default=None, description="Error message if status is not operational")
    message: Optional[str] = Field(default=None, description="Additional status message")


class StatusResponse(BaseModel):
    """Response model for overall system status."""

    status: str = Field(..., description="Overall status (operational, degraded, down)")
    timestamp: str = Field(..., description="ISO timestamp of status check")
    check_duration_ms: float = Field(..., description="Duration of status check in milliseconds")
    services: dict[str, Any] = Field(..., description="Status of individual services")


class UptimeStatsResponse(BaseModel):
    """Response model for uptime statistics."""

    period_days: int = Field(..., description="Number of days for uptime calculation")
    total_checks: int = Field(..., description="Total number of status checks")
    operational_checks: int = Field(..., description="Number of operational checks")
    uptime_percentage: float = Field(..., description="Uptime percentage")
    error: Optional[str] = Field(default=None, description="Error message if calculation failed")
    message: Optional[str] = Field(default=None, description="Informational message about uptime statistics")


class CostBreakdownItem(BaseModel):
    """Response model for a single cost breakdown item."""

    resource: str = Field(..., description="Resource identifier (cloud:service:instance_type)")
    quantity: int = Field(..., description="Quantity")
    monthly: float = Field(..., description="Monthly cost in USD")
    annual: float = Field(..., description="Annual cost in USD")
    region: Optional[str] = Field(default=None, description="Region ID")
    pricing_category: Optional[str] = Field(default=None, description="Pricing category (OnDemand, Reserved, Spot)")
    category: Optional[str] = Field(default=None, description="Category (existing, new)")
    error: Optional[str] = Field(default=None, description="Error message if pricing data not available")


class BudgetCheckResponse(BaseModel):
    """Response model for budget check results."""

    status: str = Field(..., description="Budget status (within_limit, warning, exceeded)")
    applicable_budgets: list[dict[str, Any]] = Field(
        default_factory=list,
        description="List of applicable budgets with status",
    )
    projected_total: float = Field(..., description="Projected total monthly cost")


class PricingCalculationResponse(BaseModel):
    """Response model for infrastructure cost calculation."""

    total_monthly: float = Field(..., description="Total monthly cost in USD")
    total_annual: float = Field(..., description="Total annual cost in USD")
    breakdown: list[CostBreakdownItem] = Field(default_factory=list, description="Cost breakdown by resource")
    optimizations: list[str] = Field(default_factory=list, description="Optimization suggestions")
    existing_monthly: Optional[float] = Field(default=None, description="Existing infrastructure monthly spending")
    existing_annual: Optional[float] = Field(default=None, description="Existing infrastructure annual spending")
    total_with_existing: Optional[float] = Field(
        default=None,
        description="Total cost including existing infrastructure",
    )
    budget_check: Optional[BudgetCheckResponse] = Field(default=None, description="Budget check results")


class CodeExampleResponse(BaseModel):
    """Response model for a single code example."""

    example_id: str = Field(..., description="Unique example identifier")
    title: str = Field(..., description="Example title")
    description: str = Field(default="", description="Example description")
    contextual_description: Optional[str] = Field(default=None, description="Contextual description")
    code_type: str = Field(..., description="Code type (terraform, kubernetes, etc.)")
    cloud_provider: str = Field(..., description="Cloud provider (aws, gcp, azure)")
    services: list[str] = Field(default_factory=list, description="Cloud services used")
    resources: list[str] = Field(default_factory=list, description="Resource types")
    code: str = Field(..., description="Code content")
    github_url: str = Field(..., description="GitHub repository URL")
    file_path: str = Field(default="", description="File path in repository")
    stars: int = Field(default=0, description="GitHub stars count")
    quality_score: int = Field(default=0, description="Quality score (0-100)")
    best_practices: list[str] = Field(default_factory=list, description="Best practices identified")
    hybrid_score: float = Field(default=0.0, description="Hybrid search score")
    vector_score: float = Field(default=0.0, description="Vector search score")
    bm25_score: float = Field(default=0.0, description="BM25 search score")
    compliance_analysis: Optional[dict[str, Any]] = Field(default=None, description="Compliance analysis")
    cost_analysis: Optional[dict[str, Any]] = Field(default=None, description="Cost analysis")


class CodeExamplesSearchResponse(BaseModel):
    """Response model for code examples search."""

    examples: list[CodeExampleResponse] = Field(default_factory=list, description="List of code examples")
    total: int = Field(..., description="Total number of results")
    query: str = Field(..., description="Search query used")

