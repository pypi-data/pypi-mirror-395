"""
Validator registry for managing validator types.

This module provides a registry pattern for validators, following SOLID principles:
- SRP: Registry only manages validator registration and creation
- OCP: Open for extension (new validators) but closed for modification
- DIP: Depends on BaseValidator abstraction, not concrete implementations
"""

import importlib
import logging
import sys
from typing import Dict, List, Optional, Type

from pytemplify.validation.base import BaseValidator, ValidatorConfig, ValidatorType

logger = logging.getLogger(__name__)


class ValidatorRegistry:
    """
    Registry for validator classes (SOLID: SRP, OCP, DIP).

    Responsibilities:
        - Register validator types
        - Create validator instances from config
        - Support auto-discovery

    Open for Extension:
        - New validators can be registered without modifying this class
    """

    def __init__(self):
        """Initialize empty registry."""
        self._validators: Dict[ValidatorType, Type[BaseValidator]] = {}
        self._custom_validators: Dict[str, Type[BaseValidator]] = {}
        self._register_builtin_validators()

    def _register_builtin_validators(self) -> None:
        """
        Register built-in validators (DRY: centralized registration).

        Note: Validators are imported here to avoid circular imports
        and to fail gracefully if validators are not yet implemented.
        """
        # Import built-in validators (lazy import to avoid circular dependencies)
        try:
            # pylint: disable=import-outside-toplevel
            from pytemplify.validation.validators.gtest_validator import GTestValidator

            self.register(ValidatorType.GTEST, GTestValidator)
            logger.debug("Registered GTestValidator")
        except ImportError as e:
            logger.debug("GTestValidator not available: %s", e)

        try:
            # pylint: disable=import-outside-toplevel
            from pytemplify.validation.validators.json_validator import JSONSchemaValidator

            self.register(ValidatorType.JSON_SCHEMA, JSONSchemaValidator)
            logger.debug("Registered JSONSchemaValidator")
        except ImportError as e:
            logger.debug("JSONSchemaValidator not available: %s", e)

        try:
            # pylint: disable=import-outside-toplevel
            from pytemplify.validation.validators.file_validator import FileStructureValidator

            self.register(ValidatorType.FILE_STRUCTURE, FileStructureValidator)
            logger.debug("Registered FileStructureValidator")
        except ImportError as e:
            logger.debug("FileStructureValidator not available: %s", e)

    def register(self, validator_type: ValidatorType, validator_class: Type[BaseValidator]) -> None:
        """
        Register a validator class for a given type.

        Args:
            validator_type: Type of validator
            validator_class: Validator class (must inherit from BaseValidator)

        Raises:
            TypeError: If validator_class doesn't inherit from BaseValidator
        """
        if not issubclass(validator_class, BaseValidator):
            raise TypeError(f"{validator_class} must inherit from BaseValidator")

        self._validators[validator_type] = validator_class
        logger.info("Registered validator: %s -> %s", validator_type.value, validator_class.__name__)

    def register_custom(self, name: str, validator_class: Type[BaseValidator]) -> None:
        """
        Register a custom validator by name.

        Args:
            name: Unique name for the custom validator
            validator_class: Validator class

        Raises:
            ValueError: If name is already registered
            TypeError: If validator_class doesn't inherit from BaseValidator
        """
        if name in self._custom_validators:
            raise ValueError(f"Custom validator '{name}' already registered")

        if not issubclass(validator_class, BaseValidator):
            raise TypeError(f"{validator_class} must inherit from BaseValidator")

        self._custom_validators[name] = validator_class
        logger.info("Registered custom validator: %s -> %s", name, validator_class.__name__)

    def create_validator(self, config: ValidatorConfig) -> BaseValidator:
        """
        Create validator instance from configuration.

        Args:
            config: Validator configuration

        Returns:
            Validator instance

        Raises:
            ValueError: If validator type is not registered
        """
        if config.type == ValidatorType.CUSTOM:
            # Custom validator: resolve from options
            validator_class_name = config.options.get("validator_class")
            if not validator_class_name:
                raise ValueError("Custom validator requires 'validator_class' option")

            validator_class = self._resolve_custom_validator(validator_class_name, config)
        else:
            # Built-in validator
            validator_class = self._validators.get(config.type)
            if not validator_class:
                available_types = list(self._validators.keys())
                raise ValueError(f"Unknown validator type: {config.type}. Available types: {available_types}")

        return validator_class(config)

    def _resolve_custom_validator(self, class_name: str, config: ValidatorConfig) -> Type[BaseValidator]:
        """
        Resolve custom validator class by name.

        DRY: Similar to data helpers loader logic.

        Args:
            class_name: Fully qualified class name (module.ClassName)
            config: Validator configuration

        Returns:
            Validator class

        Raises:
            ValueError: If class cannot be loaded
        """
        # Check if already registered by name
        if class_name in self._custom_validators:
            return self._custom_validators[class_name]

        # Dynamic import
        validator_path = config.options.get("validator_path")
        if validator_path:
            sys.path.insert(0, str(validator_path))

        try:
            # Split module and class name
            if "." not in class_name:
                raise ValueError(f"Invalid class name format: {class_name}. Expected 'module.ClassName'")

            module_name, class_name_only = class_name.rsplit(".", 1)
            module = importlib.import_module(module_name)
            validator_class = getattr(module, class_name_only)

            if not issubclass(validator_class, BaseValidator):
                raise TypeError(f"{validator_class} must inherit from BaseValidator")

            # Cache for future use
            self._custom_validators[class_name] = validator_class

            return validator_class

        except (ImportError, AttributeError, ValueError) as e:
            raise ValueError(f"Failed to load custom validator '{class_name}': {e}") from e
        finally:
            if validator_path and str(validator_path) in sys.path:
                sys.path.remove(str(validator_path))

    def get_registered_types(self) -> List[ValidatorType]:
        """
        Get list of registered validator types.

        Returns:
            List of registered validator types
        """
        return list(self._validators.keys())

    def get_custom_validators(self) -> List[str]:
        """
        Get list of registered custom validator names.

        Returns:
            List of custom validator names
        """
        return list(self._custom_validators.keys())


