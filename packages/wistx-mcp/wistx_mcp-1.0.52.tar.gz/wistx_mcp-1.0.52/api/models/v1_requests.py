"""Request models for v1 API."""

from typing import Any, Optional

from pydantic import BaseModel, Field, model_validator


class ComplianceRequirementsRequest(BaseModel):
    """Request model for compliance requirements query."""

    resource_types: list[str] = Field(
        ...,
        min_length=1,
        max_length=50,
        description="List of resource types (RDS, S3, EC2, Lambda, EKS, etc.)",
        examples=[["RDS", "S3"]],
    )
    standards: list[str] = Field(
        default_factory=list,
        max_length=20,
        description="Compliance standards (PCI-DSS, HIPAA, CIS, SOC2, NIST-800-53, ISO-27001, GDPR, FedRAMP, etc.)",
        examples=[["PCI-DSS", "HIPAA"]],
    )
    severity: str | None = Field(
        default=None,
        enum=["CRITICAL", "HIGH", "MEDIUM", "LOW"],
        description="Filter by severity level",
    )
    include_remediation: bool = Field(
        default=True,
        description="Include remediation guidance and code snippets",
    )
    include_verification: bool = Field(
        default=True,
        description="Include verification procedures",
    )


class KnowledgeResearchRequest(BaseModel):
    """Request model for knowledge base research query."""

    query: str = Field(
        ...,
        min_length=10,
        max_length=10000,
        description="Research query in natural language",
        examples=["What are the best practices for securing RDS databases?"],
    )
    domains: list[str] = Field(
        default_factory=list,
        max_length=20,
        description="Filter by domains: compliance, finops, devops, infrastructure, security, architecture",
        examples=[["compliance", "security"]],
    )
    content_types: list[str] = Field(
        default_factory=list,
        max_length=20,
        description="Filter by content types: guide, pattern, strategy, checklist, reference, best_practice",
        examples=[["guide", "best_practice"]],
    )
    include_cross_domain: bool = Field(
        default=True,
        description="Include cross-domain relationships and impacts",
    )
    include_global: bool = Field(
        default=True,
        description="Include global/shared knowledge base content. Set to False to search only user's indexed content.",
    )
    format: str = Field(
        default="structured",
        enum=["structured", "markdown", "executive_summary"],
        description="Response format",
    )
    max_results: int = Field(
        default=1000,
        ge=1,
        le=50000,
        description="Maximum number of results (1-50000). Higher values may take longer to process. Default: 1000.",
    )


class CreateBudgetRequest(BaseModel):
    """Request model for creating infrastructure budget."""

    name: str = Field(..., min_length=1, max_length=200, description="Budget name")
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Budget description",
    )
    scope: dict[str, Any] = Field(
        ...,
        description="Budget scope: {type: 'overall'|'cloud_provider'|'environment', cloud_provider?: str, environment_id?: str, environment_name?: str}. Can combine cloud_provider and environment_id for combined scoping.",
    )
    monthly_limit_usd: float = Field(..., gt=0, description="Monthly budget limit in USD")
    alert_threshold_percent: float = Field(
        default=80.0,
        ge=0,
        le=100,
        description="Alert threshold percentage (default: 80%)",
    )
    critical_threshold_percent: float = Field(
        default=95.0,
        ge=0,
        le=100,
        description="Critical threshold percentage (default: 95%)",
    )
    enforcement_mode: str = Field(
        default="alert",
        description="Enforcement mode: 'alert' or 'enforce' (block)",
    )
    organization_id: Optional[str] = Field(
        default=None,
        description="Organization ID",
    )
    blocking: bool = Field(
        default=False,
        description="Whether to block infrastructure creation when budget is exceeded (deprecated, use enforcement_mode)",
    )


