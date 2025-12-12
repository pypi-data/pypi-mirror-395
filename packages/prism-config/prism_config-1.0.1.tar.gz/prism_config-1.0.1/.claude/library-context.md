# 🧱 prism-config - Library Context

> **Parent Context:** Read `00-PRISM-OVERVIEW.md` first for project-wide context.

---

## Library Identity

- **Name:** prism-config
- **Icon:** 🔮
- **Tagline:** "Typed, tiered configuration with secret resolution"
- **Position:** Foundation layer (no dependencies on other Prism libraries)
- **Version:** 0.1.0 (currently in development)

---

## Purpose

Provides a **single source of truth** for application configuration with:

1. **Strict typing** - Catch config errors at load time, not runtime
2. **Tiered loading** - Defaults → File → Env → CLI (12-factor app compliant)
3. **Secret resolution** - `REF::PROVIDER::KEY` syntax for external secrets
4. **PQC readiness** - Supports large values (up to 16KB for quantum-safe keys)
5. **Beautiful output** - "Neon Dump" config table on startup

---

## What This Library Does

### Core Features

#### 1. Configuration Loading
```python
# From dict (in-memory)
config = PrismConfig.from_dict({
    "app": {"name": "my-app", "environment": "dev"},
    "database": {"host": "localhost", "port": 5432}
})

# From YAML file
config = PrismConfig.from_file("config.yaml")

# From all sources (precedence: defaults < file < env < cli)
config = PrismConfig.from_all(
    file="config.yaml",
    env_prefix="APP_",
    cli_args=sys.argv[1:]
)
```

#### 2. Type Safety (Pydantic Models)
```python
# Access is fully typed
config.app.name          # str
config.database.port     # int (not string!)
config.database.enabled  # bool

# Invalid types caught immediately
config = PrismConfig.from_dict({
    "database": {"port": "not-a-number"}  # ❌ ValidationError
})
```

#### 3. Secret Resolution
```yaml
# config.yaml
database:
  host: localhost
  username: admin
  password: REF::ENV::DB_PASSWORD       # Resolved from environment
  ssl_cert: REF::FILE::/run/secrets/cert.pem  # Resolved from file
```

```python
# In code, secrets are already resolved
config.database.password  # Returns actual password, not "REF::..."
```

#### 4. The Neon Dump
```python
config.display()  # Prints beautiful startup table

# Output:
# ╔═══════════════════════════════════════════════════════╗
# ║              🔮 PRISM CONFIG LOADED 🔮                ║
# ╠═══════════════════════════════════════════════════════╣
# ║ Key                    │ Value                        ║
# ╟────────────────────────┼──────────────────────────────╢
# ║ 💾 database.host       │ localhost                    ║
# ║ 💾 database.port       │ 5432                         ║
# ║ 🔒 database.password   │ [🔒 REDACTED]                ║
# ╚═══════════════════════════════════════════════════════╝
```

---

## What This Library Does NOT Do

❌ **Hot-reload** - Config is immutable after load (restart to reload)  
❌ **Validation logic** - Use custom Pydantic validators for business rules  
❌ **Encryption at rest** - Secrets are resolved, not encrypted  
❌ **Distributed config** - No Consul/etcd integration (use FILE provider)  
❌ **Schema migration** - Config structure changes require code changes  

---

## Architecture

### Module Structure

```
src/prism/config/
├── __init__.py          # Public API exports
├── loader.py            # PrismConfig class (main entry point)
├── models.py            # Pydantic models (AppConfig, DatabaseConfig, etc.)
├── providers.py         # Secret providers (ENV, FILE, VAULT)
├── display.py           # Neon Dump rendering
└── exceptions.py        # Custom exceptions
```

### Key Classes

#### `PrismConfig` (loader.py)
**Responsibility:** Main configuration loader and accessor

**Methods:**
- `from_dict(data: dict) -> PrismConfig`
- `from_file(path: str | Path) -> PrismConfig`
- `from_env(prefix: str = "APP_") -> dict`
- `from_args(args: list[str]) -> dict`
- `from_all(...) -> PrismConfig`
- `display() -> None` (prints Neon Dump)
- `to_dict() -> dict` (exports config, secrets redacted)

