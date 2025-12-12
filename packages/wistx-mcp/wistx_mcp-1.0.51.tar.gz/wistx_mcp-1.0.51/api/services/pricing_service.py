"""Pricing service - business logic for infrastructure cost calculation."""

import logging
import time
from typing import Any

from api.models.v1_requests import PricingCalculationRequest
from api.models.v1_responses import (
    BudgetCheckResponse,
    CostBreakdownItem,
    PricingCalculationResponse,
)
from wistx_mcp.tools.pricing import calculate_infrastructure_cost as mcp_calculate_cost
from api.exceptions import ValidationError, ExternalServiceError

logger = logging.getLogger(__name__)


class PricingService:
    """Service for infrastructure cost calculation operations."""

    async def calculate_infrastructure_cost(
        self,
        request: PricingCalculationRequest,
        user_id: str,
        request_id: str | None = None,
    ) -> PricingCalculationResponse:
        """Calculate infrastructure costs from resource specifications.

        Args:
            request: Pricing calculation request with resource specifications
            user_id: User ID for budget checking
            request_id: Optional request ID for tracing

        Returns:
            Pricing calculation response with cost breakdown and optimizations

        Raises:
            ValueError: If budget exceeded and blocking budgets are enforced
            RuntimeError: If calculation fails
        """
        start_time = time.time()

        try:
            resources_dict = [
                {
                    "cloud": resource.cloud,
                    "service": resource.service,
                    "instance_type": resource.instance_type,
                    "quantity": resource.quantity,
                    "region": resource.region,
                    "environment": resource.environment or resource.environment_name,
                    "environment_name": resource.environment_name or resource.environment,
                }
                for resource in request.resources
            ]

            result = await mcp_calculate_cost(
                resources=resources_dict,
                user_id=user_id,
                check_budgets=request.check_budgets,
                environment_name=request.environment_name,
                include_existing=request.include_existing,
            )

            breakdown_items = [
                CostBreakdownItem(
                    resource=item.get("resource", ""),
                    quantity=item.get("quantity", 1),
                    monthly=item.get("monthly", 0.0),
                    annual=item.get("annual", 0.0),
                    region=item.get("region"),
                    pricing_category=item.get("pricing_category"),
                    category=item.get("category"),
                    error=item.get("error"),
                )
                for item in result.get("breakdown", [])
            ]

            budget_check = None
            if result.get("budget_check"):
                budget_check_data = result["budget_check"]
                budget_check = BudgetCheckResponse(
                    status=budget_check_data.get("status", "within_limit"),
                    applicable_budgets=budget_check_data.get("applicable_budgets", []),
                    projected_total=budget_check_data.get("projected_total", result.get("total_monthly", 0.0)),
                )

            query_time_ms = int((time.time() - start_time) * 1000)

            response = PricingCalculationResponse(
                total_monthly=result.get("total_monthly", 0.0),
                total_annual=result.get("total_annual", 0.0),
                breakdown=breakdown_items,
                optimizations=result.get("optimizations", []),
                existing_monthly=result.get("existing_monthly"),
                existing_annual=result.get("existing_annual"),
                total_with_existing=result.get("total_with_existing"),
                budget_check=budget_check,
            )

            logger.info(
                "Cost calculation completed: total_monthly=%.2f, resources=%d, query_time_ms=%d [request_id=%s]",
                response.total_monthly,
                len(request.resources),
                query_time_ms,
                request_id or "unknown",
            )

            return response

        except ValueError as e:
            if "Budget exceeded" in str(e):
                logger.warning(
                    "Budget exceeded for user %s: %s [request_id=%s]",
                    user_id,
                    e,
                    request_id or "unknown",
                )
                raise ValidationError(
                    message=str(e),
                    user_message="Budget limit exceeded. Please adjust your infrastructure configuration or increase your budget.",
                    error_code="BUDGET_EXCEEDED",
                    details={"request_id": request_id, "user_id": user_id}
                ) from e
            raise ValidationError(
                message=str(e),
                user_message="Invalid request parameters",
                error_code="INVALID_REQUEST",
                details={"request_id": request_id, "error": str(e)}
            ) from e
        except Exception as e:
            logger.error(
                "Error calculating infrastructure costs: %s [request_id=%s]",
                e,
                request_id or "unknown",
                exc_info=True,
            )
            raise ExternalServiceError(
                message=f"Failed to calculate infrastructure costs: {e}",
                user_message="Unable to calculate infrastructure costs. Please try again later.",
                error_code="COST_CALCULATION_ERROR",
                details={"request_id": request_id, "user_id": user_id}
            ) from e


pricing_service = PricingService()

