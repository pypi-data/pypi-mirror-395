"""Organization API key endpoints."""

import logging
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from api.auth.api_keys import api_key_manager
from api.dependencies.organization import (
    OrganizationContext,
    require_organization_admin_from_path,
    require_organization_member_from_path,
)
from api.models.admin.security import AdminAPIKeyResponse, APIKeyListResponse
from api.routers.v1.auth import APIKeyResponse, CreateAPIKeyRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/organizations/{org_id}/api-keys", tags=["organization-api-keys"])


@router.post("", response_model=APIKeyResponse, status_code=status.HTTP_201_CREATED)
async def create_organization_api_key(
    org_id: str,
    request: CreateAPIKeyRequest,
    org_context: Annotated[OrganizationContext, Depends(require_organization_admin_from_path)],
) -> APIKeyResponse:
    """Create organization API key.

    **CRITICAL**: Only organization admins and owners can create API keys.
    Organization API keys are shared across all team members.

    Args:
        org_id: Organization ID
        request: Create API key request
        org_context: Organization context (ensures admin role)

    Returns:
        Created API key response

    Raises:
        HTTPException: If user is not organization admin/owner or limit exceeded
    """
    user_id = str(org_context.user_id)

    try:
        result = await api_key_manager.create_organization_api_key(
            organization_id=org_id,
            name=request.name,
            created_by=user_id,
            description=request.description,
            expires_at=request.expires_at,
        )

        return APIKeyResponse(
            api_key=result["api_key"],
            api_key_id=result["api_key_id"],
            key_prefix=result["key_prefix"],
            created_at=result["created_at"],
            expires_at=result.get("expires_at"),
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error creating organization API key: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create organization API key",
        ) from e


@router.get("", response_model=APIKeyListResponse)
async def list_organization_api_keys(
    org_id: str,
    org_context: Annotated[OrganizationContext, Depends(require_organization_member_from_path)],
) -> APIKeyListResponse:
    """List all organization API keys.

    **CRITICAL**: Only organization members can list organization API keys.

    Args:
        org_id: Organization ID
        org_context: Organization context (ensures membership)

    Returns:
        List of organization API keys

    Raises:
        HTTPException: If user is not organization member
    """
    user_id = str(org_context.user_id)

    try:
        keys = await api_key_manager.list_organization_api_keys(
            organization_id=org_id,
            user_id=user_id,
        )

        from api.models.admin.security import AdminAPIKeyResponse

        api_keys = [
            AdminAPIKeyResponse(
                api_key_id=key["api_key_id"],
                key_prefix=key["key_prefix"],
                name=key.get("name"),
                user_id=key.get("created_by", ""),
                user_email=None,
                organization_id=org_id,
                plan="",
                is_active=key.get("is_active", False),
            )
            for key in keys
        ]

        return APIKeyListResponse(
            api_keys=api_keys,
            total=len(api_keys),
            limit=len(api_keys),
            offset=0,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error listing organization API keys: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list organization API keys",
        ) from e


@router.delete("/{api_key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_organization_api_key(
    org_id: str,
    api_key_id: str,
    http_request: Request,
    org_context: Annotated[OrganizationContext, Depends(require_organization_admin_from_path)],
) -> Response:
    """Revoke organization API key.

    **CRITICAL**: Only organization admins and owners can revoke API keys.

    Args:
        org_id: Organization ID
        api_key_id: API key ID
        http_request: FastAPI request object
        org_context: Organization context (ensures admin role)

    Returns:
        Empty response

    Raises:
        HTTPException: If user is not organization admin/owner or key not found
    """
    user_id = str(org_context.user_id)

    try:
        ip_address = http_request.client.host if http_request.client else None
        user_agent = http_request.headers.get("user-agent")

        success = await api_key_manager.revoke_organization_api_key(
            organization_id=org_id,
            api_key_id=api_key_id,
            user_id=user_id,
            reason=None,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization API key not found or access denied",
            )

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error revoking organization API key: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to revoke organization API key",
        ) from e

