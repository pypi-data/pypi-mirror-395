"""
Example 04: Secret Resolution

This example demonstrates how to use secret references in your configuration.
Instead of hardcoding sensitive values, you reference them with REF::PROVIDER::KEY
syntax and prism-config resolves them at runtime.

Run this example:
    python examples/04-secrets/secrets_example.py
"""

import os
from pathlib import Path
from prism.config import PrismConfig


def main():
    """Demonstrate secret resolution."""

    print("🔮 Secret Resolution Example")
    print("=" * 50)
    print()

    # Set secret values in environment (in production, these would be set by your infrastructure)
    print("🔐 Setting secrets in environment:")
    os.environ["API_KEY"] = "sk_live_abc123xyz789"
    os.environ["DB_PASSWORD"] = "super_secret_db_password_456"
    print("  API_KEY=sk_live_***")
    print("  DB_PASSWORD=super_secret_***")
    print()

    # Get path to config file
    config_file = Path(__file__).parent / "config.yaml"

    # Show config file content
    print("📄 Configuration file contains references:")
    with open(config_file) as f:
        content = f.read()
        print("  " + "\n  ".join(content.split("\n")[:10]))
    print()

    # Load configuration WITH secret resolution
    print("✨ Loading configuration with secret resolution...")
    config = PrismConfig.from_file(config_file, resolve_secrets=True)
    print("  ✅ Secrets resolved successfully!")
    print()

    # Access resolved values (secrets are decrypted/fetched)
    print("📋 Configuration values (secrets resolved):")
    print(f"  App Name: {config.app.name}")
    print(f"  API Key: {config.app.api_key[:10]}*** (resolved from ENV)")
    print(f"  DB Password: {config.database.password[:10]}*** (resolved from ENV)")
    print()

    # Display with automatic secret redaction
    print("🌈 Beautiful Display (secrets automatically redacted):")
    print()
    config.display()
    print()

    # Export with secret redaction
    print("📤 Export with secret redaction:")
    print()
    print("YAML (secrets redacted):")
    print(config.to_yaml(redact_secrets=True))
    print()

    # Show full values (for demonstration only - don't do this in production!)
    print("⚠️  Full values (for demonstration only):")
    print(f"  API Key: {config.app.api_key}")
    print(f"  DB Password: {config.database.password}")
    print()

    # Demonstrate FILE provider
    print("📁 FILE Provider Example:")
    # Create a temporary secret file
    secret_file = Path(__file__).parent / "db_password.txt"
    secret_file.write_text("file_based_password_xyz")
    print(f"  Created secret file: {secret_file}")

    # Load config with FILE provider reference
    file_config_data = {
        "app": {
            "name": "file-secret-app",
            "environment": "production"
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "mydb",
            "password": f"REF::FILE::{secret_file}"
        }
    }

    file_config = PrismConfig.from_dict(file_config_data, resolve_secrets=True)
    print(f"  Resolved from file: {file_config.database.password}")

    # Cleanup
    secret_file.unlink()
    print("  ✅ Cleaned up secret file")


if __name__ == "__main__":
    main()
