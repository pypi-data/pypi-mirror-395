"""Cost Intelligence Data Models.

FOCUS-compliant data models for cost records, anomalies, forecasts,
and optimization recommendations.

These models are designed to provide rich cost context to AI coding
assistants during infrastructure code generation.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class AnomalySeverity(str, Enum):
    """Cost anomaly severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RecommendationType(str, Enum):
    """Types of cost optimization recommendations."""
    RESERVED_INSTANCE = "reserved_instance"
    SAVINGS_PLAN = "savings_plan"
    SPOT_INSTANCE = "spot_instance"
    RIGHTSIZING = "rightsizing"
    AUTO_SCALING = "auto_scaling"
    STORAGE_TIERING = "storage_tiering"
    REGION_OPTIMIZATION = "region_optimization"
    INSTANCE_FAMILY_UPGRADE = "instance_family_upgrade"
    IDLE_RESOURCE = "idle_resource"
    SCHEDULED_SCALING = "scheduled_scaling"


class RecommendationStrength(str, Enum):
    """How strongly we recommend the optimization."""
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"


@dataclass
class CostRecord:
    """FOCUS-compliant cost record from cloud billing.
    
    Follows the FinOps Open Cost and Usage Specification (FOCUS) v1.0.
    """
    # Identifiers
    billing_account_id: str
    billing_period_start: datetime
    billing_period_end: datetime
    
    # Resource identification
    resource_id: str
    resource_name: str | None = None
    resource_type: str | None = None
    
    # Service identification
    provider_name: str = "aws"  # aws, gcp, azure
    service_name: str | None = None
    service_category: str | None = None  # compute, storage, database, network
    
    # Location
    region: str | None = None
    availability_zone: str | None = None
    
    # Cost
    billed_cost: float = 0.0
    effective_cost: float = 0.0  # After discounts
    list_cost: float = 0.0  # Before discounts
    
    # Usage
    usage_quantity: float = 0.0
    usage_unit: str | None = None
    pricing_quantity: float = 0.0
    pricing_unit: str | None = None
    
    # Pricing
    pricing_category: str | None = None  # on_demand, reserved, spot, savings_plan
    commitment_discount_id: str | None = None
    
    # Tags for allocation
    tags: dict[str, str] = field(default_factory=dict)
    
    # WISTX extensions
    environment: str | None = None  # Inferred: dev, staging, production
    project: str | None = None  # Inferred from tags or naming


@dataclass
class CostAnomaly:
    """Detected cost anomaly."""
    anomaly_id: str
    detected_at: datetime
    anomaly_type: str  # spike, drop, trend_change
    severity: AnomalySeverity
    
    # Cost details
    expected_spend: float
    actual_spend: float
    deviation_amount: float
    deviation_percent: float
    
    # Context
    service_name: str | None = None
    resource_id: str | None = None
    region: str | None = None
    
    # Analysis
    root_cause_analysis: str | None = None
    contributing_factors: list[str] = field(default_factory=list)
    
    # Source
    source: str = "wistx"  # wistx, aws_anomaly_detection


@dataclass
class DailyForecast:
    """Single day in a cost forecast."""
    date: datetime
    predicted_cost: float
    lower_bound: float  # 80% CI lower
    upper_bound: float  # 80% CI upper
    confidence: float


@dataclass
class CostForecast:
    """Cost forecast with confidence intervals."""
    forecast_id: str
    generated_at: datetime
    forecast_start: datetime
    forecast_end: datetime
    
    # Predictions
    daily_forecasts: list[DailyForecast] = field(default_factory=list)
    predicted_monthly_total: float = 0.0
    
    # Confidence
    confidence_level: float = 0.8  # 80% confidence
    lower_bound_monthly: float = 0.0
    upper_bound_monthly: float = 0.0
    
    # Budget impact
    current_budget: float | None = None
    budget_remaining: float | None = None
    budget_exceedance_date: datetime | None = None
    days_until_exceeded: int | None = None
    
    # Planned changes impact
    planned_changes_impact: float = 0.0
    forecast_with_changes: float | None = None
    
    # Source
    source: str = "wistx"  # wistx, aws_cost_explorer


@dataclass
class OptimizationRecommendation:
    """Cost optimization recommendation.

    Context-aware, specific recommendations - not generic advice.
    """
    recommendation_id: str
    recommendation_type: RecommendationType
    title: str
    description: str

    # Savings
    estimated_monthly_savings: float
    estimated_annual_savings: float
    savings_percentage: float

    # Confidence
    confidence: float  # 0.0 to 1.0
    strength: RecommendationStrength

    # Action
    action_required: str
    implementation_effort: str  # low, medium, high
    risk_level: str  # low, medium, high

    # Context
    affected_resources: list[str] = field(default_factory=list)
    prerequisites: list[str] = field(default_factory=list)
    trade_offs: list[str] = field(default_factory=list)

    # Suitability
    suitable_for: list[str] = field(default_factory=list)  # use cases
    not_suitable_for: list[str] = field(default_factory=list)


