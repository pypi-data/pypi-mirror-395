"""Cost data search and query API endpoints."""

import logging
from datetime import datetime
from decimal import Decimal
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from api.database.mongodb import mongodb_manager
from api.config import settings
from pinecone import Pinecone
from data_pipelines.processors.embedding_generator import EmbeddingGenerator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/cost", tags=["cost"])


class CostSearchRequest(BaseModel):
    """Cost search request model."""

    query: str = Field(..., description="Search query")
    providers: list[str] | None = Field(default=None, description="Filter by providers")
    service_categories: list[str] | None = Field(default=None, description="Filter by service categories")
    regions: list[str] | None = Field(default=None, description="Filter by regions")
    pricing_categories: list[str] | None = Field(default=None, description="Filter by pricing categories")
    max_price: Decimal | None = Field(default=None, description="Maximum price filter")
    min_price: Decimal | None = Field(default=None, description="Minimum price filter")
    max_results: int = Field(default=20, ge=1, le=100, description="Maximum results")


class CostSearchResponse(BaseModel):
    """Cost search response model."""

    results: list[dict[str, Any]] = Field(..., description="Search results")
    total: int = Field(..., description="Total results found")
    query: str = Field(..., description="Original query")
    filters: dict[str, Any] = Field(..., description="Applied filters")


@router.post("/search", response_model=CostSearchResponse)
async def search_costs(request: CostSearchRequest) -> CostSearchResponse:
    """Search cost data using semantic search.

    Args:
        request: Search request with query and filters

    Returns:
        Search results with cost data
    """
    try:
        embedding_generator = EmbeddingGenerator()
        query_embedding = await embedding_generator.generate_embeddings_batch([request.query])
        
        if not query_embedding or len(query_embedding) == 0:
            raise HTTPException(status_code=500, detail="Failed to generate query embedding")

        if not settings.pinecone_api_key:
            raise HTTPException(status_code=500, detail="Pinecone API key not configured")
        
        pc = Pinecone(api_key=settings.pinecone_api_key)
        index = pc.Index(settings.pinecone_index_name)

        filter_dict: dict[str, Any] = {"collection": "cost_data_focus"}
        
        if request.providers:
            if len(request.providers) == 1:
                filter_dict["provider"] = request.providers[0]
            else:
                filter_dict["provider"] = {"$in": request.providers}
        if request.service_categories:
            if len(request.service_categories) == 1:
                filter_dict["service_category"] = request.service_categories[0]
            else:
                filter_dict["service_category"] = {"$in": request.service_categories}
        if request.regions:
            if len(request.regions) == 1:
                filter_dict["region_id"] = request.regions[0]
            else:
                filter_dict["region_id"] = {"$in": request.regions}
        if request.pricing_categories:
            if len(request.pricing_categories) == 1:
                filter_dict["pricing_category"] = request.pricing_categories[0]
            else:
                filter_dict["pricing_category"] = {"$in": request.pricing_categories}
        if request.max_price is not None or request.min_price is not None:
            price_filter: dict[str, float] = {}
            if request.max_price is not None:
                price_filter["$lte"] = float(request.max_price)
            if request.min_price is not None:
                price_filter["$gte"] = float(request.min_price)
            if price_filter:
                filter_dict["list_unit_price"] = price_filter

        query_response = index.query(
            vector=query_embedding[0],
            filter=filter_dict,
            top_k=request.max_results,
            include_metadata=True,
        )

        results = query_response.get("matches", [])

        mongodb_manager.connect()
        db = mongodb_manager.get_database()
        collection = db.cost_data_focus

        enriched_results = []
        for match in results:
            if hasattr(match, "metadata"):
                metadata = match.metadata
                score = match.score
            else:
                metadata = match.get("metadata", {})
                score = match.get("score", 0)
            
            lookup_key = metadata.get("lookup_key") if isinstance(metadata, dict) else getattr(metadata, "lookup_key", None)
            if lookup_key:
                full_record = collection.find_one({"lookup_key": lookup_key})
                if full_record:
                    full_record["similarity"] = score
                    enriched_results.append(full_record)

        return CostSearchResponse(
            results=enriched_results,
            total=len(enriched_results),
            query=request.query,
            filters={
                "providers": request.providers,
                "service_categories": request.service_categories,
                "regions": request.regions,
                "pricing_categories": request.pricing_categories,
                "max_price": float(request.max_price) if request.max_price else None,
                "min_price": float(request.min_price) if request.min_price else None,
            },
        )

    except Exception as e:
        logger.error("Error searching costs: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/by-provider/{provider}")
