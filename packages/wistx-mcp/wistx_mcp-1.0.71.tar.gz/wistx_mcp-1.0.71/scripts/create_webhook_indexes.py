"""Create indexes for webhook processing."""

import logging
from api.database.mongodb import mongodb_manager

logger = logging.getLogger(__name__)


def create_webhook_indexes():
    """Create indexes for webhook processing."""
    db = mongodb_manager.get_database()

    try:
        webhook_events = db.webhook_events

        webhook_events.create_index(
            [("event_id", 1), ("source", 1)],
            unique=True,
            name="event_id_source_unique",
        )
        logger.info("Created index: event_id_source_unique")

        webhook_events.create_index(
            [("stripe_created_at", 1)],
            name="stripe_created_at_idx",
        )
        logger.info("Created index: stripe_created_at_idx")

        webhook_events.create_index(
            [("processing_status", 1), ("stripe_created_at", 1)],
            name="pending_events_idx",
        )
        logger.info("Created index: pending_events_idx")

        webhook_events.create_index(
            [("expires_at", 1)],
            expireAfterSeconds=0,
            name="expires_at_ttl",
        )
        logger.info("Created TTL index: expires_at_ttl")

        webhook_locks = db.webhook_locks

        webhook_locks.create_index(
            [("lock_key", 1)],
            unique=True,
            name="lock_key_unique",
        )
        logger.info("Created index: lock_key_unique")

        webhook_locks.create_index(
            [("expires_at", 1)],
            expireAfterSeconds=0,
            name="lock_expires_at_ttl",
        )
        logger.info("Created TTL index: lock_expires_at_ttl")

        subscription_cache = db.subscription_cache

        subscription_cache.create_index(
            [("cache_key", 1)],
            unique=True,
            name="cache_key_unique",
        )
        logger.info("Created index: cache_key_unique")

        subscription_cache.create_index(
            [("expires_at", 1)],
            expireAfterSeconds=0,
            name="cache_expires_at_ttl",
        )
        logger.info("Created TTL index: cache_expires_at_ttl")

        subscription_cache.create_index(
            [("user_id", 1)],
            name="user_id_idx",
        )
        logger.info("Created index: user_id_idx")

        logger.info("All webhook indexes created successfully")

    except Exception as e:
        logger.error("Error creating webhook indexes: %s", e, exc_info=True)
        raise


if __name__ == "__main__":
    create_webhook_indexes()

