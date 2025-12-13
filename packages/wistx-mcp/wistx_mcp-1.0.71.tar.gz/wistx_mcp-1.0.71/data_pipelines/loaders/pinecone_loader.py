"""Pinecone loader for vector data."""

import logging
import re
from typing import Any, TYPE_CHECKING

from pinecone import Pinecone
from pinecone.exceptions import NotFoundException
from tqdm import tqdm

from data_pipelines.utils.config import PipelineSettings
from data_pipelines.utils.circuit_breaker import CircuitBreaker, CircuitBreakerOpenError

if TYPE_CHECKING:
    from pinecone import Index

logger = logging.getLogger(__name__)
settings = PipelineSettings()


class PineconeLoader:
    """Load vector data into Pinecone."""

    def __init__(self):
        """Initialize Pinecone loader."""
        self._pc: Pinecone | None = None
        self._index: "Index | None" = None
        self._index_name = settings.pinecone_index_name
        self._api_key = settings.pinecone_api_key
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=5,
            recovery_timeout=60.0,
            success_threshold=2,
        )

    @property
    def index(self) -> "Index":
        """Lazy initialization of Pinecone index with automatic retry.
        
        The index is only created when first accessed. If the index doesn't exist,
        it will be created automatically by the startup event in api/main.py.
        This property will retry initialization if the index becomes available later.
        
        Returns:
            Pinecone Index instance
            
        Raises:
            ValueError: If Pinecone API key is not configured
            NotFoundException: If the index doesn't exist (will be created on startup)
        """
        if self._index is None:
            if not self._api_key:
                logger.warning(
                    "Pinecone API key not configured. Pinecone features will be disabled."
                )
                raise ValueError("Pinecone API key not configured")
            
            if self._pc is None:
                self._pc = Pinecone(api_key=self._api_key)
            
            try:
                self._index = self._pc.Index(self._index_name)
                try:
                    self._index.describe_index_stats()
                except NotFoundException:
                    self._index = None
                    raise
            except NotFoundException:
                logger.debug(
                    "Pinecone index '%s' does not exist yet. "
                    "The index will be created automatically during application startup.",
                    self._index_name,
                )
                raise
            except Exception as e:
                error_msg = str(e)
                if "NOT_FOUND" in error_msg or "not found" in error_msg.lower():
                    logger.debug(
                        "Pinecone index '%s' does not exist yet. "
                        "The index will be created automatically during application startup.",
                        self._index_name,
                    )
                    raise NotFoundException(
                        f"Index '{self._index_name}' does not exist. "
                        "It will be created automatically on startup."
                    ) from e
                else:
                    logger.error(
                        "Failed to initialize Pinecone index '%s': %s. "
                        "Pinecone features will be disabled.",
                        self._index_name,
                        e,
                    )
                    raise
        
        return self._index
    
    def reset_index(self) -> None:
        """Reset the cached index instance to force re-initialization.
        
        Useful after the index is created during startup.
        """
        self._index = None
    
    def is_available(self) -> bool:
        """Check if Pinecone index is available.
        
        Returns:
            True if Pinecone is configured and index exists, False otherwise
        """
        if not self._api_key:
            return False
        try:
            _ = self.index
            return True
        except Exception:
            return False

    def _safe_str(self, value: Any) -> str:
        """Safely convert value to string, handling None.

        Args:
            value: Value to convert (can be None)

        Returns:
            String representation, or empty string if None
        """
        if value is None:
            return ""
        return str(value)

    def upsert_single_control(self, control: dict[str, Any]) -> bool:
        """Upsert a single compliance control to Pinecone immediately.

        Args:
            control: Control document with embedding

        Returns:
            True if upserted successfully
        """
        control_id = control.get("control_id")
        if not control_id:
            logger.warning("Cannot upsert control without control_id")
            return False

        if not control.get("embedding"):
            logger.warning("Skipping control %s - no embedding", control_id)
            return False

        pinecone_id = self._sanitize_id(f"compliance_{control_id}")
        if not pinecone_id:
            logger.error("Failed to generate valid Pinecone ID for control_id: %s", control_id)
            return False

        metadata = self._clean_metadata({
            "collection": "compliance_controls",
            "control_id": str(control_id),
            "standard": str(control.get("standard", "")),
            "version": str(control.get("version", "")),
            "severity": str(control.get("severity", "")),
            "title": str(control.get("title", ""))[:500],
            "description": str(control.get("description", ""))[:1000],
            "category": self._safe_str(control.get("category")),
            "subcategory": self._safe_str(control.get("subcategory")),
        })

        vector = {
            "id": pinecone_id,
            "values": control["embedding"],
            "metadata": metadata,
        }

        try:
            self.circuit_breaker.call(
                self.index.upsert,
                vectors=[vector]
            )
            return True
        except CircuitBreakerOpenError:
            logger.error("Pinecone circuit breaker is OPEN - skipping upsert")
            return False
        except (ValueError, TypeError, KeyError, AttributeError) as e:
            logger.error("Failed to upsert control %s to Pinecone: %s", control_id, e)
            return False

    def load_compliance_controls(
        self, controls: list[dict[str, Any]], batch_size: int = 100
    ) -> None:
        """Load compliance controls into Pinecone.

        Args:
            controls: List of compliance control documents
            batch_size: Batch size for upsert operations
        """
        logger.info("Loading %d compliance controls into Pinecone...", len(controls))

        vectors = []
        skipped = []
        for control in controls:
            control_id = control.get("control_id")
            if not control_id:
                logger.warning("Skipping control without control_id: %s", control.get("title", "unknown"))
                skipped.append("no_control_id")
                continue

            if not control.get("embedding"):
                logger.warning("Skipping control %s - no embedding", control_id)
                skipped.append(control_id)
                continue

            pinecone_id = self._sanitize_id(f"compliance_{control_id}")
            if not pinecone_id:
                logger.error("Failed to generate valid Pinecone ID for control_id: %s", control_id)
                skipped.append(control_id)
                continue

            metadata = self._clean_metadata({
                "collection": "compliance_controls",
                "control_id": str(control_id),
                "standard": str(control.get("standard", "")),
                "version": str(control.get("version", "")),
                "severity": str(control.get("severity", "")),
                "title": str(control.get("title", ""))[:500],
                "description": str(control.get("description", ""))[:1000],
                "category": self._safe_str(control.get("category")),
                "subcategory": self._safe_str(control.get("subcategory")),
            })

            vector = {
                "id": pinecone_id,
                "values": control["embedding"],
                "metadata": metadata,
            }
            vectors.append(vector)

        if skipped:
            logger.warning("Skipped %d controls: %s", len(skipped), ", ".join(skipped[:5]))

        if not vectors:
            logger.warning("No vectors to load to Pinecone")
            return

        logger.info("Prepared %d vectors for Pinecone upsert", len(vectors))

        failed_count = 0
        for i in tqdm(range(0, len(vectors), batch_size), desc="Loading compliance controls"):
            batch = vectors[i : i + batch_size]
            try:
                self.index.upsert(vectors=batch)
            except (ValueError, TypeError, KeyError, AttributeError) as e:
                logger.error("Failed to upsert batch %d-%d: %s", i, min(i + batch_size, len(vectors)), e)
                failed_count += len(batch)
                continue
            except Exception as e:
                logger.error("Unexpected error upserting batch %d-%d: %s", i, min(i + batch_size, len(vectors)), e, exc_info=True)
                failed_count += len(batch)
                continue

        if failed_count > 0:
            logger.error("Failed to load %d controls to Pinecone", failed_count)
        else:
            logger.info("Successfully loaded %d compliance controls into Pinecone", len(vectors))

    def _sanitize_id(self, raw_id: str) -> str:
        """Sanitize ID for Pinecone compatibility.

        Pinecone IDs must:
        - Be alphanumeric, hyphens, underscores
        - Not contain spaces or special characters
        - Be under 100 characters

        Args:
            raw_id: Raw ID string

        Returns:
            Sanitized ID string
        """
        if not raw_id:
            return ""

        sanitized = str(raw_id).strip()

        sanitized = re.sub(r"[^a-zA-Z0-9_-]", "_", sanitized)

        sanitized = re.sub(r"_+", "_", sanitized)

        sanitized = sanitized.strip("_")

        if len(sanitized) > 100:
            sanitized = sanitized[:100]

        if not sanitized:
            sanitized = "unknown"

        return sanitized

    def _clean_metadata(self, metadata: dict[str, Any]) -> dict[str, Any]:
        """Clean metadata to ensure Pinecone compatibility.

        Removes None/null values and ensures all values are valid types:
        - string, number, boolean, or list of strings

        Args:
            metadata: Raw metadata dictionary

        Returns:
            Cleaned metadata dictionary
        """
        cleaned = {}
        for key, value in metadata.items():
            if value is None:
                continue
            
            if isinstance(value, (str, int, float, bool)):
                if isinstance(value, str) and not value.strip():
                    continue
                cleaned[key] = value
            elif isinstance(value, list):
                cleaned_list = [str(v) for v in value if v is not None]
                if cleaned_list:
                    cleaned[key] = cleaned_list
            else:
                cleaned[key] = str(value)
        
        return cleaned

    def load_pricing_data(
        self, pricing_items: list[dict[str, Any]], batch_size: int = 100
    ) -> None:
        """Load pricing data into Pinecone.

        Args:
            pricing_items: List of pricing data documents
            batch_size: Batch size for upsert operations
        """
        logger.info("Loading %d pricing items into Pinecone...", len(pricing_items))

        vectors = []
        for item in pricing_items:
            if not item.get("embedding"):
                logger.warning("Skipping pricing item %s - no embedding", item.get("lookup_key"))
                continue

            metadata = self._clean_metadata({
                "collection": "pricing_data",
                "lookup_key": str(item["lookup_key"]),
                "cloud": str(item.get("cloud", "")),
                "service": str(item.get("service", "")),
                "resource_type": str(item.get("resource_type", "")),
                "region": str(item.get("region", "")),
            })

            vector = {
                "id": f"pricing_{item['lookup_key']}",
                "values": item["embedding"],
                "metadata": metadata,
            }
            vectors.append(vector)

        if not vectors:
            logger.warning("No vectors to load to Pinecone")
            return

        for i in tqdm(range(0, len(vectors), batch_size), desc="Loading pricing data"):
            batch = vectors[i : i + batch_size]
            self.index.upsert(vectors=batch)

        logger.info("Loaded %d pricing items into Pinecone", len(vectors))

    def load_code_examples(
        self, examples: list[dict[str, Any]], batch_size: int = 100
    ) -> None:
        """Load code examples into Pinecone.

        Args:
            examples: List of code example documents
            batch_size: Batch size for upsert operations
        """
        logger.info("Loading %d code examples into Pinecone...", len(examples))

        vectors = []
        for example in examples:
            if not example.get("embedding"):
                logger.warning("Skipping example %s - no embedding", example.get("example_id"))
                continue

            services_list = example.get("services", [])
            if isinstance(services_list, str):
                services_list = [services_list]

            metadata = self._clean_metadata({
                "collection": "code_examples",
                "example_id": str(example["example_id"]),
                "infrastructure_type": str(example.get("code_type", "")),
                "cloud_provider": str(example.get("cloud_provider", "")),
                "title": str(example.get("title", ""))[:500],
                "description": str(example.get("description", ""))[:1000],
                "services": services_list,
                "quality_score": int(example.get("quality_score", 0)),
            })

            vector = {
                "id": f"code_{example['example_id']}",
                "values": example["embedding"],
                "metadata": metadata,
            }
            vectors.append(vector)

        if not vectors:
            logger.warning("No vectors to load to Pinecone")
            return

        for i in tqdm(range(0, len(vectors), batch_size), desc="Loading code examples"):
            batch = vectors[i : i + batch_size]
            self.index.upsert(vectors=batch)

        logger.info("Loaded %d code examples into Pinecone", len(vectors))

    def load_knowledge_articles(
        self, articles: list[dict[str, Any]], batch_size: int = 100
    ) -> None:
        """Load knowledge articles into Pinecone.
        
        Args:
            articles: List of knowledge article documents
            batch_size: Batch size for upsert operations
        """
        logger.info("Loading %d knowledge articles into Pinecone...", len(articles))

        vectors = []
        for article in articles:
            if not article.get("embedding"):
                logger.warning("Skipping article %s - no embedding", article.get("article_id"))
                continue

            article_id = article.get("article_id", "")
            domain = article.get("domain", "")
            if hasattr(domain, "value"):
                domain = domain.value
            domain = str(domain) if domain else ""
            
            subdomain = article.get("subdomain", "")
            content_type = article.get("content_type", "")
            if hasattr(content_type, "value"):
                content_type = content_type.value
            content_type = str(content_type) if content_type else ""

            metadata = self._clean_metadata({
                "collection": "knowledge_articles",
                "article_id": str(article_id),
                "domain": self._safe_str(domain),
                "subdomain": self._safe_str(subdomain),
                "content_type": self._safe_str(content_type),
                "title": str(article.get("title", ""))[:200],
                "summary": str(article.get("summary", ""))[:1000],
                "tags": ",".join(article.get("tags", [])[:10]),
                "industries": ",".join(article.get("industries", [])[:5]),
                "cloud_providers": ",".join(article.get("cloud_providers", [])[:5]),
            })

            pinecone_id = self._sanitize_id(f"knowledge_{article_id}")
            if not pinecone_id:
                logger.error("Failed to generate valid Pinecone ID for article_id: %s", article_id)
                continue

            vector = {
                "id": pinecone_id,
                "values": article["embedding"],
                "metadata": metadata,
            }
            vectors.append(vector)

        if not vectors:
            logger.warning("No vectors to load to Pinecone")
            return

        for i in tqdm(range(0, len(vectors), batch_size), desc="Loading knowledge articles"):
            batch = vectors[i : i + batch_size]
            try:
                self.circuit_breaker.call(
                    self.index.upsert,
                    vectors=batch
                )
            except CircuitBreakerOpenError:
                logger.error("Pinecone circuit breaker is OPEN - skipping batch")
                break
            except (ValueError, TypeError, KeyError, AttributeError) as e:
                logger.error("Failed to upsert knowledge articles batch: %s", e)
                continue

        logger.info("Loaded %d knowledge articles into Pinecone", len(vectors))

    def load_cost_data_focus(
        self, cost_records: list[dict[str, Any]], batch_size: int = 100
    ) -> None:
        """Load FOCUS-compliant cost data into Pinecone.

        Args:
            cost_records: List of FOCUSCostData documents
            batch_size: Batch size for upsert operations
        """
        logger.info("Loading %d FOCUS cost records into Pinecone...", len(cost_records))

        vectors = []
        skipped = []
        for record in cost_records:
            if not record.get("embedding"):
                logger.warning("Skipping cost record %s - no embedding", record.get("lookup_key"))
                skipped.append(record.get("lookup_key", "unknown"))
                continue

            lookup_key = record.get("lookup_key")
            if not lookup_key:
                logger.warning("Skipping cost record without lookup_key")
                skipped.append("no_lookup_key")
                continue

            metadata = self._clean_metadata({
                "collection": "cost_data_focus",
                "provider": str(record.get("provider", "")),
                "service_category": str(record.get("service_category", "")),
                "service_name": str(record.get("service_name", "")),
                "region_id": str(record.get("region_id", "")),
                "pricing_category": str(record.get("pricing_category", "")),
                "resource_type": str(record.get("resource_type", "")),
                "list_unit_price": float(record.get("list_unit_price", 0)),
                "billing_currency": str(record.get("billing_currency", "USD")),
                "lookup_key": str(lookup_key),
                "last_updated": str(record.get("last_updated", "")),
            })

            if record.get("service_subcategory"):
                metadata["service_subcategory"] = str(record.get("service_subcategory"))

            if record.get("tags"):
                tags_dict = record.get("tags")
                if isinstance(tags_dict, dict):
                    tags_list = [f"{k}:{v}" for k, v in tags_dict.items() if v]
                    if tags_list:
                        metadata["tags"] = tags_list
                elif isinstance(tags_dict, list):
                    metadata["tags"] = [str(t) for t in tags_dict if t]
                else:
                    metadata["tags"] = [str(tags_dict)]

            pinecone_id = self._sanitize_id(f"cost_{record.get('provider')}_{lookup_key}")
            if not pinecone_id:
                logger.error("Failed to generate valid Pinecone ID for lookup_key: %s", lookup_key)
                skipped.append(lookup_key)
                continue

            vector = {
                "id": pinecone_id,
                "values": record["embedding"],
                "metadata": metadata,
            }
            vectors.append(vector)

        if skipped:
            logger.warning("Skipped %d cost records: %s", len(skipped), ", ".join(skipped[:5]))

        if not vectors:
            logger.warning("No vectors to load to Pinecone")
            return

        logger.info("Prepared %d vectors for Pinecone upsert", len(vectors))

        failed_count = 0
        for i in tqdm(range(0, len(vectors), batch_size), desc="Loading FOCUS cost data"):
            batch = vectors[i : i + batch_size]
            try:
                self.circuit_breaker.call(
                    self.index.upsert,
                    vectors=batch
                )
            except CircuitBreakerOpenError:
                logger.error("Pinecone circuit breaker is OPEN - skipping batch")
                break
            except (ValueError, TypeError, KeyError, AttributeError) as e:
                logger.error("Failed to upsert batch %d-%d: %s", i, min(i + batch_size, len(vectors)), e)
                failed_count += len(batch)
                continue
            except Exception as e:
                logger.error("Unexpected error upserting batch %d-%d: %s", i, min(i + batch_size, len(vectors)), e, exc_info=True)
                failed_count += len(batch)
                continue

        if failed_count > 0:
            logger.error("Failed to load %d cost records to Pinecone", failed_count)
            if failed_count == len(vectors):
                raise RuntimeError(
                    f"Failed to load all {len(vectors)} cost records to Pinecone. "
                    "Check logs for specific error details."
                )
            else:
                logger.warning(
                    "Partially loaded: %d succeeded, %d failed out of %d total",
                    len(vectors) - failed_count,
                    failed_count,
                    len(vectors),
                )
        else:
            logger.info("Successfully loaded %d FOCUS cost records into Pinecone", len(vectors))

    def delete_single_control(self, control_id: str) -> bool:
        """Delete a single compliance control from Pinecone.

        Args:
            control_id: Control ID to delete

        Returns:
            True if deleted successfully, False otherwise
        """
        if not control_id:
            logger.warning("Cannot delete control without control_id")
            return False

        pinecone_id = self._sanitize_id(f"compliance_{control_id}")
        if not pinecone_id:
            logger.error("Failed to generate valid Pinecone ID for control_id: %s", control_id)
            return False

        try:
            self.circuit_breaker.call(
                self.index.delete,
                ids=[pinecone_id]
            )
            return True
        except CircuitBreakerOpenError:
            logger.error("Pinecone circuit breaker is OPEN - skipping delete")
            return False
        except Exception as e:
            logger.error("Failed to delete control %s from Pinecone: %s", control_id, e)
            return False

    def load_user_knowledge_chunks(
        self,
        chunks: list[dict[str, Any]],
        user_id: str,
        batch_size: int = 100,
    ) -> int:
        """Load user-scoped knowledge chunks into Pinecone.

        Uses user-specific namespace for isolation.

        Args:
            chunks: List of chunk documents with embeddings
            user_id: User ID for namespace isolation
            batch_size: Batch size for upserts

        Returns:
            Number of vectors loaded
        """
        if not chunks:
            return 0

        # Use user-specific namespace
        namespace = f"user_{user_id}"

        vectors = []
        for chunk in chunks:
            embedding = chunk.get("embedding")
            if not embedding:
                continue

            chunk_id = chunk.get("chunk_id")
            if not chunk_id:
                continue

            pinecone_id = self._sanitize_id(f"chunk_{chunk_id}")
            if not pinecone_id:
                continue

            metadata = {
                "chunk_id": chunk_id,
                "user_id": user_id,
                "source_url": chunk.get("source_url", "")[:500],
                "document_title": chunk.get("document_title", "")[:200],
                "section_title": chunk.get("section_title", "")[:200] if chunk.get("section_title") else "",
                "research_session_id": chunk.get("research_session_id", ""),
                "content_preview": chunk.get("original_content", "")[:500],
            }

            vectors.append({
                "id": pinecone_id,
                "values": embedding,
                "metadata": metadata,
            })

        if not vectors:
            logger.warning("No valid vectors to load for user %s", user_id)
            return 0

        logger.info(
            "Loading %d user knowledge vectors to Pinecone namespace '%s'",
            len(vectors),
            namespace,
        )

        loaded_count = 0
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i : i + batch_size]
            try:
                self.circuit_breaker.call(
                    self.index.upsert,
                    vectors=batch,
                    namespace=namespace,
                )
                loaded_count += len(batch)
            except CircuitBreakerOpenError:
                logger.error("Pinecone circuit breaker is OPEN - skipping batch")
                break
            except Exception as e:
                logger.error("Failed to upsert user knowledge batch: %s", e)

        logger.info(
            "Loaded %d user knowledge vectors to Pinecone",
            loaded_count,
        )

        return loaded_count

    def query_user_knowledge(
        self,
        user_id: str,
        query_embedding: list[float],
        top_k: int = 10,
        filter_dict: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Query user's knowledge chunks from Pinecone.

        Args:
            user_id: User ID for namespace
            query_embedding: Query embedding vector
            top_k: Number of results to return
            filter_dict: Optional metadata filter

        Returns:
            List of matching chunks with scores
        """
        namespace = f"user_{user_id}"

        try:
            results = self.circuit_breaker.call(
                self.index.query,
                vector=query_embedding,
                top_k=top_k,
                namespace=namespace,
                filter=filter_dict,
                include_metadata=True,
            )

            matches = []
            for match in results.get("matches", []):
                matches.append({
                    "chunk_id": match.get("metadata", {}).get("chunk_id"),
                    "score": match.get("score", 0.0),
                    "metadata": match.get("metadata", {}),
                })

            return matches
        except CircuitBreakerOpenError:
            logger.error("Pinecone circuit breaker is OPEN - returning empty results")
            return []
        except Exception as e:
            logger.error("Failed to query user knowledge: %s", e)
            return []

    def delete_user_knowledge(
        self,
        user_id: str,
        chunk_ids: list[str] | None = None,
        delete_all: bool = False,
    ) -> bool:
        """Delete user's knowledge chunks from Pinecone.

        Args:
            user_id: User ID for namespace
            chunk_ids: Optional specific chunk IDs to delete
            delete_all: If True, delete all vectors in user's namespace

        Returns:
            True if deletion succeeded
        """
        namespace = f"user_{user_id}"

        try:
            if delete_all:
                # Delete entire namespace
                self.circuit_breaker.call(
                    self.index.delete,
                    delete_all=True,
                    namespace=namespace,
                )
                logger.info("Deleted all vectors in namespace '%s'", namespace)
            elif chunk_ids:
                # Delete specific chunks
                pinecone_ids = [
                    self._sanitize_id(f"chunk_{cid}")
                    for cid in chunk_ids
                    if self._sanitize_id(f"chunk_{cid}")
                ]
                if pinecone_ids:
                    self.circuit_breaker.call(
                        self.index.delete,
                        ids=pinecone_ids,
                        namespace=namespace,
                    )
                    logger.info(
                        "Deleted %d vectors from namespace '%s'",
                        len(pinecone_ids),
                        namespace,
                    )
            return True
        except CircuitBreakerOpenError:
            logger.error("Pinecone circuit breaker is OPEN - skipping delete")
            return False
        except Exception as e:
            logger.error("Failed to delete user knowledge: %s", e)
            return False

