"""Test script for automated source discovery."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from data_pipelines.collectors.source_discovery import SourceDiscovery
from data_pipelines.collectors.discovery_helper import get_discovered_urls
from data_pipelines.config.source_registry import TRUSTED_DOMAINS
from data_pipelines.utils.logger import setup_logger

logger = setup_logger(__name__)


async def test_sitemap_discovery():
    """Test sitemap discovery for PCI-DSS domain."""
    logger.info("=" * 80)
    logger.info("Testing Automated Source Discovery")
    logger.info("=" * 80)

    domain_config = {
        "domain": "pcisecuritystandards.org",
        "discovery_mode": "sitemap",
        "path_patterns": ["/document_library/", "/requirements/"],
        "content_types": ["pdf", "html"],
    }

    async with SourceDiscovery() as discovery:
        logger.info("Discovering URLs from: %s", domain_config["domain"])
        result = await discovery.discover_all_for_domain(domain_config)

        logger.info("=" * 80)
        logger.info("Discovery Results:")
        logger.info("  Web URLs: %d", len(result["web_urls"]))
        logger.info("  PDF URLs: %d", len(result["pdf_urls"]))
        logger.info("=" * 80)

        if result["web_urls"]:
            logger.info("\nSample Web URLs (first 5):")
            for url in result["web_urls"][:5]:
                logger.info("  - %s", url)

        if result["pdf_urls"]:
            logger.info("\nPDF URLs:")
            for url in result["pdf_urls"]:
                logger.info("  - %s", url)

        return result


async def test_all_domains():
    """Test discovery for all configured domains."""
    logger.info("=" * 80)
    logger.info("Testing All Configured Domains")
    logger.info("=" * 80)

    results = {}

    for domain_name, domain_data in TRUSTED_DOMAINS.items():
        logger.info("\nDomain: %s", domain_name)
        logger.info("-" * 80)

        tier_1_domains = domain_data.get("tier_1", [])

        domain_web_urls: list[str] = []
        domain_pdf_urls: list[str] = []

        async with SourceDiscovery() as discovery:
            for domain_config in tier_1_domains:
                domain = domain_config.get("domain", "unknown")
                logger.info("  Discovering from: %s", domain)

                try:
                    discovered = await discovery.discover_all_for_domain(domain_config)
                    domain_web_urls.extend(discovered["web_urls"])
                    domain_pdf_urls.extend(discovered["pdf_urls"])

                    logger.info(
                        "    Found: %d web URLs, %d PDF URLs",
                        len(discovered["web_urls"]),
                        len(discovered["pdf_urls"]),
                    )
                except Exception as e:
                    logger.error("    Error: %s", e)

        results[domain_name] = {
            "web_urls": len(domain_web_urls),
            "pdf_urls": len(domain_pdf_urls),
            "total": len(domain_web_urls) + len(domain_pdf_urls),
        }

        logger.info(
            "  Total for %s: %d URLs (%d web, %d PDF)",
            domain_name,
            results[domain_name]["total"],
            results[domain_name]["web_urls"],
            results[domain_name]["pdf_urls"],
        )

    logger.info("\n" + "=" * 80)
    logger.info("Summary:")
    logger.info("=" * 80)
    for domain_name, stats in results.items():
        logger.info(
            "%s: %d total URLs (%d web, %d PDF)",
            domain_name,
            stats["total"],
            stats["web_urls"],
            stats["pdf_urls"],
        )

    return results


async def test_helper_function():
    """Test the discovery helper function."""
    logger.info("=" * 80)
    logger.info("Testing Discovery Helper Function")
    logger.info("=" * 80)

    result = await get_discovered_urls("compliance", "PCI-DSS")

    logger.info("Discovered URLs for compliance/PCI-DSS:")
    logger.info("  Web URLs: %d", len(result["web_urls"]))
    logger.info("  PDF URLs: %d", len(result["pdf_urls"]))

    if result["web_urls"]:
        logger.info("\nSample Web URLs:")
        for url in result["web_urls"][:3]:
            logger.info("  - %s", url)

    if result["pdf_urls"]:
        logger.info("\nPDF URLs:")
        for url in result["pdf_urls"]:
            logger.info("  - %s", url)

    return result


async def main():
    """Main test function."""
    import argparse

    parser = argparse.ArgumentParser(description="Test automated source discovery")
    parser.add_argument(
        "--test",
        choices=["sitemap", "all", "helper"],
        default="sitemap",
        help="Test to run",
    )

    args = parser.parse_args()

    try:
        if args.test == "sitemap":
            await test_sitemap_discovery()
        elif args.test == "all":
            await test_all_domains()
        elif args.test == "helper":
            await test_helper_function()
    except KeyboardInterrupt:
        logger.info("\nTest interrupted by user")
    except Exception as e:
        logger.error("Test failed: %s", e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

