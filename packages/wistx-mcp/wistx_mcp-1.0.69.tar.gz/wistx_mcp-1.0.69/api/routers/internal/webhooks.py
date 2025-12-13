"""Stripe webhook handlers."""

import logging
from typing import Any

from fastapi import APIRouter, HTTPException, Request, status

from api.config import settings
from api.services.billing_service import billing_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/stripe")
async def stripe_webhook(request: Request) -> dict[str, str]:
    """Handle Stripe webhook events.

    Args:
        request: FastAPI request object

    Returns:
        Success response
    """
    if not settings.stripe_webhook_secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Webhook secret not configured",
        )

    import stripe

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not sig_header:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing stripe-signature header",
        )

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.stripe_webhook_secret,
        )
    except ValueError as e:
        logger.error("Invalid payload: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid payload",
        ) from e
    except stripe.SignatureVerificationError as e:
        logger.error("Invalid signature: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid signature",
        ) from e

    event_id = event.get("id")
    event_type = event["type"]
    event_data = event["data"]["object"]
    created_at = event.get("created", 0)

    if not event_id:
        logger.error("Stripe webhook event missing ID")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid webhook event: missing ID",
        )

    from api.services.webhook_lock_service import WebhookLockService
    from api.services.webhook_event_store import WebhookEventStore

    event_stored = WebhookEventStore.store_event(
        event_id=event_id,
        event_type=event_type,
        source="stripe",
        event_data=event_data,
        created_at=created_at,
    )

    if not event_stored:
        logger.info("Duplicate event detected, skipping: %s", event_id)
        return {"status": "success", "message": "Event already processed"}

    lock_acquired = WebhookLockService.acquire_lock(event_id, "stripe")
    if not lock_acquired:
        logger.warning("Could not acquire lock for event, may be processing: %s", event_id)
        return {"status": "success", "message": "Event is being processed"}

    logger.info("Received Stripe webhook: %s [event_id=%s]", event_type, event_id)

    try:
        from api.database.mongodb import mongodb_manager
        from pymongo import errors as pymongo_errors

        db = mongodb_manager.get_database()

        with db.client.start_session() as session:
            with session.start_transaction():
                try:
                    if event_type == "customer.subscription.created":
                        await handle_subscription_created(event_data)
                    elif event_type == "customer.subscription.updated":
                        await handle_subscription_updated(event_data)
                    elif event_type == "customer.subscription.deleted":
                        await handle_subscription_deleted(event_data)
                    elif event_type == "customer.subscription.trial_will_end":
                        await handle_trial_will_end(event_data)
                    elif event_type == "invoice.payment_succeeded":
                        await handle_payment_succeeded(event_data)
                    elif event_type == "invoice.payment_failed":
                        await handle_payment_failed(event_data)
                    elif event_type == "invoice.payment_action_required":
                        await handle_payment_action_required(event_data)
                    elif event_type == "invoice.upcoming":
                        await handle_invoice_upcoming(event_data)
                    elif event_type == "checkout.session.completed":
                        await handle_checkout_completed(event_data)
                    else:
                        logger.info("Unhandled event type: %s", event_type)

                    WebhookEventStore.mark_event_processed(event_id, "stripe", success=True)
                    session.commit_transaction()

                except Exception as e:
                    session.abort_transaction()
                    WebhookEventStore.mark_event_processed(event_id, "stripe", success=False)
                    raise

        return {"status": "success"}

    except Exception as e:
        logger.error("Error handling webhook event: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Webhook processing failed",
        ) from e
    finally:
        WebhookLockService.release_lock(event_id, "stripe")


