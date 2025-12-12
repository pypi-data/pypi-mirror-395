"""Discover Cloud Resources MCP Tool.

This tool discovers existing cloud resources and generates Terraform import context.
It connects to the customer's AWS account using assumed role authentication and
discovers resources that can be imported into Terraform management.

Security:
- Uses ONLY STS AssumeRole with External ID (no direct credentials)
- Credentials exist only in memory, never persisted
- Read-only operations only

Features:
- Multi-region resource discovery
- Automatic dependency resolution
- Terraform name generation from resource names/tags
- Import order calculation
- Compliance, pricing, and best practices enrichment
- Auto-retrieval of saved connections
- Helpful setup guides when connection not configured
"""

import logging
import os
from typing import Any

from wistx_mcp.models.cloud_discovery import (
    AWSConnection,
    CloudProvider,
    DiscoveredResource,
    DiscoveryRequest,
    DiscoveryResponse,
    DiscoverySummary,
    ImportPhase,
)
from wistx_mcp.tools.lib.api_client import WISTXAPIClient
from wistx_mcp.tools.lib.auth_context import validate_api_key_and_get_user_id
from wistx_mcp.tools.lib.cloud_discovery.credential_providers.aws_assumed_role import (
    AWSAssumedRoleCredentialProvider,
)
from wistx_mcp.tools.lib.cloud_discovery.dependency_resolver import DependencyResolver
from wistx_mcp.tools.lib.cloud_discovery.name_resolvers.aws_name_resolver import (
    AWSNameResolver,
)
from wistx_mcp.tools.lib.cloud_discovery.providers.aws_provider import (
    AWSDiscoveryProvider,
)
from wistx_mcp.tools.lib.plan_enforcement import require_query_quota

logger = logging.getLogger(__name__)

api_client = WISTXAPIClient()


