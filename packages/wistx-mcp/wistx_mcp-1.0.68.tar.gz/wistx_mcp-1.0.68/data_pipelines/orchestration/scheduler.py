"""Pipeline scheduler for automated runs."""

import asyncio
import schedule
import time
from datetime import datetime

from data_pipelines.orchestration.daily_pipeline import run_daily_pipeline
from data_pipelines.orchestration.weekly_pipeline import run_weekly_pipeline
from data_pipelines.utils.logger import setup_logger

logger = setup_logger(__name__)


def schedule_daily_pipeline():
    """Schedule daily pipeline runs."""
    schedule.every().day.at("02:00").do(lambda: asyncio.run(run_daily_pipeline()))
    logger.info("Scheduled daily pipeline at 02:00 UTC")


def schedule_weekly_pipeline():
    """Schedule weekly pipeline runs."""
    schedule.every().sunday.at("03:00").do(lambda: asyncio.run(run_weekly_pipeline()))
    logger.info("Scheduled weekly pipeline every Sunday at 03:00 UTC")


def run_scheduler():
    """Run the scheduler loop."""
    schedule_daily_pipeline()
    schedule_weekly_pipeline()
    
    logger.info("Pipeline scheduler started at %s", datetime.utcnow().isoformat())
    
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    run_scheduler()
