"""Vector search using Pinecone and MongoDB with hybrid retrieval and reranking."""

import logging
from typing import Any

from pinecone import Pinecone

from wistx_mcp.config import settings
from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.gemini_client import GeminiClient

logger = logging.getLogger(__name__)


class VectorSearch:
    """Vector search using Pinecone for semantic search."""

    def __init__(
        self,
        mongodb_client: MongoDBClient,
        gemini_api_key: str | None = None,
        pinecone_api_key: str | None = None,
        pinecone_index_name: str | None = None,
    ):
        """Initialize vector search with hybrid retrieval and reranking.

        Args:
            mongodb_client: MongoDB client instance
            gemini_api_key: Gemini API key for embeddings (optional, falls back to settings)
            pinecone_api_key: Pinecone API key (optional, falls back to settings)
            pinecone_index_name: Pinecone index name (optional, falls back to settings)

        Raises:
            ValueError: If Gemini or Pinecone API keys are not configured
        """
        self.mongodb_client = mongodb_client
        
        api_key = gemini_api_key or settings.gemini_api_key

        if not api_key or not api_key.strip():
            logger.debug("Gemini API key not configured - vector search will be disabled")
            self.embedding_client = None
            self.index = None
            return

        pinecone_key = pinecone_api_key or settings.pinecone_api_key
        index_name = pinecone_index_name or settings.pinecone_index_name

        if not pinecone_key or not pinecone_key.strip():
            logger.debug("Pinecone API key not configured - vector search will be disabled")
            self.embedding_client = None
            self.index = None
            return

        self.embedding_client = GeminiClient(api_key=api_key)

        try:
            pc = Pinecone(api_key=pinecone_key)
            self.index = pc.Index(index_name)
        except Exception as e:
            logger.warning("Failed to initialize Pinecone index - vector search will be disabled: %s", e)
            self.index = None

        try:
            from api.services.bm25_service import BM25Service
            self.bm25_service = BM25Service(mongodb_client)
        except Exception as e:
            logger.warning("BM25 service not available: %s", e)
            self.bm25_service = None

        try:
            from api.services.reranking_service import RerankingService
            self.reranking_service = RerankingService()
        except Exception as e:
            logger.warning("Reranking service not available: %s", e)
            self.reranking_service = None

    def is_available(self) -> bool:
        """Check if vector search is available.

        Returns:
            True if Gemini and Pinecone are configured, False otherwise
        """
        return self.embedding_client is not None and self.embedding_client.is_available() and self.index is not None

    async def _get_query_embedding(self, query: str) -> list[float]:
        """Get embedding for query string.

        Args:
            query: Query string

        Returns:
            Embedding vector

        Raises:
            RuntimeError: If embedding generation fails or vector search is not available
            ValueError: If query is empty or invalid
        """
        if not self.is_available():
            raise RuntimeError("Vector search is not available - Gemini API key or Pinecone API key not configured")
        
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        try:
            embedding = await self.embedding_client.create_embedding(
                text=query,
                task_type="RETRIEVAL_QUERY",
            )
            if not embedding or len(embedding) == 0:
                raise RuntimeError("Empty embedding response from Gemini")
            return embedding
        except Exception as e:
            logger.error("Failed to generate embedding for query: %s", e, exc_info=True)
            raise RuntimeError(f"Failed to generate embedding: {e}") from e

    async def search_compliance(
        self,
        query: str,
        standards: list[str] | None = None,
        severity: str | None = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """Search compliance controls using Pinecone vector search.

        Args:
            query: Search query
            standards: Filter by compliance standards
            severity: Filter by severity level
            limit: Maximum number of results

        Returns:
            List of compliance controls with full document data

        Raises:
            RuntimeError: If search operation fails
            ValueError: If query is invalid
        """
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        if limit <= 0 or limit > 50000:
            raise ValueError("Limit must be between 1 and 50000")

        try:
            query_embedding = await self._get_query_embedding(query)
        except (RuntimeError, ValueError) as e:
            logger.error("Failed to generate embedding: %s", e)
            raise

        filter_dict: dict[str, Any] = {"collection": "compliance_controls"}

        if standards:
            if not isinstance(standards, list):
                raise ValueError("Standards must be a list")
            filter_dict["standard"] = {"$in": standards}

        if severity:
            if severity not in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
                raise ValueError(f"Invalid severity: {severity}")
            filter_dict["severity"] = severity

        initial_limit = min(limit * 2, 10000)

        try:
            query_response = self.index.query(
                vector=query_embedding,
                filter=filter_dict if filter_dict else None,
                top_k=initial_limit,
                include_metadata=True,
            )
        except Exception as e:
            logger.error("Pinecone query failed: %s", e, exc_info=True)
            raise RuntimeError(f"Pinecone query failed: {e}") from e

        if not query_response or not hasattr(query_response, "matches"):
            logger.warning("Invalid Pinecone response structure")
            return []

        vector_control_ids = []
        for match in query_response.matches:
            if match.metadata and match.metadata.get("control_id"):
                vector_control_ids.append(match.metadata["control_id"])

        vector_score_map = {
            match.metadata["control_id"]: match.score
            for match in query_response.matches
            if match.metadata and match.metadata.get("control_id")
        }

        bm25_control_ids = []
        bm25_score_map = {}
        if self.bm25_service:
            try:
                await self.mongodb_client.connect()
                if self.mongodb_client.database is None:
                    logger.warning("MongoDB database not available for BM25 compliance search")
                else:
                    collection = self.mongodb_client.database.compliance_controls
                    mongo_filter: dict[str, Any] = {}
                    if standards:
                        mongo_filter["standard"] = {"$in": standards}
                    if severity:
                        mongo_filter["severity"] = severity

                    cursor = collection.find(mongo_filter if mongo_filter else {})
                    max_bm25_load = max(limit * 2, 50000)
                    controls_for_bm25 = await cursor.to_list(length=max_bm25_load)

                    if controls_for_bm25:
                        from rank_bm25 import BM25Okapi
                        import re

                        def tokenize(text: str) -> list[str]:
                            text_lower = text.lower()
                            tokens = re.findall(r"\b[a-z0-9]+\b", text_lower)
                            return tokens

                        tokenized_docs = []
                        control_ids_bm25 = []
                        for control in controls_for_bm25:
                            control_id = control.get("control_id", "")
                            if not control_id:
                                continue

                            contextual_desc = control.get("contextual_description", "")
                            title = control.get("title", "")
                            description = control.get("description", "")
                            requirement = control.get("requirement", "")

                            searchable_text = ""
                            if contextual_desc:
                                searchable_text += contextual_desc + " "
                            searchable_text += f"{title} {description} {requirement}"

                            tokens = tokenize(searchable_text)
                            if tokens:
                                tokenized_docs.append(tokens)
                                control_ids_bm25.append(control_id)

                        if tokenized_docs:
                            bm25_index = BM25Okapi(tokenized_docs)
                            query_tokens = tokenize(query)
                            if query_tokens:
                                scores = bm25_index.get_scores(query_tokens)
                                bm25_results = [
                                    (control_ids_bm25[i], float(scores[i]))
                                    for i in range(len(control_ids_bm25))
                                    if scores[i] > 0
                                ]
                                bm25_results.sort(key=lambda x: x[1], reverse=True)
                                bm25_control_ids = [cid for cid, _ in bm25_results[:initial_limit]]
                                bm25_score_map = {cid: score for cid, score in bm25_results[:initial_limit]}
            except Exception as e:
                logger.warning("BM25 search for compliance controls failed: %s", e)

        combined_control_ids = list(set(vector_control_ids + bm25_control_ids))

        if not combined_control_ids:
            logger.info("No control IDs found in search results for query: %s", query[:50])
            return []

        try:
            await self.mongodb_client.connect()

            if self.mongodb_client.database is None:
                logger.error("MongoDB database is None after connection")
                raise RuntimeError("MongoDB database connection failed")

            collection = self.mongodb_client.database.compliance_controls
            cursor = collection.find({"control_id": {"$in": combined_control_ids}})
            results = await cursor.to_list(length=len(combined_control_ids))

            if len(results) != len(combined_control_ids):
                logger.warning(
                    "Mismatch between search results (%d) and MongoDB results (%d)",
                    len(combined_control_ids),
                    len(results),
                )

            for result in results:
                control_id = result.get("control_id", "")
                vector_score = vector_score_map.get(control_id, 0.0)
                bm25_score = bm25_score_map.get(control_id, 0.0)

                normalized_vector_score = vector_score
                normalized_bm25_score = bm25_score / 10.0 if bm25_score > 0 else 0.0

                hybrid_score = (normalized_vector_score * 0.7) + (normalized_bm25_score * 0.3)
                result["hybrid_score"] = hybrid_score
                result["vector_score"] = vector_score
                result["bm25_score"] = bm25_score

            results.sort(key=lambda x: x.get("hybrid_score", 0), reverse=True)

            if self.reranking_service and results:
                try:
                    results = self.reranking_service.rerank(
                        query=query,
                        articles=results,
                        top_k=limit,
                    )
                except Exception as e:
                    logger.warning("Reranking failed for compliance controls: %s", e)

            final_results = results[:limit]
            
            if len(final_results) > 10000:
                logger.warning(
                    "Large compliance result set: %d results (limit: %d). Performance may be impacted.",
                    len(final_results),
                    limit
                )
            
            return final_results
        except Exception as e:
            logger.error("MongoDB query failed: %s", e, exc_info=True)
            raise RuntimeError(f"MongoDB query failed: {e}") from e

    async def search_knowledge_articles(
        self,
        query: str,
        domains: list[str] | None = None,
        content_types: list[str] | None = None,
        user_id: str | None = None,
        organization_id: str | None = None,
        include_global: bool = True,
        resource_ids: list[str] | None = None,
        limit: int = 1000,
    ) -> list[dict[str, Any]]:
        """Search knowledge articles using hybrid retrieval (vector + BM25) with reranking.

        Args:
            query: Search query
            domains: Filter by domains
            content_types: Filter by content types
            user_id: User ID for user-specific content
            organization_id: Organization ID for org-shared content
            include_global: Include global/shared content in results
            resource_ids: Filter by resource IDs (only search articles from these resources)
            limit: Maximum number of results

        Returns:
            List of knowledge articles with full document data, reranked by relevance
        """
        try:
            from wistx_mcp.tools.lib.retry_utils import with_timeout
            query_embedding = await with_timeout(
                self._get_query_embedding,
                timeout_seconds=10.0,
                query=query,
            )
        except Exception as e:
            logger.error("Failed to generate query embedding: %s", e, exc_info=True)
            raise RuntimeError(f"Failed to generate query embedding: {e}") from e

        filter_dict: dict[str, Any] = {"collection": "knowledge_articles"}

        if domains:
            filter_dict["domain"] = {"$in": domains}

        if content_types:
            filter_dict["content_type"] = {"$in": content_types}

        # OPTIMIZATION: Filter by resource_id at Pinecone level for much better performance
        # This prevents fetching thousands of irrelevant articles when searching specific repositories
        # resource_id is stored as STRING in Pinecone metadata (see github_service.py line 1786)
        if resource_ids:
            valid_resource_ids = [rid for rid in resource_ids if rid and isinstance(rid, str)]
            if valid_resource_ids:
                filter_dict["resource_id"] = {"$in": valid_resource_ids}
                logger.debug(
                    "Pinecone filter includes resource_ids: %s",
                    valid_resource_ids[:5],  # Log first 5 for debugging
                )

        visibility_filters = []
        if include_global:
            visibility_filters.append("global")
        if user_id:
            visibility_filters.append("user")
            if not include_global:
                filter_dict["user_id"] = user_id
        if organization_id:
            visibility_filters.append("organization")
            if not include_global and not user_id:
                filter_dict["organization_id"] = organization_id

        if visibility_filters:
            filter_dict["visibility"] = {"$in": visibility_filters}

        # Reduce initial_limit when filtering by resource_ids since results will be more targeted
        if resource_ids:
            initial_limit = min(limit * 3, 2000)  # Smaller batch for targeted search
        else:
            initial_limit = min(limit * 2, 5000)  # Larger batch for global search

        try:
            from wistx_mcp.tools.lib.retry_utils import with_timeout
            
            async def query_pinecone() -> Any:
                return self.index.query(
                    vector=query_embedding,
                    filter=filter_dict if filter_dict else None,
                    top_k=initial_limit,
                    include_metadata=True,
                )
            
            query_response = await with_timeout(
                query_pinecone,
                timeout_seconds=30.0,
            )
        except Exception as e:
            logger.error("Pinecone query failed or timed out: %s", e, exc_info=True)
            raise RuntimeError(f"Pinecone query failed: {e}") from e

        vector_article_ids = [
            match.metadata["article_id"]
            for match in query_response.matches
            if match.metadata.get("article_id")
        ]

        vector_score_map = {
            match.metadata["article_id"]: match.score
            for match in query_response.matches
            if match.metadata.get("article_id")
        }

        bm25_article_ids = []
        bm25_score_map = {}
        if self.bm25_service:
            try:
                from wistx_mcp.tools.lib.retry_utils import with_timeout
                bm25_results = await with_timeout(
                    self.bm25_service.search,
                    timeout_seconds=15.0,
                    query=query,
                    limit=min(initial_limit, 500),
                )
                bm25_article_ids = [aid for aid, _ in bm25_results]
                bm25_score_map = {aid: score for aid, score in bm25_results}
            except Exception as e:
                logger.warning("BM25 search failed or timed out (non-critical): %s", e)

        combined_article_ids = list(set(vector_article_ids + bm25_article_ids))

        if not combined_article_ids:
            return []

        await self.mongodb_client.connect()

        if self.mongodb_client.database is None:
            return []

        collection = self.mongodb_client.database.knowledge_articles

        mongo_filter: dict[str, Any] = {"article_id": {"$in": combined_article_ids}}

        # CRITICAL FIX: resource_id is stored as STRING in knowledge_articles collection
        # (see github_service.py _store_articles_batch - only user_id and organization_id are converted to ObjectId)
        # So we must query with STRING, not ObjectId
        if resource_ids:
            # Filter out empty/None values and keep as strings
            valid_resource_ids = [rid for rid in resource_ids if rid and isinstance(rid, str)]
            if valid_resource_ids:
                mongo_filter["resource_id"] = {"$in": valid_resource_ids}
                logger.debug("Filtering by resource_ids (as strings): %s", valid_resource_ids)
            else:
                logger.warning("No valid resource IDs provided for filtering")

        # CRITICAL FIX: user_id and organization_id are stored as ObjectId in knowledge_articles
        # (see github_service.py lines 1763-1765)
        # So we must convert to ObjectId for the visibility query
        from bson import ObjectId as BsonObjectId

        visibility_query = []
        if include_global:
            visibility_query.append({"visibility": "global", "user_id": None})
        if user_id:
            # Convert user_id string to ObjectId for MongoDB query
            try:
                user_id_obj = BsonObjectId(user_id) if BsonObjectId.is_valid(user_id) else user_id
                visibility_query.append({"visibility": "user", "user_id": user_id_obj})
            except Exception:
                visibility_query.append({"visibility": "user", "user_id": user_id})
        if organization_id:
            # Convert organization_id string to ObjectId for MongoDB query
            try:
                org_id_obj = BsonObjectId(organization_id) if BsonObjectId.is_valid(organization_id) else organization_id
                visibility_query.append({"visibility": "organization", "organization_id": org_id_obj})
            except Exception:
                visibility_query.append({"visibility": "organization", "organization_id": organization_id})

        if visibility_query:
            if len(visibility_query) > 1:
                mongo_filter["$or"] = visibility_query
            else:
                mongo_filter.update(visibility_query[0])

        try:
            from wistx_mcp.tools.lib.retry_utils import with_timeout
            
            async def fetch_mongo_results() -> list[dict[str, Any]]:
                cursor = collection.find(mongo_filter)
                return await cursor.to_list(length=min(len(combined_article_ids), 5000))
            
            article_count = len(combined_article_ids)
            base_timeout = 20.0
            
            if article_count <= 100:
                mongo_timeout = base_timeout
            elif article_count <= 500:
                mongo_timeout = base_timeout + (article_count / 100) * 2.0
            elif article_count <= 1000:
                mongo_timeout = base_timeout + (article_count / 100) * 1.5
            else:
                mongo_timeout = min(60.0, base_timeout + (article_count / 100) * 1.0)
            
            logger.debug(
                "MongoDB query timeout: %.1fs for %d article IDs",
                mongo_timeout,
                article_count,
            )
            
            results = await with_timeout(
                fetch_mongo_results,
                timeout_seconds=mongo_timeout,
            )
        except Exception as e:
            logger.error(
                "MongoDB query failed or timed out: %s (article_count=%d)",
                e,
                len(combined_article_ids),
                exc_info=True,
            )
            raise RuntimeError(f"MongoDB query failed: {e}") from e

        for result in results:
            article_id = result.get("article_id", "")
            vector_score = vector_score_map.get(article_id, 0.0)
            bm25_score = bm25_score_map.get(article_id, 0.0)

            normalized_vector_score = vector_score
            normalized_bm25_score = bm25_score / 10.0 if bm25_score > 0 else 0.0

            hybrid_score = (normalized_vector_score * 0.7) + (normalized_bm25_score * 0.3)
            result["hybrid_score"] = hybrid_score
            result["vector_score"] = vector_score
            result["bm25_score"] = bm25_score

        results.sort(key=lambda x: x.get("hybrid_score", 0), reverse=True)

        if self.reranking_service and results:
            try:
                from wistx_mcp.tools.lib.retry_utils import with_timeout
                
                rerank_limit = min(limit, 100)
                rerank_timeout = min(20.0, max(5.0, len(results) / 50))
                
                async def rerank_articles() -> list[dict[str, Any]]:
                    return self.reranking_service.rerank(
                        query=query,
                        articles=results[:rerank_limit * 2],
                        top_k=rerank_limit,
                    )
                
                reranked = await with_timeout(
                    rerank_articles,
                    timeout_seconds=rerank_timeout,
                )
                if reranked:
                    results = reranked + results[rerank_limit:]
            except Exception as e:
                logger.warning("Reranking failed or timed out (non-critical): %s", e)

        final_results = results[:limit]
        
        if len(final_results) > 10000:
            logger.warning(
                "Large knowledge articles result set: %d results (limit: %d). Performance may be impacted.",
                len(final_results),
                limit
            )
        
        return final_results

    async def search_code_examples(
        self,
        query: str,
        code_types: list[str] | None = None,
        cloud_provider: str | None = None,
        services: list[str] | None = None,
        min_quality_score: int | None = None,
        compliance_standard: str | None = None,
        limit: int = 1000,
    ) -> list[dict[str, Any]]:
        """Search code examples using hybrid retrieval (vector + BM25) with reranking.
        
        Args:
            query: Search query
            code_types: Filter by code types (terraform, kubernetes, docker, etc.)
            cloud_provider: Filter by cloud provider (aws, gcp, azure)
            services: Filter by cloud services (rds, s3, ec2, etc.)
            min_quality_score: Minimum quality score (0-100)
            compliance_standard: Filter by compliance standard (requires compliance mappings)
            limit: Maximum number of results
            
        Returns:
            List of code examples with full document data, reranked by relevance
        """
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")
        
        if limit <= 0 or limit > 50000:
            raise ValueError("Limit must be between 1 and 50000")
        
        try:
            query_embedding = await self._get_query_embedding(query)
        except (RuntimeError, ValueError) as e:
            logger.error("Failed to generate embedding: %s", e)
            raise
        
        filter_dict: dict[str, Any] = {"collection": "code_examples"}
        
        if code_types:
            if not isinstance(code_types, list):
                raise ValueError("code_types must be a list")
            filter_dict["infrastructure_type"] = {"$in": code_types}
        
        if cloud_provider:
            if cloud_provider not in ["aws", "gcp", "azure", "oracle", "alibaba"]:
                raise ValueError(f"Invalid cloud provider: {cloud_provider}")
            filter_dict["cloud_provider"] = cloud_provider
        
        if services:
            if not isinstance(services, list):
                raise ValueError("services must be a list")
            filter_dict["services"] = {"$in": services}
        
        if min_quality_score is not None:
            filter_dict["quality_score"] = {"$gte": min_quality_score}
        
        initial_limit = min(limit * 2, 10000)
        
        try:
            query_response = self.index.query(
                vector=query_embedding,
                filter=filter_dict if filter_dict else None,
                top_k=initial_limit,
                include_metadata=True,
            )
        except Exception as e:
            logger.error("Pinecone query failed: %s", e, exc_info=True)
            raise RuntimeError(f"Pinecone query failed: {e}") from e
        
        if not query_response or not hasattr(query_response, "matches"):
            logger.warning("Invalid Pinecone response structure")
            return []
        
        vector_example_ids = []
        for match in query_response.matches:
            if match.metadata and match.metadata.get("example_id"):
                vector_example_ids.append(match.metadata["example_id"])
        
        vector_score_map = {
            match.metadata["example_id"]: match.score
            for match in query_response.matches
            if match.metadata and match.metadata.get("example_id")
        }
        
        bm25_example_ids = []
        bm25_score_map = {}
        
        if self.bm25_service:
            try:
                await self.mongodb_client.connect()
                if self.mongodb_client.database is None:
                    logger.warning("MongoDB database not available for BM25 code examples search")
                else:
                    collection = self.mongodb_client.database.code_examples
                    mongo_filter: dict[str, Any] = {}
                    
                    if code_types:
                        mongo_filter["code_type"] = {"$in": code_types}
                    if cloud_provider:
                        mongo_filter["cloud_provider"] = cloud_provider
                    if services:
                        mongo_filter["services"] = {"$in": services}
                    if min_quality_score is not None:
                        mongo_filter["quality_score"] = {"$gte": min_quality_score}
                    
                    cursor = collection.find(mongo_filter if mongo_filter else {})
                    max_bm25_load = max(limit * 2, 50000)
                    examples_for_bm25 = await cursor.to_list(length=max_bm25_load)
                    
                    if examples_for_bm25:
                        from rank_bm25 import BM25Okapi
                        import re
                        
                        def tokenize(text: str) -> list[str]:
                            text_lower = text.lower()
                            tokens = re.findall(r"\b[a-z0-9]+\b", text_lower)
                            return tokens
                        
                        tokenized_docs = []
                        example_ids_bm25 = []
                        
                        for example in examples_for_bm25:
                            example_id = example.get("example_id", "")
                            if not example_id:
                                continue
                            
                            contextual_desc = example.get("contextual_description", "")
                            title = example.get("title", "")
                            description = example.get("description", "")
                            code = example.get("code", "")[:2000]
                            
                            searchable_text = ""
                            if contextual_desc:
                                searchable_text += contextual_desc + " "
                            searchable_text += f"{title} {description} {code}"
                            
                            tokens = tokenize(searchable_text)
                            if tokens:
                                tokenized_docs.append(tokens)
                                example_ids_bm25.append(example_id)
                        
                        if tokenized_docs:
                            bm25_index = BM25Okapi(tokenized_docs)
                            query_tokens = tokenize(query)
                            if query_tokens:
                                scores = bm25_index.get_scores(query_tokens)
                                bm25_results = [
                                    (example_ids_bm25[i], float(scores[i]))
                                    for i in range(len(example_ids_bm25))
                                    if scores[i] > 0
                                ]
                                bm25_results.sort(key=lambda x: x[1], reverse=True)
                                bm25_example_ids = [eid for eid, _ in bm25_results[:initial_limit]]
                                bm25_score_map = {eid: score for eid, score in bm25_results[:initial_limit]}
            except Exception as e:
                logger.warning("BM25 search for code examples failed: %s", e)
        
        combined_example_ids = list(set(vector_example_ids + bm25_example_ids))
        
        if compliance_standard and combined_example_ids:
            try:
                await self.mongodb_client.connect()
                if self.mongodb_client.database is not None:
                    mappings_collection = self.mongodb_client.database.code_example_compliance_mappings
                    compliance_filter = {
                        "standard": compliance_standard,
                        "implementation_status": "implemented",
                        "example_id": {"$in": combined_example_ids},
                    }
                    cursor = mappings_collection.find(compliance_filter)
                    compliant_mappings = await cursor.to_list(length=None)
                    compliant_example_ids = [m.get("example_id") for m in compliant_mappings if m.get("example_id")]
                    
                    if compliant_example_ids:
                        combined_example_ids = [eid for eid in combined_example_ids if eid in compliant_example_ids]
                        logger.info(
                            "Found %d compliant examples for standard: %s",
                            len(combined_example_ids),
                            compliance_standard,
                        )
                    else:
                        logger.warning(
                            "No compliant examples found for %s, falling back to all results",
                            compliance_standard,
                        )
            except Exception as e:
                logger.warning("Compliance filtering failed, using all results: %s", e)
        
        if not combined_example_ids:
            logger.info("No example IDs found in search results for query: %s", query[:50])
            
            broader_filter = {"collection": "code_examples"}
            if code_types:
                broader_filter["infrastructure_type"] = {"$in": code_types}
            if cloud_provider:
                broader_filter["cloud_provider"] = cloud_provider
            
            try:
                broader_query_response = self.index.query(
                    vector=query_embedding,
                    filter=broader_filter if broader_filter else None,
                    top_k=min(limit * 3, 5000),
                    include_metadata=True,
                )
                
                if broader_query_response and hasattr(broader_query_response, "matches"):
                    fallback_ids = [
                        match.metadata["example_id"]
                        for match in broader_query_response.matches
                        if match.metadata and match.metadata.get("example_id")
                    ]
                    if fallback_ids:
                        combined_example_ids = fallback_ids[:limit * 2]
                        logger.info("Fallback search found %d examples", len(combined_example_ids))
            except Exception as e:
                logger.warning("Fallback search failed: %s", e)
            
            if not combined_example_ids:
                return []
        
        try:
            await self.mongodb_client.connect()
            
            if self.mongodb_client.database is None:
                logger.error("MongoDB database is None after connection")
                raise RuntimeError("MongoDB database connection failed")
            
            collection = self.mongodb_client.database.code_examples
            cursor = collection.find({"example_id": {"$in": combined_example_ids}})
            results = await cursor.to_list(length=len(combined_example_ids))
            
            if len(results) != len(combined_example_ids):
                logger.warning(
                    "Mismatch between search results (%d) and MongoDB results (%d)",
                    len(combined_example_ids),
                    len(results),
                )
            
            for result in results:
                example_id = result.get("example_id", "")
                vector_score = vector_score_map.get(example_id, 0.0)
                bm25_score = bm25_score_map.get(example_id, 0.0)
                
                normalized_vector_score = vector_score
                normalized_bm25_score = bm25_score / 10.0 if bm25_score > 0 else 0.0
                
                hybrid_score = (normalized_vector_score * 0.7) + (normalized_bm25_score * 0.3)
                result["hybrid_score"] = hybrid_score
                result["vector_score"] = vector_score
                result["bm25_score"] = bm25_score
            
            results.sort(key=lambda x: x.get("hybrid_score", 0), reverse=True)
            
            if self.reranking_service and results:
                try:
                    results = self.reranking_service.rerank(
                        query=query,
                        articles=results,
                        top_k=limit,
                    )
                except Exception as e:
                    logger.warning("Reranking failed for code examples: %s", e)
            
            final_results = results[:limit]
            
            if len(final_results) > 10000:
                logger.warning(
                    "Large code examples result set: %d results (limit: %d). Performance may be impacted.",
                    len(final_results),
                    limit
                )
            
            return final_results
        except Exception as e:
            logger.error("MongoDB query failed: %s", e, exc_info=True)
            raise RuntimeError(f"MongoDB query failed: {e}") from e

