"""Billing and subscription endpoints."""

import logging
from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from api.dependencies import get_current_user
from api.models.billing import (
    CheckoutSessionRequest,
    CheckoutSessionResponse,
    CustomerPortalRequest,
    CustomerPortalResponse,
    SubscriptionPlan,
    SubscriptionStatus,
)
from api.services.billing_service import billing_service
from api.services.plan_service import plan_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/billing", tags=["billing"])


@router.get("/plans", response_model=list[SubscriptionPlan])
async def list_plans(
    active_only: bool = Query(False, description="If true, only return active plans"),
) -> list[SubscriptionPlan]:
    """List all available subscription plans.

    Args:
        active_only: If true, only return active plans

    Returns:
        List of subscription plans
    """
    return plan_service.list_plans(active_only=active_only)


@router.get("/subscription", response_model=SubscriptionStatus)
async def get_subscription(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> SubscriptionStatus:
    """Get current user's subscription.

    Args:
        current_user: Current authenticated user

    Returns:
        Current subscription status
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    from api.database.mongodb import mongodb_manager
    from bson import ObjectId

    db = mongodb_manager.get_database()
    user = db.users.find_one({"_id": ObjectId(user_id)})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    subscription_id = user.get("stripe_subscription_id")
    subscription_status = user.get("subscription_status")
    plan = user.get("plan", "professional")
    organization_id = user.get("organization_id")
    
    is_admin = current_user.get("is_admin", False)
    is_super_admin = user.get("is_super_admin", False)
    
    if is_admin or is_super_admin:
        now = datetime.utcnow()
        return SubscriptionStatus(
            plan_id=plan,
            status="active",
            subscription_id=subscription_id,
            current_period_start=now,
            current_period_end=now + timedelta(days=365),
        )

    if organization_id:
        org = db.organizations.find_one({"_id": ObjectId(organization_id), "status": "active"})
        if org:
            org_subscription_id = org.get("stripe_subscription_id")
            org_subscription_status = org.get("subscription_status")
            org_plan_id = org.get("plan_id")

            if org_subscription_id:
                subscription_id = org_subscription_id
            if org_subscription_status:
                subscription_status = org_subscription_status
            if org_plan_id:
                plan = org_plan_id

    if subscription_id:
        try:
            subscription_data = await billing_service.get_subscription(subscription_id)
            if subscription_data:
                return SubscriptionStatus(
                    plan_id=plan,
                    status=subscription_data.get("status", subscription_status or "inactive"),
                    subscription_id=subscription_id,
                    current_period_start=subscription_data.get("current_period_start"),
                    current_period_end=subscription_data.get("current_period_end"),
                    cancel_at_period_end=subscription_data.get("cancel_at_period_end", False),
                )
        except Exception as e:
            logger.error("Error fetching subscription from Stripe: %s", e, exc_info=True)

    now = datetime.utcnow()
    return SubscriptionStatus(
        plan_id=plan,
        status=subscription_status or "inactive",
        subscription_id=subscription_id,
        current_period_start=now,
        current_period_end=now + timedelta(days=30),
    )


@router.post("/checkout", response_model=CheckoutSessionResponse)
async def create_checkout_session(
    request: CheckoutSessionRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> CheckoutSessionResponse:
    """Create Stripe checkout session.

    Args:
        request: Checkout session request
        current_user: Current authenticated user

    Returns:
        Checkout session response with URL
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    plan = plan_service.get_plan(request.plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plan {request.plan_id} not found",
        )

    if not plan.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Plan {request.plan_id} is not active for new signups",
        )

    price_id = plan.stripe_monthly_price_id if request.billing_cycle == "monthly" else plan.stripe_annual_price_id
    if not price_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stripe price ID not configured for {request.plan_id} plan ({request.billing_cycle})",
        )

    from api.database.mongodb import mongodb_manager
    from bson import ObjectId

    db = mongodb_manager.get_database()
    user = db.users.find_one({"_id": ObjectId(user_id)})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    stripe_customer_id = user.get("stripe_customer_id")
    if not stripe_customer_id:
        user_email = user.get("email", "")
        user_name = user.get("full_name") or user.get("name", "")
        customer = await billing_service.create_customer(
            user_id=user_id,
            email=user_email,
            name=user_name,
        )
        stripe_customer_id = customer["customer_id"]

    try:
        session = await billing_service.create_checkout_session(
            customer_id=stripe_customer_id,
            price_id=price_id,
            success_url=request.success_url,
            cancel_url=request.cancel_url,
            metadata={"user_id": user_id, "plan_id": request.plan_id},
        )
        return CheckoutSessionResponse(
            session_id=session["id"],
            url=session["url"],
        )
    except Exception as e:
        logger.error("Error creating checkout session: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create checkout session",
        ) from e


