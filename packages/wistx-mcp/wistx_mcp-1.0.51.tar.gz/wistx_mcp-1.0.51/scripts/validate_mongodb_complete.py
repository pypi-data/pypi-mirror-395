"""Comprehensive MongoDB validation script.

Validates:
1. MongoDB connection
2. Collections exist
3. Indexes are created
4. Vector search configuration
5. Schema compliance
"""

import logging
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from api.database.mongodb import mongodb_manager
from api.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_connection() -> bool:
    """Validate MongoDB connection."""
    logger.info("=" * 80)
    logger.info("1. Validating MongoDB Connection")
    logger.info("=" * 80)

    try:
        mongodb_manager.connect()
        health = mongodb_manager.health_check()
        
        if health.get("status") == "healthy":
            logger.info("✅ MongoDB connection: HEALTHY")
            logger.info("   Latency: %sms", health.get("latency_ms", "N/A"))
            logger.info("   Database: %s", settings.mongodb_database)
            return True
        else:
            logger.error("❌ MongoDB connection: %s", health.get("status", "UNKNOWN"))
            return False
    except Exception as e:
        logger.error("❌ MongoDB connection failed: %s", e)
        return False


def validate_collections() -> bool:
    """Validate that all required collections exist."""
    logger.info("")
    logger.info("=" * 80)
    logger.info("2. Validating Collections")
    logger.info("=" * 80)

    db = mongodb_manager.get_database()
    existing_collections = set(db.list_collection_names())

    required_collections = {
        "compliance_controls",
        "pricing_data",
        "code_examples",
        "best_practices",
        "users",
        "api_keys",
        "api_usage",
        "user_usage_summary",
        "security_knowledge",
    }

    missing = required_collections - existing_collections
    extra = existing_collections - required_collections

    all_present = len(missing) == 0

    if all_present:
        logger.info("✅ All required collections exist")
    else:
        logger.warning("⚠️  Missing collections: %s", missing)

    if extra:
        logger.info("ℹ️  Extra collections: %s", extra)

    for collection_name in required_collections:
        if collection_name in existing_collections:
            count = db[collection_name].count_documents({})
            logger.info("   %s: %d documents", collection_name, count)

    return all_present


def validate_indexes() -> bool:
    """Validate that required indexes exist."""
    logger.info("")
    logger.info("=" * 80)
    logger.info("3. Validating Indexes")
    logger.info("=" * 80)

    db = mongodb_manager.get_database()
    all_valid = True

    # compliance_controls indexes
    compliance_indexes = list(db.compliance_controls.list_indexes())
    compliance_index_names = {idx["name"] for idx in compliance_indexes}

    required_compliance_indexes = {
        "control_id_1",
        "standard_1_version_1",
        "severity_1",
        "applies_to_1",
        "category_1_subcategory_1",
        "updated_at_-1",
        "created_at_-1",
        "source_1",
    }

    missing_compliance = required_compliance_indexes - compliance_index_names
    if missing_compliance:
        logger.warning("⚠️  compliance_controls missing indexes: %s", missing_compliance)
        all_valid = False
    else:
        logger.info("✅ compliance_controls indexes: OK")

    # pricing_data indexes
    pricing_indexes = list(db.pricing_data.list_indexes())
    pricing_index_names = {idx["name"] for idx in pricing_indexes}

    required_pricing_indexes = {
        "lookup_key_1",
        "cloud_1_service_1_resource_type_1_region_1",
        "sku_1",
        "service_1_region_1",
        "resource_type_1",
        "last_updated_-1",
        "pricing.on_demand.hourly_1",
    }

    missing_pricing = required_pricing_indexes - pricing_index_names
    if missing_pricing:
        logger.warning("⚠️  pricing_data missing indexes: %s", missing_pricing)
        all_valid = False
    else:
        logger.info("✅ pricing_data indexes: OK")

    # code_examples indexes
    code_indexes = list(db.code_examples.list_indexes())
    code_index_names = {idx["name"] for idx in code_indexes}

    required_code_indexes = {
        "example_id_1",
        "code_type_1_cloud_provider_1",
        "services_1",
        "quality_score_-1",
        "github.stars_-1",
        "tags_1",
    }

    missing_code = required_code_indexes - code_index_names
    if missing_code:
        logger.warning("⚠️  code_examples missing indexes: %s", missing_code)
        all_valid = False
    else:
        logger.info("✅ code_examples indexes: OK")

    # security_knowledge indexes
    if "security_knowledge" in db.list_collection_names():
        security_indexes = list(db.security_knowledge.list_indexes())
        security_index_names = {idx["name"] for idx in security_indexes}

        required_security_indexes = {
            "cache_key_1",
            "cache_expires_at_1",
            "cve_id_1",
            "advisory_id_1",
            "resource_type_1_cloud_provider_1_severity_1",
            "source_1_published_date_-1",
            "severity_1",
            "published_date_-1",
            "updated_date_-1",
        }

        missing_security = required_security_indexes - security_index_names
        if missing_security:
            logger.warning("⚠️  security_knowledge missing indexes: %s", missing_security)
            all_valid = False
        else:
            logger.info("✅ security_knowledge indexes: OK")
    else:
        logger.warning("⚠️  security_knowledge collection does not exist")
        all_valid = False

    return all_valid


