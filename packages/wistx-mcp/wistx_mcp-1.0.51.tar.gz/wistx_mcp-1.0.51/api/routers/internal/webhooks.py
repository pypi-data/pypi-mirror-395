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

    if not event_id:
        logger.error("Stripe webhook event missing ID")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid webhook event: missing ID",
        )

    from api.database.mongodb import mongodb_manager
    from datetime import datetime, timedelta

    db = mongodb_manager.get_database()
    webhook_collection = db.webhook_events
    
    existing_event = webhook_collection.find_one({"event_id": event_id, "source": "stripe"})
    if existing_event:
        logger.warning("Duplicate Stripe webhook event detected: %s", event_id)
        return {"status": "success", "message": "Event already processed"}
    
    webhook_collection.insert_one({
        "event_id": event_id,
        "source": "stripe",
        "event_type": event_type,
        "processed_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(days=1),
    })

    logger.info("Received Stripe webhook: %s [event_id=%s]", event_type, event_id)

    try:
        if event_type == "customer.subscription.created":
            await handle_subscription_created(event_data)
        elif event_type == "customer.subscription.updated":
            await handle_subscription_updated(event_data)
        elif event_type == "customer.subscription.deleted":
            await handle_subscription_deleted(event_data)
        elif event_type == "invoice.payment_succeeded":
            await handle_payment_succeeded(event_data)
        elif event_type == "invoice.payment_failed":
            await handle_payment_failed(event_data)
        elif event_type == "checkout.session.completed":
            await handle_checkout_completed(event_data)
        else:
            logger.info("Unhandled event type: %s", event_type)

        return {"status": "success"}
    except Exception as e:
        logger.error("Error handling webhook event: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Webhook processing failed",
        ) from e


async def handle_subscription_created(subscription: dict[str, Any]) -> None:
    """Handle subscription created event.

    Args:
        subscription: Stripe subscription object
    """
    customer_id = subscription.get("customer")
    subscription_id = subscription.get("id")
    status_value = subscription.get("status")

    from api.database.mongodb import mongodb_manager
    from api.services.billing_service import billing_service

    db = mongodb_manager.get_database()

    org_doc = db.organizations.find_one({"stripe_customer_id": customer_id})
    if org_doc:
        await handle_organization_subscription_created(subscription, org_doc)
        return

    user_doc = db.users.find_one({"stripe_customer_id": customer_id})
    if not user_doc:
        logger.warning("User or organization not found for customer: %s", customer_id)
        return

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

    from bson import ObjectId
    from datetime import datetime

    price_id = subscription.get("items", {}).get("data", [{}])[0].get("price", {}).get("id")
    plan_id = determine_plan_from_price_id(price_id)
    validated_plan_id = validate_and_get_plan_id(plan_id)

    current_plan = user_doc.get("plan", "professional")
    plan_hierarchy = {
        "professional": 1,
        "team": 2,
        "enterprise": 3,
    }
    current_level = plan_hierarchy.get(current_plan, 0)
    new_level = plan_hierarchy.get(validated_plan_id, 0)
    
    if new_level < current_level and status_value != "canceled":
        logger.warning("Attempted plan downgrade via webhook: user=%s, current=%s, attempted=%s", 
                     user_doc["_id"], current_plan, validated_plan_id)
        validated_plan_id = current_plan

    db.users.update_one(
        {"_id": user_doc["_id"]},
        {
            "$set": {
                "stripe_subscription_id": subscription_id,
                "subscription_status": status_value,
                "plan": validated_plan_id,
                "subscription_start": datetime.utcfromtimestamp(subscription.get("current_period_start", 0)),
                "subscription_renews_at": datetime.utcfromtimestamp(subscription.get("current_period_end", 0)),
            }
        },
    )

    logger.info("Updated user %s subscription: %s, plan: %s", user_doc["_id"], subscription_id, validated_plan_id)


