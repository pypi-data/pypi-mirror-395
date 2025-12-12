"""Setup script for MongoDB collections and indexes."""

import logging
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from api.database.mongodb import mongodb_manager
from api.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_collections():
    """Create all collections if they don't exist."""
    db = mongodb_manager.get_database()

    collections = [
        "compliance_controls",
        "pricing_data",
        "code_examples",
        "best_practices",
        "knowledge_articles",
        "users",
        "api_keys",
        "api_usage",
        "user_usage_summary",
        "security_knowledge",
        "template_registry",
        "template_ratings",
        "template_analytics",
        "troubleshooting_incidents",
        "solution_knowledge",
        "quality_templates",
        "pipeline_jobs",
        "packages",
        "indexed_resources",
        "indexed_files",
        "architecture_design_cache",
        "user_knowledge_chunks",
        "user_research_sessions",
    ]

    logger.info("Creating collections...")
    for collection_name in collections:
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            logger.info("Created collection: %s", collection_name)
        else:
            logger.info("Collection already exists: %s", collection_name)


def create_indexes():
    """Create all indexes for collections."""
    db = mongodb_manager.get_database()

    logger.info("Creating indexes...")

    # compliance_controls indexes
    compliance_collection = db.compliance_controls
    compliance_collection.create_index([("control_id", 1)], unique=True)
    compliance_collection.create_index([("standard", 1), ("version", 1)])
    compliance_collection.create_index([("severity", 1)])
    compliance_collection.create_index([("applies_to", 1)])
    compliance_collection.create_index([("category", 1), ("subcategory", 1)])
    compliance_collection.create_index([("updated_at", -1)])
    compliance_collection.create_index([("created_at", -1)])
    compliance_collection.create_index([("source", 1)])
    logger.info("Created compliance_controls indexes")

    # pricing_data indexes
    pricing_collection = db.pricing_data
    pricing_collection.create_index([("lookup_key", 1)], unique=True)
    pricing_collection.create_index([("cloud", 1), ("service", 1), ("resource_type", 1), ("region", 1)])
    pricing_collection.create_index([("sku", 1)])
    pricing_collection.create_index([("service", 1), ("region", 1)])
    pricing_collection.create_index([("resource_type", 1)])
    pricing_collection.create_index([("last_updated", -1)])
    pricing_collection.create_index([("pricing.on_demand.hourly", 1)])
    # Partial index for available pricing only
    pricing_collection.create_index(
        [("lookup_key", 1)],
        partialFilterExpression={"availability.available": True},
    )
    logger.info("Created pricing_data indexes")

    # code_examples indexes
    code_collection = db.code_examples
    code_collection.create_index([("example_id", 1)], unique=True)
    code_collection.create_index([("code_type", 1), ("cloud_provider", 1)])
    code_collection.create_index([("services", 1)])
    code_collection.create_index([("quality_score", -1)])
    code_collection.create_index([("github.stars", -1)])
    code_collection.create_index([("tags", 1)])
    logger.info("Created code_examples indexes")

    # users indexes
    users_collection = db.users
    users_collection.create_index([("email", 1)], unique=True)
    users_collection.create_index([("stripe_customer_id", 1)], unique=True, sparse=True)
    users_collection.create_index([("organization_id", 1)])
    users_collection.create_index([("created_at", -1)])
    users_collection.create_index([("plan", 1), ("status", 1)])
    users_collection.create_index([("profile_completed", 1)])
    users_collection.create_index([("organization_name", 1)])
    users_collection.create_index([("referral_source", 1)])
    users_collection.create_index([("role", 1)])
    users_collection.create_index([("profile_completed", 1), ("created_at", -1)])
    logger.info("Created users indexes")

    # api_keys indexes
    api_keys_collection = db.api_keys
    api_keys_collection.create_index([("key_hash", 1), ("is_active", 1)], unique=True)
    api_keys_collection.create_index([("user_id", 1), ("is_active", 1)])
    api_keys_collection.create_index([("organization_id", 1)])
    api_keys_collection.create_index([("last_used_at", -1)])
    api_keys_collection.create_index([("expires_at", 1)], sparse=True)
    api_keys_collection.create_index([("created_at", -1)])
    logger.info("Created api_keys indexes")

    # api_usage indexes
    api_usage_collection = db.api_usage
    api_usage_collection.create_index([("request_id", 1)], unique=True)
    api_usage_collection.create_index([("user_id", 1), ("timestamp", -1)])
    api_usage_collection.create_index([("api_key_id", 1), ("timestamp", -1)])
    api_usage_collection.create_index([("date", -1), ("user_id", 1)])
    api_usage_collection.create_index([("timestamp", -1)])
    api_usage_collection.create_index([("date", 1), ("endpoint", 1)])
    # Compound index for common queries
    api_usage_collection.create_index([("user_id", 1), ("date", -1), ("timestamp", -1)])
    # TTL index for automatic deletion after 90 days
    api_usage_collection.create_index([("ttl", 1)], expireAfterSeconds=0)
    logger.info("Created api_usage indexes")

    # user_usage_summary indexes
    usage_summary_collection = db.user_usage_summary
    usage_summary_collection.create_index([("user_id", 1), ("period", 1)], unique=True)
    usage_summary_collection.create_index([("period", 1)])
    usage_summary_collection.create_index([("limits.overage", 1)])
    usage_summary_collection.create_index([("updated_at", -1)])
    logger.info("Created user_usage_summary indexes")

    # knowledge_articles indexes
    knowledge_collection = db.knowledge_articles
    knowledge_collection.create_index([("article_id", 1)], unique=True)
    knowledge_collection.create_index([("domain", 1), ("subdomain", 1)])
    knowledge_collection.create_index([("content_type", 1)])
    knowledge_collection.create_index([("industries", 1)])
    knowledge_collection.create_index([("cloud_providers", 1)])
    knowledge_collection.create_index([("services", 1)])
    knowledge_collection.create_index([("related_controls", 1)])
    knowledge_collection.create_index([("related_articles", 1)])
    knowledge_collection.create_index([("tags", 1)])
    knowledge_collection.create_index([("quality_score", -1)])
    knowledge_collection.create_index([("updated_at", -1)])
    knowledge_collection.create_index([("created_at", -1)])
    # Text search index
    knowledge_collection.create_index([
        ("title", "text"),
        ("summary", "text"),
        ("content", "text"),
    ])
    logger.info("Created knowledge_articles indexes")

    # security_knowledge indexes
    security_collection = db.security_knowledge
    security_collection.create_index([("cache_key", 1)], unique=True)
    security_collection.create_index([("cache_expires_at", 1)], expireAfterSeconds=0)
    security_collection.create_index([("cve_id", 1)], unique=True, sparse=True)
    security_collection.create_index([("advisory_id", 1)], unique=True, sparse=True)
    security_collection.create_index([("resource_type", 1), ("cloud_provider", 1), ("severity", 1)])
    security_collection.create_index([("source", 1), ("published_date", -1)])
    security_collection.create_index([("severity", 1)])
    security_collection.create_index([("published_date", -1)])
    security_collection.create_index([("updated_date", -1)])
    logger.info("Created security_knowledge indexes")

    # template_registry indexes
    template_collection = db.template_registry
    template_collection.create_index([("template_id", 1), ("version", 1)], unique=True)
    template_collection.create_index([("template_id", 1), ("is_latest", 1)], partialFilterExpression={"is_latest": True})
    template_collection.create_index([("project_type", 1), ("cloud_provider", 1), ("architecture_type", 1)])
    template_collection.create_index([("tags", 1)])
    template_collection.create_index([("usage_count", -1)])
    template_collection.create_index([("visibility", 1), ("user_id", 1), ("organization_id", 1)])
    template_collection.create_index([("source_type", 1)])
    template_collection.create_index({
        "name": "text",
        "description": "text",
        "tags": "text"
    })
    logger.info("Created template_registry indexes")

    # template_ratings indexes
    rating_collection = db.template_ratings
    rating_collection.create_index([("rating_id", 1)], unique=True)
    rating_collection.create_index([("template_id", 1), ("created_at", -1)])
    rating_collection.create_index([("user_id", 1), ("template_id", 1)])
    rating_collection.create_index([("rating", 1)])
    logger.info("Created template_ratings indexes")

    # template_analytics indexes
    analytics_collection = db.template_analytics
    analytics_collection.create_index([("template_id", 1)], unique=True)
    analytics_collection.create_index([("average_rating", -1)])
    analytics_collection.create_index([("usage_count", -1)])
    analytics_collection.create_index([("total_ratings", -1)])
    logger.info("Created template_analytics indexes")

    # troubleshooting_incidents indexes
    incidents_collection = db.troubleshooting_incidents
    incidents_collection.create_index([("incident_id", 1)], unique=True)
    incidents_collection.create_index([("status", 1), ("user_id", 1), ("created_at", -1)])
    incidents_collection.create_index({
        "issue_description": "text",
        "error_patterns": "text",
        "root_cause": "text"
    })
    incidents_collection.create_index([("infrastructure_type", 1), ("cloud_provider", 1), ("resource_type", 1)])
    incidents_collection.create_index([("user_id", 1), ("status", 1), ("resolved_at", 1)])
    incidents_collection.create_index([("created_at", -1)])
    incidents_collection.create_index([("resolved_at", -1)])
    incidents_collection.create_index([("severity", 1)])
    logger.info("Created troubleshooting_incidents indexes")

    # solution_knowledge indexes
    solutions_collection = db.solution_knowledge
    solutions_collection.create_index([("solution_id", 1)], unique=True)
    solutions_collection.create_index([("problem_pattern", 1)], unique=True, sparse=True)
    solutions_collection.create_index([("infrastructure_type", 1), ("cloud_provider", 1), ("resource_type", 1)])
    solutions_collection.create_index([("quality_score", -1), ("success_rate", -1)])
    solutions_collection.create_index([("verified", 1), ("success_rate", -1)], partialFilterExpression={"verified": True})
    solutions_collection.create_index({
        "problem_summary": "text",
        "solution_description": "text",
        "root_cause": "text"
    })
    solutions_collection.create_index([("tags", 1)])
    solutions_collection.create_index([("success_rate", -1)])
    logger.info("Created solution_knowledge indexes")

    # report_templates indexes
    report_templates_collection = db.report_templates
    report_templates_collection.create_index([("template_id", 1), ("version", 1)], unique=True)
    report_templates_collection.create_index([("template_id", 1), ("is_latest", 1)], partialFilterExpression={"is_latest": True})
    report_templates_collection.create_index([("document_type", 1), ("compliance_standards", 1)])
    report_templates_collection.create_index([("document_type", 1), ("resource_types", 1)])
    report_templates_collection.create_index([("template_engine", 1)])
    report_templates_collection.create_index([("visibility", 1), ("user_id", 1), ("organization_id", 1)])
    report_templates_collection.create_index([("usage_count", -1)])
    report_templates_collection.create_index({
        "name": "text",
        "description": "text",
        "tags": "text"
    })
    logger.info("Created report_templates indexes")

    # reports indexes
    reports_collection = db.reports
    reports_collection.create_index([("report_id", 1)], unique=True)
    reports_collection.create_index([("user_id", 1), ("created_at", -1)])
    reports_collection.create_index([("document_type", 1), ("created_at", -1)])
    reports_collection.create_index([("format", 1)])
    logger.info("Created reports indexes")

    # quality_templates indexes
    quality_templates_collection = db.quality_templates
    quality_templates_collection.create_index([("template_id", 1)], unique=True)
    quality_templates_collection.create_index([("type", 1)])
    quality_templates_collection.create_index([("quality_score", -1)])
    quality_templates_collection.create_index([("tags", 1)])
    quality_templates_collection.create_index([("categories", 1)])
    quality_templates_collection.create_index([("visibility", 1)])
    quality_templates_collection.create_index([("user_id", 1)])
    quality_templates_collection.create_index([("organization_id", 1)])
    quality_templates_collection.create_index([("type", 1), ("quality_score", -1), ("tags", 1)])
    quality_templates_collection.create_index([("visibility", 1), ("user_id", 1), ("organization_id", 1)])
    quality_templates_collection.create_index([("created_at", -1)])
    quality_templates_collection.create_index([("last_used_at", -1)])
    logger.info("Created quality_templates indexes")

    # pipeline_jobs indexes
    pipeline_jobs_collection = db.pipeline_jobs
    pipeline_jobs_collection.create_index([("pipeline_id", 1)], unique=True)
    pipeline_jobs_collection.create_index([("status", 1), ("created_at", -1)])
    pipeline_jobs_collection.create_index([("pipeline_type", 1), ("status", 1)])
    pipeline_jobs_collection.create_index([("user_id", 1), ("created_at", -1)])
    pipeline_jobs_collection.create_index([("created_at", -1)])
    pipeline_jobs_collection.create_index([("priority", -1), ("created_at", 1)])
    logger.info("Created pipeline_jobs indexes")

    # pipeline_config indexes
    pipeline_config_collection = db.pipeline_config
    pipeline_config_collection.create_index([("_id", 1)], unique=True)
    logger.info("Created pipeline_config indexes")

    # packages indexes
    packages_collection = db.packages
    packages_collection.create_index([("package_id", 1)], unique=True)
    packages_collection.create_index([("registry", 1), ("name", 1)])
    packages_collection.create_index([("domain_tags", 1)])
    packages_collection.create_index([("category", 1)])
    packages_collection.create_index([("health_score", -1)])
    packages_collection.create_index([("relevance_score", -1)])
    packages_collection.create_index([("indexed_at", -1)])
    packages_collection.create_index([("downloads", -1)])
    packages_collection.create_index([("stars", -1)])
    packages_collection.create_index({
        "name": "text",
        "description": "text",
        "keywords": "text",
        "searchable_text": "text",
    })
    logger.info("Created packages indexes")

    logger.info("All indexes created successfully!")


