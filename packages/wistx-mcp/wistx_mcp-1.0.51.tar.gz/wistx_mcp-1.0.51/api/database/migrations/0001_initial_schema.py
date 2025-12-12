"""Initial schema migration - creates all collections and indexes."""

import logging
import sys
from pathlib import Path

from api.database.migrations.base_migration import BaseMigration
from pymongo.database import Database

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

logger = logging.getLogger(__name__)


class Migration0001InitialSchema(BaseMigration):
    """Initial schema migration.

    Creates all collections and indexes as defined in setup_mongodb.py.
    This migration is idempotent - it can be run multiple times safely.
    """

    @property
    def version(self) -> int:
        """Migration version."""
        return 1

    @property
    def description(self) -> str:
        """Migration description."""
        return "Initial schema - create all collections and indexes"

    async def up(self, db: Database) -> None:
        """Apply migration."""
        from scripts.setup_mongodb import create_collections, create_indexes

        logger.info("Running initial schema migration...")
        create_collections()
        create_indexes()
        logger.info("Initial schema migration complete")

    async def down(self, db: Database) -> None:
        """Rollback migration."""
        collections_to_drop = [
            "compliance_controls",
            "pricing_data",
            "code_examples",
            "best_practices",
            "knowledge_articles",
            "users",
            "api_keys",
            "api_usage",
            "user_usage_summary",
            "security_knowledge",
            "template_registry",
            "template_ratings",
            "template_analytics",
            "troubleshooting_incidents",
            "solution_knowledge",
            "quality_templates",
        ]

        for collection_name in collections_to_drop:
            if collection_name in db.list_collection_names():
                db.drop_collection(collection_name)

