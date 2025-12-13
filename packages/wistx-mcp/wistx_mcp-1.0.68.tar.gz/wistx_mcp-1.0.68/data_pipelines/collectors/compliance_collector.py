"""Compliance standards collector with standard-specific implementations."""

from collections.abc import Awaitable, Callable
from typing import Any

from bs4 import BeautifulSoup

from .base_collector import BaseComplianceCollector
from ..config.compliance_urls import COMPLIANCE_URLS
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class PCIDSSCollector(BaseComplianceCollector):
    """Collector for PCI-DSS 4.0 requirements.

    Source: https://www.pcisecuritystandards.org/
    Expected: ~400 controls
    """

    def __init__(self):
        """Initialize PCI-DSS collector."""
        config = COMPLIANCE_URLS["PCI-DSS"]
        super().__init__("PCI-DSS", config["version"])
        self.base_url = config["base_url"]
        self.urls = config["urls"]

    def get_source_urls(self) -> list[str]:
        """Get PCI-DSS source URLs from config.

        Returns:
            List of URLs to scrape
        """
        return self.urls

    def parse_control(self, soup: BeautifulSoup, url: str) -> list[dict[str, Any]]:
        """Parse PCI-DSS controls from page.

        Handles multiple website structures:
        - Official PCI-DSS site
        - Third-party compliance sites (Drata, Sprinto, CrowdStrike, etc.)
        - Blog posts and guides

        Args:
            soup: Parsed BeautifulSoup object
            url: Source URL

        Returns:
            List of control dictionaries
        """
        controls = []

        if "pcisecuritystandards.org" in url:
            requirement_sections = (
                soup.find_all("div", class_="requirement")
                + soup.find_all("section", class_="requirement")
                + soup.find_all("article", class_="requirement")
            )

            for section in requirement_sections:
                control_id_elem = (
                    section.find("span", class_="control-id")
                    or section.find("h2")
                    or section.find("h3")
                )
                requirement_elem = (
                    section.find("div", class_="requirement-text")
                    or section.find("p", class_="requirement")
                    or section.find("div", class_="content")
                )
                testing_procedures_elem = section.find("div", class_="testing-procedures")
                guidance_elem = section.find("div", class_="guidance")

                if not control_id_elem or not requirement_elem:
                    continue

                control = {
                    "control_id": control_id_elem.get_text(strip=True),
                    "requirement": requirement_elem.get_text(strip=True),
                    "testing_procedures": (
                        [
                            p.get_text(strip=True)
                            for p in testing_procedures_elem.find_all("p")
                        ]
                        if testing_procedures_elem
                        else []
                    ),
                    "guidance": (
                        guidance_elem.get_text(strip=True) if guidance_elem else ""
                    ),
                    "source_url": url,
                }

                controls.append(control)

        elif any(domain in url for domain in ["drata.com", "sprinto.com", "crowdstrike.com"]):
            article_content = (
                soup.find("article")
                or soup.find("main")
                or soup.find("div", class_="content")
                or soup.find("div", class_="post-content")
            )

            if article_content:
                headings = article_content.find_all(["h2", "h3", "h4"])
                for heading in headings:
                    heading_text = heading.get_text(strip=True)
                    if any(
                        keyword in heading_text.lower()
                        for keyword in ["requirement", "control", "pci", "dss"]
                    ):
                        content_elem = heading.find_next_sibling(["p", "div", "ul"])
                        if content_elem:
                            control = {
                                "control_id": heading_text,
                                "requirement": content_elem.get_text(strip=True),
                                "testing_procedures": [],
                                "guidance": "",
                                "source_url": url,
                            }
                            controls.append(control)

        elif "rsisecurity.com" in url:
            article_content = soup.find("article") or soup.find("div", class_="entry-content")
            if article_content:
                headings = article_content.find_all(["h2", "h3"])
                for heading in headings:
                    heading_text = heading.get_text(strip=True)
                    if "control" in heading_text.lower() or "requirement" in heading_text.lower():
                        content_elem = heading.find_next_sibling(["p", "div"])
                        if content_elem:
                            control = {
                                "control_id": heading_text,
                                "requirement": content_elem.get_text(strip=True),
                                "testing_procedures": [],
                                "guidance": "",
                                "source_url": url,
                            }
                            controls.append(control)

        else:
            headings = soup.find_all(["h2", "h3", "h4"])
            for heading in headings:
                heading_text = heading.get_text(strip=True)
                if any(
                    keyword in heading_text.lower()
                    for keyword in ["requirement", "control", "pci", "dss", "article"]
                ):
                    content_elem = heading.find_next_sibling(["p", "div", "ul"])
                    if content_elem:
                        control = {
                            "control_id": heading_text,
                            "requirement": content_elem.get_text(strip=True),
                            "testing_procedures": [],
                            "guidance": "",
                            "source_url": url,
                        }
                        controls.append(control)

        return controls


