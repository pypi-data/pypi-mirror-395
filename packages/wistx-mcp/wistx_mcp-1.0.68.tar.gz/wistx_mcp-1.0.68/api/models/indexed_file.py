"""Model for tracking indexed files (checkpoint system)."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class IndexedFile(BaseModel):
    """Model for tracking indexed files (checkpoint system).
    
    Used to enable resume capability and prevent re-processing
    unchanged files.
    """

    resource_id: str = Field(..., description="Resource ID")
    file_path: str = Field(..., description="Relative file path from repo root")
    commit_sha: str = Field(..., description="Commit SHA when file was processed")
    file_hash: str = Field(..., description="SHA-256 hash of file content")
    processed_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Processing timestamp",
    )
    articles_created: int = Field(
        default=0,
        ge=0,
        description="Number of articles created from this file",
    )
    file_size_mb: float = Field(
        default=0.0,
        ge=0.0,
        description="File size in MB",
    )
    status: str = Field(
        default="completed",
        description="Processing status: completed, failed, skipped",
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message if status is failed",
    )

    def to_dict(self) -> dict:
        """Convert to dictionary for MongoDB storage.
        
        Returns:
            Dictionary representation
        """
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict) -> "IndexedFile":
        """Create from MongoDB document.
        
        Args:
            data: MongoDB document
            
        Returns:
            IndexedFile instance
        """
        return cls(**data)

