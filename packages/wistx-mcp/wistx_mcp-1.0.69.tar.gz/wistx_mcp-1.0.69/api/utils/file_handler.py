"""File handling utilities for document indexing."""

import logging
import tempfile
from pathlib import Path
from typing import Optional

import httpx
from fastapi import UploadFile

from api.services.plan_service import plan_service

logger = logging.getLogger(__name__)

MAX_FILE_SIZES = {
    "professional": 10 * 1024 * 1024,
    "team": 50 * 1024 * 1024,
    "enterprise": 1024 * 1024 * 1024,
}

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/markdown",
    "text/plain",
    "text/x-markdown",
    "application/xml",
    "text/xml",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-excel",
    "text/csv",
    "application/csv",
}

EXTENSION_TO_TYPE = {
    ".pdf": "pdf",
    ".docx": "docx",
    ".md": "markdown",
    ".markdown": "markdown",
    ".txt": "txt",
    ".xml": "xml",
    ".xlsx": "excel",
    ".xls": "excel",
    ".csv": "csv",
}


class FileHandler:
    """Handle file uploads and URL downloads for document indexing."""

    @staticmethod
    def get_max_file_size(plan: str) -> int:
        """Get maximum file size for plan.

        Args:
            plan: User plan ID

        Returns:
            Maximum file size in bytes
        """
        plan_obj = plan_service.get_plan(plan)
        if plan_obj and hasattr(plan_obj, "limits") and hasattr(plan_obj.limits, "storage_mb"):
            max_storage_mb = plan_obj.limits.storage_mb
            if max_storage_mb > 0:
                return int(max_storage_mb * 1024 * 1024)
        return MAX_FILE_SIZES.get(plan, MAX_FILE_SIZES["professional"])

    @staticmethod
    def validate_file_type(filename: str, content_type: Optional[str] = None) -> str:
        """Validate file type and return document type.

        Args:
            filename: File name
            content_type: MIME type (optional)

        Returns:
            Document type (pdf, docx, markdown, txt, xml, excel, csv)

        Raises:
            ValueError: If file type is invalid
        """
        file_ext = Path(filename).suffix.lower()
        document_type = EXTENSION_TO_TYPE.get(file_ext)

        if not document_type:
            raise ValueError(
                f"Unsupported file type: {file_ext}. "
                f"Supported types: {', '.join(sorted(EXTENSION_TO_TYPE.keys()))}"
            )

        if content_type and content_type not in ALLOWED_MIME_TYPES:
            logger.warning(
                "MIME type %s not in allowed list, but extension %s is valid. Proceeding.",
                content_type,
                file_ext,
            )

        return document_type

    @staticmethod
    async def save_uploaded_file(
        file: UploadFile,
        plan: str,
    ) -> tuple[Path, str]:
        """Save uploaded file temporarily.

        Args:
            file: FastAPI UploadFile
            plan: User plan for size limit

        Returns:
            Tuple of (file_path, document_type)

        Raises:
            ValueError: If file is too large or invalid type
        """
        max_size = FileHandler.get_max_file_size(plan)

        content = await file.read()
        file_size = len(content)

        if file_size > max_size:
            raise ValueError(
                f"File size {file_size / 1024 / 1024:.2f} MB exceeds "
                f"limit of {max_size / 1024 / 1024:.2f} MB for plan {plan}"
            )

        if file_size == 0:
            raise ValueError("File is empty")

        document_type = FileHandler.validate_file_type(
            file.filename or "unknown",
            file.content_type,
        )

        suffix = Path(file.filename or "unknown").suffix or f".{document_type}"

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_path = Path(tmp_file.name)
            tmp_path.write_bytes(content)
            logger.info(
                "Saved uploaded file: %s (%d bytes) to %s",
                file.filename,
                file_size,
                tmp_path,
            )

        return tmp_path, document_type

    @staticmethod
    async def download_file_from_url(
        url: str,
        plan: str,
        timeout: float = 30.0,
    ) -> tuple[Path, str]:
        """Download file from URL temporarily.

        Args:
            url: File URL
            plan: User plan for size limit
            timeout: Download timeout in seconds

        Returns:
            Tuple of (file_path, document_type)

        Raises:
            ValueError: If download fails or file is too large
            httpx.HTTPError: If HTTP request fails
        """
        max_size = FileHandler.get_max_file_size(plan)

        try:
            async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
                async with client.stream("GET", url) as response:
                    response.raise_for_status()

                    content_length = response.headers.get("content-length")

                    if content_length and int(content_length) > max_size:
                        raise ValueError(
                            f"File size {int(content_length) / 1024 / 1024:.2f} MB exceeds "
                            f"limit of {max_size / 1024 / 1024:.2f} MB for plan {plan}"
                        )

                    file_ext = Path(url).suffix.lower()
                    document_type = EXTENSION_TO_TYPE.get(file_ext)

                    if not document_type:
                        raise ValueError(
                            f"Unsupported file type from URL: {file_ext}. "
                            f"Supported types: {', '.join(EXTENSION_TO_TYPE.keys())}"
                        )

                    suffix = file_ext or f".{document_type}"

                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                        tmp_path = Path(tmp_file.name)
                        file_size = 0
                        chunks = []

                        async for chunk in response.aiter_bytes():
                            file_size += len(chunk)
                            if file_size > max_size:
                                if tmp_path.exists():
                                    tmp_path.unlink()
                                raise ValueError(
                                    f"File size exceeds limit of {max_size / 1024 / 1024:.2f} MB for plan {plan}"
                                )
                            chunks.append(chunk)

                        tmp_path.write_bytes(b"".join(chunks))

                        logger.info(
                            "Downloaded file from URL: %s (%d bytes) to %s",
                            url,
                            file_size,
                            tmp_path,
                        )

                    return tmp_path, document_type

        except httpx.HTTPError as e:
            logger.error("HTTP error downloading file from %s: %s", url, e)
            raise ValueError(f"Failed to download file from URL: {str(e)}") from e
        except (ValueError, RuntimeError, ConnectionError, TimeoutError) as e:
            logger.error("Error downloading file from %s: %s", url, e)
            raise ValueError(f"Failed to download file: {str(e)}") from e
        except Exception as e:
            logger.error("Unexpected error downloading file from %s: %s", url, e)
            raise ValueError(f"Failed to download file: Unexpected error") from e

    @staticmethod
    def cleanup_file(file_path: Path) -> None:
        """Clean up temporary file.

        Args:
            file_path: Path to file to delete
        """
        try:
            if file_path.exists():
                file_path.unlink()
                logger.debug("Cleaned up temporary file: %s", file_path)
        except (OSError, PermissionError) as e:
            logger.warning("Failed to cleanup file %s: %s", file_path, e)
        except Exception as e:
            logger.warning("Unexpected error cleaning up file %s: %s", file_path, e)

    @staticmethod
    def is_temporary_file(file_path: Path) -> bool:
        """Check if file is a temporary file (uploaded or downloaded).

        Args:
            file_path: Path to check

        Returns:
            True if file is in temp directory
        """
        try:
            temp_dir = Path(tempfile.gettempdir())
            return temp_dir in file_path.parents or str(file_path).startswith(str(temp_dir))
        except (OSError, ValueError, RuntimeError):
            return False

    @staticmethod
    def validate_file_path(file_path: Path, allowed_base: Path | None = None) -> Path:
        """Validate file path is safe and within allowed base directory.

        Args:
            file_path: Path to validate
            allowed_base: Allowed base directory (defaults to temp directory)

        Returns:
            Resolved and validated Path

        Raises:
            ValueError: If path traversal detected or path outside allowed base
        """
        if allowed_base is None:
            allowed_base = Path(tempfile.gettempdir())

        try:
            resolved = file_path.resolve()
            base_resolved = allowed_base.resolve()

            if ".." in str(resolved):
                raise ValueError("Path traversal detected: '..' in path")

            if not str(resolved).startswith(str(base_resolved)):
                raise ValueError(
                    f"Path outside allowed directory: {resolved} not in {base_resolved}"
                )

            relative = resolved.relative_to(base_resolved)
            if ".." in str(relative):
                raise ValueError("Path traversal detected in relative path")

            return resolved
        except (OSError, ValueError, RuntimeError) as e:
            if isinstance(e, ValueError):
                raise
            raise ValueError(f"Invalid file path: {e}") from e


file_handler = FileHandler()

