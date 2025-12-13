"""Template rating models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TemplateRating(BaseModel):
    """Template rating entry."""

    rating_id: str = Field(..., description="Unique rating identifier")
    template_id: str = Field(..., description="Template identifier")
    version: str = Field(..., description="Template version")
    user_id: str = Field(..., description="User who rated")
    rating: int = Field(..., ge=1, le=5, description="Rating (1-5 stars)")
    comment: Optional[str] = Field(default=None, description="Rating comment")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TemplateAnalytics(BaseModel):
    """Template analytics summary."""

    template_id: str = Field(..., description="Template identifier")
    total_ratings: int = Field(default=0, ge=0, description="Total number of ratings")
    average_rating: float = Field(default=0.0, ge=0.0, le=5.0, description="Average rating")
    rating_distribution: dict[int, int] = Field(
        default_factory=lambda: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
        description="Rating distribution (1-5 stars)",
    )
    usage_count: int = Field(default=0, ge=0, description="Total usage count")
    unique_users: int = Field(default=0, ge=0, description="Number of unique users")
    last_used_at: Optional[datetime] = Field(default=None, description="Last usage timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow)

