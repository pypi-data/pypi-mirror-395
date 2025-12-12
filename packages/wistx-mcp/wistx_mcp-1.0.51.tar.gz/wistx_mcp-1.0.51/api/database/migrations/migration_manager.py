"""MongoDB migration manager."""

import logging

from pymongo.database import Database
from pymongo.errors import PyMongoError

from api.database.mongodb import mongodb_manager
from api.database.migrations.base_migration import BaseMigration

logger = logging.getLogger(__name__)

MIGRATIONS_COLLECTION = "_migrations"


class MigrationManager:
    """Manages MongoDB migrations.

    Tracks applied migrations in a `_migrations` collection.
    Migrations are applied in version order (ascending).
    """

    def __init__(self, db: Database | None = None):
        """Initialize migration manager.

        Args:
            db: MongoDB database instance (uses mongodb_manager if not provided)
        """
        self.db = db or mongodb_manager.get_database()
        self._ensure_migrations_collection()

    def _ensure_migrations_collection(self) -> None:
        """Ensure migrations collection exists."""
        if MIGRATIONS_COLLECTION not in self.db.list_collection_names():
            self.db.create_collection(MIGRATIONS_COLLECTION)
            logger.info("Created migrations collection: %s", MIGRATIONS_COLLECTION)

    async def get_applied_versions(self) -> list[int]:
        """Get list of applied migration versions.

        Returns:
            List of applied migration version numbers
        """
        try:
            applied = self.db[MIGRATIONS_COLLECTION].find(
                {}, {"version": 1, "_id": 0}
            ).sort("version", 1)
            return [doc["version"] for doc in applied]
        except PyMongoError as e:
            logger.error("Failed to get applied migrations: %s", e)
            return []

    async def is_applied(self, migration: BaseMigration) -> bool:
        """Check if a migration has been applied.

        Args:
            migration: Migration instance

        Returns:
            True if migration is applied, False otherwise
        """
        try:
            result = self.db[MIGRATIONS_COLLECTION].find_one({"version": migration.version})
            return result is not None
        except PyMongoError as e:
            logger.error("Failed to check if migration is applied: %s", e)
            return False

    async def apply(self, migration: BaseMigration) -> None:
        """Apply a migration.

        Args:
            migration: Migration instance to apply

        Raises:
            ValueError: If migration version is already applied
            Exception: If migration fails
        """
        if await self.is_applied(migration):
            logger.info("Migration %d already applied, skipping", migration.version)
            return

        logger.info("Applying migration %d: %s", migration.version, migration.description)

        try:
            await migration.up(self.db)

            self.db[MIGRATIONS_COLLECTION].insert_one({
                "version": migration.version,
                "description": migration.description,
                "applied_at": self.db.client.server_info()["localTime"],
            })

            logger.info("Successfully applied migration %d", migration.version)
        except Exception as e:
            logger.error("Failed to apply migration %d: %s", migration.version, e, exc_info=True)
            raise

    async def rollback(self, migration: BaseMigration) -> None:
        """Rollback a migration.

        Args:
            migration: Migration instance to rollback

        Raises:
            ValueError: If migration is not applied
            NotImplementedError: If rollback is not supported
            Exception: If rollback fails
        """
        if not await self.is_applied(migration):
            raise ValueError(f"Migration {migration.version} is not applied")

        logger.info("Rolling back migration %d: %s", migration.version, migration.description)

        try:
            await migration.down(self.db)

            self.db[MIGRATIONS_COLLECTION].delete_one({"version": migration.version})

            logger.info("Successfully rolled back migration %d", migration.version)
        except NotImplementedError:
            logger.warning("Rollback not supported for migration %d", migration.version)
            raise
        except Exception as e:
            logger.error("Failed to rollback migration %d: %s", migration.version, e, exc_info=True)
            raise

    async def migrate(self, migrations: list[BaseMigration]) -> None:
        """Apply all pending migrations in order.

        Args:
            migrations: List of migration instances (must be sorted by version)

        Raises:
            ValueError: If migrations are not sorted or have duplicate versions
        """
        if not migrations:
            logger.info("No migrations to apply")
            return

        versions = [m.version for m in migrations]
        if len(versions) != len(set(versions)):
            raise ValueError("Duplicate migration versions found")

        if versions != sorted(versions):
            raise ValueError("Migrations must be sorted by version")

        applied_versions = await self.get_applied_versions()
        pending = [m for m in migrations if m.version not in applied_versions]

        if not pending:
            logger.info("All migrations are already applied")
            return

        logger.info("Applying %d pending migrations", len(pending))

        for migration in pending:
            await self.apply(migration)

        logger.info("Migration complete: %d migrations applied", len(pending))

    async def get_current_version(self) -> int:
        """Get current database version (highest applied migration version).

        Returns:
            Current database version, or 0 if no migrations applied
        """
        applied_versions = await self.get_applied_versions()
        return max(applied_versions) if applied_versions else 0

