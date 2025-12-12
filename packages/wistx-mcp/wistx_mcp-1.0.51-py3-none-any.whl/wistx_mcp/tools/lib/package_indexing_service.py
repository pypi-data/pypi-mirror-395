"""Package indexing service - index packages for search."""

import asyncio
import logging
from datetime import datetime
from typing import Any

from wistx_mcp.config import settings
from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.package_discovery_service import PackageDiscoveryService
from wistx_mcp.tools.lib.package_health_service import PackageHealthService
from wistx_mcp.tools.lib.package_registry_integrator import RegistryIntegratorFactory
from wistx_mcp.tools.lib.gemini_client import GeminiClient

logger = logging.getLogger(__name__)


class PackageIndexingService:
    """Service for indexing packages for search."""

    def __init__(self, mongodb_client: MongoDBClient):
        """Initialize package indexing service.

        Args:
            mongodb_client: MongoDB client instance
        """
        self.mongodb_client = mongodb_client
        self.discovery_service = PackageDiscoveryService()
        self.health_service = PackageHealthService()
        self.embedding_client = GeminiClient(api_key=settings.gemini_api_key) if settings.gemini_api_key else None

        if not self.embedding_client or not self.embedding_client.is_available():
            logger.warning("Gemini API key not set, embeddings will not be generated")

    async def index_package(
        self,
        registry: str,
        package_name: str,
        version: str | None = None,
        pre_indexed: bool = False,
    ) -> dict[str, Any]:
        """Index a package for search.

        Args:
            registry: Registry name (pypi, npm, terraform)
            package_name: Package name
            version: Optional version
            pre_indexed: Whether this is a pre-indexed package

        Returns:
            Indexed package document
        """
        try:
            integrator = RegistryIntegratorFactory.create(registry)
            metadata = await integrator.get_package_metadata(package_name, version)
            await integrator.close()

            if not self.discovery_service.domain_filter.is_devops_infrastructure_package(metadata):
                raise ValueError(f"Package {package_name} is not DevOps/infrastructure related")

            domain_tags = self.discovery_service.domain_filter.get_domain_tags(metadata)
            category = self.discovery_service.domain_filter.get_category(metadata)
            relevance_score = self.discovery_service.domain_filter.calculate_relevance_score(metadata)

            searchable_text = self._build_searchable_text(metadata)

            embedding = None
            if self.embedding_client:
                try:
                    embedding = await self._generate_embedding(searchable_text)
                except Exception as e:
                    logger.warning("Failed to generate embedding for package %s: %s", package_name, e)

            health_metrics = await self.health_service.calculate_health_metrics(
                metadata, registry, package_name
            )

            package_doc = {
                "package_id": f"{registry}:{package_name}",
                "registry": registry,
                "name": package_name,
                "version": metadata.get("version", ""),
                "latest_version": metadata.get("latest_version", ""),
                "description": metadata.get("description", ""),
                "keywords": metadata.get("keywords", []),
                "homepage": metadata.get("homepage"),
                "github_url": metadata.get("github_url"),
                "domain_tags": domain_tags,
                "category": category,
                "relevance_score": relevance_score,
                "searchable_text": searchable_text,
                "downloads": metadata.get("downloads", 0),
                "pre_indexed": pre_indexed,
                "indexed_at": datetime.utcnow(),
                "metadata": metadata,
                "health_metrics": health_metrics.model_dump(),
                "health_score": health_metrics.health_score,
            }

            if embedding:
                package_doc["embedding"] = embedding

            await self._save_to_mongodb(package_doc)
            await self._save_to_vector_db(package_doc, embedding)

            logger.info("Indexed package: %s:%s", registry, package_name)
            return package_doc
        except Exception as e:
            logger.error("Failed to index package %s:%s: %s", registry, package_name, e, exc_info=True)
            raise

    async def index_packages_batch(
        self,
        packages: list[dict[str, Any]],
        pre_indexed: bool = False,
    ) -> list[dict[str, Any]]:
        """Index multiple packages in batch.

        Args:
            packages: List of package dictionaries with registry and name
            pre_indexed: Whether these are pre-indexed packages

        Returns:
            List of indexed package documents
        """
        results = []
        for package in packages:
            try:
                registry = package.get("registry", "pypi")
                package_name = package.get("name") or package.get("package_name")
                version = package.get("version")

                if not package_name:
                    logger.warning("Skipping package without name: %s", package)
                    continue

                indexed = await self.index_package(registry, package_name, version, pre_indexed)
                results.append(indexed)
            except Exception as e:
                logger.warning("Failed to index package in batch: %s", e)
                continue

        return results

    async def is_package_indexed(self, registry: str, package_name: str) -> bool:
        """Check if package is already indexed.

        Args:
            registry: Registry name
            package_name: Package name

        Returns:
            True if package is indexed
        """
        await self.mongodb_client.connect()
        if self.mongodb_client.database is None:
            return False

        package_id = f"{registry}:{package_name}"
        existing = await self.mongodb_client.database.packages.find_one({"package_id": package_id})
        return existing is not None

    def _build_searchable_text(self, metadata: dict[str, Any]) -> str:
        """Build searchable text from package metadata.

        Args:
            metadata: Package metadata dictionary

        Returns:
            Searchable text string
        """
        parts = []
        parts.append(metadata.get("name", ""))
        parts.append(metadata.get("description", ""))
        keywords = metadata.get("keywords", [])
        if isinstance(keywords, list):
            parts.extend(keywords)
        elif isinstance(keywords, str):
            parts.append(keywords)

        classifiers = metadata.get("classifiers", [])
        if isinstance(classifiers, list):
            parts.extend(classifiers)

        return " ".join(str(p) for p in parts if p)

    async def _generate_embedding(self, text: str) -> list[float]:
        """Generate embedding for text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        if not self.embedding_client:
            raise ValueError("Embedding client not available")

        embedding = await self.embedding_client.create_embedding(
            text=text,
            task_type="RETRIEVAL_DOCUMENT",
        )
        return embedding

    async def _save_to_mongodb(self, package_doc: dict[str, Any]) -> None:
        """Save package document to MongoDB.

        Args:
            package_doc: Package document dictionary
        """
        await self.mongodb_client.connect()
        if self.mongodb_client.database is None:
            raise RuntimeError("MongoDB database not connected")

        collection = self.mongodb_client.database.packages
        package_id = package_doc["package_id"]

        await collection.update_one(
            {"package_id": package_id},
            {"$set": package_doc},
            upsert=True,
        )

    async def _save_to_vector_db(self, package_doc: dict[str, Any], embedding: list[float] | None) -> None:
        """Save package embedding to vector database.

        Args:
            package_doc: Package document dictionary
            embedding: Embedding vector
        """
        if not embedding:
            return

        try:
            from pinecone import Pinecone

            if not settings.pinecone_api_key:
                logger.warning("Pinecone API key not set, skipping vector DB save")
                return

            pc = Pinecone(api_key=settings.pinecone_api_key)
            index = pc.Index(settings.pinecone_index_name)

            metadata = {
                "package_id": package_doc["package_id"],
                "registry": package_doc["registry"],
                "name": package_doc["name"],
                "domain_tags": package_doc.get("domain_tags", []),
                "category": package_doc.get("category"),
                "pre_indexed": package_doc.get("pre_indexed", False),
                "health_score": package_doc.get("health_score", 0.0),
            }

            index.upsert(
                vectors=[{
                    "id": package_doc["package_id"],
                    "values": embedding,
                    "metadata": metadata,
                }]
            )
        except Exception as e:
            logger.warning("Failed to save to vector DB: %s", e)

