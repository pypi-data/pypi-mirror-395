# CODEX - Prism Config Python Implementation

**Design decisions, architecture, and implementation guide**

**Version:** 2.1.1 (Structured Error Metadata)
**Last Updated:** 2025-12-06
**Status:** Production Release

---

## Overview

Prism Config is a modern Python configuration library providing type-safe, validated configuration management with multiple loading sources, environment overrides, and secret resolution. Built on Pydantic v2 with a focus on developer experience and production readiness.

---

## Design Principles

### 1. Type Safety First
- Use Pydantic v2 models for all configuration schemas
- Leverage Python's type hints throughout (PEP 561 compliant)
- Fail fast on validation errors with clear, actionable messages
- Immutable configurations by default (frozen models)

### 2. Developer Experience
- Clear, actionable error messages with suggestions
- Beautiful terminal output with the "Neon Dump"
- Simple, intuitive API with minimal boilerplate
- Comprehensive documentation and examples

### 3. Production Ready
- Secure by default (`yaml.safe_load()`, secret redaction)
- 12-factor app compatible (environment variable overrides)
- Docker and Kubernetes ready (FILE provider for secrets)
- Post-quantum cryptography support (16KB+ values)

### 4. Test-Driven Development
- Comprehensive test coverage (101 unit tests + 6 parity tests)
- Property-based testing with Hypothesis (1,100+ test cases)
- Cross-language parity tests for behavioral consistency
- 86% code coverage across all modules

---

## Architecture

### Module Structure

```
src/prism/config/
├── __init__.py         # Public API exports (PrismConfig, exceptions)
├── loader.py           # Configuration loading logic (~500 LOC)
├── models.py           # Pydantic schema definitions (~180 LOC)
├── providers.py        # Secret resolution providers (~120 LOC)
├── display.py          # Neon Dump rendering (~430 LOC)
├── exceptions.py       # Custom exception hierarchy (~180 LOC)
└── py.typed            # PEP 561 type marker
```

### Data Flow

```
Input Source → Parse → Override Chain → Validation → Frozen Config
     ↓           ↓           ↓              ↓            ↓
   YAML       safe_load   CLI > Secrets  Pydantic    Immutable
   Dict                   > ENV > File    Models      Instance
   File
```

### Loading Precedence (Highest to Lowest)

1. **CLI Arguments** - `--section.key=value` (runtime overrides)
2. **Secret Resolution** - `REF::ENV::` or `REF::FILE::` (secure values)
3. **Environment Variables** - `APP_SECTION__KEY` (deployment config)
4. **YAML/Config Files** - `config.yaml` (application defaults)
5. **Dictionary/Code** - Direct dict input (testing/programmatic)

---

## Core Features

### 1. Multiple Loading Methods

**from_dict()** - Load from Python dictionary
```python
config = PrismConfig.from_dict(config_data)
```

**from_file()** - Load from YAML file
```python
config = PrismConfig.from_file("config.yaml", apply_env=True, resolve_secrets=True)
```

**from_all()** - Convenience method with full precedence chain
```python
config = PrismConfig.from_all("config.yaml", cli_args=sys.argv[1:])
```

### 2. Environment Variable Overrides

**Format:** `{PREFIX}{SECTION}__{KEY}`
- Default prefix: `APP_`
- Double underscore for nesting
- Case-insensitive matching
- Automatic type coercion

**Example:**
```bash
export APP_DATABASE__HOST=prod.example.com
export APP_DATABASE__PORT=5432
```

### 3. CLI Argument Overrides

**Formats:**
- Dot notation: `--database.host=value`
- Dash notation: `--database-host=value`

**Features:**
- Highest precedence in override chain
- Case-insensitive matching
- Automatic type coercion

### 4. Secret Resolution

**Syntax:** `REF::PROVIDER::KEY_PATH`

**Providers:**
- **ENV** - Environment variable secrets: `REF::ENV::DB_PASSWORD`
- **FILE** - File-based secrets: `REF::FILE::/run/secrets/db_password`

**Features:**
- Automatic newline stripping for FILE provider
- 16KB+ value support for PQC keys
- Clear error messages for missing secrets
- Extensible provider system

### 5. Beautiful Terminal Display

**The Neon Dump** - Vaporwave-inspired terminal output
- ANSI 256-color support
- Box-drawing characters (single, double, rounded, bold)
- Automatic secret redaction
- Customizable themes via `prism-palette.toml`
- NO_COLOR environment variable support

### 6. Immutability

