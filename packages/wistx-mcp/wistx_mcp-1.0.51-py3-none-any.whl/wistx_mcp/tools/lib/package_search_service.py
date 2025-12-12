"""Package search service - search indexed packages."""

import asyncio
import hashlib
import logging
import re
from typing import Any

from wistx_mcp.config import settings
from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.package_indexing_service import PackageIndexingService
from wistx_mcp.tools.lib.package_registry_integrator import RegistryIntegratorFactory
from wistx_mcp.tools.lib.pattern_templates import PatternTemplates
from wistx_mcp.tools.lib.pattern_validator import PatternValidator
from wistx_mcp.tools.lib.gemini_client import GeminiClient

logger = logging.getLogger(__name__)


class PackageSearchService:
    """Service for searching indexed packages."""

    def __init__(self, mongodb_client: MongoDBClient):
        """Initialize package search service.

        Args:
            mongodb_client: MongoDB client instance
        """
        self.mongodb_client = mongodb_client
        self.indexing_service = PackageIndexingService(mongodb_client)
        self.embedding_client = GeminiClient(api_key=settings.gemini_api_key) if settings.gemini_api_key else None
        self.pattern_validator = PatternValidator()

        if not self.embedding_client or not self.embedding_client.is_available():
            logger.warning("Gemini API key not set, semantic search will be limited")

    async def semantic_search(
        self,
        query: str,
        registry: str | None = None,
        domain: str | None = None,
        category: str | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Semantic search across indexed packages.

        Args:
            query: Search query
            registry: Optional registry filter
            domain: Optional domain filter
            category: Optional category filter
            limit: Maximum results

        Returns:
            List of matching packages
        """
        if not self.embedding_client:
            return await self._keyword_search(query, registry, domain, category, limit)

        try:
            query_embedding = await self._generate_embedding(query)

            from pinecone import Pinecone

            if not settings.pinecone_api_key:
                return await self._keyword_search(query, registry, domain, category, limit)

            pc = Pinecone(api_key=settings.pinecone_api_key)
            index = pc.Index(settings.pinecone_index_name)

            filter_dict: dict[str, Any] = {}
            if registry:
                filter_dict["registry"] = registry
            if domain:
                filter_dict["domain_tags"] = {"$in": [domain]}
            if category:
                filter_dict["category"] = category

            query_response = index.query(
                vector=query_embedding,
                filter=filter_dict if filter_dict else None,
                top_k=limit * 2,
                include_metadata=True,
            )

            package_ids = []
            score_map = {}
            for match in query_response.matches:
                package_id = match.metadata.get("package_id", "")
                if package_id:
                    package_ids.append(package_id)
                    score_map[package_id] = match.score

            logger.info(
                "Pinecone semantic search: query='%s', registry=%s, found %d matches",
                query[:100],
                registry,
                len(package_ids),
            )

            if not package_ids:
                logger.info("No Pinecone matches found, falling back to registry web search")
                registry_packages = await self._search_registries(query, registry, domain, category, limit)
                return await self._enhance_packages_with_files(registry_packages, include_files=True)

            await self.mongodb_client.connect()
            if self.mongodb_client.database is None:
                logger.warning("MongoDB not connected, falling back to registry web search")
                registry_packages = await self._search_registries(query, registry, domain, category, limit)
                return await self._enhance_packages_with_files(registry_packages, include_files=True)

            collection = self.mongodb_client.database.packages
            cursor = collection.find({"package_id": {"$in": package_ids}})
            packages = await cursor.to_list(length=len(package_ids))

            logger.info(
                "MongoDB lookup: found %d packages out of %d package_ids",
                len(packages),
                len(package_ids),
            )

            if not packages:
                logger.info("No packages found in MongoDB, falling back to registry web search")
                registry_packages = await self._search_registries(query, registry, domain, category, limit)
                return await self._enhance_packages_with_files(registry_packages, include_files=True)

            for package in packages:
                package_id = package.get("package_id", "")
                package["vector_score"] = score_map.get(package_id, 0.0)
                package["similarity_score"] = score_map.get(package_id, 0.0)

            packages.sort(key=lambda x: x.get("vector_score", 0), reverse=True)
            enhanced_packages = await self._enhance_packages_with_files(packages[:limit], include_files=True)
            return enhanced_packages
        except Exception as e:
            logger.warning("Semantic search failed, falling back to registry web search: %s", e)
            registry_packages = await self._search_registries(query, registry, domain, category, limit)
            return await self._enhance_packages_with_files(registry_packages, include_files=True)

    async def regex_search(
        self,
        pattern: str | None = None,
        template: str | None = None,
        registry: str | None = None,
        package_name: str | None = None,
        limit: int = 20,
        allow_unindexed: bool = True,
    ) -> list[dict[str, Any]]:
        """Regex search across package source code.

        Supports both indexed packages and on-demand fetching (no indexing required).

        Args:
            pattern: Regex pattern
            template: Pre-built template name
            registry: Optional registry filter
            package_name: Optional specific package
            limit: Maximum results
            allow_unindexed: If True, fetch packages on-demand if not indexed

        Returns:
            List of matches with package and file information
        """
        if template:
            pattern_str = PatternTemplates.get_template(template)
            if not pattern_str:
                raise ValueError(f"Invalid template: {template}")
        elif pattern:
            pattern_str = pattern
        else:
            raise ValueError("Either pattern or template must be provided")

        validation = await self.pattern_validator.validate_pattern(pattern_str)
        if not validation["valid"]:
            raise ValueError(f"Invalid regex pattern: {validation.get('error')}")

        compiled_pattern = re.compile(pattern_str, re.IGNORECASE | re.MULTILINE)

        matches = []
        packages_to_search = []

        if package_name:
            if not registry:
                raise ValueError("registry is required when package_name is specified")

            await self.mongodb_client.connect()
            is_indexed = False
            package_doc = None

            if self.mongodb_client.database is not None:
                collection = self.mongodb_client.database.packages
                package_doc = await collection.find_one({"name": package_name, "registry": registry})

            if package_doc:
                packages_to_search.append(package_doc)
                is_indexed = True
            elif allow_unindexed:
                logger.info("Package %s:%s not indexed, fetching on-demand", registry, package_name)
                try:
                    integrator = RegistryIntegratorFactory.create(registry)
                    metadata = await integrator.get_package_metadata(package_name)
                    await integrator.close()

                    package_doc = {
                        "package_id": f"{registry}:{package_name}",
                        "registry": registry,
                        "name": package_name,
                        "metadata": metadata,
                    }
                    packages_to_search.append(package_doc)
                except Exception as e:
                    logger.warning("Failed to fetch metadata for unindexed package %s:%s: %s", registry, package_name, e)
                    raise RuntimeError(f"Package {package_name} not found in registry {registry}") from e
            else:
                raise ValueError(f"Package {package_name} not indexed. Set allow_unindexed=True to fetch on-demand.")
        else:
            await self.mongodb_client.connect()
            if self.mongodb_client.database is not None:
                collection = self.mongodb_client.database.packages
                filter_dict: dict[str, Any] = {}
                if registry:
                    filter_dict["registry"] = registry
                cursor = collection.find(filter_dict).limit(100)
                packages_to_search = await cursor.to_list(length=100)

        for package_doc in packages_to_search:
            try:
                registry_name = package_doc.get("registry", "pypi")
                package_name_val = package_doc.get("name", "")

                integrator = RegistryIntegratorFactory.create(registry_name)
                source_files = await integrator.get_package_source(package_name_val)
                await integrator.close()

                if not source_files:
                    logger.warning("No source files found for package %s:%s", registry_name, package_name_val)
                    continue

                import hashlib

                for file_path, content in source_files.items():
                    file_hash = hashlib.sha256(file_path.encode()).hexdigest()
                    for match in compiled_pattern.finditer(content):
                        line_number = content[:match.start()].count("\n") + 1
                        matches.append({
                            "package_id": package_doc.get("package_id", f"{registry_name}:{package_name_val}"),
                            "package_name": package_name_val,
                            "registry": registry_name,
                            "file_path": file_path,
                            "filename_sha256": file_hash,
                            "line_number": line_number,
                            "match_text": match.group(),
                            "context": self._extract_context(content, match.start(), match.end()),
                        })

                        if len(matches) >= limit:
                            break

                if len(matches) >= limit:
                    break
            except Exception as e:
                logger.warning("Failed to search package %s: %s", package_doc.get("name"), e)
                continue

        return matches[:limit]

    async def hybrid_search(
        self,
        query: str,
        pattern: str | None = None,
        template: str | None = None,
        registry: str | None = None,
        domain: str | None = None,
        category: str | None = None,
        limit: int = 20,
    ) -> dict[str, Any]:
        """Hybrid search combining semantic and regex.

        Args:
            query: Natural language query
            pattern: Optional regex pattern
            template: Optional template name
            registry: Optional registry filter
            domain: Optional domain filter
            category: Optional category filter
            limit: Maximum results

        Returns:
            Dictionary with semantic and regex results
        """
        semantic_results = await self.semantic_search(query, registry, domain, category, limit)

        regex_results = []
        if pattern or template:
            try:
                regex_results = await self.regex_search(pattern, template, registry, limit=limit, allow_unindexed=True)
            except Exception as e:
                logger.warning("Regex search failed in hybrid search: %s", e)

        combined_results = self._combine_results(semantic_results, regex_results, limit)

        return {
            "packages": combined_results,
            "semantic_count": len(semantic_results),
            "regex_count": len(regex_results),
            "total": len(combined_results),
        }

    async def _keyword_search(
        self,
        query: str,
        registry: str | None = None,
        domain: str | None = None,
        category: str | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Keyword search fallback.

        Args:
            query: Search query
            registry: Optional registry filter
            domain: Optional domain filter
            category: Optional category filter
            limit: Maximum results

        Returns:
            List of matching packages
        """
        await self.mongodb_client.connect()
        if self.mongodb_client.database is None:
            logger.warning("MongoDB not connected for keyword search")
            return []

        collection = self.mongodb_client.database.packages

        query_words = query.lower().split()
        filter_dict: dict[str, Any] = {}

        if registry:
            filter_dict["registry"] = registry
        if domain:
            filter_dict["domain_tags"] = {"$in": [domain]}
        if category:
            filter_dict["category"] = category

        try:
            text_filter = {"$text": {"$search": query}}
            filter_dict.update(text_filter)
            cursor = collection.find(filter_dict).limit(limit)
            packages = await cursor.to_list(length=limit)
            if packages:
                logger.info("Keyword search (text index): found %d packages", len(packages))
                return await self._enhance_packages_with_files(packages, include_files=True)
            else:
                logger.info("Keyword search (text index): found 0 packages, falling back to registry search")
                registry_packages = await self._search_registries(query, registry, domain, category, limit)
                return await self._enhance_packages_with_files(registry_packages, include_files=True)
        except Exception as e:
            logger.debug("Text index search failed (index may not exist): %s", e)

        filter_dict.pop("$text", None)
        regex_filters = []
        for word in query_words:
            if len(word) >= 3:
                regex_filters.append({"name": {"$regex": word, "$options": "i"}})
                regex_filters.append({"description": {"$regex": word, "$options": "i"}})

        if regex_filters:
            filter_dict["$or"] = regex_filters
            cursor = collection.find(filter_dict).limit(limit)
            packages = await cursor.to_list(length=limit)
            logger.info("Keyword search (regex): found %d packages", len(packages))
            if packages:
                return await self._enhance_packages_with_files(packages, include_files=True)

        logger.info("Keyword search found no results, falling back to registry web search")
        registry_packages = await self._search_registries(query, registry, domain, category, limit)
        return await self._enhance_packages_with_files(registry_packages, include_files=True)

    async def _search_registries(
        self,
        query: str,
        registry: str | None = None,
        domain: str | None = None,
        category: str | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Search packages directly from registry APIs (web search fallback).

        Args:
            query: Search query
            registry: Optional registry filter
            domain: Optional domain filter (not used in registry search)
            category: Optional category filter (not used in registry search)
            limit: Maximum results

        Returns:
            List of matching packages from registries
        """
        logger.info(
            "Searching registries directly: query='%s', registry=%s",
            query[:100],
            registry,
        )

        registries_to_search = []
        if registry:
            registries_to_search = [registry]
        else:
            registries_to_search = ["terraform", "pypi", "npm", "helm", "ansible"]

        all_packages = []
        for reg in registries_to_search:
            try:
                integrator = RegistryIntegratorFactory.create(reg)
                packages = await integrator.search_packages(query, limit=limit)
                await integrator.close()

                for package in packages:
                    package_doc = {
                        "package_id": f"{reg}:{package.get('name', '')}",
                        "name": package.get("name", ""),
                        "registry": reg,
                        "description": package.get("description", ""),
                        "version": package.get("version"),
                        "github_url": package.get("source_url") or package.get("homepage"),
                        "download_count": package.get("downloads") or package.get("download_count"),
                        "stars": package.get("stars") or package.get("github_stars"),
                        "similarity_score": 0.5,
                        "source": "registry_api",
                    }
                    all_packages.append(package_doc)

                logger.info("Registry %s search: found %d packages", reg, len(packages))
            except Exception as e:
                logger.warning("Failed to search registry %s: %s", reg, e)
                continue

        logger.info("Registry web search: found %d total packages", len(all_packages))
        
        packages_to_return = all_packages[:limit]
        
        if packages_to_return:
            await self._auto_index_top_packages(packages_to_return[:5])
        
        enhanced_packages = await self._enhance_packages_with_files(packages_to_return, include_files=True)
        return enhanced_packages

    def _extract_context(self, content: str, start: int, end: int, context_lines: int = 3) -> str:
        """Extract context around match.

        Args:
            content: File content
            start: Match start position
            end: Match end position
            context_lines: Number of context lines

        Returns:
            Context string
        """
        lines = content.split("\n")
        start_line = content[:start].count("\n")
        end_line = content[:end].count("\n")

        context_start = max(0, start_line - context_lines)
        context_end = min(len(lines), end_line + context_lines + 1)

        context = "\n".join(lines[context_start:context_end])
        return context

    def _combine_results(
        self,
        semantic_results: list[dict[str, Any]],
        regex_results: list[dict[str, Any]],
        limit: int,
    ) -> list[dict[str, Any]]:
        """Combine semantic and regex results.

        Args:
            semantic_results: Semantic search results
            regex_results: Regex search results
            limit: Maximum results

        Returns:
            Combined results
        """
        combined = {}
        for result in semantic_results:
            package_id = result.get("package_id", "")
            if package_id:
                combined[package_id] = {
                    **result,
                    "match_type": "semantic",
                }

        for result in regex_results:
            package_id = result.get("package_id", "")
            if package_id in combined:
                combined[package_id]["match_type"] = "both"
                if "regex_matches" not in combined[package_id]:
                    combined[package_id]["regex_matches"] = []
                combined[package_id]["regex_matches"].append(result)
            else:
                combined[package_id] = {
                    "package_id": package_id,
                    "package_name": result.get("package_name"),
                    "registry": result.get("registry"),
                    "match_type": "regex",
                    "regex_matches": [result],
                }

        results = list(combined.values())
        results.sort(key=lambda x: (
            x.get("vector_score", 0) if x.get("match_type") in ["semantic", "both"] else 0,
            len(x.get("regex_matches", [])) if x.get("match_type") in ["regex", "both"] else 0,
        ), reverse=True)

        return results[:limit]

    async def _auto_index_top_packages(self, packages: list[dict[str, Any]]) -> None:
        """Auto-index top packages found during search.

        Args:
            packages: List of package dictionaries from registry search
        """
        if not packages:
            return

        await self.mongodb_client.connect()
        if self.mongodb_client.database is None:
            logger.warning("MongoDB not connected, skipping auto-indexing")
            return

        collection = self.mongodb_client.database.packages

        for package_doc in packages:
            try:
                package_id = package_doc.get("package_id", "")
                registry = package_doc.get("registry", "")
                name = package_doc.get("name", "")

                if not package_id or not registry or not name:
                    continue

                existing = await collection.find_one({"package_id": package_id})
                if existing:
                    logger.debug("Package already indexed: %s", package_id)
                    continue

                logger.info("Auto-indexing package: %s", package_id)

                try:
                    await self.indexing_service.index_package(
                        registry=registry,
                        package_name=name,
                        pre_indexed=False,
                    )
                    logger.info("Successfully auto-indexed package: %s", package_id)
                except Exception as e:
                    logger.warning("Failed to auto-index package %s: %s", package_id, e)
                    continue

            except Exception as e:
                logger.warning("Error in auto-indexing for package %s: %s", package_doc.get("package_id", "unknown"), e)
                continue

    async def _get_key_files_for_package(
        self,
        registry: str,
        package_name: str,
        version: str | None = None,
        max_files: int = 5,
    ) -> list[dict[str, str]]:
        """Get key files from package with SHA256 hashes.

        Args:
            registry: Package registry
            package_name: Package name
            version: Optional package version
            max_files: Maximum number of files to return

        Returns:
            List of file dictionaries with 'file_path' and 'filename_sha256'
        """
        key_file_patterns = [
            "README",
            "readme",
            "main",
            "index",
            "setup",
            "package.json",
            "requirements.txt",
            "go.mod",
            "Cargo.toml",
            "pom.xml",
            "build.gradle",
            "*.tf",
            "*.py",
            "*.js",
            "*.ts",
            "*.go",
            "*.rs",
        ]

        try:
            integrator = RegistryIntegratorFactory.create(registry)
            try:
                source_files = await integrator.get_package_source(package_name, version)
            except Exception as e:
                logger.debug("Failed to fetch source files for %s:%s: %s", registry, package_name, e)
                return []
            finally:
                await integrator.close()

            if not source_files:
                return []

            key_files = []
            file_paths = sorted(source_files.keys())
            seen_paths = set()

            for pattern in key_file_patterns:
                if len(key_files) >= max_files:
                    break

                pattern_lower = pattern.lower()
                for file_path in file_paths:
                    if file_path in seen_paths:
                        continue

                    file_path_lower = file_path.lower()
                    file_name = file_path.split("/")[-1].lower()

                    if pattern_lower in file_path_lower or pattern_lower == file_name or (
                        pattern.startswith("*") and file_path_lower.endswith(pattern_lower[1:])
                    ):
                        file_hash = hashlib.sha256(file_path.encode()).hexdigest()
                        key_files.append({
                            "file_path": file_path,
                            "filename_sha256": file_hash,
                        })
                        seen_paths.add(file_path)
                        if len(key_files) >= max_files:
                            break

            if len(key_files) < max_files:
                for file_path in file_paths:
                    if file_path not in seen_paths:
                        file_hash = hashlib.sha256(file_path.encode()).hexdigest()
                        key_files.append({
                            "file_path": file_path,
                            "filename_sha256": file_hash,
                        })
                        seen_paths.add(file_path)
                        if len(key_files) >= max_files:
                            break

            return key_files[:max_files]

        except Exception as e:
            logger.debug("Failed to get key files for package %s:%s: %s", registry, package_name, e)
            return []

    async def _enhance_packages_with_files(
        self,
        packages: list[dict[str, Any]],
        include_files: bool = True,
    ) -> list[dict[str, Any]]:
        """Enhance package dictionaries with source file references.

        Args:
            packages: List of package dictionaries
            include_files: Whether to include file references (default: True)

        Returns:
            Enhanced package dictionaries with 'source_files' field
        """
        if not include_files or not packages:
            return packages

        enhanced_packages = []
        for package in packages:
            enhanced_package = package.copy()

            registry = package.get("registry", "")
            package_name = package.get("name", "")
            version = package.get("version") or package.get("latest_version")

            if registry and package_name:
                try:
                    source_files = await self._get_key_files_for_package(
                        registry=registry,
                        package_name=package_name,
                        version=version,
                        max_files=5,
                    )
                    enhanced_package["source_files"] = source_files
                except Exception as e:
                    logger.debug("Failed to enhance package %s:%s with files: %s", registry, package_name, e)
                    enhanced_package["source_files"] = []
            else:
                enhanced_package["source_files"] = []

            enhanced_packages.append(enhanced_package)

        return enhanced_packages

    async def _generate_embedding(self, text: str) -> list[float]:
        """Generate embedding for text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        if not self.embedding_client or not self.embedding_client.is_available():
            raise ValueError("Embedding client not available")

        embedding = await self.embedding_client.create_embedding(
            text=text,
            task_type="RETRIEVAL_QUERY",
        )
        return embedding

