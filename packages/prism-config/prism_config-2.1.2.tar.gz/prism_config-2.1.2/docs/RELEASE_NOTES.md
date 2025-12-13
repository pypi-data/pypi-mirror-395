# prism-config Release Notes

All notable releases are documented here. For the complete version history, see [CHANGELOG.md](../CHANGELOG.md).

---

## v2.1.2 - Namespace Package Fix (2025-12-08)

### Highlights

Fixes namespace package compatibility when both prism-config and prism-view are installed together.

### Bug Fixes

- **Added `src/prism/__init__.py`** for explicit namespace package support
  - Resolves `ModuleNotFoundError: No module named 'prism.config'` when prism-view is also installed
  - Both packages now use consistent explicit namespace packages (PEP 420)

### Background

When using multiple packages under the same namespace (`prism.*`), Python requires consistent handling:
- Either ALL packages omit `__init__.py` in the namespace folder (implicit)
- Or ALL packages include it (explicit)

Since prism-view uses explicit namespace packages, prism-config now matches.

### Testing

- **318 tests passing**
- Verified compatibility with prism-view v1.0.0

---

## v2.1.1 - Structured Error Metadata (2025-12-06)

### Highlights

Version 2.1.1 adds comprehensive error metadata for integration with logging and observability systems like prism-view.

### New Features

- **`ErrorCode`** enum with standardized PRISM-XXXX error codes
- **`Severity`** enum with logging levels (debug, info, warning, error, critical)
- **UTC timestamps** on all exceptions
- **`to_dict()`** method for JSON-serializable structured logging
- **`with_context()`** method for adding correlation/trace IDs

```python
from prism.config import PrismConfig, ErrorCode, Severity

try:
    config = PrismConfig.from_file("missing.yaml")
except PrismConfigError as e:
    # Structured logging
    print(e.to_dict())
    # {
    #   "error_code": "PRISM-1001",
    #   "severity": "error",
    #   "message": "Configuration file not found...",
    #   "timestamp": "2025-12-06T...",
    #   "context": {...}
    # }

    # Add correlation context
    e.with_context(correlation_id="abc-123")
```

### Testing

- **318 tests passing**
- All existing functionality verified

---

## v2.1.0 - Secret Visibility & Emoji Fixes (2025-12-06)

### Highlights

Version 2.1.0 adds developer-friendly features for debugging and fixes visual alignment issues in the terminal output.

### New Features

#### Secret Visibility Option

New `redact_secrets` parameter for `dump()` and `display()` methods:

```python
# Show actual secret values (use with caution!)
config.display(redact_secrets=False)

# Or get unredacted dump as string
table = config.dump(redact_secrets=False)
```

#### Version Display in Banner

The Neon Dump banner now shows the prism-config version:

```
    CONFIGURATION LOADED  (v2.1.0)
```

### Bug Fixes

- Fixed table column alignment for emojis with variation selectors (e.g., ⏱️, 🖥️)
- Updated `display_width()` to handle Unicode variation selectors correctly

### Testing

- **297 tests passing**
- All existing functionality verified

---

## v2.0.0 - Custom Schemas & Flexible Mode (2025-12-05)

### Highlights

A major release introducing **custom schemas** and **flexible mode** while maintaining **100% backward compatibility** with v1.x!

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
```

### Dynamic Emoji Registration (NEW!)

Register custom emojis for beautiful terminal output:

```python
from prism.config import register_emoji
register_emoji("payments", "💳")
register_emoji("analytics", "📊")

config.display()  # Uses your custom emojis!
```

### What's New

#### New Classes
- **`BaseConfigSection`** - Base class for custom configuration sections
- **`BaseConfigRoot`** - Base class for custom root configurations
- **`DynamicConfig`** - Dot-notation access to arbitrary structures

#### New Functions
- **`register_emoji(name, emoji)`** - Register custom section emoji
- **`unregister_emoji(name)`** - Remove custom emoji
- **`get_registered_emojis()`** - Get all registered emojis
- **`clear_registered_emojis()`** - Clear all registrations

#### New Parameters
| Method | Parameter | Description |
|--------|-----------|-------------|
| `from_dict()` | `schema=` | Custom schema class |
| `from_dict()` | `strict=` | Enable flexible mode (False) |
| `from_file()` | `schema=` | Custom schema class |
| `from_file()` | `strict=` | Enable flexible mode (False) |
| `from_all()` | `schema=` | Custom schema class |
| `from_all()` | `strict=` | Enable flexible mode (False) |

#### New Features
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

### Testing
- **297 tests** (up from 240 in v1.x)
- **8 new property-based tests** for custom schemas
- **35 v2.0.0 feature tests** for backward compatibility
- **14 performance benchmarks**

### Breaking Changes

**None!** Version 2.0.0 is fully backward compatible with v1.x.

---

## v1.0.0 - Production Release (2025-12-03)

### Highlights

The first production-ready release of prism-config, a modern Python configuration library.

### Features

- **Type-safe configuration** with Pydantic v2 validation
- **Tiered loading** - Dict, YAML files, environment variables, CLI arguments
- **Secret resolution** - REF::ENV:: and REF::FILE:: syntax
- **The Neon Dump** - Beautiful vaporwave-inspired terminal output
- **PQC support** - Handles 16KB+ post-quantum cryptography keys
- **Immutability** - Frozen configurations by default
- **Export/Diff** - YAML, JSON export with configuration diffing

### Testing
- **107 tests** (101 unit + 6 parity)
- **86% code coverage**
- **Property-based testing** with Hypothesis

### Development Iterations
1. Dict Loading
2. YAML File Loading
3. Environment Variable Overrides
4. CLI Argument Overrides
5. Secret Resolution (REF:: syntax)
6. The Neon Dump (Beautiful Terminal Output)
7. PQC Stress Testing (16KB+ values)
8. Property-Based Testing with Hypothesis
9. Advanced Features (Freeze, Export, Diff)
10. Performance & Optimization
11. Error Handling & Developer Experience
12. Documentation & Examples
13. Cross-Language Parity Testing
14. Packaging & Distribution

---

## Links

- **GitHub**: https://github.com/lukeudell/prism-config
- **PyPI**: https://pypi.org/project/prism-config/
- **Documentation**: https://github.com/lukeudell/prism-config#readme
- **Changelog**: [CHANGELOG.md](../CHANGELOG.md)
- **Migration Guide**: [migration-v2.md](migration-v2.md)
