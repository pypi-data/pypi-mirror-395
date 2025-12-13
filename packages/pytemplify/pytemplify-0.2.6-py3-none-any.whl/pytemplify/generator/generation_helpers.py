"""Helper classes for code generation.

This module contains utility classes used by BaseCodeGenerator:
- DictAttrWrapper: Makes dict keys accessible as attributes
- TemplateIterationContext: Represents context for template iteration
- NestedIterationHandler: Handles nested foreach iteration logic
- EnhancedTemplateRenderer: Enhanced template renderer with filtering
- TemplateSetFilter: Filters template sets by patterns
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from pytemplify.exceptions import BaseGeneratorError
from pytemplify.pattern_matcher import PatternMatcher
from pytemplify.renderer import TemplateRenderer

from .utils import get_nested_attr_or_key


class DictAttrWrapper:
    """Wrapper that makes dictionary keys accessible as attributes for condition evaluation.

    This allows conditions like 'item.field == value' to work with dict objects,
    while still supporting bracket notation like item['field'].
    """

    def __init__(self, data: Any) -> None:
        """Initialize wrapper with data (dict, list, or primitive)."""
        self._data = data

    def __getattr__(self, name: str) -> Any:
        """Access dict keys as attributes."""
        if isinstance(self._data, dict):
            if name in self._data:
                # Recursively wrap nested dicts/lists
                return self._wrap(self._data[name])
            raise AttributeError(f"'{type(self._data).__name__}' object has no attribute '{name}'")
        raise AttributeError(f"'{type(self._data).__name__}' object has no attribute '{name}'")

    def __getitem__(self, key: Any) -> Any:
        """Support bracket notation for dict access."""
        if isinstance(self._data, (dict, list)):
            return self._wrap(self._data[key])
        raise TypeError(f"'{type(self._data).__name__}' object is not subscriptable")

    def __eq__(self, other: Any) -> bool:
        """Support equality comparison."""
        if isinstance(other, DictAttrWrapper):
            return self._data == other._data
        return self._data == other

    def __ne__(self, other: Any) -> bool:
        """Support inequality comparison."""
        return not self.__eq__(other)

    def __repr__(self) -> str:
        """String representation."""
        return f"DictAttrWrapper({self._data!r})"

    def __str__(self) -> str:
        """String conversion."""
        return str(self._data)

    def __bool__(self) -> bool:
        """Boolean conversion."""
        return bool(self._data)

    def __len__(self) -> int:
        """Support len() for lists and dicts."""
        return len(self._data)

    def __iter__(self):
        """Support iteration for lists and dicts."""
        if isinstance(self._data, list):
            return (self._wrap(item) for item in self._data)
        return iter(self._data)

    @classmethod
    def _wrap(cls, obj: Any) -> Any:
        """Recursively wrap dicts and lists, leave primitives unchanged.

        Note: Objects that already support attribute-style access (like DictProxy
        from data_helpers) are left unwrapped since they already work with eval().
        """
        # Check if object already supports attribute access (like DictProxy)
        # DictProxy and similar objects have __getattr__ and work with eval() already
        if hasattr(obj, "__getattr__") and not isinstance(obj, dict):
            return obj

        if isinstance(obj, dict):
            return cls(obj)
        if isinstance(obj, list):
            return [cls._wrap(item) for item in obj]
        return obj

    @classmethod
    def wrap_context(cls, context: Dict[str, Any]) -> Dict[str, Any]:
        """Wrap all values in a context dict to support dot notation in eval().

        This is a helper method for consistent context wrapping before using eval()
        with user-provided expressions.

        Args:
            context: Dictionary containing variables for eval()

        Returns:
            Dictionary with all values wrapped using DictAttrWrapper
        """
        return {k: cls._wrap(v) for k, v in context.items()}


class TemplateIterationContext:
    """Represents context for template iteration."""

    def __init__(
        self,
        template_set: Dict[str, Any],
        context: Dict[str, Any],
        template_folder: Path,
        output_dir: Path,
    ) -> None:
        self.template_set = template_set
        self.context = context
        self.template_folder = template_folder
        self.output_dir = output_dir
        # Support files object format
        files = template_set.get("files", {})
        self.include_patterns = files.get("include", [])
        self.exclude_patterns = files.get("exclude", [])


class NestedIterationHandler:
    """Handles nested foreach iteration logic."""

    @staticmethod
    def parse_foreach_expression(expression: str) -> Tuple[str, str]:
        """Parse 'var in collection' expression."""
        parts = expression.split(" in ", 1)
        if len(parts) != 2:
            raise BaseGeneratorError(
                f"Invalid foreach expression: '{expression}'\n"
                f"Expected format: 'item in collection' or 'item in collection if condition'\n"
                f"Examples:\n"
                f"  - 'service in services'\n"
                f"  - 'user in users if user.active'\n"
                f"  - 'module in project.modules'"
            )
        return parts[0].strip(), parts[1].strip()

    @staticmethod
    def evaluate_collection(expression: str, context: Dict[str, Any]) -> List[Any]:
        """Safely evaluate collection expression."""
        try:
            result = get_nested_attr_or_key(context, expression)
            if result is not None:
                return list(result)

            # Fallback to eval for complex expressions
            # Wrap context to support dot notation with dict objects (e.g., item.field)
            wrapped_context = DictAttrWrapper.wrap_context(context)
            safe_globals = {"__builtins__": {}}
            result = eval(expression, safe_globals, wrapped_context)  # pylint: disable=eval-used

            # Unwrap the result if it's wrapped
            if isinstance(result, DictAttrWrapper):
                return list(result)
            return list(result)
        except (AttributeError, KeyError, TypeError) as exc:
            # Missing attribute or key in expression
            raise BaseGeneratorError(
                f"Failed to evaluate expression '{expression}': {exc}\n"
                f"Make sure the collection exists in your data and is iterable.\n"
                f"Available top-level keys: {list(context.keys())}"
            ) from exc
        except (SyntaxError, NameError) as exc:
            # Invalid expression syntax
            raise BaseGeneratorError(
                f"Invalid expression syntax '{expression}': {exc}\n" f"Check for typos in variable or collection names."
            ) from exc


class EnhancedTemplateRenderer:
    """Enhanced template renderer with filtering support."""

    def __init__(self, logger) -> None:
        self.logger = logger

    def create_renderer(
        self,
        context: Dict[str, Any],
        filters: Dict[str, Any],
        dry_run: bool = False,
        manual_section_config: Dict[str, str] = None,
    ) -> TemplateRenderer:
        """Create pytemplify renderer with context and filters."""
        return TemplateRenderer(
            context, "", filters=filters, dry_run=dry_run, manual_section_config=manual_section_config
        )

    def render_with_patterns(
        self,
        iteration_context: TemplateIterationContext,
        filters: Dict[str, Any],
        dry_run: bool = False,
        manual_section_config: Dict[str, str] = None,
    ) -> None:
        """Render templates with automatic file filtering."""
        # Get files that should be processed for this iteration context
        filtered_files = self._get_files_for_iteration_context(iteration_context)

        if not filtered_files:
            self.logger.debug(f"No files matched iteration context in " f"{iteration_context.template_folder}")
            return

        renderer = self.create_renderer(iteration_context.context, filters, dry_run, manual_section_config)

        for file_path in filtered_files:
            # Calculate relative path from template folder
            rel_path = file_path.relative_to(iteration_context.template_folder)

            # Render filename template variables if any exist
            rendered_rel_path = renderer.render_string(str(rel_path))

            # Remove foreach prefixes from filename based on iteration context
            cleaned_rel_path = self._remove_foreach_prefixes(rendered_rel_path, iteration_context.context)

            # Determine output file path (remove .j2 extension if present)
            if cleaned_rel_path.endswith(".j2"):
                cleaned_rel_path = cleaned_rel_path[:-3]  # Remove .j2 extension
            output_file = iteration_context.output_dir / cleaned_rel_path

            # Use pytemplify's generate_file for each file
            renderer.generate_file(temp_filepath=str(file_path), output_filepath=str(output_file))

    def _get_files_for_iteration_context(self, iteration_context: TemplateIterationContext) -> Set[Path]:
        """Get files that should be processed for this iteration context."""
        # Get all files in template folder
        all_files = set()
        for file_path in iteration_context.template_folder.rglob("*"):
            if file_path.is_file():
                all_files.add(file_path)

        # Apply include/exclude patterns first if specified
        if iteration_context.include_patterns or iteration_context.exclude_patterns:
            all_files = self._get_filtered_files(
                iteration_context.template_folder,
                iteration_context.include_patterns,
                iteration_context.exclude_patterns,
            )

        # Then apply automatic foreach prefix filtering
        filtered_files = set()
        iteration_vars = self._get_iteration_variables(iteration_context.context)

        for file_path in all_files:
            if self._should_process_file_for_iteration(file_path, iteration_vars):
                filtered_files.add(file_path)

        return filtered_files

    def _get_iteration_variables(self, context: Dict[str, Any]) -> Set[str]:
        """Extract iteration variable names from context."""
        iteration_vars = set()
        # Standard context variables that are not iteration variables
        standard_vars = {"dd", "globals", "gg"}

        for key in context.keys():
            if key not in standard_vars:
                iteration_vars.add(key)

        return iteration_vars

    def _should_process_file_for_iteration(self, file_path: Path, iteration_vars: Set[str]) -> bool:
        """Determine if a file should be processed for the current iteration."""
        filename = file_path.name
        full_path_str = str(file_path)

        # Check for _foreach_ prefix first
        if filename.startswith("_foreach_"):
            # Extract the variable from _foreach_<var>_ prefix
            parts = filename.split("_")
            if len(parts) < 3:
                return True  # Malformed prefix, process it anyway

            foreach_var = parts[2]
            # Only process if the foreach variable is in our current iteration
            return foreach_var in iteration_vars

        # Check if the filename/path contains template variables
        if "{{" in full_path_str and "}}" in full_path_str:
            # Extract template variables from the path
            template_vars = re.findall(r"{{\s*([^}|.\s]+)", full_path_str)

            # If this is a static context (no iteration vars), don't process dynamic templates
            if not iteration_vars:
                return len(template_vars) == 0

            # For iteration contexts, only process if all template vars are available
            for var in template_vars:
                if var not in iteration_vars and var not in {"globals", "gg"}:  # globals/gg is always available
                    return False

        return True

    def _get_filtered_files(
        self,
        template_folder: Path,
        include_patterns: Optional[List[str]],
        exclude_patterns: Optional[List[str]],
    ) -> Set[Path]:
        """Get filtered list of files based on include/exclude patterns."""
        # Get all files in the template folder
        all_files = set()
        for file_path in template_folder.rglob("*"):
            if file_path.is_file():
                all_files.add(file_path)

        if not include_patterns and not exclude_patterns:
            return all_files

        # Create a TemplateSetFilter to reuse existing pattern matching logic
        filter_patterns = TemplateSetFilter(
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
        )

        filtered = set()
        for file_path in all_files:
            filename = file_path.name
            if filter_patterns.should_include(filename):
                filtered.add(file_path)

        return filtered

    def _remove_foreach_prefixes(self, filename: str, context: Dict[str, Any]) -> str:
        """Remove _foreach_{var}_ prefixes where {var} is a known context var."""
        # Convert to Path for easier manipulation
        path = Path(filename)

        # Check if the filename (not the full path) has a foreach prefix
        filename_only = path.name

        # Check for foreach prefixes using exact context variable names
        for var_name in context.keys():
            prefix = f"_foreach_{var_name}_"
            if filename_only.startswith(prefix):
                # Remove the prefix from just the filename part
                cleaned_filename = filename_only[len(prefix) :]
                # Reconstruct the full path with cleaned filename
                return str(path.parent / cleaned_filename)

        # If no known foreach prefix found, return path as-is
        return filename


class TemplateSetFilter:
    """Filters template sets based on include/exclude patterns.

    Delegates to PatternMatcher for the actual matching logic.
    """

    def __init__(
        self,
        include_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
    ) -> None:
        """Initialize the template set filter."""
        self._matcher = PatternMatcher(include_patterns, exclude_patterns)

    def should_include(self, template_name: str) -> bool:
        """Determine if template should be included based on filters."""
        return self._matcher.should_include(template_name)
