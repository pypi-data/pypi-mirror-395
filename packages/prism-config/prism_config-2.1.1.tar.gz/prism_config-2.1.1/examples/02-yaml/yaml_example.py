"""
Example 02: YAML File Configuration

This example demonstrates loading configuration from a YAML file.
This is the recommended approach for most applications.

Run this example:
    python examples/02-yaml/yaml_example.py
"""

from pathlib import Path
from prism.config import PrismConfig


def main():
    """Demonstrate YAML file loading."""

    # Get path to config file (relative to this script)
    config_file = Path(__file__).parent / "config.yaml"

    print("🔮 YAML File Configuration Example")
    print("=" * 50)
    print(f"Loading from: {config_file}")
    print()

    # Load configuration from YAML file
    config = PrismConfig.from_file(config_file)

    # Access configuration values
    print("📋 Configuration values:")
    print(f"  App Name: {config.app.name}")
    print(f"  Environment: {config.app.environment}")
    print(f"  Database Host: {config.database.host}")
    print(f"  Database Port: {config.database.port}")
    print()

    # Display beautiful output
    print("🌈 Beautiful Display:")
    print()
    config.display()
    print()

    # Save to a different format
    print("💾 Export to JSON:")
    json_output = config.to_json(indent=2)
    print(json_output)
    print()

    # Save to file
    output_file = Path(__file__).parent / "config_export.json"
    config.to_json_file(output_file, indent=2)
    print(f"✅ Saved to: {output_file}")


if __name__ == "__main__":
    main()
