"""High-performance regex matching engine with parallel processing and timeout handling."""

import asyncio
import logging
import re
from datetime import datetime
from typing import Any

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient

logger = logging.getLogger(__name__)


class RegexEngine:
    """High-performance regex matching engine."""

    def __init__(
        self,
        mongodb_client: MongoDBClient,
        timeout: float = 30.0,
        batch_size: int = 100,
        max_concurrent: int = 10,
    ) -> None:
        """Initialize regex engine.

        Args:
            mongodb_client: MongoDB client instance
            timeout: Maximum search time in seconds
            batch_size: Number of articles to process per batch
            max_concurrent: Maximum concurrent regex operations
        """
        self.mongodb_client = mongodb_client
        self.timeout = timeout
        self.batch_size = batch_size
        self.max_concurrent = max_concurrent
        self.files_searched = 0

    async def search(
        self,
        pattern: re.Pattern[str],
        mongo_filter: dict[str, Any],
        file_types: list[str] | None = None,
        code_type: str | None = None,
        cloud_provider: str | None = None,
        include_context: bool = True,
        context_lines: int = 3,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Search for regex pattern in knowledge articles.

        Args:
            pattern: Compiled regex pattern
            mongo_filter: MongoDB filter for articles
            file_types: Filter by file extensions
            code_type: Filter by code type
            cloud_provider: Filter by cloud provider
            include_context: Include surrounding code context
            context_lines: Number of context lines
            limit: Maximum results

        Returns:
            List of matches with file paths, line numbers, and context
        """
        if self.mongodb_client.database is None:
            raise RuntimeError("MongoDB database not connected")

        collection = self.mongodb_client.database.knowledge_articles

        cursor = collection.find(mongo_filter)

        matches: list[dict[str, Any]] = []
        start_time = datetime.utcnow()

        async def process_article(doc: dict[str, Any]) -> list[dict[str, Any]]:
            """Process a single article for regex matches."""
            article_matches: list[dict[str, Any]] = []

            article_id = doc.get("article_id", "")
            source_url = doc.get("source_url", "")
            content = doc.get("content", "")
            tags = doc.get("tags", [])

            if not content:
                return article_matches

            if file_types:
                if not any(ft in tags for ft in file_types):
                    return article_matches

            if code_type:
                content_lower = content.lower()
                tags_str = " ".join(tags).lower()
                if code_type.lower() not in tags and code_type.lower() not in content_lower:
                    return article_matches

            if cloud_provider:
                content_lower = content.lower()
                tags_str = " ".join(tags).lower()
                if cloud_provider.lower() not in content_lower and cloud_provider.lower() not in tags_str:
                    return article_matches

            lines = content.split("\n")

            for line_num, line in enumerate(lines, start=1):
                if (datetime.utcnow() - start_time).total_seconds() > self.timeout:
                    logger.warning("Regex search timeout reached")
                    break

                match = pattern.search(line)
                if match:
                    resource_id = doc.get("resource_id", "")
                    match_data: dict[str, Any] = {
                        "article_id": article_id,
                        "resource_id": resource_id,
                        "file_path": source_url,
                        "line_number": line_num,
                        "line_content": line,
                        "match_text": match.group(0),
                        "match_start": match.start(),
                        "match_end": match.end(),
                        "groups": match.groups() if match.groups() else [],
                    }

                    if include_context:
                        context_start = max(0, line_num - context_lines - 1)
                        context_end = min(len(lines), line_num + context_lines)
                        match_data["context"] = {
                            "before": lines[context_start:line_num - 1],
                            "after": lines[line_num:context_end],
                        }

                    article_matches.append(match_data)

                    if len(matches) + len(article_matches) >= limit:
                        break

            self.files_searched += 1
            return article_matches

        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def process_with_semaphore(doc: dict[str, Any]) -> list[dict[str, Any]]:
            async with semaphore:
                return await process_article(doc)

        tasks: list[asyncio.Task[list[dict[str, Any]]]] = []
        async for doc in cursor:
            if len(matches) >= limit:
                break

            if (datetime.utcnow() - start_time).total_seconds() > self.timeout:
                logger.warning("Regex search timeout reached")
                break

            task = asyncio.create_task(process_with_semaphore(doc))
            tasks.append(task)

            if len(tasks) >= self.batch_size:
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                for result in batch_results:
                    if isinstance(result, Exception):
                        logger.warning("Error processing article: %s", result)
                    else:
                        matches.extend(result)
                        if len(matches) >= limit:
                            break
                tasks = []

        if tasks:
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in batch_results:
                if isinstance(result, Exception):
                    logger.warning("Error processing article: %s", result)
                else:
                    matches.extend(result)

        return matches[:limit]

