"""Migration 0007: Hybrid Retrieval Indexes.

Creates indexes for:
- User-scoped knowledge articles
- Research sessions
- Retrieval evaluation feedback
- BM25 search support
"""

import logging

from pymongo.database import Database

from .base_migration import BaseMigration

logger = logging.getLogger(__name__)


class Migration0007HybridRetrievalIndexes(BaseMigration):
    """Create indexes for hybrid retrieval system."""

    @property
    def version(self) -> int:
        """Migration version."""
        return 7

    @property
    def description(self) -> str:
        """Migration description."""
        return "Create indexes for hybrid retrieval, research sessions, and evaluation"

    async def up(self, db: Database) -> None:
        """Apply migration."""
        logger.info("Running migration 0007: Hybrid retrieval indexes...")

        # =================================================================
        # User-scoped knowledge articles indexes
        # =================================================================
        knowledge_collection = db.knowledge_articles
        
        logger.info("Creating indexes for knowledge_articles (user-scoped)...")
        
        try:
            knowledge_collection.create_index(
                [("user_id", 1), ("research_session_id", 1)],
                name="user_session_lookup",
                background=True,
            )
            logger.info("Created user_session_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            knowledge_collection.create_index(
                [("user_id", 1), ("source_url", 1)],
                name="user_source_lookup",
                background=True,
            )
            logger.info("Created user_source_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            knowledge_collection.create_index(
                [("user_id", 1), ("created_at", -1)],
                name="user_created_desc",
                background=True,
            )
            logger.info("Created user_created_desc index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            knowledge_collection.create_index(
                [("user_id", 1), ("domain", 1), ("content_type", 1)],
                name="user_domain_type_lookup",
                background=True,
            )
            logger.info("Created user_domain_type_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        # =================================================================
        # Research sessions indexes
        # =================================================================
        sessions_collection = db.research_sessions
        
        logger.info("Creating indexes for research_sessions...")
        
        try:
            sessions_collection.create_index(
                [("session_id", 1)],
                unique=True,
                name="session_id_unique",
                background=True,
            )
            logger.info("Created session_id_unique index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            sessions_collection.create_index(
                [("user_id", 1), ("status", 1), ("created_at", -1)],
                name="user_status_created",
                background=True,
            )
            logger.info("Created user_status_created index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            sessions_collection.create_index(
                [("user_id", 1), ("technologies", 1)],
                name="user_technologies",
                background=True,
            )
            logger.info("Created user_technologies index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        # =================================================================
        # Retrieval evaluation indexes
        # =================================================================
        feedback_collection = db.retrieval_feedback
        
        logger.info("Creating indexes for retrieval_feedback...")
        
        try:
            feedback_collection.create_index(
                [("user_id", 1), ("created_at", -1)],
                name="user_feedback_created",
                background=True,
            )
            logger.info("Created user_feedback_created index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            feedback_collection.create_index(
                [("query_id", 1), ("result_id", 1)],
                unique=True,
                name="query_result_unique",
                background=True,
            )
            logger.info("Created query_result_unique index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            feedback_collection.create_index(
                [("relevance_score", 1)],
                name="relevance_score_lookup",
                background=True,
            )
            logger.info("Created relevance_score_lookup index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        # =================================================================
        # BM25 chunks collection for hybrid search
        # =================================================================
        bm25_collection = db.bm25_chunks

        logger.info("Creating indexes for bm25_chunks...")

        try:
            bm25_collection.create_index(
                [("chunk_id", 1)],
                unique=True,
                name="chunk_id_unique",
                background=True,
            )
            logger.info("Created chunk_id_unique index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            bm25_collection.create_index(
                [("user_id", 1), ("research_session_id", 1)],
                name="user_session_bm25",
                background=True,
            )
            logger.info("Created user_session_bm25 index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            # Text index for BM25 keyword search fallback
            bm25_collection.create_index(
                [("tokens", "text")],
                name="bm25_text_search",
                background=True,
            )
            logger.info("Created bm25_text_search index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        # =================================================================
        # Evaluation metrics aggregation index
        # =================================================================
        metrics_collection = db.retrieval_metrics

        logger.info("Creating indexes for retrieval_metrics...")

        try:
            metrics_collection.create_index(
                [("user_id", 1), ("period", 1)],
                unique=True,
                name="user_period_unique",
                background=True,
            )
            logger.info("Created user_period_unique index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        try:
            metrics_collection.create_index(
                [("computed_at", -1)],
                name="metrics_computed_desc",
                background=True,
            )
            logger.info("Created metrics_computed_desc index")
        except Exception as e:
            logger.warning("Index creation failed (may already exist): %s", e)

        logger.info("✅ Migration 0007 complete")

