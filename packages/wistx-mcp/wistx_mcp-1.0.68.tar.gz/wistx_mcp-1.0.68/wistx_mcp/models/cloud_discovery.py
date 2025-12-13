"""Data models for Cloud Resource Discovery feature.

These models define the structure for discovering existing cloud resources
and generating context for AI coding assistants to produce Terraform code.
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class CloudProvider(str, Enum):
    """Supported cloud providers."""
    
    AWS = "aws"
    GCP = "gcp"  # Future
    AZURE = "azure"  # Future


class NameSource(str, Enum):
    """Source of the resolved Terraform name."""
    
    TAGS_NAME = "Tags.Name"
    RESOURCE_NAME = "ResourceName"
    RESOURCE_ID = "ResourceId"
    ARN_DERIVED = "ARN"
    GENERATED = "Generated"


class ImportPhase(str, Enum):
    """Terraform import phases for dependency ordering."""
    
    FOUNDATION = "Foundation"
    NETWORKING = "Networking"
    SECURITY = "Security"
    DATA_LAYER = "DataLayer"
    DATABASES = "Databases"
    LOAD_BALANCING = "LoadBalancing"
    COMPUTE = "Compute"


class NameResolution(BaseModel):
    """Resolution of cloud resource name to valid Terraform identifier."""
    
    terraform_name: str = Field(
        ...,
        description="Valid Terraform resource name (sanitized)",
        min_length=1,
        max_length=255,
    )
    source: NameSource = Field(
        ...,
        description="Where the name was derived from",
    )
    original_cloud_name: str = Field(
        ...,
        description="Original name from cloud provider",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score (1.0 = from Name tag, lower = derived)",
    )


class ComplianceFinding(BaseModel):
    """A compliance finding for a resource."""
    
    control_id: str = Field(..., description="Compliance control ID")
    severity: str = Field(..., description="Severity: critical, high, medium, low")
    message: str = Field(..., description="Description of the finding")
    remediation: str = Field(default="", description="How to remediate")


class ComplianceAssessment(BaseModel):
    """Compliance assessment results for a resource."""
    
    passed: int = Field(default=0, description="Number of passed controls")
    failed: int = Field(default=0, description="Number of failed controls")
    total: int = Field(default=0, description="Total controls assessed")
    findings: list[ComplianceFinding] = Field(
        default_factory=list,
        description="List of compliance findings",
    )


class CostAnalysis(BaseModel):
    """Cost analysis for a resource."""
    
    monthly_estimate: float = Field(
        default=0.0,
        ge=0.0,
        description="Estimated monthly cost in USD",
    )
    currency: str = Field(default="USD", description="Currency code")
    breakdown: dict[str, float] = Field(
        default_factory=dict,
        description="Cost breakdown by component",
    )


class BestPracticeResult(BaseModel):
    """Result of best practice evaluation."""
    
    rule_id: str = Field(..., description="Best practice rule ID")
    status: str = Field(..., description="pass, fail, or warning")
    message: str = Field(default="", description="Description")


class ResourceDependency(BaseModel):
    """A dependency relationship between resources."""
    
    source_id: str = Field(..., description="Source resource cloud ID")
    target_id: str = Field(..., description="Target resource cloud ID (depends on)")
    dependency_type: str = Field(
        ...,
        description="Type: vpc_membership, subnet_placement, security_group, etc.",
    )


class DiscoveredResource(BaseModel):
    """A discovered cloud resource with all enrichment data."""

    # Core identification
    cloud_provider: CloudProvider = Field(
        default=CloudProvider.AWS,
        description="Cloud provider (AWS, Azure, GCP)",
    )
    cloud_resource_id: str = Field(
        ...,
        description="Cloud provider resource ID (e.g., i-0abc123)",
    )
    cloud_resource_type: str = Field(
        ...,
        description="Cloud provider type (e.g., AWS::EC2::Instance)",
    )
    terraform_resource_type: str = Field(
        default="",
        description="Terraform resource type (e.g., aws_instance)",
    )
    terraform_import_id: str | None = Field(
        default=None,
        description="ID to use with terraform import command",
    )

    # Name resolution (populated after discovery)
    name_resolution: NameResolution | None = Field(
        default=None,
        description="How the Terraform name was resolved",
    )
    name: str | None = Field(
        default=None,
        description="Human-readable name from tags or identifier",
    )

    # Location
    region: str | None = Field(default=None, description="Cloud region")
    availability_zone: str | None = Field(
        default=None,
        description="Availability zone if applicable",
    )
    
    # Metadata
    tags: dict[str, str] = Field(
        default_factory=dict,
        description="Resource tags",
    )
    arn: str | None = Field(
        default=None,
        description="AWS ARN if applicable",
    )
    
    # Configuration
    raw_config: dict[str, Any] = Field(
        default_factory=dict,
        description="Raw configuration from cloud provider API",
    )
    provider_specific_config: dict[str, Any] = Field(
        default_factory=dict,
        description="Provider-specific configuration details",
    )
    normalized_config: dict[str, Any] = Field(
        default_factory=dict,
        description="Normalized config for Terraform",
    )

    # Import ordering
    import_phase: ImportPhase = Field(
        default=ImportPhase.COMPUTE,
        description="Which phase this resource should be imported in",
    )
    import_order: int = Field(
        default=999,
        description="Order within the phase",
    )

    # Dependencies
    depends_on: list[str] = Field(
        default_factory=list,
        description="List of resource IDs this resource depends on",
    )

    # Enrichment (optional - populated when requested)
    compliance_assessment: ComplianceAssessment | None = Field(
        default=None,
        description="Compliance assessment if requested",
    )
    cost_analysis: CostAnalysis | None = Field(
        default=None,
        description="Cost analysis if requested",
    )
    best_practices: list[BestPracticeResult] | None = Field(
        default=None,
        description="Best practices evaluation if requested",
    )

    # Timestamps
    discovered_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the resource was discovered",
    )


class DependencyGraph(BaseModel):
    """Directed Acyclic Graph of resource dependencies."""

    nodes: list[str] = Field(
        default_factory=list,
        description="List of resource IDs (nodes in the graph)",
    )
    edges: list[ResourceDependency] = Field(
        default_factory=list,
        description="Dependency edges",
    )
    topological_order: list[str] = Field(
        default_factory=list,
        description="Resources in dependency order (import order)",
    )
    phases: dict[str, list[str]] = Field(
        default_factory=dict,
        description="Resources grouped by import phase",
    )
    has_cycles: bool = Field(
        default=False,
        description="True if circular dependencies detected",
    )
    cycle_details: list[list[str]] | None = Field(
        default=None,
        description="Details of circular dependencies if any",
    )


class AWSConnection(BaseModel):
    """AWS connection configuration using AssumeRole."""

    role_arn: str = Field(
        ...,
        description="ARN of the IAM role to assume",
        pattern=r"^arn:aws:iam::\d{12}:role/[\w+=,.@-]+$",
    )
    external_id: str = Field(
        ...,
        description="External ID for secure cross-account access",
        min_length=10,
        max_length=1224,
    )
    session_name: str = Field(
        default="wistx-discovery",
        description="Session name for CloudTrail auditing",
        max_length=64,
    )
    duration_seconds: int = Field(
        default=3600,
        ge=900,
        le=43200,
        description="Session duration (15 min to 12 hours)",
    )


class DiscoveryRequest(BaseModel):
    """Request to discover cloud resources."""

    cloud_provider: CloudProvider = Field(
        ...,
        description="Cloud provider to discover resources from",
    )

    # AWS-specific connection
    aws_connection: AWSConnection | None = Field(
        default=None,
        description="AWS connection details (required for AWS)",
    )

    # Discovery scope
    regions: list[str] = Field(
        default_factory=list,
        description="Regions to scan (empty = all regions)",
    )
    resource_types: list[str] | None = Field(
        default=None,
        description="Filter by resource types (None = all supported)",
    )
    tag_filters: dict[str, str] | None = Field(
        default=None,
        description="Filter by tags (e.g., {'Environment': 'production'})",
    )

    # Enrichment options
    compliance_standards: list[str] | None = Field(
        default=None,
        description="Compliance standards to check (e.g., ['SOC2', 'HIPAA'])",
    )
    include_pricing: bool = Field(
        default=False,
        description="Include cost analysis",
    )
    include_best_practices: bool = Field(
        default=False,
        description="Include best practices evaluation",
    )

    # Output options
    generate_diagrams: bool = Field(
        default=True,
        description="Generate infrastructure diagrams",
    )
    diagram_types: list[str] = Field(
        default_factory=lambda: [
            "system_overview",
            "networking",
            "security",
            "dependencies",
        ],
        description="Types of diagrams to generate",
    )


class InfrastructureDiagram(BaseModel):
    """A generated infrastructure diagram."""

    diagram_type: str = Field(..., description="Type of diagram")
    title: str = Field(..., description="Diagram title")
    description: str = Field(default="", description="What the diagram shows")
    mermaid_code: str = Field(..., description="Mermaid diagram code")
    resource_count: int = Field(default=0, description="Resources in diagram")


class DiscoverySummary(BaseModel):
    """Summary statistics for the discovery operation."""

    total_resources: int = Field(default=0)
    by_type: dict[str, int] = Field(default_factory=dict)
    by_region: dict[str, int] = Field(default_factory=dict)
    by_phase: dict[str, int] = Field(default_factory=dict)
    discovery_duration_seconds: float = Field(default=0.0)


class ComplianceSummary(BaseModel):
    """Summary of compliance assessment across all resources."""

    total_controls: int = Field(default=0)
    passed: int = Field(default=0)
    failed: int = Field(default=0)
    by_standard: dict[str, dict[str, int]] = Field(default_factory=dict)
    by_severity: dict[str, int] = Field(default_factory=dict)


class CostSummary(BaseModel):
    """Summary of cost analysis across all resources."""

    total_monthly_estimate: float = Field(default=0.0)
    currency: str = Field(default="USD")
    by_service: dict[str, float] = Field(default_factory=dict)
    by_region: dict[str, float] = Field(default_factory=dict)


class TerraformProjectStructure(BaseModel):
    """Recommended Terraform project structure."""

    project_root: str = Field(default="terraform")
    environments: list[str] = Field(
        default_factory=lambda: ["dev", "staging", "prod"],
    )
    modules: list[str] = Field(default_factory=list)
    import_scripts: dict[str, str] = Field(
        default_factory=dict,
        description="Import scripts by phase",
    )
    file_structure: dict[str, Any] = Field(
        default_factory=dict,
        description="Recommended file structure",
    )


class DiscoveryResponse(BaseModel):
    """Complete response from cloud resource discovery."""

    # Request echo
    request_id: str = Field(..., description="Unique request ID")
    cloud_provider: CloudProvider = Field(..., description="Cloud provider")

    # Discovered resources
    discovered_resources: list[DiscoveredResource] = Field(
        default_factory=list,
        description="All discovered resources with enrichment",
    )

    # Dependency analysis
    dependency_graph: DependencyGraph = Field(
        default_factory=DependencyGraph,
        description="Resource dependency graph",
    )

    # Diagrams
    infrastructure_diagrams: list[InfrastructureDiagram] = Field(
        default_factory=list,
        description="Generated infrastructure diagrams",
    )

    # Summaries
    discovery_summary: DiscoverySummary = Field(
        default_factory=DiscoverySummary,
        description="Discovery statistics",
    )
    compliance_summary: ComplianceSummary | None = Field(
        default=None,
        description="Compliance summary if requested",
    )
    cost_summary: CostSummary | None = Field(
        default=None,
        description="Cost summary if requested",
    )

    # Terraform project recommendation
    terraform_project: TerraformProjectStructure = Field(
        default_factory=TerraformProjectStructure,
        description="Recommended Terraform project structure",
    )

    # Metadata
    discovered_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When discovery completed",
    )
    warnings: list[str] = Field(
        default_factory=list,
        description="Any warnings during discovery",
    )
    errors: list[str] = Field(
        default_factory=list,
        description="Any errors during discovery",
    )

