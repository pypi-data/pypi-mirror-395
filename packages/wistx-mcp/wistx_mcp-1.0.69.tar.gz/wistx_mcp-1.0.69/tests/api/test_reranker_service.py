"""Unit tests for RerankerService.

Tests the LLM-based reranking for improved retrieval precision.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from api.services.reranker_service import RerankerService
from api.services.hybrid_retrieval_service import RetrievalResult


class TestRerankerService:
    """Tests for RerankerService."""

    @pytest.fixture
    def service(self):
        """Create reranker service instance."""
        with patch("api.services.reranker_service.settings") as mock_settings:
            mock_settings.gemini_api_key = "test-key"
            return RerankerService()

    @pytest.fixture
    def sample_results(self):
        """Sample retrieval results for testing."""
        return [
            RetrievalResult(
                chunk_id="chunk-1",
                content="Kubernetes deployment strategies for production",
                score=0.85,
                source_url="https://docs.example.com/k8s",
                document_title="K8s Production Guide",
                retrieval_method="hybrid",
            ),
            RetrievalResult(
                chunk_id="chunk-2",
                content="Docker container best practices",
                score=0.80,
                source_url="https://docs.example.com/docker",
                document_title="Docker Guide",
                retrieval_method="hybrid",
            ),
            RetrievalResult(
                chunk_id="chunk-3",
                content="AWS EKS cluster configuration",
                score=0.75,
                source_url="https://docs.example.com/eks",
                document_title="EKS Setup",
                retrieval_method="hybrid",
            ),
        ]

    def test_service_initialization(self, service):
        """Test service initializes correctly."""
        assert service is not None
        assert hasattr(service, "rerank")

    @pytest.mark.asyncio
    async def test_rerank_empty_results(self, service):
        """Test reranking with empty results."""
        results = await service.rerank(
            query="test query",
            results=[],
        )
        
        assert results == []

    @pytest.mark.asyncio
    async def test_rerank_single_result(self, service, sample_results):
        """Test reranking with single result returns as-is."""
        single_result = [sample_results[0]]
        
        with patch.object(service, "_llm_rerank", new_callable=AsyncMock) as mock_llm:
            # Single result shouldn't need LLM reranking
            results = await service.rerank(
                query="kubernetes deployment",
                results=single_result,
            )
            
            assert len(results) == 1
            assert results[0].chunk_id == "chunk-1"

    @pytest.mark.asyncio
    async def test_rerank_preserves_all_results(self, service, sample_results):
        """Test reranking preserves all results."""
        with patch.object(service, "_llm_rerank", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = sample_results  # Return same order
            
            results = await service.rerank(
                query="kubernetes best practices",
                results=sample_results,
            )
            
            assert len(results) == len(sample_results)

    @pytest.mark.asyncio
    async def test_rerank_changes_order(self, service, sample_results):
        """Test reranking can change result order."""
        # Reverse order to simulate reranking
        reranked = list(reversed(sample_results))
        
        with patch.object(service, "_llm_rerank", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = reranked
            
            results = await service.rerank(
                query="AWS EKS configuration",
                results=sample_results,
            )
            
            # First result should now be EKS (was last)
            assert results[0].chunk_id == "chunk-3"

    def test_build_rerank_prompt(self, service, sample_results):
        """Test building the reranking prompt."""
        query = "kubernetes deployment strategies"
        prompt = service._build_rerank_prompt(query, sample_results)
        
        assert query in prompt
        assert "chunk-1" in prompt or "Kubernetes deployment" in prompt
        assert "relevance" in prompt.lower() or "rank" in prompt.lower()

    def test_calculate_relevance_boost(self, service):
        """Test relevance boost calculation based on query overlap."""
        query = "kubernetes deployment production"
        content = "Kubernetes deployment strategies for production environments"
        
        boost = service._calculate_relevance_boost(query, content)
        
        # High overlap should give positive boost
        assert boost > 0

    def test_calculate_relevance_boost_no_overlap(self, service):
        """Test relevance boost with no query overlap."""
        query = "terraform aws modules"
        content = "Docker container orchestration with Kubernetes"
        
        boost = service._calculate_relevance_boost(query, content)
        
        # No overlap should give zero or negative boost
        assert boost <= 0

    @pytest.mark.asyncio
    async def test_rerank_with_top_n(self, service, sample_results):
        """Test reranking with top_n limit."""
        with patch.object(service, "_llm_rerank", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = sample_results
            
            results = await service.rerank(
                query="kubernetes",
                results=sample_results,
                top_n=2,
            )
            
            assert len(results) == 2

    @pytest.mark.asyncio
    async def test_rerank_handles_llm_failure(self, service, sample_results):
        """Test reranking handles LLM failure gracefully."""
        with patch.object(service, "_llm_rerank", new_callable=AsyncMock) as mock_llm:
            mock_llm.side_effect = Exception("LLM API error")
            
            # Should fall back to original order
            results = await service.rerank(
                query="kubernetes",
                results=sample_results,
            )
            
            # Should return original results on failure
            assert len(results) == len(sample_results)
            assert results[0].chunk_id == sample_results[0].chunk_id

