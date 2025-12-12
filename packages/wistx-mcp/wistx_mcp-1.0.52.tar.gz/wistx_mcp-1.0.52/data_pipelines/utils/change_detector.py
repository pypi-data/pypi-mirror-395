"""Change detection utilities for efficient pipeline processing."""

import hashlib
import json
from decimal import Decimal
from typing import Any

from pymongo.errors import (
    ServerSelectionTimeoutError,
    NetworkTimeout,
    ConnectionFailure,
    AutoReconnect,
    NotPrimaryError,
    ExecutionTimeout,
)

from ..utils.logger import setup_logger

logger = setup_logger(__name__)


def _json_serializer(obj: Any) -> Any:
    """Custom JSON serializer for non-serializable types.

    Handles Decimal, datetime, and other types that json.dumps can't serialize.

    Args:
        obj: Object to serialize

    Returns:
        JSON-serializable representation
    """
    if isinstance(obj, Decimal):
        return float(obj)
    if hasattr(obj, "isoformat"):
        return obj.isoformat()
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    return str(obj)


def calculate_source_hash(raw_data: dict[str, Any]) -> str:
    """Calculate SHA-256 hash of raw source data.

    Args:
        raw_data: Raw compliance control or cost data dictionary

    Returns:
        Hexadecimal hash string

    Raises:
        ValueError: If hash calculation fails
    """
    try:
        normalized = json.dumps(raw_data, sort_keys=True, ensure_ascii=False, default=_json_serializer)
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    except (TypeError, ValueError, AttributeError) as e:
        logger.error("Failed to calculate source hash: %s", e)
        raise ValueError(f"Hash calculation failed: {e}") from e


def calculate_content_hash(processed_data: dict[str, Any]) -> str:
    """Calculate SHA-256 hash of processed content.

    Excludes fields that don't affect content (timestamps, hashes, embeddings).

    Args:
        processed_data: Processed compliance control or cost data dictionary

    Returns:
        Hexadecimal hash string

    Raises:
        ValueError: If hash calculation fails
    """
    try:
        content_data = {k: v for k, v in processed_data.items() 
                       if k not in ["_id", "created_at", "updated_at", 
                                   "source_hash", "content_hash", "embedding"]}
        normalized = json.dumps(content_data, sort_keys=True, ensure_ascii=False, default=_json_serializer)
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    except (TypeError, ValueError, AttributeError) as e:
        logger.error("Failed to calculate content hash: %s", e)
        raise ValueError(f"Hash calculation failed: {e}") from e


def extract_control_id(raw_data: dict[str, Any]) -> str | None:
    """Extract control_id from raw data.

    Args:
        raw_data: Raw compliance control dictionary

    Returns:
        Control ID string or None if not found
    """
    return (
        raw_data.get("control_id")
        or raw_data.get("benchmark_id")
        or raw_data.get("article_id")
        or raw_data.get("requirement_id")
    )


