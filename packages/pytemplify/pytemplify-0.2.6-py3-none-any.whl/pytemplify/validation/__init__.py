"""
Validation framework for pytemplify.

This module provides a comprehensive validation framework for generated files,
supporting multiple validator types including Google Tests, JSON schema validation,
file structure checks, and custom user-defined validators.

Key Components:
    - BaseValidator: Abstract base class for all validators
    - ValidatorRegistry: Registry for validator types
    - ValidationRunner: Orchestrates validation workflow
    - Built-in validators: GTest, JSON Schema, File Structure

Example:
    >>> from pytemplify.validation import create_validators_from_config, ValidationRunner
    >>> config = {
    ...     "validators": [{
    ...         "name": "Unit Tests",
    ...         "type": "gtest",
    ...         "enabled": True
    ...     }]
    ... }
    >>> validators = create_validators_from_config(config)
    >>> runner = ValidationRunner(validators)
    >>> results = runner.run_all(output_dir)
"""

from pytemplify.validation.base import (
    BaseValidator,
    ValidationResult,
    ValidatorConfig,
    ValidatorType,
)
from pytemplify.validation.registry import (
    ValidatorRegistry,
    create_validators_from_config,
    get_registry,
    register_validator,
)
from pytemplify.validation.runner import ValidationRunner

__all__ = [
    # Base classes
    "BaseValidator",
    "ValidationResult",
    "ValidatorConfig",
    "ValidatorType",
    # Registry
    "ValidatorRegistry",
    "create_validators_from_config",
    "get_registry",
    "register_validator",
    # Runner
    "ValidationRunner",
]

__version__ = "0.1.0"