#### `ConfigRoot` (models.py)
**Responsibility:** Root Pydantic model defining config structure

**Sections:**
- `app: AppConfig` - Application metadata
- `database: DatabaseConfig` - Database connection info
- (More sections added by user as needed)

#### `SecretProvider` (providers.py)
**Responsibility:** Protocol for resolving external secrets

**Implementations:**
- `EnvSecretProvider` - Reads from environment variables
- `FileSecretProvider` - Reads from filesystem
- `VaultSecretProvider` - Reads from HashiCorp Vault (future)

---

## Design Decisions

### Why Pydantic?
- ✅ **Runtime validation** with excellent error messages
- ✅ **Type coercion** (string "5432" → int 5432)
- ✅ **JSON Schema generation** (auto-documentation)
- ✅ **Performance** (Pydantic v2 is Rust-based, very fast)

### Why Tiered Loading?
Follows **12-Factor App** methodology:
1. Code has sensible defaults (hardcoded in models)
2. Config file overrides defaults (local development)
3. Env vars override config file (Docker/K8s deployments)
4. CLI args override everything (one-off operations)

### Why `REF::` Syntax?
- ✅ **Grep-able** - Easy to find all secret references
- ✅ **Language-agnostic** - Same syntax in Java and Python
- ✅ **Explicit** - No magic, clear what's a secret vs plain value
- ✅ **Tooling-friendly** - Can validate before runtime

### Why Immutable Config?
- ✅ **Thread-safe** by default
- ✅ **Predictable** behavior (no surprise changes)
- ✅ **Simpler** code (no watchers, no locks)
- ❌ **Trade-off:** Must restart to reload (acceptable for our use case)

---

## Dependencies

### Production
- `pydantic>=2.0.0` - Data validation and typing
- `pyyaml>=6.0.0` - YAML parsing

### Development
- `pytest>=7.4.0` - Test runner
- `pytest-cov>=4.1.0` - Coverage reporting
- `pytest-mock>=3.11.1` - Mocking utilities
- `hypothesis>=6.82.0` - Property-based testing
- `ruff>=0.1.0` - Linting and formatting
- `mypy>=1.5.0` - Static type checking

### Optional (for specific providers)
- `hvac>=1.0.0` - HashiCorp Vault client (for VaultSecretProvider)

---

## Exports (What Other Libraries Can Import)

```python
from prism.config import (
    PrismConfig,           # Main configuration class
    SecretProvider,        # Protocol for custom providers
    register_provider,     # Register custom secret provider
    ConfigValidationError, # Exception for validation failures
)
```

### Usage by Other Prism Libraries

**prism-view:**
```python
from prism.config import PrismConfig

config = PrismConfig.from_file("config.yaml")
log_level = config.logging.level  # "INFO", "DEBUG", etc.
```

**prism-guard:**
```python
from prism.config import PrismConfig

config = PrismConfig.from_file("config.yaml")
jwt_secret = config.security.jwt_secret  # Resolved from REF::ENV::...
```

---

## Imports (What This Library Depends On)

**None.** This is the foundation library.

---

## Configuration Schema

The default schema (extensible by users):

```python
class AppConfig(BaseModel):
    """Application-level configuration."""
    name: str
    environment: str  # "dev", "staging", "prod"
    version: str = "0.1.0"
    debug: bool = False

class DatabaseConfig(BaseModel):
    """Database connection configuration."""
    host: str = "localhost"
    port: int = 5432
    name: str
    username: str = "postgres"
    password: str  # Can be REF::ENV::DB_PASSWORD
    ssl_enabled: bool = False

class ConfigRoot(BaseModel):
    """Root configuration model."""
    app: AppConfig
    database: DatabaseConfig
    
    model_config = {
        "extra": "forbid",  # Reject unknown fields
        "validate_assignment": True,
    }
```

Users extend this for their needs:

