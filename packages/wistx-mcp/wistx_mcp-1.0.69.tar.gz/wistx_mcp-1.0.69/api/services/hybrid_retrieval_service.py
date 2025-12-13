"""Hybrid Retrieval Service.

Implements hybrid search combining:
1. Semantic search (via Pinecone embeddings)
2. BM25 keyword search (via MongoDB)
3. Reciprocal Rank Fusion (RRF) for result merging

This achieves Anthropic's recommended approach for contextual retrieval,
with up to 49% reduction in retrieval failures compared to standard RAG.

Reference: https://www.anthropic.com/news/contextual-retrieval
"""

import logging
from dataclasses import dataclass, field
from typing import Any

from api.database.mongodb import mongodb_manager
from data_pipelines.loaders.pinecone_loader import PineconeLoader
from data_pipelines.services.hybrid_indexer import HybridIndexer, BM25Tokenizer
from data_pipelines.processors.embedding_generator import EmbeddingGenerator

logger = logging.getLogger(__name__)


@dataclass
class RetrievalResult:
    """A single retrieval result with scores."""
    chunk_id: str
    content: str
    context: str
    source_url: str
    document_title: str
    section_title: str | None = None
    semantic_score: float = 0.0
    bm25_score: float = 0.0
    rrf_score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class HybridSearchResult:
    """Result of a hybrid search operation."""
    results: list[RetrievalResult]
    total_semantic: int = 0
    total_bm25: int = 0
    query_time_ms: int = 0