class CISCollector(BaseComplianceCollector):
    """Collector for CIS Benchmarks.

    Source: https://www.cisecurity.org/
    Expected: ~200 benchmarks per cloud provider
    """

    def __init__(self, cloud: str = "aws"):
        """Initialize CIS collector.

        Args:
            cloud: Cloud provider (aws, gcp, azure)
        """
        config = COMPLIANCE_URLS["CIS"]
        super().__init__("CIS", config["version"])
        self.cloud = cloud
        self.base_url = config["base_url"]
        self.urls = config["urls"].get(cloud, [])

    def get_source_urls(self) -> list[str]:
        """Get CIS benchmark source URLs from config.

        Returns:
            List of URLs to scrape
        """
        return self.urls

    def parse_control(self, soup: BeautifulSoup, url: str) -> list[dict[str, Any]]:
        """Parse CIS benchmarks from page.

        Args:
            soup: Parsed BeautifulSoup object
            url: Source URL

        Returns:
            List of benchmark dictionaries
        """
        controls = []

        benchmark_items = soup.find_all("div", class_="benchmark-item")

        for item in benchmark_items:
            benchmark_id_elem = item.find("span", class_="benchmark-id")
            title_elem = item.find("h3")
            description_elem = item.find("div", class_="description")
            audit_elem = item.find("div", class_="audit")
            remediation_elem = item.find("div", class_="remediation")
            level_elem = item.find("span", class_="level")

            if not benchmark_id_elem or not title_elem:
                continue

            control = {
                "benchmark_id": benchmark_id_elem.get_text(strip=True),
                "title": title_elem.get_text(strip=True),
                "description": (
                    description_elem.get_text(strip=True) if description_elem else ""
                ),
                "audit": audit_elem.get_text(strip=True) if audit_elem else "",
                "remediation": (
                    remediation_elem.get_text(strip=True) if remediation_elem else ""
                ),
                "level": level_elem.get_text(strip=True) if level_elem else "1",
                "cloud": self.cloud,
                "source_url": url,
            }

            controls.append(control)

        return controls


class HIPAACollector(BaseComplianceCollector):
    """Collector for HIPAA Security Rule.

    Source: https://www.hhs.gov/hipaa/
    Expected: ~50 requirements
    """

    def __init__(self):
        """Initialize HIPAA collector."""
        config = COMPLIANCE_URLS["HIPAA"]
        super().__init__("HIPAA", config["version"])
        self.base_url = config["base_url"]
        self.urls = config["urls"]

    def get_source_urls(self) -> list[str]:
        """Get HIPAA source URLs from config.

        Returns:
            List of URLs to scrape
        """
        return self.urls

    def parse_control(self, soup: BeautifulSoup, url: str) -> list[dict[str, Any]]:
        """Parse HIPAA requirements from page.

        Args:
            soup: Parsed BeautifulSoup object
            url: Source URL

        Returns:
            List of requirement dictionaries
        """
        controls = []

        requirement_sections = soup.find_all("section", class_="requirement")

        for section in requirement_sections:
            requirement_id_elem = section.find("h2")
            requirement_text_elem = section.find("div", class_="requirement-text")
            technical_safeguards_elem = section.find("div", class_="technical-safeguards")

            if not requirement_id_elem or not requirement_text_elem:
                continue

            control = {
                "requirement_id": requirement_id_elem.get_text(strip=True),
                "requirement": requirement_text_elem.get_text(strip=True),
                "technical_safeguards": (
                    [
                        s.get_text(strip=True)
                        for s in technical_safeguards_elem.find_all("li")
                    ]
                    if technical_safeguards_elem
                    else []
                ),
                "source_url": url,
            }

            controls.append(control)

        return controls


