"""Manage infrastructure tool - Kubernetes and multi-cloud lifecycle management."""

import logging
from typing import Any

from wistx_mcp.tools.lib.api_client import WISTXAPIClient
from wistx_mcp.tools.lib.plan_enforcement import require_query_quota

logger = logging.getLogger(__name__)

api_client = WISTXAPIClient()


@require_query_quota
async def manage_infrastructure(
    action: str,
    infrastructure_type: str,
    resource_name: str,
    cloud_provider: str | list[str] | None = None,
    configuration: dict[str, Any] | None = None,
    compliance_standards: list[str] | None = None,
    current_version: str | None = None,
    target_version: str | None = None,
    backup_type: str = "full",
    api_key: str = "",
) -> dict[str, Any]:
    """Manage infrastructure lifecycle (Kubernetes clusters, multi-cloud resources).

    Args:
        action: Action to perform (create, update, upgrade, backup, restore, monitor, optimize)
        infrastructure_type: Type of infrastructure (kubernetes, multi_cloud, hybrid_cloud)
        resource_name: Name of the resource/cluster
        cloud_provider: Cloud provider(s) - single string or list for multi-cloud
        configuration: Infrastructure configuration
            Example for Kubernetes: {
                "node_pools": [...],
                "addons": [...],
                "networking": {...},
                "security": {...}
            }
            Example for Multi-Cloud: {
                "resources": [
                    {"cloud": "aws", "type": "eks", "name": "cluster-1"},
                    {"cloud": "gcp", "type": "gke", "name": "cluster-2"}
                ],
                "integration": {...}
            }
        compliance_standards: Compliance standards to enforce
        current_version: Current version (for upgrade action)
        target_version: Target version (for upgrade action)
        backup_type: Type of backup (for backup action)

    Returns:
        Dictionary with infrastructure status:
        - resource_id: Resource identifier
        - status: Current status
        - endpoints: Access endpoints
        - compliance_status: Compliance status
        - cost_summary: Cost information
        - recommendations: Optimization recommendations

    Raises:
        ValueError: If invalid action or parameters
        Exception: If infrastructure management fails
    """
    valid_actions = ["create", "update", "upgrade", "backup", "restore", "monitor", "optimize"]
    if action not in valid_actions:
        raise ValueError(f"Invalid action: {action}. Must be one of {valid_actions}")

    valid_types = ["kubernetes", "multi_cloud", "hybrid_cloud"]
    if infrastructure_type not in valid_types:
        raise ValueError(f"Invalid infrastructure_type: {infrastructure_type}. Must be one of {valid_types}")

    from wistx_mcp.tools.lib.auth_context import validate_api_key_and_get_user_id

    try:
        await validate_api_key_and_get_user_id(api_key)
    except (ValueError, RuntimeError) as e:
        raise

    logger.info(
        "Managing infrastructure: action=%s, type=%s, resource=%s, provider=%s",
        action,
        infrastructure_type,
        resource_name,
        cloud_provider,
    )

    try:
        api_response = await api_client.manage_infrastructure(
            action=action,
            infrastructure_type=infrastructure_type,
            resource_name=resource_name,
            cloud_provider=cloud_provider,
            configuration=configuration,
            compliance_standards=compliance_standards,
            current_version=current_version,
            target_version=target_version,
            backup_type=backup_type,
            api_key=api_key,
        )

        if api_response.get("data"):
            return api_response["data"]
        return api_response

    except Exception as e:
        logger.error("Error in manage_infrastructure: %s", e, exc_info=True)
        raise

