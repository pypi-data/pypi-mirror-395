"""Research Orchestrator Service.

Orchestrates on-demand knowledge research using Anthropic's contextual retrieval approach.
This service coordinates:
1. Intent analysis (when no URL provided)
2. Source discovery (official docs, GitHub, web search)
3. Content fetching
4. Contextual chunking
5. Hybrid indexing (embeddings + BM25)
6. User-scoped storage

Reference: https://www.anthropic.com/news/contextual-retrieval
"""

import asyncio
import hashlib
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from api.database.mongodb import mongodb_manager
from data_pipelines.services.intent_analysis_service import (
    IntentAnalysisService,
    IntentAnalysisResult,
)
from data_pipelines.services.source_discovery_service import (
    SourceDiscoveryService,
    DiscoveryResult,
    DiscoveredSource,
)
from data_pipelines.processors.contextual_chunker import (
    ContextualChunker,
    ContextualChunk,
)
from data_pipelines.services.hybrid_indexer import (
    HybridIndexer,
    IndexedChunk,
)
from data_pipelines.loaders.mongodb_loader import MongoDBLoader
from wistx_mcp.tools.lib.web_fetcher import WebFetcher

logger = logging.getLogger(__name__)


@dataclass
class ResearchSession:
    """Represents a research session."""
    session_id: str
    user_id: str
    original_query: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    sources: list[dict[str, Any]] = field(default_factory=list)
    total_chunks: int = 0
    status: str = "pending"  # pending, in_progress, completed, failed
    error_message: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "original_query": self.original_query,
            "created_at": self.created_at,
            "sources": self.sources,
            "total_chunks": self.total_chunks,
            "status": self.status,
            "error_message": self.error_message,
            "metadata": self.metadata,
        }


@dataclass
class ResearchResult:
    """Result of a research operation."""
    session: ResearchSession
    chunks_indexed: int
    sources_processed: int
    intent_analysis: IntentAnalysisResult | None = None
    discovery_result: DiscoveryResult | None = None
    errors: list[str] = field(default_factory=list)