All configurations are **frozen by default**:
- Prevents accidental runtime modifications
- Thread-safe by design
- Catches bugs early in development

### 7. Export & Serialization

Export to multiple formats with optional secret redaction:
- `to_dict()` - Python dictionary
- `to_yaml()` / `to_yaml_file()` - YAML format
- `to_json()` / `to_json_file()` - JSON format

### 8. Configuration Diffing

Compare configurations to detect changes:
- `diff()` - Returns dict of differences
- `diff_str()` - Human-readable diff output

---

## Implementation Details

### Type System (models.py)

**Pydantic Configuration:**
```python
model_config = {
    "frozen": True,              # Immutable
    "extra": "forbid",           # Reject unknown fields
    "validate_assignment": True  # Validate on changes
}
```

**Built-in Schema:**
- `AppConfig` - Application-level configuration
- `DatabaseConfig` - Database connection settings
- `ConfigRoot` - Root model combining all sections

**Custom Schema Support (v2.0.0+):**
- `BaseConfigSection` - Base class for custom config sections
- `BaseConfigRoot` - Base class for custom root schemas
- `DynamicConfig` - Schema-less configuration container
- `T = TypeVar("T", bound=BaseModel)` - Generic type for schema parameter

### Error Handling (exceptions.py)

**Exception Hierarchy:**
```
PrismConfigError (base)
├── ConfigFileNotFoundError
├── ConfigParseError
├── ConfigValidationError
├── SecretResolutionError
├── SecretProviderNotFoundError
├── InvalidSecretReferenceError
└── EnvironmentVariableError
```

**Features:**
- Context-rich error messages
- Actionable suggestions for resolution
- Original exceptions preserved via `raise from`
- Field paths extracted from Pydantic errors

### Secret Resolution (providers.py)

**Provider Interface:**
```python
class SecretProvider(Protocol):
    def resolve(self, key: str) -> str:
        """Resolve a secret value."""
        ...
```

**Built-in Providers:**
- `EnvSecretProvider` - Read from `os.environ`
- `FileSecretProvider` - Read from filesystem with newline stripping

**Registry:**
- `get_provider(name)` - Retrieve provider by name
- `register_provider(name, provider)` - Add custom provider

### Display System (display.py)

**Components:**
- `Palette` - Theme configuration (colors, box style, emojis)
- `dump()` - Generate formatted table string
- `display()` - Print banner + table with colors

**Palette Caching:**
- TOML palette files cached for performance
- 3x faster dump operations with caching

---

## Design Decisions

### Why Pydantic v2 over Dataclasses?

**Decision:** Use Pydantic v2 for schema definition

**Rationale:**
- Runtime validation with detailed error messages
- Automatic type coercion (string → int, etc.)
- Built-in serialization/deserialization
- Wide ecosystem adoption
- JSON Schema generation capability

**Trade-offs:**
- ✅ Superior validation and error messages
- ✅ More features out of the box
- ✅ Active development and community
- ❌ Additional dependency (but well-maintained)

### Why yaml.safe_load() over yaml.load()?

**Decision:** Use `yaml.safe_load()` exclusively

**Rationale:**
- **Security:** Prevents arbitrary code execution
- **Sufficient:** Handles all standard configuration data
- **Best Practice:** Industry standard for untrusted YAML

### Why Tiered Loading with Precedence?

**Decision:** Implement multiple loading methods with clear precedence chain

**Rationale:**
- **Flexibility:** Different deployment scenarios (dev, staging, prod)
- **12-Factor Apps:** Environment-based configuration
- **Industry Standard:** Matches Spring Boot, Django, etc.
- **Developer Intent:** CLI args have highest priority

