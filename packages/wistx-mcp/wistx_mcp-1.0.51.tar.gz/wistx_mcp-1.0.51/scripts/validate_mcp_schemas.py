"""Validate MCP tool schemas against their implementations.

This script systematically checks all tool schemas in wistx_mcp/server.py
against their actual function signatures and implementations to find mismatches.
"""

import ast
import inspect
import logging
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SchemaValidator:
    """Validate MCP tool schemas against implementations."""

    def __init__(self):
        """Initialize validator."""
        self.mismatches: list[dict[str, Any]] = []
        self.tools_checked = 0

    def extract_schema_limits(self, schema: dict[str, Any]) -> dict[str, dict[str, Any]]:
        """Extract min/max/default values from schema properties.
        
        Args:
            schema: Tool inputSchema dictionary
            
        Returns:
            Dictionary mapping parameter names to their limits
        """
        limits = {}
        properties = schema.get("properties", {})
        
        for param_name, param_schema in properties.items():
            param_info = {
                "type": param_schema.get("type"),
                "minimum": param_schema.get("minimum"),
                "maximum": param_schema.get("maximum"),
                "default": param_schema.get("default"),
                "minLength": param_schema.get("minLength"),
                "maxLength": param_schema.get("maxLength"),
                "enum": param_schema.get("enum"),
                "required": param_name in schema.get("required", []),
            }
            limits[param_name] = param_info
        
        return limits

    def extract_function_signature(self, tool_name: str) -> dict[str, Any] | None:
        """Extract function signature and validation logic from implementation.
        
        Args:
            tool_name: Tool name (e.g., 'wistx_research_knowledge_base')
            
        Returns:
            Dictionary with function signature info, or None if not found
        """
        function_name = tool_name.replace("wistx_", "")
        
        try:
            if tool_name == "wistx_research_knowledge_base":
                from wistx_mcp.tools import mcp_tools
                func = getattr(mcp_tools, "research_knowledge_base", None)
            elif tool_name == "wistx_web_search":
                from wistx_mcp.tools import web_search
                func = getattr(web_search, "web_search", None)
            elif tool_name == "wistx_get_compliance_requirements":
                from wistx_mcp.tools import mcp_tools
                func = getattr(mcp_tools, "get_compliance_requirements", None)
            elif tool_name == "wistx_calculate_infrastructure_cost":
                from wistx_mcp.tools import pricing
                func = getattr(pricing, "calculate_infrastructure_cost", None)
            elif tool_name == "wistx_index_repository":
                from wistx_mcp.tools import user_indexing
                func = getattr(user_indexing, "index_repository", None)
            elif tool_name == "wistx_index_resource":
                from wistx_mcp.tools import user_indexing
                func = getattr(user_indexing, "index_content", None)
            elif tool_name == "wistx_list_resources":
                from wistx_mcp.tools import user_indexing
                func = getattr(user_indexing, "list_resources", None)
            elif tool_name == "wistx_check_resource_status":
                from wistx_mcp.tools import user_indexing
                func = getattr(user_indexing, "check_resource_status", None)
            elif tool_name == "wistx_delete_resource":
                from wistx_mcp.tools import user_indexing
                func = getattr(user_indexing, "delete_resource", None)
            elif tool_name == "wistx_search_codebase":
                from wistx_mcp.tools import search_codebase
                func = getattr(search_codebase, "search_codebase", None)
            elif tool_name == "wistx_regex_search":
                from wistx_mcp.tools import regex_search
                func = getattr(regex_search, "regex_search_codebase", None)
            elif tool_name == "wistx_design_architecture":
                from wistx_mcp.tools import design_architecture
                func = getattr(design_architecture, "design_architecture", None)
            elif tool_name == "wistx_troubleshoot_issue":
                from wistx_mcp.tools import troubleshoot_issue
                func = getattr(troubleshoot_issue, "troubleshoot_issue", None)
            elif tool_name == "wistx_generate_documentation":
                from wistx_mcp.tools import generate_documentation
                func = getattr(generate_documentation, "generate_documentation", None)
            elif tool_name == "wistx_manage_infrastructure_lifecycle":
                from wistx_mcp.tools import manage_infrastructure_lifecycle
                func = getattr(manage_infrastructure_lifecycle, "manage_infrastructure_lifecycle", None)
            elif tool_name == "wistx_search_devops_resources":
                from wistx_mcp.tools import package_search
                func = getattr(package_search, "search_devops_resources", None)
            elif tool_name == "wistx_read_package_file":
                from wistx_mcp.tools import package_search
                func = getattr(package_search, "read_package_file_mcp", None)
            elif tool_name == "wistx_get_existing_infrastructure":
                from wistx_mcp.tools import infrastructure_context
                func = getattr(infrastructure_context, "get_existing_infrastructure", None)
            elif tool_name == "wistx_get_devops_infra_code_examples":
                from wistx_mcp.tools import code_examples
                func = getattr(code_examples, "get_code_examples", None)
            else:
                logger.warning("Unknown tool: %s", tool_name)
                return None
            
            if func is None:
                logger.warning("Function not found for tool: %s", tool_name)
                return None
            
            sig = inspect.signature(func)
            func_info = {
                "name": func.__name__,
                "parameters": {},
                "source_file": inspect.getfile(func),
            }
            
            for param_name, param in sig.parameters.items():
                param_info = {
                    "name": param_name,
                    "kind": str(param.kind),
                    "default": param.default if param.default != inspect.Parameter.empty else None,
                    "annotation": str(param.annotation) if param.annotation != inspect.Parameter.empty else None,
                }
                func_info["parameters"][param_name] = param_info
            
            func_info["source_code"] = inspect.getsource(func)
            
            return func_info
            
        except Exception as e:
            logger.error("Error extracting function signature for %s: %s", tool_name, e)
            return None

    def find_validation_logic(self, source_code: str, param_name: str) -> dict[str, Any] | None:
        """Find validation logic for a parameter in function source code.
        
        Args:
            source_code: Function source code
            param_name: Parameter name
            
        Returns:
            Dictionary with validation limits found, or None
        """
        validation = {}
        
        patterns = [
            (rf"{param_name}\s*<\s*(\d+)", "maximum"),
            (rf"{param_name}\s*>\s*(\d+)", "minimum"),
            (rf"{param_name}\s*<=\s*(\d+)", "maximum"),
            (rf"{param_name}\s*>=\s*(\d+)", "minimum"),
            (rf"len\({param_name}\)\s*>\s*(\d+)", "minLength"),
            (rf"len\({param_name}\)\s*<\s*(\d+)", "maxLength"),
            (rf"len\({param_name}\)\s*>=\s*(\d+)", "minLength"),
            (rf"len\({param_name}\)\s*<=\s*(\d+)", "maxLength"),
        ]
        
        for pattern, limit_type in patterns:
            matches = re.findall(pattern, source_code)
            if matches:
                validation[limit_type] = int(matches[0])
        
        if not validation:
            return None
        
        return validation

    def check_parameter_mismatch(
        self,
        tool_name: str,
        param_name: str,
        schema_info: dict[str, Any],
        func_info: dict[str, Any] | None,
    ) -> dict[str, Any] | None:
        """Check if schema parameter matches function implementation.
        
        Args:
            tool_name: Tool name
            param_name: Parameter name
            schema_info: Schema parameter info
            func_info: Function signature info
            
        Returns:
            Mismatch dictionary if found, None otherwise
        """
        if func_info is None:
            return None
        
        func_params = func_info.get("parameters", {})
        if param_name not in func_params:
            return {
                "tool": tool_name,
                "parameter": param_name,
                "issue": "parameter_not_in_function",
                "schema": schema_info,
                "function": None,
            }
        
        func_param = func_params[param_name]
        source_code = func_info.get("source_code", "")
        
        mismatches = []
        
        if schema_info.get("type") == "integer":
            schema_min = schema_info.get("minimum")
            schema_max = schema_info.get("maximum")
            schema_default = schema_info.get("default")
            
            func_default = func_param.get("default")
            if func_default is not None and func_default != inspect.Parameter.empty:
                if schema_default is not None and func_default != schema_default:
                    mismatches.append({
                        "field": "default",
                        "schema": schema_default,
                        "function": func_default,
                    })
            
            validation = self.find_validation_logic(source_code, param_name)
            if validation:
                func_min = validation.get("minimum")
                func_max = validation.get("maximum")
                
                if func_min is not None and schema_min is not None and func_min != schema_min:
                    mismatches.append({
                        "field": "minimum",
                        "schema": schema_min,
                        "function": func_min,
                    })
                
                if func_max is not None and schema_max is not None and func_max != schema_max:
                    mismatches.append({
                        "field": "maximum",
                        "schema": schema_max,
                        "function": func_max,
                    })
        
        elif schema_info.get("type") == "string":
            schema_min_len = schema_info.get("minLength")
            schema_max_len = schema_info.get("maxLength")
            
            validation = self.find_validation_logic(source_code, param_name)
            if validation:
                func_min_len = validation.get("minLength")
                func_max_len = validation.get("maxLength")
                
                if func_min_len is not None and schema_min_len is not None and func_min_len != schema_min_len:
                    mismatches.append({
                        "field": "minLength",
                        "schema": schema_min_len,
                        "function": func_min_len,
                    })
                
                if func_max_len is not None and schema_max_len is not None and func_max_len != schema_max_len:
                    mismatches.append({
                        "field": "maxLength",
                        "schema": schema_max_len,
                        "function": func_max_len,
                    })
        
        if mismatches:
            return {
                "tool": tool_name,
                "parameter": param_name,
                "issue": "limit_mismatch",
                "mismatches": mismatches,
                "schema": schema_info,
                "function": func_param,
            }
        
        return None

    def validate_tool(self, tool_name: str, schema: dict[str, Any]) -> list[dict[str, Any]]:
        """Validate a single tool's schema against its implementation.
        
        Args:
            tool_name: Tool name
            schema: Tool inputSchema dictionary
            
        Returns:
            List of mismatches found
        """
        mismatches = []
        self.tools_checked += 1
        
        logger.info("Validating tool: %s", tool_name)
        
        schema_limits = self.extract_schema_limits(schema)
        func_info = self.extract_function_signature(tool_name)
        
        for param_name, schema_info in schema_limits.items():
            mismatch = self.check_parameter_mismatch(
                tool_name,
                param_name,
                schema_info,
                func_info,
            )
            if mismatch:
                mismatches.append(mismatch)
        
        return mismatches

    def extract_tools_from_server(self) -> list[tuple[str, dict[str, Any]]]:
        """Extract all Tool definitions from server.py.
        
        Returns:
            List of (tool_name, schema) tuples
        """
        server_file = Path(__file__).parent.parent / "wistx_mcp" / "server.py"
        
        if not server_file.exists():
            logger.error("server.py not found: %s", server_file)
            return []
        
        content = server_file.read_text()
        
        tools = []
        
        tool_pattern = r'Tool\(\s*name="(wistx_\w+)"'
        tool_matches = list(re.finditer(tool_pattern, content))
        
        for match in tool_matches:
            tool_name = match.group(1)
            start_pos = match.start()
            
            input_schema_pattern = r'inputSchema=\s*\{'
            schema_match = re.search(input_schema_pattern, content[start_pos:start_pos + 5000])
            
            if schema_match:
                schema_start = start_pos + schema_match.end() - 1
                schema_str = self._extract_dict(content, schema_start)
                
                try:
                    import json
                    schema = ast.literal_eval(schema_str)
                    tools.append((tool_name, schema))
                except Exception as e:
                    logger.warning("Failed to parse schema for %s: %s", tool_name, e)
        
        return tools

    def _extract_dict(self, content: str, start_pos: int) -> str:
        """Extract dictionary string from content starting at position.
        
        Args:
            content: File content
            start_pos: Starting position
            
        Returns:
            Dictionary string
        """
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

    def validate_all(self) -> list[dict[str, Any]]:
        """Validate all tools.
        
        Returns:
            List of all mismatches found
        """
        tools = self.extract_tools_from_server()
        logger.info("Found %d tools to validate", len(tools))
        
        all_mismatches = []
        
        for tool_name, schema in tools:
            mismatches = self.validate_tool(tool_name, schema)
            all_mismatches.extend(mismatches)
        
        return all_mismatches

    def generate_fix_report(self, mismatches: list[dict[str, Any]]) -> str:
        """Generate a report with recommended fixes.
        
        Args:
            mismatches: List of mismatch dictionaries
            
        Returns:
            Markdown report string
        """
        if not mismatches:
            return "# Schema Validation Report\n\n✅ **No mismatches found!** All schemas match their implementations.\n"
        
        report = ["# Schema Validation Report\n"]
        report.append(f"## Summary\n\n")
        report.append(f"- **Tools Checked**: {self.tools_checked}\n")
        report.append(f"- **Mismatches Found**: {len(mismatches)}\n\n")
        
        report.append("## Mismatches\n\n")
        
        for mismatch in mismatches:
            tool_name = mismatch["tool"]
            param_name = mismatch["parameter"]
            issue = mismatch["issue"]
            
            report.append(f"### {tool_name} - `{param_name}`\n\n")
            report.append(f"**Issue**: {issue}\n\n")
            
            if issue == "limit_mismatch":
                for m in mismatch["mismatches"]:
                    field = m["field"]
                    schema_val = m["schema"]
                    func_val = m["function"]
                    
                    report.append(f"- **{field}**: Schema={schema_val}, Function={func_val}\n")
                    report.append(f"  - **Fix**: Update schema `{field}` from `{schema_val}` to `{func_val}`\n")
            
            elif issue == "parameter_not_in_function":
                report.append(f"- Parameter `{param_name}` is in schema but not in function signature\n")
                report.append(f"  - **Fix**: Remove parameter from schema or add to function\n")
            
            report.append("\n")
        
        report.append("## Recommended Fixes\n\n")
        report.append("1. Review each mismatch above\n")
        report.append("2. Update schemas in `wistx_mcp/server.py` to match function implementations\n")
        report.append("3. Re-run validation to confirm fixes\n")
        report.append("4. Add unit tests to prevent future mismatches\n")
        
        return "".join(report)


def main():
    """Main validation function."""
    validator = SchemaValidator()
    
    logger.info("Starting schema validation...")
    mismatches = validator.validate_all()
    
    logger.info("Validation complete. Found %d mismatches", len(mismatches))
    
    report = validator.generate_fix_report(mismatches)
    
    report_file = Path(__file__).parent.parent / "docs" / "SCHEMA_VALIDATION_REPORT.md"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(report)
    
    print("\n" + "=" * 80)
    print(report)
    print("=" * 80)
    print(f"\nReport saved to: {report_file}")
    
    if mismatches:
        print("\n⚠️  MISMATCHES FOUND - Review and fix before production deployment")
        return 1
    else:
        print("\n✅ All schemas validated successfully!")
        return 0


if __name__ == "__main__":
    sys.exit(main())

