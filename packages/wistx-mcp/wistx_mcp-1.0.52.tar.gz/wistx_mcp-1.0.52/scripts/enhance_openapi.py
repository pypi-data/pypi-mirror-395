"""Enhance OpenAPI specification with examples and better documentation."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from api.main import app


def add_examples_to_schemas(spec: dict) -> dict:
    """Add examples to request/response schemas."""
    for path, methods in spec.get("paths", {}).items():
        for method, details in methods.items():
            if "requestBody" in details:
                content = details["requestBody"].get("content", {})
                for content_type, schema_info in content.items():
                    if "schema" in schema_info:
                        schema = schema_info["schema"]
                        if "properties" in schema:
                            for prop_name, prop_info in schema["properties"].items():
                                if "example" not in prop_info:
                                    prop_type = prop_info.get("type")
                                    if prop_type == "string":
                                        prop_info["example"] = f"example_{prop_name}"
                                    elif prop_type == "integer":
                                        prop_info["example"] = 1
                                    elif prop_type == "boolean":
                                        prop_info["example"] = True
                                    elif prop_type == "array":
                                        prop_info["example"] = []

            if "responses" in details:
                for status_code, response_info in details["responses"].items():
                    if status_code.startswith("2"):
                        content = response_info.get("content", {})
                        for content_type, schema_info in content.items():
                            if "example" not in schema_info and "schema" in schema_info:
                                schema = schema_info["schema"]
                                if schema.get("type") == "object" and "properties" in schema:
                                    example = {}
                                    for prop_name, prop_info in schema["properties"].items():
                                        prop_type = prop_info.get("type")
                                        if prop_type == "string":
                                            example[prop_name] = f"example_{prop_name}"
                                        elif prop_type == "integer":
                                            example[prop_name] = 1
                                        elif prop_type == "boolean":
                                            example[prop_name] = True
                                        elif prop_type == "array":
                                            example[prop_name] = []
                                    if example:
                                        schema_info["example"] = example

    return spec


def enhance_descriptions(spec: dict) -> dict:
    """Enhance endpoint descriptions with more context."""
    info = spec.get("info", {})
    if "description" not in info:
        info["description"] = (
            "WISTX REST API - DevOps compliance, pricing, and best practices context. "
            "Use this API for programmatic access to WISTX's knowledge base."
        )

    if "contact" not in info:
        info["contact"] = {
            "name": "WISTX Support",
            "email": "hi@wistx.ai",
            "url": "https://app.wistx.ai",
        }

    return spec


def add_authentication_info(spec: dict) -> dict:
    """Add authentication information to OpenAPI spec."""
    if "components" not in spec:
        spec["components"] = {}

    if "securitySchemes" not in spec["components"]:
        spec["components"]["securitySchemes"] = {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "API Key",
                "description": "API key authentication. Get your API key from https://app.wistx.ai",
            }
        }

    for path, methods in spec.get("paths", {}).items():
        for method, details in methods.items():
            if path not in ["/health", "/docs", "/openapi.json", "/redoc"]:
                if "security" not in details:
                    details["security"] = [{"bearerAuth": []}]
                
                if "responses" not in details:
                    details["responses"] = {}
                
                if "401" not in details["responses"]:
                    details["responses"]["401"] = {
                        "description": "Unauthorized - Authentication required",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "detail": {
                                            "type": "string",
                                            "example": "Invalid authorization header. Expected 'Bearer {token}'"
                                        }
                                    }
                                }
                            }
                        }
                    }

    return spec


def export_enhanced_openapi() -> None:
    """Export enhanced OpenAPI specification."""
    spec = app.openapi()
    spec = add_examples_to_schemas(spec)
    spec = enhance_descriptions(spec)
    spec = add_authentication_info(spec)
    
    if "servers" not in spec or not spec.get("servers"):
        spec["servers"] = [
            {
                "url": "http://localhost:8000",
                "description": "Local development server"
            },
            {
                "url": "https://api.wistx.ai",
                "description": "Production API"
            }
        ]
    else:
        for server in spec["servers"]:
            if server.get("url") == "http://127.0.0.1:8000":
                server["url"] = "http://localhost:8000"

    output_file = Path("docs/api-reference/openapi.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w") as f:
        json.dump(spec, f, indent=2)

    print(f"✅ Enhanced OpenAPI spec exported to: {output_file}")
    print(f"   Total endpoints: {len(spec.get('paths', {}))}")
    print(f"   API version: {spec.get('info', {}).get('version')}")
    print(f"   Servers configured: {len(spec.get('servers', []))}")


if __name__ == "__main__":
    export_enhanced_openapi()