```python
# In user's application
from prism.config.models import ConfigRoot
from pydantic import BaseModel

class RedisConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379

class MyAppConfig(ConfigRoot):
    redis: RedisConfig  # Add new section

config = PrismConfig.from_file("config.yaml", model=MyAppConfig)
```

---

## Testing Strategy

### Test Pyramid

1. **Unit Tests** (60%)
   - Test each function in isolation
   - Mock external dependencies
   - Fast (<1ms per test)

2. **Integration Tests** (30%)
   - Test combinations (file loading + secret resolution)
   - Use real file I/O, real env vars
   - Medium speed (10-50ms per test)

3. **Property Tests** (10%)
   - Test with random inputs (Hypothesis)
   - Find edge cases we didn't think of
   - Slow but thorough (100-1000 examples)

### The Golden Path Test

**File:** `tests/test_golden_path.py`

This is the **ONE test** that proves the library works end-to-end.

```python
def test_golden_path():
    """
    Load config from YAML with:
    - File-based values
    - Environment variable overrides
    - Secret resolution
    - Display the Neon Dump
    
    If this test passes, the library is functional.
    """
    # Setup
    config_file = create_temp_config()
    os.environ["APP_DATABASE_HOST"] = "prod.db.example.com"
    os.environ["DB_PASSWORD"] = "super-secret"
    
    # Act
    config = PrismConfig.from_all(file=config_file, env_prefix="APP_")
    
    # Assert
    assert config.app.name == "test-app"
    assert config.database.host == "prod.db.example.com"  # Env override
    assert config.database.password == "super-secret"     # Secret resolved
    
    # Visual verification (manual inspection)
    config.display()
```

### Coverage Requirements

- **Overall:** 100% of implemented features
- **Uncovered code:** Only future placeholders (clearly marked with `# TODO`)
- **Critical paths:** 100% (config loading, secret resolution, error handling)

---

## Error Handling

### Custom Exceptions

```python
class ConfigError(Exception):
    """Base exception for all config errors."""
    pass

class ConfigFileNotFoundError(ConfigError):
    """Config file doesn't exist."""
    # Error message includes: full path, current directory, suggestions

class ConfigValidationError(ConfigError):
    """Config failed Pydantic validation."""
    # Error message includes: field name, expected type, actual value

class SecretResolutionError(ConfigError):
    """Failed to resolve a REF:: reference."""
    # Error message includes: provider name, key path, underlying error
```

### Error Message Quality

All errors must be **actionable**:

❌ **Bad:** `"Invalid config"`

✅ **Good:**
```
ConfigValidationError: Invalid value for 'database.port'
  Expected: int
  Got: "not-a-number" (str)
  
  Suggestion: Ensure database.port is a number in config.yaml (line 12)
```

---

## Performance Characteristics

### Benchmarks (Target)

| Operation | Target | Measured |
|-----------|--------|----------|
| Load small config (<1KB) | <10ms | TBD |
| Load large config (1MB) | <100ms | TBD |
| Resolve ENV secret | <1ms | TBD |
| Resolve FILE secret | <5ms | TBD |
| Display Neon Dump | <50ms | TBD |

### Optimization Strategies

- ✅ **Lazy resolution** - Secrets resolved only when accessed (future)
- ✅ **Caching** - Parsed YAML cached in memory
- ✅ **Pydantic v2** - Rust-based, much faster than v1

---

## Security Considerations

### Secrets Never Logged
```python
# ❌ NEVER do this:
logger.info(f"Database password: {config.database.password}")

# ✅ Automatic redaction:
logger.info(f"Config: {config}")  # Password shows as [🔒 REDACTED]
```

### Secrets Not in Version Control
```gitignore
# .gitignore
config.local.yaml
*.secret.yaml
.env
```

### Secrets Not in Error Messages
```python
try:
    config = PrismConfig.from_file("config.yaml")
except ConfigValidationError as e:
    # Error message NEVER includes actual secret values
    print(e)  # "Field 'database.password' failed validation"
              # (Not: "Field 'database.password' with value 'abc123' failed")
```