class SOC2Collector(BaseComplianceCollector):
    """Collector for SOC 2 controls.

    Source: https://www.aicpa.org/
    Expected: ~60 controls
    """

    def __init__(self):
        """Initialize SOC 2 collector."""
        config = COMPLIANCE_URLS["SOC2"]
        super().__init__("SOC2", config["version"])
        self.base_url = config["base_url"]
        self.urls = config["urls"]

    def get_source_urls(self) -> list[str]:
        """Get SOC 2 source URLs from config.

        Returns:
            List of URLs to scrape
        """
        return self.urls

    def parse_control(self, soup: BeautifulSoup, url: str) -> list[dict[str, Any]]:
        """Parse SOC 2 controls from page.

        Args:
            soup: Parsed BeautifulSoup object
            url: Source URL

        Returns:
            List of control dictionaries
        """
        controls = []

        control_sections = soup.find_all("div", class_="control") or soup.find_all(
            "section", class_="trust-service-criteria"
        )

        for section in control_sections:
            control_id_elem = section.find("span", class_="control-id") or section.find(
                "h3"
            )
            description_elem = section.find("div", class_="description") or section.find("p")
            criteria_elem = section.find("div", class_="criteria")
            testing_elem = section.find("div", class_="testing-procedures")

            if not control_id_elem or not description_elem:
                continue

            control = {
                "control_id": control_id_elem.get_text(strip=True),
                "description": description_elem.get_text(strip=True),
                "criteria": (
                    criteria_elem.get_text(strip=True) if criteria_elem else ""
                ),
                "testing_procedures": (
                    [p.get_text(strip=True) for p in testing_elem.find_all("p")]
                    if testing_elem
                    else []
                ),
                "source_url": url,
            }

            controls.append(control)

        return controls


class NIST80053Collector(BaseComplianceCollector):
    """Collector for NIST 800-53 controls.

    Source: https://csrc.nist.gov/
    Expected: ~900 controls
    """

    def __init__(self):
        """Initialize NIST 800-53 collector."""
        config = COMPLIANCE_URLS["NIST-800-53"]
        super().__init__("NIST-800-53", config["version"])
        self.base_url = config["base_url"]
        self.urls = config["urls"]

    def get_source_urls(self) -> list[str]:
        """Get NIST 800-53 source URLs from config.

        Returns:
            List of URLs to scrape
        """
        return self.urls

    def parse_control_json(
        self, data: dict[str, Any] | list[dict[str, Any]], url: str
    ) -> list[dict[str, Any]]:
        """Parse NIST 800-53 controls from JSON data.

        Args:
            data: JSON data (dict or list)
            url: Source URL

        Returns:
            List of control dictionaries
        """
        controls = []

        if isinstance(data, dict) and "controls" in data:
            json_controls = data["controls"]
        elif isinstance(data, list):
            json_controls = data
        else:
            logger.warning("Unexpected JSON structure from %s", url)
            return controls

        for item in json_controls:
            if isinstance(item, dict):
                control = {
                    "control_id": item.get("id", ""),
                    "title": item.get("title", ""),
                    "description": item.get("description", ""),
                    "guidance": item.get("guidance", ""),
                    "source_url": url,
                }
                controls.append(control)

        return controls

    def parse_control(self, soup: BeautifulSoup, url: str) -> list[dict[str, Any]]:
        """Parse NIST 800-53 controls from HTML page.

        Args:
            soup: Parsed BeautifulSoup object
            url: Source URL

        Returns:
            List of control dictionaries
        """
        controls = []

        control_sections = soup.find_all("div", class_="control") or soup.find_all(
            "section", class_="control"
        )

        for section in control_sections:
            control_id_elem = section.find("span", class_="control-id") or section.find(
                "h2"
            )
            title_elem = section.find("h3") or section.find("span", class_="title")
            description_elem = section.find("div", class_="description") or section.find(
                "p"
            )
            guidance_elem = section.find("div", class_="guidance")

            if not control_id_elem:
                continue

            control = {
                "control_id": control_id_elem.get_text(strip=True),
                "title": title_elem.get_text(strip=True) if title_elem else "",
                "description": (
                    description_elem.get_text(strip=True) if description_elem else ""
                ),
                "guidance": (
                    guidance_elem.get_text(strip=True) if guidance_elem else ""
                ),
                "source_url": url,
            }

            controls.append(control)

        return controls


