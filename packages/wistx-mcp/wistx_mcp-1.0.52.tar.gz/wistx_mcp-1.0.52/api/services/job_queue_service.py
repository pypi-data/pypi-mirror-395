"""Job queue service for persistent indexing job management."""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Optional

from bson import ObjectId

from api.database.mongodb import mongodb_manager
from api.models.indexing import IndexingJob, JobStatus, generate_job_id

logger = logging.getLogger(__name__)


class JobQueueService:
    """Service for managing indexing job queue."""

    def __init__(self):
        """Initialize job queue service."""
        self._db = None

    def _get_db(self):
        """Get MongoDB database instance."""
        if self._db is None:
            self._db = mongodb_manager.get_database()
        return self._db

    async def enqueue_job(
        self,
        resource_id: str,
        user_id: str,
        job_type: str,
        plan: str = "professional",
        organization_id: Optional[str] = None,
        max_retries: int = 3,
    ) -> IndexingJob:
        """Enqueue a new indexing job.

        Args:
            resource_id: Resource ID to index
            user_id: User ID who owns the job
            job_type: Type of job (repository, documentation, document)
            plan: User's plan (affects priority)
            organization_id: Organization ID (optional)
            max_retries: Maximum retry attempts

        Returns:
            Created IndexingJob
        """
        job_id = generate_job_id()

        priority_map = {
            "professional": 1,
            "team": 5,
            "enterprise": 10,
        }
        priority = priority_map.get(plan.lower(), 1)

        job = IndexingJob(
            job_id=job_id,
            resource_id=resource_id,
            user_id=user_id,
            organization_id=organization_id,
            status=JobStatus.PENDING,
            priority=priority,
            job_type=job_type,
            plan=plan,
            max_retries=max_retries,
        )

        db = self._get_db()
        collection = db.indexing_jobs

        job_dict = job.to_dict()
        collection.insert_one(job_dict)

        logger.info(
            "Enqueued indexing job: %s (resource: %s, type: %s, priority: %d)",
            job_id,
            resource_id,
            job_type,
            priority,
        )

        return job

    async def dequeue_job(self) -> Optional[IndexingJob]:
        """Dequeue next pending job (by priority).

        Returns:
            Next IndexingJob to process, or None if no jobs available
        """
        db = self._get_db()
        collection = db.indexing_jobs

        job_doc = collection.find_one_and_update(
            {
                "status": JobStatus.PENDING,
            },
            {
                "$set": {
                    "status": JobStatus.RUNNING,
                    "started_at": datetime.utcnow(),
                }
            },
            sort=[("priority", -1), ("created_at", 1)],
        )

        if not job_doc:
            return None

        return IndexingJob.from_dict(job_doc)

    async def update_job_status(
        self,
        job_id: str,
        status: JobStatus,
        progress: Optional[float] = None,
        error_message: Optional[str] = None,
        error_details: Optional[dict[str, Any]] = None,
    ) -> None:
        """Update job status and progress.

        Args:
            job_id: Job ID
            status: New status
            progress: Progress percentage (0-100)
            error_message: Error message (if failed)
            error_details: Error details
        """
        db = self._get_db()
        collection = db.indexing_jobs

        update: dict[str, Any] = {}

        if status == JobStatus.COMPLETED:
            update["completed_at"] = datetime.utcnow()
        elif status == JobStatus.FAILED:
            update["error_message"] = error_message
            update["error_details"] = error_details

        if progress is not None:
            update["progress"] = progress

        update["status"] = status.value

        collection.update_one(
            {"_id": job_id},
            {"$set": update},
        )

        logger.debug(
            "Updated job %s: status=%s, progress=%.1f%%",
            job_id,
            status.value,
            progress or 0.0,
        )

    async def retry_job(self, job_id: str) -> bool:
        """Retry a failed job.

        Args:
            job_id: Job ID

        Returns:
            True if job was retried, False if max retries exceeded
        """
        db = self._get_db()
        collection = db.indexing_jobs

        job_doc = collection.find_one({"_id": job_id})
        if not job_doc:
            return False

        job = IndexingJob.from_dict(job_doc)

        if job.retry_count >= job.max_retries:
            logger.warning(
                "Job %s exceeded max retries (%d)",
                job_id,
                job.max_retries,
            )
            return False

        collection.update_one(
            {"_id": job_id},
            {
                "$set": {
                    "status": JobStatus.PENDING.value,
                    "error_message": None,
                    "error_details": None,
                },
                "$inc": {"retry_count": 1},
            },
        )

        logger.info("Retrying job %s (attempt %d/%d)", job_id, job.retry_count + 1, job.max_retries)
        return True

    async def cancel_job(self, job_id: str, user_id: str) -> bool:
        """Cancel a job (only if user owns it).

        Args:
            job_id: Job ID
            user_id: User ID (for authorization)

        Returns:
            True if job was cancelled, False otherwise
        """
        db = self._get_db()
        collection = db.indexing_jobs

        result = collection.update_one(
            {
                "_id": job_id,
                "user_id": ObjectId(user_id),
                "status": {"$in": [JobStatus.PENDING.value, JobStatus.RUNNING.value]},
            },
            {
                "$set": {
                    "status": JobStatus.CANCELLED.value,
                    "completed_at": datetime.utcnow(),
                }
            },
        )

        if result.modified_count > 0:
            logger.info("Cancelled job %s", job_id)
            return True

        return False

    async def get_job(self, job_id: str, user_id: Optional[str] = None) -> Optional[IndexingJob]:
        """Get job by ID.

        Args:
            job_id: Job ID
            user_id: User ID (optional, for authorization)

        Returns:
            IndexingJob or None
        """
        db = self._get_db()
        collection = db.indexing_jobs

        query = {"_id": job_id}
        if user_id:
            query["user_id"] = ObjectId(user_id)

        job_doc = collection.find_one(query)
        if not job_doc:
            return None

        return IndexingJob.from_dict(job_doc)

    async def get_job_by_resource_id(
        self,
        resource_id: str,
        user_id: Optional[str] = None,
    ) -> Optional[IndexingJob]:
        """Get job by resource ID.

        Args:
            resource_id: Resource ID
            user_id: User ID (optional, for authorization)

        Returns:
            IndexingJob or None
        """
        db = self._get_db()
        collection = db.indexing_jobs

        query = {"resource_id": resource_id}
        if user_id:
            query["user_id"] = ObjectId(user_id)

        job_doc = collection.find_one(query, sort=[("created_at", -1)])
        if not job_doc:
            return None

        return IndexingJob.from_dict(job_doc)

    async def recover_stale_jobs(self, stale_threshold_minutes: int = 30) -> int:
        """Recover stale running jobs (e.g., from server restart).

        Args:
            stale_threshold_minutes: Minutes after which a running job is considered stale

        Returns:
            Number of jobs recovered
        """
        db = self._get_db()
        collection = db.indexing_jobs

        threshold = datetime.utcnow() - timedelta(minutes=stale_threshold_minutes)

        result = collection.update_many(
            {
                "status": JobStatus.RUNNING.value,
                "started_at": {"$lt": threshold},
            },
            {
                "$set": {
                    "status": JobStatus.PENDING.value,
                    "started_at": None,
                }
            },
        )

        recovered = result.modified_count
        if recovered > 0:
            logger.info("Recovered %d stale jobs", recovered)

        return recovered

    async def list_jobs(
        self,
        user_id: Optional[str] = None,
        status: Optional[JobStatus] = None,
        limit: int = 100,
    ) -> list[IndexingJob]:
        """List jobs with optional filtering.

        Args:
            user_id: Filter by user ID
            status: Filter by status
            limit: Maximum number of jobs to return

        Returns:
            List of IndexingJob
        """
        db = self._get_db()
        collection = db.indexing_jobs

        query: dict[str, Any] = {}
        if user_id:
            query["user_id"] = ObjectId(user_id)
        if status:
            query["status"] = status.value

        cursor = collection.find(query).sort("created_at", -1).limit(limit)
        jobs = [IndexingJob.from_dict(doc) for doc in cursor]

        return jobs


job_queue_service = JobQueueService()

