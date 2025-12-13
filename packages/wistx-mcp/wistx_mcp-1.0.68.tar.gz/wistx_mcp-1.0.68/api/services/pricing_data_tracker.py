"""Pricing data tracker - tracks missing pricing data for continuous improvement."""

import logging
from datetime import datetime
from typing import Any

from api.database.mongodb import mongodb_manager

logger = logging.getLogger(__name__)


class PricingDataTracker:
    """Track missing pricing data for continuous improvement."""

    async def track_missing_pricing(
        self,
        resource_spec: dict[str, Any],
        context: dict[str, Any],
    ) -> None:
        """Track resource without pricing data.
        
        Args:
            resource_spec: Resource specification
            context: Analysis context (file, repo, etc.)
        """
        db = mongodb_manager.get_database()
        collection = db.missing_pricing_data
        
        missing_record = {
            "resource_spec": resource_spec,
            "context": context,
            "first_seen": datetime.utcnow(),
            "last_seen": datetime.utcnow(),
            "occurrence_count": 1,
            "status": "pending",
        }
        
        cloud = resource_spec.get("cloud", "")
        service = resource_spec.get("service", "")
        instance_type = resource_spec.get("instance_type", "")
        
        existing = collection.find_one({
            "resource_spec.cloud": cloud,
            "resource_spec.service": service,
            "resource_spec.instance_type": instance_type,
        })
        
        if existing:
            collection.update_one(
                {"_id": existing["_id"]},
                {
                    "$inc": {"occurrence_count": 1},
                    "$set": {"last_seen": datetime.utcnow()},
                }
            )
            logger.info(
                "Updated missing pricing data: %s/%s/%s (count: %d)",
                cloud,
                service,
                instance_type,
                existing["occurrence_count"] + 1,
            )
        else:
            collection.insert_one(missing_record)
            logger.info(
                "Tracked missing pricing data: %s/%s/%s",
                cloud,
                service,
                instance_type,
            )

    async def get_missing_pricing_data(
        self,
        limit: int = 100,
        status: str = "pending",
    ) -> list[dict[str, Any]]:
        """Get missing pricing data for admin review.
        
        Args:
            limit: Maximum number of records to return
            status: Filter by status (pending, in_progress, resolved)
            
        Returns:
            List of missing pricing records
        """
        db = mongodb_manager.get_database()
        collection = db.missing_pricing_data
        
        missing = list(
            collection.find({"status": status})
            .sort("occurrence_count", -1)
            .limit(limit)
        )
        
        return missing

    async def mark_as_resolved(
        self,
        cloud: str,
        service: str,
        instance_type: str,
    ) -> bool:
        """Mark missing pricing data as resolved.
        
        Args:
            cloud: Cloud provider
            service: Service name
            instance_type: Instance type
            
        Returns:
            True if updated, False if not found
        """
        db = mongodb_manager.get_database()
        collection = db.missing_pricing_data
        
        result = collection.update_many(
            {
                "resource_spec.cloud": cloud,
                "resource_spec.service": service,
                "resource_spec.instance_type": instance_type,
                "status": "pending",
            },
            {
                "$set": {
                    "status": "resolved",
                    "resolved_at": datetime.utcnow(),
                }
            }
        )
        
        return result.modified_count > 0


pricing_data_tracker = PricingDataTracker()

