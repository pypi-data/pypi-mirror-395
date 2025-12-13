"""Distributed locking service for webhook event processing.

Uses MongoDB with TTL indexes for automatic lock expiration.
This prevents race conditions when processing webhook events concurrently.
"""

import logging
from datetime import datetime, timedelta
from typing import Optional

from api.database.mongodb import mongodb_manager

logger = logging.getLogger(__name__)


class WebhookLockService:
    """Service for managing distributed locks for webhook events."""

    LOCK_TTL_SECONDS = 300

    @staticmethod
    def acquire_lock(event_id: str, source: str = "stripe") -> bool:
        """Acquire lock for webhook event processing.

        Args:
            event_id: Stripe event ID
            source: Event source (stripe, etc.)

        Returns:
            True if lock acquired, False if already locked
        """
        db = mongodb_manager.get_database()
        locks_collection = db.webhook_locks

        lock_key = f"{source}:{event_id}"
        now = datetime.utcnow()
        expires_at = now + timedelta(seconds=WebhookLockService.LOCK_TTL_SECONDS)

        try:
            result = locks_collection.insert_one(
                {
                    "lock_key": lock_key,
                    "event_id": event_id,
                    "source": source,
                    "acquired_at": now,
                    "expires_at": expires_at,
                }
            )
            return result.inserted_id is not None
        except Exception as e:
            logger.warning("Failed to acquire lock (likely already locked): %s", e)
            return False

    @staticmethod
    def release_lock(event_id: str, source: str = "stripe") -> None:
        """Release lock for webhook event.

        Args:
            event_id: Stripe event ID
            source: Event source
        """
        db = mongodb_manager.get_database()
        locks_collection = db.webhook_locks

        lock_key = f"{source}:{event_id}"
        locks_collection.delete_one({"lock_key": lock_key})

    @staticmethod
    def cleanup_expired_locks() -> int:
        """Clean up expired locks (should be called periodically).

        Returns:
            Number of locks cleaned up
        """
        db = mongodb_manager.get_database()
        locks_collection = db.webhook_locks

        now = datetime.utcnow()
        result = locks_collection.delete_many({"expires_at": {"$lt": now}})
        return result.deleted_count

