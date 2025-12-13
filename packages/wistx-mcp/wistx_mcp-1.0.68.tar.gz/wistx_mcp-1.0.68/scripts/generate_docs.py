"""Complete documentation generation pipeline."""

import subprocess
import sys
from pathlib import Path


def run_script(script_name: str) -> bool:
    """Run a Python script and return success status."""
    script_path = Path("scripts") / script_name
    if not script_path.exists():
        print(f"❌ Script not found: {script_path}")
        return False

    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"❌ Error running {script_name}:")
        print(result.stderr)
        return False

    print(result.stdout)
    return True


def validate_docs() -> bool:
    """Validate generated documentation."""
    docs_dir = Path("docs")

    required_files = [
        "mint.json",
        "intro.mdx",
    ]

    for file_path in required_files:
        full_path = docs_dir / file_path
        if not full_path.exists():
            print(f"❌ Missing required file: {file_path}")
            return False

    api_ref_dir = docs_dir / "api-reference"
    if api_ref_dir.exists():
        openapi_file = api_ref_dir / "openapi.json"
        if not openapi_file.exists():
            print("⚠️  OpenAPI spec not found (optional)")

    print("✅ Documentation validation passed")
    return True


def main() -> None:
    """Run complete documentation generation pipeline."""
    print("🚀 Starting documentation generation...\n")

    steps = [
        ("Export OpenAPI spec", "export_openapi.py"),
        ("Enhance OpenAPI spec", "enhance_openapi.py"),
        ("Extract MCP schemas", "extract_mcp_schemas.py"),
    ]

    for step_name, script_name in steps:
        print(f"📝 {step_name}...")
        if not run_script(script_name):
            print(f"❌ Failed at step: {step_name}")
            sys.exit(1)
        print()

    print("✅ Validating documentation...")
    if not validate_docs():
        print("❌ Documentation validation failed")
        sys.exit(1)

    print("\n✅ Documentation generation complete!")


if __name__ == "__main__":
    main()