class UpdateBudgetRequest(BaseModel):
    """Request model for updating infrastructure budget."""

    name: Optional[str] = Field(default=None, min_length=1, max_length=200, description="Budget name")
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Budget description",
    )
    monthly_limit_usd: Optional[float] = Field(default=None, gt=0, description="Monthly budget limit in USD")
    alert_threshold_percent: Optional[float] = Field(
        default=None,
        ge=0,
        le=100,
        description="Alert threshold percentage",
    )
    blocking: Optional[bool] = Field(
        default=None,
        description="Whether to block infrastructure creation when budget is exceeded",
    )
    enabled: Optional[bool] = Field(default=None, description="Whether budget is enabled")


class SelectGitHubOrganizationsRequest(BaseModel):
    """Request model for selecting GitHub organizations during OAuth."""

    organization_ids: list[str] = Field(
        ...,
        min_length=1,
        description="List of GitHub organization IDs to grant access to",
    )


class RecordManualSpendingRequest(BaseModel):
    """Request model for recording manual infrastructure spending."""

    amount_usd: float = Field(..., gt=0, description="Spending amount in USD")
    description: str = Field(..., min_length=1, max_length=500, description="Spending description")
    cloud_provider: Optional[str] = Field(
        default=None,
        enum=["aws", "gcp", "azure"],
        description="Cloud provider",
    )
    service: Optional[str] = Field(default=None, max_length=100, description="Cloud service")
    environment_id: Optional[str] = Field(default=None, description="Environment ID")
    environment_name: Optional[str] = Field(default=None, description="Environment name")
    date: Optional[str] = Field(
        default=None,
        description="Date in ISO format (YYYY-MM-DD). Defaults to today.",
    )


class CodebaseSearchRequest(BaseModel):
    """Request model for codebase search."""

    query: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="Natural language search question",
        examples=["How is authentication implemented?"],
    )
    repositories: Optional[list[str]] = Field(
        default=None,
        max_length=50,
        description="List of repositories to search (owner/repo format)",
    )
    resource_ids: Optional[list[str]] = Field(
        default=None,
        max_length=50,
        description="Filter by specific indexed resources",
    )
    resource_types: Optional[list[str]] = Field(
        default=None,
        max_length=10,
        enum=["repository", "documentation", "document"],
        description="Filter by resource type",
    )
    file_types: Optional[list[str]] = Field(
        default=None,
        max_length=20,
        description="Filter by file extensions (.tf, .yaml, .py, .md, etc.)",
    )
    code_type: Optional[str] = Field(
        default=None,
        enum=["terraform", "kubernetes", "docker", "python", "javascript", "yaml"],
        description="Filter by code type",
    )
    cloud_provider: Optional[str] = Field(
        default=None,
        enum=["aws", "gcp", "azure"],
        description="Filter by cloud provider mentioned in code",
    )
    include_sources: bool = Field(
        default=True,
        description="Include source code snippets in results",
    )
    include_ai_analysis: bool = Field(
        default=True,
        description="Include AI-analyzed results with explanations",
    )
    limit: int = Field(default=1000, ge=1, le=1000, description="Maximum number of results (1-1000). Default: 1000.")
    group_by_section: bool = Field(
        default=False,
        description="Group search results by documentation section",
    )
    include_fresh_content: bool = Field(
        default=False,
        description="Fetch fresh content from GitHub for stale results (may increase latency)",
    )
    max_stale_minutes: int = Field(
        default=60,
        ge=1,
        le=10080,  # 7 days max
        description="Consider content stale if older than this many minutes (1-10080). Default: 60.",
    )
    check_freshness: bool = Field(
        default=False,
        description="Check if indexed content is stale compared to repository (adds freshness metadata)",
    )