async def handle_subscription_updated(subscription: dict[str, Any]) -> None:
    """Handle subscription updated event.

    Args:
        subscription: Stripe subscription object
    """
    customer_id = subscription.get("customer")
    subscription_id = subscription.get("id")
    status_value = subscription.get("status")

    from api.database.mongodb import mongodb_manager
    from api.services.billing_service import billing_service
    from bson import ObjectId
    from datetime import datetime

    db = mongodb_manager.get_database()

    org_doc = db.organizations.find_one({"stripe_subscription_id": subscription_id})
    if org_doc:
        await handle_organization_subscription_updated(subscription, org_doc)
        return

    user_doc = db.users.find_one({"stripe_subscription_id": subscription_id})
    if not user_doc:
        logger.warning("User or organization not found for subscription: %s", subscription_id)
        return

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
    }

    validated_plan_id = None
    if plan_id:
        validated_plan_id = validate_and_get_plan_id(plan_id)
        current_plan = user_doc.get("plan", "professional")
        plan_hierarchy = {
            "professional": 1,
            "team": 2,
            "enterprise": 3,
        }
        current_level = plan_hierarchy.get(current_plan, 0)
        new_level = plan_hierarchy.get(validated_plan_id, 0)
        
        if new_level < current_level and status_value not in ("canceled", "past_due"):
            logger.warning("Attempted plan downgrade via webhook: user=%s, current=%s, attempted=%s", 
                         user_doc["_id"], current_plan, validated_plan_id)
            validated_plan_id = current_plan
        
        if validated_plan_id:
            update_data["plan"] = validated_plan_id

    db.users.update_one(
        {"_id": user_doc["_id"]},
        {"$set": update_data},
    )

    logger.info("Updated user %s subscription status: %s, plan: %s", user_doc["_id"], status_value, validated_plan_id if validated_plan_id else "unchanged")


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
        {"$set": {"subscription_status": "active"}},
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

    update_data = {
        "$set": {
            "stripe_customer_id": customer_id,
            "stripe_subscription_id": subscription_id,
            "subscription_status": "active",
            "plan": validated_plan_id,
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

    user_doc = db.users.find_one({"_id": ObjectId(user_id)})
    if user_doc and user_doc.get("subscription_status") == "inactive":
        if not user_doc.get("money_back_guarantee_start"):
            update_data["$set"]["money_back_guarantee_start"] = datetime.utcnow()
            update_data["$set"]["money_back_guarantee_end"] = datetime.utcnow() + timedelta(days=30)

    db.users.update_one(
        {"_id": ObjectId(user_id)},
        update_data,
    )

    logger.info("Checkout completed for user %s, subscription %s, plan %s", user_id, subscription_id, validated_plan_id)


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
    plan_hierarchy = {
        "professional": 1,
        "team": 2,
        "enterprise": 3,
    }
    current_level = plan_hierarchy.get(current_plan, 0)
    new_level = plan_hierarchy.get(validated_plan_id, 0)

    if new_level < current_level and status_value != "canceled":
        logger.warning(
            "Attempted plan downgrade via webhook: org=%s, current=%s, attempted=%s",
            org_doc["_id"],
            current_plan,
            validated_plan_id,
        )
        validated_plan_id = current_plan

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
        "Updated organization %s subscription: %s, plan: %s",
        org_doc["_id"],
        subscription_id,
        validated_plan_id,
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
        plan_hierarchy = {
            "professional": 1,
            "team": 2,
            "enterprise": 3,
        }
        current_level = plan_hierarchy.get(current_plan, 0)
        new_level = plan_hierarchy.get(validated_plan_id, 0)

        if new_level < current_level and status_value not in ("canceled", "past_due"):
            logger.warning(
                "Attempted plan downgrade via webhook: org=%s, current=%s, attempted=%s",
                org_doc["_id"],
                current_plan,
                validated_plan_id,
            )
            validated_plan_id = current_plan

        if validated_plan_id:
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


def determine_plan_from_price_id(price_id: str | None) -> str | None:
    """Determine plan ID from Stripe price ID.

    Args:
        price_id: Stripe price ID

    Returns:
        Plan ID or None
    """
    if not price_id:
        return None

    from api.services.plan_service import plan_service

    for plan in plan_service.list_plans():
        if plan.stripe_monthly_price_id == price_id or plan.stripe_annual_price_id == price_id:
            return plan.plan_id

    logger.warning("Price ID %s not found in any plan", price_id)
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

