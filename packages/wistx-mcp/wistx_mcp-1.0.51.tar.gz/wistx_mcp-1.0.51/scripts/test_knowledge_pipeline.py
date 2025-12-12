#!/usr/bin/env python3
"""Test script for knowledge base pipeline (compliance domain).

This script tests the complete E2E knowledge base pipeline:
1. Source Discovery
2. Collection
3. LLM Extraction
4. Processing
5. Quality Validation
6. Embedding
7. Loading (MongoDB + Pinecone)
"""

import asyncio
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from data_pipelines.processors.knowledge_pipeline_orchestrator import KnowledgePipelineOrchestrator
from data_pipelines.utils.logger import setup_logger

logger = setup_logger(__name__)


async def test_knowledge_pipeline(domain: str, subdomain: str | None = None, limit_urls: int | None = None):
    """Test knowledge base pipeline.
    
    Args:
        domain: Knowledge domain (e.g., "compliance")
        subdomain: Optional subdomain (e.g., "pci-dss")
        limit_urls: Limit number of URLs to process (for testing)
    """
    logger.info("=" * 80)
    logger.info("Knowledge Base Pipeline Test")
    logger.info("=" * 80)
    logger.info("Domain: %s", domain)
    if subdomain:
        logger.info("Subdomain: %s", subdomain)
    if limit_urls:
        logger.info("URL Limit: %d", limit_urls)
    logger.info("=" * 80)
    logger.info("")

    orchestrator = KnowledgePipelineOrchestrator()
    
    if limit_urls:
        original_collect = orchestrator._collect_from_urls
        
        async def limited_collect(web_urls, pdf_urls, domain, subdomain):
            limited_web = web_urls[:limit_urls] if len(web_urls) > limit_urls else web_urls
            limited_pdf = pdf_urls[:max(0, limit_urls - len(limited_web))] if len(pdf_urls) > 0 else []
            logger.info("Limiting URLs: %d web + %d PDF = %d total", len(limited_web), len(limited_pdf), len(limited_web) + len(limited_pdf))
            return await original_collect(limited_web, limited_pdf, domain, subdomain)
        
        orchestrator._collect_from_urls = limited_collect

    try:
        stats = await orchestrator.run_knowledge_pipeline(
            domain=domain,
            subdomain=subdomain,
            run_collection=True,
        )

        logger.info("")
        logger.info("=" * 80)
        logger.info("Pipeline Results")
        logger.info("=" * 80)
        logger.info("Collected: %d articles", stats.get("collected", 0))
        logger.info("Processed: %d articles", stats.get("processed", 0))
        logger.info("Validated: %d articles", stats.get("validated", 0))
        logger.info("Embedded: %d articles", stats.get("embedded", 0))
        logger.info("Loaded MongoDB: %d articles", stats.get("loaded_mongodb", 0))
        logger.info("Loaded Pinecone: %d articles", stats.get("loaded_pinecone", 0))
        logger.info("Quality Rejected: %d articles", stats.get("quality_rejected", 0))
        logger.info("Errors: %d", len(stats.get("errors", [])))

        if stats.get("errors"):
            logger.warning("")
            logger.warning("Errors encountered:")
            for error in stats["errors"][:10]:
                logger.warning("  - %s: %s", error.get("stage", "unknown"), error.get("error", "unknown"))

        metrics_summary = orchestrator.get_metrics_summary()
        logger.info("")
        logger.info("Total Duration: %.2fs", metrics_summary.get("total_duration_seconds", 0))

        logger.info("")
        logger.info("=" * 80)
        logger.info("✅ Pipeline Test Complete")
        logger.info("=" * 80)

        return stats

    except Exception as e:
        logger.error("Pipeline test failed: %s", e, exc_info=True)
        raise


async def verify_mongodb(domain: str, subdomain: str | None = None):
    """Verify articles in MongoDB.
    
    Args:
        domain: Knowledge domain
        subdomain: Optional subdomain
    """
    from api.database.mongodb import mongodb_manager

    logger.info("")
    logger.info("Verifying MongoDB...")

    mongodb_manager.connect()
    db = mongodb_manager.get_database()
    collection = db.knowledge_articles

    query = {"domain": domain}
    if subdomain:
        query["subdomain"] = subdomain

    count = collection.count_documents(query)
    logger.info("Found %d articles in MongoDB", count)

    sample = list(collection.find(query).limit(3))
    if sample:
        logger.info("")
        logger.info("Sample articles:")
        for article in sample:
            logger.info("  - %s: %s", article.get("article_id"), article.get("title", "Untitled")[:60])

    return count


async def verify_pinecone(domain: str):
    """Verify vectors in Pinecone.
    
    Args:
        domain: Knowledge domain
    """
    from data_pipelines.utils.config import PipelineSettings
    from pinecone import Pinecone

    logger.info("")
    logger.info("Verifying Pinecone...")

    settings = PipelineSettings()
    pc = Pinecone(api_key=settings.pinecone_api_key)
    index = pc.Index(settings.pinecone_index_name)

    try:
        stats = index.describe_index_stats()
        logger.info("Pinecone index stats: %s", stats)

        dummy_vector = [0.0] * 1536
        results = index.query(
            vector=dummy_vector,
            top_k=5,
            filter={"collection": "knowledge_articles", "domain": domain},
            include_metadata=True,
        )

        logger.info("Found %d knowledge article vectors", len(results.matches))
        if results.matches:
            logger.info("")
            logger.info("Sample vectors:")
            for match in results.matches[:3]:
                logger.info("  - %s: %s", match.id, match.metadata.get("title", "Untitled")[:60])

        return len(results.matches)

    except Exception as e:
        logger.warning("Could not verify Pinecone: %s", e)
        return 0


async def main():
    """Main test function."""
    parser = argparse.ArgumentParser(description="Test knowledge base pipeline")
    parser.add_argument(
        "--domain",
        type=str,
        default="compliance",
        help="Knowledge domain (default: compliance)",
    )
    parser.add_argument(
        "--subdomain",
        type=str,
        default=None,
        help="Subdomain (e.g., pci-dss, hipaa)",
    )
    parser.add_argument(
        "--limit-urls",
        type=int,
        default=None,
        help="Limit number of URLs to process (for testing)",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Only verify existing data, don't run pipeline",
    )

    args = parser.parse_args()

    if args.verify_only:
        logger.info("Verification mode - checking existing data")
        mongodb_count = await verify_mongodb(args.domain, args.subdomain)
        pinecone_count = await verify_pinecone(args.domain)
        logger.info("")
        logger.info("Verification complete:")
        logger.info("  MongoDB: %d articles", mongodb_count)
        logger.info("  Pinecone: %d vectors", pinecone_count)
    else:
        stats = await test_knowledge_pipeline(
            domain=args.domain,
            subdomain=args.subdomain,
            limit_urls=args.limit_urls,
        )

        logger.info("")
        logger.info("Running verification...")
        mongodb_count = await verify_mongodb(args.domain, args.subdomain)
        pinecone_count = await verify_pinecone(args.domain)

        logger.info("")
        logger.info("Final Summary:")
        logger.info("  Pipeline: %d articles processed", stats.get("processed", 0))
        logger.info("  MongoDB: %d articles stored", mongodb_count)
        logger.info("  Pinecone: %d vectors stored", pinecone_count)


if __name__ == "__main__":
    asyncio.run(main())

