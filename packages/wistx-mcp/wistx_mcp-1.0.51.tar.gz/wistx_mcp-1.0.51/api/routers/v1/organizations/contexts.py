"""Organization context endpoints for sharing contexts with team."""

import logging
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies.organization import (
    OrganizationContext,
    require_organization_member_from_path,
)
from api.services.intelligent_context_service import intelligent_context_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/organizations/{org_id}/contexts", tags=["organization-contexts"])


@router.post("/{context_id}/share", status_code=status.HTTP_200_OK)
async def share_context_with_organization(
    org_id: str,
    context_id: str,
    org_context: Annotated[OrganizationContext, Depends(require_organization_member_from_path)] = None,
) -> dict[str, Any]:
    """Share context with organization.

    **CRITICAL**: Only context owner can share with organization.

    Args:
        org_id: Organization ID
        context_id: Context ID
        org_context: Organization context (ensures membership)

    Returns:
        Dictionary with updated context

    Raises:
        HTTPException: If context not found or access denied
    """
    user_id = str(org_context.user_id)

    try:
        context = await intelligent_context_service.share_context_with_organization(
            context_id=context_id,
            user_id=user_id,
            organization_id=org_id,
        )

        if not context:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Context not found or access denied: {context_id}",
            )

        return {"data": context.model_dump()}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error sharing context with organization: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to share context with organization",
        ) from e


@router.post("/{context_id}/unshare", status_code=status.HTTP_200_OK)
async def unshare_context_from_organization(
    org_id: str,
    context_id: str,
    org_context: Annotated[OrganizationContext, Depends(require_organization_member_from_path)] = None,
) -> dict[str, Any]:
    """Unshare context from organization (make it private).

    **CRITICAL**: Only context owner can unshare from organization.

    Args:
        org_id: Organization ID
        context_id: Context ID
        org_context: Organization context (ensures membership)

    Returns:
        Dictionary with updated context

    Raises:
        HTTPException: If context not found or access denied
    """
    user_id = str(org_context.user_id)

    try:
        context = await intelligent_context_service.unshare_context_from_organization(
            context_id=context_id,
            user_id=user_id,
        )

        if not context:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Context not found or access denied: {context_id}",
            )

        return {"data": context.model_dump()}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error unsharing context from organization: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to unshare context from organization",
        ) from e
