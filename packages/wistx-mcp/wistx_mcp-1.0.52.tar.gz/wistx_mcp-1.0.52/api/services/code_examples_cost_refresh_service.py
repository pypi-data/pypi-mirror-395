"""Code examples cost refresh service - refreshes stale cost data."""

import logging
from datetime import datetime
from typing import Any

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.pricing import calculate_infrastructure_cost
from api.exceptions import DatabaseError

logger = logging.getLogger(__name__)


class CodeExamplesCostRefreshService:
    """Service for refreshing cost data in code examples."""

    def __init__(self):
        """Initialize cost refresh service."""

    async def get_latest_pricing_timestamp(self, cloud_provider: str | None = None) -> datetime | None:
        """Get the timestamp of the most recent pricing data update.
        
        Args:
            cloud_provider: Optional cloud provider filter (aws, gcp, azure)
            
        Returns:
            Latest pricing data timestamp or None if no pricing data exists
        """
        async with MongoDBClient() as client:
            await client.connect()
            
            if client.database is None:
                return None
            
            collection = client.database.cost_data_focus
            
            query_filter: dict[str, Any] = {}
            if cloud_provider:
                query_filter["provider"] = cloud_provider.lower()
            
            cursor = collection.find(query_filter).sort("last_updated", -1).limit(1)
            records = await cursor.to_list(length=1)
            
            if not records:
                return None
            
            last_updated = records[0].get("last_updated")
            if isinstance(last_updated, datetime):
                return last_updated
            if isinstance(last_updated, str):
                try:
                    return datetime.fromisoformat(last_updated.replace("Z", "+00:00"))
                except ValueError:
                    logger.warning("Invalid timestamp format: %s", last_updated)
                    return None
            
            return None

    async def is_cost_stale(
        self,
        cost_analysis: dict[str, Any] | None,
        cloud_provider: str | None = None,
    ) -> bool:
        """Check if cost analysis is stale compared to latest pricing data.
        
        Args:
            cost_analysis: Cost analysis dictionary from code example
            cloud_provider: Cloud provider for filtering pricing data
            
        Returns:
            True if cost is stale, False otherwise
        """
        if not cost_analysis:
            return True
        
        analysis_timestamp = cost_analysis.get("analysis_timestamp")
        if not analysis_timestamp:
            return True
        
        if isinstance(analysis_timestamp, str):
            try:
                analysis_timestamp = datetime.fromisoformat(analysis_timestamp.replace("Z", "+00:00"))
            except ValueError:
                logger.warning("Invalid analysis_timestamp format: %s", analysis_timestamp)
                return True
        
        latest_pricing_timestamp = await self.get_latest_pricing_timestamp(cloud_provider)
        if not latest_pricing_timestamp:
            return False
        
        return analysis_timestamp < latest_pricing_timestamp

    async def refresh_cost_for_example(
        self,
        example: dict[str, Any],
    ) -> dict[str, Any]:
        """Refresh cost analysis for a single code example.
        
        Args:
            example: Code example dictionary from MongoDB
            
        Returns:
            Updated cost analysis dictionary
        """
        resources = example.get("resources", [])
        cloud_provider = example.get("cloud_provider", "unknown")
        
        if not resources or cloud_provider == "unknown":
            return {
                "estimated_monthly": 0.0,
                "estimated_annual": 0.0,
                "resource_costs": [],
                "analysis_timestamp": datetime.utcnow(),
            }
        
        resource_specs = []
        for resource in resources[:10]:
            service = self._extract_service_from_resource(resource)
            instance_type = self._extract_instance_type_from_resource(resource)
            
            if service and instance_type:
                resource_specs.append({
                    "cloud": cloud_provider,
                    "service": service,
                    "instance_type": instance_type,
                    "quantity": 1,
                })
        
        if not resource_specs:
            return {
                "estimated_monthly": 0.0,
                "estimated_annual": 0.0,
                "resource_costs": [],
                "analysis_timestamp": datetime.utcnow(),
            }
        
        try:
            result = await calculate_infrastructure_cost(
                resources=resource_specs,
                user_id=None,
                check_budgets=False,
            )
            
            return {
                "estimated_monthly": result.get("total_monthly", 0.0),
                "estimated_annual": result.get("total_annual", 0.0),
                "resource_costs": result.get("breakdown", []),
                "analysis_timestamp": datetime.utcnow(),
            }
        except Exception as e:
            logger.warning("Error refreshing cost for example %s: %s", example.get("example_id"), e)
            return {
                "estimated_monthly": 0.0,
                "estimated_annual": 0.0,
                "resource_costs": [],
                "analysis_timestamp": datetime.utcnow(),
                "error": str(e),
            }

    async def refresh_costs_batch(
        self,
        cloud_provider: str | None = None,
        batch_size: int = 100,
        max_examples: int | None = None,
    ) -> dict[str, Any]:
        """Refresh costs for code examples in batches.
        
        Args:
            cloud_provider: Optional cloud provider filter
            batch_size: Number of examples to process per batch
            max_examples: Maximum number of examples to refresh (None for all)
            
        Returns:
            Dictionary with refresh statistics
        """
        async with MongoDBClient() as client:
            await client.connect()
            
            if client.database is None:
                raise DatabaseError(
                    message="MongoDB database not available",
                    user_message="Database connection failed. Please try again later.",
                    error_code="DATABASE_NOT_AVAILABLE",
                    details={"service": "code_examples_cost_refresh"}
                )
            
            collection = client.database.code_examples
            
            query_filter: dict[str, Any] = {
                "cost_analysis": {"$exists": True},
            }
            
            if cloud_provider:
                query_filter["cloud_provider"] = cloud_provider.lower()
            
            latest_pricing_timestamp = await self.get_latest_pricing_timestamp(cloud_provider)
            if latest_pricing_timestamp:
                query_filter["cost_analysis.analysis_timestamp"] = {
                    "$lt": latest_pricing_timestamp,
                }
            
            total_count = await collection.count_documents(query_filter)
            
            if max_examples:
                total_count = min(total_count, max_examples)
            
            logger.info(
                "Starting cost refresh: %d examples to refresh (cloud_provider=%s)",
                total_count,
                cloud_provider or "all",
            )
            
            stats = {
                "total_found": total_count,
                "refreshed": 0,
                "failed": 0,
                "skipped": 0,
                "errors": [],
            }
            
            cursor = collection.find(query_filter).limit(max_examples or total_count)
            
            batch = []
            processed = 0
            
            async for example in cursor:
                batch.append(example)
                
                if len(batch) >= batch_size:
                    await self._process_batch(client, collection, batch, stats)
                    processed += len(batch)
                    batch = []
                    
                    if processed % 1000 == 0:
                        logger.info("Processed %d/%d examples", processed, total_count)
            
            if batch:
                await self._process_batch(client, collection, batch, stats)
            
            logger.info(
                "Cost refresh completed: refreshed=%d, failed=%d, skipped=%d",
                stats["refreshed"],
                stats["failed"],
                stats["skipped"],
            )
            
            return stats

    async def _process_batch(
        self,
        client: MongoDBClient,
        collection: Any,
        batch: list[dict[str, Any]],
        stats: dict[str, Any],
    ) -> None:
        """Process a batch of examples for cost refresh.
        
        Args:
            client: MongoDB client
            collection: MongoDB collection
            batch: List of example dictionaries
            stats: Statistics dictionary to update
        """
        for example in batch:
            try:
                example_id = example.get("example_id")
                if not example_id:
                    stats["skipped"] += 1
                    continue
                
                updated_cost = await self.refresh_cost_for_example(example)
                
                await collection.update_one(
                    {"example_id": example_id},
                    {
                        "$set": {
                            "cost_analysis": updated_cost,
                            "updated_at": datetime.utcnow(),
                        },
                    },
                )
                
                stats["refreshed"] += 1
            except Exception as e:
                stats["failed"] += 1
                error_msg = f"Example {example.get('example_id', 'unknown')}: {str(e)}"
                stats["errors"].append(error_msg)
                logger.warning("Failed to refresh cost: %s", error_msg)

    def _extract_service_from_resource(self, resource: str) -> str:
        """Extract service name from resource type.
        
        Args:
            resource: Resource type string
            
        Returns:
            Service name or empty string
        """
        resource_lower = resource.lower()
        
        if "rds" in resource_lower or "database" in resource_lower:
            return "rds"
        if "s3" in resource_lower or "bucket" in resource_lower:
            return "s3"
        if "ec2" in resource_lower or "instance" in resource_lower:
            return "ec2"
        if "lambda" in resource_lower:
            return "lambda"
        if "eks" in resource_lower or "kubernetes" in resource_lower:
            return "eks"
        if "elb" in resource_lower or "load" in resource_lower:
            return "elb"
        if "cloudfront" in resource_lower:
            return "cloudfront"
        if "dynamodb" in resource_lower:
            return "dynamodb"
        if "redshift" in resource_lower:
            return "redshift"
        if "elasticache" in resource_lower:
            return "elasticache"
        
        return ""

    def _extract_instance_type_from_resource(self, resource: str) -> str:
        """Extract instance type from resource type.
        
        Args:
            resource: Resource type string (e.g., "aws_db_instance", "db.t3.medium")
            
        Returns:
            Instance type or empty string
        """
        resource_lower = resource.lower()
        
        if "." in resource_lower:
            parts = resource_lower.split(".")
            if len(parts) >= 2:
                return ".".join(parts[-2:])
        
        if "t3" in resource_lower or "t4g" in resource_lower:
            for size in ["micro", "small", "medium", "large", "xlarge", "2xlarge"]:
                if size in resource_lower:
                    return f"t3.{size}"
        
        return ""


code_examples_cost_refresh_service = CodeExamplesCostRefreshService()