async def get_costs_by_provider(
    provider: str,
    region: str | None = Query(default=None, description="Filter by region"),
    service_category: str | None = Query(default=None, description="Filter by service category"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum results"),
    offset: int = Query(default=0, ge=0, description="Pagination offset"),
) -> dict[str, Any]:
    """Get costs by provider with optional filters.

    Args:
        provider: Cloud provider (aws, gcp, azure, oracle, alibaba)
        region: Optional region filter
        service_category: Optional service category filter
        limit: Maximum results
        offset: Pagination offset

    Returns:
        Cost data results
    """
    try:
        mongodb_manager.connect()
        db = mongodb_manager.get_database()
        collection = db.cost_data_focus

        query = {"provider": provider}
        if region:
            query["region_id"] = region
        if service_category:
            query["service_category"] = service_category

        total = collection.count_documents(query)
        records = list(
            collection.find(query)
            .sort("last_updated", -1)
            .skip(offset)
            .limit(limit)
        )

        return {
            "provider": provider,
            "total": total,
            "count": len(records),
            "offset": offset,
            "limit": limit,
            "results": records,
        }

    except Exception as e:
        logger.error("Error getting costs by provider: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@router.get("/compare")
async def compare_costs(
    service_name: str = Query(..., description="Service name to compare"),
    resource_type: str | None = Query(default=None, description="Resource type filter"),
    regions: list[str] = Query(default=[], description="Regions to compare"),
    providers: list[str] = Query(default=[], description="Providers to compare"),
) -> dict[str, Any]:
    """Compare costs across providers/regions.

    Args:
        service_name: Service name to compare
        resource_type: Optional resource type filter
        regions: List of regions to compare
        providers: List of providers to compare

    Returns:
        Comparison results
    """
    try:
        mongodb_manager.connect()
        db = mongodb_manager.get_database()
        collection = db.cost_data_focus

        query = {"service_name": service_name, "pricing_category": "OnDemand"}
        if resource_type:
            query["resource_type"] = resource_type
        if regions:
            query["region_id"] = {"$in": regions}
        if providers:
            query["provider"] = {"$in": providers}

        records = list(collection.find(query).sort("list_unit_price", 1))

        comparison = {}
        for record in records:
            provider = record.get("provider")
            region = record.get("region_id")
            key = f"{provider}:{region}"
            if key not in comparison:
                comparison[key] = {
                    "provider": provider,
                    "region": region,
                    "price": float(record.get("list_unit_price", 0)),
                    "currency": record.get("billing_currency", "USD"),
                    "unit": record.get("pricing_unit", "hour"),
                }

        return {
            "service_name": service_name,
            "resource_type": resource_type,
            "comparison": list(comparison.values()),
            "cheapest": min(comparison.values(), key=lambda x: x["price"]) if comparison else None,
        }

    except Exception as e:
        logger.error("Error comparing costs: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")


@router.get("/optimization-opportunities")
async def get_optimization_opportunities(
    provider: str | None = Query(default=None, description="Filter by provider"),
    min_savings_percentage: float = Query(default=20.0, description="Minimum savings percentage"),
    limit: int = Query(default=50, ge=1, le=200, description="Maximum results"),
) -> dict[str, Any]:
    """Get cost optimization opportunities.

    Args:
        provider: Optional provider filter
        min_savings_percentage: Minimum savings percentage threshold
        limit: Maximum results

    Returns:
        Optimization opportunities
    """
    try:
        mongodb_manager.connect()
        db = mongodb_manager.get_database()
        collection = db.cost_data_focus

        query = {"pricing_category": "OnDemand"}
        if provider:
            query["provider"] = provider

        on_demand_records = list(collection.find(query).limit(limit * 2))

        opportunities = []
        for record in on_demand_records:
            lookup_key = record.get("lookup_key")
            provider_name = record.get("provider")
            region = record.get("region_id")
            service = record.get("service_name")
            resource_type = record.get("resource_type")
            on_demand_price = float(record.get("list_unit_price", 0))

            reserved_query = {
                "provider": provider_name,
                "region_id": region,
                "service_name": service,
                "resource_type": resource_type,
                "pricing_category": "Reserved",
            }

            reserved_record = collection.find_one(reserved_query)
            if reserved_record:
                reserved_price = float(reserved_record.get("list_unit_price", 0))
                if reserved_price > 0:
                    savings = on_demand_price - reserved_price
                    savings_percentage = (savings / on_demand_price) * 100

                    if savings_percentage >= min_savings_percentage:
                        opportunities.append({
                            "provider": provider_name,
                            "service": service,
                            "resource_type": resource_type,
                            "region": region,
                            "current_price": on_demand_price,
                            "optimized_price": reserved_price,
                            "savings": savings,
                            "savings_percentage": round(savings_percentage, 2),
                            "optimization_type": "Reserved Instance",
                        })

        opportunities.sort(key=lambda x: x["savings_percentage"], reverse=True)

        return {
            "opportunities": opportunities[:limit],
            "total": len(opportunities),
            "total_potential_savings": sum(opp["savings"] for opp in opportunities[:limit]),
        }

    except Exception as e:
        logger.error("Error getting optimization opportunities: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

