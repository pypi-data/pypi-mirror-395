"""Cloud Discovery API Router.

Endpoints for cloud resource discovery and AWS connection management.
"""

import logging
import uuid
from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException, status

from api.dependencies import get_current_user
from api.models.cloud_discovery import (
    CloudConnectionDocument,
    CloudProviderEnum,
    ConnectionSetupResponse,
    ConnectionValidationResponse,
    CredentialStatusEnum,
    DiscoveryListItem,
    DiscoveryListResponse,
    DiscoveryMetadataDocument,
    DiscoveryStatusEnum,
    ExternalIdResponse,
    GenerateExternalIdRequest,
    StartDiscoveryRequest,
    TerraformMappingResponse,
    ValidateConnectionRequest,
)
from api.services.cloud_discovery_service import CloudDiscoveryService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/cloud-discovery", tags=["cloud-discovery"])

# WISTX AWS Account ID for trust policy
WISTX_AWS_ACCOUNT_ID = "123456789012"  # TODO: Replace with actual WISTX AWS account ID


def _generate_external_id() -> str:
    """Generate a cryptographically secure External ID."""
    import secrets
    return f"wistx-{secrets.token_hex(16)}"


def _get_trust_policy(external_id_placeholder: str = "EXTERNAL_ID_PLACEHOLDER") -> str:
    """Generate AWS trust policy JSON."""
    import json
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": f"arn:aws:iam::{WISTX_AWS_ACCOUNT_ID}:root"},
                "Action": "sts:AssumeRole",
                "Condition": {
                    "StringEquals": {"sts:ExternalId": external_id_placeholder}
                },
            }
        ],
    }
    return json.dumps(policy, indent=2)


def _get_permission_policy() -> str:
    """Generate AWS permission policy JSON for read-only discovery."""
    import json
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "ResourceExplorerAccess",
                "Effect": "Allow",
                "Action": [
                    "resource-explorer-2:Search",
                    "resource-explorer-2:GetView",
                    "resource-explorer-2:ListViews",
                ],
                "Resource": "*",
            },
            {
                "Sid": "ResourceGroupsTaggingAccess",
                "Effect": "Allow",
                "Action": ["tag:GetResources", "tag:GetTagKeys", "tag:GetTagValues"],
                "Resource": "*",
            },
            {
                "Sid": "ReadOnlyDescribeAccess",
                "Effect": "Allow",
                "Action": [
                    "ec2:Describe*",
                    "rds:Describe*",
                    "s3:GetBucket*",
                    "s3:ListBucket",
                    "lambda:GetFunction*",
                    "lambda:List*",
                    "iam:GetRole*",
                    "iam:List*",
                    "dynamodb:Describe*",
                    "dynamodb:List*",
                    "elasticache:Describe*",
                    "eks:Describe*",
                    "eks:List*",
                    "ecs:Describe*",
                    "ecs:List*",
                    "sns:GetTopic*",
                    "sns:List*",
                    "sqs:GetQueue*",
                    "sqs:List*",
                    "kms:Describe*",
                    "kms:List*",
                    "secretsmanager:Describe*",
                    "secretsmanager:List*",
                ],
                "Resource": "*",
            },
        ],
    }
    return json.dumps(policy, indent=2)


