"""Cloud Discovery Service.

Service layer for cloud resource discovery persistence.
Handles MongoDB operations for discovery metadata and cloud connections.

IMPORTANT: We persist METADATA ONLY, not full resource data, because:
1. Cloud infrastructure changes constantly - stored data becomes stale quickly
2. Full resource configs may contain sensitive data (IPs, security groups)
3. The AI coding agent in the user's IDE has the full data locally
4. Reduces database storage and improves query performance
"""

import logging
from datetime import datetime, timezone
from typing import Any

from bson import ObjectId

from api.database.async_mongodb import async_mongodb_adapter
from api.models.cloud_discovery import (
    CloudConnectionDocument,
    CloudProviderEnum,
    CredentialStatusEnum,
    DiscoveryMetadataDocument,
    DiscoveryStatusEnum,
)

logger = logging.getLogger(__name__)

# Collection names
CONNECTIONS_COLLECTION = "cloud_connections"
DISCOVERIES_COLLECTION = "cloud_discoveries"


class CloudDiscoveryService:
    """Service for managing cloud discovery metadata persistence."""

    # --- Cloud Connections ---

    @staticmethod
    async def save_connection(connection: CloudConnectionDocument) -> str:
        """Save or update a cloud connection.

        Args:
            connection: CloudConnectionDocument to save

        Returns:
            The connection ID (role_arn hash or generated ID)
        """
        await async_mongodb_adapter.connect()
        db = async_mongodb_adapter.get_database()
        collection = db[CONNECTIONS_COLLECTION]

        doc = connection.model_dump()
        doc["updated_at"] = datetime.now(timezone.utc)

        # Upsert by user_id + provider + role_arn (unique constraint)
        result = await collection.update_one(
            {
                "user_id": connection.user_id,
                "provider": connection.provider.value,
                "role_arn": connection.role_arn,
            },
            {"$set": doc, "$setOnInsert": {"created_at": datetime.now(timezone.utc)}},
            upsert=True,
        )

        logger.info(
            "Saved cloud connection for user %s, provider %s",
            connection.user_id,
            connection.provider.value,
        )
        return str(result.upserted_id) if result.upserted_id else connection.role_arn

    @staticmethod
    async def get_connection(
        user_id: str, provider: CloudProviderEnum, role_arn: str | None = None
    ) -> CloudConnectionDocument | None:
        """Get a cloud connection for a user.

        Args:
            user_id: User ID
            provider: Cloud provider
            role_arn: Optional specific role ARN (if None, returns first active)

        Returns:
            CloudConnectionDocument or None
        """
        await async_mongodb_adapter.connect()
        db = async_mongodb_adapter.get_database()
        collection = db[CONNECTIONS_COLLECTION]

        query: dict[str, Any] = {
            "user_id": user_id,
            "provider": provider.value,
            "is_active": True,
        }
        if role_arn:
            query["role_arn"] = role_arn

        doc = await collection.find_one(query, sort=[("updated_at", -1)])
        if doc:
            doc.pop("_id", None)
            return CloudConnectionDocument(**doc)
        return None

    @staticmethod
    async def list_connections(
        user_id: str, provider: CloudProviderEnum | None = None
    ) -> list[CloudConnectionDocument]:
        """List all cloud connections for a user.

        Args:
            user_id: User ID
            provider: Optional filter by provider

        Returns:
            List of CloudConnectionDocument
        """
        await async_mongodb_adapter.connect()
        db = async_mongodb_adapter.get_database()
        collection = db[CONNECTIONS_COLLECTION]

        query: dict[str, Any] = {"user_id": user_id, "is_active": True}
        if provider:
            query["provider"] = provider.value

        cursor = collection.find(query).sort("updated_at", -1)
        connections = []
        async for doc in cursor:
            doc.pop("_id", None)
            connections.append(CloudConnectionDocument(**doc))
        return connections

    @staticmethod
    async def update_connection_status(
        user_id: str,
        role_arn: str,
        status: CredentialStatusEnum,
        account_id: str | None = None,
        regions_accessible: list[str] | None = None,
    ) -> bool:
        """Update connection validation status.

        Args:
            user_id: User ID
            role_arn: Role ARN
            status: New credential status
            account_id: AWS account ID (if validated)
            regions_accessible: List of accessible regions

        Returns:
            True if updated, False if not found
        """
        await async_mongodb_adapter.connect()
        db = async_mongodb_adapter.get_database()
        collection = db[CONNECTIONS_COLLECTION]

        update: dict[str, Any] = {
            "status": status.value,
            "last_validated": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
        if account_id:
            update["account_id"] = account_id
        if regions_accessible is not None:
            update["regions_accessible"] = regions_accessible

        result = await collection.update_one(
            {"user_id": user_id, "role_arn": role_arn},
            {"$set": update},
        )
        return result.modified_count > 0

    @staticmethod
    async def deactivate_connection(user_id: str, role_arn: str) -> bool:
        """Deactivate a cloud connection (soft delete).

        Args:
            user_id: User ID
            role_arn: Role ARN

        Returns:
            True if deactivated, False if not found
        """
        await async_mongodb_adapter.connect()
        db = async_mongodb_adapter.get_database()
        collection = db[CONNECTIONS_COLLECTION]

        result = await collection.update_one(
            {"user_id": user_id, "role_arn": role_arn},
            {"$set": {"is_active": False, "updated_at": datetime.now(timezone.utc)}},
        )
        return result.modified_count > 0

    # --- Discovery Metadata ---

    @staticmethod
    async def save_discovery_metadata(metadata: DiscoveryMetadataDocument) -> str:
        """Save discovery metadata (NOT full resource data).

        Args:
            metadata: DiscoveryMetadataDocument to save

        Returns:
            The discovery_id
        """
        await async_mongodb_adapter.connect()
        db = async_mongodb_adapter.get_database()
        collection = db[DISCOVERIES_COLLECTION]

        doc = metadata.model_dump()
        doc["created_at"] = datetime.now(timezone.utc)

        await collection.insert_one(doc)

        logger.info(
            "Saved discovery metadata: discovery_id=%s, user_id=%s, resources=%d",
            metadata.discovery_id,
            metadata.user_id,
            metadata.total_resources,
        )
        return metadata.discovery_id

    @staticmethod
    async def get_discovery_metadata(
        discovery_id: str, user_id: str
    ) -> DiscoveryMetadataDocument | None:
        """Get discovery metadata by ID.

        Args:
            discovery_id: Discovery ID
            user_id: User ID (for authorization)

        Returns:
            DiscoveryMetadataDocument or None
        """
        await async_mongodb_adapter.connect()
        db = async_mongodb_adapter.get_database()
        collection = db[DISCOVERIES_COLLECTION]

        doc = await collection.find_one(
            {"discovery_id": discovery_id, "user_id": user_id}
        )
        if doc:
            doc.pop("_id", None)
            return DiscoveryMetadataDocument(**doc)
        return None

    @staticmethod
    async def list_discoveries(
        user_id: str,
        provider: CloudProviderEnum | None = None,
        status: DiscoveryStatusEnum | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[DiscoveryMetadataDocument], int]:
        """List discoveries for a user with pagination.

        Args:
            user_id: User ID
            provider: Optional filter by provider
            status: Optional filter by status
            page: Page number (1-indexed)
            per_page: Items per page

        Returns:
            Tuple of (list of discoveries, total count)
        """
        await async_mongodb_adapter.connect()
        db = async_mongodb_adapter.get_database()
        collection = db[DISCOVERIES_COLLECTION]

        query: dict[str, Any] = {"user_id": user_id}
        if provider:
            query["provider"] = provider.value
        if status:
            query["status"] = status.value

        # Get total count
        total = await collection.count_documents(query)

        # Get paginated results
        skip = (page - 1) * per_page
        cursor = collection.find(query).sort("created_at", -1).skip(skip).limit(per_page)

        discoveries = []
        async for doc in cursor:
            doc.pop("_id", None)
            discoveries.append(DiscoveryMetadataDocument(**doc))

        return discoveries, total

    @staticmethod
    async def update_discovery_status(
        discovery_id: str,
        user_id: str,
        status: DiscoveryStatusEnum,
        completed_at: datetime | None = None,
        errors_count: int | None = None,
        error_summaries: list[str] | None = None,
    ) -> bool:
        """Update discovery status.

        Args:
            discovery_id: Discovery ID
            user_id: User ID
            status: New status
            completed_at: Completion timestamp
            errors_count: Number of errors
            error_summaries: Error summary messages

        Returns:
            True if updated, False if not found
        """
        await async_mongodb_adapter.connect()
        db = async_mongodb_adapter.get_database()
        collection = db[DISCOVERIES_COLLECTION]

        update: dict[str, Any] = {"status": status.value}
        if completed_at:
            update["completed_at"] = completed_at
        if errors_count is not None:
            update["errors_count"] = errors_count
        if error_summaries is not None:
            update["error_summaries"] = error_summaries

        result = await collection.update_one(
            {"discovery_id": discovery_id, "user_id": user_id},
            {"$set": update},
        )
        return result.modified_count > 0

    @staticmethod
    async def get_discovery_stats(user_id: str) -> dict[str, Any]:
        """Get discovery statistics for a user.

        Args:
            user_id: User ID

        Returns:
            Statistics dictionary
        """
        await async_mongodb_adapter.connect()
        db = async_mongodb_adapter.get_database()
        collection = db[DISCOVERIES_COLLECTION]

        pipeline = [
            {"$match": {"user_id": user_id}},
            {
                "$group": {
                    "_id": None,
                    "total_discoveries": {"$sum": 1},
                    "total_resources_discovered": {"$sum": "$total_resources"},
                    "providers_used": {"$addToSet": "$provider"},
                    "last_discovery": {"$max": "$created_at"},
                }
            },
        ]

        async for result in collection.aggregate(pipeline):
            return {
                "total_discoveries": result.get("total_discoveries", 0),
                "total_resources_discovered": result.get("total_resources_discovered", 0),
                "providers_used": result.get("providers_used", []),
                "last_discovery": result.get("last_discovery"),
            }

        return {
            "total_discoveries": 0,
            "total_resources_discovered": 0,
            "providers_used": [],
            "last_discovery": None,
        }

