"""Unified infrastructure tool - consolidates all infrastructure management capabilities.

This module merges five infrastructure tools into one unified interface:
- design_architecture (project initialization and architecture design)
- manage_infrastructure_lifecycle (design, integration, lifecycle)
- manage_infrastructure (Kubernetes/multi-cloud lifecycle)
- get_existing_infrastructure (get context from indexed repos)
- discover_cloud_resources (AWS resource discovery for Terraform import)

Usage:
    # Project design
    result = await wistx_infrastructure(action="init_project", project_type="terraform", ...)

    # Infrastructure analysis
    result = await wistx_infrastructure(action="analyze", infrastructure_code="...", ...)

    # Get existing infrastructure
    result = await wistx_infrastructure(action="get_existing", repository_url="...", ...)

    # Discover cloud resources
    result = await wistx_infrastructure(action="discover", role_arn="...", ...)
"""

import logging
from typing import Any

from wistx_mcp.tools.lib.plan_enforcement import require_query_quota

logger = logging.getLogger(__name__)

# Action groups for documentation and validation
PROJECT_ACTIONS = ["init_project", "design_project", "review_project", "optimize_project"]
ANALYSIS_ACTIONS = ["analyze", "design", "validate"]
INTEGRATION_ACTIONS = ["integrate", "analyze_integration"]
LIFECYCLE_ACTIONS = ["create", "update", "upgrade", "backup", "restore", "monitor", "optimize_resources"]
DISCOVERY_ACTIONS = ["get_existing", "discover"]

ALL_VALID_ACTIONS = PROJECT_ACTIONS + ANALYSIS_ACTIONS + INTEGRATION_ACTIONS + LIFECYCLE_ACTIONS + DISCOVERY_ACTIONS