class ISO27001Collector(BaseComplianceCollector):
    """Collector for ISO 27001 controls.

    Source: https://www.iso.org/
    Expected: ~114 controls
    """

    def __init__(self):
        """Initialize ISO 27001 collector."""
        config = COMPLIANCE_URLS["ISO-27001"]
        super().__init__("ISO-27001", config["version"])
        self.base_url = config["base_url"]
        self.urls = config["urls"]

    def get_source_urls(self) -> list[str]:
        """Get ISO 27001 source URLs from config.

        Returns:
            List of URLs to scrape
        """
        return self.urls

    def parse_control(self, soup: BeautifulSoup, url: str) -> list[dict[str, Any]]:
        """Parse ISO 27001 controls from page.

        Args:
            soup: Parsed BeautifulSoup object
            url: Source URL

        Returns:
            List of control dictionaries
        """
        controls = []

        if "iso.org" in url:
            main_content = (
                soup.find("main")
                or soup.find("div", class_="content")
                or soup.find("article")
            )

            if main_content:
                headings = main_content.find_all(["h2", "h3", "h4"])
                for heading in headings:
                    heading_text = heading.get_text(strip=True)
                    if any(
                        keyword in heading_text.lower()
                        for keyword in ["control", "annex", "a.", "requirement"]
                    ):
                        content_elem = heading.find_next_sibling(["p", "div", "ul"])
                        if content_elem:
                            control = {
                                "control_id": heading_text,
                                "title": heading_text,
                                "description": content_elem.get_text(strip=True),
                                "guidance": "",
                                "source_url": url,
                            }
                            controls.append(control)

        else:
            control_sections = soup.find_all("div", class_="control") or soup.find_all(
                "section", class_="annex-a-control"
            )

            for section in control_sections:
                control_id_elem = (
                    section.find("span", class_="control-id") or section.find("h3")
                )
                title_elem = section.find("h4") or section.find("span", class_="title")
                description_elem = (
                    section.find("div", class_="description") or section.find("p")
                )
                guidance_elem = section.find("div", class_="guidance")

                if not control_id_elem:
                    continue

                control = {
                    "control_id": control_id_elem.get_text(strip=True),
                    "title": title_elem.get_text(strip=True) if title_elem else "",
                    "description": (
                        description_elem.get_text(strip=True) if description_elem else ""
                    ),
                    "guidance": (
                        guidance_elem.get_text(strip=True) if guidance_elem else ""
                    ),
                    "source_url": url,
                }

                controls.append(control)

        return controls


