"""
Example 05: Docker Integration

This is a complete example of a Dockerized application using prism-config
with Docker secrets and environment variables.

This file would be your main application entry point.
"""

import sys
from pathlib import Path
from prism.config import PrismConfig


def main():
    """Main application entry point."""

    print("🐳 Docker Integration Example")
    print("=" * 50)
    print()

    # In Docker, the config file would be at /app/config.yaml
    # For this example, we use a relative path
    config_file = Path(__file__).parent / "config.yaml"

    print("📋 Loading configuration...")
    print(f"  Config file: {config_file}")
    print(f"  CLI args: {sys.argv[1:]}")
    print()

    try:
        # Load configuration with all features:
        # - YAML file (base config)
        # - Environment variables (container overrides)
        # - CLI arguments (runtime overrides)
        # - Secret resolution (Docker secrets via FILE provider)
        config = PrismConfig.from_all(
            config_file,
            cli_args=sys.argv[1:],
            resolve_secrets=True
        )

        print("✅ Configuration loaded successfully!")
        print()

        # Show configuration
        print("🌈 Configuration Display:")
        print()
        config.display()
        print()

        # Access configuration in your application
        print("📊 Application Configuration:")
        print(f"  App Name: {config.app.name}")
        print(f"  Environment: {config.app.environment}")
        print(f"  API Key: {config.app.api_key[:10] if config.app.api_key else None}***")
        print()
        print(f"  Database Host: {config.database.host}")
        print(f"  Database Port: {config.database.port}")
        print(f"  Database Name: {config.database.name}")
        print(f"  Database Password: {'***' if config.database.password else None}")
        print()

        # Your application logic would go here
        print("🚀 Application would start here...")
        print("   - Connect to database")
        print("   - Initialize API client")
        print("   - Start web server")
        print()

    except Exception as e:
        print(f"❌ Configuration error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
