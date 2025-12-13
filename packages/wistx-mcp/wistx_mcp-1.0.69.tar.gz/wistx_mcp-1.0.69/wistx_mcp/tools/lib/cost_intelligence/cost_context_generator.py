"""Cost Context Generator.

Generates rich cost context for AI coding assistants during infrastructure
code generation. This is THE key differentiator - providing cost intelligence
WHERE and WHEN decisions are made.

Industry Comparison:
- Infracost: PR-level cost estimation (too late)
- CloudZero: Dashboard-based (not in IDE)
- WISTX: Code generation time (shift-left)
"""

import logging
import uuid
from datetime import datetime, timezone, timedelta
from typing import Any

from wistx_mcp.tools.lib.cost_intelligence.models import (
    CostContext,
    ResourceCostBreakdown,
    BudgetStatus,
    CostAlternative,
    OptimizationRecommendation,
    UnitEconomics,
    RecommendationType,
    RecommendationStrength,
)

logger = logging.getLogger(__name__)


class CostContextGenerator:
    """Generate rich cost context for AI assistants.
    
    This service is called during code generation to provide:
    1. Cost estimates for requested resources
    2. Budget status and enforcement
    3. Cost-optimized alternatives
    4. Intelligent optimization recommendations
    5. Historical cost context
    6. Anomaly awareness
    """
    
    def __init__(
        self,
        pricing_data: dict[str, Any] | None = None,
        budget_service: Any | None = None,
        spending_tracker: Any | None = None,
    ):
        """Initialize the cost context generator.
        
        Args:
            pricing_data: Pricing data for cost estimation
            budget_service: Budget service for budget checks
            spending_tracker: Spending tracker for historical data
        """
        self.pricing_data = pricing_data or {}
        self.budget_service = budget_service
        self.spending_tracker = spending_tracker
    
    async def generate_context(
        self,
        user_id: str,
        resources: list[dict[str, Any]],
        cloud_provider: str = "aws",
        environment: str | None = None,
    ) -> CostContext:
        """Generate comprehensive cost context for AI assistant.
        
        This is the main entry point called during code generation.
        
        Args:
            user_id: User ID for budget and history lookup
            resources: List of resources being generated
            cloud_provider: Target cloud provider
            environment: Target environment (dev, staging, production)
            
        Returns:
            Rich CostContext with estimates, alternatives, and recommendations
        """
        context_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        
        # 1. Calculate cost breakdown for requested resources
        cost_breakdown = await self._calculate_cost_breakdown(
            resources, cloud_provider
        )
        
        total_monthly = sum(r.monthly_cost for r in cost_breakdown)
        total_annual = total_monthly * 12
        
        # 2. Check budget status
        budget_status = await self._get_budget_status(
            user_id, total_monthly, cloud_provider, environment
        )
        
        # 3. Generate cost-optimized alternatives
        alternatives = await self._generate_alternatives(
            resources, cost_breakdown, budget_status, cloud_provider
        )
        
        # 4. Generate intelligent recommendations
        recommendations = await self._generate_recommendations(
            resources, cost_breakdown, budget_status, environment
        )
        
        # 5. Get unit economics context
        unit_economics = await self._get_unit_economics(user_id)
        
        return CostContext(
            context_id=context_id,
            generated_at=now,
            user_id=user_id,
            estimated_monthly_cost=total_monthly,
            estimated_annual_cost=total_annual,
            cost_breakdown=cost_breakdown,
            budget_status=budget_status,
            budget_remaining=budget_status.remaining if budget_status else None,
            budget_will_exceed=budget_status.will_exceed_with_new if budget_status else False,
            budget_exceeded_by=budget_status.exceeded_by if budget_status else None,
            alternatives=alternatives,
            optimization_recommendations=recommendations,
            unit_economics=unit_economics,
        )
    
    async def _calculate_cost_breakdown(
        self,
        resources: list[dict[str, Any]],
        cloud_provider: str,
    ) -> list[ResourceCostBreakdown]:
        """Calculate detailed cost breakdown for each resource."""
        breakdowns = []
        
        for resource in resources:
            breakdown = await self._estimate_resource_cost(resource, cloud_provider)
            breakdowns.append(breakdown)
        
        return breakdowns
    
    async def _estimate_resource_cost(
        self,
        resource: dict[str, Any],
        cloud_provider: str,
    ) -> ResourceCostBreakdown:
        """Estimate cost for a single resource.
        
        Uses pricing data to calculate accurate cost estimates.
        """
        resource_type = resource.get("type", "unknown")
        instance_type = resource.get("instance_type")
        region = resource.get("region", "us-east-1")
        quantity = resource.get("quantity", 1)
        
        # Get pricing from pricing data or use estimation
        hourly_cost = self._get_hourly_price(
            cloud_provider, resource_type, instance_type, region
        )
        
        return ResourceCostBreakdown(
            resource_name=resource.get("name", resource_type),
            cloud_provider=cloud_provider,
            service=resource_type,
            instance_type=instance_type,
            region=region,
            quantity=quantity,
            hourly_cost=hourly_cost * quantity,
            daily_cost=hourly_cost * 24 * quantity,
            monthly_cost=hourly_cost * 730 * quantity,  # 730 hours/month
            annual_cost=hourly_cost * 8760 * quantity,  # 8760 hours/year
            pricing_category=resource.get("pricing_category", "on_demand"),
        )

    def _get_hourly_price(
        self,
        cloud_provider: str,
        resource_type: str,
        instance_type: str | None,
        region: str,
    ) -> float:
        """Get hourly price for a resource.

        Uses pricing data if available, otherwise falls back to estimates.
        """
        # Try to get from pricing data
        if self.pricing_data:
            key = f"{cloud_provider}:{resource_type}:{instance_type}:{region}"
            if key in self.pricing_data:
                return self.pricing_data[key]

        # Fallback to common instance type estimates
        # These are approximate on-demand prices for us-east-1
        ec2_prices = {
            "t3.micro": 0.0104,
            "t3.small": 0.0208,
            "t3.medium": 0.0416,
            "t3.large": 0.0832,
            "t3.xlarge": 0.1664,
            "t3.2xlarge": 0.3328,
            "m5.large": 0.096,
            "m5.xlarge": 0.192,
            "m5.2xlarge": 0.384,
            "m5.4xlarge": 0.768,
            "m6i.large": 0.096,
            "m6i.xlarge": 0.192,
            "c5.large": 0.085,
            "c5.xlarge": 0.17,
            "c5.2xlarge": 0.34,
            "r5.large": 0.126,
            "r5.xlarge": 0.252,
        }

        rds_prices = {
            "db.t3.micro": 0.017,
            "db.t3.small": 0.034,
            "db.t3.medium": 0.068,
            "db.m5.large": 0.171,
            "db.m5.xlarge": 0.342,
            "db.r5.large": 0.24,
        }

        if resource_type in ["ec2", "instance", "compute"]:
            return ec2_prices.get(instance_type or "t3.medium", 0.05)
        elif resource_type in ["rds", "database"]:
            return rds_prices.get(instance_type or "db.t3.medium", 0.10)
        elif resource_type in ["s3", "storage"]:
            return 0.023 / 730  # $0.023/GB/month converted to hourly
        elif resource_type in ["lambda", "function"]:
            return 0.0  # Pay per invocation, not hourly
        elif resource_type in ["elb", "load_balancer"]:
            return 0.0225  # ALB hourly rate

        return 0.05  # Default fallback

    async def _get_budget_status(
        self,
        user_id: str,
        new_monthly_cost: float,
        cloud_provider: str,
        environment: str | None,
    ) -> BudgetStatus | None:
        """Get current budget status and check if new resources fit."""
        if not self.budget_service:
            return None

        try:
            # Get active budget for user
            budget = await self.budget_service.get_active_budget(
                user_id=user_id,
                cloud_provider=cloud_provider,
                environment=environment,
            )

            if not budget:
                return None

            # Calculate current spending
            current_spent = await self.budget_service.get_current_spending(
                budget_id=budget.id
            )

            remaining = budget.amount - current_spent
            will_exceed = (current_spent + new_monthly_cost) > budget.amount
            exceeded_by = max(0, (current_spent + new_monthly_cost) - budget.amount)

            return BudgetStatus(
                budget_id=str(budget.id),
                budget_name=budget.name,
                budget_amount=budget.amount,
                total_spent=current_spent,
                remaining=remaining,
                utilization_percent=(current_spent / budget.amount * 100) if budget.amount > 0 else 0,
                enforcement_mode=budget.enforcement_mode,
                is_exceeded=current_spent > budget.amount,
                will_exceed_with_new=will_exceed,
                exceeded_by=exceeded_by if will_exceed else None,
            )
        except Exception as e:
            logger.warning("Failed to get budget status: %s", e)
            return None

    async def _generate_alternatives(
        self,
        resources: list[dict[str, Any]],
        cost_breakdown: list[ResourceCostBreakdown],
        budget_status: BudgetStatus | None,
        cloud_provider: str,
    ) -> list[CostAlternative]:
        """Generate cost-optimized alternatives.

        This is a KEY differentiator - providing alternatives DURING code
        generation, not after deployment.
        """
        alternatives = []
        total_original = sum(r.monthly_cost for r in cost_breakdown)

        # Alternative 1: Spot instances (if applicable)
        spot_resources = []
        spot_savings = 0.0
        for resource in resources:
            if resource.get("type") in ["ec2", "instance", "compute"]:
                spot_resource = resource.copy()
                spot_resource["pricing_category"] = "spot"
                spot_resources.append(spot_resource)
                # Spot typically saves 60-90%
                original_cost = next(
                    (r.monthly_cost for r in cost_breakdown
                     if r.resource_name == resource.get("name", resource.get("type"))),
                    0
                )
                spot_savings += original_cost * 0.7  # 70% savings estimate

        if spot_resources and spot_savings > 0:
            alternatives.append(CostAlternative(
                alternative_id=str(uuid.uuid4()),
                name="Spot Instance Configuration",
                description="Use Spot Instances for fault-tolerant workloads",
                resources=spot_resources,
                monthly_cost=total_original - spot_savings,
                original_cost=total_original,
                savings_amount=spot_savings,
                savings_percentage=(spot_savings / total_original * 100) if total_original > 0 else 0,
                strength=RecommendationStrength.STRONG,
                trade_offs=[
                    "Instances can be interrupted with 2-minute warning",
                    "Not suitable for stateful applications",
                ],
                benefits=[
                    "Up to 90% cost savings",
                    "Same compute capacity",
                ],
                suitable_for=[
                    "Batch processing",
                    "CI/CD workloads",
                    "Stateless web servers",
                    "Development environments",
                ],
                not_suitable_for=[
                    "Production databases",
                    "Stateful applications",
                    "Long-running critical processes",
                ],
            ))

        # Alternative 2: Smaller instance sizes
        downsized_resources = []
        downsize_savings = 0.0
        for i, resource in enumerate(resources):
            if resource.get("instance_type"):
                smaller = self._get_smaller_instance(resource.get("instance_type"))
                if smaller:
                    downsized = resource.copy()
                    downsized["instance_type"] = smaller
                    downsized_resources.append(downsized)
                    # Typically 50% savings for one size down
                    downsize_savings += cost_breakdown[i].monthly_cost * 0.5

        if downsized_resources and downsize_savings > 0:
            alternatives.append(CostAlternative(
                alternative_id=str(uuid.uuid4()),
                name="Right-Sized Configuration",
                description="Use smaller instance sizes - can scale up if needed",
                resources=downsized_resources,
                monthly_cost=total_original - downsize_savings,
                original_cost=total_original,
                savings_amount=downsize_savings,
                savings_percentage=(downsize_savings / total_original * 100) if total_original > 0 else 0,
                strength=RecommendationStrength.MODERATE,
                trade_offs=[
                    "Less compute capacity",
                    "May need to scale up later",
                ],
                benefits=[
                    "~50% cost savings",
                    "Can scale up if needed",
                    "Start small, grow as needed",
                ],
                suitable_for=[
                    "New projects with unknown load",
                    "Development environments",
                    "Low-traffic applications",
                ],
                not_suitable_for=[
                    "Known high-traffic applications",
                    "CPU/memory intensive workloads",
                ],
            ))

        # Alternative 3: Budget-compliant option (if over budget)
        if budget_status and budget_status.will_exceed_with_new:
            budget_fit = await self._generate_budget_fit_alternative(
                resources, cost_breakdown, budget_status, cloud_provider
            )
            if budget_fit:
                alternatives.append(budget_fit)

        return alternatives

    def _get_smaller_instance(self, instance_type: str) -> str | None:
        """Get the next smaller instance type."""
        size_order = ["nano", "micro", "small", "medium", "large", "xlarge", "2xlarge", "4xlarge"]

        for i, size in enumerate(size_order):
            if size in instance_type and i > 0:
                return instance_type.replace(size, size_order[i - 1])

        return None

    async def _generate_budget_fit_alternative(
        self,
        resources: list[dict[str, Any]],
        cost_breakdown: list[ResourceCostBreakdown],
        budget_status: BudgetStatus,
        cloud_provider: str,
    ) -> CostAlternative | None:
        """Generate an alternative that fits within budget."""
        total_original = sum(r.monthly_cost for r in cost_breakdown)
        target_cost = budget_status.remaining * 0.9  # 90% of remaining budget

        if target_cost <= 0:
            return None

        reduction_needed = total_original - target_cost
        reduction_percent = reduction_needed / total_original

        # Create budget-fit resources
        budget_resources = []
        for resource in resources:
            budget_resource = resource.copy()

            # Apply multiple cost reduction strategies
            if resource.get("type") in ["ec2", "instance", "compute"]:
                # Use spot + smaller instance
                budget_resource["pricing_category"] = "spot"
                smaller = self._get_smaller_instance(resource.get("instance_type", ""))
                if smaller:
                    budget_resource["instance_type"] = smaller

            budget_resources.append(budget_resource)

        return CostAlternative(
            alternative_id=str(uuid.uuid4()),
            name="Budget-Compliant Configuration",
            description=f"Configuration that fits within your ${budget_status.remaining:.2f} remaining budget",
            resources=budget_resources,
            monthly_cost=target_cost,
            original_cost=total_original,
            savings_amount=reduction_needed,
            savings_percentage=reduction_percent * 100,
            strength=RecommendationStrength.STRONG,
            trade_offs=[
                "Reduced compute capacity",
                "May use interruptible instances",
            ],
            benefits=[
                "Stays within budget",
                "Avoids budget enforcement actions",
            ],
            suitable_for=[
                "Budget-constrained projects",
                "Development environments",
            ],
            not_suitable_for=[
                "Production workloads requiring guaranteed capacity",
            ],
        )

    async def _generate_recommendations(
        self,
        resources: list[dict[str, Any]],
        cost_breakdown: list[ResourceCostBreakdown],
        budget_status: BudgetStatus | None,
        environment: str | None,
    ) -> list[OptimizationRecommendation]:
        """Generate intelligent, context-aware recommendations.

        Unlike generic suggestions, these are specific to the resources
        being generated and the user's context.
        """
        recommendations = []
        total_monthly = sum(r.monthly_cost for r in cost_breakdown)

        # Check for Reserved Instance opportunity
        if total_monthly > 100 and environment == "production":
            annual_cost = total_monthly * 12
            ri_savings = annual_cost * 0.35  # ~35% savings with 1-year RI

            recommendations.append(OptimizationRecommendation(
                recommendation_id=str(uuid.uuid4()),
                recommendation_type=RecommendationType.RESERVED_INSTANCE,
                title="Consider Reserved Instances for Production",
                description=(
                    f"Your production workload costs ${total_monthly:.2f}/month. "
                    f"A 1-year Reserved Instance commitment could save ~${ri_savings:.2f}/year."
                ),
                estimated_monthly_savings=ri_savings / 12,
                estimated_annual_savings=ri_savings,
                savings_percentage=35.0,
                confidence=0.85,
                strength=RecommendationStrength.STRONG,
                action_required="Purchase Reserved Instances through AWS Console or API",
                implementation_effort="low",
                risk_level="low",
                affected_resources=[r.resource_name for r in cost_breakdown],
                prerequisites=["Stable, predictable workload", "1-year commitment"],
                trade_offs=["Upfront commitment", "Less flexibility"],
                suitable_for=["Production workloads", "Stable traffic patterns"],
                not_suitable_for=["Variable workloads", "Short-term projects"],
            ))

        # Check for Savings Plans opportunity
        if total_monthly > 200:
            sp_savings = total_monthly * 12 * 0.30  # ~30% savings

            recommendations.append(OptimizationRecommendation(
                recommendation_id=str(uuid.uuid4()),
                recommendation_type=RecommendationType.SAVINGS_PLAN,
                title="Consider Compute Savings Plans",
                description=(
                    f"With ${total_monthly:.2f}/month in compute costs, "
                    f"a Compute Savings Plan could save ~${sp_savings:.2f}/year "
                    "with more flexibility than Reserved Instances."
                ),
                estimated_monthly_savings=sp_savings / 12,
                estimated_annual_savings=sp_savings,
                savings_percentage=30.0,
                confidence=0.80,
                strength=RecommendationStrength.MODERATE,
                action_required="Purchase Savings Plan through AWS Console",
                implementation_effort="low",
                risk_level="low",
                affected_resources=[r.resource_name for r in cost_breakdown],
                prerequisites=["Consistent compute usage"],
                trade_offs=["1-year commitment"],
                suitable_for=["Any compute workload", "Multi-region deployments"],
                not_suitable_for=["Highly variable usage"],
            ))

        # Check for auto-scaling opportunity
        has_compute = any(
            r.get("type") in ["ec2", "instance", "compute"] for r in resources
        )
        if has_compute and environment in ["production", "staging"]:
            recommendations.append(OptimizationRecommendation(
                recommendation_id=str(uuid.uuid4()),
                recommendation_type=RecommendationType.AUTO_SCALING,
                title="Implement Auto Scaling",
                description=(
                    "Add Auto Scaling to automatically adjust capacity based on demand. "
                    "This can reduce costs during low-traffic periods by 20-40%."
                ),
                estimated_monthly_savings=total_monthly * 0.25,
                estimated_annual_savings=total_monthly * 12 * 0.25,
                savings_percentage=25.0,
                confidence=0.70,
                strength=RecommendationStrength.MODERATE,
                action_required="Configure Auto Scaling Group with appropriate policies",
                implementation_effort="medium",
                risk_level="low",
                affected_resources=[
                    r.resource_name for r in cost_breakdown
                    if r.service in ["ec2", "instance", "compute"]
                ],
                prerequisites=["Stateless application design", "Health checks configured"],
                trade_offs=["Additional complexity", "Potential cold start latency"],
                suitable_for=["Variable traffic patterns", "Web applications"],
                not_suitable_for=["Stateful applications", "Constant load workloads"],
            ))

        # Check for storage tiering opportunity
        has_storage = any(r.get("type") in ["s3", "storage"] for r in resources)
        if has_storage:
            recommendations.append(OptimizationRecommendation(
                recommendation_id=str(uuid.uuid4()),
                recommendation_type=RecommendationType.STORAGE_TIERING,
                title="Use S3 Intelligent-Tiering",
                description=(
                    "S3 Intelligent-Tiering automatically moves data between access tiers "
                    "based on usage patterns, potentially saving 40-70% on storage costs."
                ),
                estimated_monthly_savings=total_monthly * 0.10,  # Conservative estimate
                estimated_annual_savings=total_monthly * 12 * 0.10,
                savings_percentage=40.0,
                confidence=0.75,
                strength=RecommendationStrength.MODERATE,
                action_required="Enable S3 Intelligent-Tiering on buckets",
                implementation_effort="low",
                risk_level="low",
                affected_resources=[
                    r.resource_name for r in cost_breakdown
                    if r.service in ["s3", "storage"]
                ],
                prerequisites=["Objects > 128KB"],
                trade_offs=["Small monitoring fee per object"],
                suitable_for=["Unknown access patterns", "Mixed access data"],
                not_suitable_for=["Frequently accessed data only"],
            ))

        # Budget warning recommendation
        if budget_status and budget_status.utilization_percent > 80:
            recommendations.append(OptimizationRecommendation(
                recommendation_id=str(uuid.uuid4()),
                recommendation_type=RecommendationType.RIGHTSIZING,
                title="⚠️ Budget Alert: Consider Cost Reduction",
                description=(
                    f"Your budget is {budget_status.utilization_percent:.1f}% utilized. "
                    f"Only ${budget_status.remaining:.2f} remaining. "
                    "Consider using the budget-compliant alternative above."
                ),
                estimated_monthly_savings=budget_status.exceeded_by or 0,
                estimated_annual_savings=(budget_status.exceeded_by or 0) * 12,
                savings_percentage=0,
                confidence=1.0,
                strength=RecommendationStrength.STRONG,
                action_required="Review and reduce resource specifications",
                implementation_effort="medium",
                risk_level="medium",
                affected_resources=[r.resource_name for r in cost_breakdown],
                prerequisites=[],
                trade_offs=["Reduced capacity"],
                suitable_for=["Budget-constrained projects"],
                not_suitable_for=[],
            ))

        return recommendations

    async def _get_unit_economics(self, user_id: str) -> UnitEconomics | None:
        """Get unit economics context for the user.

        Enhanced to use the new UnitEconomicsService when cost records are available.
        """
        if not self.spending_tracker:
            return None

        try:
            # Get spending breakdown by environment and cloud
            summary = await self.spending_tracker.get_spending_summary(
                user_id=user_id,
                days=30,
            )

            if not summary:
                return None

            # Calculate unit economics
            cost_per_env = summary.get("by_environment", {})
            cost_per_cloud = summary.get("by_cloud", {})
            cost_per_service = summary.get("by_service", {})

            # Calculate dev to prod ratio
            dev_cost = cost_per_env.get("development", 0) + cost_per_env.get("dev", 0)
            prod_cost = cost_per_env.get("production", 0) + cost_per_env.get("prod", 0)
            dev_to_prod = dev_cost / prod_cost if prod_cost > 0 else None

            total_cost = sum(cost_per_env.values())
            non_prod = total_cost - prod_cost
            non_prod_pct = (non_prod / total_cost * 100) if total_cost > 0 else None

            # Calculate cost trend
            trend_data = summary.get("trend", {})
            cost_trend = trend_data.get("direction", "stable")
            mom_change = trend_data.get("month_over_month_change")

            return UnitEconomics(
                cost_per_environment=cost_per_env,
                cost_per_cloud=cost_per_cloud,
                cost_per_service_category=cost_per_service,
                dev_to_prod_ratio=dev_to_prod,
                non_prod_percentage=non_prod_pct,
                cost_trend=cost_trend,
                month_over_month_change=mom_change,
            )
        except Exception as e:
            logger.warning("Failed to get unit economics: %s", e)
            return None

    async def generate_efficiency_context(
        self,
        user_id: str,
        cost_records: list | None = None,
    ) -> dict:
        """Generate efficiency metrics context for AI assistants.

        This provides efficiency KPIs and benchmarks during code generation.

        Args:
            user_id: User ID for context
            cost_records: Optional cost records for analysis

        Returns:
            Dictionary with efficiency metrics and recommendations
        """
        from wistx_mcp.tools.lib.cost_intelligence.efficiency_metrics import (
            EfficiencyMetricsCalculator,
        )

        calculator = EfficiencyMetricsCalculator()

        # If no cost records provided, try to get from spending tracker
        if not cost_records and self.spending_tracker:
            try:
                # Get raw cost data if available
                raw_data = await self.spending_tracker.get_raw_cost_data(
                    user_id=user_id,
                    days=30,
                )
                if raw_data:
                    cost_records = raw_data
            except Exception as e:
                logger.debug("Could not get raw cost data: %s", e)

        if not cost_records:
            return {
                "efficiency_available": False,
                "message": "No cost data available for efficiency analysis",
            }

        # Generate efficiency report
        report = calculator.generate_efficiency_report(cost_records)

        return {
            "efficiency_available": True,
            "overall_score": report.overall_efficiency_score,
            "overall_status": report.overall_status.value,
            "kpis": [
                {
                    "name": kpi.name,
                    "value": kpi.value,
                    "unit": kpi.unit,
                    "status": kpi.status.value,
                    "target": kpi.target,
                    "insight": kpi.insight,
                    "recommendation": kpi.recommendation,
                }
                for kpi in report.kpis
            ],
            "critical_issues": report.critical_issues,
            "warnings": report.warnings,
            "recommendations": report.recommendations[:5],  # Top 5
            "savings_potential": report.total_savings_potential,
            "quick_wins": report.quick_wins,
        }

    async def generate_allocation_context(
        self,
        user_id: str,
        resources: list[dict] | None = None,
        environment: str | None = None,
        team: str | None = None,
        project: str | None = None,
    ) -> dict:
        """Generate cost allocation context for AI assistants.

        Provides tagging recommendations and allocation guidance.

        Args:
            user_id: User ID for context
            resources: Resources being created
            environment: Target environment
            team: Team name
            project: Project name

        Returns:
            Dictionary with allocation guidance
        """
        from wistx_mcp.tools.lib.cost_intelligence.cost_allocation import (
            CostAllocationEngine,
        )

        engine = CostAllocationEngine()

        result = {
            "allocation_guidance_available": True,
            "required_tags": engine.RECOMMENDED_TAGS,
        }

        # Generate tagging recommendations for new resources
        if resources:
            recommendations = engine.generate_tagging_recommendations(
                resources=resources,
                environment=environment,
                team=team,
                project=project,
            )
            result["tagging_recommendations"] = recommendations

            # Calculate tagging completeness
            total_tags_needed = len(engine.RECOMMENDED_TAGS) * len(resources)
            tags_present = sum(
                len(r.get("tags", {})) for r in resources
            )
            result["tagging_completeness"] = (
                (tags_present / total_tags_needed * 100)
                if total_tags_needed > 0 else 0
            )

        # Add allocation best practices
        result["best_practices"] = [
            "Always tag resources with Team, Environment, and Project",
            "Use consistent tag values across all resources",
            "Include CostCenter for chargeback/showback",
            "Add Owner tag for accountability",
        ]

        return result
