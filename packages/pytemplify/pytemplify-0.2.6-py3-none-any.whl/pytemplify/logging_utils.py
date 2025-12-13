"""Centralized logging utilities with colored output and clickable file URIs.

This module provides consistent logging utilities across the pytemplify package,
using the colorama library for cross-platform colored output with automatic initialization.
"""

import logging
import os
import sys
from enum import Enum
from pathlib import Path
from typing import Callable, Optional

from colorama import Fore, Style, init

from pytemplify.file_uri_utils import FileUriBuilder

# Initialize colorama for cross-platform colored output
# strip=None means auto-detect: colors on TTY, strip on pipes
# autoreset=False means we control resets ourselves
# Respect FORCE_COLOR for stripping (if forced, don't strip even if not TTY)
_strip = False if os.environ.get("FORCE_COLOR") else None
init(autoreset=False, strip=_strip)


def _colors_enabled() -> bool:
    """Check if colored output should be enabled.

    Returns:
        True if colors should be enabled, False otherwise
    """
    # Respect NO_COLOR environment variable (https://no-color.org/)
    if os.environ.get("NO_COLOR"):
        return False

    # FORCE_COLOR overrides detection
    if os.environ.get("FORCE_COLOR"):
        return True

    # Check if stdout is a TTY
    if hasattr(sys.stdout, "isatty") and sys.stdout.isatty():
        return True

    return False


# Determine if we should use colors
COLORS_ENABLED = _colors_enabled()


def configure_logging(
    level: int = logging.WARNING,
    format_string: Optional[str] = None,
    logger: Optional[logging.Logger] = None,
) -> None:
    """Configure logging for pytemplify with sensible defaults.

    Args:
        level: Logging level (default: WARNING)
        format_string: Custom format string (default: simple format)
        logger: Optional logger to configure. If None, configures the root logger.
    """
    # Use ColoredFormatter for the handler
    handler = logging.StreamHandler()
    handler.setFormatter(ColoredFormatter(fmt=format_string))

    # Configure target logger
    target_logger = logger or logging.getLogger()
    target_logger.setLevel(level)

    # Remove existing handlers to avoid duplicates
    if target_logger.handlers:
        for existing_handler in target_logger.handlers[:]:
            target_logger.removeHandler(existing_handler)

    target_logger.addHandler(handler)