---

## Extension Points

### Custom Secret Providers

```python
from prism.config import SecretProvider, register_provider

class VaultSecretProvider:
    def __init__(self, vault_url: str, token: str):
        self.client = hvac.Client(url=vault_url, token=token)
    
    def resolve(self, key_path: str) -> str:
        return self.client.secrets.kv.v2.read_secret_version(path=key_path)
    
    def supports_rotation(self) -> bool:
        return True
    
    def max_value_size(self) -> int:
        return 1024 * 1024  # 1MB

# Register it
register_provider("VAULT", VaultSecretProvider(
    vault_url="https://vault.example.com",
    token=os.getenv("VAULT_TOKEN")
))

# Now you can use it in config:
# database:
#   password: REF::VAULT::/secret/db/password
```

### Custom Config Sections

```python
from prism.config.models import ConfigRoot
from pydantic import BaseModel

class MyCustomConfig(BaseModel):
    feature_flag_enabled: bool = False
    timeout_seconds: int = 30

class MyAppConfig(ConfigRoot):
    custom: MyCustomConfig

# Use the extended model
config = PrismConfig.from_file("config.yaml", model=MyAppConfig)
print(config.custom.feature_flag_enabled)
```

---

## Current Status

### Completed (Iteration 1)
- ✅ Project scaffolding
- ✅ Virtual environment setup
- ✅ Pydantic models defined
- ✅ `from_dict()` implementation
- ✅ Type validation
- ✅ Error handling (basic)
- ✅ Test infrastructure
- ✅ Documentation (README, CODEX)

### In Progress (Iteration 2)
- 🚧 YAML file loading
- 🚧 File error handling
- 🚧 YAML parse error handling

### Not Started
- 📋 Environment variable override
- 📋 CLI argument parsing
- 📋 Secret resolution system
- 📋 Neon Dump rendering
- 📋 PQC stress testing
- 📋 Property-based testing
- 📋 Performance optimization

---

## Common Tasks

### Running Tests
```bash
# All tests
pytest -v

# With coverage
pytest --cov

# Specific test file
pytest tests/test_loader.py -v

# Specific test
pytest tests/test_loader.py::test_from_dict -v

# Watch mode (requires pytest-watch)
ptw
```

### Code Quality
```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type check
mypy src/

# All quality checks
ruff check . && mypy src/ && pytest --cov
```

### Manual Testing
```python
# Create a test script: manual_test.py
from prism.config import PrismConfig

config = PrismConfig.from_dict({
    "app": {"name": "manual-test", "environment": "dev"},
    "database": {"host": "localhost", "port": 5432, "name": "testdb"}
})

print(config.app.name)
print(config.database.port)
print(config)
```

```bash
python manual_test.py
```

---

## Troubleshooting

### Import Errors
**Problem:** `ModuleNotFoundError: No module named 'prism'`

**Solution:**
```bash
# Make sure you're in the venv
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate      # Mac/Linux

# Install in editable mode
pip install -e .
```

### Test Failures
**Problem:** Tests pass locally but fail in CI

**Solution:** Check for:
- Environment-specific paths (use `tmp_path` fixture)
- Timezone differences (use UTC)
- Random data (use fixed seeds in tests)

### Coverage Drops
**Problem:** Coverage decreased after adding code

**Solution:**
- Did you add tests for the new code?
- Are there unreachable branches? (remove them)
- Is it a future placeholder? (mark with `# pragma: no cover`)

---

## Next Steps

See `todo.md` for the complete task list.

**Current:** Iteration 2 - YAML File Loading  
**Next Task:** Task 2.1 - Write test for YAML loading

---

## Questions? Check These Resources

1. **Design questions:** `../../.claude/01-design-principles.md`
2. **Architecture questions:** `../../.claude/02-architecture.md`
3. **API usage:** `README.md`
4. **Implementation details:** `CODEX.md`
5. **Cross-language patterns:** `../../.claude/parity-tests.md`

---

**Last Updated:** 2025-12-03  
**Library Version:** 0.1.0 (in development)