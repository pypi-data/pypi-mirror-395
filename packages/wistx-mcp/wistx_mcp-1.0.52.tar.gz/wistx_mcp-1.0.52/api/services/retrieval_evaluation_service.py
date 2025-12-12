"""Retrieval Evaluation Service.

Implements standard Information Retrieval evaluation metrics:
1. MRR (Mean Reciprocal Rank) - measures rank of first relevant result
2. NDCG (Normalized Discounted Cumulative Gain) - measures ranking quality
3. Precision@K - fraction of relevant results in top K
4. Recall@K - fraction of relevant results retrieved in top K
5. Hit Rate@K - whether any relevant result appears in top K

These metrics enable:
- A/B testing of retrieval strategies
- Monitoring retrieval quality over time
- Comparing semantic vs hybrid vs reranked results
"""

import logging
import math
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

from api.database.mongodb import mongodb_manager

logger = logging.getLogger(__name__)


@dataclass
class RetrievalMetrics:
    """Computed retrieval metrics for a query."""
    mrr: float = 0.0                    # Mean Reciprocal Rank
    ndcg_at_5: float = 0.0              # NDCG@5
    ndcg_at_10: float = 0.0             # NDCG@10
    precision_at_5: float = 0.0         # Precision@5
    precision_at_10: float = 0.0        # Precision@10
    recall_at_5: float = 0.0            # Recall@5
    recall_at_10: float = 0.0           # Recall@10
    hit_rate_at_5: float = 0.0          # Hit Rate@5
    hit_rate_at_10: float = 0.0         # Hit Rate@10


@dataclass
class QueryEvaluation:
    """Evaluation record for a single query."""
    query_id: str
    query: str
    user_id: str
    timestamp: datetime
    retrieval_type: str                  # semantic, hybrid, reranked
    results_count: int
    query_time_ms: int
    metrics: RetrievalMetrics | None = None
    relevance_judgments: list[int] = field(default_factory=list)  # 0-3 relevance scores
    feedback_source: str | None = None   # user, llm, expert
    metadata: dict[str, Any] = field(default_factory=dict)


