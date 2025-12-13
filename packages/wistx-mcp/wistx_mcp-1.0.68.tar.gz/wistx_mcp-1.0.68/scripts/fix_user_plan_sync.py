"""Script to manually sync user subscription and fix plan mismatch.

This script:
1. Fetches subscription from Stripe
2. Determines correct plan from price_id
3. Updates user document in MongoDB
4. Clears subscription cache
"""

import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from api.database.mongodb import mongodb_manager
from api.services.billing_service import billing_service
from api.services.subscription_cache_service import SubscriptionCacheService
from api.routers.internal.webhooks import determine_plan_from_price_id, validate_and_get_plan_id
from api.utils.subscription_sync import sync_subscription_from_stripe
from bson import ObjectId

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def fix_user_plan(user_id: str) -> None:
    """Fix user plan by syncing from Stripe.
    
    Args:
        user_id: User ID to fix
    """
    db = mongodb_manager.get_database()
    user = db.users.find_one({"_id": ObjectId(user_id)})
    
    if not user:
        logger.error("User not found: %s", user_id)
        return
    
    logger.info("Current user state:")
    logger.info("  Plan: %s", user.get("plan"))
    logger.info("  Subscription ID: %s", user.get("stripe_subscription_id"))
    logger.info("  Subscription Status: %s", user.get("subscription_status"))
    logger.info("  Customer ID: %s", user.get("stripe_customer_id"))
    
    stripe_customer_id = user.get("stripe_customer_id")
    if not stripe_customer_id:
        logger.error("User has no Stripe customer ID")
        return
    
    try:
        customer_subscriptions = await billing_service.get_customer_subscriptions(stripe_customer_id)
        logger.info("Found %d subscriptions for customer", len(customer_subscriptions))
        
        for sub in customer_subscriptions:
            logger.info("  Subscription: %s, Status: %s", sub.get("subscription_id"), sub.get("status"))
        
        active_subscription = next(
            (s for s in customer_subscriptions if s.get("status") in ("active", "trialing", "past_due")),
            customer_subscriptions[0] if customer_subscriptions else None
        )
        
        if not active_subscription:
            logger.error("No active subscription found")
            return
        
        subscription_id = active_subscription.get("subscription_id")
        logger.info("Using subscription: %s (status: %s)", subscription_id, active_subscription.get("status"))
        
        subscription_data = await billing_service.get_subscription(subscription_id)
        price_id = subscription_data.get("price_id")
        logger.info("Price ID from Stripe: %s", price_id)
        
        plan_id = determine_plan_from_price_id(price_id)
        validated_plan_id = validate_and_get_plan_id(plan_id)
        logger.info("Determined plan: %s (validated: %s)", plan_id, validated_plan_id)
        
        logger.info("Syncing subscription...")
        sync_result = await sync_subscription_from_stripe(user_id, user, force=True)
        
        if sync_result:
            logger.info("Sync successful!")
            logger.info("  Plan: %s", sync_result.get("plan"))
            logger.info("  Status: %s", sync_result.get("status"))
            logger.info("  Subscription ID: %s", sync_result.get("subscription_id"))
            
            await SubscriptionCacheService.invalidate_cache(user_id)
            logger.info("Cache invalidated")
            
            updated_user = db.users.find_one({"_id": ObjectId(user_id)})
            logger.info("Updated user state:")
            logger.info("  Plan: %s", updated_user.get("plan"))
            logger.info("  Subscription ID: %s", updated_user.get("stripe_subscription_id"))
            logger.info("  Subscription Status: %s", updated_user.get("subscription_status"))
        else:
            logger.error("Sync failed or returned None")
            
    except Exception as e:
        logger.error("Error fixing user plan: %s", e, exc_info=True)


if __name__ == "__main__":
    user_id = "693260123c4f18252fa7af3d"
    asyncio.run(fix_user_plan(user_id))

