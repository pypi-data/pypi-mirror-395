"""Unit Economics Service.

Provides cost-per-unit metrics for infrastructure cost analysis.
Enables understanding of cost efficiency across deployments, environments,
teams, and features.

Industry Comparison:
- CloudZero: Strong unit economics, but dashboard-focused
- Finout: Good unit cost metrics
- WISTX: Real-time unit economics integrated into code generation context
"""

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any
from statistics import mean

from wistx_mcp.tools.lib.cost_intelligence.models import (
    CostRecord,
    UnitEconomics,
)

logger = logging.getLogger(__name__)


class CostUnit(str, Enum):
    """Types of cost units for analysis."""
    DEPLOYMENT = "deployment"
    ENVIRONMENT = "environment"
    TEAM = "team"
    SERVICE = "service"
    FEATURE = "feature"
    PROJECT = "project"
    CUSTOMER = "customer"  # For multi-tenant


class EfficiencyRating(str, Enum):
    """Efficiency rating levels."""
    EXCELLENT = "excellent"  # Top 10%
    GOOD = "good"  # Top 25%
    AVERAGE = "average"  # Middle 50%
    BELOW_AVERAGE = "below_average"  # Bottom 25%
    POOR = "poor"  # Bottom 10%


@dataclass
class CostPerUnit:
    """Cost breakdown for a specific unit."""
    unit_type: CostUnit
    unit_id: str
    unit_name: str
    
    # Cost metrics
    total_cost: float
    daily_average: float
    cost_trend: str  # increasing, stable, decreasing
    trend_percentage: float
    
    # Efficiency
    efficiency_score: float  # 0-100
    efficiency_rating: EfficiencyRating
    
    # Breakdown
    cost_by_service: dict[str, float] = field(default_factory=dict)
    cost_by_resource_type: dict[str, float] = field(default_factory=dict)
    
    # Benchmarks
    vs_average: float = 0.0  # % above/below average
    vs_best: float = 0.0  # % above best performer
    
    # Optimization potential
    estimated_savings_potential: float = 0.0
    optimization_opportunities: list[str] = field(default_factory=list)


@dataclass
class TeamCostAllocation:
    """Cost allocation for a team."""
    team_id: str
    team_name: str
    
    # Direct costs (resources with team tag)
    direct_costs: float
    
    # Shared costs (allocated based on usage)
    shared_costs: float
    
    # Total
    total_costs: float
    
    # Breakdown
    environments: dict[str, float] = field(default_factory=dict)
    services: dict[str, float] = field(default_factory=dict)
    
    # Efficiency
    cost_per_engineer: float | None = None
    cost_per_deployment: float | None = None


@dataclass
class EnvironmentCostBreakdown:
    """Cost breakdown by environment."""
    environment: str  # production, staging, development, etc.
    
    total_cost: float
    percentage_of_total: float
    
    # Resource counts
    resource_count: int
    
    # Efficiency metrics
    cost_per_resource: float
    utilization_estimate: float  # Estimated based on patterns
    
    # Recommendations
    is_oversized: bool = False
    recommended_action: str | None = None


@dataclass
class DeploymentCost:
    """Cost tracking for a deployment."""
    deployment_id: str
    deployment_name: str | None
    deployed_at: datetime
    
    # Resources
    resources: list[str]
    resource_count: int
    
    # Costs
    estimated_monthly_cost: float
    actual_cost_to_date: float
    cost_per_day: float
    
    # Comparison
    vs_previous_deployment: float | None = None  # % change
    
    # Tags
    environment: str | None = None
    team: str | None = None
    project: str | None = None


