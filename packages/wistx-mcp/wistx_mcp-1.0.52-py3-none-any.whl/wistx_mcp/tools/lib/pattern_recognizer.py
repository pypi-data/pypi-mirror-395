"""Pattern recognition engine for troubleshooting."""

import logging
import re
from collections import Counter
from typing import Any

from wistx_mcp.models.incident import Incident, SolutionKnowledge
from wistx_mcp.tools.lib.mongodb_client import MongoDBClient

logger = logging.getLogger(__name__)


class PatternRecognizer:
    """Recognizes patterns in incidents and solutions."""

    def __init__(self, mongodb_client: MongoDBClient):
        """Initialize pattern recognizer.

        Args:
            mongodb_client: MongoDB client instance
        """
        self.mongodb_client = mongodb_client

    def extract_problem_pattern(
        self,
        issue_description: str,
        error_messages: list[str],
    ) -> str:
        """Extract normalized problem pattern.

        Args:
            issue_description: Issue description
            error_messages: Error messages

        Returns:
            Normalized problem pattern
        """
        text = issue_description.lower()

        for error in error_messages:
            text += " " + error.lower()

        text = re.sub(r"[^a-z0-9\s]+", "", text)
        words = text.split()
        words = [w for w in words if len(w) > 3]

        return " ".join(sorted(set(words)))[:200]

    async def detect_recurring_patterns(
        self,
        incidents: list[Incident],
        min_occurrences: int = 2,
    ) -> list[dict[str, Any]]:
        """Detect recurring problem patterns.

        Args:
            incidents: List of incidents
            min_occurrences: Minimum occurrences to consider recurring

        Returns:
            List of recurring patterns with metadata
        """
        pattern_counter: Counter[str] = Counter()

        for incident in incidents:
            pattern = self.extract_problem_pattern(
                incident.issue_description,
                incident.error_messages,
            )
            pattern_counter[pattern] += 1

        recurring_patterns = []

        for pattern, count in pattern_counter.items():
            if count >= min_occurrences:
                related_incidents = [
                    i.incident_id
                    for i in incidents
                    if self.extract_problem_pattern(i.issue_description, i.error_messages) == pattern
                ]

                recurring_patterns.append({
                    "pattern": pattern,
                    "occurrence_count": count,
                    "related_incidents": related_incidents,
                    "severity": self._get_pattern_severity(related_incidents, incidents),
                })

        recurring_patterns.sort(key=lambda x: x["occurrence_count"], reverse=True)

        return recurring_patterns

    def suggest_prevention(
        self,
        pattern: str,
        solutions: list[SolutionKnowledge],
    ) -> list[str]:
        """Suggest prevention strategies based on pattern.

        Args:
            pattern: Problem pattern
            solutions: Related solutions

        Returns:
            List of prevention strategies
        """
        strategies: set[str] = set()

        for solution in solutions:
            strategies.update(solution.prevention_strategies)

        if not strategies:
            strategies = {
                "Implement proper error handling and logging",
                "Use infrastructure as code with validation",
                "Set up monitoring and alerting",
                "Follow best practices for the infrastructure type",
                "Regular security audits and compliance checks",
            }

        return list(strategies)[:5]

    def _get_pattern_severity(
        self,
        incident_ids: list[str],
        all_incidents: list[Incident],
    ) -> str:
        """Get severity for a pattern based on related incidents.

        Args:
            incident_ids: List of incident IDs
            all_incidents: All incidents

        Returns:
            Severity string
        """
        incident_map = {i.incident_id: i for i in all_incidents}
        severities = [
            incident_map[iid].severity.value
            for iid in incident_ids
            if iid in incident_map
        ]

        if not severities:
            return "medium"

        if "critical" in severities:
            return "critical"
        elif "high" in severities:
            return "high"
        elif "medium" in severities:
            return "medium"
        return "low"

