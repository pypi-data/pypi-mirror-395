"""Virtual filesystem service for infrastructure-aware file navigation."""

import fnmatch
import logging
import secrets
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from bson import ObjectId

from api.database.mongodb import mongodb_manager
from api.models.virtual_filesystem import (
    FilesystemEntryType,
    InfrastructureMetadata,
    VirtualFilesystemEntry,
)
from api.exceptions import ValidationError

logger = logging.getLogger(__name__)


def generate_entry_id() -> str:
    """Generate unique filesystem entry ID.

    Returns:
        Unique entry ID (e.g., 'fs_abc123')
    """
    random_part = secrets.token_urlsafe(8)[:8]
    return f"fs_{random_part}"


class VirtualFilesystemService:
    """Service for managing virtual filesystem entries."""

    def __init__(self):
        """Initialize virtual filesystem service."""
        self._db = None

    def _get_db(self):
        """Get MongoDB database instance."""
        if self._db is None:
            self._db = mongodb_manager.get_database()
        return self._db

    async def create_entry(
        self,
        resource_id: str,
        user_id: str,
        entry_type: FilesystemEntryType,
        path: str,
        name: str,
        parent_path: Optional[str] = None,
        original_file_path: Optional[str] = None,
        article_id: Optional[str] = None,
        indexed_file_id: Optional[str] = None,
        infrastructure_metadata: Optional[InfrastructureMetadata] = None,
        file_size_bytes: Optional[int] = None,
        line_count: Optional[int] = None,
        language: Optional[str] = None,
        code_type: Optional[str] = None,
        tags: Optional[list[str]] = None,
        organization_id: Optional[str] = None,
    ) -> VirtualFilesystemEntry:
        """Create a new filesystem entry.

        Args:
            resource_id: Resource ID this entry belongs to
            user_id: User ID who owns this entry
            entry_type: Type of filesystem entry
            path: Virtual filesystem path
            name: Entry name
            parent_path: Parent directory path
            original_file_path: Original file path in repository
            article_id: Knowledge article ID
            indexed_file_id: Indexed file ID
            infrastructure_metadata: Infrastructure-specific metadata
            file_size_bytes: File size in bytes
            line_count: Number of lines
            language: Programming language
            code_type: Code type (terraform, kubernetes, etc.)
            tags: Tags for categorization
            organization_id: Organization ID

        Returns:
            Created VirtualFilesystemEntry

        Raises:
            ValueError: If path is invalid or entry already exists
        """
        if not path.startswith("/"):
            raise ValidationError(
                message="Path must start with '/'",
                user_message="Path must start with '/' (e.g., '/path/to/file')",
                error_code="INVALID_PATH_FORMAT",
                details={"path": path}
            )

        db = self._get_db()
        collection = db.virtual_filesystem

        existing = collection.find_one({"resource_id": resource_id, "path": path})
        if existing:
            logger.warning(
                "Filesystem entry already exists: resource_id=%s, path=%s",
                resource_id,
                path,
            )
            return VirtualFilesystemEntry.from_dict(existing)

        entry_id = generate_entry_id()

        entry = VirtualFilesystemEntry(
            entry_id=entry_id,
            resource_id=resource_id,
            user_id=user_id,
            organization_id=organization_id,
            entry_type=entry_type,
            path=path,
            name=name,
            parent_path=parent_path,
            original_file_path=original_file_path,
            article_id=article_id,
            indexed_file_id=indexed_file_id,
            infrastructure_metadata=infrastructure_metadata,
            file_size_bytes=file_size_bytes,
            line_count=line_count,
            language=language,
            code_type=code_type,
            tags=tags or [],
        )

        entry_dict = entry.to_dict()
        collection.insert_one(entry_dict)

        if parent_path:
            await self._update_parent_children_count(resource_id, parent_path)

        logger.info(
            "Created filesystem entry: entry_id=%s, resource_id=%s, path=%s",
            entry_id,
            resource_id,
            path,
        )

        return entry

    async def _update_parent_children_count(
        self, resource_id: str, parent_path: str
    ) -> None:
        """Update parent directory children count.

        Args:
            resource_id: Resource ID
            parent_path: Parent directory path
        """
        db = self._get_db()
        collection = db.virtual_filesystem

        children_count = collection.count_documents(
            {"resource_id": resource_id, "parent_path": parent_path}
        )

        collection.update_one(
            {"resource_id": resource_id, "path": parent_path},
            {"$set": {"children_count": children_count}},
        )

    async def get_entry(
        self, resource_id: str, path: str, user_id: Optional[str] = None
    ) -> Optional[VirtualFilesystemEntry]:
        """Get filesystem entry by path.

        Args:
            resource_id: Resource ID
            path: Virtual filesystem path
            user_id: User ID (for access control)

        Returns:
            VirtualFilesystemEntry if found, None otherwise
        """
        db = self._get_db()
        collection = db.virtual_filesystem

        query = {"resource_id": resource_id, "path": path}
        if user_id:
            query["user_id"] = ObjectId(user_id)

        doc = collection.find_one(query)
        if not doc:
            return None

        return VirtualFilesystemEntry.from_dict(doc)

    async def list_directory(
        self,
        resource_id: str,
        path: str = "/",
        user_id: Optional[str] = None,
        view_mode: str = "standard",
        include_metadata: bool = False,
    ) -> list[dict[str, Any]]:
        """List directory contents.

        Args:
            resource_id: Resource ID
            path: Directory path (default: '/')
            user_id: User ID (for access control)
            view_mode: View mode ('standard', 'infrastructure', 'compliance', 'costs', 'security')
            include_metadata: Include infrastructure metadata

        Returns:
            List of directory entries
        """
        db = self._get_db()
        collection = db.virtual_filesystem

        query = {"resource_id": resource_id, "parent_path": path}
        if user_id:
            query["user_id"] = ObjectId(user_id)

        cursor = collection.find(query).sort("name", 1)

        entries = []
        for doc in cursor:
            entry = VirtualFilesystemEntry.from_dict(doc)
            entry_dict = entry.model_dump()

            if view_mode == "infrastructure":
                if entry.infrastructure_metadata:
                    entry_dict["infrastructure"] = entry.infrastructure_metadata.model_dump()
            elif view_mode == "compliance":
                if (
                    entry.infrastructure_metadata
                    and entry.infrastructure_metadata.compliance_standards
                ):
                    entry_dict["compliance"] = {
                        "standards": entry.infrastructure_metadata.compliance_standards
                    }
            elif view_mode == "costs":
                if (
                    entry.infrastructure_metadata
                    and entry.infrastructure_metadata.estimated_monthly_cost_usd
                ):
                    entry_dict["cost"] = {
                        "monthly_usd": entry.infrastructure_metadata.estimated_monthly_cost_usd
                    }
            elif view_mode == "security":
                if (
                    entry.infrastructure_metadata
                    and entry.infrastructure_metadata.security_score is not None
                ):
                    entry_dict["security"] = {
                        "score": entry.infrastructure_metadata.security_score
                    }

            if not include_metadata:
                entry_dict.pop("infrastructure_metadata", None)

            entries.append(entry_dict)

        return entries

    async def get_tree(
        self,
        resource_id: str,
        root_path: str = "/",
        max_depth: int = 10,
        user_id: Optional[str] = None,
        view_mode: str = "standard",
    ) -> dict[str, Any]:
        """Get filesystem tree structure.

        Args:
            resource_id: Resource ID
            root_path: Root path for tree (default: '/')
            max_depth: Maximum depth to traverse
            user_id: User ID (for access control)
            view_mode: View mode ('standard', 'infrastructure', 'compliance', 'costs', 'security')

        Returns:
            Tree structure dictionary
        """
        db = self._get_db()
        collection = db.virtual_filesystem

        query = {"resource_id": resource_id}
        if user_id:
            query["user_id"] = ObjectId(user_id)

        cursor = collection.find(query).sort("path", 1)

        tree: dict[str, Any] = {
            "path": root_path,
            "name": root_path.split("/")[-1] or "/",
            "type": "directory",
            "children": [],
        }

        path_map: dict[str, dict[str, Any]] = {root_path: tree}

        for doc in cursor:
            entry = VirtualFilesystemEntry.from_dict(doc)
            entry_path = entry.path

            if not entry_path.startswith(root_path):
                continue

            relative_path = entry_path[len(root_path) :].lstrip("/")
            depth = len(relative_path.split("/")) if relative_path else 0

            if depth > max_depth:
                continue

            entry_dict = {
                "path": entry_path,
                "name": entry.name,
                "type": entry.entry_type.value,
                "children": [],
            }

            if view_mode == "infrastructure" and entry.infrastructure_metadata:
                entry_dict["infrastructure"] = entry.infrastructure_metadata.model_dump()
            elif view_mode == "compliance" and entry.infrastructure_metadata:
                if entry.infrastructure_metadata.compliance_standards:
                    entry_dict["compliance"] = {
                        "standards": entry.infrastructure_metadata.compliance_standards
                    }
            elif view_mode == "costs" and entry.infrastructure_metadata:
                if entry.infrastructure_metadata.estimated_monthly_cost_usd:
                    entry_dict["cost"] = {
                        "monthly_usd": entry.infrastructure_metadata.estimated_monthly_cost_usd
                    }
            elif view_mode == "security" and entry.infrastructure_metadata:
                if entry.infrastructure_metadata.security_score is not None:
                    entry_dict["security"] = {
                        "score": entry.infrastructure_metadata.security_score
                    }

            path_map[entry_path] = entry_dict

            if entry.parent_path and entry.parent_path in path_map:
                path_map[entry.parent_path]["children"].append(entry_dict)
            elif entry.parent_path == root_path:
                tree["children"].append(entry_dict)

        return tree

    async def glob(
        self,
        resource_id: str,
        pattern: str,
        user_id: Optional[str] = None,
        entry_type: Optional[FilesystemEntryType] = None,
        code_type: Optional[str] = None,
        cloud_provider: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        """Find filesystem entries matching glob pattern.

        Args:
            resource_id: Resource ID
            pattern: Glob pattern (e.g., '**/*.tf', '/infrastructure/**')
            user_id: User ID (for access control)
            entry_type: Filter by entry type
            code_type: Filter by code type
            cloud_provider: Filter by cloud provider

        Returns:
            List of matching entries
        """
        db = self._get_db()
        collection = db.virtual_filesystem

        query: dict[str, Any] = {"resource_id": resource_id}
        if user_id:
            query["user_id"] = ObjectId(user_id)
        if entry_type:
            query["entry_type"] = entry_type.value
        if code_type:
            query["code_type"] = code_type
        if cloud_provider:
            query["infrastructure_metadata.cloud_provider"] = cloud_provider

        cursor = collection.find(query)

        matches = []
        for doc in cursor:
            entry = VirtualFilesystemEntry.from_dict(doc)
            if fnmatch.fnmatch(entry.path, pattern):
                matches.append(entry.model_dump())

        return matches

    async def delete_entry(
        self, resource_id: str, path: str, user_id: Optional[str] = None
    ) -> bool:
        """Delete filesystem entry.

        Args:
            resource_id: Resource ID
            path: Virtual filesystem path
            user_id: User ID (for access control)

        Returns:
            True if deleted, False if not found
        """
        db = self._get_db()
        collection = db.virtual_filesystem

        query = {"resource_id": resource_id, "path": path}
        if user_id:
            query["user_id"] = ObjectId(user_id)

        result = collection.delete_one(query)
        return result.deleted_count > 0

    async def delete_resource_entries(self, resource_id: str) -> int:
        """Delete all filesystem entries for a resource.

        Args:
            resource_id: Resource ID

        Returns:
            Number of entries deleted
        """
        db = self._get_db()
        collection = db.virtual_filesystem

        result = collection.delete_many({"resource_id": resource_id})
        return result.deleted_count


virtual_filesystem_service = VirtualFilesystemService()

