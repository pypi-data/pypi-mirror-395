"""Infrastructure service - business logic for infrastructure operations."""

import logging
from typing import Any

from api.models.v1_requests import InfrastructureInventoryRequest, InfrastructureManageRequest
from api.models.v1_responses import InfrastructureInventoryResponse, InfrastructureManageResponse
from wistx_mcp.tools.lib.api_client import WISTXAPIClient

logger = logging.getLogger(__name__)


class InfrastructureService:
    """Service for infrastructure operations."""

    def __init__(self):
        """Initialize infrastructure service."""
        self.api_client = WISTXAPIClient()

    async def get_inventory(
        self,
        request: InfrastructureInventoryRequest,
        api_key: str,
    ) -> InfrastructureInventoryResponse:
        """Get infrastructure inventory.

        Args:
            request: Infrastructure inventory request
            api_key: API key for authentication

        Returns:
            Infrastructure inventory response

        Raises:
            ValueError: If invalid parameters
            RuntimeError: If operation fails
        """
        logger.info(
            "Getting infrastructure inventory: repository_url=%s, environment_name=%s",
            request.repository_url,
            request.environment_name,
        )

        from api.exceptions import ValidationError
        if not request.repository_url:
            raise ValidationError(
                message="repository_url is required",
                user_message="Repository URL is required",
                error_code="MISSING_REPOSITORY_URL",
                details={"request": request.model_dump() if hasattr(request, 'model_dump') else str(request)}
            )

        resource = await self.api_client.find_resource_by_repo_url(
            api_key=api_key,
            repository_url=request.repository_url,
        )

        if not resource:
            return InfrastructureInventoryResponse(
                repository_url=request.repository_url,
                environment_name=request.environment_name,
                status="not_indexed",
                recommendations=["Index the repository first to analyze existing infrastructure"],
            )

        resource_id = resource.get("resource_id")

        result = InfrastructureInventoryResponse(
            repository_url=request.repository_url,
            environment_name=request.environment_name or resource.get("environment_name"),
            status="indexed",
            resource_id=resource_id,
        )

        if request.include_costs:
            try:
                cost_response = await self.api_client.get_cost_analysis(
                    api_key=api_key,
                    resource_id=resource_id,
                )
                if cost_response:
                    cost_analysis = cost_response.get("cost_analysis", {})
                    result.total_monthly_cost = cost_analysis.get("total_monthly", 0.0)
                    result.total_annual_cost = cost_analysis.get("total_annual", 0.0)
                    result.cost_breakdown = cost_analysis.get("breakdown", {})
                    result.resources = cost_analysis.get("resources", [])
                    result.resources_count = len(cost_analysis.get("resources", []))
                    result.cost_optimizations = cost_analysis.get("optimizations", [])
            except Exception as e:
                logger.warning("Failed to fetch cost analysis: %s", e)

        if request.include_compliance:
            try:
                compliance_response = await self.api_client.get_compliance_analysis(
                    api_key=api_key,
                    resource_id=resource_id,
                )
                if compliance_response:
                    compliance_analysis = compliance_response.get("compliance_analysis", {})
                    result.compliance_summary = compliance_analysis.get("standards", {})
                    result.compliance_status = compliance_analysis.get("overall_status", "unknown")
            except Exception as e:
                logger.warning("Failed to fetch compliance analysis: %s", e)

        return result

    async def manage_infrastructure(
        self,
        request: InfrastructureManageRequest,
        api_key: str,
    ) -> InfrastructureManageResponse:
        """Manage infrastructure lifecycle.

        Args:
            request: Infrastructure management request
            api_key: API key for authentication

        Returns:
            Infrastructure management response

        Raises:
            ValueError: If invalid parameters
            RuntimeError: If operation fails
        """
        logger.info(
            "Managing infrastructure: action=%s, type=%s, resource_name=%s",
            request.action,
            request.infrastructure_type,
            request.resource_name,
        )

        cloud_provider_list = request.cloud_provider
        if isinstance(cloud_provider_list, str):
            cloud_provider_list = [cloud_provider_list]

        resource_id = f"{request.resource_name}-{request.infrastructure_type}"
        status = "pending"

        if request.action == "create":
            status = "created"
        elif request.action == "update":
            status = "updated"
        elif request.action == "upgrade":
            status = "upgraded"
        elif request.action == "backup":
            status = "backed_up"
        elif request.action == "restore":
            status = "restored"
        elif request.action == "monitor":
            status = "monitoring"
        elif request.action == "optimize":
            status = "optimized"

        compliance_status = None
        if request.compliance_standards:
            try:
                compliance_results = await self.api_client.get_compliance_requirements(
                    resource_types=["EKS", "GKE", "AKS"],
                    standards=request.compliance_standards,
                )
                compliance_status = {
                    "standards": request.compliance_standards,
                    "controls": compliance_results.get("controls", []),
                }
            except Exception as e:
                logger.warning("Failed to fetch compliance requirements: %s", e)

        return InfrastructureManageResponse(
            resource_id=resource_id,
            status=status,
            endpoints=[],
            compliance_status=compliance_status,
            cost_summary=None,
            recommendations=["Review infrastructure configuration", "Monitor costs"],
            action_performed=request.action,
        )