@router.post("/portal", response_model=CustomerPortalResponse)
async def create_portal_session(
    request: CustomerPortalRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> CustomerPortalResponse:
    """Create Stripe customer portal session.

    Args:
        request: Customer portal request
        current_user: Current authenticated user

    Returns:
        Customer portal session response with URL
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    from api.database.mongodb import mongodb_manager
    from bson import ObjectId

    db = mongodb_manager.get_database()
    user = db.users.find_one({"_id": ObjectId(user_id)})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    stripe_customer_id = user.get("stripe_customer_id")
    if not stripe_customer_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Stripe customer ID found. Please create a subscription first.",
        )

    try:
        session = await billing_service.create_portal_session(
            customer_id=stripe_customer_id,
            return_url=request.return_url,
        )
        return CustomerPortalResponse(
            url=session["url"],
        )
    except Exception as e:
        logger.error("Error creating portal session: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create portal session",
        ) from e


@router.post("/trial/start")
async def start_trial(
    plan: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Start 7-day free trial for Professional or Team plan.

    Args:
        plan: Plan ID (professional or team)
        current_user: Current authenticated user

    Returns:
        Trial activation response
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    if plan not in ["professional", "team"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Trial only available for Professional or Team plans. "
                f"Enterprise plans require custom pricing. "
                f"Visit https://app.wistx.ai/billing to subscribe."
            ),
        )

    from api.services.quota_service import quota_service

    try:
        quota_service.start_trial(user_id, plan)
        return {
            "status": "success",
            "message": f"7-day free trial started for {plan} plan",
            "trial_end": (datetime.utcnow() + timedelta(days=7)).isoformat(),
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error starting trial: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start trial",
        ) from e


@router.post("/migrate")
async def migrate_plan(
    target_plan_id: str = Query(..., description="Target plan ID to migrate to"),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Upgrade user to a higher plan.

    Args:
        target_plan_id: Target plan ID (professional, team, or enterprise)
        current_user: Current authenticated user

    Returns:
        Upgrade result
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    from api.database.mongodb import mongodb_manager
    from bson import ObjectId

    db = mongodb_manager.get_database()
    user = db.users.find_one({"_id": ObjectId(user_id)})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    current_plan = user.get("plan", "professional")

    valid_plans = ["professional", "team", "enterprise"]
    if target_plan_id not in valid_plans:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid plan ID {target_plan_id}. Valid plans are: {', '.join(valid_plans)}.",
        )

    if current_plan == target_plan_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"You are already on the {target_plan_id} plan.",
        )

    target_plan = plan_service.get_plan(target_plan_id)
    if not target_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Target plan {target_plan_id} not found",
        )

    if not target_plan.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Target plan {target_plan_id} is not active",
        )

    subscription_id = user.get("stripe_subscription_id")
    if subscription_id:
        try:
            subscription_data = await billing_service.get_subscription(subscription_id)
            if subscription_data and subscription_data.get("status") not in ("canceled", "past_due"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        f"You have an active Stripe subscription. "
                        f"Please use the billing portal to upgrade your plan, or contact support for migration assistance. "
                        f"Visit https://app.wistx.ai/billing to manage your subscription."
                    ),
                )
        except Exception as e:
            logger.error("Error checking subscription: %s", e, exc_info=True)

    try:
        db.users.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "plan": target_plan_id,
                    "migrated_from": current_plan,
                    "migrated_at": datetime.utcnow(),
                },
            },
        )

        logger.info("User %s migrated from %s to %s", user_id, current_plan, target_plan_id)

        return {
            "status": "success",
            "message": f"Successfully migrated from {current_plan} to {target_plan_id}",
            "previous_plan": current_plan,
            "new_plan": target_plan_id,
            "migrated_at": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error("Error migrating plan: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to migrate plan",
        ) from e
