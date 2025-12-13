"""
JSON schema for validation configuration.

This module defines the schema for validation configuration in YAML files.
"""

VALIDATION_CONFIG_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Pytemplify Validation Configuration",
    "description": (
        "Schema for validation configuration in templates.yaml. "
        "Supports profile-based configuration for simplified setup."
    ),
    "type": "object",
    "properties": {
        "enabled": {"type": "boolean", "default": True, "description": "Enable/disable validation globally"},
        "fail_fast": {
            "type": "boolean",
            "default": False,
            "description": "Stop validation on first failure",
        },
        "validators": {
            "type": "array",
            "description": "List of validator configurations",
            "items": {
                "type": "object",
                "required": ["name", "type"],
                "properties": {
                    "name": {"type": "string", "description": "Unique name for the validator"},
                    "type": {
                        "type": "string",
                        "enum": ["gtest", "json_schema", "file_structure", "custom"],
                        "description": "Type of validator",
                    },
                    "enabled": {"type": "boolean", "default": True, "description": "Enable/disable this validator"},
                    "patterns": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "File/test patterns to validate (glob or regex)",
                    },
                    "options": {"type": "object", "description": "Validator-specific options"},
                    "profile": {
                        "type": "string",
                        "enum": ["basic", "coverage", "strict", "custom"],
                        "default": "basic",
                        "description": "Configuration profile (basic, coverage, strict, custom)",
                    },
                },
            },
        },
    },
}


def validate_config(config: dict) -> bool:
    """
    Validate configuration against schema.

    Args:
        config: Configuration dictionary to validate

    Returns:
        True if valid

    Raises:
        jsonschema.ValidationError: If configuration is invalid
    """
    try:
        import jsonschema  # pylint: disable=import-outside-toplevel

        jsonschema.validate(instance=config, schema=VALIDATION_CONFIG_SCHEMA)
        return True
    except ImportError:
        # jsonschema not installed, skip validation
        return True
