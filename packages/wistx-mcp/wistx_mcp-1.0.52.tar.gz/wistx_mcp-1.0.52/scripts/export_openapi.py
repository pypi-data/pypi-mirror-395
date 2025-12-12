"""Export OpenAPI specification from FastAPI app."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from api.main import app

output_file = Path(__file__).parent.parent / "api" / "openapi.json"


def export_openapi():
    """Export OpenAPI specification to JSON file."""
    spec = app.openapi()
    
    with open(output_file, "w") as f:
        json.dump(spec, f, indent=2)
    
    print(f"✅ OpenAPI spec exported to: {output_file}")
    print(f"   Total endpoints: {len(spec.get('paths', {}))}")
    print(f"   API version: {spec.get('info', {}).get('version')}")


if __name__ == "__main__":
    export_openapi()

