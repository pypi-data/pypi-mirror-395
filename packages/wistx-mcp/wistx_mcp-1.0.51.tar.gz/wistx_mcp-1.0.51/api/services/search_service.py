"""Search service - business logic for codebase and package search operations."""

import logging
from typing import Any

from bson import ObjectId

from api.models.v1_requests import CodebaseSearchRequest, PackageSearchRequest
from api.models.v1_responses import (
    CodebaseSearchResponse,
    CodebaseSearchResult,
    FreshnessInfo,
    PackageSearchResponse,
    PackageSearchResult,
)
from api.database.async_mongodb import async_mongodb_adapter
from wistx_mcp.tools.lib.vector_search import VectorSearch
from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.package_search_service import PackageSearchService
from wistx_mcp.tools.lib.ai_analyzer import AIAnalyzer
from api.config import settings
from api.services.fresh_content_service import fresh_content_service
from api.exceptions import ValidationError

logger = logging.getLogger(__name__)


class SearchService:
    """Service for codebase and package search operations."""

    def __init__(self):
        """Initialize search service."""
        self.mongodb_adapter = async_mongodb_adapter
        mcp_mongodb_client = MongoDBClient()
        self.vector_search = VectorSearch(
            mcp_mongodb_client,
            gemini_api_key=settings.gemini_api_key,
            pinecone_api_key=settings.pinecone_api_key,
            pinecone_index_name=settings.pinecone_index_name,
        )
        self.ai_analyzer = AIAnalyzer()

    async def search_codebase(
        self,
        request: CodebaseSearchRequest,
        user_id: str,
    ) -> CodebaseSearchResponse:
        """Search user's indexed codebase.

        Args:
            request: Codebase search request
            user_id: User ID for filtering user's indexed content

        Returns:
            Codebase search response with results

        Raises:
            ValueError: If invalid parameters
            RuntimeError: If search fails
        """
        logger.info(
            "Searching codebase: query='%s', repositories=%s, resource_ids=%s, user_id=%s",
            request.query[:100],
            request.repositories,
            request.resource_ids,
            user_id,
        )

        await self.mongodb_adapter.connect()

        resolved_resource_ids = list(request.resource_ids) if request.resource_ids else []

        if request.repositories:
            db = self.mongodb_adapter.get_database()
            if db is None:
                raise RuntimeError("Failed to connect to MongoDB")

            resources_collection = db.indexed_resources
            repo_resource_ids = []

            for repo in request.repositories:
                normalized_repo = repo.replace(".git", "").rstrip("/")
                if "/" not in normalized_repo:
                    raise ValidationError(
                        message=f"Invalid repository format: {repo}",
                        user_message=f"Invalid repository format: {repo}. Expected 'owner/repo' format (e.g., 'owner/repository').",
                        error_code="INVALID_REPOSITORY_FORMAT",
                        details={"repository": repo, "expected_format": "owner/repo"}
                    )

                repo_patterns = [
                    f"https://github.com/{normalized_repo}",
                    f"https://github.com/{normalized_repo}.git",
                    f"http://github.com/{normalized_repo}",
                    f"http://github.com/{normalized_repo}.git",
                    normalized_repo,
                ]

                found = False
                for pattern in repo_patterns:
                    resource_doc = await resources_collection.find_one({
                        "user_id": ObjectId(user_id),
                        "resource_type": "repository",
                        "repo_url": {"$regex": pattern, "$options": "i"},
                        "status": "completed",
                    })
                    if resource_doc:
                        repo_resource_ids.append(str(resource_doc["_id"]))
                        found = True
                        break

                if not found:
                    logger.warning(
                        "No completed indexed resource found for repository: %s (may still be indexing)",
                        repo,
                    )

            if not repo_resource_ids:
                logger.warning("No indexed resources found for repositories: %s", request.repositories)

            resolved_resource_ids.extend(repo_resource_ids)

        if not resolved_resource_ids:
            logger.warning(
                "No completed indexed resources found for search. Repository may still be indexing. "
                "Use wistx_check_resource_status to check indexing progress."
            )

        results = await self.vector_search.search_knowledge_articles(
            query=request.query,
            user_id=user_id,
            include_global=False,
            limit=request.limit,
            resource_ids=resolved_resource_ids if resolved_resource_ids else None,
        )

        if request.file_types:
            filtered_results = []
            for result in results:
                tags = result.get("tags", [])
                if any(ft in tags for ft in request.file_types):
                    filtered_results.append(result)
            results = filtered_results

        if request.code_type:
            filtered_results = []
            for result in results:
                tags = result.get("tags", [])
                content = result.get("content", "").lower()
                if request.code_type.lower() in tags or request.code_type.lower() in content:
                    filtered_results.append(result)
            results = filtered_results

        if request.cloud_provider:
            filtered_results = []
            for result in results:
                content = result.get("content", "").lower()
                tags_str = " ".join(result.get("tags", [])).lower()
                if request.cloud_provider.lower() in content or request.cloud_provider.lower() in tags_str:
                    filtered_results.append(result)
            results = filtered_results

        resources_info = []
        if results:
            resource_ids_found = set(
                r.get("resource_id") for r in results if r.get("resource_id")
            )
            if resource_ids_found:
                db = self.mongodb_adapter.get_database()
                if db:
                    resources_collection = db.indexed_resources
                    resources_cursor = resources_collection.find(
                        {"_id": {"$in": [ObjectId(rid) for rid in resource_ids_found if ObjectId.is_valid(rid)]}}
                    )
                    resources_info = []
                    async for doc in resources_cursor:
                        doc["_id"] = str(doc["_id"])
                        resources_info.append(doc)

        highlights = []
        if request.include_sources:
            query_lower = request.query.lower()
            for result in results[:5]:
                content = result.get("content", "")
                if query_lower in content.lower():
                    start_idx = content.lower().find(query_lower)
                    highlight_start = max(0, start_idx - 50)
                    highlight_end = min(len(content), start_idx + len(request.query) + 50)
                    highlight = content[highlight_start:highlight_end]
                    highlights.append({
                        "article_id": result.get("article_id"),
                        "highlight": highlight,
                        "file_path": result.get("source_url", ""),
                    })

        search_results = [
            CodebaseSearchResult(
                article_id=result.get("article_id", ""),
                resource_id=result.get("resource_id", ""),
                title=result.get("title", ""),
                content=result.get("content", ""),
                source_url=result.get("source_url"),
                file_path=result.get("source_url"),
                tags=result.get("tags", []),
                similarity_score=result.get("similarity_score"),
            )
            for result in results
        ]

        response = CodebaseSearchResponse(
            results=search_results,
            resources=resources_info,
            total=len(search_results),
            highlights=highlights,
        )

        if request.include_ai_analysis and results:
            try:
                ai_analysis = await self.ai_analyzer.analyze_search_results(
                    query=request.query,
                    results=results,
                    resources=resources_info,
                )
                if ai_analysis:
                    response.ai_analysis = ai_analysis
            except Exception as e:
                logger.warning("AI analysis failed, continuing without analysis: %s", e)

        if request.group_by_section and resolved_resource_ids:
            try:
                from api.services.section_organizer import section_organizer

                grouped = await section_organizer.group_results_by_section(
                    results=[r.model_dump() for r in search_results],
                    resource_ids=resolved_resource_ids,
                    user_id=user_id,
                )
                response.grouped_by_section = grouped
            except Exception as e:
                logger.warning("Section grouping failed, continuing without grouping: %s", e)

        # Freshness checking and fresh content fetching
        if request.check_freshness or request.include_fresh_content:
            try:
                # Enrich results with repository metadata for freshness checking
                enriched_results = []
                for result in results:
                    enriched_result = dict(result)
                    # Find repository info for this result
                    resource_id = result.get("resource_id")
                    if resource_id:
                        for resource in resources_info:
                            if str(resource.get("_id")) == resource_id:
                                enriched_result["repository_url"] = resource.get("repo_url")
                                enriched_result["branch"] = resource.get("branch", "main")
                                enriched_result["commit_sha"] = resource.get("last_commit_sha")
                                enriched_result["analyzed_at"] = resource.get("last_indexed_at")
                                break
                    enriched_results.append(enriched_result)

                # Check freshness and optionally fetch fresh content
                enriched_results, freshness_info = await fresh_content_service.enrich_search_results_with_freshness(
                    results=enriched_results,
                    user_id=user_id,
                    include_fresh_content=request.include_fresh_content,
                    max_stale_minutes=request.max_stale_minutes,
                    max_files_to_check=min(10, len(enriched_results)),
                )

                # Convert freshness info to response model
                response.freshness = FreshnessInfo(
                    index_last_updated=freshness_info.index_last_updated.isoformat() if freshness_info.index_last_updated else None,
                    latest_commit_sha=freshness_info.latest_commit_sha,
                    indexed_commit_sha=freshness_info.indexed_commit_sha,
                    commits_behind=freshness_info.commits_behind,
                    stale_files_count=len(freshness_info.stale_files),
                    stale_files=freshness_info.stale_files[:10],
                    fresh_content_fetched=freshness_info.fresh_content_fetched,
                    freshness_check_performed=freshness_info.freshness_check_performed,
                    freshness_check_error=freshness_info.freshness_check_error,
                )

                # Update results with fresh content if fetched
                if request.include_fresh_content and freshness_info.fresh_content_fetched:
                    updated_results = []
                    for i, enriched_result in enumerate(enriched_results):
                        if i < len(search_results):
                            result = search_results[i]
                            # If fresh content was fetched, update the content
                            if "fresh_content" in enriched_result:
                                fresh = enriched_result["fresh_content"]
                                if fresh.get("is_changed"):
                                    # Create new result with fresh content
                                    result = CodebaseSearchResult(
                                        article_id=result.article_id,
                                        resource_id=result.resource_id,
                                        title=result.title + " [FRESH]",
                                        content=fresh.get("content", result.content),
                                        source_url=result.source_url,
                                        file_path=result.file_path,
                                        tags=result.tags + ["fresh_content"],
                                        similarity_score=result.similarity_score,
                                    )
                            updated_results.append(result)
                    response.results = updated_results

                logger.info(
                    "Freshness check completed: commits_behind=%d, stale_files=%d, fresh_fetched=%s",
                    freshness_info.commits_behind,
                    len(freshness_info.stale_files),
                    freshness_info.fresh_content_fetched,
                )

            except Exception as e:
                logger.warning("Freshness check failed, continuing without freshness info: %s", e)
                response.freshness = FreshnessInfo(
                    freshness_check_performed=False,
                    freshness_check_error=str(e),
                )

        return response

    async def search_packages(
        self,
        request: PackageSearchRequest,
        user_id: str,
    ) -> PackageSearchResponse:
        """Search DevOps/infrastructure packages.

        Args:
            request: Package search request
            user_id: User ID for authentication

        Returns:
            Package search response with results

        Raises:
            ValueError: If invalid parameters
            RuntimeError: If search fails
        """
        logger.info(
            "Searching packages: type=%s, query=%s, registry=%s, domain=%s",
            request.search_type,
            request.query[:100] if request.query else None,
            request.registry,
            request.domain,
        )

        await self.mongodb_adapter.connect()
        db = self.mongodb_adapter.get_database()
        if db is None:
            raise RuntimeError("Failed to connect to MongoDB")

        mcp_mongodb_client = MongoDBClient()
        await mcp_mongodb_client.connect()
        search_service = PackageSearchService(mcp_mongodb_client)

        if request.search_type == "semantic":
            if not request.query:
                raise ValidationError(
                    message="query is required for semantic search",
                    user_message="Search query is required for semantic search",
                    error_code="MISSING_QUERY",
                    details={"search_type": request.search_type}
                )

            logger.info(
                "Searching packages: type=semantic, query=%s, registry=%s, domain=%s, category=%s, limit=%d",
                request.query[:100],
                request.registry,
                request.domain,
                request.category,
                request.limit,
            )

            results = await search_service.semantic_search(
                query=request.query,
                registry=request.registry,
                domain=request.domain,
                category=request.category,
                limit=request.limit,
            )

            logger.info("Package search returned %d results", len(results))

            from api.models.v1_responses import PackageFileReference

            package_results = []
            for p in results:
                source_files = None
                if p.get("source_files"):
                    source_files = [
                        PackageFileReference(
                            file_path=sf.get("file_path", ""),
                            filename_sha256=sf.get("filename_sha256", ""),
                        )
                        for sf in p.get("source_files", [])
                        if sf.get("file_path") and sf.get("filename_sha256")
                    ]

                package_results.append(
                    PackageSearchResult(
                        package_id=p.get("package_id", ""),
                        name=p.get("name", ""),
                        registry=p.get("registry", ""),
                        version=p.get("version"),
                        description=p.get("description"),
                        domain=p.get("domain"),
                        category=p.get("category"),
                        github_url=p.get("github_url"),
                        download_count=p.get("download_count"),
                        stars=p.get("stars"),
                        similarity_score=p.get("similarity_score") or p.get("vector_score"),
                        source_files=source_files if source_files else None,
                    )
                )

            logger.info("Created %d PackageSearchResult objects", len(package_results))

            return PackageSearchResponse(
                results=package_results,
                total=len(package_results),
                search_type="semantic",
            )

        elif request.search_type == "regex":
            if not request.pattern and not request.template:
                raise ValidationError(
                    message="pattern or template is required for regex search",
                    user_message="Either a search pattern or template is required for regex search",
                    error_code="MISSING_PATTERN_OR_TEMPLATE",
                    details={"search_type": request.search_type}
                )

            results = await search_service.regex_search(
                pattern=request.pattern,
                template=request.template,
                registry=request.registry,
                package_name=request.package_name,
                limit=request.limit,
                allow_unindexed=True,
            )

            from api.models.v1_responses import PackageFileReference

            package_results = []
            for p in results:
                source_files = None
                if p.get("source_files"):
                    source_files = [
                        PackageFileReference(
                            file_path=sf.get("file_path", ""),
                            filename_sha256=sf.get("filename_sha256", ""),
                        )
                        for sf in p.get("source_files", [])
                        if sf.get("file_path") and sf.get("filename_sha256")
                    ]

                package_results.append(
                    PackageSearchResult(
                        package_id=p.get("package_id", ""),
                        name=p.get("name", ""),
                        registry=p.get("registry", ""),
                        version=p.get("version"),
                        description=p.get("description"),
                        domain=p.get("domain"),
                        category=p.get("category"),
                        github_url=p.get("github_url"),
                        download_count=p.get("download_count"),
                        stars=p.get("stars"),
                        similarity_score=None,
                        source_files=source_files if source_files else None,
                    )
                )

            return PackageSearchResponse(
                matches=package_results,
                total=len(package_results),
                search_type="regex",
            )

        else:
            if not request.query:
                raise ValidationError(
                    message="query is required for hybrid search",
                    user_message="Search query is required for hybrid search",
                    error_code="MISSING_QUERY",
                    details={"search_type": request.search_type}
                )
            if not request.pattern and not request.template:
                raise ValidationError(
                    message="pattern or template is required for hybrid search",
                    user_message="Either a search pattern or template is required for hybrid search",
                    error_code="MISSING_PATTERN_OR_TEMPLATE",
                    details={"search_type": request.search_type}
                )

            hybrid_results = await search_service.hybrid_search(
                query=request.query,
                pattern=request.pattern,
                template=request.template,
                registry=request.registry,
                domain=request.domain,
                category=request.category,
                limit=request.limit,
            )

            from api.models.v1_responses import PackageFileReference

            package_results = []
            for p in hybrid_results.get("packages", []):
                source_files = None
                if p.get("source_files"):
                    source_files = [
                        PackageFileReference(
                            file_path=sf.get("file_path", ""),
                            filename_sha256=sf.get("filename_sha256", ""),
                        )
                        for sf in p.get("source_files", [])
                        if sf.get("file_path") and sf.get("filename_sha256")
                    ]

                package_results.append(
                    PackageSearchResult(
                        package_id=p.get("package_id", ""),
                        name=p.get("name", ""),
                        registry=p.get("registry", ""),
                        version=p.get("version"),
                        description=p.get("description"),
                        domain=p.get("domain"),
                        category=p.get("category"),
                        github_url=p.get("github_url"),
                        download_count=p.get("download_count"),
                        stars=p.get("stars"),
                        similarity_score=p.get("similarity_score"),
                        source_files=source_files if source_files else None,
                    )
                )

            return PackageSearchResponse(
                results=package_results,
                semantic_count=hybrid_results.get("semantic_count", 0),
                regex_count=hybrid_results.get("regex_count", 0),
                total=hybrid_results.get("total", 0),
                search_type="hybrid",
            )

