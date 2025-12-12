"""Pipeline progress tracking and checkpoint management."""

from datetime import datetime
from typing import Any

from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class PipelineProgress:
    """Track pipeline progress for resume capability.
    
    Stores checkpoints in MongoDB to enable resuming failed pipelines.
    Each checkpoint contains:
    - Pipeline ID
    - Stage (collection, processing, embedding, loading)
    - Processed URLs/articles
    - Statistics
    - Timestamp
    """

    def __init__(self, pipeline_id: str, collection_name: str = "pipeline_progress"):
        """Initialize pipeline progress tracker.
        
        Args:
            pipeline_id: Unique pipeline identifier
            collection_name: MongoDB collection name for progress storage
        """
        self.pipeline_id = pipeline_id
        self.collection_name = collection_name
        self._db = None
        self._collection = None

    def _get_collection(self):
        """Get MongoDB collection (lazy initialization).
        
        Returns:
            MongoDB collection for progress storage
        """
        if self._collection is None:
            from api.database.mongodb import mongodb_manager
            
            mongodb_manager.connect()
            self._db = mongodb_manager.get_database()
            self._collection = self._db[self.collection_name]
            
            self._collection.create_index(
                [("pipeline_id", 1), ("stage", 1)],
                unique=True,
                background=True
            )
            self._collection.create_index(
                [("pipeline_id", 1), ("timestamp", -1)],
                background=True
            )
        
        return self._collection

    async def save_checkpoint(
        self,
        stage: str,
        stats: dict[str, Any],
        processed_urls: list[str] | None = None,
        processed_articles: list[dict[str, Any]] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Save checkpoint for a pipeline stage.
        
        Args:
            stage: Pipeline stage name (collection, processing, embedding, loading)
            stats: Pipeline statistics dictionary
            processed_urls: List of processed URLs (for collection stage)
            processed_articles: List of processed article IDs (for processing stage)
            metadata: Additional metadata to store
        """
        try:
            collection = self._get_collection()
            
            checkpoint = {
                "pipeline_id": self.pipeline_id,
                "stage": stage,
                "stats": stats.copy(),
                "timestamp": datetime.utcnow(),
            }
            
            if processed_urls is not None:
                checkpoint["processed_urls"] = processed_urls
            
            if processed_articles is not None:
                checkpoint["processed_articles"] = processed_articles
            
            if metadata is not None:
                checkpoint["metadata"] = metadata
            
            collection.update_one(
                {"pipeline_id": self.pipeline_id, "stage": stage},
                {"$set": checkpoint},
                upsert=True,
            )
            
            logger.debug(
                "Saved checkpoint for pipeline %s, stage %s",
                self.pipeline_id,
                stage
            )
        except Exception as e:
            logger.warning(
                "Failed to save checkpoint for pipeline %s, stage %s: %s",
                self.pipeline_id,
                stage,
                e
            )

    async def load_checkpoint(self, stage: str) -> dict[str, Any] | None:
        """Load checkpoint for a pipeline stage.
        
        Args:
            stage: Pipeline stage name
            
        Returns:
            Checkpoint dictionary or None if not found
        """
        try:
            collection = self._get_collection()
            checkpoint = collection.find_one(
                {"pipeline_id": self.pipeline_id, "stage": stage}
            )
            
            if checkpoint:
                checkpoint.pop("_id", None)
                logger.info(
                    "Loaded checkpoint for pipeline %s, stage %s",
                    self.pipeline_id,
                    stage
                )
                return checkpoint
            
            return None
        except Exception as e:
            logger.warning(
                "Failed to load checkpoint for pipeline %s, stage %s: %s",
                self.pipeline_id,
                stage,
                e
            )
            return None

    async def get_latest_checkpoint(self) -> dict[str, Any] | None:
        """Get the latest checkpoint across all stages.
        
        Returns:
            Latest checkpoint dictionary or None if not found
        """
        try:
            collection = self._get_collection()
            checkpoint = collection.find_one(
                {"pipeline_id": self.pipeline_id},
                sort=[("timestamp", -1)]
            )
            
            if checkpoint:
                checkpoint.pop("_id", None)
                return checkpoint
            
            return None
        except Exception as e:
            logger.warning(
                "Failed to get latest checkpoint for pipeline %s: %s",
                self.pipeline_id,
                e
            )
            return None

    async def get_all_checkpoints(self) -> list[dict[str, Any]]:
        """Get all checkpoints for this pipeline.
        
        Returns:
            List of checkpoint dictionaries
        """
        try:
            collection = self._get_collection()
            checkpoints = list(
                collection.find(
                    {"pipeline_id": self.pipeline_id}
                ).sort("timestamp", 1)
            )
            
            for checkpoint in checkpoints:
                checkpoint.pop("_id", None)
            
            return checkpoints
        except Exception as e:
            logger.warning(
                "Failed to get all checkpoints for pipeline %s: %s",
                self.pipeline_id,
                e
            )
            return []

    async def clear_checkpoints(self) -> None:
        """Clear all checkpoints for this pipeline."""
        try:
            collection = self._get_collection()
            collection.delete_many({"pipeline_id": self.pipeline_id})
            logger.info("Cleared all checkpoints for pipeline %s", self.pipeline_id)
        except Exception as e:
            logger.warning(
                "Failed to clear checkpoints for pipeline %s: %s",
                self.pipeline_id,
                e
            )

    async def update_checkpoint_stats(
        self,
        stage: str,
        stats_updates: dict[str, Any],
    ) -> None:
        """Update statistics in an existing checkpoint.
        
        Args:
            stage: Pipeline stage name
            stats_updates: Dictionary of statistics to update
        """
        try:
            collection = self._get_collection()
            collection.update_one(
                {"pipeline_id": self.pipeline_id, "stage": stage},
                {
                    "$set": {
                        "stats": stats_updates,
                        "timestamp": datetime.utcnow(),
                    }
                },
            )
            logger.debug(
                "Updated checkpoint stats for pipeline %s, stage %s",
                self.pipeline_id,
                stage
            )
        except Exception as e:
            logger.warning(
                "Failed to update checkpoint stats for pipeline %s, stage %s: %s",
                self.pipeline_id,
                stage,
                e
            )

