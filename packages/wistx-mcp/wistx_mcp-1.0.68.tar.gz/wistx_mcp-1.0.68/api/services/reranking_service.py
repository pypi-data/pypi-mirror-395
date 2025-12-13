"""Reranking service for improving retrieval precision.

Uses cross-encoder models to rerank search results.
"""

import logging
from typing import Any, Optional

try:
    from sentence_transformers import CrossEncoder
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False
    CrossEncoder = None

logger = logging.getLogger(__name__)


class RerankingService:
    """Reranking service using cross-encoder models."""

    def __init__(self):
        """Initialize reranking service."""
        if not HAS_SENTENCE_TRANSFORMERS:
            logger.warning(
                "sentence-transformers not installed. Install with: pip install sentence-transformers. "
                "Reranking will be disabled."
            )
            self.model = None
        else:
            try:
                self.model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
                logger.info("Loaded reranking model: cross-encoder/ms-marco-MiniLM-L-6-v2")
            except Exception as e:
                logger.error("Failed to load reranking model: %s", e, exc_info=True)
                self.model = None

    def rerank(
        self,
        query: str,
        articles: list[dict[str, Any]],
        top_k: Optional[int] = None,
    ) -> list[dict[str, Any]]:
        """Rerank articles based on query relevance.

        Args:
            query: Search query
            articles: List of article dictionaries with at least 'article_id', 'title', 'summary', 'content'
            top_k: Return top K results (None = return all)

        Returns:
            Reranked list of articles, sorted by relevance score descending
        """
        if not self.model or not HAS_SENTENCE_TRANSFORMERS:
            return articles

        if not articles:
            return []

        try:
            pairs = []
            for article in articles:
                contextual_desc = article.get("contextual_description", "")
                title = article.get("title", "")
                summary = article.get("summary", "")
                content = article.get("content", "")
                
                if not content and not summary:
                    description = article.get("description", "")
                    requirement = article.get("requirement", "")
                    content = f"{description} {requirement}".strip()
                
                article_text_parts = []
                if contextual_desc:
                    article_text_parts.append(contextual_desc)
                article_text_parts.append(title)
                if summary:
                    article_text_parts.append(summary)
                if content:
                    article_text_parts.append(content[:500])
                
                article_text = " ".join(article_text_parts)
                pairs.append([query, article_text])

            scores = self.model.predict(pairs)

            reranked = [
                {
                    **article,
                    "rerank_score": float(score),
                }
                for article, score in zip(articles, scores)
            ]

            reranked.sort(key=lambda x: x.get("rerank_score", 0), reverse=True)

            if top_k is not None:
                reranked = reranked[:top_k]

            return reranked
        except Exception as e:
            logger.error("Reranking failed: %s", e, exc_info=True)
            return articles

