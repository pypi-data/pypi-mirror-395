"""Migration 0002: Add custom compliance control fields.

Adds fields to compliance_controls collection for enterprise custom controls:
- user_id, organization_id, visibility, is_custom
- source_document_id, source_document_name
- extraction_method, extraction_confidence
- reviewed, reviewed_at, reviewed_by

Also creates new compliance_uploads collection and required indexes.
"""

import logging
from datetime import datetime

from api.database.migrations.base_migration import BaseMigration
from pymongo.database import Database

logger = logging.getLogger(__name__)


class Migration0002AddCustomComplianceFields(BaseMigration):
    """Migration to add custom compliance control fields."""

    @property
    def version(self) -> int:
        """Migration version."""
        return 2

    @property
    def description(self) -> str:
        """Migration description."""
        return "Add custom compliance control fields and compliance_uploads collection"

    async def up(self, db: Database) -> None:
        """Apply migration."""
        logger.info("Running migration 0002: Add custom compliance fields...")

        compliance_controls = db.compliance_controls

        logger.info("Adding default fields to existing compliance_controls...")
        result = compliance_controls.update_many(
            {"is_custom": {"$exists": False}},
            {
                "$set": {
                    "is_custom": False,
                    "user_id": None,
                    "organization_id": None,
                    "visibility": "global",
                    "source": "wistx",
                    "reviewed": False,
                }
            },
        )
        logger.info("Updated %d existing compliance controls", result.modified_count)

        logger.info("Creating indexes for compliance_controls...")
        compliance_controls.create_index(
            [("user_id", 1), ("is_custom", 1), ("visibility", 1)],
            name="user_custom_visibility_idx",
            background=True,
        )
        compliance_controls.create_index(
            [("organization_id", 1), ("is_custom", 1), ("visibility", 1)],
            name="org_custom_visibility_idx",
            background=True,
        )
        compliance_controls.create_index(
            [("is_custom", 1), ("standard", 1), ("visibility", 1)],
            name="custom_standard_visibility_idx",
            background=True,
        )
        compliance_controls.create_index(
            [("source_document_id", 1)],
            name="source_document_idx",
            background=True,
        )
        compliance_controls.create_index(
            [("reviewed", 1), ("is_custom", 1)],
            name="reviewed_custom_idx",
            background=True,
        )

        logger.info("Creating compliance_uploads collection...")
        compliance_uploads = db.compliance_uploads

        logger.info("Creating indexes for compliance_uploads...")
        compliance_uploads.create_index(
            [("user_id", 1), ("status", 1)],
            name="user_status_idx",
            background=True,
        )
        compliance_uploads.create_index(
            [("organization_id", 1), ("status", 1)],
            name="org_status_idx",
            background=True,
        )
        compliance_uploads.create_index(
            [("upload_id", 1)],
            name="upload_id_idx",
            unique=True,
            background=True,
        )
        compliance_uploads.create_index(
            [("document_id", 1)],
            name="document_id_idx",
            background=True,
        )

        logger.info("Migration 0002 complete")

    async def down(self, db: Database) -> None:
        """Rollback migration."""
        logger.info("Rolling back migration 0002...")

        compliance_controls = db.compliance_controls

        logger.info("Removing custom compliance fields from compliance_controls...")
        compliance_controls.update_many(
            {},
            {
                "$unset": {
                    "user_id": "",
                    "organization_id": "",
                    "visibility": "",
                    "is_custom": "",
                    "source_document_id": "",
                    "source_document_name": "",
                    "extraction_method": "",
                    "extraction_confidence": "",
                    "reviewed": "",
                    "reviewed_at": "",
                    "reviewed_by": "",
                }
            },
        )

        logger.info("Dropping indexes...")
        try:
            compliance_controls.drop_index("user_custom_visibility_idx")
        except Exception:
            pass
        try:
            compliance_controls.drop_index("org_custom_visibility_idx")
        except Exception:
            pass
        try:
            compliance_controls.drop_index("custom_standard_visibility_idx")
        except Exception:
            pass
        try:
            compliance_controls.drop_index("source_document_idx")
        except Exception:
            pass
        try:
            compliance_controls.drop_index("reviewed_custom_idx")
        except Exception:
            pass

        logger.info("Dropping compliance_uploads collection...")
        if "compliance_uploads" in db.list_collection_names():
            db.drop_collection("compliance_uploads")

        logger.info("Rollback complete")