**Precedence Order:**
1. CLI arguments (developer's immediate intent)
2. Secrets (secure, resolved values)
3. Environment variables (deployment-specific)
4. Config files (application defaults)

### Why Frozen Models (Immutability)?

**Decision:** Make all configuration models frozen by default

**Rationale:**
- **Safety:** Prevents accidental modifications at runtime
- **Thread-Safe:** No synchronization needed
- **Debugging:** Configuration state is predictable
- **Best Practice:** Configuration should be read-only after load

### Why REF:: Syntax for Secrets?

**Decision:** Use `REF::PROVIDER::KEY` syntax for secret references

**Rationale:**
- **Explicit:** Clear indication of secret resolution
- **Extensible:** Easy to add new providers
- **Standard:** Similar to URI schemes
- **Safe:** Secrets not exposed in config files

### Why Custom Exceptions?

**Decision:** Create custom exception hierarchy instead of using built-in exceptions

**Rationale:**
- **Clarity:** Specific error types for specific failures
- **Context:** Include relevant information (file path, field name, etc.)
- **Suggestions:** Provide actionable next steps
- **Catching:** Allow targeted exception handling

---

## Performance Characteristics

### Benchmarks (measured)

| Operation | Time | Notes |
|-----------|------|-------|
| from_dict() small | 0.002ms | Dictionary loading |
| from_file() YAML | 0.277ms | Includes file I/O |
| from_dict() large (1MB) | 0.002ms | Scales well |
| Secret resolution | +0.010ms | Per secret resolved |
| Env override | +0.030ms | Environment scan |
| dump() with cache | 0.083ms | Palette cached |
| dump() without cache | ~0.25ms | TOML parse overhead |

### Optimizations

- **Palette Caching:** TOML palette parsed once, cached for reuse
- **Lazy Imports:** Heavy dependencies imported only when needed
- **Minimal Overhead:** Pydantic validation is extremely fast
- **O(n) Complexity:** Linear with configuration size

---

## Testing Strategy

### Test Coverage

**Unit Tests (101 tests):**
- Iteration 1 (Dict): 3 tests
- Iteration 2 (YAML): 10 tests
- Iteration 3 (Env): 10 tests
- Iteration 4 (CLI): 11 tests
- Iteration 5 (Secrets): 13 tests
- Iteration 6 (Display): 11 tests
- Iteration 7 (PQC): 10 tests
- Iteration 8 (Property): 10 tests
- Iteration 9 (Advanced): 13 tests
- Iteration 10 (Performance): 10 tests
- Iteration 11 (Errors): 10 tests

**Property-Based Tests (1,100+ cases):**
- Using Hypothesis for randomized testing
- Validates invariants across random inputs
- Tests edge cases human testers miss

**Parity Tests (6 JSON tests):**
- Language-agnostic test definitions
- Ensures behavioral consistency
- Foundation for future language implementations

### Coverage Statistics

- **Overall:** 86%
- **loader.py:** 93%
- **models.py:** 100%
- **providers.py:** 78%
- **display.py:** 76%
- **exceptions.py:** 90%

---

## Code Quality Standards

### Type Hints
- All public methods have complete type hints
- PEP 561 compliant with `py.typed` marker
- Compatible with mypy and pyright

### Documentation
- Comprehensive docstrings with examples
- Google/NumPy style format
- Parameter descriptions and return types
- "See Also" sections for related methods

### Error Messages
- Include context (file paths, field names, line numbers)
- Suggest solutions ("Check if...", "Ensure that...")
- Use clear, non-technical language
- Preserve original exceptions for debugging

### Code Style
- Ruff for linting and formatting
- Line length: 100 characters
- PEP 8 conventions
- Zero linter errors

---

## Security Considerations

### YAML Loading
- ✅ Uses `yaml.safe_load()` to prevent code execution
- ✅ Validates file contents before parsing
- ✅ UTF-8 encoding by default

### Secret Management
- ✅ Secrets never logged or exposed in errors
- ✅ Automatic redaction in display/export
- ✅ FILE provider strips newlines securely
- ✅ Clear errors for missing secrets (no silent failures)

### Configuration Immutability
- ✅ Frozen models prevent runtime tampering
- ✅ No setter methods for configuration values
- ✅ Deep copies used during override application

---

## v2.0.0 Features

### Custom Schema Support

**BaseConfigSection and BaseConfigRoot:**
```python
from prism.config import BaseConfigSection, BaseConfigRoot

class AuthConfig(BaseConfigSection):
    jwt_secret: str
    token_expiry: int = 3600

class MyConfig(BaseConfigRoot):
    app: AppConfig
    database: DatabaseConfig
    auth: AuthConfig  # Custom!

config = PrismConfig.from_file("config.yaml", schema=MyConfig)
```

### Flexible Mode (strict=False)

Load any configuration structure without a schema:
```python
config = PrismConfig.from_file("config.yaml", strict=False)
config.any_section.any_nested.value  # Works!
```

### DynamicConfig

Schema-less configuration container with dot-notation access:
```python
from prism.config import DynamicConfig

data = {"auth": {"jwt": {"secret": "abc123"}}}
dynamic = DynamicConfig(data)
dynamic.auth.jwt.secret  # "abc123"
```

### Custom Emoji Registration

Register emojis for custom sections:
```python
from prism.config import register_emoji

register_emoji("auth", "🔑")
register_emoji("rate_limit", "⏱️")
```

### Enhanced Secret Detection

Custom secret keywords and patterns:
```python
palette = Palette(
    secret_keywords=["internal_token"],
    secret_patterns=[r".*_credential$"]
)
```

### Configurable Display Depth

Limit flattening depth for display:
```python
palette = Palette(max_depth=3)
```

## Future Enhancements (v2.1.0+)

### Potential Features
- Additional secret providers (AWS Secrets Manager, Vault, Azure Key Vault)
- Hot-reload support (watch config files for changes)
- Configuration validation UI (web-based editor)
- TOML and JSON config file support
- Config migration tools
- Encrypted config files
- Remote configuration stores

### Backward Compatibility
- v2.0.0 is fully backward compatible with v1.x
- Semantic versioning for all future releases
- Deprecation warnings before removal
- Migration guides for major version upgrades

---

## Integration Guide

### For Prism Libraries

When integrating prism-config into other prism libraries:

1. **Install Dependency:**
   ```toml
   [project]
   dependencies = ["prism-config>=1.0.0,<2.0.0"]
   ```

2. **Extend Base Config:**
   ```python
   from prism.config import PrismConfig as BasePrismConfig

   class YourLibraryConfig(BasePrismConfig):
       # Add your library's config section
       @property
       def your_library(self) -> YourLibraryConfigSection:
           return self._config.your_library
   ```

3. **Define Schema:**
   ```python
   class YourLibraryConfigSection(BaseModel):
       feature_enabled: bool = True
       timeout: int = 30
       api_key: str

       model_config = {"frozen": True}
   ```

4. **Use Configuration:**
   ```python
   config = YourLibraryConfig.from_file("config.yaml")
   if config.your_library.feature_enabled:
       # Use configuration
       api_client = APIClient(api_key=config.your_library.api_key)
   ```

---

## Version History

### v2.0.0 (2025-12-05) - Flexible Schema Support
- ✅ Custom schema support with `BaseConfigSection` and `BaseConfigRoot`
- ✅ Flexible mode with `strict=False` parameter
- ✅ `DynamicConfig` class for schema-free configuration
- ✅ Runtime emoji registration (`register_emoji`, etc.)
- ✅ Custom secret keywords and patterns in `Palette`
- ✅ `max_depth` parameter for display flattening
- ✅ Hierarchical emoji detection for nested sections
- ✅ 50+ new emoji mappings for common sections
- ✅ 5 new comprehensive examples (FastAPI, Django, etc.)
- ✅ Migration guide for v1.x users
- ✅ Full backward compatibility with v1.x
- ✅ 240+ tests passing

### v1.0.0 (2025-12-03) - Production Release
- ✅ All 14 development iterations complete
- ✅ 107 tests passing (101 unit + 6 parity)
- ✅ 86% code coverage
- ✅ Comprehensive documentation
- ✅ PyPI package ready
- ✅ GitHub Actions CI/CD
- ✅ Production-ready code quality

### Development Iterations (v1.x)
1. ✅ Dict Loading
2. ✅ YAML File Loading
3. ✅ Environment Variable Overrides
4. ✅ CLI Argument Overrides
5. ✅ Secret Resolution (REF:: syntax)
6. ✅ The Neon Dump (Beautiful Terminal Output)
7. ✅ PQC Stress Testing (16KB+ values)
8. ✅ Property-Based Testing with Hypothesis
9. ✅ Advanced Features (Freeze, Export, Diff)
10. ✅ Performance & Optimization
11. ✅ Error Handling & Developer Experience
12. ✅ Documentation & Examples
13. ✅ Cross-Language Parity Testing
14. ✅ Packaging & Distribution

### Development Iterations (v2.0.0)
15. ✅ Expanded Built-in Support (emoji mappings)
16. ✅ Generic Schema Support
17. ✅ Flexible/Catch-All Mode
18. ✅ Enhanced Display System
19. ✅ Documentation & Examples

---

## References

### Documentation
- [README.md](../README.md) - User documentation
- [CHANGELOG.md](../CHANGELOG.md) - Version history
- [RELEASE_NOTES.md](RELEASE_NOTES.md) - Release announcements
- [migration-v2.md](migration-v2.md) - Migration guide for v1.x to v2.x
- [examples/](../examples/) - 10 complete examples

### External Resources
- [Pydantic v2 Documentation](https://docs.pydantic.dev/)
- [PyYAML Documentation](https://pyyaml.org/)
- [12-Factor App Config](https://12factor.net/config)
- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)

---

**Maintained by:** Prism Config Team
**License:** MIT
**Repository:** https://github.com/lukeudell/prism-config