@require_query_quota
async def discover_cloud_resources(
    role_arn: str | None = None,
    external_id: str | None = None,
    connection_name: str | None = None,
    api_key: str = "",
    regions: list[str] | None = None,
    resource_types: list[str] | None = None,
    tag_filters: dict[str, str] | None = None,
    include_compliance: bool = False,
    compliance_standards: list[str] | None = None,
    include_pricing: bool = False,
    include_best_practices: bool = False,
    generate_diagrams: bool = True,
    terraform_state_content: str | None = None,
) -> dict[str, Any]:
    """Discover cloud resources and generate Terraform import context.
    
    This tool connects to a customer's AWS account using assumed role authentication
    and discovers existing resources that can be imported into Terraform.
    
    **Connection Management:**
    - If `role_arn` and `external_id` are provided, uses them directly
    - If `connection_name` is provided, retrieves saved connection by name
    - If neither provided, attempts to use most recent saved connection
    - If no saved connection exists, returns helpful setup guide
    
    **Filtering Already-Managed Resources:**
    The discovery results include helper code (Python) that you can use with your
    local Terraform state file to filter out resources that are already managed.
    This keeps your state file private and leverages your IDE's native file access.
    
    Example workflow:
    1. Run this discovery tool
    2. Locate your terraform.tfstate file (or run `terraform state pull`)
    3. Use the provided helper code to filter results
    4. Generate Terraform code only for unmanaged resources
    
    Args:
        role_arn: ARN of the IAM role to assume in the customer's account (optional if connection_name provided)
            Example: "arn:aws:iam::123456789012:role/WISTXDiscoveryRole"
        external_id: External ID for security (optional if connection_name provided)
            Must start with "wistx-". Generate using the API or dashboard.
        connection_name: Name of saved connection to use (optional, alternative to role_arn/external_id)
        api_key: WISTX API key for authentication
        regions: List of AWS regions to scan. Default: common regions
            Example: ["us-east-1", "us-west-2", "eu-west-1"]
        resource_types: CloudFormation resource types to discover. Default: all supported
            Example: ["AWS::EC2::Instance", "AWS::RDS::DBInstance"]
        tag_filters: Filter resources by tags
            Example: {"Environment": "production", "Team": "platform"}
        include_compliance: Enrich with compliance requirements (requires compliance_standards)
        compliance_standards: Standards to check (e.g., ["SOC2", "HIPAA", "PCI-DSS"])
        include_pricing: Enrich with current pricing information
        include_best_practices: Enrich with AWS best practices recommendations
        generate_diagrams: Generate infrastructure diagrams (default: True)
        terraform_state_content: Optional JSON string of terraform.tfstate file content.
            If provided, resources already in state will be filtered out server-side.
            If not provided, helper code for client-side filtering is included in context.
    
    Returns:
        Discovery response with:
        - discovered_resources: List of discovered resources with Terraform metadata
        - dependency_graph: Resource dependencies and import order
        - terraform_names: Mapping of resource IDs to Terraform names
        - import_commands: Generated terraform import commands
        - diagrams: Infrastructure diagrams (if generate_diagrams=True)
        - summary: Discovery summary statistics
        
        OR setup guide if connection not configured:
        - setup_required: True
        - setup_guide: Comprehensive setup instructions
        - api_endpoints: Available API endpoints for setup
    
    Raises:
        ValueError: If connection resolution fails or parameters are invalid
        PermissionError: If role assumption fails
    
    Example:
        # Using saved connection (recommended)
        result = await discover_cloud_resources(
            connection_name="production-aws",
            api_key="wistx_...",
            regions=["us-east-1"],
        )
        
        # Using explicit credentials
        result = await discover_cloud_resources(
            role_arn="arn:aws:iam::123456789012:role/WISTXDiscoveryRole",
            external_id="wistx-abc123-def456",
            api_key="wistx_...",
            regions=["us-east-1"],
        )
    """
    # Validate authentication
    user_id = await validate_api_key_and_get_user_id(api_key)
    if not user_id:
        raise ValueError("Authentication required - api_key is invalid")
    
    # Check for environment variables (for CI/CD usage)
    if not role_arn:
        role_arn = os.getenv("WISTX_AWS_ROLE_ARN") or os.getenv("AWS_ROLE_ARN")
    if not external_id:
        external_id = os.getenv("WISTX_AWS_EXTERNAL_ID") or os.getenv("AWS_EXTERNAL_ID")
    
    # Security warning if Role ARN provided via parameters (chat)
    if role_arn and not os.getenv("WISTX_AWS_ROLE_ARN"):
        logger.warning(
            "Role ARN provided via tool parameters - this will be stored in chat history. "
            "For production, use dashboard connection or environment variables."
        )
    
    # Resolve connection (auto-retrieve from database if not provided)
    resolved_role_arn, resolved_external_id = await _resolve_aws_connection(
        user_id=user_id,
        api_key=api_key,
        role_arn=role_arn,
        external_id=external_id,
        connection_name=connection_name,
    )
    
    # If no connection resolved, return setup guide
    if not resolved_role_arn or not resolved_external_id:
        logger.info("No AWS connection found for user %s, returning setup guide", user_id)
        return await _get_connection_setup_guide(user_id, api_key)
    
    # Validate external_id format
    if not resolved_external_id.startswith("wistx-"):
        raise ValueError("external_id must start with 'wistx-' for security")
    
    if include_compliance and not compliance_standards:
        raise ValueError("compliance_standards required when include_compliance=True")
    
    logger.info(
        "Starting cloud resource discovery for user %s, role %s",
        user_id,
        resolved_role_arn,
    )
    
    # Initialize providers
    credential_provider = AWSAssumedRoleCredentialProvider()
    discovery_provider = AWSDiscoveryProvider()
    name_resolver = AWSNameResolver()
    dependency_resolver = DependencyResolver()
    
    try:
        # Get credentials via STS AssumeRole
        credentials = await credential_provider.get_credentials(
            role_arn=resolved_role_arn,
            external_id=resolved_external_id,
            session_name="wistx-discovery",
        )
        
        logger.info("Successfully assumed role, starting discovery")
        
        # Discover resources
        resources = await discovery_provider.discover_resources(
            credentials=credentials,
            regions=regions,
            resource_types=resource_types,
            tag_filters=tag_filters,
        )
        
        logger.info("Discovered %d resources", len(resources))

        # Filter managed resources if state provided
        filtered_count = 0
        filtering_applied = False
        if terraform_state_content:
            try:
                from wistx_mcp.tools.lib.cloud_discovery.terraform_state_parser import (
                    parse_terraform_state,
                    is_resource_managed,
                )
                
                managed_ids = parse_terraform_state(terraform_state_content)
                original_count = len(resources)
                
                # Filter resources
                filtered_resources = []
                for resource in resources:
                    if not is_resource_managed(
                        resource_id=resource.cloud_resource_id,
                        arn=resource.arn,
                        name=resource.name,
                        managed_ids=managed_ids,
                    ):
                        filtered_resources.append(resource)
                
                filtered_count = original_count - len(filtered_resources)
                resources = filtered_resources
                filtering_applied = True
                
                logger.info(
                    "Filtered out %d already-managed resources, %d remaining",
                    filtered_count,
                    len(resources),
                )
            except Exception as e:
                logger.warning("Failed to parse Terraform state: %s", e)
                filtering_applied = False

        # Resolve Terraform names
        terraform_names: dict[str, str] = {}
        name_resolver.reset_used_names()  # Start fresh

        for resource in resources:
            name_resolution = name_resolver.resolve_terraform_name(resource)
            terraform_names[resource.cloud_resource_id] = name_resolution.terraform_name

        # Build dependency graph and import order
        dependency_graph = dependency_resolver.resolve_dependencies(resources)

        # Generate import commands
        import_commands = dependency_resolver.generate_import_commands(
            dependency_graph, terraform_names
        )

        # Validate dependencies
        validation_issues = dependency_resolver.validate_dependencies(dependency_graph)

        # Build summary
        summary = _build_discovery_summary(resources, dependency_graph)

        # Prepare response
        response: dict[str, Any] = {
            "discovered_resources": [_resource_to_dict(r) for r in resources],
            "terraform_names": terraform_names,
            "import_order": dependency_graph.topological_order,
            "import_commands": import_commands,
            "dependencies": [
                {
                    "source_id": d.source_id,
                    "target_id": d.target_id,
                    "type": d.dependency_type,
                }
                for d in dependency_graph.edges
            ],
            "phases": {
                phase: ids
                for phase, ids in dependency_graph.phases.items()
                if ids
            },
            "has_circular_dependencies": dependency_graph.has_cycles,
            "validation_issues": validation_issues,
            "summary": summary,
            "filtering": {
                "applied": filtering_applied,
                "method": "server_side" if filtering_applied else "client_side",
                "filtered_count": filtered_count if filtering_applied else 0,
                "remaining_count": len(resources) if filtering_applied else None,
            },
        }

        # Optional enrichments
        if include_compliance and compliance_standards:
            response["compliance"] = await _enrich_with_compliance(
                resources, compliance_standards, api_key
            )

        if include_pricing:
            response["pricing"] = await _enrich_with_pricing(resources, api_key)

        if include_best_practices:
            response["best_practices"] = await _enrich_with_best_practices(
                resources, api_key
            )

        if generate_diagrams:
            response["diagrams"] = await _generate_diagrams(
                resources, dependency_graph, terraform_names
            )

        logger.info(
            "Discovery complete: %d resources, %d import commands",
            len(resources),
            len(import_commands),
        )

        return response

    finally:
        # Always clear credentials after use
        credential_provider.clear_credentials()
        logger.debug("Cleared temporary credentials")


