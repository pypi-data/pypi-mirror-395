"""Reranker Service.

Implements LLM-based reranking for improved retrieval precision.
This is the final stage in the retrieval pipeline, taking hybrid search
results and reordering them based on relevance to the query.

The reranker uses an LLM to score each result's relevance, providing
significant precision improvements over pure embedding-based retrieval.
"""

import asyncio
import logging
from dataclasses import dataclass
from typing import Any

from api.services.hybrid_retrieval_service import RetrievalResult
from wistx_mcp.tools.lib.gemini_client import GeminiClient
from wistx_mcp.tools.lib.retry_utils import with_timeout_and_retry

logger = logging.getLogger(__name__)


@dataclass
class RankedResult:
    """A reranked retrieval result."""
    result: RetrievalResult
    relevance_score: float
    relevance_explanation: str | None = None


class RerankerService:
    """LLM-based reranker for improved retrieval precision.
    
    Takes hybrid search results and reorders them based on
    semantic relevance to the query using an LLM.
    """
    
    def __init__(
        self,
        llm_client: GeminiClient | None = None,
        model: str = "gemini-2.0-flash",
        max_concurrent: int = 5,
    ):
        """Initialize reranker service.
        
        Args:
            llm_client: LLM client for scoring
            model: Model to use for reranking
            max_concurrent: Maximum concurrent LLM calls
        """
        self.llm_client = llm_client or GeminiClient()
        self.model = model
        self.max_concurrent = max_concurrent
    
    async def rerank(
        self,
        query: str,
        results: list[RetrievalResult],
        top_k: int | None = None,
        include_explanations: bool = False,
    ) -> list[RankedResult]:
        """Rerank results based on relevance to query.
        
        Args:
            query: Original search query
            results: Results from hybrid search
            top_k: Number of results to return (default: all)
            include_explanations: Include relevance explanations
            
        Returns:
            Reranked results sorted by relevance
        """
        if not results:
            return []
        
        # Score all results concurrently
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def score_result(result: RetrievalResult) -> RankedResult:
            async with semaphore:
                score, explanation = await self._score_relevance(
                    query, result, include_explanations
                )
                return RankedResult(
                    result=result,
                    relevance_score=score,
                    relevance_explanation=explanation if include_explanations else None,
                )
        
        tasks = [score_result(r) for r in results]
        ranked_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and sort by score
        valid_results = []
        for r in ranked_results:
            if isinstance(r, Exception):
                logger.warning("Reranking failed for result: %s", r)
            else:
                valid_results.append(r)
        
        # Sort by relevance score descending
        valid_results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        # Apply top_k if specified
        if top_k:
            valid_results = valid_results[:top_k]
        
        logger.info(
            "Reranked %d results, top score: %.2f",
            len(valid_results),
            valid_results[0].relevance_score if valid_results else 0,
        )
        
        return valid_results
    
    async def _score_relevance(
        self,
        query: str,
        result: RetrievalResult,
        include_explanation: bool = False,
    ) -> tuple[float, str | None]:
        """Score a single result's relevance to the query.
        
        Args:
            query: Search query
            result: Result to score
            include_explanation: Include explanation in response
            
        Returns:
            Tuple of (score, explanation)
        """
        # Truncate content for efficiency
        content = result.content[:2000] if result.content else ""
        context = result.context[:500] if result.context else ""
        
        prompt = f"""Rate the relevance of this document chunk to the query on a scale of 0-10.

Query: {query}

Document Title: {result.document_title}
Section: {result.section_title or "N/A"}
Context: {context}

Content:
{content}

Respond with ONLY a JSON object in this format:
{{"score": <0-10>, "explanation": "<brief explanation if requested>"}}

{"Include a brief explanation." if include_explanation else "Do not include explanation."}"""

        try:
            response = await with_timeout_and_retry(
                self._call_llm,
                timeout_seconds=10.0,
                max_attempts=2,
                retryable_exceptions=(Exception,),
                prompt=prompt,
            )
            
            if response:
                return self._parse_score_response(response, include_explanation)
            
            # Fallback to RRF score if LLM fails
            return result.rrf_score * 10, None
        except Exception as e:
            logger.warning("Relevance scoring failed: %s", e)
            return result.rrf_score * 10, None

    async def _call_llm(self, prompt: str) -> str | None:
        """Call the LLM with the given prompt."""
        messages = [{"role": "user", "content": prompt}]

        response = await self.llm_client.chat_completion(
            messages=messages,
            model=self.model,
            temperature=0.0,  # Deterministic for scoring
            max_tokens=100,
        )

        return response

    def _parse_score_response(
        self,
        response: str,
        include_explanation: bool,
    ) -> tuple[float, str | None]:
        """Parse LLM response to extract score and explanation.

        Args:
            response: LLM response string
            include_explanation: Whether explanation was requested

        Returns:
            Tuple of (score, explanation)
        """
        import json
        import re

        try:
            # Try to parse as JSON
            # Handle potential markdown code blocks
            json_match = re.search(r'\{[^}]+\}', response)
            if json_match:
                data = json.loads(json_match.group())
                score = float(data.get("score", 5))
                explanation = data.get("explanation") if include_explanation else None
                return min(max(score, 0), 10), explanation
        except (json.JSONDecodeError, ValueError, KeyError):
            pass

        # Fallback: try to extract number from response
        try:
            numbers = re.findall(r'\b(\d+(?:\.\d+)?)\b', response)
            if numbers:
                score = float(numbers[0])
                return min(max(score, 0), 10), None
        except ValueError:
            pass

        # Default score if parsing fails
        return 5.0, None

    async def rerank_with_fallback(
        self,
        query: str,
        results: list[RetrievalResult],
        top_k: int | None = None,
        timeout_seconds: float = 30.0,
    ) -> list[RankedResult]:
        """Rerank with timeout fallback to RRF scores.

        If reranking takes too long, falls back to using
        the original RRF scores from hybrid search.

        Args:
            query: Search query
            results: Results from hybrid search
            top_k: Number of results to return
            timeout_seconds: Timeout for reranking

        Returns:
            Reranked or fallback results
        """
        try:
            return await asyncio.wait_for(
                self.rerank(query, results, top_k),
                timeout=timeout_seconds,
            )
        except asyncio.TimeoutError:
            logger.warning(
                "Reranking timed out after %.1fs, using RRF scores",
                timeout_seconds,
            )
            # Fallback to RRF scores
            fallback_results = [
                RankedResult(
                    result=r,
                    relevance_score=r.rrf_score * 10,
                    relevance_explanation="Fallback to RRF score (reranking timed out)",
                )
                for r in results
            ]
            fallback_results.sort(key=lambda x: x.relevance_score, reverse=True)

            if top_k:
                fallback_results = fallback_results[:top_k]

            return fallback_results

