"""PyTemplify - A generic text file generator framework using Jinja2 templates.

This package provides a powerful template rendering and code generation framework
with features like manual section preservation, content injection, and data helpers.

## Public API

### Core Classes (Stable)
- `TemplateRenderer`: Main template rendering engine
- `GenericCodeGenerator`: YAML-based code generation with data helpers

### Exceptions (Stable)
- `PyTemplifyError`: Base exception for all pytemplify errors
- `TemplateRendererException`: Template rendering errors
- `BaseGeneratorError`: Code generation errors
- `FormattingError`, `ValidationError`, `HelperError`, etc.

### Manual Section Management (Stable)
- `ManualSectionManager`: Centralized manual section handling
- `ManualSectionError`: Manual section validation errors

### Subpackages (Stable)
- `pytemplify.generator`: Code generation framework
- `pytemplify.data_helpers`: Data helper extension system
- `pytemplify.validation`: Validation framework
- `pytemplify.filters`: Built-in Jinja2 filters

### Version
- `__version__`: Package version string

## Stability Guarantee

Classes and functions exported from this module and documented in the API
reference are considered **stable** and follow semantic versioning:
- **Major version change**: Breaking API changes
- **Minor version change**: New features, backwards compatible
- **Patch version change**: Bug fixes, backwards compatible

Internal modules (prefixed with `_` or not in `__all__`) may change without notice.
"""

# Import exceptions for easy access
from pytemplify.exceptions import (
    BaseGeneratorError,
    FormattingError,
    GeneratorError,
    HelperError,
    HelperLoaderError,
    ManualSectionError,
    PyTemplifyError,
    TemplateConfigError,
    TemplateError,
    TemplateRendererException,
    ValidationError,
)

# Core public classes
from pytemplify.generator import GenericCodeGenerator

# Import manual section utilities
from pytemplify.manual_sections import ManualSectionManager
from pytemplify.renderer import TemplateRenderer

__all__ = [
    # Core Classes
    "TemplateRenderer",
    "GenericCodeGenerator",
    # Exceptions
    "PyTemplifyError",
    "TemplateError",
    "TemplateRendererException",
    "TemplateConfigError",
    "GeneratorError",
    "BaseGeneratorError",
    "FormattingError",
    "ValidationError",
    "HelperError",
    "HelperLoaderError",
    # Manual Section Management
    "ManualSectionManager",
    "ManualSectionError",
]

__version__ = "0.2.0"
