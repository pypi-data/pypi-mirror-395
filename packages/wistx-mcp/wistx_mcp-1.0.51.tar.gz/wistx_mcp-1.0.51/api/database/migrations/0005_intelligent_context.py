"""Migration 0005: Intelligent context management.

Adds:
1. contexts collection for persistent context storage
2. context_links collection for context relationships
3. Indexes for efficient queries and graph traversal
"""

import logging
import secrets

from api.database.migrations.base_migration import BaseMigration
from pymongo.database import Database

logger = logging.getLogger(__name__)


def generate_context_id() -> str:
    """Generate unique context ID.

    Returns:
        Unique context ID (e.g., 'ctx_abc123')
    """
    random_part = secrets.token_urlsafe(8)[:8]
    return f"ctx_{random_part}"


class Migration0005IntelligentContext(BaseMigration):
    """Migration for intelligent context management."""

    @property
    def version(self) -> int:
        """Migration version."""
        return 5

    @property
    def description(self) -> str:
        """Migration description."""
        return "Intelligent context management - add contexts and context_links collections with indexes"

    async def up(self, db: Database) -> None:
        """Apply migration."""
        logger.info("Running migration 0005: Intelligent context management...")

        contexts_collection = db.contexts
        context_links_collection = db.context_links

        logger.info("Creating indexes for contexts collection...")

        try:
            contexts_collection.create_index(
                [("user_id", 1), ("context_type", 1)],
                name="user_type_lookup",
                background=True,
            )
            logger.info("Created user_type_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            contexts_collection.create_index(
                [("user_id", 1), ("status", 1), ("created_at", -1)],
                name="user_status_created_lookup",
                background=True,
            )
            logger.info("Created user_status_created_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            contexts_collection.create_index(
                [("organization_id", 1), ("status", 1)],
                name="org_status_lookup",
                background=True,
            )
            logger.info("Created org_status_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            contexts_collection.create_index(
                [("linked_resources", 1)],
                name="linked_resources_lookup",
                background=True,
            )
            logger.info("Created linked_resources_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            contexts_collection.create_index(
                [("linked_contexts", 1)],
                name="linked_contexts_lookup",
                background=True,
            )
            logger.info("Created linked_contexts_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            contexts_collection.create_index(
                [("tags", 1)],
                name="tags_lookup",
                background=True,
            )
            logger.info("Created tags_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            contexts_collection.create_index(
                [("workspace", 1), ("user_id", 1)],
                name="workspace_lookup",
                background=True,
            )
            logger.info("Created workspace_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            contexts_collection.create_index(
                [("analysis.analyzed_at", -1)],
                name="analysis_date_lookup",
                background=True,
            )
            logger.info("Created analysis_date_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        logger.info("Creating indexes for context_links collection...")

        try:
            context_links_collection.create_index(
                [("source_context_id", 1), ("target_context_id", 1)],
                unique=True,
                name="unique_context_link",
                background=True,
            )
            logger.info("Created unique_context_link index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            context_links_collection.create_index(
                [("source_context_id", 1)],
                name="source_context_lookup",
                background=True,
            )
            logger.info("Created source_context_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            context_links_collection.create_index(
                [("target_context_id", 1)],
                name="target_context_lookup",
                background=True,
            )
            logger.info("Created target_context_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            context_links_collection.create_index(
                [("relationship_type", 1)],
                name="relationship_type_lookup",
                background=True,
            )
            logger.info("Created relationship_type_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        logger.info("Migration 0005 completed successfully")

    async def down(self, db: Database) -> None:
        """Rollback migration."""
        logger.info("Rolling back migration 0005: Intelligent context management...")

        contexts_collection = db.contexts
        context_links_collection = db.context_links

        try:
            contexts_collection.drop_index("user_type_lookup")
            contexts_collection.drop_index("user_status_created_lookup")
            contexts_collection.drop_index("org_status_lookup")
            contexts_collection.drop_index("linked_resources_lookup")
            contexts_collection.drop_index("linked_contexts_lookup")
            contexts_collection.drop_index("tags_lookup")
            contexts_collection.drop_index("workspace_lookup")
            contexts_collection.drop_index("analysis_date_lookup")
            logger.info("Dropped contexts indexes")
        except Exception as e:
            logger.warning("Index drop failed: %s", e)

        try:
            context_links_collection.drop_index("unique_context_link")
            context_links_collection.drop_index("source_context_lookup")
            context_links_collection.drop_index("target_context_lookup")
            context_links_collection.drop_index("relationship_type_lookup")
            logger.info("Dropped context_links indexes")
        except Exception as e:
            logger.warning("Index drop failed: %s", e)

        logger.info("Migration 0005 rollback completed")

