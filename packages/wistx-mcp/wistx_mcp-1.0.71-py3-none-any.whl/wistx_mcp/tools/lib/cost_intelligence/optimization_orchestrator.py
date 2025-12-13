"""Optimization Orchestrator.

Orchestrates all cost optimization services to provide unified
recommendations during infrastructure code generation.

This is the main entry point for cost optimization intelligence,
combining:
- Commitment Optimizer (RI/Savings Plans)
- Spot Instance Advisor
- Rightsizing Analyzer
- Existing efficiency metrics

Industry Comparison:
- Cast.ai: Real-time optimization
- CloudHealth: Multi-pillar recommendations
- WISTX: Proactive optimization at code generation time
"""

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from wistx_mcp.tools.lib.cost_intelligence.models import CostRecord
from wistx_mcp.tools.lib.cost_intelligence.commitment_optimizer import (
    CommitmentOptimizer,
    CommitmentPortfolio,
    CommitmentRecommendation,
)
from wistx_mcp.tools.lib.cost_intelligence.spot_advisor import (
    SpotInstanceAdvisor,
    SpotAnalysis,
    SpotRecommendation,
    WorkloadType,
)
from wistx_mcp.tools.lib.cost_intelligence.rightsizing_analyzer import (
    RightsizingAnalyzer,
    RightsizingAnalysis,
    RightsizingRecommendation,
)

logger = logging.getLogger(__name__)


class OptimizationCategory(str, Enum):
    """Categories of optimization."""
    COMMITMENT = "commitment"  # RI/SP
    SPOT = "spot"  # Spot instances
    RIGHTSIZING = "rightsizing"  # Instance sizing
    ARCHITECTURE = "architecture"  # Design changes
    SCHEDULING = "scheduling"  # Start/stop
    STORAGE = "storage"  # EBS, S3, etc.


class OptimizationPriority(str, Enum):
    """Priority level for optimization."""
    CRITICAL = "critical"  # Immediate action needed
    HIGH = "high"  # Should address soon
    MEDIUM = "medium"  # Good to address
    LOW = "low"  # Nice to have


@dataclass
class UnifiedRecommendation:
    """Unified recommendation from any optimization service."""
    recommendation_id: str
    category: OptimizationCategory
    priority: OptimizationPriority

    # Description
    title: str
    description: str

    # Impact
    estimated_monthly_savings: float
    estimated_annual_savings: float
    savings_percentage: float

    # Implementation
    implementation_effort: str  # "low", "medium", "high"

    # Risk
    risk_level: str

    # Metadata
    source_service: str

    # Fields with defaults must come last
    implementation_steps: list[str] = field(default_factory=list)
    risk_factors: list[str] = field(default_factory=list)
    source_recommendation_id: str | None = None
    terraform_example: str | None = None
    cdk_example: str | None = None


@dataclass
class OptimizationSummary:
    """Summary of optimization opportunities."""
    analysis_id: str
    generated_at: datetime
    
    # Overall metrics
    current_monthly_spend: float
    potential_monthly_savings: float
    potential_annual_savings: float
    optimization_score: float  # 0-100
    
    # By category
    savings_by_category: dict[str, float] = field(default_factory=dict)
    recommendations_by_category: dict[str, int] = field(default_factory=dict)
    
    # All recommendations (prioritized)
    recommendations: list[UnifiedRecommendation] = field(default_factory=list)
    
    # Quick wins (low effort, high impact)
    quick_wins: list[UnifiedRecommendation] = field(default_factory=list)
    
    # Detailed analyses
    commitment_analysis: CommitmentPortfolio | None = None
    spot_analysis: SpotAnalysis | None = None
    rightsizing_analysis: RightsizingAnalysis | None = None
    
    # Key insights
    key_insights: list[str] = field(default_factory=list)
    
    # Code generation context
    code_generation_guidance: dict[str, Any] = field(default_factory=dict)