class ResearchOrchestrator:
    """Orchestrates on-demand knowledge research.
    
    Implements the full pipeline:
    1. Analyze user intent (if no URL provided)
    2. Discover relevant sources
    3. Fetch content from sources
    4. Chunk content with contextual enrichment
    5. Index chunks for hybrid retrieval
    6. Store in user-scoped collections
    """
    
    def __init__(
        self,
        intent_service: IntentAnalysisService | None = None,
        discovery_service: SourceDiscoveryService | None = None,
        chunker: ContextualChunker | None = None,
        indexer: HybridIndexer | None = None,
        mongodb_loader: MongoDBLoader | None = None,
    ):
        """Initialize research orchestrator.
        
        Args:
            intent_service: Intent analysis service
            discovery_service: Source discovery service
            chunker: Contextual chunker
            indexer: Hybrid indexer
            mongodb_loader: MongoDB loader for storage
        """
        self.intent_service = intent_service or IntentAnalysisService()
        self.discovery_service = discovery_service or SourceDiscoveryService()
        self.chunker = chunker or ContextualChunker()
        self.indexer = indexer or HybridIndexer()
        self.mongodb_loader = mongodb_loader or MongoDBLoader()
        self.web_fetcher = WebFetcher()
        self.db = mongodb_manager.get_database()
    
    async def research(
        self,
        query: str,
        user_id: str,
        url: str | None = None,
        max_sources: int = 5,
        generate_context: bool = True,
    ) -> ResearchResult:
        """Execute on-demand research.
        
        Args:
            query: Research query or intent description
            user_id: User ID for scoping
            url: Optional explicit URL to research
            max_sources: Maximum number of sources to process
            generate_context: Whether to generate LLM context for chunks
            
        Returns:
            ResearchResult with session info and statistics
        """
        # Create research session
        session_id = self._generate_session_id(user_id, query)
        session = ResearchSession(
            session_id=session_id,
            user_id=user_id,
            original_query=query,
            status="in_progress",
        )
        
        errors: list[str] = []
        intent_analysis: IntentAnalysisResult | None = None
        discovery_result: DiscoveryResult | None = None
        
        try:
            # Save initial session
            await self._save_session(session)
            
            # Step 1: Determine sources
            sources: list[DiscoveredSource] = []
            
            if url:
                # Explicit URL provided - use it directly
                logger.info("Research with explicit URL: %s", url)
                source = await self.discovery_service.discover_for_url(url)
                if source:
                    sources = [source]
            else:
                # No URL - analyze intent and discover sources
                logger.info("Research with intent analysis for: %s", query[:100])
                intent_analysis = await self.intent_service.analyze_intent(query)
                
                session.metadata["intent_analysis"] = {
                    "technologies": intent_analysis.technologies,
                    "task_type": intent_analysis.task_type,
                    "research_queries": intent_analysis.research_queries,
                }

                # Discover sources based on intent
                discovery_result = await self.discovery_service.discover_sources(
                    intent_analysis,
                    max_sources=max_sources,
                )
                sources = discovery_result.sources[:max_sources]

            if not sources:
                session.status = "completed"
                session.metadata["note"] = "No sources found for research query"
                await self._save_session(session)
                return ResearchResult(
                    session=session,
                    chunks_indexed=0,
                    sources_processed=0,
                    intent_analysis=intent_analysis,
                    discovery_result=discovery_result,
                    errors=["No sources found for research query"],
                )

            # Step 2: Fetch and process each source
            all_chunks: list[IndexedChunk] = []

            for source in sources:
                try:
                    # Fetch content
                    content = await self._fetch_source(source.url)
                    if not content:
                        errors.append(f"Failed to fetch: {source.url}")
                        continue

                    # Chunk with context
                    contextual_chunks = await self.chunker.chunk_document(
                        content=content,
                        source_url=source.url,
                        document_title=source.title or source.url,
                        generate_context=generate_context,
                    )

                    # Index chunks
                    indexed_chunks = await self.indexer.index_chunks(
                        chunks=contextual_chunks,
                        user_id=user_id,
                        research_session_id=session_id,
                    )

                    all_chunks.extend(indexed_chunks)

                    # Track source in session
                    session.sources.append({
                        "url": source.url,
                        "title": source.title,
                        "source_type": source.source_type,
                        "chunks_count": len(indexed_chunks),
                    })

                except Exception as e:
                    logger.error("Error processing source %s: %s", source.url, e)
                    errors.append(f"Error processing {source.url}: {str(e)}")

            # Step 3: Store indexed chunks
            if all_chunks:
                chunk_dicts = [chunk.to_dict() for chunk in all_chunks]
                self.mongodb_loader.load_user_knowledge_chunks(
                    chunks=chunk_dicts,
                    user_id=user_id,
                    research_session_id=session_id,
                )

            # Update session
            session.total_chunks = len(all_chunks)
            session.status = "completed"
            await self._save_session(session)

            logger.info(
                "Research completed: %d chunks from %d sources for user %s",
                len(all_chunks),
                len(session.sources),
                user_id,
            )

            return ResearchResult(
                session=session,
                chunks_indexed=len(all_chunks),
                sources_processed=len(session.sources),
                intent_analysis=intent_analysis,
                discovery_result=discovery_result,
                errors=errors,
            )

        except Exception as e:
            logger.error("Research failed: %s", e, exc_info=True)
            session.status = "failed"
            session.error_message = str(e)
            await self._save_session(session)

            return ResearchResult(
                session=session,
                chunks_indexed=0,
                sources_processed=0,
                intent_analysis=intent_analysis,
                discovery_result=discovery_result,
                errors=[str(e)],
            )

    async def _fetch_source(self, url: str) -> str | None:
        """Fetch content from a URL.

        Args:
            url: URL to fetch

        Returns:
            Content as string or None if failed
        """
        try:
            result = await self.web_fetcher.fetch_url(url)
            if result and result.get("content"):
                return result["content"]
            return None
        except Exception as e:
            logger.error("Failed to fetch %s: %s", url, e)
            return None

    async def _save_session(self, session: ResearchSession) -> None:
        """Save research session to MongoDB.

        Args:
            session: Research session to save
        """
        collection = self.db.user_research_sessions
        collection.update_one(
            {"session_id": session.session_id},
            {"$set": session.to_dict()},
            upsert=True,
        )

    def _generate_session_id(self, user_id: str, query: str) -> str:
        """Generate unique session ID.

        Args:
            user_id: User ID
            query: Research query

        Returns:
            Unique session ID
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        content = f"{user_id}:{query}:{timestamp}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    async def get_user_sessions(
        self,
        user_id: str,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Get user's research sessions.

        Args:
            user_id: User ID
            limit: Maximum sessions to return

        Returns:
            List of session documents
        """
        collection = self.db.user_research_sessions
        return list(
            collection.find({"user_id": user_id})
            .sort("created_at", -1)
            .limit(limit)
        )

    async def delete_session(
        self,
        user_id: str,
        session_id: str,
    ) -> bool:
        """Delete a research session and its chunks.

        Args:
            user_id: User ID
            session_id: Session ID to delete

        Returns:
            True if deleted successfully
        """
        # Delete chunks
        self.mongodb_loader.delete_user_knowledge_chunks(
            user_id=user_id,
            research_session_id=session_id,
        )

        # Delete session
        collection = self.db.user_research_sessions
        result = collection.delete_one({
            "session_id": session_id,
            "user_id": user_id,
        })

        return result.deleted_count > 0