def _resource_to_dict(resource: DiscoveredResource) -> dict[str, Any]:
    """Convert DiscoveredResource to dictionary."""
    return {
        "cloud_provider": resource.cloud_provider.value,
        "cloud_resource_type": resource.cloud_resource_type,
        "cloud_resource_id": resource.cloud_resource_id,
        "arn": resource.arn,
        "region": resource.region,
        "name": resource.name,
        "tags": resource.tags,
        "terraform_resource_type": resource.terraform_resource_type,
        "import_phase": resource.import_phase.value,
    }


def _build_discovery_summary(
    resources: list[DiscoveredResource],
    dependency_graph: Any,
) -> dict[str, Any]:
    """Build summary statistics for the discovery."""
    # Count by resource type
    by_type: dict[str, int] = {}
    for resource in resources:
        tf_type = resource.terraform_resource_type
        by_type[tf_type] = by_type.get(tf_type, 0) + 1

    # Count by region
    by_region: dict[str, int] = {}
    for resource in resources:
        region = resource.region or "unknown"
        by_region[region] = by_region.get(region, 0) + 1

    # Count by phase
    by_phase: dict[str, int] = {}
    for resource in resources:
        phase = resource.import_phase.value
        by_phase[phase] = by_phase.get(phase, 0) + 1

    return {
        "total_resources": len(resources),
        "by_resource_type": by_type,
        "by_region": by_region,
        "by_phase": by_phase,
        "total_dependencies": len(dependency_graph.edges),
        "has_circular_dependencies": dependency_graph.has_cycles,
    }


