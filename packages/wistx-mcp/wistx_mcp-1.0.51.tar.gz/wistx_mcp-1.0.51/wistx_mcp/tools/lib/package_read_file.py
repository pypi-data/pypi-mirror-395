"""Package read file tool - read specific file sections from packages."""

import hashlib
import logging
from typing import Any

from wistx_mcp.tools.lib.package_registry_integrator import RegistryIntegratorFactory

logger = logging.getLogger(__name__)


async def read_package_file(
    registry: str,
    package_name: str,
    filename_sha256: str,
    start_line: int,
    end_line: int,
    version: str | None = None,
) -> dict[str, Any]:
    """Read exact file section from package source using SHA256 hash.

    Args:
        registry: Registry name (pypi, npm, terraform)
        package_name: Package name
        filename_sha256: SHA256 hash of filename (from search results)
        start_line: Starting line (1-based)
        end_line: Ending line (max 200 lines from start_line)
        version: Optional package version

    Returns:
        Dictionary with file content and metadata

    Raises:
        ValueError: If file not found or invalid parameters
        RuntimeError: If package source cannot be fetched
    """
    if start_line < 1:
        raise ValueError("start_line must be >= 1")
    if end_line < start_line:
        raise ValueError("end_line must be >= start_line")
    if end_line - start_line > 200:
        raise ValueError("Maximum 200 lines can be read at once")

    integrator = RegistryIntegratorFactory.create(registry)
    try:
        source_files = await integrator.get_package_source(package_name, version)
    finally:
        await integrator.close()

    if not source_files:
        raise RuntimeError(f"No source files found for package {package_name}")

    target_file = None
    target_path = None

    for file_path, content in source_files.items():
        file_hash = hashlib.sha256(file_path.encode()).hexdigest()
        if file_hash == filename_sha256:
            target_file = content
            target_path = file_path
            break

    if not target_file:
        available_files = list(source_files.keys())[:10]
        available_hashes = [hashlib.sha256(fp.encode()).hexdigest()[:16] for fp in available_files]
        raise ValueError(
            f"File with hash {filename_sha256[:16]}... not found in package {package_name}. "
            f"Available files (first 10): {', '.join(available_files[:5])}. "
            f"Ensure you're using the correct filename_sha256 from package search results."
        )

    lines = target_file.split("\n")
    total_lines = len(lines)

    start_idx = max(0, start_line - 1)
    end_idx = min(total_lines, end_line)

    selected_lines = lines[start_idx:end_idx]
    content = "\n".join(selected_lines)

    return {
        "package_name": package_name,
        "registry": registry,
        "file_path": target_path,
        "filename_sha256": filename_sha256,
        "start_line": start_line,
        "end_line": end_idx,
        "total_lines": total_lines,
        "content": content,
        "line_count": len(selected_lines),
    }

