"""Secure storage for sensitive strings like API keys.

This module provides SecureString class for storing sensitive data
in memory with best-effort security measures.

Note: True secure memory requires OS-level support (mlock, etc.),
which is complex in Python. For production, consider using GCP Secret Manager.
"""

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)


class SecureString:
    """Secure string storage that attempts to minimize memory exposure.

    This class provides best-effort secure storage by:
    1. Storing strings in byte arrays that can be zeroed
    2. Clearing memory on deletion
    3. Preventing accidental string conversion in logs

    Limitations:
    - Python's garbage collector may keep copies in memory
    - Cannot prevent memory dumps at OS level
    - For production, use GCP Secret Manager or similar service
    """

    def __init__(self, value: str):
        """Initialize secure string storage.

        Args:
            value: String value to store securely
        """
        if not isinstance(value, str):
            raise TypeError("SecureString requires a string value")
        
        self._bytes: Optional[bytearray] = None
        self._length = len(value)
        self._set_value(value)

    def _set_value(self, value: str) -> None:
        """Set value in secure byte array."""
        if self._bytes is not None:
            self._clear_bytes()
        
        encoded = value.encode("utf-8")
        self._bytes = bytearray(encoded)

    def get(self) -> str:
        """Get the stored string value.

        Returns:
            String value
        """
        if self._bytes is None:
            raise ValueError("SecureString has been cleared")
        
        return self._bytes.decode("utf-8")

    def clear(self) -> None:
        """Clear the stored value from memory."""
        self._clear_bytes()
        self._length = 0

    def _clear_bytes(self) -> None:
        """Zero out the byte array."""
        if self._bytes is not None:
            try:
                for i in range(len(self._bytes)):
                    self._bytes[i] = 0
            except Exception as e:
                logger.warning("Failed to clear secure string bytes: %s", e)
            finally:
                self._bytes = None

    def __len__(self) -> int:
        """Get length of stored string."""
        return self._length

    def __bool__(self) -> bool:
        """Check if string is non-empty."""
        return self._length > 0

    def __del__(self):
        """Destructor: clear memory on deletion."""
        self.clear()

    def __repr__(self) -> str:
        """String representation (does not expose value)."""
        return f"SecureString(length={self._length}, cleared={self._bytes is None})"

    def __str__(self) -> str:
        """String conversion (returns redacted value)."""
        return "[REDACTED]"