class PackageSearchRequest(BaseModel):
    """Request model for package search."""

    search_type: str = Field(
        default="semantic",
        enum=["semantic", "regex", "hybrid"],
        description="Search type (semantic, regex, or hybrid)",
    )
    query: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=1000,
        description="Natural language search query (required for semantic/hybrid search)",
        validate_default=False,
    )
    pattern: Optional[str] = Field(
        default=None,
        max_length=10000,
        description="Regex pattern (required for regex/hybrid search)",
    )
    template: Optional[str] = Field(
        default=None,
        enum=[
            "api_key", "password", "secret_key", "token", "credential",
            "terraform_resource", "kubernetes_secret", "import_statement",
        ],
        description="Pre-built regex template (alternative to pattern)",
    )
    registry: Optional[str] = Field(
        default=None,
        enum=["pypi", "npm", "terraform", "crates_io", "golang", "helm", "ansible", "maven", "nuget", "rubygems"],
        description="Filter by registry",
    )
    domain: Optional[str] = Field(
        default=None,
        enum=["devops", "infrastructure", "compliance", "finops", "platform", "sre"],
        description="Filter by domain",
    )
    category: Optional[str] = Field(
        default=None,
        description="Filter by category",
    )
    package_name: Optional[str] = Field(
        default=None,
        description="Search specific package",
    )
    limit: int = Field(default=1000, ge=1, le=1000, description="Maximum number of results (1-1000). Default: 1000.")

    @model_validator(mode="after")
    def validate_search_requirements(self) -> "PackageSearchRequest":
        """Validate that required fields are provided based on search_type."""
        if self.search_type == "semantic":
            if not self.query:
                raise ValueError("query is required for semantic search")
        elif self.search_type == "regex":
            if not self.pattern and not self.template:
                raise ValueError("pattern or template is required for regex search")
        elif self.search_type == "hybrid":
            if not self.query:
                raise ValueError("query is required for hybrid search")
            if not self.pattern and not self.template:
                raise ValueError("pattern or template is required for hybrid search")
        return self


class ArchitectureDesignRequest(BaseModel):
    """Request model for architecture design."""

    action: str = Field(
        ...,
        enum=["initialize", "design", "review", "optimize"],
        description="Action to perform",
    )
    project_type: Optional[str] = Field(
        default=None,
        enum=["terraform", "kubernetes", "devops", "platform"],
        description="Type of project (required for initialize)",
    )
    project_name: Optional[str] = Field(default=None, description="Name of the project (required for initialize)")
    architecture_type: Optional[str] = Field(
        default=None,
        enum=["microservices", "serverless", "monolith", "event-driven"],
        description="Architecture pattern",
    )
    cloud_provider: Optional[str] = Field(
        default=None,
        enum=["aws", "gcp", "azure", "multi-cloud"],
        description="Cloud provider",
    )
    compliance_standards: Optional[list[str]] = Field(
        default=None,
        max_length=10,
        description="Compliance standards to include",
    )
    requirements: Optional[dict[str, Any]] = Field(
        default=None,
        description="Project requirements (scalability, availability, security, cost)",
    )
    existing_architecture: Optional[str] = Field(
        default=None,
        description="Existing architecture code/documentation (for review/optimize)",
    )
    output_directory: Optional[str] = Field(default=".", description="Directory to create project")


class InfrastructureInventoryRequest(BaseModel):
    """Request model for infrastructure inventory."""

    repository_url: str = Field(..., description="GitHub repository URL")
    environment_name: Optional[str] = Field(default=None, description="Environment name")


class InfrastructureManageRequest(BaseModel):
    """Request model for infrastructure management."""

    action: str = Field(
        ...,
        enum=["create", "update", "upgrade", "backup", "restore", "monitor", "optimize"],
        description="Action to perform",
    )
    infrastructure_type: str = Field(
        ...,
        enum=["kubernetes", "multi_cloud", "hybrid_cloud"],
        description="Type of infrastructure",
    )
    resource_name: str = Field(..., description="Name of the resource/cluster")
    cloud_provider: Optional[str] = Field(default=None, description="Cloud provider(s)")
    configuration: Optional[dict[str, Any]] = Field(default=None, description="Infrastructure configuration")
    compliance_standards: Optional[list[str]] = Field(default=None, description="Compliance standards to enforce")
    current_version: Optional[str] = Field(default=None, description="Current version (for upgrade)")
    target_version: Optional[str] = Field(default=None, description="Target version (for upgrade)")
    backup_type: Optional[str] = Field(
        default="full",
        enum=["full", "incremental", "selective"],
        description="Type of backup (for backup action)",
    )


