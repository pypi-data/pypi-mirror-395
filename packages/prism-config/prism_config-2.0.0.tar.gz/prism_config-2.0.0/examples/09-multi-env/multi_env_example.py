"""
Example 09: Multi-Environment Configuration (v2.0.0)

This example demonstrates managing configuration across multiple
environments (development, staging, production) using prism-config.

Key features demonstrated:
- Base configuration with environment overrides
- Environment-specific secret resolution
- Loading configuration based on APP_ENV variable
- Merging base and environment configs

Run this example:
    # Development (default)
    python examples/09-multi-env/multi_env_example.py

    # Staging
    APP_ENV=staging DB_PASSWORD=stg_pass CACHE_PASSWORD=cache_pass \
        python examples/09-multi-env/multi_env_example.py

    # Production
    APP_ENV=production DB_PASSWORD=prod_pass CACHE_PASSWORD=cache_pass \
        python examples/09-multi-env/multi_env_example.py
"""

import os
import sys
from pathlib import Path
from typing import Optional

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from prism.config import (
    BaseConfigSection,
    BaseConfigRoot,
    PrismConfig,
)


# =============================================================================
# Configuration Schema
# =============================================================================


class AppConfig(BaseConfigSection):
    """Application metadata."""

    name: str
    version: str = "1.0.0"
    environment: str = "development"


class DatabaseConfig(BaseConfigSection):
    """Database configuration."""

    host: str = "localhost"
    port: int = 5432
    name: str = "myapp"
    password: Optional[str] = None
    pool_size: int = 5


class CacheConfig(BaseConfigSection):
    """Cache configuration."""

    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    ttl: int = 300


class LoggingConfig(BaseConfigSection):
    """Logging configuration."""

    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


class FeaturesConfig(BaseConfigSection):
    """Feature flags."""

    beta_features: bool = False
    maintenance_mode: bool = False
    debug_mode: bool = False


class MultiEnvConfig(BaseConfigRoot):
    """Configuration for multi-environment application."""

    app: AppConfig
    database: DatabaseConfig
    cache: CacheConfig
    logging: LoggingConfig
    features: FeaturesConfig


# =============================================================================
# Configuration Loading Functions
# =============================================================================


def merge_configs(base: dict, override: dict) -> dict:
    """
    Deep merge two configuration dictionaries.

    Values in override take precedence over base.
    """
    result = base.copy()

    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value

    return result


def load_config_for_env(env: str, config_dir: Path) -> PrismConfig:
    """
    Load configuration for specified environment.

    1. Load base.yaml
    2. Load {env}.yaml
    3. Merge with env overriding base
    4. Resolve secrets
    """
    import yaml

    # Load base config
    base_file = config_dir / "base.yaml"
    with open(base_file) as f:
        base_config = yaml.safe_load(f)

    # Load environment-specific config
    env_file = config_dir / f"{env}.yaml"
    if env_file.exists():
        with open(env_file) as f:
            env_config = yaml.safe_load(f)
    else:
        print(f"  Warning: {env}.yaml not found, using base config only")
        env_config = {}

    # Merge configs
    merged_config = merge_configs(base_config, env_config)

    # Create PrismConfig from merged dict
    return PrismConfig.from_dict(
        merged_config,
        schema=MultiEnvConfig,
        resolve_secrets=True,
    )


# =============================================================================
# Main Example
# =============================================================================


def main():
    """Demonstrate multi-environment configuration loading."""

    print("=" * 70)
    print("Multi-Environment Configuration Example (prism-config v2.0.0)")
    print("=" * 70)
    print()

    # -------------------------------------------------------------------------
    # Step 1: Determine environment
    # -------------------------------------------------------------------------
    env = os.getenv("APP_ENV", "development")
    config_dir = Path(__file__).parent

    print(f"Step 1: Loading configuration for environment: {env}")
    print(f"  Config directory: {config_dir}")
    print()

    # -------------------------------------------------------------------------
    # Step 2: Load configuration
    # -------------------------------------------------------------------------
    print("Step 2: Loading and merging configuration files...")
    config = load_config_for_env(env, config_dir)
    print(f"  Loaded: base.yaml + {env}.yaml")
    print()

    # -------------------------------------------------------------------------
    # Step 3: Display configuration
    # -------------------------------------------------------------------------
    print("Step 3: Configuration values for this environment:")
    print()

    print("  Application:")
    print(f"    Name: {config.app.name}")
    print(f"    Version: {config.app.version}")
    print(f"    Environment: {config.app.environment}")
    print()

    print("  Database:")
    print(f"    Host: {config.database.host}")
    print(f"    Name: {config.database.name}")
    print(f"    Pool Size: {config.database.pool_size}")
    print()

    print("  Cache:")
    print(f"    Host: {config.cache.host}")
    print(f"    TTL: {config.cache.ttl}s")
    print()

    print("  Logging:")
    print(f"    Level: {config.logging.level}")
    print()

    print("  Feature Flags:")
    print(f"    Beta Features: {config.features.beta_features}")
    print(f"    Maintenance Mode: {config.features.maintenance_mode}")
    print(f"    Debug Mode: {config.features.debug_mode}")
    print()

    # -------------------------------------------------------------------------
    # Step 4: Show environment differences
    # -------------------------------------------------------------------------
    print("Step 4: Environment comparison:")
    print()
    print("  | Setting           | Development | Staging     | Production  |")
    print("  |-------------------|-------------|-------------|-------------|")
    print("  | database.host     | localhost   | staging-db  | prod-db     |")
    print("  | database.pool_size| 5           | 10          | 20          |")
    print("  | cache.ttl         | 300         | 600         | 3600        |")
    print("  | logging.level     | DEBUG       | INFO        | WARNING     |")
    print("  | beta_features     | true        | true        | false       |")
    print("  | debug_mode        | true        | false       | false       |")
    print()

    # -------------------------------------------------------------------------
    # Step 5: Display with neon dump
    # -------------------------------------------------------------------------
    print("Step 5: Full configuration display:")
    print()
    config.display()
    print()

    # -------------------------------------------------------------------------
    # Step 6: Usage patterns
    # -------------------------------------------------------------------------
    print("Step 6: Usage patterns:")
    print()
    print("""
    # Pattern 1: Environment variable selection
    import os
    from my_app.config import load_config_for_env

    env = os.getenv("APP_ENV", "development")
    config = load_config_for_env(env, config_dir)

    # Pattern 2: Using from_all with environment files
    from prism.config import PrismConfig

    config = PrismConfig.from_all(
        f"config/{env}.yaml",
        cli_args=sys.argv[1:],
        resolve_secrets=True,
    )

    # Pattern 3: Environment-aware initialization
    def init_app():
        config = load_config()

        if config.features.maintenance_mode:
            return MaintenanceApp()

        if config.features.debug_mode:
            enable_debugging()

        return App(config)

    # Pattern 4: Different log levels per environment
    import logging
    logging.basicConfig(level=getattr(logging, config.logging.level))
    """)

    print("=" * 70)
    print("Example complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
