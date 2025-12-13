"""
File structure validator for pytemplify.

This validator checks that generated files and directories match expected
structure and content requirements.

SOLID Principles:
    - SRP: Single responsibility - validate file structure
    - OCP: Open for extension through rules
    - LSP: Substitutable for BaseValidator
    - DIP: Depends on abstractions (BaseValidator)

DRY Principle:
    - Reuses BaseValidator pattern matching logic
    - Reuses existing file reading utilities
"""

import logging
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from pytemplify.validation.base import BaseValidator, ValidationResult

logger = logging.getLogger(__name__)


class FileStructureValidator(BaseValidator):  # pylint: disable=too-many-instance-attributes
    """
    Validates file structure and content requirements (SOLID: SRP, LSP).

    Responsibilities:
        - Check required files exist
        - Check forbidden files don't exist
        - Validate file content patterns
        - Validate directory structure
        - Check file permissions (optional)

    DRY: Reuses BaseValidator pattern matching logic.
    """

    def __init__(self, config):
        """
        Initialize File Structure validator.

        Args:
            config: ValidatorConfig instance

        Options supported:
            - required_files: List of required file patterns (glob)
            - forbidden_files: List of forbidden file patterns (glob)
            - required_dirs: List of required directory patterns
            - forbidden_dirs: List of forbidden directory patterns
            - content_rules: Dict mapping file patterns to content requirements
              Example: {"*.cpp": {"must_contain": ["#include"], "must_not_contain": ["TODO"]}}
            - check_empty_files: Warn about empty files (default: True)
            - check_permissions: Check file permissions (default: False)
            - required_permissions: Dict mapping file patterns to required permissions (e.g., {"*.sh": "755"})
        """
        super().__init__(config)

        # Extract configuration
        self._required_files = self.config.options.get("required_files", [])
        self._forbidden_files = self.config.options.get("forbidden_files", [])
        self._required_dirs = self.config.options.get("required_dirs", [])
        self._forbidden_dirs = self.config.options.get("forbidden_dirs", [])
        self._content_rules = self.config.options.get("content_rules", {})
        self._check_empty_files = self.config.options.get("check_empty_files", True)
        self._check_permissions = self.config.options.get("check_permissions", False)
        self._required_permissions = self.config.options.get("required_permissions", {})

    def discover(self, output_dir: Path) -> List[Path]:
        """
        Discover output directory for structure validation.

        For file structure validation, we validate the entire directory,
        so we return the output_dir itself as the single target.

        Args:
            output_dir: Directory to validate

        Returns:
            List containing the output directory
        """
        self._logger.info("Preparing to validate file structure in %s", output_dir)
        return [output_dir]

    def _run_all_checks(self, target: Path) -> tuple[List[str], List[str]]:
        """
        Run all validation checks and collect errors and warnings.

        Args:
            target: Directory to validate

        Returns:
            Tuple of (errors, warnings)
        """
        errors: List[str] = []
        warnings: List[str] = []

        # Check required files
        if self._required_files:
            missing_files = self._check_required_files(target)
            errors.extend([f"Missing required file: {f}" for f in missing_files])

        # Check forbidden files
        if self._forbidden_files:
            forbidden_found = self._check_forbidden_files(target)
            errors.extend([f"Forbidden file found: {f}" for f in forbidden_found])

        # Check required directories
        if self._required_dirs:
            missing_dirs = self._check_required_directories(target)
            errors.extend([f"Missing required directory: {d}" for d in missing_dirs])

        # Check forbidden directories
        if self._forbidden_dirs:
            forbidden_dirs_found = self._check_forbidden_directories(target)
            errors.extend([f"Forbidden directory found: {d}" for d in forbidden_dirs_found])

        # Check content rules
        if self._content_rules:
            content_errors = self._check_content_rules(target)
            errors.extend(content_errors)

        # Check empty files
        if self._check_empty_files:
            empty_files = self._find_empty_files(target)
            if empty_files:
                warnings.extend([f"Empty file: {f}" for f in empty_files])

        # Check permissions
        if self._check_permissions and self._required_permissions:
            permission_errors = self._check_file_permissions(target)
            errors.extend(permission_errors)

        return errors, warnings

    def _format_validation_details(self, duration: float, warnings: List[str]) -> str:
        """Format validation details with duration and warnings."""
        details = f"Validated in {duration:.3f}s"
        if warnings:
            warning_list = "\n".join([f"  - {w}" for w in warnings])
            details += f"\nWarnings ({len(warnings)}):\n{warning_list}"
        return details

    def validate(self, target: Path, context: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """
        Validate the file structure of the target directory.

        Args:
            target: Directory path to validate
            context: Optional context (unused for file structure validation)

        Returns:
            ValidationResult with validation results
        """
        _ = context  # Unused but part of interface
        start_time = time.time()
        dir_name = target.name if target.name else str(target)

        self._logger.info("Validating file structure: %s", dir_name)

        try:
            # Run all validation checks
            errors, warnings = self._run_all_checks(target)
            duration = time.time() - start_time

            # Build result
            if not errors:
                message = f"File structure validation passed for '{dir_name}'"
                details = self._format_validation_details(duration, warnings)
                return self.create_success_result(
                    target_name=dir_name, message=message, details=details, file_path=target, duration_seconds=duration
                )

            # Failure case
            error_details = "\n".join([f"  - {err}" for err in errors])
            if warnings:
                warning_list = "\n".join([f"  - {w}" for w in warnings])
                error_details += f"\n\nWarnings ({len(warnings)}):\n{warning_list}"

            return ValidationResult(
                validator_name=self.config.name,
                target_name=dir_name,
                success=False,
                message=f"File structure validation failed for '{dir_name}'",
                details=f"Errors ({len(errors)}):\n{error_details}",
                file_path=target,
                errors=errors,
                duration_seconds=duration,
            )

        except Exception as e:  # pylint: disable=broad-exception-caught
            duration = time.time() - start_time
            self._logger.error("Validation failed for %s: %s", dir_name, e)
            return ValidationResult(
                validator_name=self.config.name,
                target_name=dir_name,
                success=False,
                message=f"Validation error for '{dir_name}'",
                details=str(e),
                file_path=target,
                errors=[str(e)],
                duration_seconds=duration,
            )

    def _check_required_files(self, directory: Path) -> List[str]:
        """
        Check that all required files exist.

        Args:
            directory: Directory to check

        Returns:
            List of missing required file patterns
        """
        missing = []
        for pattern in self._required_files:
            matches = list(directory.rglob(pattern))
            if not matches:
                missing.append(pattern)
        return missing

    def _check_forbidden_files(self, directory: Path) -> List[str]:
        """
        Check that no forbidden files exist.

        Args:
            directory: Directory to check

        Returns:
            List of found forbidden file paths (relative to directory)
        """
        found = []
        for pattern in self._forbidden_files:
            matches = list(directory.rglob(pattern))
            for match in matches:
                try:
                    rel_path = match.relative_to(directory)
                    found.append(str(rel_path))
                except ValueError:
                    found.append(str(match))
        return found

    def _check_required_directories(self, directory: Path) -> List[str]:
        """
        Check that all required directories exist.

        Args:
            directory: Directory to check

        Returns:
            List of missing required directory patterns
        """
        missing = []
        for pattern in self._required_dirs:
            # Handle simple patterns (no wildcards)
            if "*" not in pattern:
                dir_path = directory / pattern
                if not dir_path.exists() or not dir_path.is_dir():
                    missing.append(pattern)
            else:
                # Handle glob patterns
                matches = [p for p in directory.rglob(pattern) if p.is_dir()]
                if not matches:
                    missing.append(pattern)
        return missing

    def _check_forbidden_directories(self, directory: Path) -> List[str]:
        """
        Check that no forbidden directories exist.

        Args:
            directory: Directory to check

        Returns:
            List of found forbidden directory paths (relative to directory)
        """
        found = []
        for pattern in self._forbidden_dirs:
            # Handle simple patterns (no wildcards)
            if "*" not in pattern:
                dir_path = directory / pattern
                if dir_path.exists() and dir_path.is_dir():
                    found.append(pattern)
            else:
                # Handle glob patterns
                matches = [p for p in directory.rglob(pattern) if p.is_dir()]
                for match in matches:
                    try:
                        rel_path = match.relative_to(directory)
                        found.append(str(rel_path))
                    except ValueError:
                        found.append(str(match))
        return found

    def _check_content_rules(self, directory: Path) -> List[str]:  # pylint: disable=too-many-branches
        """
        Check content rules for files.

        Args:
            directory: Directory to check

        Returns:
            List of content rule violations
        """
        errors = []

        for file_pattern, rules in self._content_rules.items():
            matching_files = list(directory.rglob(file_pattern))

            for file_path in matching_files:
                if not file_path.is_file():
                    continue

                try:
                    content = file_path.read_text(encoding="utf-8")
                except Exception as e:  # pylint: disable=broad-exception-caught
                    errors.append(f"Failed to read {file_path.name}: {e}")
                    continue

                # Check must_contain rules
                for must_contain in rules.get("must_contain", []):
                    if isinstance(must_contain, str):
                        # Simple string match
                        if must_contain not in content:
                            errors.append(f"{file_path.name}: Missing required content '{must_contain}'")
                    elif isinstance(must_contain, dict) and "regex" in must_contain:
                        # Regex match
                        pattern = must_contain["regex"]
                        if not re.search(pattern, content):
                            errors.append(f"{file_path.name}: Missing required pattern '{pattern}'")

                # Check must_not_contain rules
                for must_not_contain in rules.get("must_not_contain", []):
                    if isinstance(must_not_contain, str):
                        # Simple string match
                        if must_not_contain in content:
                            errors.append(f"{file_path.name}: Contains forbidden content '{must_not_contain}'")
                    elif isinstance(must_not_contain, dict) and "regex" in must_not_contain:
                        # Regex match
                        pattern = must_not_contain["regex"]
                        if re.search(pattern, content):
                            errors.append(f"{file_path.name}: Contains forbidden pattern '{pattern}'")

        return errors

    def _find_empty_files(self, directory: Path) -> List[str]:
        """
        Find empty files in directory.

        Args:
            directory: Directory to check

        Returns:
            List of empty file paths (relative to directory)
        """
        empty_files = []

        for file_path in directory.rglob("*"):
            if file_path.is_file() and file_path.stat().st_size == 0:
                try:
                    rel_path = file_path.relative_to(directory)
                    empty_files.append(str(rel_path))
                except ValueError:
                    empty_files.append(str(file_path))

        return empty_files

    def _check_file_permissions(self, directory: Path) -> List[str]:
        """
        Check file permissions match requirements.

        Args:
            directory: Directory to check

        Returns:
            List of permission violations
        """
        errors = []

        for file_pattern, required_perms in self._required_permissions.items():
            matching_files = list(directory.rglob(file_pattern))

            for file_path in matching_files:
                if not file_path.is_file():
                    continue

                try:
                    # Get file permissions (octal)
                    import stat  # pylint: disable=import-outside-toplevel

                    file_perms = oct(stat.S_IMODE(file_path.stat().st_mode))[-3:]

                    # Compare with required permissions
                    if file_perms != required_perms:
                        errors.append(
                            f"{file_path.name}: Incorrect permissions {file_perms}, " f"expected {required_perms}"
                        )
                except Exception as e:  # pylint: disable=broad-exception-caught
                    errors.append(f"{file_path.name}: Failed to check permissions: {e}")

        return errors

    def cleanup(self, output_dir: Path) -> None:
        """
        Clean up validation artifacts.

        File structure validation doesn't create artifacts, so this is a no-op.

        Args:
            output_dir: Directory where validation was run
        """
        # No cleanup needed for file structure validation
