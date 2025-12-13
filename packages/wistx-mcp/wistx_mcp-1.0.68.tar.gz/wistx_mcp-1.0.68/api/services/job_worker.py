"""Background worker for processing indexing jobs from queue."""

import asyncio
import logging
from typing import Optional

from api.models.indexing import JobStatus
from api.services.indexing_service import indexing_service
from api.services.job_queue_service import job_queue_service

logger = logging.getLogger(__name__)


class JobWorker:
    """Background worker for processing indexing jobs."""

    def __init__(self, worker_id: str = "worker-1", poll_interval: float = 5.0):
        """Initialize job worker.

        Args:
            worker_id: Unique worker identifier
            poll_interval: Seconds between queue polls
        """
        self.worker_id = worker_id
        self.poll_interval = poll_interval
        self.running = False
        self._task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        """Start the worker."""
        if self.running:
            logger.warning("Worker %s is already running", self.worker_id)
            return

        self.running = True
        self._task = asyncio.create_task(self._run())
        logger.info("Started job worker: %s", self.worker_id)

    async def stop(self) -> None:
        """Stop the worker."""
        self.running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Stopped job worker: %s", self.worker_id)

    async def _run(self) -> None:
        """Main worker loop."""
        await job_queue_service.recover_stale_jobs(stale_threshold_minutes=30)

        while self.running:
            try:
                job = await job_queue_service.dequeue_job()
                if job:
                    await self._process_job(job)
                else:
                    await asyncio.sleep(self.poll_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Error in worker loop: %s", e, exc_info=True)
                await asyncio.sleep(self.poll_interval)

    async def _process_job(self, job) -> None:
        """Process a single job.

        Args:
            job: IndexingJob to process
        """
        logger.info("Processing job: %s (resource: %s)", job.job_id, job.resource_id)

        try:
            resource = await indexing_service.get_resource(job.resource_id, job.user_id)
            if not resource:
                await job_queue_service.update_job_status(
                    job.job_id,
                    JobStatus.FAILED,
                    error_message="Resource not found",
                )
                return

            await indexing_service._run_indexing_job(
                resource_id=job.resource_id,
                resource=resource,
                user_id=job.user_id,
                plan=job.plan,
                job_id=job.job_id,
            )

            await job_queue_service.update_job_status(
                job.job_id,
                JobStatus.COMPLETED,
                progress=100.0,
            )

            logger.info("Completed job: %s", job.job_id)

        except Exception as e:
            logger.error("Job %s failed: %s", job.job_id, e, exc_info=True)

            should_retry = await job_queue_service.retry_job(job.job_id)
            if not should_retry:
                await job_queue_service.update_job_status(
                    job.job_id,
                    JobStatus.FAILED,
                    error_message=str(e),
                    error_details={"error_type": type(e).__name__},
                )


job_worker = JobWorker()

