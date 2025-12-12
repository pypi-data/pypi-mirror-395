"""Hybrid Indexer for contextual retrieval.

Implements hybrid indexing combining:
1. Semantic embeddings (via Gemini)
2. BM25 keyword index

This enables Anthropic's contextual retrieval approach with hybrid search,
achieving up to 49% reduction in retrieval failures compared to standard RAG.

Reference: https://www.anthropic.com/news/contextual-retrieval
"""

import asyncio
import hashlib
import logging
import math
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from ..processors.contextual_chunker import ContextualChunk
from ..processors.embedding_generator import EmbeddingGenerator
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class IndexedChunk:
    """A chunk that has been indexed for hybrid retrieval."""
    chunk_id: str
    contextualized_content: str
    original_content: str
    context: str
    embedding: list[float] | None = None
    bm25_tokens: list[str] = field(default_factory=list)
    bm25_term_frequencies: dict[str, int] = field(default_factory=dict)
    source_url: str = ""
    document_title: str = ""
    section_title: str | None = None
    user_id: str | None = None
    research_session_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "chunk_id": self.chunk_id,
            "contextualized_content": self.contextualized_content,
            "original_content": self.original_content,
            "context": self.context,
            "embedding": self.embedding,
            "bm25_tokens": self.bm25_tokens,
            "bm25_term_frequencies": self.bm25_term_frequencies,
            "source_url": self.source_url,
            "document_title": self.document_title,
            "section_title": self.section_title,
            "user_id": self.user_id,
            "research_session_id": self.research_session_id,
            "metadata": self.metadata,
        }


class BM25Tokenizer:
    """Simple BM25 tokenizer for keyword indexing."""
    
    # Common English stop words
    STOP_WORDS = {
        "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
        "has", "he", "in", "is", "it", "its", "of", "on", "that", "the",
        "to", "was", "were", "will", "with", "the", "this", "but", "they",
        "have", "had", "what", "when", "where", "who", "which", "why", "how",
    }
    
    @classmethod
    def tokenize(cls, text: str) -> list[str]:
        """Tokenize text for BM25 indexing.
        
        Args:
            text: Text to tokenize
            
        Returns:
            List of tokens (lowercased, stop words removed)
        """
        # Lowercase and extract words
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9_-]+\b', text)
        
        # Remove stop words and short tokens
        tokens = [t for t in tokens if t not in cls.STOP_WORDS and len(t) > 2]
        
        return tokens
    
    @classmethod
    def get_term_frequencies(cls, tokens: list[str]) -> dict[str, int]:
        """Get term frequencies from tokens.
        
        Args:
            tokens: List of tokens
            
        Returns:
            Dictionary mapping terms to frequencies
        """
        return dict(Counter(tokens))


