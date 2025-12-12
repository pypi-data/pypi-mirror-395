"""Organization management endpoints."""

import logging
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

logger = logging.getLogger(__name__)

from api.dependencies.auth import get_current_user
from api.dependencies.organization import (
    OrganizationContext,
    get_organization_context,
    require_organization_admin,
    require_organization_admin_from_path,
    require_organization_member,
    require_organization_member_from_path,
    require_organization_owner,
    require_organization_owner_from_path,
)
from api.models.organization import (
    CreateOrganizationRequest,
    InviteMemberRequest,
    Organization,
    UpdateAllowedDomainsRequest,
    UpdateMemberRoleRequest,
    UpdateOrganizationRequest,
)
from api.services.organization_service import organization_service

router = APIRouter(prefix="/organizations", tags=["organizations"])

from api.routers.v1.organizations.billing import router as billing_router
from api.routers.v1.organizations.api_keys import router as api_keys_router
from api.routers.v1.organizations.analytics import router as analytics_router
from api.routers.v1.organizations.contexts import router as contexts_router

router.include_router(billing_router)
router.include_router(api_keys_router)
router.include_router(analytics_router)
router.include_router(contexts_router)


@router.post("", response_model=Organization, status_code=status.HTTP_201_CREATED)
async def create_organization(
    request: CreateOrganizationRequest,
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
    http_request: Request,
) -> Organization:
    """Create new organization.

    **CRITICAL**: Only Team and Enterprise plans can create organizations.
    Professional plan users will receive a 403 Forbidden error.

    Args:
        request: Create organization request
        current_user: Current authenticated user
        http_request: FastAPI request object

    Returns:
        Created organization

    Raises:
        HTTPException: If user plan doesn't support organizations
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    org_dict = await organization_service.create_organization(
        user_id=user_id,
        name=request.name,
        plan_id=request.plan_id,
        request=http_request,
    )

    org = Organization.from_dict(org_dict)
    return org.model_dump(by_alias=False)


@router.get("", response_model=list[Organization])
async def list_organizations(
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
) -> list[Organization]:
    """List user's organizations.

    Args:
        current_user: Current authenticated user

    Returns:
        List of organizations user is a member of
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    orgs = await organization_service.list_user_organizations(user_id)
    organizations = [Organization.from_dict(org) for org in orgs]
    return [org.model_dump(by_alias=False, mode="json") for org in organizations]


