# Changelog

All notable changes to prism-config will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.1] - 2025-12-06

### Added

#### Structured Error Metadata for Observability (v2.1.1+)
- **`ErrorCode`** enum with standardized PRISM-XXXX error codes:
  - File errors: PRISM-1001 to PRISM-1005
  - Validation errors: PRISM-2001 to PRISM-2004
  - Secret errors: PRISM-3001 to PRISM-3005
  - Environment errors: PRISM-4001 to PRISM-4002
  - General errors: PRISM-9999
- **`Severity`** enum with logging levels: debug, info, warning, error, critical
- **UTC timestamps** on all exceptions for time-based correlation
- **`to_dict()`** method for JSON-serializable structured logging output
- **`with_context()`** method for adding correlation/trace IDs
- **Enhanced context metadata** on all exception types

```python
from prism.config import PrismConfig, ErrorCode, Severity

try:
    config = PrismConfig.from_file("missing.yaml")
except PrismConfigError as e:
    # Structured logging (perfect for prism-view integration)
    print(e.to_dict())
    # {
    #   "error_code": "PRISM-1001",
    #   "severity": "error",
    #   "message": "Configuration file not found: missing.yaml",
    #   "timestamp": "2025-12-06T...",
    #   "context": {"file_path": "missing.yaml", ...},
    #   "suggestion": "Check if the file exists..."
    # }

    # Add correlation context
    e.with_context(correlation_id="abc-123", request_id="req-456")
```

---

## [2.1.0] - 2025-12-06

### Added

#### Secret Visibility Option (v2.1.0+)
- **`redact_secrets`** parameter for `dump()` and `display()` methods
- When set to `False`, shows actual secret values instead of `[REDACTED]`
- Useful for debugging in secure development environments

```python
# Show actual secret values (use with caution!)
config.display(redact_secrets=False)

# Or get unredacted dump as string
table = config.dump(redact_secrets=False)
```

⚠️ **Warning**: Only use `redact_secrets=False` in secure development environments. Never expose secrets in logs or production output.

### Fixed

#### Emoji Width Alignment
- Fixed table column alignment for emojis with variation selectors (e.g., ⏱️, 🖥️)
- Updated `display_width()` function to properly handle:
  - Variation selectors (VS1-VS16) as zero-width characters
  - Base characters followed by emoji variation selector (VS16/U+FE0F) as wide (2 columns)
  - Zero-width joiners and combining marks

---

## [2.0.0] - 2025-12-05

### 🎉 Major Release - Custom Schemas & Flexible Mode

Version 2.0.0 introduces powerful new features while maintaining **full backward compatibility** with v1.x code.

### Added

#### Custom Schemas (v2.0.0+)
- **`BaseConfigSection`** - Base class for defining custom configuration sections with type safety
- **`BaseConfigRoot`** - Base class for defining custom root configurations with multiple sections
- **Custom schema support** in `from_dict()`, `from_file()`, and `from_all()` via `schema=` parameter
- **IDE autocomplete** for custom sections with full type hints
- **Pydantic v2 validation** for all custom schema fields

```python
from prism.config import PrismConfig, BaseConfigSection, BaseConfigRoot

class AuthConfig(BaseConfigSection):
    jwt_secret: str
    token_expiry: int = 3600

class MyAppConfig(BaseConfigRoot):
    app: AppConfig
    database: DatabaseConfig
    auth: AuthConfig

config = PrismConfig.from_dict(data, schema=MyAppConfig)
print(config.auth.jwt_secret)  # Full type safety!
```

#### Flexible Mode (v2.0.0+)
- **`strict=False`** parameter for schema-free configuration loading
- **`DynamicConfig`** class for dot-notation access to arbitrary structures
- **No schema required** - load any YAML/dict structure without predefined schema
- **Deep nested access** via attribute notation (`config.any.nested.path`)

```python
config = PrismConfig.from_file("config.yaml", strict=False)
config.my_custom_section.nested.value  # Works without schema!
```

#### Dynamic Emoji Registration (v2.0.0+)
- **`register_emoji(section_name, emoji)`** - Register custom emojis for sections
- **`unregister_emoji(section_name)`** - Remove custom emoji registration
- **`get_registered_emojis()`** - Get all registered emojis
- **`clear_registered_emojis()`** - Clear all custom registrations
- **50+ built-in emoji mappings** for common section names (auth, cache, redis, etc.)
- **Hierarchical emoji detection** - Smart matching for nested config keys

