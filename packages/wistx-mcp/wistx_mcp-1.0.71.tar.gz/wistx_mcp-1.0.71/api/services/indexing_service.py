"""Indexing service for managing user-provided resource indexing jobs."""

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from bson import ObjectId

import hashlib

from api.database.mongodb import mongodb_manager
from api.models.indexed_file import IndexedFile
from api.models.indexing import (
    IndexedResource,
    IndexingActivity,
    ActivityType,
    JobStatus,
    ResourceStatus,
    ResourceType,
    generate_resource_id,
)
from api.services.job_queue_service import job_queue_service
from api.services.exceptions import QuotaExceededError
from api.services.quota_service import quota_service
from api.utils.repo_normalizer import normalize_repo_url
from pymongo.errors import DuplicateKeyError
from api.exceptions import ValidationError, NotFoundError, DatabaseError

logger = logging.getLogger(__name__)

# Collection name for indexing activities
ACTIVITIES_COLLECTION = "indexing_activities"


class IndexingService:
    """Service for managing indexing jobs and background processing."""

    def __init__(self):
        """Initialize indexing service."""
        self.running_jobs: dict[str, asyncio.Task] = {}
        self._indexing_start_times: dict[str, datetime] = {}

    # ==================== Activity Logging Methods ====================

    async def log_activity(
        self,
        resource_id: str,
        activity_type: ActivityType,
        message: str,
        file_path: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
        progress: Optional[float] = None,
        files_processed: Optional[int] = None,
        total_files: Optional[int] = None,
    ) -> None:
        """Log an indexing activity event.

        Args:
            resource_id: Resource ID
            activity_type: Type of activity
            message: Human-readable message
            file_path: Optional file path
            details: Optional additional details
            progress: Current progress percentage
            files_processed: Files processed count
            total_files: Total files count
        """
        try:
            db = mongodb_manager.get_database()
            collection = db[ACTIVITIES_COLLECTION]

            # Calculate elapsed time
            elapsed_seconds = None
            if resource_id in self._indexing_start_times:
                elapsed = datetime.utcnow() - self._indexing_start_times[resource_id]
                elapsed_seconds = elapsed.total_seconds()

            activity = IndexingActivity(
                resource_id=resource_id,
                activity_type=activity_type,
                message=message,
                file_path=file_path,
                details=details,
                progress=progress,
                files_processed=files_processed,
                total_files=total_files,
                elapsed_seconds=elapsed_seconds,
            )

            collection.insert_one(activity.to_dict())

            # Broadcast activity via WebSocket
            try:
                await self._broadcast_activity(resource_id, activity)
            except Exception as ws_error:
                logger.debug("WebSocket activity broadcast failed: %s", ws_error)
        except Exception as e:
            # Don't fail indexing if activity logging fails
            logger.warning("Failed to log activity for %s: %s", resource_id, e)

    async def _broadcast_activity(
        self,
        resource_id: str,
        activity: IndexingActivity,
    ) -> None:
        """Broadcast activity via WebSocket.

        Args:
            resource_id: Resource ID
            activity: Activity to broadcast
        """
        try:
            from api.routers.v1.websocket import connection_manager

            # Get user_id for the resource
            resource = await self.get_resource_by_id_internal(resource_id)
            if not resource:
                return

            user_id = str(resource.user_id) if resource.user_id else ""

            await connection_manager.broadcast_activity(
                resource_id=resource_id,
                user_id=user_id,
                activity=activity.to_dict(),
            )
        except ImportError:
            # WebSocket module not available
            pass
        except Exception as e:
            logger.debug("Failed to broadcast activity: %s", e)

    async def get_activities(
        self,
        resource_id: str,
        limit: int = 100,
        after_timestamp: Optional[datetime] = None,
    ) -> list[IndexingActivity]:
        """Get activities for a resource.

        Args:
            resource_id: Resource ID
            limit: Maximum number of activities to return
            after_timestamp: Only return activities after this time

        Returns:
            List of IndexingActivity objects
        """
        db = mongodb_manager.get_database()
        collection = db[ACTIVITIES_COLLECTION]

        query: dict[str, Any] = {"resource_id": resource_id}
        if after_timestamp:
            query["created_at"] = {"$gt": after_timestamp}

        cursor = collection.find(query).sort("created_at", -1).limit(limit)

        activities = []
        for doc in cursor:
            activities.append(IndexingActivity.from_dict(doc))

        # Return in chronological order (oldest first)
        return list(reversed(activities))

    async def clear_activities(self, resource_id: str) -> int:
        """Clear all activities for a resource.

        Args:
            resource_id: Resource ID

        Returns:
            Number of activities deleted
        """
        db = mongodb_manager.get_database()
        collection = db[ACTIVITIES_COLLECTION]
        result = collection.delete_many({"resource_id": resource_id})
        return result.deleted_count

    # ==================== End Activity Logging Methods ====================

    async def create_resource(
        self,
        user_id: str,
        resource_type: ResourceType,
        name: str,
        organization_id: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[list[str]] = None,
        repo_url: Optional[str] = None,
        branch: Optional[str] = None,
        documentation_url: Optional[str] = None,
        include_patterns: Optional[list[str]] = None,
        exclude_patterns: Optional[list[str]] = None,
        document_url: Optional[str] = None,
        document_type: Optional[str] = None,
        github_token: Optional[str] = None,
        compliance_standards: Optional[list[str]] = None,
        environment_name: Optional[str] = None,
        max_pages: int = 100,
        max_depth: int = 5,
        incremental_update: bool = True,
    ) -> IndexedResource:
        """Create a new indexed resource with duplicate detection.

        Args:
            user_id: User ID
            resource_type: Type of resource
            name: Resource name
            organization_id: Organization ID (optional)
            description: Resource description
            tags: Tags for categorization
            repo_url: GitHub repository URL (for repository type)
            branch: GitHub branch name
            documentation_url: Documentation URL (for documentation type)
            include_patterns: URL patterns to include
            exclude_patterns: URL patterns to exclude
            document_url: Document URL (for document type)
            document_type: Document type
            github_token: GitHub token (for private repos)
            compliance_standards: Compliance standards to check
            environment_name: Environment name (dev, stage, prod, etc.)

        Returns:
            Created or existing IndexedResource

        Raises:
            ValueError: If required fields are missing for resource type
        """
        normalized_repo_url = None
        if resource_type == ResourceType.REPOSITORY and repo_url:
            normalized_repo_url = normalize_repo_url(repo_url)

        if resource_type == ResourceType.REPOSITORY and not repo_url:
            raise ValidationError(
                message="repo_url is required for repository type",
                user_message="Repository URL is required for repository indexing",
                error_code="MISSING_REPO_URL",
                details={"resource_type": resource_type}
            )
        if resource_type == ResourceType.DOCUMENTATION and not documentation_url:
            raise ValidationError(
                message="documentation_url is required for documentation type",
                user_message="Documentation URL is required for documentation indexing",
                error_code="MISSING_DOCUMENTATION_URL",
                details={"resource_type": resource_type}
            )
        if resource_type == ResourceType.DOCUMENT and not document_url:
            raise ValidationError(
                message="document_url is required for document type",
                user_message="Document URL is required for document indexing",
                error_code="MISSING_DOCUMENT_URL",
                details={"resource_type": resource_type}
            )

        if resource_type == ResourceType.REPOSITORY and normalized_repo_url:
            existing = await self._find_existing_repository(
                user_id=user_id,
                normalized_repo_url=normalized_repo_url,
                branch=branch or "main",
                include_patterns=include_patterns,
            )

            if existing:
                if existing.status == ResourceStatus.COMPLETED:
                    logger.info(
                        "Repository already indexed: %s (resource_id: %s)",
                        normalized_repo_url,
                        existing.resource_id,
                    )
                    return existing
                elif existing.status == ResourceStatus.FAILED:
                    logger.info("Re-indexing failed resource: %s", existing.resource_id)
                    await self._reset_resource_for_reindex(existing.resource_id)
                    return existing
                elif existing.status == ResourceStatus.INDEXING:
                    logger.info("Repository already indexing: %s", existing.resource_id)
                    return existing

        resource_id = generate_resource_id()

        github_token_encrypted = None
        if github_token:
            github_token_encrypted = self._encrypt_token(github_token, resource_id)

        resource_data = {
            "resource_id": resource_id,
            "user_id": user_id,
            "organization_id": organization_id,
            "resource_type": resource_type,
            "status": ResourceStatus.PENDING,
            "progress": 0.0,
            "name": name,
            "description": description,
            "tags": tags or [],
            "repo_url": repo_url,
            "normalized_repo_url": normalized_repo_url,
            "branch": branch or "main",
            "documentation_url": documentation_url,
            "include_patterns": include_patterns,
            "exclude_patterns": exclude_patterns,
            "document_url": document_url,
            "document_type": document_type,
            "github_token_encrypted": github_token_encrypted,
            "max_pages": max_pages,
            "max_depth": max_depth,
            "incremental_update": incremental_update,
        }

        if compliance_standards:
            resource_data["compliance_standards"] = compliance_standards
        if environment_name:
            resource_data["environment_name"] = environment_name

        resource = IndexedResource(**resource_data)

        db = mongodb_manager.get_database()
        collection = db.indexed_resources

        resource_dict = resource.to_dict()
        try:
            collection.insert_one(resource_dict)
        except DuplicateKeyError:
            logger.warning(
                "Duplicate key error (race condition), fetching existing resource"
            )
            existing = await self._find_existing_repository(
                user_id=user_id,
                normalized_repo_url=normalized_repo_url or "",
                branch=branch or "main",
                include_patterns=include_patterns,
            )
            if existing:
                return existing
            raise

        logger.info(
            "Created indexed resource: %s (type: %s, user: %s)",
            resource_id,
            resource_type,
            user_id,
        )

        return resource

    async def _find_existing_repository(
        self,
        user_id: str,
        normalized_repo_url: str,
        branch: str,
        include_patterns: Optional[list[str]] = None,
    ) -> Optional[IndexedResource]:
        """Find existing repository resource.

        Args:
            user_id: User ID
            normalized_repo_url: Normalized repository URL
            branch: Branch name
            include_patterns: Include patterns (for uniqueness check)

        Returns:
            Existing IndexedResource or None
        """
        db = mongodb_manager.get_database()
        collection = db.indexed_resources

        query: dict[str, Any] = {
            "user_id": ObjectId(user_id),
            "resource_type": ResourceType.REPOSITORY.value,
            "normalized_repo_url": normalized_repo_url,
            "branch": branch,
            "status": {"$ne": ResourceStatus.DELETED.value},
        }

        if include_patterns:
            query["include_patterns"] = include_patterns

        doc = collection.find_one(query, sort=[("created_at", -1)])

        return IndexedResource.from_dict(doc) if doc else None

    async def _reset_resource_for_reindex(self, resource_id: str) -> None:
        """Reset failed resource for re-indexing.

        Args:
            resource_id: Resource ID to reset
        """
        await self._update_resource_status(
            resource_id,
            status=ResourceStatus.PENDING,
            progress=0.0,
            error_message=None,
            error_details=None,
        )

    async def start_indexing_job(
        self,
        resource_id: str,
        user_id: str,
        plan: str,
        organization_id: Optional[str] = None,
    ) -> str:
        """Start indexing job by enqueueing it.

        Args:
            resource_id: Resource ID
            user_id: User ID
            plan: User's plan
            organization_id: Organization ID (optional)

        Returns:
            Job ID

        Raises:
            ValueError: If resource not found
            QuotaExceededError: If quota exceeded
        """
        resource = await self.get_resource(resource_id, user_id)
        if not resource:
            raise NotFoundError(
                message=f"Resource not found: {resource_id}",
                user_message="Resource not found",
                error_code="RESOURCE_NOT_FOUND",
                details={"resource_id": resource_id, "user_id": user_id}
            )

        if resource.status in [ResourceStatus.INDEXING, ResourceStatus.COMPLETED]:
            logger.warning(
                "Resource %s already in status: %s",
                resource_id,
                resource.status,
            )
            existing_job = await job_queue_service.get_job_by_resource_id(
                resource_id=resource_id,
                user_id=user_id,
            )
            if existing_job and existing_job.status in [JobStatus.PENDING, JobStatus.RUNNING]:
                return existing_job.job_id
            return ""

        await quota_service.check_indexing_quota(
            user_id=user_id,
            plan=plan,
            estimated_storage_mb=0.0,
        )

        await self._update_resource_status(
            resource_id,
            status=ResourceStatus.INDEXING,
            progress=0.0,
        )

        job = await job_queue_service.enqueue_job(
            resource_id=resource_id,
            user_id=user_id,
            job_type=resource.resource_type.value,
            plan=plan,
            organization_id=organization_id,
        )

        logger.info("Enqueued indexing job: %s (resource: %s)", job.job_id, resource_id)

        return job.job_id

    async def _run_indexing_job(
        self,
        resource_id: str,
        resource: IndexedResource,
        user_id: str,
        plan: str,
        job_id: Optional[str] = None,
    ) -> None:
        """Run indexing job with progress updates.

        Args:
            resource_id: Resource ID
            resource: IndexedResource instance
            user_id: User ID
            plan: User's plan
            job_id: Job ID (optional, for progress updates)
        """
        # Track start time for elapsed calculations
        self._indexing_start_times[resource_id] = datetime.utcnow()

        # Clear previous activities for re-indexing
        await self.clear_activities(resource_id)

        # Log indexing started
        await self.log_activity(
            resource_id=resource_id,
            activity_type=ActivityType.INDEXING_STARTED,
            message=f"Started indexing {resource.resource_type.value}: {resource.name}",
            progress=0.0,
            details={"resource_type": resource.resource_type.value, "job_id": job_id},
        )

        try:
            if resource.resource_type == ResourceType.REPOSITORY:
                await self._index_repository(resource_id, resource, user_id, plan, job_id)
            elif resource.resource_type == ResourceType.DOCUMENTATION:
                await self._index_documentation(resource_id, resource, user_id, plan)
            elif resource.resource_type == ResourceType.DOCUMENT:
                await self._index_document(resource_id, resource, user_id, plan)
            else:
                raise ValidationError(
                    message=f"Unsupported resource type: {resource.resource_type}",
                    user_message=f"Resource type '{resource.resource_type}' is not supported",
                    error_code="UNSUPPORTED_RESOURCE_TYPE",
                    details={"resource_type": resource.resource_type, "resource_id": resource_id}
                )

            await self._update_resource_status(
                resource_id,
                status=ResourceStatus.COMPLETED,
                progress=100.0,
                indexed_at=datetime.utcnow(),
            )

            # Log indexing completed
            await self.log_activity(
                resource_id=resource_id,
                activity_type=ActivityType.INDEXING_COMPLETED,
                message=f"Successfully completed indexing: {resource.name}",
                progress=100.0,
            )

            # Create in-app notification for user
            await self._create_indexing_notification(
                user_id=user_id,
                resource_id=resource_id,
                resource_name=resource.name,
                notification_type="indexing_complete",
                title=f"Indexing Complete: {resource.name}",
                message=f"Successfully indexed {resource.articles_indexed or 0} articles from {resource.name}",
            )

            logger.info("Completed indexing job: %s", resource_id)

        except QuotaExceededError as e:
            await self._update_resource_status(
                resource_id,
                status=ResourceStatus.FAILED,
                error_message=str(e),
                error_details={"error_type": "quota_exceeded"},
            )
            await self.log_activity(
                resource_id=resource_id,
                activity_type=ActivityType.INDEXING_FAILED,
                message=f"Indexing failed: Quota exceeded - {str(e)}",
                details={"error_type": "quota_exceeded", "error": str(e)},
            )
            await self._create_indexing_notification(
                user_id=user_id,
                resource_id=resource_id,
                resource_name=resource.name,
                notification_type="indexing_failed",
                title=f"Indexing Failed: {resource.name}",
                message=f"Quota exceeded while indexing {resource.name}",
            )
            logger.error("Indexing job failed due to quota: %s", resource_id)
            raise
        except (ValueError, RuntimeError, ConnectionError, TimeoutError) as e:
            await self._update_resource_status(
                resource_id,
                status=ResourceStatus.FAILED,
                error_message=str(e),
                error_details={"error_type": type(e).__name__},
            )
            await self.log_activity(
                resource_id=resource_id,
                activity_type=ActivityType.INDEXING_FAILED,
                message=f"Indexing failed: {str(e)[:100]}",
                details={"error_type": type(e).__name__, "error": str(e)},
            )
            await self._create_indexing_notification(
                user_id=user_id,
                resource_id=resource_id,
                resource_name=resource.name,
                notification_type="indexing_failed",
                title=f"Indexing Failed: {resource.name}",
                message=f"An error occurred while indexing {resource.name}",
            )
            logger.error("Indexing job failed: %s - %s", resource_id, e, exc_info=True)
            raise
        except Exception as e:
            await self._update_resource_status(
                resource_id,
                status=ResourceStatus.FAILED,
                error_message="Unexpected error occurred",
                error_details={"error_type": "unexpected_error"},
            )
            await self.log_activity(
                resource_id=resource_id,
                activity_type=ActivityType.INDEXING_FAILED,
                message="Indexing failed: Unexpected error occurred",
                details={"error_type": "unexpected_error", "error": str(e)},
            )
            await self._create_indexing_notification(
                user_id=user_id,
                resource_id=resource_id,
                resource_name=resource.name,
                notification_type="indexing_failed",
                title=f"Indexing Failed: {resource.name}",
                message=f"An unexpected error occurred while indexing {resource.name}",
            )
            logger.error("Unexpected error in indexing job %s: %s", resource_id, e, exc_info=True)
            raise RuntimeError(f"Unexpected error in indexing job: {e}") from e

        finally:
            if resource_id in self.running_jobs:
                del self.running_jobs[resource_id]
            # Clean up start time tracking
            if resource_id in self._indexing_start_times:
                del self._indexing_start_times[resource_id]

    async def _index_repository(
        self,
        resource_id: str,
        resource: IndexedResource,
        user_id: str,
        plan: str,
        job_id: Optional[str] = None,
    ) -> None:
        """Index a GitHub repository.

        Args:
            resource_id: Resource ID
            resource: IndexedResource instance
            user_id: User ID
            plan: User's plan
            job_id: Job ID (for progress updates)
        """
        from api.services.github_service import github_service

        github_token = None
        if resource.github_token_encrypted:
            github_token = self._decrypt_token(resource.github_token_encrypted, resource_id)

        await self._update_resource_status(resource_id, progress=10.0)

        # Log activity: starting repository indexing
        await self.log_activity(
            resource_id=resource_id,
            activity_type=ActivityType.ANALYSIS_STARTED,
            message=f"Preparing to clone repository: {resource.repo_url}",
            progress=10.0,
            details={"branch": resource.branch or "main"},
        )

        async def progress_callback(progress: float) -> None:
            await self._update_resource_progress(resource_id, progress)
            if job_id:
                await job_queue_service.update_job_status(job_id, JobStatus.RUNNING, progress=progress)

        # Activity callback for detailed logging from github_service
        async def activity_callback(
            activity_type_str: str,
            message: str,
            file_path: Optional[str],
            details: Optional[dict[str, Any]],
        ) -> None:
            # Map string activity types to enum
            activity_type_map = {
                "repo_cloned": ActivityType.REPO_CLONED,
                "files_discovered": ActivityType.FILES_DISCOVERED,
                "file_processing": ActivityType.FILE_PROCESSING,
                "file_processed": ActivityType.FILE_PROCESSED,
                "file_skipped": ActivityType.FILE_SKIPPED,
                "file_failed": ActivityType.FILE_FAILED,
                "checkpoint_saved": ActivityType.CHECKPOINT_SAVED,
                "articles_batch_stored": ActivityType.ARTICLES_BATCH_STORED,
                "analysis_completed": ActivityType.ANALYSIS_COMPLETED,
            }
            activity_type = activity_type_map.get(activity_type_str, ActivityType.FILE_PROCESSED)
            await self.log_activity(
                resource_id=resource_id,
                activity_type=activity_type,
                message=message,
                file_path=file_path,
                details=details,
            )

        compliance_standards = getattr(resource, "compliance_standards", None)
        environment_name = getattr(resource, "environment_name", None)

        await github_service.index_repository(
            resource_id=resource_id,
            repo_url=resource.repo_url or "",
            branch=resource.branch or "main",
            user_id=user_id,
            github_token=github_token,
            include_patterns=resource.include_patterns,
            exclude_patterns=resource.exclude_patterns,
            compliance_standards=compliance_standards,
            environment_name=environment_name,
            progress_callback=progress_callback,
            activity_callback=activity_callback,
        )

        try:
            from api.services.section_organizer import section_organizer

            sections = await section_organizer.organize_components_into_sections(
                resource_id=resource_id,
                user_id=user_id,
                commit_sha=getattr(resource, "last_commit_sha", None),
                branch=resource.branch or "main",
            )

            logger.info(
                "Created %d sections for resource %s",
                len(sections),
                resource_id,
            )
        except Exception as e:
            logger.warning(
                "Failed to organize sections for resource %s: %s",
                resource_id,
                e,
                exc_info=True,
            )

    async def _index_documentation(
        self,
        resource_id: str,
        resource: IndexedResource,
        user_id: str,
        plan: str,
    ) -> None:
        """Index a documentation website using multi-page crawler and Claude Opus.

        Uses DocumentationCrawler for multi-page crawling (sitemap + link following)
        and DocumentationAnalyzer (Claude Opus) for industry-leading analysis,
        matching the quality of repository indexing.

        Args:
            resource_id: Resource ID
            resource: IndexedResource instance
            user_id: User ID
            plan: User's plan
        """
        from datetime import datetime
        from api.services.documentation_analyzer import documentation_analyzer
        from api.services.github_service import github_service
        from api.services.context_generator import context_generator
        from data_pipelines.collectors.docs_collector import (
            DocumentationCrawler,
            CrawlConfig,
            checkpoint_manager,
        )

        await self._update_resource_status(resource_id, progress=5.0)

        url = resource.documentation_url or ""
        articles_created = 0
        total_pages_crawled = 0
        pages_skipped = 0

        # Activity callback for logging progress
        async def activity_callback_async(activity_type_str: str, message: str, details: dict | None = None):
            try:
                activity_map = {
                    "ANALYSIS_STARTED": ActivityType.INDEXING_STARTED,
                    "TOPICS_EXTRACTED": ActivityType.INDEXING_PROGRESS,
                    "PROCESSING_CHUNKS": ActivityType.INDEXING_PROGRESS,
                    "ANALYZING_CHUNK": ActivityType.INDEXING_PROGRESS,
                    "ANALYSIS_COMPLETE": ActivityType.INDEXING_COMPLETED,
                    "CRAWL_STARTED": ActivityType.INDEXING_STARTED,
                    "SITEMAP_FOUND": ActivityType.INDEXING_PROGRESS,
                    "CRAWLING_BATCH": ActivityType.INDEXING_PROGRESS,
                    "PAGE_CRAWLED": ActivityType.INDEXING_PROGRESS,
                    "CRAWL_COMPLETE": ActivityType.INDEXING_PROGRESS,
                    "PAGE_UNCHANGED": ActivityType.INDEXING_PROGRESS,
                    "PAGE_CHANGED": ActivityType.INDEXING_PROGRESS,
                    "CHECKPOINT_SAVED": ActivityType.CHECKPOINT_SAVED,
                }
                mapped_type = activity_map.get(activity_type_str, ActivityType.INDEXING_PROGRESS)

                await self.log_activity(
                    resource_id=resource_id,
                    activity_type=mapped_type,
                    message=message,
                    details={
                        "activity_subtype": activity_type_str,
                        **(details or {}),
                    },
                )
            except Exception as e:
                logger.warning("Failed to log activity: %s", e)

        def activity_callback(activity_type: str, message: str, details: dict | None = None):
            """Sync wrapper for activity callback."""
            try:
                asyncio.create_task(activity_callback_async(activity_type, message, details))
            except Exception as e:
                logger.warning("Failed to schedule activity log: %s", e)

        try:
            # Configure crawler based on resource settings and plan limits
            plan_max_pages = 50 if plan == "free" else 500
            effective_max_pages = min(resource.max_pages, plan_max_pages)

            crawl_config = CrawlConfig(
                max_pages=effective_max_pages,
                max_depth=resource.max_depth,
                rate_limit_delay=0.5,
                parallel_requests=5,
                include_patterns=resource.include_patterns or [],
                exclude_patterns=resource.exclude_patterns or [],
            )

            crawler = DocumentationCrawler(config=crawl_config)

            # Use incremental crawl if enabled, otherwise full crawl
            if resource.incremental_update:
                changed_pages, unchanged_pages = await crawler.crawl_incremental(
                    start_url=url,
                    resource_id=resource_id,
                    activity_callback=activity_callback,
                )
            else:
                # Full crawl - treat all pages as changed
                all_pages = await crawler.crawl(
                    start_url=url,
                    activity_callback=activity_callback,
                )
                changed_pages = all_pages
                unchanged_pages = []

            total_pages_crawled = len(changed_pages) + len(unchanged_pages)
            pages_skipped = len(unchanged_pages)

            if not changed_pages and not unchanged_pages:
                logger.warning("No pages crawled from documentation URL: %s", url)
                activity_callback(
                    "NO_CONTENT",
                    f"No pages crawled from {url}",
                    {"url": url},
                )
                await self._update_resource_status(
                    resource_id,
                    articles_indexed=0,
                    storage_mb=0.0,
                )
                return

            await self._update_resource_status(resource_id, progress=30.0)

            activity_callback(
                "CRAWL_COMPLETE",
                f"Crawled {total_pages_crawled} pages ({len(changed_pages)} changed, {pages_skipped} unchanged)",
                {"total_pages": total_pages_crawled, "changed": len(changed_pages), "unchanged": pages_skipped},
            )

            # Analyze only changed pages with Claude Opus
            doc_context = {
                "resource_id": resource_id,
                "user_id": user_id,
                "compliance_standards": resource.compliance_standards or [],
            }

            for idx, page in enumerate(changed_pages):
                progress = 30.0 + (idx / max(len(changed_pages), 1)) * 50.0
                await self._update_resource_status(resource_id, progress=progress)

                activity_callback(
                    "ANALYZING_PAGE",
                    f"Analyzing page {idx + 1}/{len(changed_pages)}: {page.title}",
                    {"page_url": page.url, "page_title": page.title},
                )

                page_articles_count = 0
                try:
                    # Analyze page content
                    articles = await documentation_analyzer.analyze_documentation(
                        content=page.content,
                        source_url=page.url,
                        title=page.title,
                        doc_context=doc_context,
                        activity_callback=activity_callback,
                    )

                    # Store articles with context generation
                    for article in articles:
                        try:
                            contextual_description = await context_generator.generate_context(
                                article=article,
                                repo_context=None,
                            )
                            article.contextual_description = contextual_description
                            article.context_generated_at = datetime.utcnow()
                            article.context_version = "1.0"
                        except Exception as e:
                            logger.warning(
                                "Failed to generate contextual description for documentation article %s: %s",
                                article.article_id,
                                e,
                                exc_info=True,
                            )

                        await github_service._store_article(article)
                        articles_created += 1
                        page_articles_count += 1

                        activity_callback(
                            "ARTICLE_CREATED",
                            f"Created article: {article.title}",
                            {"article_id": article.article_id, "title": article.title},
                        )

                    # Save checkpoint for successful page
                    checkpoint_manager.save_page_checkpoint(
                        resource_id=resource_id,
                        page_url=page.url,
                        content_hash=page.content_hash,
                        articles_created=page_articles_count,
                        status="completed",
                    )

                    activity_callback(
                        "CHECKPOINT_SAVED",
                        f"Checkpoint saved for {page.title}",
                        {"page_url": page.url, "articles": page_articles_count},
                    )

                except Exception as e:
                    # Save checkpoint for failed page
                    checkpoint_manager.save_page_checkpoint(
                        resource_id=resource_id,
                        page_url=page.url,
                        content_hash=page.content_hash,
                        articles_created=0,
                        status="failed",
                        error=str(e),
                    )
                    logger.warning("Failed to analyze page %s: %s", page.url, e)

            await self._update_resource_status(
                resource_id,
                progress=90.0,
                articles_indexed=articles_created,
            )

        except (ValueError, RuntimeError, ConnectionError, TimeoutError, AttributeError) as e:
            logger.error("Error indexing documentation: %s", e, exc_info=True)
            activity_callback("ERROR", f"Error indexing documentation: {e}", {"error": str(e)})
            raise
        except Exception as e:
            logger.error("Unexpected error indexing documentation: %s", e, exc_info=True)
            activity_callback("ERROR", f"Unexpected error: {e}", {"error": str(e)})
            raise RuntimeError(f"Unexpected error indexing documentation: {e}") from e

        await self._update_resource_status(
            resource_id,
            articles_indexed=articles_created,
            storage_mb=0.0,
        )

        # Organize articles into sections (same as repository indexing)
        try:
            from api.services.section_organizer import section_organizer

            activity_callback(
                "ORGANIZING_SECTIONS",
                "Organizing articles into sections",
                {"articles_count": articles_created},
            )

            sections = await section_organizer.organize_components_into_sections(
                resource_id=resource_id,
                user_id=user_id,
                commit_sha=None,
                branch=None,
            )

            logger.info(
                "Created %d sections for documentation resource %s",
                len(sections),
                resource_id,
            )

            activity_callback(
                "SECTIONS_CREATED",
                f"Created {len(sections)} sections",
                {"sections_count": len(sections)},
            )
        except Exception as e:
            logger.warning(
                "Failed to organize sections for documentation resource %s: %s",
                resource_id,
                e,
                exc_info=True,
            )

        activity_callback(
            "INDEXING_COMPLETE",
            f"Completed indexing {url}: {total_pages_crawled} pages ({pages_skipped} unchanged), {articles_created} articles",
            {
                "pages_crawled": total_pages_crawled,
                "pages_skipped": pages_skipped,
                "articles_created": articles_created,
            },
        )

    async def _index_document(
        self,
        resource_id: str,
        resource: IndexedResource,
        user_id: str,
        plan: str,
    ) -> None:
        """Index a single uploaded document using Claude Opus.

        Uses DocumentationAnalyzer (Claude Opus) for industry-leading analysis,
        matching the quality of repository indexing.

        Args:
            resource_id: Resource ID
            resource: IndexedResource instance
            user_id: User ID
            plan: User's plan
        """
        import asyncio
        import tempfile
        from datetime import datetime
        from pathlib import Path

        await self._update_resource_status(resource_id, progress=5.0)

        from data_pipelines.processors.document_processor import DocumentProcessor
        from api.services.documentation_analyzer import documentation_analyzer
        from api.services.github_service import github_service
        from api.utils.file_handler import file_handler
        from api.services.file_storage_service import file_storage_service
        from api.services.context_generator import context_generator
        from data_pipelines.collectors.docs_collector import checkpoint_manager
        import hashlib

        # Activity callback for logging progress
        async def activity_callback_async(activity_type_str: str, message: str, details: dict | None = None):
            try:
                activity_map = {
                    "ANALYSIS_STARTED": ActivityType.INDEXING_STARTED,
                    "TOPICS_EXTRACTED": ActivityType.INDEXING_PROGRESS,
                    "PROCESSING_CHUNKS": ActivityType.INDEXING_PROGRESS,
                    "ANALYZING_CHUNK": ActivityType.INDEXING_PROGRESS,
                    "ANALYSIS_COMPLETE": ActivityType.INDEXING_COMPLETED,
                    "ARTICLE_CREATED": ActivityType.INDEXING_PROGRESS,
                    "CHECKPOINT_SAVED": ActivityType.CHECKPOINT_SAVED,
                    "DOCUMENT_UNCHANGED": ActivityType.INDEXING_PROGRESS,
                    "DOCUMENT_PROCESSING": ActivityType.INDEXING_PROGRESS,
                }
                mapped_type = activity_map.get(activity_type_str, ActivityType.INDEXING_PROGRESS)

                await self.log_activity(
                    resource_id=resource_id,
                    activity_type=mapped_type,
                    message=message,
                    details={
                        "activity_subtype": activity_type_str,
                        **(details or {}),
                    },
                )
            except Exception as e:
                logger.warning("Failed to log activity: %s", e)

        def activity_callback(activity_type: str, message: str, details: dict | None = None):
            """Sync wrapper for activity callback."""
            try:
                asyncio.create_task(activity_callback_async(activity_type, message, details))
            except Exception as e:
                logger.warning("Failed to schedule activity log: %s", e)

        file_path = Path(resource.document_url or "")

        if not file_path.exists():
            if resource.file_storage_id:
                file_content_bytes, metadata = file_storage_service.retrieve_file(
                    resource.file_storage_id,
                )
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(metadata.get("filename", "file")).suffix) as tmp_file:
                    tmp_path = Path(tmp_file.name)
                    tmp_path.write_bytes(file_content_bytes)
                    file_path = tmp_path
                    is_temporary_file = True
            else:
                raise NotFoundError(
                    message=f"Document file not found: {resource.document_url}",
                    user_message="Document file not found",
                    error_code="DOCUMENT_FILE_NOT_FOUND",
                    details={"document_url": resource.document_url, "resource_id": resource_id}
                )
        else:
            is_temporary_file = file_handler.is_temporary_file(file_path)

        try:
            activity_callback("DOCUMENT_PROCESSING", f"Processing document: {file_path.name}", {"file_name": file_path.name})

            # Compute content hash for incremental update detection
            file_content_bytes = file_path.read_bytes()
            content_hash = hashlib.sha256(file_content_bytes).hexdigest()

            # Check if document is unchanged
            if checkpoint_manager.is_page_unchanged(resource_id, str(file_path), content_hash):
                activity_callback(
                    "DOCUMENT_UNCHANGED",
                    f"Document unchanged, skipping re-indexing: {file_path.name}",
                    {"file_name": file_path.name, "content_hash": content_hash},
                )
                logger.info("Document %s unchanged, skipping re-indexing", file_path.name)
                await self._update_resource_status(resource_id, progress=100.0)
                return

            if not resource.file_storage_id:
                file_id, file_hash = file_storage_service.store_file(
                    file_path=file_path,
                    resource_id=resource_id,
                    user_id=user_id,
                    filename=file_path.name,
                )

                db = mongodb_manager.get_database()
                collection = db.indexed_resources
                collection.update_one(
                    {"_id": resource_id},
                    {
                        "$set": {
                            "file_storage_id": file_id,
                            "file_hash": file_hash,
                        }
                    },
                )

            processor = DocumentProcessor()

            loop = asyncio.get_event_loop()
            doc_content = await loop.run_in_executor(
                None,
                lambda: processor.process_document(
                    content=file_path,
                    source_url=str(file_path),
                    content_type=resource.document_type or "auto",
                ),
            )

            await self._update_resource_status(resource_id, progress=30.0)

            activity_callback(
                "CONTENT_EXTRACTED",
                f"Extracted {len(doc_content.get('text', ''))} characters from document",
                {"content_length": len(doc_content.get("text", ""))},
            )

            # Use DocumentationAnalyzer (Claude Opus) instead of LLMKnowledgeExtractor (GPT-4o-mini)
            content = doc_content.get("markdown") or doc_content.get("text", "")

            doc_context = {
                "resource_id": resource_id,
                "user_id": user_id,
                "compliance_standards": resource.compliance_standards or [],
            }

            articles = await documentation_analyzer.analyze_uploaded_document(
                content=content,
                file_path=str(file_path),
                file_name=file_path.name,
                doc_context=doc_context,
                activity_callback=activity_callback,
            )

            await self._update_resource_status(resource_id, progress=70.0)

            articles_created = 0
            for article in articles:
                try:
                    contextual_description = await context_generator.generate_context(
                        article=article,
                        repo_context=None,
                    )

                    article.contextual_description = contextual_description
                    article.context_generated_at = datetime.utcnow()
                    article.context_version = "1.0"
                except Exception as e:
                    logger.warning(
                        "Failed to generate contextual description for document article %s: %s",
                        article.article_id,
                        e,
                        exc_info=True,
                    )

                await github_service._store_article(article)
                articles_created += 1

                activity_callback(
                    "ARTICLE_CREATED",
                    f"Created article: {article.title}",
                    {"article_id": article.article_id, "title": article.title},
                )

            file_size_mb = file_path.stat().st_size / (1024 * 1024) if file_path.exists() else 0.0

            try:
                from api.services.filesystem_integration import create_filesystem_entry_for_file

                stored_articles = [{"article_id": a.article_id} for a in articles]
                file_content_str = file_path.read_text(encoding="utf-8", errors="ignore") if file_path.exists() else ""

                await create_filesystem_entry_for_file(
                    resource_id=resource_id,
                    user_id=user_id,
                    file_path=Path(file_path),
                    relative_path=file_path.name,
                    file_content=file_content_str,
                    articles=stored_articles,
                    organization_id=resource.organization_id,
                    compliance_standards=resource.compliance_standards,
                    environment_name=resource.environment_name,
                )
            except Exception as e:
                logger.warning("Failed to create filesystem entry for document: %s", e)

            await self._update_resource_status(
                resource_id,
                articles_indexed=articles_created,
                storage_mb=file_size_mb,
            )

            # Organize articles into sections (same as repository indexing)
            try:
                from api.services.section_organizer import section_organizer

                activity_callback(
                    "ORGANIZING_SECTIONS",
                    "Organizing articles into sections",
                    {"articles_count": articles_created},
                )

                sections = await section_organizer.organize_components_into_sections(
                    resource_id=resource_id,
                    user_id=user_id,
                    commit_sha=None,
                    branch=None,
                )

                logger.info(
                    "Created %d sections for document resource %s",
                    len(sections),
                    resource_id,
                )

                activity_callback(
                    "SECTIONS_CREATED",
                    f"Created {len(sections)} sections",
                    {"sections_count": len(sections)},
                )
            except Exception as e:
                logger.warning(
                    "Failed to organize sections for document resource %s: %s",
                    resource_id,
                    e,
                    exc_info=True,
                )

            # Save checkpoint for successful document indexing
            checkpoint_manager.save_page_checkpoint(
                resource_id=resource_id,
                page_url=str(file_path),
                content_hash=content_hash,
                articles_created=articles_created,
                status="completed",
            )

            activity_callback(
                "CHECKPOINT_SAVED",
                f"Checkpoint saved for {file_path.name}",
                {"file_name": file_path.name, "articles": articles_created},
            )

            activity_callback(
                "INDEXING_COMPLETE",
                f"Completed indexing {file_path.name} with {articles_created} articles",
                {"articles_created": articles_created, "file_size_mb": file_size_mb},
            )

        except Exception as e:
            # Save checkpoint for failed document
            checkpoint_manager.save_page_checkpoint(
                resource_id=resource_id,
                page_url=str(file_path),
                content_hash=content_hash,
                articles_created=0,
                status="failed",
                error=str(e),
            )
            raise

        finally:
            if is_temporary_file and file_path.exists():
                file_handler.cleanup_file(file_path)
                logger.info("Cleaned up temporary file after indexing: %s", file_path)

    async def get_resource(self, resource_id: str, user_id: str) -> Optional[IndexedResource]:
        """Get resource by ID (with user ownership check).

        Args:
            resource_id: Resource ID
            user_id: User ID

        Returns:
            IndexedResource or None
        """
        db = mongodb_manager.get_database()
        collection = db.indexed_resources

        doc = collection.find_one(
            {
                "_id": resource_id,
                "user_id": ObjectId(user_id),
            }
        )

        if not doc:
            return None

        return IndexedResource.from_dict(doc)

    async def get_resource_by_id_internal(self, resource_id: str) -> Optional[IndexedResource]:
        """Get resource by ID (internal use, no ownership check).

        This is used for WebSocket updates where we've already verified connection.

        Args:
            resource_id: Resource ID

        Returns:
            IndexedResource or None
        """
        db = mongodb_manager.get_database()
        collection = db.indexed_resources

        doc = collection.find_one({"_id": resource_id})

        if not doc:
            return None

        return IndexedResource.from_dict(doc)

    async def find_resource_by_identifier(
        self,
        identifier: str,
        resource_type: ResourceType,
        user_id: str,
    ) -> Optional[IndexedResource]:
        """Find resource by identifier (repo URL, documentation URL, or resource_id).

        Args:
            identifier: Repository URL, documentation URL, document URL, or resource_id
            resource_type: Type of resource
            user_id: User ID

        Returns:
            IndexedResource or None
        """
        db = mongodb_manager.get_database()
        collection = db.indexed_resources

        query: dict[str, Any] = {
            "user_id": ObjectId(user_id),
            "resource_type": resource_type.value,
        }

        if identifier.startswith("res_"):
            query["_id"] = identifier
        elif resource_type == ResourceType.REPOSITORY:
            normalized_url = identifier.replace(".git", "").rstrip("/")
            query["repo_url"] = {"$regex": normalized_url, "$options": "i"}
        elif resource_type == ResourceType.DOCUMENTATION:
            normalized_url = identifier.rstrip("/")
            query["documentation_url"] = {"$regex": normalized_url, "$options": "i"}
        elif resource_type == ResourceType.DOCUMENT:
            query["document_url"] = identifier
        else:
            return None

        doc = collection.find_one(query)

        if not doc:
            return None

        return IndexedResource.from_dict(doc)

    async def list_resources(
        self,
        user_id: str,
        organization_id: Optional[str] = None,
        resource_type: Optional[ResourceType] = None,
        status: Optional[ResourceStatus] = None,
    ) -> list[IndexedResource]:
        """List resources for user.

        Args:
            user_id: User ID
            organization_id: Organization ID (optional)
            resource_type: Filter by resource type
            status: Filter by status

        Returns:
            List of IndexedResource
        """
        db = mongodb_manager.get_database()
        collection = db.indexed_resources

        query: dict[str, Any] = {"user_id": ObjectId(user_id)}

        if organization_id:
            query["organization_id"] = ObjectId(organization_id)

        if resource_type:
            query["resource_type"] = resource_type.value

        if status:
            query["status"] = status.value

        docs = list(collection.find(query).sort("created_at", -1))

        return [IndexedResource.from_dict(doc) for doc in docs]

    async def update_document_metadata(
        self,
        resource_id: str,
        user_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[list[str]] = None,
    ) -> Optional[IndexedResource]:
        """Update document metadata.

        Args:
            resource_id: Resource ID
            user_id: User ID
            name: Updated name
            description: Updated description
            tags: Updated tags

        Returns:
            Updated IndexedResource or None if not found
        """
        resource = await self.get_resource(resource_id, user_id)
        if not resource:
            return None

        if resource.resource_type != ResourceType.DOCUMENT:
            raise ValidationError(
                message="Resource is not a document",
                user_message="This operation is only available for document resources",
                error_code="INVALID_RESOURCE_TYPE",
                details={"resource_id": resource_id, "resource_type": resource.resource_type if hasattr(resource, 'resource_type') else None}
            )

        updates: dict[str, Any] = {"updated_at": datetime.utcnow()}
        
        if name is not None:
            updates["name"] = name
        if description is not None:
            updates["description"] = description
        if tags is not None:
            updates["tags"] = tags

        db = mongodb_manager.get_database()
        collection = db.indexed_resources

        collection.update_one(
            {"_id": resource_id, "user_id": ObjectId(user_id)},
            {"$set": updates},
        )

        logger.info("Updated document metadata: %s", resource_id)
        return await self.get_resource(resource_id, user_id)

    async def replace_document_content(
        self,
        resource_id: str,
        user_id: str,
        file_path: Path,
        re_index: bool = True,
    ) -> Optional[IndexedResource]:
        """Replace document content and optionally re-index.

        Args:
            resource_id: Resource ID
            user_id: User ID
            file_path: Path to new file
            re_index: Whether to re-index after replacement

        Returns:
            Updated IndexedResource or None if not found
        """
        from api.services.file_storage_service import file_storage_service
        import hashlib

        resource = await self.get_resource(resource_id, user_id)
        if not resource:
            return None

        if resource.resource_type != ResourceType.DOCUMENT:
            raise ValidationError(
                message="Resource is not a document",
                user_message="This operation is only available for document resources",
                error_code="INVALID_RESOURCE_TYPE",
                details={"resource_id": resource_id, "resource_type": resource.resource_type if hasattr(resource, 'resource_type') else None}
            )

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        file_content = file_path.read_bytes()
        new_hash = hashlib.sha256(file_content).hexdigest()

        if resource.file_hash == new_hash and not re_index:
            logger.info("File content unchanged, skipping replacement: %s", resource_id)
            return resource

        if resource.file_storage_id:
            file_storage_service.delete_file(resource.file_storage_id)

        file_id, file_hash = file_storage_service.store_file(
            file_path=file_path,
            resource_id=resource_id,
            user_id=user_id,
            filename=file_path.name,
        )

        version = resource.version + 1
        version_entry = {
            "version": resource.version,
            "file_hash": resource.file_hash,
            "indexed_at": resource.indexed_at.isoformat() if resource.indexed_at else None,
            "articles_count": resource.articles_indexed,
        }

        versions = resource.versions + [version_entry]
        if len(versions) > 10:
            versions = versions[-10:]

        db = mongodb_manager.get_database()
        collection = db.indexed_resources

        updates = {
            "file_storage_id": file_id,
            "file_hash": file_hash,
            "version": version,
            "versions": versions,
            "updated_at": datetime.utcnow(),
        }

        if re_index:
            updates["status"] = ResourceStatus.PENDING.value
            updates["progress"] = 0.0
            updates["articles_indexed"] = 0

            db.knowledge_articles.delete_many({"resource_id": resource_id})

        collection.update_one(
            {"_id": resource_id, "user_id": ObjectId(user_id)},
            {"$set": updates},
        )

        logger.info("Replaced document content: %s (version: %d)", resource_id, version)

        if re_index:
            plan = "professional"
            await self.start_indexing_job(
                resource_id=resource_id,
                user_id=user_id,
                plan=plan,
            )

        return await self.get_resource(resource_id, user_id)

    async def reindex_document(
        self,
        resource_id: str,
        user_id: str,
        force: bool = False,
    ) -> Optional[IndexedResource]:
        """Re-index an existing document.

        Args:
            resource_id: Resource ID
            user_id: User ID
            force: Force re-index even if content unchanged

        Returns:
            Updated IndexedResource or None if not found
        """
        from api.services.file_storage_service import file_storage_service
        import tempfile
        from pathlib import Path

        resource = await self.get_resource(resource_id, user_id)
        if not resource:
            return None

        if resource.resource_type != ResourceType.DOCUMENT:
            raise ValidationError(
                message="Resource is not a document",
                user_message="This operation is only available for document resources",
                error_code="INVALID_RESOURCE_TYPE",
                details={"resource_id": resource_id, "resource_type": resource.resource_type if hasattr(resource, 'resource_type') else None}
            )

        if not resource.file_storage_id:
            raise NotFoundError(
                message="Document file not stored in GridFS",
                user_message="Document file not found in storage",
                error_code="DOCUMENT_NOT_IN_STORAGE",
                details={"resource_id": resource_id}
            )

        file_content, metadata = file_storage_service.retrieve_file(resource.file_storage_id)

        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(metadata.get("filename", "file")).suffix) as tmp_file:
            tmp_path = Path(tmp_file.name)
            tmp_path.write_bytes(file_content)

        try:
            return await self.replace_document_content(
                resource_id=resource_id,
                user_id=user_id,
                file_path=tmp_path,
                re_index=True,
            )
        finally:
            if tmp_path.exists():
                tmp_path.unlink()

    async def cancel_indexing(self, resource_id: str, user_id: str) -> dict[str, Any]:
        """Cancel an active indexing job.

        Args:
            resource_id: Resource ID of the job to cancel
            user_id: User ID for authorization

        Returns:
            dict with status information about the cancellation
        """
        resource = await self.get_resource(resource_id, user_id)
        if not resource:
            return {
                "success": False,
                "error": "Resource not found",
                "resource_id": resource_id,
            }

        # Check if there's an active job
        if resource_id not in self.running_jobs:
            # Check if the resource status indicates it's indexing
            if resource.status in [ResourceStatus.PENDING, ResourceStatus.INDEXING]:
                # Job might have finished or crashed - update status
                await self._update_resource_status(
                    resource_id,
                    status=ResourceStatus.FAILED,
                    error_message="Indexing cancelled by user",
                )
                await self.log_activity(
                    resource_id,
                    ActivityType.INDEXING_FAILED,
                    "Indexing cancelled by user",
                )
                return {
                    "success": True,
                    "message": "Resource status updated to failed (job was not running)",
                    "resource_id": resource_id,
                    "previous_status": resource.status.value,
                }
            return {
                "success": False,
                "error": f"Resource is not being indexed (status: {resource.status.value})",
                "resource_id": resource_id,
            }

        # Cancel the running task
        task = self.running_jobs[resource_id]
        task.cancel()

        try:
            await task
        except asyncio.CancelledError:
            pass  # Expected
        except Exception as e:
            logger.warning("Error while cancelling task for %s: %s", resource_id, e)

        # Clean up
        if resource_id in self.running_jobs:
            del self.running_jobs[resource_id]
        if resource_id in self._indexing_start_times:
            del self._indexing_start_times[resource_id]

        # Update resource status
        await self._update_resource_status(
            resource_id,
            status=ResourceStatus.FAILED,
            error_message="Indexing cancelled by user",
        )

        # Log the cancellation activity
        await self.log_activity(
            resource_id,
            ActivityType.INDEXING_FAILED,
            "Indexing cancelled by user",
        )

        logger.info("Cancelled indexing job for resource: %s", resource_id)

        return {
            "success": True,
            "message": "Indexing job cancelled successfully",
            "resource_id": resource_id,
        }

    async def retry_indexing(
        self,
        resource_id: str,
        user_id: str,
        plan: str = "professional",
    ) -> dict[str, Any]:
        """Retry indexing for a failed or cancelled resource.

        Args:
            resource_id: Resource ID to retry
            user_id: User ID for authorization
            plan: User's plan

        Returns:
            dict with status information about the retry
        """
        resource = await self.get_resource(resource_id, user_id)
        if not resource:
            return {
                "success": False,
                "error": "Resource not found",
                "resource_id": resource_id,
            }

        # Only allow retry for failed resources
        if resource.status not in [ResourceStatus.FAILED]:
            return {
                "success": False,
                "error": f"Cannot retry indexing for resource in '{resource.status.value}' status. Only failed resources can be retried.",
                "resource_id": resource_id,
                "current_status": resource.status.value,
            }

        # Reset the resource status
        await self._reset_resource_for_reindex(resource_id)

        # Clear previous activities
        await self.clear_activities(resource_id)

        # Log retry activity
        await self.log_activity(
            resource_id,
            ActivityType.INDEXING_STARTED,
            "Indexing retry initiated by user",
        )

        # Start the indexing job
        try:
            job_id = await self.start_indexing_job(
                resource_id=resource_id,
                user_id=user_id,
                plan=plan,
            )

            logger.info("Retry indexing started for resource: %s, job: %s", resource_id, job_id)

            return {
                "success": True,
                "message": "Indexing retry started successfully",
                "resource_id": resource_id,
                "job_id": job_id,
            }
        except Exception as e:
            logger.error("Failed to retry indexing for %s: %s", resource_id, e)
            await self._update_resource_status(
                resource_id,
                status=ResourceStatus.FAILED,
                error_message=f"Failed to retry indexing: {str(e)}",
            )
            return {
                "success": False,
                "error": f"Failed to start indexing: {str(e)}",
                "resource_id": resource_id,
            }

    async def delete_resource(self, resource_id: str, user_id: str) -> bool:
        """Delete a resource and its indexed content.

        Args:
            resource_id: Resource ID
            user_id: User ID

        Returns:
            True if deleted, False otherwise
        """
        from api.services.file_storage_service import file_storage_service

        resource = await self.get_resource(resource_id, user_id)
        if not resource:
            return False

        if resource_id in self.running_jobs:
            task = self.running_jobs[resource_id]
            task.cancel()
            del self.running_jobs[resource_id]

        await self._update_resource_status(resource_id, status=ResourceStatus.DELETED)

        if resource.file_storage_id:
            file_storage_service.delete_file(resource.file_storage_id)

        db = mongodb_manager.get_database()

        knowledge_collection = db.knowledge_articles
        articles = list(knowledge_collection.find({"resource_id": resource_id}, {"_id": 1}))
        article_ids = [article["_id"] for article in articles]

        knowledge_collection.delete_many({"resource_id": resource_id})

        try:
            from api.services.github_service import github_service
            pinecone_index = github_service._get_pinecone_index()
            
            if article_ids:
                batch_size = 1000
                for i in range(0, len(article_ids), batch_size):
                    batch_ids = article_ids[i:i + batch_size]
                    try:
                        pinecone_index.delete(ids=batch_ids)
                        logger.info("Deleted %d vectors from Pinecone for resource %s", len(batch_ids), resource_id)
                    except Exception as e:
                        logger.warning("Error deleting Pinecone vectors for resource %s (batch %d): %s", resource_id, i // batch_size + 1, e)
        except Exception as e:
            logger.warning("Could not delete Pinecone vectors for resource %s: %s", resource_id, e)

        resources_collection = db.indexed_resources
        resources_collection.delete_one({"_id": resource_id})

        indexed_files_collection = db.indexed_files
        indexed_files_collection.delete_many({"resource_id": resource_id})

        logger.info("Deleted resource: %s (%d articles, %d vectors)", resource_id, len(article_ids), len(article_ids))

        return True

    async def _update_resource_status(
        self,
        resource_id: str,
        status: Optional[ResourceStatus] = None,
        progress: Optional[float] = None,
        error_message: Optional[str] = None,
        error_details: Optional[dict[str, Any]] = None,
        indexed_at: Optional[datetime] = None,
        articles_indexed: Optional[int] = None,
        storage_mb: Optional[float] = None,
    ) -> None:
        """Update resource status and progress.

        Args:
            resource_id: Resource ID
            status: New status
            progress: New progress percentage
            error_message: Error message (if failed)
            error_details: Error details
            indexed_at: Indexing completion time
        """
        db = mongodb_manager.get_database()
        collection = db.indexed_resources

        update: dict[str, Any] = {"updated_at": datetime.utcnow()}

        if status:
            update["status"] = status.value

        if progress is not None:
            update["progress"] = progress

        if error_message:
            update["error_message"] = error_message

        if error_details:
            update["error_details"] = error_details

        if indexed_at:
            update["indexed_at"] = indexed_at

        if articles_indexed is not None:
            update["articles_indexed"] = articles_indexed

        if storage_mb is not None:
            update["storage_mb"] = storage_mb

        collection.update_one({"_id": resource_id}, {"$set": update})

        # Broadcast progress update via WebSocket
        try:
            await self._broadcast_progress_update(
                resource_id=resource_id,
                status=status.value if status else None,
                progress=progress,
                articles_indexed=articles_indexed,
            )
        except Exception as e:
            # Don't fail the status update if WebSocket broadcast fails
            logger.debug("WebSocket broadcast failed (non-critical): %s", e)

    async def _broadcast_progress_update(
        self,
        resource_id: str,
        status: Optional[str] = None,
        progress: Optional[float] = None,
        files_processed: Optional[int] = None,
        total_files: Optional[int] = None,
        articles_indexed: Optional[int] = None,
    ) -> None:
        """Broadcast progress update via WebSocket.

        Args:
            resource_id: Resource ID
            status: Current status
            progress: Progress percentage
            files_processed: Files processed count
            total_files: Total files count
            articles_indexed: Articles indexed count
        """
        try:
            from api.routers.v1.websocket import connection_manager

            # Get user_id for the resource
            resource = await self.get_resource_by_id_internal(resource_id)
            if not resource:
                return

            user_id = str(resource.user_id) if resource.user_id else None
            current_status = status or (resource.status.value if resource.status else None)
            current_progress = progress if progress is not None else (resource.progress or 0)

            await connection_manager.broadcast_progress(
                resource_id=resource_id,
                user_id=user_id or "",
                progress=current_progress,
                status=current_status or "unknown",
                files_processed=files_processed or resource.files_processed,
                total_files=total_files or resource.total_files,
                articles_indexed=articles_indexed or resource.articles_indexed,
            )
        except ImportError:
            # WebSocket module not available
            pass
        except Exception as e:
            logger.debug("Failed to broadcast progress update: %s", e)

    async def _create_indexing_notification(
        self,
        user_id: str,
        resource_id: str,
        resource_name: str,
        notification_type: str,
        title: str,
        message: str,
    ) -> None:
        """Create in-app notification for indexing events.

        Args:
            user_id: User ID
            resource_id: Resource ID
            resource_name: Resource name
            notification_type: Type of notification (indexing_complete, indexing_failed)
            title: Notification title
            message: Notification message
        """
        try:
            db = mongodb_manager.get_database()
            notifications_collection = db.user_notifications

            notification = {
                "user_id": ObjectId(user_id),
                "type": notification_type,
                "title": title,
                "message": message,
                "resource_id": resource_id,
                "resource_name": resource_name,
                "read": False,
                "created_at": datetime.utcnow(),
            }

            notifications_collection.insert_one(notification)
            logger.info(
                "Created in-app notification for user %s: %s",
                user_id,
                notification_type,
            )
        except Exception as e:
            # Don't fail indexing if notification creation fails
            logger.warning("Failed to create indexing notification: %s", e)

    async def _update_resource_progress(self, resource_id: str, progress: float) -> None:
        """Update resource progress.

        Args:
            resource_id: Resource ID
            progress: Progress percentage (0-100)
        """
        await self._update_resource_status(resource_id, progress=progress)

    def _encrypt_token(self, token: str, resource_id: str) -> str:
        """Encrypt GitHub token for storage.

        Args:
            token: Plain token
            resource_id: Resource ID for salt generation

        Returns:
            Encrypted token

        Note: Uses resource-specific salt for enhanced security.
        """
        from api.services.token_encryption_service import TokenEncryptionService

        return TokenEncryptionService.encrypt_token(token, resource_id)

    def _decrypt_token(self, encrypted_token: str, resource_id: str) -> str:
        """Decrypt GitHub token.

        Args:
            encrypted_token: Encrypted token
            resource_id: Resource ID for salt verification

        Returns:
            Plain token

        Raises:
            ValueError: If decryption fails (e.g., old token format)
        """
        from api.services.token_encryption_service import TokenEncryptionService

        try:
            return TokenEncryptionService.decrypt_token(encrypted_token, resource_id)
        except ValueError:
            logger.warning(
                "Failed to decrypt token with new method, trying legacy method for resource %s",
                resource_id
            )
            return self._decrypt_token_legacy(encrypted_token)

    def _decrypt_token_legacy(self, encrypted_token: str) -> str:
        """Decrypt token using legacy method (for backward compatibility).

        Args:
            encrypted_token: Encrypted token (old format)

        Returns:
            Plain token

        Note: This method supports old tokens encrypted with hardcoded salt.
        Should only be used during migration period.
        """
        from api.config import settings
        from cryptography.fernet import Fernet
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        import base64

        password = settings.secret_key.encode()
        salt = b"wistx_github_token_salt"
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        fernet = Fernet(key)
        return fernet.decrypt(encrypted_token.encode()).decode()

    async def _get_processed_files(
        self,
        resource_id: str,
        commit_sha: str,
    ) -> list[dict[str, Any]]:
        """Get processed files for a resource and commit.
        
        Args:
            resource_id: Resource ID
            commit_sha: Commit SHA
            
        Returns:
            List of processed file dictionaries
        """
        db = mongodb_manager.get_database()
        collection = db.indexed_files
        
        cursor = collection.find({
            "resource_id": resource_id,
            "commit_sha": commit_sha,
        })
        
        return [doc for doc in cursor]

    async def _save_file_checkpoint(
        self,
        resource_id: str,
        file_path: str,
        commit_sha: str,
        file_hash: str,
        articles_created: int = 0,
        file_size_mb: float = 0.0,
        status: str = "completed",
        error: Optional[str] = None,
    ) -> None:
        """Save file processing checkpoint.
        
        Args:
            resource_id: Resource ID
            file_path: Relative file path
            commit_sha: Commit SHA
            file_hash: File content hash
            articles_created: Number of articles created
            file_size_mb: File size in MB
            status: Processing status
            error: Error message if failed
        """
        from datetime import datetime
        
        db = mongodb_manager.get_database()
        collection = db.indexed_files
        
        checkpoint = {
            "resource_id": resource_id,
            "file_path": file_path,
            "commit_sha": commit_sha,
            "file_hash": file_hash,
            "articles_created": articles_created,
            "file_size_mb": file_size_mb,
            "status": status,
            "error": error,
            "processed_at": datetime.utcnow(),
        }
        
        collection.update_one(
            {
                "resource_id": resource_id,
                "file_path": file_path,
                "commit_sha": commit_sha,
            },
            {"$set": checkpoint},
            upsert=True,
        )

    def _aggregate_processed_stats(
        self,
        processed_files: list[dict[str, Any]],
    ) -> tuple[int, int, float]:
        """Aggregate statistics from processed files.
        
        Args:
            processed_files: List of processed file dictionaries
            
        Returns:
            Tuple of (articles_created, files_processed, total_size_mb)
        """
        articles_created = sum(f.get("articles_created", 0) for f in processed_files)
        files_processed = len([f for f in processed_files if f.get("status") == "completed"])
        total_size_mb = sum(f.get("file_size_mb", 0.0) for f in processed_files)
        
        return articles_created, files_processed, total_size_mb


indexing_service = IndexingService()