class ChangeDetector:
    """Detects changes in compliance controls to avoid unnecessary processing."""

    def __init__(self, collection: Any, enabled: bool = True):
        """Initialize change detector.

        Args:
            collection: MongoDB collection instance
            enabled: Whether change detection is enabled (default: True)
        """
        self.collection = collection
        self.enabled = enabled

    def batch_check_source_hashes(
        self, raw_controls: list[dict[str, Any]]
    ) -> dict[str, dict[str, Any]]:
        """Batch check source hashes for multiple controls.

        Args:
            raw_controls: List of raw compliance control dictionaries

        Returns:
            Dictionary mapping control_id to existing document (with hashes)
        """
        if not self.enabled:
            return {}

        control_ids = []
        for raw_control in raw_controls:
            control_id = extract_control_id(raw_control)
            if control_id:
                control_ids.append(control_id)

        if not control_ids:
            return {}

        try:
            existing_controls = self.collection.find(
                {"control_id": {"$in": control_ids}},
                {"control_id": 1, "source_hash": 1, "content_hash": 1}
            )
            return {doc["control_id"]: doc for doc in existing_controls}
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            RuntimeError,
            ServerSelectionTimeoutError,
            NetworkTimeout,
            ConnectionFailure,
            AutoReconnect,
            NotPrimaryError,
            ExecutionTimeout,
        ) as e:
            logger.warning("Failed to batch check source hashes: %s - processing all", e)
            return {}

    def should_process_source(
        self, raw_data: dict[str, Any], control_id: str | None = None
    ) -> tuple[bool, str | None]:
        """Check if source data changed and should be processed.

        Args:
            raw_data: Raw compliance control dictionary
            control_id: Control ID (extracted if not provided)

        Returns:
            Tuple of (should_process, source_hash)
            - should_process: True if source changed or unknown
            - source_hash: Calculated source hash
        """
        if not self.enabled:
            try:
                source_hash = calculate_source_hash(raw_data)
                return True, source_hash
            except ValueError:
                return True, None

        if control_id is None:
            control_id = extract_control_id(raw_data)

        if not control_id:
            try:
                source_hash = calculate_source_hash(raw_data)
                return True, source_hash
            except ValueError:
                return True, None

        try:
            source_hash = calculate_source_hash(raw_data)
        except ValueError:
            logger.warning("Failed to calculate source hash for control %s - processing anyway", control_id)
            return True, None

        try:
            existing = self.collection.find_one(
                {"control_id": control_id},
                {"source_hash": 1, "content_hash": 1}
            )
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            RuntimeError,
            ServerSelectionTimeoutError,
            NetworkTimeout,
            ConnectionFailure,
            AutoReconnect,
            NotPrimaryError,
            ExecutionTimeout,
        ) as e:
            logger.warning("Failed to check existing hash for control %s: %s - processing anyway", control_id, e)
            return True, source_hash

        if not existing:
            return True, source_hash

        existing_source_hash = existing.get("source_hash")
        if existing_source_hash is None:
            logger.debug("Control %s missing source_hash - processing to populate", control_id)
            return True, source_hash

        if existing_source_hash != source_hash:
            logger.debug("Source changed for control %s - reprocessing", control_id)
            return True, source_hash

        logger.debug("Source unchanged for control %s - skipping processing", control_id)
        return False, source_hash

    def should_generate_embedding(
        self, processed_data: dict[str, Any], control_id: str, existing_doc: dict[str, Any] | None = None
    ) -> tuple[bool, str | None]:
        """Check if processed content changed and embedding should be generated.

        Args:
            processed_data: Processed compliance control dictionary
            control_id: Control ID
            existing_doc: Existing MongoDB document (fetched if not provided)

        Returns:
            Tuple of (should_generate, content_hash)
            - should_generate: True if content changed or unknown
            - content_hash: Calculated content hash
        """
        if not self.enabled:
            try:
                content_hash = calculate_content_hash(processed_data)
                return True, content_hash
            except ValueError:
                return True, None

        try:
            content_hash = calculate_content_hash(processed_data)
        except ValueError:
            logger.warning("Failed to calculate content hash for control %s - generating embedding anyway", control_id)
            return True, None

        if existing_doc is None:
            try:
                existing_doc = self.collection.find_one(
                    {"control_id": control_id},
                    {"content_hash": 1}
                )
            except (
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                RuntimeError,
                ServerSelectionTimeoutError,
                NetworkTimeout,
                ConnectionFailure,
                AutoReconnect,
                NotPrimaryError,
                ExecutionTimeout,
            ) as e:
                logger.warning("Failed to check existing content hash for control %s: %s - generating embedding anyway", control_id, e)
                return True, content_hash

        if not existing_doc:
            return True, content_hash

        existing_content_hash = existing_doc.get("content_hash")
        if existing_content_hash is None:
            logger.debug("Control %s missing content_hash - generating embedding", control_id)
            return True, content_hash

        if existing_content_hash != content_hash:
            logger.debug("Content changed for control %s - regenerating embedding", control_id)
            return True, content_hash

        logger.debug("Content unchanged for control %s - skipping embedding generation", control_id)
        return False, content_hash

    def batch_check_article_source_hashes(
        self, raw_articles: list[dict[str, Any]]
    ) -> dict[str, dict[str, Any]]:
        """Batch check source hashes for multiple articles.
        
        Args:
            raw_articles: List of raw article dictionaries
            
        Returns:
            Dictionary mapping article_id to existing document (with hashes)
        """
        if not self.enabled:
            return {}
        
        article_ids = []
        for raw_article in raw_articles:
            article_id = raw_article.get("article_id")
            if article_id:
                article_ids.append(article_id)
        
        if not article_ids:
            return {}
        
        try:
            existing_articles = self.collection.find(
                {"article_id": {"$in": article_ids}},
                {"article_id": 1, "source_hash": 1, "content_hash": 1}
            )
            return {doc["article_id"]: doc for doc in existing_articles}
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            RuntimeError,
            ServerSelectionTimeoutError,
            NetworkTimeout,
            ConnectionFailure,
            AutoReconnect,
            NotPrimaryError,
            ExecutionTimeout,
        ) as e:
            logger.warning("Failed to batch check article source hashes: %s - processing all", e)
            return {}
    
    def should_process_article_source(
        self, raw_data: dict[str, Any], article_id: str | None = None
    ) -> tuple[bool, str | None]:
        """Check if article source data changed and should be processed.
        
        Args:
            raw_data: Raw article dictionary
            article_id: Article ID (extracted if not provided)
            
        Returns:
            Tuple of (should_process, source_hash)
            - should_process: True if source changed or unknown
            - source_hash: Calculated source hash
        """
        if not self.enabled:
            try:
                source_hash = calculate_source_hash(raw_data)
                return True, source_hash
            except ValueError:
                return True, None
        
        if article_id is None:
            article_id = raw_data.get("article_id")
        
        if not article_id:
            try:
                source_hash = calculate_source_hash(raw_data)
                return True, source_hash
            except ValueError:
                return True, None
        
        try:
            source_hash = calculate_source_hash(raw_data)
        except ValueError:
            logger.warning("Failed to calculate source hash for article %s - processing anyway", article_id)
            return True, None
        
        try:
            existing = self.collection.find_one(
                {"article_id": article_id},
                {"source_hash": 1, "content_hash": 1}
            )
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            RuntimeError,
            ServerSelectionTimeoutError,
            NetworkTimeout,
            ConnectionFailure,
            AutoReconnect,
            NotPrimaryError,
            ExecutionTimeout,
        ) as e:
            logger.warning("Failed to check existing hash for article %s: %s - processing anyway", article_id, e)
            return True, source_hash
        
        if not existing:
            return True, source_hash
        
        existing_source_hash = existing.get("source_hash")
        if existing_source_hash is None:
            logger.debug("Article %s missing source_hash - processing to populate", article_id)
            return True, source_hash
        
        if existing_source_hash != source_hash:
            logger.debug("Source changed for article %s - reprocessing", article_id)
            return True, source_hash
        
        logger.debug("Source unchanged for article %s - skipping processing", article_id)
        return False, source_hash
    
    def should_generate_article_embedding(
        self, processed_data: dict[str, Any], article_id: str, existing_doc: dict[str, Any] | None = None
    ) -> tuple[bool, str | None]:
        """Check if article processed content changed and embedding should be generated.
        
        Args:
            processed_data: Processed article dictionary
            article_id: Article ID
            existing_doc: Existing MongoDB document (fetched if not provided)
            
        Returns:
            Tuple of (should_generate, content_hash)
            - should_generate: True if content changed or unknown
            - content_hash: Calculated content hash
        """
        if not self.enabled:
            try:
                content_hash = calculate_content_hash(processed_data)
                return True, content_hash
            except ValueError:
                return True, None
        
        try:
            content_hash = calculate_content_hash(processed_data)
        except ValueError:
            logger.warning("Failed to calculate content hash for article %s - generating embedding anyway", article_id)
            return True, None
        
        if existing_doc is None:
            try:
                existing_doc = self.collection.find_one(
                    {"article_id": article_id},
                    {"content_hash": 1}
                )
            except (
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                RuntimeError,
                ServerSelectionTimeoutError,
                NetworkTimeout,
                ConnectionFailure,
                AutoReconnect,
                NotPrimaryError,
                ExecutionTimeout,
            ) as e:
                logger.warning("Failed to check existing content hash for article %s: %s - generating embedding anyway", article_id, e)
                return True, content_hash
        
        if not existing_doc:
            return True, content_hash
        
        existing_content_hash = existing_doc.get("content_hash")
        if existing_content_hash is None:
            logger.debug("Article %s missing content_hash - generating embedding", article_id)
            return True, content_hash
        
        if existing_content_hash != content_hash:
            logger.debug("Content changed for article %s - regenerating embedding", article_id)
            return True, content_hash
        
        logger.debug("Content unchanged for article %s - skipping embedding generation", article_id)
        return False, content_hash