class _RegistrySingleton:
    """Singleton holder for global registry."""

    _instance: Optional[ValidatorRegistry] = None

    @classmethod
    def get_instance(cls) -> ValidatorRegistry:
        """Get or create the singleton instance."""
        if cls._instance is None:
            cls._instance = ValidatorRegistry()
        return cls._instance


def get_registry() -> ValidatorRegistry:
    """
    Get the global validator registry (singleton).

    Returns:
        Global ValidatorRegistry instance
    """
    return _RegistrySingleton.get_instance()


def register_validator(validator_type: ValidatorType, validator_class: Type[BaseValidator]) -> None:
    """
    Convenience function to register a validator globally.

    Args:
        validator_type: Type of validator
        validator_class: Validator class
    """
    registry = get_registry()
    registry.register(validator_type, validator_class)


def create_validators_from_config(validation_config: Dict) -> List[BaseValidator]:
    """
    Create validator instances from YAML configuration.

    Args:
        validation_config: Validation section from YAML config

    Returns:
        List of validator instances

    Example:
        >>> config = {
        ...     "validators": [{
        ...         "name": "Unit Tests",
        ...         "type": "gtest",
        ...         "enabled": True,
        ...         "patterns": ["test_*.cpp"]
        ...     }]
        ... }
        >>> validators = create_validators_from_config(config)
    """
    validators = []
    registry = get_registry()

    for validator_dict in validation_config.get("validators", []):
        try:
            # Create config
            validator_type = ValidatorType(validator_dict["type"])

            # Merge profile into options if specified (for profile-based validators like gtest)
            options = validator_dict.get("options", {}).copy()
            if "profile" in validator_dict:
                options["profile"] = validator_dict["profile"]

            config = ValidatorConfig(
                name=validator_dict["name"],
                type=validator_type,
                enabled=validator_dict.get("enabled", True),
                patterns=validator_dict.get("patterns", []),
                options=options,
            )

            # Create validator if enabled
            if config.enabled:
                validator = registry.create_validator(config)
                validators.append(validator)
                logger.info("Created validator: %s", config.name)
            else:
                logger.debug("Skipped disabled validator: %s", config.name)

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Failed to create validator from config: %s", e)
            logger.debug("Validator config: %s", validator_dict)
            # Continue with other validators instead of failing completely
            continue

    return validators