@require_query_quota
async def wistx_infrastructure(
    # REQUIRED
    action: str,

    # COMMON PARAMETERS
    api_key: str | None = None,  # Optional - uses context or MCP initialization
    cloud_provider: str | list[str] | None = None,
    compliance_standards: list[str] | None = None,
    include_compliance: bool = False,

    # === PROJECT DESIGN (init_project, design_project, review_project, optimize_project) ===
    project_type: str | None = None,
    project_name: str | None = None,
    description: str | None = None,  # Project description
    architecture_type: str | None = None,
    requirements: dict[str, Any] | None = None,
    output_directory: str = ".",
    template_id: str | None = None,
    github_url: str | None = None,
    user_template: dict[str, Any] | None = None,
    include_security: bool = True,
    include_best_practices: bool = True,
    existing_architecture: str | None = None,

    # === INFRASTRUCTURE ANALYSIS (analyze, design, validate) ===
    infrastructure_code: str | None = None,

    # === INTEGRATION (integrate, analyze_integration) ===
    components: list[dict[str, Any]] | None = None,
    integration_type: str | None = None,
    pattern_name: str | None = None,

    # === LIFECYCLE (create, update, upgrade, backup, restore, monitor, optimize_resources) ===
    infrastructure_type: str | None = None,
    resource_type: str | None = None,  # Resource type for lifecycle actions
    resource_name: str | None = None,
    configuration: dict[str, Any] | None = None,
    target_environment: str | None = None,  # Target environment (dev, staging, prod)
    current_version: str | None = None,
    target_version: str | None = None,
    backup_type: str = "full",
    source_component: str | None = None,  # Source component for integration
    target_component: str | None = None,  # Target component for integration

    # === GET EXISTING (get_existing) ===
    repository_url: str | None = None,
    environment_name: str | None = None,
    include_costs: bool = True,

    # === DISCOVER CLOUD (discover) ===
    account_id: str | None = None,  # Cloud account ID
    role_arn: str | None = None,
    external_id: str | None = None,
    connection_name: str | None = None,
    regions: list[str] | None = None,
    resource_types: list[str] | None = None,
    tag_filters: dict[str, str] | None = None,
    include_pricing: bool = False,
    generate_diagrams: bool = True,
    terraform_state_content: str | None = None,
    discovery_method: str | None = None,  # Discovery method: sts_assume_role, iam_role_anywhere
) -> dict[str, Any]:
    """Unified infrastructure management - design, integration, lifecycle, and discovery.

    **Action Groups:**

    PROJECT DESIGN (for new projects):
    - "init_project": Initialize new project structure
    - "design_project": Design project architecture
    - "review_project": Review existing project
    - "optimize_project": Optimize project structure

    INFRASTRUCTURE ANALYSIS (for existing code):
    - "analyze": Analyze infrastructure code for issues
    - "design": Design new infrastructure
    - "validate": Validate infrastructure design

    INTEGRATION:
    - "integrate": Recommend integration patterns for components
    - "analyze_integration": Analyze existing integration patterns

    LIFECYCLE OPERATIONS:
    - "create": Create infrastructure resources
    - "update": Update infrastructure configuration
    - "upgrade": Upgrade infrastructure versions
    - "backup": Backup infrastructure state
    - "restore": Restore from backup
    - "monitor": Monitor infrastructure health
    - "optimize_resources": Optimize resource performance

    DISCOVERY:
    - "get_existing": Get existing infrastructure from indexed repo
    - "discover": Discover cloud resources (AWS) for Terraform import

    Args:
        action: Operation to perform (required)
        api_key: WISTX API key for authentication (required)

        Common:
        - cloud_provider: Cloud provider(s) - string or list for multi-cloud
        - compliance_standards: Compliance standards (SOC2, PCI-DSS, HIPAA, etc.)
        - include_compliance: Include compliance analysis (default: False)

        For project design:
        - project_type: terraform, kubernetes, devops, platform
        - project_name: Name for the project
        - architecture_type: microservices, serverless, monolith
        - requirements: {"resources": ["EC2", "RDS", "S3"]}
        - output_directory: Where to create project
        - template_id: MongoDB template ID
        - github_url: GitHub template URL
        - user_template: Custom template dict
        - include_security: Include security best practices (default: True)
        - include_best_practices: Include best practices (default: True)

        For analysis:
        - infrastructure_code: Code to analyze
        - existing_architecture: Existing architecture docs

        For integration:
        - components: [{"type": "ec2", "id": "web-server"}]
        - integration_type: networking, security, monitoring, service
        - pattern_name: Specific pattern to apply

        For lifecycle:
        - infrastructure_type: kubernetes, multi_cloud, hybrid_cloud
        - resource_name: Resource/cluster name
        - configuration: Resource configuration dict
        - current_version: For upgrades
        - target_version: For upgrades
        - backup_type: full, incremental, snapshot

        For get_existing:
        - repository_url: GitHub repository URL
        - environment_name: dev, stage, prod
        - include_costs: Include cost information

        For discover:
        - role_arn: AWS IAM role ARN for assume role
        - external_id: External ID for assume role
        - connection_name: Saved connection name
        - regions: AWS regions to scan
        - resource_types: Resource types to discover
        - tag_filters: Filter by tags
        - include_pricing: Include pricing data
        - generate_diagrams: Generate architecture diagrams
        - terraform_state_content: Existing Terraform state

    Returns:
        Dictionary with results specific to the action

    Raises:
        ValueError: If invalid action or missing required parameters
        RuntimeError: If operation fails
    """
    if action not in ALL_VALID_ACTIONS:
        raise ValueError(
            f"Invalid action: {action}. "
            f"Valid actions: {', '.join(ALL_VALID_ACTIONS)}"
        )

    logger.info(
        "Unified infrastructure: action=%s, cloud_provider=%s",
        action,
        cloud_provider,
    )

    # Route to appropriate handler based on action
    if action in PROJECT_ACTIONS:
        return await _handle_project_design(
            action=action,
            api_key=api_key,
            project_type=project_type,
            project_name=project_name,
            architecture_type=architecture_type,
            cloud_provider=cloud_provider,
            include_compliance=include_compliance,
            compliance_standards=compliance_standards,
            include_security=include_security,
            include_best_practices=include_best_practices,
            requirements=requirements,
            existing_architecture=existing_architecture,
            output_directory=output_directory,
            template_id=template_id,
            github_url=github_url,
            user_template=user_template,
        )

    elif action in ANALYSIS_ACTIONS or action in INTEGRATION_ACTIONS:
        return await _handle_lifecycle_management(
            action=action,
            api_key=api_key,
            infrastructure_type=infrastructure_type,
            resource_name=resource_name,
            infrastructure_code=infrastructure_code,
            components=components,
            integration_type=integration_type,
            cloud_provider=cloud_provider,
            configuration=configuration,
            compliance_standards=compliance_standards,
            pattern_name=pattern_name,
            current_version=current_version,
            target_version=target_version,
            backup_type=backup_type,
            repository_url=repository_url,
        )

    elif action in LIFECYCLE_ACTIONS:
        return await _handle_infrastructure_ops(
            action=action,
            api_key=api_key,
            infrastructure_type=infrastructure_type,
            resource_name=resource_name,
            cloud_provider=cloud_provider,
            configuration=configuration,
            compliance_standards=compliance_standards,
            current_version=current_version,
            target_version=target_version,
            backup_type=backup_type,
        )

    elif action == "get_existing":
        return await _handle_get_existing(
            api_key=api_key,
            repository_url=repository_url,
            environment_name=environment_name,
            include_compliance=include_compliance,
            include_costs=include_costs,
        )

    elif action == "discover":
        return await _handle_discover(
            api_key=api_key,
            role_arn=role_arn,
            external_id=external_id,
            connection_name=connection_name,
            regions=regions,
            resource_types=resource_types,
            tag_filters=tag_filters,
            include_compliance=include_compliance,
            compliance_standards=compliance_standards,
            include_pricing=include_pricing,
            include_best_practices=include_best_practices,
            generate_diagrams=generate_diagrams,
            terraform_state_content=terraform_state_content,
        )



