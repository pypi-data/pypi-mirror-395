"""Migration script for contextual retrieval.

Generates contextual descriptions for existing knowledge articles and re-embeds them.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any

from bson import ObjectId

from api.database.mongodb_manager import mongodb_manager
from api.services.context_generator import context_generator
from data_pipelines.models.knowledge_article import KnowledgeArticle
from data_pipelines.processors.embedding_generator import EmbeddingGenerator
from wistx_mcp.tools.lib.pinecone_loader import PineconeLoader

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def migrate_articles(
    batch_size: int = 100,
    limit: int | None = None,
    dry_run: bool = False,
) -> None:
    """Migrate existing articles to use contextual retrieval.

    Args:
        batch_size: Number of articles to process per batch
        limit: Maximum number of articles to migrate (None = all)
        dry_run: If True, only log what would be done without making changes
    """
    db = mongodb_manager.get_database()
    collection = db.knowledge_articles

    query = {"contextual_description": {"$exists": False}}
    total_count = collection.count_documents(query)

    if limit:
        total_count = min(total_count, limit)

    logger.info("Found %d articles without contextual descriptions", total_count)

    if dry_run:
        logger.info("DRY RUN MODE - No changes will be made")

    processed = 0
    updated = 0
    failed = 0

    embedding_generator = EmbeddingGenerator()
    pinecone_loader = PineconeLoader()

    cursor = collection.find(query).limit(limit) if limit else collection.find(query)

    batch = []
    for doc in cursor:
        try:
            article = KnowledgeArticle.model_validate(doc)
            
            if article.contextual_description:
                logger.debug("Article %s already has context, skipping", article.article_id)
                continue

            repo_context = None
            if article.resource_id:
                resource = db.indexed_resources.find_one({"_id": ObjectId(article.resource_id)})
                if resource:
                    repo_context = {
                        "repo_url": resource.get("repo_url", ""),
                        "branch": resource.get("branch", "main"),
                        "commit_sha": article.commit_sha,
                        "resource_id": article.resource_id,
                        "user_id": article.user_id,
                    }

            contextual_description = await context_generator.generate_context(
                article=article,
                repo_context=repo_context,
            )

            article.contextual_description = contextual_description
            article.context_generated_at = datetime.utcnow()
            article.context_version = "1.0"

            searchable_text = article.to_searchable_text()
            embeddings = await embedding_generator.generate_embeddings_batch([searchable_text])
            
            if embeddings and len(embeddings) > 0:
                article.embedding = embeddings[0]

            batch.append(article)
            processed += 1

            if len(batch) >= batch_size:
                if not dry_run:
                    await _update_batch(collection, batch, pinecone_loader)
                updated += len(batch)
                logger.info(
                    "Processed %d/%d articles (updated: %d, failed: %d)",
                    processed,
                    total_count,
                    updated,
                    failed,
                )
                batch = []

        except Exception as e:
            logger.error("Failed to migrate article %s: %s", doc.get("article_id", "unknown"), e, exc_info=True)
            failed += 1
            processed += 1

    if batch:
        if not dry_run:
            await _update_batch(collection, batch, pinecone_loader)
        updated += len(batch)

    logger.info(
        "Migration complete: processed=%d, updated=%d, failed=%d",
        processed,
        updated,
        failed,
    )


async def _update_batch(
    collection: Any,
    articles: list[KnowledgeArticle],
    pinecone_loader: PineconeLoader,
) -> None:
    """Update a batch of articles in MongoDB and Pinecone.

    Args:
        collection: MongoDB collection
        articles: List of articles to update
        pinecone_loader: Pinecone loader instance
    """
    mongo_updates = []
    pinecone_vectors = []

    for article in articles:
        article_dict = article.model_dump_for_mongodb()
        mongo_updates.append({
            "filter": {"article_id": article.article_id},
            "update": {
                "$set": {
                    "contextual_description": article.contextual_description,
                    "context_generated_at": article.context_generated_at,
                    "context_version": article.context_version,
                    "embedding": article.embedding,
                }
            }
        })

        if article.embedding:
            pinecone_data = article.model_dump_for_pinecone()
            pinecone_vectors.append(pinecone_data)

    for update_op in mongo_updates:
        collection.update_one(update_op["filter"], update_op["update"])

    if pinecone_vectors:
        pinecone_loader.load_knowledge_articles(
            [article.model_dump() for article in articles],
            batch_size=len(pinecone_vectors),
        )


if __name__ == "__main__":
    import sys

    dry_run = "--dry-run" in sys.argv
    limit = None
    if "--limit" in sys.argv:
        idx = sys.argv.index("--limit")
        if idx + 1 < len(sys.argv):
            limit = int(sys.argv[idx + 1])

    asyncio.run(migrate_articles(limit=limit, dry_run=dry_run))

