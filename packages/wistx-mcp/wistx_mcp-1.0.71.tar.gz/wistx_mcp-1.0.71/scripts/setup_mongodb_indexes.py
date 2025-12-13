"""Setup MongoDB indexes for optimal query performance."""

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from api.database.mongodb import mongodb_manager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def setup_indexes():
    """Create all recommended indexes for optimal query performance."""
    logger.info("Connecting to MongoDB...")
    mongodb_manager.connect()
    db = mongodb_manager.get_database()

    logger.info("Creating indexes...")

    try:
        logger.info("Creating indexes for compliance_controls collection...")
        db.compliance_controls.create_index(
            [("control_id", 1)], unique=True, name="control_id_unique", background=True
        )
        db.compliance_controls.create_index(
            [("standard", 1), ("version", 1)], name="standard_version", background=True
        )
        db.compliance_controls.create_index(
            [("source_hash", 1)], name="source_hash", background=True
        )
        db.compliance_controls.create_index(
            [("content_hash", 1)], name="content_hash", background=True
        )
        db.compliance_controls.create_index(
            [("control_id", 1), ("source_hash", 1), ("content_hash", 1)],
            name="control_id_hashes",
            background=True,
        )
        logger.info("✅ Created indexes for compliance_controls")

        logger.info("Creating indexes for pricing_data collection...")
        db.pricing_data.create_index(
            [("lookup_key", 1)], unique=True, name="lookup_key_unique", background=True
        )
        db.pricing_data.create_index(
            [("cloud", 1), ("service", 1)], name="cloud_service", background=True
        )
        db.pricing_data.create_index(
            [("region", 1)], name="region", background=True
        )
        logger.info("✅ Created indexes for pricing_data")

        logger.info("Creating indexes for code_examples collection...")
        db.code_examples.create_index(
            [("example_id", 1)], unique=True, name="example_id_unique", background=True
        )
        db.code_examples.create_index(
            [("cloud_provider", 1)], name="cloud_provider", background=True
        )
        db.code_examples.create_index(
            [("code_type", 1)], name="code_type", background=True
        )
        logger.info("✅ Created indexes for code_examples")

        logger.info("Creating indexes for best_practices collection...")
        db.best_practices.create_index(
            [("practice_id", 1)], unique=True, name="practice_id_unique", background=True
        )
        db.best_practices.create_index(
            [("category", 1)], name="category", background=True
        )
        logger.info("✅ Created indexes for best_practices")

        logger.info("Creating indexes for knowledge_articles collection...")
        db.knowledge_articles.create_index(
            [("article_id", 1)], unique=True, name="article_id_unique", background=True
        )
        db.knowledge_articles.create_index(
            [("domain", 1), ("subdomain", 1)], name="domain_subdomain", background=True
        )
        db.knowledge_articles.create_index(
            [("content_type", 1)], name="content_type", background=True
        )
        db.knowledge_articles.create_index(
            [("user_id", 1), ("organization_id", 1)], name="user_org", background=True
        )
        logger.info("✅ Created indexes for knowledge_articles")

        logger.info("Creating indexes for cost_data_focus collection...")
        db.cost_data_focus.create_index(
            [("lookup_key", 1)], unique=True, name="lookup_key_unique", background=True
        )
        db.cost_data_focus.create_index(
            [("billing_account_id", 1), ("billing_period_start", -1)],
            name="billing_account_period",
            background=True,
        )
        db.cost_data_focus.create_index(
            [("provider", 1), ("region_id", 1)], name="provider_region", background=True
        )
        db.cost_data_focus.create_index(
            [("service_category", 1), ("service_name", 1)], name="service_category_name", background=True
        )
        db.cost_data_focus.create_index(
            [("resource_type", 1), ("resource_id", 1)], name="resource_type_id", background=True
        )
        db.cost_data_focus.create_index(
            [("sku_id", 1)], name="sku_id", background=True
        )
        db.cost_data_focus.create_index(
            [("pricing_category", 1)], name="pricing_category", background=True
        )
        db.cost_data_focus.create_index(
            [("source_hash", 1)], name="source_hash", background=True
        )
        db.cost_data_focus.create_index(
            [("last_updated", -1)], name="last_updated", background=True
        )
        db.cost_data_focus.create_index(
            [("tags.BusinessUnit", 1), ("tags.Project", 1)], name="allocation_tags", background=True
        )
        logger.info("✅ Created indexes for cost_data_focus")

        logger.info("Creating indexes for infrastructure_budgets collection...")
        db.infrastructure_budgets.create_index(
            [("user_id", 1), ("status", 1)], name="user_status", background=True
        )
        db.infrastructure_budgets.create_index(
            [("scope.type", 1), ("scope.cloud_provider", 1), ("scope.environment_name", 1)],
            name="scope_lookup",
            background=True,
        )
        db.infrastructure_budgets.create_index(
            [("_id", 1), ("user_id", 1)], name="budget_user", background=True
        )
        logger.info("✅ Created indexes for infrastructure_budgets")

        logger.info("Creating indexes for infrastructure_spending collection...")
        db.infrastructure_spending.create_index(
            [("budget_id", 1), ("period", 1)], name="budget_period", background=True
        )
        db.infrastructure_spending.create_index(
            [("user_id", 1), ("period", 1)], name="user_period", background=True
        )
        db.infrastructure_spending.create_index(
            [("date", -1)], name="date_desc", background=True
        )
        db.infrastructure_spending.create_index(
            [("source_type", 1), ("source_id", 1), ("period", 1)],
            name="deduplication_key",
            background=True,
        )
        logger.info("✅ Created indexes for infrastructure_spending")

        logger.info("Creating indexes for budget_status collection...")
        db.budget_status.create_index(
            [("budget_id", 1), ("period", 1)],
            unique=True,
            name="budget_period_unique",
            background=True,
        )
        db.budget_status.create_index(
            [("user_id", 1), ("period", 1)], name="user_period_status", background=True
        )
        logger.info("✅ Created indexes for budget_status")

        logger.info("Creating compound index for cost_data_focus pricing queries...")
        db.cost_data_focus.create_index(
            [
                ("provider", 1),
                ("service_name", 1),
                ("resource_type", 1),
                ("region_id", 1),
                ("pricing_category", 1),
                ("last_updated", -1),
            ],
            name="pricing_lookup_compound",
            background=True,
        )
        logger.info("✅ Created compound index for pricing queries")

        logger.info("Creating indexes for organizations collection...")
        db.organizations.create_index("slug", unique=True, name="slug_unique", background=True)
        db.organizations.create_index(
            "stripe_customer_id", unique=True, sparse=True, name="stripe_customer_id_unique", background=True
        )
        db.organizations.create_index("created_by", name="created_by", background=True)
        db.organizations.create_index("status", name="status", background=True)
        db.organizations.create_index(
            [("plan_id", 1), ("status", 1)], name="plan_status", background=True
        )
        logger.info("✅ Created indexes for organizations")

        logger.info("Creating indexes for organization_members collection...")
        db.organization_members.create_index(
            [("organization_id", 1), ("user_id", 1)],
            unique=True,
            name="org_user_unique",
            background=True,
        )
        db.organization_members.create_index("user_id", name="user_id", background=True)
        db.organization_members.create_index("organization_id", name="organization_id", background=True)
        db.organization_members.create_index("status", name="status", background=True)
        db.organization_members.create_index(
            [("organization_id", 1), ("status", 1), ("role", 1)],
            name="org_status_role",
            background=True,
        )
        db.organization_members.create_index(
            [("organization_id", 1), ("user_id", 1)],
            partialFilterExpression={"status": "active"},
            name="org_user_active",
            background=True,
        )
        logger.info("✅ Created indexes for organization_members")

        logger.info("Creating indexes for organization_invitations collection...")
        db.organization_invitations.create_index("token", unique=True, name="token_unique", background=True)
        db.organization_invitations.create_index("organization_id", name="organization_id", background=True)
        db.organization_invitations.create_index("email", name="email", background=True)
        db.organization_invitations.create_index(
            [("organization_id", 1), ("email", 1), ("status", 1)],
            name="org_email_status",
            background=True,
        )
        logger.info("✅ Created indexes for organization_invitations")

        logger.info("Creating indexes for indexed_files collection...")
        db.indexed_files.create_index(
            [
                ("resource_id", 1),
                ("file_path", 1),
                ("commit_sha", 1),
            ],
            unique=True,
            name="unique_file_per_commit",
            background=True,
        )
        db.indexed_files.create_index(
            [("resource_id", 1), ("status", 1)],
            name="resource_status",
            background=True,
        )
        db.indexed_files.create_index(
            [("resource_id", 1), ("processed_at", -1)],
            name="resource_processed",
            background=True,
        )
        logger.info("✅ Created indexes for indexed_files")

        logger.info("Creating indexes for architecture_design_cache collection...")
        db.architecture_design_cache.create_index(
            [("_id", 1)], unique=True, name="cache_key_unique", background=True
        )
        db.architecture_design_cache.create_index(
            [("user_id", 1), ("_id", 1)], name="user_cache_key", background=True
        )
        db.architecture_design_cache.create_index(
            [("user_id", 1), ("action", 1), ("project_type", 1)], name="user_action_project", background=True
        )
        db.architecture_design_cache.create_index(
            [("expires_at", 1)], name="expires_at", background=True
        )
        db.architecture_design_cache.create_index(
            [("last_accessed_at", -1)], name="last_accessed_desc", background=True
        )
        db.architecture_design_cache.create_index(
            [("created_at", -1)], name="created_at_desc", background=True
        )
        logger.info("✅ Created indexes for architecture_design_cache")

        logger.info("Creating indexes for documentation_sections collection...")
        db.documentation_sections.create_index(
            [("section_id", 1)], unique=True, name="section_id_unique", background=True
        )
        db.documentation_sections.create_index(
            [("resource_id", 1), ("user_id", 1)], name="resource_user", background=True
        )
        db.documentation_sections.create_index(
            [("section_type", 1)], name="section_type", background=True
        )
        db.documentation_sections.create_index(
            [("parent_section_id", 1)], name="parent_section", background=True
        )
        logger.info("✅ Created indexes for documentation_sections")

        logger.info("Creating indexes for github_webhook_events collection...")
        db.github_webhook_events.create_index(
            [("delivery_id", 1)], unique=True, name="delivery_id_unique", background=True
        )
        db.github_webhook_events.create_index(
            [("repository_url", 1), ("processed_at", -1)], name="repo_rate_limit", background=True
        )
        db.github_webhook_events.create_index(
            [("expires_at", 1)], expireAfterSeconds=0, name="expires_ttl", background=True
        )
        db.github_webhook_events.create_index(
            [("status", 1), ("processed_at", -1)], name="status_processed", background=True
        )
        logger.info("✅ Created indexes for github_webhook_events")

        logger.info("Creating indexes for github_webhook_dead_letter_queue collection...")
        db.github_webhook_dead_letter_queue.create_index(
            [("delivery_id", 1)], unique=True, name="dlq_delivery_id_unique", background=True
        )
        db.github_webhook_dead_letter_queue.create_index(
            [("status", 1), ("failed_at", 1)], name="dlq_status_failed_at", background=True
        )
        logger.info("✅ Created indexes for github_webhook_dead_letter_queue")

        logger.info("Creating indexes for user_knowledge_chunks collection...")
        db.user_knowledge_chunks.create_index(
            [("user_id", 1), ("research_session_id", 1)],
            name="user_session",
            background=True,
        )
        db.user_knowledge_chunks.create_index(
            [("user_id", 1), ("source_url", 1)],
            name="user_source",
            background=True,
        )
        db.user_knowledge_chunks.create_index(
            [("chunk_id", 1), ("user_id", 1)],
            unique=True,
            name="chunk_user_unique",
            background=True,
        )
        db.user_knowledge_chunks.create_index(
            [("user_id", 1), ("created_at", -1)],
            name="user_created_desc",
            background=True,
        )
        logger.info("✅ Created indexes for user_knowledge_chunks")

        logger.info("Creating indexes for user_research_sessions collection...")
        db.user_research_sessions.create_index(
            [("user_id", 1), ("created_at", -1)],
            name="user_created_desc",
            background=True,
        )
        db.user_research_sessions.create_index(
            [("session_id", 1), ("user_id", 1)],
            unique=True,
            name="session_user_unique",
            background=True,
        )
        db.user_research_sessions.create_index(
            [("user_id", 1), ("status", 1)],
            name="user_status",
            background=True,
        )
        logger.info("✅ Created indexes for user_research_sessions")

        logger.info("=" * 80)
        logger.info("✅ All indexes created successfully!")
        logger.info("=" * 80)

        logger.info("Index creation is running in background. Check status with:")
        logger.info("  db.compliance_controls.getIndexes()")

    except Exception as e:
        logger.error("Error creating indexes: %s", e, exc_info=True)
        raise
    finally:
        mongodb_manager.close()


if __name__ == "__main__":
    setup_indexes()

