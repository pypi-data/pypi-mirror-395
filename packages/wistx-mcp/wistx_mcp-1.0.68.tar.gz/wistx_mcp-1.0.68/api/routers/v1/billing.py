"""Billing and subscription endpoints."""

import logging
from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.dependencies import get_current_user
from api.exceptions import ExternalServiceError
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
    force_sync: bool = Query(False, description="Force sync from Stripe"),
) -> SubscriptionStatus:
    """Get current user's subscription with automatic sync from Stripe.

    This endpoint automatically syncs subscription data from Stripe on every call,
    ensuring the database always has the latest subscription status and plan information.
    Works automatically without any manual intervention.

    Args:
        current_user: Current authenticated user

    Returns:
        Current subscription status (always synced with Stripe)
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
    stripe_customer_id = user.get("stripe_customer_id")
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
            cancel_at_period_end=False,
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

            if org_subscription_id:
                try:
                    subscription_data = await billing_service.get_subscription(org_subscription_id)
                    if subscription_data:
                        org_stripe_status = subscription_data.get("status", org_subscription_status or "inactive")
                        period_start_dt = None
                        period_end_dt = None
                        
                        current_period_start_raw = subscription_data.get("current_period_start")
                        current_period_end_raw = subscription_data.get("current_period_end")
                        
                        if current_period_start_raw:
                            if isinstance(current_period_start_raw, (int, float)):
                                period_start_dt = datetime.utcfromtimestamp(current_period_start_raw)
                            elif isinstance(current_period_start_raw, datetime):
                                period_start_dt = current_period_start_raw
                        
                        if current_period_end_raw:
                            if isinstance(current_period_end_raw, (int, float)):
                                period_end_dt = datetime.utcfromtimestamp(current_period_end_raw)
                            elif isinstance(current_period_end_raw, datetime):
                                period_end_dt = current_period_end_raw
                        
                        return SubscriptionStatus(
                            plan_id=plan,
                            status=org_stripe_status,
                            subscription_id=org_subscription_id,
                            current_period_start=period_start_dt,
                            current_period_end=period_end_dt,
                            cancel_at_period_end=subscription_data.get("cancel_at_period_end", False),
                        )
                except Exception as e:
                    logger.error("Error fetching organization subscription from Stripe: %s", e, exc_info=True)

    from api.services.subscription_cache_service import SubscriptionCacheService
    from api.services.subscription_sync_service import SubscriptionSyncService

    if not force_sync:
        cached = await SubscriptionCacheService.get_cached_subscription(user_id)
        if cached:
            cached_status = cached.get("status")
            cached_plan = cached.get("plan")
            cached_subscription_id = cached.get("subscription_id")
            db_status = user.get("subscription_status")
            db_plan = user.get("plan")
            db_subscription_id = user.get("stripe_subscription_id")

            # Check for any mismatch between cache and database
            status_mismatch = cached_status and db_status and cached_status != db_status
            plan_mismatch = cached_plan and db_plan and cached_plan != db_plan
            subscription_id_mismatch = cached_subscription_id and db_subscription_id and cached_subscription_id != db_subscription_id

            if status_mismatch or plan_mismatch or subscription_id_mismatch:
                logger.warning(
                    "Cache-MongoDB mismatch detected: user=%s, status=%s/%s, plan=%s/%s, sub_id=%s/%s - invalidating cache and forcing sync",
                    user_id,
                    cached_status, db_status,
                    cached_plan, db_plan,
                    cached_subscription_id, db_subscription_id,
                )
                await SubscriptionCacheService.invalidate_cache(user_id)
                force_sync = True
            else:
                logger.debug("Returning cached subscription for user: %s", user_id)
                period_start_dt = None
                period_end_dt = None

                current_period_start = cached.get("current_period_start")
                current_period_end = cached.get("current_period_end")

                if current_period_start:
                    if isinstance(current_period_start, (int, float)):
                        period_start_dt = datetime.utcfromtimestamp(current_period_start)
                    elif isinstance(current_period_start, datetime):
                        period_start_dt = current_period_start

                if current_period_end:
                    if isinstance(current_period_end, (int, float)):
                        period_end_dt = datetime.utcfromtimestamp(current_period_end)
                    elif isinstance(current_period_end, datetime):
                        period_end_dt = current_period_end

                return SubscriptionStatus(
                    plan_id=cached.get("plan"),
                    status=cached.get("status"),
                    subscription_id=cached.get("subscription_id"),
                    current_period_start=period_start_dt,
                    current_period_end=period_end_dt,
                    cancel_at_period_end=cached.get("cancel_at_period_end", False),
                )

    sync_result = None
    if stripe_customer_id:
        try:
            logger.info("Syncing subscription from Stripe for user: %s, customer_id: %s", user_id, stripe_customer_id)
            sync_result = await SubscriptionSyncService.sync_user_subscription(user_id, force=force_sync)
            if sync_result:
                logger.info("Sync successful: user=%s, status=%s, plan=%s, subscription_id=%s", user_id, sync_result.get("status"), sync_result.get("plan"), sync_result.get("subscription_id"))
            else:
                logger.warning("Sync returned None for user: %s (may not have subscription)", user_id)
            
            if sync_result:
                user = db.users.find_one({"_id": ObjectId(user_id)})
                subscription_id = sync_result.get("subscription_id")
                subscription_status = sync_result.get("status")
                plan = sync_result.get("plan")
                
                period_start_dt = None
                period_end_dt = None
                
                current_period_start = sync_result.get("current_period_start")
                current_period_end = sync_result.get("current_period_end")
                
                if current_period_start:
                    if isinstance(current_period_start, (int, float)):
                        period_start_dt = datetime.utcfromtimestamp(current_period_start)
                    elif isinstance(current_period_start, datetime):
                        period_start_dt = current_period_start
                
                if current_period_end:
                    if isinstance(current_period_end, (int, float)):
                        period_end_dt = datetime.utcfromtimestamp(current_period_end)
                    elif isinstance(current_period_end, datetime):
                        period_end_dt = current_period_end
                
                return SubscriptionStatus(
                    plan_id=plan,
                    status=subscription_status,
                    subscription_id=subscription_id,
                    current_period_start=period_start_dt,
                    current_period_end=period_end_dt,
                    cancel_at_period_end=sync_result.get("cancel_at_period_end", False),
                )
        except Exception as e:
            logger.error("Automatic subscription sync failed (using cached data): user=%s, error=%s", user_id, e, exc_info=True)

    now = datetime.utcnow()
    subscription_status_value = subscription_status or "inactive"
    
    period_start_dt = None
    period_end_dt = None
    
    if subscription_status_value in ("active", "trialing") and subscription_id:
        try:
            subscription_data = await billing_service.get_subscription(subscription_id)
            if subscription_data:
                current_period_start_raw = subscription_data.get("current_period_start")
                current_period_end_raw = subscription_data.get("current_period_end")
                
                if current_period_start_raw:
                    if isinstance(current_period_start_raw, (int, float)):
                        period_start_dt = datetime.utcfromtimestamp(current_period_start_raw)
                    elif isinstance(current_period_start_raw, datetime):
                        period_start_dt = current_period_start_raw
                
                if current_period_end_raw:
                    if isinstance(current_period_end_raw, (int, float)):
                        period_end_dt = datetime.utcfromtimestamp(current_period_end_raw)
                    elif isinstance(current_period_end_raw, datetime):
                        period_end_dt = current_period_end_raw
        except Exception as e:
            logger.warning(
                "Failed to fetch subscription period dates from Stripe: subscription_id=%s, user_id=%s, error=%s",
                subscription_id,
                user_id,
                e,
            )
    
    return SubscriptionStatus(
        plan_id=plan,
        status=subscription_status_value,
        subscription_id=subscription_id,
        current_period_start=period_start_dt if period_start_dt else (now if subscription_status_value in ("active", "trialing") else None),
        current_period_end=period_end_dt,
        cancel_at_period_end=False,
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

    plan_id = None
    for plan in plan_service.list_plans():
        if plan.stripe_monthly_price_id == request.price_id or plan.stripe_annual_price_id == request.price_id:
            plan_id = plan.plan_id
            break

    if not plan_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plan not found for price ID: {request.price_id}",
        )

    plan = plan_service.get_plan(plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plan {plan_id} not found",
        )

    if not plan.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Plan {plan_id} is not active for new signups",
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
    user_email = user.get("email", "")
    user_name = user.get("full_name") or user.get("name", "")
    existing_subscription_id = user.get("stripe_subscription_id")
    subscription_status = user.get("subscription_status")
    
    if not stripe_customer_id:
        customer = await billing_service.get_or_create_customer(
            user_id=user_id,
            email=user_email,
            name=user_name,
        )
        stripe_customer_id = customer.customer_id
        logger.info("Retrieved or created Stripe customer: %s for user: %s", stripe_customer_id, user_id)
    else:
        try:
            import stripe
            from stripe import _error as stripe_error
            stripe.Customer.retrieve(stripe_customer_id)
            logger.debug("Using existing Stripe customer: %s", stripe_customer_id)
        except stripe_error.StripeError:
            logger.warning("Stripe customer %s not found, creating new one", stripe_customer_id)
            customer = await billing_service.get_or_create_customer(
                user_id=user_id,
                email=user_email,
                name=user_name,
            )
            stripe_customer_id = customer.customer_id

    if existing_subscription_id and subscription_status in ("active", "trialing", "past_due"):
        try:
            subscription_data = await billing_service.get_subscription(existing_subscription_id)
            if subscription_data and subscription_data.get("status") in ("active", "trialing", "past_due"):
                logger.info(
                    "User %s has active subscription %s, redirecting to Stripe Customer Portal for plan change",
                    user_id,
                    existing_subscription_id,
                )
                
                return_url = request.success_url or f"{request.cancel_url or '/billing?tab=overview'}"
                portal_session = await billing_service.create_portal_session(
                    customer_id=stripe_customer_id,
                    return_url=return_url,
                )
                
                from api.config import settings
                
                return CheckoutSessionResponse(
                    session_id="portal_redirect",
                    url=portal_session.url,
                    publishable_key=settings.stripe_publishable_key or "",
                )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(
                "Error creating portal session for plan change: %s",
                e,
                exc_info=True,
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to open billing portal. Please try again or contact support.",
            ) from e

    try:
        session = await billing_service.create_checkout_session(
            customer_id=stripe_customer_id,
            price_id=request.price_id,
            success_url=request.success_url,
            cancel_url=request.cancel_url,
            metadata={"user_id": user_id, "plan_id": plan_id},
        )
        return CheckoutSessionResponse(
            session_id=session.session_id,
            url=session.url,
            publishable_key=session.publishable_key,
        )
    except ExternalServiceError as e:
        if e.error_code == "STRIPE_CUSTOMER_NOT_FOUND":
            logger.warning(
                "Stripe customer ID %s not found in Stripe. Clearing invalid customer ID and creating new customer.",
                stripe_customer_id,
            )
            db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$unset": {"stripe_customer_id": ""}},
            )
            user_email = user.get("email", "")
            user_name = user.get("full_name") or user.get("name", "")
            customer = await billing_service.get_or_create_customer(
                user_id=user_id,
                email=user_email,
                name=user_name,
            )
            stripe_customer_id = customer.customer_id
            logger.info("Created new Stripe customer: %s for user: %s", stripe_customer_id, user_id)
            session = await billing_service.create_checkout_session(
                customer_id=stripe_customer_id,
                price_id=request.price_id,
                success_url=request.success_url,
                cancel_url=request.cancel_url,
                metadata={"user_id": user_id, "plan_id": plan_id},
            )
            return CheckoutSessionResponse(
                session_id=session.session_id,
                url=session.url,
                publishable_key=session.publishable_key,
            )
        raise
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
            url=session.url,
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


@router.post("/subscription/cancel")
async def cancel_subscription(
    immediately: bool = Query(False, description="Cancel immediately or at period end"),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Cancel user's subscription.

    Args:
        immediately: Cancel immediately or at period end
        current_user: Current authenticated user

    Returns:
        Cancellation result
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    from api.database.mongodb import mongodb_manager
    from bson import ObjectId
    from api.services.subscription_cache_service import SubscriptionCacheService

    db = mongodb_manager.get_database()
    user = db.users.find_one({"_id": ObjectId(user_id)})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    subscription_id = user.get("stripe_subscription_id")
    if not subscription_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active subscription found",
        )

    try:
        result = await billing_service.cancel_subscription(
            subscription_id=subscription_id,
            immediately=immediately,
        )

        await SubscriptionCacheService.invalidate_cache(user_id)

        update_data = {
            "cancel_at_period_end": not immediately,
        }

        if immediately:
            update_data["subscription_status"] = "canceled"
            update_data["canceled_at"] = datetime.utcnow()
        else:
            update_data["subscription_status"] = user.get("subscription_status", "active")

        db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})

        logger.info("Subscription canceled: user=%s, immediately=%s", user_id, immediately)

        return {
            "status": "success",
            "message": "Subscription canceled successfully",
            "canceled_immediately": immediately,
            "cancel_at_period_end": not immediately,
            "access_until": user.get("subscription_renews_at") if not immediately else None,
        }

    except Exception as e:
        logger.error("Error canceling subscription: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel subscription",
        ) from e


@router.post("/checkout/verify", response_model=SubscriptionStatus)
async def verify_checkout(
    session_id: str = Query(..., description="Stripe checkout session ID"),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> SubscriptionStatus:
    """Verify checkout completion and sync subscription immediately.

    This endpoint is called after successful checkout to immediately
    sync subscription data from Stripe, even before webhooks are processed.

    Args:
        session_id: Stripe checkout session ID
        current_user: Current authenticated user

    Returns:
        Updated subscription status
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    from api.database.mongodb import mongodb_manager
    from bson import ObjectId

    try:
        session_data = await billing_service.get_checkout_session(session_id)
        customer_id = session_data.get("customer")
        subscription_id = session_data.get("subscription")
        metadata = session_data.get("metadata", {})

        if not customer_id or not subscription_id:
            logger.warning(
                "Checkout session missing customer or subscription: session_id=%s, customer_id=%s, subscription_id=%s",
                session_id,
                customer_id,
                subscription_id,
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Checkout session is incomplete",
            )

        db = mongodb_manager.get_database()
        user = db.users.find_one({"_id": ObjectId(user_id)})

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        session_user_id = metadata.get("user_id")
        if session_user_id and session_user_id != user_id:
            logger.warning(
                "Checkout session user_id mismatch: session_user_id=%s, current_user_id=%s",
                session_user_id,
                user_id,
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Checkout session does not belong to current user",
            )

        from api.services.subscription_sync_service import SubscriptionSyncService
        from api.routers.internal.webhooks import determine_plan_from_price_id, validate_and_get_plan_id

        subscription_data = await billing_service.get_subscription(subscription_id)
        price_id = subscription_data.get("price_id")
        plan_id = determine_plan_from_price_id(price_id)
        validated_plan_id = validate_and_get_plan_id(plan_id)

        logger.info(
            "Checkout verification: user_id=%s, subscription_id=%s, price_id=%s, plan_id=%s",
            user_id,
            subscription_id,
            price_id,
            validated_plan_id,
        )

        update_data = {
            "$set": {
                "stripe_customer_id": customer_id,
                "stripe_subscription_id": subscription_id,
                "plan": validated_plan_id,
                "subscription_status": subscription_data.get("status", "active"),
                "is_active": subscription_data.get("status") in ("active", "trialing"),
            }
        }

        current_period_start = subscription_data.get("current_period_start")
        current_period_end = subscription_data.get("current_period_end")

        if current_period_start:
            if isinstance(current_period_start, (int, float)):
                update_data["$set"]["subscription_start"] = datetime.utcfromtimestamp(current_period_start)
            else:
                update_data["$set"]["subscription_start"] = current_period_start

        if current_period_end:
            if isinstance(current_period_end, (int, float)):
                update_data["$set"]["subscription_renews_at"] = datetime.utcfromtimestamp(current_period_end)
            else:
                update_data["$set"]["subscription_renews_at"] = current_period_end

        update_result = db.users.update_one(
            {"_id": ObjectId(user_id)},
            update_data,
        )

        if update_result.modified_count > 0:
            logger.info(
                "Updated user with checkout session data: user_id=%s, customer_id=%s, subscription_id=%s, plan=%s",
                user_id,
                customer_id,
                subscription_id,
                validated_plan_id,
            )
        else:
            logger.warning(
                "Checkout verification update had no effect: user_id=%s, subscription_id=%s",
                user_id,
                subscription_id,
            )

        sync_result = await SubscriptionSyncService.sync_user_subscription(user_id, force=True)

        if sync_result:
            period_start_dt = None
            period_end_dt = None

            current_period_start = sync_result.get("current_period_start")
            current_period_end = sync_result.get("current_period_end")

            if current_period_start:
                if isinstance(current_period_start, (int, float)):
                    period_start_dt = datetime.utcfromtimestamp(current_period_start)
                elif isinstance(current_period_start, datetime):
                    period_start_dt = current_period_start

            if current_period_end:
                if isinstance(current_period_end, (int, float)):
                    period_end_dt = datetime.utcfromtimestamp(current_period_end)
                elif isinstance(current_period_end, datetime):
                    period_end_dt = current_period_end

            return SubscriptionStatus(
                plan_id=sync_result.get("plan"),
                status=sync_result.get("status"),
                subscription_id=sync_result.get("subscription_id"),
                current_period_start=period_start_dt,
                current_period_end=period_end_dt,
                cancel_at_period_end=sync_result.get("cancel_at_period_end", False),
            )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to sync subscription after checkout",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Error verifying checkout: user_id=%s, session_id=%s, error=%s",
            user_id,
            session_id,
            e,
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to verify checkout",
        ) from e


