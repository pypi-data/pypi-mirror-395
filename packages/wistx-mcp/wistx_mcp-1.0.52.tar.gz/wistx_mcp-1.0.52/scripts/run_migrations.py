"""Run MongoDB migrations."""

import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from api.database.migrations.migration_manager import MigrationManager
from api.database.migrations import BaseMigration

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def get_all_migrations() -> list[BaseMigration]:
    """Get all migration instances.

    Returns:
        List of migration instances sorted by version
    """
    from api.database.migrations.0001_initial_schema import (
        Migration0001InitialSchema,
    )
    from api.database.migrations.0003_resource_deduplication_and_checkpoints import (
        Migration0003ResourceDeduplicationAndCheckpoints,
    )

    migrations = [
        Migration0001InitialSchema(),
    ]

    try:
        from api.database.migrations.0002_add_custom_compliance_fields import (
            Migration0002AddCustomComplianceFields,
        )
        migrations.append(Migration0002AddCustomComplianceFields())
    except ImportError:
        pass

    try:
        migrations.append(Migration0003ResourceDeduplicationAndCheckpoints())
    except ImportError as e:
        logger.warning("Could not import migration 0003: %s", e)

    return sorted(migrations, key=lambda m: m.version)


async def main() -> None:
    """Run migrations."""
    logger.info("Starting migration process...")

    try:
        manager = MigrationManager()
        migrations = get_all_migrations()

        current_version = await manager.get_current_version()
        logger.info("Current database version: %d", current_version)

        await manager.migrate(migrations)

        new_version = await manager.get_current_version()
        logger.info("Migration complete. New database version: %d", new_version)

    except Exception as e:
        logger.error("Migration failed: %s", e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

