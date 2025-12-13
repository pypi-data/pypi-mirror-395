"""Retrieval Evaluation API endpoints.

Provides endpoints for:
- Logging query evaluations
- Adding relevance feedback
- Viewing aggregate metrics
- A/B test comparisons
"""

import logging
import time
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from api.dependencies import get_current_user
from api.services.retrieval_evaluation_service import RetrievalEvaluationService
from api.models.v1_responses import APIResponse, ErrorResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/evaluation", tags=["evaluation"])

evaluation_service = RetrievalEvaluationService()


class RelevanceFeedbackRequest(BaseModel):
    """Request to add relevance feedback to a query."""
    query_id: str = Field(..., description="Query identifier")
    relevance_judgments: list[int] = Field(
        ...,
        description="Relevance scores for each result (0=irrelevant, 1=marginal, 2=relevant, 3=highly relevant)",
    )
    feedback_source: str = Field(
        default="user",
        description="Source of feedback (user, llm, expert)",
    )
    total_relevant: int | None = Field(
        default=None,
        description="Total number of relevant documents (for recall calculation)",
    )


class MetricsQueryParams(BaseModel):
    """Query parameters for metrics endpoints."""
    days: int = Field(default=7, ge=1, le=90, description="Number of days to aggregate")
    retrieval_type: str | None = Field(default=None, description="Filter by retrieval type")


class ComparisonRequest(BaseModel):
    """Request to compare two retrieval types."""
    type_a: str = Field(..., description="First retrieval type to compare")
    type_b: str = Field(..., description="Second retrieval type to compare")
    days: int = Field(default=7, ge=1, le=90, description="Number of days to compare")


@router.post(
    "/feedback",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Add relevance feedback",
    description="Add relevance judgments to a logged query for evaluation",
)
async def add_relevance_feedback(
    request: RelevanceFeedbackRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> APIResponse:
    """Add relevance feedback for a query.
    
    Relevance scale:
    - 0: Irrelevant
    - 1: Marginally relevant
    - 2: Relevant
    - 3: Highly relevant
    """
    start_time = time.time()
    
    # Validate relevance judgments
    if not all(0 <= r <= 3 for r in request.relevance_judgments):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Relevance judgments must be 0-3",
        )
    
    metrics = await evaluation_service.add_relevance_feedback(
        query_id=request.query_id,
        relevance_judgments=request.relevance_judgments,
        feedback_source=request.feedback_source,
        total_relevant=request.total_relevant,
    )
    
    if metrics is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Query not found: {request.query_id}",
        )
    
    return APIResponse(
        data={
            "query_id": request.query_id,
            "metrics": {
                "mrr": metrics.mrr,
                "ndcg@5": metrics.ndcg_at_5,
                "ndcg@10": metrics.ndcg_at_10,
                "precision@5": metrics.precision_at_5,
                "precision@10": metrics.precision_at_10,
                "hit_rate@5": metrics.hit_rate_at_5,
                "hit_rate@10": metrics.hit_rate_at_10,
            },
        },
        metadata={
            "timestamp": time.time(),
            "query_time_ms": int((time.time() - start_time) * 1000),
        },
    )


@router.get(
    "/metrics",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Get aggregate metrics",
    description="Get aggregate retrieval metrics over a time period",
)
async def get_aggregate_metrics(
    days: int = 7,
    retrieval_type: str | None = None,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> APIResponse:
    """Get aggregate retrieval metrics.
    
    Returns average MRR, NDCG, precision, and hit rate
    across all queries in the specified time period.
    """
    start_time = time.time()
    user_id = current_user.get("user_id")
    
    metrics = await evaluation_service.get_aggregate_metrics(
        user_id=user_id,
        retrieval_type=retrieval_type,
        days=days,
    )
    
    return APIResponse(
        data=metrics,
        metadata={
            "timestamp": time.time(),
            "query_time_ms": int((time.time() - start_time) * 1000),
        },
    )


@router.get(
    "/metrics/global",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Get global aggregate metrics",
    description="Get aggregate retrieval metrics across all users (admin only)",
)
async def get_global_metrics(
    days: int = 7,
    retrieval_type: str | None = None,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> APIResponse:
    """Get global aggregate metrics across all users.

    Note: This endpoint may be restricted to admins in production.
    """
    start_time = time.time()

    metrics = await evaluation_service.get_aggregate_metrics(
        user_id=None,  # All users
        retrieval_type=retrieval_type,
        days=days,
    )

    return APIResponse(
        data=metrics,
        metadata={
            "timestamp": time.time(),
            "query_time_ms": int((time.time() - start_time) * 1000),
        },
    )


@router.post(
    "/compare",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Compare retrieval types",
    description="A/B test comparison between two retrieval strategies",
)
async def compare_retrieval_types(
    request: ComparisonRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> APIResponse:
    """Compare two retrieval types.

    Compares metrics between two retrieval strategies
    (e.g., 'semantic' vs 'hybrid' or 'hybrid' vs 'reranked').

    Returns improvement percentages and a recommendation.
    """
    start_time = time.time()

    comparison = await evaluation_service.compare_retrieval_types(
        type_a=request.type_a,
        type_b=request.type_b,
        days=request.days,
    )

    return APIResponse(
        data=comparison,
        metadata={
            "timestamp": time.time(),
            "query_time_ms": int((time.time() - start_time) * 1000),
        },
    )


@router.get(
    "/cache/stats",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Get cache statistics",
    description="Get retrieval cache hit/miss statistics",
)
async def get_cache_stats(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> APIResponse:
    """Get cache statistics for retrieval operations."""
    from api.services.retrieval_cache_service import RetrievalCacheService

    cache_service = RetrievalCacheService()
    stats = cache_service.get_stats()

    return APIResponse(
        data=stats,
        metadata={"timestamp": time.time()},
    )