async def _enrich_with_compliance(
    resources: list[DiscoveredResource],
    standards: list[str],
    api_key: str,
) -> dict[str, Any]:
    """Enrich resources with compliance requirements."""
    from wistx_mcp.tools import mcp_tools

    # Get unique resource types
    resource_types = list({r.terraform_resource_type for r in resources})

    # Map to WISTX resource types
    wistx_types = []
    for tf_type in resource_types:
        # aws_instance -> EC2, aws_db_instance -> RDS, etc.
        if "instance" in tf_type and "db" not in tf_type:
            wistx_types.append("EC2")
        elif "db_instance" in tf_type or "rds" in tf_type:
            wistx_types.append("RDS")
        elif "s3" in tf_type:
            wistx_types.append("S3")
        elif "vpc" in tf_type:
            wistx_types.append("VPC")
        elif "lambda" in tf_type:
            wistx_types.append("Lambda")
        elif "iam" in tf_type:
            wistx_types.append("IAM")
        elif "eks" in tf_type:
            wistx_types.append("EKS")
        elif "ecs" in tf_type:
            wistx_types.append("ECS")

    wistx_types = list(set(wistx_types)) or ["EC2"]

    try:
        compliance_result = await mcp_tools.get_compliance_requirements(
            resource_types=wistx_types,
            standards=standards,
            api_key=api_key,
            include_remediation=True,
            generate_report=False,
        )
        return compliance_result
    except Exception as e:
        logger.warning("Failed to get compliance requirements: %s", e)
        return {"error": str(e), "standards": standards}


async def _enrich_with_pricing(
    resources: list[DiscoveredResource],
    api_key: str,
) -> dict[str, Any]:
    """Enrich resources with pricing information."""
    from wistx_mcp.tools import pricing as pricing_tool

    # Build pricing request
    pricing_resources = []
    for resource in resources:
        pricing_resources.append({
            "cloud": "aws",
            "service": _map_terraform_to_service(resource.terraform_resource_type),
            "region": resource.region or "us-east-1",
        })

    try:
        pricing_result = await pricing_tool.get_pricing_info(
            resources=pricing_resources[:20],  # Limit to avoid timeout
            api_key=api_key,
        )
        return pricing_result
    except Exception as e:
        logger.warning("Failed to get pricing info: %s", e)
        return {"error": str(e)}


def _map_terraform_to_service(terraform_type: str) -> str:
    """Map Terraform resource type to AWS service name."""
    service_map = {
        "aws_instance": "ec2",
        "aws_db_instance": "rds",
        "aws_rds_cluster": "rds",
        "aws_s3_bucket": "s3",
        "aws_lambda_function": "lambda",
        "aws_lb": "elb",
        "aws_ecs_service": "ecs",
        "aws_eks_cluster": "eks",
        "aws_dynamodb_table": "dynamodb",
        "aws_elasticache_cluster": "elasticache",
    }
    return service_map.get(terraform_type, "ec2")


async def _enrich_with_best_practices(
    resources: list[DiscoveredResource],
    api_key: str,
) -> dict[str, Any]:
    """Enrich resources with AWS best practices."""
    from wistx_mcp.tools import mcp_tools

    resource_types = list({r.terraform_resource_type for r in resources})

    try:
        best_practices = await mcp_tools.get_best_practices(
            resource_types=resource_types,
            cloud_provider="aws",
            api_key=api_key,
        )
        return best_practices
    except Exception as e:
        logger.warning("Failed to get best practices: %s", e)
        return {"error": str(e)}


