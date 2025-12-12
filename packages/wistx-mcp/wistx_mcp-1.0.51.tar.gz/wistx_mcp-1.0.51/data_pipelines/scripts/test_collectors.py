#!/usr/bin/env python3
"""Test script for compliance collectors against actual websites."""

import json
import os
import sys
from pathlib import Path

base_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(base_path))

os.environ.setdefault("GEMINI_API_KEY", "test-key-for-testing")
os.environ.setdefault("MONGODB_URI", "mongodb://localhost:27017/test")
os.environ.setdefault("DATABASE_NAME", "test")

import importlib.util

def load_module(module_name, file_path, parent_modules=None):
    """Load a module dynamically."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    
    if parent_modules:
        for parent in parent_modules:
            if parent not in sys.modules:
                sys.modules[parent] = type(sys)(parent)
    
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

config_util = load_module(
    "data_pipelines.utils.config",
    base_path / "data-pipelines" / "utils" / "config.py",
    ["data_pipelines", "data_pipelines.utils"]
)

logger_util = load_module(
    "data_pipelines.utils.logger",
    base_path / "data-pipelines" / "utils" / "logger.py",
    ["data_pipelines", "data_pipelines.utils"]
)

retry_handler = load_module(
    "data_pipelines.utils.retry_handler",
    base_path / "data-pipelines" / "utils" / "retry_handler.py",
    ["data_pipelines", "data_pipelines.utils"]
)

base_collector = load_module(
    "data_pipelines.collectors.base_collector",
    base_path / "data-pipelines" / "collectors" / "base_collector.py",
    ["data_pipelines", "data_pipelines.collectors"]
)

compliance_urls = load_module(
    "data_pipelines.config.compliance_urls",
    base_path / "data-pipelines" / "config" / "compliance_urls.py",
    ["data_pipelines", "data_pipelines.config"]
)

compliance_collector = load_module(
    "data_pipelines.collectors.compliance_collector",
    base_path / "data-pipelines" / "collectors" / "compliance_collector.py",
    ["data_pipelines", "data_pipelines.collectors"]
)

PCIDSSCollector = compliance_collector.PCIDSSCollector
CISCollector = compliance_collector.CISCollector
HIPAACollector = compliance_collector.HIPAACollector
SOC2Collector = compliance_collector.SOC2Collector
NIST80053Collector = compliance_collector.NIST80053Collector
ISO27001Collector = compliance_collector.ISO27001Collector
GDPRCollector = compliance_collector.GDPRCollector
FedRAMPCollector = compliance_collector.FedRAMPCollector
CCPACollector = compliance_collector.CCPACollector
SOXCollector = compliance_collector.SOXCollector
GLBACollector = compliance_collector.GLBACollector

setup_logger = logger_util.setup_logger
logger = setup_logger(__name__)


def test_collector_urls(collector_name: str, collector_instance) -> dict:
    """Test URLs for a collector."""
    print(f"\n{'='*60}")
    print(f"Testing: {collector_name}")
    print(f"{'='*60}")

    result = {
        "collector": collector_name,
        "urls_tested": 0,
        "urls_accessible": 0,
        "urls_failed": 0,
        "errors": [],
    }

    try:
        urls = collector_instance.get_source_urls()
        result["urls_tested"] = len(urls)
        print(f"Total URLs: {len(urls)}")

        for url in urls[:2]:
            print(f"\n  Testing: {url}")
            try:
                soup = collector_instance.fetch_page(url)
                print(f"  ✓ Successfully fetched page")
                result["urls_accessible"] += 1

                controls = collector_instance.parse_control(soup, url)
                print(f"  ✓ Parsed {len(controls)} controls")
                if controls:
                    print(f"  Sample keys: {list(controls[0].keys())}")
            except Exception as e:
                error_msg = f"{url}: {str(e)}"
                print(f"  ✗ Failed: {error_msg}")
                result["urls_failed"] += 1
                result["errors"].append(error_msg)

    except Exception as e:
        error_msg = f"Collector test failed: {str(e)}"
        print(f"✗ {error_msg}")
        result["errors"].append(error_msg)

    return result


def main():
    """Main test function."""
    print("=" * 60)
    print("Compliance Collector URL Test")
    print("=" * 60)

    collectors = {
        "PCI-DSS": PCIDSSCollector(),
        "CIS-AWS": CISCollector("aws"),
        "HIPAA": HIPAACollector(),
        "SOC2": SOC2Collector(),
        "NIST-800-53": NIST80053Collector(),
        "ISO-27001": ISO27001Collector(),
        "GDPR": GDPRCollector(),
        "FedRAMP": FedRAMPCollector(),
        "CCPA": CCPACollector(),
        "SOX": SOXCollector(),
        "GLBA": GLBACollector(),
    }

    results = []
    for name, collector in collectors.items():
        result = test_collector_urls(name, collector)
        results.append(result)

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    total_urls = sum(r["urls_tested"] for r in results)
    accessible = sum(r["urls_accessible"] for r in results)
    failed = sum(r["urls_failed"] for r in results)

    print(f"Total collectors: {len(collectors)}")
    print(f"Total URLs tested: {total_urls}")
    print(f"Accessible: {accessible}")
    print(f"Failed: {failed}")

    output_file = base_path / "data-pipelines" / "data" / "test_results" / "url_tests.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        json.dump({
            "results": results,
            "summary": {"total": total_urls, "accessible": accessible, "failed": failed}
        }, f, indent=2)

    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()