class HybridIndexer:
    """Hybrid indexer combining semantic embeddings and BM25.
    
    Indexes chunks for both:
    1. Semantic search (via embeddings)
    2. Keyword search (via BM25)
    
    This enables hybrid retrieval with Reciprocal Rank Fusion (RRF).
    """
    
    def __init__(self, embedding_generator: EmbeddingGenerator | None = None):
        """Initialize hybrid indexer.
        
        Args:
            embedding_generator: Optional embedding generator (creates one if not provided)
        """
        self.embedding_generator = embedding_generator or EmbeddingGenerator()
        self.tokenizer = BM25Tokenizer()
    
    async def index_chunks(
        self,
        chunks: list[ContextualChunk],
        user_id: str | None = None,
        research_session_id: str | None = None,
        generate_embeddings: bool = True,
    ) -> list[IndexedChunk]:
        """Index chunks for hybrid retrieval.
        
        Args:
            chunks: List of contextual chunks to index
            user_id: Optional user ID for user-scoped storage
            research_session_id: Optional research session ID
            generate_embeddings: Whether to generate embeddings
            
        Returns:
            List of indexed chunks ready for storage
        """
        if not chunks:
            return []
        
        logger.info("Indexing %d chunks for hybrid retrieval", len(chunks))
        
        # Step 1: Generate BM25 tokens for all chunks
        indexed_chunks = []
        for chunk in chunks:
            tokens = self.tokenizer.tokenize(chunk.contextualized_content)
            term_freqs = self.tokenizer.get_term_frequencies(tokens)
            
            indexed_chunks.append(IndexedChunk(
                chunk_id=chunk.chunk_id,
                contextualized_content=chunk.contextualized_content,
                original_content=chunk.original_content,
                context=chunk.context,
                bm25_tokens=tokens,
                bm25_term_frequencies=term_freqs,
                source_url=chunk.source_url,
                document_title=chunk.document_title,
                section_title=chunk.section_title,
                user_id=user_id,
                research_session_id=research_session_id,
                metadata=chunk.metadata,
            ))

        # Step 2: Generate embeddings for all chunks
        if generate_embeddings:
            indexed_chunks = await self._generate_embeddings(indexed_chunks)

        logger.info(
            "Indexed %d chunks: %d with embeddings, %d with BM25 tokens",
            len(indexed_chunks),
            sum(1 for c in indexed_chunks if c.embedding),
            sum(1 for c in indexed_chunks if c.bm25_tokens),
        )

        return indexed_chunks

    async def _generate_embeddings(
        self,
        chunks: list[IndexedChunk],
    ) -> list[IndexedChunk]:
        """Generate embeddings for indexed chunks.

        Args:
            chunks: List of indexed chunks

        Returns:
            Chunks with embeddings added
        """
        # Prepare items for embedding generator
        items = []
        for chunk in chunks:
            items.append({
                "chunk_id": chunk.chunk_id,
                "content": chunk.contextualized_content,
            })

        # Generate embeddings
        try:
            items_with_embeddings, failed = await self.embedding_generator.generate_embeddings(
                items, "knowledge"
            )

            # Map embeddings back to chunks
            embedding_map = {
                item["chunk_id"]: item.get("embedding")
                for item in items_with_embeddings
            }

            for chunk in chunks:
                chunk.embedding = embedding_map.get(chunk.chunk_id)

            if failed:
                logger.warning("Failed to generate embeddings for %d chunks", len(failed))

        except Exception as e:
            logger.error("Embedding generation failed: %s", e)

        return chunks

    def compute_bm25_scores(
        self,
        query: str,
        chunks: list[IndexedChunk],
        k1: float = 1.5,
        b: float = 0.75,
    ) -> list[tuple[IndexedChunk, float]]:
        """Compute BM25 scores for chunks against a query.

        Args:
            query: Search query
            chunks: List of indexed chunks
            k1: BM25 k1 parameter (term frequency saturation)
            b: BM25 b parameter (document length normalization)

        Returns:
            List of (chunk, score) tuples sorted by score descending
        """
        if not chunks:
            return []

        # Tokenize query
        query_tokens = self.tokenizer.tokenize(query)
        if not query_tokens:
            return [(chunk, 0.0) for chunk in chunks]

        # Calculate corpus statistics
        num_docs = len(chunks)
        avg_doc_len = sum(len(c.bm25_tokens) for c in chunks) / num_docs if num_docs > 0 else 0

        # Calculate document frequencies for query terms
        doc_freqs = {}
        for token in query_tokens:
            doc_freqs[token] = sum(
                1 for c in chunks if token in c.bm25_term_frequencies
            )

        # Calculate BM25 scores
        scores = []
        for chunk in chunks:
            score = 0.0
            doc_len = len(chunk.bm25_tokens)

            for token in query_tokens:
                if token not in chunk.bm25_term_frequencies:
                    continue

                tf = chunk.bm25_term_frequencies[token]
                df = doc_freqs.get(token, 0)

                # IDF component
                idf = math.log((num_docs - df + 0.5) / (df + 0.5) + 1)

                # TF component with saturation
                tf_component = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * doc_len / avg_doc_len))

                score += idf * tf_component

            scores.append((chunk, score))

        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)

        return scores

    def get_corpus_stats(self, chunks: list[IndexedChunk]) -> dict[str, Any]:
        """Get corpus statistics for BM25 calculations.

        Args:
            chunks: List of indexed chunks

        Returns:
            Dictionary with corpus statistics
        """
        if not chunks:
            return {
                "num_docs": 0,
                "avg_doc_len": 0,
                "total_tokens": 0,
                "unique_tokens": 0,
            }

        all_tokens = []
        for chunk in chunks:
            all_tokens.extend(chunk.bm25_tokens)

        return {
            "num_docs": len(chunks),
            "avg_doc_len": len(all_tokens) / len(chunks),
            "total_tokens": len(all_tokens),
            "unique_tokens": len(set(all_tokens)),
        }

