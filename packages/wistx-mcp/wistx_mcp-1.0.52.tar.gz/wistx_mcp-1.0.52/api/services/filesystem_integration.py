"""Filesystem integration helper for automatic entry creation during indexing."""

import logging
from pathlib import Path
from typing import Any, Optional, Union

from api.models.virtual_filesystem import (
    FilesystemEntryType,
    InfrastructureMetadata,
)
from api.services.virtual_filesystem_service import virtual_filesystem_service

logger = logging.getLogger(__name__)


def detect_code_type(file_path: Path, file_content: str) -> Optional[str]:
    """Detect code type from file path and content.

    Args:
        file_path: File path
        file_content: File content

    Returns:
        Code type ('terraform', 'kubernetes', 'docker', etc.) or None
    """
    path_str = str(file_path).lower()
    suffix = file_path.suffix.lower()

    if suffix == ".tf" or "terraform" in path_str:
        return "terraform"
    if suffix in [".yaml", ".yml"] and ("kubernetes" in path_str or "k8s" in path_str):
        return "kubernetes"
    if "dockerfile" in path_str.lower() or suffix == ".dockerfile":
        return "docker"
    if suffix == ".py":
        return "python"
    if suffix == ".js" or suffix == ".ts":
        return "javascript"
    if suffix == ".go":
        return "go"
    if suffix == ".rs":
        return "rust"

    content_lower = file_content.lower()[:500]
    if "apiVersion:" in content_lower and "kind:" in content_lower:
        return "kubernetes"
    if "provider" in content_lower and "terraform" in content_lower:
        return "terraform"
    if "FROM" in content_lower and ("docker" in content_lower or "alpine" in content_lower):
        return "docker"

    return None


def detect_language(file_path: Path) -> Optional[str]:
    """Detect programming language from file extension.

    Args:
        file_path: File path

    Returns:
        Language name or None
    """
    suffix = file_path.suffix.lower()
    language_map = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".go": "go",
        ".rs": "rust",
        ".java": "java",
        ".rb": "ruby",
        ".php": "php",
        ".tf": "hcl",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".json": "json",
        ".md": "markdown",
        ".sh": "bash",
        ".ps1": "powershell",
    }
    return language_map.get(suffix)


def build_virtual_path(original_path: str, code_type: Optional[str] = None) -> str:
    """Build virtual filesystem path from original file path.

    Args:
        original_path: Original file path in repository
        code_type: Code type (terraform, kubernetes, etc.)

    Returns:
        Virtual filesystem path
    """
    path_parts = original_path.replace("\\", "/").strip("/").split("/")

    if code_type == "terraform":
        if "modules" in path_parts:
            module_idx = path_parts.index("modules")
            if module_idx + 1 < len(path_parts):
                module_name = path_parts[module_idx + 1]
                return f"/infrastructure/terraform/modules/{module_name}/{'/'.join(path_parts[module_idx + 2:])}"
        return f"/infrastructure/terraform/{'/'.join(path_parts)}"
    elif code_type == "kubernetes":
        if "manifests" in path_parts:
            manifest_idx = path_parts.index("manifests")
            return f"/infrastructure/kubernetes/manifests/{'/'.join(path_parts[manifest_idx + 1:])}"
        return f"/infrastructure/kubernetes/{'/'.join(path_parts)}"
    elif code_type == "docker":
        return f"/infrastructure/docker/{'/'.join(path_parts)}"
    else:
        return f"/{'/'.join(path_parts)}"


async def create_filesystem_entry_for_file(
    resource_id: str,
    user_id: str,
    file_path: Path,
    relative_path: str,
    file_content: str,
    articles: list[Union[dict[str, Any], Any]],
    organization_id: Optional[str] = None,
    compliance_standards: Optional[list[str]] = None,
    environment_name: Optional[str] = None,
) -> Optional[str]:
    """Create filesystem entry for a file during indexing.

    Args:
        resource_id: Resource ID
        user_id: User ID
        file_path: File path object
        relative_path: Relative file path from repo root
        file_content: File content
        articles: List of article dictionaries created from this file
        organization_id: Organization ID
        compliance_standards: Compliance standards
        environment_name: Environment name

    Returns:
        Entry ID if created, None otherwise
    """
    try:
        code_type = detect_code_type(file_path, file_content)
        language = detect_language(file_path)
        virtual_path = build_virtual_path(relative_path, code_type)

        parent_path = "/".join(virtual_path.split("/")[:-1]) or "/"
        file_name = virtual_path.split("/")[-1]

        line_count = len(file_content.splitlines())
        file_size_bytes = len(file_content.encode("utf-8"))

        article_ids = []
        for article in articles:
            if isinstance(article, dict):
                article_id = article.get("article_id")
            else:
                article_id = getattr(article, "article_id", None)
            if article_id:
                article_ids.append(article_id)

        infrastructure_metadata = None
        if code_type or compliance_standards:
            infrastructure_metadata = InfrastructureMetadata(
                compliance_standards=compliance_standards or [],
                environment=environment_name,
            )

        entry = await virtual_filesystem_service.create_entry(
            resource_id=resource_id,
            user_id=user_id,
            organization_id=organization_id,
            entry_type=FilesystemEntryType.FILE,
            path=virtual_path,
            name=file_name,
            parent_path=parent_path,
            original_file_path=relative_path,
            article_id=article_ids[0] if article_ids else None,
            infrastructure_metadata=infrastructure_metadata,
            file_size_bytes=file_size_bytes,
            line_count=line_count,
            language=language,
            code_type=code_type,
        )

        await ensure_directory_structure(resource_id, user_id, parent_path, organization_id)

        logger.info(
            "Created filesystem entry for file: resource_id=%s, path=%s, entry_id=%s",
            resource_id,
            virtual_path,
            entry.entry_id,
        )

        return entry.entry_id

    except Exception as e:
        logger.warning(
            "Failed to create filesystem entry for file %s: %s",
            relative_path,
            e,
            exc_info=True,
        )
        return None


async def ensure_directory_structure(
    resource_id: str,
    user_id: str,
    directory_path: str,
    organization_id: Optional[str] = None,
) -> None:
    """Ensure directory structure exists in filesystem.

    Args:
        resource_id: Resource ID
        user_id: User ID
        directory_path: Directory path (e.g., '/infrastructure/terraform')
        organization_id: Organization ID
    """
    if directory_path == "/":
        return

    parts = directory_path.strip("/").split("/")
    current_path = "/"

    for part in parts:
        current_path = f"{current_path}{part}/" if current_path != "/" else f"/{part}/"

        try:
            existing = await virtual_filesystem_service.get_entry(
                resource_id=resource_id,
                path=current_path.rstrip("/"),
                user_id=user_id,
            )

            if not existing:
                parent_path = "/".join(current_path.rstrip("/").split("/")[:-1]) or "/"
                await virtual_filesystem_service.create_entry(
                    resource_id=resource_id,
                    user_id=user_id,
                    organization_id=organization_id,
                    entry_type=FilesystemEntryType.DIRECTORY,
                    path=current_path.rstrip("/"),
                    name=part,
                    parent_path=parent_path,
                )
        except Exception as e:
            logger.debug("Error ensuring directory %s: %s", current_path, e)