class OptimizationOrchestrator:
    """Orchestrates all optimization services.
    
    Provides:
    1. Unified optimization analysis
    2. Prioritized recommendations
    3. Code generation guidance
    4. Quick wins identification
    """
    
    def __init__(self):
        """Initialize the orchestrator with all optimization services."""
        self.commitment_optimizer = CommitmentOptimizer()
        self.spot_advisor = SpotInstanceAdvisor()
        self.rightsizing_analyzer = RightsizingAnalyzer()
    
    def analyze(
        self,
        cost_records: list[CostRecord],
        resources: list[dict[str, Any]] | None = None,
        workload_type: str = "containerized",
        environment: str = "production",
        current_coverage: float = 0.0,
        current_utilization: float = 0.0,
        total_committed: float = 0.0,
    ) -> OptimizationSummary:
        """Run comprehensive optimization analysis.
        
        Args:
            cost_records: Cost data for analysis
            resources: Resource details for rightsizing
            workload_type: Type of workload
            environment: Target environment
            current_coverage: Current commitment coverage %
            current_utilization: Current commitment utilization %
            total_committed: Total committed spend
            
        Returns:
            OptimizationSummary with all recommendations
        """
        all_recommendations: list[UnifiedRecommendation] = []

        # Calculate current spend
        current_spend = sum(r.billed_cost for r in cost_records)

        # 1. Run commitment analysis
        commitment_analysis = self.commitment_optimizer.generate_portfolio_analysis(
            cost_records=cost_records,
            current_coverage=current_coverage,
            current_utilization=current_utilization,
            total_committed=total_committed,
            environment=environment,
        )

        # Convert commitment recommendations
        for rec in commitment_analysis.recommendations:
            all_recommendations.append(self._convert_commitment_recommendation(rec))

        # 2. Run Spot analysis
        spot_analysis = self.spot_advisor.assess_workload(
            workload_type=workload_type,
            can_handle_interruption=(environment.lower() != "production" or workload_type in ["batch", "ci_cd"]),
        )

        # Convert Spot recommendations
        for rec in spot_analysis.recommendations:
            all_recommendations.append(self._convert_spot_recommendation(rec, current_spend))

        # 3. Run rightsizing analysis (if resources provided)
        rightsizing_analysis = None
        if resources:
            rightsizing_analysis = self.rightsizing_analyzer.analyze_resources(resources)

            for rec in rightsizing_analysis.recommendations:
                all_recommendations.append(self._convert_rightsizing_recommendation(rec))

        # Sort by savings (highest first)
        all_recommendations.sort(key=lambda r: r.estimated_annual_savings, reverse=True)

        # Calculate totals
        total_savings = sum(r.estimated_monthly_savings for r in all_recommendations)

        # Identify quick wins
        quick_wins = [
            r for r in all_recommendations
            if r.implementation_effort == "low" and r.estimated_monthly_savings > 50
        ][:5]

        # Calculate savings by category
        savings_by_category: dict[str, float] = {}
        recommendations_by_category: dict[str, int] = {}
        for rec in all_recommendations:
            cat = rec.category.value
            savings_by_category[cat] = savings_by_category.get(cat, 0) + rec.estimated_monthly_savings
            recommendations_by_category[cat] = recommendations_by_category.get(cat, 0) + 1

        # Calculate optimization score
        opt_score = self._calculate_optimization_score(
            current_coverage,
            current_utilization,
            commitment_analysis,
            spot_analysis,
            rightsizing_analysis,
        )

        # Generate insights
        insights = self._generate_insights(
            commitment_analysis,
            spot_analysis,
            rightsizing_analysis,
            total_savings,
        )

        # Generate code guidance
        code_guidance = self._generate_code_guidance(
            spot_analysis,
            rightsizing_analysis,
            environment,
        )

        return OptimizationSummary(
            analysis_id=str(uuid.uuid4()),
            generated_at=datetime.now(timezone.utc),
            current_monthly_spend=current_spend,
            potential_monthly_savings=total_savings,
            potential_annual_savings=total_savings * 12,
            optimization_score=opt_score,
            savings_by_category=savings_by_category,
            recommendations_by_category=recommendations_by_category,
            recommendations=all_recommendations,
            quick_wins=quick_wins,
            commitment_analysis=commitment_analysis,
            spot_analysis=spot_analysis,
            rightsizing_analysis=rightsizing_analysis,
            key_insights=insights,
            code_generation_guidance=code_guidance,
        )

    def get_code_generation_context(
        self,
        instance_type: str,
        region: str,
        workload_type: str = "containerized",
        environment: str = "production",
        monthly_budget: float | None = None,
    ) -> dict[str, Any]:
        """Get optimization context for code generation.

        Used during Terraform/CDK code generation to provide
        optimization recommendations inline.

        Args:
            instance_type: Target instance type
            region: AWS region
            workload_type: Type of workload
            environment: Target environment
            monthly_budget: Budget constraint if any

        Returns:
            Context dict with optimization guidance
        """
        context: dict[str, Any] = {
            "instance_type": instance_type,
            "region": region,
            "environment": environment,
            "recommendations": [],
            "warnings": [],
        }

        # Get Spot recommendation
        spot_rec = self.spot_advisor.get_instance_recommendation(
            instance_type=instance_type,
            region=region,
            on_demand_price=self.rightsizing_analyzer._estimate_instance_spec(instance_type).hourly_cost,
            workload_type=self.spot_advisor._parse_workload_type(workload_type),
        )

        if spot_rec.suitability.value != "not_recommended":
            context["spot_recommendation"] = {
                "suitable": True,
                "savings_percentage": spot_rec.estimated_savings_percentage,
                "monthly_savings": spot_rec.estimated_monthly_savings,
                "recommended_spot_percentage": 100 - spot_rec.min_on_demand_percentage,
                "allocation_strategy": spot_rec.recommended_allocation_strategy,
                "fallback_instances": spot_rec.fallback_instance_types,
            }
            context["recommendations"].append(
                f"Consider Spot instances for {spot_rec.estimated_savings_percentage:.0f}% savings"
            )
        else:
            context["spot_recommendation"] = {"suitable": False}
            context["recommendations"].append(
                "Spot instances not recommended for this workload type"
            )

        # Get rightsizing recommendation
        initial_rec = self.rightsizing_analyzer.recommend_initial_size(
            workload_description=workload_type,
            is_production=(environment.lower() in ["production", "prod"]),
        )

        if initial_rec.instance_type != instance_type:
            context["sizing_recommendation"] = {
                "suggested_type": initial_rec.instance_type,
                "suggested_vcpu": initial_rec.vcpu,
                "suggested_memory_gb": initial_rec.memory_gb,
                "current_type": instance_type,
            }
            context["recommendations"].append(
                f"Consider {initial_rec.instance_type} based on workload analysis"
            )

        # Budget check
        if monthly_budget:
            monthly_cost = initial_rec.hourly_cost * 730
            if monthly_cost > monthly_budget:
                context["warnings"].append(
                    f"Estimated ${monthly_cost:.2f}/month exceeds budget of ${monthly_budget:.2f}"
                )

        # Commitment recommendation for production
        if environment.lower() in ["production", "prod"]:
            context["commitment_recommendation"] = {
                "should_consider": True,
                "recommendation": "Consider Reserved Instances or Savings Plans for stable production workloads",
                "typical_savings": "30-40%",
            }

        return context

    def _convert_commitment_recommendation(
        self,
        rec: CommitmentRecommendation,
    ) -> UnifiedRecommendation:
        """Convert commitment recommendation to unified format."""
        return UnifiedRecommendation(
            recommendation_id=str(uuid.uuid4()),
            category=OptimizationCategory.COMMITMENT,
            priority=self._determine_priority(rec.estimated_annual_savings, rec.risk_level.value),
            title=f"Purchase {rec.commitment_type.value} for {rec.service}",
            description=rec.rationale,
            estimated_monthly_savings=rec.estimated_monthly_savings,
            estimated_annual_savings=rec.estimated_annual_savings,
            savings_percentage=rec.savings_percentage,
            implementation_effort="low",  # Purchasing commitments is straightforward
            implementation_steps=[
                f"1. Navigate to AWS Cost Explorer > Recommendations",
                f"2. Review {rec.commitment_type.value} recommendations",
                f"3. Purchase {rec.term.value} {rec.payment_option.value} commitment",
                f"4. Monitor utilization weekly",
            ],
            risk_level=rec.risk_level.value,
            risk_factors=[f"Break-even at {rec.break_even_months:.1f} months"],
            source_service="commitment_optimizer",
            source_recommendation_id=rec.recommendation_id,
        )

    def _convert_spot_recommendation(
        self,
        rec: SpotRecommendation,
        current_spend: float,
    ) -> UnifiedRecommendation:
        """Convert Spot recommendation to unified format."""
        # Estimate savings based on current spend proportion
        estimated_savings = current_spend * (rec.estimated_savings_percentage / 100) * 0.1  # 10% of spend assumed eligible

        return UnifiedRecommendation(
            recommendation_id=str(uuid.uuid4()),
            category=OptimizationCategory.SPOT,
            priority=self._determine_priority(estimated_savings * 12, rec.risk_level.value),
            title=f"Use Spot instances for {rec.workload_type.value} workload",
            description=rec.rationale,
            estimated_monthly_savings=rec.estimated_monthly_savings,
            estimated_annual_savings=rec.estimated_monthly_savings * 12,
            savings_percentage=rec.estimated_savings_percentage,
            implementation_effort="medium",
            implementation_steps=rec.prerequisites,
            risk_level=rec.risk_level.value,
            risk_factors=rec.warnings,
            source_service="spot_advisor",
            source_recommendation_id=rec.recommendation_id,
            terraform_example=self._generate_spot_terraform(rec),
        )

    def _convert_rightsizing_recommendation(
        self,
        rec: RightsizingRecommendation,
    ) -> UnifiedRecommendation:
        """Convert rightsizing recommendation to unified format."""
        return UnifiedRecommendation(
            recommendation_id=str(uuid.uuid4()),
            category=OptimizationCategory.RIGHTSIZING,
            priority=self._determine_priority(rec.monthly_savings * 12, rec.risk_level.value),
            title=f"Rightsize {rec.resource_id}: {rec.current_instance.instance_type} → {rec.recommended_instance.instance_type}",
            description=rec.rationale,
            estimated_monthly_savings=rec.monthly_savings,
            estimated_annual_savings=rec.monthly_savings * 12,
            savings_percentage=rec.savings_percentage,
            implementation_effort="low" if rec.risk_level.value == "low" else "medium",
            implementation_steps=rec.validation_steps,
            risk_level=rec.risk_level.value,
            risk_factors=rec.risk_factors,
            source_service="rightsizing_analyzer",
            source_recommendation_id=rec.recommendation_id,
            terraform_example=self._generate_rightsizing_terraform(rec),
        )

    def _determine_priority(
        self,
        annual_savings: float,
        risk_level: str,
    ) -> OptimizationPriority:
        """Determine priority based on savings and risk."""
        # High savings + low risk = critical
        if annual_savings > 10000 and risk_level == "low":
            return OptimizationPriority.CRITICAL
        elif annual_savings > 5000:
            return OptimizationPriority.HIGH
        elif annual_savings > 1000:
            return OptimizationPriority.MEDIUM
        return OptimizationPriority.LOW

    def _calculate_optimization_score(
        self,
        coverage: float,
        utilization: float,
        commitment: CommitmentPortfolio,
        spot: SpotAnalysis,
        rightsizing: RightsizingAnalysis | None,
    ) -> float:
        """Calculate overall optimization score (0-100)."""
        scores = []

        # Coverage score (target: 70%)
        coverage_score = min(100, coverage / 0.7 * 100) if coverage > 0 else 50
        scores.append(coverage_score * 0.3)  # 30% weight

        # Utilization score (target: 85%)
        util_score = min(100, utilization / 0.85 * 100) if utilization > 0 else 50
        scores.append(util_score * 0.2)  # 20% weight

        # Spot readiness score
        spot_score = 100 if spot.is_spot_suitable else 50
        if spot.suitability_rating.value == "excellent":
            spot_score = 100
        elif spot.suitability_rating.value == "good":
            spot_score = 80
        elif spot.suitability_rating.value == "moderate":
            spot_score = 60
        scores.append(spot_score * 0.2)  # 20% weight

        # Rightsizing score
        if rightsizing:
            optimal_ratio = rightsizing.optimal_count / max(1, rightsizing.total_resources_analyzed)
            rightsizing_score = optimal_ratio * 100
        else:
            rightsizing_score = 70  # Default if no data
        scores.append(rightsizing_score * 0.3)  # 30% weight

        return sum(scores)

    def _generate_insights(
        self,
        commitment: CommitmentPortfolio,
        spot: SpotAnalysis,
        rightsizing: RightsizingAnalysis | None,
        total_savings: float,
    ) -> list[str]:
        """Generate key insights from all analyses."""
        insights = []

        # Add commitment insights
        insights.extend(commitment.key_insights)

        # Add Spot insights
        if spot.is_spot_suitable:
            insights.append(
                f"Workload is {spot.suitability_rating.value} for Spot instances "
                f"with up to {spot.total_potential_savings:.0f}% potential savings."
            )

        # Add rightsizing insights
        if rightsizing and rightsizing.oversized_count > 0:
            insights.append(
                f"{rightsizing.oversized_count} oversized resources identified "
                f"with ${rightsizing.total_monthly_savings:.0f}/month savings potential."
            )

        # Overall insight
        if total_savings > 0:
            insights.append(
                f"Total optimization potential: ${total_savings:,.0f}/month "
                f"(${total_savings * 12:,.0f}/year)."
            )

        return insights

    def _generate_code_guidance(
        self,
        spot: SpotAnalysis,
        rightsizing: RightsizingAnalysis | None,
        environment: str,
    ) -> dict[str, Any]:
        """Generate code generation guidance."""
        guidance: dict[str, Any] = {
            "environment": environment,
            "recommendations": [],
        }

        # Spot guidance
        if spot.is_spot_suitable and environment.lower() not in ["production", "prod"]:
            guidance["use_spot"] = True
            guidance["spot_percentage"] = spot.recommended_spot_percentage
            guidance["recommendations"].append(
                "Configure Auto Scaling Group with mixed instances policy for Spot"
            )
        else:
            guidance["use_spot"] = False

        # Production guidance
        if environment.lower() in ["production", "prod"]:
            guidance["recommendations"].extend([
                "Consider Reserved Instances or Savings Plans",
                "Maintain On-Demand baseline for stability",
                "Configure multi-AZ for high availability",
            ])

        # Best practices
        guidance["best_practices"] = spot.best_practices

        return guidance

    def _generate_spot_terraform(self, rec: SpotRecommendation) -> str:
        """Generate Terraform example for Spot configuration."""
        fallbacks = ", ".join(f'"{f}"' for f in rec.fallback_instance_types[:2])

        return f'''# Spot Instance Configuration
resource "aws_launch_template" "spot_optimized" {{
  name_prefix   = "spot-"
  instance_type = "{rec.instance_type}"

  instance_market_options {{
    market_type = "spot"
    spot_options {{
      max_price          = "" # Use on-demand price
      spot_instance_type = "one-time"
    }}
  }}
}}

resource "aws_autoscaling_group" "mixed" {{
  mixed_instances_policy {{
    instances_distribution {{
      on_demand_base_capacity                  = 1
      on_demand_percentage_above_base_capacity = {rec.min_on_demand_percentage}
      spot_allocation_strategy                 = "{rec.recommended_allocation_strategy}"
    }}
    launch_template {{
      launch_template_specification {{
        launch_template_id = aws_launch_template.spot_optimized.id
      }}
      override {{
        instance_type = "{rec.instance_type}"
      }}
      override {{
        instance_type = [{fallbacks}][0]
      }}
    }}
  }}
}}'''

    def _generate_rightsizing_terraform(self, rec: RightsizingRecommendation) -> str:
        """Generate Terraform example for rightsized instance."""
        return f'''# Rightsized Instance
# Previous: {rec.current_instance.instance_type} (${rec.current_instance.hourly_cost:.4f}/hr)
# Recommended: {rec.recommended_instance.instance_type} (${rec.recommended_instance.hourly_cost:.4f}/hr)
# Savings: ${rec.monthly_savings:.2f}/month ({rec.savings_percentage:.0f}%)

resource "aws_instance" "optimized" {{
  instance_type = "{rec.recommended_instance.instance_type}"

  # ... other configuration
}}'''