@dataclass
class CostAlternative:
    """A cost-optimized alternative to requested resources.

    Generated during code generation to help AI assistants suggest
    budget-compliant infrastructure options.
    """
    alternative_id: str
    name: str
    description: str

    # Resources
    resources: list[dict[str, Any]] = field(default_factory=list)

    # Cost comparison
    monthly_cost: float = 0.0
    original_cost: float = 0.0
    savings_amount: float = 0.0
    savings_percentage: float = 0.0

    # Recommendation
    strength: RecommendationStrength = RecommendationStrength.MODERATE

    # Trade-offs
    trade_offs: list[str] = field(default_factory=list)
    benefits: list[str] = field(default_factory=list)

    # Suitability
    suitable_for: list[str] = field(default_factory=list)
    not_suitable_for: list[str] = field(default_factory=list)


@dataclass
class ResourceCostBreakdown:
    """Cost breakdown for a single resource."""
    resource_name: str
    cloud_provider: str
    service: str
    instance_type: str | None = None
    region: str | None = None
    quantity: int = 1

    # Costs
    hourly_cost: float = 0.0
    daily_cost: float = 0.0
    monthly_cost: float = 0.0
    annual_cost: float = 0.0

    # Pricing details
    pricing_category: str | None = None  # on_demand, reserved, spot
    pricing_tier: str | None = None

    # Notes
    notes: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class BudgetStatus:
    """Current budget status for context."""
    budget_id: str
    budget_name: str
    budget_amount: float

    # Current state
    total_spent: float
    remaining: float
    utilization_percent: float

    # Enforcement
    enforcement_mode: str  # alert, warn, block
    is_exceeded: bool = False
    will_exceed_with_new: bool = False
    exceeded_by: float | None = None

    # Alerts
    alert_thresholds: list[float] = field(default_factory=list)
    triggered_alerts: list[str] = field(default_factory=list)


@dataclass
class UnitEconomics:
    """Unit economics breakdown for cost efficiency analysis."""
    # Cost per environment
    cost_per_environment: dict[str, float] = field(default_factory=dict)

    # Cost per cloud
    cost_per_cloud: dict[str, float] = field(default_factory=dict)

    # Cost per service category
    cost_per_service_category: dict[str, float] = field(default_factory=dict)

    # Efficiency metrics
    dev_to_prod_ratio: float | None = None  # Ideally <0.5
    non_prod_percentage: float | None = None
    reserved_coverage: float | None = None  # % covered by commitments
    spot_utilization: float | None = None

    # Trends
    cost_trend: str | None = None  # increasing, stable, decreasing
    month_over_month_change: float | None = None


@dataclass
class ReservationUtilization:
    """Reserved Instance / Savings Plan utilization."""
    utilization_percentage: float
    coverage_percentage: float

    # Breakdown
    total_reserved_hours: float = 0.0
    used_hours: float = 0.0
    unused_hours: float = 0.0

    # Savings
    total_potential_savings: float = 0.0
    realized_savings: float = 0.0
    missed_savings: float = 0.0

    # Recommendations
    underutilized_reservations: list[str] = field(default_factory=list)


@dataclass
class RightsizingRecommendation:
    """AWS Rightsizing recommendation."""
    resource_id: str
    resource_type: str
    region: str

    # Current
    current_instance_type: str
    current_monthly_cost: float

    # Recommended
    recommended_instance_type: str
    recommended_monthly_cost: float

    # Savings
    savings_amount: float
    savings_percentage: float

    # Metrics
    cpu_utilization_avg: float | None = None
    memory_utilization_avg: float | None = None

    # Risk
    risk: str = "medium"  # low, medium, high


@dataclass
class CostContext:
    """Rich cost context for AI coding assistants.

    This is THE key differentiator - providing comprehensive cost
    intelligence during code generation, not post-deployment.
    """
    # Request identification
    context_id: str
    generated_at: datetime
    user_id: str

    # Basic cost estimates
    estimated_monthly_cost: float = 0.0
    estimated_annual_cost: float = 0.0
    cost_breakdown: list[ResourceCostBreakdown] = field(default_factory=list)

    # Budget integration
    budget_status: BudgetStatus | None = None
    budget_remaining: float | None = None
    budget_will_exceed: bool = False
    budget_exceeded_by: float | None = None

    # Cost-optimized alternatives (THE KEY DIFFERENTIATOR)
    alternatives: list[CostAlternative] = field(default_factory=list)

    # Intelligent recommendations
    optimization_recommendations: list[OptimizationRecommendation] = field(
        default_factory=list
    )

    # Anomaly awareness
    recent_anomalies: list[CostAnomaly] = field(default_factory=list)
    anomaly_risk: str = "low"  # low, medium, high

    # Forecast impact
    forecast: CostForecast | None = None
    current_monthly_forecast: float | None = None
    forecast_with_new_resources: float | None = None

    # Historical context
    similar_resources_avg_cost: float | None = None
    cost_trend: str | None = None  # increasing, stable, decreasing

    # Unit economics
    unit_economics: UnitEconomics | None = None

