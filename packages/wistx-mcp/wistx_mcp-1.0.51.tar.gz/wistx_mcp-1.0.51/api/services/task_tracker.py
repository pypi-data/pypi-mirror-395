"""Task tracking service for agent improvement measurement."""

import logging
import secrets
from datetime import datetime
from typing import Any, Optional

from bson import ObjectId

from api.database.mongodb import mongodb_manager
from api.models.task_tracking import TaskMetrics, TaskRecord, ValidationResults

logger = logging.getLogger(__name__)


class TaskTracker:
    """Service for tracking agent task performance."""

    async def start_task(
        self,
        user_id: str,
        task_type: str,
        task_description: str,
        wistx_enabled: bool,
    ) -> str:
        """Start tracking a new task.

        Args:
            user_id: User ID
            task_type: Task type (compliance, pricing, code_generation, best_practices)
            task_description: Task description
            wistx_enabled: Whether WISTX is enabled

        Returns:
            Task ID
        """
        task_id = f"task_{secrets.token_hex(12)}"
        db = mongodb_manager.get_database()
        collection = db.agent_tasks

        task_record = TaskRecord(
            task_id=task_id,
            user_id=user_id,
            task_type=task_type,
            task_description=task_description,
            wistx_enabled=wistx_enabled,
            start_time=datetime.utcnow(),
            status="in_progress",
            attempts=1,
        )

        try:
            collection.insert_one(task_record.model_dump())
            logger.info("Started tracking task %s (type: %s, WISTX: %s)", task_id, task_type, wistx_enabled)
        except Exception as e:
            logger.error("Failed to start task tracking: %s", e, exc_info=True)
            raise

        return task_id

    async def record_tool_usage(self, task_id: str, tool_name: str) -> None:
        """Record WISTX tool usage for a task.

        Args:
            task_id: Task ID
            tool_name: Name of WISTX tool used
        """
        db = mongodb_manager.get_database()
        collection = db.agent_tasks

        try:
            collection.update_one(
                {"task_id": task_id},
                {"$addToSet": {"wistx_tools_used": tool_name}},
            )
            logger.debug("Recorded tool usage: task=%s, tool=%s", task_id, tool_name)
        except Exception as e:
            logger.error("Failed to record tool usage: %s", e, exc_info=True)

    async def record_attempt(self, task_id: str) -> None:
        """Record an additional attempt for a task.

        Args:
            task_id: Task ID
        """
        db = mongodb_manager.get_database()
        collection = db.agent_tasks

        try:
            collection.update_one(
                {"task_id": task_id},
                {"$inc": {"attempts": 1}},
            )
            logger.debug("Recorded attempt: task=%s", task_id)
        except Exception as e:
            logger.error("Failed to record attempt: %s", e, exc_info=True)

    async def complete_task(
        self,
        task_id: str,
        status: str,
        metrics: Optional[TaskMetrics] = None,
        generated_code: Optional[str] = None,
        validation_results: Optional[ValidationResults] = None,
    ) -> None:
        """Complete a task and record final metrics.

        Args:
            task_id: Task ID
            status: Task status (completed, failed)
            metrics: Task metrics
            generated_code: Generated code (if applicable)
            validation_results: Validation results
        """
        db = mongodb_manager.get_database()
        collection = db.agent_tasks

        end_time = datetime.utcnow()

        update_data: dict[str, Any] = {
            "end_time": end_time,
            "status": status,
        }

        task = await self.get_task(task_id)
        if task:
            start_time = task["start_time"]
            duration = (end_time - start_time).total_seconds()
            update_data["duration_seconds"] = duration

        if metrics:
            update_data["metrics"] = metrics.model_dump()

        if generated_code:
            update_data["generated_code"] = generated_code

        if validation_results:
            update_data["validation_results"] = validation_results.model_dump()

        try:
            collection.update_one({"task_id": task_id}, {"$set": update_data})
            logger.info(
                "Completed task %s (status: %s, duration: %.2fs)",
                task_id,
                status,
                update_data.get("duration_seconds", 0),
            )
        except Exception as e:
            logger.error("Failed to complete task: %s", e, exc_info=True)
            raise

    async def record_user_feedback(
        self,
        task_id: str,
        rating: int,
        comments: Optional[str] = None,
    ) -> None:
        """Record user feedback for a task.

        Args:
            task_id: Task ID
            rating: User rating (1-5)
            comments: Optional comments
        """
        db = mongodb_manager.get_database()
        collection = db.agent_tasks

        feedback = {
            "rating": rating,
            "timestamp": datetime.utcnow(),
        }

        if comments:
            feedback["comments"] = comments

        try:
            collection.update_one(
                {"task_id": task_id},
                {"$set": {"user_feedback": feedback}},
            )
            logger.info("Recorded user feedback: task=%s, rating=%d", task_id, rating)
        except Exception as e:
            logger.error("Failed to record user feedback: %s", e, exc_info=True)

    async def get_task(self, task_id: str) -> Optional[dict[str, Any]]:
        """Get a task record.

        Args:
            task_id: Task ID

        Returns:
            Task record or None
        """
        db = mongodb_manager.get_database()
        collection = db.agent_tasks

        try:
            task = collection.find_one({"task_id": task_id})
            if task and "_id" in task:
                task["_id"] = str(task["_id"])
            return task
        except Exception as e:
            logger.error("Failed to get task: %s", e, exc_info=True)
            return None

    async def get_tasks(
        self,
        user_id: Optional[str] = None,
        task_type: Optional[str] = None,
        wistx_enabled: Optional[bool] = None,
        status: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Get tasks matching criteria.

        Args:
            user_id: Filter by user ID
            task_type: Filter by task type
            wistx_enabled: Filter by WISTX enabled status
            status: Filter by status
            start_date: Filter by start date
            end_date: Filter by end date
            limit: Maximum number of results

        Returns:
            List of task records
        """
        db = mongodb_manager.get_database()
        collection = db.agent_tasks

        query: dict[str, Any] = {}

        if user_id:
            query["user_id"] = user_id

        if task_type:
            query["task_type"] = task_type

        if wistx_enabled is not None:
            query["wistx_enabled"] = wistx_enabled

        if status:
            query["status"] = status

        if start_date or end_date:
            query["start_time"] = {}
            if start_date:
                query["start_time"]["$gte"] = start_date
            if end_date:
                query["start_time"]["$lte"] = end_date

        try:
            tasks = list(collection.find(query).sort("start_time", -1).limit(limit))
            for task in tasks:
                if "_id" in task:
                    task["_id"] = str(task["_id"])
            return tasks
        except Exception as e:
            logger.error("Failed to get tasks: %s", e, exc_info=True)
            return []


task_tracker = TaskTracker()

