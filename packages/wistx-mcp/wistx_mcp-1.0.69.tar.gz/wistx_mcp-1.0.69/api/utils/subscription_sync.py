"""Automatic subscription sync utilities."""

import logging
from datetime import datetime
from typing import Any

from api.services.billing_service import billing_service
from api.routers.internal.webhooks import determine_plan_from_price_id, validate_and_get_plan_id

logger = logging.getLogger(__name__)


def _get_plan_hierarchy_level(plan_id: str | None) -> int:
    """Get the hierarchy level of a plan (higher is better).

    Args:
        plan_id: The plan ID

    Returns:
        Hierarchy level (0 for unknown, 1 for professional, 2 for team, 3 for enterprise)
    """
    hierarchy = {
        "professional": 1,
        "team": 2,
        "enterprise": 3,
    }
    return hierarchy.get(plan_id or "", 0)


def _select_best_subscription(subscriptions: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Select the best subscription when multiple exist.

    Priority order:
    1. Active subscriptions not set to cancel at period end
    2. Among those, prefer higher tier plans (enterprise > team > professional)
    3. If all are canceling, still prefer higher tier plans
    4. Fall back to first subscription if nothing else matches

    Args:
        subscriptions: List of subscription dicts from Stripe

    Returns:
        The best subscription to use, or None if list is empty
    """
    if not subscriptions:
        return None

    active_statuses = ("active", "trialing", "past_due")

    # Separate subscriptions into categories
    active_not_canceling = []
    active_canceling = []
    other = []

    for sub in subscriptions:
        status = sub.get("status")
        cancel_at_period_end = sub.get("cancel_at_period_end", False)

        if status in active_statuses:
            if not cancel_at_period_end:
                active_not_canceling.append(sub)
            else:
                active_canceling.append(sub)
        else:
            other.append(sub)

    # Helper to pick highest tier from a list
    def pick_highest_tier(subs: list[dict[str, Any]]) -> dict[str, Any] | None:
        if not subs:
            return None

        best = subs[0]
        best_level = _get_plan_hierarchy_level(determine_plan_from_price_id(best.get("price_id")))

        for sub in subs[1:]:
            plan_id = determine_plan_from_price_id(sub.get("price_id"))
            level = _get_plan_hierarchy_level(plan_id)
            if level > best_level:
                best = sub
                best_level = level

        return best

    # Priority: active not canceling > active canceling > other
    result = pick_highest_tier(active_not_canceling)
    if result:
        logger.debug("Selected active non-canceling subscription: %s", result.get("subscription_id"))
        return result

    result = pick_highest_tier(active_canceling)
    if result:
        logger.debug("Selected active canceling subscription (no non-canceling available): %s", result.get("subscription_id"))
        return result

    result = pick_highest_tier(other)
    if result:
        logger.debug("Selected non-active subscription (no active available): %s", result.get("subscription_id"))
        return result

    # Absolute fallback
    logger.warning("No categorized subscription found, using first subscription")
    return subscriptions[0]


async def sync_subscription_from_stripe(
    user_id: str,
    user: dict[str, Any],
    force: bool = True
) -> dict[str, Any] | None:
    """Sync subscription from Stripe to database automatically.

    Always checks Stripe for latest status and updates database.
    This function is idempotent and safe to call multiple times.

    Args:
        user_id: User ID
        user: User document from database
        force: If True, always sync even if data appears unchanged

    Returns:
        Sync result with status and plan, or None if sync failed/no subscription
    """
    stripe_customer_id = user.get("stripe_customer_id")
    if not stripe_customer_id:
        return None

    try:
        customer_subscriptions = await billing_service.get_customer_subscriptions(stripe_customer_id)
    except Exception as e:
        logger.error("Failed to get customer subscriptions for sync: user=%s, error=%s", user_id, e, exc_info=True)
        return None

    if not customer_subscriptions:
        logger.debug("No subscriptions found for customer: %s", stripe_customer_id)
        return None

    # Log all subscriptions for debugging
    logger.info(
        "Found %d subscriptions for user=%s: %s",
        len(customer_subscriptions),
        user_id,
        [
            {
                "id": s.get("subscription_id"),
                "status": s.get("status"),
                "cancel_at_period_end": s.get("cancel_at_period_end"),
                "price_id": s.get("price_id"),
                "plan": determine_plan_from_price_id(s.get("price_id")),
            }
            for s in customer_subscriptions
        ]
    )

    # Select the best subscription using smart logic
    active_subscription = _select_best_subscription(customer_subscriptions)

    subscription_id = active_subscription.get("subscription_id")
    stripe_status = active_subscription.get("status")

    try:
        subscription_data = await billing_service.get_subscription(subscription_id)
    except Exception as e:
        logger.error("Failed to get subscription details for sync: subscription_id=%s, error=%s", subscription_id, e, exc_info=True)
        return None

    price_id = subscription_data.get("price_id")
    plan_id = determine_plan_from_price_id(price_id)
    validated_plan_id = validate_and_get_plan_id(plan_id)

    db_status = user.get("subscription_status")
    db_plan = user.get("plan", "professional")
    db_subscription_id = user.get("stripe_subscription_id")

    needs_sync = force or (
        stripe_status != db_status or
        validated_plan_id != db_plan or
        subscription_id != db_subscription_id
    )

    if not needs_sync and not force:
        logger.debug("Subscription already in sync: user=%s", user_id)
        return {
            "subscription_id": subscription_id,
            "status": stripe_status,
            "plan": validated_plan_id,
            "synced": False,
        }

    from api.database.mongodb import mongodb_manager
    from bson import ObjectId

    db = mongodb_manager.get_database()

    update_data = {
        "stripe_subscription_id": subscription_id,
        "subscription_status": stripe_status,
        "plan": validated_plan_id,
        "is_active": stripe_status in ("active", "trialing"),
    }
    
    current_period_start = subscription_data.get("current_period_start")
    current_period_end = subscription_data.get("current_period_end")
    
    if current_period_start:
        update_data["subscription_start"] = datetime.utcfromtimestamp(current_period_start) if isinstance(current_period_start, (int, float)) else current_period_start
    
    if current_period_end:
        update_data["subscription_renews_at"] = datetime.utcfromtimestamp(current_period_end) if isinstance(current_period_end, (int, float)) else current_period_end

    result = db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )

    # Always invalidate cache after sync to ensure fresh data
    try:
        from api.services.subscription_cache_service import SubscriptionCacheService
        await SubscriptionCacheService.invalidate_cache(user_id)
        logger.debug("Cache invalidated after sync: user=%s", user_id)
    except Exception as e:
        logger.warning("Failed to invalidate cache after sync: user=%s, error=%s", user_id, e)

    if result.modified_count > 0:
        logger.info(
            "Auto-synced subscription: user=%s, status=%s, plan=%s (was %s), subscription_id=%s",
            user_id,
            stripe_status,
            validated_plan_id,
            db_plan,
            subscription_id,
        )
    else:
        logger.debug("Sync completed but no changes made: user=%s", user_id)

    return {
        "subscription_id": subscription_id,
        "status": stripe_status,
        "plan": validated_plan_id,
        "current_period_start": subscription_data.get("current_period_start"),
        "current_period_end": subscription_data.get("current_period_end"),
        "cancel_at_period_end": subscription_data.get("cancel_at_period_end", False),
        "synced": True,
    }

