"""Unit tests for HybridRetrievalService.

Tests the hybrid search combining semantic embeddings and BM25 with RRF fusion.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from api.services.hybrid_retrieval_service import (
    HybridRetrievalService,
    RetrievalResult,
    SearchConfig,
)


class TestHybridRetrievalService:
    """Tests for HybridRetrievalService."""

    @pytest.fixture
    def service(self):
        """Create hybrid retrieval service instance."""
        with patch("api.services.hybrid_retrieval_service.settings") as mock_settings:
            mock_settings.pinecone_api_key = "test-key"
            mock_settings.pinecone_index_name = "test-index"
            mock_settings.gemini_api_key = "test-gemini-key"
            return HybridRetrievalService()

    @pytest.fixture
    def mock_embedding_response(self):
        """Mock embedding vector."""
        return [0.1] * 768  # Standard embedding dimension

    @pytest.fixture
    def sample_chunks(self):
        """Sample chunks for testing."""
        return [
            {
                "chunk_id": "chunk-1",
                "contextualized_content": "Kubernetes deployment best practices for production",
                "original_content": "Best practices for production",
                "source_url": "https://docs.example.com/k8s",
                "document_title": "K8s Guide",
                "user_id": "user-123",
            },
            {
                "chunk_id": "chunk-2",
                "contextualized_content": "Docker container security hardening guide",
                "original_content": "Security hardening guide",
                "source_url": "https://docs.example.com/docker",
                "document_title": "Docker Security",
                "user_id": "user-123",
            },
        ]

    def test_retrieval_result_creation(self):
        """Test RetrievalResult dataclass creation."""
        result = RetrievalResult(
            chunk_id="test-chunk",
            content="Test content",
            score=0.85,
            source_url="https://example.com",
            document_title="Test Doc",
            retrieval_method="hybrid",
        )
        
        assert result.chunk_id == "test-chunk"
        assert result.score == 0.85
        assert result.retrieval_method == "hybrid"

    def test_retrieval_result_to_dict(self):
        """Test RetrievalResult conversion to dictionary."""
        result = RetrievalResult(
            chunk_id="test-chunk",
            content="Test content",
            score=0.85,
            source_url="https://example.com",
            document_title="Test Doc",
            retrieval_method="semantic",
            metadata={"key": "value"},
        )
        
        result_dict = result.to_dict()
        
        assert result_dict["chunk_id"] == "test-chunk"
        assert result_dict["score"] == 0.85
        assert result_dict["metadata"]["key"] == "value"

    def test_search_config_defaults(self):
        """Test SearchConfig default values."""
        config = SearchConfig()
        
        assert config.semantic_weight == 0.5
        assert config.bm25_weight == 0.5
        assert config.top_k == 10
        assert config.min_score == 0.0
        assert config.rrf_k == 60

    def test_search_config_custom_values(self):
        """Test SearchConfig with custom values."""
        config = SearchConfig(
            semantic_weight=0.7,
            bm25_weight=0.3,
            top_k=20,
            min_score=0.5,
        )
        
        assert config.semantic_weight == 0.7
        assert config.bm25_weight == 0.3
        assert config.top_k == 20
        assert config.min_score == 0.5

    def test_compute_rrf_score(self, service):
        """Test RRF score computation."""
        # RRF formula: 1 / (k + rank)
        # With k=60 (default), rank 1 should give 1/61 ≈ 0.0164
        score = service._compute_rrf_score(rank=1, k=60)
        expected = 1.0 / (60 + 1)
        
        assert abs(score - expected) < 0.0001

    def test_compute_rrf_score_higher_rank(self, service):
        """Test RRF score decreases with higher rank."""
        score_rank_1 = service._compute_rrf_score(rank=1, k=60)
        score_rank_10 = service._compute_rrf_score(rank=10, k=60)
        
        assert score_rank_1 > score_rank_10

    def test_bm25_tokenize(self, service):
        """Test BM25 tokenization."""
        text = "Kubernetes deployment best practices"
        tokens = service._bm25_tokenize(text)
        
        assert "kubernetes" in tokens
        assert "deployment" in tokens
        assert "best" in tokens
        assert "practices" in tokens
        assert all(t.islower() for t in tokens)

    def test_bm25_tokenize_removes_stopwords(self, service):
        """Test BM25 tokenization removes common stopwords."""
        text = "the deployment is a best practice for the system"
        tokens = service._bm25_tokenize(text)
        
        # Common stopwords should be filtered
        assert "the" not in tokens
        assert "is" not in tokens
        assert "a" not in tokens
        assert "for" not in tokens
        # Content words should remain
        assert "deployment" in tokens
        assert "best" in tokens
        assert "practice" in tokens

