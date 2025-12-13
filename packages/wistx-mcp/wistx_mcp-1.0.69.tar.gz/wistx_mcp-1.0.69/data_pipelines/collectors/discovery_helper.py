"""Helper functions for automated source discovery integration."""

from ..config.source_registry import (
    TRUSTED_DOMAINS,
    MANUAL_URLS,
    is_category_enabled,
    get_disabled_categories,
)
from .source_discovery import SourceDiscovery
from ..utils.logger import setup_logger
from ..utils.url_cache import url_cache

logger = setup_logger(__name__)


async def get_discovered_urls(
    domain: str,
    subdomain: str | None = None,
    use_cache: bool = True,
    disable_deep_crawl: bool = False,
    bypass_category_check: bool = False,
) -> dict[str, list[str]]:
    """Get discovered URLs for a domain using automated discovery.

    Falls back to manual URLs if automated discovery fails.
    Uses caching to reduce redundant discovery work.

    Note: Categories can be disabled in source_registry.py to prevent pre-crawling.
    Disabled categories will return empty results unless bypass_category_check=True.
    Use on-demand research for disabled categories instead.

    Args:
        domain: Knowledge domain (compliance, finops, architecture, etc.)
        subdomain: Optional subdomain filter (e.g., "PCI-DSS")
        use_cache: Use cache if available (default: True)
        disable_deep_crawl: If True, disable deep crawling (sitemap recursion) (default: False)
        bypass_category_check: If True, ignore category enabled/disabled status (default: False)
            Use this for on-demand research that needs to access disabled categories.

    Returns:
        Dictionary with "web_urls" and "pdf_urls" lists
    """
    # Check if category is enabled for pre-crawling
    if not bypass_category_check and not is_category_enabled(domain):
        logger.info(
            "Category '%s' is disabled for pre-crawling. "
            "Use on-demand research via research_knowledge_base tool instead. "
            "Disabled categories: %s",
            domain,
            get_disabled_categories(),
        )
        return {"web_urls": [], "pdf_urls": []}

    cache_key_kwargs = {
        "enable_rss": False,
        "enable_link_following": False,
    }

    if use_cache:
        cached_urls = url_cache.get(domain, subdomain, **cache_key_kwargs)
        if cached_urls:
            logger.info(
                "Using cached URLs for domain %s (subdomain: %s): %d web, %d PDF",
                domain,
                subdomain,
                len(cached_urls.get("web_urls", [])),
                len(cached_urls.get("pdf_urls", [])),
            )
            return cached_urls

    domain_configs = TRUSTED_DOMAINS.get(domain, {}).get("tier_1", [])

    all_web_urls: list[str] = []
    all_pdf_urls: list[str] = []

    if domain_configs:
        async with SourceDiscovery() as discovery:
            for domain_config in domain_configs:
                try:
                    if disable_deep_crawl:
                        domain_config = domain_config.copy()
                        domain_config["max_sitemap_depth"] = 0
                    discovered = await discovery.discover_all_for_domain(domain_config)
                    all_web_urls.extend(discovered["web_urls"])
                    all_pdf_urls.extend(discovered["pdf_urls"])
                    
                    enable_rss = domain_config.get("enable_rss_discovery", False)
                    enable_link_following = domain_config.get("enable_link_following", False)
                    cache_key_kwargs["enable_rss"] = enable_rss
                    cache_key_kwargs["enable_link_following"] = enable_link_following
                except (ValueError, RuntimeError, AttributeError, TypeError, ConnectionError) as e:
                    logger.warning(
                        "Failed to discover URLs from %s: %s",
                        domain_config.get("domain"),
                        e,
                    )

    domain_manual_urls = MANUAL_URLS.get(domain, {})
    
    if subdomain:
        manual_urls = domain_manual_urls.get(subdomain, [])
    else:
        manual_urls = []
        for urls in domain_manual_urls.values():
            manual_urls.extend(urls)

    if manual_urls:
        manual_pdf_urls = [url for url in manual_urls if url.endswith(".pdf")]
        manual_web_urls = [url for url in manual_urls if not url.endswith(".pdf")]
        all_web_urls.extend(manual_web_urls)
        all_pdf_urls.extend(manual_pdf_urls)
        logger.info(
            "Added %d manual URLs (%d web, %d PDF) for %s",
            len(manual_urls),
            len(manual_web_urls),
            len(manual_pdf_urls),
            subdomain or domain,
        )

    if not all_web_urls and not all_pdf_urls:
        logger.warning(
            "No URLs discovered for domain %s (subdomain: %s). "
            "Consider adding manual URLs to source_registry.py",
            domain,
            subdomain,
        )

    result = {
        "web_urls": list(set(all_web_urls)),
        "pdf_urls": list(set(all_pdf_urls)),
    }
    
    if use_cache and (all_web_urls or all_pdf_urls):
        url_cache.set(domain, result, subdomain, **cache_key_kwargs)
        logger.debug("Cached discovered URLs for domain %s (subdomain: %s)", domain, subdomain)

    return result


def get_all_urls_for_domain(domain: str) -> list[str]:
    """Get all URLs (web + PDF) for a domain.
    
    Convenience function that combines web and PDF URLs.
    
    Args:
        domain: Knowledge domain
        
    Returns:
        Combined list of all URLs
    """
    import asyncio

    discovered = asyncio.run(get_discovered_urls(domain))
    return discovered["web_urls"] + discovered["pdf_urls"]

