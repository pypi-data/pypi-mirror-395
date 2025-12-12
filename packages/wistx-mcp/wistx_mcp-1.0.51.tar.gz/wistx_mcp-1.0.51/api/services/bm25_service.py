"""BM25 service for keyword-based retrieval.

Implements contextual BM25 indexing and search for hybrid retrieval.
"""

import logging
import re
from collections import Counter
from typing import Any, Optional

try:
    from rank_bm25 import BM25Okapi
    HAS_BM25 = True
except ImportError:
    HAS_BM25 = False
    BM25Okapi = None

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient

logger = logging.getLogger(__name__)


class BM25Service:
    """BM25 keyword search service with contextual enrichment."""

    def __init__(self, mongodb_client: MongoDBClient):
        """Initialize BM25 service.

        Args:
            mongodb_client: MongoDB client instance
        """
        if not HAS_BM25:
            logger.warning(
                "rank_bm25 not installed. Install with: pip install rank-bm25. "
                "BM25 search will be disabled."
            )
            self.bm25_index = None
            self.article_ids: list[str] = []
            self.tokenized_docs: list[list[str]] = []
        else:
            self.mongodb_client = mongodb_client
            self.bm25_index: Optional[BM25Okapi] = None
            self.article_ids: list[str] = []
            self.tokenized_docs: list[list[str]] = []
            self._index_loaded = False

    def _tokenize(self, text: str) -> list[str]:
        """Tokenize text for BM25 indexing.

        Args:
            text: Text to tokenize

        Returns:
            List of tokens (lowercased, alphanumeric only)
        """
        text_lower = text.lower()
        tokens = re.findall(r"\b[a-z0-9]+\b", text_lower)
        return tokens

    async def _load_index(self) -> None:
        """Load BM25 index from MongoDB.

        Loads all knowledge articles and builds BM25 index with contextual text.
        """
        if not HAS_BM25:
            return

        try:
            await self.mongodb_client.connect()
            if self.mongodb_client.database is None:
                logger.warning("MongoDB database not available, skipping BM25 index load")
                return

            collection = self.mongodb_client.database.knowledge_articles
            cursor = collection.find({})
            
            article_ids = []
            tokenized_docs = []
            
            async for doc in cursor:
                article_id = doc.get("article_id", "")
                if not article_id:
                    continue

                contextual_description = doc.get("contextual_description", "")
                title = doc.get("title", "")
                summary = doc.get("summary", "")
                content = doc.get("content", "")
                tags = doc.get("tags", [])
                categories = doc.get("categories", [])

                searchable_text = ""
                if contextual_description:
                    searchable_text += contextual_description + " "
                searchable_text += f"{title} {summary} {content} "
                searchable_text += " ".join(tags) + " "
                searchable_text += " ".join(categories)

                tokens = self._tokenize(searchable_text)
                if tokens:
                    article_ids.append(article_id)
                    tokenized_docs.append(tokens)

            if tokenized_docs:
                self.bm25_index = BM25Okapi(tokenized_docs)
                self.article_ids = article_ids
                self.tokenized_docs = tokenized_docs
                logger.info(
                    "Loaded BM25 index with %d articles",
                    len(article_ids),
                )
            else:
                logger.warning("No articles found for BM25 indexing")
        except Exception as e:
            logger.error("Failed to load BM25 index: %s", e, exc_info=True)
            self.bm25_index = None

    async def search(
        self,
        query: str,
        limit: int = 20,
    ) -> list[tuple[str, float]]:
        """Search using BM25.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of (article_id, score) tuples, sorted by score descending
        """
        if not HAS_BM25:
            return []

        if not self._index_loaded:
            await self._load_index()
            self._index_loaded = True

        if not self.bm25_index:
            return []

        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        scores = self.bm25_index.get_scores(query_tokens)
        
        results = [
            (self.article_ids[i], float(scores[i]))
            for i in range(len(self.article_ids))
            if scores[i] > 0
        ]
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:limit]

    def add_document(
        self,
        article_id: str,
        contextual_description: str,
        title: str,
        summary: str,
        content: str,
        tags: list[str],
        categories: list[str],
    ) -> None:
        """Add document to BM25 index.

        Args:
            article_id: Article ID
            contextual_description: Contextual description
            title: Article title
            summary: Article summary
            content: Article content
            tags: Article tags
            categories: Article categories
        """
        if not HAS_BM25:
            return

        searchable_text = ""
        if contextual_description:
            searchable_text += contextual_description + " "
        searchable_text += f"{title} {summary} {content} "
        searchable_text += " ".join(tags) + " "
        searchable_text += " ".join(categories)

        tokens = self._tokenize(searchable_text)
        if not tokens:
            return

        if self.bm25_index is None:
            self.bm25_index = BM25Okapi([tokens])
            self.article_ids = [article_id]
            self.tokenized_docs = [tokens]
        else:
            self.article_ids.append(article_id)
            self.tokenized_docs.append(tokens)
            self.bm25_index = BM25Okapi(self.tokenized_docs)

    def remove_document(self, article_id: str) -> None:
        """Remove document from BM25 index.

        Args:
            article_id: Article ID to remove
        """
        if not HAS_BM25 or not self.bm25_index:
            return

        try:
            index = self.article_ids.index(article_id)
            self.article_ids.pop(index)
            self.tokenized_docs.pop(index)
            if self.tokenized_docs:
                self.bm25_index = BM25Okapi(self.tokenized_docs)
            else:
                self.bm25_index = None
        except ValueError:
            pass