class RegexSearchRequest(BaseModel):
    """Request model for regex search."""

    pattern: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Regex pattern (required if template not provided)",
    )
    template: Optional[str] = Field(
        default=None,
        enum=[
            "api_key",
            "password",
            "secret",
            "token",
            "credential",
            "aws_access_key",
            "aws_secret_key",
            "private_key",
            "ip_address",
            "email",
            "url",
            "credit_card",
            "ssn",
        ],
        description="Pre-built regex template (required if pattern not provided)",
    )
    repositories: Optional[list[str]] = Field(
        default=None,
        max_length=50,
        description="List of repositories to search",
    )
    resource_ids: Optional[list[str]] = Field(
        default=None,
        max_length=50,
        description="Filter by specific indexed resources",
    )
    resource_types: Optional[list[str]] = Field(
        default=None,
        max_length=10,
        enum=["repository", "documentation", "document"],
        description="Filter by resource type",
    )
    file_types: Optional[list[str]] = Field(
        default=None,
        max_length=20,
        description="Filter by file extensions (.tf, .yaml, .py, .md, etc.)",
    )
    code_type: Optional[str] = Field(
        default=None,
        enum=["terraform", "kubernetes", "docker", "python", "javascript", "yaml"],
        description="Filter by code type",
    )
    cloud_provider: Optional[str] = Field(
        default=None,
        enum=["aws", "gcp", "azure"],
        description="Filter by cloud provider mentioned in code",
    )
    case_sensitive: bool = Field(default=False, description="Case-sensitive matching")
    multiline: bool = Field(
        default=False,
        description="Multiline mode (^ and $ match line boundaries)",
    )
    dotall: bool = Field(default=False, description="Dot matches newline")
    include_context: bool = Field(default=True, description="Include surrounding code context")
    context_lines: int = Field(default=3, ge=0, le=10, description="Number of lines before/after match")
    limit: int = Field(default=100, ge=1, le=1000, description="Maximum number of results")
    timeout: float = Field(default=30.0, ge=1.0, le=300.0, description="Maximum search time in seconds")


class WebSearchRequest(BaseModel):
    """Request model for web search."""

    query: str = Field(..., min_length=3, max_length=500, description="Search query")
    search_type: str = Field(
        default="general",
        enum=["general", "security"],
        description="Type of search (general includes web search, security focuses on CVEs/advisories)",
    )
    resource_type: Optional[str] = Field(
        default=None,
        description="Filter by resource type (RDS, S3, EKS, GKE, AKS, etc.)",
    )
    cloud_provider: Optional[str] = Field(
        default=None,
        enum=["aws", "gcp", "azure"],
        description="Filter by cloud provider",
    )
    severity: Optional[str] = Field(
        default=None,
        enum=["CRITICAL", "HIGH", "MEDIUM", "LOW"],
        description="Filter by severity (for security searches)",
    )
    include_cves: bool = Field(default=True, description="Include CVE database results")
    include_advisories: bool = Field(default=True, description="Include security advisories")
    limit: int = Field(default=1000, ge=1, le=1000, description="Maximum number of results (1-1000). Default: 1000.")


