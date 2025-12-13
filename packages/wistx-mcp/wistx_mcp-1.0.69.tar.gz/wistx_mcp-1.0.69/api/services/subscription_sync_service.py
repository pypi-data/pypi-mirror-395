"""Background service for syncing subscriptions from Stripe."""

import logging
from datetime import datetime
from typing import Optional

from api.database.mongodb import mongodb_manager
from api.services.billing_service import billing_service
from api.services.subscription_cache_service import SubscriptionCacheService
from api.utils.subscription_sync import sync_subscription_from_stripe
from bson import ObjectId

logger = logging.getLogger(__name__)


class SubscriptionSyncService:
    """Service for background subscription synchronization."""

    @staticmethod
    async def sync_user_subscription(
        user_id: str, force: bool = False
    ) -> Optional[dict]:
        """Sync user subscription from Stripe.

        Args:
            user_id: User ID
            force: Force sync even if cache is valid

        Returns:
            Sync result or None
        """
        if not force:
            cached = await SubscriptionCacheService.get_cached_subscription(user_id)
            if cached:
                logger.debug("Using cached subscription for user: %s", user_id)
                return cached

        db = mongodb_manager.get_database()
        user = db.users.find_one({"_id": ObjectId(user_id)})

        if not user:
            logger.warning("User not found for sync: %s", user_id)
            return None

        try:
            sync_result = await sync_subscription_from_stripe(user_id, user, force=True)

            if sync_result:
                await SubscriptionCacheService.set_cached_subscription(
                    user_id, sync_result
                )
                return sync_result

            return None

        except Exception as e:
            logger.error(
                "Failed to sync subscription for user %s: %s", user_id, e, exc_info=True
            )
            return None

    @staticmethod
    async def sync_all_active_subscriptions(limit: int = 100) -> dict:
        """Sync all active subscriptions (for background job).

        Args:
            limit: Maximum number of subscriptions to sync

        Returns:
            Sync statistics
        """
        db = mongodb_manager.get_database()

        users = list(
            db.users.find(
                {
                    "stripe_customer_id": {"$exists": True, "$ne": None},
                    "subscription_status": {"$in": ["active", "trialing", "past_due"]},
                }
            ).limit(limit)
        )

        synced = 0
        failed = 0

        for user in users:
            try:
                result = await SubscriptionSyncService.sync_user_subscription(
                    str(user["_id"]), force=False
                )
                if result:
                    synced += 1
                else:
                    failed += 1
            except Exception as e:
                logger.error(
                    "Failed to sync subscription for user %s: %s", user["_id"], e
                )
                failed += 1

        return {"synced": synced, "failed": failed, "total": len(users)}

