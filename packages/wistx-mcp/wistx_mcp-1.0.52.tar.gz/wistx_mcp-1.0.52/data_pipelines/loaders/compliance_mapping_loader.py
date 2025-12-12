"""Compliance mapping loader - stores compliance mappings in MongoDB."""

import logging
from typing import Any

from pymongo.collection import Collection
from pymongo.errors import BulkWriteError
from pymongo.operations import UpdateOne

from data_pipelines.loaders.mongodb_loader import MongoDBLoader
from data_pipelines.models.compliance_mapping import ComplianceMapping

logger = logging.getLogger(__name__)


class ComplianceMappingLoader:
    """Load compliance mappings into MongoDB."""

    def __init__(self, mongodb_loader: MongoDBLoader | None = None):
        """Initialize compliance mapping loader.
        
        Args:
            mongodb_loader: MongoDB loader instance (optional, creates new if not provided)
        """
        self.mongodb_loader = mongodb_loader or MongoDBLoader()
        self.collection_name = "code_example_compliance_mappings"

    def load_mappings(
        self,
        mappings: list[ComplianceMapping],
        batch_size: int = 100,
    ) -> dict[str, int]:
        """Load compliance mappings into MongoDB.
        
        Args:
            mappings: List of compliance mappings
            batch_size: Batch size for MongoDB operations
            
        Returns:
            Dictionary with loading statistics
        """
        if not mappings:
            logger.info("No mappings to load")
            return {
                "inserted": 0,
                "updated": 0,
                "errors": 0,
            }
        
        db = self.mongodb_loader.db
        if not db:
            raise RuntimeError("Failed to connect to MongoDB")
        
        collection: Collection = db[self.collection_name]
        
        logger.info("Loading %d compliance mappings into MongoDB...", len(mappings))
        
        stats = {
            "inserted": 0,
            "updated": 0,
            "errors": 0,
        }
        
        operations = []
        
        for mapping in mappings:
            mapping_dict = mapping.model_dump()
            mapping_dict["_id"] = mapping.mapping_id
            
            operations.append(
                UpdateOne(
                    {"mapping_id": mapping.mapping_id},
                    {"$set": mapping_dict},
                    upsert=True,
                )
            )
        
        try:
            for i in range(0, len(operations), batch_size):
                batch = operations[i : i + batch_size]
                result = collection.bulk_write(batch, ordered=False)
                
                stats["inserted"] += result.upserted_count
                stats["updated"] += result.modified_count
        
        except BulkWriteError as e:
            write_errors = e.details.get("writeErrors", [])
            stats["inserted"] += e.details.get("nInserted", 0)
            stats["updated"] += e.details.get("nModified", 0)
            stats["errors"] += len(write_errors)
            
            if write_errors:
                logger.warning(
                    "Bulk write had %d errors out of %d operations. "
                    "Inserted: %d, Modified: %d",
                    len(write_errors),
                    len(operations),
                    e.details.get("nInserted", 0),
                    e.details.get("nModified", 0),
                )
        
        except Exception as e:
            logger.error("Error loading compliance mappings: %s", e)
            stats["errors"] = len(operations)
            raise
        
        logger.info(
            "Compliance mappings loaded: Inserted %d, Updated %d, Errors %d",
            stats["inserted"],
            stats["updated"],
            stats["errors"],
        )
        
        return stats

    def get_mappings_for_example(
        self,
        example_id: str,
    ) -> list[dict[str, Any]]:
        """Get all compliance mappings for a code example.
        
        Args:
            example_id: Code example ID
            
        Returns:
            List of mapping dictionaries
        """
        db = self.mongodb_loader.db
        if not db:
            raise RuntimeError("Failed to connect to MongoDB")
        
        collection: Collection = db[self.collection_name]
        
        mappings = list(collection.find({"example_id": example_id}))
        
        return [dict(mapping) for mapping in mappings]

    def get_mappings_for_standard(
        self,
        standard: str,
        implementation_status: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get compliance mappings for a specific standard.
        
        Args:
            standard: Compliance standard (PCI-DSS, HIPAA, etc.)
            implementation_status: Optional filter by implementation status
            
        Returns:
            List of mapping dictionaries
        """
        db = self.mongodb_loader.db
        if not db:
            raise RuntimeError("Failed to connect to MongoDB")
        
        collection: Collection = db[self.collection_name]
        
        query = {"standard": standard}
        if implementation_status:
            query["implementation_status"] = implementation_status
        
        mappings = list(collection.find(query))
        
        return [dict(mapping) for mapping in mappings]

    def get_compliant_examples(
        self,
        standard: str,
        resource_types: list[str] | None = None,
        min_relevance_score: float = 0.5,
    ) -> list[str]:
        """Get example IDs that are compliant with a standard.
        
        Args:
            standard: Compliance standard
            resource_types: Optional filter by resource types
            min_relevance_score: Minimum relevance score
            
        Returns:
            List of example IDs
        """
        db = self.mongodb_loader.db
        if not db:
            raise RuntimeError("Failed to connect to MongoDB")
        
        collection: Collection = db[self.collection_name]
        
        query = {
            "standard": standard,
            "implementation_status": "implemented",
            "relevance_score": {"$gte": min_relevance_score},
        }
        
        if resource_types:
            query["applies_to_resources"] = {"$in": resource_types}
        
        mappings = list(collection.find(query, {"example_id": 1}))
        
        example_ids = list(set(mapping["example_id"] for mapping in mappings))
        
        return example_ids

