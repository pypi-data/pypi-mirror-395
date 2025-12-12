"""Script to migrate integration patterns from hardcoded dictionary to knowledge base.

Converts all patterns in INTEGRATION_PATTERNS to KnowledgeArticle objects and stores
them in MongoDB and Pinecone for dynamic retrieval via vector search.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any

from data_pipelines.models.knowledge_article import ContentType, Domain, KnowledgeArticle
from wistx_mcp.tools.lib.integration_patterns import INTEGRATION_PATTERNS
from api.services.github_service import GitHubService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_pattern_article(
    integration_type: str,
    pattern_name: str,
    pattern_data: dict[str, Any],
) -> KnowledgeArticle:
    """Create KnowledgeArticle from pattern data.

    Args:
        integration_type: Integration type (networking, security, service, monitoring)
        pattern_name: Pattern name (e.g., "vpc_peering")
        pattern_data: Pattern dictionary

    Returns:
        KnowledgeArticle object
    """
    article_id = f"pattern-{integration_type}-{pattern_name}"
    
    description = pattern_data.get("description", "")
    providers = pattern_data.get("providers", [])
    components = pattern_data.get("components", [])
    
    terraform_example = pattern_data.get("terraform_example", "")
    kubernetes_example = pattern_data.get("kubernetes_example", "")
    
    code_examples = []
    if terraform_example:
        code_examples.append(f"## Terraform Example\n\n```hcl\n{terraform_example.strip()}\n```")
    if kubernetes_example:
        code_examples.append(f"## Kubernetes Example\n\n```yaml\n{kubernetes_example.strip()}\n```")
    
    content_parts = [
        f"# {pattern_name.replace('_', ' ').title()} Pattern",
        "",
        f"## Description\n\n{description}",
        "",
    ]
    
    if code_examples:
        content_parts.append("\n\n".join(code_examples))
        content_parts.append("")
    
    dependencies = pattern_data.get("dependencies", [])
    if dependencies:
        content_parts.append("## Dependencies\n\n")
        for dep in dependencies:
            content_parts.append(f"- {dep}")
        content_parts.append("")
    
    security_rules = pattern_data.get("security_rules", [])
    if security_rules:
        content_parts.append("## Security Rules\n\n")
        for rule in security_rules:
            content_parts.append(f"- {rule}")
        content_parts.append("")
    
    monitoring_config = pattern_data.get("monitoring_config", {})
    if monitoring_config:
        content_parts.append("## Monitoring Configuration\n\n")
        if monitoring_config.get("metrics"):
            content_parts.append("### Metrics\n")
            for metric in monitoring_config["metrics"]:
                content_parts.append(f"- {metric}")
            content_parts.append("")
        if monitoring_config.get("alarms"):
            content_parts.append("### Alarms\n")
            for alarm in monitoring_config["alarms"]:
                content_parts.append(f"- {alarm}")
            content_parts.append("")
        if monitoring_config.get("logs"):
            content_parts.append("### Logs\n")
            for log in monitoring_config["logs"]:
                content_parts.append(f"- {log}")
            content_parts.append("")
    
    implementation_guidance = pattern_data.get("implementation_guidance", [])
    if implementation_guidance:
        content_parts.append("## Implementation Guidance\n\n")
        for step in implementation_guidance:
            content_parts.append(step)
        content_parts.append("")
    
    compliance_considerations = pattern_data.get("compliance_considerations", [])
    if compliance_considerations:
        content_parts.append("## Compliance Considerations\n\n")
        for consideration in compliance_considerations:
            content_parts.append(f"- {consideration}")
        content_parts.append("")
    
    content = "\n".join(content_parts)
    
    structured_data = {
        "integration_type": integration_type,
        "pattern_name": pattern_name,
        "providers": providers,
        "components": components,
        "terraform_example": terraform_example,
        "kubernetes_example": kubernetes_example,
        "dependencies": dependencies,
        "security_rules": security_rules,
        "monitoring_config": monitoring_config,
        "implementation_guidance": implementation_guidance,
        "compliance_considerations": compliance_considerations,
    }
    
    tags = [integration_type, pattern_name] + components + providers
    categories = [integration_type, "infrastructure", "integration"]
    
    services = []
    for component in components:
        if component not in ["vpc", "subnet", "route_table", "service", "resource"]:
            services.append(component)
    
    article = KnowledgeArticle(
        article_id=article_id,
        domain=Domain.INFRASTRUCTURE,
        subdomain=integration_type,
        content_type=ContentType.PATTERN,
        title=f"{pattern_name.replace('_', ' ').title()} Integration Pattern",
        summary=description[:500] if len(description) > 500 else description,
        content=content,
        structured_data=structured_data,
        tags=tags[:20],
        categories=categories,
        cloud_providers=providers,
        services=services,
        source_url=f"https://wistx.ai/patterns/{integration_type}/{pattern_name}",
        version="1.0",
        visibility="global",
        source_type="automated",
        quality_score=100.0,
    )
    
    return article


async def migrate_all_patterns() -> list[str]:
    """Migrate all patterns to knowledge base.

    Returns:
        List of article IDs created
    """
    github_service = GitHubService()
    article_ids = []
    
    for integration_type, patterns in INTEGRATION_PATTERNS.items():
        for pattern_name, pattern_data in patterns.items():
            try:
                article = create_pattern_article(integration_type, pattern_name, pattern_data)
                await github_service._store_article(article)
                article_ids.append(article.article_id)
                
                logger.info(
                    "Migrated pattern %s/%s to knowledge base: %s",
                    integration_type,
                    pattern_name,
                    article.article_id,
                )
            except Exception as e:
                logger.error(
                    "Failed to migrate pattern %s/%s: %s",
                    integration_type,
                    pattern_name,
                    e,
                    exc_info=True,
                )
    
    return article_ids


async def main():
    """Main function to migrate patterns."""
    logger.info("Starting pattern migration to knowledge base...")
    
    article_ids = await migrate_all_patterns()
    
    logger.info(
        "Migration complete: %d patterns migrated to knowledge base",
        len(article_ids),
    )
    
    logger.info("Patterns are now available via vector search with content_type='pattern'")


if __name__ == "__main__":
    asyncio.run(main())

