"""
Validation runner for orchestrating validators.

This module provides the main orchestration logic for running validators,
following SOLID principles:
- SRP: Runner only orchestrates validation workflow
- DIP: Depends on BaseValidator abstraction
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from pytemplify.validation.base import BaseValidator, ValidationResult

logger = logging.getLogger(__name__)


class ValidationRunner:
    """
    Runs validators on generated files (SOLID: SRP - Single Responsibility).

    Responsibilities:
        - Discover targets for each validator
        - Execute validators in sequence
        - Aggregate and report results
        - Handle fail-fast mode
    """

    def __init__(self, validators: List[BaseValidator]):
        """
        Initialize validation runner with validators.

        Args:
            validators: List of validator instances to run
        """
        self.validators = validators
        self._logger = logging.getLogger(f"{__name__}.ValidationRunner")

    def _validate_single_target(
        self, validator: BaseValidator, target: Path, context: Optional[Dict[str, Any]]
    ) -> ValidationResult:
        """
        Validate a single target with a validator.

        Args:
            validator: Validator to use
            target: Target to validate
            context: Optional validation context

        Returns:
            ValidationResult from the validator
        """
        try:
            result = validator.validate(target, context)
            if result.success:
                self._logger.info("  ✅ %s", result.message)
            else:
                self._logger.error("  ❌ %s", result.message)
                if result.details:
                    self._logger.debug("  Details: %s", result.details)
            return result
        except Exception as e:  # pylint: disable=broad-exception-caught
            # Validator raised an exception - catch all to continue validation
            self._logger.error("  ❌ Error validating %s: %s", target.name, e)
            return ValidationResult(
                validator_name=validator.name,
                target_name=target.name,
                success=False,
                message=f"Validation error: {str(e)}",
                file_path=target,
            )

    def _should_stop_validation(self, fail_fast: bool, result: ValidationResult) -> bool:
        """Check if validation should stop based on result and fail_fast flag."""
        if fail_fast and not result.success:
            self._logger.error("Stopping validation (fail_fast=True)")
            return True
        return False

    def run_all(
        self, output_dir: Path, context: Optional[Dict[str, Any]] = None, fail_fast: bool = False
    ) -> Dict[str, List[ValidationResult]]:
        """
        Run all validators on the output directory.

        Args:
            output_dir: Directory containing generated files
            context: Optional context data (e.g., original data dict, helpers)
            fail_fast: Stop on first failure

        Returns:
            Dictionary mapping validator names to their results
        """
        if not output_dir.exists():
            self._logger.error("Output directory does not exist: %s", output_dir)
            return {}

        results: Dict[str, List[ValidationResult]] = {}

        for validator in self.validators:
            if not validator.config.enabled:
                self._logger.info("Skipping disabled validator: %s", validator.name)
                continue

            self._logger.info("Running validator: %s", validator.name)

            try:
                # Discover targets
                targets = validator.discover(output_dir)
                self._logger.info("  Found %d target(s)", len(targets))

                if not targets:
                    self._logger.info("  No targets found for %s", validator.name)
                    results[validator.name] = []
                    continue

                validator_results = []

                # Validate each target
                for target in targets:
                    if not validator.should_validate(target):
                        self._logger.debug("  Skipping %s (filtered out by patterns)", target)
                        continue

                    self._logger.info("  Validating: %s", target.name)
                    result = self._validate_single_target(validator, target, context)
                    validator_results.append(result)

                    if self._should_stop_validation(fail_fast, result):
                        results[validator.name] = validator_results
                        return results

                results[validator.name] = validator_results

            except Exception as e:  # pylint: disable=broad-exception-caught
                # Validator discovery or setup failed
                self._logger.error("Failed to run validator %s: %s", validator.name, e)
                results[validator.name] = [
                    ValidationResult(
                        validator_name=validator.name,
                        target_name="(discovery failed)",
                        success=False,
                        message=f"Validator failed: {str(e)}",
                    )
                ]

                if fail_fast:
                    self._logger.error("Stopping validation (fail_fast=True)")
                    return results

            finally:
                # Cleanup
                try:
                    validator.cleanup(output_dir)
                except Exception as e:  # pylint: disable=broad-exception-caught
                    self._logger.warning("Cleanup failed for %s: %s", validator.name, e)

        return results

    def _print_passed_targets(self, validator_results: List[ValidationResult]) -> None:
        """Print passed targets with coverage info if available."""
        for result in validator_results:
            if result.success and result.details and "Coverage:" in result.details:
                coverage_line = [line for line in result.details.split("\n") if "Coverage:" in line]
                if coverage_line:
                    coverage_info = coverage_line[0].replace("Coverage:", "").strip()
                    target_info = result.file_path.name if result.file_path else result.target_name
                    self._logger.info("  - %s: %s", target_info, coverage_info)

    def _print_failed_targets(self, validator_results: List[ValidationResult]) -> None:
        """Print failed targets with error messages."""
        for result in validator_results:
            if not result.success:
                target_info = result.file_path or result.target_name
                self._logger.error("  - %s: %s", target_info, result.message)

    def print_summary(self, results: Dict[str, List[ValidationResult]]) -> bool:
        """
        Print summary of validation results.

        Args:
            results: Validation results from run_all()

        Returns:
            True if all validations passed, False otherwise
        """
        if not results:
            self._logger.info("No validation results to display")
            return True

        total_targets = sum(len(r) for r in results.values())
        passed = sum(1 for r in results.values() for res in r if res.success)
        failed = total_targets - passed

        # Print separator
        separator = "=" * 60
        self._logger.info("\n%s", separator)
        self._logger.info("VALIDATION SUMMARY")
        self._logger.info("%s", separator)

        # Print results for each validator
        for validator_name, validator_results in results.items():
            if not validator_results:
                self._logger.info("%s: ⚠️  NO TARGETS", validator_name)
                continue

            validator_passed = sum(1 for r in validator_results if r.success)
            validator_failed = len(validator_results) - validator_passed

            status = "✅ PASSED" if validator_failed == 0 else "❌ FAILED"
            self._logger.info(
                "%s: %s (%d/%d)",
                validator_name,
                status,
                validator_passed,
                len(validator_results),
            )

            # Show passed targets with coverage (if available)
            if validator_passed > 0:
                self._print_passed_targets(validator_results)

            # Show failed targets
            if validator_failed > 0:
                self._print_failed_targets(validator_results)

        # Print overall summary
        self._logger.info("%s", separator)
        overall_status = "✅ ALL PASSED" if failed == 0 else f"❌ {failed} FAILED"
        self._logger.info(
            "Total: %d/%d validations passed - %s",
            passed,
            total_targets,
            overall_status,
        )
        self._logger.info("%s", separator)

        return failed == 0

    def export_results(self, results: Dict[str, List[ValidationResult]], output_file: Path) -> None:
        """
        Export validation results to JSON file.

        Args:
            results: Validation results from run_all()
            output_file: Path to output JSON file
        """
        import json  # pylint: disable=import-outside-toplevel

        export_data = {
            "summary": {
                "total_validators": len(results),
                "total_targets": sum(len(r) for r in results.values()),
                "passed": sum(1 for r in results.values() for res in r if res.success),
                "failed": sum(1 for r in results.values() for res in r if not res.success),
            },
            "results": {
                validator_name: [result.to_dict() for result in validator_results]
                for validator_name, validator_results in results.items()
            },
        }

        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2)

        self._logger.info("Results exported to: %s", output_file)
