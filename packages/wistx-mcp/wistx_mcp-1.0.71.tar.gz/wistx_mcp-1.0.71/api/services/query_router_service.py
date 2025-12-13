"""Query Router Service.

Routes queries to appropriate knowledge sources based on query analysis.
Determines whether to search:
1. User's personal knowledge base (on-demand research)
2. Global knowledge base (pre-indexed content)
3. Both (hybrid approach)

This enables intelligent routing for optimal retrieval performance.
"""

import logging
import re
from dataclasses import dataclass
from enum import Enum
from typing import Any

from data_pipelines.config.official_docs_registry import get_all_technologies

logger = logging.getLogger(__name__)


class QueryTarget(Enum):
    """Target knowledge sources for a query."""
    USER_ONLY = "user_only"           # Only user's personal KB
    GLOBAL_ONLY = "global_only"       # Only global KB
    USER_FIRST = "user_first"         # User KB first, then global
    GLOBAL_FIRST = "global_first"     # Global KB first, then user
    BOTH_PARALLEL = "both_parallel"   # Search both in parallel


@dataclass
class RoutingDecision:
    """Result of query routing analysis."""
    target: QueryTarget
    confidence: float
    reasoning: str
    detected_technologies: list[str]
    is_specific_query: bool
    suggested_domains: list[str]


class QueryRouterService:
    """Routes queries to appropriate knowledge sources.
    
    Analyzes queries to determine the best retrieval strategy:
    - Specific technology queries → User KB (if researched) or Global
    - General best practices → Global KB
    - Recent/specific project context → User KB
    """
    
    # Keywords indicating user-specific context
    USER_CONTEXT_KEYWORDS = {
        "my", "our", "this project", "my project", "our project",
        "i researched", "we researched", "i added", "we added",
        "my knowledge", "my docs", "my documentation",
    }
    
    # Keywords indicating global/general queries
    GLOBAL_CONTEXT_KEYWORDS = {
        "best practice", "best practices", "industry standard",
        "recommended", "general", "common", "typical",
        "how to", "what is", "explain", "overview",
    }
    
    def __init__(self):
        """Initialize query router."""
        self.known_technologies = set(get_all_technologies())
    
    def route_query(
        self,
        query: str,
        user_has_kb: bool = False,
        user_kb_technologies: list[str] | None = None,
    ) -> RoutingDecision:
        """Route a query to appropriate knowledge sources.
        
        Args:
            query: Search query
            user_has_kb: Whether user has personal KB content
            user_kb_technologies: Technologies in user's KB
            
        Returns:
            RoutingDecision with target and reasoning
        """
        query_lower = query.lower()
        
        # Detect technologies in query
        detected_techs = self._detect_technologies(query_lower)
        
        # Check for user-specific context
        has_user_context = any(
            kw in query_lower for kw in self.USER_CONTEXT_KEYWORDS
        )
        
        # Check for global/general context
        has_global_context = any(
            kw in query_lower for kw in self.GLOBAL_CONTEXT_KEYWORDS
        )
        
        # Determine if query is specific (mentions specific tech)
        is_specific = len(detected_techs) > 0
        
        # Suggest domains based on detected technologies
        suggested_domains = self._suggest_domains(detected_techs)
        
        # Routing logic
        if has_user_context and user_has_kb:
            return RoutingDecision(
                target=QueryTarget.USER_FIRST,
                confidence=0.9,
                reasoning="Query contains user-specific context keywords",
                detected_technologies=detected_techs,
                is_specific_query=is_specific,
                suggested_domains=suggested_domains,
            )
        
        if has_global_context:
            return RoutingDecision(
                target=QueryTarget.GLOBAL_FIRST,
                confidence=0.85,
                reasoning="Query asks for general/best practice information",
                detected_technologies=detected_techs,
                is_specific_query=is_specific,
                suggested_domains=suggested_domains,
            )
        
        # Check if user has researched the detected technologies
        user_kb_techs = set(user_kb_technologies or [])
        if detected_techs and user_has_kb:
            matching_techs = set(detected_techs) & user_kb_techs
            if matching_techs:
                return RoutingDecision(
                    target=QueryTarget.USER_FIRST,
                    confidence=0.8,
                    reasoning=f"User has researched: {', '.join(matching_techs)}",
                    detected_technologies=detected_techs,
                    is_specific_query=is_specific,
                    suggested_domains=suggested_domains,
                )
        
        # Default: search both if user has KB, otherwise global only
        if user_has_kb:
            return RoutingDecision(
                target=QueryTarget.BOTH_PARALLEL,
                confidence=0.6,
                reasoning="No specific context detected, searching both sources",
                detected_technologies=detected_techs,
                is_specific_query=is_specific,
                suggested_domains=suggested_domains,
            )
        
        return RoutingDecision(
            target=QueryTarget.GLOBAL_ONLY,
            confidence=0.7,
            reasoning="User has no personal KB, using global only",
            detected_technologies=detected_techs,
            is_specific_query=is_specific,
            suggested_domains=suggested_domains,
        )

    def _detect_technologies(self, query: str) -> list[str]:
        """Detect technologies mentioned in query.

        Args:
            query: Lowercase query string

        Returns:
            List of detected technology names
        """
        detected = []

        for tech in self.known_technologies:
            # Check for exact word match
            pattern = r'\b' + re.escape(tech.lower()) + r'\b'
            if re.search(pattern, query):
                detected.append(tech)

        return detected

    def _suggest_domains(self, technologies: list[str]) -> list[str]:
        """Suggest domains based on detected technologies.

        Args:
            technologies: List of detected technologies

        Returns:
            List of suggested domain names
        """
        from data_pipelines.services.intent_analysis_service import (
            WISTX_TECHNOLOGY_CATEGORIES,
        )

        domains = set()

        for tech in technologies:
            tech_lower = tech.lower()
            for category, techs in WISTX_TECHNOLOGY_CATEGORIES.items():
                if tech_lower in [t.lower() for t in techs]:
                    domains.add(category)

        return list(domains) if domains else ["devops", "infrastructure"]

    async def get_user_kb_info(self, user_id: str) -> dict[str, Any]:
        """Get information about user's knowledge base.

        Args:
            user_id: User ID

        Returns:
            Dictionary with KB info (has_content, technologies, session_count)
        """
        from api.database.mongodb import mongodb_manager

        db = mongodb_manager.get_database()

        # Check for user chunks
        chunks_collection = db.user_knowledge_chunks
        chunk_count = chunks_collection.count_documents({"user_id": user_id})

        if chunk_count == 0:
            return {
                "has_content": False,
                "technologies": [],
                "session_count": 0,
                "chunk_count": 0,
            }

        # Get unique technologies from sessions
        sessions_collection = db.user_research_sessions
        sessions = list(sessions_collection.find(
            {"user_id": user_id, "status": "completed"},
            {"metadata.intent_analysis.technologies": 1},
        ))

        technologies = set()
        for session in sessions:
            intent = session.get("metadata", {}).get("intent_analysis", {})
            techs = intent.get("technologies", [])
            technologies.update(techs)

        return {
            "has_content": True,
            "technologies": list(technologies),
            "session_count": len(sessions),
            "chunk_count": chunk_count,
        }

