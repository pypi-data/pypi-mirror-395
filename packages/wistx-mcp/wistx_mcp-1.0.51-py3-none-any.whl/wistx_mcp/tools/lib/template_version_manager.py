"""Template version management utilities."""

import logging
from datetime import datetime
from typing import Any

from semantic_version import Version

logger = logging.getLogger(__name__)


class TemplateVersionManager:
    """Manages template versioning and changelogs."""

    @staticmethod
    def parse_version(version_str: str) -> Version:
        """Parse semantic version string.

        Args:
            version_str: Version string (e.g., "1.2.3")

        Returns:
            Version object

        Raises:
            ValueError: If invalid version format
        """
        try:
            return Version(version_str)
        except ValueError as e:
            raise ValueError(f"Invalid semantic version: {version_str}") from e

    @staticmethod
    def compare_versions(version1: str, version2: str) -> int:
        """Compare two semantic versions.

        Args:
            version1: First version string
            version2: Second version string

        Returns:
            -1 if version1 < version2, 0 if equal, 1 if version1 > version2

        Raises:
            ValueError: If invalid version format
        """
        v1 = TemplateVersionManager.parse_version(version1)
        v2 = TemplateVersionManager.parse_version(version2)

        if v1 < v2:
            return -1
        elif v1 > v2:
            return 1
        return 0

    @staticmethod
    def is_newer_version(new_version: str, existing_version: str) -> bool:
        """Check if new version is newer than existing version.

        Args:
            new_version: New version string
            existing_version: Existing version string

        Returns:
            True if new_version > existing_version

        Raises:
            ValueError: If invalid version format
        """
        return TemplateVersionManager.compare_versions(new_version, existing_version) > 0

    @staticmethod
    def get_latest_version(versions: list[str]) -> str:
        """Get the latest version from a list of versions.

        Args:
            versions: List of version strings

        Returns:
            Latest version string

        Raises:
            ValueError: If empty list or invalid versions
        """
        if not versions:
            raise ValueError("Empty version list")

        latest = versions[0]
        for version in versions[1:]:
            if TemplateVersionManager.is_newer_version(version, latest):
                latest = version

        return latest

    @staticmethod
    def suggest_next_version(
        current_version: str,
        change_type: str = "patch",
    ) -> str:
        """Suggest next version based on change type.

        Args:
            current_version: Current version string
            change_type: Type of change (major, minor, patch)

        Returns:
            Suggested next version string

        Raises:
            ValueError: If invalid version or change_type
        """
        version = TemplateVersionManager.parse_version(current_version)

        if change_type == "major":
            return str(version.next_major())
        elif change_type == "minor":
            return str(version.next_minor())
        elif change_type == "patch":
            return str(version.next_patch())
        else:
            raise ValueError(f"Invalid change_type: {change_type}. Use 'major', 'minor', or 'patch'")

    @staticmethod
    def format_changelog_entry(
        version: str,
        changes: list[str],
        author: str | None = None,
    ) -> str:
        """Format changelog entry.

        Args:
            version: Version string
            changes: List of change descriptions
            author: Author name (optional)

        Returns:
            Formatted changelog entry
        """
        lines = [f"## {version} - {datetime.utcnow().strftime('%Y-%m-%d')}"]
        if author:
            lines.append(f"**Author**: {author}")
        lines.append("")
        for change in changes:
            lines.append(f"- {change}")
        return "\n".join(lines)

    @staticmethod
    def validate_changelog(changelog: list[str]) -> dict[str, Any]:
        """Validate changelog entries.

        Args:
            changelog: List of changelog entries

        Returns:
            Validation result with 'valid' and 'errors' keys
        """
        errors: list[str] = []
        warnings: list[str] = []

        if not changelog:
            warnings.append("Empty changelog")

        for i, entry in enumerate(changelog):
            if not isinstance(entry, str):
                errors.append(f"Changelog entry {i} must be a string")
            elif len(entry.strip()) == 0:
                warnings.append(f"Empty changelog entry at index {i}")
            elif len(entry) > 500:
                warnings.append(f"Changelog entry {i} is very long ({len(entry)} chars)")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }

