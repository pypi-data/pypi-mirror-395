"""Regex pattern validation and security checks."""

import asyncio
import logging
import re
from concurrent.futures import ThreadPoolExecutor
from typing import Any

logger = logging.getLogger(__name__)

_COMPILATION_TIMEOUT = 1.0
_TEST_MATCH_TIMEOUT = 0.5
_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="regex_validator")


class PatternValidator:
    """Validate and compile regex patterns with security checks."""

    MAX_PATTERN_LENGTH = 10000
    MAX_COMPLEXITY_SCORE = 1000

    def __init__(self) -> None:
        """Initialize pattern validator."""
        self.dangerous_patterns = [
            r"\(.*\)\+",
            r"\.\*\+",
            r"\(.+\)\+",
            r"\(.+\)\*",
            r"\(.*\)\*",
            r"\(.+\)\{",
            r"\(.*\)\{",
        ]
        
        self.regex_redos_patterns = [
            r"(.+)+",
            r"(.*)*",
            r"(.+)*",
            r"(.*)+",
            r"(.+){",
            r"(.*){",
            r"(.+)\+",
            r"(.*)\+",
            r"(.+)\*",
            r"(.*)\*",
        ]

    async def validate_pattern(self, pattern: str, timeout: float = _COMPILATION_TIMEOUT) -> dict[str, Any]:
        """Validate regex pattern for security and correctness with timeout protection.

        Args:
            pattern: Regex pattern to validate
            timeout: Maximum time allowed for compilation (seconds)

        Returns:
            Dictionary with validation results:
            - valid: Whether pattern is valid
            - error: Error message if invalid
            - warnings: List of warnings
        """
        warnings: list[str] = []

        if not pattern:
            return {
                "valid": False,
                "error": "Pattern cannot be empty",
                "warnings": [],
            }

        if len(pattern) > self.MAX_PATTERN_LENGTH:
            return {
                "valid": False,
                "error": f"Pattern exceeds maximum length of {self.MAX_PATTERN_LENGTH}",
                "warnings": [],
            }

        complexity_score = self._calculate_complexity(pattern)
        if complexity_score > self.MAX_COMPLEXITY_SCORE:
            return {
                "valid": False,
                "error": f"Pattern complexity too high ({complexity_score} > {self.MAX_COMPLEXITY_SCORE}). "
                         "This pattern may cause performance issues or ReDoS attacks.",
                "warnings": warnings,
            }

        for dangerous_pattern in self.dangerous_patterns:
            if re.search(dangerous_pattern, pattern):
                return {
                    "valid": False,
                    "error": "Pattern contains dangerous constructs that may cause "
                             "ReDoS (Regular Expression Denial of Service). "
                             "Please use a simpler pattern.",
                    "warnings": warnings,
                }

        for redos_pattern in self.regex_redos_patterns:
            if redos_pattern in pattern:
                return {
                    "valid": False,
                    "error": f"Pattern contains ReDoS vulnerability: '{redos_pattern}'. "
                             "This pattern can cause catastrophic backtracking.",
                    "warnings": warnings,
                }

        try:
            compiled_pattern = await self._compile_with_timeout(pattern, timeout)
            await self._test_match_with_timeout(compiled_pattern, timeout=_TEST_MATCH_TIMEOUT)
        except asyncio.TimeoutError:
            return {
                "valid": False,
                "error": f"Pattern compilation or testing timed out after {timeout} seconds. "
                         "This may indicate a ReDoS vulnerability.",
                "warnings": warnings,
            }
        except re.error as e:
            return {
                "valid": False,
                "error": f"Invalid regex pattern: {e}",
                "warnings": warnings,
            }
        except Exception as e:
            logger.warning("Unexpected error validating pattern: %s", e)
            return {
                "valid": False,
                "error": f"Pattern validation failed: {e}",
                "warnings": warnings,
            }

        return {
            "valid": True,
            "error": None,
            "warnings": warnings,
        }

    async def _compile_with_timeout(self, pattern: str, timeout: float) -> re.Pattern[str]:
        """Compile regex pattern with timeout protection.

        Args:
            pattern: Regex pattern to compile
            timeout: Maximum time allowed (seconds)

        Returns:
            Compiled regex pattern

        Raises:
            asyncio.TimeoutError: If compilation exceeds timeout
            re.error: If pattern is invalid
        """
        loop = asyncio.get_event_loop()
        try:
            compiled = await asyncio.wait_for(
                loop.run_in_executor(_executor, re.compile, pattern),
                timeout=timeout,
            )
            return compiled
        except asyncio.TimeoutError:
            logger.warning("Regex compilation timed out: %s", pattern[:100])
            raise

    async def _test_match_with_timeout(
        self,
        compiled_pattern: re.Pattern[str],
        test_string: str = "test",
        timeout: float = _TEST_MATCH_TIMEOUT,
    ) -> None:
        """Test regex pattern matching with timeout protection.

        Tests with multiple strings including potential ReDoS triggers.

        Args:
            compiled_pattern: Compiled regex pattern
            test_string: Test string to match against
            timeout: Maximum time allowed (seconds)

        Raises:
            asyncio.TimeoutError: If matching exceeds timeout
        """
        loop = asyncio.get_event_loop()
        test_strings = [
            test_string,
            "a" * 50,
            "a" * 100,
            "ab" * 50,
            "a" * 1000,
            "a" + "b" * 50 + "a",
            "".join(chr(i) for i in range(256)),
        ]
        
        for test_str in test_strings:
            try:
                await asyncio.wait_for(
                    loop.run_in_executor(_executor, compiled_pattern.search, test_str),
                    timeout=timeout,
                )
            except asyncio.TimeoutError:
                logger.warning("Regex matching timed out during validation with test string length %d", len(test_str))
                raise

    def compile_pattern(
        self,
        pattern: str,
        case_sensitive: bool = False,
        multiline: bool = False,
        dotall: bool = False,
    ) -> re.Pattern[str]:
        """Compile regex pattern with flags.

        Args:
            pattern: Regex pattern
            case_sensitive: Case-sensitive matching
            multiline: Multiline mode
            dotall: Dot matches newline

        Returns:
            Compiled regex pattern

        Raises:
            ValueError: If pattern is invalid
        """
        flags = 0
        if not case_sensitive:
            flags |= re.IGNORECASE
        if multiline:
            flags |= re.MULTILINE
        if dotall:
            flags |= re.DOTALL

        try:
            return re.compile(pattern, flags)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}") from e

    def _calculate_complexity(self, pattern: str) -> int:
        """Calculate pattern complexity score.

        Args:
            pattern: Regex pattern

        Returns:
            Complexity score (higher = more complex)
        """
        score = 0

        score += len(pattern)
        score += pattern.count("(") * 10
        score += pattern.count("+") * 5
        score += pattern.count("*") * 5
        score += pattern.count("?") * 3
        score += pattern.count("|") * 10
        score += pattern.count("[") * 5
        score += pattern.count("{") * 10

        return score

