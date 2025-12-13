"""Manual section management for template rendering.

This module provides centralized functionality for handling MANUAL SECTION markers
in generated files. Manual sections allow users to preserve hand-written code between
template regenerations.

The ManualSectionManager class provides:
- Extraction of manual sections from content
- Validation of manual section structure and IDs
- Restoration of manual sections into newly generated content
"""

import re
from typing import Dict, List, Optional

from pytemplify.exceptions import ManualSectionError
from pytemplify.logging_utils import StructuredLogger


class RenderContext:  # pylint: disable=too-few-public-methods
    """Context for tracking filename and line number during rendering operations.

    This is a minimal version for use in manual section operations.
    The full RenderContext is defined in renderer.py.
    """

    def __init__(self, filename: str = "", lineno: int = 1):
        self.filename = filename
        self.lineno = lineno

    def update(self, filename: Optional[str] = None, lineno: Optional[int] = None) -> None:
        """Update context with new filename or line number."""
        if filename is not None:
            self.filename = filename
        if lineno is not None:
            self.lineno = lineno


class ManualSectionManager:
    """Manager for manual section preservation in template rendering.

    This class provides a centralized implementation of manual section handling,
    eliminating code duplication between TemplateRenderer and CodeFormatter.

    Manual sections are marked with:
        MANUAL SECTION START: section_id
        ... user content ...
        MANUAL SECTION END

    The manager ensures:
    - Section IDs are valid (alphanumeric, underscore, hyphen only)
    - No duplicate section IDs
    - Proper nesting (no nested sections)
    - Complete structure (matching START/END pairs)
    - Section preservation across regenerations
    """

    # Default pattern constants
    DEFAULT_START_MARKER = "MANUAL SECTION START"
    DEFAULT_END_MARKER = "MANUAL SECTION END"
    MANUAL_SECTION_ID = "[a-zA-Z0-9_-]+"

    def __init__(self, start_marker: str = None, end_marker: str = None):
        """Initialize the manager with optional custom markers.

        Args:
            start_marker: Custom start marker (default: "MANUAL SECTION START")
            end_marker: Custom end marker (default: "MANUAL SECTION END")
        """
        self.start_marker = start_marker or self.DEFAULT_START_MARKER
        self.end_marker = end_marker or self.DEFAULT_END_MARKER

        # Compile regex patterns
        self.manual_section_pattern = re.compile(
            rf"{re.escape(self.start_marker)}: ({self.MANUAL_SECTION_ID}(?:\s|$))(.*?){re.escape(self.end_marker)}",
            re.DOTALL,
        )

        self.manual_section_check_pattern = re.compile(
            rf"{re.escape(self.start_marker)}.*?{re.escape(self.end_marker)}",
            re.DOTALL,
        )

    # For backwards compatibility and class-level access (read-only properties)
    @property
    def MANUAL_SECTION_START(self):  # pylint: disable=invalid-name
        """Return start marker for backwards compatibility."""
        return self.start_marker

    @property
    def MANUAL_SECTION_END(self):  # pylint: disable=invalid-name
        """Return end marker for backwards compatibility."""
        return self.end_marker

    @property
    def MANUAL_SECTION_PATTERN(self):  # pylint: disable=invalid-name
        """Return compiled pattern for backwards compatibility."""
        return self.manual_section_pattern

    @property
    def MANUAL_SECTION_CHECK_PATTERN(self):  # pylint: disable=invalid-name
        """Return compiled check pattern for backwards compatibility."""
        return self.manual_section_check_pattern

    def extract_sections(self, content: str) -> Dict[str, str]:
        """Extract manual sections from content.

        Args:
            content: Content to extract sections from

        Returns:
            Dictionary mapping section IDs to their full section content
            (including markers)
        """
        sections = {}
        for match in self.MANUAL_SECTION_PATTERN.finditer(content):
            section_id = match.group(1).strip()
            # Store the full match (including markers)
            sections[section_id] = match.group(0)
        return sections

    def extract_section_content(self, section_full_content: str) -> str:
        """Extract just the content part from a full section (between markers).

        Args:
            section_full_content: Full section content including markers

        Returns:
            Just the content between START and END markers, with leading/trailing
            whitespace properly handled
        """
        match = self.MANUAL_SECTION_PATTERN.search(section_full_content)
        if match:
            content = match.group(2)
            # Remove leading/trailing newlines but preserve internal formatting
            content = content.strip("\n")
            # Remove trailing empty lines and comment prefixes that are artifacts
            lines = content.split("\n")
            # Remove trailing empty lines
            while lines and lines[-1].strip() == "":
                lines.pop()
            # If the last line is just a comment prefix, remove it
            if lines and lines[-1].strip() in ("#", "//", "/*", "--"):
                lines.pop()
            return "\n".join(lines)
        return ""

    def remove_sections(self, content: str) -> str:
        """Remove all manual sections from content, leaving only markers.

        This removes the content between START and END markers, leaving
        empty sections that can be restored later. This is useful when
        you need to format content without formatting manual sections.

        Args:
            content: Content to remove sections from

        Returns:
            Content with manual section content removed (markers remain)
        """

        def replace_section(match):
            # Keep the markers but remove the content between them
            section_id = match.group(1).strip()
            return f"{self.MANUAL_SECTION_START}: {section_id}\n{self.MANUAL_SECTION_END}"

        return self.MANUAL_SECTION_PATTERN.sub(replace_section, content)

    def restore_sections(self, content: str, sections: Dict[str, str]) -> str:
        """Restore manual sections into content.

        Args:
            content: Content to restore sections into
            sections: Dictionary of section ID to section content (including MANUAL SECTION markers)

        Returns:
            Content with manual sections restored

        Note:
            The sections dictionary values should contain the full section text including
            the MANUAL SECTION START and END markers. The markers should match the format
            expected by MANUAL_SECTION_PATTERN (no comment prefix).

            If you need to preserve comment prefixes or indentation on marker lines,
            use restore_sections_preserve_markers() instead.
        """
        if not sections:
            return content

        result = content
        for section_id, original_section in sections.items():
            # Create pattern that matches the section with any content
            # Important: Include (?:\s|$) after section_id to ensure we match
            # the exact section and not sections with similar names like
            # "foo" matching "foo_bar"
            section_pattern = re.compile(
                rf"{re.escape(self.start_marker)}: "
                rf"{re.escape(section_id)}(?:\s|$).*?"
                rf"{re.escape(self.end_marker)}",
                re.DOTALL,
            )
            # Replace with the original section
            # IMPORTANT: Use lambda with default argument to prevent re.sub() from interpreting
            # backslash sequences in the replacement string (e.g., \\n -> \n)
            # and to avoid cell-var-from-loop issue
            result = section_pattern.sub(lambda m, section=original_section: section, result)

        return result

    def check_section_ids(
        self, content: str, content_name: str = "content", context: Optional[RenderContext] = None
    ) -> List[str]:
        """Check manual section IDs for validity and duplicates.

        Args:
            content: Content to check
            content_name: Name of content for error messages
            context: Render context for error reporting

        Returns:
            List of valid section IDs found

        Raises:
            ManualSectionError: If sections have invalid IDs or duplicates
        """
        filename = context.filename if context else content_name

        # Find all possible sections (may include invalid ones)
        possible_matches = list(self.MANUAL_SECTION_CHECK_PATTERN.finditer(content))
        valid_matches = list(self.MANUAL_SECTION_PATTERN.finditer(content))

        # Check for invalid section IDs
        if len(possible_matches) != len(valid_matches):
            # Find the first invalid section
            bad_match = None
            for match in possible_matches:
                span_text = content[match.start() : match.end()]
                if not self.MANUAL_SECTION_PATTERN.search(span_text):
                    bad_match = match
                    break

            lineno = 1
            if bad_match is not None:
                lineno = content[: bad_match.start()].count("\n") + 1
            if context:
                context.update(lineno=lineno)

            raise ManualSectionError(filename, lineno, f"{content_name} has invalid section")

        # Extract section IDs
        section_ids = [match.group(1).strip() for match in valid_matches]

        # Check for duplicates
        duplicates = {sid for sid in section_ids if section_ids.count(sid) > 1}
        if duplicates:
            # Find first duplicate for error reporting
            dup_id = next(iter(duplicates))
            dup_match = None
            for match in valid_matches:
                if match.group(1).strip() == dup_id:
                    dup_match = match
                    break

            lineno = 1
            if dup_match is not None:
                lineno = content[: dup_match.start()].count("\n") + 1
            if context:
                context.update(lineno=lineno)

            raise ManualSectionError(filename, lineno, f"{content_name} has duplicated id: {duplicates}")

        return section_ids

    def check_section_structure(
        self, content: str, content_name: str = "content", context: Optional[RenderContext] = None
    ) -> None:
        """Check manual section structure for completeness and proper nesting.

        Args:
            content: Content to check
            content_name: Name of content for error messages
            context: Render context for error reporting

        Raises:
            ManualSectionError: If sections are improperly nested or incomplete
        """
        filename = context.filename if context else content_name

        # Check for nested sections
        matches = list(self.MANUAL_SECTION_CHECK_PATTERN.finditer(content))
        for match in matches:
            section = content[match.start() : match.end()]
            start_count_in_section = section.count(self.MANUAL_SECTION_START)
            end_count_in_section = section.count(self.MANUAL_SECTION_END)

            if start_count_in_section > 1 or end_count_in_section > 1:
                lineno = content[: match.start()].count("\n") + 1
                if context:
                    context.update(lineno=lineno)
                raise ManualSectionError(filename, lineno, f"Nested section in {content_name}")

        # Check for matching START/END pairs
        start_count = content.count(self.MANUAL_SECTION_START)
        end_count = content.count(self.MANUAL_SECTION_END)

        if start_count != end_count:
            # Find the position of the unmatched marker
            lineno = 1
            start_positions = [m.start() for m in re.finditer(re.escape(self.MANUAL_SECTION_START), content)]
            end_positions = [m.start() for m in re.finditer(re.escape(self.MANUAL_SECTION_END), content)]

            if start_count > end_count and start_positions:
                lineno = content[: start_positions[-1]].count("\n") + 1
            elif end_count > start_count and end_positions:
                lineno = content[: end_positions[-1]].count("\n") + 1

            if context:
                context.update(lineno=lineno)

            raise ManualSectionError(
                filename,
                lineno,
                f"Incomplete section in {content_name}: start={start_count}, end={end_count}",
            )

    def validate_sections(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        template: str,
        rendered: str,
        previous: str = "",
        context: Optional[RenderContext] = None,
        output_file: Optional[str] = None,
    ) -> None:
        """Validate manual sections across template, rendered, and previous content.

        This performs comprehensive validation including:
        - Structure validation for all content
        - ID validation for rendered and previous content
        - Checking that no sections were lost from previous to current
        - Logging warnings for new manual sections

        Args:
            template: Template string
            rendered: Newly rendered content
            previous: Previously rendered content (optional)
            context: Render context for error reporting
            output_file: Output file path for logging new manual sections (uses context filename if not provided)

        Raises:
            ManualSectionError: If validation fails
        """
        # Validate structure of all content
        self.check_section_structure(template, "template", context)
        self.check_section_structure(rendered, "rendered", context)

        # Validate IDs in rendered content
        curr_ids = self.check_section_ids(rendered, "rendered", context)

        # If there's previous content, validate it and check for lost sections
        if previous:
            self.check_section_structure(previous, "prev_rendered", context)
            prev_ids = self.check_section_ids(previous, "prev_rendered", context)

            # Check for lost sections
            for section_id in prev_ids:
                if section_id not in curr_ids:
                    # Try to locate the missing section for better error reporting
                    # Look in the previous rendered content (output file) for the line number
                    lineno = 1
                    match = re.search(rf"{self.MANUAL_SECTION_START}: {re.escape(section_id)}", previous)
                    if match:
                        lineno = previous[: match.start()].count("\n") + 1
                    else:
                        # Fallback to template location
                        match2 = re.search(rf"{self.MANUAL_SECTION_START}: {re.escape(section_id)}", template)
                        if match2:
                            lineno = template[: match2.start()].count("\n") + 1

                    if context:
                        context.update(lineno=lineno)

                    # Use output_file if provided, otherwise fall back to context filename
                    # This shows where the section was lost (in the output file)
                    filename = output_file if output_file else (context.filename if context else "template")
                    raise ManualSectionError(filename, lineno, f"New template lost manual section: {section_id}")

            # Check for new manual sections (sections in current but not in previous)
            # Only log if previous content exists (legacy file) - don't log for new files
            new_sections = [section_id for section_id in curr_ids if section_id not in prev_ids]
            if new_sections:
                self._log_new_sections(new_sections, rendered, context, output_file)

    def _log_new_sections(
        self,
        section_ids: List[str],
        rendered_content: str,
        context: Optional[RenderContext] = None,
        output_file: Optional[str] = None,
    ) -> None:
        """Log warning messages for newly discovered manual sections with clickable file URIs.

        Args:
            section_ids: List of new section IDs
            rendered_content: Rendered content to search for line numbers
            context: Render context for filename information
            output_file: Output file path to use in logs (overrides context filename)
        """
        # Use output_file if provided, otherwise fall back to context filename
        filename = output_file if output_file else (context.filename if context else "template")

        for section_id in section_ids:
            # Find the line number where this section starts
            lineno = self._find_section_line(rendered_content, section_id)

            # Use centralized structured logger
            StructuredLogger.warning(f"New manual section found: '{section_id}'", file_path=filename, lineno=lineno)

    def _find_section_line(self, content: str, section_id: str) -> int:
        """Find the line number where a manual section starts.

        Args:
            content: Content to search in
            section_id: Section ID to find

        Returns:
            Line number (1-indexed) where the section starts, or 1 if not found
        """
        # Search for the section start marker with the specific ID
        pattern = rf"{re.escape(self.start_marker)}: {re.escape(section_id)}(?:\s|$)"
        match = re.search(pattern, content)

        if match:
            # Count newlines up to the match position
            return content[: match.start()].count("\n") + 1

        return 1  # Default to line 1 if not found

    def replace_section_content(self, content: str, section_id: str, new_content: str) -> str:
        """Replace the content of a section while preserving its marker formatting.

        This function finds a section and replaces only the content between the markers,
        keeping the START and END marker lines exactly as they appear in the original.

        The key insight: we insert content right after the section ID AND any trailing whitespace/newline
        that's part of the START marker line. This way, the backup content (which was captured after
        that whitespace) fits perfectly back.

        Args:
            content: The full file content
            section_id: The section ID to replace
            new_content: The new content to insert (as captured from backup)

        Returns:
            Updated content with the section replaced
        """
        # Find the START marker text - use regex to ensure exact match
        # Important: Match section_id followed by whitespace or end of line to avoid
        # matching "foo" when the actual section is "foo_bar"
        start_pattern = re.compile(rf"{re.escape(self.MANUAL_SECTION_START)}: {re.escape(section_id)}(?=\s|$)")
        start_match = start_pattern.search(content)
        if not start_match:
            return content  # Marker not found

        # Find where the section ID ends (right after the ID, not including any whitespace)
        # Using lookahead (?=\s|$) means the match ends at the section ID, not consuming whitespace
        section_id_end = start_match.end()

        # Skip any trailing whitespace on the START marker line (but not the newline)
        # This matches what the regex captures in group(1): ID + optional trailing space/tab
        while section_id_end < len(content) and content[section_id_end] in (" ", "\t"):
            section_id_end += 1

        # Now skip the newline if present (this is where content insertion starts)
        if section_id_end < len(content) and content[section_id_end] == "\n":
            section_id_end += 1

        # Find END marker after the START marker
        end_marker = self.MANUAL_SECTION_END
        end_idx = content.find(end_marker, section_id_end)
        if end_idx == -1:
            return content  # END marker not found

        # Find the beginning of the line containing END marker (last newline before END marker)
        end_line_start = content.rfind("\n", section_id_end, end_idx)
        if end_line_start == -1:
            # END marker has no newline before it - unusual but handle it
            end_line_start = section_id_end

        # Reconstruct: [before insertion point] + [new_content] + [from END line start onwards]
        result = (
            content[:section_id_end]  # Up to after the newline following section ID
            + new_content  # Content from backup
            + content[end_line_start:]  # From newline before END marker onwards
        )

        return result

    def section_exists(self, content: str, section_id: str) -> bool:
        """Check if a manual section exists in the content.

        Args:
            content: Content to check
            section_id: Section ID to look for

        Returns:
            True if the section exists, False otherwise
        """
        sections = self.extract_sections(content)
        return section_id in sections

    def get_section_content(self, content: str, section_id: str) -> Optional[str]:
        """Get the content of a specific manual section.

        Args:
            content: Content to extract from
            section_id: Section ID to get content for

        Returns:
            The section content (between markers) or None if not found
        """
        sections = self.extract_sections(content)
        if section_id not in sections:
            return None
        full_section = sections[section_id]
        return self.extract_section_content(full_section)
