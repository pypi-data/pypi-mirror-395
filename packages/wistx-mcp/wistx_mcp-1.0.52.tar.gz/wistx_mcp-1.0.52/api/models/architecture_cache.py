"""Architecture design cache models."""

import hashlib
import json
from datetime import datetime, timedelta
from typing import Any, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class ArchitectureDesignCache(BaseModel):
    """Model for caching architecture design results."""

    cache_key: str = Field(..., description="Unique cache key (hash of parameters)")
    user_id: str = Field(..., description="User ID who owns this cache entry")
    organization_id: Optional[str] = Field(
        default=None,
        description="Organization ID (if cache is shared within org)",
    )

    action: str = Field(..., description="Action type (initialize, design, review, optimize)")
    project_type: Optional[str] = Field(default=None, description="Project type")
    architecture_type: Optional[str] = Field(default=None, description="Architecture pattern")
    cloud_provider: Optional[str] = Field(default=None, description="Cloud provider")
    compliance_standards: Optional[list[str]] = Field(
        default=None,
        description="Compliance standards",
    )
    requirements_hash: Optional[str] = Field(
        default=None,
        description="Hash of requirements dict for cache key",
    )

    design_result: dict[str, Any] = Field(..., description="Cached design result")
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata",
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Cache creation timestamp",
    )
    expires_at: datetime = Field(..., description="Cache expiration timestamp")
    hit_count: int = Field(default=0, ge=0, description="Number of cache hits")
    last_accessed_at: Optional[datetime] = Field(
        default=None,
        description="Last access timestamp",
    )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for MongoDB storage.

        Returns:
            Dictionary representation
        """
        data = self.model_dump(exclude={"cache_key"})
        data["_id"] = self.cache_key
        data["user_id"] = ObjectId(self.user_id) if self.user_id else None
        data["organization_id"] = ObjectId(self.organization_id) if self.organization_id else None
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ArchitectureDesignCache":
        """Create from MongoDB document.

        Args:
            data: MongoDB document

        Returns:
            ArchitectureDesignCache instance
        """
        if "_id" in data:
            data["cache_key"] = str(data["_id"])
        if "user_id" in data and isinstance(data["user_id"], ObjectId):
            data["user_id"] = str(data["user_id"])
        if "organization_id" in data and isinstance(data["organization_id"], ObjectId):
            data["organization_id"] = str(data["organization_id"])
        return cls(**data)

    def is_expired(self) -> bool:
        """Check if cache entry is expired.

        Returns:
            True if expired, False otherwise
        """
        return datetime.utcnow() > self.expires_at

    def record_hit(self) -> None:
        """Record a cache hit."""
        self.hit_count += 1
        self.last_accessed_at = datetime.utcnow()


def generate_cache_key(
    action: str,
    user_id: str,
    project_type: Optional[str] = None,
    architecture_type: Optional[str] = None,
    cloud_provider: Optional[str] = None,
    compliance_standards: Optional[list[str]] = None,
    requirements: Optional[dict[str, Any]] = None,
) -> str:
    """Generate cache key from architecture design parameters.

    Args:
        action: Action type (initialize, design, review, optimize)
        user_id: User ID
        project_type: Project type
        architecture_type: Architecture pattern
        cloud_provider: Cloud provider
        compliance_standards: Compliance standards list
        requirements: Requirements dictionary

    Returns:
        Cache key (SHA256 hash)
    """
    key_parts = [
        action,
        user_id,
        project_type or "",
        architecture_type or "",
        cloud_provider or "",
    ]

    if compliance_standards:
        key_parts.append("|".join(sorted(compliance_standards)))

    if requirements:
        requirements_str = json.dumps(requirements, sort_keys=True)
        requirements_hash = hashlib.sha256(requirements_str.encode()).hexdigest()[:16]
        key_parts.append(requirements_hash)

    key_string = "|".join(key_parts)
    return hashlib.sha256(key_string.encode()).hexdigest()


def get_cache_ttl(action: str) -> timedelta:
    """Get cache TTL based on action type.

    Args:
        action: Action type

    Returns:
        Timedelta for cache expiration
    """
    if action == "review":
        return timedelta(days=30)
    elif action == "design":
        return timedelta(days=7)
    elif action == "optimize":
        return timedelta(days=3)
    else:
        return timedelta(days=7)