async def _handle_project_design(
    action: str,
    api_key: str,
    project_type: str | None,
    project_name: str | None,
    architecture_type: str | None,
    cloud_provider: str | list[str] | None,
    include_compliance: bool,
    compliance_standards: list[str] | None,
    include_security: bool,
    include_best_practices: bool,
    requirements: dict[str, Any] | None,
    existing_architecture: str | None,
    output_directory: str,
    template_id: str | None,
    github_url: str | None,
    user_template: dict[str, Any] | None,
) -> dict[str, Any]:
    """Handle project design actions - delegates to design_architecture."""
    # Map action names to design_architecture action parameter
    action_map = {
        "init_project": "initialize",
        "design_project": "design",
        "review_project": "review",
        "optimize_project": "optimize",
    }
    design_action = action_map.get(action, action)

    # Validate required parameters for init_project action
    if action == "init_project":
        if not project_type or not project_name:
            raise ValueError(
                f"project_type and project_name are required for action='{action}'. "
                f"Example: wistx_infrastructure(action='init_project', project_type='terraform', "
                f"project_name='my-infrastructure', cloud_provider='aws')"
            )

    from wistx_mcp.tools.design_architecture import design_architecture

    # Handle cloud_provider for multi-cloud scenarios:
    # - If list with multiple providers: set provider="multi-cloud" and store full list in requirements
    # - If single string (including "multi-cloud"): pass through as-is
    # - This ensures requirements.cloud_providers is always available for multi-cloud processing
    if isinstance(cloud_provider, list):
        if len(cloud_provider) > 1:
            # Multiple providers - this is a multi-cloud project
            provider = "multi-cloud"
            # Ensure requirements dict exists and has cloud_providers list
            if requirements is None:
                requirements = {}
            requirements["cloud_providers"] = cloud_provider
        else:
            # Single provider in list format
            provider = cloud_provider[0] if cloud_provider else None
    else:
        provider = cloud_provider
        # If "multi-cloud" string, check if requirements has the actual providers
        if provider == "multi-cloud" and requirements:
            # requirements.cloud_providers may already have the list from AI
            pass  # Keep existing requirements.cloud_providers

    return await design_architecture(
        action=design_action,
        project_type=project_type,
        project_name=project_name,
        architecture_type=architecture_type,
        cloud_provider=provider,
        include_compliance=include_compliance,
        compliance_standards=compliance_standards,
        include_security=include_security,
        include_best_practices=include_best_practices,
        requirements=requirements,
        existing_architecture=existing_architecture,
        output_directory=output_directory,
        template_id=template_id,
        github_url=github_url,
        user_template=user_template,
        api_key=api_key,
    )