```python
from prism.config import register_emoji
register_emoji("analytics", "📊")
register_emoji("payments", "💳")
```

#### Enhanced Secret Detection (v2.0.0+)
- **Custom secret keywords** via `Palette(secret_keywords=[...])`
- **Custom secret patterns** via `Palette(secret_patterns=[r"..."])`
- **Configurable display depth** via `Palette(max_depth=N)`

#### New Examples (v2.0.0+)
- **Example 06**: FastAPI with custom schemas (auth, rate limiting, CORS)
- **Example 07**: Django-style settings configuration
- **Example 08**: Microservice with multiple backends (databases, caches, queues)
- **Example 09**: Multi-environment configuration (dev/staging/prod)
- **Example 10**: Catch-all flexible configuration mode

#### Testing (v2.0.0+)
- **8 new property-based tests** for custom schemas and flexible mode
- **35 v2.0.0 feature tests** covering parity, backward compatibility, and real-world patterns
- **14 performance benchmarks** for loading, access, and memory efficiency
- **297 total tests** (up from 240 in v1.x)

### Documentation
- **Migration guide** (`docs/migration-v2.md`) for v1.x to v2.0.0 upgrade
- **Updated README** with Section 6: Custom Schemas
- **Updated CODEX.md** with v2.0.0 features
- **Updated examples README** with v2.0.0 examples section

### Breaking Changes

**None!** Version 2.0.0 is fully backward compatible with v1.x code:
- Existing `from_dict()`, `from_file()`, `from_all()` calls work unchanged
- Built-in `app` and `database` sections work as before
- All v1.x APIs continue to work identically

### Technical Details