class HybridRetrievalService:
    """Hybrid retrieval service combining semantic and BM25 search.
    
    Implements Reciprocal Rank Fusion (RRF) to merge results from
    semantic and keyword search for optimal retrieval quality.
    """
    
    # RRF constant (k=60 is standard)
    RRF_K = 60
    
    # Default weights for hybrid search
    DEFAULT_SEMANTIC_WEIGHT = 0.6
    DEFAULT_BM25_WEIGHT = 0.4
    
    def __init__(
        self,
        pinecone_loader: PineconeLoader | None = None,
        embedding_generator: EmbeddingGenerator | None = None,
    ):
        """Initialize hybrid retrieval service.
        
        Args:
            pinecone_loader: Pinecone loader for semantic search
            embedding_generator: Embedding generator for query embeddings
        """
        self.pinecone_loader = pinecone_loader or PineconeLoader()
        self.embedding_generator = embedding_generator or EmbeddingGenerator()
        self.tokenizer = BM25Tokenizer()
        self.db = mongodb_manager.get_database()
    
    async def search(
        self,
        query: str,
        user_id: str,
        top_k: int = 10,
        semantic_weight: float | None = None,
        bm25_weight: float | None = None,
        research_session_id: str | None = None,
    ) -> HybridSearchResult:
        """Perform hybrid search combining semantic and BM25.
        
        Args:
            query: Search query
            user_id: User ID for scoping
            top_k: Number of results to return
            semantic_weight: Weight for semantic results (default: 0.6)
            bm25_weight: Weight for BM25 results (default: 0.4)
            research_session_id: Optional filter by research session
            
        Returns:
            HybridSearchResult with merged results
        """
        import time
        start_time = time.time()
        
        semantic_weight = semantic_weight or self.DEFAULT_SEMANTIC_WEIGHT
        bm25_weight = bm25_weight or self.DEFAULT_BM25_WEIGHT
        
        # Normalize weights
        total_weight = semantic_weight + bm25_weight
        semantic_weight = semantic_weight / total_weight
        bm25_weight = bm25_weight / total_weight
        
        # Fetch more results for merging
        fetch_k = top_k * 3
        
        # Run semantic and BM25 search in parallel
        import asyncio
        semantic_task = self._semantic_search(
            query, user_id, fetch_k, research_session_id
        )
        bm25_task = self._bm25_search(
            query, user_id, fetch_k, research_session_id
        )
        
        semantic_results, bm25_results = await asyncio.gather(
            semantic_task, bm25_task
        )
        
        # Apply RRF fusion
        merged_results = self._rrf_fusion(
            semantic_results,
            bm25_results,
            semantic_weight,
            bm25_weight,
        )
        
        # Take top_k results
        final_results = merged_results[:top_k]
        
        query_time_ms = int((time.time() - start_time) * 1000)
        
        logger.info(
            "Hybrid search completed: %d semantic, %d BM25, %d merged in %dms",
            len(semantic_results),
            len(bm25_results),
            len(final_results),
            query_time_ms,
        )
        
        return HybridSearchResult(
            results=final_results,
            total_semantic=len(semantic_results),
            total_bm25=len(bm25_results),
            query_time_ms=query_time_ms,
        )
    
    async def _semantic_search(
        self,
        query: str,
        user_id: str,
        top_k: int,
        research_session_id: str | None = None,
    ) -> list[RetrievalResult]:
        """Perform semantic search via Pinecone."""
        try:
            # Generate query embedding
            query_item = {"chunk_id": "query", "content": query}
            items_with_embeddings, _ = await self.embedding_generator.generate_embeddings(
                [query_item], "knowledge"
            )

            if not items_with_embeddings or not items_with_embeddings[0].get("embedding"):
                logger.warning("Failed to generate query embedding")
                return []

            query_embedding = items_with_embeddings[0]["embedding"]

            # Build filter
            filter_dict = None
            if research_session_id:
                filter_dict = {"research_session_id": research_session_id}

            # Query Pinecone
            matches = self.pinecone_loader.query_user_knowledge(
                user_id=user_id,
                query_embedding=query_embedding,
                top_k=top_k,
                filter_dict=filter_dict,
            )

            # Convert to RetrievalResult
            results = []
            for match in matches:
                metadata = match.get("metadata", {})
                results.append(RetrievalResult(
                    chunk_id=match.get("chunk_id", ""),
                    content=metadata.get("content_preview", ""),
                    context="",  # Will be fetched from MongoDB if needed
                    source_url=metadata.get("source_url", ""),
                    document_title=metadata.get("document_title", ""),
                    section_title=metadata.get("section_title"),
                    semantic_score=match.get("score", 0.0),
                    metadata=metadata,
                ))

            return results
        except Exception as e:
            logger.error("Semantic search failed: %s", e)
            return []

    async def _bm25_search(
        self,
        query: str,
        user_id: str,
        top_k: int,
        research_session_id: str | None = None,
    ) -> list[RetrievalResult]:
        """Perform BM25 keyword search via MongoDB."""
        try:
            collection = self.db.user_knowledge_chunks

            # Build query
            mongo_query: dict[str, Any] = {"user_id": user_id}
            if research_session_id:
                mongo_query["research_session_id"] = research_session_id

            # Get all user chunks for BM25 scoring
            chunks = list(collection.find(mongo_query).limit(1000))

            if not chunks:
                return []

            # Tokenize query
            query_tokens = self.tokenizer.tokenize(query)
            if not query_tokens:
                return []

            # Calculate BM25 scores
            indexer = HybridIndexer()
            from data_pipelines.services.hybrid_indexer import IndexedChunk

            indexed_chunks = []
            for chunk in chunks:
                indexed_chunks.append(IndexedChunk(
                    chunk_id=chunk.get("chunk_id", ""),
                    contextualized_content=chunk.get("contextualized_content", ""),
                    original_content=chunk.get("original_content", ""),
                    context=chunk.get("context", ""),
                    bm25_tokens=chunk.get("bm25_tokens", []),
                    bm25_term_frequencies=chunk.get("bm25_term_frequencies", {}),
                    source_url=chunk.get("source_url", ""),
                    document_title=chunk.get("document_title", ""),
                    section_title=chunk.get("section_title"),
                ))

            scored_chunks = indexer.compute_bm25_scores(query, indexed_chunks)

            # Convert to RetrievalResult
            results = []
            for chunk, score in scored_chunks[:top_k]:
                if score > 0:
                    results.append(RetrievalResult(
                        chunk_id=chunk.chunk_id,
                        content=chunk.original_content,
                        context=chunk.context,
                        source_url=chunk.source_url,
                        document_title=chunk.document_title,
                        section_title=chunk.section_title,
                        bm25_score=score,
                    ))

            return results
        except Exception as e:
            logger.error("BM25 search failed: %s", e)
            return []

    def _rrf_fusion(
        self,
        semantic_results: list[RetrievalResult],
        bm25_results: list[RetrievalResult],
        semantic_weight: float,
        bm25_weight: float,
    ) -> list[RetrievalResult]:
        """Apply Reciprocal Rank Fusion to merge results.

        RRF score = sum(weight / (k + rank)) for each result list

        Args:
            semantic_results: Results from semantic search
            bm25_results: Results from BM25 search
            semantic_weight: Weight for semantic results
            bm25_weight: Weight for BM25 results

        Returns:
            Merged and sorted results
        """
        # Build chunk_id -> result mapping
        results_map: dict[str, RetrievalResult] = {}

        # Add semantic results with RRF scores
        for rank, result in enumerate(semantic_results, start=1):
            rrf_score = semantic_weight / (self.RRF_K + rank)

            if result.chunk_id in results_map:
                results_map[result.chunk_id].rrf_score += rrf_score
                results_map[result.chunk_id].semantic_score = result.semantic_score
            else:
                result.rrf_score = rrf_score
                results_map[result.chunk_id] = result

        # Add BM25 results with RRF scores
        for rank, result in enumerate(bm25_results, start=1):
            rrf_score = bm25_weight / (self.RRF_K + rank)

            if result.chunk_id in results_map:
                results_map[result.chunk_id].rrf_score += rrf_score
                results_map[result.chunk_id].bm25_score = result.bm25_score
                # Prefer content from BM25 (has full content)
                if result.content:
                    results_map[result.chunk_id].content = result.content
                if result.context:
                    results_map[result.chunk_id].context = result.context
            else:
                result.rrf_score = rrf_score
                results_map[result.chunk_id] = result

        # Sort by RRF score descending
        merged = sorted(
            results_map.values(),
            key=lambda x: x.rrf_score,
            reverse=True,
        )

        return merged

