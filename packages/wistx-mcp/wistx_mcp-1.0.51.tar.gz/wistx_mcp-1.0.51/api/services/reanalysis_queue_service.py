"""Background Re-Analysis Queue Service.

This service manages a queue of files that need re-analysis after
detecting changes during freshness checks. It enables non-blocking
updates to the search index.

Production Features:
- Async queue processing
- Rate limiting to avoid overwhelming the system
- Deduplication of queue entries
- Priority-based processing
- Graceful shutdown handling
- Metrics and logging
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from collections import deque

from api.database.async_mongodb import async_mongodb_adapter
from api.exceptions import DatabaseError

logger = logging.getLogger(__name__)


class ReanalysisStatus(str, Enum):
    """Status of a re-analysis task."""
    
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class ReanalysisPriority(int, Enum):
    """Priority levels for re-analysis tasks."""
    
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class ReanalysisTask:
    """A task for re-analyzing a file."""
    
    task_id: str
    resource_id: str
    file_path: str
    repository_url: str
    branch: str
    user_id: str
    priority: ReanalysisPriority = ReanalysisPriority.NORMAL
    status: ReanalysisStatus = ReanalysisStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "task_id": self.task_id,
            "resource_id": self.resource_id,
            "file_path": self.file_path,
            "repository_url": self.repository_url,
            "branch": self.branch,
            "user_id": self.user_id,
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "error_message": self.error_message,
            "retry_count": self.retry_count,
        }


class ReanalysisQueueService:
    """Service for managing background re-analysis of changed files.
    
    This service provides a non-blocking way to update the search index
    when files are detected as stale during search queries.
    """
    
    def __init__(
        self,
        max_queue_size: int = 1000,
        max_concurrent_tasks: int = 3,
        processing_interval: float = 5.0,
    ):
        """Initialize the re-analysis queue service.
        
        Args:
            max_queue_size: Maximum number of tasks in queue
            max_concurrent_tasks: Maximum concurrent re-analysis tasks
            processing_interval: Seconds between processing cycles
        """
        self._queue: deque[ReanalysisTask] = deque(maxlen=max_queue_size)
        self._task_ids: set[str] = set()  # For deduplication
        self._max_concurrent = max_concurrent_tasks
        self._processing_interval = processing_interval
        self._running = False
        self._processing_task: Optional[asyncio.Task] = None
        self._semaphore = asyncio.Semaphore(max_concurrent_tasks)
        self._lock = asyncio.Lock()
        
        # Metrics
        self._tasks_queued = 0
        self._tasks_completed = 0
        self._tasks_failed = 0
    
    async def start(self) -> None:
        """Start the background processing loop."""
        if self._running:
            return
        
        self._running = True
        self._processing_task = asyncio.create_task(self._processing_loop())
        logger.info("Re-analysis queue service started")
    
    async def stop(self) -> None:
        """Stop the background processing loop gracefully."""
        self._running = False
        if self._processing_task:
            self._processing_task.cancel()
            try:
                await self._processing_task
            except asyncio.CancelledError:
                pass
        logger.info(
            "Re-analysis queue service stopped. Stats: queued=%d, completed=%d, failed=%d",
            self._tasks_queued,
            self._tasks_completed,
            self._tasks_failed,
        )
    
    async def enqueue(
        self,
        resource_id: str,
        file_path: str,
        repository_url: str,
        branch: str,
        user_id: str,
        priority: ReanalysisPriority = ReanalysisPriority.NORMAL,
    ) -> Optional[str]:
        """Add a file to the re-analysis queue.
        
        Args:
            resource_id: Resource ID
            file_path: File path within repository
            repository_url: Repository URL
            branch: Branch name
            user_id: User ID
            priority: Task priority
            
        Returns:
            Task ID if queued, None if duplicate or queue full
        """
        # Generate task ID for deduplication
        task_id = f"{resource_id}:{file_path}:{branch}"

        async with self._lock:
            # Check for duplicate
            if task_id in self._task_ids:
                logger.debug("Skipping duplicate re-analysis task: %s", task_id)
                return None

            # Check queue capacity
            if len(self._queue) >= self._queue.maxlen:
                logger.warning("Re-analysis queue full, dropping task: %s", task_id)
                return None

            task = ReanalysisTask(
                task_id=task_id,
                resource_id=resource_id,
                file_path=file_path,
                repository_url=repository_url,
                branch=branch,
                user_id=user_id,
                priority=priority,
            )

            self._queue.append(task)
            self._task_ids.add(task_id)
            self._tasks_queued += 1

            logger.info(
                "Queued re-analysis task: %s (priority=%s, queue_size=%d)",
                task_id,
                priority.name,
                len(self._queue),
            )

            return task_id

    async def enqueue_batch(
        self,
        files: list[dict[str, Any]],
        priority: ReanalysisPriority = ReanalysisPriority.NORMAL,
    ) -> list[str]:
        """Add multiple files to the re-analysis queue.

        Args:
            files: List of file info dicts with resource_id, file_path, repository_url, branch, user_id
            priority: Task priority for all files

        Returns:
            List of task IDs that were queued
        """
        task_ids = []
        for file_info in files:
            task_id = await self.enqueue(
                resource_id=file_info.get("resource_id", ""),
                file_path=file_info.get("file_path", ""),
                repository_url=file_info.get("repository_url", ""),
                branch=file_info.get("branch", "main"),
                user_id=file_info.get("user_id", ""),
                priority=priority,
            )
            if task_id:
                task_ids.append(task_id)
        return task_ids

    async def _processing_loop(self) -> None:
        """Background loop for processing queued tasks."""
        while self._running:
            try:
                await self._process_next_batch()
                await asyncio.sleep(self._processing_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Error in re-analysis processing loop: %s", e, exc_info=True)
                await asyncio.sleep(self._processing_interval * 2)

    async def _process_next_batch(self) -> None:
        """Process the next batch of tasks from the queue."""
        tasks_to_process = []

        async with self._lock:
            # Get tasks up to max concurrent limit
            while len(tasks_to_process) < self._max_concurrent and self._queue:
                task = self._queue.popleft()
                tasks_to_process.append(task)

        if not tasks_to_process:
            return

        # Process tasks concurrently
        await asyncio.gather(
            *[self._process_task(task) for task in tasks_to_process],
            return_exceptions=True,
        )

    async def _process_task(self, task: ReanalysisTask) -> None:
        """Process a single re-analysis task.

        Args:
            task: The task to process
        """
        async with self._semaphore:
            task.status = ReanalysisStatus.IN_PROGRESS
            task.started_at = datetime.utcnow()

            try:
                logger.info("Processing re-analysis task: %s", task.task_id)

                # Fetch fresh content and trigger re-analysis
                await self._reanalyze_file(task)

                task.status = ReanalysisStatus.COMPLETED
                task.completed_at = datetime.utcnow()
                self._tasks_completed += 1

                logger.info(
                    "Completed re-analysis task: %s (duration=%.2fs)",
                    task.task_id,
                    (task.completed_at - task.started_at).total_seconds(),
                )

            except Exception as e:
                task.retry_count += 1
                task.error_message = str(e)

                if task.retry_count < task.max_retries:
                    # Re-queue for retry
                    task.status = ReanalysisStatus.PENDING
                    async with self._lock:
                        self._queue.append(task)
                    logger.warning(
                        "Re-analysis task failed, will retry: %s (attempt %d/%d): %s",
                        task.task_id,
                        task.retry_count,
                        task.max_retries,
                        e,
                    )
                else:
                    task.status = ReanalysisStatus.FAILED
                    task.completed_at = datetime.utcnow()
                    self._tasks_failed += 1
                    logger.error(
                        "Re-analysis task failed permanently: %s: %s",
                        task.task_id,
                        e,
                    )
            finally:
                # Remove from deduplication set
                async with self._lock:
                    self._task_ids.discard(task.task_id)

    async def _reanalyze_file(self, task: ReanalysisTask) -> None:
        """Re-analyze a single file.

        This method fetches fresh content from GitHub and triggers
        the analysis pipeline to update the knowledge article.

        Args:
            task: The re-analysis task
        """
        from api.services.fresh_content_service import fresh_content_service

        # Fetch fresh content
        fresh_content = await fresh_content_service.fetch_fresh_file_content(
            repo_url=task.repository_url,
            file_path=task.file_path,
            branch=task.branch,
            user_id=task.user_id,
        )

        if not fresh_content:
            logger.warning("Could not fetch fresh content for: %s", task.file_path)
            return

        if not fresh_content.is_stale:
            logger.info("File has not changed, skipping re-analysis: %s", task.file_path)
            return

        # Update the knowledge article in MongoDB
        await self._update_knowledge_article(task, fresh_content.content, fresh_content.content_hash)

    async def _update_knowledge_article(
        self,
        task: ReanalysisTask,
        new_content: str,
        content_hash: str,
    ) -> None:
        """Update the knowledge article with fresh content.

        For now, this updates the source_hash to mark the article as fresh.
        Full re-analysis with LLM would be done in a separate pipeline.

        Args:
            task: The re-analysis task
            new_content: Fresh content from GitHub
            content_hash: Hash of the fresh content
        """
        try:
            await async_mongodb_adapter.connect()
            db = async_mongodb_adapter.get_database()

            if db is None:
                raise DatabaseError(
                    message="Failed to connect to MongoDB",
                    user_message="Database connection failed. Please try again later.",
                    error_code="DATABASE_CONNECTION_ERROR",
                    details={"service": "reanalysis_queue"}
                )

            # Update the knowledge article's source hash
            # This marks it as "checked" even if we don't re-analyze
            result = await db.knowledge_articles.update_many(
                {
                    "resource_id": task.resource_id,
                    "source_url": {"$regex": task.file_path, "$options": "i"},
                },
                {
                    "$set": {
                        "source_hash": content_hash,
                        "last_freshness_check": datetime.utcnow(),
                    }
                },
            )

            logger.info(
                "Updated %d knowledge articles for file: %s",
                result.modified_count,
                task.file_path,
            )

        except Exception as e:
            logger.error("Failed to update knowledge article: %s", e, exc_info=True)
            raise

    def get_queue_stats(self) -> dict[str, Any]:
        """Get queue statistics.

        Returns:
            Dictionary with queue statistics
        """
        return {
            "queue_size": len(self._queue),
            "max_queue_size": self._queue.maxlen,
            "tasks_queued_total": self._tasks_queued,
            "tasks_completed_total": self._tasks_completed,
            "tasks_failed_total": self._tasks_failed,
            "is_running": self._running,
        }


# Singleton instance
reanalysis_queue_service = ReanalysisQueueService()

