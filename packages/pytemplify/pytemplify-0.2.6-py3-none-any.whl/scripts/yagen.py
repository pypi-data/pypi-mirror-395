"""YAML-based generator script for pytemplify.

This script provides command-line interface for enhanced template generation
using YAML configuration files with advanced iteration patterns.
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Type, Union

from pytemplify.data_helpers import DataHelper, HelperLoaderError
from pytemplify.generator import BaseGeneratorError, GenericCodeGenerator, TemplateSetFilter
from pytemplify.logging_utils import configure_logging


def setup_logging(verbose: bool = False) -> None:
    """Configure logging for the generator."""
    level = logging.DEBUG if verbose else logging.INFO
    configure_logging(level=level, format_string="%(asctime)s - %(levelname)s - %(message)s")


def create_template_filter(
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None,
) -> Optional[TemplateSetFilter]:
    """Create template filter from command line arguments."""
    if include_patterns or exclude_patterns:
        return TemplateSetFilter(
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
        )
    return None


def load_json_data(json_path: Path) -> Dict:
    """Load JSON data from file."""
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as exc:
        raise BaseGeneratorError(f"Failed to load JSON data from {json_path}: {exc}")


def main() -> None:
    """Main entry point for yagen CLI."""
    parser = argparse.ArgumentParser(
        description="YAML-based template generator for pytemplify",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic generation (output specified in YAML)
  yagen --config templates.yaml --data data.json

  # With base output directory override
  yagen --config templates.yaml --data data.json --output ./output

  # With template filtering
  yagen --config templates.yaml --data data.json \\
        --include "Core*" --exclude "*Test*"

  # With data helpers
  yagen --config templates.yaml --data data.json \\
        --helpers "my_helpers.CompanyHelpers" \\
        --helper-path "./helpers/"

  # Verbose output
  yagen --config templates.yaml --data data.json --verbose

  # Disable data flattening (requires dd. prefix)
  yagen --config templates.yaml --data data.json --no-flatten

Data Flattening:
  By default, top-level data keys are accessible directly (e.g., {{ project_name }}).
  You can also use the dd. namespace (e.g., {{ dd.project_name }}).

  Configure in YAML:
    flatten_data: false  # Requires dd. prefix for all data access

  Or via CLI (overrides YAML):
    --no-flatten  # Disables flattening

  Precedence: CLI --no-flatten > YAML flatten_data > default (true)

Template Filtering:
  --include and --exclude support:
  - Exact matching: "Core Infrastructure"
  - Glob patterns: "Core*", "*Debug*", "Unit Test*"
  - Regex patterns: "regex:.*Plugin.*", "regex:^Core.*$"

Data Helpers:
  --helpers supports multiple formats:
  - Single class: "my_helpers.CompanyHelpers"
  - Multiple classes: "my_helpers.CompanyHelpers,my_helpers.EmployeeHelpers"
  - Entire module: "my_helpers" (loads all DataHelper classes)
  - Python file: "my_helpers.py" (loads all DataHelper classes from file)
  
  --helper-path discovers helpers from directories:
  - Single path: "./helpers/"
  - Multiple paths: "./helpers/" "./shared_helpers/"
  
  Precedence: CLI args > YAML config > auto-discovery
        """,
    )

    parser.add_argument(
        "--config",
        "-c",
        type=Path,
        required=True,
        help="Path to YAML template configuration file",
    )

    parser.add_argument(
        "--data",
        "-d",
        type=Path,
        required=True,
        help="Path to JSON data file",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Base output directory for generated files (optional if specified in YAML)",
    )

    parser.add_argument(
        "--include",
        "-i",
        action="append",
        help="Include pattern for template sets (can be used multiple times)",
    )

    parser.add_argument(
        "--exclude",
        "-e",
        action="append",
        help="Exclude pattern for template sets (can be used multiple times)",
    )

    # Data helpers arguments
    parser.add_argument(
        "--helpers",
        action="append",
        help="Helper specifications (module.Class or module.py). Can be used multiple times.",
    )

    parser.add_argument(
        "--helper-path",
        action="append",
        help="Directory paths to discover helper classes. Can be used multiple times.",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    parser.add_argument(
        "--no-flatten",
        action="store_true",
        help="Disable data flattening (requires dd. prefix for all data access)",
    )

    # Validation arguments
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Run validation after generation (requires validation config in YAML)",
    )

    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip validation even if configured in YAML",
    )

    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop validation on first failure",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate generation without writing files to disk",
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    try:
        # Validate input files
        if not args.config.exists():
            logger.error(f"Template config file not found: {args.config}")
            sys.exit(1)

        if not args.data.exists():
            logger.error(f"Data file not found: {args.data}")
            sys.exit(1)

        # Load data
        logger.info(f"Loading data from {args.data}")
        data = load_json_data(args.data)

        # Create template filter if patterns provided
        template_filter = create_template_filter(
            include_patterns=args.include,
            exclude_patterns=args.exclude,
        )

        if template_filter:
            logger.info("Template filtering enabled")
            if args.include:
                logger.info(f"Include patterns: {', '.join(args.include)}")
            if args.exclude:
                logger.info(f"Exclude patterns: {', '.join(args.exclude)}")

        # Log data helpers configuration
        if args.helpers:
            logger.info(f"Using helper specifications: {', '.join(args.helpers)}")
        if args.helper_path:
            logger.info(f"Using helper discovery paths: {', '.join(args.helper_path)}")

        # Create generator with data helpers support
        logger.info(f"Loading template configuration from {args.config}")

        # Determine flatten_data: CLI flag takes precedence over YAML config
        flatten_data_arg = False if args.no_flatten else None  # None means use YAML config

        generator = GenericCodeGenerator(
            data=data,
            template_config_filepath=args.config,
            template_filter=template_filter,
            helper_specs=args.helpers,
            helper_discovery_paths=args.helper_path,
            flatten_data=flatten_data_arg,
        )

        # Generate files
        output_dir = None
        if args.output:
            logger.info(f"Generating files to {args.output}")
            args.output.mkdir(parents=True, exist_ok=True)
            output_dir = args.output
        else:
            logger.info("Generating files (output directories from YAML configuration)")
            # When no --output is specified, use config file's parent
            # Templates will use their own 'output' values relative to base
            output_dir = args.config.parent

        # Generate with automatic validation
        # Validation is now integrated into generate() method
        # It will run automatically if configured in templates.yaml
        try:
            # Determine validation flags
            run_val = args.validate if args.validate else (None if not args.no_validate else False)
            fail_fast_val = args.fail_fast if args.fail_fast else None

            generator.generate(
                output_base_dir=output_dir,
                run_validation=run_val,
                fail_fast_validation=fail_fast_val,
                dry_run=args.dry_run,
            )
            logger.info("Generation completed successfully!")
        except Exception as exc:
            if "ValidationError" in str(type(exc).__name__):
                logger.error("Generation completed but validation failed!")
                sys.exit(1)
            raise

    except BaseGeneratorError as exc:
        logger.error(f"Generation failed: {exc}")
        sys.exit(1)
    except HelperLoaderError as exc:
        logger.error(f"Helper loading failed: {exc}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Generation interrupted by user")
        sys.exit(1)
    except Exception as exc:
        logger.error(f"Unexpected error: {exc}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
