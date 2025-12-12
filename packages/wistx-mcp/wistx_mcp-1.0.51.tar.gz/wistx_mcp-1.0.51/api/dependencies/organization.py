"""Organization context and dependencies for automatic data isolation."""

import logging
from typing import Annotated, Any, Optional

from bson import ObjectId
from fastapi import Depends, HTTPException, Path, Request, status

from api.database.mongodb import mongodb_manager
from api.dependencies.auth import get_current_user

logger = logging.getLogger(__name__)


class OrganizationContext:
    """Organization context for automatic data isolation.

    This ensures all queries are automatically filtered by organization_id,
    preventing data leakage between organizations (enterprise security requirement).
    """

    def __init__(
        self,
        organization_id: Optional[ObjectId],
        user_id: ObjectId,
        user_role: str,
        permissions: list[str],
        organization_plan: str,
    ):
        """Initialize organization context.

        Args:
            organization_id: Organization ID (None for individual users)
            user_id: User ID
            user_role: User role in organization (owner, admin, member, viewer, individual)
            permissions: Granular permissions
            organization_plan: Organization plan (team, enterprise, professional, etc.)
        """
        self.organization_id = organization_id
        self.user_id = user_id
        self.user_role = user_role
        self.permissions = permissions
        self.organization_plan = organization_plan

    def get_query_filter(self, base_query: dict[str, Any] | None = None) -> dict[str, Any]:
        """Get MongoDB query filter with automatic organization isolation.

        Args:
            base_query: Base query to extend

        Returns:
            Query filter with organization_id included
        """
        query = base_query or {}
        if self.organization_id:
            query["organization_id"] = self.organization_id
        return query

    def can_access_resource(self, resource_org_id: Optional[ObjectId]) -> bool:
        """Check if user can access a resource based on organization.

        Args:
            resource_org_id: Organization ID of the resource

        Returns:
            True if user can access, False otherwise
        """
        if not self.organization_id:
            return resource_org_id is None
        return resource_org_id == self.organization_id


async def get_organization_context(
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
) -> OrganizationContext:
    """Get organization context with automatic isolation.

    This dependency automatically:
    1. Loads user's organization membership
    2. Validates active membership
    3. Returns context with role and permissions
    4. Ensures all subsequent queries are isolated

    Args:
        current_user: Current authenticated user

    Returns:
        OrganizationContext with isolation guarantees

    Raises:
        HTTPException: If user is not in organization or membership is invalid
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    plan = current_user.get("plan", "professional")

    db = mongodb_manager.get_database()
    user = db.users.find_one({"_id": ObjectId(user_id)})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    organization_id = user.get("organization_id")

    if not organization_id:
        return OrganizationContext(
            organization_id=None,
            user_id=ObjectId(user_id),
            user_role="individual",
            permissions=[],
            organization_plan=plan,
        )

    member = db.organization_members.find_one(
        {
            "organization_id": ObjectId(organization_id),
            "user_id": ObjectId(user_id),
            "status": "active",
        }
    )

    if not member:
        logger.warning("User %s has organization_id but no active membership", user_id)
        return OrganizationContext(
            organization_id=None,
            user_id=ObjectId(user_id),
            user_role="individual",
            permissions=[],
            organization_plan=plan,
        )

    organization = db.organizations.find_one({"_id": ObjectId(organization_id)})
    if not organization:
        logger.warning("Organization %s not found for user %s", organization_id, user_id)
        return OrganizationContext(
            organization_id=None,
            user_id=ObjectId(user_id),
            user_role="individual",
            permissions=[],
            organization_plan=plan,
        )

    return OrganizationContext(
        organization_id=ObjectId(organization_id),
        user_id=ObjectId(user_id),
        user_role=member.get("role", "member"),
        permissions=member.get("permissions", []),
        organization_plan=organization.get("plan_id", "team"),
    )


def require_organization_member(organization_id: str):
    """Dependency factory to require organization membership.

    Args:
        organization_id: Organization ID to require membership for

    Returns:
        Dependency function
    """

    async def dependency(
        org_context: OrganizationContext = Depends(get_organization_context),
    ) -> OrganizationContext:
        if not org_context.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not a member of any organization",
            )
        if str(org_context.organization_id) != organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not a member of this organization",
            )
        return org_context

    return dependency


def require_organization_admin(organization_id: str):
    """Dependency factory to require admin or owner role.

    Args:
        organization_id: Organization ID to require admin for

    Returns:
        Dependency function
    """

    async def dependency(
        org_context: OrganizationContext = Depends(require_organization_member(organization_id)),
    ) -> OrganizationContext:
        if org_context.user_role not in ["owner", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin or owner role required",
            )
        return org_context

    return dependency


def require_organization_owner(organization_id: str):
    """Dependency factory to require owner role.

    Args:
        organization_id: Organization ID to require owner for

    Returns:
        Dependency function
    """

    async def dependency(
        org_context: OrganizationContext = Depends(require_organization_member(organization_id)),
    ) -> OrganizationContext:
        if org_context.user_role != "owner":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Owner role required",
            )
        return org_context

    return dependency


async def require_organization_member_from_path(
    org_id: Annotated[str, Path(..., description="Organization ID")],
    org_context: Annotated[OrganizationContext, Depends(get_organization_context)],
) -> OrganizationContext:
    """Dependency to require organization membership from path parameter.

    This dependency can be used directly in route handlers where org_id is a path parameter.

    Args:
        org_id: Organization ID from path parameter
        org_context: Organization context from user's membership

    Returns:
        OrganizationContext with membership validated

    Raises:
        HTTPException: If user is not a member of the organization
    """
    if not org_context.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a member of any organization",
        )
    if str(org_context.organization_id) != org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a member of this organization",
        )
    return org_context


async def require_organization_admin_from_path(
    org_id: Annotated[str, Path(..., description="Organization ID")],
    org_context: Annotated[OrganizationContext, Depends(get_organization_context)],
) -> OrganizationContext:
    """Dependency to require admin or owner role for organization from path parameter.

    This dependency can be used directly in route handlers where org_id is a path parameter.

    Args:
        org_id: Organization ID from path parameter
        org_context: Organization context from user's membership

    Returns:
        OrganizationContext with admin/owner role validated

    Raises:
        HTTPException: If user is not admin/owner of the organization
    """
    if not org_context.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a member of any organization",
        )
    if str(org_context.organization_id) != org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a member of this organization",
        )
    if org_context.user_role not in ["owner", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin or owner role required",
        )
    return org_context


async def require_organization_owner_from_path(
    org_id: Annotated[str, Path(..., description="Organization ID")],
    org_context: Annotated[OrganizationContext, Depends(get_organization_context)],
) -> OrganizationContext:
    """Dependency to require owner role for organization from path parameter.

    This dependency can be used directly in route handlers where org_id is a path parameter.

    Args:
        org_id: Organization ID from path parameter
        org_context: Organization context from user's membership

    Returns:
        OrganizationContext with owner role validated

    Raises:
        HTTPException: If user is not owner of the organization
    """
    if not org_context.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a member of any organization",
        )
    if str(org_context.organization_id) != org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a member of this organization",
        )
    if org_context.user_role != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Owner role required",
        )
    return org_context