class GDPRCollector(BaseComplianceCollector):
    """Collector for GDPR requirements.

    Source: https://gdpr.eu/
    Expected: ~99 articles
    """

    def __init__(self):
        """Initialize GDPR collector."""
        config = COMPLIANCE_URLS["GDPR"]
        super().__init__("GDPR", config["version"])
        self.base_url = config["base_url"]
        self.urls = config["urls"]

    def get_source_urls(self) -> list[str]:
        """Get GDPR source URLs from config.

        Returns:
            List of URLs to scrape
        """
        return self.urls

    def parse_control(self, soup: BeautifulSoup, url: str) -> list[dict[str, Any]]:
        """Parse GDPR articles from page.

        Handles multiple GDPR sources:
        - gdpr-info.eu (official text)
        - gdpr.eu (guides and explanations)
        - eur-lex.europa.eu (official EU legislation)

        Args:
            soup: Parsed BeautifulSoup object
            url: Source URL

        Returns:
            List of article dictionaries
        """
        controls = []

        if "gdpr-info.eu" in url:
            article_sections = (
                soup.find_all("article")
                + soup.find_all("div", class_="article")
                + soup.find_all("section", class_="article")
            )

            for section in article_sections:
                article_id_elem = (
                    section.find("h2")
                    or section.find("span", class_="article-id")
                    or section.find("div", class_="article-number")
                )
                title_elem = section.find("h3") or section.find("h2")
                content_elem = (
                    section.find("div", class_="content")
                    or section.find("div", class_="article-content")
                    or section.find("p")
                )

                if article_id_elem or title_elem:
                    control = {
                        "article_id": (
                            article_id_elem.get_text(strip=True) if article_id_elem else ""
                        ),
                        "title": title_elem.get_text(strip=True) if title_elem else "",
                        "content": (
                            content_elem.get_text(strip=True) if content_elem else ""
                        ),
                        "source_url": url,
                    }
                    controls.append(control)

        elif "eur-lex.europa.eu" in url:
            articles = soup.find_all(["article", "div"], class_=lambda x: x and "article" in x.lower())
            for article in articles:
                article_num = article.find(["h2", "h3", "span"], class_=lambda x: x and "number" in str(x).lower())
                content = article.find(["p", "div"], class_=lambda x: x and "content" in str(x).lower())
                if article_num or content:
                    control = {
                        "article_id": article_num.get_text(strip=True) if article_num else "",
                        "title": "",
                        "content": content.get_text(strip=True) if content else "",
                        "source_url": url,
                    }
                    controls.append(control)

        else:
            headings = soup.find_all(["h2", "h3", "h4"])
            for heading in headings:
                heading_text = heading.get_text(strip=True)
                if "article" in heading_text.lower() or "gdpr" in heading_text.lower():
                    content_elem = heading.find_next_sibling(["p", "div", "ul"])
                    if content_elem:
                        control = {
                            "article_id": heading_text,
                            "title": heading_text,
                            "content": content_elem.get_text(strip=True),
                            "source_url": url,
                        }
                        controls.append(control)

        return controls


class FedRAMPCollector(BaseComplianceCollector):
    """Collector for FedRAMP controls.

    Source: https://www.fedramp.gov/
    Expected: ~325 controls
    """

    def __init__(self):
        """Initialize FedRAMP collector."""
        config = COMPLIANCE_URLS["FedRAMP"]
        super().__init__("FedRAMP", config["version"])
        self.base_url = config["base_url"]
        self.urls = config["urls"]

    def get_source_urls(self) -> list[str]:
        """Get FedRAMP source URLs from config.

        Returns:
            List of URLs to scrape
        """
        return self.urls

    def parse_control(self, soup: BeautifulSoup, url: str) -> list[dict[str, Any]]:
        """Parse FedRAMP controls from page.

        Args:
            soup: Parsed BeautifulSoup object
            url: Source URL

        Returns:
            List of control dictionaries
        """
        controls = []

        if url.endswith(".xlsx"):
            logger.warning("Skipping Excel file: %s (not yet supported)", url)
            return controls

        control_sections = soup.find_all("div", class_="control") or soup.find_all(
            "section", class_="control"
        )

        for section in control_sections:
            control_id_elem = section.find("span", class_="control-id") or section.find(
                "h3"
            )
            description_elem = section.find("div", class_="description") or section.find(
                "p"
            )

            if not control_id_elem:
                continue

            control = {
                "control_id": control_id_elem.get_text(strip=True),
                "description": (
                    description_elem.get_text(strip=True) if description_elem else ""
                ),
                "source_url": url,
            }

            controls.append(control)

        return controls