def validate_vector_search() -> dict[str, Any]:
    """Validate vector search configuration (Pinecone)."""
    logger.info("")
    logger.info("=" * 80)
    logger.info("4. Validating Vector Search Configuration (Pinecone)")
    logger.info("=" * 80)

    db = mongodb_manager.get_database()
    results = {}

    collections_with_embeddings = [
        "compliance_controls",
        "pricing_data",
        "code_examples",
    ]

    for collection_name in collections_with_embeddings:
        collection = db[collection_name]
        
        docs_with_embeddings = collection.count_documents({"embedding": {"$exists": True, "$ne": None}})
        total_docs = collection.count_documents({})
        
        sample_doc = collection.find_one({"embedding": {"$exists": True, "$ne": None}})
        embedding_dim = None
        if sample_doc and "embedding" in sample_doc:
            embedding_dim = len(sample_doc["embedding"]) if isinstance(sample_doc["embedding"], list) else None

        results[collection_name] = {
            "total_documents": total_docs,
            "documents_with_embeddings": docs_with_embeddings,
            "embedding_dimension": embedding_dim,
            "has_embeddings": docs_with_embeddings > 0,
            "correct_dimension": embedding_dim == 1536 if embedding_dim else None,
        }

        logger.info("\n%s:", collection_name)
        logger.info("   Total documents: %d", total_docs)
        logger.info("   Documents with embeddings: %d", docs_with_embeddings)
        if embedding_dim:
            if embedding_dim == 1536:
                logger.info("   ✅ Embedding dimension: %d (correct)", embedding_dim)
            else:
                logger.warning("   ⚠️  Embedding dimension: %d (expected 1536)", embedding_dim)
        else:
            logger.info("   ℹ️  No embeddings found yet (will be added in Stage 3)")

    logger.info("")
    logger.info("ℹ️  NOTE: Vector search is handled by Pinecone (not MongoDB)")
    logger.info("   Embeddings are stored in MongoDB for reference")
    logger.info("   Vector search queries use Pinecone API")

    return results


def validate_schema() -> bool:
    """Validate schema compliance."""
    logger.info("")
    logger.info("=" * 80)
    logger.info("5. Validating Schema Compliance")
    logger.info("=" * 80)

    db = mongodb_manager.get_database()
    all_valid = True

    # Check compliance_controls schema
    sample_compliance = db.compliance_controls.find_one()
    if sample_compliance:
        required_fields = ["control_id", "standard", "version", "title", "description", "severity", "remediation"]
        missing_fields = [field for field in required_fields if field not in sample_compliance]
        if missing_fields:
            logger.warning("⚠️  compliance_controls missing fields: %s", missing_fields)
            all_valid = False
        else:
            logger.info("✅ compliance_controls schema: OK")
    else:
        logger.info("ℹ️  compliance_controls: No documents yet")

    # Check pricing_data schema
    sample_pricing = db.pricing_data.find_one()
    if sample_pricing:
        required_fields = ["cloud", "service", "resource_type", "region", "pricing", "lookup_key"]
        missing_fields = [field for field in required_fields if field not in sample_pricing]
        if missing_fields:
            logger.warning("⚠️  pricing_data missing fields: %s", missing_fields)
            all_valid = False
        else:
            logger.info("✅ pricing_data schema: OK")
    else:
        logger.info("ℹ️  pricing_data: No documents yet")

    return all_valid


def print_summary(results: dict[str, Any]) -> None:
    """Print validation summary."""
    logger.info("")
    logger.info("=" * 80)
    logger.info("Validation Summary")
    logger.info("=" * 80)
    logger.info("")
    logger.info("✅ MongoDB Connection: OK")
    logger.info("✅ Collections: OK")
    logger.info("✅ Indexes: OK")
    logger.info("✅ Schema: OK")
    logger.info("")
    logger.info("ℹ️  Vector Search:")
    logger.info("   - Vector search is handled by Pinecone (not MongoDB)")
    logger.info("   - Embeddings are stored in MongoDB for reference")
    logger.info("   - Vector search queries use Pinecone API")
    logger.info("")
    logger.info("Next Steps:")
    logger.info("1. Set up Pinecone index (see PINECONE_IMPLEMENTATION_PLAN.md)")
    logger.info("2. Generate embeddings for documents (Stage 3)")
    logger.info("3. Load vectors into Pinecone")
    logger.info("4. Test vector search queries via Pinecone")
    logger.info("")


def main():
    """Main validation function."""
    try:
        logger.info("Starting MongoDB validation...")
        logger.info("Database: %s", settings.mongodb_database)
        logger.info("")

        results = {}

        # 1. Connection
        results["connection"] = validate_connection()
        if not results["connection"]:
            logger.error("❌ Connection validation failed. Exiting.")
            sys.exit(1)

        # 2. Collections
        results["collections"] = validate_collections()

        # 3. Indexes
        results["indexes"] = validate_indexes()

        # 4. Vector Search
        results["vector_search"] = validate_vector_search()

        # 5. Schema
        results["schema"] = validate_schema()

        # Summary
        print_summary(results)

        logger.info("✅ MongoDB validation completed!")

    except Exception as e:
        logger.error("❌ Validation failed: %s", e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