async def _generate_diagrams(
    resources: list[DiscoveredResource],
    dependency_graph: Any,
    terraform_names: dict[str, str],
) -> dict[str, str]:
    """Generate infrastructure diagrams."""
    from wistx_mcp.tools.lib.infrastructure_visualizer import InfrastructureVisualizer

    visualizer = InfrastructureVisualizer()
    diagrams = {}

    # Build component data for visualizer
    components = []
    for resource in resources:
        components.append({
            "id": resource.cloud_resource_id,
            "name": terraform_names.get(resource.cloud_resource_id, resource.name),
            "type": resource.terraform_resource_type,
            "region": resource.region,
            "phase": resource.import_phase.value,
        })

    # Build connection data
    connections = []
    for dep in dependency_graph.edges:
        connections.append({
            "from": dep.source_id,
            "to": dep.target_id,
            "type": dep.dependency_type,
        })

    try:
        # System overview diagram
        diagrams["system_overview"] = visualizer.generate_system_diagram(
            components=components,
            connections=connections,
            title="Discovered Infrastructure Overview",
        )

        # Dependency/import order diagram
        diagrams["import_order"] = visualizer.generate_dependency_diagram(
            components=components,
            dependencies=connections,
            title="Terraform Import Order",
        )

    except Exception as e:
        logger.warning("Failed to generate diagrams: %s", e)
        diagrams["error"] = str(e)

    return diagrams


async def _resolve_aws_connection(
    user_id: str,
    api_key: str,
    role_arn: str | None = None,
    external_id: str | None = None,
    connection_name: str | None = None,
) -> tuple[str | None, str | None]:
    """Resolve AWS connection from parameters or saved connections.
    
    Resolution order:
    1. If role_arn and external_id provided, use them
    2. If connection_name provided, retrieve saved connection by name
    3. Otherwise, retrieve most recent saved connection
    
    Args:
        user_id: User ID
        api_key: API key for authentication
        role_arn: Optional explicit role ARN
        external_id: Optional explicit external ID
        connection_name: Optional connection name to retrieve
    
    Returns:
        Tuple of (role_arn, external_id) or (None, None) if not found
    """
    # If explicit credentials provided, use them
    if role_arn and external_id:
        logger.debug("Using explicit credentials for user %s", user_id)
        return role_arn, external_id
    
    # Try to retrieve from database
    try:
        from api.models.cloud_discovery import CloudProviderEnum
        from api.services.cloud_discovery_service import CloudDiscoveryService
        
        if connection_name:
            logger.debug("Connection name lookup not yet fully implemented, using most recent")
        
        # Get most recent saved connection
        connections = await CloudDiscoveryService.list_connections(
            user_id=user_id,
            provider=CloudProviderEnum.AWS,
        )
        
        if connections:
            # Filter to only valid connections
            valid_connections = [
                c for c in connections
                if c.status.value == "valid" and c.is_active
            ]
            
            if valid_connections:
                connection = valid_connections[0]  # Most recent
                logger.info(
                    "Using saved connection for user %s: %s",
                    user_id,
                    connection.role_arn,
                )
                return connection.role_arn, connection.external_id
        
        logger.debug("No saved connections found for user %s", user_id)
        return None, None
        
    except ImportError:
        logger.debug("CloudDiscoveryService not available, cannot retrieve saved connections")
        return None, None
    except Exception as e:
        logger.warning("Failed to retrieve saved connections: %s", e)
        return None, None


