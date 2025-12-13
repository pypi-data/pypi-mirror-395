"""
Generator module for pytemplify.

This module provides enhanced template generation capabilities with YAML-based
configuration, advanced iteration patterns, and sophisticated template organization.

Key Components:
    - BaseCodeGenerator: Abstract base class for code generation with iteration support
    - GenericCodeGenerator: Concrete implementation for JSON/dict data with data_helpers
    - TemplateConfig: YAML configuration loading and validation
    - TemplateSetFilter: Template filtering by name patterns (glob/regex)

Features:
    - Multiple iteration patterns (simple, nested, conditional, array)
    - Template filtering by include/exclude patterns
    - Automatic file organization with _foreach_ prefixes
    - Data helper integration for enhanced template capabilities
    - Extra data loading from external JSON files
    - Jinja2 template rendering with custom filters

Usage Example:
    from pathlib import Path
    from pytemplify.generator import GenericCodeGenerator

    # Load data from JSON
    generator = GenericCodeGenerator.from_json_file(
        json_filepath=Path("data.json"),
        template_config_filepath=Path("templates.yaml")
    )

    # Generate files
    generator.generate(output_base_dir=Path("output"))

With Data Helpers:
    from pytemplify.data_helpers import DataHelper
    from pytemplify.generator import GenericCodeGenerator

    class MyHelper(DataHelper):
        @staticmethod
        def matches(data: dict) -> bool:
            return "my_field" in data

        @property
        def computed_value(self) -> str:
            return f"computed_{self._data.my_field}"

    generator = GenericCodeGenerator(
        data=my_data,
        template_config_filepath=Path("templates.yaml"),
        helpers=[MyHelper]
    )
    generator.generate()

See individual class documentation for detailed usage patterns.
"""

from .base_generator import BaseCodeGenerator, BaseGeneratorError, TemplateSetFilter
from .generic_generator import GenericCodeGenerator
from .template_config import TemplateConfig, TemplateConfigError

__all__ = [
    "BaseCodeGenerator",
    "BaseGeneratorError",
    "TemplateSetFilter",
    "GenericCodeGenerator",
    "TemplateConfig",
    "TemplateConfigError",
]
