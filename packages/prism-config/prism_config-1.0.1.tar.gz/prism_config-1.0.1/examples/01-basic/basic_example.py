"""
Example 01: Basic Dictionary Configuration

This example demonstrates the simplest way to use prism-config:
loading configuration from a Python dictionary.

Run this example:
    python examples/01-basic/basic_example.py
"""

from prism.config import PrismConfig


def main():
    """Demonstrate basic dict loading."""

    # Define configuration as a Python dictionary
    config_data = {
        "app": {
            "name": "hello-world-app",
            "environment": "development",
            "api_key": "dev_key_12345"
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "development_db",
            "password": "dev_password_123"
        }
    }

    # Load configuration from dict
    config = PrismConfig.from_dict(config_data)

    # Access configuration values with type safety
    print("Basic Configuration Example")
    print("=" * 50)
    print(f"App Name: {config.app.name}")
    print(f"Environment: {config.app.environment}")
    print(f"API Key: {config.app.api_key}")
    print()
    print(f"Database Host: {config.database.host}")
    print(f"Database Port: {config.database.port}")
    print(f"Database Name: {config.database.name}")
    print()

    # Configuration is immutable (frozen)
    print("Configuration is immutable:")
    try:
        config.app.name = "new-name"
        print("  ERROR: Should have raised an error!")
    except Exception as e:
        print(f"  Prevented mutation: {type(e).__name__}")
    print()

    # Display beautiful output
    print("Beautiful Display:")
    print()
    config.display()
    print()

    # Export to different formats
    print("Export to different formats:")
    print()
    print("As YAML:")
    print(config.to_yaml())
    print()
    print("As JSON:")
    print(config.to_json(indent=2))


if __name__ == "__main__":
    main()