async def _get_connection_setup_guide(
    user_id: str,
    api_key: str,
) -> dict[str, Any]:
    """Generate comprehensive setup guide for AWS connection.
    
    Args:
        user_id: User ID
        api_key: API key for authentication
    
    Returns:
        Dictionary with setup guide and instructions
    """
    try:
        # Get setup instructions from API
        url = f"{api_client.api_url}/v1/cloud-discovery/aws/setup"
        response = await api_client.client.get(
            url,
            headers={"Authorization": f"Bearer {api_key}"},
        )
        response.raise_for_status()
        setup_response = response.json()
        
        if setup_response and "wistx_account_id" in setup_response:
            wistx_account_id = setup_response["wistx_account_id"]
            trust_policy = setup_response.get("trust_policy", "")
            permission_policy = setup_response.get("permission_policy", "")
        else:
            # Fallback if API unavailable
            wistx_account_id = "WISTX_ACCOUNT_ID"
            provider = AWSAssumedRoleCredentialProvider()
            trust_policy_dict = provider.get_trust_policy_template(
                wistx_account_id=wistx_account_id,
                external_id="EXTERNAL_ID_PLACEHOLDER",
            )
            permission_policy_dict = provider.get_permission_policy_template()
            import json
            trust_policy = json.dumps(trust_policy_dict, indent=2)
            permission_policy = json.dumps(permission_policy_dict, indent=2)
    except Exception as e:
        logger.warning("Failed to get setup instructions from API: %s", e)
        wistx_account_id = "WISTX_ACCOUNT_ID"
        provider = AWSAssumedRoleCredentialProvider()
        trust_policy_dict = provider.get_trust_policy_template(
            wistx_account_id=wistx_account_id,
            external_id="EXTERNAL_ID_PLACEHOLDER",
        )
        permission_policy_dict = provider.get_permission_policy_template()
        import json
        trust_policy = json.dumps(trust_policy_dict, indent=2)
        permission_policy = json.dumps(permission_policy_dict, indent=2)
    
    # Try to generate External ID automatically for the user
    external_id_response = None
    try:
        url = f"{api_client.api_url}/v1/cloud-discovery/external-id"
        response = await api_client.client.post(
            url,
            json={"provider": "aws"},
            headers={"Authorization": f"Bearer {api_key}"},
        )
        response.raise_for_status()
        external_id_response = response.json()
        logger.info("Generated External ID for user %s", user_id)
    except Exception as e:
        logger.warning("Failed to auto-generate External ID: %s", e)
    
    return {
        "setup_required": True,
        "error": "AWS connection not configured",
        "message": (
            "To discover AWS resources, you need to connect your AWS account first. "
            "**For security best practices, I strongly recommend using the WISTX dashboard** "
            "to connect your AWS account (see 'Recommended Method' below). "
            "This keeps your Role ARN out of chat history and stores it securely."
        ),
        "external_id_generated": external_id_response is not None,
        "external_id": external_id_response.get("external_id") if external_id_response else None,
        "setup_guide": {
            "overview": (
                "You need to create an IAM role in your AWS account that allows WISTX "
                "to discover your resources. This uses secure cross-account access "
                "with no credentials stored."
            ),
            "steps": [
                {
                    "step": 1,
                    "title": "Generate External ID",
                    "description": "Get a secure External ID from WISTX (required for security)",
                    "status": "completed" if external_id_response else "pending",
                    "external_id": external_id_response.get("external_id") if external_id_response else None,
                    "action": "I've automatically generated an External ID for you" if external_id_response else "Call the API endpoint to generate an External ID",
                    "api_endpoint": "POST /v1/cloud-discovery/external-id",
                    "example_request": {
                        "method": "POST",
                        "url": "/v1/cloud-discovery/external-id",
                        "headers": {"Authorization": "Bearer YOUR_API_KEY"},
                        "body": {"provider": "aws"},
                    },
                    "example_response": {
                        "external_id": external_id_response.get("external_id", "wistx-abc123def456-789012345678") if external_id_response else "wistx-abc123def456-789012345678",
                        "created_at": external_id_response.get("created_at", "2025-01-15T10:30:00Z") if external_id_response else "2025-01-15T10:30:00Z",
                        "expires_at": external_id_response.get("expires_at", "2026-01-15T10:30:00Z") if external_id_response else "2026-01-15T10:30:00Z",
                    },
                    "note": (
                        f"✅ External ID generated: `{external_id_response.get('external_id')}`" 
                        if external_id_response 
                        else "Save the external_id - you'll need it for the IAM role trust policy"
                    ),
                    "next_action": "Use this External ID in Step 2 when creating the IAM role" if external_id_response else None,
                },
                {
                    "step": 2,
                    "title": "Create IAM Role in AWS",
                    "description": "Create an IAM role with trust policy allowing WISTX to assume it. This step requires AWS Console or AWS CLI access.",
                    "status": "pending",
                    "requires_user_action": True,
                    "instructions": [
                        "1. Go to AWS Console → IAM → Roles → Create role",
                        "2. Select 'Another AWS account' as trusted entity",
                        f"3. Enter Account ID: {wistx_account_id}",
                        "4. Check 'Require external ID' and enter the External ID from Step 1",
                        "5. Click 'Next'",
                        "6. Create a new policy with the permission policy JSON (see below)",
                        "7. Attach the policy to the role",
                        "8. Name your role (e.g., 'WISTXDiscoveryRole')",
                        "9. Create the role",
                        "10. Copy the Role ARN (format: arn:aws:iam::ACCOUNT_ID:role/ROLE_NAME)",
                    ],
                    "trust_policy": trust_policy,
                    "permission_policy": permission_policy,
                    "aws_cli_example": (
                        "# Create trust policy file\n"
                        "cat > trust-policy.json <<'EOF'\n"
                        f"{trust_policy}\n"
                        "EOF\n\n"
                        "# Create permission policy file\n"
                        "cat > permission-policy.json <<'EOF'\n"
                        f"{permission_policy}\n"
                        "EOF\n\n"
                        "# Create IAM role\n"
                        "aws iam create-role \\\n"
                        "  --role-name WISTXDiscoveryRole \\\n"
                        "  --assume-role-policy-document file://trust-policy.json\n\n"
                        "# Create and attach permission policy\n"
                        "aws iam create-policy \\\n"
                        "  --policy-name WISTXDiscoveryPolicy \\\n"
                        "  --policy-document file://permission-policy.json\n\n"
                        "aws iam attach-role-policy \\\n"
                        "  --role-name WISTXDiscoveryRole \\\n"
                        "  --policy-arn arn:aws:iam::YOUR_ACCOUNT_ID:policy/WISTXDiscoveryPolicy\n\n"
                        "# Get the role ARN\n"
                        "aws iam get-role --role-name WISTXDiscoveryRole --query 'Role.Arn' --output text"
                    ),
                },
                {
                    "step": 3,
                    "title": "Validate Connection",
                    "description": (
                        "After creating the IAM role, validate the connection. "
                        "**Recommended**: Use dashboard to validate (keeps Role ARN out of chat). "
                        "Alternatively, provide Role ARN here (⚠️ will be stored in chat history)."
                    ),
                    "status": "pending",
                    "requires_user_input": True,
                    "security_warning": (
                        "⚠️ **Security Notice**: If you provide Role ARN here, it will be stored in "
                        "conversation history. For production, use dashboard validation instead."
                    ),
                    "user_input_prompt": (
                        "Please provide the Role ARN from Step 2, or use the dashboard to validate. "
                        "Role ARN format: arn:aws:iam::123456789012:role/WISTXDiscoveryRole"
                    ),
                    "dashboard_alternative": (
                        "**Better**: Go to dashboard → Cloud Discovery → Validate Connection "
                        "(no chat exposure, secure storage)"
                    ),
                    "action": "Once you provide the Role ARN, I'll call the validation endpoint automatically",
                    "api_endpoint": "POST /v1/cloud-discovery/validate",
                    "example_request": {
                        "method": "POST",
                        "url": "/v1/cloud-discovery/validate",
                        "headers": {"Authorization": "Bearer YOUR_API_KEY"},
                        "body": {
                            "provider": "aws",
                            "role_arn": "arn:aws:iam::123456789012:role/WISTXDiscoveryRole",
                            "external_id": external_id_response.get("external_id", "wistx-abc123-def456") if external_id_response else "wistx-abc123-def456",
                        },
                    },
                    "note": (
                        "After validation, your connection will be saved automatically. "
                        "You won't need to provide credentials again in the future."
                    ),
                },
                {
                    "step": 4,
                    "title": "Run Discovery",
                    "description": "Once the connection is validated, I'll automatically run discovery for you",
                    "status": "pending",
                    "note": (
                        "After validation, I'll automatically use your saved connection to discover resources. "
                        "You won't need to provide role_arn and external_id again."
                    ),
                },
            ],
            "recommended_method": {
                "title": "🔒 Recommended: Dashboard Connection (Most Secure)",
                "description": (
                    "**For production use and security best practices, connect via the WISTX dashboard.**\n\n"
                    "Benefits:\n"
                    "- ✅ No Role ARN exposed in chat history\n"
                    "- ✅ Secure storage in encrypted database\n"
                    "- ✅ Visual guided setup experience\n"
                    "- ✅ Automatic connection management\n"
                    "- ✅ Works seamlessly with discovery tool\n\n"
                    "**Dashboard URL**: https://app.wistx.com/cloud-discovery\n\n"
                    "After connecting via dashboard, the discovery tool will automatically "
                    "use your saved connection - no credentials needed in chat!"
                ),
                "steps": [
                    "1. Go to https://app.wistx.com/cloud-discovery",
                    "2. Click 'Connect AWS Account'",
                    "3. Follow the guided setup (External ID generated automatically)",
                    "4. Create IAM role in AWS using provided instructions",
                    "5. Validate connection in dashboard",
                    "6. Return here and run discovery - tool will use saved connection automatically",
                ],
            },
            "alternative_methods": {
                "environment_variables": {
                    "title": "Alternative: Environment Variables (For CI/CD)",
                    "description": (
                        "For programmatic usage (CI/CD, scripts), use environment variables:\n\n"
                        "```bash\n"
                        "export WISTX_AWS_ROLE_ARN='arn:aws:iam::123456789012:role/WISTXDiscoveryRole'\n"
                        "export WISTX_AWS_EXTERNAL_ID='wistx-abc123-def456'\n"
                        "```\n\n"
                        "The tool will automatically read these if not provided as parameters."
                    ),
                },
                "direct_parameters": {
                    "title": "⚠️ Not Recommended: Direct Parameters (Chat)",
                    "description": (
                        "You can provide Role ARN directly, but this is **not recommended** for security reasons:\n\n"
                        "⚠️ **Security Concerns:**\n"
                        "- Role ARN stored in chat history\n"
                        "- Visible in conversation logs\n"
                        "- Not ideal for production environments\n\n"
                        "**Use only for:**\n"
                        "- One-off testing\n"
                        "- Development environments\n"
                        "- When dashboard is not accessible\n\n"
                        "If you must use this method, the tool will work but will show a security warning."
                    ),
                },
            },
            "interactive_flow": {
                "description": (
                    "If you choose to proceed via chat (not recommended for production):\n"
                    "1. ✅ External ID generated automatically (done)\n"
                    "2. ⏳ You create IAM role in AWS (requires AWS Console/CLI)\n"
                    "3. ⏳ You provide Role ARN → I validate automatically\n"
                    "4. ⏳ I run discovery automatically\n\n"
                    "**Note**: Providing Role ARN in chat will store it in conversation history."
                ),
                "coding_agent_can_help": [
                    "Generate External ID (already done)",
                    "Validate connection once you provide Role ARN",
                    "Run discovery automatically after validation",
                ],
                "requires_user_action": [
                    "Create IAM role in AWS Console or via AWS CLI",
                    "Provide Role ARN after creating the role (⚠️ will be stored in chat)",
                ],
                "security_warning": (
                    "⚠️ **Security Notice**: Providing Role ARN via chat will store it in conversation history. "
                    "For production use, please connect via dashboard instead."
                ),
            },
        },
        "api_endpoints": {
            "generate_external_id": {
                "method": "POST",
                "path": "/v1/cloud-discovery/external-id",
                "description": "Generate a secure External ID",
            },
            "get_setup_instructions": {
                "method": "GET",
                "path": "/v1/cloud-discovery/aws/setup",
                "description": "Get complete setup instructions and policy templates",
            },
            "validate_connection": {
                "method": "POST",
                "path": "/v1/cloud-discovery/validate",
                "description": "Validate and save AWS connection",
            },
            "list_connections": {
                "method": "GET",
                "path": "/v1/cloud-discovery/connections",
                "description": "List all saved cloud connections",
            },
        },
        "wistx_account_id": wistx_account_id,
    }


async def generate_external_id(customer_id: str) -> dict[str, Any]:
    """Generate a secure External ID for a customer.

    This helper function generates an External ID that the customer should
    configure in their IAM role's trust policy.

    Args:
        customer_id: Unique identifier for the customer

    Returns:
        Dictionary with external_id and trust policy template
    """
    provider = AWSAssumedRoleCredentialProvider()
    external_id = provider.generate_external_id(customer_id)

    # Get trust policy template (placeholder account ID)
    trust_policy = provider.get_trust_policy_template(
        wistx_account_id="WISTX_ACCOUNT_ID",  # Replace with actual in production
        external_id=external_id,
    )

    # Get permission policy
    permission_policy = provider.get_permission_policy_template()

    return {
        "external_id": external_id,
        "trust_policy": trust_policy,
        "permission_policy": permission_policy,
        "instructions": (
            "1. Create an IAM role in your AWS account\n"
            "2. Attach the trust_policy to allow WISTX to assume the role\n"
            "3. Attach the permission_policy for read-only discovery access\n"
            "4. Use the role ARN and external_id when calling discover_cloud_resources"
        ),
    }

