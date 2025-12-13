"""Commitment Optimizer.

Analyzes and recommends Reserved Instances (RI) and Savings Plans (SP)
for AWS cost optimization. Provides recommendations during code generation.

Industry Comparison:
- ProsperOps: Automated RI/SP management
- CloudHealth: RI recommendations
- WISTX: Proactive commitment recommendations at code generation time

Key Features:
1. Coverage analysis - How much on-demand usage could be covered
2. Utilization analysis - How well existing commitments are used
3. Purchase recommendations - What to buy and for how long
4. Break-even analysis - When commitments become profitable
"""

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any
from statistics import mean

from wistx_mcp.tools.lib.cost_intelligence.models import CostRecord

logger = logging.getLogger(__name__)


class CommitmentType(str, Enum):
    """Types of AWS commitments."""
    RESERVED_INSTANCE = "reserved_instance"
    SAVINGS_PLAN_COMPUTE = "savings_plan_compute"
    SAVINGS_PLAN_EC2 = "savings_plan_ec2"
    SAVINGS_PLAN_SAGEMAKER = "savings_plan_sagemaker"


class PaymentOption(str, Enum):
    """RI/SP payment options."""
    NO_UPFRONT = "no_upfront"
    PARTIAL_UPFRONT = "partial_upfront"
    ALL_UPFRONT = "all_upfront"


class Term(str, Enum):
    """Commitment term length."""
    ONE_YEAR = "1_year"
    THREE_YEAR = "3_year"


class CommitmentRisk(str, Enum):
    """Risk level of a commitment."""
    LOW = "low"  # Stable, predictable workload
    MEDIUM = "medium"  # Some variability
    HIGH = "high"  # Unpredictable or short-lived


@dataclass
class CoverageAnalysis:
    """Analysis of commitment coverage."""
    total_on_demand_cost: float
    covered_cost: float
    uncovered_cost: float
    coverage_percentage: float
    
    # By service
    coverage_by_service: dict[str, float] = field(default_factory=dict)
    
    # Recommendation
    recommended_additional_coverage: float = 0.0
    potential_savings: float = 0.0


@dataclass
class UtilizationAnalysis:
    """Analysis of commitment utilization."""
    total_committed_cost: float
    utilized_cost: float
    wasted_cost: float
    utilization_percentage: float
    
    # Issues
    underutilized_commitments: list[dict] = field(default_factory=list)
    
    # Recommendations
    recommendations: list[str] = field(default_factory=list)


@dataclass
class CommitmentRecommendation:
    """Recommendation for purchasing a commitment."""
    recommendation_id: str
    commitment_type: CommitmentType
    
    # What to buy
    service: str
    instance_family: str | None
    region: str | None
    
    # How much
    recommended_quantity: int
    hourly_commitment: float  # For Savings Plans
    monthly_cost: float
    
    # Terms
    term: Term
    payment_option: PaymentOption
    
    # Savings
    estimated_monthly_savings: float
    estimated_annual_savings: float
    savings_percentage: float
    
    # Analysis
    break_even_months: float
    risk_level: CommitmentRisk
    confidence: float  # 0-1
    
    # Context
    based_on_days: int
    workload_stability: str
    rationale: str


@dataclass
class CommitmentPortfolio:
    """Complete view of commitment portfolio and recommendations."""
    generated_at: datetime
    
    # Current state
    coverage: CoverageAnalysis
    utilization: UtilizationAnalysis
    
    # Recommendations
    recommendations: list[CommitmentRecommendation] = field(default_factory=list)
    
    # Summary
    total_potential_savings: float = 0.0
    optimization_score: float = 0.0  # 0-100
    
    # Quick insights
    key_insights: list[str] = field(default_factory=list)


