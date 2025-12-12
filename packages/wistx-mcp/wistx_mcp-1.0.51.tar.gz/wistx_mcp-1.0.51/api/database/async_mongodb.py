"""Async MongoDB adapter for services using MongoDBManager configuration."""

import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from api.config import settings

logger = logging.getLogger(__name__)


class AsyncMongoDBAdapter:
    """Async MongoDB adapter using MongoDBManager's configuration.

    This adapter uses Motor (async MongoDB driver) but follows
    MongoDBManager's connection string and settings for consistency.
    """

    _client: AsyncIOMotorClient | None = None
    _database: AsyncIOMotorDatabase | None = None

    def __init__(self):
        """Initialize async MongoDB adapter."""

    async def connect(self) -> None:
        """Connect to MongoDB using Motor (async driver).

        This method is idempotent - it will only connect once and reuse the connection.
        """
        # If already connected, verify connection is alive and return
        if self._client is not None and self._database is not None:
            try:
                # Quick ping to verify connection is still alive (with short timeout)
                await self._client.admin.command("ping", maxTimeMS=1000)
                logger.debug("MongoDB connection already established and healthy")
                return
            except Exception as e:
                logger.warning(
                    "Existing MongoDB connection unhealthy, reconnecting: %s",
                    str(e)
                )
                # Connection is stale, close and reconnect
                self._client.close()
                self._client = None
                self._database = None

        # Establish new connection
        connection_string = str(settings.mongodb_url).strip().rstrip("/")
        options = settings.get_mongodb_connection_options()

        motor_options = {
            "maxPoolSize": options["maxPoolSize"],
            "minPoolSize": options["minPoolSize"],
            "maxIdleTimeMS": options["maxIdleTimeMS"],
            "serverSelectionTimeoutMS": options["serverSelectionTimeoutMS"],
            "connectTimeoutMS": options["connectTimeoutMS"],
            "socketTimeoutMS": options["socketTimeoutMS"],
            "heartbeatFrequencyMS": options["heartbeatFrequencyMS"],
            "retryWrites": options["retryWrites"],
            "readPreference": options["readPreference"],
            "appName": options["appName"],
            "compressors": options["compressors"],
        }

        if options.get("tls"):
            motor_options["tls"] = True
            motor_options["tlsAllowInvalidCertificates"] = options.get(
                "tlsAllowInvalidCertificates", False
            )

        self._client = AsyncIOMotorClient(connection_string, **motor_options)
        self._database = self._client[settings.mongodb_database]

        # Verify connection with ping
        await self._client.admin.command("ping")

        logger.info(
            "Async MongoDB adapter connected: %s (pool size: %s)",
            settings.mongodb_database,
            options["maxPoolSize"],
        )

    async def disconnect(self) -> None:
        """Disconnect from MongoDB."""
        if self._client:
            self._client.close()
            self._client = None
            self._database = None

    def get_database(self) -> AsyncIOMotorDatabase:
        """Get MongoDB database instance.

        Returns:
            MongoDB database instance

        Raises:
            RuntimeError: If not connected
        """
        if self._database is None:
            raise RuntimeError("MongoDB database not connected. Call connect() first.")

        return self._database

    async def get_collection(self, collection_name: str):
        """Get a collection from the database.

        Args:
            collection_name: Name of the collection

        Returns:
            Collection instance
        """
        db = self.get_database()
        return db[collection_name]


async_mongodb_adapter = AsyncMongoDBAdapter()

