"""MongoDB loader for document storage with Pinecone sync."""

import logging
from typing import Any

from pymongo import UpdateOne
from pymongo.errors import BulkWriteError, DuplicateKeyError
from tqdm import tqdm

from api.database.mongodb import mongodb_manager
from data_pipelines.loaders.pinecone_loader import PineconeLoader
from data_pipelines.utils.config import PipelineSettings
from data_pipelines.utils.sanitization import sanitize_control_id

logger = logging.getLogger(__name__)
settings = PipelineSettings()


class MongoDBLoader:
    """Load documents into MongoDB (without embeddings) and sync vectors to Pinecone.

    This loader implements the sync strategy:
    1. Strip embeddings from documents before MongoDB storage
    2. Upsert documents to MongoDB (idempotent)
    3. Load vectors to Pinecone (with embeddings)
    """

    def __init__(self):
        """Initialize MongoDB loader."""
        self.db = mongodb_manager.get_database()
        self.pinecone_loader = PineconeLoader()
        self.batch_size = settings.batch_size

    def _strip_embedding(self, document: dict[str, Any]) -> dict[str, Any]:
        """Strip embedding field from document.

        Args:
            document: Document dictionary (may contain embedding)

        Returns:
            Document dictionary without embedding field
        """
        return {k: v for k, v in document.items() if k != "embedding"}

    def save_single_control(self, doc: dict[str, Any]) -> tuple[bool, str]:
        """Save a single control to MongoDB immediately.

        Args:
            doc: Control document dictionary

        Returns:
            Tuple of (success: bool, action: str)
            - success: True if saved successfully
            - action: "inserted" or "updated"
        """
        collection = self.db.compliance_controls
        
        try:
            control_id = doc.get("control_id")
            if not control_id:
                logger.warning("Cannot save control without control_id")
                return False, "error"

            control_id = sanitize_control_id(control_id, max_length=100)
            doc["control_id"] = control_id

            source_hash = doc.pop("_source_hash", None)
            content_hash = doc.pop("_content_hash", None)
            
            if source_hash:
                doc["source_hash"] = source_hash
            if content_hash:
                doc["content_hash"] = content_hash

            doc.pop("embedding", None)

            result = collection.update_one(
                {"control_id": control_id},
                {"$set": doc},
                upsert=True,
            )

            if result.upserted_id:
                logger.debug("Saved control to MongoDB: %s (INSERTED)", control_id)
                return True, "inserted"
            else:
                logger.debug("Saved control to MongoDB: %s (UPDATED)", control_id)
                return True, "updated"
        except Exception as e:
            logger.error("Error saving control %s: %s", doc.get("control_id"), e, exc_info=True)
            return False, "error"

    async def save_single_control_async(self, doc: dict[str, Any]) -> tuple[bool, str]:
        """Save a single control to MongoDB asynchronously (non-blocking).

        Args:
            doc: Control document dictionary

        Returns:
            Tuple of (success: bool, action: str)
            - success: True if saved successfully
            - action: "inserted" or "updated"
        """
        import asyncio
        return await asyncio.to_thread(self.save_single_control, doc)

    async def save_controls_batch_async(self, docs: list[dict[str, Any]]) -> dict[str, int]:
        """Save multiple controls to MongoDB asynchronously using bulk operations.

        Args:
            docs: List of control document dictionaries

        Returns:
            Dictionary with statistics: {"inserted": int, "updated": int, "errors": int}
        """
        import asyncio
        from pymongo import UpdateOne
        
        collection = self.db.compliance_controls
        stats = {"inserted": 0, "updated": 0, "errors": 0}
        
        if not docs:
            return stats
        
        operations = []
        for doc in docs:
            try:
                control_id = doc.get("control_id")
                if not control_id:
                    stats["errors"] += 1
                    continue

                control_id = sanitize_control_id(control_id, max_length=100)
                doc["control_id"] = control_id

                source_hash = doc.pop("_source_hash", None)
                content_hash = doc.pop("_content_hash", None)
                
                if source_hash:
                    doc["source_hash"] = source_hash
                if content_hash:
                    doc["content_hash"] = content_hash

                doc.pop("embedding", None)

                operations.append(
                    UpdateOne(
                        {"control_id": control_id},
                        {"$set": doc},
                        upsert=True,
                    )
                )
            except Exception as e:
                logger.warning("Error preparing control for batch save: %s", e)
                stats["errors"] += 1
        
        if operations:
            try:
                result = await asyncio.to_thread(
                    collection.bulk_write,
                    operations,
                    ordered=False
                )
                stats["inserted"] = result.upserted_count
                stats["updated"] = result.modified_count
            except Exception as e:
                logger.error("Error in batch save: %s", e, exc_info=True)
                stats["errors"] += len(operations)
        
        return stats

    async def update_control_embedding_streaming(
        self, control_id: str, _embedding: list[float], content_hash: str | None = None
    ) -> bool:
        """Update a single control with embedding immediately.

        Args:
            control_id: Control ID
            _embedding: Embedding vector (not used, kept for API compatibility)
            content_hash: Optional content hash

        Returns:
            True if updated successfully
        """
        collection = self.db.compliance_controls
        
        try:
            update_doc: dict[str, Any] = {}
            if content_hash:
                update_doc["content_hash"] = content_hash
            
            result = collection.update_one(
                {"control_id": control_id},
                {"$set": update_doc}
            )
            return result.modified_count > 0 or result.matched_count > 0
        except (ValueError, KeyError, TypeError) as e:
            logger.error("Error updating embedding for control %s: %s", control_id, e)
            return False

    def load_compliance_controls(
        self, controls: list[dict[str, Any]], batch_size: int | None = None
    ) -> dict[str, int]:
        """Load compliance controls into MongoDB and Pinecone.

        Args:
            controls: List of compliance control documents (with embeddings)
            batch_size: Batch size for MongoDB operations (default: settings.batch_size)

        Returns:
            Dictionary with loading statistics:
            {
                "mongodb_inserted": int,
                "mongodb_updated": int,
                "mongodb_errors": int,
                "pinecone_loaded": int,
                "pinecone_skipped": int
            }
        """
        batch_size = batch_size or self.batch_size
        collection = self.db.compliance_controls

        logger.info("Loading %d compliance controls into MongoDB and Pinecone...", len(controls))

        stats = {
            "mongodb_inserted": 0,
            "mongodb_updated": 0,
            "mongodb_errors": 0,
            "pinecone_loaded": 0,
            "pinecone_skipped": 0,
        }

        documents_without_embeddings = [self._strip_embedding(control) for control in controls]

        for i in tqdm(
            range(0, len(documents_without_embeddings), batch_size),
            desc="Loading compliance controls to MongoDB",
        ):
            batch = documents_without_embeddings[i : i + batch_size]
            operations = []

            for doc in batch:
                control_id = doc.get("control_id")
                if not control_id:
                    logger.warning("Skipping control without control_id: %s", doc.get("title", "unknown"))
                    stats["mongodb_errors"] += 1
                    continue

                control_id = sanitize_control_id(control_id, max_length=100)
                doc["control_id"] = control_id

                source_hash = doc.pop("_source_hash", None)
                content_hash = doc.pop("_content_hash", None)
                
                if source_hash:
                    doc["source_hash"] = source_hash
                if content_hash:
                    doc["content_hash"] = content_hash

                operations.append(
                    UpdateOne(
                        {"control_id": control_id},
                        {"$set": doc},
                        upsert=True,
                    )
                )

            if operations:
                try:
                    result = collection.bulk_write(operations, ordered=False)
                    stats["mongodb_inserted"] += result.upserted_count
                    stats["mongodb_updated"] += result.modified_count
                except BulkWriteError as e:
                    write_errors = e.details.get("writeErrors", [])
                    stats["mongodb_inserted"] += e.details.get("nInserted", 0)
                    stats["mongodb_updated"] += e.details.get("nModified", 0)
                    stats["mongodb_errors"] += len(write_errors)
                    if write_errors:
                        logger.warning(
                            "Bulk write had %d errors out of %d operations. "
                            "Inserted: %d, Modified: %d",
                            len(write_errors),
                            len(operations),
                            e.details.get("nInserted", 0),
                            e.details.get("nModified", 0),
                        )
                except (ValueError, KeyError, TypeError) as e:
                    logger.error("Error in bulk write: %s", e)
                    stats["mongodb_errors"] += len(operations)

        logger.info(
            "MongoDB: Inserted %d, Updated %d, Errors %d",
            stats["mongodb_inserted"],
            stats["mongodb_updated"],
            stats["mongodb_errors"],
        )

        controls_with_embeddings = [c for c in controls if c.get("embedding")]
        controls_without_embeddings_count = len(controls) - len(controls_with_embeddings)

        if controls_without_embeddings_count > 0:
            logger.info(
                "Skipping %d controls without embeddings for Pinecone",
                controls_without_embeddings_count,
            )
            stats["pinecone_skipped"] = controls_without_embeddings_count

        if controls_with_embeddings:
            try:
                self.pinecone_loader.load_compliance_controls(controls_with_embeddings)
                stats["pinecone_loaded"] = len(controls_with_embeddings)
            except Exception as e:
                logger.error("Error loading compliance controls to Pinecone: %s", e)
                raise

        logger.info(
            "Loaded %d compliance controls: MongoDB (%d docs), Pinecone (%d vectors)",
            len(controls),
            stats["mongodb_inserted"] + stats["mongodb_updated"],
            stats["pinecone_loaded"],
        )

        return stats

    def load_pricing_data(
        self, pricing_items: list[dict[str, Any]], batch_size: int | None = None
    ) -> dict[str, int]:
        """Load pricing data into MongoDB and Pinecone.

        Args:
            pricing_items: List of pricing data documents (with embeddings)
            batch_size: Batch size for MongoDB operations (default: settings.batch_size)

        Returns:
            Dictionary with loading statistics
        """
        batch_size = batch_size or self.batch_size
        collection = self.db.pricing_data

        logger.info("Loading %d pricing items into MongoDB and Pinecone...", len(pricing_items))

        stats = {
            "mongodb_inserted": 0,
            "mongodb_updated": 0,
            "mongodb_errors": 0,
            "pinecone_loaded": 0,
            "pinecone_skipped": 0,
        }

        documents_without_embeddings = [
            self._strip_embedding(item) for item in pricing_items
        ]

        for i in tqdm(
            range(0, len(documents_without_embeddings), batch_size),
            desc="Loading pricing data to MongoDB",
        ):
            batch = documents_without_embeddings[i : i + batch_size]
            operations = []

            for doc in batch:
                lookup_key = doc.get("lookup_key")
                if not lookup_key:
                    logger.warning(
                        "Skipping pricing item without lookup_key: %s",
                        doc.get("resource_type", "unknown"),
                    )
                    stats["mongodb_errors"] += 1
                    continue

                operations.append(
                    UpdateOne(
                        {"lookup_key": lookup_key},
                        {"$set": doc},
                        upsert=True,
                    )
                )

            if operations:
                try:
                    result = collection.bulk_write(operations, ordered=False)
                    stats["mongodb_inserted"] += result.upserted_count
                    stats["mongodb_updated"] += result.modified_count
                except BulkWriteError as e:
                    write_errors = e.details.get("writeErrors", [])
                    stats["mongodb_inserted"] += e.details.get("nInserted", 0)
                    stats["mongodb_updated"] += e.details.get("nModified", 0)
                    stats["mongodb_errors"] += len(write_errors)
                    if write_errors:
                        logger.warning(
                            "Bulk write had %d errors out of %d operations. "
                            "Inserted: %d, Modified: %d",
                            len(write_errors),
                            len(operations),
                            e.details.get("nInserted", 0),
                            e.details.get("nModified", 0),
                        )
                except (ValueError, KeyError, TypeError) as e:
                    logger.error("Error in bulk write: %s", e)
                    stats["mongodb_errors"] += len(operations)

        logger.info(
            "MongoDB: Inserted %d, Updated %d, Errors %d",
            stats["mongodb_inserted"],
            stats["mongodb_updated"],
            stats["mongodb_errors"],
        )

        items_with_embeddings = [item for item in pricing_items if item.get("embedding")]
        items_without_embeddings_count = len(pricing_items) - len(items_with_embeddings)

        if items_without_embeddings_count > 0:
            logger.info(
                "Skipping %d pricing items without embeddings for Pinecone",
                items_without_embeddings_count,
            )
            stats["pinecone_skipped"] = items_without_embeddings_count

        if items_with_embeddings:
            try:
                self.pinecone_loader.load_pricing_data(items_with_embeddings)
                stats["pinecone_loaded"] = len(items_with_embeddings)
            except Exception as e:
                logger.error("Error loading pricing data to Pinecone: %s", e)
                raise

        logger.info(
            "Loaded %d pricing items: MongoDB (%d docs), Pinecone (%d vectors)",
            len(pricing_items),
            stats["mongodb_inserted"] + stats["mongodb_updated"],
            stats["pinecone_loaded"],
        )

        return stats

    def load_cost_data_focus(
        self, cost_records: list[dict[str, Any]], batch_size: int | None = None
    ) -> dict[str, int]:
        """Load FOCUS-compliant cost data into MongoDB and Pinecone.

        Args:
            cost_records: List of FOCUSCostData documents (with embeddings)
            batch_size: Batch size for MongoDB operations (default: settings.batch_size)

        Returns:
            Dictionary with loading statistics
        """
        batch_size = batch_size or self.batch_size
        collection = self.db.cost_data_focus

        logger.info("Loading %d FOCUS cost records into MongoDB and Pinecone...", len(cost_records))

        stats = {
            "mongodb_inserted": 0,
            "mongodb_updated": 0,
            "mongodb_errors": 0,
            "pinecone_loaded": 0,
            "pinecone_skipped": 0,
        }

        documents_without_embeddings = [
            self._strip_embedding(item) for item in cost_records
        ]

        for i in tqdm(
            range(0, len(documents_without_embeddings), batch_size),
            desc="Loading FOCUS cost data to MongoDB",
        ):
            batch = documents_without_embeddings[i : i + batch_size]
            operations = []

            for doc in batch:
                lookup_key = doc.get("lookup_key")
                if not lookup_key:
                    logger.warning(
                        "Skipping cost record without lookup_key: %s",
                        doc.get("resource_id", "unknown"),
                    )
                    stats["mongodb_errors"] += 1
                    continue

                operations.append(
                    UpdateOne(
                        {"lookup_key": lookup_key},
                        {"$set": doc},
                        upsert=True,
                    )
                )

            if operations:
                try:
                    lookup_keys_in_batch = [op._filter.get("lookup_key") for op in operations]
                    logger.debug("Upserting batch with lookup_keys: %s", lookup_keys_in_batch[:5])
                    
                    result = collection.bulk_write(operations, ordered=False)
                    stats["mongodb_inserted"] += result.upserted_count
                    stats["mongodb_updated"] += result.modified_count
                    
                    if result.upserted_count > 0:
                        logger.info("Inserted %d new cost records with lookup_keys: %s", result.upserted_count, lookup_keys_in_batch[:result.upserted_count])
                    if result.modified_count > 0:
                        logger.info("Updated %d existing cost records. Sample lookup_keys: %s", result.modified_count, lookup_keys_in_batch[:min(3, len(lookup_keys_in_batch))])
                        
                        sample_key = lookup_keys_in_batch[0] if lookup_keys_in_batch else None
                        if sample_key:
                            sample_doc = collection.find_one({"lookup_key": sample_key})
                            if sample_doc:
                                logger.debug("Sample updated cost record - provider: %s, service: %s, region: %s, last_updated: %s", 
                                           sample_doc.get("provider"), sample_doc.get("service_name"), 
                                           sample_doc.get("region_id"), sample_doc.get("last_updated"))
                except BulkWriteError as e:
                    write_errors = e.details.get("writeErrors", [])
                    stats["mongodb_inserted"] += e.details.get("nInserted", 0)
                    stats["mongodb_updated"] += e.details.get("nModified", 0)
                    stats["mongodb_errors"] += len(write_errors)
                    if write_errors:
                        logger.warning(
                            "Bulk write had %d errors out of %d operations. "
                            "Inserted: %d, Modified: %d",
                            len(write_errors),
                            len(operations),
                            e.details.get("nInserted", 0),
                            e.details.get("nModified", 0),
                        )
                except (ValueError, KeyError, TypeError) as e:
                    logger.error("Error in bulk write: %s", e)
                    stats["mongodb_errors"] += len(operations)

        total_processed = stats["mongodb_inserted"] + stats["mongodb_updated"]
        logger.info(
            "MongoDB: Inserted %d (new), Updated %d (existing), Total processed: %d, Errors: %d",
            stats["mongodb_inserted"],
            stats["mongodb_updated"],
            total_processed,
            stats["mongodb_errors"],
        )
        
        if total_processed > 0:
            sample_query = collection.find_one({"provider": "gcp"})
            if sample_query:
                logger.info("Verification: Found sample GCP record in MongoDB - provider: %s, service: %s, lookup_key: %s, last_updated: %s", 
                           sample_query.get("provider"), sample_query.get("service_name"), 
                           sample_query.get("lookup_key"), sample_query.get("last_updated"))

        records_with_embeddings = [item for item in cost_records if item.get("embedding")]
        records_without_embeddings_count = len(cost_records) - len(records_with_embeddings)

        if records_without_embeddings_count > 0:
            logger.info(
                "Skipping %d cost records without embeddings for Pinecone",
                records_without_embeddings_count,
            )
            stats["pinecone_skipped"] = records_without_embeddings_count

        if records_with_embeddings:
            try:
                self.pinecone_loader.load_cost_data_focus(records_with_embeddings)
                stats["pinecone_loaded"] = len(records_with_embeddings)
            except Exception as e:
                logger.error("Error loading FOCUS cost data to Pinecone: %s", e, exc_info=True)
                stats["pinecone_errors"] = str(e)
                stats["pinecone_loaded"] = 0
                logger.warning(
                    "Pinecone loading failed. MongoDB data saved successfully, but vectors not indexed. "
                    "Re-run pipeline after fixing Pinecone issues to index vectors."
                )
        else:
            logger.warning(
                "No records with embeddings to load to Pinecone. "
                "Ensure embedding stage completed successfully before loading."
            )

        logger.info(
            "Loaded %d FOCUS cost records: MongoDB (%d docs), Pinecone (%d vectors)",
            len(cost_records),
            stats["mongodb_inserted"] + stats["mongodb_updated"],
            stats["pinecone_loaded"],
        )

        return stats

    def load_code_examples(
        self, examples: list[dict[str, Any]], batch_size: int | None = None
    ) -> dict[str, int]:
        """Load code examples into MongoDB and Pinecone.

        Args:
            examples: List of code example documents (with embeddings)
            batch_size: Batch size for MongoDB operations (default: settings.batch_size)

        Returns:
            Dictionary with loading statistics
        """
        batch_size = batch_size or self.batch_size
        collection = self.db.code_examples

        logger.info("Loading %d code examples into MongoDB and Pinecone...", len(examples))

        stats = {
            "mongodb_inserted": 0,
            "mongodb_updated": 0,
            "mongodb_errors": 0,
            "pinecone_loaded": 0,
            "pinecone_skipped": 0,
        }

        documents_without_embeddings = [self._strip_embedding(example) for example in examples]

        for i in tqdm(
            range(0, len(documents_without_embeddings), batch_size),
            desc="Loading code examples to MongoDB",
        ):
            batch = documents_without_embeddings[i : i + batch_size]
            operations = []

            for doc in batch:
                example_id = doc.get("example_id")
                if not example_id:
                    logger.warning(
                        "Skipping code example without example_id: %s",
                        doc.get("title", "unknown"),
                    )
                    stats["mongodb_errors"] += 1
                    continue

                operations.append(
                    UpdateOne(
                        {"example_id": example_id},
                        {"$set": doc},
                        upsert=True,
                    )
                )

            if operations:
                try:
                    result = collection.bulk_write(operations, ordered=False)
                    stats["mongodb_inserted"] += result.upserted_count
                    stats["mongodb_updated"] += result.modified_count
                except BulkWriteError as e:
                    write_errors = e.details.get("writeErrors", [])
                    stats["mongodb_inserted"] += e.details.get("nInserted", 0)
                    stats["mongodb_updated"] += e.details.get("nModified", 0)
                    stats["mongodb_errors"] += len(write_errors)
                    if write_errors:
                        logger.warning(
                            "Bulk write had %d errors out of %d operations. "
                            "Inserted: %d, Modified: %d",
                            len(write_errors),
                            len(operations),
                            e.details.get("nInserted", 0),
                            e.details.get("nModified", 0),
                        )
                except (ValueError, KeyError, TypeError) as e:
                    logger.error("Error in bulk write: %s", e)
                    stats["mongodb_errors"] += len(operations)

        logger.info(
            "MongoDB: Inserted %d, Updated %d, Errors %d",
            stats["mongodb_inserted"],
            stats["mongodb_updated"],
            stats["mongodb_errors"],
        )

        examples_with_embeddings = [ex for ex in examples if ex.get("embedding")]
        examples_without_embeddings_count = len(examples) - len(examples_with_embeddings)

        if examples_without_embeddings_count > 0:
            logger.info(
                "Skipping %d code examples without embeddings for Pinecone",
                examples_without_embeddings_count,
            )
            stats["pinecone_skipped"] = examples_without_embeddings_count

        if examples_with_embeddings:
            try:
                self.pinecone_loader.load_code_examples(examples_with_embeddings)
                stats["pinecone_loaded"] = len(examples_with_embeddings)
            except Exception as e:
                logger.error("Error loading code examples to Pinecone: %s", e)
                raise

        logger.info(
            "Loaded %d code examples: MongoDB (%d docs), Pinecone (%d vectors)",
            len(examples),
            stats["mongodb_inserted"] + stats["mongodb_updated"],
            stats["pinecone_loaded"],
        )

        return stats

    def load_knowledge_articles(
        self, articles: list[dict[str, Any]], batch_size: int | None = None
    ) -> dict[str, int]:
        """Load knowledge articles into MongoDB and Pinecone.
        
        Args:
            articles: List of knowledge article documents (with embeddings)
            batch_size: Batch size for MongoDB operations (default: settings.batch_size)
            
        Returns:
            Dictionary with loading statistics
        """
        batch_size = batch_size or self.batch_size
        collection = self.db.knowledge_articles

        logger.info("Loading %d knowledge articles into MongoDB and Pinecone...", len(articles))

        stats = {
            "mongodb_inserted": 0,
            "mongodb_updated": 0,
            "mongodb_errors": 0,
            "pinecone_loaded": 0,
            "pinecone_skipped": 0,
        }

        documents_without_embeddings = [
            self._strip_embedding(article) for article in articles
        ]

        for i in tqdm(
            range(0, len(documents_without_embeddings), batch_size),
            desc="Loading knowledge articles to MongoDB",
        ):
            batch = documents_without_embeddings[i : i + batch_size]
            operations = []

            for doc in batch:
                article_id = doc.get("article_id")
                if not article_id:
                    logger.warning(
                        "Skipping knowledge article without article_id: %s",
                        doc.get("title", "unknown"),
                    )
                    stats["mongodb_errors"] += 1
                    continue

                domain = doc.get("domain")
                if hasattr(domain, "value"):
                    doc["domain"] = domain.value
                
                content_type = doc.get("content_type")
                if hasattr(content_type, "value"):
                    doc["content_type"] = content_type.value

                operations.append(
                    UpdateOne(
                        {"article_id": article_id},
                        {"$set": doc},
                        upsert=True,
                    )
                )

            if operations:
                try:
                    result = collection.bulk_write(operations, ordered=False)
                    stats["mongodb_inserted"] += result.upserted_count
                    stats["mongodb_updated"] += result.modified_count
                except BulkWriteError as e:
                    write_errors = e.details.get("writeErrors", [])
                    stats["mongodb_inserted"] += e.details.get("nInserted", 0)
                    stats["mongodb_updated"] += e.details.get("nModified", 0)
                    stats["mongodb_errors"] += len(write_errors)
                    if write_errors:
                        logger.warning(
                            "Bulk write had %d errors out of %d operations. "
                            "Inserted: %d, Modified: %d",
                            len(write_errors),
                            len(operations),
                            e.details.get("nInserted", 0),
                            e.details.get("nModified", 0),
                        )
                except (ValueError, KeyError, TypeError) as e:
                    logger.error("Error in bulk write: %s", e)
                    stats["mongodb_errors"] += len(operations)

        logger.info(
            "MongoDB: Inserted %d, Updated %d, Errors %d",
            stats["mongodb_inserted"],
            stats["mongodb_updated"],
            stats["mongodb_errors"],
        )

        articles_with_embeddings = [a for a in articles if a.get("embedding")]
        articles_without_embeddings_count = len(articles) - len(articles_with_embeddings)

        if articles_without_embeddings_count > 0:
            logger.info(
                "Skipping %d knowledge articles without embeddings for Pinecone",
                articles_without_embeddings_count,
            )
            stats["pinecone_skipped"] = articles_without_embeddings_count

        if articles_with_embeddings:
            try:
                self.pinecone_loader.load_knowledge_articles(articles_with_embeddings)  # type: ignore[attr-defined]
                stats["pinecone_loaded"] = len(articles_with_embeddings)
            except Exception as e:
                logger.error("Error loading knowledge articles to Pinecone: %s", e)
                raise

        logger.info(
            "Loaded %d knowledge articles: MongoDB (%d docs), Pinecone (%d vectors)",
            len(articles),
            stats["mongodb_inserted"] + stats["mongodb_updated"],
            stats["pinecone_loaded"],
        )

        return stats

    def load_user_knowledge_chunks(
        self,
        chunks: list[dict[str, Any]],
        user_id: str,
        research_session_id: str | None = None,
        batch_size: int | None = None,
    ) -> dict[str, int]:
        """Load user-scoped knowledge chunks into MongoDB.

        This stores chunks from on-demand research in a user-specific collection.
        Chunks are indexed for hybrid retrieval (semantic + BM25).

        Args:
            chunks: List of indexed chunk documents
            user_id: User ID for scoping
            research_session_id: Optional research session ID
            batch_size: Batch size for MongoDB operations

        Returns:
            Dictionary with loading statistics
        """
        batch_size = batch_size or self.batch_size
        collection = self.db.user_knowledge_chunks

        logger.info(
            "Loading %d user knowledge chunks for user %s...",
            len(chunks),
            user_id,
        )

        stats = {
            "mongodb_inserted": 0,
            "mongodb_updated": 0,
            "mongodb_errors": 0,
            "pinecone_loaded": 0,
        }

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]
            operations = []

            for chunk in batch:
                chunk_id = chunk.get("chunk_id")
                if not chunk_id:
                    logger.warning("Skipping chunk without chunk_id")
                    stats["mongodb_errors"] += 1
                    continue

                # Ensure user_id is set
                chunk["user_id"] = user_id
                if research_session_id:
                    chunk["research_session_id"] = research_session_id

                # Strip embedding for MongoDB (stored in Pinecone)
                doc = self._strip_embedding(chunk)

                operations.append(
                    UpdateOne(
                        {"chunk_id": chunk_id, "user_id": user_id},
                        {"$set": doc},
                        upsert=True,
                    )
                )

            if operations:
                try:
                    result = collection.bulk_write(operations, ordered=False)
                    stats["mongodb_inserted"] += result.upserted_count
                    stats["mongodb_updated"] += result.modified_count
                except BulkWriteError as e:
                    stats["mongodb_inserted"] += e.details.get("nInserted", 0)
                    stats["mongodb_updated"] += e.details.get("nModified", 0)
                    stats["mongodb_errors"] += len(e.details.get("writeErrors", []))
                except Exception as e:
                    logger.error("Error in bulk write: %s", e)
                    stats["mongodb_errors"] += len(operations)

        # Load embeddings to Pinecone with user namespace
        chunks_with_embeddings = [c for c in chunks if c.get("embedding")]
        if chunks_with_embeddings:
            try:
                self.pinecone_loader.load_user_knowledge_chunks(
                    chunks_with_embeddings,
                    user_id=user_id,
                )
                stats["pinecone_loaded"] = len(chunks_with_embeddings)
            except Exception as e:
                logger.error("Error loading to Pinecone: %s", e)

        logger.info(
            "Loaded %d user chunks: MongoDB (%d), Pinecone (%d)",
            len(chunks),
            stats["mongodb_inserted"] + stats["mongodb_updated"],
            stats["pinecone_loaded"],
        )

        return stats

    def get_user_knowledge_chunks(
        self,
        user_id: str,
        research_session_id: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Get user's knowledge chunks from MongoDB.

        Args:
            user_id: User ID
            research_session_id: Optional filter by research session
            limit: Maximum number of chunks to return

        Returns:
            List of chunk documents
        """
        collection = self.db.user_knowledge_chunks

        query = {"user_id": user_id}
        if research_session_id:
            query["research_session_id"] = research_session_id

        return list(collection.find(query).limit(limit))

    def delete_user_knowledge_chunks(
        self,
        user_id: str,
        research_session_id: str | None = None,
        chunk_ids: list[str] | None = None,
    ) -> int:
        """Delete user's knowledge chunks.

        Args:
            user_id: User ID
            research_session_id: Optional filter by research session
            chunk_ids: Optional specific chunk IDs to delete

        Returns:
            Number of deleted documents
        """
        collection = self.db.user_knowledge_chunks

        query: dict[str, Any] = {"user_id": user_id}
        if research_session_id:
            query["research_session_id"] = research_session_id
        if chunk_ids:
            query["chunk_id"] = {"$in": chunk_ids}

        result = collection.delete_many(query)

        logger.info(
            "Deleted %d user knowledge chunks for user %s",
            result.deleted_count,
            user_id,
        )

        return result.deleted_count
