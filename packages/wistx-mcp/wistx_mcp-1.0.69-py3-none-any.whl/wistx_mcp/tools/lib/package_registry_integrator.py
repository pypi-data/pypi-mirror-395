"""Package registry integrator - fetch packages from PyPI, NPM, Terraform Registry."""

import asyncio
import logging
from datetime import datetime
from typing import Any

import httpx

from wistx_mcp.tools.lib.package_cache import get_cache

logger = logging.getLogger(__name__)


class PackageRegistryIntegrator:
    """Base class for package registry integrators."""

    def __init__(self, timeout: float = 30.0):
        """Initialize registry integrator.

        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)

    async def close(self) -> None:
        """Close HTTP client."""
        await self.client.aclose()

    async def get_package_metadata(self, package_name: str, version: str | None = None) -> dict[str, Any]:
        """Get package metadata from registry (with caching).

        Args:
            package_name: Package name
            version: Optional version (defaults to latest)

        Returns:
            Package metadata dictionary

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        cache = get_cache()
        class_name = self.__class__.__name__
        if class_name == "PyPIIntegrator":
            registry_name = "pypi"
        elif class_name == "NPMIntegrator":
            registry_name = "npm"
        elif class_name == "TerraformRegistryIntegrator":
            registry_name = "terraform"
        elif class_name == "CratesIOIntegrator":
            registry_name = "crates_io"
        elif class_name == "GoModulesIntegrator":
            registry_name = "golang"
        elif class_name == "HelmChartsIntegrator":
            registry_name = "helm"
        elif class_name == "AnsibleGalaxyIntegrator":
            registry_name = "ansible"
        elif class_name == "MavenCentralIntegrator":
            registry_name = "maven"
        elif class_name == "NuGetIntegrator":
            registry_name = "nuget"
        elif class_name == "RubyGemsIntegrator":
            registry_name = "rubygems"
        else:
            registry_name = class_name.replace("Integrator", "").lower()

        if not version:
            cached = await cache.get(registry_name, package_name)
            if cached:
                logger.debug("Cache hit for %s:%s", registry_name, package_name)
                return cached

        metadata = await self._fetch_package_metadata(package_name, version)

        if not version:
            await cache.set(registry_name, package_name, metadata)

        return metadata

    async def _fetch_package_metadata(self, package_name: str, version: str | None = None) -> dict[str, Any]:
        """Fetch package metadata from registry (to be implemented by subclasses).

        Args:
            package_name: Package name
            version: Optional version

        Returns:
            Package metadata dictionary

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement _fetch_package_metadata")

    async def search_packages(self, query: str, limit: int = 100) -> list[dict[str, Any]]:
        """Search packages in registry.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of package metadata dictionaries

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement search_packages")

    async def get_package_source(self, package_name: str, version: str | None = None) -> dict[str, str]:
        """Get package source code files.

        Args:
            package_name: Package name
            version: Optional version

        Returns:
            Dictionary mapping file paths to content

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement get_package_source")


class PyPIIntegrator(PackageRegistryIntegrator):
    """PyPI (Python Package Index) integrator."""

    BASE_URL = "https://pypi.org/pypi"

    async def _fetch_package_metadata(self, package_name: str, version: str | None = None) -> dict[str, Any]:
        """Fetch package metadata from PyPI.

        Args:
            package_name: Package name
            version: Optional version (defaults to latest)

        Returns:
            Package metadata dictionary
        """
        try:
            url = f"{self.BASE_URL}/{package_name}/json"
            if version:
                url = f"{self.BASE_URL}/{package_name}/{version}/json"

            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()

            info = data.get("info", {})
            releases = data.get("releases", {})

            latest_version = info.get("version", "")
            if not version:
                version = latest_version

            release_data = releases.get(version, [])
            source_url = None
            for release in release_data:
                if release.get("packagetype") == "sdist":
                    source_url = release.get("url")
                    break

            github_url = None
            project_urls = info.get("project_urls", {}) or {}
            for url_key in ["Homepage", "Source", "Repository", "Code"]:
                url_value = project_urls.get(url_key, "")
                if url_value and "github.com" in url_value:
                    github_url = url_value
                    break

            return {
                "package_id": package_name,
                "registry": "pypi",
                "name": package_name,
                "version": version,
                "latest_version": latest_version,
                "description": info.get("summary", ""),
                "keywords": info.get("keywords", "").split(",") if info.get("keywords") else [],
                "classifiers": info.get("classifiers", []),
                "homepage": info.get("home_page") or project_urls.get("Homepage"),
                "github_url": github_url,
                "source_url": source_url,
                "author": info.get("author", ""),
                "author_email": info.get("author_email", ""),
                "license": info.get("license", ""),
                "requires_python": info.get("requires_python"),
                "downloads": self._get_download_count(data),
                "created_at": info.get("upload_time"),
            }
        except httpx.HTTPError as e:
            logger.error("Failed to fetch PyPI package %s: %s", package_name, e)
            raise RuntimeError(f"Failed to fetch PyPI package {package_name}: {e}") from e

    async def search_packages(self, query: str, limit: int = 100) -> list[dict[str, Any]]:
        """Search packages in PyPI.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of package metadata dictionaries
        """
        try:
            url = "https://pypi.org/search"
            params = {"q": query, "c": "Package"}
            response = await self.client.get(url, params=params)
            response.raise_for_status()

            packages = []
            html_content = response.text

            import re
            from html import unescape

            pattern = r'<a[^>]*href="/project/([^/]+)/"[^>]*>([^<]+)</a>'
            matches = re.findall(pattern, html_content)

            for package_name, package_title in matches[:limit]:
                try:
                    metadata = await self.get_package_metadata(package_name)
                    packages.append(metadata)
                except Exception as e:
                    logger.warning("Failed to fetch metadata for PyPI package %s: %s", package_name, e)
                    continue

            return packages
        except httpx.HTTPError as e:
            logger.error("Failed to search PyPI packages: %s", e)
            raise RuntimeError(f"Failed to search PyPI packages: {e}") from e

    async def get_package_source(self, package_name: str, version: str | None = None) -> dict[str, str]:
        """Get package source code from PyPI.

        Args:
            package_name: Package name
            version: Optional version

        Returns:
            Dictionary mapping file paths to content
        """
        metadata = await self.get_package_metadata(package_name, version)
        github_url = metadata.get("github_url")

        if github_url:
            try:
                return await self._fetch_from_github(github_url)
            except Exception as e:
                logger.warning("Failed to fetch from GitHub, trying PyPI source: %s", e)

        source_url = metadata.get("source_url")
        if source_url:
            try:
                return await self._fetch_from_pypi_source(source_url)
            except Exception as e:
                logger.warning("Failed to fetch from PyPI source: %s", e)

        return {}

    def _get_download_count(self, data: dict[str, Any]) -> int:
        """Extract download count from PyPI data."""
        urls = data.get("urls", [])
        total_downloads = sum(url.get("downloads", 0) for url in urls)
        return total_downloads

    async def _fetch_from_github(self, github_url: str) -> dict[str, str]:
        """Fetch source code from GitHub."""
        import re

        match = re.search(r"github\.com/([^/]+)/([^/]+)", github_url)
        if not match:
            return {}

        owner, repo = match.groups()
        repo = repo.rstrip(".git")

        api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
        headers = {"Accept": "application/vnd.github.v3+json"}

        try:
            response = await self.client.get(api_url, headers=headers)
            response.raise_for_status()
            tree_data = response.json()

            files = {}
            for item in tree_data.get("tree", []):
                if item.get("type") == "blob" and item.get("path", "").endswith((".py", ".yaml", ".yml", ".tf", ".md")):
                    file_url = item.get("url")
                    if file_url:
                        file_response = await self.client.get(file_url, headers=headers)
                        file_response.raise_for_status()
                        file_data = file_response.json()
                        import base64

                        content = base64.b64decode(file_data.get("content", "")).decode("utf-8")
                        files[item.get("path", "")] = content

            return files
        except Exception as e:
            logger.warning("Failed to fetch from GitHub: %s", e)
            return {}

    async def _fetch_from_pypi_source(self, source_url: str) -> dict[str, str]:
        """Fetch source code from PyPI source distribution."""
        return {}


class NPMIntegrator(PackageRegistryIntegrator):
    """NPM (Node Package Manager) integrator."""

    BASE_URL = "https://registry.npmjs.org"

    async def _fetch_package_metadata(self, package_name: str, version: str | None = None) -> dict[str, Any]:
        """Fetch package metadata from NPM.

        Args:
            package_name: Package name
            version: Optional version (defaults to latest)

        Returns:
            Package metadata dictionary
        """
        try:
            url = f"{self.BASE_URL}/{package_name}"
            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()

            dist_tags = data.get("dist-tags", {})
            latest_version = dist_tags.get("latest", "")
            if not version:
                version = latest_version

            version_data = data.get("versions", {}).get(version, {})
            if not version_data:
                version_data = data.get("versions", {}).get(latest_version, {})

            repository = version_data.get("repository", {})
            github_url = None
            if isinstance(repository, dict):
                github_url = repository.get("url", "")
            elif isinstance(repository, str):
                github_url = repository

            if github_url and github_url.startswith("git+"):
                github_url = github_url[4:]
            if github_url and github_url.endswith(".git"):
                github_url = github_url[:-4]

            return {
                "package_id": package_name,
                "registry": "npm",
                "name": package_name,
                "version": version,
                "latest_version": latest_version,
                "description": version_data.get("description", ""),
                "keywords": version_data.get("keywords", []),
                "homepage": version_data.get("homepage"),
                "github_url": github_url,
                "author": version_data.get("author", {}),
                "license": version_data.get("license"),
                "main": version_data.get("main"),
                "dependencies": version_data.get("dependencies", {}),
                "downloads": self._get_download_count(data),
                "created_at": data.get("time", {}).get(version),
            }
        except httpx.HTTPError as e:
            logger.error("Failed to fetch NPM package %s: %s", package_name, e)
            raise RuntimeError(f"Failed to fetch NPM package {package_name}: {e}") from e

    async def search_packages(self, query: str, limit: int = 100) -> list[dict[str, Any]]:
        """Search packages in NPM.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of package metadata dictionaries
        """
        try:
            url = "https://registry.npmjs.org/-/v1/search"
            params = {"text": query, "size": limit}
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            packages = []
            for item in data.get("objects", [])[:limit]:
                package_data = item.get("package", {})
                package_name = package_data.get("name", "")
                if package_name:
                    try:
                        metadata = await self.get_package_metadata(package_name)
                        packages.append(metadata)
                    except Exception as e:
                        logger.warning("Failed to fetch metadata for NPM package %s: %s", package_name, e)
                        continue

            return packages
        except httpx.HTTPError as e:
            logger.error("Failed to search NPM packages: %s", e)
            raise RuntimeError(f"Failed to search NPM packages: {e}") from e

    async def get_package_source(self, package_name: str, version: str | None = None) -> dict[str, str]:
        """Get package source code from NPM.

        Args:
            package_name: Package name
            version: Optional version

        Returns:
            Dictionary mapping file paths to content
        """
        metadata = await self.get_package_metadata(package_name, version)
        github_url = metadata.get("github_url")

        if github_url:
            try:
                return await self._fetch_from_github(github_url)
            except Exception as e:
                logger.warning("Failed to fetch from GitHub: %s", e)

        tarball_url = metadata.get("tarball_url")
        if tarball_url:
            try:
                return await self._fetch_from_tarball(tarball_url)
            except Exception as e:
                logger.warning("Failed to fetch from tarball: %s", e)

        return {}

    def _get_download_count(self, data: dict[str, Any]) -> int:
        """Extract download count from NPM data."""
        return data.get("downloads", {}).get("all", 0) if isinstance(data.get("downloads"), dict) else 0

    async def _fetch_from_github(self, github_url: str) -> dict[str, str]:
        """Fetch source code from GitHub."""
        import re

        match = re.search(r"github\.com/([^/]+)/([^/]+)", github_url)
        if not match:
            return {}

        owner, repo = match.groups()
        repo = repo.rstrip(".git")

        api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
        headers = {"Accept": "application/vnd.github.v3+json"}

        try:
            response = await self.client.get(api_url, headers=headers)
            response.raise_for_status()
            tree_data = response.json()

            files = {}
            for item in tree_data.get("tree", []):
                if item.get("type") == "blob" and item.get("path", "").endswith((".ts", ".js", ".tsx", ".jsx", ".json", ".yaml", ".yml", ".md")):
                    file_url = item.get("url")
                    if file_url:
                        file_response = await self.client.get(file_url, headers=headers)
                        file_response.raise_for_status()
                        file_data = file_response.json()
                        import base64

                        content = base64.b64decode(file_data.get("content", "")).decode("utf-8")
                        files[item.get("path", "")] = content

            return files
        except Exception as e:
            logger.warning("Failed to fetch from GitHub: %s", e)
            return {}

    async def _fetch_from_tarball(self, tarball_url: str) -> dict[str, str]:
        """Fetch source code from NPM tarball."""
        return {}


class TerraformRegistryIntegrator(PackageRegistryIntegrator):
    """Terraform Registry integrator."""

    BASE_URL = "https://registry.terraform.io/v1"

    async def _fetch_package_metadata(self, package_name: str, version: str | None = None) -> dict[str, Any]:
        """Fetch module/provider metadata from Terraform Registry.

        Args:
            package_name: Module/provider name (format: namespace/name/provider)
            version: Optional version

        Returns:
            Package metadata dictionary
        """
        try:
            parts = package_name.split("/")
            if len(parts) < 2:
                raise ValueError(f"Invalid Terraform package name: {package_name}. Expected format: namespace/name or namespace/name/provider")

            namespace = parts[0]
            name = parts[1]
            provider = parts[2] if len(parts) > 2 else None

            if provider:
                url = f"{self.BASE_URL}/modules/{namespace}/{name}/{provider}"
            else:
                url = f"{self.BASE_URL}/providers/{namespace}/{name}"

            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()

            source = data.get("source", "")
            github_url = None
            if "github.com" in source:
                github_url = source

            return {
                "package_id": package_name,
                "registry": "terraform",
                "name": package_name,
                "namespace": namespace,
                "module_name": name,
                "provider": provider,
                "version": version or data.get("version", ""),
                "description": data.get("description", ""),
                "source": source,
                "github_url": github_url,
                "downloads": data.get("downloads", 0),
                "published_at": data.get("published_at"),
                "created_at": data.get("created_at"),
            }
        except httpx.HTTPError as e:
            logger.error("Failed to fetch Terraform package %s: %s", package_name, e)
            raise RuntimeError(f"Failed to fetch Terraform package {package_name}: {e}") from e

    async def search_packages(self, query: str, limit: int = 100) -> list[dict[str, Any]]:
        """Search modules/providers in Terraform Registry.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of package metadata dictionaries
        """
        try:
            url = f"{self.BASE_URL}/modules"
            params = {"q": query, "limit": limit}
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            packages = []
            for item in data.get("modules", [])[:limit]:
                namespace = item.get("namespace", "")
                name = item.get("name", "")
                provider = item.get("provider", "")
                package_name = f"{namespace}/{name}/{provider}" if provider else f"{namespace}/{name}"

                try:
                    metadata = await self.get_package_metadata(package_name)
                    packages.append(metadata)
                except Exception as e:
                    logger.warning("Failed to fetch metadata for Terraform package %s: %s", package_name, e)
                    continue

            return packages
        except httpx.HTTPError as e:
            logger.error("Failed to search Terraform packages: %s", e)
            raise RuntimeError(f"Failed to search Terraform packages: {e}") from e

    async def get_package_source(self, package_name: str, version: str | None = None) -> dict[str, str]:
        """Get package source code from Terraform Registry.

        Args:
            package_name: Package name
            version: Optional version

        Returns:
            Dictionary mapping file paths to content
        """
        metadata = await self.get_package_metadata(package_name, version)
        github_url = metadata.get("github_url")

        if github_url:
            try:
                return await self._fetch_from_github(github_url)
            except Exception as e:
                logger.warning("Failed to fetch from GitHub: %s", e)

        return {}

    async def _fetch_from_github(self, github_url: str) -> dict[str, str]:
        """Fetch source code from GitHub."""
        import re

        match = re.search(r"github\.com/([^/]+)/([^/]+)", github_url)
        if not match:
            return {}

        owner, repo = match.groups()
        repo = repo.rstrip(".git")

        api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
        headers = {"Accept": "application/vnd.github.v3+json"}

        try:
            response = await self.client.get(api_url, headers=headers)
            response.raise_for_status()
            tree_data = response.json()

            files = {}
            for item in tree_data.get("tree", []):
                if item.get("type") == "blob" and item.get("path", "").endswith((".tf", ".tfvars", ".hcl", ".yaml", ".yml", ".md")):
                    file_url = item.get("url")
                    if file_url:
                        file_response = await self.client.get(file_url, headers=headers)
                        file_response.raise_for_status()
                        file_data = file_response.json()
                        import base64

                        content = base64.b64decode(file_data.get("content", "")).decode("utf-8")
                        files[item.get("path", "")] = content

            return files
        except Exception as e:
            logger.warning("Failed to fetch from GitHub: %s", e)
            return {}


class CratesIOIntegrator(PackageRegistryIntegrator):
    """Crates.io (Rust Package Registry) integrator."""

    BASE_URL = "https://crates.io/api/v1"

    async def _fetch_package_metadata(self, package_name: str, version: str | None = None) -> dict[str, Any]:
        """Fetch package metadata from Crates.io.

        Args:
            package_name: Package name
            version: Optional version (defaults to latest)

        Returns:
            Package metadata dictionary
        """
        try:
            url = f"{self.BASE_URL}/crates/{package_name}"
            if version:
                url = f"{self.BASE_URL}/crates/{package_name}/{version}"

            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()

            crate_data = data.get("crate", {})
            version_data = data.get("versions", [{}])[0] if data.get("versions") else {}

            if version:
                for v in data.get("versions", []):
                    if v.get("num") == version:
                        version_data = v
                        break

            repository = crate_data.get("repository", "")
            github_url = None
            if repository and "github.com" in repository:
                github_url = repository.rstrip(".git")

            return {
                "package_id": package_name,
                "registry": "crates_io",
                "name": package_name,
                "version": version or version_data.get("num", ""),
                "latest_version": crate_data.get("newest_version", ""),
                "description": crate_data.get("description", ""),
                "keywords": [k.get("id", "") for k in crate_data.get("keywords", [])],
                "categories": [c.get("id", "") for c in crate_data.get("categories", [])],
                "homepage": crate_data.get("homepage"),
                "github_url": github_url,
                "repository": repository,
                "documentation": crate_data.get("documentation"),
                "downloads": crate_data.get("downloads", 0),
                "created_at": crate_data.get("created_at"),
                "updated_at": crate_data.get("updated_at"),
            }
        except httpx.HTTPError as e:
            logger.error("Failed to fetch Crates.io package %s: %s", package_name, e)
            raise RuntimeError(f"Failed to fetch Crates.io package {package_name}: {e}") from e

    async def search_packages(self, query: str, limit: int = 100) -> list[dict[str, Any]]:
        """Search packages in Crates.io.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of package metadata dictionaries
        """
        try:
            url = f"{self.BASE_URL}/crates"
            params = {"q": query, "per_page": min(limit, 100)}
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            packages = []
            for crate in data.get("crates", [])[:limit]:
                package_name = crate.get("name", "")
                if package_name:
                    try:
                        metadata = await self.get_package_metadata(package_name)
                        packages.append(metadata)
                    except Exception as e:
                        logger.warning("Failed to fetch metadata for Crates.io package %s: %s", package_name, e)
                        continue

            return packages
        except httpx.HTTPError as e:
            logger.error("Failed to search Crates.io packages: %s", e)
            raise RuntimeError(f"Failed to search Crates.io packages: {e}") from e

    async def get_package_source(self, package_name: str, version: str | None = None) -> dict[str, str]:
        """Get package source code from Crates.io.

        Args:
            package_name: Package name
            version: Optional version

        Returns:
            Dictionary mapping file paths to content
        """
        metadata = await self.get_package_metadata(package_name, version)
        github_url = metadata.get("github_url")

        if github_url:
            try:
                return await self._fetch_from_github(github_url)
            except Exception as e:
                logger.warning("Failed to fetch from GitHub: %s", e)

        return {}

    async def _fetch_from_github(self, github_url: str) -> dict[str, str]:
        """Fetch source code from GitHub."""
        import re

        match = re.search(r"github\.com/([^/]+)/([^/]+)", github_url)
        if not match:
            return {}

        owner, repo = match.groups()
        repo = repo.rstrip(".git")

        api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
        headers = {"Accept": "application/vnd.github.v3+json"}

        try:
            response = await self.client.get(api_url, headers=headers)
            response.raise_for_status()
            tree_data = response.json()

            files = {}
            for item in tree_data.get("tree", []):
                if item.get("type") == "blob" and item.get("path", "").endswith((".rs", ".toml", ".md")):
                    file_url = item.get("url")
                    if file_url:
                        file_response = await self.client.get(file_url, headers=headers)
                        file_response.raise_for_status()
                        file_data = file_response.json()
                        import base64

                        content = base64.b64decode(file_data.get("content", "")).decode("utf-8")
                        files[item.get("path", "")] = content

            return files
        except Exception as e:
            logger.warning("Failed to fetch from GitHub: %s", e)
            return {}


class GoModulesIntegrator(PackageRegistryIntegrator):
    """Go Modules (Go Package Registry) integrator."""

    BASE_URL = "https://proxy.golang.org"

    async def _fetch_package_metadata(self, package_name: str, version: str | None = None) -> dict[str, Any]:
        """Fetch package metadata from Go Modules proxy.

        Args:
            package_name: Module path (e.g., "golang.org/x/tools")
            version: Optional version (defaults to latest)

        Returns:
            Package metadata dictionary
        """
        try:
            if not version:
                versions_url = f"{self.BASE_URL}/{package_name}/@v/list"
                versions_response = await self.client.get(versions_url)
                versions_response.raise_for_status()
                versions_text = versions_response.text.strip()
                versions = [v.strip() for v in versions_text.split("\n") if v.strip()]
                if versions:
                    version = versions[-1]

            if not version:
                raise RuntimeError(f"No versions found for Go module {package_name}")

            info_url = f"{self.BASE_URL}/{package_name}/@v/{version}.info"
            info_response = await self.client.get(info_url)
            info_response.raise_for_status()
            info_data = info_response.json()

            mod_url = f"{self.BASE_URL}/{package_name}/@v/{version}.mod"
            mod_response = await self.client.get(mod_url)
            mod_response.raise_for_status()
            mod_content = mod_response.text

            github_url = None
            if "github.com" in package_name:
                github_url = f"https://{package_name}"

            return {
                "package_id": package_name,
                "registry": "golang",
                "name": package_name,
                "version": version,
                "latest_version": version,
                "description": self._extract_description_from_mod(mod_content),
                "github_url": github_url,
                "module_path": package_name,
                "go_version": info_data.get("Version", ""),
                "time": info_data.get("Time", ""),
            }
        except httpx.HTTPError as e:
            logger.error("Failed to fetch Go module %s: %s", package_name, e)
            raise RuntimeError(f"Failed to fetch Go module {package_name}: {e}") from e

    def _extract_description_from_mod(self, mod_content: str) -> str:
        """Extract description from go.mod content."""
        lines = mod_content.split("\n")
        for line in lines[:10]:
            if line.startswith("module "):
                return f"Go module: {line.split()[1] if len(line.split()) > 1 else ''}"
        return "Go module"

    async def search_packages(self, query: str, limit: int = 100) -> list[dict[str, Any]]:
        """Search packages in Go Modules (via pkg.go.dev).

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of package metadata dictionaries
        """
        try:
            search_url = "https://pkg.go.dev/search"
            params = {"q": query, "limit": limit}
            response = await self.client.get(search_url, params=params)
            response.raise_for_status()

            from bs4 import BeautifulSoup

            soup = BeautifulSoup(response.text, "html.parser")
            packages = []

            for result in soup.find_all("div", class_="SearchSnippet")[:limit]:
                try:
                    title_elem = result.find("h2", class_="SearchSnippet-headerContainer")
                    if title_elem:
                        link = title_elem.find("a")
                        if link:
                            module_path = link.get("href", "").replace("/", "")
                            if module_path.startswith("github.com") or module_path.startswith("golang.org"):
                                try:
                                    metadata = await self.get_package_metadata(module_path)
                                    packages.append(metadata)
                                except Exception as e:
                                    logger.warning("Failed to fetch metadata for Go module %s: %s", module_path, e)
                                    continue
                except Exception as e:
                    logger.warning("Failed to parse Go module search result: %s", e)
                    continue

            return packages
        except Exception as e:
            logger.error("Failed to search Go modules: %s", e)
            return []

    async def get_package_source(self, package_name: str, version: str | None = None) -> dict[str, str]:
        """Get package source code from Go Modules.

        Args:
            package_name: Module path
            version: Optional version

        Returns:
            Dictionary mapping file paths to content
        """
        metadata = await self.get_package_metadata(package_name, version)
        github_url = metadata.get("github_url")

        if github_url:
            try:
                return await self._fetch_from_github(github_url)
            except Exception as e:
                logger.warning("Failed to fetch from GitHub: %s", e)

        return {}

    async def _fetch_from_github(self, github_url: str) -> dict[str, str]:
        """Fetch source code from GitHub."""
        import re

        match = re.search(r"github\.com/([^/]+)/([^/]+)", github_url)
        if not match:
            return {}

        owner, repo = match.groups()
        repo = repo.rstrip(".git")

        api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
        headers = {"Accept": "application/vnd.github.v3+json"}

        try:
            response = await self.client.get(api_url, headers=headers)
            response.raise_for_status()
            tree_data = response.json()

            files = {}
            for item in tree_data.get("tree", []):
                if item.get("type") == "blob" and item.get("path", "").endswith((".go", ".mod", ".md")):
                    file_url = item.get("url")
                    if file_url:
                        file_response = await self.client.get(file_url, headers=headers)
                        file_response.raise_for_status()
                        file_data = file_response.json()
                        import base64

                        content = base64.b64decode(file_data.get("content", "")).decode("utf-8")
                        files[item.get("path", "")] = content

            return files
        except Exception as e:
            logger.warning("Failed to fetch from GitHub: %s", e)
            return {}


class HelmChartsIntegrator(PackageRegistryIntegrator):
    """Helm Charts (Artifact Hub) integrator."""

    BASE_URL = "https://artifacthub.io/api/v1"

    async def _fetch_package_metadata(self, package_name: str, version: str | None = None) -> dict[str, Any]:
        """Fetch Helm chart metadata from Artifact Hub.

        Args:
            package_name: Chart name (format: repo/chart-name)
            version: Optional version (defaults to latest)

        Returns:
            Package metadata dictionary
        """
        try:
            parts = package_name.split("/")
            if len(parts) != 2:
                raise ValueError(f"Invalid Helm chart name: {package_name}. Expected format: repo/chart-name")

            repo_name, chart_name = parts

            url = f"{self.BASE_URL}/packages/helm/{repo_name}/{chart_name}"
            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()

            latest_version = data.get("version", "")
            if version:
                versions_url = f"{self.BASE_URL}/packages/helm/{repo_name}/{chart_name}/versions"
                versions_response = await self.client.get(versions_url)
                versions_response.raise_for_status()
                versions_data = versions_response.json()
                for v in versions_data:
                    if v.get("version") == version:
                        data = v
                        break

            repository_url = data.get("repository", {}).get("url", "")
            github_url = None
            if "github.com" in repository_url:
                github_url = repository_url.rstrip(".git")

            return {
                "package_id": package_name,
                "registry": "helm",
                "name": package_name,
                "version": version or latest_version,
                "latest_version": latest_version,
                "description": data.get("description", ""),
                "keywords": data.get("keywords", []),
                "homepage": data.get("home_url"),
                "github_url": github_url,
                "repository_url": repository_url,
                "maintainers": data.get("maintainers", []),
                "app_version": data.get("app_version", ""),
                "created_at": data.get("ts", 0),
            }
        except httpx.HTTPError as e:
            logger.error("Failed to fetch Helm chart %s: %s", package_name, e)
            raise RuntimeError(f"Failed to fetch Helm chart {package_name}: {e}") from e

    async def search_packages(self, query: str, limit: int = 100) -> list[dict[str, Any]]:
        """Search Helm charts in Artifact Hub.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of package metadata dictionaries
        """
        try:
            url = f"{self.BASE_URL}/packages/search"
            params = {"kind": 0, "ts_query_web": query, "limit": min(limit, 60)}
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            packages = []
            for package in data.get("packages", [])[:limit]:
                if package.get("kind") == 0:
                    repo_name = package.get("repository", {}).get("name", "")
                    chart_name = package.get("name", "")
                    package_id = f"{repo_name}/{chart_name}"
                    try:
                        metadata = await self.get_package_metadata(package_id)
                        packages.append(metadata)
                    except Exception as e:
                        logger.warning("Failed to fetch metadata for Helm chart %s: %s", package_id, e)
                        continue

            return packages
        except httpx.HTTPError as e:
            logger.error("Failed to search Helm charts: %s", e)
            raise RuntimeError(f"Failed to search Helm charts: {e}") from e

    async def get_package_source(self, package_name: str, version: str | None = None) -> dict[str, str]:
        """Get Helm chart source files.

        Args:
            package_name: Chart name
            version: Optional version

        Returns:
            Dictionary mapping file paths to content
        """
        metadata = await self.get_package_metadata(package_name, version)
        github_url = metadata.get("github_url")

        if github_url:
            try:
                return await self._fetch_from_github(github_url)
            except Exception as e:
                logger.warning("Failed to fetch from GitHub: %s", e)

        return {}

    async def _fetch_from_github(self, github_url: str) -> dict[str, str]:
        """Fetch source code from GitHub."""
        import re

        match = re.search(r"github\.com/([^/]+)/([^/]+)", github_url)
        if not match:
            return {}

        owner, repo = match.groups()
        repo = repo.rstrip(".git")

        api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
        headers = {"Accept": "application/vnd.github.v3+json"}

        try:
            response = await self.client.get(api_url, headers=headers)
            response.raise_for_status()
            tree_data = response.json()

            files = {}
            for item in tree_data.get("tree", []):
                if item.get("type") == "blob" and item.get("path", "").endswith((".yaml", ".yml", ".tpl", ".md", "Chart.yaml", "values.yaml")):
                    file_url = item.get("url")
                    if file_url:
                        file_response = await self.client.get(file_url, headers=headers)
                        file_response.raise_for_status()
                        file_data = file_response.json()
                        import base64

                        content = base64.b64decode(file_data.get("content", "")).decode("utf-8")
                        files[item.get("path", "")] = content

            return files
        except Exception as e:
            logger.warning("Failed to fetch from GitHub: %s", e)
            return {}


class AnsibleGalaxyIntegrator(PackageRegistryIntegrator):
    """Ansible Galaxy integrator."""

    BASE_URL = "https://galaxy.ansible.com/api/v1"

    async def _fetch_package_metadata(self, package_name: str, version: str | None = None) -> dict[str, Any]:
        """Fetch Ansible role/collection metadata from Galaxy.

        Args:
            package_name: Role/collection name (format: namespace.name or namespace/name)
            version: Optional version (defaults to latest)

        Returns:
            Package metadata dictionary
        """
        try:
            package_name = package_name.replace("/", ".")
            parts = package_name.split(".")
            if len(parts) < 2:
                raise ValueError(f"Invalid Ansible package name: {package_name}. Expected format: namespace.name")

            namespace = parts[0]
            name = ".".join(parts[1:])

            url = f"{self.BASE_URL}/roles/?namespace__name={namespace}&name={name}"
            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()

            if not data.get("results"):
                raise RuntimeError(f"Ansible role {package_name} not found")

            role_data = data["results"][0]
            latest_version = role_data.get("summary_fields", {}).get("versions", [{}])[0].get("name", "")
            if not version:
                version = latest_version

            github_url = role_data.get("github_branch", "")
            if github_url and "github.com" not in github_url:
                github_url = role_data.get("github_repo", "")

            return {
                "package_id": package_name,
                "registry": "ansible",
                "name": package_name,
                "version": version or latest_version,
                "latest_version": latest_version,
                "description": role_data.get("description", ""),
                "tags": [t.get("name", "") for t in role_data.get("summary_fields", {}).get("tags", [])],
                "github_url": github_url,
                "download_count": role_data.get("download_count", 0),
                "created_at": role_data.get("created"),
                "modified_at": role_data.get("modified"),
            }
        except httpx.HTTPError as e:
            logger.error("Failed to fetch Ansible role %s: %s", package_name, e)
            raise RuntimeError(f"Failed to fetch Ansible role {package_name}: {e}") from e

    async def search_packages(self, query: str, limit: int = 100) -> list[dict[str, Any]]:
        """Search Ansible roles in Galaxy.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of package metadata dictionaries
        """
        try:
            url = f"{self.BASE_URL}/roles/"
            params = {"page_size": min(limit, 100), "search": query}
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            packages = []
            for role in data.get("results", [])[:limit]:
                namespace = role.get("summary_fields", {}).get("namespace", {}).get("name", "")
                name = role.get("name", "")
                package_id = f"{namespace}.{name}"
                try:
                    metadata = await self.get_package_metadata(package_id)
                    packages.append(metadata)
                except Exception as e:
                    logger.warning("Failed to fetch metadata for Ansible role %s: %s", package_id, e)
                    continue

            return packages
        except httpx.HTTPError as e:
            logger.error("Failed to search Ansible roles: %s", e)
            raise RuntimeError(f"Failed to search Ansible roles: {e}") from e

    async def get_package_source(self, package_name: str, version: str | None = None) -> dict[str, str]:
        """Get Ansible role source files.

        Args:
            package_name: Role name
            version: Optional version

        Returns:
            Dictionary mapping file paths to content
        """
        metadata = await self.get_package_metadata(package_name, version)
        github_url = metadata.get("github_url")

        if github_url:
            try:
                return await self._fetch_from_github(github_url)
            except Exception as e:
                logger.warning("Failed to fetch from GitHub: %s", e)

        return {}

    async def _fetch_from_github(self, github_url: str) -> dict[str, str]:
        """Fetch source code from GitHub."""
        import re

        match = re.search(r"github\.com/([^/]+)/([^/]+)", github_url)
        if not match:
            return {}

        owner, repo = match.groups()
        repo = repo.rstrip(".git")

        api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
        headers = {"Accept": "application/vnd.github.v3+json"}

        try:
            response = await self.client.get(api_url, headers=headers)
            response.raise_for_status()
            tree_data = response.json()

            files = {}
            for item in tree_data.get("tree", []):
                if item.get("type") == "blob" and item.get("path", "").endswith((".yml", ".yaml", ".py", ".md", "tasks", "handlers", "vars", "defaults")):
                    file_url = item.get("url")
                    if file_url:
                        file_response = await self.client.get(file_url, headers=headers)
                        file_response.raise_for_status()
                        file_data = file_response.json()
                        import base64

                        content = base64.b64decode(file_data.get("content", "")).decode("utf-8")
                        files[item.get("path", "")] = content

            return files
        except Exception as e:
            logger.warning("Failed to fetch from GitHub: %s", e)
            return {}


class MavenCentralIntegrator(PackageRegistryIntegrator):
    """Maven Central (Java packages) integrator."""

    BASE_URL = "https://search.maven.org/solrsearch/select"

    async def _fetch_package_metadata(self, package_name: str, version: str | None = None) -> dict[str, Any]:
        """Fetch Maven package metadata.

        Args:
            package_name: Maven coordinates (format: groupId:artifactId)
            version: Optional version (defaults to latest)

        Returns:
            Package metadata dictionary
        """
        try:
            parts = package_name.split(":")
            if len(parts) < 2:
                raise ValueError(f"Invalid Maven coordinates: {package_name}. Expected format: groupId:artifactId")

            group_id = parts[0]
            artifact_id = parts[1]

            search_url = f"{self.BASE_URL}?q=g:{group_id}+AND+a:{artifact_id}&rows=1&wt=json"
            search_response = await self.client.get(search_url)
            search_response.raise_for_status()
            search_data = search_response.json()

            docs = search_data.get("response", {}).get("docs", [])
            if not docs:
                raise RuntimeError(f"Maven package {package_name} not found")

            doc = docs[0]
            latest_version = doc.get("latestVersion", "")

            if not version:
                version = latest_version

            github_url = None
            if doc.get("ec"):
                for ext in doc.get("ec", []):
                    if "source" in ext.lower():
                        source_url = f"https://repo1.maven.org/maven2/{group_id.replace('.', '/')}/{artifact_id}/{version}/{artifact_id}-{version}-sources.jar"
                        break

            return {
                "package_id": package_name,
                "registry": "maven",
                "name": package_name,
                "group_id": group_id,
                "artifact_id": artifact_id,
                "version": version or latest_version,
                "latest_version": latest_version,
                "description": doc.get("description", ""),
                "github_url": github_url,
                "download_count": doc.get("downloadCount", 0),
                "created_at": doc.get("timestamp", 0),
            }
        except httpx.HTTPError as e:
            logger.error("Failed to fetch Maven package %s: %s", package_name, e)
            raise RuntimeError(f"Failed to fetch Maven package {package_name}: {e}") from e

    async def search_packages(self, query: str, limit: int = 100) -> list[dict[str, Any]]:
        """Search Maven packages.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of package metadata dictionaries
        """
        try:
            url = f"{self.BASE_URL}?q={query}&rows={min(limit, 100)}&wt=json"
            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()

            packages = []
            for doc in data.get("response", {}).get("docs", [])[:limit]:
                group_id = doc.get("g", "")
                artifact_id = doc.get("a", "")
                package_id = f"{group_id}:{artifact_id}"
                try:
                    metadata = await self.get_package_metadata(package_id)
                    packages.append(metadata)
                except Exception as e:
                    logger.warning("Failed to fetch metadata for Maven package %s: %s", package_id, e)
                    continue

            return packages
        except httpx.HTTPError as e:
            logger.error("Failed to search Maven packages: %s", e)
            raise RuntimeError(f"Failed to search Maven packages: {e}") from e

    async def get_package_source(self, package_name: str, version: str | None = None) -> dict[str, str]:
        """Get Maven package source code.

        Args:
            package_name: Maven coordinates
            version: Optional version

        Returns:
            Dictionary mapping file paths to content
        """
        metadata = await self.get_package_metadata(package_name, version)
        github_url = metadata.get("github_url")

        if github_url:
            try:
                return await self._fetch_from_github(github_url)
            except Exception as e:
                logger.warning("Failed to fetch from GitHub: %s", e)

        return {}

    async def _fetch_from_github(self, github_url: str) -> dict[str, str]:
        """Fetch source code from GitHub."""
        import re

        match = re.search(r"github\.com/([^/]+)/([^/]+)", github_url)
        if not match:
            return {}

        owner, repo = match.groups()
        repo = repo.rstrip(".git")

        api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
        headers = {"Accept": "application/vnd.github.v3+json"}

        try:
            response = await self.client.get(api_url, headers=headers)
            response.raise_for_status()
            tree_data = response.json()

            files = {}
            for item in tree_data.get("tree", []):
                if item.get("type") == "blob" and item.get("path", "").endswith((".java", ".xml", ".md", "pom.xml")):
                    file_url = item.get("url")
                    if file_url:
                        file_response = await self.client.get(file_url, headers=headers)
                        file_response.raise_for_status()
                        file_data = file_response.json()
                        import base64

                        content = base64.b64decode(file_data.get("content", "")).decode("utf-8")
                        files[item.get("path", "")] = content

            return files
        except Exception as e:
            logger.warning("Failed to fetch from GitHub: %s", e)
            return {}


class NuGetIntegrator(PackageRegistryIntegrator):
    """NuGet (.NET packages) integrator."""

    BASE_URL = "https://api.nuget.org/v3-flatcontainer"

    async def _fetch_package_metadata(self, package_name: str, version: str | None = None) -> dict[str, Any]:
        """Fetch NuGet package metadata.

        Args:
            package_name: Package name
            version: Optional version (defaults to latest)

        Returns:
            Package metadata dictionary
        """
        try:
            if not version:
                index_url = f"https://api.nuget.org/v3/registration5-semver1/{package_name.lower()}/index.json"
                index_response = await self.client.get(index_url)
                index_response.raise_for_status()
                index_data = index_response.json()

                if index_data.get("items"):
                    latest_item = index_data["items"][-1]
                    if latest_item.get("items"):
                        version = latest_item["items"][0].get("catalogEntry", {}).get("version", "")

            if not version:
                raise RuntimeError(f"No versions found for NuGet package {package_name}")

            catalog_url = f"https://api.nuget.org/v3/registration5-semver1/{package_name.lower()}/{version}.json"
            catalog_response = await self.client.get(catalog_url)
            catalog_response.raise_for_status()
            catalog_data = catalog_response.json()

            catalog_entry = catalog_data.get("catalogEntry", {})
            project_url = catalog_entry.get("projectUrl", "")
            github_url = None
            if "github.com" in project_url:
                github_url = project_url

            return {
                "package_id": package_name,
                "registry": "nuget",
                "name": package_name,
                "version": version,
                "latest_version": version,
                "description": catalog_entry.get("description", ""),
                "tags": catalog_entry.get("tags", "").split() if catalog_entry.get("tags") else [],
                "authors": catalog_entry.get("authors", ""),
                "homepage": catalog_entry.get("projectUrl"),
                "github_url": github_url,
                "license_url": catalog_entry.get("licenseUrl"),
                "download_count": catalog_entry.get("downloads", 0),
                "published": catalog_entry.get("published"),
            }
        except httpx.HTTPError as e:
            logger.error("Failed to fetch NuGet package %s: %s", package_name, e)
            raise RuntimeError(f"Failed to fetch NuGet package {package_name}: {e}") from e

    async def search_packages(self, query: str, limit: int = 100) -> list[dict[str, Any]]:
        """Search NuGet packages.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of package metadata dictionaries
        """
        try:
            search_url = "https://azuresearch-usnc.nuget.org/query"
            params = {"q": query, "take": min(limit, 100), "prerelease": "false"}
            response = await self.client.get(search_url, params=params)
            response.raise_for_status()
            data = response.json()

            packages = []
            for package in data.get("data", [])[:limit]:
                package_name = package.get("id", "")
                if package_name:
                    try:
                        metadata = await self.get_package_metadata(package_name)
                        packages.append(metadata)
                    except Exception as e:
                        logger.warning("Failed to fetch metadata for NuGet package %s: %s", package_name, e)
                        continue

            return packages
        except httpx.HTTPError as e:
            logger.error("Failed to search NuGet packages: %s", e)
            raise RuntimeError(f"Failed to search NuGet packages: {e}") from e

    async def get_package_source(self, package_name: str, version: str | None = None) -> dict[str, str]:
        """Get NuGet package source code.

        Args:
            package_name: Package name
            version: Optional version

        Returns:
            Dictionary mapping file paths to content
        """
        metadata = await self.get_package_metadata(package_name, version)
        github_url = metadata.get("github_url")

        if github_url:
            try:
                return await self._fetch_from_github(github_url)
            except Exception as e:
                logger.warning("Failed to fetch from GitHub: %s", e)

        return {}

    async def _fetch_from_github(self, github_url: str) -> dict[str, str]:
        """Fetch source code from GitHub."""
        import re

        match = re.search(r"github\.com/([^/]+)/([^/]+)", github_url)
        if not match:
            return {}

        owner, repo = match.groups()
        repo = repo.rstrip(".git")

        api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
        headers = {"Accept": "application/vnd.github.v3+json"}

        try:
            response = await self.client.get(api_url, headers=headers)
            response.raise_for_status()
            tree_data = response.json()

            files = {}
            for item in tree_data.get("tree", []):
                if item.get("type") == "blob" and item.get("path", "").endswith((".cs", ".csproj", ".sln", ".md", ".ps1")):
                    file_url = item.get("url")
                    if file_url:
                        file_response = await self.client.get(file_url, headers=headers)
                        file_response.raise_for_status()
                        file_data = file_response.json()
                        import base64

                        content = base64.b64decode(file_data.get("content", "")).decode("utf-8")
                        files[item.get("path", "")] = content

            return files
        except Exception as e:
            logger.warning("Failed to fetch from GitHub: %s", e)
            return {}


class RubyGemsIntegrator(PackageRegistryIntegrator):
    """RubyGems (Ruby packages) integrator."""

    BASE_URL = "https://rubygems.org/api/v1"

    async def _fetch_package_metadata(self, package_name: str, version: str | None = None) -> dict[str, Any]:
        """Fetch RubyGem metadata.

        Args:
            package_name: Gem name
            version: Optional version (defaults to latest)

        Returns:
            Package metadata dictionary
        """
        try:
            url = f"{self.BASE_URL}/gems/{package_name}.json"
            if version:
                url = f"{self.BASE_URL}/gems/{package_name}/versions/{version}.json"

            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()

            homepage = data.get("homepage_uri", "")
            source_code_uri = data.get("source_code_uri", "")
            github_url = None
            if source_code_uri and "github.com" in source_code_uri:
                github_url = source_code_uri
            elif homepage and "github.com" in homepage:
                github_url = homepage

            return {
                "package_id": package_name,
                "registry": "rubygems",
                "name": package_name,
                "version": version or data.get("version", ""),
                "latest_version": data.get("version", ""),
                "description": data.get("info", ""),
                "authors": data.get("authors", ""),
                "homepage": homepage,
                "github_url": github_url,
                "licenses": data.get("licenses", []),
                "download_count": data.get("downloads", 0),
                "created_at": data.get("created_at"),
            }
        except httpx.HTTPError as e:
            logger.error("Failed to fetch RubyGem %s: %s", package_name, e)
            raise RuntimeError(f"Failed to fetch RubyGem {package_name}: {e}") from e

    async def search_packages(self, query: str, limit: int = 100) -> list[dict[str, Any]]:
        """Search RubyGems.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of package metadata dictionaries
        """
        try:
            url = f"{self.BASE_URL}/search.json"
            params = {"query": query}
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            packages = []
            for gem in data[:limit]:
                package_name = gem.get("name", "")
                if package_name:
                    try:
                        metadata = await self.get_package_metadata(package_name)
                        packages.append(metadata)
                    except Exception as e:
                        logger.warning("Failed to fetch metadata for RubyGem %s: %s", package_name, e)
                        continue

            return packages
        except httpx.HTTPError as e:
            logger.error("Failed to search RubyGems: %s", e)
            raise RuntimeError(f"Failed to search RubyGems: {e}") from e

    async def get_package_source(self, package_name: str, version: str | None = None) -> dict[str, str]:
        """Get RubyGem source code.

        Args:
            package_name: Gem name
            version: Optional version

        Returns:
            Dictionary mapping file paths to content
        """
        metadata = await self.get_package_metadata(package_name, version)
        github_url = metadata.get("github_url")

        if github_url:
            try:
                return await self._fetch_from_github(github_url)
            except Exception as e:
                logger.warning("Failed to fetch from GitHub: %s", e)

        return {}

    async def _fetch_from_github(self, github_url: str) -> dict[str, str]:
        """Fetch source code from GitHub."""
        import re

        match = re.search(r"github\.com/([^/]+)/([^/]+)", github_url)
        if not match:
            return {}

        owner, repo = match.groups()
        repo = repo.rstrip(".git")

        api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
        headers = {"Accept": "application/vnd.github.v3+json"}

        try:
            response = await self.client.get(api_url, headers=headers)
            response.raise_for_status()
            tree_data = response.json()

            files = {}
            for item in tree_data.get("tree", []):
                if item.get("type") == "blob" and item.get("path", "").endswith((".rb", ".gemspec", ".md", "Rakefile", "Gemfile")):
                    file_url = item.get("url")
                    if file_url:
                        file_response = await self.client.get(file_url, headers=headers)
                        file_response.raise_for_status()
                        file_data = file_response.json()
                        import base64

                        content = base64.b64decode(file_data.get("content", "")).decode("utf-8")
                        files[item.get("path", "")] = content

            return files
        except Exception as e:
            logger.warning("Failed to fetch from GitHub: %s", e)
            return {}


class RegistryIntegratorFactory:
    """Factory for creating registry integrators."""

    @staticmethod
    def create(registry: str, timeout: float = 30.0) -> PackageRegistryIntegrator:
        """Create registry integrator for specified registry.

        Args:
            registry: Registry name (pypi, npm, terraform, crates_io, golang, helm, ansible, maven, nuget, rubygems)
            timeout: Request timeout

        Returns:
            Registry integrator instance

        Raises:
            ValueError: If registry not supported
        """
        if registry == "pypi":
            return PyPIIntegrator(timeout=timeout)
        elif registry == "npm":
            return NPMIntegrator(timeout=timeout)
        elif registry == "terraform":
            return TerraformRegistryIntegrator(timeout=timeout)
        elif registry == "crates_io":
            return CratesIOIntegrator(timeout=timeout)
        elif registry == "golang":
            return GoModulesIntegrator(timeout=timeout)
        elif registry == "helm":
            return HelmChartsIntegrator(timeout=timeout)
        elif registry == "ansible":
            return AnsibleGalaxyIntegrator(timeout=timeout)
        elif registry == "maven":
            return MavenCentralIntegrator(timeout=timeout)
        elif registry == "nuget":
            return NuGetIntegrator(timeout=timeout)
        elif registry == "rubygems":
            return RubyGemsIntegrator(timeout=timeout)
        else:
            raise ValueError(f"Unsupported registry: {registry}")

