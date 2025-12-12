"""Unit tests for RetrievalEvaluationService.

Tests IR metrics calculation: MRR, NDCG, Precision@K, Recall@K, Hit Rate.
"""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

from api.services.retrieval_evaluation_service import (
    RetrievalEvaluationService,
    RelevanceFeedback,
    EvaluationMetrics,
)


class TestRetrievalEvaluationService:
    """Tests for RetrievalEvaluationService."""

    @pytest.fixture
    def service(self):
        """Create evaluation service instance."""
        with patch("api.services.retrieval_evaluation_service.async_mongodb_adapter") as mock_db:
            mock_db.get_collection = AsyncMock()
            return RetrievalEvaluationService()

    @pytest.fixture
    def sample_feedback(self):
        """Sample relevance feedback data."""
        return RelevanceFeedback(
            query_id="query-123",
            query_text="kubernetes deployment best practices",
            result_id="chunk-456",
            relevance_score=3,  # Scale of 0-3
            user_id="user-789",
        )

    def test_relevance_feedback_creation(self, sample_feedback):
        """Test RelevanceFeedback dataclass creation."""
        assert sample_feedback.query_id == "query-123"
        assert sample_feedback.relevance_score == 3
        assert sample_feedback.user_id == "user-789"

    def test_relevance_feedback_to_dict(self, sample_feedback):
        """Test RelevanceFeedback conversion to dictionary."""
        result = sample_feedback.to_dict()
        
        assert result["query_id"] == "query-123"
        assert result["relevance_score"] == 3
        assert "timestamp" in result

    def test_evaluation_metrics_defaults(self):
        """Test EvaluationMetrics default values."""
        metrics = EvaluationMetrics()
        
        assert metrics.mrr == 0.0
        assert metrics.ndcg_at_5 == 0.0
        assert metrics.ndcg_at_10 == 0.0
        assert metrics.precision_at_5 == 0.0
        assert metrics.precision_at_10 == 0.0
        assert metrics.recall_at_5 == 0.0
        assert metrics.recall_at_10 == 0.0
        assert metrics.hit_rate_at_5 == 0.0
        assert metrics.hit_rate_at_10 == 0.0
        assert metrics.total_queries == 0

    def test_compute_mrr_first_relevant(self, service):
        """Test MRR when first result is relevant."""
        # First result is relevant -> MRR = 1.0
        rankings = [1]  # Position 1 is relevant
        mrr = service._compute_mrr(rankings)
        
        assert mrr == 1.0

    def test_compute_mrr_second_relevant(self, service):
        """Test MRR when second result is first relevant."""
        # Second result is first relevant -> MRR = 0.5
        rankings = [2]  # First relevant at position 2
        mrr = service._compute_mrr(rankings)
        
        assert mrr == 0.5

    def test_compute_mrr_multiple_queries(self, service):
        """Test MRR across multiple queries."""
        # Query 1: relevant at position 1 (RR=1.0)
        # Query 2: relevant at position 2 (RR=0.5)
        # Query 3: relevant at position 5 (RR=0.2)
        # MRR = (1.0 + 0.5 + 0.2) / 3 = 0.567
        rankings = [1, 2, 5]
        mrr = service._compute_mrr(rankings)
        
        assert abs(mrr - 0.567) < 0.01

    def test_compute_ndcg_perfect_ranking(self, service):
        """Test NDCG with perfect ranking."""
        # Relevance scores in perfect order (3, 2, 1, 0)
        relevances = [3, 2, 1, 0]
        ndcg = service._compute_ndcg(relevances, k=4)
        
        # Perfect ranking should give NDCG = 1.0
        assert ndcg == 1.0

    def test_compute_ndcg_worst_ranking(self, service):
        """Test NDCG with reversed (worst) ranking."""
        # Relevance scores in worst order (0, 1, 2, 3)
        relevances = [0, 1, 2, 3]
        ideal_relevances = [3, 2, 1, 0]
        
        ndcg = service._compute_ndcg(relevances, k=4)
        
        # Worst ranking should give lower NDCG
        assert ndcg < 1.0

    def test_compute_precision_at_k(self, service):
        """Test Precision@K calculation."""
        # 3 relevant out of 5 results
        relevant_flags = [True, False, True, False, True]
        precision = service._compute_precision_at_k(relevant_flags, k=5)
        
        assert precision == 0.6  # 3/5

    def test_compute_precision_at_k_all_relevant(self, service):
        """Test Precision@K when all results are relevant."""
        relevant_flags = [True, True, True, True, True]
        precision = service._compute_precision_at_k(relevant_flags, k=5)
        
        assert precision == 1.0

    def test_compute_precision_at_k_none_relevant(self, service):
        """Test Precision@K when no results are relevant."""
        relevant_flags = [False, False, False, False, False]
        precision = service._compute_precision_at_k(relevant_flags, k=5)
        
        assert precision == 0.0

    def test_compute_recall_at_k(self, service):
        """Test Recall@K calculation."""
        # 3 relevant retrieved out of 5 total relevant
        retrieved_relevant = 3
        total_relevant = 5
        recall = service._compute_recall_at_k(retrieved_relevant, total_relevant)
        
        assert recall == 0.6  # 3/5

    def test_compute_recall_at_k_all_retrieved(self, service):
        """Test Recall@K when all relevant are retrieved."""
        recall = service._compute_recall_at_k(5, 5)
        assert recall == 1.0

    def test_compute_recall_at_k_zero_relevant(self, service):
        """Test Recall@K when there are no relevant documents."""
        recall = service._compute_recall_at_k(0, 0)
        assert recall == 0.0  # Handle division by zero

    def test_compute_hit_rate(self, service):
        """Test Hit Rate calculation."""
        # 7 out of 10 queries had at least one relevant result
        queries_with_hits = 7
        total_queries = 10
        hit_rate = service._compute_hit_rate(queries_with_hits, total_queries)
        
        assert hit_rate == 0.7

    @pytest.mark.asyncio
    async def test_record_feedback(self, service, sample_feedback):
        """Test recording relevance feedback."""
        mock_collection = AsyncMock()
        mock_collection.insert_one = AsyncMock(return_value=MagicMock(inserted_id="feedback-id"))
        
        with patch.object(service, "_get_feedback_collection", return_value=mock_collection):
            result = await service.record_feedback(sample_feedback)
            
            mock_collection.insert_one.assert_called_once()
            assert result is not None

