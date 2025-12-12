"""Spending tracker service - tracks actual spending from created infrastructure."""

import logging
from datetime import datetime
from typing import Any, Optional

from bson import ObjectId

from api.database.mongodb import mongodb_manager
from api.services.budget_service import budget_service

logger = logging.getLogger(__name__)


class SpendingTracker:
    """Service for tracking spending from created infrastructure resources."""

    async def track_infrastructure_creation(
        self,
        user_id: str,
        resources: list[dict[str, Any]],
        cloud_provider: str,
        environment_name: Optional[str] = None,
        source_type: str = "infrastructure_creation",
        source_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Track spending from infrastructure resources created by coding agents.

        This method should be called when coding agents create infrastructure.
        It calculates costs and records spending against applicable budgets.
        Automatically generates a cost report.

        Args:
            user_id: User ID
            resources: List of resource specifications
                Example: [
                    {"cloud": "aws", "service": "rds", "instance_type": "db.t3.medium", "quantity": 1},
                    {"cloud": "aws", "service": "ec2", "instance_type": "t3.medium", "quantity": 2},
                ]
            cloud_provider: Cloud provider (aws, gcp, azure, etc.)
            environment_name: Environment name (dev, stage, prod, etc.)
            source_type: Source type (infrastructure_creation, manual_entry, etc.)
            source_id: Source ID (resource ID, deployment ID, etc.)

        Returns:
            Dictionary with tracking results and report information
        """
        if not resources:
            return {
                "spending_tracked": False,
                "error": "No resources provided",
            }

        try:
            from wistx_mcp.tools.pricing import calculate_infrastructure_cost

            cost_result = await calculate_infrastructure_cost(
                resources=resources,
                user_id=user_id,
                check_budgets=False,
                environment_name=environment_name,
            )

            total_monthly = cost_result.get("total_monthly", 0.0)

            if total_monthly <= 0:
                logger.debug("No cost calculated for resources, skipping spending tracking")
                return {
                    "spending_tracked": False,
                    "error": "No cost calculated for resources",
                }

            for resource in resources:
                service = resource.get("service", "")
                resource_type = resource.get("instance_type", "")
                quantity = resource.get("quantity", 1)

                resource_cost = 0.0
                for breakdown_item in cost_result.get("breakdown", []):
                    if (
                        cloud_provider in breakdown_item.get("resource", "")
                        and service in breakdown_item.get("resource", "")
                        and resource_type in breakdown_item.get("resource", "")
                    ):
                        resource_cost = breakdown_item.get("monthly", 0.0) / quantity
                        break

                if resource_cost > 0:
                    await budget_service.record_spending(
                        user_id=user_id,
                        amount_usd=resource_cost * quantity,
                        source_type=source_type,
                        source_id=source_id or f"{cloud_provider}:{service}:{resource_type}",
                        component_id=None,
                        cloud_provider=cloud_provider,
                        environment_name=environment_name,
                        service=service,
                        resource_type=resource_type,
                        resource_spec=resource,
                    )

            logger.info(
                "Tracked spending: $%.2f/month for user %s (%d resources)",
                total_monthly,
                user_id,
                len(resources),
            )

            report_info = await self._generate_cost_report(
                user_id=user_id,
                resources=resources,
                cost_result=cost_result,
                source_id=source_id,
                environment_name=environment_name,
            )

            return {
                "spending_tracked": True,
                "total_monthly": total_monthly,
                "resources_count": len(resources),
                "report_id": report_info.get("report_id"),
                "report_download_url": report_info.get("download_url"),
            }
        except Exception as e:
            logger.error(
                "Failed to track infrastructure spending: %s",
                e,
                exc_info=True,
            )
            return {
                "spending_tracked": False,
                "error": str(e),
            }

    async def track_from_cloud_billing(
        self,
        user_id: str,
        cloud_provider: str,
        billing_data: list[dict[str, Any]],
        environment_name: Optional[str] = None,
    ) -> None:
        """Track spending from cloud provider billing data.

        This method processes actual billing data from cloud providers
        (AWS Cost Explorer, GCP Billing API, Azure Cost Management, etc.)

        Args:
            user_id: User ID
            cloud_provider: Cloud provider (aws, gcp, azure, etc.)
            billing_data: List of billing records from cloud provider
                Example: [
                    {
                        "service": "rds",
                        "resource_type": "db.t3.medium",
                        "amount_usd": 50.0,
                        "period": "2024-12",
                        "tags": {"Environment": "prod"},
                    },
                ]
            environment_name: Environment name (if not in tags)
        """
        for record in billing_data:
            amount = record.get("amount_usd", 0)
            if amount <= 0:
                continue

            env_name = (
                record.get("tags", {}).get("Environment")
                or record.get("tags", {}).get("environment")
                or environment_name
            )

            await budget_service.record_spending(
                user_id=user_id,
                amount_usd=amount,
                source_type="cloud_billing",
                source_id=record.get("resource_id") or record.get("resource_arn"),
                component_id=None,
                cloud_provider=cloud_provider,
                environment_id=None,
                environment_name=env_name,
                service=record.get("service"),
                resource_type=record.get("resource_type"),
                resource_spec=record,
            )

        logger.info(
            "Tracked spending from %s billing: %d records for user %s",
            cloud_provider,
            len(billing_data),
            user_id,
        )

    async def sync_cloud_spending(
        self,
        user_id: str,
        cloud_provider: str,
        start_date: datetime,
        end_date: datetime,
    ) -> dict[str, Any]:
        """Sync spending from cloud provider billing APIs.

        NOTE: This is a placeholder - cloud billing API integration is not yet implemented.
        The system currently relies on agent reporting for spending tracking.

        To implement this, you would need:
        - Customer cloud provider credentials/API keys storage
        - AWS Cost Explorer API integration
        - GCP Billing API integration
        - Azure Cost Management API integration
        - User consent and credential management

        Args:
            user_id: User ID
            cloud_provider: Cloud provider (aws, gcp, azure, etc.)
            start_date: Start date for billing period
            end_date: End date for billing period

        Returns:
            Dictionary with sync results (currently always returns 0 synced)
        """
        logger.debug(
            "Cloud billing sync called for %s (user %s) - not yet implemented, relying on agent reporting",
            cloud_provider,
            user_id,
        )

        try:
            if cloud_provider.lower() == "aws":
                billing_data = await self._fetch_aws_billing(user_id, start_date, end_date)
            elif cloud_provider.lower() == "gcp":
                billing_data = await self._fetch_gcp_billing(user_id, start_date, end_date)
            elif cloud_provider.lower() == "azure":
                billing_data = await self._fetch_azure_billing(user_id, start_date, end_date)
            else:
                logger.warning("Unsupported cloud provider: %s", cloud_provider)
                return {"synced": 0, "errors": 1}

            if billing_data:
                await self.track_from_cloud_billing(user_id, cloud_provider, billing_data)
                return {"synced": len(billing_data), "errors": 0}

            return {"synced": 0, "errors": 0}
        except Exception as e:
            logger.debug(
                "Cloud billing sync not implemented for %s: %s",
                cloud_provider,
                e,
            )
            return {"synced": 0, "errors": 0}

    async def _fetch_aws_billing(
        self,
        user_id: str,
        start_date: datetime,
        end_date: datetime,
    ) -> list[dict[str, Any]]:
        """Fetch billing data from AWS Cost Explorer API.

        NOTE: This is a placeholder - AWS Cost Explorer API integration is not yet implemented.
        To implement this, you would need:
        - Customer AWS credentials (access key, secret key)
        - AWS Cost Explorer API client setup
        - Proper IAM permissions for Cost Explorer
        - User consent and credential storage

        Args:
            user_id: User ID
            start_date: Start date
            end_date: End date

        Returns:
            List of billing records (currently empty - placeholder)
        """
        logger.debug(
            "AWS billing fetch called for user %s - not yet implemented (placeholder)",
            user_id,
        )
        return []

    async def _fetch_gcp_billing(
        self,
        user_id: str,
        start_date: datetime,
        end_date: datetime,
    ) -> list[dict[str, Any]]:
        """Fetch billing data from GCP Billing API.

        NOTE: This is a placeholder - GCP Billing API integration is not yet implemented.
        To implement this, you would need:
        - Customer GCP service account credentials
        - GCP Billing API client setup
        - Proper IAM permissions for billing data
        - User consent and credential storage

        Args:
            user_id: User ID
            start_date: Start date
            end_date: End date

        Returns:
            List of billing records (currently empty - placeholder)
        """
        logger.debug(
            "GCP billing fetch called for user %s - not yet implemented (placeholder)",
            user_id,
        )
        return []

    async def _fetch_azure_billing(
        self,
        user_id: str,
        start_date: datetime,
        end_date: datetime,
    ) -> list[dict[str, Any]]:
        """Fetch billing data from Azure Cost Management API.

        NOTE: This is a placeholder - Azure Cost Management API integration is not yet implemented.
        To implement this, you would need:
        - Customer Azure service principal credentials
        - Azure Cost Management API client setup
        - Proper RBAC permissions for cost data
        - User consent and credential storage

        Args:
            user_id: User ID
            start_date: Start date
            end_date: End date

        Returns:
            List of billing records (currently empty - placeholder)
        """
        logger.debug(
            "Azure billing fetch called for user %s - not yet implemented (placeholder)",
            user_id,
        )
        return []

    async def _generate_cost_report(
        self,
        user_id: str,
        resources: list[dict[str, Any]],
        cost_result: dict[str, Any],
        source_id: Optional[str] = None,
        environment_name: Optional[str] = None,
    ) -> dict[str, Any]:
        """Generate cost report automatically after infrastructure creation.

        Args:
            user_id: User ID
            resources: List of resource specifications
            cost_result: Cost calculation result
            source_id: Source ID for report subject
            environment_name: Environment name

        Returns:
            Dictionary with report_id and download_url
        """
        try:
            from wistx_mcp.tools.lib.document_generator import DocumentGenerator
            from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
            from api.database.mongodb import mongodb_manager
            import base64
            from datetime import datetime

            mongodb_client = MongoDBClient()
            await mongodb_client.connect()
            try:
                doc_gen = DocumentGenerator(mongodb_client)
                
                subject = f"Infrastructure Creation"
                if source_id:
                    subject += f" - {source_id}"
                if environment_name:
                    subject += f" ({environment_name})"

                report_content = await doc_gen.generate_cost_report(
                    subject=subject,
                    resources=resources,
                )

                report_id = f"report-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{user_id[:8]}"
                
                db = mongodb_manager.get_database()
                reports_collection = db.reports

                content_b64 = base64.b64encode(report_content.encode("utf-8")).decode("utf-8")

                await reports_collection.insert_one({
                    "report_id": report_id,
                    "user_id": ObjectId(user_id),
                    "document_type": "cost_report",
                    "subject": subject,
                    "format": "markdown",
                    "content": content_b64,
                    "content_type": "text/markdown",
                    "sections": [],
                    "metadata": {
                        "source_type": "infrastructure_creation",
                        "source_id": source_id,
                        "environment_name": environment_name,
                        "total_monthly": cost_result.get("total_monthly", 0),
                        "resources_count": len(resources),
                    },
                    "created_at": datetime.utcnow(),
                })

                download_url = f"/v1/reports/{report_id}/download?format=markdown"

                logger.info("Generated cost report: %s for user %s", report_id, user_id)

                return {
                    "report_id": report_id,
                    "download_url": download_url,
                }
            finally:
                await mongodb_client.disconnect()
        except Exception as e:
            logger.warning("Failed to generate cost report: %s", e, exc_info=True)
            return {
                "report_id": None,
                "download_url": None,
            }

    async def record_manual_spending(
        self,
        user_id: str,
        amount_usd: float,
        cloud_provider: str,
        environment_name: Optional[str] = None,
        service: Optional[str] = None,
        resource_type: Optional[str] = None,
        description: Optional[str] = None,
        source_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Record spending for manually created or existing infrastructure.

        Use this method to record spending for infrastructure that was:
        - Created manually (not through coding agents)
        - Created before WISTX was implemented
        - Created outside the system
        - Needs to be tracked retroactively

        Args:
            user_id: User ID
            amount_usd: Monthly spending amount in USD
            cloud_provider: Cloud provider (aws, gcp, azure, etc.)
            environment_name: Environment name (dev, stage, prod, etc.)
            service: Service name (ec2, rds, s3, etc.)
            resource_type: Resource type (instance type, etc.)
            description: Description of the infrastructure
            source_id: Source ID (resource ID, etc.)

        Returns:
            Dictionary with recording results
        """
        try:
            await budget_service.record_spending(
                user_id=user_id,
                amount_usd=amount_usd,
                source_type="manual_entry",
                source_id=source_id or f"manual_{cloud_provider}_{service}",
                component_id=None,
                cloud_provider=cloud_provider,
                environment_name=environment_name,
                service=service,
                resource_type=resource_type,
                resource_spec={
                    "description": description,
                    "source": "manual_entry",
                },
            )

            logger.info(
                "Recorded manual spending: $%.2f/month for user %s (%s:%s)",
                amount_usd,
                user_id,
                cloud_provider,
                service or "unknown",
            )

            return {
                "spending_recorded": True,
                "amount_usd": amount_usd,
                "cloud_provider": cloud_provider,
                "environment_name": environment_name,
            }
        except Exception as e:
            logger.error(
                "Failed to record manual spending: %s",
                e,
                exc_info=True,
            )
            return {
                "spending_recorded": False,
                "error": str(e),
            }


spending_tracker = SpendingTracker()