class ColoredFormatter(logging.Formatter):
    """Custom formatter for colored log output."""

    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None):
        # Default format if none provided - simple format without timestamp
        fmt = fmt or "%(levelname)s - %(message)s"
        super().__init__(fmt, datefmt)

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with colors."""
        orig_msg = record.msg
        orig_levelname = record.levelname

        if COLORS_ENABLED:
            # Colorize level name
            color = self._get_level_color(record.levelno)
            record.levelname = f"{color}{Style.BRIGHT}{record.levelname}{Style.RESET_ALL}"

            # If the message comes from StructuredLogger, it might already have colors/structure
            # But standard logs need coloring. We'll color the message too for standard consistency.
            if (
                not isinstance(record.msg, str)
                or not record.msg.startswith(Fore.RED)
                and not record.msg.startswith(Fore.YELLOW)
            ):
                # For standard logs, color the message same as level
                record.msg = f"{color}{record.msg}{Style.RESET_ALL}"

        # Use super's formatting
        # Default format is ensured in __init__
        result = super().format(record)

        # Restore original info to avoid side effects
        record.msg = orig_msg
        record.levelname = orig_levelname

        return result

    def _get_level_color(self, levelno: int) -> str:
        """Get color for log level."""
        if levelno >= logging.ERROR:
            return Fore.RED
        if levelno >= logging.WARNING:
            return Fore.YELLOW
        if levelno >= logging.INFO:
            return Fore.CYAN
        if levelno >= logging.DEBUG:
            return Fore.MAGENTA
        return Fore.WHITE


class LogLevel(Enum):
    """Log levels with associated colors and logging functions."""

    WARNING: tuple[str, str, Callable] = ("WARNING", Fore.YELLOW, logging.warning)
    ERROR: tuple[str, str, Callable] = ("ERROR", Fore.RED, logging.error)
    INFO: tuple[str, str, Callable] = ("INFO", Fore.CYAN, logging.info)
    SUCCESS: tuple[str, str, Callable] = ("SUCCESS", Fore.GREEN, logging.info)

    def __init__(self, label: str, color: str, log_func: Callable):
        self.label = label
        self.color = color
        self.log_func = log_func


class StructuredLogger:
    """Logger that provides structured, colored output with clickable file URIs.

    This logger follows the Single Responsibility Principle by focusing solely on
    formatting and logging messages with optional file location information.

    Thread-safety: This module uses Python's standard logging which is thread-safe.
    However, colorama initialization is global and should be called once at startup.

    Example output:
        [WARNING] New manual section found: 'my_section'
            ↳ file:///path/to/file.cpp:42

        [ERROR] Template validation failed
            ↳ file:///path/to/template.j2:15
    """

    @staticmethod
    def log(level: LogLevel, message: str, file_path: Optional[str] = None, lineno: Optional[int] = None) -> None:
        """Log a message at the specified level with optional file URI.

        This is the core method that all other logging methods delegate to (DRY principle).

        Args:
            level: Log level enum value
            message: Log message
            file_path: Optional file path for clickable URI
            lineno: Optional line number
        """
        formatted_msg = StructuredLogger._format_message(level, message)

        if file_path:
            file_uri = StructuredLogger._create_file_uri(file_path, lineno)
            formatted_msg += f"\n    ↳ {file_uri}"

        level.log_func(formatted_msg)

    @staticmethod
    def warning(message: str, file_path: Optional[str] = None, lineno: Optional[int] = None) -> None:
        """Log a warning message with optional file URI.

        Args:
            message: Warning message
            file_path: Optional file path for clickable URI
            lineno: Optional line number
        """
        StructuredLogger.log(LogLevel.WARNING, message, file_path, lineno)

    @staticmethod
    def error(message: str, file_path: Optional[str] = None, lineno: Optional[int] = None) -> None:
        """Log an error message with optional file URI.

        Args:
            message: Error message
            file_path: Optional file path for clickable URI
            lineno: Optional line number
        """
        StructuredLogger.log(LogLevel.ERROR, message, file_path, lineno)

    @staticmethod
    def info(message: str, file_path: Optional[str] = None, lineno: Optional[int] = None) -> None:
        """Log an info message with optional file URI.

        Args:
            message: Info message
            file_path: Optional file path for clickable URI
            lineno: Optional line number
        """
        StructuredLogger.log(LogLevel.INFO, message, file_path, lineno)

    @staticmethod
    def success(message: str, file_path: Optional[str] = None, lineno: Optional[int] = None) -> None:
        """Log a success message with optional file URI.

        Args:
            message: Success message
            file_path: Optional file path for clickable URI
            lineno: Optional line number
        """
        StructuredLogger.log(LogLevel.SUCCESS, message, file_path, lineno)

    @staticmethod
    def _format_message(level: LogLevel, message: str) -> str:
        """Format a message with color based on log level.

        Args:
            level: Log level enum value
            message: Message to format

        Returns:
            Formatted message string with or without colors
        """
        if COLORS_ENABLED:
            return (
                f"{level.color}{Style.BRIGHT}[{level.label}]{Style.RESET_ALL} "
                f"{level.color}{message}{Style.RESET_ALL}"
            )
        return f"[{level.label}] {message}"

    @staticmethod
    def _create_file_uri(file_path: str, lineno: Optional[int]) -> str:
        """Create a clickable file URI.

        Args:
            file_path: File path
            lineno: Optional line number

        Returns:
            Clickable file URI or plain filename if URI creation fails
        """
        # Don't create URIs for inline templates or special names
        if not file_path or file_path.startswith(("Inline", "template", "<")):
            return file_path

        try:
            # Try to create a proper file URI
            path = Path(file_path)
            # Only create URIs for absolute paths if possible, but FileUriBuilder handles resolving
            return FileUriBuilder.create_uri(path, lineno)
        except (ValueError, OSError, TypeError) as e:
            # Log debug message for troubleshooting
            logging.debug("Failed to create URI for %s: %s", file_path, e)
            if lineno:
                return f"{file_path}:{lineno}"
            return file_path


def create_file_uri(file_path: str, lineno: Optional[int] = None) -> str:
    """Create a clickable file URI for logging and error messages.

    This is a convenience function that can be used independently.

    Args:
        file_path: File path
        lineno: Optional line number

    Returns:
        Clickable file URI string
    """
    return StructuredLogger._create_file_uri(file_path, lineno)  # pylint: disable=protected-access
