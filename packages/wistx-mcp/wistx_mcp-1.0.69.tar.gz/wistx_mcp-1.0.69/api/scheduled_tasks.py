"""Scheduled tasks for budget monitoring and spending sync."""

import asyncio
import logging
from datetime import datetime, timedelta

from api.services.budget_monitor import budget_monitor
from api.services.spending_tracker import spending_tracker

logger = logging.getLogger(__name__)


async def run_budget_monitoring() -> None:
    """Run budget monitoring check.

    This should be scheduled to run periodically (e.g., every hour).
    """
    try:
        results = await budget_monitor.check_all_budgets()
        logger.info(
            "Budget monitoring completed: %d budgets checked, %d alerts sent",
            results["checked"],
            results.get("alerts_sent", 0),
        )
    except Exception as e:
        logger.error("Error running budget monitoring: %s", e, exc_info=True)


async def run_spending_sync() -> None:
    """Sync spending from cloud provider billing APIs.

    NOTE: This is a placeholder - cloud billing API integration is not yet implemented.
    The system currently relies on agent reporting for spending tracking.

    This should be scheduled to run periodically (e.g., daily) once cloud billing
    API integration is implemented.
    """
    logger.info("Spending sync scheduled task called (placeholder - not yet implemented)")
    logger.info(
        "Cloud billing API integration requires customer cloud provider credentials. "
        "Currently, spending tracking relies on agent reporting via spending_tracker.track_infrastructure_creation()"
    )
    
    try:
        from api.database.mongodb import mongodb_manager

        db = mongodb_manager.get_database()
        users_collection = db.users

        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=1)

        users = users_collection.find({})

        synced_count = 0
        for user in users:
            user_id = str(user["_id"])

            cloud_providers = user.get("cloud_providers", ["aws"])
            for provider in cloud_providers:
                try:
                    result = await spending_tracker.sync_cloud_spending(
                        user_id=user_id,
                        cloud_provider=provider,
                        start_date=start_date,
                        end_date=end_date,
                    )
                    synced_count += result.get("synced", 0)
                except Exception as e:
                    logger.debug(
                        "Cloud billing sync not implemented for %s (user %s): %s",
                        provider,
                        user_id,
                        e,
                    )

        if synced_count == 0:
            logger.info(
                "Spending sync completed: 0 records synced (cloud billing API integration not yet implemented)"
            )
        else:
            logger.info("Spending sync completed: %d records synced", synced_count)
    except Exception as e:
        logger.error("Error running spending sync: %s", e, exc_info=True)


if __name__ == "__main__":
    asyncio.run(run_budget_monitoring())