def verify_setup():
    """Verify that collections and indexes are set up correctly."""
    db = mongodb_manager.get_database()

    logger.info("Verifying setup...")

    # Check collections
    collections = db.list_collection_names()
    expected_collections = [
        "compliance_controls",
        "pricing_data",
        "code_examples",
        "best_practices",
        "knowledge_articles",
        "users",
        "api_keys",
        "api_usage",
        "user_usage_summary",
        "security_knowledge",
        "template_registry",
        "template_ratings",
        "template_analytics",
        "troubleshooting_incidents",
        "solution_knowledge",
        "report_templates",
        "reports",
        "quality_templates",
        "pipeline_jobs",
        "pipeline_config",
        "packages",
        "indexed_resources",
        "indexed_files",
        "architecture_design_cache",
    ]

    missing_collections = set(expected_collections) - set(collections)
    if missing_collections:
        logger.warning("Missing collections: %s", missing_collections)
    else:
        logger.info("All collections exist")

    # Check indexes (sample check)
    compliance_indexes = db.compliance_controls.list_indexes()
    index_names = [idx["name"] for idx in compliance_indexes]
    logger.info("compliance_controls indexes: %s", index_names)

    logger.info("Setup verification complete")


def main():
    """Main setup function."""
    try:
        logger.info("Starting MongoDB setup...")
        logger.info("Database: %s", settings.mongodb_database)

        # Connect to MongoDB
        mongodb_manager.connect()

        # Create collections
        create_collections()

        # Create indexes
        create_indexes()

        # Verify setup
        verify_setup()

        logger.info("MongoDB setup completed successfully!")

    except Exception as e:
        logger.error("MongoDB setup failed: %s", e, exc_info=True)
        sys.exit(1)
    finally:
        # Don't close connection - keep it alive
        pass


if __name__ == "__main__":
    main()

