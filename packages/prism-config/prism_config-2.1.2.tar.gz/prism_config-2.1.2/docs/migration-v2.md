# Migration Guide: v1.x to v2.0.0

This guide helps you migrate from prism-config v1.x to v2.0.0. Version 2.0.0 introduces powerful new features while maintaining full backward compatibility.

## Quick Summary

**Good news:** v2.0.0 is fully backward compatible. Your existing code will work without changes.

**New in v2.0.0:**
- Custom schema support with `BaseConfigSection` and `BaseConfigRoot`
- Flexible mode with `strict=False` for schema-free loading
- Dynamic emoji registration for custom sections
- Enhanced secret detection with custom patterns
- Configurable display depth

## Breaking Changes

**None!** Version 2.0.0 is fully backward compatible with v1.x code.

## New Features Overview

### 1. Custom Schemas (Type Safety for Custom Sections)

**Before (v1.x):** Only `app` and `database` sections were supported.

```python
# v1.x - Limited to built-in sections
config = PrismConfig.from_file("config.yaml")
config.app.name        # Works
config.database.host   # Works
config.auth.jwt_secret # Error! No auth section
```

**After (v2.0.0):** Define custom schemas for any section.

```python
# v2.0.0 - Custom schemas for any structure
from prism.config import BaseConfigSection, BaseConfigRoot

class AuthConfig(BaseConfigSection):
    jwt_secret: str
    token_expiry: int = 3600

class MyConfig(BaseConfigRoot):
    app: AppConfig
    database: DatabaseConfig
    auth: AuthConfig  # Custom section!

config = PrismConfig.from_file("config.yaml", schema=MyConfig)
config.auth.jwt_secret  # Works with full type safety!
```

### 2. Flexible Mode (Schema-Free Loading)

**v2.0.0 only:** Load any configuration structure without a schema.

```python
# No schema needed - accepts any structure
config = PrismConfig.from_file("config.yaml", strict=False)

# Access any nested path
config.my_custom_section.nested.value
config.analytics.providers.google.tracking_id
```

### 3. Dynamic Emoji Registration

**v2.0.0 only:** Register emojis for custom sections.

```python
from prism.config import register_emoji

register_emoji("auth", "🔑")
register_emoji("cache", "⚡")
register_emoji("my_custom_section", "🎯")

config.display()  # Uses your custom emojis!
```

### 4. Enhanced Secret Detection

**v2.0.0 only:** Custom secret keywords and patterns.

```python
from prism.config import Palette

palette = Palette(
    secret_keywords=["internal_token", "private_key"],
    secret_patterns=[r".*_credential$", r"api_\w+_key"]
)

# Custom keywords are now redacted in display
```

## Migration Paths

### Path 1: No Changes Needed (Most Common)

If your code only uses the built-in `app` and `database` sections, no changes are needed.

```python
# This code works exactly the same in v1.x and v2.0.0
from prism.config import PrismConfig

config = PrismConfig.from_file("config.yaml")
print(config.app.name)
print(config.database.host)
```

### Path 2: Adding Custom Sections

If you have custom sections in your YAML that you want type-safe access to:

**Step 1:** Define your custom section classes.

```python
from prism.config import BaseConfigSection, BaseConfigRoot

class RedisConfig(BaseConfigSection):
    host: str = "localhost"
    port: int = 6379
    password: Optional[str] = None

class LoggingConfig(BaseConfigSection):
    level: str = "INFO"
    format: str = "json"
```

**Step 2:** Create a root config that includes your sections.

```python
class MyAppConfig(BaseConfigRoot):
    app: AppConfig
    database: DatabaseConfig
    redis: RedisConfig     # Your custom section
    logging: LoggingConfig # Another custom section
```

**Step 3:** Load with your schema.

```python
config = PrismConfig.from_file("config.yaml", schema=MyAppConfig)

# Full type safety and IDE autocomplete!
config.redis.host        # str
config.redis.port        # int
config.logging.level     # str
```

