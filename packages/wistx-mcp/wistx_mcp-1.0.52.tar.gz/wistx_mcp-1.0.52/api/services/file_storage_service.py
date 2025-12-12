"""File storage service using MongoDB GridFS for document storage."""

import hashlib
import logging
from pathlib import Path
from typing import Any, Optional

from bson import ObjectId

from api.database.mongodb import mongodb_manager
from api.exceptions import ValidationError, DatabaseError

try:
    from gridfs import GridFS
    from gridfs.errors import NoFile
    HAS_GRIDFS = True
except ImportError:
    HAS_GRIDFS = False
    GridFS = None
    NoFile = Exception

logger = logging.getLogger(__name__)


class FileStorageService:
    """Service for storing and retrieving files using MongoDB GridFS."""

    def __init__(self):
        """Initialize file storage service."""
        if not HAS_GRIDFS:
            logger.warning("GridFS not available. Install pymongo with GridFS support.")
            self.gridfs = None
            self.db = None
            return
        
        self.db = mongodb_manager.get_database()
        self.gridfs = GridFS(self.db, collection="document_files")

    def store_file(
        self,
        file_path: Path,
        resource_id: str,
        user_id: str,
        filename: Optional[str] = None,
        content_type: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> tuple[str, str]:
        """Store file in GridFS.

        Args:
            file_path: Path to file to store
            resource_id: Resource ID this file belongs to
            user_id: User ID who owns this file
            filename: Filename (defaults to file_path.name)
            content_type: MIME type (optional)
            metadata: Additional metadata (optional)

        Returns:
            Tuple of (file_id, file_hash)

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is empty or GridFS not available
        """
        if not self.gridfs:
            raise DatabaseError(
                message="GridFS not available",
                user_message="File storage service is not available. Please contact support.",
                error_code="GRIDFS_NOT_AVAILABLE",
                details={"service": "file_storage"}
            )

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        file_size = file_path.stat().st_size
        if file_size == 0:
            raise ValidationError(
                message="Cannot store empty file",
                user_message="Cannot store empty file",
                error_code="EMPTY_FILE",
                details={"file_path": str(file_path)}
            )

        file_content = file_path.read_bytes()
        file_hash = self._calculate_hash(file_content)

        filename = filename or file_path.name
        content_type = content_type or self._detect_content_type(file_path)

        gridfs_metadata = {
            "resource_id": resource_id,
            "user_id": user_id,
            "file_hash": file_hash,
            "file_size_bytes": file_size,
            **(metadata or {}),
        }

        file_id = self.gridfs.put(
            file_content,
            filename=filename,
            content_type=content_type,
            metadata=gridfs_metadata,
        )

        logger.info(
            "Stored file in GridFS: %s (id: %s, size: %d bytes, hash: %s)",
            filename,
            file_id,
            file_size,
            file_hash[:16],
        )

        return str(file_id), file_hash

    def retrieve_file(
        self,
        file_id: str,
        output_path: Optional[Path] = None,
    ) -> tuple[bytes, dict[str, Any]]:
        """Retrieve file from GridFS.

        Args:
            file_id: GridFS file ID
            output_path: Optional path to save file (if None, returns bytes only)

        Returns:
            Tuple of (file_content_bytes, metadata_dict)

        Raises:
            FileNotFoundError: If file not found in GridFS
            ValueError: If GridFS not available
        """
        if not self.gridfs:
            raise DatabaseError(
                message="GridFS not available",
                user_message="File storage service is not available. Please contact support.",
                error_code="GRIDFS_NOT_AVAILABLE",
                details={"service": "file_storage"}
            )

        try:
            grid_file = self.gridfs.get(ObjectId(file_id))
        except (NoFile, ValueError, TypeError) as e:
            raise FileNotFoundError(f"File not found in GridFS: {file_id}") from e

        file_content = grid_file.read()
        metadata = {
            "filename": grid_file.filename,
            "content_type": grid_file.content_type,
            "length": grid_file.length,
            "upload_date": grid_file.upload_date,
            **grid_file.metadata,
        }

        if output_path:
            output_path.write_bytes(file_content)
            logger.debug("Retrieved file from GridFS to: %s", output_path)

        return file_content, metadata

    def delete_file(self, file_id: str) -> bool:
        """Delete file from GridFS.

        Args:
            file_id: GridFS file ID

        Returns:
            True if deleted, False if not found
        """
        if not self.gridfs:
            logger.warning("GridFS not available, cannot delete file: %s", file_id)
            return False

        try:
            self.gridfs.delete(ObjectId(file_id))
            logger.info("Deleted file from GridFS: %s", file_id)
            return True
        except (NoFile, ValueError, TypeError) as e:
            logger.warning("File not found in GridFS for deletion: %s", file_id)
            return False

    def get_file_metadata(self, file_id: str) -> Optional[dict[str, Any]]:
        """Get file metadata without retrieving content.

        Args:
            file_id: GridFS file ID

        Returns:
            Metadata dictionary or None if not found
        """
        if not self.gridfs:
            return None

        try:
            grid_file = self.gridfs.get(ObjectId(file_id))
            return {
                "file_id": str(grid_file._id),
                "filename": grid_file.filename,
                "content_type": grid_file.content_type,
                "length": grid_file.length,
                "upload_date": grid_file.upload_date,
                **grid_file.metadata,
            }
        except (NoFile, ValueError, TypeError):
            return None

    def get_file_hash(self, file_id: str) -> Optional[str]:
        """Get file hash from metadata.

        Args:
            file_id: GridFS file ID

        Returns:
            File hash or None if not found
        """
        metadata = self.get_file_metadata(file_id)
        return metadata.get("file_hash") if metadata else None

    def file_exists(self, file_id: str) -> bool:
        """Check if file exists in GridFS.

        Args:
            file_id: GridFS file ID

        Returns:
            True if file exists, False otherwise
        """
        if not self.gridfs:
            return False

        try:
            self.gridfs.get(ObjectId(file_id))
            return True
        except (NoFile, ValueError, TypeError):
            return False

    def list_files_by_resource(self, resource_id: str) -> list[dict[str, Any]]:
        """List all files for a resource.

        Args:
            resource_id: Resource ID

        Returns:
            List of file metadata dictionaries
        """
        if not self.gridfs:
            return []

        files = []
        for grid_file in self.gridfs.find({"metadata.resource_id": resource_id}):
            files.append({
                "file_id": str(grid_file._id),
                "filename": grid_file.filename,
                "content_type": grid_file.content_type,
                "length": grid_file.length,
                "upload_date": grid_file.upload_date,
                **grid_file.metadata,
            })
        return files

    def _calculate_hash(self, content: bytes) -> str:
        """Calculate SHA-256 hash of content.

        Args:
            content: File content bytes

        Returns:
            Hexadecimal hash string
        """
        return hashlib.sha256(content).hexdigest()

    def _detect_content_type(self, file_path: Path) -> str:
        """Detect content type from file extension.

        Args:
            file_path: File path

        Returns:
            MIME type string
        """
        extension = file_path.suffix.lower()
        mime_types = {
            ".pdf": "application/pdf",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".md": "text/markdown",
            ".markdown": "text/markdown",
            ".txt": "text/plain",
            ".xml": "application/xml",
            ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ".xls": "application/vnd.ms-excel",
            ".csv": "text/csv",
        }
        return mime_types.get(extension, "application/octet-stream")


file_storage_service = FileStorageService()

