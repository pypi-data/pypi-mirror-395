# Example 09: Multi-Environment Configuration (v2.0.0)

This example demonstrates managing configuration across multiple environments (development, staging, production) with base configuration and environment-specific overrides.

## Features Demonstrated

- Base configuration with shared defaults
- Environment-specific override files
- Configuration merging strategy
- Environment selection via `APP_ENV` variable
- Different settings per environment

## Files

- `base.yaml` - Shared configuration across all environments
- `development.yaml` - Development-specific overrides
- `staging.yaml` - Staging-specific overrides
- `production.yaml` - Production-specific overrides
- `multi_env_example.py` - Python code demonstrating environment loading

## Prerequisites

```bash
# Install prism-config
cd prism-config
pip install -e .
```

## Running the Example

```bash
# Development (default)
python examples/09-multi-env/multi_env_example.py

# Staging
APP_ENV=staging DB_PASSWORD=stg_pass CACHE_PASSWORD=cache_pass \
    python examples/09-multi-env/multi_env_example.py

# Production
APP_ENV=production DB_PASSWORD=prod_pass CACHE_PASSWORD=cache_pass \
    python examples/09-multi-env/multi_env_example.py
```

## Configuration Strategy

### Base Configuration (base.yaml)

Contains shared defaults used by all environments:

```yaml
app:
  name: my-application
  version: "1.0.0"

database:
  host: localhost
  port: 5432
  pool_size: 5

features:
  beta_features: false
  debug_mode: false
```

### Environment Override (e.g., production.yaml)

Contains only the values that differ from base:

```yaml
app:
  environment: production

database:
  host: prod-db.internal
  pool_size: 20

logging:
  level: WARNING

features:
  beta_features: false
```

### Resulting Configuration

Base values are used unless overridden:

| Setting           | Base      | Production Override | Result    |
|-------------------|-----------|---------------------|-----------|
| database.host     | localhost | prod-db.internal    | prod-db.internal |
| database.port     | 5432      | (not set)           | 5432      |
| database.pool_size| 5         | 20                  | 20        |
| logging.level     | INFO      | WARNING             | WARNING   |

## Environment Comparison

| Setting           | Development | Staging     | Production  |
|-------------------|-------------|-------------|-------------|
| database.host     | localhost   | staging-db  | prod-db     |
| database.pool_size| 5           | 10          | 20          |
| cache.ttl         | 300         | 600         | 3600        |
| logging.level     | DEBUG       | INFO        | WARNING     |
| beta_features     | true        | true        | false       |
| debug_mode        | true        | false       | false       |

## Implementation

### Configuration Loading

```python
def load_config_for_env(env: str, config_dir: Path) -> PrismConfig:
    import yaml

    # Load base config
    with open(config_dir / "base.yaml") as f:
        base_config = yaml.safe_load(f)

    # Load environment-specific config
    with open(config_dir / f"{env}.yaml") as f:
        env_config = yaml.safe_load(f)

    # Merge with env overriding base
    merged_config = merge_configs(base_config, env_config)

    return PrismConfig.from_dict(
        merged_config,
        schema=MultiEnvConfig,
        resolve_secrets=True,
    )
```

### Usage in Application

```python
import os

# Determine environment
env = os.getenv("APP_ENV", "development")

# Load appropriate configuration
config = load_config_for_env(env, config_dir)

# Use configuration
if config.features.debug_mode:
    enable_debugging()

if config.app.environment == "production":
    setup_production_logging()
```

## Best Practices

1. **Keep base.yaml minimal** - Only shared defaults
2. **Override only what changes** - Don't duplicate base values
3. **Use secrets in non-dev environments** - `REF::ENV::` references
4. **Feature flags per environment** - Enable beta in dev/staging only
5. **Log levels appropriate to environment** - DEBUG for dev, WARNING for prod

## Alternative Approaches

### Single File with Environment Sections

```yaml
environments:
  development:
    database:
      host: localhost
  production:
    database:
      host: prod-db.internal
```

### Environment Variables Only

```bash
DATABASE__HOST=prod-db.internal python app.py
```

### Layered Configuration Files

```
config/
  base.yaml
  base.production.yaml  # Production base
  production.yaml       # Production overrides
```

## Next Steps

- See [10-flexible](../10-flexible/) for catch-all flexible configuration
