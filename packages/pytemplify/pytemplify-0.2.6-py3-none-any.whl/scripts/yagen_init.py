#!/usr/bin/env python3
"""Initialize a new pytemplify project with sample files.

This script creates a basic project structure with templates.yaml and data.json.
"""

import argparse
import json
import sys
from pathlib import Path


SAMPLE_TEMPLATES_YAML = """# Pytemplify Template Configuration
# For detailed documentation, see: https://github.com/robinbreast/pytemplify

globals:
  version: "1.0.0"
  project: "MyProject"

# Optional: Configure manual sections (defaults shown)
# manual_sections:
#   start_marker: "MANUAL SECTION START"
#   end_marker: "MANUAL SECTION END"

templates:
  - name: "Sample Template"
    folder: "templates"
    output: "output"
    # Optional: Iterate over data
    # iterate: "item in dd.items"
"""

SAMPLE_DATA_JSON = """{
  "project_name": "MyProject",
  "version": "1.0.0",
  "items": [
    {
      "name": "Item1",
      "description": "First item"
    },
    {
      "name": "Item2",
      "description": "Second item"
    }
  ]
}
"""

SAMPLE_TEMPLATE = """# {{ project_name }}

Version: {{ version }}

## Items
{% for item in items %}
- {{ item.name }}: {{ item.description }}
{% endfor %}

MANUAL SECTION START: custom_section
Add your custom content here. This section will be preserved during regeneration.
MANUAL SECTION END
"""


def create_sample_project(directory: Path, force: bool = False) -> None:
    """Create a sample pytemplify project structure.
    
    Args:
        directory: Target directory for the project
        force: Overwrite existing files
    """
    # Create directories
    directory.mkdir(parents=True, exist_ok=True)
    templates_dir = directory / "templates"
    templates_dir.mkdir(exist_ok=True)
    
    files_to_create = {
        directory / "templates.yaml": SAMPLE_TEMPLATES_YAML,
        directory / "data.json": SAMPLE_DATA_JSON,
        templates_dir / "README.md.j2": SAMPLE_TEMPLATE,
    }
    
    created_files = []
    skipped_files = []
    
    for file_path, content in files_to_create.items():
        if file_path.exists() and not force:
            skipped_files.append(file_path.name)
            print(f"⊘ Skipped {file_path.name} (already exists)")
        else:
            file_path.write_text(content.strip() + "\n")
            created_files.append(file_path.name)
            print(f"✓ Created {file_path.name}")
    
    print("\nProject initialized!")
    print(f"\nNext steps:")
    print(f"  1. Edit data.json with your data")
    print(f"  2. Customize templates in templates/")
    print(f"  3. Run: yagen --config templates.yaml --data data.json --output output")
    
    if skipped_files and not force:
        print(f"\nNote: Use --force to overwrite existing files")


def main() -> None:
    """Main entry point for yagen init."""
    parser = argparse.ArgumentParser(
        description="Initialize a new pytemplify project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create project in current directory
  yagen-init

  # Create project in specific directory
  yagen-init --directory my_project

  # Overwrite existing files
  yagen-init --force
        """,
    )
    
    parser.add_argument(
        "--directory",
        "-d",
        type=Path,
        default=Path.cwd(),
        help="Target directory for the project (default: current directory)",
    )
    
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Overwrite existing files",
    )
    
    args = parser.parse_args()
    
    try:
        create_sample_project(args.directory, args.force)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
