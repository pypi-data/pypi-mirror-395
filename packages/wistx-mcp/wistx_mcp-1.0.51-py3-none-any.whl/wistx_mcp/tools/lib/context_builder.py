"""Context builder - format data for LLM context using markdown."""

import markdown as markdown_lib
from typing import Any

from wistx_mcp.tools.lib.constants import (
    MAX_DISPLAY_SERVICES_PER_COMPONENT,
    MAX_DISPLAY_COMPLIANCE_CONTROLS,
)


class MarkdownBuilder:
    """Helper class for building markdown strings consistently."""

    def __init__(self):
        """Initialize markdown builder."""
        self.lines: list[str] = []

    def add_header(self, text: str, level: int = 1) -> "MarkdownBuilder":
        """Add a header.

        Args:
            text: Header text
            level: Header level (1-6)

        Returns:
            Self for method chaining
        """
        prefix = "#" * min(max(level, 1), 6)
        self.lines.append(f"{prefix} {text}\n")
        return self

    def add_paragraph(self, text: str) -> "MarkdownBuilder":
        """Add a paragraph.

        Args:
            text: Paragraph text

        Returns:
            Self for method chaining
        """
        self.lines.append(f"{text}\n")
        return self

    def add_bold(self, text: str) -> "MarkdownBuilder":
        """Add bold text.

        Args:
            text: Text to make bold

        Returns:
            Self for method chaining
        """
        self.lines.append(f"**{text}**")
        return self

    def add_code_block(self, code: str, language: str = "") -> "MarkdownBuilder":
        """Add a code block.

        Args:
            code: Code content
            language: Language identifier

        Returns:
            Self for method chaining
        """
        lang = language if language else ""
        self.lines.append(f"```{lang}\n{code}\n```\n")
        return self

    def add_list_item(self, text: str, indent: int = 0) -> "MarkdownBuilder":
        """Add a list item.

        Args:
            text: List item text
            indent: Indentation level

        Returns:
            Self for method chaining
        """
        prefix = "  " * indent + "- "
        self.lines.append(f"{prefix}{text}\n")
        return self

    def add_separator(self) -> "MarkdownBuilder":
        """Add a horizontal separator.

        Returns:
            Self for method chaining
        """
        self.lines.append("---\n")
        return self

    def add_line_break(self) -> "MarkdownBuilder":
        """Add a line break.

        Returns:
            Self for method chaining
        """
        self.lines.append("\n")
        return self

    def build(self, validate: bool = True) -> str:
        """Build the markdown string.

        Args:
            validate: Whether to validate the markdown syntax

        Returns:
            Formatted markdown string

        Raises:
            ValueError: If markdown validation fails and validate=True
        """
        result = "".join(self.lines)
        
        if not result.strip():
            return ""
        
        if validate:
            try:
                html_output = markdown_lib.markdown(result)
                if not html_output or html_output.strip() == "":
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.warning("Markdown produced empty HTML output")
            except (ValueError, TypeError, AttributeError) as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.warning("Markdown validation warning: %s", e)
        
        return result

    def reset(self) -> "MarkdownBuilder":
        """Reset the builder.

        Returns:
            Self for method chaining
        """
        self.lines = []
        return self


class TOONBuilder:
    """Helper class for building TOON format strings for LLM consumption."""

    def __init__(self):
        """Initialize TOON builder."""
        self.lines: list[str] = []
        self.current_array: list[dict[str, Any]] | None = None
        self.array_fields: list[str] | None = None

    def start_array(self, fields: list[str], count: int | None = None) -> "TOONBuilder":
        """Start a tabular array with field headers.

        Args:
            fields: List of field names
            count: Optional count (unused, calculated from data)

        Returns:
            Self for method chaining
        """
        self.array_fields = fields
        self.current_array = []
        return self

    def add_array_row(self, values: dict[str, Any]) -> "TOONBuilder":
        """Add a row to the current array.

        Args:
            values: Dictionary of field values

        Returns:
            Self for method chaining
        """
        if self.current_array is None:
            raise ValueError("Must call start_array() before add_array_row()")
        self.current_array.append(values)
        return self

    def add_single_object(self, fields: list[str], values: dict[str, Any]) -> "TOONBuilder":
        """Add a single object (non-array).

        Args:
            fields: List of field names
            values: Dictionary of field values

        Returns:
            Self for method chaining
        """
        field_str = ",".join(fields)
        value_list = [self._escape_value(values.get(f, "")) for f in fields]
        value_str = ",".join(value_list)
        self.lines.append(f"{{{field_str}}}:\n{value_str}")
        return self

    def _escape_value(self, value: Any) -> str:
        """Escape TOON value (handle newlines, commas, special chars).

        Args:
            value: Value to escape

        Returns:
            Escaped string
        """
        if value is None:
            return ""
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, list):
            return "|".join(str(v) for v in value)
        if isinstance(value, dict):
            return self._serialize_dict(value)

        str_value = str(value)
        if "\n" in str_value or "," in str_value or '"' in str_value:
            escaped = str_value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
            return f'"{escaped}"'
        return str_value

    def _serialize_dict(self, d: dict[str, Any]) -> str:
        """Serialize nested dictionary to compact format.

        Args:
            d: Dictionary to serialize

        Returns:
            Serialized string
        """
        parts = []
        for k, v in d.items():
            if v is None or v == "":
                continue
            if isinstance(v, list):
                v_str = "|".join(str(item) for item in v)
            else:
                v_str = str(v)
            parts.append(f"{k}:{v_str}")
        return ";".join(parts)

    def build(self) -> str:
        """Build the final TOON string.

        Returns:
            Formatted TOON string
        """
        if self.current_array is not None and self.array_fields is not None:
            self._finalize_array()

        return "\n".join(self.lines)

    def _finalize_array(self) -> None:
        """Finalize the current array and add to lines."""
        if not self.current_array or not self.array_fields:
            return

        count = len(self.current_array)
        fields_str = ",".join(self.array_fields)

        self.lines.append(f"[{count}]{{{fields_str}}}:")

        for row in self.current_array:
            values = [self._escape_value(row.get(f, "")) for f in self.array_fields]
            self.lines.append(",".join(values))

        self.current_array = None
        self.array_fields = None

    def reset(self) -> "TOONBuilder":
        """Reset the builder.

        Returns:
            Self for method chaining
        """
        self.lines = []
        self.current_array = None
        self.array_fields = None
        return self


