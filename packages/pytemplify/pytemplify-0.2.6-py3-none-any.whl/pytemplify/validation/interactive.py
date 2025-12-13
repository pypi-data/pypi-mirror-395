"""
Interactive CLI for validation selection and configuration.

This module provides Click-based interactive commands for validator selection
and configuration using questionary for enhanced UX.

SOLID Principles:
    - SRP: Single responsibility - CLI interaction
    - OCP: Open for extension through plugin validators
    - DIP: Depends on abstractions (ValidatorRegistry)

DRY Principle:
    - Reuses ValidatorRegistry for validator discovery
    - Reuses ValidationRunner for execution
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional

import click

from pytemplify.validation.base import ValidatorType
from pytemplify.validation.registry import create_validators_from_config, get_registry
from pytemplify.validation.runner import ValidationRunner

logger = logging.getLogger(__name__)

# Optional questionary import (graceful degradation)
try:
    import questionary

    QUESTIONARY_AVAILABLE = True
except ImportError:
    QUESTIONARY_AVAILABLE = False
    logger.debug("questionary not available, using Click prompts")


def select_validators_interactive(available_types: List[ValidatorType]) -> List[str]:
    """
    Interactively select validators using questionary.

    Args:
        available_types: List of available validator types

    Returns:
        List of selected validator type names
    """
    if not QUESTIONARY_AVAILABLE:
        click.echo("Warning: questionary not installed. Install with: pip install questionary")
        click.echo("Using basic selection...")
        return _select_validators_basic(available_types)

    choices = [
        {"name": f"{vtype.value.upper()}: {_get_validator_description(vtype)}", "value": vtype.value}
        for vtype in available_types
    ]

    selected = questionary.checkbox(
        "Select validators to run:",
        choices=choices,
    ).ask()

    return selected if selected else []


def _select_validators_basic(available_types: List[ValidatorType]) -> List[str]:
    """
    Basic validator selection using Click prompts (fallback).

    Args:
        available_types: List of available validator types

    Returns:
        List of selected validator type names
    """
    selected = []

    click.echo("\nAvailable validators:")
    for idx, vtype in enumerate(available_types, 1):
        click.echo(f"  {idx}. {vtype.value.upper()}: {_get_validator_description(vtype)}")

    while True:
        choice = click.prompt(
            "\nEnter validator number (or 'done' to finish)",
            type=str,
            default="done",
        )

        if choice.lower() == "done":
            break

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(available_types):
                vtype = available_types[idx]
                if vtype.value not in selected:
                    selected.append(vtype.value)
                    click.echo(f"  ✓ Added {vtype.value}")
                else:
                    click.echo(f"  - Already selected: {vtype.value}")
            else:
                click.echo(f"  ✗ Invalid choice: {choice}")
        except ValueError:
            click.echo(f"  ✗ Invalid input: {choice}")

    return selected


def _get_validator_description(vtype: ValidatorType) -> str:
    """
    Get human-readable description for validator type.

    Args:
        vtype: Validator type

    Returns:
        Description string
    """
    descriptions = {
        ValidatorType.GTEST: "Validate C++ Google Tests",
        ValidatorType.JSON_SCHEMA: "Validate JSON files against schemas",
        ValidatorType.FILE_STRUCTURE: "Validate file/directory structure",
        ValidatorType.CUSTOM: "Custom validator",
    }
    return descriptions.get(vtype, "Unknown validator")


def configure_validator_interactive(vtype: str) -> Dict:
    """
    Interactively configure a validator.

    Args:
        vtype: Validator type name

    Returns:
        Configuration dictionary
    """
    config = {
        "name": f"{vtype.upper()} Validator",
        "type": vtype,
        "enabled": True,
        "patterns": [],
        "options": {},
    }

    if not QUESTIONARY_AVAILABLE:
        click.echo(f"\nConfiguring {vtype.upper()} validator...")
        return _configure_validator_basic(vtype, config)

    # Get validator name
    name = questionary.text(
        "Validator name:",
        default=config["name"],
    ).ask()
    if name:
        config["name"] = name

    # Get file patterns
    patterns_input = questionary.text(
        "File patterns (comma-separated, or press Enter for defaults):",
        default=_get_default_patterns(vtype),
    ).ask()

    if patterns_input:
        config["patterns"] = [p.strip() for p in patterns_input.split(",") if p.strip()]

    # Type-specific configuration
    config["options"] = _configure_validator_options(vtype)

    return config


def _configure_validator_basic(vtype: str, config: Dict) -> Dict:
    """
    Basic validator configuration using Click prompts (fallback).

    Args:
        vtype: Validator type name
        config: Initial configuration

    Returns:
        Configuration dictionary
    """
    # Get validator name
    name = click.prompt("Validator name", default=config["name"])
    config["name"] = name

    # Get file patterns
    default_patterns = _get_default_patterns(vtype)
    patterns_input = click.prompt(
        "File patterns (comma-separated)",
        default=default_patterns,
    )

    if patterns_input:
        config["patterns"] = [p.strip() for p in patterns_input.split(",") if p.strip()]

    return config


def _get_default_patterns(vtype: str) -> str:
    """
    Get default file patterns for validator type.

    Args:
        vtype: Validator type name

    Returns:
        Comma-separated pattern string
    """
    defaults = {
        "gtest": "test_*.cpp, *_test.cpp",
        "json_schema": "*.json",
        "file_structure": "*",
    }
    return defaults.get(vtype, "*")


def _configure_validator_options(vtype: str) -> Dict:
    """
    Configure validator-specific options.

    Args:
        vtype: Validator type name

    Returns:
        Options dictionary
    """
    options = {}

    if vtype == "gtest":
        options = _configure_gtest_options()
    elif vtype == "json_schema":
        options = _configure_json_schema_options()
    elif vtype == "file_structure":
        options = _configure_file_structure_options()

    return options


def _configure_gtest_options() -> Dict:
    """Configure Google Test validator options."""
    if not QUESTIONARY_AVAILABLE:
        return {}

    options = {}

    # C++ standard
    cxx_standard = questionary.select(
        "C++ standard:",
        choices=["11", "14", "17", "20", "23"],
        default="17",
    ).ask()
    options["cxx_standard"] = int(cxx_standard)

    # Coverage
    enable_coverage = questionary.confirm(
        "Enable code coverage?",
        default=True,
    ).ask()
    options["enable_coverage"] = enable_coverage

    return options


def _configure_json_schema_options() -> Dict:
    """Configure JSON Schema validator options."""
    if not QUESTIONARY_AVAILABLE:
        return {}

    options = {}

    # Schema file
    schema_file = questionary.text(
        "Schema file path:",
        default="schemas/schema.json",
    ).ask()
    if schema_file:
        options["schema_file"] = schema_file

    # Additional properties
    allow_additional = questionary.confirm(
        "Allow additional properties?",
        default=False,
    ).ask()
    options["allow_additional_properties"] = allow_additional

    return options


def _configure_file_structure_options() -> Dict:
    """Configure File Structure validator options."""
    if not QUESTIONARY_AVAILABLE:
        return {}

    options = {}

    # Required files
    required = questionary.text(
        "Required files (comma-separated patterns):",
        default="README.md, LICENSE",
    ).ask()
    if required:
        options["required_files"] = [f.strip() for f in required.split(",") if f.strip()]

    # Forbidden files
    forbidden = questionary.text(
        "Forbidden files (comma-separated patterns):",
        default="*.tmp, *.pyc, .DS_Store",
    ).ask()
    if forbidden:
        options["forbidden_files"] = [f.strip() for f in forbidden.split(",") if f.strip()]

    return options


@click.command()
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    required=True,
    help="Output directory to validate",
)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    help="Validation configuration file (YAML)",
)
@click.option(
    "--interactive",
    "-i",
    is_flag=True,
    help="Interactive validator selection",
)
@click.option(
    "--fail-fast",
    is_flag=True,
    help="Stop on first validation failure",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Verbose output",
)
def validate(  # pylint: disable=too-many-locals
    output_dir: Path,
    config: Optional[Path],
    interactive: bool,
    fail_fast: bool,
    verbose: bool,
):
    """
    Run validation on generated files.

    Examples:

        # Interactive selection
        pytemplify-validate -o output/ --interactive

        # From configuration file
        pytemplify-validate -o output/ --config validation.yaml

        # Fail fast mode
        pytemplify-validate -o output/ --config validation.yaml --fail-fast
    """
    # Setup logging
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    click.echo(f"Validating output directory: {output_dir}")

    # Load or create validation configuration
    if config:
        # Load from file
        import yaml  # pylint: disable=import-outside-toplevel

        with open(config, encoding="utf-8") as f:
            validation_config = yaml.safe_load(f).get("validation", {})
        validators = create_validators_from_config(validation_config)
    elif interactive:
        # Interactive selection
        registry = get_registry()
        available_types = registry.get_registered_types()

        if not available_types:
            click.echo("No validators available")
            return

        selected_types = select_validators_interactive(available_types)

        if not selected_types:
            click.echo("No validators selected")
            return

        # Configure each selected validator
        validator_configs = []
        for vtype in selected_types:
            vconfig = configure_validator_interactive(vtype)
            validator_configs.append(vconfig)

        # Create validators
        validators = []
        for vconfig in validator_configs:
            validator = registry.create_validator(vconfig)
            validators.append(validator)
    else:
        raise click.UsageError("Either --config or --interactive must be specified")

    # Run validation
    runner = ValidationRunner(validators)
    results = runner.run_all(output_dir, fail_fast=fail_fast)

    # Print results
    success = runner.print_summary(results)

    # Additional CLI-friendly output
    if success:
        click.echo("\n✅ All validations passed!")
    else:
        click.echo("\n❌ Some validations failed")

    # Exit with appropriate code
    if not success:
        raise click.ClickException("Validation failed")


if __name__ == "__main__":
    validate.main(standalone_mode=False)  # pylint: disable=no-value-for-parameter
