"""Test script to verify schema fixes work correctly.

This script tests that the fixed schemas match their function implementations
by checking the actual values in server.py against expected values.
"""

import ast
import re
from pathlib import Path


def extract_tool_schema(server_file: Path, tool_name: str) -> dict[str, dict[str, any]] | None:
    """Extract schema for a specific tool from server.py.
    
    Args:
        server_file: Path to server.py
        tool_name: Tool name (e.g., 'wistx_web_search')
        
    Returns:
        Dictionary mapping parameter names to their schema, or None if not found
    """
    content = server_file.read_text()
    
    tool_pattern = rf'Tool\(\s*name="{tool_name}"'
    match = re.search(tool_pattern, content)
    
    if not match:
        return None
    
    start_pos = match.start()
    
    input_schema_pattern = r'inputSchema=\s*\{'
    schema_match = re.search(input_schema_pattern, content[start_pos:start_pos + 5000])
    
    if not schema_match:
        return None
    
    schema_start = start_pos + schema_match.end() - 1
    schema_str = extract_dict_string(content, schema_start)
    
    try:
        schema = ast.literal_eval(schema_str)
        properties = schema.get("properties", {})
        return properties
    except Exception as e:
        print(f"Error parsing schema for {tool_name}: {e}")
        return None


def extract_dict_string(content: str, start_pos: int) -> str:
    """Extract dictionary string from content starting at position."""
    brace_count = 0
    in_string = False
    escape_next = False
    quote_char = None
    result = []
    
    i = start_pos
    while i < len(content):
        char = content[i]
        
        if escape_next:
            result.append(char)
            escape_next = False
            i += 1
            continue
        
        if char == "\\":
            escape_next = True
            result.append(char)
            i += 1
            continue
        
        if char in ('"', "'") and not escape_next:
            if not in_string:
                in_string = True
                quote_char = char
            elif char == quote_char:
                in_string = False
                quote_char = None
            result.append(char)
            i += 1
            continue
        
        if not in_string:
            if char == "{":
                brace_count += 1
            elif char == "}":
                brace_count -= 1
                if brace_count == 0:
                    result.append(char)
                    break
        
        result.append(char)
        i += 1
    
    return "".join(result)


def test_schema_fix(tool_name: str, param_name: str, expected_max: int, expected_default: int) -> bool:
    """Test that a schema parameter has the correct values.
    
    Args:
        tool_name: Tool name
        param_name: Parameter name
        expected_max: Expected maximum value
        expected_default: Expected default value
        
    Returns:
        True if test passes, False otherwise
    """
    server_file = Path(__file__).parent.parent / "wistx_mcp" / "server.py"
    properties = extract_tool_schema(server_file, tool_name)
    
    if not properties:
        print(f"❌ {tool_name}: Schema not found")
        return False
    
    if param_name not in properties:
        print(f"❌ {tool_name}.{param_name}: Parameter not found in schema")
        return False
    
    param_schema = properties[param_name]
    actual_max = param_schema.get("maximum")
    actual_default = param_schema.get("default")
    
    passed = True
    
    if actual_max != expected_max:
        print(f"❌ {tool_name}.{param_name}: maximum={actual_max}, expected={expected_max}")
        passed = False
    else:
        print(f"✅ {tool_name}.{param_name}: maximum={actual_max} (correct)")
    
    if actual_default != expected_default:
        print(f"❌ {tool_name}.{param_name}: default={actual_default}, expected={expected_default}")
        passed = False
    else:
        print(f"✅ {tool_name}.{param_name}: default={actual_default} (correct)")
    
    return passed


def main():
    """Run all schema fix tests."""
    print("=" * 80)
    print("Testing Schema Fixes")
    print("=" * 80)
    print()
    
    tests = [
        ("wistx_web_search", "limit", 50000, 1000),
        ("wistx_search_codebase", "limit", 50000, 1000),
        ("wistx_research_knowledge_base", "max_results", 50000, 100),
    ]
    
    passed = 0
    failed = 0
    
    for tool_name, param_name, expected_max, expected_default in tests:
        print(f"\nTesting {tool_name}.{param_name}:")
        if test_schema_fix(tool_name, param_name, expected_max, expected_default):
            passed += 1
        else:
            failed += 1
    
    print()
    print("=" * 80)
    print("Test Results")
    print("=" * 80)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Total: {passed + failed}")
    print()
    
    if failed == 0:
        print("🎉 All schema fixes verified!")
        return 0
    else:
        print("⚠️  Some schema fixes need attention")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())

