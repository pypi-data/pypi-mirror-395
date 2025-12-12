"""
Example 10: Catch-All Flexible Configuration (v2.0.0)

This example demonstrates prism-config's flexible mode, which accepts
ANY configuration structure without requiring a predefined schema.

Key v2.0.0 features demonstrated:
- Schema-free configuration loading
- Dot-notation access for any nested path
- DynamicConfig for arbitrary structures
- Hybrid mode (typed + flexible)
- No validation constraints

Run this example:
    export SENDGRID_API_KEY=sg_test_key
    export TWILIO_SID=AC123
    export TWILIO_TOKEN=auth_token
    export STRIPE_SECRET=sk_test_xxx
    export STRIPE_WEBHOOK=whsec_xxx

    python examples/10-flexible/flexible_example.py
"""

import sys
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from prism.config import (
    PrismConfig,
    DynamicConfig,
    register_emoji,
)


# =============================================================================
# Main Example
# =============================================================================


def main():
    """Demonstrate flexible schema-free configuration."""

    print("=" * 70)
    print("Flexible Configuration Example (prism-config v2.0.0)")
    print("=" * 70)
    print()

    # -------------------------------------------------------------------------
    # Step 1: Register custom emojis for arbitrary sections
    # -------------------------------------------------------------------------
    print("Step 1: Registering emojis for custom sections...")
    register_emoji("my_service", "🔧")
    register_emoji("analytics", "📊")
    register_emoji("notifications", "🔔")
    register_emoji("feature_flags", "🚩")
    register_emoji("vendor_config", "🏢")
    register_emoji("metadata", "📋")
    print("  Registered emojis for: my_service, analytics, notifications,")
    print("  feature_flags, vendor_config, metadata")
    print()

    # -------------------------------------------------------------------------
    # Step 2: Load configuration WITHOUT a schema (flexible mode)
    # -------------------------------------------------------------------------
    print("Step 2: Loading configuration in flexible mode (no schema)...")
    config_file = Path(__file__).parent / "config.yaml"

    # strict=False enables flexible mode - no schema validation!
    config = PrismConfig.from_file(
        config_file,
        resolve_secrets=True,
        strict=False,  # This is the key!
    )

    print(f"  Loaded from: {config_file}")
    print("  Mode: Flexible (no schema validation)")
    print()

    # -------------------------------------------------------------------------
    # Step 3: Access standard sections
    # -------------------------------------------------------------------------
    print("Step 3: Accessing standard sections...")
    print()

    print("  App Configuration:")
    print(f"    Name: {config.app.name}")
    print(f"    Environment: {config.app.environment}")
    print(f"    Custom Field: {config.app.custom_field}")  # Works!
    print()

    # -------------------------------------------------------------------------
    # Step 4: Access completely custom sections
    # -------------------------------------------------------------------------
    print("Step 4: Accessing custom sections...")
    print()

    print("  🔧 My Service (custom section):")
    print(f"    Endpoint: {config.my_service.endpoint}")
    print(f"    Timeout: {config.my_service.timeout}")
    print(f"    Retry Max: {config.my_service.retry.max_attempts}")
    print(f"    Retry Backoff: {config.my_service.retry.backoff}")
    print()

    # -------------------------------------------------------------------------
    # Step 5: Access deeply nested arbitrary structures
    # -------------------------------------------------------------------------
    print("Step 5: Accessing deeply nested structures...")
    print()

    print("  📊 Analytics Providers:")
    print(f"    Google Tracking ID: {config.analytics.providers.google.tracking_id}")
    print(f"    Google Enabled: {config.analytics.providers.google.enabled}")
    print(f"    Mixpanel Enabled: {config.analytics.providers.mixpanel.enabled}")
    print(f"    Segment Integrations: {config.analytics.providers.segment.integrations}")
    print()

    # -------------------------------------------------------------------------
    # Step 6: Access lists of complex objects
    # -------------------------------------------------------------------------
    print("Step 6: Accessing lists of complex objects...")
    print()

    print("  🔔 Notification Channels:")
    for i, channel in enumerate(config.notifications.channels):
        print(f"    Channel {i + 1}:")
        print(f"      Type: {channel.type}")
        print(f"      Provider: {channel.provider}")
    print()

    # -------------------------------------------------------------------------
    # Step 7: Access feature flags
    # -------------------------------------------------------------------------
    print("Step 7: Feature flags (arbitrary key-value)...")
    print()

    print("  🚩 Feature Flags:")
    print(f"    dark_mode: {config.feature_flags.dark_mode}")
    print(f"    new_dashboard: {config.feature_flags.new_dashboard}")
    print(f"    beta_api: {config.feature_flags.beta_api}")
    print(f"    experiments.checkout_v2: {config.feature_flags.experiments.checkout_v2}")
    print()

    # -------------------------------------------------------------------------
    # Step 8: Access vendor configurations
    # -------------------------------------------------------------------------
    print("Step 8: Vendor configurations...")
    print()

    print("  🏢 Stripe Config:")
    print(f"    Publishable Key: {config.vendor_config.stripe.publishable_key}")
    print()

    print("  🏢 AWS Config:")
    print(f"    Region: {config.vendor_config.aws.region}")
    print(f"    S3 Bucket: {config.vendor_config.aws.services.s3.bucket}")
    print(f"    S3 Prefix: {config.vendor_config.aws.services.s3.prefix}")
    print()

    # -------------------------------------------------------------------------
    # Step 9: Access metadata
    # -------------------------------------------------------------------------
    print("Step 9: Arbitrary metadata...")
    print()

    print("  📋 Metadata:")
    print(f"    Version: {config.metadata.version}")
    print(f"    Build: {config.metadata.build_number}")
    print(f"    Git Commit: {config.metadata.git_commit}")
    print(f"    Deployed By: {config.metadata.deployed_by}")
    print()

    # -------------------------------------------------------------------------
    # Step 10: Display configuration
    # -------------------------------------------------------------------------
    print("Step 10: Full configuration display (with auto-detected emojis)...")
    print()
    config.display()
    print()

    # -------------------------------------------------------------------------
    # Step 11: Demonstrate DynamicConfig directly
    # -------------------------------------------------------------------------
    print("Step 11: Using DynamicConfig directly...")
    print()

    # Create DynamicConfig from arbitrary dict
    custom_data = {
        "server": {
            "host": "localhost",
            "port": 8080,
            "ssl": {"enabled": True, "cert_path": "/etc/ssl/cert.pem"},
        },
        "plugins": [{"name": "auth", "enabled": True}, {"name": "cache", "enabled": False}],
    }

    dynamic = DynamicConfig(custom_data)
    print("  Created DynamicConfig from dict:")
    print(f"    server.host: {dynamic.server.host}")
    print(f"    server.ssl.enabled: {dynamic.server.ssl.enabled}")
    print(f"    plugins[0].name: {dynamic.plugins[0].name}")
    print()

    # -------------------------------------------------------------------------
    # Step 12: Usage patterns
    # -------------------------------------------------------------------------
    print("Step 12: When to use flexible mode:")
    print()
    print("""
    Use FLEXIBLE mode (strict=False) when:
    - You don't know the configuration structure upfront
    - Configuration comes from external sources (CMS, API)
    - You need maximum flexibility without constraints
    - Rapid prototyping without schema definition
    - Dynamic plugin/extension configurations

    Use TYPED mode (with schema, strict=True) when:
    - You need compile-time type checking
    - IDE autocomplete is important
    - Configuration errors should fail fast
    - Documentation through code (schema as docs)
    - Team conventions need enforcement

    Use HYBRID mode when:
    - Core settings need type safety
    - Extensions/plugins can add arbitrary config
    - You want best of both worlds

    Example hybrid schema:

    class MyConfig(BaseConfigRoot):
        app: AppConfig           # Typed, validated
        database: DatabaseConfig # Typed, validated

        model_config = {"extra": "allow"}  # Allow extra!

    config = PrismConfig.from_file("config.yaml", schema=MyConfig)
    config.app.name              # Typed access
    config.my_custom_section     # Also works (flexible)
    """)

    print("=" * 70)
    print("Example complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