class ContextBuilder:
    """Build formatted context for LLM consumption using markdown."""

    @staticmethod
    def format_compliance_as_markdown(controls: list[dict[str, Any]], resource_type: str | None = None) -> str:
        """Format compliance controls as markdown for LLM consumption.

        Args:
            controls: List of compliance control dictionaries
            resource_type: Optional resource type for context

        Returns:
            Formatted markdown string
        """
        import logging
        logger = logging.getLogger(__name__)

        if not controls:
            return "No compliance controls found."

        if not isinstance(controls, list):
            logger.error("Controls must be a list, got %s", type(controls))
            return "Invalid controls format."

        builder = MarkdownBuilder()
        title = "Compliance Requirements"
        if resource_type:
            title += f" for {resource_type}"
        builder.add_header(title, level=1)

        for i, control in enumerate(controls):
            if not isinstance(control, dict):
                logger.warning("Control %d is not a dict, skipping", i)
                continue

            try:
                standard = control.get("standard", "Unknown")
                control_id = control.get("control_id", "")
                severity = control.get("severity", "MEDIUM")
                title_text = control.get("title", "")
                description = control.get("description", "")

                builder.add_header(f"{standard} {control_id}: {title_text}", level=2)
                builder.add_bold(f"Severity: {severity}")
                builder.add_line_break()
                builder.add_paragraph(str(description))

                remediation = control.get("remediation", {})
                if remediation and isinstance(remediation, dict):
                    if remediation.get("guidance"):
                        builder.add_header("Remediation Guidance", level=3)
                        builder.add_paragraph(str(remediation["guidance"]))

                    if remediation.get("code_snippet"):
                        builder.add_header("Code Example", level=3)
                        builder.add_code_block(str(remediation["code_snippet"]), language="hcl")

                verification = control.get("verification", {})
                if verification and isinstance(verification, dict):
                    if verification.get("procedure"):
                        builder.add_header("Verification", level=3)
                        builder.add_paragraph(str(verification["procedure"]))

                builder.add_separator()
            except (ValueError, TypeError, KeyError, AttributeError) as e:
                logger.warning("Error formatting control %d: %s", i, e)
                continue
            except Exception as e:  # noqa: BLE001
                logger.warning("Unexpected error formatting control %d: %s", i, e, exc_info=True)
                continue

        markdown_output = builder.build(validate=True)
        
        if not markdown_output or not markdown_output.strip():
            logger.warning("Generated markdown is empty")
            return "No compliance controls found."
        
        try:
            markdown_lib.markdown(markdown_output)
        except Exception as e:  # noqa: BLE001
            logger.error("Generated markdown failed validation: %s", e)
            return "Error formatting compliance requirements. Please try again."
        
        return markdown_output

    @staticmethod
    def format_compliance_as_toon(
        controls: list[dict[str, Any]], resource_type: str | None = None
    ) -> str:
        """Format compliance controls as TOON for LLM consumption.

        Args:
            controls: List of compliance control dictionaries
            resource_type: Optional resource type for context

        Returns:
            Formatted TOON string
        """
        import logging
        logger = logging.getLogger(__name__)

        if not controls:
            return "No compliance controls found."

        if not isinstance(controls, list):
            logger.error("Controls must be a list, got %s", type(controls))
            return "Invalid controls format."

        builder = TOONBuilder()

        if resource_type:
            builder.add_single_object(
                ["context"],
                {"context": f"Compliance Requirements for {resource_type}"}
            )
            builder.lines.append("")

        primary_fields = [
            "standard",
            "control_id",
            "title",
            "severity",
            "description"
        ]

        optional_fields = [
            "category",
            "subcategory",
            "applies_to",
            "remediation_guidance",
            "remediation_steps",
            "code_snippet",
            "verification",
            "references"
        ]

        all_fields = primary_fields + optional_fields

        builder.start_array(all_fields, len(controls))

        for i, control in enumerate(controls):
            if not isinstance(control, dict):
                logger.warning("Control %d is not a dict, skipping", i)
                continue

            try:
                row_data: dict[str, Any] = {}

                row_data["standard"] = control.get("standard", "Unknown")
                row_data["control_id"] = control.get("control_id", "")
                row_data["title"] = control.get("title", "")
                row_data["severity"] = control.get("severity", "MEDIUM")
                row_data["description"] = control.get("description", "")

                row_data["category"] = control.get("category", "")
                row_data["subcategory"] = control.get("subcategory", "")

                applies_to = control.get("applies_to", [])
                if isinstance(applies_to, list):
                    row_data["applies_to"] = ",".join(applies_to)
                else:
                    row_data["applies_to"] = str(applies_to) if applies_to else ""

                remediation = control.get("remediation", {})
                if remediation and isinstance(remediation, dict):
                    row_data["remediation_guidance"] = remediation.get("summary", "") or remediation.get("guidance", "")

                    steps = remediation.get("steps", [])
                    if isinstance(steps, list):
                        row_data["remediation_steps"] = "|".join(str(s) for s in steps)
                    else:
                        row_data["remediation_steps"] = ""

                    code_snippets = remediation.get("code_snippets", [])
                    if code_snippets and isinstance(code_snippets, list) and len(code_snippets) > 0:
                        first_snippet = code_snippets[0]
                        if isinstance(first_snippet, dict):
                            row_data["code_snippet"] = first_snippet.get("code", "")
                        elif hasattr(first_snippet, "code"):
                            row_data["code_snippet"] = first_snippet.code
                        else:
                            row_data["code_snippet"] = ""
                    elif remediation.get("code_snippet"):
                        row_data["code_snippet"] = str(remediation["code_snippet"])
                    else:
                        row_data["code_snippet"] = ""
                else:
                    row_data["remediation_guidance"] = ""
                    row_data["remediation_steps"] = ""
                    row_data["code_snippet"] = ""

                verification = control.get("verification", {})
                if verification and isinstance(verification, dict):
                    row_data["verification"] = verification.get("procedure", "")
                else:
                    row_data["verification"] = ""

                references = control.get("references", [])
                if isinstance(references, list) and references:
                    ref_urls = []
                    for ref in references:
                        if isinstance(ref, dict):
                            ref_urls.append(ref.get("url", ""))
                        elif hasattr(ref, "url"):
                            ref_urls.append(ref.url)
                    row_data["references"] = "|".join(ref_urls)
                else:
                    row_data["references"] = ""

                builder.add_array_row(row_data)

            except (ValueError, TypeError, KeyError, AttributeError) as e:
                logger.warning("Error formatting control %d: %s", i, e)
                continue
            except Exception as e:  # noqa: BLE001
                logger.warning("Unexpected error formatting control %d: %s", i, e, exc_info=True)
                continue

        toon_output = builder.build()

        if not toon_output or not toon_output.strip():
            logger.warning("Generated TOON is empty")
            return "No compliance controls found."

        return toon_output

    @staticmethod
    def format_compliance_context(controls: list[dict[str, Any]]) -> str:
        """Format compliance controls as context string (legacy method).

        Args:
            controls: List of compliance control dictionaries

        Returns:
            Formatted context string
        """
        return ContextBuilder.format_compliance_as_markdown(controls)

    @staticmethod
    def format_pricing_context(pricing: dict[str, Any]) -> str:
        """Format pricing data as context string.

        Args:
            pricing: Pricing data dictionary

        Returns:
            Formatted context string
        """
        builder = MarkdownBuilder()
        builder.add_header("Infrastructure Cost Estimate", level=2)
        builder.add_bold(f"Total Monthly: ${pricing.get('total_monthly', 0):.2f}")
        builder.add_line_break()
        builder.add_bold(f"Total Annual: ${pricing.get('total_annual', 0):.2f}")
        builder.add_line_break()

        budget_check = pricing.get("budget_check")
        if budget_check:
            builder.add_header("Budget Status", level=3)
            status = budget_check.get("status", "unknown")
            builder.add_bold(
                f"Status: {status.upper().replace('_', ' ')}"
            )
            builder.add_line_break()

            applicable_budgets = budget_check.get("applicable_budgets", [])
            if applicable_budgets:
                for budget_status in applicable_budgets:
                    builder.add_list_item(
                        f"**{budget_status['name']}**: "
                        f"${budget_status.get('current_spending', 0):.2f} spent, "
                        f"${budget_status.get('estimated_cost', 0):.2f} estimated → "
                        f"${budget_status.get('projected_spending', 0):.2f} projected "
                        f"({budget_status.get('utilization_percent', 0):.1f}% of "
                        f"${budget_status.get('budget_limit', 0):.2f} limit)"
                    )

            alerts = budget_check.get("alerts", [])
            if alerts:
                builder.add_header("Budget Alerts", level=3)
                for alert in alerts:
                    alert_type = alert.get("type", "warning").upper()
                    builder.add_list_item(
                        f"[{alert_type}] {alert.get('message', '')}"
                    )

        builder.add_header("Breakdown", level=3)

        for item in pricing.get("breakdown", []):
            resource_text = f"{item['resource']} (x{item['quantity']}): "
            resource_text += f"${item['monthly']:.2f}/month (${item['annual']:.2f}/year)"
            if item.get("region"):
                resource_text += f" [{item['region']}]"
            if item.get("pricing_category"):
                resource_text += f" ({item['pricing_category']})"
            if item.get("error"):
                resource_text += f" - [WARNING] {item['error']}"
            builder.add_list_item(resource_text)

        if pricing.get("optimizations"):
            builder.add_header("Optimization Suggestions", level=3)
            for opt in pricing["optimizations"]:
                builder.add_list_item(opt)

        return builder.build()

    @staticmethod
    def format_pricing_as_toon(pricing: dict[str, Any]) -> str:
        """Format pricing data as TOON for LLM consumption.

        Args:
            pricing: Pricing data dictionary

        Returns:
            Formatted TOON string
        """
        import logging
        logger = logging.getLogger(__name__)

        builder = TOONBuilder()

        builder.add_single_object(
            ["total_monthly", "total_annual"],
            {
                "total_monthly": f"{pricing.get('total_monthly', 0):.2f}",
                "total_annual": f"{pricing.get('total_annual', 0):.2f}"
            }
        )
        builder.lines.append("")

        budget_check = pricing.get("budget_check")
        if budget_check:
            status = budget_check.get("status", "unknown")
            builder.add_single_object(
                ["budget_status"],
                {"budget_status": status.upper().replace("_", " ")}
            )
            builder.lines.append("")

            applicable_budgets = budget_check.get("applicable_budgets", [])
            if applicable_budgets:
                budget_fields = [
                    "name",
                    "current_spending",
                    "estimated_cost",
                    "projected_spending",
                    "utilization_percent",
                    "budget_limit"
                ]
                builder.start_array(budget_fields, len(applicable_budgets))
                for budget_status in applicable_budgets:
                    builder.add_array_row({
                        "name": budget_status.get("name", ""),
                        "current_spending": f"{budget_status.get('current_spending', 0):.2f}",
                        "estimated_cost": f"{budget_status.get('estimated_cost', 0):.2f}",
                        "projected_spending": f"{budget_status.get('projected_spending', 0):.2f}",
                        "utilization_percent": f"{budget_status.get('utilization_percent', 0):.1f}",
                        "budget_limit": f"{budget_status.get('budget_limit', 0):.2f}"
                    })
                builder.lines.append("")

            alerts = budget_check.get("alerts", [])
            if alerts:
                builder.start_array(["type", "message"], len(alerts))
                for alert in alerts:
                    builder.add_array_row({
                        "type": alert.get("type", ""),
                        "message": alert.get("message", "")
                    })
                builder.lines.append("")

        breakdown = pricing.get("breakdown", [])
        if breakdown:
            breakdown_fields = [
                "resource",
                "quantity",
                "monthly",
                "annual",
                "region",
                "pricing_category",
                "error"
            ]
            builder.start_array(breakdown_fields, len(breakdown))
            for item in breakdown:
                builder.add_array_row({
                    "resource": item.get("resource", ""),
                    "quantity": str(item.get("quantity", 0)),
                    "monthly": f"{item.get('monthly', 0):.2f}",
                    "annual": f"{item.get('annual', 0):.2f}",
                    "region": item.get("region", ""),
                    "pricing_category": item.get("pricing_category", ""),
                    "error": item.get("error", "")
                })
            builder.lines.append("")

        optimizations = pricing.get("optimizations", [])
        if optimizations:
            builder.start_array(["optimization"], len(optimizations))
            for opt in optimizations:
                builder.add_array_row({"optimization": str(opt)})

        return builder.build()

    @staticmethod
    def format_code_examples_context(examples: list[dict[str, Any]]) -> str:
        """Format code examples as context string.

        Args:
            examples: List of code example dictionaries

        Returns:
            Formatted context string
        """
        if not examples:
            return "No code examples found."

        builder = MarkdownBuilder()
        builder.add_header("Code Examples", level=2)

        for example in examples:
            builder.add_header(example.get("title", "Example"), level=3)
            
            if example.get("contextual_description"):
                builder.add_paragraph(example["contextual_description"])
                builder.add_line_break()
            
            if example.get("description"):
                builder.add_bold(f"Description: {example['description']}")
                builder.add_line_break()
            
            code_type = example.get("code_type") or example.get("language") or example.get("infrastructure_type")
            cloud_provider = example.get("cloud_provider", "")
            services = example.get("services", [])
            resources = example.get("resources", [])
            
            builder.add_bold(f"Code Type: {code_type}")
            builder.add_line_break()
            
            if cloud_provider:
                builder.add_bold(f"Cloud Provider: {cloud_provider.upper()}")
                builder.add_line_break()
            
            if services:
                builder.add_bold(f"Services: {', '.join(services)}")
                builder.add_line_break()
            
            if resources:
                builder.add_bold(f"Resources: {', '.join(resources[:5])}")
                builder.add_line_break()
            
            github_url = example.get("github_url")
            if github_url:
                builder.add_bold(f"Source: {github_url}")
                builder.add_line_break()
            
            quality_score = example.get("quality_score", 0)
            stars = example.get("stars", 0)
            if quality_score > 0 or stars > 0:
                builder.add_bold(f"Quality Score: {quality_score}/100 | Stars: {stars}")
                builder.add_line_break()
            
            builder.add_code_block(example.get("code", ""), language=code_type or "")

        return builder.build()

    @staticmethod
    def format_code_examples_as_toon(
        examples: list[dict[str, Any]],
        suggestions: dict[str, Any] | None = None,
        message: str | None = None,
    ) -> str:
        """Format code examples as TOON for LLM consumption.

        Args:
            examples: List of code example dictionaries

        Returns:
            Formatted TOON string
        """
        import logging
        logger = logging.getLogger(__name__)

        if not examples:
            if suggestions or message:
                builder = MarkdownBuilder()
                builder.add_header("Infrastructure Code Examples", level=1)
                if message:
                    builder.add_paragraph(f"**{message}**")
                    builder.add_line_break()
                
                if suggestions:
                    builder.add_header("💡 Query Suggestions", level=2)
                    
                    alternative_queries = suggestions.get("alternative_queries", [])
                    if alternative_queries:
                        builder.add_header("Alternative Queries", level=3)
                        for alt_query in alternative_queries:
                            builder.add_list_item(f"`{alt_query}`")
                        builder.add_line_break()
                    
                    tips = suggestions.get("tips", [])
                    if tips:
                        builder.add_header("Search Tips", level=3)
                        for tip in tips:
                            builder.add_list_item(tip)
                        builder.add_line_break()
                
                return builder.build()
            return "No code examples found."

        if not isinstance(examples, list):
            logger.error("Examples must be a list, got %s", type(examples))
            return "Invalid examples format."

        builder = TOONBuilder()

        example_fields = [
            "title",
            "contextual_description",
            "description",
            "code_type",
            "cloud_provider",
            "services",
            "resources",
            "github_url",
            "quality_score",
            "stars",
            "code"
        ]

        builder.start_array(example_fields, len(examples))

        for i, example in enumerate(examples):
            if not isinstance(example, dict):
                logger.warning("Example %d is not a dict, skipping", i)
                continue

            try:
                code_type = example.get("code_type") or example.get("language") or example.get("infrastructure_type") or ""
                services = example.get("services", [])
                resources = example.get("resources", [])

                row_data: dict[str, Any] = {
                    "title": example.get("title", ""),
                    "contextual_description": example.get("contextual_description", ""),
                    "description": example.get("description", ""),
                    "code_type": code_type,
                    "cloud_provider": example.get("cloud_provider", ""),
                    "services": ",".join(services) if isinstance(services, list) else str(services),
                    "resources": ",".join(resources[:10]) if isinstance(resources, list) else str(resources),
                    "github_url": example.get("github_url", ""),
                    "quality_score": str(example.get("quality_score", 0)),
                    "stars": str(example.get("stars", 0)),
                    "code": example.get("code", "")
                }

                builder.add_array_row(row_data)

            except (ValueError, TypeError, KeyError, AttributeError) as e:
                logger.warning("Error formatting example %d: %s", i, e)
                continue
            except Exception as e:  # noqa: BLE001
                logger.warning("Unexpected error formatting example %d: %s", i, e, exc_info=True)
                continue

        toon_output = builder.build()

        if not toon_output or not toon_output.strip():
            logger.warning("Generated TOON is empty")
            return "No code examples found."

        return toon_output

    @staticmethod
    def format_web_search_results(results: dict[str, Any]) -> str:
        """Format web search results as markdown.

        Args:
            results: Web search results dictionary

        Returns:
            Formatted markdown string
        """
        builder = MarkdownBuilder()
        builder.add_header("Web Search Results", level=1)
        builder.add_bold(f"Total Results: {results.get('total', 0)}")
        builder.add_line_break()

        if results.get("web"):
            builder.add_header("Web Search Results", level=2)
            for item in results["web"][:10]:
                if item.get("type") == "answer":
                    builder.add_header(item.get("title", "AI Answer"), level=3)
                    builder.add_paragraph(item.get("content", ""))
                else:
                    builder.add_header(item.get("title", "Result"), level=3)
                    if item.get("url"):
                        builder.add_bold(f"URL: {item['url']}")
                        builder.add_line_break()
                    if item.get("content"):
                        content = item["content"][:500]
                        builder.add_paragraph(content)
                    if item.get("score"):
                        builder.add_bold(f"Relevance Score: {item['score']:.2f}")
                        builder.add_line_break()
                builder.add_separator()

        if results.get("web_results"):
            builder.add_header("Real-Time Web Research", level=2)
            web_results = results["web_results"]
            
            freshness_info = web_results.get("freshness_info", {})
            if freshness_info:
                max_age = freshness_info.get("max_age_days", 0)
                builder.add_bold(f"Data Freshness: Results from last {max_age} days")
                builder.add_line_break()
            
            if web_results.get("answer"):
                builder.add_header("AI Summary", level=3)
                builder.add_paragraph(web_results["answer"])
            if web_results.get("results"):
                builder.add_header("Web Sources", level=3)
                for item in web_results["results"][:5]:
                    builder.add_bold(item.get("title", "Source"))
                    builder.add_line_break()
                    if item.get("url"):
                        builder.add_paragraph(f"URL: {item['url']}")
                    if item.get("published_date"):
                        builder.add_paragraph(f"Published: {item['published_date']}")
                    if item.get("content"):
                        content = item["content"][:300]
                        builder.add_paragraph(content)
                    builder.add_separator()

        if results.get("security"):
            builder.add_header("Security Information", level=2)
            for item in results["security"][:10]:
                title = item.get("title") or item.get("cve_id") or "Security Item"
                builder.add_header(title, level=3)
                if item.get("description"):
                    builder.add_paragraph(item["description"])
                if item.get("severity"):
                    builder.add_bold(f"Severity: {item['severity']}")
                    builder.add_line_break()
                if item.get("source"):
                    builder.add_bold(f"Source: {item['source']}")
                    builder.add_line_break()
                if item.get("published_date"):
                    builder.add_bold(f"Published: {item['published_date']}")
                    builder.add_line_break()
                builder.add_separator()

        if results.get("compliance"):
            builder.add_header("Compliance Requirements", level=2)
            compliance_md = ContextBuilder.format_compliance_as_markdown(results["compliance"])
            builder.add_paragraph(compliance_md)

        if results.get("best_practices"):
            builder.add_header("Best Practices", level=2)
            for item in results["best_practices"][:10]:
                builder.add_header(item.get("title", "Best Practice"), level=3)
                if item.get("summary"):
                    builder.add_paragraph(item["summary"])
                if item.get("domain"):
                    builder.add_bold(f"Domain: {item['domain']}")
                    builder.add_line_break()
                builder.add_separator()

        if results.get("knowledge"):
            builder.add_header("Knowledge Base", level=2)
            for item in results["knowledge"][:10]:
                builder.add_header(item.get("title", "Knowledge Article"), level=3)
                if item.get("summary"):
                    builder.add_paragraph(item["summary"])
                if item.get("domain"):
                    builder.add_bold(f"Domain: {item['domain']}")
                    builder.add_line_break()
                builder.add_separator()

        return builder.build()

    @staticmethod
    def format_codebase_search_results(results: dict[str, Any]) -> str:
        """Format codebase search results as markdown.

        Args:
            results: Codebase search results dictionary

        Returns:
            Formatted markdown string
        """
        # Check if this is a setup guide response
        if results.get("setup_required"):
            return ContextBuilder.format_indexing_setup_guide(results)
        
        builder = MarkdownBuilder()
        builder.add_header("Codebase Search Results", level=1)
        builder.add_bold(f"Total Results: {results.get('total', 0)}")
        builder.add_line_break()

        if results.get("ai_analysis"):
            ai_analysis = results["ai_analysis"]
            builder.add_header("AI Analysis", level=2)
            if ai_analysis.get("analysis"):
                builder.add_paragraph(ai_analysis["analysis"])
            builder.add_separator()

        if results.get("resources"):
            builder.add_header("Resources", level=2)
            for resource in results["resources"]:
                builder.add_list_item(
                    f"**{resource.get('name', 'Unknown')}** "
                    f"({resource.get('resource_type', 'unknown')})"
                )

        # Show empty results metadata if present
        if results.get("empty_results_metadata"):
            metadata = results["empty_results_metadata"]
            builder.add_header("⚠️ No Results Found", level=2)
            builder.add_paragraph(f"**{metadata.get('explanation', 'No results found')}**")
            builder.add_line_break()
            
            possible_causes = metadata.get("possible_causes", [])
            if possible_causes:
                builder.add_header("Possible Causes", level=3)
                for cause in possible_causes:
                    builder.add_list_item(cause)
                builder.add_line_break()
            
            suggestions = metadata.get("suggestions", [])
            if suggestions:
                builder.add_header("Suggestions", level=3)
                for suggestion in suggestions:
                    builder.add_list_item(suggestion)
                builder.add_line_break()
            
            builder.add_separator()
            builder.add_line_break()

        if results.get("results"):
            builder.add_header("Search Results", level=2)
            for result in results["results"][:20]:
                builder.add_header(result.get("title", "Result"), level=3)
                builder.add_bold(f"Source: {result.get('source_type', 'unknown')}")
                builder.add_line_break()
                if result.get("summary"):
                    builder.add_paragraph(result["summary"])

                if result.get("content"):
                    content = result.get("content", "")[:500]
                    builder.add_code_block(content)

                if result.get("source_url"):
                    builder.add_bold(f"Source URL: {result['source_url']}")
                    builder.add_line_break()

                builder.add_separator()

        if results.get("highlights"):
            builder.add_header("Code Highlights", level=2)
            for highlight in results["highlights"][:5]:
                if highlight.get("file_path"):
                    builder.add_bold(f"File: {highlight['file_path']}")
                    builder.add_line_break()
                builder.add_code_block(highlight.get("highlight", ""))

        return builder.build()

    @staticmethod
    def format_regex_search_results(results: dict[str, Any]) -> str:
        """Format regex search results as markdown.

        Args:
            results: Regex search results dictionary

        Returns:
            Formatted markdown string
        """
        # Check if this is a setup guide response
        if results.get("setup_required"):
            return ContextBuilder.format_indexing_setup_guide(results)
        
        builder = MarkdownBuilder()
        builder.add_header("Regex Search Results", level=1)
        builder.add_bold(f"Total Matches: {results.get('total', 0)}")
        builder.add_line_break()

        # Show empty results metadata if present
        if results.get("empty_results_metadata"):
            metadata = results["empty_results_metadata"]
            builder.add_header("⚠️ No Matches Found", level=2)
            builder.add_paragraph(f"**{metadata.get('explanation', 'No matches found')}**")
            builder.add_line_break()
            
            if metadata.get("files_searched") is not None:
                builder.add_bold(f"Files searched: {metadata['files_searched']}")
                builder.add_line_break()
            
            possible_causes = metadata.get("possible_causes", [])
            if possible_causes:
                builder.add_header("Possible Causes", level=3)
                for cause in possible_causes:
                    builder.add_list_item(cause)
                builder.add_line_break()
            
            suggestions = metadata.get("suggestions", [])
            if suggestions:
                builder.add_header("Suggestions", level=3)
                for suggestion in suggestions:
                    builder.add_list_item(suggestion)
                builder.add_line_break()
            
            builder.add_separator()
            builder.add_line_break()

        if results.get("helpful_message"):
            builder.add_header("⚠️ Important Information", level=2)
            builder.add_paragraph(results["helpful_message"])
            builder.add_line_break()

        if results.get("suggestion"):
            suggestion = results["suggestion"]
            builder.add_header("💡 Suggestion", level=2)
            builder.add_paragraph(suggestion.get("message", ""))
            builder.add_line_break()

        pattern_info = results.get("pattern_info", {})
        if pattern_info:
            builder.add_header("Pattern Information", level=2)
            builder.add_bold(f"Pattern: `{pattern_info.get('pattern', '')}`")
            builder.add_line_break()

            if pattern_info.get("template"):
                builder.add_bold(f"Template: {pattern_info['template']}")
                builder.add_line_break()

            warnings = pattern_info.get("warnings", [])
            if warnings:
                builder.add_bold("Warnings:")
                builder.add_line_break()
                for warning in warnings:
                    builder.add_list_item(warning)

        performance = results.get("performance", {})
        if performance:
            builder.add_header("Performance", level=2)
            builder.add_list_item(f"Search Time: {performance.get('search_time_seconds', 0):.2f} seconds")
            builder.add_list_item(f"Files Searched: {performance.get('files_searched', 0)}")
            builder.add_list_item(f"Matches Found: {performance.get('matches_found', 0)}")

        resources = results.get("resources", [])
        if resources:
            builder.add_header("Resources", level=2)
            for resource in resources:
                builder.add_list_item(
                    f"**{resource.get('name', 'Unknown')}** "
                    f"({resource.get('resource_type', 'unknown')})"
                )

        matches = results.get("matches", [])
        if matches:
            builder.add_header("Matches", level=2)

            current_file = None
            for match in matches[:100]:
                file_path = match.get("file_path", "")
                line_number = match.get("line_number", 0)
                line_content = match.get("line_content", "")
                match_text = match.get("match_text", "")

                if file_path != current_file:
                    current_file = file_path
                    builder.add_header(f"File: {file_path}", level=3)

                builder.add_bold(f"Line {line_number}:")
                builder.add_line_break()

                highlighted_line = line_content.replace(
                    match_text,
                    f"**{match_text}**",
                    1,
                )
                builder.add_code_block(highlighted_line)

                context = match.get("context")
                if context:
                    before = context.get("before", [])
                    after = context.get("after", [])

                    if before:
                        builder.add_bold("Context (before):")
                        builder.add_line_break()
                        builder.add_code_block("\n".join(before[-3:]))

                    if after:
                        builder.add_bold("Context (after):")
                        builder.add_line_break()
                        builder.add_code_block("\n".join(after[:3]))

                builder.add_separator()
        else:
            builder.add_paragraph("No matches found.")

        return builder.build()

    @staticmethod
    def format_architecture_results(results: dict[str, Any]) -> str:
        """Format architecture design results as markdown.

        Args:
            results: Architecture results dictionary

        Returns:
            Formatted markdown string
        """
        builder = MarkdownBuilder()
        builder.add_header("Architecture Design Results", level=1)

        if "project_path" in results:
            builder.add_header("Project Initialized", level=2)
            builder.add_bold(f"Project Path: `{results.get('project_path')}`")
            builder.add_line_break()
            builder.add_bold(f"Files Created: {len(results.get('files_created', []))}")
            builder.add_line_break()

            if results.get("structure"):
                builder.add_header("Project Structure", level=3)
                for item in results["structure"][:20]:
                    builder.add_list_item(item)

            if results.get("next_steps"):
                builder.add_header("Next Steps", level=3)
                for step in results["next_steps"]:
                    builder.add_list_item(step)

        if "visualization" in results:
            builder.add_header("Architecture Visualization", level=2)
            builder.add_code_block(results.get("visualization", ""), language="mermaid")
            builder.add_paragraph(
                "**Note**: This Mermaid diagram can be rendered in Markdown viewers that support Mermaid (GitHub, GitLab, etc.)"
            )

        if "architecture_diagram" in results:
            builder.add_header("Architecture Diagram (Text)", level=2)
            builder.add_code_block(results.get("architecture_diagram", ""))

        if "components" in results:
            builder.add_header("Components", level=2)
            for component in results.get("components", []):
                builder.add_list_item(f"**{component.get('name')}** ({component.get('type')})")

        if "recommendations" in results:
            builder.add_header("Recommendations", level=2)
            for rec in results.get("recommendations", []):
                builder.add_list_item(rec)

        if "issues" in results:
            builder.add_header("Issues Found", level=2)
            for issue in results.get("issues", []):
                builder.add_list_item(f"[WARNING] {issue}")

        if "optimizations" in results:
            builder.add_header("Optimizations", level=2)
            for opt in results.get("optimizations", []):
                builder.add_list_item(f"[OK] {opt}")

        return builder.build()

    @staticmethod
    def format_troubleshooting_results(results: dict[str, Any]) -> str:
        """Format troubleshooting results as markdown.

        Args:
            results: Troubleshooting results dictionary

        Returns:
            Formatted markdown string
        """
        builder = MarkdownBuilder()
        builder.add_header("Troubleshooting Results", level=1)

        diagnosis = results.get("diagnosis", {})
        if diagnosis:
            builder.add_header("Diagnosis", level=2)
            if diagnosis.get("root_cause"):
                builder.add_bold(f"Root Cause: {diagnosis['root_cause']}")
                builder.add_line_break()
            if diagnosis.get("confidence"):
                builder.add_bold(f"Confidence: {diagnosis['confidence']}")
                builder.add_line_break()

            if diagnosis.get("issues"):
                builder.add_header("Identified Issues", level=3)
                for issue in diagnosis["issues"]:
                    builder.add_list_item(issue)

            if diagnosis.get("error_patterns"):
                builder.add_header("Error Patterns", level=3)
                for pattern in diagnosis["error_patterns"]:
                    builder.add_list_item(pattern)

            if diagnosis.get("visualization"):
                builder.add_header("Infrastructure Visualization", level=3)
                builder.add_code_block(diagnosis.get("visualization", ""), language="mermaid")
                builder.add_paragraph(
                    "**Note**: This Mermaid diagram shows the infrastructure being troubleshot. It can be rendered in Markdown viewers that support Mermaid."
                )

        if results.get("fixes"):
            builder.add_header("Recommended Fixes", level=2)
            for i, fix in enumerate(results["fixes"][:10], 1):
                builder.add_header(f"{i}. {fix.get('title', 'Fix')}", level=3)
                if fix.get("description"):
                    builder.add_paragraph(fix["description"])
                if fix.get("code_example"):
                    builder.add_code_block(fix["code_example"])
                if fix.get("url"):
                    builder.add_bold(f"Source: {fix['url']}")
                    builder.add_line_break()
                builder.add_separator()

        if results.get("prevention"):
            builder.add_header("Prevention Strategies", level=2)
            for strategy in results["prevention"]:
                builder.add_list_item(strategy)

        if results.get("related_knowledge"):
            builder.add_header("Related Knowledge", level=2)
            for article in results["related_knowledge"][:5]:
                builder.add_header(article.get("title", "Article"), level=3)
                if article.get("summary"):
                    builder.add_paragraph(article["summary"])
                builder.add_separator()

        if results.get("web_sources"):
            builder.add_header("Web Sources", level=2)
            for source in results["web_sources"][:5]:
                builder.add_header(source.get("title", "Source"), level=3)
                if source.get("url"):
                    builder.add_bold(f"URL: {source['url']}")
                    builder.add_line_break()
                if source.get("content"):
                    content = source["content"][:300]
                    builder.add_paragraph(content)
                builder.add_separator()

        return builder.build()

    @staticmethod
    def format_documentation_results(results: dict[str, Any]) -> str:
        """Format documentation generation results as markdown.

        Args:
            results: Documentation results dictionary

        Returns:
            Formatted markdown string
        """
        builder = MarkdownBuilder()
        builder.add_header("Documentation Generated", level=1)

        metadata = results.get("metadata", {})
        if metadata:
            builder.add_bold(f"Generated: {metadata.get('generated_at', '')}")
            builder.add_line_break()
            builder.add_bold(f"Document Type: {results.get('document_type', '')}")
            builder.add_line_break()
            builder.add_bold(f"Subject: {results.get('subject', '')}")
            builder.add_line_break()

        if results.get("sections"):
            builder.add_header("Document Sections", level=2)
            for section in results["sections"][:10]:
                builder.add_list_item(section)

        if results.get("content"):
            builder.add_header("Document Content", level=2)
            builder.add_paragraph(results["content"])

        return builder.build()

    @staticmethod
    def format_integration_results(results: dict[str, Any]) -> str:
        """Format integration management results as markdown.

        Args:
            results: Integration results dictionary

        Returns:
            Formatted markdown string
        """
        builder = MarkdownBuilder()
        builder.add_header(f"Integration Management: {results.get('action', 'unknown')}", level=1)

        action = results.get("action", "")

        if action == "analyze":
            builder.add_header("Analysis Results", level=2)

            if results.get("missing_connections"):
                builder.add_header("Missing Connections", level=3)
                for conn in results["missing_connections"]:
                    builder.add_list_item(f"[WARNING] {conn}")

            if results.get("dependency_issues"):
                builder.add_header("Dependency Issues", level=3)
                for issue in results["dependency_issues"]:
                    builder.add_list_item(f"[WARNING] {issue}")

            if results.get("security_gaps"):
                builder.add_header("Security Gaps", level=3)
                for gap in results["security_gaps"]:
                    builder.add_list_item(f"[SECURITY] {gap}")

            if results.get("recommendations"):
                builder.add_header("Recommendations", level=3)
                for rec in results["recommendations"]:
                    builder.add_list_item(f"[OK] {rec}")

        elif action == "generate":
            builder.add_header("Generated Integration Code", level=2)

            if results.get("description"):
                builder.add_bold(f"Pattern: {results.get('description')}")
                builder.add_line_break()

            if results.get("pattern_used"):
                builder.add_bold(f"Pattern Used: {results['pattern_used']}")
                builder.add_line_break()

            if results.get("integration_code"):
                builder.add_header("Integration Code", level=3)
                builder.add_code_block(results["integration_code"], language="hcl")

            if results.get("dependencies"):
                builder.add_header("Dependencies", level=3)
                for dep in results["dependencies"]:
                    builder.add_list_item(dep)

            if results.get("security_rules"):
                builder.add_header("Security Rules", level=3)
                for rule in results["security_rules"]:
                    builder.add_list_item(f"[SECURITY] {rule}")

            if results.get("monitoring"):
                monitoring = results["monitoring"]
                if monitoring.get("metrics"):
                    builder.add_header("Monitoring Metrics", level=3)
                    for metric in monitoring["metrics"]:
                        builder.add_list_item(metric)

        elif action == "validate":
            builder.add_header("Validation Results", level=2)

            is_valid = results.get("valid", False)
            builder.add_bold(f"Status: {'Valid' if is_valid else 'Invalid'}")
            builder.add_line_break()

            if results.get("issues"):
                builder.add_header("Issues", level=3)
                for issue in results["issues"]:
                    builder.add_list_item(f"[WARNING] {issue}")

            if results.get("fixes"):
                builder.add_header("Recommended Fixes", level=3)
                for fix in results["fixes"]:
                    builder.add_list_item(f"[OK] {fix}")

        return builder.build()

    @staticmethod
    def format_infrastructure_lifecycle_results(results: dict[str, Any]) -> str:
        """Format unified infrastructure lifecycle management results as markdown.

        Args:
            results: Infrastructure lifecycle results dictionary

        Returns:
            Formatted markdown string
        """
        builder = MarkdownBuilder()
        action = results.get("action", "unknown")
        
        design_actions = ["analyze", "design", "validate"]
        integration_actions = ["integrate", "analyze_integration"]
        lifecycle_actions = ["create", "update", "upgrade", "backup", "restore", "monitor", "optimize"]
        
        if action in design_actions:
            builder.add_header(f"Infrastructure Design & Analysis: {action}", level=1)
            
            if action == "analyze":
                if results.get("missing_connections"):
                    builder.add_header("Missing Connections", level=2)
                    for conn in results["missing_connections"]:
                        builder.add_list_item(f"[WARNING] {conn}")
                
                if results.get("dependency_issues"):
                    builder.add_header("Dependency Issues", level=2)
                    for issue in results["dependency_issues"]:
                        builder.add_list_item(f"[WARNING] {issue}")
                
                if results.get("security_gaps"):
                    builder.add_header("Security Gaps", level=2)
                    for gap in results["security_gaps"]:
                        builder.add_list_item(f"[SECURITY] {gap}")
                
                if results.get("recommendations"):
                    builder.add_header("Recommendations", level=2)
                    for rec in results["recommendations"]:
                        builder.add_list_item(f"[OK] {rec}")
                
                if results.get("visualization"):
                    builder.add_header("Visualization", level=2)
                    builder.add_code_block(results["visualization"], language="mermaid")
            
            elif action == "design":
                builder.add_header("Design Recommendations", level=2)
                
                if results.get("components"):
                    builder.add_header("Components", level=3)
                    for comp in results["components"]:
                        comp_id = comp.get("name", comp.get("id", comp.get("type", "unknown")))
                        comp_type = comp.get("type", "unknown")
                        builder.add_list_item(f"**{comp_id}** ({comp_type})")
                        
                        if comp.get("services"):
                            services = comp["services"]
                            if isinstance(services, list) and services:
                                max_services = MAX_DISPLAY_SERVICES_PER_COMPONENT
                                services_str = ", ".join(str(s) for s in services[:max_services])
                                if len(services) > max_services:
                                    services_str += f" (+{len(services) - max_services} more)"
                                builder.add_list_item(f"  Services: {services_str}", indent=1)
                
                if results.get("compliance_requirements"):
                    builder.add_header("Compliance Requirements", level=3)
                    controls = results["compliance_requirements"]
                    if isinstance(controls, list):
                        max_controls = MAX_DISPLAY_COMPLIANCE_CONTROLS
                        for control in controls[:max_controls]:
                            if isinstance(control, dict):
                                control_id = control.get("control_id", control.get("id", "Unknown"))
                                title = control.get("title", control.get("name", ""))
                                if title:
                                    builder.add_list_item(f"**{control_id}**: {title}")
                                else:
                                    builder.add_list_item(f"**{control_id}**")
                        if len(controls) > max_controls:
                            builder.add_list_item(f"... and {len(controls) - max_controls} more controls")
                
                if results.get("integration_recommendations"):
                    builder.add_header("Integration Recommendations", level=3)
                    int_recs = results["integration_recommendations"]
                    if int_recs.get("recommended_patterns"):
                        builder.add_header("Recommended Patterns", level=4)
                        for pattern in int_recs["recommended_patterns"]:
                            builder.add_list_item(f"**{pattern.get('name')}**: {pattern.get('description')}")
                    
                    if int_recs.get("dependencies"):
                        builder.add_header("Dependencies", level=4)
                        for dep in int_recs["dependencies"]:
                            builder.add_list_item(dep)
                    
                    if int_recs.get("security_rules"):
                        builder.add_header("Security Rules", level=4)
                        for rule in int_recs["security_rules"]:
                            builder.add_list_item(f"[SECURITY] {rule}")
                
                if results.get("recommendations"):
                    builder.add_header("General Recommendations", level=3)
                    for rec in results["recommendations"]:
                        builder.add_list_item(rec)
            
            elif action == "validate":
                is_valid = results.get("valid", False)
                builder.add_bold(f"Validation Status: {'✅ Valid' if is_valid else '❌ Invalid'}")
                builder.add_line_break()
                
                if results.get("issues"):
                    builder.add_header("Issues", level=2)
                    for issue in results["issues"]:
                        builder.add_list_item(f"[WARNING] {issue}")
                
                if results.get("fixes"):
                    builder.add_header("Recommended Fixes", level=2)
                    for fix in results["fixes"]:
                        builder.add_list_item(f"[OK] {fix}")
        
        elif action in integration_actions:
            builder.add_header(f"Integration Management: {action}", level=1)
            
            if action == "integrate":
                if results.get("recommended_patterns"):
                    builder.add_header("Recommended Patterns", level=2)
                    for pattern in results["recommended_patterns"]:
                        builder.add_header(pattern.get("name", "Unknown"), level=3)
                        builder.add_paragraph(pattern.get("description", ""))
                        builder.add_bold(f"Suitability Score: {pattern.get('suitability', 0)}%")
                        builder.add_line_break()
                
                if results.get("pattern_details"):
                    pattern = results["pattern_details"]
                    builder.add_header("Selected Pattern", level=2)
                    builder.add_bold(f"Pattern: {pattern.get('name')}")
                    builder.add_line_break()
                    builder.add_paragraph(pattern.get("description", ""))
                
                if results.get("dependencies"):
                    builder.add_header("Dependencies", level=2)
                    for dep in results["dependencies"]:
                        builder.add_list_item(dep)
                
                if results.get("security_rules"):
                    builder.add_header("Security Rules & Best Practices", level=2)
                    for rule in results["security_rules"]:
                        builder.add_list_item(f"[SECURITY] {rule}")
                
                if results.get("monitoring"):
                    monitoring = results["monitoring"]
                    builder.add_header("Monitoring Configuration", level=2)
                    if monitoring.get("metrics"):
                        builder.add_header("Metrics", level=3)
                        for metric in monitoring["metrics"]:
                            builder.add_list_item(metric)
                    if monitoring.get("alarms"):
                        builder.add_header("Alarms", level=3)
                        for alarm in monitoring["alarms"]:
                            builder.add_list_item(alarm)
                    if monitoring.get("recommendations"):
                        builder.add_header("Recommendations", level=3)
                        for rec in monitoring["recommendations"]:
                            builder.add_list_item(rec)
                
                if results.get("implementation_guidance"):
                    builder.add_header("Implementation Guidance", level=2)
                    for step in results["implementation_guidance"]:
                        builder.add_list_item(step)
                
                if results.get("compliance_considerations"):
                    builder.add_header("Compliance Considerations", level=2)
                    for consideration in results["compliance_considerations"]:
                        builder.add_list_item(consideration)
            
            elif action == "analyze_integration":
                if results.get("missing_connections"):
                    builder.add_header("Missing Connections", level=2)
                    for conn in results["missing_connections"]:
                        builder.add_list_item(f"[WARNING] {conn}")
                
                if results.get("dependency_issues"):
                    builder.add_header("Dependency Issues", level=2)
                    for issue in results["dependency_issues"]:
                        builder.add_list_item(f"[WARNING] {issue}")
                
                if results.get("security_gaps"):
                    builder.add_header("Security Gaps", level=2)
                    for gap in results["security_gaps"]:
                        builder.add_list_item(f"[SECURITY] {gap}")
                
                if results.get("recommendations"):
                    builder.add_header("Recommendations", level=2)
                    for rec in results["recommendations"]:
                        builder.add_list_item(f"[OK] {rec}")
        
        elif action in lifecycle_actions:
            builder.add_header(f"Infrastructure Lifecycle: {action}", level=1)
            
            resource_id = results.get("resource_id", "")
            status = results.get("status", "")
            
            if resource_id:
                builder.add_bold(f"Resource ID: {resource_id}")
                builder.add_line_break()
            if status:
                builder.add_bold(f"Status: {status}")
                builder.add_line_break()
            
            if action == "create":
                if results.get("endpoints"):
                    builder.add_header("Endpoints", level=2)
                    endpoints = results["endpoints"]
                    if isinstance(endpoints, dict):
                        for key, value in endpoints.items():
                            if isinstance(value, dict):
                                builder.add_header(key, level=3)
                                for k, v in value.items():
                                    builder.add_list_item(f"**{k}**: {v}")
                            else:
                                builder.add_list_item(f"**{key}**: {value}")
            
            if results.get("compliance_status"):
                builder.add_header("Compliance Status", level=2)
                compliance = results["compliance_status"]
                if isinstance(compliance, dict):
                    for standard, status_val in compliance.items():
                        builder.add_list_item(f"**{standard}**: {status_val}")
            
            if results.get("cost_summary"):
                builder.add_header("Cost Summary", level=2)
                cost = results["cost_summary"]
                if isinstance(cost, dict):
                    for key, value in cost.items():
                        builder.add_list_item(f"**{key}**: {value}")
            
            if results.get("recommendations"):
                builder.add_header("Recommendations", level=2)
                for rec in results["recommendations"]:
                    builder.add_list_item(rec)
        
        return builder.build()

    @staticmethod
    def format_infrastructure_results(results: dict[str, Any]) -> str:
        """Format infrastructure management results as markdown.

        Args:
            results: Infrastructure results dictionary

        Returns:
            Formatted markdown string
        """
        builder = MarkdownBuilder()
        builder.add_header(f"Infrastructure Management: {results.get('action', 'unknown')}", level=1)

        action = results.get("action", "")
        resource_id = results.get("resource_id", "")
        status = results.get("status", "")

        builder.add_bold(f"Resource ID: {resource_id}")
        builder.add_line_break()
        builder.add_bold(f"Status: {status}")
        builder.add_line_break()

        if action == "create":
            if results.get("endpoints"):
                builder.add_header("Endpoints", level=2)
                endpoints = results["endpoints"]
                if isinstance(endpoints, dict):
                    for key, value in endpoints.items():
                        if isinstance(value, dict):
                            builder.add_header(key, level=3)
                            for k, v in value.items():
                                builder.add_list_item(f"**{k}**: {v}")
                        else:
                            builder.add_list_item(f"**{key}**: {value}")

            if results.get("visualization"):
                builder.add_header("Infrastructure Visualization", level=2)
                builder.add_code_block(results.get("visualization", ""), language="mermaid")
                builder.add_paragraph(
                    "**Note**: This Mermaid diagram visualizes the generated infrastructure. It can be rendered in Markdown viewers that support Mermaid (GitHub, GitLab, etc.)"
                )

            if results.get("terraform_code"):
                builder.add_header("Terraform Code", level=2)
                builder.add_code_block(results["terraform_code"], language="hcl")

            if results.get("next_steps"):
                builder.add_header("Next Steps", level=2)
                for step in results["next_steps"]:
                    builder.add_list_item(step)

        elif action == "upgrade":
            if results.get("strategy"):
                builder.add_bold(f"Upgrade Strategy: {results['strategy']}")
                builder.add_line_break()

            if results.get("steps"):
                builder.add_header("Upgrade Steps", level=2)
                for i, step in enumerate(results["steps"], 1):
                    builder.add_list_item(f"{i}. {step}")

            if results.get("rollback_plan"):
                builder.add_header("Rollback Plan", level=2)
                for step in results["rollback_plan"]:
                    builder.add_list_item(step)

            if results.get("estimated_downtime"):
                builder.add_bold(f"Estimated Downtime: {results['estimated_downtime']}")
                builder.add_line_break()

        elif action == "backup":
            if results.get("backup_commands"):
                builder.add_header("Backup Commands", level=2)
                backup_cmds = "\n".join(results["backup_commands"])
                builder.add_code_block(backup_cmds, language="bash")

            if results.get("restore_commands"):
                builder.add_header("Restore Commands", level=2)
                restore_cmds = "\n".join(results["restore_commands"])
                builder.add_code_block(restore_cmds, language="bash")

            if results.get("retention_policy"):
                builder.add_bold(f"Retention Policy: {results['retention_policy']}")
                builder.add_line_break()

        elif action == "update":
            if results.get("visualization"):
                builder.add_header("Infrastructure Visualization", level=2)
                builder.add_code_block(results.get("visualization", ""), language="mermaid")
                builder.add_paragraph(
                    "**Note**: This Mermaid diagram visualizes the updated infrastructure. It can be rendered in Markdown viewers that support Mermaid."
                )

            if results.get("terraform_code"):
                builder.add_header("Terraform Code", level=2)
                builder.add_code_block(results["terraform_code"], language="hcl")

            if results.get("update_plan"):
                builder.add_header("Update Plan", level=2)
                for step in results["update_plan"]:
                    builder.add_list_item(step)

            if results.get("rollback_plan"):
                builder.add_header("Rollback Plan", level=2)
                for step in results["rollback_plan"]:
                    builder.add_list_item(step)

            if results.get("estimated_downtime"):
                builder.add_bold(f"Estimated Downtime: {results['estimated_downtime']}")
                builder.add_line_break()

        elif action == "monitor":
            if results.get("metrics"):
                builder.add_header("Metrics", level=2)
                for metric in results["metrics"]:
                    builder.add_list_item(metric)

            if results.get("alerts"):
                builder.add_header("Alerts", level=2)
                for alert in results["alerts"]:
                    builder.add_list_item(f"[ALERT] {alert}")

            if results.get("dashboards"):
                builder.add_header("Dashboards", level=2)
                for dashboard in results["dashboards"]:
                    builder.add_list_item(dashboard)

        elif action == "optimize":
            if results.get("recommendations"):
                builder.add_header("Optimization Recommendations", level=2)
                for rec in results["recommendations"]:
                    builder.add_list_item(f"[OPTIMIZATION] {rec}")

            if results.get("estimated_savings"):
                builder.add_bold(f"Estimated Savings: {results['estimated_savings']}")
                builder.add_line_break()

            if results.get("migration_plan"):
                builder.add_header("Migration Plan", level=2)
                for step in results["migration_plan"]:
                    builder.add_list_item(step)

        return builder.build()

    @staticmethod
    def format_indexing_results(results: dict[str, Any], operation: str = "index") -> str:
        """Format indexing operation results as markdown.

        Args:
            results: Indexing results dictionary
            operation: Operation type (index, list, check, delete)

        Returns:
            Formatted markdown string
        """
        builder = MarkdownBuilder()
        builder.add_header(f"{operation.title()} Operation Results", level=1)

        if results.get("resource_id"):
            builder.add_bold(f"Resource ID: `{results['resource_id']}`")
            builder.add_line_break()

        if results.get("status"):
            status = results["status"]
            builder.add_bold(f"Status: {status}")
            builder.add_line_break()

        if results.get("message"):
            builder.add_paragraph(results["message"])

        if results.get("progress") is not None:
            progress_value = results["progress"]
            if isinstance(progress_value, (int, float)):
                builder.add_bold(f"Progress: {progress_value:.1f}%")
            elif isinstance(progress_value, dict):
                builder.add_bold(f"Progress: {progress_value.get('percentage', 0)}%")
            builder.add_line_break()
        
        if results.get("files_processed"):
            builder.add_list_item(f"Files Processed: {results['files_processed']}")
        if results.get("total_files"):
            builder.add_list_item(f"Total Files: {results['total_files']}")

        if results.get("ai_analysis"):
            ai_analysis = results["ai_analysis"]
            builder.add_header("AI Analysis", level=2)
            if ai_analysis.get("analysis"):
                builder.add_paragraph(ai_analysis["analysis"])
            builder.add_separator()

        if results.get("resources"):
            builder.add_header("Resources", level=2)
            for resource in results["resources"]:
                resource_type = resource.get("resource_type", "unknown")
                name = resource.get("name", "Unknown")
                status = resource.get("status", "unknown")
                resource_id = resource.get("resource_id", "")
                
                builder.add_list_item(f"**{name}** ({resource_type}) - Status: {status}")
                if resource_id:
                    builder.add_list_item(f"Resource ID: `{resource_id}`", indent=1)
                if resource.get("created_at"):
                    builder.add_list_item(f"Created: {resource['created_at']}", indent=1)

        if results.get("total"):
            builder.add_bold(f"Total Resources: {results['total']}")
            builder.add_line_break()

        if results.get("next_steps"):
            builder.add_header("Next Steps", level=2)
            for step in results["next_steps"]:
                builder.add_list_item(step)

        return builder.build()

    @staticmethod
    def format_resource_management_results(results: dict[str, Any], action: str = "list") -> str:
        """Format resource management operation results as markdown.

        Args:
            results: Resource management results dictionary
            action: Action type (list, status, delete)

        Returns:
            Formatted markdown string
        """
        builder = MarkdownBuilder()

        if action == "list":
            builder.add_header("Indexed Resources", level=1)

            # Summary statistics
            if results.get("summary"):
                summary = results["summary"]
                builder.add_header("Summary", level=2)
                if summary.get("total"):
                    builder.add_bold(f"Total Resources: {summary['total']}")
                    builder.add_line_break()
                if summary.get("by_type"):
                    builder.add_list_item(f"By Type: {summary['by_type']}")
                if summary.get("by_status"):
                    builder.add_list_item(f"By Status: {summary['by_status']}")
                builder.add_separator()

            # AI Analysis
            if results.get("ai_analysis"):
                ai_analysis = results["ai_analysis"]
                builder.add_header("AI Analysis", level=2)
                if ai_analysis.get("analysis"):
                    builder.add_paragraph(ai_analysis["analysis"])
                builder.add_separator()

            # Resources list
            if results.get("resources"):
                builder.add_header("Resources", level=2)
                for resource in results["resources"]:
                    resource_type = resource.get("resource_type", "unknown")
                    name = resource.get("name", "Unknown")
                    status = resource.get("status", "unknown")
                    resource_id = resource.get("resource_id", "")

                    builder.add_list_item(f"**{name}** ({resource_type}) - Status: {status}")
                    if resource_id:
                        builder.add_list_item(f"Resource ID: `{resource_id}`", indent=1)
                    if resource.get("created_at"):
                        builder.add_list_item(f"Created: {resource['created_at']}", indent=1)
                    if resource.get("url"):
                        builder.add_list_item(f"URL: {resource['url']}", indent=1)
                    if resource.get("deletion_hint"):
                        builder.add_list_item(f"Delete: {resource['deletion_hint']}", indent=1)

            if results.get("total"):
                builder.add_bold(f"Total: {results['total']}")
                builder.add_line_break()

        elif action == "status":
            builder.add_header("Resource Status", level=1)

            if results.get("resource_id"):
                builder.add_bold(f"Resource ID: `{results['resource_id']}`")
                builder.add_line_break()

            if results.get("name"):
                builder.add_bold(f"Name: {results['name']}")
                builder.add_line_break()

            if results.get("status"):
                status = results["status"]
                builder.add_bold(f"Status: {status}")
                builder.add_line_break()

            if results.get("progress") is not None:
                progress_value = results["progress"]
                if isinstance(progress_value, (int, float)):
                    builder.add_bold(f"Progress: {progress_value:.1f}%")
                elif isinstance(progress_value, dict):
                    builder.add_bold(f"Progress: {progress_value.get('percentage', 0)}%")
                builder.add_line_break()

            if results.get("files_processed"):
                builder.add_list_item(f"Files Processed: {results['files_processed']}")
            if results.get("total_files"):
                builder.add_list_item(f"Total Files: {results['total_files']}")

            if results.get("message"):
                builder.add_paragraph(results["message"])

        elif action == "delete":
            builder.add_header("Resource Deletion", level=1)

            if results.get("status"):
                builder.add_bold(f"Status: {results['status']}")
                builder.add_line_break()

            if results.get("message"):
                builder.add_paragraph(results["message"])

            if results.get("resource_id"):
                builder.add_list_item(f"Deleted Resource ID: `{results['resource_id']}`")
            if results.get("resource_type"):
                builder.add_list_item(f"Resource Type: {results['resource_type']}")

        # Common fields
        if results.get("error"):
            builder.add_header("Error", level=2)
            builder.add_paragraph(results["error"])

        if results.get("next_steps"):
            builder.add_header("Next Steps", level=2)
            for step in results["next_steps"]:
                builder.add_list_item(step)

        return builder.build()

    @staticmethod
    def format_health_check_results(results: dict[str, Any]) -> str:
        """Format health check results as markdown.

        Args:
            results: Health check results dictionary

        Returns:
            Formatted markdown string
        """
        builder = MarkdownBuilder()
        builder.add_header("Health Check Results", level=1)

        overall_status = results.get("status", "unknown")
        builder.add_bold(f"Overall Status: {overall_status}")
        builder.add_line_break()

        if results.get("mongodb"):
            mongodb = results["mongodb"]
            mongodb_status = mongodb.get("status", "unknown")
            builder.add_header("MongoDB", level=2)
            builder.add_bold(f"Status: {mongodb_status}")
            builder.add_line_break()
            if mongodb.get("database"):
                builder.add_bold(f"Database: {mongodb['database']}")
                builder.add_line_break()
            if mongodb.get("error"):
                builder.add_bold(f"Error: {mongodb['error']}")
                builder.add_line_break()

        if results.get("pinecone"):
            pinecone = results["pinecone"]
            pinecone_status = pinecone.get("status", "unknown")
            builder.add_header("Pinecone", level=2)
            builder.add_bold(f"Status: {pinecone_status}")
            builder.add_line_break()
            if pinecone.get("index"):
                builder.add_bold(f"Index: {pinecone['index']}")
                builder.add_line_break()
            if pinecone.get("vector_count") is not None:
                builder.add_bold(f"Vector Count: {pinecone['vector_count']}")
                builder.add_line_break()
            if pinecone.get("error"):
                builder.add_bold(f"Error: {pinecone['error']}")
                builder.add_line_break()

        if results.get("api_client"):
            api_client = results["api_client"]
            api_status = api_client.get("status", "unknown")
            builder.add_header("API Client", level=2)
            builder.add_bold(f"Status: {api_status}")
            builder.add_line_break()
            if api_client.get("api_url"):
                builder.add_bold(f"API URL: {api_client['api_url']}")
                builder.add_line_break()
            if api_client.get("error"):
                builder.add_bold(f"Error: {api_client['error']}")
                builder.add_line_break()

        return builder.build()

    @staticmethod
    def format_knowledge_research_results(results: dict[str, Any]) -> str:
        """Format knowledge research results as markdown.

        Args:
            results: Knowledge research results dictionary

        Returns:
            Formatted markdown string
        """
        if results.get("markdown"):
            return results["markdown"]

        builder = MarkdownBuilder()
        builder.add_header("Knowledge Research Results", level=1)

        if results.get("research_summary"):
            summary = results["research_summary"]
            builder.add_header("Research Summary", level=2)
            if summary.get("total_found"):
                builder.add_bold(f"Total Results: {summary['total_found']}")
                builder.add_line_break()
            if summary.get("domains_covered"):
                builder.add_bold(f"Domains Covered: {', '.join(summary['domains_covered'])}")
                builder.add_line_break()
            if summary.get("key_insights"):
                builder.add_header("Key Insights", level=3)
                for insight in summary["key_insights"]:
                    builder.add_list_item(insight)

        if results.get("results"):
            builder.add_header("Knowledge Articles", level=2)
            for article in results["results"][:20]:
                builder.add_header(article.get("title", "Article"), level=3)
                if article.get("summary"):
                    builder.add_paragraph(article["summary"])
                if article.get("domain"):
                    builder.add_bold(f"Domain: {article['domain']}")
                    builder.add_line_break()
                if article.get("subdomain"):
                    builder.add_bold(f"Subdomain: {article['subdomain']}")
                    builder.add_line_break()
                if article.get("source_url"):
                    builder.add_bold(f"Source: {article['source_url']}")
                    builder.add_line_break()
                builder.add_separator()

        if results.get("web_results"):
            web_results = results["web_results"]
            builder.add_header("Web Search Results", level=2)
            
            if web_results.get("freshness_info"):
                freshness = web_results["freshness_info"]
                max_age = freshness.get("max_age_days", 0)
                builder.add_bold(f"Data Freshness: Results from last {max_age} days")
                builder.add_line_break()
            
            if web_results.get("answer"):
                builder.add_header("AI Summary", level=3)
                builder.add_paragraph(web_results["answer"])
            
            if web_results.get("results"):
                builder.add_header("Web Sources", level=3)
                for item in web_results["results"][:10]:
                    builder.add_bold(item.get("title", "Source"))
                    builder.add_line_break()
                    if item.get("url"):
                        builder.add_paragraph(f"URL: {item['url']}")
                    if item.get("published_date"):
                        builder.add_paragraph(f"Published: {item['published_date']}")
                    if item.get("content"):
                        content = item["content"][:300]
                        builder.add_paragraph(content)
                    builder.add_separator()

        return builder.build()

    @staticmethod
    def format_github_tree_results(results: dict[str, Any]) -> str:
        """Format GitHub file tree results as markdown.

        Args:
            results: GitHub tree results dictionary

        Returns:
            Formatted markdown string
        """
        builder = MarkdownBuilder()
        builder.add_header("GitHub Repository Structure", level=1)

        builder.add_bold(f"Repository: {results.get('repo_url', '')}")
        builder.add_line_break()
        builder.add_bold(f"Branch: {results.get('branch', 'main')}")
        builder.add_line_break()

        metadata = results.get("metadata", {})
        if metadata:
            builder.add_header("Repository Statistics", level=2)
            builder.add_list_item(f"Total Files: {metadata.get('total_files', 0)}")
            builder.add_list_item(f"Total Directories: {metadata.get('total_directories', 0)}")
            builder.add_list_item(f"Total Size: {metadata.get('total_size', 0)} bytes")

            if metadata.get("languages"):
                builder.add_list_item(f"Languages: {', '.join(metadata['languages'][:10])}")

        format_type = results.get("format", "json")

        if format_type == "tree":
            builder.add_header("File Tree", level=2)
            builder.add_code_block(results.get("tree", ""), language="text")
        elif format_type == "markdown":
            builder.add_header("Structure", level=2)
            builder.add_paragraph(results.get("markdown", ""))
        else:
            builder.add_header("Structure (JSON)", level=2)
            import json

            structure_json = json.dumps(results.get("structure", {}), indent=2)
            builder.add_code_block(structure_json, language="json")

        return builder.build()

    @staticmethod
    def format_visualization_results(results: dict[str, Any]) -> str:
        """Format infrastructure visualization results as markdown.

        Args:
            results: Visualization results dictionary

        Returns:
            Formatted markdown string
        """
        builder = MarkdownBuilder()
        builder.add_header(f"Infrastructure Visualization: {results.get('type', 'flow')}", level=1)

        format_type = results.get("format", "mermaid")
        builder.add_bold(f"Format: {format_type}")
        builder.add_line_break()

        metadata = results.get("metadata", {})
        if metadata:
            builder.add_header("Visualization Statistics", level=2)
            builder.add_list_item(f"Components: {metadata.get('component_count', 0)}")
            builder.add_list_item(f"Connections: {metadata.get('connection_count', 0)}")

        visualization = results.get("visualization", "")
        if visualization:
            builder.add_header("Diagram", level=2)

            if format_type == "mermaid":
                builder.add_code_block(visualization, language="mermaid")
                builder.add_paragraph(
                    "**Note**: This Mermaid diagram can be rendered in Markdown viewers that support Mermaid (GitHub, GitLab, etc.)"
                )
            else:
                builder.add_code_block(visualization, language="plantuml")

        components = results.get("components", [])
        if components:
            builder.add_header("Components", level=2)
            for comp in components[:20]:
                comp_name = comp.get("name", comp.get("id", "unknown"))
                comp_type = comp.get("type", "unknown")
                builder.add_list_item(f"**{comp_name}** ({comp_type})")

        connections = results.get("connections", [])
        if connections:
            builder.add_header("Connections", level=2)
            for conn in connections[:20]:
                from_comp = conn.get("from", "unknown")
                to_comp = conn.get("to", "unknown")
                conn_type = conn.get("type", "dependency")
                builder.add_list_item(f"{from_comp} → {to_comp} ({conn_type})")

        return builder.build()

    @staticmethod
    def format_devops_resource_search_results(results: dict[str, Any]) -> str:
        """Format unified DevOps resource search results as markdown.

        Args:
            results: DevOps resource search results dictionary

        Returns:
            Formatted markdown string
        """
        builder = MarkdownBuilder()
        builder.add_header("DevOps Resource Search Results", level=1)

        total = results.get("total", 0)
        builder.add_bold(f"Total Results: {total}")
        builder.add_line_break()

        packages = results.get("packages", [])
        tools = results.get("tools", [])
        services = results.get("services", [])
        documentation = results.get("documentation", [])
        unified_results = results.get("unified_results", [])

        if unified_results:
            builder.add_header("Top Results (Unified Ranking)", level=2)
            for item in unified_results[:20]:
                resource_type = item.get("resource_type", "unknown")
                name = item.get("name", item.get("title", "Unknown"))
                description = item.get("description", item.get("summary", ""))

                builder.add_header(f"{name} ({resource_type})", level=3)
                if description:
                    builder.add_paragraph(description[:300])
                builder.add_separator()

        if packages:
            builder.add_header(f"Packages ({len(packages)})", level=2)
            for package in packages[:20]:
                name = package.get("name", "Unknown")
                registry = package.get("registry", "unknown")
                description = package.get("description", "")
                builder.add_header(f"{name} ({registry})", level=3)
                if description:
                    builder.add_paragraph(description[:200])
                builder.add_separator()

        if tools:
            builder.add_header(f"CLI Tools ({len(tools)})", level=2)
            for tool in tools[:20]:
                name = tool.get("name", "Unknown")
                description = tool.get("description", "")
                category = tool.get("category", "")
                install_command = tool.get("install_command", "")
                official_url = tool.get("official_url", "")

                builder.add_header(f"{name}", level=3)
                if description:
                    builder.add_paragraph(description[:200])
                if category:
                    builder.add_bold(f"Category: {category}")
                    builder.add_line_break()
                if install_command:
                    builder.add_bold(f"Install: `{install_command}`")
                    builder.add_line_break()
                if official_url:
                    builder.add_bold(f"URL: {official_url}")
                    builder.add_line_break()
                builder.add_separator()

        if services:
            builder.add_header(f"Services ({len(services)})", level=2)
            for service in services[:20]:
                name = service.get("name", "Unknown")
                description = service.get("description", "")
                category = service.get("category", "")
                official_url = service.get("official_url", "")

                builder.add_header(f"{name}", level=3)
                if description:
                    builder.add_paragraph(description[:200])
                if category:
                    builder.add_bold(f"Category: {category}")
                    builder.add_line_break()
                if official_url:
                    builder.add_bold(f"URL: {official_url}")
                    builder.add_line_break()
                builder.add_separator()

        if documentation:
            builder.add_header(f"Documentation ({len(documentation)})", level=2)
            for doc in documentation[:20]:
                title = doc.get("title", "Unknown")
                summary = doc.get("summary", "")
                url = doc.get("url", "")

                builder.add_header(f"{title}", level=3)
                if summary:
                    builder.add_paragraph(summary[:200])
                if url:
                    builder.add_bold(f"URL: {url}")
                    builder.add_line_break()
                builder.add_separator()

        return builder.build()

    @staticmethod
    def format_package_search_results(results: dict[str, Any]) -> str:
        """Format package search results as markdown.

        Args:
            results: Package search results dictionary

        Returns:
            Formatted markdown string
        """
        builder = MarkdownBuilder()
        builder.add_header("Package Search Results", level=1)

        search_type = results.get("search_type", "semantic")
        total = results.get("total", 0)

        builder.add_bold(f"Search Type: {search_type.title()}")
        builder.add_line_break()
        builder.add_bold(f"Total Results: {total}")
        builder.add_line_break()

        if search_type == "hybrid":
            semantic_count = results.get("semantic_count", 0)
            regex_count = results.get("regex_count", 0)
            builder.add_bold(f"Semantic Matches: {semantic_count}")
            builder.add_line_break()
            builder.add_bold(f"Regex Matches: {regex_count}")
            builder.add_line_break()

        packages = results.get("results", [])
        matches = results.get("matches", [])

        if search_type == "regex" and matches:
            builder.add_header("Regex Matches", level=2)
            for match in matches[:50]:
                package_name = match.get("package_name", "Unknown")
                registry = match.get("registry", "unknown")
                file_path = match.get("file_path", "")
                line_number = match.get("line_number", 0)
                match_text = match.get("match_text", "")

                builder.add_header(f"{package_name} ({registry})", level=3)
                builder.add_bold(f"File: `{file_path}`")
                builder.add_line_break()
                builder.add_bold(f"Line {line_number}:")
                builder.add_line_break()
                builder.add_code_block(match_text)

                context = match.get("context")
                if context:
                    builder.add_bold("Context:")
                    builder.add_line_break()
                    builder.add_code_block(context[:500])

                builder.add_separator()

        elif packages:
            builder.add_header("Packages", level=2)
            for package in packages[:50]:
                name = package.get("name", "Unknown")
                registry = package.get("registry", "unknown")
                description = package.get("description", "")
                github_url = package.get("github_url")
                domain_tags = package.get("domain_tags", [])
                category = package.get("category")
                relevance_score = package.get("relevance_score", 0)

                builder.add_header(f"{name} ({registry})", level=3)

                if description:
                    builder.add_paragraph(description[:300])

                if domain_tags:
                    builder.add_bold(f"Domains: {', '.join(domain_tags)}")
                    builder.add_line_break()

                if category:
                    builder.add_bold(f"Category: {category}")
                    builder.add_line_break()

                if relevance_score:
                    builder.add_bold(f"Relevance Score: {relevance_score:.2f}")
                    builder.add_line_break()

                health_score = package.get("health_score", 0.0)
                health_metrics = package.get("health_metrics", {})
                if health_score > 0 or health_metrics:
                    builder.add_bold(f"Health Score: {health_score:.1f}/100")
                    builder.add_line_break()

                    if health_metrics:
                        maintenance = health_metrics.get("maintenance_status", "unknown")
                        security = health_metrics.get("security_status", "unknown")
                        builder.add_bold(f"Maintenance: {maintenance.title()} | Security: {security.title()}")
                        builder.add_line_break()

                        downloads = health_metrics.get("downloads", 0)
                        if downloads > 0:
                            builder.add_bold(f"Downloads: {downloads:,}")
                            builder.add_line_break()

                if github_url:
                    builder.add_bold(f"GitHub: {github_url}")
                    builder.add_line_break()

                regex_matches = package.get("regex_matches", [])
                if regex_matches:
                    builder.add_bold(f"Regex Matches: {len(regex_matches)}")
                    builder.add_line_break()
                    for match in regex_matches[:3]:
                        builder.add_list_item(
                            f"`{match.get('file_path', '')}`: Line {match.get('line_number', 0)}"
                        )

                builder.add_separator()

        if not packages and not matches:
            builder.add_paragraph("No packages found matching your search criteria.")

        return builder.build()

    @staticmethod
    def format_package_read_file_results(result: dict[str, Any]) -> str:
        """Format package read file results as markdown."""
        builder = MarkdownBuilder()
        builder.add_header("Package File Content", level=1)
        
        package_name = result.get("package_name", "Unknown")
        registry = result.get("registry", "Unknown")
        filename = result.get("filename", "Unknown")
        
        builder.add_bold(f"Package: {package_name}")
        builder.add_line_break()
        builder.add_bold(f"Registry: {registry}")
        builder.add_line_break()
        builder.add_bold(f"File: {filename}")
        builder.add_line_break()
        
        content = result.get("content", "")
        if content:
            builder.add_header("File Content", level=2)
            builder.add_code_block(content, language="")
        else:
            builder.add_paragraph("No content available.")
        
        return builder.build()

    @staticmethod
    def format_tool_recommendations(result: dict[str, Any]) -> str:
        """Format tool recommendations as markdown."""
        builder = MarkdownBuilder()
        builder.add_header("Recommended Tools", level=1)
        
        task = result.get("task", "")
        if task:
            builder.add_paragraph(f"**Task:** {task}")
            builder.add_line_break()
        
        category_filter = result.get("category_filter")
        if category_filter:
            builder.add_paragraph(f"**Category Filter:** {category_filter}")
            builder.add_line_break()
        
        recommendations = result.get("recommendations", [])
        count = result.get("count", len(recommendations))
        
        builder.add_paragraph(f"Found {count} recommended tool(s):")
        builder.add_line_break()
        
        for i, rec in enumerate(recommendations, 1):
            tool_name = rec.get("tool", "Unknown")
            score = rec.get("score", 0)
            reason = rec.get("reason", "")
            short_desc = rec.get("short_description", "")
            category = rec.get("category", "")
            
            builder.add_header(f"{i}. {tool_name}", level=2)
            builder.add_list_item(f"**Relevance Score:** {score:.2f}/1.0")
            builder.add_list_item(f"**Category:** {category}")
            if reason:
                builder.add_list_item(f"**Reason:** {reason}")
            if short_desc:
                builder.add_list_item(f"**Description:** {short_desc}")
            builder.add_line_break()
        
        guidance = result.get("guidance", "")
        if guidance:
            builder.add_header("Usage Guidance", level=2)
            builder.add_paragraph(guidance)
        
        return builder.build()

    @staticmethod
    def format_tools_by_category(result: dict[str, Any]) -> str:
        """Format tools by category as markdown."""
        builder = MarkdownBuilder()
        
        category = result.get("category", "Unknown")
        builder.add_header(f"Tools in Category: {category}", level=1)
        
        tools = result.get("tools", [])
        count = result.get("count", len(tools))
        
        if count == 0:
            builder.add_paragraph("No tools found in this category.")
            available_categories = result.get("available_categories", [])
            if available_categories:
                builder.add_header("Available Categories", level=2)
                for cat in available_categories:
                    builder.add_list_item(cat)
        else:
            builder.add_paragraph(f"Found {count} tool(s):")
            builder.add_line_break()
            
            for tool in tools:
                tool_name = tool.get("name", "Unknown")
                short_desc = tool.get("short_description", "")
                
                builder.add_header(tool_name, level=2)
                if short_desc:
                    builder.add_paragraph(short_desc)
                builder.add_line_break()
        
        available_categories = result.get("available_categories", [])
        if available_categories:
            builder.add_header("All Available Categories", level=2)
            for cat in available_categories:
                builder.add_list_item(cat)
        
        return builder.build()

    @staticmethod
    def format_tool_documentation(result: dict[str, Any]) -> str:
        """Format tool documentation as markdown."""
        builder = MarkdownBuilder()
        
        tool_name = result.get("tool_name", "Unknown")
        builder.add_header(f"Tool Documentation: {tool_name}", level=1)
        
        category = result.get("category", "")
        if category:
            builder.add_list_item(f"**Category:** {category}")
        
        short_desc = result.get("short_description", "")
        if short_desc:
            builder.add_header("Short Description", level=2)
            builder.add_paragraph(short_desc)
            builder.add_line_break()
        
        detailed_desc = result.get("detailed_description", "")
        if detailed_desc and detailed_desc != "Detailed description not available yet.":
            builder.add_header("Detailed Description", level=2)
            builder.add_paragraph(detailed_desc)
        else:
            builder.add_header("Detailed Description", level=2)
            builder.add_paragraph("Detailed description not available yet. This tool's documentation is being updated.")
        
        guidance = result.get("guidance", "")
        if guidance:
            builder.add_header("Usage Guidance", level=2)
            builder.add_paragraph(guidance)
        
        return builder.build()

    @staticmethod
    def format_filesystem_list_results(results: dict[str, Any]) -> str:
        """Format filesystem list results as markdown.

        Args:
            results: Filesystem list results dictionary

        Returns:
            Formatted markdown string
        """
        builder = MarkdownBuilder()
        data = results.get("data", results)
        
        resource_id = data.get("resource_id", "")
        path = data.get("path", "/")
        entries = data.get("entries", [])
        total = data.get("total", len(entries))

        builder.add_header(f"Filesystem Listing: {path}", level=1)
        builder.add_bold(f"Resource ID: {resource_id}")
        builder.add_line_break()
        builder.add_bold(f"Path: {path}")
        builder.add_line_break()
        builder.add_bold(f"Total Entries: {total}")
        builder.add_line_break()

        if entries:
            builder.add_header("Entries", level=2)
            for entry in entries:
                entry_type = entry.get("type", entry.get("entry_type", "unknown"))
                name = entry.get("name", "")
                entry_path = entry.get("path", "")
                
                builder.add_list_item(f"**{name}** ({entry_type}) - `{entry_path}`")
                
                if entry.get("infrastructure"):
                    infra = entry["infrastructure"]
                    if infra.get("resource_type"):
                        builder.add_paragraph(f"  - Resource Type: {infra['resource_type']}")
                    if infra.get("cloud_provider"):
                        builder.add_paragraph(f"  - Cloud Provider: {infra['cloud_provider']}")
                
                if entry.get("compliance"):
                    builder.add_paragraph(f"  - Compliance: {', '.join(entry['compliance'].get('standards', []))}")
                
                if entry.get("cost"):
                    builder.add_paragraph(f"  - Monthly Cost: ${entry['cost'].get('monthly_usd', 0):.2f}")
                
                if entry.get("security"):
                    builder.add_paragraph(f"  - Security Score: {entry['security'].get('score', 0)}/100")
        else:
            builder.add_paragraph("No entries found in this directory.")

        return builder.build()

    @staticmethod
    def format_file_read_results(results: dict[str, Any]) -> str:
        """Format file read results as markdown.

        Args:
            results: File read results dictionary

        Returns:
            Formatted markdown string
        """
        builder = MarkdownBuilder()
        data = results.get("data", results)
        
        path = data.get("path", "")
        name = data.get("name", "")
        content = data.get("content", "")
        language = data.get("language", "")

        builder.add_header(f"File: {name}", level=1)
        builder.add_bold(f"Path: {path}")
        builder.add_line_break()

        if language:
            builder.add_bold(f"Language: {language}")
            builder.add_line_break()

        if content:
            builder.add_header("Content", level=2)
            builder.add_code_block(content, language=language or "text")

        if data.get("dependencies"):
            deps = data["dependencies"]
            builder.add_header("Dependencies", level=2)
            if deps.get("direct"):
                builder.add_header("Direct Dependencies", level=3)
                for dep in deps["direct"]:
                    builder.add_list_item(dep)
            if deps.get("dependents"):
                builder.add_header("Dependents", level=3)
                for dep in deps["dependents"]:
                    builder.add_list_item(dep)

        if data.get("compliance"):
            builder.add_header("Compliance", level=2)
            standards = data["compliance"].get("standards", [])
            if standards:
                builder.add_list_item(f"Standards: {', '.join(standards)}")

        if data.get("costs"):
            builder.add_header("Costs", level=2)
            monthly = data["costs"].get("monthly_usd", 0)
            builder.add_list_item(f"Monthly Cost: ${monthly:.2f}")

        if data.get("security"):
            builder.add_header("Security", level=2)
            score = data["security"].get("score", 0)
            builder.add_list_item(f"Security Score: {score}/100")

        return builder.build()

    @staticmethod
    def format_filesystem_tree_results(results: dict[str, Any]) -> str:
        """Format filesystem tree results as markdown.

        Args:
            results: Filesystem tree results dictionary

        Returns:
            Formatted markdown string
        """
        builder = MarkdownBuilder()
        data = results.get("data", results)
        
        path = data.get("path", "/")
        name = data.get("name", "/")

        builder.add_header(f"Filesystem Tree: {name}", level=1)
        builder.add_bold(f"Root Path: {path}")
        builder.add_line_break()

        def format_tree_node(node: dict[str, Any], level: int = 0) -> None:
            """Recursively format tree node."""
            indent = "  " * level
            node_name = node.get("name", "")
            node_type = node.get("type", "unknown")
            node_path = node.get("path", "")
            
            builder.add_paragraph(f"{indent}- **{node_name}** ({node_type}) - `{node_path}`")
            
            if node.get("infrastructure"):
                infra = node["infrastructure"]
                builder.add_paragraph(f"{indent}  - Infrastructure: {infra.get('resource_type', 'N/A')}")
            
            if node.get("compliance"):
                builder.add_paragraph(f"{indent}  - Compliance: {', '.join(node['compliance'].get('standards', []))}")
            
            if node.get("cost"):
                builder.add_paragraph(f"{indent}  - Cost: ${node['cost'].get('monthly_usd', 0):.2f}/month")
            
            children = node.get("children", [])
            for child in children:
                format_tree_node(child, level + 1)

        format_tree_node(data)

        return builder.build()

    @staticmethod
    def format_glob_results(results: dict[str, Any]) -> str:
        """Format glob search results as markdown.

        Args:
            results: Glob search results dictionary

        Returns:
            Formatted markdown string
        """
        builder = MarkdownBuilder()
        data = results.get("data", results)
        
        resource_id = data.get("resource_id", "")
        pattern = data.get("pattern", "")
        matches = data.get("matches", [])
        total = data.get("total", len(matches))

        builder.add_header(f"Glob Search Results", level=1)
        builder.add_bold(f"Resource ID: {resource_id}")
        builder.add_line_break()
        builder.add_bold(f"Pattern: {pattern}")
        builder.add_line_break()
        builder.add_bold(f"Matches Found: {total}")
        builder.add_line_break()

        if matches:
            builder.add_header("Matches", level=2)
            for match in matches:
                name = match.get("name", "")
                path = match.get("path", "")
                entry_type = match.get("type", match.get("entry_type", "unknown"))
                
                builder.add_list_item(f"**{name}** ({entry_type}) - `{path}`")
        else:
            builder.add_paragraph("No matches found for the given pattern.")

        return builder.build()

    @staticmethod
    def format_context_save_results(results: dict[str, Any]) -> str:
        """Format context save results as markdown.

        Args:
            results: Context save results dictionary

        Returns:
            Formatted markdown string
        """
        builder = MarkdownBuilder()
        data = results.get("data", results)
        
        context_id = data.get("context_id", "")
        title = data.get("title", "")
        summary = data.get("summary", "")
        context_type = data.get("context_type", "")

        builder.add_header(f"Context Saved: {title}", level=1)
        builder.add_bold(f"Context ID: {context_id}")
        builder.add_line_break()
        builder.add_bold(f"Type: {context_type}")
        builder.add_line_break()
        builder.add_paragraph(summary)

        analysis = data.get("analysis")
        if analysis:
            builder.add_header("Automatic Analysis", level=2)
            
            if analysis.get("compliance"):
                compliance = analysis["compliance"]
                builder.add_header("Compliance", level=3)
                if compliance.get("standards"):
                    builder.add_list_item(f"Standards: {', '.join(compliance['standards'])}")
                if compliance.get("status"):
                    for standard, status in compliance["status"].items():
                        builder.add_list_item(f"{standard}: {status}")
            
            if analysis.get("costs"):
                costs = analysis["costs"]
                builder.add_header("Costs", level=3)
                if costs.get("estimated_monthly"):
                    builder.add_list_item(f"Monthly: ${costs['estimated_monthly']:.2f}")
                if costs.get("estimated_annual"):
                    builder.add_list_item(f"Annual: ${costs['estimated_annual']:.2f}")
            
            if analysis.get("security"):
                security = analysis["security"]
                builder.add_header("Security", level=3)
                if security.get("score") is not None:
                    builder.add_list_item(f"Security Score: {security['score']}/100")
                if security.get("issues"):
                    builder.add_list_item(f"Issues Found: {len(security['issues'])}")
            
            if analysis.get("infrastructure"):
                infra = analysis["infrastructure"]
                builder.add_header("Infrastructure", level=3)
                if infra.get("total_resources"):
                    builder.add_list_item(f"Total Resources: {infra['total_resources']}")
                if infra.get("cloud_providers"):
                    builder.add_list_item(f"Cloud Providers: {', '.join(infra['cloud_providers'])}")

        return builder.build()

    @staticmethod
    def format_context_search_results(results: dict[str, Any]) -> str:
        """Format context search results as markdown.

        Args:
            results: Context search results dictionary

        Returns:
            Formatted markdown string
        """
        builder = MarkdownBuilder()
        data = results.get("data", results)
        
        query = data.get("query", "")
        search_results = data.get("results", [])
        total = data.get("total", len(search_results))

        builder.add_header(f"Context Search Results", level=1)
        builder.add_bold(f"Query: {query}")
        builder.add_line_break()
        builder.add_bold(f"Found: {total} contexts")
        builder.add_line_break()

        if search_results:
            builder.add_header("Results", level=2)
            for idx, ctx in enumerate(search_results, 1):
                context_id = ctx.get("context_id", "")
                title = ctx.get("title", "")
                context_type = ctx.get("context_type", "")
                summary = ctx.get("summary", "")
                
                builder.add_header(f"{idx}. {title}", level=3)
                builder.add_list_item(f"**ID**: {context_id}")
                builder.add_list_item(f"**Type**: {context_type}")
                builder.add_paragraph(summary)
                
                analysis = ctx.get("analysis")
                if analysis:
                    if analysis.get("compliance"):
                        standards = analysis["compliance"].get("standards", [])
                        if standards:
                            builder.add_paragraph(f"**Compliance**: {', '.join(standards)}")
                    if analysis.get("costs"):
                        monthly = analysis["costs"].get("estimated_monthly", 0)
                        if monthly:
                            builder.add_paragraph(f"**Monthly Cost**: ${monthly:.2f}")
                    if analysis.get("security"):
                        score = analysis["security"].get("score")
                        if score is not None:
                            builder.add_paragraph(f"**Security Score**: {score}/100")
        else:
            builder.add_paragraph("No contexts found matching your query.")

        return builder.build()

    @staticmethod
    def format_context_details_results(results: dict[str, Any]) -> str:
        """Format context details results as markdown.

        Args:
            results: Context details results dictionary

        Returns:
            Formatted markdown string
        """
        builder = MarkdownBuilder()
        data = results.get("data", results)
        
        context_id = data.get("context_id", "")
        title = data.get("title", "")
        summary = data.get("summary", "")
        description = data.get("description", "")
        context_type = data.get("context_type", "")

        builder.add_header(f"Context: {title}", level=1)
        builder.add_bold(f"Context ID: {context_id}")
        builder.add_line_break()
        builder.add_bold(f"Type: {context_type}")
        builder.add_line_break()
        builder.add_header("Summary", level=2)
        builder.add_paragraph(summary)

        if description:
            builder.add_header("Description", level=2)
            builder.add_paragraph(description)

        infrastructure_resources = data.get("infrastructure_resources", [])
        if infrastructure_resources:
            builder.add_header("Infrastructure Resources", level=2)
            for resource in infrastructure_resources:
                builder.add_list_item(
                    f"**{resource.get('name', '')}** ({resource.get('resource_type', '')}) - "
                    f"`{resource.get('path', '')}`"
                )

        analysis = data.get("analysis")
        if analysis:
            builder.add_header("Analysis", level=2)
            
            if analysis.get("compliance"):
                compliance = analysis["compliance"]
                builder.add_header("Compliance", level=3)
                if compliance.get("standards"):
                    builder.add_list_item(f"Standards: {', '.join(compliance['standards'])}")
            
            if analysis.get("costs"):
                costs = analysis["costs"]
                builder.add_header("Costs", level=3)
                if costs.get("estimated_monthly"):
                    builder.add_list_item(f"Monthly: ${costs['estimated_monthly']:.2f}")
            
            if analysis.get("security"):
                security = analysis["security"]
                builder.add_header("Security", level=3)
                if security.get("score") is not None:
                    builder.add_list_item(f"Score: {security['score']}/100")

        linked_contexts = data.get("linked_contexts", [])
        if linked_contexts:
            builder.add_header("Linked Contexts", level=2)
            for linked_id in linked_contexts:
                builder.add_list_item(linked_id)

        return builder.build()

    @staticmethod
    def format_context_list_results(results: dict[str, Any]) -> str:
        """Format context list results as markdown.

        Args:
            results: Context list results dictionary

        Returns:
            Formatted markdown string
        """
        builder = MarkdownBuilder()
        data = results.get("data", results)
        
        contexts = data.get("contexts", [])
        total = data.get("total", len(contexts))
        limit = data.get("limit", 100)
        offset = data.get("offset", 0)

        builder.add_header("Contexts List", level=1)
        builder.add_bold(f"Total: {total}")
        builder.add_line_break()
        builder.add_bold(f"Showing: {offset + 1}-{offset + len(contexts)}")
        builder.add_line_break()

        if contexts:
            for ctx in contexts:
                context_id = ctx.get("context_id", "")
                title = ctx.get("title", "")
                context_type = ctx.get("context_type", "")
                created_at = ctx.get("created_at", "")
                
                builder.add_header(f"{title}", level=2)
                builder.add_list_item(f"**ID**: {context_id}")
                builder.add_list_item(f"**Type**: {context_type}")
                if created_at:
                    builder.add_list_item(f"**Created**: {created_at}")
        else:
            builder.add_paragraph("No contexts found.")

        return builder.build()

    @staticmethod
    def format_context_link_results(results: dict[str, Any]) -> str:
        """Format context link results as markdown.

        Args:
            results: Context link results dictionary

        Returns:
            Formatted markdown string
        """
        builder = MarkdownBuilder()
        data = results.get("data", results)
        
        link_id = data.get("link_id", "")
        source_context_id = data.get("source_context_id", "")
        target_context_id = data.get("target_context_id", "")
        relationship_type = data.get("relationship_type", "")
        strength = data.get("strength", 1.0)

        builder.add_header("Context Link Created", level=1)
        builder.add_bold(f"Link ID: {link_id}")
        builder.add_line_break()
        builder.add_bold(f"Source: {source_context_id}")
        builder.add_line_break()
        builder.add_bold(f"Target: {target_context_id}")
        builder.add_line_break()
        builder.add_bold(f"Relationship: {relationship_type}")
        builder.add_line_break()
        builder.add_bold(f"Strength: {strength:.2f}")

        return builder.build()

    @staticmethod
    def format_context_graph_results(results: dict[str, Any]) -> str:
        """Format context graph results as markdown.

        Args:
            results: Context graph results dictionary

        Returns:
            Formatted markdown string
        """
        builder = MarkdownBuilder()
        data = results.get("data", results)
        
        root_context_id = data.get("root_context_id", "")
        nodes = data.get("nodes", [])
        edges = data.get("edges", [])

        builder.add_header("Context Dependency Graph", level=1)
        builder.add_bold(f"Root Context: {root_context_id}")
        builder.add_line_break()
        builder.add_bold(f"Nodes: {len(nodes)}")
        builder.add_line_break()
        builder.add_bold(f"Edges: {len(edges)}")
        builder.add_line_break()

        if nodes:
            builder.add_header("Contexts", level=2)
            for node in nodes:
                context_id = node.get("context_id", "")
                title = node.get("title", "")
                context_type = node.get("type", "")
                builder.add_list_item(f"**{title}** ({context_type}) - `{context_id}`")

        if edges:
            builder.add_header("Relationships", level=2)
            for edge in edges:
                source = edge.get("source", "")
                target = edge.get("target", "")
                relationship = edge.get("relationship", "")
                strength = edge.get("strength", 1.0)
                builder.add_list_item(
                    f"`{source}` --[{relationship}]--> `{target}` (strength: {strength:.2f})"
                )

        return builder.build()

    @staticmethod
    def format_cloud_discovery_results(results: dict[str, Any]) -> str:
        """Format cloud resource discovery results as markdown.

        Args:
            results: Cloud discovery results dictionary

        Returns:
            Formatted markdown string
        """
        # Check if this is a setup guide response
        if results.get("setup_required"):
            return ContextBuilder.format_connection_setup_guide(results)
        
        builder = MarkdownBuilder()
        builder.add_header("Cloud Resource Discovery Results", level=1)

        # Summary section
        summary = results.get("summary", {})
        if summary:
            builder.add_header("Discovery Summary", level=2)
            builder.add_list_item(f"Total Resources: {summary.get('total_resources', 0)}")
            builder.add_list_item(f"Total Dependencies: {summary.get('total_dependencies', 0)}")
            builder.add_list_item(f"Circular Dependencies: {'Yes' if summary.get('has_circular_dependencies') else 'No'}")
            builder.add_line_break()

            # By resource type
            by_type = summary.get("by_resource_type", {})
            if by_type:
                builder.add_header("Resources by Type", level=3)
                for tf_type, count in sorted(by_type.items(), key=lambda x: -x[1]):
                    builder.add_list_item(f"`{tf_type}`: {count}")
                builder.add_line_break()

            # By region
            by_region = summary.get("by_region", {})
            if by_region:
                builder.add_header("Resources by Region", level=3)
                for region, count in sorted(by_region.items(), key=lambda x: -x[1]):
                    builder.add_list_item(f"`{region}`: {count}")
                builder.add_line_break()

            # By phase
            by_phase = summary.get("by_phase", {})
            if by_phase:
                builder.add_header("Resources by Import Phase", level=3)
                phase_order = ["Foundation", "Networking", "Security", "DataLayer", "Databases", "LoadBalancing", "Compute"]
                for phase in phase_order:
                    if phase in by_phase:
                        builder.add_list_item(f"**{phase}**: {by_phase[phase]}")
                builder.add_line_break()

        # Import order
        import_order = results.get("import_order", [])
        if import_order:
            builder.add_header("Terraform Import Order", level=2)
            builder.add_paragraph("Resources should be imported in this order to satisfy dependencies:")
            builder.add_line_break()
            terraform_names = results.get("terraform_names", {})
            for i, resource_id in enumerate(import_order[:20], 1):  # Limit to first 20
                tf_name = terraform_names.get(resource_id, resource_id)
                builder.add_list_item(f"{i}. `{tf_name}`")
            if len(import_order) > 20:
                builder.add_paragraph(f"... and {len(import_order) - 20} more resources")
            builder.add_line_break()

        # Import commands
        import_commands = results.get("import_commands", [])
        if import_commands:
            builder.add_header("Terraform Import Commands", level=2)
            builder.add_paragraph("Run these commands to import resources into Terraform:")
            builder.add_line_break()
            # Show first 10 commands
            commands_preview = import_commands[:10]
            builder.add_code_block("\n".join(commands_preview), language="bash")
            if len(import_commands) > 10:
                builder.add_paragraph(f"... and {len(import_commands) - 10} more import commands")
            builder.add_line_break()

        # Discovered resources (brief)
        resources = results.get("discovered_resources", [])
        if resources:
            builder.add_header("Discovered Resources", level=2)
            # Group by type for cleaner display
            by_type_list: dict[str, list[dict[str, Any]]] = {}
            for res in resources:
                tf_type = res.get("terraform_resource_type", "unknown")
                if tf_type not in by_type_list:
                    by_type_list[tf_type] = []
                by_type_list[tf_type].append(res)

            for tf_type, type_resources in sorted(by_type_list.items()):
                builder.add_header(f"`{tf_type}` ({len(type_resources)})", level=3)
                for res in type_resources[:5]:  # Show first 5 per type
                    name = res.get("name", res.get("cloud_resource_id", "unnamed"))
                    region = res.get("region", "")
                    builder.add_list_item(f"`{name}` ({region})")
                if len(type_resources) > 5:
                    builder.add_paragraph(f"... and {len(type_resources) - 5} more")
            builder.add_line_break()

        # Diagrams
        diagrams = results.get("diagrams", {})
        if diagrams and "system_overview" in diagrams:
            builder.add_header("Infrastructure Diagram", level=2)
            builder.add_code_block(diagrams["system_overview"], language="mermaid")
            builder.add_line_break()

        # Validation issues
        validation_issues = results.get("validation_issues", [])
        if validation_issues:
            builder.add_header("Validation Issues", level=2)
            for issue in validation_issues:
                builder.add_list_item(f"⚠️ {issue}")
            builder.add_line_break()

        # Compliance (if included)
        compliance = results.get("compliance", {})
        if compliance and not compliance.get("error"):
            builder.add_header("Compliance Considerations", level=2)
            controls = compliance.get("controls", [])
            if controls:
                builder.add_paragraph(f"Found {len(controls)} compliance controls to consider.")
            builder.add_line_break()

        # Best practices (if included)
        best_practices = results.get("best_practices", {})
        if best_practices and not best_practices.get("error"):
            builder.add_header("Best Practices", level=2)
            recommendations = best_practices.get("recommendations", [])
            for rec in recommendations[:5]:
                builder.add_list_item(rec)
            builder.add_line_break()

        # Filtering status
        filtering = results.get("filtering", {})
        if filtering.get("applied"):
            builder.add_header("Filtering Applied", level=2)
            builder.add_paragraph(
                f"**Server-side filtering applied**: Filtered out "
                f"{filtering.get('filtered_count', 0)} already-managed resources. "
                f"{filtering.get('remaining_count', 0)} resources remaining for import."
            )
            builder.add_line_break()
        else:
            # Show helper code for client-side filtering
            builder.add_header("Filtering Already-Managed Resources", level=2)
            builder.add_paragraph(
                "To exclude resources already managed by Terraform, you can either:\n\n"
                "1. **Provide state content** (recommended): Pass `terraform_state_content` "
                "parameter with your state file JSON for server-side filtering\n\n"
                "2. **Use helper code** (fallback): Use the helper code below with your "
                "local Terraform state file for client-side filtering"
            )
            builder.add_line_break()

        builder.add_header("Python Helper Code", level=3)
        builder.add_code_block("""import json
from pathlib import Path
from typing import Any

def filter_managed_resources(
    discovered_resources: list[dict[str, Any]],
    terraform_state_path: str | Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    \"\"\"Filter out resources already managed by Terraform.
    
    Args:
        discovered_resources: List of discovered resources from WISTX
        terraform_state_path: Path to terraform.tfstate file
        
    Returns:
        Tuple of (unmanaged_resources, managed_resources)
    \"\"\"
    with open(terraform_state_path, 'r') as f:
        state = json.load(f)
    
    managed_ids = set()
    resources = state.get("resources", [])
    
    for resource in resources:
        resource_type = resource.get("type", "")
        instances = resource.get("instances", [])
        
        for instance in instances:
            attributes = instance.get("attributes", {})
            resource_id = attributes.get("id") or attributes.get("arn") or attributes.get("name")
            if resource_id:
                managed_ids.add(resource_id)
    
    unmanaged = []
    managed = []
    
    for resource in discovered_resources:
        resource_id = resource.get("cloud_resource_id")
        arn = resource.get("arn")
        name = resource.get("name")
        
        is_managed = (
            resource_id in managed_ids or
            (arn and arn in managed_ids) or
            (name and name in managed_ids)
        )
        
        if is_managed:
            managed.append(resource)
        else:
            unmanaged.append(resource)
    
    return unmanaged, managed
""", language="python")
        builder.add_line_break()

        builder.add_header("Finding Your Terraform State File", level=3)
        builder.add_list_item("**Local state**: Look for `terraform.tfstate` in your Terraform directory")
        builder.add_list_item("**Remote backend**: Run `terraform state pull > terraform.tfstate` to download")
        builder.add_list_item("**Common locations**:")
        builder.add_code_block("""# Local state
./terraform.tfstate
./.terraform/terraform.tfstate

# Remote backend (download first)
terraform state pull > terraform.tfstate
""", language="bash")
        builder.add_line_break()

        # Next steps
        builder.add_header("Next Steps", level=2)
        builder.add_list_item("1. Locate your Terraform state file (see hints above)")
        builder.add_list_item("2. Use the helper code to filter discovered resources")
        builder.add_list_item("3. Create Terraform configuration files only for unmanaged resources")
        builder.add_list_item("4. Run the import commands in the specified order")
        builder.add_list_item("5. Run `terraform plan` to verify the imported state matches actual infrastructure")
        builder.add_list_item("6. Commit the Terraform configuration to version control")

        return builder.build()
    
    @staticmethod
    def format_indexing_setup_guide(results: dict[str, Any]) -> str:
        """Format repository indexing setup guide as markdown.
        
        Args:
            results: Setup guide dictionary from search_codebase
            
        Returns:
            Formatted markdown string with setup instructions
        """
        builder = MarkdownBuilder()
        builder.add_header("Repository Indexing Required", level=1)
        
        message = results.get("message", "No indexed resources found")
        builder.add_paragraph(f"**{message}**")
        builder.add_line_break()
        
        setup_guide = results.get("setup_guide", {})
        overview = setup_guide.get("overview", "")
        if overview:
            builder.add_paragraph(overview)
            builder.add_line_break()
        
        steps = setup_guide.get("steps", [])
        if steps:
            builder.add_header("Setup Steps", level=2)
            builder.add_line_break()
            
            for step_data in steps:
                step_num = step_data.get("step", 0)
                title = step_data.get("title", "")
                description = step_data.get("description", "")
                status = step_data.get("status", "pending")
                status_icon = "✅" if status == "completed" else "⏳"
                
                builder.add_header(f"{status_icon} Step {step_num}: {title}", level=3)
                builder.add_paragraph(description)
                builder.add_line_break()
                
                instructions = step_data.get("instructions", [])
                if instructions:
                    for instruction in instructions:
                        builder.add_list_item(instruction)
                    builder.add_line_break()
                
                example_request = step_data.get("example_request", {})
                if example_request:
                    builder.add_header("Example Usage", level=4)
                    if example_request.get("tool"):
                        import json
                        params = json.dumps(example_request.get("parameters", {}), indent=2)
                        builder.add_code_block(
                            f"{example_request.get('tool')}(\n{params}\n)",
                            language="python",
                        )
                    builder.add_line_break()
                
                note = step_data.get("note", "")
                if note:
                    builder.add_paragraph(f"*Note: {note}*")
                    builder.add_line_break()
        
        quick_start = setup_guide.get("quick_start", {})
        if quick_start:
            builder.add_separator()
            builder.add_header("Quick Start", level=2)
            builder.add_paragraph(quick_start.get("description", ""))
            builder.add_code_block(quick_start.get("example", ""), language="python")
            builder.add_line_break()
        
        alternatives = setup_guide.get("alternative_methods", {})
        if alternatives:
            builder.add_separator()
            builder.add_header("Alternative Methods", level=2)
            dashboard = alternatives.get("dashboard", "")
            if dashboard:
                builder.add_paragraph(dashboard)
            builder.add_line_break()
        
        api_endpoints = results.get("api_endpoints", {})
        if api_endpoints:
            builder.add_header("Available Tools", level=2)
            for endpoint_name, endpoint_info in api_endpoints.items():
                tool = endpoint_info.get("tool", "")
                desc = endpoint_info.get("description", "")
                builder.add_list_item(f"**{tool}**: {desc}")
            builder.add_line_break()
        
        builder.add_separator()
        builder.add_paragraph(
            "Once you've indexed at least one repository, you can search your codebase. "
            "The tool will automatically use your indexed repositories."
        )
        
        return builder.build()
    
    @staticmethod
    def format_connection_setup_guide(results: dict[str, Any]) -> str:
        """Format AWS connection setup guide as markdown.
        
        Args:
            results: Setup guide dictionary from discover_cloud_resources
            
        Returns:
            Formatted markdown string with setup instructions
        """
        builder = MarkdownBuilder()
        builder.add_header("AWS Connection Setup Required", level=1)
        
        message = results.get("message", "AWS connection not configured")
        builder.add_paragraph(f"**{message}**")
        builder.add_line_break()
        
        setup_guide = results.get("setup_guide", {})
        overview = setup_guide.get("overview", "")
        if overview:
            builder.add_paragraph(overview)
            builder.add_line_break()
        
        steps = setup_guide.get("steps", [])
        if steps:
            builder.add_header("Setup Steps", level=2)
            builder.add_line_break()
            
            for step_data in steps:
                step_num = step_data.get("step", 0)
                title = step_data.get("title", "")
                description = step_data.get("description", "")
                
                builder.add_header(f"Step {step_num}: {title}", level=3)
                builder.add_paragraph(description)
                builder.add_line_break()
                
                instructions = step_data.get("instructions", [])
                if instructions:
                    for instruction in instructions:
                        builder.add_list_item(instruction)
                    builder.add_line_break()
                
                api_endpoint = step_data.get("api_endpoint", "")
                example_request = step_data.get("example_request", {})
                if api_endpoint and example_request:
                    builder.add_header("API Example", level=4)
                    import json
                    body_str = json.dumps(example_request.get("body", {}), indent=2)
                    builder.add_code_block(
                        f"curl -X {example_request.get('method', 'POST')} "
                        f"'{example_request.get('url', '')}' \\\n"
                        f"  -H 'Authorization: Bearer YOUR_API_KEY' \\\n"
                        f"  -H 'Content-Type: application/json' \\\n"
                        f"  -d '{body_str}'",
                        language="bash",
                    )
                    builder.add_line_break()
                
                aws_cli_example = step_data.get("aws_cli_example", "")
                if aws_cli_example:
                    builder.add_header("AWS CLI Example", level=4)
                    builder.add_code_block(aws_cli_example, language="bash")
                    builder.add_line_break()
                
                trust_policy = step_data.get("trust_policy", "")
                if trust_policy:
                    builder.add_header("Trust Policy", level=4)
                    builder.add_code_block(trust_policy, language="json")
                    builder.add_line_break()
                
                permission_policy = step_data.get("permission_policy", "")
                if permission_policy:
                    builder.add_header("Permission Policy", level=4)
                    builder.add_code_block(permission_policy, language="json")
                    builder.add_line_break()
                
                security_warning = step_data.get("security_warning", "")
                if security_warning:
                    builder.add_paragraph(f"**{security_warning}**")
                    builder.add_line_break()
                
                dashboard_alternative = step_data.get("dashboard_alternative", "")
                if dashboard_alternative:
                    builder.add_paragraph(f"💡 **{dashboard_alternative}**")
                    builder.add_line_break()
                
                note = step_data.get("note", "")
                if note:
                    builder.add_paragraph(f"*Note: {note}*")
                    builder.add_line_break()
        
        alternatives = setup_guide.get("alternative_methods", {})
        if alternatives:
            builder.add_header("Alternative Methods", level=2)
            dashboard = alternatives.get("dashboard", "")
            if dashboard:
                builder.add_paragraph(dashboard)
            builder.add_line_break()
        
        api_endpoints = results.get("api_endpoints", {})
        if api_endpoints:
            builder.add_header("Available API Endpoints", level=2)
            for endpoint_name, endpoint_info in api_endpoints.items():
                method = endpoint_info.get("method", "")
                path = endpoint_info.get("path", "")
                desc = endpoint_info.get("description", "")
                builder.add_list_item(f"**{method} {path}**: {desc}")
            builder.add_line_break()
        
        wistx_account_id = results.get("wistx_account_id", "")
        if wistx_account_id and wistx_account_id != "WISTX_ACCOUNT_ID":
            builder.add_paragraph(f"**WISTX AWS Account ID**: `{wistx_account_id}`")
            builder.add_line_break()
        
        # Recommended method (dashboard)
        recommended = setup_guide.get("recommended_method", {})
        if recommended:
            builder.add_separator()
            builder.add_header(recommended.get("title", "Recommended Method"), level=2)
            description = recommended.get("description", "")
            if description:
                builder.add_code_block(description, language="markdown")
                builder.add_line_break()
            
            steps = recommended.get("steps", [])
            if steps:
                builder.add_header("Dashboard Setup Steps", level=3)
                for step in steps:
                    builder.add_list_item(step)
                builder.add_line_break()
        
        # Alternative methods
        alternatives = setup_guide.get("alternative_methods", {})
        if alternatives:
            builder.add_separator()
            builder.add_header("Alternative Methods", level=2)
            
            env_vars = alternatives.get("environment_variables", {})
            if env_vars:
                builder.add_header(env_vars.get("title", "Environment Variables"), level=3)
                builder.add_paragraph(env_vars.get("description", ""))
                builder.add_line_break()
            
            direct_params = alternatives.get("direct_parameters", {})
            if direct_params:
                builder.add_header(direct_params.get("title", "Direct Parameters"), level=3)
                builder.add_paragraph(direct_params.get("description", ""))
                builder.add_line_break()
        
        # Interactive flow section (with security warning)
        interactive_flow = setup_guide.get("interactive_flow", {})
        if interactive_flow:
            builder.add_separator()
            builder.add_header("Chat-Based Setup (Not Recommended for Production)", level=2)
            
            security_warning = interactive_flow.get("security_warning", "")
            if security_warning:
                builder.add_paragraph(f"**{security_warning}**")
                builder.add_line_break()
            
            description = interactive_flow.get("description", "")
            if description:
                builder.add_code_block(description, language="text")
                builder.add_line_break()
            
            agent_can_help = interactive_flow.get("coding_agent_can_help", [])
            if agent_can_help:
                builder.add_header("What I Can Help With", level=3)
                for item in agent_can_help:
                    builder.add_list_item(item)
                builder.add_line_break()
            
            requires_user = interactive_flow.get("requires_user_action", [])
            if requires_user:
                builder.add_header("What You Need To Do", level=3)
                for item in requires_user:
                    builder.add_list_item(item)
                builder.add_line_break()
        
        # Step status indicators
        steps = setup_guide.get("steps", [])
        if steps:
            builder.add_separator()
            builder.add_header("Setup Progress", level=2)
            for step_data in steps:
                step_num = step_data.get("step", 0)
                title = step_data.get("title", "")
                status = step_data.get("status", "pending")
                status_icon = "✅" if status == "completed" else "⏳"
                builder.add_list_item(f"{status_icon} Step {step_num}: {title} ({status})")
            builder.add_line_break()
        
        builder.add_separator()
        builder.add_paragraph(
            "**Next Steps:** Once you've created the IAM role in AWS, just provide me with the Role ARN "
            "and I'll validate the connection and run discovery automatically!"
        )
        
        return builder.build()