async def _handle_lifecycle_management(
    action: str,
    api_key: str,
    infrastructure_type: str | None,
    resource_name: str | None,
    infrastructure_code: str | None,
    components: list[dict[str, Any]] | None,
    integration_type: str | None,
    cloud_provider: str | list[str] | None,
    configuration: dict[str, Any] | None,
    compliance_standards: list[str] | None,
    pattern_name: str | None,
    current_version: str | None,
    target_version: str | None,
    backup_type: str,
    repository_url: str | None,
) -> dict[str, Any]:
    """Handle lifecycle management actions - delegates to manage_infrastructure_lifecycle."""
    from wistx_mcp.tools.manage_infrastructure_lifecycle import manage_infrastructure_lifecycle

    return await manage_infrastructure_lifecycle(
        action=action,
        infrastructure_type=infrastructure_type,
        resource_name=resource_name,
        infrastructure_code=infrastructure_code,
        components=components,
        integration_type=integration_type,
        cloud_provider=cloud_provider,
        configuration=configuration,
        compliance_standards=compliance_standards,
        pattern_name=pattern_name,
        current_version=current_version,
        target_version=target_version,
        backup_type=backup_type,
        repository_url=repository_url,
        api_key=api_key,
    )


async def _handle_infrastructure_ops(
    action: str,
    api_key: str,
    infrastructure_type: str | None,
    resource_name: str | None,
    cloud_provider: str | list[str] | None,
    configuration: dict[str, Any] | None,
    compliance_standards: list[str] | None,
    current_version: str | None,
    target_version: str | None,
    backup_type: str,
) -> dict[str, Any]:
    """Handle infrastructure ops actions - delegates to manage_infrastructure."""
    if not infrastructure_type:
        raise ValueError(f"infrastructure_type is required for action='{action}'")
    if not resource_name:
        raise ValueError(f"resource_name is required for action='{action}'")

    # Map optimize_resources back to optimize for manage_infrastructure
    infra_action = "optimize" if action == "optimize_resources" else action

    from wistx_mcp.tools.manage_infrastructure import manage_infrastructure

    return await manage_infrastructure(
        action=infra_action,
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



async def _handle_get_existing(
    api_key: str,
    repository_url: str | None,
    environment_name: str | None,
    include_compliance: bool,
    include_costs: bool,
) -> dict[str, Any]:
    """Handle get_existing action - delegates to get_existing_infrastructure."""
    if not repository_url:
        raise ValueError("repository_url is required for action='get_existing'")

    from wistx_mcp.tools.infrastructure_context import get_existing_infrastructure

    return await get_existing_infrastructure(
        repository_url=repository_url,
        environment_name=environment_name,
        include_compliance=include_compliance,
        include_costs=include_costs,
        api_key=api_key,
    )


async def _handle_discover(
    api_key: str,
    role_arn: str | None,
    external_id: str | None,
    connection_name: str | None,
    regions: list[str] | None,
    resource_types: list[str] | None,
    tag_filters: dict[str, str] | None,
    include_compliance: bool,
    compliance_standards: list[str] | None,
    include_pricing: bool,
    include_best_practices: bool,
    generate_diagrams: bool,
    terraform_state_content: str | None,
) -> dict[str, Any]:
    """Handle discover action - delegates to discover_cloud_resources."""
    from wistx_mcp.tools.discover_cloud_resources import discover_cloud_resources

    return await discover_cloud_resources(
        role_arn=role_arn,
        external_id=external_id,
        connection_name=connection_name,
        api_key=api_key,
        regions=regions,
        resource_types=resource_types,
        tag_filters=tag_filters,
        include_compliance=include_compliance,
        compliance_standards=compliance_standards,
        include_pricing=include_pricing,
        include_best_practices=include_best_practices,
        generate_diagrams=generate_diagrams,
        terraform_state_content=terraform_state_content,
    )