@router.get("/{org_id}", response_model=Organization)
async def get_organization(
    org_id: str,
    org_context: Annotated[OrganizationContext, Depends(require_organization_member_from_path)],
) -> Organization:
    """Get organization details.

    Args:
        org_id: Organization ID
        org_context: Organization context (ensures membership)

    Returns:
        Organization details

    Raises:
        HTTPException: If organization not found or user is not a member
    """
    org = await organization_service.get_organization(org_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    org_model = Organization.from_dict(org)
    return org_model.model_dump(by_alias=False)


@router.patch("/{org_id}", response_model=Organization)
async def update_organization(
    org_id: str,
    request: UpdateOrganizationRequest,
    org_context: Annotated[OrganizationContext, Depends(require_organization_admin_from_path)],
    http_request: Request,
) -> Organization:
    """Update organization.

    Args:
        org_id: Organization ID
        request: Update request
        org_context: Organization context (ensures admin role)
        http_request: FastAPI request object

    Returns:
        Updated organization

    Raises:
        HTTPException: If organization not found or user lacks permission
    """
    org = await organization_service.update_organization(
        organization_id=org_id,
        updates=request,
        updated_by=str(org_context.user_id),
        request=http_request,
    )

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    org_model = Organization.from_dict(org)
    return org_model.model_dump(by_alias=False)


@router.get("/invitations/validate", summary="Validate organization invitation token")
async def validate_invitation_token(
    token: str = Query(..., description="Invitation token"),
) -> dict[str, Any]:
    """Validate organization invitation token and return details.

    Args:
        token: Invitation token

    Returns:
        Invitation details including organization name and inviter name

    Raises:
        HTTPException: If invitation not found, expired, or invalid
    """
    invitation_details = await organization_service.validate_invitation_token(token)
    return invitation_details


@router.post("/{org_id}/members/invite", status_code=status.HTTP_201_CREATED)
async def invite_member(
    org_id: str,
    request: InviteMemberRequest,
    org_context: Annotated[OrganizationContext, Depends(require_organization_admin_from_path)],
    http_request: Request,
) -> dict[str, Any]:
    """Invite member to organization.

    Args:
        org_id: Organization ID
        request: Invite member request
        org_context: Organization context (ensures admin role)
        http_request: FastAPI request object

    Returns:
        Created invitation

    Raises:
        HTTPException: If organization not found, user lacks permission, or invitation already exists
    """
    invitation = await organization_service.invite_member(
        organization_id=org_id,
        email=request.email,
        role=request.role,
        invited_by=str(org_context.user_id),
        request=http_request,
    )

    return {
        "id": str(invitation["_id"]),
        "email": invitation["email"],
        "role": invitation["role"],
        "expires_at": invitation["expires_at"],
        "status": invitation["status"],
    }


@router.post("/invitations/{token}/accept", status_code=status.HTTP_200_OK)
async def accept_invitation(
    token: str,
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
    http_request: Request,
) -> dict[str, Any]:
    """Accept organization invitation.

    Args:
        token: Invitation token
        current_user: Current authenticated user
        http_request: FastAPI request object

    Returns:
        List of organization members

    Raises:
        HTTPException: If invitation not found, expired, or invalid
    """
    user_id = current_user.get("user_id")
    if not user_id:
        logger.error("User ID not found in current_user when accepting invitation", {"token": token[:20] + "..."})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    logger.info("Accepting organization invitation", {"user_id": user_id, "token": token[:20] + "..."})

    try:
        members = await organization_service.accept_invitation(
            token=token,
            user_id=user_id,
            request=http_request,
        )
        logger.info("Successfully accepted organization invitation", {"user_id": user_id, "token": token[:20] + "..."})
        return {"members": members}
    except HTTPException as e:
        logger.error(
            "Failed to accept organization invitation",
            {
                "user_id": user_id,
                "token": token[:20] + "...",
                "status_code": e.status_code,
                "detail": str(e.detail),
            },
            exc_info=True,
        )
        raise
    except Exception as e:
        logger.error(
            "Unexpected error accepting organization invitation",
            {
                "user_id": user_id,
                "token": token[:20] + "...",
                "error": str(e),
            },
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to accept invitation",
        ) from e


@router.get("/{org_id}/invitations", status_code=status.HTTP_200_OK)
async def list_organization_invitations(
    org_id: str,
    org_context: Annotated[OrganizationContext, Depends(require_organization_member_from_path)],
    status: str = Query(default="pending", description="Filter by invitation status"),
) -> dict[str, Any]:
    """List organization invitations.

    Args:
        org_id: Organization ID
        org_context: Organization context (ensures member role)
        status: Invitation status filter

    Returns:
        List of invitations
    """
    invitations = await organization_service.list_invitations(
        organization_id=org_id, status=status
    )
    return {"invitations": invitations}


@router.get("/{org_id}/members", status_code=status.HTTP_200_OK)
async def list_members(
    org_id: str,
    org_context: Annotated[OrganizationContext, Depends(require_organization_member_from_path)],
) -> dict[str, Any]:
    """List organization members.

    Args:
        org_id: Organization ID
        org_context: Organization context (ensures membership)

    Returns:
        List of organization members

    Raises:
        HTTPException: If organization not found or user is not a member
    """
    members = await organization_service.list_members(org_id)
    return {"members": members}


@router.delete("/{org_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    org_id: str,
    user_id: str,
    org_context: Annotated[OrganizationContext, Depends(require_organization_admin_from_path)],
    http_request: Request,
) -> None:
    """Remove member from organization.

    Args:
        org_id: Organization ID
        user_id: User ID to remove
        org_context: Organization context (ensures admin role)
        http_request: FastAPI request object

    Raises:
        HTTPException: If organization not found, user lacks permission, or cannot remove owner
    """
    await organization_service.remove_member(
        organization_id=org_id,
        user_id=user_id,
        removed_by=str(org_context.user_id),
        request=http_request,
    )


@router.patch("/{org_id}/members/{user_id}/role", status_code=status.HTTP_200_OK)
async def update_member_role(
    org_id: str,
    user_id: str,
    request: UpdateMemberRoleRequest,
    org_context: Annotated[OrganizationContext, Depends(require_organization_owner_from_path)],
    http_request: Request,
) -> dict[str, str]:
    """Update member role.

    Args:
        org_id: Organization ID
        user_id: User ID to update
        request: Update role request
        org_context: Organization context (ensures owner role)
        http_request: FastAPI request object

    Returns:
        Success message

    Raises:
        HTTPException: If organization not found, user lacks permission, or invalid role
    """
    await organization_service.update_member_role(
        organization_id=org_id,
        user_id=user_id,
        role=request.role,
        updated_by=str(org_context.user_id),
        request=http_request,
    )

    return {"message": f"Member role updated to {request.role}"}


@router.patch("/{org_id}/settings/domains", response_model=Organization)
async def update_allowed_domains(
    org_id: str,
    request: UpdateAllowedDomainsRequest,
    org_context: Annotated[OrganizationContext, Depends(require_organization_owner_from_path)],
    http_request: Request,
) -> Organization:
    """Update allowed email domains for organization.

    **CRITICAL**: Only Enterprise plans can enable domain restriction.
    Only organization owners can update domain settings.

    Args:
        org_id: Organization ID
        request: Update allowed domains request
        org_context: Organization context (ensures owner role)
        http_request: FastAPI request object

    Returns:
        Updated organization

    Raises:
        HTTPException: If organization not found, user lacks permission, or plan is not Enterprise
    """
    org = await organization_service.get_organization(org_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    if org.get("plan_id") != "enterprise":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Domain restriction is only available for Enterprise plans",
        )

    current_settings = org.get("settings", {})
    current_settings.update({
        "allowed_domains": request.allowed_domains,
        "require_domain_match": request.require_domain_match,
    })

    updated_org = await organization_service.update_organization(
        organization_id=org_id,
        updates=UpdateOrganizationRequest(settings=current_settings),
        updated_by=str(org_context.user_id),
        request=http_request,
    )

    if not updated_org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    org_model = Organization.from_dict(updated_org)
    return org_model.model_dump(by_alias=False)