#### New Exports
```python
from prism.config import (
    # Custom schemas
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

#### New Parameters
| Method | Parameter | Description |
|--------|-----------|-------------|
| `from_dict()` | `schema=` | Custom schema class |
| `from_dict()` | `strict=` | Enable flexible mode (False) |
| `from_file()` | `schema=` | Custom schema class |
| `from_file()` | `strict=` | Enable flexible mode (False) |
| `from_all()` | `schema=` | Custom schema class |
| `from_all()` | `strict=` | Enable flexible mode (False) |

---

## [1.1.0] - 2025-12-05

### Added
- **PRISM ASCII art banner** - Beautiful vaporwave-gradient ASCII art banner displayed on startup with pink-to-cyan color gradient

### Fixed
- **Emoji width alignment** - Fixed table column alignment issues caused by double-width emoji characters. Now uses proper Unicode width calculation to ensure borders align correctly
- **Neon Dump table formatting** - Added minimum column widths to prevent cramped output when configuration keys and values are short

---

## [1.0.0] - 2025-12-03

### 🎉 Initial Release

The first stable release of prism-config Python library with complete feature set!

### Added

#### Core Features
- **Type-safe configuration** using Pydantic v2 models
- **Multiple loading methods**: `from_dict()`, `from_file()`, `from_all()`
- **YAML file support** with secure `yaml.safe_load()`
- **Environment variable overrides** with double-underscore nesting (`APP_DATABASE__PORT`)
- **CLI argument overrides** with dot and dash notation
- **Secret resolution** with `REF::PROVIDER::KEY` syntax
  - ENV provider for environment variable secrets
  - FILE provider for Docker/Kubernetes secrets
- **Configuration precedence**: CLI args > Secrets > ENV vars > File values
- **Immutable configuration** (frozen Pydantic models)
- **Post-Quantum Cryptography support** (values up to 16KB)

#### Display & Export
- **Beautiful terminal output** ("Neon Dump") with ANSI colors
- **Automatic secret redaction** in display and export
- **Multiple export formats**: YAML, JSON, dict
- **Configuration diffing** to detect changes between configs
- **Customizable themes** via `prism-palette.toml`

#### Developer Experience
- **Custom exception hierarchy** with clear, actionable error messages
  - `ConfigFileNotFoundError` - Missing file with full path
  - `ConfigParseError` - YAML syntax errors with line numbers
  - `ConfigValidationError` - Type errors with field paths
  - `SecretResolutionError` - Secret resolution failures
- **Comprehensive docstrings** with usage examples
- **Type hints throughout** (PEP 561 compliant with `py.typed`)
- **IDE autocomplete support** via type annotations

#### Testing
- **101 unit tests** with 86% code coverage
- **Property-based tests** using Hypothesis (1,100+ randomized test cases)
- **PQC stress tests** validating large value support
- **6 cross-language parity tests** for behavioral consistency
- **13 advanced feature tests** (freezing, serialization, diffing)

#### Documentation
- **Comprehensive README** with ASCII logo and badges
- **5 practical examples** with full documentation:
  1. Basic dictionary configuration
  2. YAML file loading
  3. Environment variable overrides
  4. Secret resolution
  5. Complete Docker integration
- **API documentation** with detailed method docstrings
- **Parity test specification** (v1.0.0) for cross-language implementations

#### Performance
- **Benchmarking suite** for performance validation
- **File caching** support to avoid re-parsing YAML
- **Optimized secret resolution** with regex pattern caching
- **Efficient deep copy** operations

#### Deployment
- **Docker Compose** example with secrets
- **Kubernetes** deployment examples
- **12-factor app** compatible
- **Production-ready** configuration management

### Technical Details

#### Dependencies
- Python >=3.10
- Pydantic >=2.0.0, <3.0.0
- PyYAML >=6.0.0, <7.0.0

#### Development Dependencies
- pytest >=7.4.0
- pytest-cov >=4.1.0
- hypothesis >=6.82.0
- ruff >=0.1.0
- mypy >=1.5.0

#### Package Structure
```
src/prism/config/
├── __init__.py         # Public API exports
├── loader.py           # PrismConfig class (~500 LOC)
├── models.py           # Pydantic models (~180 LOC)
├── providers.py        # Secret providers (~120 LOC)
├── display.py          # Terminal output (~430 LOC)
├── exceptions.py       # Custom exceptions (~180 LOC)
└── py.typed            # PEP 561 marker
```

#### Git History
- 12+ commits following conventional commit format
- Complete iteration tracking (14 iterations)
- Clean, semantic commit messages

### Iterations Completed

1. ✅ Dict Loading - Basic configuration from dictionaries
2. ✅ YAML File Loading - File-based configuration
3. ✅ Environment Variable Override - 12-factor app support
4. ✅ CLI Arguments Override - Runtime configuration
5. ✅ Secret Resolution - Secure secret management
6. ✅ Neon Dump - Beautiful terminal output
7. ✅ PQC Stress Testing - Large value validation
8. ✅ Property-Based Testing - Hypothesis integration
9. ✅ Advanced Features - Freezing, export, diff
10. ✅ Performance & Optimization - Benchmarks and caching
11. ✅ Error Handling & Developer Experience - Custom exceptions
12. ✅ Documentation & Examples - Comprehensive guides
13. ✅ Cross-Language Parity Testing - Behavioral consistency
14. ✅ Packaging & Distribution - PyPI release preparation

### Breaking Changes
None - this is the initial release

### Security
- Uses `yaml.safe_load()` to prevent code execution
- Automatic secret redaction in display and export
- Secure by default (opt-in for environment overrides and secret resolution)
- No hardcoded secrets or credentials in examples

### Known Limitations
- Windows console may have Unicode display issues (set `PYTHONIOENCODING=utf-8`)
- FILE provider for secrets requires file system access
- Configuration schema is fixed (app + database sections)

### Migration Guide
Not applicable - this is the initial release. For users starting fresh:

```python
# Install
pip install prism-config

# Basic usage
from prism.config import PrismConfig

config = PrismConfig.from_file("config.yaml")
print(config.app.name)
print(config.database.port)
```

### Contributors
- Initial development and all 14 iterations
- 101 tests, 2,200+ lines of production code
- Comprehensive documentation and examples

### Links
- [GitHub Repository](https://github.com/lukeudell/prism-config)
- [Documentation](https://github.com/lukeudell/prism-config#readme)
- [Issue Tracker](https://github.com/lukeudell/prism-config/issues)
- [PyPI Package](https://pypi.org/project/prism-config/)

---

## How to Read This Changelog

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security fixes

For upgrade instructions, see the Migration Guide section in each release.

---

**Note**: This changelog follows [Keep a Changelog](https://keepachangelog.com/) format and [Semantic Versioning](https://semver.org/) principles.
