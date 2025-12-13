"""Command-based formatters that execute external tools.

This module provides formatters that execute external command-line
tools like clang-format, prettier (when not using Python API), etc.
"""

import logging
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional

from pytemplify.formatting.base import CodeFormatter, FormattingError

logger = logging.getLogger(__name__)


class CommandFormatter(CodeFormatter):
    """Formatter that executes external command-line tools.

    This formatter supports formatters that are executed as external commands:
    - clang-format (C/C++)
    - prettier (when using CLI)
    - Custom user-defined formatters
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize the command formatter.

        Args:
            config: Formatter configuration including command template
        """
        self.config = config
        self.command_template = config.get("command", "")
        self.timeout = config.get("timeout", 30)  # Default 30 seconds

        if not self.command_template:
            raise FormattingError("Command template is required for command formatter", "command")

        # For command formatters, we need to determine supported extensions
        # This could be improved by parsing the command or having explicit config
        supported_extensions = config.get("extensions", [".txt"])  # Default fallback

        super().__init__("command", supported_extensions)

        # Validate configuration
        self.validate_options(config.get("options", {}))

    def format(self, content: str, options: Optional[Dict[str, Any]] = None) -> str:
        """Format content by executing an external command.

        Args:
            content: Content to format
            options: Formatter-specific options

        Returns:
            Formatted content

        Raises:
            FormattingError: If command execution fails
        """
        options = options or {}

        try:
            # Create a temporary file for input
            with tempfile.NamedTemporaryFile(mode="w", suffix=".tmp", delete=False) as input_file:
                input_file.write(content)
                input_file_path = input_file.name

            # Create a temporary file for output
            with tempfile.NamedTemporaryFile(mode="w", suffix=".tmp", delete=False) as output_file:
                output_file_path = output_file.name

            try:
                # Prepare the command
                command = self._prepare_command(input_file_path, output_file_path, options)

                # Execute the command
                result = subprocess.run(
                    command,
                    shell=True,  # Allow shell features like pipes
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    cwd=None,  # Use current working directory
                    check=False,  # Don't raise exception on non-zero exit codes
                )

                if result.returncode != 0:
                    error_msg = result.stderr.strip() if result.stderr else "Command failed"
                    raise FormattingError(f"Command execution failed: {error_msg}", self.name)

                # Read the formatted output
                with open(output_file_path, "r", encoding="utf-8") as f:
                    formatted_content = f.read()

                return formatted_content

            finally:
                # Clean up temporary files
                try:
                    Path(input_file_path).unlink(missing_ok=True)
                    Path(output_file_path).unlink(missing_ok=True)
                except (OSError, IOError) as exc:
                    # File system errors during cleanup - log but don't fail
                    logger.warning("Failed to clean up temporary files: %s", exc)

        except subprocess.TimeoutExpired as exc:
            raise FormattingError(f"Command execution timed out after {self.timeout} seconds", self.name) from exc
        except FileNotFoundError as exc:
            raise FormattingError(
                f"Command not found: {exc.filename}. Make sure the formatter is installed", self.name
            ) from exc
        except (OSError, IOError, UnicodeDecodeError) as exc:
            # File system or encoding errors
            raise FormattingError(f"File system error during formatting: {exc}", self.name) from exc
        except subprocess.SubprocessError as exc:
            # Subprocess execution errors
            raise FormattingError(f"Command execution failed: {exc}", self.name) from exc

    def _prepare_command(self, input_path: str, output_path: str, options: Dict[str, Any]) -> str:
        """Prepare the command string with variable substitution.

        Args:
            input_path: Path to input file
            output_path: Path to output file
            options: Formatter options

        Returns:
            Prepared command string
        """
        command = self.command_template

        # Substitute common variables
        replacements = {
            "${input}": input_path,
            "${output}": output_path,
            "${INPUT}": input_path,
            "${OUTPUT}": output_path,
        }

        # Add any additional options from the options dict
        for key, value in options.items():
            if isinstance(value, bool):
                # For boolean options, include the flag if true
                if value:
                    replacements[f"${{{key}}}"] = f"--{key}"
                else:
                    replacements[f"${{{key}}}"] = ""
            else:
                # For other values, substitute directly
                replacements[f"${{{key}}}"] = str(value)

        # Apply replacements
        for placeholder, replacement in replacements.items():
            command = command.replace(placeholder, replacement)

        return command

    def validate_options(self, options: Optional[Dict[str, Any]] = None) -> None:
        """Validate formatter options.

        Args:
            options: Options to validate

        Raises:
            FormattingError: If options are invalid
        """
        super().validate_options(options)

        if options is None:
            return

        # Validate timeout if specified
        if "timeout" in options:
            timeout = options["timeout"]
            if not isinstance(timeout, (int, float)) or timeout <= 0:
                raise FormattingError("timeout must be a positive number", self.name)


# Pre-configured command formatters for common tools


class ClangFormatFormatter(CommandFormatter):
    """Clang-format command formatter for C/C++ files."""

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize clang-format formatter."""
        # Set default command if not provided
        if "command" not in config:
            config["command"] = "clang-format ${input} > ${output}"

        # Set supported extensions
        config["extensions"] = [".c", ".cpp", ".h", ".hpp", ".cc", ".cxx", ".hxx"]

        super().__init__(config)


class PrettierCommandFormatter(CommandFormatter):
    """Prettier command formatter for web files."""

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize prettier command formatter."""
        # Set default command if not provided
        if "command" not in config:
            config["command"] = "prettier --stdin-filepath ${input} < ${input} > ${output}"

        # Set supported extensions
        config["extensions"] = [".js", ".ts", ".jsx", ".tsx", ".json", ".css", ".html", ".md", ".yaml", ".yml"]

        super().__init__(config)


class GoFormatFormatter(CommandFormatter):
    """Go format command formatter."""

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize go format formatter."""
        # Set default command if not provided
        if "command" not in config:
            config["command"] = "gofmt ${input} > ${output}"

        # Set supported extensions
        config["extensions"] = [".go"]

        super().__init__(config)


class RustFormatFormatter(CommandFormatter):
    """Rust format command formatter."""

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize rust format formatter."""
        # Set default command if not provided
        if "command" not in config:
            config["command"] = "rustfmt ${input} > ${output}"

        # Set supported extensions
        config["extensions"] = [".rs"]

        super().__init__(config)
