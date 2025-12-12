"""Secure path validation to prevent directory traversal attacks."""

import os
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class PathValidationError(Exception):
    """Raised when path validation fails."""
    pass


def validate_file_path_for_upload(
    file_path: str,
    allowed_base: Path | None = None,
    allow_symlinks: bool = False,
) -> Path:
    """Validate file path and prevent directory traversal.
    
    Args:
        file_path: User-provided file path
        allowed_base: Required base directory (if None, uses configured default)
        allow_symlinks: Whether to allow symlinks (default: False for security)
    
    Returns:
        Resolved, validated Path object
    
    Raises:
        PathValidationError: If path is invalid or dangerous
        FileNotFoundError: If file doesn't exist
    """
    if not file_path or not isinstance(file_path, str):
        raise PathValidationError("File path must be a non-empty string")
    
    # Convert to Path and normalize
    path = Path(file_path)
    
    # Check for null bytes (path injection)
    if '\x00' in file_path:
        raise PathValidationError("Null bytes not allowed in file path")
    
    # Check for directory traversal patterns BEFORE resolution
    path_str = str(path)
    if '..' in path_str or '..' in path.parts:
        raise PathValidationError("Path traversal detected: '..' sequences not allowed")
    
    # Check for encoded directory traversal
    path_lower = path_str.lower()
    if '%2e%2e' in path_lower or '%2E%2E' in path_str:
        raise PathValidationError("Path traversal detected: encoded '..' sequences not allowed")
    
    # Resolve to absolute path (follows symlinks by default)
    try:
        resolved = path.resolve(strict=True)
    except (OSError, RuntimeError) as e:
        raise PathValidationError(f"Invalid file path: {e}") from e
    
    # Check for absolute paths if base is required
    if allowed_base is None:
        # Use configured upload directory
        from wistx_mcp.config import settings
        upload_base = getattr(settings, 'upload_base_dir', '/tmp/wistx_uploads')
        allowed_base = Path(upload_base)
    
    allowed_base = Path(allowed_base).resolve()
    
    # Ensure path is within allowed base directory
    try:
        resolved.relative_to(allowed_base)
    except ValueError:
        raise PathValidationError(
            f"File path outside allowed directory: {resolved} not in {allowed_base}"
        )
    
    # Check if path is a symlink (security risk)
    if not allow_symlinks and path.is_symlink():
        raise PathValidationError("Symlinks not allowed for security reasons")
    
    # Check if file exists
    if not resolved.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Check if it's actually a file (not directory)
    if not resolved.is_file():
        raise PathValidationError(f"Path is not a file: {file_path}")
    
    # Additional security checks
    # Block common sensitive file patterns
    sensitive_patterns = [
        '/etc/passwd', '/etc/shadow', '/etc/hosts',
        '/.ssh/', '/.aws/', '/.env',
        'C:\\Windows\\System32', 'C:\\Windows\\SysWOW64',
    ]
    
    path_lower = str(resolved).lower()
    for pattern in sensitive_patterns:
        if pattern.lower() in path_lower:
            raise PathValidationError(f"Access to sensitive path blocked: {pattern}")
    
    logger.debug("Validated file path: %s -> %s", file_path, resolved)
    return resolved

