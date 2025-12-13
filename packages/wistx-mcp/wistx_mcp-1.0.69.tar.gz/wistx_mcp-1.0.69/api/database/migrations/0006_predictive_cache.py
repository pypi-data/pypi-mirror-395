"""Migration 0006: Predictive caching.

Adds:
1. cache_entries collection for cache storage
2. dependencies collection for dependency tracking
3. usage_patterns collection for usage pattern tracking
4. Indexes for efficient queries
"""

import logging
import secrets

from api.database.migrations.base_migration import BaseMigration
from pymongo.database import Database

logger = logging.getLogger(__name__)


class Migration0006PredictiveCache(BaseMigration):
    """Migration for predictive caching."""

    @property
    def version(self) -> int:
        """Migration version."""
        return 6

    @property
    def description(self) -> str:
        """Migration description."""
        return "Predictive caching - add cache_entries, dependencies, and usage_patterns collections with indexes"

    async def up(self, db: Database) -> None:
        """Apply migration."""
        logger.info("Running migration 0006: Predictive caching...")

        cache_collection = db.cache_entries
        dependencies_collection = db.dependencies
        usage_patterns_collection = db.usage_patterns

        logger.info("Creating indexes for cache_entries collection...")

        try:
            cache_collection.create_index(
                [("user_id", 1), ("resource_id", 1), ("key", 1)],
                unique=True,
                name="unique_user_resource_key",
                background=True,
            )
            logger.info("Created unique_user_resource_key index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            cache_collection.create_index(
                [("user_id", 1), ("status", 1), ("expires_at", 1)],
                name="user_status_expires_lookup",
                background=True,
            )
            logger.info("Created user_status_expires_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            cache_collection.create_index(
                [("resource_id", 1), ("entry_type", 1)],
                name="resource_type_lookup",
                background=True,
            )
            logger.info("Created resource_type_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            cache_collection.create_index(
                [("last_accessed_at", -1)],
                name="last_accessed_lookup",
                background=True,
            )
            logger.info("Created last_accessed_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        logger.info("Creating indexes for dependencies collection...")

        try:
            dependencies_collection.create_index(
                [("resource_id", 1), ("source_path", 1), ("target_path", 1)],
                unique=True,
                name="unique_resource_source_target",
                background=True,
            )
            logger.info("Created unique_resource_source_target index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            dependencies_collection.create_index(
                [("resource_id", 1), ("source_path", 1)],
                name="resource_source_lookup",
                background=True,
            )
            logger.info("Created resource_source_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            dependencies_collection.create_index(
                [("resource_id", 1), ("target_path", 1)],
                name="resource_target_lookup",
                background=True,
            )
            logger.info("Created resource_target_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            dependencies_collection.create_index(
                [("dependency_type", 1)],
                name="dependency_type_lookup",
                background=True,
            )
            logger.info("Created dependency_type_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        logger.info("Creating indexes for usage_patterns collection...")

        try:
            usage_patterns_collection.create_index(
                [("user_id", 1), ("resource_id", 1), ("path", 1)],
                unique=True,
                name="unique_user_resource_path",
                background=True,
            )
            logger.info("Created unique_user_resource_path index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            usage_patterns_collection.create_index(
                [("resource_id", 1), ("access_type", 1)],
                name="resource_access_type_lookup",
                background=True,
            )
            logger.info("Created resource_access_type_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            usage_patterns_collection.create_index(
                [("last_accessed_at", -1)],
                name="pattern_last_accessed_lookup",
                background=True,
            )
            logger.info("Created pattern_last_accessed_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        logger.info("Migration 0006 completed successfully")

    async def down(self, db: Database) -> None:
        """Rollback migration."""
        logger.info("Rolling back migration 0006: Predictive caching...")

        cache_collection = db.cache_entries
        dependencies_collection = db.dependencies
        usage_patterns_collection = db.usage_patterns

        try:
            cache_collection.drop_index("unique_user_resource_key")
            cache_collection.drop_index("user_status_expires_lookup")
            cache_collection.drop_index("resource_type_lookup")
            cache_collection.drop_index("last_accessed_lookup")
            logger.info("Dropped cache_entries indexes")
        except Exception as e:
            logger.warning("Index drop failed: %s", e)

        try:
            dependencies_collection.drop_index("unique_resource_source_target")
            dependencies_collection.drop_index("resource_source_lookup")
            dependencies_collection.drop_index("resource_target_lookup")
            dependencies_collection.drop_index("dependency_type_lookup")
            logger.info("Dropped dependencies indexes")
        except Exception as e:
            logger.warning("Index drop failed: %s", e)

        try:
            usage_patterns_collection.drop_index("unique_user_resource_path")
            usage_patterns_collection.drop_index("resource_access_type_lookup")
            usage_patterns_collection.drop_index("pattern_last_accessed_lookup")
            logger.info("Dropped usage_patterns indexes")
        except Exception as e:
            logger.warning("Index drop failed: %s", e)

        logger.info("Migration 0006 rollback completed")

