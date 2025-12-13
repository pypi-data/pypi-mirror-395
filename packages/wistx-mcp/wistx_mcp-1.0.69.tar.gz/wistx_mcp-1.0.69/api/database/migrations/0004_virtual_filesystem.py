"""Migration 0004: Virtual filesystem for infrastructure-aware navigation.

Adds:
1. virtual_filesystem collection for filesystem entries
2. Indexes for efficient path-based queries
3. Optional fields to indexed_resources and indexed_files for filesystem linking
"""

import logging

from api.database.migrations.base_migration import BaseMigration
from pymongo.database import Database

logger = logging.getLogger(__name__)


class Migration0004VirtualFilesystem(BaseMigration):
    """Migration for virtual filesystem collection."""

    @property
    def version(self) -> int:
        """Migration version."""
        return 4

    @property
    def description(self) -> str:
        """Migration description."""
        return "Virtual filesystem for infrastructure-aware navigation - add virtual_filesystem collection and indexes"

    async def up(self, db: Database) -> None:
        """Apply migration."""
        logger.info("Running migration 0004: Virtual filesystem...")

        collection = db.virtual_filesystem

        logger.info("Creating indexes for virtual_filesystem collection...")

        try:
            collection.create_index(
                [("resource_id", 1), ("path", 1)],
                unique=True,
                name="unique_path_per_resource",
                background=True,
            )
            logger.info("Created unique_path_per_resource index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            collection.create_index(
                [("resource_id", 1), ("parent_path", 1)],
                name="parent_path_lookup",
                background=True,
            )
            logger.info("Created parent_path_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            collection.create_index(
                [("user_id", 1), ("resource_id", 1)],
                name="user_resource_lookup",
                background=True,
            )
            logger.info("Created user_resource_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            collection.create_index(
                [("entry_type", 1), ("resource_id", 1)],
                name="entry_type_lookup",
                background=True,
            )
            logger.info("Created entry_type_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            collection.create_index(
                [
                    ("infrastructure_metadata.resource_type", 1),
                    ("infrastructure_metadata.cloud_provider", 1),
                ],
                name="infrastructure_lookup",
                background=True,
            )
            logger.info("Created infrastructure_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            collection.create_index(
                [("article_id", 1)],
                name="article_lookup",
                background=True,
            )
            logger.info("Created article_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            collection.create_index(
                [("indexed_file_id", 1)],
                name="indexed_file_lookup",
                background=True,
            )
            logger.info("Created indexed_file_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            collection.create_index(
                [("tags", 1)],
                name="tags_lookup",
                background=True,
            )
            logger.info("Created tags_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        logger.info("Migration 0004 completed successfully")

    async def down(self, db: Database) -> None:
        """Rollback migration."""
        logger.info("Rolling back migration 0004: Virtual filesystem...")

        collection = db.virtual_filesystem

        try:
            collection.drop_index("unique_path_per_resource")
            collection.drop_index("parent_path_lookup")
            collection.drop_index("user_resource_lookup")
            collection.drop_index("entry_type_lookup")
            collection.drop_index("infrastructure_lookup")
            collection.drop_index("article_lookup")
            collection.drop_index("indexed_file_lookup")
            collection.drop_index("tags_lookup")
            logger.info("Dropped virtual_filesystem indexes")
        except Exception as e:
            logger.warning("Index drop failed: %s", e)

        logger.info("Migration 0004 rollback completed")

