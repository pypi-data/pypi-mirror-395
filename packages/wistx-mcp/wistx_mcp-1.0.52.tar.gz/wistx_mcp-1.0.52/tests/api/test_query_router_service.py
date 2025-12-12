"""Unit tests for QueryRouterService.

Tests the query routing logic that determines which knowledge base to search.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from api.services.query_router_service import (
    QueryRouterService,
    QueryTarget,
    RoutingDecision,
)


class TestQueryRouterService:
    """Tests for QueryRouterService."""

    @pytest.fixture
    def service(self):
        """Create query router service instance."""
        return QueryRouterService()

    def test_query_target_enum_values(self):
        """Test QueryTarget enum has expected values."""
        assert QueryTarget.USER_ONLY.value == "user_only"
        assert QueryTarget.GLOBAL_ONLY.value == "global_only"
        assert QueryTarget.USER_FIRST.value == "user_first"
        assert QueryTarget.GLOBAL_FIRST.value == "global_first"
        assert QueryTarget.BOTH_PARALLEL.value == "both_parallel"

    def test_routing_decision_creation(self):
        """Test RoutingDecision dataclass creation."""
        decision = RoutingDecision(
            target=QueryTarget.USER_FIRST,
            confidence=0.85,
            reasoning="Query contains user-specific terms",
        )
        
        assert decision.target == QueryTarget.USER_FIRST
        assert decision.confidence == 0.85
        assert "user-specific" in decision.reasoning

    def test_routing_decision_to_dict(self):
        """Test RoutingDecision conversion to dictionary."""
        decision = RoutingDecision(
            target=QueryTarget.BOTH_PARALLEL,
            confidence=0.75,
            reasoning="General query",
        )
        
        result = decision.to_dict()
        
        assert result["target"] == "both_parallel"
        assert result["confidence"] == 0.75
        assert result["reasoning"] == "General query"

    @pytest.mark.asyncio
    async def test_route_user_specific_query(self, service):
        """Test routing for user-specific queries."""
        decision = await service.route_query(
            query="What's in my knowledge base about Kubernetes?",
            user_id="user-123",
            has_user_kb=True,
        )
        
        # User-specific query should route to user KB
        assert decision.target in [QueryTarget.USER_ONLY, QueryTarget.USER_FIRST]

    @pytest.mark.asyncio
    async def test_route_general_query_no_user_kb(self, service):
        """Test routing for general queries when user has no KB."""
        decision = await service.route_query(
            query="What are Kubernetes best practices?",
            user_id="user-123",
            has_user_kb=False,
        )
        
        # No user KB should route to global
        assert decision.target == QueryTarget.GLOBAL_ONLY

    @pytest.mark.asyncio
    async def test_route_explicit_global_query(self, service):
        """Test routing for explicitly global queries."""
        decision = await service.route_query(
            query="What are the industry standard practices for AWS security?",
            user_id="user-123",
            has_user_kb=True,
        )
        
        # Industry standards should include global KB
        assert decision.target in [QueryTarget.GLOBAL_ONLY, QueryTarget.GLOBAL_FIRST, QueryTarget.BOTH_PARALLEL]

    @pytest.mark.asyncio
    async def test_route_query_without_user_id(self, service):
        """Test routing when no user ID provided."""
        decision = await service.route_query(
            query="Kubernetes deployment patterns",
            user_id=None,
            has_user_kb=False,
        )
        
        # No user should default to global
        assert decision.target == QueryTarget.GLOBAL_ONLY

    @pytest.mark.asyncio
    async def test_route_my_documents_query(self, service):
        """Test routing for queries about user's documents."""
        decision = await service.route_query(
            query="Search my documents for terraform modules",
            user_id="user-123",
            has_user_kb=True,
        )
        
        # "my documents" should strongly indicate user KB
        assert decision.target in [QueryTarget.USER_ONLY, QueryTarget.USER_FIRST]

    @pytest.mark.asyncio
    async def test_route_research_query(self, service):
        """Test routing for research-focused queries."""
        decision = await service.route_query(
            query="Research the latest best practices for container security",
            user_id="user-123",
            has_user_kb=True,
        )
        
        # Research queries often benefit from both KBs
        assert decision.target in [QueryTarget.BOTH_PARALLEL, QueryTarget.GLOBAL_FIRST]

    def test_detect_user_specific_indicators(self, service):
        """Test detection of user-specific language indicators."""
        indicators = [
            "my knowledge base",
            "my documents",
            "my research",
            "I uploaded",
            "I added",
        ]
        
        for indicator in indicators:
            query = f"Find in {indicator} about AWS"
            has_indicator = service._has_user_specific_indicators(query)
            assert has_indicator, f"Should detect: {indicator}"

    def test_detect_global_indicators(self, service):
        """Test detection of global/standard indicators."""
        indicators = [
            "industry standard",
            "best practices",
            "official documentation",
            "general guidance",
        ]
        
        for indicator in indicators:
            query = f"What are the {indicator} for Kubernetes?"
            has_indicator = service._has_global_indicators(query)
            assert has_indicator, f"Should detect: {indicator}"

