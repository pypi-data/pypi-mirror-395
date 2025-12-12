"""Base migration class for MongoDB migrations."""

import logging
from abc import ABC, abstractmethod

from pymongo.database import Database

logger = logging.getLogger(__name__)


class BaseMigration(ABC):
    """Base class for MongoDB migrations.

    All migrations should inherit from this class and implement:
    - version: Migration version number (incrementing integer)
    - description: Human-readable description of what the migration does
    - up(): Apply the migration
    - down(): Rollback the migration (optional)
    """

    @property
    @abstractmethod
    def version(self) -> int:
        """Migration version number (must be unique and incrementing)."""

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description of the migration."""

    @abstractmethod
    async def up(self, db: Database) -> None:
        """Apply the migration.

        Args:
            db: MongoDB database instance

        Raises:
            Exception: If migration fails
        """

    async def down(self, db: Database) -> None:
        """Rollback the migration (optional).

        Args:
            db: MongoDB database instance

        Raises:
            NotImplementedError: If rollback is not supported
        """
        raise NotImplementedError(f"Rollback not supported for migration {self.version}")

    def __repr__(self) -> str:
        """String representation of migration."""
        return f"Migration(version={self.version}, description={self.description})"

