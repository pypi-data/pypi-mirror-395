# 🔮 prism-config v2.0.0 Release Notes

**Release Date:** December 5, 2025

We're excited to announce **prism-config v2.0.0**, a major release introducing **custom schemas** and **flexible mode** while maintaining **100% backward compatibility** with v1.x!

## ✨ Highlights

### Custom Schemas (NEW!)

Define type-safe configuration schemas for any structure:

```python
from prism.config import PrismConfig, BaseConfigSection, BaseConfigRoot

class AuthConfig(BaseConfigSection):
    jwt_secret: str
    token_expiry: int = 3600

class MyAppConfig(BaseConfigRoot):
    app: AppConfig
    database: DatabaseConfig
    auth: AuthConfig  # Your custom section!

config = PrismConfig.from_dict(data, schema=MyAppConfig)
print(config.auth.jwt_secret)  # Full type safety and IDE autocomplete!
```

### Flexible Mode (NEW!)

Load any configuration structure without defining a schema:

```python
config = PrismConfig.from_file("config.yaml", strict=False)
config.analytics.providers.google.tracking_id  # Just works!
config.my_custom_section.nested.value  # Any path!
```

### Dynamic Emoji Registration (NEW!)

Register custom emojis for beautiful terminal output:

```python
from prism.config import register_emoji
register_emoji("payments", "💳")
register_emoji("analytics", "📊")
register_emoji("auth", "🔑")

config.display()  # Uses your custom emojis!
```

## 🚀 What's New in v2.0.0

### New Classes
- **`BaseConfigSection`** - Base class for custom configuration sections
- **`BaseConfigRoot`** - Base class for custom root configurations
- **`DynamicConfig`** - Dot-notation access to arbitrary structures

### New Functions
- **`register_emoji(name, emoji)`** - Register custom section emoji
- **`unregister_emoji(name)`** - Remove custom emoji
- **`get_registered_emojis()`** - Get all registered emojis
- **`clear_registered_emojis()`** - Clear all registrations

### New Parameters
| Method | Parameter | Description |
|--------|-----------|-------------|
| `from_dict()` | `schema=` | Custom schema class |
| `from_dict()` | `strict=` | Enable flexible mode (False) |
| `from_file()` | `schema=` | Custom schema class |
| `from_file()` | `strict=` | Enable flexible mode (False) |
| `from_all()` | `schema=` | Custom schema class |
| `from_all()` | `strict=` | Enable flexible mode (False) |

### New Features
- **50+ built-in emoji mappings** for common config keys
- **Hierarchical emoji detection** for nested keys
- **Custom secret keywords** and regex patterns
- **Configurable display depth**

### New Examples
1. **Example 06**: FastAPI with custom schemas (auth, rate limiting, CORS)
2. **Example 07**: Django-style settings configuration
3. **Example 08**: Microservice with multiple backends
4. **Example 09**: Multi-environment configuration
5. **Example 10**: Catch-all flexible mode

## 📊 Testing

- **297 tests** (up from 240 in v1.x)
- **8 new property-based tests** for custom schemas
- **35 v2.0.0 feature tests** for backward compatibility
- **14 performance benchmarks**
- **All tests passing** ✅

## ⚠️ Breaking Changes

**None!** Version 2.0.0 is fully backward compatible:

- Your existing `from_dict()`, `from_file()`, `from_all()` calls work unchanged
- Built-in `app` and `database` sections work as before
- All v1.x APIs continue to work identically

## 🔄 Upgrade Guide

### Simple Upgrade
```bash
pip install --upgrade prism-config
```

### Your Existing Code Works!
```python
# This v1.x code works unchanged in v2.0.0
from prism.config import PrismConfig

config = PrismConfig.from_file("config.yaml")
print(config.app.name)
print(config.database.port)
```

### Try New Features
```python
# Add custom sections when you're ready
from prism.config import BaseConfigSection, BaseConfigRoot

class AuthConfig(BaseConfigSection):
    jwt_secret: str
    token_expiry: int = 3600

class MyConfig(BaseConfigRoot):
    app: AppConfig
    database: DatabaseConfig
    auth: AuthConfig

config = PrismConfig.from_file("config.yaml", schema=MyConfig)
```

## 📚 Documentation

- **[Migration Guide](docs/migration-v2.md)** - Detailed v1.x to v2.0.0 upgrade
- **[README](README.md)** - Updated with custom schema section
- **[Examples](examples/)** - 10 complete examples (5 new for v2.0.0)
- **[CHANGELOG](CHANGELOG.md)** - Complete change history

## 📦 Package Information

- **Package Name:** `prism-config`
- **Version:** 2.0.0
- **Python:** >=3.10
- **Dependencies:** Pydantic >=2.0.0, PyYAML >=6.0.0
- **License:** MIT

## 🎯 Use Cases

### FastAPI with Auth
```python
class AuthConfig(BaseConfigSection):
    jwt_secret: str
    token_expiry: int = 3600

class APIConfig(BaseConfigRoot):
    app: AppConfig
    database: DatabaseConfig
    auth: AuthConfig

config = PrismConfig.from_file("config.yaml", schema=APIConfig)
```

### Microservice with Multiple Databases
```python
class DatabaseConfig(BaseConfigSection):
    host: str
    port: int = 5432
    name: str

class ServiceConfig(BaseConfigRoot):
    app: AppConfig
    primary_db: DatabaseConfig
    replica_db: DatabaseConfig
    analytics_db: DatabaseConfig
```

### Plugin System
```python
# No schema needed!
config = PrismConfig.from_file("plugins.yaml", strict=False)
config.plugins.analytics.tracking_id
config.plugins.payments.gateway
```

## 📊 Stats

- **Iterations Completed:** 20/20 (100%)
- **Lines of Code:** ~3,500 (production + tests)
- **Test Coverage:** 86%
- **Tests Passing:** 297/297
- **Examples:** 10 complete examples
- **Documentation:** Comprehensive guides and API docs

## 🔮 What's Next

Future releases may include:
- Additional secret providers (AWS Secrets Manager, HashiCorp Vault)
- Configuration hot-reload
- Schema generation from YAML
- TOML file support

## 📖 Links

- **GitHub**: https://github.com/lukeudell/prism-config
- **PyPI**: https://pypi.org/project/prism-config/
- **Documentation**: https://github.com/lukeudell/prism-config#readme
- **Changelog**: https://github.com/lukeudell/prism-config/blob/main/CHANGELOG.md

## 💬 Feedback

Found a bug? Have a feature request? We'd love to hear from you!

- **Issues**: https://github.com/lukeudell/prism-config/issues
- **Discussions**: https://github.com/lukeudell/prism-config/discussions

---

**Happy Configuring!** 🔮

The prism-config Team
