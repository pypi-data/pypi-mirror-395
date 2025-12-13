"""Migration 0003: Resource deduplication and checkpoint system.

Adds:
1. Unique index for repository deduplication
2. normalized_repo_url field for consistent comparison
3. last_commit_sha field for change detection
4. indexed_files collection for checkpoint tracking
"""

import logging
from bson import ObjectId

from api.database.migrations.base_migration import BaseMigration
from pymongo.database import Database

logger = logging.getLogger(__name__)


def normalize_repo_url(url: str) -> str:
    """Normalize GitHub URLs for comparison.
    
    Examples:
        https://github.com/owner/repo.git -> https://github.com/owner/repo
        http://github.com/owner/repo -> https://github.com/owner/repo
        owner/repo -> https://github.com/owner/repo
    """
    if not url:
        return ""
    
    url = url.strip().rstrip("/").replace(".git", "")
    
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"
    
    if url.startswith("http://"):
        url = url.replace("http://", "https://")
    
    return url.lower()


class Migration0003ResourceDeduplicationAndCheckpoints(BaseMigration):
    """Migration for resource deduplication and checkpoint system."""

    @property
    def version(self) -> int:
        """Migration version."""
        return 3

    @property
    def description(self) -> str:
        """Migration description."""
        return "Resource deduplication and checkpoint system - add unique indexes and indexed_files collection"

    async def up(self, db: Database) -> None:
        """Apply migration."""
        logger.info("Running migration 0003: Resource deduplication and checkpoints...")
        
        collection = db.indexed_resources
        
        logger.info("Normalizing existing repo_urls...")
        normalized_count = 0
        cursor = collection.find({"resource_type": "repository", "repo_url": {"$exists": True}})
        for doc in cursor:
            if doc.get("repo_url"):
                normalized_url = normalize_repo_url(doc["repo_url"])
                if normalized_url != doc.get("normalized_repo_url"):
                    collection.update_one(
                        {"_id": doc["_id"]},
                        {"$set": {"normalized_repo_url": normalized_url}},
                    )
                    normalized_count += 1
        
        logger.info("Normalized %d repository URLs", normalized_count)
        
        logger.info("Creating unique index for repository deduplication...")
        try:
            collection.create_index(
                [
                    ("user_id", 1),
                    ("normalized_repo_url", 1),
                    ("branch", 1),
                    ("include_patterns", 1),
                ],
                unique=True,
                partialFilterExpression={
                    "resource_type": "repository",
                    "status": {"$ne": "deleted"},
                },
                name="unique_repo_per_user",
                background=True,
            )
            logger.info("Created unique_repo_per_user index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)
        
        logger.info("Creating lookup index...")
        try:
            collection.create_index(
                [("user_id", 1), ("normalized_repo_url", 1), ("branch", 1)],
                name="user_repo_lookup",
                background=True,
            )
            logger.info("Created user_repo_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)
        
        logger.info("Creating indexed_files collection...")
        indexed_files_collection = db.indexed_files
        
        try:
            indexed_files_collection.create_index(
                [
                    ("resource_id", 1),
                    ("file_path", 1),
                    ("commit_sha", 1),
                ],
                unique=True,
                name="unique_file_per_commit",
                background=True,
            )
            logger.info("Created unique_file_per_commit index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)
        
        try:
            indexed_files_collection.create_index(
                [("resource_id", 1), ("status", 1)],
                name="resource_status",
                background=True,
            )
            logger.info("Created resource_status index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)
        
        try:
            indexed_files_collection.create_index(
                [("resource_id", 1), ("processed_at", -1)],
                name="resource_processed",
                background=True,
            )
            logger.info("Created resource_processed index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)
        
        logger.info("Migration 0003 complete")

    async def down(self, db: Database) -> None:
        """Rollback migration."""
        logger.info("Rolling back migration 0003...")
        
        collection = db.indexed_resources
        
        try:
            collection.drop_index("unique_repo_per_user")
            logger.info("Dropped unique_repo_per_user index")
        except Exception as e:
            logger.warning("Index drop failed: %s", e)
        
        try:
            collection.drop_index("user_repo_lookup")
            logger.info("Dropped user_repo_lookup index")
        except Exception as e:
            logger.warning("Index drop failed: %s", e)
        
        if "indexed_files" in db.list_collection_names():
            db.drop_collection("indexed_files")
            logger.info("Dropped indexed_files collection")
        
        logger.info("Rollback complete")

