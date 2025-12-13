"""Dead letter queue for failed URLs.

Tracks URLs that failed to fetch for later retry or manual review.
"""

import logging
from datetime import datetime, timedelta
from typing import Any
from urllib.parse import urlparse

from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class DeadLetterQueue:
    """Dead letter queue for failed URL fetches.
    
    Stores failed URLs in MongoDB for later retry or manual review.
    """

    def __init__(self, collection_name: str = "failed_urls"):
        """Initialize dead letter queue.
        
        Args:
            collection_name: MongoDB collection name for failed URLs
        """
        self.collection_name = collection_name
        self._db = None
        self._collection = None
        self._initialized = False

    def _get_collection(self):
        """Get MongoDB collection (lazy initialization).
        
        Returns:
            MongoDB collection for failed URLs
        """
        if not self._initialized:
            from api.database.mongodb import mongodb_manager
            
            mongodb_manager.connect()
            self._db = mongodb_manager.get_database()
            self._collection = self._db[self.collection_name]
            
            self._collection.create_index(
                [("url", 1)],
                unique=True,
                background=True
            )
            self._collection.create_index(
                [("domain", 1), ("status", 1)],
                background=True
            )
            self._collection.create_index(
                [("retry_after", 1)],
                background=True
            )
            self._collection.create_index(
                [("failed_at", -1)],
                background=True
            )
            
            self._initialized = True
        
        return self._collection

    def _get_domain(self, url: str) -> str:
        """Extract domain from URL.
        
        Args:
            url: Full URL
            
        Returns:
            Domain name (e.g., "example.com")
        """
        try:
            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path.split("/")[0]
            if domain.startswith("www."):
                domain = domain[4:]
            return domain.lower()
        except Exception as e:
            logger.warning("Failed to parse domain from URL %s: %s", url, e)
            return "unknown"

    async def record_failure(
        self,
        url: str,
        error: str,
        error_type: str,
        attempts: int,
        retry_after_hours: int = 6,
    ) -> None:
        """Record a failed URL fetch.
        
        Args:
            url: URL that failed
            error: Error message
            error_type: Type of error (TimeoutError, ConnectionError, etc.)
            attempts: Number of attempts made
            retry_after_hours: Hours to wait before retry (default: 6)
        """
        try:
            collection = self._get_collection()
            domain = self._get_domain(url)
            
            failed_at = datetime.utcnow()
            retry_after = failed_at + timedelta(hours=retry_after_hours)
            
            document = {
                "url": url,
                "domain": domain,
                "error": error,
                "error_type": error_type,
                "attempts": attempts,
                "failed_at": failed_at,
                "retry_after": retry_after,
                "status": "pending_retry",
                "last_updated": failed_at,
            }
            
            collection.update_one(
                {"url": url},
                {
                    "$set": document,
                    "$inc": {"failure_count": 1},
                    "$setOnInsert": {"first_failed_at": failed_at},
                },
                upsert=True,
            )
            
            logger.debug(
                "Recorded failed URL in dead letter queue: %s (domain: %s, error: %s)",
                url,
                domain,
                error_type
            )
        except Exception as e:
            logger.warning(
                "Failed to record failed URL %s in dead letter queue: %s",
                url,
                e
            )

    async def get_retryable_urls(
        self,
        domain: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Get URLs that are ready for retry.
        
        Args:
            domain: Optional domain filter
            limit: Maximum number of URLs to return
            
        Returns:
            List of URLs ready for retry
        """
        try:
            collection = self._get_collection()
            query: dict[str, Any] = {
                "status": "pending_retry",
                "retry_after": {"$lte": datetime.utcnow()},
            }
            
            if domain:
                query["domain"] = domain
            
            urls = list(
                collection.find(query)
                .sort("retry_after", 1)
                .limit(limit)
            )
            
            for url_doc in urls:
                url_doc.pop("_id", None)
            
            return urls
        except Exception as e:
            logger.warning(
                "Failed to get retryable URLs from dead letter queue: %s",
                e
            )
            return []

    async def mark_retried(self, url: str, success: bool) -> None:
        """Mark a URL as retried.
        
        Args:
            url: URL that was retried
            success: Whether the retry was successful
        """
        try:
            collection = self._get_collection()
            
            if success:
                collection.update_one(
                    {"url": url},
                    {
                        "$set": {
                            "status": "resolved",
                            "resolved_at": datetime.utcnow(),
                            "last_updated": datetime.utcnow(),
                        }
                    }
                )
                logger.debug("Marked URL as resolved: %s", url)
            else:
                collection.update_one(
                    {"url": url},
                    {
                        "$set": {
                            "status": "pending_retry",
                            "last_updated": datetime.utcnow(),
                        }
                    }
                )
                logger.debug("Marked URL for retry: %s", url)
        except Exception as e:
            logger.warning(
                "Failed to mark URL %s as retried: %s",
                url,
                e
            )

    async def get_stats(self) -> dict[str, Any]:
        """Get statistics about failed URLs.
        
        Returns:
            Dictionary with statistics
        """
        try:
            collection = self._get_collection()
            
            total = collection.count_documents({})
            pending = collection.count_documents({"status": "pending_retry"})
            resolved = collection.count_documents({"status": "resolved"})
            
            domain_stats = list(
                collection.aggregate([
                    {"$group": {
                        "_id": "$domain",
                        "count": {"$sum": 1},
                        "pending": {
                            "$sum": {"$cond": [{"$eq": ["$status", "pending_retry"]}, 1, 0]}
                        }
                    }},
                    {"$sort": {"count": -1}},
                    {"$limit": 10}
                ])
            )
            
            return {
                "total_failed_urls": total,
                "pending_retry": pending,
                "resolved": resolved,
                "top_failing_domains": [
                    {"domain": stat["_id"], "count": stat["count"], "pending": stat["pending"]}
                    for stat in domain_stats
                ],
            }
        except Exception as e:
            logger.warning("Failed to get dead letter queue stats: %s", e)
            return {
                "total_failed_urls": 0,
                "pending_retry": 0,
                "resolved": 0,
                "top_failing_domains": [],
            }

