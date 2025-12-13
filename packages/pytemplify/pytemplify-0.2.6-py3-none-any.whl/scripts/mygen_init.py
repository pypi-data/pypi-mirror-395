from pathlib import Path
from pytemplify.renderer import TemplateRenderer

MYGEN_TEMPLATE_DIR = Path(__file__).parent / "mygen_template"


def main():
    # Prompt the user for additional information with default values
    mygen_name = (
        input("Enter the custom mygen name (default: 'mygen'): ")
        or "mygen"
    )
    your_name = input("Enter your name (default: 'John Doe'): ") or "John Doe"
    your_email = (
        input("Enter your email address (default: 'john.doe@example.com'): ")
        or "john.doe@example.com"
    )
    mygen_license = input("Enter the license (default: 'MIT'): ") or "MIT"
    mygen_description = input("Enter the mygen description (default: 'A custom mygen'): ") or "A custom mygen"
    output_dir = (
        input("Enter the target generation folder (default: './'): ")
        or "./"
    )

    # Create a dictionary with the input data
    data = {
        "mygen_name": mygen_name,
        "your_name": your_name,
        "your_email": your_email,
        "mygen_license": mygen_license,
        "mygen_description": mygen_description,
    }

    template_dir = Path(MYGEN_TEMPLATE_DIR)
    output_dir = Path(output_dir)

    renderer = TemplateRenderer(data, "dict_data")
    renderer.generate(template_dir, output_dir)


if __name__ == "__main__":
    main()
