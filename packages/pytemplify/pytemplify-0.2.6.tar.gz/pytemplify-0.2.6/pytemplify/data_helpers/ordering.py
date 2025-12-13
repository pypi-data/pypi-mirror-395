"""
Helper ordering based on specificity analysis.

This module provides automatic ordering of DataHelper classes by analyzing their
matches() method implementations. More specific helpers (those with more detailed
matching criteria) are prioritized to be checked first during helper selection.

Specificity Scoring:
    The scoring system analyzes the AST (Abstract Syntax Tree) of the matches() method:
    - Each `"key" in data` check: +10 points (strong indicator of specific structure)
    - Each `isinstance()` check: +5 points (type validation)
    - Each `.get()` call: +3 points (careful key access)
    - Each comparison operator (==, !=, <, >, etc.): +2 points (value validation)
    - Explicit `priority` attribute: overrides automatic calculation

Why This Matters:
    When multiple helpers match the same data, the most specific one should be used.
    For example, if you have both a generic "DocumentHelper" and a specific
    "InvoiceDocumentHelper", the invoice helper should be checked first.

Example:
    from pytemplify.data_helpers import DataHelper
    from pytemplify.data_helpers.ordering import sort_helpers_by_specificity

    class GenericHelper(DataHelper):
        @staticmethod
        def matches(data: dict) -> bool:
            return "type" in data  # Score: 10

    class SpecificHelper(DataHelper):
        @staticmethod
        def matches(data: dict) -> bool:
            return "type" in data and "subtype" in data and data["type"] == "special"
            # Score: 10 + 10 + 2 = 22

    # SpecificHelper will be checked first
    ordered = sort_helpers_by_specificity([GenericHelper, SpecificHelper])
    assert ordered[0] == SpecificHelper

Manual Priority Override:
    class HighPriorityHelper(DataHelper):
        priority = 1000  # Explicit priority overrides automatic calculation

        @staticmethod
        def matches(data: dict) -> bool:
            return "special_field" in data
"""

import ast
import inspect
import textwrap
from typing import TYPE_CHECKING, List, Type

if TYPE_CHECKING:
    from pytemplify.data_helpers.base import DataHelper


def calculate_specificity(helper_class: Type["DataHelper"]) -> int:
    """
    Calculate specificity score for a helper class.

    Higher scores mean more specific helpers (should be checked first).

    Scoring:
    - Each `"key" in data` check: +10 points
    - Each `isinstance()` check: +5 points
    - Each `.get()` call: +3 points
    - Each comparison operator: +2 points
    - Explicit priority attribute: overrides automatic calculation

    Args:
        helper_class: The helper class to analyze

    Returns:
        Specificity score (higher = more specific)
    """
    # Check for explicit priority
    if hasattr(helper_class, "priority"):
        return helper_class.priority

    try:
        # Get the source code of the matches method
        source = inspect.getsource(helper_class.matches)
        # Dedent the source to remove leading whitespace
        source = textwrap.dedent(source)
        tree = ast.parse(source)

        score = 0

        # Walk the AST to count specific patterns
        for node in ast.walk(tree):
            # Count `"key" in data` checks
            if isinstance(node, ast.Compare):
                if isinstance(node.ops[0], ast.In):
                    # Check if it's a string literal being checked in something
                    if isinstance(node.left, ast.Constant) and isinstance(node.left.value, str):
                        score += 10

            # Count isinstance() calls
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == "isinstance":
                    score += 5
                # Count .get() calls
                elif isinstance(node.func, ast.Attribute) and node.func.attr == "get":
                    score += 3

            # Count comparison operators (>, <, ==, !=, etc.)
            elif isinstance(node, ast.Compare):
                for op in node.ops:
                    if isinstance(op, (ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE)):
                        score += 2

        return score

    except (OSError, TypeError, SyntaxError, ValueError):
        # If we can't retrieve or parse the source (e.g. dynamically created
        # functions or lambdas), return default score.
        return 0


def sort_helpers_by_specificity(helper_classes: List[Type["DataHelper"]]) -> List[Type["DataHelper"]]:
    """
    Sort helper classes by specificity (most specific first).

    Args:
        helper_classes: List of helper classes to sort

    Returns:
        Sorted list with most specific helpers first
    """
    # Calculate specificity for each helper and sort by it (descending)
    scored_helpers = [(calculate_specificity(helper), helper) for helper in helper_classes]
    scored_helpers.sort(key=lambda x: x[0], reverse=True)

    return [helper for score, helper in scored_helpers]