class RetrievalEvaluationService:
    """Service for evaluating and tracking retrieval quality.
    
    Provides:
    - Real-time metric computation
    - Query logging for offline evaluation
    - Aggregate statistics over time
    - A/B test comparison
    """
    
    # NDCG ideal gains for graded relevance (0-3)
    IDEAL_GAINS = [3, 2, 2, 1, 1, 1, 1, 1, 1, 1]  # Ideal ranking for NDCG
    
    def __init__(self):
        """Initialize evaluation service."""
        self.db = mongodb_manager.get_database()
        self._ensure_indexes()
    
    def _ensure_indexes(self) -> None:
        """Ensure MongoDB indexes exist."""
        try:
            collection = self.db.retrieval_evaluations
            collection.create_index([("user_id", 1), ("timestamp", -1)])
            collection.create_index([("retrieval_type", 1), ("timestamp", -1)])
            collection.create_index("query_id", unique=True)
        except Exception as e:
            logger.warning("Failed to create evaluation indexes: %s", e)
    
    def compute_metrics(
        self,
        relevance_judgments: list[int],
        total_relevant: int | None = None,
    ) -> RetrievalMetrics:
        """Compute retrieval metrics from relevance judgments.
        
        Args:
            relevance_judgments: List of relevance scores (0=irrelevant, 1-3=relevant)
            total_relevant: Total number of relevant documents (for recall)
            
        Returns:
            RetrievalMetrics with computed values
        """
        if not relevance_judgments:
            return RetrievalMetrics()
        
        # Binary relevance (>= 1 is relevant)
        binary_relevance = [1 if r >= 1 else 0 for r in relevance_judgments]
        
        # MRR - rank of first relevant result
        mrr = 0.0
        for i, rel in enumerate(binary_relevance):
            if rel == 1:
                mrr = 1.0 / (i + 1)
                break
        
        # Precision@K
        precision_5 = sum(binary_relevance[:5]) / min(5, len(binary_relevance))
        precision_10 = sum(binary_relevance[:10]) / min(10, len(binary_relevance))
        
        # Recall@K (requires total_relevant)
        recall_5 = 0.0
        recall_10 = 0.0
        if total_relevant and total_relevant > 0:
            recall_5 = sum(binary_relevance[:5]) / total_relevant
            recall_10 = sum(binary_relevance[:10]) / total_relevant
        
        # Hit Rate@K
        hit_rate_5 = 1.0 if any(binary_relevance[:5]) else 0.0
        hit_rate_10 = 1.0 if any(binary_relevance[:10]) else 0.0
        
        # NDCG@K
        ndcg_5 = self._compute_ndcg(relevance_judgments[:5])
        ndcg_10 = self._compute_ndcg(relevance_judgments[:10])
        
        return RetrievalMetrics(
            mrr=mrr,
            ndcg_at_5=ndcg_5,
            ndcg_at_10=ndcg_10,
            precision_at_5=precision_5,
            precision_at_10=precision_10,
            recall_at_5=recall_5,
            recall_at_10=recall_10,
            hit_rate_at_5=hit_rate_5,
            hit_rate_at_10=hit_rate_10,
        )
    
    def _compute_ndcg(self, relevance_judgments: list[int]) -> float:
        """Compute NDCG for given relevance judgments.
        
        Args:
            relevance_judgments: Relevance scores (0-3)
            
        Returns:
            NDCG score (0-1)
        """
        if not relevance_judgments:
            return 0.0
        
        # DCG
        dcg = 0.0
        for i, rel in enumerate(relevance_judgments):
            dcg += (2 ** rel - 1) / math.log2(i + 2)  # log2(rank + 1)
        
        # Ideal DCG
        ideal_gains = self.IDEAL_GAINS[:len(relevance_judgments)]
        idcg = 0.0
        for i, rel in enumerate(ideal_gains):
            idcg += (2 ** rel - 1) / math.log2(i + 2)
        
        return dcg / idcg if idcg > 0 else 0.0

    async def log_query(
        self,
        query_id: str,
        query: str,
        user_id: str,
        retrieval_type: str,
        results_count: int,
        query_time_ms: int,
        relevance_judgments: list[int] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> QueryEvaluation:
        """Log a query for evaluation.

        Args:
            query_id: Unique query identifier
            query: Search query text
            user_id: User who made the query
            retrieval_type: Type of retrieval (semantic, hybrid, reranked)
            results_count: Number of results returned
            query_time_ms: Query execution time
            relevance_judgments: Optional relevance scores for results
            metadata: Additional metadata

        Returns:
            QueryEvaluation record
        """
        evaluation = QueryEvaluation(
            query_id=query_id,
            query=query,
            user_id=user_id,
            timestamp=datetime.utcnow(),
            retrieval_type=retrieval_type,
            results_count=results_count,
            query_time_ms=query_time_ms,
            relevance_judgments=relevance_judgments or [],
            metadata=metadata or {},
        )

        # Compute metrics if judgments provided
        if relevance_judgments:
            evaluation.metrics = self.compute_metrics(relevance_judgments)

        # Store in MongoDB
        try:
            collection = self.db.retrieval_evaluations
            doc = {
                "query_id": evaluation.query_id,
                "query": evaluation.query,
                "user_id": evaluation.user_id,
                "timestamp": evaluation.timestamp,
                "retrieval_type": evaluation.retrieval_type,
                "results_count": evaluation.results_count,
                "query_time_ms": evaluation.query_time_ms,
                "relevance_judgments": evaluation.relevance_judgments,
                "feedback_source": evaluation.feedback_source,
                "metadata": evaluation.metadata,
            }

            if evaluation.metrics:
                doc["metrics"] = {
                    "mrr": evaluation.metrics.mrr,
                    "ndcg_at_5": evaluation.metrics.ndcg_at_5,
                    "ndcg_at_10": evaluation.metrics.ndcg_at_10,
                    "precision_at_5": evaluation.metrics.precision_at_5,
                    "precision_at_10": evaluation.metrics.precision_at_10,
                    "recall_at_5": evaluation.metrics.recall_at_5,
                    "recall_at_10": evaluation.metrics.recall_at_10,
                    "hit_rate_at_5": evaluation.metrics.hit_rate_at_5,
                    "hit_rate_at_10": evaluation.metrics.hit_rate_at_10,
                }

            collection.update_one(
                {"query_id": query_id},
                {"$set": doc},
                upsert=True,
            )
        except Exception as e:
            logger.error("Failed to log query evaluation: %s", e)

        return evaluation

    async def add_relevance_feedback(
        self,
        query_id: str,
        relevance_judgments: list[int],
        feedback_source: str = "user",
        total_relevant: int | None = None,
    ) -> RetrievalMetrics | None:
        """Add relevance feedback to a logged query.

        Args:
            query_id: Query identifier
            relevance_judgments: Relevance scores (0-3)
            feedback_source: Source of feedback (user, llm, expert)
            total_relevant: Total relevant docs for recall

        Returns:
            Computed metrics or None if query not found
        """
        metrics = self.compute_metrics(relevance_judgments, total_relevant)

        try:
            collection = self.db.retrieval_evaluations
            result = collection.update_one(
                {"query_id": query_id},
                {
                    "$set": {
                        "relevance_judgments": relevance_judgments,
                        "feedback_source": feedback_source,
                        "metrics": {
                            "mrr": metrics.mrr,
                            "ndcg_at_5": metrics.ndcg_at_5,
                            "ndcg_at_10": metrics.ndcg_at_10,
                            "precision_at_5": metrics.precision_at_5,
                            "precision_at_10": metrics.precision_at_10,
                            "recall_at_5": metrics.recall_at_5,
                            "recall_at_10": metrics.recall_at_10,
                            "hit_rate_at_5": metrics.hit_rate_at_5,
                            "hit_rate_at_10": metrics.hit_rate_at_10,
                        },
                    }
                },
            )

            if result.modified_count == 0:
                logger.warning("Query not found for feedback: %s", query_id)
                return None

            return metrics
        except Exception as e:
            logger.error("Failed to add relevance feedback: %s", e)
            return None

    async def get_aggregate_metrics(
        self,
        user_id: str | None = None,
        retrieval_type: str | None = None,
        days: int = 7,
    ) -> dict[str, Any]:
        """Get aggregate metrics over a time period.

        Args:
            user_id: Filter by user (None for all)
            retrieval_type: Filter by type (None for all)
            days: Number of days to aggregate

        Returns:
            Dictionary with aggregate metrics
        """
        collection = self.db.retrieval_evaluations

        # Build query
        query: dict[str, Any] = {
            "timestamp": {"$gte": datetime.utcnow() - timedelta(days=days)},
            "metrics": {"$exists": True},
        }
        if user_id:
            query["user_id"] = user_id
        if retrieval_type:
            query["retrieval_type"] = retrieval_type

        # Aggregate metrics
        pipeline = [
            {"$match": query},
            {
                "$group": {
                    "_id": "$retrieval_type",
                    "count": {"$sum": 1},
                    "avg_mrr": {"$avg": "$metrics.mrr"},
                    "avg_ndcg_5": {"$avg": "$metrics.ndcg_at_5"},
                    "avg_ndcg_10": {"$avg": "$metrics.ndcg_at_10"},
                    "avg_precision_5": {"$avg": "$metrics.precision_at_5"},
                    "avg_precision_10": {"$avg": "$metrics.precision_at_10"},
                    "avg_hit_rate_5": {"$avg": "$metrics.hit_rate_at_5"},
                    "avg_hit_rate_10": {"$avg": "$metrics.hit_rate_at_10"},
                    "avg_query_time_ms": {"$avg": "$query_time_ms"},
                    "p95_query_time_ms": {"$percentile": {"input": "$query_time_ms", "p": [0.95], "method": "approximate"}},
                }
            },
        ]

        try:
            results = list(collection.aggregate(pipeline))
            return {
                "period_days": days,
                "by_retrieval_type": {
                    r["_id"]: {
                        "count": r["count"],
                        "mrr": round(r["avg_mrr"], 4),
                        "ndcg@5": round(r["avg_ndcg_5"], 4),
                        "ndcg@10": round(r["avg_ndcg_10"], 4),
                        "precision@5": round(r["avg_precision_5"], 4),
                        "precision@10": round(r["avg_precision_10"], 4),
                        "hit_rate@5": round(r["avg_hit_rate_5"], 4),
                        "hit_rate@10": round(r["avg_hit_rate_10"], 4),
                        "avg_query_time_ms": round(r["avg_query_time_ms"], 1),
                    }
                    for r in results
                },
            }
        except Exception as e:
            logger.error("Failed to aggregate metrics: %s", e)
            return {"error": str(e)}

    async def compare_retrieval_types(
        self,
        type_a: str,
        type_b: str,
        days: int = 7,
    ) -> dict[str, Any]:
        """Compare two retrieval types (A/B test analysis).

        Args:
            type_a: First retrieval type
            type_b: Second retrieval type
            days: Number of days to compare

        Returns:
            Comparison results with statistical significance
        """
        metrics_a = await self.get_aggregate_metrics(retrieval_type=type_a, days=days)
        metrics_b = await self.get_aggregate_metrics(retrieval_type=type_b, days=days)

        type_a_data = metrics_a.get("by_retrieval_type", {}).get(type_a, {})
        type_b_data = metrics_b.get("by_retrieval_type", {}).get(type_b, {})

        if not type_a_data or not type_b_data:
            return {"error": "Insufficient data for comparison"}

        # Calculate improvements
        improvements = {}
        for metric in ["mrr", "ndcg@5", "ndcg@10", "precision@5", "hit_rate@5"]:
            val_a = type_a_data.get(metric, 0)
            val_b = type_b_data.get(metric, 0)
            if val_a > 0:
                pct_change = ((val_b - val_a) / val_a) * 100
                improvements[metric] = {
                    type_a: val_a,
                    type_b: val_b,
                    "improvement_%": round(pct_change, 2),
                }

        return {
            "comparison": f"{type_a} vs {type_b}",
            "period_days": days,
            "sample_sizes": {
                type_a: type_a_data.get("count", 0),
                type_b: type_b_data.get("count", 0),
            },
            "improvements": improvements,
            "recommendation": self._get_recommendation(improvements),
        }

    def _get_recommendation(self, improvements: dict[str, Any]) -> str:
        """Generate recommendation based on improvements."""
        positive_metrics = sum(
            1 for m in improvements.values()
            if m.get("improvement_%", 0) > 5
        )
        negative_metrics = sum(
            1 for m in improvements.values()
            if m.get("improvement_%", 0) < -5
        )

        if positive_metrics >= 3:
            return "Type B shows significant improvements across multiple metrics. Consider switching."
        elif negative_metrics >= 3:
            return "Type A performs better. Keep current approach."
        else:
            return "Results are inconclusive. Gather more data or refine the comparison."