@router.get(
    "/aws/setup",
    response_model=ConnectionSetupResponse,
    summary="Get AWS connection setup instructions",
)
async def get_aws_setup_instructions(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> ConnectionSetupResponse:
    """Get AWS IAM role setup instructions for WISTX integration."""
    logger.info("User %s requested AWS setup instructions", current_user.get("user_id"))

    return ConnectionSetupResponse(
        trust_policy=_get_trust_policy(),
        permission_policy=_get_permission_policy(),
        setup_instructions=[
            "1. Go to AWS Console → IAM → Roles → Create role",
            "2. Select 'Another AWS account' as trusted entity",
            f"3. Enter Account ID: {WISTX_AWS_ACCOUNT_ID}",
            "4. Check 'Require external ID' and enter your generated External ID",
            "5. Click 'Next' and create a new policy with the permission policy JSON",
            "6. Name your role (e.g., 'WISTXDiscoveryRole') and create it",
            "7. Copy the Role ARN and paste it in WISTX",
        ],
        wistx_account_id=WISTX_AWS_ACCOUNT_ID,
    )


@router.post(
    "/external-id",
    response_model=ExternalIdResponse,
    summary="Generate a new External ID",
)
async def generate_external_id(
    request: GenerateExternalIdRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> ExternalIdResponse:
    """Generate a new External ID for AWS role assumption."""
    user_id = current_user.get("user_id")
    logger.info("Generating External ID for user %s, provider %s", user_id, request.provider)

    external_id = _generate_external_id()
    now = datetime.utcnow()

    return ExternalIdResponse(
        external_id=external_id,
        created_at=now,
        expires_at=now + timedelta(days=365),  # 1 year expiry
    )


@router.get(
    "/connections",
    summary="List cloud connections",
)
async def list_connections(
    provider: CloudProviderEnum | None = None,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """List all cloud connections for the current user."""
    user_id = current_user.get("user_id")
    logger.info("Listing connections for user %s", user_id)

    connections = await CloudDiscoveryService.list_connections(user_id, provider)

    return {
        "connections": [
            {
                "provider": c.provider.value,
                "role_arn": c.role_arn,
                "status": c.status.value,
                "account_id": c.account_id,
                "regions_accessible": c.regions_accessible,
                "last_validated": c.last_validated.isoformat() if c.last_validated else None,
                "created_at": c.created_at.isoformat() if c.created_at else None,
            }
            for c in connections
        ],
        "total": len(connections),
    }


@router.delete(
    "/connections/{role_arn:path}",
    summary="Deactivate a cloud connection",
)
async def deactivate_connection(
    role_arn: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Deactivate a cloud connection (soft delete)."""
    user_id = current_user.get("user_id")
    logger.info("Deactivating connection for user %s, role %s", user_id, role_arn)

    success = await CloudDiscoveryService.deactivate_connection(user_id, role_arn)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found",
        )

    return {"status": "deactivated", "role_arn": role_arn}


@router.get(
    "/stats",
    summary="Get discovery statistics",
)
async def get_discovery_stats(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Get discovery statistics for the current user."""
    user_id = current_user.get("user_id")
    logger.info("Getting discovery stats for user %s", user_id)

    stats = await CloudDiscoveryService.get_discovery_stats(user_id)
    return stats


@router.post(
    "/validate",
    response_model=ConnectionValidationResponse,
    summary="Validate AWS connection",
)
async def validate_connection(
    request: ValidateConnectionRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> ConnectionValidationResponse:
    """Validate AWS connection by attempting to assume the provided role."""
    user_id = current_user.get("user_id")
    logger.info("Validating connection for user %s, role %s", user_id, request.role_arn)

    try:
        from wistx_mcp.tools.lib.cloud_discovery.credential_providers.aws_assumed_role import (
            AWSAssumedRoleCredentialProvider,
        )

        provider = AWSAssumedRoleCredentialProvider(
            role_arn=request.role_arn,
            external_id=request.external_id,
        )

        is_valid = await provider.validate_credentials()
        account_id = request.role_arn.split(":")[4]  # Extract from ARN
        regions_accessible = ["us-east-1", "us-west-2", "eu-west-1"]  # TODO: Actually check

        # Save/update connection in database
        connection = CloudConnectionDocument(
            user_id=user_id,
            provider=request.provider,
            role_arn=request.role_arn,
            external_id=request.external_id,
            status=CredentialStatusEnum.VALID if is_valid else CredentialStatusEnum.INVALID,
            last_validated=datetime.utcnow(),
            account_id=account_id if is_valid else None,
            regions_accessible=regions_accessible if is_valid else [],
        )
        await CloudDiscoveryService.save_connection(connection)

        if is_valid:
            return ConnectionValidationResponse(
                is_valid=True,
                regions_accessible=regions_accessible,
                account_id=account_id,
            )
        else:
            return ConnectionValidationResponse(
                is_valid=False,
                error_message="Failed to assume role. Please verify the role ARN and External ID.",
            )

    except Exception as e:
        logger.error("Connection validation failed: %s", e)
        return ConnectionValidationResponse(
            is_valid=False,
            error_message=str(e),
        )


@router.post(
    "/start",
    summary="Start resource discovery",
)
async def start_discovery(
    request: StartDiscoveryRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
    authorization: str | None = Header(None, alias="Authorization"),
) -> dict[str, Any]:
    """Start resource discovery for the specified cloud provider.

    IMPORTANT: Data Persistence Strategy
    ------------------------------------
    We persist METADATA ONLY, not full resource data, because:
    1. Cloud infrastructure changes constantly - stored data becomes stale quickly
    2. Full resource configs may contain sensitive data (IPs, security groups)
    3. The AI coding agent in the user's IDE has the full data locally
    4. Reduces database storage and improves query performance

    The full discovery results are returned to the client for immediate use,
    but only summary metadata is stored in the database for audit/history.
    """
    user_id = current_user.get("user_id")
    discovery_id = str(uuid.uuid4())
    started_at = datetime.utcnow()
    logger.info("Starting discovery %s for user %s", discovery_id, user_id)

    try:
        from wistx_mcp.tools.discover_cloud_resources import discover_cloud_resources

        # Extract API key from authorization header for discover_cloud_resources function
        api_key = ""
        if authorization and authorization.startswith("Bearer "):
            api_key = authorization.replace("Bearer ", "").strip()

        # Start discovery (this could be async/background task in production)
        # Note: discover_cloud_resources uses saved connections if role_arn/external_id not provided
        result = await discover_cloud_resources(
            role_arn=request.role_arn if request.role_arn else None,
            external_id=request.external_id if request.external_id else None,
            connection_name=None,
            api_key=api_key,
            regions=request.regions,
            resource_types=request.resource_types,
            tag_filters=request.tags_filter,
            include_compliance=False,
            include_pricing=False,
            include_best_practices=False,
            generate_diagrams=True,
            terraform_state_content=None,
        )

        completed_at = datetime.utcnow()
        summary = result.get("summary", {})
        errors = result.get("validation_issues", [])

        # Create metadata document for database storage (NOT full resource data)
        # This is what gets persisted - summary only
        metadata_doc = DiscoveryMetadataDocument(
            discovery_id=discovery_id,
            user_id=user_id,
            provider=CloudProviderEnum(request.provider.value),
            status=DiscoveryStatusEnum.COMPLETED if not errors else DiscoveryStatusEnum.PARTIAL,
            regions_scanned=request.regions or [],
            resource_types_requested=request.resource_types,
            tags_filter=request.tags_filter,
            total_resources=summary.get("total_resources", 0),
            resource_type_counts=summary.get("by_resource_type", {}),
            region_counts=summary.get("by_region", {}),
            phase_counts=summary.get("by_phase", {}),
            total_dependencies=summary.get("total_dependencies", 0),
            has_circular_dependencies=summary.get("has_circular_dependencies", False),
            started_at=started_at,
            completed_at=completed_at,
            duration_seconds=(completed_at - started_at).total_seconds(),
            errors_count=len(errors),
            error_summaries=[e.get("error_message", str(e))[:200] for e in errors[:10]],
        )

        # Persist METADATA ONLY to MongoDB (not full resource data)
        await CloudDiscoveryService.save_discovery_metadata(metadata_doc)

        # Return FULL results to client (not persisted)
        # The client/AI agent uses this data locally
        return {
            "discovery_id": discovery_id,
            "status": result.get("status", "completed"),
            "provider": request.provider.value,
            "discovered_resources": result.get("discovered_resources", []),  # Full data - NOT persisted
            "dependency_graph": {
                "edges": result.get("dependencies", []),
                "topological_order": result.get("import_order", []),
                "phases": result.get("phases", {}),
                "has_cycles": result.get("has_circular_dependencies", False),
            },
            "terraform_names": result.get("terraform_names", {}),
            "import_commands": result.get("import_commands", []),
            "summary": summary,
            "validation_issues": errors,
            "started_at": started_at.isoformat(),
            "completed_at": completed_at.isoformat(),
        }

    except Exception as e:
        logger.error("Discovery failed: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Discovery failed: {str(e)}",
        ) from e


@router.get(
    "/discoveries",
    response_model=DiscoveryListResponse,
    summary="List discoveries",
)
async def list_discoveries(
    page: int = 1,
    per_page: int = 20,
    provider: CloudProviderEnum | None = None,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> DiscoveryListResponse:
    """List all discoveries for the current user."""
    user_id = current_user.get("user_id")
    logger.info("Listing discoveries for user %s", user_id)

    discoveries, total = await CloudDiscoveryService.list_discoveries(
        user_id=user_id,
        provider=provider,
        page=page,
        per_page=per_page,
    )

    # Convert to list items (summary view)
    items = [
        DiscoveryListItem(
            discovery_id=d.discovery_id,
            status=d.status,
            provider=d.provider,
            total_resources=d.total_resources,
            started_at=d.started_at,
            completed_at=d.completed_at,
            errors_count=d.errors_count,
        )
        for d in discoveries
    ]

    return DiscoveryListResponse(
        discoveries=items,
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get(
    "/discoveries/{discovery_id}",
    summary="Get discovery metadata",
)
async def get_discovery(
    discovery_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Get discovery metadata (summary only, not full resource data).

    NOTE: Full resource data is NOT stored in the database.
    This endpoint returns metadata/summary only. The full discovery
    results are returned at discovery time and should be used by
    the AI coding agent in the user's IDE.
    """
    user_id = current_user.get("user_id")
    logger.info("Getting discovery %s for user %s", discovery_id, user_id)

    metadata = await CloudDiscoveryService.get_discovery_metadata(discovery_id, user_id)
    if not metadata:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Discovery {discovery_id} not found",
        )

    return {
        "discovery_id": metadata.discovery_id,
        "status": metadata.status.value,
        "provider": metadata.provider.value,
        "regions_scanned": metadata.regions_scanned,
        "total_resources": metadata.total_resources,
        "resource_type_counts": metadata.resource_type_counts,
        "region_counts": metadata.region_counts,
        "phase_counts": metadata.phase_counts,
        "total_dependencies": metadata.total_dependencies,
        "has_circular_dependencies": metadata.has_circular_dependencies,
        "started_at": metadata.started_at.isoformat() if metadata.started_at else None,
        "completed_at": metadata.completed_at.isoformat() if metadata.completed_at else None,
        "duration_seconds": metadata.duration_seconds,
        "errors_count": metadata.errors_count,
        "error_summaries": metadata.error_summaries,
        # NOTE: resources and dependency_graph are NOT stored - use discovery results directly
        "note": "Full resource data is not persisted. Use discovery results from the initial discovery call.",
    }


@router.get(
    "/terraform-mappings/{provider}",
    response_model=TerraformMappingResponse,
    summary="Get Terraform mappings",
)
async def get_terraform_mappings(
    provider: CloudProviderEnum,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> TerraformMappingResponse:
    """Get Terraform resource type mappings for a cloud provider."""
    logger.info("Getting Terraform mappings for provider %s", provider)

    try:
        from wistx_mcp.tools.lib.cloud_discovery.terraform_mapping_loader import (
            TerraformMappingLoader,
        )

        loader = TerraformMappingLoader()
        mappings = loader.load_mappings(provider.value)

        return TerraformMappingResponse(
            provider=provider,
            total_mappings=len(mappings),
            mappings={m.cloud_type: m.model_dump() for m in mappings.values()},
        )

    except Exception as e:
        logger.error("Failed to load Terraform mappings: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load mappings: {str(e)}",
        ) from e


# Request model for documentation generation
from pydantic import BaseModel, Field


class GenerateInfraDocRequest(BaseModel):
    """Request model for infrastructure documentation generation."""

    subject: str = Field(..., description="Project/infrastructure name")
    discovery_data: dict[str, Any] = Field(
        ..., description="Discovery results (resources, dependency_graph, metrics)"
    )
    format: str = Field(
        default="markdown",
        description="Output format: markdown, html, pdf, docx",
    )
    include_compliance: bool = Field(default=True, description="Include compliance analysis")
    include_security: bool = Field(default=True, description="Include security recommendations")
    include_diagram: bool = Field(default=True, description="Include architecture diagram")
    include_import_commands: bool = Field(default=True, description="Include Terraform import commands")
    include_toc: bool = Field(default=True, description="Include table of contents")


@router.post(
    "/generate-documentation",
    summary="Generate infrastructure documentation",
    description="Generate comprehensive technical documentation from discovery results in various formats (Markdown, HTML, PDF, DOCX).",
)
async def generate_infrastructure_documentation(
    request: GenerateInfraDocRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Generate infrastructure import documentation from discovery results.

    This endpoint generates comprehensive technical documentation including:
    - Executive summary with discovery metrics
    - Resource inventory by type and import phase
    - Architecture diagram (Mermaid)
    - Dependency analysis and import order
    - Terraform import commands
    - Security recommendations
    - Compliance considerations

    The documentation can be exported in multiple formats for download.
    """
    user_id = current_user.get("user_id")
    logger.info("Generating infrastructure documentation for user %s", user_id)

    try:
        from wistx_mcp.tools.generate_documentation import generate_documentation

        result = await generate_documentation(
            document_type="infrastructure_import_report",
            subject=request.subject,
            format=request.format,
            configuration={
                "discovery_data": request.discovery_data,
                "include_toc": request.include_toc,
                "include_import_commands": request.include_import_commands,
                "include_diagram": request.include_diagram,
            },
            include_compliance=request.include_compliance,
            include_security=request.include_security,
        )

        import base64

        content = result.get("content", "")
        output_format = result.get("format", "markdown")

        content_type_map = {
            "markdown": "text/markdown",
            "html": "text/html",
            "pdf": "application/pdf",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        }

        if isinstance(content, bytes):
            content_b64 = base64.b64encode(content).decode("utf-8")
            is_binary = True
        else:
            content_b64 = base64.b64encode(content.encode("utf-8")).decode("utf-8")
            is_binary = False

        return {
            "content": content if not is_binary else content_b64,
            "content_base64": content_b64,
            "format": output_format,
            "content_type": content_type_map.get(output_format, "text/plain"),
            "is_binary": is_binary,
            "document_type": "infrastructure_import_report",
            "subject": request.subject,
            "sections": result.get("sections", []),
            "metadata": result.get("metadata", {}),
        }

    except ValueError as e:
        logger.warning("Invalid documentation request: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Documentation generation failed: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Documentation generation failed: {str(e)}",
        ) from e