async def find_user_for_subscription(
    subscription_id: str | None = None,
    customer_id: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> tuple[dict[str, Any] | None, bool]:
    """Unified user/org lookup with multiple fallback strategies.

    Tries multiple strategies to find the user or organization:
    1. Lookup by subscription_id (most specific)
    2. Lookup by customer_id (checks org first, then user)
    3. Lookup by metadata user_id (from checkout session)

    Args:
        subscription_id: Stripe subscription ID
        customer_id: Stripe customer ID
        metadata: Webhook metadata (for user_id)

    Returns:
        (user_or_org_doc, is_organization)
    """
    from api.database.mongodb import mongodb_manager
    from api.services.billing_service import billing_service
    from bson import ObjectId

    db = mongodb_manager.get_database()

    if subscription_id:
        org_doc = db.organizations.find_one({"stripe_subscription_id": subscription_id})
        if org_doc:
            logger.info("Found organization by subscription_id: %s", subscription_id)
            return org_doc, True

        user_doc = db.users.find_one({"stripe_subscription_id": subscription_id})
        if user_doc:
            logger.info("Found user by subscription_id: %s", subscription_id)
            return user_doc, False

    if customer_id:
        org_doc = db.organizations.find_one({"stripe_customer_id": customer_id})
        if org_doc:
            if subscription_id:
                try:
                    subscription_data = await billing_service.get_subscription(subscription_id)
                    if subscription_data and subscription_data.get("customer_id") == customer_id:
                        logger.info("Found organization by customer_id: %s", customer_id)
                        return org_doc, True
                except Exception as e:
                    logger.warning("Failed to verify subscription for org: %s", e)
            else:
                logger.info("Found organization by customer_id (no subscription_id to verify): %s", customer_id)
                return org_doc, True

        user_doc = db.users.find_one({"stripe_customer_id": customer_id})
        if user_doc:
            if subscription_id:
                try:
                    subscription_data = await billing_service.get_subscription(subscription_id)
                    if subscription_data and subscription_data.get("customer_id") == customer_id:
                        logger.info("Found user by customer_id: %s", customer_id)
                        return user_doc, False
                except Exception as e:
                    logger.warning("Failed to verify subscription for user: %s", e)
            else:
                logger.info("Found user by customer_id (no subscription_id to verify): %s", customer_id)
                return user_doc, False

    if metadata and metadata.get("user_id"):
        user_id = metadata.get("user_id")
        try:
            user_doc = db.users.find_one({"_id": ObjectId(user_id)})
            if user_doc:
                logger.info("Found user by metadata user_id: %s", user_id)
                return user_doc, False
        except Exception as e:
            logger.warning("Failed to lookup user by metadata user_id: %s", e)

    logger.warning(
        "Could not find user/org for subscription: subscription_id=%s, customer_id=%s",
        subscription_id,
        customer_id
    )
    return None, False


async def handle_subscription_created(subscription: dict[str, Any]) -> None:
    """Handle subscription created event.

    Args:
        subscription: Stripe subscription object
    """
    customer_id = subscription.get("customer")
    subscription_id = subscription.get("id")
    status_value = subscription.get("status")

    user_or_org, is_organization = await find_user_for_subscription(
        subscription_id=subscription_id,
        customer_id=customer_id,
        metadata=None
    )

    if not user_or_org:
        logger.warning("User/org not found for subscription: subscription_id=%s, customer_id=%s", subscription_id, customer_id)
        return

    if is_organization:
        await handle_organization_subscription_created(subscription, user_or_org)
        return

    user_doc = user_or_org

    if user_doc.get("stripe_subscription_id") == subscription_id:
        logger.info("Subscription already linked to user, skipping duplicate event: subscription_id=%s", subscription_id)
        return

    from api.services.billing_service import billing_service
    from api.database.mongodb import mongodb_manager
    from bson import ObjectId
    from datetime import datetime

    try:
        subscription_data = await billing_service.get_subscription(subscription_id)
        if not subscription_data:
            logger.error("Could not verify subscription %s with Stripe API", subscription_id)
            return
        
        verified_status = subscription_data.get("status")
        if verified_status != status_value:
            logger.warning("Status mismatch: webhook=%s, verified=%s", status_value, verified_status)
            status_value = verified_status
    except Exception as e:
        logger.error("Failed to verify subscription with Stripe API: %s", e)
        return

    price_id = subscription.get("items", {}).get("data", [{}])[0].get("price", {}).get("id")
    plan_id = determine_plan_from_price_id(price_id)
    validated_plan_id = validate_and_get_plan_id(plan_id)

    current_plan = user_doc.get("plan", "professional")
    allowed_plan, is_upgrade = validate_plan_change(current_plan, validated_plan_id, status_value)

    if allowed_plan != validated_plan_id:
        logger.info(
            "Plan change validated: user=%s, current=%s, attempted=%s, allowed=%s, is_upgrade=%s",
            user_doc["_id"], current_plan, validated_plan_id, allowed_plan, is_upgrade
        )

    db = mongodb_manager.get_database()
    update_result = db.users.update_one(
        {"_id": user_doc["_id"]},
        {
            "$set": {
                "stripe_subscription_id": subscription_id,
                "subscription_status": status_value,
                "plan": allowed_plan,
                "subscription_start": datetime.utcfromtimestamp(subscription.get("current_period_start", 0)),
                "subscription_renews_at": datetime.utcfromtimestamp(subscription.get("current_period_end", 0)),
                "is_active": status_value in ("active", "trialing"),
            }
        },
    )

    if update_result.modified_count > 0:
        logger.info("Updated user %s subscription: %s, plan: %s (was: %s)", user_doc["_id"], subscription_id, allowed_plan, current_plan)
    else:
        logger.warning("Subscription update had no effect: user=%s, subscription_id=%s", user_doc["_id"], subscription_id)


async def handle_subscription_updated(subscription: dict[str, Any]) -> None:
    """Handle subscription updated event.

    Args:
        subscription: Stripe subscription object
    """
    customer_id = subscription.get("customer")
    subscription_id = subscription.get("id")
    status_value = subscription.get("status")

    user_or_org, is_organization = await find_user_for_subscription(
        subscription_id=subscription_id,
        customer_id=customer_id,
        metadata=None
    )

    if not user_or_org:
        logger.warning("User/org not found for subscription: subscription_id=%s, customer_id=%s", subscription_id, customer_id)
        return

    if is_organization:
        await handle_organization_subscription_updated(subscription, user_or_org)
        return

    user_doc = user_or_org

    from api.database.mongodb import mongodb_manager
    from api.services.billing_service import billing_service
    from bson import ObjectId
    from datetime import datetime

    try:
        subscription_data = await billing_service.get_subscription(subscription_id)
        if not subscription_data:
            logger.error("Could not verify subscription %s with Stripe API", subscription_id)
            return
        
        verified_status = subscription_data.get("status")
        if verified_status != status_value:
            logger.warning("Status mismatch: webhook=%s, verified=%s", status_value, verified_status)
            status_value = verified_status
    except Exception as e:
        logger.error("Failed to verify subscription with Stripe API: %s", e)
        return

    price_id = subscription.get("items", {}).get("data", [{}])[0].get("price", {}).get("id")
    plan_id = determine_plan_from_price_id(price_id)

    update_data = {
        "subscription_status": status_value,
        "subscription_renews_at": datetime.utcfromtimestamp(subscription.get("current_period_end", 0)),
        "is_active": status_value in ("active", "trialing"),
    }

    if plan_id:
        validated_plan_id = validate_and_get_plan_id(plan_id)
        current_plan = user_doc.get("plan", "professional")
        allowed_plan, is_upgrade = validate_plan_change(current_plan, validated_plan_id, status_value)

        logger.info(
            "Subscription updated webhook: user=%s, subscription_id=%s, current_plan=%s, new_plan=%s, allowed_plan=%s, is_upgrade=%s",
            user_doc["_id"], subscription_id, current_plan, validated_plan_id, allowed_plan, is_upgrade
        )
        
        update_data["plan"] = allowed_plan
        
        current_period_start = subscription_data.get("current_period_start")
        current_period_end = subscription_data.get("current_period_end")
        
        if current_period_start:
            if isinstance(current_period_start, (int, float)):
                update_data["subscription_start"] = datetime.utcfromtimestamp(current_period_start)
            else:
                update_data["subscription_start"] = current_period_start
        
        if current_period_end:
            if isinstance(current_period_end, (int, float)):
                update_data["subscription_renews_at"] = datetime.utcfromtimestamp(current_period_end)
            else:
                update_data["subscription_renews_at"] = current_period_end

    db = mongodb_manager.get_database()
    update_result = db.users.update_one(
        {"_id": user_doc["_id"]},
        {"$set": update_data},
    )

    if update_result.modified_count > 0:
        logger.info("Updated user %s subscription status: %s", user_doc["_id"], status_value)
        
        from api.services.subscription_cache_service import SubscriptionCacheService
        await SubscriptionCacheService.invalidate_cache(str(user_doc["_id"]))
        logger.debug("Invalidated subscription cache for user: %s", user_doc["_id"])
    else:
        logger.debug("Subscription update had no effect (already up-to-date): user=%s, subscription_id=%s", user_doc["_id"], subscription_id)


async def handle_subscription_deleted(subscription: dict[str, Any]) -> None:
    """Handle subscription deleted event.

    Args:
        subscription: Stripe subscription object
    """
    subscription_id = subscription.get("id")

    from api.database.mongodb import mongodb_manager
    from bson import ObjectId
    from datetime import datetime

    db = mongodb_manager.get_database()

    org_doc = db.organizations.find_one({"stripe_subscription_id": subscription_id})
    if org_doc:
        db.organizations.update_one(
            {"_id": org_doc["_id"]},
            {
                "$set": {
                    "subscription_status": "canceled",
                    "updated_at": datetime.utcnow(),
                },
                "$unset": {"stripe_subscription_id": ""},
            },
        )
        logger.info("Canceled subscription for organization %s", org_doc["_id"])
        return

    user_doc = db.users.find_one({"stripe_subscription_id": subscription_id})
    if not user_doc:
        logger.warning("User or organization not found for subscription: %s", subscription_id)
        return

    db.users.update_one(
        {"_id": user_doc["_id"]},
        {
            "$set": {
                "subscription_status": "canceled",
                "plan": "professional",
            },
            "$unset": {
                "stripe_subscription_id": "",
                "subscription_renews_at": "",
            },
        },
    )

    logger.info("Canceled subscription for user %s", user_doc["_id"])


async def handle_payment_succeeded(invoice: dict[str, Any]) -> None:
    """Handle payment succeeded event.

    Args:
        invoice: Stripe invoice object
    """
    customer_id = invoice.get("customer")
    subscription_id = invoice.get("subscription")

    if not subscription_id:
        return

    from api.database.mongodb import mongodb_manager
    from datetime import datetime

    db = mongodb_manager.get_database()

    org_doc = db.organizations.find_one({"stripe_customer_id": customer_id})
    if org_doc:
        db.organizations.update_one(
            {"_id": org_doc["_id"]},
            {
                "$set": {
                    "subscription_status": "active",
                    "updated_at": datetime.utcnow(),
                }
            },
        )
        logger.info("Payment succeeded for organization %s - quota access restored", org_doc["_id"])
        return

    user_doc = db.users.find_one({"stripe_customer_id": customer_id})
    if not user_doc:
        logger.warning("User or organization not found for customer: %s", customer_id)
        return

    db.users.update_one(
        {"_id": user_doc["_id"]},
        {"$set": {"subscription_status": "active", "is_active": True}},
    )

    logger.info("Payment succeeded for user %s - quota access restored", user_doc["_id"])


async def handle_payment_failed(invoice: dict[str, Any]) -> None:
    """Handle payment failed event.

    Args:
        invoice: Stripe invoice object
    """
    customer_id = invoice.get("customer")

    from api.database.mongodb import mongodb_manager
    from datetime import datetime

    db = mongodb_manager.get_database()

    org_doc = db.organizations.find_one({"stripe_customer_id": customer_id})
    if org_doc:
        db.organizations.update_one(
            {"_id": org_doc["_id"]},
            {
                "$set": {
                    "subscription_status": "past_due",
                    "updated_at": datetime.utcnow(),
                }
            },
        )
        logger.warning("Payment failed for organization %s - quota access blocked", org_doc["_id"])
        return

    user_doc = db.users.find_one({"stripe_customer_id": customer_id})
    if not user_doc:
        logger.warning("User or organization not found for customer: %s", customer_id)
        return

    db.users.update_one(
        {"_id": user_doc["_id"]},
        {"$set": {"subscription_status": "past_due"}},
    )

    logger.warning("Payment failed for user %s - quota access blocked", user_doc["_id"])


async def handle_checkout_completed(session: dict[str, Any]) -> None:
    """Handle checkout session completed event.

    Args:
        session: Stripe checkout session object
    """
    customer_id = session.get("customer")
    subscription_id = session.get("subscription")
    metadata = session.get("metadata", {})
    user_id = metadata.get("user_id")
    organization_id = metadata.get("organization_id")
    is_organization = metadata.get("type") == "organization"

    if not subscription_id:
        logger.warning("Missing subscription_id in checkout session")
        return

    from api.database.mongodb import mongodb_manager
    from bson import ObjectId
    from datetime import datetime

    db = mongodb_manager.get_database()

    subscription_data = await billing_service.get_subscription(subscription_id)
    price_id = subscription_data.get("price_id")
    plan_id = determine_plan_from_price_id(price_id)
    validated_plan_id = validate_and_get_plan_id(plan_id)

    if is_organization and organization_id:
        await handle_organization_checkout_completed(session, organization_id, subscription_data, validated_plan_id)
        return

    if not user_id:
        logger.warning("Missing user_id in checkout session")
        return

    user_doc = db.users.find_one({"_id": ObjectId(user_id)})
    if not user_doc:
        logger.warning("User not found for checkout completion: user_id=%s", user_id)
        return

    current_plan = user_doc.get("plan", "professional")
    allowed_plan, is_upgrade = validate_plan_change(current_plan, validated_plan_id, "active")

    if allowed_plan != validated_plan_id:
        logger.info(
            "Plan change validated during checkout: user=%s, current=%s, attempted=%s, allowed=%s",
            user_id, current_plan, validated_plan_id, allowed_plan
        )

    update_data = {
        "$set": {
            "stripe_customer_id": customer_id,
            "stripe_subscription_id": subscription_id,
            "subscription_status": "active",
            "is_active": True,
            "plan": allowed_plan,
            "subscription_start": datetime.utcfromtimestamp(subscription_data.get("current_period_start", 0)),
            "subscription_renews_at": datetime.utcfromtimestamp(subscription_data.get("current_period_end", 0)),
            "trial_used": True,
        },
        "$unset": {
            "trial_start": "",
            "trial_end": "",
            "trial_plan": "",
        }
    }

    if user_doc.get("subscription_status") == "inactive":
        if not user_doc.get("money_back_guarantee_start"):
            update_data["$set"]["money_back_guarantee_start"] = datetime.utcnow()
            update_data["$set"]["money_back_guarantee_end"] = datetime.utcnow() + timedelta(days=30)

    update_result = db.users.update_one(
        {"_id": ObjectId(user_id)},
        update_data,
    )

    if update_result.modified_count > 0:
        logger.info("Checkout completed for user %s, subscription %s, plan %s (was %s)", user_id, subscription_id, allowed_plan, current_plan)
        
        from api.services.subscription_cache_service import SubscriptionCacheService
        await SubscriptionCacheService.invalidate_cache(user_id)
        logger.debug("Invalidated subscription cache for user: %s", user_id)
    else:
        logger.warning("Checkout update had no effect: user=%s, subscription_id=%s", user_id, subscription_id)


async def handle_organization_subscription_created(
    subscription: dict[str, Any],
    org_doc: dict[str, Any],
) -> None:
    """Handle organization subscription created event.

    Args:
        subscription: Stripe subscription object
        org_doc: Organization document
    """
    subscription_id = subscription.get("id")
    status_value = subscription.get("status")

    from api.services.billing_service import billing_service
    from bson import ObjectId
    from datetime import datetime

    try:
        subscription_data = await billing_service.get_subscription(subscription_id)
        if not subscription_data:
            logger.error("Could not verify subscription %s with Stripe API", subscription_id)
            return

        verified_status = subscription_data.get("status")
        if verified_status != status_value:
            logger.warning("Status mismatch: webhook=%s, verified=%s", status_value, verified_status)
            status_value = verified_status
    except Exception as e:
        logger.error("Failed to verify subscription with Stripe API: %s", e)
        return

    from api.database.mongodb import mongodb_manager

    db = mongodb_manager.get_database()

    price_id = subscription.get("items", {}).get("data", [{}])[0].get("price", {}).get("id")
    plan_id = determine_plan_from_price_id(price_id)
    validated_plan_id = validate_and_get_plan_id(plan_id)

    current_plan = org_doc.get("plan_id", "team")
    if current_plan != validated_plan_id:
        logger.info("Organization plan change detected: org=%s, current=%s, new=%s",
                   org_doc["_id"], current_plan, validated_plan_id)

    db.organizations.update_one(
        {"_id": org_doc["_id"]},
        {
            "$set": {
                "stripe_subscription_id": subscription_id,
                "subscription_status": status_value,
                "plan_id": validated_plan_id,
                "updated_at": datetime.utcnow(),
            }
        },
    )

    logger.info(
        "Updated organization %s subscription: %s, plan: %s (was: %s)",
        org_doc["_id"],
        subscription_id,
        validated_plan_id,
        current_plan,
    )


async def handle_organization_subscription_updated(
    subscription: dict[str, Any],
    org_doc: dict[str, Any],
) -> None:
    """Handle organization subscription updated event.

    Args:
        subscription: Stripe subscription object
        org_doc: Organization document
    """
    subscription_id = subscription.get("id")
    status_value = subscription.get("status")

    from api.services.billing_service import billing_service
    from bson import ObjectId
    from datetime import datetime

    try:
        subscription_data = await billing_service.get_subscription(subscription_id)
        if not subscription_data:
            logger.error("Could not verify subscription %s with Stripe API", subscription_id)
            return

        verified_status = subscription_data.get("status")
        if verified_status != status_value:
            logger.warning("Status mismatch: webhook=%s, verified=%s", status_value, verified_status)
            status_value = verified_status
    except Exception as e:
        logger.error("Failed to verify subscription with Stripe API: %s", e)
        return

    from api.database.mongodb import mongodb_manager

    db = mongodb_manager.get_database()

    price_id = subscription.get("items", {}).get("data", [{}])[0].get("price", {}).get("id")
    plan_id = determine_plan_from_price_id(price_id)

    update_data = {
        "subscription_status": status_value,
        "updated_at": datetime.utcnow(),
    }

    validated_plan_id = None
    if plan_id:
        validated_plan_id = validate_and_get_plan_id(plan_id)
        current_plan = org_doc.get("plan_id", "team")
        if current_plan != validated_plan_id:
            logger.info("Organization plan change detected: org=%s, current=%s, new=%s",
                       org_doc["_id"], current_plan, validated_plan_id)
            update_data["plan_id"] = validated_plan_id

    db.organizations.update_one(
        {"_id": org_doc["_id"]},
        {"$set": update_data},
    )

    logger.info(
        "Updated organization %s subscription: %s, status: %s",
        org_doc["_id"],
        subscription_id,
        status_value,
    )


async def handle_organization_checkout_completed(
    session: dict[str, Any],
    organization_id: str,
    subscription_data: dict[str, Any],
    validated_plan_id: str,
) -> None:
    """Handle organization checkout completed event.

    Args:
        session: Stripe checkout session object
        organization_id: Organization ID
        subscription_data: Subscription data from Stripe
        validated_plan_id: Validated plan ID
    """
    customer_id = session.get("customer")
    subscription_id = session.get("subscription")

    from api.database.mongodb import mongodb_manager
    from bson import ObjectId
    from datetime import datetime

    db = mongodb_manager.get_database()

    from datetime import timedelta

    org_doc = db.organizations.find_one({"_id": ObjectId(organization_id)})
    update_data = {
        "$set": {
            "stripe_customer_id": customer_id,
            "stripe_subscription_id": subscription_id,
            "subscription_status": "active",
            "plan_id": validated_plan_id,
            "updated_at": datetime.utcnow(),
        }
    }

    if org_doc and org_doc.get("subscription_status") == "inactive":
        owner_member = db.organization_members.find_one({
            "organization_id": ObjectId(organization_id),
            "role": "owner",
            "status": "active",
        })
        if owner_member:
            owner_user = db.users.find_one({"_id": owner_member["user_id"]})
            if owner_user and not owner_user.get("money_back_guarantee_start"):
                db.users.update_one(
                    {"_id": owner_member["user_id"]},
                    {
                        "$set": {
                            "money_back_guarantee_start": datetime.utcnow(),
                            "money_back_guarantee_end": datetime.utcnow() + timedelta(days=30),
                        }
                    },
                )

    db.organizations.update_one(
        {"_id": ObjectId(organization_id)},
        update_data,
    )

    logger.info(
        "Checkout completed for organization %s, subscription %s, plan %s",
        organization_id,
        subscription_id,
        validated_plan_id,
    )


async def handle_trial_will_end(subscription: dict[str, Any]) -> None:
    """Handle trial ending soon event.

    Args:
        subscription: Stripe subscription object
    """
    subscription_id = subscription.get("id")
    customer_id = subscription.get("customer")
    trial_end = subscription.get("trial_end")

    user_or_org, is_organization = await find_user_for_subscription(
        subscription_id=subscription_id,
        customer_id=customer_id,
    )

    if not user_or_org:
        logger.warning("User/org not found for trial ending: %s", subscription_id)
        return

    logger.info(
        "Trial ending soon for subscription: %s, trial_end: %s",
        subscription_id,
        trial_end,
    )


async def handle_payment_action_required(invoice: dict[str, Any]) -> None:
    """Handle payment action required (3D Secure/SCA).

    Args:
        invoice: Stripe invoice object
    """
    customer_id = invoice.get("customer")
    subscription_id = invoice.get("subscription")
    payment_intent = invoice.get("payment_intent")

    user_or_org, is_organization = await find_user_for_subscription(
        subscription_id=subscription_id,
        customer_id=customer_id,
    )

    if not user_or_org:
        logger.warning(
            "User/org not found for payment action required: %s", subscription_id
        )
        return

    from api.database.mongodb import mongodb_manager
    from datetime import datetime

    db = mongodb_manager.get_database()

    if is_organization:
        db.organizations.update_one(
            {"_id": user_or_org["_id"]},
            {
                "$set": {
                    "subscription_status": "incomplete",
                    "payment_action_required": True,
                    "payment_intent_id": payment_intent,
                    "updated_at": datetime.utcnow(),
                }
            },
        )
    else:
        db.users.update_one(
            {"_id": user_or_org["_id"]},
            {
                "$set": {
                    "subscription_status": "incomplete",
                    "payment_action_required": True,
                    "payment_intent_id": payment_intent,
                }
            },
        )

    logger.info("Payment action required for subscription: %s", subscription_id)


async def handle_invoice_upcoming(invoice: dict[str, Any]) -> None:
    """Handle upcoming invoice event.

    Args:
        invoice: Stripe invoice object
    """
    customer_id = invoice.get("customer")
    subscription_id = invoice.get("subscription")
    amount_due = invoice.get("amount_due", 0) / 100
    period_end = invoice.get("period_end")

    user_or_org, is_organization = await find_user_for_subscription(
        subscription_id=subscription_id,
        customer_id=customer_id,
    )

    if not user_or_org:
        logger.warning("User/org not found for upcoming invoice: %s", subscription_id)
        return

    logger.info(
        "Upcoming invoice for subscription: %s, amount: $%.2f, period_end: %s",
        subscription_id,
        amount_due,
        period_end,
    )


def determine_plan_from_price_id(price_id: str | None) -> str | None:
    """Determine plan ID from Stripe price ID.

    Checks current plan price IDs first, then falls back to legacy price ID mappings
    configured via STRIPE_LEGACY_PRICE_MAPPINGS environment variable.

    Args:
        price_id: Stripe price ID

    Returns:
        Plan ID or None
    """
    import os
    import json

    if not price_id:
        return None

    from api.services.plan_service import plan_service

    # Check current plan price IDs
    for plan in plan_service.list_plans():
        if plan.stripe_monthly_price_id == price_id or plan.stripe_annual_price_id == price_id:
            logger.debug("Price ID %s matched plan: %s", price_id, plan.plan_id)
            return plan.plan_id

    # Check legacy price ID mappings from environment
    # Format: {"price_xxx": "professional", "price_yyy": "team"}
    legacy_mappings_str = os.environ.get("STRIPE_LEGACY_PRICE_MAPPINGS", "")
    if legacy_mappings_str:
        try:
            legacy_mappings = json.loads(legacy_mappings_str)
            if price_id in legacy_mappings:
                plan_id = legacy_mappings[price_id]
                logger.info("Price ID %s matched via legacy mapping to plan: %s", price_id, plan_id)
                return plan_id
        except json.JSONDecodeError:
            logger.error("Failed to parse STRIPE_LEGACY_PRICE_MAPPINGS: %s", legacy_mappings_str)

    # Log detailed info to help identify unmapped price IDs
    logger.warning(
        "Price ID %s not found in any plan. Current price mappings: %s",
        price_id,
        {
            plan.plan_id: {
                "monthly": plan.stripe_monthly_price_id,
                "annual": plan.stripe_annual_price_id,
            }
            for plan in plan_service.list_plans()
        }
    )
    return None


def validate_and_get_plan_id(plan_id: str | None) -> str:
    """Validate plan ID and return valid plan or default to professional.

    Args:
        plan_id: Plan ID to validate

    Returns:
        Valid plan ID (professional if plan_id is invalid)
    """
    if not plan_id:
        return "professional"

    from api.services.plan_service import plan_service

    plan = plan_service.get_plan(plan_id)
    if not plan:
        logger.warning("Invalid plan_id: %s, defaulting to professional", plan_id)
        return "professional"

    return plan_id


def validate_plan_change(
    current_plan: str,
    new_plan: str,
    subscription_status: str
) -> tuple[str, bool]:
    """Validate plan change and return allowed plan.

    Allows upgrades immediately and downgrades (with usage validation).

    Args:
        current_plan: Current plan ID
        new_plan: New plan ID to change to
        subscription_status: Current subscription status

    Returns:
        (allowed_plan, is_upgrade)
    """
    plan_hierarchy = {
        "professional": 1,
        "team": 2,
        "enterprise": 3
    }
    
    current_level = plan_hierarchy.get(current_plan, 0)
    new_level = plan_hierarchy.get(new_plan, 0)
    is_upgrade = new_level > current_level
    
    if subscription_status in ("canceled", "past_due", "incomplete_expired"):
        return new_plan, is_upgrade
    
    if new_level < current_level:
        logger.info(
            "Plan downgrade requested: current=%s (%d), new=%s (%d), status=%s",
            current_plan, current_level, new_plan, new_level, subscription_status
        )
        return new_plan, False
    
    return new_plan, is_upgrade