@router.post("/subscription/reactivate")
async def reactivate_subscription(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Reactivate a canceled subscription.

    Args:
        current_user: Current authenticated user

    Returns:
        Reactivation result
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    from api.database.mongodb import mongodb_manager
    from bson import ObjectId
    import stripe
    from api.services.subscription_cache_service import SubscriptionCacheService

    db = mongodb_manager.get_database()
    user = db.users.find_one({"_id": ObjectId(user_id)})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    subscription_id = user.get("stripe_subscription_id")
    if not subscription_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No subscription found",
        )

    try:
        subscription = stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=False,
        )

        db.users.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "subscription_status": subscription.status,
                    "cancel_at_period_end": False,
                },
                "$unset": {"canceled_at": ""},
            },
        )

        await SubscriptionCacheService.invalidate_cache(user_id)

        logger.info("Subscription reactivated: user=%s", user_id)

        return {
            "status": "success",
            "message": "Subscription reactivated successfully",
        }

    except Exception as e:
        logger.error("Error reactivating subscription: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reactivate subscription",
        ) from e


@router.get("/verify-payment")
async def verify_payment(
    session_id: str = Query(..., description="Stripe checkout session ID"),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Verify payment and subscription status.

    Args:
        session_id: Stripe checkout session ID
        current_user: Current authenticated user

    Returns:
        Verification result
    """
    from api.services.payment_verification_service import PaymentVerificationService
    from api.services.subscription_cache_service import SubscriptionCacheService

    result = await PaymentVerificationService.verify_checkout_session(session_id)

    if result["verified"]:
        user_id = current_user.get("user_id")
        if user_id:
            await SubscriptionCacheService.invalidate_cache(user_id)

    return result


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
