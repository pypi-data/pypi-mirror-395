"""Bulk migration script for user plans.

This script migrates users from legacy plans (pro, builder, architect) to new plans
(professional, team, enterprise).

Usage:
    python scripts/migrate_user_plans.py --dry-run  # Preview changes
    python scripts/migrate_user_plans.py --execute   # Apply changes
    python scripts/migrate_user_plans.py --plan pro --execute  # Migrate only pro users
"""

import argparse
import logging
import sys
from datetime import datetime
from typing import Any

from api.database.mongodb import mongodb_manager
from api.services.plan_service import plan_service

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

MIGRATION_MAPPINGS = {
    "pro": "professional",
    "builder": "team",
    "architect": "enterprise",
}


def get_users_to_migrate(plan_filter: str | None = None) -> list[dict[str, Any]]:
    """Get users that need migration.

    Args:
        plan_filter: Optional plan ID to filter by (pro, builder, architect)

    Returns:
        List of users to migrate
    """
    db = mongodb_manager.get_database()
    query: dict[str, Any] = {"plan": {"$in": list(MIGRATION_MAPPINGS.keys())}}

    if plan_filter:
        if plan_filter not in MIGRATION_MAPPINGS:
            raise ValueError(f"Invalid plan filter: {plan_filter}. Must be one of {list(MIGRATION_MAPPINGS.keys())}")
        query["plan"] = plan_filter

    users = list(db.users.find(query))
    logger.info("Found %d users to migrate", len(users))
    return users


def migrate_user(user: dict[str, Any], dry_run: bool = True) -> dict[str, Any]:
    """Migrate a single user's plan.

    Args:
        user: User document
        dry_run: If True, don't actually update the database

    Returns:
        Migration result
    """
    current_plan = user.get("plan", "professional")
    if current_plan not in MIGRATION_MAPPINGS:
        return {
            "user_id": str(user["_id"]),
            "email": user.get("email", "unknown"),
            "status": "skipped",
            "reason": f"Plan {current_plan} not in migration mappings",
        }

    target_plan = MIGRATION_MAPPINGS[current_plan]
    target_plan_obj = plan_service.get_plan(target_plan)

    if not target_plan_obj:
        return {
            "user_id": str(user["_id"]),
            "email": user.get("email", "unknown"),
            "status": "error",
            "reason": f"Target plan {target_plan} not found",
        }

    if not target_plan_obj.is_active:
        return {
            "user_id": str(user["_id"]),
            "email": user.get("email", "unknown"),
            "status": "error",
            "reason": f"Target plan {target_plan} is not active",
        }

    subscription_id = user.get("stripe_subscription_id")
    if subscription_id:
        return {
            "user_id": str(user["_id"]),
            "email": user.get("email", "unknown"),
            "status": "skipped",
            "reason": f"User has active Stripe subscription {subscription_id}. Manual migration required.",
        }

    if dry_run:
        return {
            "user_id": str(user["_id"]),
            "email": user.get("email", "unknown"),
            "status": "would_migrate",
            "current_plan": current_plan,
            "target_plan": target_plan,
        }

    try:
        db = mongodb_manager.get_database()
        db.users.update_one(
            {"_id": user["_id"]},
            {
                "$set": {
                    "plan": target_plan,
                    "migrated_from": current_plan,
                    "migrated_at": datetime.utcnow(),
                },
            },
        )

        return {
            "user_id": str(user["_id"]),
            "email": user.get("email", "unknown"),
            "status": "migrated",
            "current_plan": current_plan,
            "target_plan": target_plan,
        }
    except Exception as e:
        logger.error("Error migrating user %s: %s", user["_id"], e, exc_info=True)
        return {
            "user_id": str(user["_id"]),
            "email": user.get("email", "unknown"),
            "status": "error",
            "reason": str(e),
        }


def main() -> None:
    """Main migration function."""
    parser = argparse.ArgumentParser(description="Migrate users from legacy plans to new plans")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without applying them",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually apply the migration (requires confirmation)",
    )
    parser.add_argument(
        "--plan",
        choices=list(MIGRATION_MAPPINGS.keys()),
        help="Only migrate users on this specific plan",
    )

    args = parser.parse_args()

    if not args.dry_run and not args.execute:
        logger.error("Must specify either --dry-run or --execute")
        sys.exit(1)

    if args.execute and not args.dry_run:
        response = input("Are you sure you want to execute the migration? (yes/no): ")
        if response.lower() != "yes":
            logger.info("Migration cancelled")
            sys.exit(0)

    dry_run = args.dry_run and not args.execute

    logger.info("Starting plan migration (dry_run=%s, plan_filter=%s)", dry_run, args.plan)

    users = get_users_to_migrate(args.plan)
    if not users:
        logger.info("No users to migrate")
        return

    results = []
    for user in users:
        result = migrate_user(user, dry_run=dry_run)
        results.append(result)

    migrated = sum(1 for r in results if r["status"] == "migrated")
    would_migrate = sum(1 for r in results if r["status"] == "would_migrate")
    skipped = sum(1 for r in results if r["status"] == "skipped")
    errors = sum(1 for r in results if r["status"] == "error")

    logger.info("Migration summary:")
    logger.info("  Total users: %d", len(results))
    if dry_run:
        logger.info("  Would migrate: %d", would_migrate)
    else:
        logger.info("  Migrated: %d", migrated)
    logger.info("  Skipped: %d", skipped)
    logger.info("  Errors: %d", errors)

    if errors > 0:
        logger.warning("Errors occurred during migration. Check logs for details.")
        error_results = [r for r in results if r["status"] == "error"]
        for result in error_results:
            logger.warning("  User %s (%s): %s", result["user_id"], result.get("email", "unknown"), result.get("reason", "Unknown error"))

    if skipped > 0:
        logger.info("Skipped users (have Stripe subscriptions or invalid plans):")
        skipped_results = [r for r in results if r["status"] == "skipped"]
        for result in skipped_results[:10]:
            logger.info("  User %s (%s): %s", result["user_id"], result.get("email", "unknown"), result.get("reason", "Unknown reason"))
        if len(skipped_results) > 10:
            logger.info("  ... and %d more", len(skipped_results) - 10)


if __name__ == "__main__":
    main()

