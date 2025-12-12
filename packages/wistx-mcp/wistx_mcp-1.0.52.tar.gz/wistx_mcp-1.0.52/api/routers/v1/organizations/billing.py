"""Organization billing endpoints."""

import logging
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies.organization import (
    OrganizationContext,
    require_organization_owner_from_path,
)
from api.models.billing import (
    CheckoutSessionRequest,
    CheckoutSessionResponse,
    CustomerPortalRequest,
    CustomerPortalResponse,
)
from api.services.billing_service import billing_service
from api.services.plan_service import plan_service
from api.services.organization_service import organization_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/organizations/{org_id}/billing", tags=["organization-billing"])


@router.post("/checkout", response_model=CheckoutSessionResponse)
async def create_organization_checkout(
    org_id: str,
    request: CheckoutSessionRequest,
    org_context: Annotated[OrganizationContext, Depends(require_organization_owner_from_path)],
) -> CheckoutSessionResponse:
    """Create Stripe checkout session for organization.

    **CRITICAL**: Only organization owners can create checkout sessions.

    Args:
        org_id: Organization ID
        request: Checkout session request
        org_context: Organization context (ensures owner role)

    Returns:
        Checkout session response with URL

    Raises:
        HTTPException: If user is not organization owner or plan not found
    """
    from api.dependencies.organization import OrganizationContext

    org = await organization_service.get_organization(org_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    plan = plan_service.get_plan(org.plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plan {org.plan_id} not found",
        )

    if not plan.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Plan {org.plan_id} is not active for new signups",
        )

    price_id = request.price_id
    if not price_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stripe price ID is required",
        )

    stripe_customer_id = org.stripe_customer_id
    if not stripe_customer_id:
        from api.database.mongodb import mongodb_manager
        from bson import ObjectId

        db = mongodb_manager.get_database()
        owner = db.organization_members.find_one(
            {
                "organization_id": ObjectId(org_id),
                "role": "owner",
                "status": "active",
            }
        )
        if owner:
            user = db.users.find_one({"_id": owner["user_id"]}, {"email": 1, "full_name": 1})
            user_email = user.get("email", "") if user else ""
            user_name = user.get("full_name", org.name) if user else org.name
        else:
            user_email = ""
            user_name = org.name

        customer = await billing_service.create_organization_customer(
            organization_id=org_id,
            email=user_email,
            name=user_name,
        )
        stripe_customer_id = customer["customer_id"]

    try:
        session = await billing_service.create_organization_checkout_session(
            customer_id=stripe_customer_id,
            price_id=price_id,
            success_url=request.success_url,
            cancel_url=request.cancel_url,
            organization_id=org_id,
        )
        return CheckoutSessionResponse(
            session_id=session["session_id"],
            url=session["url"],
        )
    except Exception as e:
        logger.error("Error creating organization checkout session: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create checkout session",
        ) from e


@router.post("/portal", response_model=CustomerPortalResponse)
async def create_organization_portal(
    org_id: str,
    request: CustomerPortalRequest,
    org_context: Annotated[OrganizationContext, Depends(require_organization_owner_from_path)],
) -> CustomerPortalResponse:
    """Create Stripe customer portal session for organization.

    **CRITICAL**: Only organization owners can access the billing portal.

    Args:
        org_id: Organization ID
        request: Customer portal request
        org_context: Organization context (ensures owner role)

    Returns:
        Customer portal session response with URL

    Raises:
        HTTPException: If user is not organization owner or no Stripe customer found
    """
    org = await organization_service.get_organization(org_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    stripe_customer_id = org.stripe_customer_id
    if not stripe_customer_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Stripe customer ID found. Please create a subscription first.",
        )

    try:
        session = await billing_service.create_organization_portal_session(
            customer_id=stripe_customer_id,
            return_url=request.return_url,
        )
        return CustomerPortalResponse(
            url=session["url"],
        )
    except Exception as e:
        logger.error("Error creating organization portal session: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create portal session",
        ) from e

