"""Predictive cache models for infrastructure-aware caching."""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class CacheEntryType(str, Enum):
    """Type of cache entry."""

    FILE_CONTENT = "file_content"
    SEARCH_RESULT = "search_result"
    CONTEXT = "context"
    ANALYSIS = "analysis"
    DEPENDENCY_GRAPH = "dependency_graph"


class CacheStatus(str, Enum):
    """Status of cache entry."""

    ACTIVE = "active"
    EXPIRED = "expired"
    INVALIDATED = "invalidated"


class DependencyType(str, Enum):
    """Type of dependency."""

    DIRECT = "direct"
    TRANSITIVE = "transitive"
    REVERSE = "reverse"
    RELATED = "related"


class CacheEntry(BaseModel):
    """Cache entry model."""

    cache_id: str = Field(
        ...,
        description="Unique cache identifier (e.g., 'cache_abc123')",
        min_length=10,
        max_length=100,
    )
    user_id: str = Field(..., description="User ID who owns this cache")
    resource_id: str = Field(..., description="Resource ID")
    entry_type: CacheEntryType = Field(..., description="Type of cache entry")
    key: str = Field(..., description="Cache key (e.g., file path, search query)")
    value: dict[str, Any] = Field(..., description="Cached value")
    dependencies: list[str] = Field(
        default_factory=list,
        description="List of dependency keys",
    )
    access_count: int = Field(
        default=0,
        ge=0,
        description="Number of times accessed",
    )
    last_accessed_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last access timestamp",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp",
    )
    expires_at: Optional[datetime] = Field(
        default=None,
        description="Expiration timestamp",
    )
    status: CacheStatus = Field(
        default=CacheStatus.ACTIVE,
        description="Cache status",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata",
    )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for MongoDB storage.

        Returns:
            Dictionary representation
        """
        data = self.model_dump(exclude={"cache_id"})
        data["_id"] = self.cache_id
        data["user_id"] = ObjectId(self.user_id) if self.user_id else None
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CacheEntry":
        """Create from MongoDB document.

        Args:
            data: MongoDB document

        Returns:
            CacheEntry instance
        """
        if "_id" in data:
            data["cache_id"] = str(data["_id"])
        if "user_id" in data and isinstance(data["user_id"], ObjectId):
            data["user_id"] = str(data["user_id"])
        return cls(**data)


class DependencyEntry(BaseModel):
    """Dependency entry model."""

    dependency_id: str = Field(
        ...,
        description="Unique dependency identifier",
        min_length=10,
        max_length=100,
    )
    resource_id: str = Field(..., description="Resource ID")
    source_path: str = Field(..., description="Source file path")
    target_path: str = Field(..., description="Target file path")
    dependency_type: DependencyType = Field(..., description="Type of dependency")
    strength: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Dependency strength (0.0-1.0)",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp",
    )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for MongoDB storage.

        Returns:
            Dictionary representation
        """
        data = self.model_dump(exclude={"dependency_id"})
        data["_id"] = self.dependency_id
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DependencyEntry":
        """Create from MongoDB document.

        Args:
            data: MongoDB document

        Returns:
            DependencyEntry instance
        """
        if "_id" in data:
            data["dependency_id"] = str(data["_id"])
        return cls(**data)


class UsagePattern(BaseModel):
    """Usage pattern model for tracking access patterns."""

    pattern_id: str = Field(
        ...,
        description="Unique pattern identifier",
        min_length=10,
        max_length=100,
    )
    user_id: str = Field(..., description="User ID")
    resource_id: str = Field(..., description="Resource ID")
    path: str = Field(..., description="File path")
    access_type: str = Field(..., description="Access type (read, search, list)")
    next_accesses: list[dict[str, Any]] = Field(
        default_factory=list,
        description="List of next accesses with frequencies",
    )
    time_patterns: dict[str, Any] = Field(
        default_factory=dict,
        description="Time-based patterns",
    )
    user_patterns: dict[str, Any] = Field(
        default_factory=dict,
        description="User-based patterns",
    )
    access_count: int = Field(
        default=0,
        ge=0,
        description="Total access count",
    )
    last_accessed_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last access timestamp",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp",
    )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for MongoDB storage.

        Returns:
            Dictionary representation
        """
        data = self.model_dump(exclude={"pattern_id"})
        data["_id"] = self.pattern_id
        data["user_id"] = ObjectId(self.user_id) if self.user_id else None
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UsagePattern":
        """Create from MongoDB document.

        Args:
            data: MongoDB document

        Returns:
            UsagePattern instance
        """
        if "_id" in data:
            data["pattern_id"] = str(data["_id"])
        if "user_id" in data and isinstance(data["user_id"], ObjectId):
            data["user_id"] = str(data["user_id"])
        return cls(**data)

