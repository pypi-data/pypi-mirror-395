"""Webhook event storage with ordering and deduplication."""

import logging
from datetime import datetime, timedelta
from typing import Optional

from api.database.mongodb import mongodb_manager

logger = logging.getLogger(__name__)


class WebhookEventStore:
    """Store for webhook events with ordering and deduplication."""

    @staticmethod
    def store_event(
        event_id: str,
        event_type: str,
        source: str,
        event_data: dict,
        created_at: int,
    ) -> bool:
        """Store webhook event with ordering information.

        Args:
            event_id: Stripe event ID
            event_type: Event type (e.g., customer.subscription.created)
            source: Event source (stripe)
            event_data: Event data object
            created_at: Unix timestamp when event was created

        Returns:
            True if event stored, False if duplicate
        """
        db = mongodb_manager.get_database()
        events_collection = db.webhook_events

        existing = events_collection.find_one({"event_id": event_id, "source": source})
        if existing:
            logger.debug("Event already stored: %s", event_id)
            return False

        events_collection.insert_one(
            {
                "event_id": event_id,
                "source": source,
                "event_type": event_type,
                "event_data": event_data,
                "created_at": datetime.utcfromtimestamp(created_at),
                "stripe_created_at": created_at,
                "processed_at": None,
                "processing_status": "pending",
                "stored_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(days=90),
            }
        )

        return True

    @staticmethod
    def mark_event_processed(event_id: str, source: str, success: bool) -> None:
        """Mark event as processed.

        Args:
            event_id: Stripe event ID
            source: Event source
            success: Whether processing was successful
        """
        db = mongodb_manager.get_database()
        events_collection = db.webhook_events

        events_collection.update_one(
            {"event_id": event_id, "source": source},
            {
                "$set": {
                    "processed_at": datetime.utcnow(),
                    "processing_status": "completed" if success else "failed",
                }
            },
        )

    @staticmethod
    def get_pending_events_for_subscription(
        subscription_id: str,
        limit: int = 10,
    ) -> list[dict]:
        """Get pending events for a subscription, ordered by creation time.

        Args:
            subscription_id: Stripe subscription ID
            limit: Maximum number of events

        Returns:
            List of events ordered by creation time
        """
        db = mongodb_manager.get_database()
        events_collection = db.webhook_events

        events = list(
            events_collection.find(
                {
                    "event_data.subscription": subscription_id,
                    "processing_status": "pending",
                }
            )
            .sort("stripe_created_at", 1)
            .limit(limit)
        )

        return events