### Path 3: Using Flexible Mode

If you want to load arbitrary configuration without defining schemas:

```python
# Just add strict=False
config = PrismConfig.from_file("config.yaml", strict=False)

# Access any path - no schema needed
config.any_section.any_key.any_nested_value
```

### Path 4: Hybrid Mode (Typed + Flexible)

Combine type safety for core settings with flexibility for extensions:

```python
class MyConfig(BaseConfigRoot):
    app: AppConfig           # Typed
    database: DatabaseConfig # Typed

    model_config = {"extra": "allow"}  # Allow extra sections

config = PrismConfig.from_file("config.yaml", schema=MyConfig)
config.app.name              # Typed, validated
config.plugin_config.option  # Also works (flexible)
```

## API Changes Reference

### New Parameters

| Method | New Parameter | Description |
|--------|---------------|-------------|
| `from_dict()` | `schema=` | Custom schema class |
| `from_dict()` | `strict=` | Enable/disable flexible mode |
| `from_file()` | `schema=` | Custom schema class |
| `from_file()` | `strict=` | Enable/disable flexible mode |
| `from_all()` | `schema=` | Custom schema class |
| `from_all()` | `strict=` | Enable/disable flexible mode |

### New Exports

```python
from prism.config import (
    # New base classes
    BaseConfigSection,
    BaseConfigRoot,

    # Flexible mode
    DynamicConfig,

    # Emoji registration
    register_emoji,
    unregister_emoji,
    get_registered_emojis,
    clear_registered_emojis,
)
```

### New Palette Options

```python
from prism.config.display import Palette

palette = Palette(
    max_depth=3,                    # Limit display nesting
    secret_keywords=["my_secret"],  # Custom secret keywords
    secret_patterns=[r".*_key$"],   # Regex patterns for secrets
)
```

## Code Examples

### Before/After: Custom Configuration

**Before (v1.x) - Workaround:**
```python
# Had to access raw dict for custom sections
config = PrismConfig.from_file("config.yaml")
redis_host = config._config_root.model_extra.get("redis", {}).get("host")
```

**After (v2.0.0) - Clean solution:**
```python
class MyConfig(BaseConfigRoot):
    app: AppConfig
    database: DatabaseConfig
    redis: RedisConfig

config = PrismConfig.from_file("config.yaml", schema=MyConfig)
redis_host = config.redis.host  # Clean, typed access!
```

### Before/After: Dynamic Configuration

**Before (v1.x) - Not possible:**
```python
# No way to load arbitrary config without errors
config = PrismConfig.from_file("dynamic.yaml")  # ValidationError!
```

**After (v2.0.0) - Flexible mode:**
```python
config = PrismConfig.from_file("dynamic.yaml", strict=False)
config.any_section.any_value  # Works!
```

## Deprecation Timeline

There are no deprecations in v2.0.0. All v1.x APIs continue to work.

## Getting Help

- **Examples:** See the [examples/](../examples/) directory for complete working code
- **Issues:** Report problems at [GitHub Issues](https://github.com/lukeudell/prism-config/issues)
- **Documentation:** Full API docs in the main [README.md](../README.md)

## Changelog Highlights

### v2.0.0

- **Added:** Custom schema support with `BaseConfigSection` and `BaseConfigRoot`
- **Added:** Flexible mode with `strict=False` parameter
- **Added:** `DynamicConfig` class for schema-free configuration
- **Added:** Runtime emoji registration (`register_emoji`, etc.)
- **Added:** Custom secret keywords and patterns in `Palette`
- **Added:** `max_depth` parameter for display flattening
- **Added:** Hierarchical emoji detection for nested sections
- **Improved:** 50+ new emoji mappings for common sections
- **Improved:** Smart emoji detection with partial/keyword matching
- **Maintained:** Full backward compatibility with v1.x
