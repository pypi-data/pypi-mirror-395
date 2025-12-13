"""
Base classes for validation framework.

This module provides the foundation for all validators in pytemplify,
following SOLID principles for extensibility and maintainability.
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, Dict, List, Optional


class ValidatorType(Enum):
    """Types of validators (extensible)."""

    GTEST = "gtest"
    JSON_SCHEMA = "json_schema"
    FILE_STRUCTURE = "file_structure"
    CUSTOM = "custom"


@dataclass
class ValidationResult:  # pylint: disable=too-many-instance-attributes
    """
    Immutable result of a validation run (SOLID: SRP - Single Responsibility).

    Attributes:
        validator_name: Name of the validator that produced this result
        target_name: Name of the target that was validated
        success: Whether validation passed
        message: Human-readable message about the result
        details: Optional detailed information (e.g., full output)
        file_path: Optional path to the validated file
        errors: List of error messages
        warnings: List of non-fatal warning messages
        duration_seconds: Time taken for validation
    """

    validator_name: str
    target_name: str
    success: bool
    message: str
    details: Optional[str] = None
    file_path: Optional[Path] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    duration_seconds: float = 0.0

    def __str__(self) -> str:
        """Human-readable string representation."""
        status = "✅ PASSED" if self.success else "❌ FAILED"
        return f"{status}: {self.target_name} - {self.message}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary for JSON serialization.

        Returns:
            Dictionary representation of the result
        """
        return {
            "validator": self.validator_name,
            "target": self.target_name,
            "success": self.success,
            "message": self.message,
            "details": self.details,
            "file_path": str(self.file_path) if self.file_path else None,
            "errors": self.errors,
            "warnings": self.warnings,
            "duration_seconds": self.duration_seconds,
        }


@dataclass
class ValidatorConfig:
    """
    Configuration for a validator (immutable after creation).

    Attributes:
        name: Unique name for this validator instance
        type: Type of validator (gtest, json_schema, etc.)
        enabled: Whether this validator is enabled
        patterns: File/test patterns to match (glob or regex)
        options: Validator-specific options
    """

    name: str
    type: ValidatorType
    enabled: bool = True
    patterns: List[str] = field(default_factory=list)
    options: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.name:
            raise ValueError("Validator name cannot be empty")
        if not isinstance(self.type, ValidatorType):
            raise TypeError(f"type must be ValidatorType, got {type(self.type)}")


class BaseValidator(ABC):
    """
    Base class for all validators (SOLID: SRP, OCP).

    This abstract base class defines the interface that all validators must implement.
    It follows the Open/Closed Principle - open for extension (new validators can be
    added) but closed for modification (this interface remains stable).

    Responsibilities:
        - Define validator interface
        - Provide common validation utilities
        - Handle pattern matching (DRY: reuses PatternMatcher)

    Extension Points:
        - discover(): Find targets to validate
        - validate(): Perform validation
        - cleanup(): Clean up resources
    """

    def __init__(self, config: ValidatorConfig):
        """
        Initialize validator with configuration.

        Args:
            config: Validator configuration

        Raises:
            ValueError: If configuration is invalid
        """
        self.config = config
        self.name = config.name
        self._logger = self._create_logger()

    def _create_logger(self) -> logging.Logger:
        """
        Create logger for this validator (DRY: centralized logging).

        Returns:
            Logger instance
        """
        return logging.getLogger(f"pytemplify.validation.{self.name}")

    @abstractmethod
    def discover(self, output_dir: Path) -> List[Path]:
        """
        Discover files/tests to validate in the output directory.

        Args:
            output_dir: Directory where files were generated

        Returns:
            List of paths to validate

        Raises:
            Exception: If discovery fails critically
        """

    @abstractmethod
    def validate(self, target: Path, context: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """
        Validate a single target (file, test, directory).

        Args:
            target: Path to the target to validate
            context: Optional context data (e.g., original data dict, helpers)

        Returns:
            ValidationResult with success status and details

        Raises:
            Exception: If validation fails critically (not test failure)
        """

    def should_validate(self, target: Path) -> bool:
        """
        Check if this validator should validate the given target.

        DRY: Reuses existing PatternMatcher logic for pattern matching.

        Args:
            target: Path to check

        Returns:
            True if validator should process this target
        """
        if not self.config.patterns:
            return True

        # Reuse existing pattern matching (DRY principle)
        # pylint: disable=import-outside-toplevel
        from pytemplify.pattern_matcher import PatternMatcher

        matcher = PatternMatcher(include_patterns=self.config.patterns, exclude_patterns=[])
        # Support simple filenames and path-aware globs (e.g., **/tests/test_auth.cpp)
        if matcher.should_include(target.name) or matcher.should_include(target.as_posix()):
            return True

        return any(
            self._match_path_glob(target, pattern)
            for pattern in self.config.patterns
            if "/" in pattern and not pattern.startswith("regex:")
        )

    @staticmethod
    def _match_path_glob(target: Path, pattern: str) -> bool:
        """
        Match a glob containing path separators by treating pattern segments as an ordered subsequence.

        This makes '**/foo/bar.cpp' match '/tmp/a/foo/baz/bar.cpp' while still respecting
        glob semantics for each individual segment.
        """
        path_parts = [part for part in target.parts if part]
        pattern_parts = [part for part in pattern.split("/") if part and part != "**"]

        path_index = 0
        for part in pattern_parts:
            while path_index < len(path_parts) and not fnmatch(path_parts[path_index], part):
                path_index += 1
            if path_index == len(path_parts):
                return False
            path_index += 1

        return True

    @abstractmethod
    def cleanup(self, output_dir: Path) -> None:
        """
        Clean up any temporary files created during validation.

        Args:
            output_dir: Directory where validation was run
        """

    def get_option(self, key: str, default: Any = None) -> Any:
        """
        Get validator option with default fallback (convenience method).

        Args:
            key: Option key
            default: Default value if key not found

        Returns:
            Option value or default
        """
        return self.config.options.get(key, default)

    def create_success_result(  # pylint: disable=too-many-arguments
        self, *, target_name: str, message: str, details: str, file_path: Path, duration_seconds: float
    ) -> ValidationResult:
        """
        Create a success ValidationResult (DRY: common pattern).

        Note: This method intentionally takes multiple arguments to match
        the ValidationResult constructor signature for successful validations.

        Args:
            target_name: Name of the validated target
            message: Success message
            details: Detailed information
            file_path: Path to validated file
            duration_seconds: Validation duration

        Returns:
            ValidationResult indicating success
        """
        return ValidationResult(
            validator_name=self.config.name,
            target_name=target_name,
            success=True,
            message=message,
            details=details,
            file_path=file_path,
            duration_seconds=duration_seconds,
        )


class ValidationError(Exception):
    """
    Exception raised when validation fails critically.

    This is for validation system errors, not for test failures.
    Test failures should be reported via ValidationResult with success=False.
    """

    def __init__(self, message: str, validator_name: str = "", target: Optional[Path] = None):
        """
        Initialize validation error.

        Args:
            message: Error message
            validator_name: Name of validator that raised the error
            target: Optional target that caused the error
        """
        self.validator_name = validator_name
        self.target = target

        full_message = message
        if validator_name:
            full_message = f"[{validator_name}] {message}"
        if target:
            full_message = f"{full_message} (target: {target})"

        super().__init__(full_message)
