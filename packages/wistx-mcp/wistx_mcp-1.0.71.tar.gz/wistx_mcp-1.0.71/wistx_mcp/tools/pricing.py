"""Pricing tool - calculate infrastructure costs.

Provides intelligent cost estimation with:
- Real-time pricing data
- Budget integration and enforcement
- Context-aware optimization recommendations
- Cost-optimized alternatives
- Unit economics context
- Advanced optimization: Spot, Reserved Instances, Savings Plans, Rightsizing

This exceeds industry standards by providing cost intelligence
during code generation, not post-deployment.

Industry Comparison:
- Traditional FinOps: Post-deployment dashboards (CloudZero, Finout)
- Infracost: PR-level cost estimation
- WISTX: Real-time during code generation with proactive optimization
"""

import logging
from typing import Any

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.auth_context import get_auth_context

logger = logging.getLogger(__name__)


def _map_workload_type(environment: str | None, service: str) -> str:
    """Map environment and service to workload type for optimization analysis."""
    service_lower = service.lower() if service else ""

    # Map common services to workload types
    if "lambda" in service_lower or "function" in service_lower:
        return "serverless"
    elif "batch" in service_lower:
        return "batch_processing"
    elif "eks" in service_lower or "ecs" in service_lower or "container" in service_lower:
        return "containerized"
    elif "rds" in service_lower or "database" in service_lower or "aurora" in service_lower:
        return "database"
    elif "ml" in service_lower or "sagemaker" in service_lower:
        return "ml_training"
    elif "ec2" in service_lower:
        # EC2 depends on environment
        if environment and environment.lower() in ["dev", "development", "test", "staging"]:
            return "dev_test"
        return "web_api"

    # Default based on environment
    if environment:
        env_lower = environment.lower()
        if env_lower in ["dev", "development"]:
            return "dev_test"
        elif env_lower in ["ci", "cd", "pipeline"]:
            return "ci_cd"

    return "web_api"  # Default


def extract_scope_from_resources(resources: list[dict[str, Any]]) -> dict[str, Any]:
    """Extract budget scope from resource specifications.

    Args:
        resources: List of resource specifications

    Returns:
        Scope dictionary for budget checking
    """
    cloud_providers = list(set(r.get("cloud") for r in resources if r.get("cloud")))
    environment_name = None
    
    for resource in resources:
        env_name = resource.get("environment") or resource.get("environment_name")
        if env_name:
            environment_name = env_name.lower()
            break

    return {
        "cloud_providers": cloud_providers,
        "environment_name": environment_name,
    }