class TroubleshootIssueRequest(BaseModel):
    """Request model for troubleshooting infrastructure issues."""

    issue_description: str = Field(..., min_length=10, description="Description of the issue")
    infrastructure_type: Optional[str] = Field(
        default=None,
        enum=["terraform", "kubernetes", "docker", "cloudformation", "ansible"],
        description="Type of infrastructure",
    )
    cloud_provider: Optional[str] = Field(
        default=None,
        enum=["aws", "gcp", "azure"],
        description="Cloud provider",
    )
    error_messages: Optional[list[str]] = Field(default=None, description="List of error messages")
    configuration_code: Optional[str] = Field(default=None, description="Relevant configuration code")
    logs: Optional[str] = Field(default=None, description="Log output")
    resource_type: Optional[str] = Field(default=None, description="Resource type (RDS, S3, EKS, etc.)")


class ReadPackageFileRequest(BaseModel):
    """Request model for reading package files."""

    package_id: str = Field(..., description="Package ID")
    file_path: str = Field(..., description="File path within package")


class ResourceSpecification(BaseModel):
    """Resource specification for cost calculation."""

    cloud: str = Field(
        ...,
        description="Cloud provider (aws, gcp, azure, oracle, alibaba)",
        examples=["aws"],
    )
    service: str = Field(..., description="Service name (rds, ec2, s3, etc.)", examples=["rds"])
    instance_type: str = Field(..., description="Instance type (db.t3.medium, etc.)", examples=["db.t3.medium"])
    quantity: int = Field(default=1, ge=1, description="Quantity", examples=[1])
    region: Optional[str] = Field(
        default=None,
        description="Region ID (us-east-1, us-central1, etc.)",
        examples=["us-east-1"],
    )
    environment: Optional[str] = Field(
        default=None,
        description="Environment name (dev, stage, prod, etc.)",
        examples=["prod"],
    )
    environment_name: Optional[str] = Field(
        default=None,
        description="Environment name (alternative to environment)",
        examples=["prod"],
    )


class PricingCalculationRequest(BaseModel):
    """Request model for infrastructure cost calculation."""

    resources: list[ResourceSpecification] = Field(
        ...,
        min_length=1,
        max_length=100,
        description="List of resource specifications",
        examples=[
            [
                {"cloud": "aws", "service": "rds", "instance_type": "db.t3.medium", "quantity": 1},
                {"cloud": "aws", "service": "ec2", "instance_type": "t3.medium", "quantity": 2},
            ]
        ],
    )
    check_budgets: bool = Field(
        default=True,
        description="Whether to check budgets and enforce limits",
    )
    environment_name: Optional[str] = Field(
        default=None,
        description="Environment name for budget scoping (overrides resource-level environment)",
        examples=["prod"],
    )
    include_existing: bool = Field(
        default=True,
        description="Whether to include existing infrastructure spending in breakdown",
    )


class CodeExamplesSearchRequest(BaseModel):
    """Request model for code examples search."""

    query: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="Search query (e.g., 'RDS database with encryption', 'Kubernetes deployment with autoscaling')",
        examples=["RDS database with encryption"],
    )
    code_types: Optional[list[str]] = Field(
        default=None,
        max_length=20,
        description="Filter by code types (terraform, kubernetes, docker, pulumi, etc.)",
        examples=[["terraform", "kubernetes"]],
    )
    cloud_provider: Optional[str] = Field(
        default=None,
        enum=["aws", "gcp", "azure", "oracle", "alibaba"],
        description="Filter by cloud provider",
    )
    services: Optional[list[str]] = Field(
        default=None,
        max_length=20,
        description="Filter by cloud services (rds, s3, ec2, etc.)",
        examples=[["rds", "s3"]],
    )
    min_quality_score: Optional[int] = Field(
        default=None,
        ge=0,
        le=100,
        description="Minimum quality score (0-100)",
    )
    compliance_standard: Optional[str] = Field(
        default=None,
        enum=["PCI-DSS", "HIPAA", "SOC2", "CIS", "NIST-800-53", "ISO-27001"],
        description="Filter by compliance standard (returns only compliant examples)",
    )
    limit: int = Field(default=1000, ge=1, le=1000, description="Maximum number of results (1-1000). Default: 1000.")