class CommitmentOptimizer:
    """Optimizer for AWS Reserved Instances and Savings Plans.
    
    Provides:
    1. Coverage analysis - identify uncovered on-demand usage
    2. Utilization tracking - ensure existing commitments are used
    3. Purchase recommendations - what/when/how much to buy
    4. Break-even analysis - ROI calculation
    """
    
    # Discount rates by commitment type and term (approximate)
    DISCOUNT_RATES = {
        CommitmentType.RESERVED_INSTANCE: {
            Term.ONE_YEAR: {
                PaymentOption.NO_UPFRONT: 0.31,
                PaymentOption.PARTIAL_UPFRONT: 0.38,
                PaymentOption.ALL_UPFRONT: 0.42,
            },
            Term.THREE_YEAR: {
                PaymentOption.NO_UPFRONT: 0.46,
                PaymentOption.PARTIAL_UPFRONT: 0.53,
                PaymentOption.ALL_UPFRONT: 0.58,
            },
        },
        CommitmentType.SAVINGS_PLAN_COMPUTE: {
            Term.ONE_YEAR: {
                PaymentOption.NO_UPFRONT: 0.28,
                PaymentOption.PARTIAL_UPFRONT: 0.35,
                PaymentOption.ALL_UPFRONT: 0.37,
            },
            Term.THREE_YEAR: {
                PaymentOption.NO_UPFRONT: 0.43,
                PaymentOption.PARTIAL_UPFRONT: 0.50,
                PaymentOption.ALL_UPFRONT: 0.52,
            },
        },
    }

    # Services eligible for commitments
    COMMITMENT_ELIGIBLE_SERVICES = [
        "ec2", "rds", "redshift", "elasticache", "elasticsearch",
        "opensearch", "lambda", "fargate", "sagemaker",
    ]

    # Minimum coverage threshold before recommending (%)
    MIN_COVERAGE_THRESHOLD = 60.0

    # Minimum utilization before warning (%)
    MIN_UTILIZATION_THRESHOLD = 80.0

    def __init__(self):
        """Initialize the commitment optimizer."""
        pass

    def analyze_coverage(
        self,
        cost_records: list[CostRecord],
        current_coverage: float = 0.0,
    ) -> CoverageAnalysis:
        """Analyze commitment coverage for cost records.

        Args:
            cost_records: Cost records to analyze
            current_coverage: Current coverage percentage (if known)

        Returns:
            CoverageAnalysis with recommendations
        """
        # Filter to eligible services
        eligible_records = [
            r for r in cost_records
            if any(s in (r.service_name or "").lower()
                   for s in self.COMMITMENT_ELIGIBLE_SERVICES)
        ]

        total_cost = sum(r.billed_cost for r in eligible_records)

        # Estimate coverage from pricing info if available
        if current_coverage > 0:
            covered = total_cost * (current_coverage / 100)
        else:
            # Estimate based on pricing patterns
            covered = sum(
                r.billed_cost for r in eligible_records
                if r.pricing_unit and "reserved" in str(r.pricing_unit).lower()
            )

        uncovered = total_cost - covered
        coverage_pct = (covered / total_cost * 100) if total_cost > 0 else 0

        # Coverage by service
        service_costs: dict[str, float] = {}
        for record in eligible_records:
            svc = record.service_name or "unknown"
            service_costs[svc] = service_costs.get(svc, 0) + record.billed_cost

        # Calculate potential savings from additional coverage
        # Assume 30% average savings from commitments
        avg_discount = 0.30
        recommended_coverage = max(0, uncovered * 0.7)  # Cover 70% of uncovered
        potential_savings = recommended_coverage * avg_discount

        return CoverageAnalysis(
            total_on_demand_cost=total_cost,
            covered_cost=covered,
            uncovered_cost=uncovered,
            coverage_percentage=coverage_pct,
            coverage_by_service=service_costs,
            recommended_additional_coverage=recommended_coverage,
            potential_savings=potential_savings,
        )

    def analyze_utilization(
        self,
        utilization_percentage: float,
        total_committed: float,
    ) -> UtilizationAnalysis:
        """Analyze commitment utilization.

        Args:
            utilization_percentage: Current utilization %
            total_committed: Total committed cost

        Returns:
            UtilizationAnalysis with recommendations
        """
        utilized = total_committed * (utilization_percentage / 100)
        wasted = total_committed - utilized

        recommendations = []
        underutilized = []

        if utilization_percentage < self.MIN_UTILIZATION_THRESHOLD:
            recommendations.append(
                f"Utilization at {utilization_percentage:.1f}% is below target "
                f"of {self.MIN_UTILIZATION_THRESHOLD}%"
            )

            if utilization_percentage < 50:
                recommendations.append(
                    "Consider selling unused reservations on RI Marketplace"
                )
                recommendations.append(
                    "Review if workload patterns have changed"
                )
            else:
                recommendations.append(
                    "Consider modifying RIs to match current instance usage"
                )

        return UtilizationAnalysis(
            total_committed_cost=total_committed,
            utilized_cost=utilized,
            wasted_cost=wasted,
            utilization_percentage=utilization_percentage,
            underutilized_commitments=underutilized,
            recommendations=recommendations,
        )

    def generate_recommendations(
        self,
        cost_records: list[CostRecord],
        coverage: CoverageAnalysis,
        environment: str = "production",
    ) -> list[CommitmentRecommendation]:
        """Generate commitment purchase recommendations.

        Args:
            cost_records: Cost records for analysis
            coverage: Coverage analysis results
            environment: Target environment

        Returns:
            List of commitment recommendations
        """
        recommendations = []

        # Only recommend for production with sufficient uncovered usage
        if environment.lower() not in ["production", "prod"]:
            return recommendations

        if coverage.uncovered_cost < 100:  # Minimum $100/month uncovered
            return recommendations

        # Analyze usage patterns for stability
        stability = self._analyze_workload_stability(cost_records)

        # Group by service for targeted recommendations
        service_costs = self._get_service_costs(cost_records)

        for service, cost in service_costs.items():
            if cost < 50:  # Skip small costs
                continue

            # Determine commitment type
            commitment_type = self._get_best_commitment_type(service)

            # Determine term and payment based on stability
            term, payment, risk = self._get_recommended_terms(stability)

            # Calculate savings
            discount = self.DISCOUNT_RATES.get(
                commitment_type, {}
            ).get(term, {}).get(payment, 0.30)

            monthly_savings = cost * discount * 0.7  # 70% coverage target

            # Calculate break-even
            if payment == PaymentOption.ALL_UPFRONT:
                upfront = cost * 0.7 * (12 if term == Term.ONE_YEAR else 36) * (1 - discount)
                break_even = upfront / monthly_savings if monthly_savings > 0 else 12
            else:
                break_even = 3 if term == Term.ONE_YEAR else 6

            recommendations.append(CommitmentRecommendation(
                recommendation_id=str(uuid.uuid4()),
                commitment_type=commitment_type,
                service=service,
                instance_family=self._extract_instance_family(cost_records, service),
                region=self._get_primary_region(cost_records, service),
                recommended_quantity=1,
                hourly_commitment=cost / 730,  # Monthly to hourly
                monthly_cost=cost * 0.7 * (1 - discount),
                term=term,
                payment_option=payment,
                estimated_monthly_savings=monthly_savings,
                estimated_annual_savings=monthly_savings * 12,
                savings_percentage=discount * 100,
                break_even_months=break_even,
                risk_level=risk,
                confidence=stability,
                based_on_days=30,
                workload_stability="stable" if stability > 0.8 else "variable",
                rationale=self._generate_rationale(service, cost, stability, discount),
            ))

        # Sort by savings
        recommendations.sort(key=lambda r: r.estimated_annual_savings, reverse=True)

        return recommendations[:5]  # Top 5 recommendations

    def generate_portfolio_analysis(
        self,
        cost_records: list[CostRecord],
        current_coverage: float = 0.0,
        current_utilization: float = 0.0,
        total_committed: float = 0.0,
        environment: str = "production",
    ) -> CommitmentPortfolio:
        """Generate complete commitment portfolio analysis.

        Args:
            cost_records: Cost records for analysis
            current_coverage: Current coverage %
            current_utilization: Current utilization %
            total_committed: Total committed cost
            environment: Target environment

        Returns:
            Complete CommitmentPortfolio analysis
        """
        # Analyze coverage
        coverage = self.analyze_coverage(cost_records, current_coverage)

        # Analyze utilization
        utilization = self.analyze_utilization(current_utilization, total_committed)

        # Generate recommendations
        recommendations = self.generate_recommendations(
            cost_records, coverage, environment
        )

        # Calculate totals
        total_savings = sum(r.estimated_annual_savings for r in recommendations)

        # Calculate optimization score
        coverage_score = min(100, coverage.coverage_percentage / 0.7 * 100)
        utilization_score = min(100, current_utilization / 0.85 * 100) if current_utilization > 0 else 50
        optimization_score = (coverage_score + utilization_score) / 2

        # Generate insights
        insights = self._generate_insights(coverage, utilization, recommendations)

        return CommitmentPortfolio(
            generated_at=datetime.now(timezone.utc),
            coverage=coverage,
            utilization=utilization,
            recommendations=recommendations,
            total_potential_savings=total_savings,
            optimization_score=optimization_score,
            key_insights=insights,
        )

    def _analyze_workload_stability(
        self,
        cost_records: list[CostRecord],
    ) -> float:
        """Analyze workload stability (0-1, higher = more stable)."""
        if len(cost_records) < 7:
            return 0.5  # Not enough data

        # Group by day
        daily: dict[str, float] = {}
        for record in cost_records:
            date_key = record.billing_period_start.strftime("%Y-%m-%d")
            daily[date_key] = daily.get(date_key, 0) + record.billed_cost

        if len(daily) < 7:
            return 0.5

        costs = list(daily.values())
        avg = mean(costs)

        if avg == 0:
            return 0.5

        # Calculate coefficient of variation
        variance = sum((c - avg) ** 2 for c in costs) / len(costs)
        cv = (variance ** 0.5) / avg

        # Convert to stability score (lower CV = higher stability)
        stability = max(0, min(1, 1 - cv))

        return stability

    def _get_service_costs(
        self,
        cost_records: list[CostRecord],
    ) -> dict[str, float]:
        """Get costs grouped by service."""
        service_costs: dict[str, float] = {}

        for record in cost_records:
            if not any(s in (record.service_name or "").lower()
                      for s in self.COMMITMENT_ELIGIBLE_SERVICES):
                continue

            svc = record.service_name or "unknown"
            service_costs[svc] = service_costs.get(svc, 0) + record.billed_cost

        return service_costs

    def _get_best_commitment_type(self, service: str) -> CommitmentType:
        """Determine best commitment type for a service."""
        service_lower = service.lower()

        # EC2-specific RI for known instance families
        if "ec2" in service_lower:
            return CommitmentType.RESERVED_INSTANCE

        # Savings Plans for more flexibility
        return CommitmentType.SAVINGS_PLAN_COMPUTE

    def _get_recommended_terms(
        self,
        stability: float,
    ) -> tuple[Term, PaymentOption, CommitmentRisk]:
        """Get recommended term and payment option based on stability."""
        if stability > 0.85:
            # Very stable - go for 3-year with more upfront
            return Term.THREE_YEAR, PaymentOption.PARTIAL_UPFRONT, CommitmentRisk.LOW
        elif stability > 0.7:
            # Stable - 1-year with partial upfront
            return Term.ONE_YEAR, PaymentOption.PARTIAL_UPFRONT, CommitmentRisk.MEDIUM
        else:
            # Less stable - 1-year with no upfront for flexibility
            return Term.ONE_YEAR, PaymentOption.NO_UPFRONT, CommitmentRisk.HIGH

    def _extract_instance_family(
        self,
        cost_records: list[CostRecord],
        service: str,
    ) -> str | None:
        """Extract primary instance family from records."""
        # Would need resource details - return None for now
        return None

    def _get_primary_region(
        self,
        cost_records: list[CostRecord],
        service: str,
    ) -> str | None:
        """Get primary region for a service."""
        region_costs: dict[str, float] = {}

        for record in cost_records:
            if service.lower() in (record.service_name or "").lower():
                region = record.region or "unknown"
                region_costs[region] = region_costs.get(region, 0) + record.billed_cost

        if not region_costs:
            return None

        return max(region_costs.items(), key=lambda x: x[1])[0]

    def _generate_rationale(
        self,
        service: str,
        cost: float,
        stability: float,
        discount: float,
    ) -> str:
        """Generate human-readable rationale for recommendation."""
        stability_desc = "stable" if stability > 0.8 else "moderately stable" if stability > 0.6 else "variable"

        return (
            f"{service} shows {stability_desc} usage patterns with ${cost:.2f}/month in eligible costs. "
            f"A commitment could save approximately {discount*100:.0f}% "
            f"(${cost * discount:.2f}/month)."
        )

    def _generate_insights(
        self,
        coverage: CoverageAnalysis,
        utilization: UtilizationAnalysis,
        recommendations: list[CommitmentRecommendation],
    ) -> list[str]:
        """Generate key insights from analysis."""
        insights = []

        # Coverage insights
        if coverage.coverage_percentage < 50:
            insights.append(
                f"Only {coverage.coverage_percentage:.0f}% of eligible spend is covered by commitments. "
                f"Industry best practice is 60-70%."
            )
        elif coverage.coverage_percentage < 70:
            insights.append(
                f"Coverage at {coverage.coverage_percentage:.0f}% - room for improvement to reach 70% target."
            )
        else:
            insights.append(
                f"Good coverage at {coverage.coverage_percentage:.0f}% of eligible spend."
            )

        # Utilization insights
        if utilization.utilization_percentage < 80 and utilization.total_committed_cost > 0:
            insights.append(
                f"Commitment utilization at {utilization.utilization_percentage:.0f}% - "
                f"${utilization.wasted_cost:.2f}/month in unused commitments."
            )

        # Savings opportunity
        if recommendations:
            total_savings = sum(r.estimated_annual_savings for r in recommendations)
            insights.append(
                f"Identified ${total_savings:,.0f}/year in potential savings from {len(recommendations)} recommendations."
            )

        return insights
