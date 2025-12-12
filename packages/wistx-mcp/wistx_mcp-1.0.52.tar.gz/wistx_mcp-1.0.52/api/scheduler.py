"""Scheduler configuration for scheduled tasks."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def setup_scheduler() -> Any:
    """Setup and configure scheduler for scheduled tasks.

    Returns:
        Scheduler instance (APScheduler or None if not available)
    """
    try:
        from apscheduler.schedulers.asyncio import AsyncIOScheduler
        from api.scheduled_tasks import run_budget_monitoring, run_spending_sync

        scheduler = AsyncIOScheduler()

        scheduler.add_job(
            run_budget_monitoring,
            "interval",
            hours=1,
            id="budget_monitoring",
            name="Budget Monitoring",
            replace_existing=True,
        )

        scheduler.add_job(
            run_spending_sync,
            "cron",
            hour=2,
            minute=0,
            id="spending_sync",
            name="Spending Sync",
            replace_existing=True,
        )

        logger.info("Scheduler configured: budget monitoring (hourly), spending sync (daily at 2 AM)")
        return scheduler
    except ImportError:
        logger.warning(
            "APScheduler not installed. Scheduled tasks will not run. "
            "Install with: pip install apscheduler"
        )
        return None