async def calculate_infrastructure_cost(
    resources: list[dict[str, Any]],
    user_id: str | None = None,
    check_budgets: bool = True,
    environment_name: str | None = None,
    include_existing: bool = True,
) -> dict[str, Any]:
    """Calculate infrastructure costs.

    Args:
        resources: List of resource specifications
            Example: [{"cloud": "aws", "service": "rds", "instance_type": "db.t3.medium", "quantity": 1}]
        user_id: User ID for budget checking
        check_budgets: Whether to check budgets
        environment_name: Environment name for budget scoping
        include_existing: Whether to include existing infrastructure spending in breakdown

    Returns:
        Dictionary with cost breakdown and optimizations

    Raises:
        RuntimeError: If quota is exceeded
    """
    auth_ctx = get_auth_context()
    if auth_ctx:
        auth_user_id = auth_ctx.get_user_id()
        if auth_user_id:
            try:
                from api.services.quota_service import quota_service, QuotaExceededError

                plan = "professional"
                if auth_ctx.user_info:
                    plan = auth_ctx.user_info.get("plan", "professional")
                await quota_service.check_query_quota(auth_user_id, plan)
                if not user_id:
                    user_id = auth_user_id
            except ImportError:
                logger.debug("API quota service not available, skipping quota check")
            except QuotaExceededError as e:
                logger.warning("Quota exceeded for user %s: %s", auth_user_id, e)
                raise RuntimeError(f"Quota exceeded: {e}") from e
            except Exception as e:
                logger.warning("Failed to check quota (continuing): %s", e)

    async with MongoDBClient() as client:

        total_monthly = 0.0
        breakdown = []

        for resource in resources:
            cloud = resource.get("cloud", "aws")
            service = resource.get("service", "")
            instance_type = resource.get("instance_type", "")
            quantity = resource.get("quantity", 1)
            region = resource.get("region")

            try:
                pricing_data = await client.get_pricing(
                    cloud=cloud,
                    service=service,
                    instance_type=instance_type,
                    region=region,
                )

                if not pricing_data:
                    breakdown.append({
                        "resource": f"{cloud}:{service}:{instance_type}",
                        "quantity": quantity,
                        "monthly": 0.0,
                        "annual": 0.0,
                        "error": "Pricing data not available",
                    })
                    continue

                monthly_cost = pricing_data.get("monthly_cost", 0) * quantity
                total_monthly += monthly_cost

                breakdown.append({
                    "resource": f"{cloud}:{service}:{instance_type}",
                    "quantity": quantity,
                    "monthly": round(monthly_cost, 2),
                    "annual": round(monthly_cost * 12, 2),
                    "region": pricing_data.get("region_id"),
                    "pricing_category": pricing_data.get("pricing_category"),
                })
            except Exception as e:
                logger.error(
                    "Error getting pricing for %s:%s:%s: %s",
                    cloud,
                    service,
                    instance_type,
                    e,
                    exc_info=True,
                )
                breakdown.append({
                    "resource": f"{cloud}:{service}:{instance_type}",
                    "quantity": quantity,
                    "monthly": 0.0,
                    "annual": 0.0,
                    "error": str(e),
                })

        # Generate intelligent, context-aware recommendations
        optimizations = []
        alternatives = []
        cost_context = None
        advanced_optimization = {}

        try:
            from wistx_mcp.tools.lib.cost_intelligence import CostContextGenerator

            # Create cost context generator
            context_gen = CostContextGenerator(pricing_data={})

            # Generate rich cost context
            cost_context = await context_gen.generate_context(
                user_id=user_id or "anonymous",
                resources=resources,
                cloud_provider=resources[0].get("cloud", "aws") if resources else "aws",
                environment=environment_name,
            )

            # Extract intelligent recommendations
            for rec in cost_context.optimization_recommendations:
                optimizations.append({
                    "title": rec.title,
                    "description": rec.description,
                    "type": rec.recommendation_type.value,
                    "estimated_monthly_savings": round(rec.estimated_monthly_savings, 2),
                    "estimated_annual_savings": round(rec.estimated_annual_savings, 2),
                    "savings_percentage": round(rec.savings_percentage, 1),
                    "strength": rec.strength.value,
                    "implementation_effort": rec.implementation_effort,
                    "risk_level": rec.risk_level,
                    "suitable_for": rec.suitable_for,
                    "not_suitable_for": rec.not_suitable_for,
                })

            # Extract cost-optimized alternatives
            for alt in cost_context.alternatives:
                alternatives.append({
                    "name": alt.name,
                    "description": alt.description,
                    "monthly_cost": round(alt.monthly_cost, 2),
                    "savings_amount": round(alt.savings_amount, 2),
                    "savings_percentage": round(alt.savings_percentage, 1),
                    "strength": alt.strength.value,
                    "trade_offs": alt.trade_offs,
                    "benefits": alt.benefits,
                    "suitable_for": alt.suitable_for,
                    "not_suitable_for": alt.not_suitable_for,
                })

        except ImportError:
            logger.debug("Cost intelligence module not available, using basic recommendations")
            # Fallback to basic recommendations if cost intelligence not available
            if total_monthly > 100:
                optimizations.append({
                    "title": "Consider Reserved Instances",
                    "description": "For stable workloads, Reserved Instances can save 30-40%",
                    "type": "reserved_instance",
                    "estimated_monthly_savings": round(total_monthly * 0.35, 2),
                    "estimated_annual_savings": round(total_monthly * 12 * 0.35, 2),
                    "savings_percentage": 35.0,
                    "strength": "moderate",
                    "implementation_effort": "low",
                    "risk_level": "low",
                })
            if total_monthly > 500:
                optimizations.append({
                    "title": "Review Instance Sizing",
                    "description": "High spend detected - review if instances are right-sized",
                    "type": "rightsizing",
                    "estimated_monthly_savings": round(total_monthly * 0.20, 2),
                    "estimated_annual_savings": round(total_monthly * 12 * 0.20, 2),
                    "savings_percentage": 20.0,
                    "strength": "moderate",
                    "implementation_effort": "medium",
                    "risk_level": "medium",
                })
        except Exception as e:
            logger.warning("Failed to generate cost context: %s", e)

        # Phase 3: Advanced Optimization Services
        # Spot, Reserved Instances, Savings Plans, Rightsizing
        try:
            from wistx_mcp.tools.lib.cost_intelligence import (
                OptimizationOrchestrator,
                SpotInstanceAdvisor,
                RightsizingAnalyzer,
                CommitmentOptimizer,
            )

            orchestrator = OptimizationOrchestrator()

            # Determine workload type from resources
            workload_type = "web_api"
            if resources:
                first_resource = resources[0]
                workload_type = _map_workload_type(
                    environment_name or first_resource.get("environment"),
                    first_resource.get("service", ""),
                )

            # Get code generation context for each EC2/compute resource
            code_guidance = []
            spot_recommendations = []
            rightsizing_recommendations = []

            for resource in resources:
                instance_type = resource.get("instance_type", "")
                service = resource.get("service", "").lower()
                region = resource.get("region", "us-east-1")

                # Only analyze compute resources for advanced optimization
                if service not in ["ec2", "rds", "elasticache", "redshift", "eks", "ecs"]:
                    continue

                # Get optimization context for this resource
                ctx = orchestrator.get_code_generation_context(
                    instance_type=instance_type,
                    region=region,
                    workload_type=workload_type,
                    environment=environment_name or "production",
                    monthly_budget=None,
                )

                # Collect Spot recommendations
                if ctx.get("spot_recommendation", {}).get("suitable"):
                    spot_rec = ctx["spot_recommendation"]
                    spot_recommendations.append({
                        "instance_type": instance_type,
                        "suitable": True,
                        "savings_percentage": round(spot_rec.get("savings_percentage", 0), 1),
                        "monthly_savings": round(spot_rec.get("monthly_savings", 0), 2),
                        "allocation_strategy": spot_rec.get("allocation_strategy", "diversified"),
                        "fallback_instances": spot_rec.get("fallback_instances", [])[:3],
                        "recommended_spot_percentage": spot_rec.get("recommended_spot_percentage", 70),
                    })

                # Collect sizing recommendations
                if ctx.get("sizing_recommendation"):
                    sizing = ctx["sizing_recommendation"]
                    if sizing.get("suggested_type") != instance_type:
                        rightsizing_recommendations.append({
                            "current_type": instance_type,
                            "suggested_type": sizing.get("suggested_type"),
                            "suggested_vcpu": sizing.get("suggested_vcpu"),
                            "suggested_memory_gb": sizing.get("suggested_memory_gb"),
                        })

                # Collect code guidance
                for rec in ctx.get("recommendations", []):
                    if rec not in code_guidance:
                        code_guidance.append(rec)

            # Build advanced optimization summary
            advanced_optimization = {
                "spot_recommendations": spot_recommendations,
                "rightsizing_recommendations": rightsizing_recommendations,
                "code_generation_guidance": code_guidance[:5],  # Top 5 guidance items
            }

            # Add commitment recommendation for production
            if environment_name and environment_name.lower() in ["production", "prod"]:
                advanced_optimization["commitment_recommendation"] = {
                    "should_consider": True,
                    "recommendation": "Consider Reserved Instances or Savings Plans for stable production workloads",
                    "typical_savings_ri": "31-58% (depending on term and payment option)",
                    "typical_savings_sp": "28-52% (depending on term and payment option)",
                    "ri_vs_sp": "RIs offer slightly higher discounts but less flexibility; Savings Plans offer more flexibility across instance families",
                }

            # Calculate total potential savings from advanced optimizations
            total_spot_savings = sum(r.get("monthly_savings", 0) for r in spot_recommendations)
            if total_spot_savings > 0:
                advanced_optimization["total_potential_spot_savings"] = round(total_spot_savings, 2)
                advanced_optimization["total_potential_spot_savings_annual"] = round(total_spot_savings * 12, 2)

        except ImportError:
            logger.debug("Advanced optimization modules not available")
        except Exception as e:
            logger.warning("Failed to generate advanced optimization: %s", e)

        result = {
            "total_monthly": round(total_monthly, 2),
            "total_annual": round(total_monthly * 12, 2),
            "breakdown": breakdown,
            "optimizations": optimizations,
            "alternatives": alternatives,
        }

        # Add advanced optimization (Phase 3: Spot, RI/SP, Rightsizing)
        if advanced_optimization:
            result["advanced_optimization"] = advanced_optimization

        # Add cost context summary if available
        if cost_context:
            result["cost_context"] = {
                "context_id": cost_context.context_id,
                "budget_will_exceed": cost_context.budget_will_exceed,
                "budget_remaining": cost_context.budget_remaining,
                "budget_exceeded_by": cost_context.budget_exceeded_by,
                "anomaly_risk": cost_context.anomaly_risk,
            }

            # Add unit economics if available
            if cost_context.unit_economics:
                result["unit_economics"] = {
                    "cost_per_environment": cost_context.unit_economics.cost_per_environment,
                    "cost_per_cloud": cost_context.unit_economics.cost_per_cloud,
                    "dev_to_prod_ratio": cost_context.unit_economics.dev_to_prod_ratio,
                    "non_prod_percentage": cost_context.unit_economics.non_prod_percentage,
                }

        if include_existing and user_id:
            try:
                from api.services.budget_service import budget_service

                scope = extract_scope_from_resources(resources)
                if environment_name:
                    scope["environment_name"] = environment_name.lower()

                applicable_budgets = await budget_service._find_applicable_budgets(user_id, scope)
                existing_total = 0.0

                for budget in applicable_budgets:
                    status = await budget_service.get_budget_status(budget.budget_id)
                    if status:
                        existing_total += status.total_spent_usd

                if existing_total > 0:
                    result["existing_monthly"] = round(existing_total, 2)
                    result["existing_annual"] = round(existing_total * 12, 2)
                    result["total_with_existing"] = round(existing_total + total_monthly, 2)
                    result["breakdown"].insert(0, {
                        "resource": "Existing Infrastructure",
                        "quantity": 1,
                        "monthly": round(existing_total, 2),
                        "annual": round(existing_total * 12, 2),
                        "region": None,
                        "pricing_category": "existing",
                        "category": "existing",
                    })
            except ImportError:
                logger.debug("API budget service not available, skipping existing spending check")
            except Exception as e:
                logger.warning("Failed to include existing spending: %s", e)

        if check_budgets and user_id:
            try:
                from api.services.budget_service import budget_service
                from api.models.budget import EnforcementMode

                scope = extract_scope_from_resources(resources)
                if environment_name:
                    scope["environment_name"] = environment_name.lower()

                budget_check = await budget_service.check_budgets(
                    user_id=user_id,
                    estimated_cost=total_monthly,
                    scope=scope,
                )

                result["budget_check"] = budget_check

                if budget_check["status"] == "exceeded":
                    blocking_budgets = [
                        bs for bs in budget_check["applicable_budgets"]
                        if bs["status"] == "exceeded"
                        and bs.get("enforcement_mode") == EnforcementMode.BLOCK.value
                    ]
                    if blocking_budgets:
                        budget_names = [bs["name"] for bs in blocking_budgets]
                        raise ValueError(
                            f"Budget exceeded - infrastructure creation blocked. "
                            f"Affected budgets: {', '.join(budget_names)}. "
                            f"Projected spending: ${total_monthly:.2f}/month exceeds budget limits."
                        )
            except ImportError:
                logger.debug("API budget service not available, skipping budget check")
            except ValueError:
                raise
            except Exception as e:
                logger.warning("Budget check failed (continuing without enforcement): %s", e)

        return result