class CCPACollector(BaseComplianceCollector):
    """Collector for CCPA requirements.

    Source: https://oag.ca.gov/
    Expected: ~50 requirements
    """

    def __init__(self):
        """Initialize CCPA collector."""
        config = COMPLIANCE_URLS["CCPA"]
        super().__init__("CCPA", config["version"])
        self.base_url = config["base_url"]
        self.urls = config["urls"]

    def get_source_urls(self) -> list[str]:
        """Get CCPA source URLs from config.

        Returns:
            List of URLs to scrape
        """
        return self.urls

    def parse_control(self, soup: BeautifulSoup, url: str) -> list[dict[str, Any]]:
        """Parse CCPA requirements from page.

        Args:
            soup: Parsed BeautifulSoup object
            url: Source URL

        Returns:
            List of requirement dictionaries
        """
        controls = []

        requirement_sections = soup.find_all("section") or soup.find_all(
            "div", class_="requirement"
        )

        for section in requirement_sections:
            requirement_id_elem = section.find("h2") or section.find("h3")
            content_elem = section.find("div", class_="content") or section.find("p")

            if not requirement_id_elem:
                continue

            control = {
                "requirement_id": requirement_id_elem.get_text(strip=True),
                "content": content_elem.get_text(strip=True) if content_elem else "",
                "source_url": url,
            }

            controls.append(control)

        return controls


class SOXCollector(BaseComplianceCollector):
    """Collector for SOX requirements.

    Source: https://www.sec.gov/
    Expected: ~40 requirements
    """

    def __init__(self):
        """Initialize SOX collector."""
        config = COMPLIANCE_URLS["SOX"]
        super().__init__("SOX", config["version"])
        self.base_url = config["base_url"]
        self.urls = config["urls"]

    def get_source_urls(self) -> list[str]:
        """Get SOX source URLs from config.

        Returns:
            List of URLs to scrape
        """
        return self.urls

    def parse_control(self, soup: BeautifulSoup, url: str) -> list[dict[str, Any]]:
        """Parse SOX requirements from page.

        Args:
            soup: Parsed BeautifulSoup object
            url: Source URL

        Returns:
            List of requirement dictionaries
        """
        controls = []

        requirement_sections = soup.find_all("section") or soup.find_all(
            "div", class_="requirement"
        )

        for section in requirement_sections:
            requirement_id_elem = section.find("h2") or section.find("h3")
            content_elem = section.find("div", class_="content") or section.find("p")

            if not requirement_id_elem:
                continue

            control = {
                "requirement_id": requirement_id_elem.get_text(strip=True),
                "content": content_elem.get_text(strip=True) if content_elem else "",
                "source_url": url,
            }

            controls.append(control)

        return controls


class GLBACollector(BaseComplianceCollector):
    """Collector for GLBA requirements.

    Source: https://www.ftc.gov/
    Expected: ~30 requirements
    """

    def __init__(self):
        """Initialize GLBA collector."""
        config = COMPLIANCE_URLS["GLBA"]
        super().__init__("GLBA", config["version"])
        self.base_url = config["base_url"]
        self.urls = config["urls"]

    def get_source_urls(self) -> list[str]:
        """Get GLBA source URLs from config.

        Returns:
            List of URLs to scrape
        """
        return self.urls

    def parse_control(self, soup: BeautifulSoup, url: str) -> list[dict[str, Any]]:
        """Parse GLBA requirements from page.

        Args:
            soup: Parsed BeautifulSoup object
            url: Source URL

        Returns:
            List of requirement dictionaries
        """
        controls = []

        requirement_sections = soup.find_all("section") or soup.find_all(
            "div", class_="requirement"
        )

        for section in requirement_sections:
            requirement_id_elem = section.find("h2") or section.find("h3")
            content_elem = section.find("div", class_="content") or section.find("p")

            if not requirement_id_elem:
                continue

            control = {
                "requirement_id": requirement_id_elem.get_text(strip=True),
                "content": content_elem.get_text(strip=True) if content_elem else "",
                "source_url": url,
            }

            controls.append(control)

        return controls