class UnitEconomicsService:
    """Service for calculating unit economics and cost allocation.
    
    Provides:
    1. Cost per deployment tracking
    2. Cost per environment analysis
    3. Team cost allocation
    4. Service cost breakdown
    5. Efficiency benchmarking
    """
    
    # Industry benchmarks (from FinOps Foundation research)
    BENCHMARKS = {
        "dev_to_prod_ratio": 0.3,  # Dev should be <30% of prod
        "staging_to_prod_ratio": 0.15,  # Staging <15% of prod
        "reserved_coverage_target": 0.7,  # 70% commitment coverage
        "spot_utilization_target": 0.3,  # 30% spot for non-prod
        "idle_resource_threshold": 0.1,  # <10% idle acceptable
    }

    def __init__(self):
        """Initialize the unit economics service."""
        self._cost_records: list[CostRecord] = []

    def calculate_environment_costs(
        self,
        cost_records: list[CostRecord],
        environment_tag_key: str = "Environment",
    ) -> list[EnvironmentCostBreakdown]:
        """Calculate cost breakdown by environment.

        Args:
            cost_records: List of cost records
            environment_tag_key: Tag key used for environment identification

        Returns:
            List of environment cost breakdowns
        """
        # Group costs by environment
        env_costs: dict[str, list[CostRecord]] = {}

        for record in cost_records:
            env = self._extract_environment(record, environment_tag_key)
            if env not in env_costs:
                env_costs[env] = []
            env_costs[env].append(record)

        # Calculate totals
        total_cost = sum(r.billed_cost for r in cost_records)

        breakdowns = []
        for env, records in env_costs.items():
            env_total = sum(r.billed_cost for r in records)
            resource_ids = set(r.resource_id for r in records if r.resource_id)

            # Estimate utilization based on environment type
            utilization = self._estimate_utilization(env)

            # Check if oversized
            is_oversized = False
            recommended_action = None

            if env.lower() in ["development", "dev"]:
                prod_cost = sum(
                    r.billed_cost for r in cost_records
                    if self._extract_environment(r, environment_tag_key).lower() in ["production", "prod"]
                )
                if prod_cost > 0 and env_total / prod_cost > self.BENCHMARKS["dev_to_prod_ratio"]:
                    is_oversized = True
                    recommended_action = (
                        f"Development costs are {env_total/prod_cost*100:.0f}% of production. "
                        f"Target: <{self.BENCHMARKS['dev_to_prod_ratio']*100:.0f}%. "
                        "Consider using smaller instances or spot instances."
                    )

            breakdowns.append(EnvironmentCostBreakdown(
                environment=env,
                total_cost=env_total,
                percentage_of_total=(env_total / total_cost * 100) if total_cost > 0 else 0,
                resource_count=len(resource_ids),
                cost_per_resource=env_total / len(resource_ids) if resource_ids else 0,
                utilization_estimate=utilization,
                is_oversized=is_oversized,
                recommended_action=recommended_action,
            ))

        # Sort by cost descending
        breakdowns.sort(key=lambda x: x.total_cost, reverse=True)
        return breakdowns

    def calculate_team_costs(
        self,
        cost_records: list[CostRecord],
        team_tag_key: str = "Team",
        shared_services: list[str] | None = None,
    ) -> list[TeamCostAllocation]:
        """Calculate cost allocation by team.

        Args:
            cost_records: List of cost records
            team_tag_key: Tag key used for team identification
            shared_services: List of service names that are shared costs

        Returns:
            List of team cost allocations
        """
        shared_services = shared_services or ["networking", "monitoring", "security"]

        # Separate direct and shared costs
        team_direct: dict[str, list[CostRecord]] = {}
        shared_costs: list[CostRecord] = []

        for record in cost_records:
            team = self._extract_tag(record, team_tag_key)
            service = record.service_name or "unknown"

            if service.lower() in [s.lower() for s in shared_services]:
                shared_costs.append(record)
            elif team:
                if team not in team_direct:
                    team_direct[team] = []
                team_direct[team].append(record)
            else:
                # Untagged resources go to "unallocated"
                if "unallocated" not in team_direct:
                    team_direct["unallocated"] = []
                team_direct["unallocated"].append(record)

        # Calculate shared cost per team (proportional to direct costs)
        total_direct = sum(
            sum(r.billed_cost for r in records)
            for records in team_direct.values()
        )
        total_shared = sum(r.billed_cost for r in shared_costs)

        allocations = []
        for team, records in team_direct.items():
            direct_cost = sum(r.billed_cost for r in records)

            # Allocate shared costs proportionally
            share_ratio = direct_cost / total_direct if total_direct > 0 else 0
            allocated_shared = total_shared * share_ratio

            # Calculate breakdowns
            env_breakdown: dict[str, float] = {}
            service_breakdown: dict[str, float] = {}

            for record in records:
                env = self._extract_environment(record, "Environment")
                service = record.service_name or "unknown"

                env_breakdown[env] = env_breakdown.get(env, 0) + record.billed_cost
                service_breakdown[service] = service_breakdown.get(service, 0) + record.billed_cost

            allocations.append(TeamCostAllocation(
                team_id=team.lower().replace(" ", "_"),
                team_name=team,
                direct_costs=direct_cost,
                shared_costs=allocated_shared,
                total_costs=direct_cost + allocated_shared,
                environments=env_breakdown,
                services=service_breakdown,
            ))

        # Sort by total cost descending
        allocations.sort(key=lambda x: x.total_costs, reverse=True)
        return allocations

    def calculate_deployment_cost(
        self,
        deployment_id: str,
        resources: list[dict[str, Any]],
        cost_records: list[CostRecord],
        deployment_name: str | None = None,
        deployed_at: datetime | None = None,
    ) -> DeploymentCost:
        """Calculate cost for a specific deployment.

        Args:
            deployment_id: Unique identifier for the deployment
            resources: List of resources in the deployment
            cost_records: Cost records for the resources
            deployment_name: Optional deployment name
            deployed_at: Deployment timestamp

        Returns:
            Deployment cost breakdown
        """
        deployed_at = deployed_at or datetime.now(timezone.utc)

        # Get resource IDs
        resource_ids = [r.get("resource_id", r.get("id", "")) for r in resources]

        # Filter cost records for these resources
        deployment_records = [
            r for r in cost_records
            if r.resource_id in resource_ids
        ]

        # Calculate costs
        total_cost = sum(r.billed_cost for r in deployment_records)

        # Calculate days since deployment
        days_since = max(1, (datetime.now(timezone.utc) - deployed_at).days)
        cost_per_day = total_cost / days_since

        # Estimate monthly cost
        estimated_monthly = cost_per_day * 30

        # Extract tags
        environment = None
        team = None
        project = None

        for resource in resources:
            tags = resource.get("tags", {})
            if not environment:
                environment = tags.get("Environment", tags.get("environment"))
            if not team:
                team = tags.get("Team", tags.get("team"))
            if not project:
                project = tags.get("Project", tags.get("project"))

        return DeploymentCost(
            deployment_id=deployment_id,
            deployment_name=deployment_name,
            deployed_at=deployed_at,
            resources=resource_ids,
            resource_count=len(resource_ids),
            estimated_monthly_cost=estimated_monthly,
            actual_cost_to_date=total_cost,
            cost_per_day=cost_per_day,
            environment=environment,
            team=team,
            project=project,
        )

    def calculate_service_costs(
        self,
        cost_records: list[CostRecord],
    ) -> dict[str, CostPerUnit]:
        """Calculate cost breakdown by service.

        Args:
            cost_records: List of cost records

        Returns:
            Dictionary of service name to cost breakdown
        """
        # Group by service
        service_costs: dict[str, list[CostRecord]] = {}

        for record in cost_records:
            service = record.service_name or "unknown"
            if service not in service_costs:
                service_costs[service] = []
            service_costs[service].append(record)

        # Calculate totals for benchmarking
        total_cost = sum(r.billed_cost for r in cost_records)
        service_totals = {
            svc: sum(r.billed_cost for r in records)
            for svc, records in service_costs.items()
        }
        avg_service_cost = mean(service_totals.values()) if service_totals else 0
        best_service_cost = min(service_totals.values()) if service_totals else 0

        results = {}
        for service, records in service_costs.items():
            svc_total = service_totals[service]

            # Calculate daily average
            dates = set(r.billing_period_start.date() for r in records)
            days = len(dates) or 1
            daily_avg = svc_total / days

            # Calculate trend
            trend, trend_pct = self._calculate_trend(records)

            # Calculate efficiency score (based on cost optimization potential)
            efficiency_score = self._calculate_efficiency_score(records)
            efficiency_rating = self._get_efficiency_rating(efficiency_score)

            # Benchmark comparisons
            vs_average = ((svc_total - avg_service_cost) / avg_service_cost * 100) if avg_service_cost > 0 else 0
            vs_best = ((svc_total - best_service_cost) / best_service_cost * 100) if best_service_cost > 0 else 0

            # Resource type breakdown
            resource_types: dict[str, float] = {}
            for record in records:
                rt = record.resource_type or "unknown"
                resource_types[rt] = resource_types.get(rt, 0) + record.billed_cost

            results[service] = CostPerUnit(
                unit_type=CostUnit.SERVICE,
                unit_id=service.lower().replace(" ", "_"),
                unit_name=service,
                total_cost=svc_total,
                daily_average=daily_avg,
                cost_trend=trend,
                trend_percentage=trend_pct,
                efficiency_score=efficiency_score,
                efficiency_rating=efficiency_rating,
                cost_by_resource_type=resource_types,
                vs_average=vs_average,
                vs_best=vs_best,
            )

        return results

    def generate_unit_economics_summary(
        self,
        cost_records: list[CostRecord],
    ) -> UnitEconomics:
        """Generate comprehensive unit economics summary.

        Args:
            cost_records: List of cost records

        Returns:
            UnitEconomics summary
        """
        # Environment costs
        env_breakdowns = self.calculate_environment_costs(cost_records)
        cost_per_env = {e.environment: e.total_cost for e in env_breakdowns}

        # Cloud costs
        cloud_costs: dict[str, float] = {}
        for record in cost_records:
            cloud = record.provider_name or "unknown"
            cloud_costs[cloud] = cloud_costs.get(cloud, 0) + record.billed_cost

        # Service category costs
        service_costs = self.calculate_service_costs(cost_records)
        cost_per_category = {
            svc: data.total_cost for svc, data in service_costs.items()
        }

        # Calculate efficiency metrics
        prod_cost = cost_per_env.get("production", cost_per_env.get("prod", 0))
        dev_cost = cost_per_env.get("development", cost_per_env.get("dev", 0))

        dev_to_prod = dev_cost / prod_cost if prod_cost > 0 else None

        total_cost = sum(cost_per_env.values())
        non_prod = sum(
            cost for env, cost in cost_per_env.items()
            if env.lower() not in ["production", "prod"]
        )
        non_prod_pct = (non_prod / total_cost * 100) if total_cost > 0 else None

        # Calculate trend
        trend, mom_change = self._calculate_trend(cost_records)

        return UnitEconomics(
            cost_per_environment=cost_per_env,
            cost_per_cloud=cloud_costs,
            cost_per_service_category=cost_per_category,
            dev_to_prod_ratio=dev_to_prod,
            non_prod_percentage=non_prod_pct,
            cost_trend=trend,
            month_over_month_change=mom_change,
        )

    def _extract_environment(
        self,
        record: CostRecord,
        tag_key: str = "Environment",
    ) -> str:
        """Extract environment from record tags."""
        if record.tags:
            # Try exact match
            if tag_key in record.tags:
                return record.tags[tag_key]
            # Try case-insensitive
            for key, value in record.tags.items():
                if key.lower() == tag_key.lower():
                    return value
        return "untagged"

    def _extract_tag(
        self,
        record: CostRecord,
        tag_key: str,
    ) -> str | None:
        """Extract a tag value from record."""
        if record.tags:
            if tag_key in record.tags:
                return record.tags[tag_key]
            for key, value in record.tags.items():
                if key.lower() == tag_key.lower():
                    return value
        return None

    def _estimate_utilization(self, environment: str) -> float:
        """Estimate utilization based on environment type."""
        env_lower = environment.lower()

        # Industry average utilization by environment type
        utilization_estimates = {
            "production": 0.65,
            "prod": 0.65,
            "staging": 0.35,
            "stage": 0.35,
            "development": 0.20,
            "dev": 0.20,
            "test": 0.15,
            "qa": 0.25,
            "sandbox": 0.10,
        }

        return utilization_estimates.get(env_lower, 0.30)

    def _calculate_trend(
        self,
        records: list[CostRecord],
    ) -> tuple[str, float]:
        """Calculate cost trend from records."""
        if len(records) < 7:
            return "insufficient_data", 0.0

        # Group by day
        daily: dict[str, float] = {}
        for record in records:
            date_key = record.billing_period_start.strftime("%Y-%m-%d")
            daily[date_key] = daily.get(date_key, 0) + record.billed_cost

        if len(daily) < 7:
            return "insufficient_data", 0.0

        # Sort by date
        sorted_days = sorted(daily.items())

        # Compare recent half to older half
        mid = len(sorted_days) // 2
        older = mean([c for _, c in sorted_days[:mid]])
        recent = mean([c for _, c in sorted_days[mid:]])

        if older == 0:
            return "stable", 0.0

        change_pct = ((recent - older) / older) * 100

        if change_pct > 10:
            return "increasing", change_pct
        elif change_pct < -10:
            return "decreasing", change_pct
        else:
            return "stable", change_pct

    def _calculate_efficiency_score(
        self,
        records: list[CostRecord],
    ) -> float:
        """Calculate efficiency score (0-100) based on optimization potential."""
        if not records:
            return 50.0  # Neutral score

        score = 70.0  # Start with a base score

        # Check for tagging (good tagging = higher efficiency)
        tagged_count = sum(1 for r in records if r.tags)
        tag_ratio = tagged_count / len(records)
        score += tag_ratio * 10  # Up to +10 for full tagging

        # Check for commitment coverage (via pricing_quantity)
        commitment_count = sum(
            1 for r in records
            if r.pricing_quantity and "reserved" in str(r.pricing_quantity).lower()
        )
        commitment_ratio = commitment_count / len(records)
        score += commitment_ratio * 15  # Up to +15 for commitment coverage

        # Penalize for cost growth
        trend, trend_pct = self._calculate_trend(records)
        if trend == "increasing" and trend_pct > 20:
            score -= 10
        elif trend == "decreasing":
            score += 5

        return min(100, max(0, score))

    def _get_efficiency_rating(self, score: float) -> EfficiencyRating:
        """Convert efficiency score to rating."""
        if score >= 90:
            return EfficiencyRating.EXCELLENT
        elif score >= 75:
            return EfficiencyRating.GOOD
        elif score >= 50:
            return EfficiencyRating.AVERAGE
        elif score >= 25:
            return EfficiencyRating.BELOW_AVERAGE
        else:
            return EfficiencyRating.POOR

