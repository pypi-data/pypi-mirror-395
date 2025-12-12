"""
Example 03: Environment Variable Overrides

This example demonstrates how to override configuration values using
environment variables. This is the recommended approach for 12-factor
apps and containerized applications.

Run this example:
    python examples/03-env-vars/env_example.py
"""

import os
from pathlib import Path
from prism.config import PrismConfig


def main():
    """Demonstrate environment variable overrides."""

    print("🔮 Environment Variable Override Example")
    print("=" * 50)
    print()

    # Get path to config file
    config_file = Path(__file__).parent / "config.yaml"

    # Load base configuration (without env overrides)
    print("📋 Base configuration (from YAML file):")
    base_config = PrismConfig.from_file(config_file)
    print(f"  Environment: {base_config.app.environment}")
    print(f"  Database Host: {base_config.database.host}")
    print(f"  Database Port: {base_config.database.port}")
    print()

    # Set environment variables to override configuration
    print("🌍 Setting environment variables:")
    os.environ["APP_APP__ENVIRONMENT"] = "production"
    os.environ["APP_DATABASE__HOST"] = "prod-db.example.com"
    os.environ["APP_DATABASE__PORT"] = "3306"
    print("  APP_APP__ENVIRONMENT=production")
    print("  APP_DATABASE__HOST=prod-db.example.com")
    print("  APP_DATABASE__PORT=3306")
    print()

    # Load configuration with environment variable overrides
    print("📋 Configuration with env overrides:")
    config = PrismConfig.from_file(config_file, apply_env=True)
    print(f"  Environment: {config.app.environment}")  # "production" (from env)
    print(f"  Database Host: {config.database.host}")  # "prod-db.example.com" (from env)
    print(f"  Database Port: {config.database.port}")  # 3306 (from env, converted to int)
    print()

    # Show type coercion
    print("✨ Automatic type coercion:")
    print(f"  PORT env var is string: {os.environ['APP_DATABASE__PORT']!r}")
    port_type = type(config.database.port).__name__
    print(f"  Config port is int: {config.database.port!r} (type: {port_type})")
    print()

    # Display beautiful output
    print("🌈 Beautiful Display:")
    print()
    config.display()
    print()

    # Demonstrate precedence
    print("📊 Precedence demonstration:")
    os.environ["APP_APP__ENVIRONMENT"] = "staging"
    config_with_cli = PrismConfig.from_file(
        config_file,
        apply_env=True,
        cli_args=["--app.environment=production"]
    )
    print("  Env var: staging")
    print("  CLI arg: production")
    print(f"  Final value: {config_with_cli.app.environment} (CLI wins!)")
    print()

    # Custom prefix
    print("🔧 Custom prefix example:")
    os.environ["MYAPP_DATABASE__HOST"] = "custom-db.example.com"
    custom_config = PrismConfig.from_file(
        config_file,
        apply_env=True,
        env_prefix="MYAPP_"
    )
    print("  Using prefix: MYAPP_")
    print(f"  MYAPP_DATABASE__HOST={os.environ['MYAPP_DATABASE__HOST']}")
    print(f"  Result: {custom_config.database.host}")


if __name__ == "__main__":
    main()