class ComplianceCollector:
    """Main collector that orchestrates all compliance standard collectors."""

    def __init__(self):
        """Initialize main collector."""
        self.collectors = {
            "pci-dss": PCIDSSCollector(),
            "cis-aws": CISCollector("aws"),
            "cis-gcp": CISCollector("gcp"),
            "cis-azure": CISCollector("azure"),
            "hipaa": HIPAACollector(),
            "soc2": SOC2Collector(),
            "nist-800-53": NIST80053Collector(),
            "iso-27001": ISO27001Collector(),
            "gdpr": GDPRCollector(),
            "fedramp": FedRAMPCollector(),
            "ccpa": CCPACollector(),
            "sox": SOXCollector(),
            "glba": GLBACollector(),
        }

    def collect_all(self) -> dict[str, list[dict[str, Any]]]:
        """Collect all compliance standards.

        Returns:
            Dictionary mapping standard names to their collected controls
        """
        results = {}

        for name, collector in self.collectors.items():
            logger.info("Collecting %s...", name)
            try:
                controls = collector.collect()
                results[name] = controls
            except (ValueError, KeyError, AttributeError) as e:
                logger.error("Failed to collect %s: %s", name, e)
                results[name] = []
            except (ConnectionError, TimeoutError) as e:
                logger.error("Network error collecting %s: %s", name, e)
                results[name] = []
            except RuntimeError as e:
                logger.error("Runtime error collecting %s: %s", name, e)
                results[name] = []
            except Exception as e:
                logger.error("Unexpected error collecting %s: %s", name, e, exc_info=True)
                results[name] = []

        return results

    async def collect_standard_async(
        self, 
        standard: str,
        max_urls: int | None = None,
        max_pdfs: int | None = None,
        max_controls: int | None = None,
        progress_callback: Callable[[int, int], None] | Callable[[int, int], Awaitable[None]] | None = None,
        disable_deep_crawl: bool = False,
    ) -> list[dict[str, Any]]:
        """Collect a specific standard (async).

        Args:
            standard: Standard name (pci-dss, cis-aws, hipaa, etc.)
            max_urls: Maximum number of seed URLs to process (None for all)
            max_pdfs: Maximum number of PDFs to process (None for all)
            max_controls: Maximum number of controls to collect (None for all)
            progress_callback: Optional callback(item_count, total_urls) for progress updates
            disable_deep_crawl: If True, disable deep crawling (default: False)

        Returns:
            List of collected controls

        Raises:
            ValueError: If standard not found
        """
        if standard not in self.collectors:
            raise ValueError(f"Unknown standard: {standard}")

        collector = self.collectors[standard]
        if disable_deep_crawl:
            collector.enable_deep_crawl = False
            logger.info("Deep crawling disabled for %s collector", standard)

        result = await collector.collect_async(
            max_urls=max_urls,
            max_pdfs=max_pdfs,
            max_controls=max_controls,
            progress_callback=progress_callback,
        )
        return result.items

    def collect_standard(self, standard: str) -> list[dict[str, Any]]:
        """Collect a specific standard (sync wrapper - deprecated, use collect_standard_async).

        Args:
            standard: Standard name (pci-dss, cis-aws, hipaa, etc.)

        Returns:
            List of collected controls

        Raises:
            ValueError: If standard not found
        """
        import asyncio

        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                raise RuntimeError(
                    "Cannot use sync collect_standard() in async context. Use collect_standard_async() instead."
                )
        except RuntimeError:
            pass

        if standard not in self.collectors:
            raise ValueError(f"Unknown standard: {standard}")

        return self.collectors[standard].collect()
