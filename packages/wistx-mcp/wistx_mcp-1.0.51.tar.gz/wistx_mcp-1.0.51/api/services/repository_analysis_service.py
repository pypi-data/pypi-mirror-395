"""Repository analysis service - aggregates cost and compliance data from knowledge articles."""

import logging
from datetime import datetime
from typing import Any, Optional

from bson import ObjectId

from api.database.mongodb import mongodb_manager

logger = logging.getLogger(__name__)


class RepositoryAnalysisService:
    """Service for analyzing indexed repositories."""

    async def get_cost_analysis(
        self,
        resource_id: str,
        user_id: str,
        refresh: bool = False,
    ) -> dict[str, Any]:
        """Get cost analysis for indexed repository.

        Aggregates cost data from knowledge articles.

        Args:
            resource_id: Resource ID
            user_id: User ID
            refresh: Force recalculation

        Returns:
            Cost analysis dictionary
        """
        db = mongodb_manager.get_database()

        if not refresh:
            cached = db.repository_analysis_cache.find_one({
                "resource_id": resource_id,
                "user_id": ObjectId(user_id),
            })
            if cached and cached.get("cost_analysis"):
                cached["cost_analysis"]["cached"] = True
                return cached["cost_analysis"]

        articles_collection = db.knowledge_articles

        query = {
            "user_id": ObjectId(user_id),
            "resource_id": resource_id,
            "source_type": "repository-analysis",
        }

        articles = list(articles_collection.find(query))

        total_monthly = 0.0
        resources = []
        by_service = {}
        by_resource_type = {}
        by_cloud_provider = {}
        optimizations = []

        for article in articles:
            cost_impact = article.get("cost_impact", {})
            monthly = cost_impact.get("total_monthly", 0)
            total_monthly += monthly

            for service in article.get("services", []):
                by_service[service] = by_service.get(service, 0) + monthly

            for provider in article.get("cloud_providers", []):
                by_cloud_provider[provider] = by_cloud_provider.get(provider, 0) + monthly

            structured_data = article.get("structured_data", {})
            article_resources = structured_data.get("resources", [])
            for resource in article_resources:
                resources.append({
                    **resource,
                    "component_name": article.get("title", "Unknown"),
                    "file_path": article.get("source_url", "").split("/")[-1] if article.get("source_url") else "",
                })

            cost_optimizations = cost_impact.get("optimizations", [])
            if cost_optimizations:
                optimizations.extend(cost_optimizations)

            breakdown = cost_impact.get("breakdown", [])
            for item in breakdown:
                resource_type = item.get("resource_type", "unknown")
                cost = item.get("monthly_cost", 0)
                by_resource_type[resource_type] = by_resource_type.get(resource_type, 0) + cost

        result = {
            "total_monthly": round(total_monthly, 2),
            "total_annual": round(total_monthly * 12, 2),
            "breakdown": {
                "by_service": {k: round(v, 2) for k, v in by_service.items()},
                "by_resource_type": {k: round(v, 2) for k, v in by_resource_type.items()},
                "by_cloud_provider": {k: round(v, 2) for k, v in by_cloud_provider.items()},
            },
            "resources": resources,
            "optimizations": list(set(optimizations)),
            "last_calculated": datetime.utcnow(),
            "articles_count": len(articles),
            "cached": False,
        }

        db.repository_analysis_cache.update_one(
            {"resource_id": resource_id, "user_id": ObjectId(user_id)},
            {"$set": {"cost_analysis": result, "updated_at": datetime.utcnow()}},
            upsert=True,
        )

        return result

    async def get_compliance_analysis(
        self,
        resource_id: str,
        user_id: str,
        standards: Optional[list[str]] = None,
        refresh: bool = False,
    ) -> dict[str, Any]:
        """Get compliance analysis for indexed repository.

        Aggregates compliance data from knowledge articles.

        Args:
            resource_id: Resource ID
            user_id: User ID
            standards: Filter by standards
            refresh: Force recalculation

        Returns:
            Compliance analysis dictionary
        """
        db = mongodb_manager.get_database()

        if not refresh:
            cached = db.repository_analysis_cache.find_one({
                "resource_id": resource_id,
                "user_id": ObjectId(user_id),
            })
            if cached and cached.get("compliance_analysis"):
                cached["compliance_analysis"]["cached"] = True
                return cached["compliance_analysis"]

        articles_collection = db.knowledge_articles

        query = {
            "user_id": ObjectId(user_id),
            "resource_id": resource_id,
            "source_type": "repository-analysis",
        }

        articles = list(articles_collection.find(query))

        standards_data = {}

        for article in articles:
            compliance_impact = article.get("compliance_impact", {})

            if isinstance(compliance_impact, dict):
                for standard_name, standard_data in compliance_impact.items():
                    if standards and standard_name.lower() not in [s.lower() for s in standards]:
                        continue

                    if standard_name not in standards_data:
                        standards_data[standard_name] = {
                            "compliant_count": 0,
                            "non_compliant_count": 0,
                            "partial_count": 0,
                            "issues": [],
                        }

                    if isinstance(standard_data, dict):
                        status = standard_data.get("status", "unknown")
                        if status == "compliant":
                            standards_data[standard_name]["compliant_count"] += 1
                        elif status == "non_compliant":
                            standards_data[standard_name]["non_compliant_count"] += 1
                            standards_data[standard_name]["issues"].append({
                                "component": article.get("title", "Unknown"),
                                "control_id": standard_data.get("control_id"),
                                "issue": standard_data.get("issue", "Non-compliant"),
                                "severity": standard_data.get("severity", "MEDIUM"),
                            })
                        elif status == "partial":
                            standards_data[standard_name]["partial_count"] += 1

        for standard_name, data in standards_data.items():
            total = data["compliant_count"] + data["non_compliant_count"] + data["partial_count"]
            data["total_components"] = total
            if total > 0:
                compliance_rate = (data["compliant_count"] / total) * 100
                data["compliance_rate"] = round(compliance_rate, 2)
            else:
                data["compliance_rate"] = 0.0
            data["last_calculated"] = datetime.utcnow()

        overall_status = "unknown"
        if standards_data:
            total_compliant = sum(s["compliant_count"] for s in standards_data.values())
            total_non_compliant = sum(s["non_compliant_count"] for s in standards_data.values())
            total_partial = sum(s["partial_count"] for s in standards_data.values())
            total = total_compliant + total_non_compliant + total_partial
            if total > 0:
                compliance_rate = (total_compliant / total) * 100
                if compliance_rate >= 90:
                    overall_status = "compliant"
                elif compliance_rate >= 50:
                    overall_status = "partial"
                else:
                    overall_status = "non_compliant"

        result = {
            "standards": standards_data,
            "overall_status": overall_status,
            "last_calculated": datetime.utcnow(),
            "articles_count": len(articles),
            "cached": False,
        }

        db.repository_analysis_cache.update_one(
            {"resource_id": resource_id, "user_id": ObjectId(user_id)},
            {"$set": {"compliance_analysis": result, "updated_at": datetime.utcnow()}},
            upsert=True,
        )

        return result


repository_analysis_service = RepositoryAnalysisService()

