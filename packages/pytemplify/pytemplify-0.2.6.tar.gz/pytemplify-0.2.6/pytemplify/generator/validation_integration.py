"""Validation integration for code generators.

This module handles the integration between code generators and the validation
framework, avoiding circular dependencies and keeping the base generator focused
on core generation functionality.
"""

import logging
from pathlib import Path
from typing import Any, Dict, Optional, Set

from pytemplify.exceptions import ValidationError

logger = logging.getLogger(__name__)


class ValidationIntegration:
    """Handles validation integration for code generators.

    This class encapsulates all validation-related logic to keep the
    BaseCodeGenerator focused on core generation functionality.
    """

    def __init__(self, generator_logger: logging.Logger):
        """Initialize validation integration.

        Args:
            generator_logger: Logger from the parent generator
        """
        self.logger = generator_logger

    def should_run_validation(
        self,
        run_validation: Optional[bool],
        validation_config: Optional[Dict[str, Any]],
    ) -> bool:
        """Determine if validation should run.

        Args:
            run_validation: Override for validation (None=use YAML config)
            validation_config: Validation config from YAML

        Returns:
            True if validation should run
        """
        should_validate = run_validation
        if should_validate is None and validation_config:
            should_validate = validation_config.get("enabled", False)

        return bool(should_validate and validation_config)

    def run_validators(
        self,
        validators,
        output_directories: Set[Path],
        fail_fast: bool,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Run validators on all output directories.

        Args:
            validators: List of validator instances
            output_directories: Directories to validate
            fail_fast: Stop on first failure
            context: Template context

        Returns:
            Dictionary of validation results
        """
        # pylint: disable=import-outside-toplevel
        from pytemplify.validation import ValidationRunner

        runner = ValidationRunner(validators)
        all_results = {}

        for output_dir in output_directories:
            self.logger.info("Validating directory: %s", output_dir)
            results = runner.run_all(output_dir, context=context, fail_fast=fail_fast)
            # Merge results
            for validator_name, validator_results in results.items():
                if validator_name not in all_results:
                    all_results[validator_name] = []
                all_results[validator_name].extend(validator_results)

        return all_results

    def _get_validation_config(self, template_config) -> Optional[Dict[str, Any]]:
        """Extract validation configuration from template config.

        Args:
            template_config: Template configuration object

        Returns:
            Validation config dictionary or None
        """
        if not template_config or not hasattr(template_config, "yaml_data"):
            return None
        return template_config.yaml_data.get("validation")

    def _log_validation_header(self) -> None:
        """Log validation header."""
        separator = "=" * 60
        self.logger.info("\n%s", separator)
        self.logger.info("Running validation...")
        self.logger.info("%s", separator)

    def run_validation_if_configured(  # pylint: disable=too-many-arguments
        self,
        template_config,
        output_directories: Set[Path],
        *,
        run_validation: Optional[bool],
        fail_fast_validation: Optional[bool],
        context: Dict[str, Any],
    ) -> None:
        """Run validation if configured in templates.yaml.

        Args:
            template_config: Template configuration object
            output_directories: Set of directories where files were generated
            run_validation: Override for validation (None=use YAML config)
            fail_fast_validation: Stop on first failure
            context: Template context (for validators that need it)

        Raises:
            ValidationError: If validation fails
        """
        # Import validation here to avoid circular imports
        try:
            # pylint: disable=import-outside-toplevel,cyclic-import
            from pytemplify.validation import ValidationRunner, create_validators_from_config
        except ImportError:
            # Validation not available
            if run_validation:
                self.logger.warning("Validation requested but validation module not available")
            return

        # Get validation configuration
        validation_config = self._get_validation_config(template_config)

        # Determine if we should run validation
        if not self.should_run_validation(run_validation, validation_config):
            return

        # Use actual output directories from generation
        if not output_directories:
            self.logger.warning("No output directories found - skipping validation")
            return

        self._log_validation_header()

        try:
            # Create validators from config
            validators = create_validators_from_config(validation_config)

            if not validators:
                self.logger.warning("No validators configured or all disabled")
                return

            # Determine fail_fast setting
            fail_fast = (
                fail_fast_validation if fail_fast_validation is not None else validation_config.get("fail_fast", False)
            )

            # Run validation on all output directories
            all_results = self.run_validators(validators, output_directories, fail_fast, context)

            # Print summary
            runner = ValidationRunner(validators)
            success = runner.print_summary(all_results)

            if not success:
                self.logger.error("\nValidation failed!")
                raise ValidationError("Validation failed")

            self.logger.info("\nValidation passed! ✓")

        except Exception as exc:
            if isinstance(exc, ValidationError):
                raise
            self.logger.error("Validation error: %s", exc)
            raise ValidationError(f"Validation error: {exc}") from exc

    @staticmethod
    def get_output_dir_from_config(template_config) -> Optional[Path]:
        """Extract output directory from template config.

        Args:
            template_config: Template configuration object

        Returns:
            Path to output directory, or None if cannot be determined
        """
        if not template_config:
            return None
        if not hasattr(template_config, "yaml_data"):
            return None

        templates = template_config.yaml_data.get("templates", [])
        for template in templates:
            if template.get("output"):
                output_path = template.get("output")
                if not Path(output_path).is_absolute():
                    return template_config.yaml_path.parent / output_path
                return Path(output_path)

        return None
