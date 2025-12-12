"""Pricing tool - calculate infrastructure costs."""

import logging
from typing import Any

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.auth_context import get_auth_context

logger = logging.getLogger(__name__)


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

        optimizations = []
        if total_monthly > 100:
            optimizations.append("Consider Reserved Instances for 30-40% savings")
        if total_monthly > 500:
            optimizations.append("Review instance sizing - may be over-provisioned")

        result = {
            "total_monthly": round(total_monthly, 2),
            "total_annual": round(total_monthly * 12, 2),
            "breakdown": breakdown,
            "optimizations": optimizations,
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

