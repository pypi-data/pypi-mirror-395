"""Pattern matching utilities for pytemplify.

This module provides reusable pattern matching functionality that can be used
by both generator and validation modules without creating circular dependencies.
"""

import logging
import re
from fnmatch import fnmatch
from typing import List, Optional

logger = logging.getLogger(__name__)


class PatternMatcher:
    """Matches strings against include/exclude patterns.

    Supports both glob patterns and regex patterns (prefixed with 'regex:').
    """

    def __init__(
        self,
        include_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
    ) -> None:
        """Initialize the pattern matcher.

        Args:
            include_patterns: Patterns to include (glob or regex:pattern)
            exclude_patterns: Patterns to exclude (glob or regex:pattern)
        """
        self.include_patterns = include_patterns or []
        self.exclude_patterns = exclude_patterns or []

    def should_include(self, text: str) -> bool:
        """Determine if text should be included based on filters.

        Args:
            text: String to check against patterns

        Returns:
            True if text matches include patterns and not exclude patterns
        """
        # If exclude patterns specified, text must not match any
        if self.exclude_patterns:
            for pattern in self.exclude_patterns:
                if self._matches_pattern(text, pattern):
                    return False

        # If include patterns specified, text must match at least one
        if self.include_patterns:
            if not any(self._matches_pattern(text, pattern) for pattern in self.include_patterns):
                return False

        return True

    def _matches_pattern(self, text: str, pattern: str) -> bool:
        """Check if text matches the given pattern.

        Args:
            text: String to match
            pattern: Pattern (glob or regex:pattern)

        Returns:
            True if text matches pattern
        """
        if pattern.startswith("regex:"):
            # Use regex matching
            regex_pattern = pattern[6:]  # Remove 'regex:' prefix
            try:
                return bool(re.match(regex_pattern, text))
            except re.error as exc:
                # Invalid regex - log warning and return False
                logger.warning("Invalid regex pattern '%s': %s", regex_pattern, exc)
                return False
        else:
            # Use glob pattern matching
            return fnmatch(text, pattern)
