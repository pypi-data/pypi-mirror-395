"""Incident tracker for troubleshooting knowledge persistence."""

import logging
import uuid
from datetime import datetime
from typing import Any

from wistx_mcp.models.incident import Incident, IncidentSeverity, IncidentStatus
from wistx_mcp.tools.lib.mongodb_client import MongoDBClient

logger = logging.getLogger(__name__)


class IncidentTracker:
    """Tracks troubleshooting incidents and resolutions."""

    def __init__(self, mongodb_client: MongoDBClient):
        """Initialize incident tracker.

        Args:
            mongodb_client: MongoDB client instance
        """
        self.mongodb_client = mongodb_client
        self.collection_name = "troubleshooting_incidents"

    async def create_incident(
        self,
        issue_description: str,
        diagnosis: dict[str, Any],
        fixes: list[dict[str, Any]],
        infrastructure_type: str | None = None,
        cloud_provider: str | None = None,
        resource_type: str | None = None,
        error_messages: list[str] | None = None,
        configuration_code: str | None = None,
        logs: str | None = None,
        user_id: str | None = None,
        organization_id: str | None = None,
    ) -> Incident:
        """Create a new incident record.

        Args:
            issue_description: Issue description
            diagnosis: Diagnosis dictionary
            fixes: List of fix recommendations
            infrastructure_type: Infrastructure type
            cloud_provider: Cloud provider
            resource_type: Resource type
            error_messages: Error messages
            configuration_code: Configuration code
            logs: Log output
            user_id: User ID
            organization_id: Organization ID

        Returns:
            Incident instance
        """
        incident_id = f"incident-{uuid.uuid4().hex[:12]}"

        root_cause = diagnosis.get("root_cause", "")
        if not root_cause and diagnosis.get("issues"):
            root_cause = diagnosis["issues"][0] if diagnosis["issues"] else ""

        severity = self._determine_severity(diagnosis, issue_description)

        incident = Incident(
            incident_id=incident_id,
            issue_description=issue_description,
            infrastructure_type=infrastructure_type,
            cloud_provider=cloud_provider,
            resource_type=resource_type,
            error_messages=error_messages or [],
            error_patterns=diagnosis.get("error_patterns", []),
            logs=logs,
            configuration_code=configuration_code,
            root_cause=root_cause,
            confidence=diagnosis.get("confidence", "medium"),
            identified_issues=diagnosis.get("issues", []),
            status=IncidentStatus.OPEN,
            severity=severity,
            fixes_attempted=fixes,
            prevention_strategies=[],
            related_knowledge=[],
            similar_incidents=[],
            attempts_count=0,
            user_id=user_id,
            organization_id=organization_id,
        )

        await self._save_incident(incident)

        logger.info(
            "Created incident: id=%s, type=%s, provider=%s",
            incident_id,
            infrastructure_type,
            cloud_provider,
        )

        return incident

    async def update_incident(
        self,
        incident_id: str,
        solution_applied: str,
        solution_effective: bool,
        solution_code: str | None = None,
        solution_source: str | None = None,
    ) -> Incident:
        """Update incident with resolution.

        Args:
            incident_id: Incident identifier
            solution_applied: Solution that was applied
            solution_effective: Whether solution was effective
            solution_code: Solution code (optional)
            solution_source: Solution source (optional)

        Returns:
            Updated Incident instance

        Raises:
            ValueError: If incident not found
        """
        incident = await self._get_incident(incident_id)
        if not incident:
            raise ValueError(f"Incident not found: {incident_id}")

        incident.solution_applied = solution_applied
        incident.solution_effective = solution_effective
        incident.solution_code = solution_code
        incident.solution_source = solution_source
        incident.attempts_count += 1

        if solution_effective:
            incident.status = IncidentStatus.RESOLVED
            incident.resolved_at = datetime.utcnow()

            if incident.created_at:
                delta = incident.resolved_at - incident.created_at
                incident.resolution_time_minutes = int(delta.total_seconds() / 60)

        incident.updated_at = datetime.utcnow()

        await self._save_incident(incident)

        logger.info(
            "Updated incident: id=%s, effective=%s, status=%s",
            incident_id,
            solution_effective,
            incident.status.value,
        )

        return incident

    async def find_similar_incidents(
        self,
        issue_description: str,
        infrastructure_type: str | None = None,
        cloud_provider: str | None = None,
        limit: int = 5,
    ) -> list[Incident]:
        """Find similar past incidents.

        Args:
            issue_description: Issue description
            infrastructure_type: Infrastructure type
            cloud_provider: Cloud provider
            limit: Maximum number of results

        Returns:
            List of similar incidents
        """
        if self.mongodb_client.database is None:
            await self.mongodb_client.connect()
        db = self.mongodb_client.database
        if db is None:
            logger.warning("MongoDB database not available for finding similar incidents")
            return []
        collection = db[self.collection_name]

        query: dict[str, Any] = {}

        if infrastructure_type:
            query["infrastructure_type"] = infrastructure_type
        if cloud_provider:
            query["cloud_provider"] = cloud_provider

        if issue_description:
            query["$text"] = {"$search": issue_description}

        cursor = collection.find(query).sort("created_at", -1).limit(limit)

        incidents = []
        async for doc in cursor:
            doc.pop("_id", None)
            try:
                incident = Incident(**doc)
                incidents.append(incident)
            except Exception as e:
                logger.warning("Failed to parse incident %s: %s", doc.get("incident_id"), e)

        return incidents

    async def get_incident_analytics(
        self,
        user_id: str | None = None,
        organization_id: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> dict[str, Any]:
        """Get incident analytics.

        Args:
            user_id: Filter by user ID
            organization_id: Filter by organization ID
            start_date: Start date filter
            end_date: End date filter

        Returns:
            Analytics dictionary
        """
        if self.mongodb_client.database is None:
            await self.mongodb_client.connect()
        db = self.mongodb_client.database
        if db is None:
            logger.warning("MongoDB database not available for incident analytics")
            return {}
        collection = db[self.collection_name]

        query: dict[str, Any] = {}
        if user_id:
            query["user_id"] = user_id
        if organization_id:
            query["organization_id"] = organization_id
        if start_date or end_date:
            query["created_at"] = {}
            if start_date:
                query["created_at"]["$gte"] = start_date
            if end_date:
                query["created_at"]["$lte"] = end_date

        total_incidents = await collection.count_documents(query)
        resolved_incidents = await collection.count_documents({**query, "status": IncidentStatus.RESOLVED.value})
        open_incidents = await collection.count_documents({**query, "status": {"$in": [IncidentStatus.OPEN.value, IncidentStatus.INVESTIGATING.value]}})

        avg_resolution_time_cursor = collection.aggregate([
            {"$match": {**query, "resolution_time_minutes": {"$exists": True, "$ne": None}}},
            {"$group": {"_id": None, "avg_time": {"$avg": "$resolution_time_minutes"}}},
        ])

        avg_resolution_time = None
        async for doc in avg_resolution_time_cursor:
            avg_resolution_time = doc.get("avg_time")

        severity_counts_cursor = collection.aggregate([
            {"$match": query},
            {"$group": {"_id": "$severity", "count": {"$sum": 1}}},
        ])

        severity_counts = {}
        async for doc in severity_counts_cursor:
            severity_counts[doc["_id"]] = doc["count"]

        return {
            "total_incidents": total_incidents,
            "resolved_incidents": resolved_incidents,
            "open_incidents": open_incidents,
            "resolution_rate": (resolved_incidents / total_incidents * 100) if total_incidents > 0 else 0.0,
            "average_resolution_time_minutes": round(avg_resolution_time, 2) if avg_resolution_time else None,
            "severity_counts": severity_counts,
        }

    async def _get_incident(self, incident_id: str) -> Incident | None:
        """Get incident by ID (internal).

        Args:
            incident_id: Incident identifier

        Returns:
            Incident instance or None
        """
        from wistx_mcp.tools.lib.mongodb_client import execute_mongodb_operation
        from wistx_mcp.tools.lib.constants import API_TIMEOUT_SECONDS

        if self.mongodb_client.database is None:
            await self.mongodb_client.connect()
        db = self.mongodb_client.database
        if db is None:
            logger.warning("MongoDB database not available for finding incident")
            return None
        collection = db[self.collection_name]

        async def _find_incident() -> dict[str, Any] | None:
            return await collection.find_one({"incident_id": incident_id})

        doc = await execute_mongodb_operation(
            _find_incident,
            timeout=API_TIMEOUT_SECONDS,
            max_retries=3,
        )
        if not doc:
            return None

        doc.pop("_id", None)
        try:
            return Incident(**doc)
        except Exception as e:
            logger.warning("Failed to parse incident %s: %s", incident_id, e)
            return None

    async def _save_incident(self, incident: Incident) -> None:
        """Save incident to MongoDB.

        Args:
            incident: Incident instance
        """
        from wistx_mcp.tools.lib.mongodb_client import execute_mongodb_operation
        from wistx_mcp.tools.lib.constants import API_TIMEOUT_SECONDS

        if self.mongodb_client.database is None:
            await self.mongodb_client.connect()
        db = self.mongodb_client.database
        if db is None:
            logger.warning("MongoDB database not available for saving incident")
            return
        collection = db[self.collection_name]

        incident_dict = incident.model_dump()
        incident_dict["updated_at"] = datetime.utcnow()

        async def _update_incident() -> None:
            await collection.update_one(
                {"incident_id": incident.incident_id},
                {"$set": incident_dict},
                upsert=True,
            )

        await execute_mongodb_operation(
            _update_incident,
            timeout=API_TIMEOUT_SECONDS,
            max_retries=3,
        )

    def _determine_severity(
        self,
        diagnosis: dict[str, Any],
        issue_description: str,
    ) -> IncidentSeverity:
        """Determine incident severity.

        Args:
            diagnosis: Diagnosis dictionary
            issues: Issue description

        Returns:
            IncidentSeverity
        """
        description_lower = issue_description.lower()

        if any(keyword in description_lower for keyword in ["critical", "down", "outage", "failed", "error"]):
            return IncidentSeverity.CRITICAL

        if any(keyword in description_lower for keyword in ["high", "severe", "broken", "not working"]):
            return IncidentSeverity.HIGH

        issues_count = len(diagnosis.get("issues", []))
        if issues_count > 3:
            return IncidentSeverity.HIGH

        return IncidentSeverity.MEDIUM

