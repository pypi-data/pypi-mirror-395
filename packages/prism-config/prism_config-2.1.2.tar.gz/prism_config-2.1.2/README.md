<div align="center">

```
    ██████╗ ██████╗ ██╗███████╗███╗   ███╗
    ██╔══██╗██╔══██╗██║██╔════╝████╗ ████║
    ██████╔╝██████╔╝██║███████╗██╔████╔██║
    ██╔═══╝ ██╔══██╗██║╚════██║██║╚██╔╝██║
    ██║     ██║  ██║██║███████║██║ ╚═╝ ██║
    ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝     ╚═╝

   ╔═══════════════════════════════╗
   ║  Configuration, Crystallized  ║
   ╚═══════════════════════════════╝
```

# 🔮 Prism Config

**Type-safe Python configuration with tiered loading, environment overrides, and secret resolution**

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://img.shields.io/pypi/v/prism-config.svg)](https://pypi.org/project/prism-config/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/lukeudell/prism-config/actions/workflows/test.yml/badge.svg)](https://github.com/lukeudell/prism-config/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/lukeudell/prism-config/branch/main/graph/badge.svg)](https://codecov.io/gh/lukeudell/prism-config)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

</div>

A modern Python configuration library that brings type safety, validation, and production-ready features to your applications. Built on Pydantic v2, prism-config makes configuration management simple, safe, and beautiful.

---

## ✨ Why Prism Config?

**🎯 For Developers:**
- Type-safe configuration with IDE autocomplete
- Clear error messages that help you fix issues fast
- Beautiful terminal output for debugging
- Works seamlessly with Docker, Kubernetes, and 12-factor apps

**🔒 For Production:**
- Secure secret resolution (ENV and FILE providers)
- Immutable configurations prevent runtime bugs
- 16KB+ value support for post-quantum cryptography
- Comprehensive testing (101 unit tests + 1,100+ property tests)

**⚡ For Performance:**
- <0.3ms YAML file loading
- <0.003ms dictionary loading
- Built-in caching for display operations
- Zero-overhead type validation via Pydantic

---

## 🚀 Quick Start

### Installation

```bash
pip install prism-config
```

### Basic Usage

```python
from prism.config import PrismConfig

# Load from YAML file
config = PrismConfig.from_file("config.yaml")

# Type-safe access with autocomplete
print(config.app.name)        # "my-app"
print(config.database.port)   # 5432 (int, not string!)

# Beautiful terminal display
config.display()
```

### Your First Config File

Create `config.yaml`:

```yaml
app:
  name: my-app
  environment: production

database:
  host: localhost
  port: 5432
  name: mydb
  password: REF::ENV::DB_PASSWORD  # Secret from environment
```

That's it! You now have type-safe, validated configuration.

---

## 📖 Complete Guide

### Table of Contents

1. [Loading Methods](#1-loading-methods)
2. [Environment Variables](#2-environment-variable-overrides)
3. [CLI Arguments](#3-cli-argument-overrides)
4. [Secret Resolution](#4-secret-resolution)
5. [Terminal Display](#5-beautiful-terminal-display)
6. [Custom Schemas (v2.0.0+)](#6-custom-schemas-v200)
7. [Advanced Features](#7-advanced-features)
8. [Error Handling](#8-error-handling)
9. [Integration Guide](#9-integration-guide-for-prism-libraries)

---

## 1. Loading Methods

Prism Config provides three primary loading methods:

### Load from Dictionary

Perfect for testing or programmatic configuration:

```python
from prism.config import PrismConfig

config_data = {
    "app": {
        "name": "my-app",
        "environment": "production"
    },
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "mydb"
    }
}

config = PrismConfig.from_dict(config_data)
print(config.app.name)  # "my-app"
```

### Load from YAML File

Most common for production use:

```python
from prism.config import PrismConfig

# From string path or Path object
config = PrismConfig.from_file("config.yaml")

# With all overrides applied
config = PrismConfig.from_file(
    "config.yaml",
    apply_env=True,        # Environment variables
    resolve_secrets=True   # Secret resolution
)
```

### Load from All Sources (Recommended)

Convenience method that applies full precedence chain:

```python
import sys
from prism.config import PrismConfig

# Automatically applies: CLI > Secrets > ENV > File
config = PrismConfig.from_all(
    "config.yaml",
    cli_args=sys.argv[1:]  # Pass CLI arguments
)
```

**Precedence Order:**
```
CLI Arguments  (highest priority)
    ↓
Secrets (REF:: resolution)
    ↓
Environment Variables
    ↓
YAML File Values
    ↓
Dictionary/Defaults  (lowest priority)
```

---

## 2. Environment Variable Overrides

Override any configuration value using environment variables - perfect for Docker and Kubernetes!

### Quick Example

```python
import os
from prism.config import PrismConfig

# Set environment variables
os.environ["APP_DATABASE__HOST"] = "prod-db.example.com"
os.environ["APP_DATABASE__PORT"] = "3306"

# Load with environment overrides
config = PrismConfig.from_file("config.yaml", apply_env=True)

print(config.database.host)  # "prod-db.example.com" (from env!)
print(config.database.port)  # 3306 (auto-converted to int)
```

### Environment Variable Format

```bash
# Pattern: APP_{SECTION}__{KEY}
# Double underscore (__) separates nested levels

export APP_APP__NAME="production-app"
export APP_APP__ENVIRONMENT="production"
export APP_DATABASE__HOST="prod.db.example.com"
export APP_DATABASE__PORT="5432"  # Strings are auto-converted
```

### Docker Example

**Dockerfile:**
```dockerfile
ENV APP_DATABASE__HOST=db.production.com
ENV APP_DATABASE__PORT=5432
ENV APP_APP__ENVIRONMENT=production
```

**Python code:**
```python
config = PrismConfig.from_file("config.yaml", apply_env=True)
# Automatically uses Docker environment variables!
```

### Features

- ✅ **Automatic Type Coercion** - Strings converted to correct types
- ✅ **Case Insensitive** - Both `APP_DATABASE__HOST` and `app_database__host` work
- ✅ **Safe by Default** - Only variables with `APP_` prefix are used
- ✅ **Custom Prefix** - Use your own: `env_prefix="MYAPP_"`
- ✅ **Deep Nesting** - Use `__` for any nesting level

---

## 3. CLI Argument Overrides

Override configuration at runtime with command-line arguments:

### Quick Example

```python
import sys
from prism.config import PrismConfig

# Pass CLI args (or use sys.argv[1:])
config = PrismConfig.from_file(
    "config.yaml",
    cli_args=["--database.port=9999", "--app.environment=staging"]
)

print(config.database.port)  # 9999 (from CLI)
```

### Supported Formats

Both dot and dash notation work:

```bash
# Dot notation (recommended)
python app.py --database.host=prod.example.com --database.port=5432

# Dash notation
python app.py --database-host=prod.example.com --database-port=5432
```

### Integration with argparse

```python
import argparse
from prism.config import PrismConfig

parser = argparse.ArgumentParser()
parser.add_argument("--database.host", help="Database host")
parser.add_argument("--database.port", type=int, help="Database port")
parser.add_argument("--app.environment", help="Environment")

args = parser.parse_args()

# Convert to prism-config format
cli_args = [f"--{k}={v}" for k, v in vars(args).items() if v is not None]

config = PrismConfig.from_file("config.yaml", apply_env=True, cli_args=cli_args)
```

### Features

- ✅ **Highest Precedence** - Overrides everything (env, secrets, files)
- ✅ **Automatic Type Coercion** - CLI strings converted to correct types
- ✅ **Dot or Dash Notation** - Use whichever you prefer
- ✅ **Safe by Default** - Invalid paths silently ignored

---

## 4. Secret Resolution

Securely manage secrets from environment variables or files using the `REF::` syntax.

### Quick Example

```python
import os
from prism.config import PrismConfig

# Set secret in environment
os.environ["DB_PASSWORD"] = "super-secret-pass"

config_data = {
    "database": {
        "password": "REF::ENV::DB_PASSWORD"  # Reference to secret
    }
}

config = PrismConfig.from_dict(config_data, resolve_secrets=True)
print(config.database.password)  # "super-secret-pass" (resolved!)
```

### Reference Format

```
REF::PROVIDER::KEY_PATH
```

- **REF::** - Prefix indicating a secret reference
- **PROVIDER** - Secret provider (ENV or FILE)
- **KEY_PATH** - Provider-specific path to secret

### ENV Provider

Read secrets from environment variables:

```yaml
# config.yaml
database:
  password: REF::ENV::DB_PASSWORD
  api_key: REF::ENV::API_KEY
```

```python
import os
os.environ["DB_PASSWORD"] = "my-password"
os.environ["API_KEY"] = "my-api-key"

config = PrismConfig.from_file("config.yaml", resolve_secrets=True)
```

### FILE Provider (Docker Secrets)

Read secrets from files:

```yaml
# config.yaml
database:
  password: REF::FILE::/run/secrets/db_password
  ssl_cert: REF::FILE::/run/secrets/ssl_cert
```

**docker-compose.yml:**
```yaml
version: '3.8'
services:
  app:
    image: my-app
    secrets:
      - db_password
      - ssl_cert
    volumes:
      - ./config.yaml:/app/config.yaml

secrets:
  db_password:
    file: ./secrets/db_password.txt
  ssl_cert:
    file: ./secrets/ssl_cert.pem
```

**Python code:**
```python
config = PrismConfig.from_file("config.yaml", resolve_secrets=True)
# Secrets automatically resolved from Docker secret files
```

### Kubernetes Secrets

```yaml
# kubernetes-deployment.yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
spec:
  containers:
  - name: app
    image: my-app
    volumeMounts:
    - name: secrets
      mountPath: /var/run/secrets
      readOnly: true
  volumes:
  - name: secrets
    secret:
      secretName: db-credentials
```

```yaml
# config.yaml
database:
  password: REF::FILE::/var/run/secrets/db-password
```

### Post-Quantum Cryptography (PQC) Support

Prism Config supports large values up to **16KB+** for post-quantum cryptographic keys:

```python
# Store large Kyber-1024 key (16KB)
config_data = {
    "database": {
        "encryption_key": "REF::FILE::/run/secrets/kyber1024_key"  # 16KB file
    }
}

config = PrismConfig.from_dict(config_data, resolve_secrets=True)
# Fully supports PQC keys!
```

### Features

- ✅ **ENV Provider** - Environment variable secrets
- ✅ **FILE Provider** - File-based secrets (Docker/Kubernetes)
- ✅ **Automatic Newline Stripping** - File content cleaned
- ✅ **16KB+ Value Support** - Ready for post-quantum crypto
- ✅ **Multiple Secrets** - Resolve many secrets in one config
- ✅ **Mixed Providers** - Use ENV and FILE together
- ✅ **Fail-Fast** - Clear errors for missing secrets

---

## 5. Beautiful Terminal Display

Visualize your configuration with the "Neon Dump" - a vaporwave-inspired terminal display:

### Basic Usage

```python
from prism.config import PrismConfig

config = PrismConfig.from_file("config.yaml")
config.display()  # Shows banner + colored table
```

**Output:**
```
    CONFIGURATION LOADED

╔═══════════════════════════════╦══════════════════════════╗
║ Configuration Key              ║ Value                    ║
╠═══════════════════════════════╬══════════════════════════╣
║ 🌐  app.environment            ║ production               ║
║ 🌐  app.name                   ║ my-app                   ║
║ 💾  database.host              ║ localhost                ║
║ 💾  database.name              ║ mydb                     ║
║ 💾  database.password          ║ [🔒 REDACTED]            ║
║ 💾  database.port              ║ 5432                     ║
╚═══════════════════════════════╩══════════════════════════╝
```

### Get Table as String

```python
# Get formatted table without banner
table_output = config.dump()
print(table_output)

# Or save to file
with open("config-output.txt", "w") as f:
    f.write(config.dump())
```

### Show Secrets (v2.1.0+)

For debugging purposes, you can disable secret redaction:

```python
# Show actual secret values (use with caution!)
config.display(redact_secrets=False)

# Or get unredacted dump as string
table = config.dump(redact_secrets=False)
```

⚠️ **Warning**: Only use `redact_secrets=False` in secure development environments. Never expose secrets in logs or shared outputs.

### Disable Colors

```python
# Explicitly disable
config.display(use_color=False)

# Or via environment variable
import os
os.environ["NO_COLOR"] = "1"
config.display()  # Auto-detects
```

### Customize Theme

Create `prism-palette.toml`:

```toml
[theme]
name = "Custom Theme"

[colors]
header_bg = 197      # Hot pink
header_fg = 231      # White
key_color = 51       # Cyan
value_color = 183    # Light purple
border_color = 213   # Pink
secret_color = 196   # Red

[box_style]
style = "double"     # single, double, rounded, bold

[emojis]
app = "🌐"
database = "💾"
api = "🔌"
```

### Features

- ✅ **Automatic Secret Redaction** - Passwords/tokens hidden
- ✅ **ANSI 256-Color Support** - Beautiful on modern terminals
- ✅ **Box-Drawing Characters** - Professional table rendering
- ✅ **Category Emojis** - Visual categorization
- ✅ **Customizable Themes** - Full theme configuration
- ✅ **NO_COLOR Support** - Respects standard conventions

---

## 6. Custom Schemas (v2.0.0+)

Define your own configuration structure with full type safety and IDE autocomplete.

### Why Custom Schemas?

- **Type Safety**: IDE knows the types of all your configuration values
- **Autocomplete**: Full IntelliSense support for your custom sections
- **Validation**: Pydantic validates your configuration at load time
- **Documentation**: Your schema documents your configuration structure

### Quick Example

```python
from prism.config import PrismConfig, BaseConfigSection, BaseConfigRoot

# Define custom sections
class AuthConfig(BaseConfigSection):
    jwt_secret: str
    token_expiry: int = 3600
    enable_refresh: bool = True

class RateLimitConfig(BaseConfigSection):
    requests_per_minute: int = 100
    burst_size: int = 20

# Create your root configuration
class MyAppConfig(BaseConfigRoot):
    app: AppConfig           # Built-in
    database: DatabaseConfig # Built-in
    auth: AuthConfig         # Custom!
    rate_limit: RateLimitConfig

# Load with your schema
config = PrismConfig.from_file("config.yaml", schema=MyAppConfig)

# Full type safety!
config.auth.jwt_secret        # str
config.auth.token_expiry      # int
config.rate_limit.burst_size  # int
```

### Flexible Mode (No Schema)

Don't know your configuration structure upfront? Use flexible mode:

```python
# Accept ANY configuration structure
config = PrismConfig.from_file("config.yaml", strict=False)

# Access any nested path
config.my_custom_section.nested.value
config.analytics.providers.google.tracking_id
```

### Hybrid Mode (Typed + Flexible)

Combine type safety for core settings with flexibility for extensions:

```python
class MyConfig(BaseConfigRoot):
    app: AppConfig           # Typed, validated
    database: DatabaseConfig # Typed, validated

    model_config = {"extra": "allow"}  # Allow additional sections

config = PrismConfig.from_file("config.yaml", schema=MyConfig)
config.app.name              # Typed access
config.plugin_config.option  # Also works (flexible)
```

### Custom Emoji Registration

Register emojis for your custom sections in the display:

```python
from prism.config import register_emoji

register_emoji("auth", "🔑")
register_emoji("rate_limit", "⏱️")
register_emoji("my_custom_section", "🎯")

config.display()  # Uses your custom emojis!
```

See the [examples/](examples/) directory for complete working examples:
- **[06-fastapi](examples/06-fastapi/)** - FastAPI with auth and rate limiting
- **[07-django](examples/07-django/)** - Django-style settings
- **[08-microservice](examples/08-microservice/)** - Multiple backends
- **[09-multi-env](examples/09-multi-env/)** - Environment-specific configs
- **[10-flexible](examples/10-flexible/)** - Catch-all flexible mode

See the [Migration Guide](docs/migration-v2.md) for upgrading from v1.x.

---

## 7. Advanced Features

### Configuration Freezing (Immutability)

All configurations are **immutable by default**:

```python
config = PrismConfig.from_file("config.yaml")

# Attempting to modify raises an error
try:
    config._config.app.name = "modified"  # ❌ Raises ValidationError
except Exception as e:
    print("Configuration is immutable!")
```

**Benefits:**
- Prevents accidental runtime changes
- Thread-safe by design
- Catches bugs early
- Ensures configuration integrity

### Export & Serialization

Export configuration to various formats:

```python
from prism.config import PrismConfig

config = PrismConfig.from_file("config.yaml")

# Export to dictionary
config_dict = config.to_dict()
safe_dict = config.to_dict(redact_secrets=True)  # With redaction

# Export to YAML
yaml_str = config.to_yaml()
config.to_yaml_file("output.yaml")
config.to_yaml_file("safe.yaml", redact_secrets=True)  # With redaction

# Export to JSON
json_str = config.to_json()
config.to_json_file("output.json")
config.to_json_file("safe.json", redact_secrets=True)  # With redaction
```

**Use Cases:**
- Share configs with teammates (secrets redacted)
- Generate configuration templates
- Archive configuration snapshots
- Convert between formats

### Configuration Diffing

Compare configurations to detect changes:

```python
from prism.config import PrismConfig

# Load two configs
config_v1 = PrismConfig.from_file("config-v1.yaml")
config_v2 = PrismConfig.from_file("config-v2.yaml")

# Get differences as dict
diff = config_v1.diff(config_v2)
print(diff)
# {
#     "app.name": {"old": "app-v1", "new": "app-v2"},
#     "database.host": {"old": "localhost", "new": "prod.example.com"}
# }

# Get human-readable diff
print(config_v1.diff_str(config_v2))
```

**Output:**
```
Configuration Differences:

app.name:
  - Old: app-v1
  + New: app-v2

database.host:
  - Old: localhost
  + New: prod.example.com
```

**Use Cases:**
- Detect configuration drift between environments
- Validate changes before deployment
- Audit configuration history
- Debug configuration issues

---

## 8. Error Handling

Prism Config provides clear, actionable error messages:

### Exception Types

All exceptions inherit from `PrismConfigError`:

```python
from prism.config import PrismConfig
from prism.config.exceptions import (
    PrismConfigError,              # Base exception
    ConfigFileNotFoundError,        # File not found
    ConfigParseError,               # YAML parsing failed
    ConfigValidationError,          # Validation failed
    SecretResolutionError,          # Secret resolution failed
    SecretProviderNotFoundError,    # Unknown provider
    InvalidSecretReferenceError     # Invalid REF:: syntax
)

# Catch all prism-config errors
try:
    config = PrismConfig.from_file("config.yaml")
except PrismConfigError as e:
    print(f"Configuration error: {e}")
```

### Example Error Messages

**Missing File:**
```
Configuration file not found: /path/to/config.yaml
  Searched at: /absolute/path/to/config.yaml
  Suggestion: Check if the file exists and the path is correct
```

**YAML Syntax Error:**
```
Failed to parse configuration file: config.yaml
  Line 5
  Reason: YAML syntax error
  Suggestion: Check YAML syntax and file encoding
```

**Validation Error:**
```
Configuration validation failed for field: database.port
  Expected type: int
  Actual type: str
  Actual value: 'not_a_number'
  Suggestion: Check configuration schema and value types
```

**Secret Resolution Error:**
```
Failed to resolve secret: ENV::DATABASE_PASSWORD
  Reason: Environment variable not found
  Suggestion: Set environment variable 'DATABASE_PASSWORD' or check variable name
```

### Type Safety

Prism Config includes full type hints and `py.typed` marker:

```bash
# Verify types with mypy
mypy your_code.py

# Verify with pyright
pyright your_code.py
```

---

## 9. Integration Guide for Prism Libraries

**For Claude Code and developers building other prism libraries:** This section shows you exactly how to integrate prism-config into your prism library.

### Step 1: Install Prism Config

```bash
pip install prism-config
```

Or add to your `pyproject.toml`:

```toml
[project]
dependencies = [
    "prism-config>=1.0.0,<2.0.0",
]
```

### Step 2: Define Your Configuration Schema

Create a configuration module for your library (e.g., `your_library/config.py`):

```python
from pydantic import BaseModel, Field
from prism.config import PrismConfig as BasePrismConfig

class YourLibraryConfig(BaseModel):
    """Configuration specific to your library."""

    feature_enabled: bool = Field(default=True, description="Enable main feature")
    timeout: int = Field(default=30, description="Operation timeout in seconds")
    api_endpoint: str = Field(..., description="API endpoint URL")
    api_key: str = Field(..., description="API authentication key")

    model_config = {
        "frozen": True,  # Immutable
        "extra": "forbid"  # Reject unknown fields
    }

class AppConfig(BaseModel):
    """Application-level configuration."""

    name: str = Field(..., description="Application name")
    environment: str = Field(..., description="Environment (dev, staging, prod)")

    model_config = {"frozen": True}

class DatabaseConfig(BaseModel):
    """Database configuration."""

    host: str = Field(default="localhost", description="Database host")
    port: int = Field(default=5432, description="Database port")
    name: str = Field(..., description="Database name")
    password: str | None = Field(default=None, description="Database password")

    model_config = {"frozen": True}

class ConfigRoot(BaseModel):
    """Root configuration combining all sections."""

    app: AppConfig
    database: DatabaseConfig
    your_library: YourLibraryConfig  # Your library's config section

    model_config = {
        "frozen": True,
        "extra": "forbid",
        "validate_assignment": True
    }

class YourLibraryPrismConfig(BasePrismConfig):
    """
    Prism Config for YourLibrary.

    This extends the base PrismConfig with your library's configuration schema.

    Usage:
        >>> config = YourLibraryPrismConfig.from_file("config.yaml")
        >>> print(config.your_library.api_endpoint)
        >>> print(config.database.host)
    """

    def __init__(self, config_root: ConfigRoot):
        """Initialize with custom ConfigRoot."""
        # Store the config root that includes your library's config
        self._config = config_root

    @property
    def your_library(self) -> YourLibraryConfig:
        """Access your library's configuration."""
        return self._config.your_library

    # Inherit all loading methods from BasePrismConfig:
    # - from_dict()
    # - from_file()
    # - from_all()
    # - to_dict(), to_yaml(), to_json()
    # - diff(), display(), etc.
```

### Step 3: Create Your Configuration File

Create `config.yaml` in your project:

```yaml
app:
  name: your-app
  environment: production

database:
  host: localhost
  port: 5432
  name: yourdb
  password: REF::ENV::DB_PASSWORD  # Secret from environment

your_library:  # Your library's configuration section
  feature_enabled: true
  timeout: 60
  api_endpoint: https://api.example.com
  api_key: REF::FILE::/run/secrets/api_key  # Secret from file
```

### Step 4: Load and Use Configuration

In your library's main module:

```python
from your_library.config import YourLibraryPrismConfig

def initialize_library(config_path: str = "config.yaml"):
    """Initialize your library with configuration."""

    # Load configuration with all features
    config = YourLibraryPrismConfig.from_all(
        config_path,
        cli_args=sys.argv[1:]  # Optional CLI args
    )

    # Access your library's configuration
    if config.your_library.feature_enabled:
        print(f"Feature enabled with timeout: {config.your_library.timeout}")

    # Access shared configuration (app, database)
    print(f"App: {config.app.name}")
    print(f"Database: {config.database.host}:{config.database.port}")

    # Display configuration (with secrets redacted)
    config.display()

    return config

# Usage
config = initialize_library("config.yaml")

# Use configuration throughout your library
api_client = APIClient(
    endpoint=config.your_library.api_endpoint,
    api_key=config.your_library.api_key,
    timeout=config.your_library.timeout
)

db_connection = Database(
    host=config.database.host,
    port=config.database.port,
    name=config.database.name,
    password=config.database.password
)
```

### Step 5: Testing Your Configuration

Create tests for your configuration:

```python
import pytest
from your_library.config import YourLibraryPrismConfig

def test_config_loading():
    """Test basic configuration loading."""
    config_data = {
        "app": {"name": "test-app", "environment": "testing"},
        "database": {"host": "localhost", "port": 5432, "name": "testdb"},
        "your_library": {
            "feature_enabled": True,
            "timeout": 30,
            "api_endpoint": "https://test.example.com",
            "api_key": "test-key"
        }
    }

    config = YourLibraryPrismConfig.from_dict(config_data)

    assert config.your_library.feature_enabled is True
    assert config.your_library.timeout == 30
    assert config.database.host == "localhost"

def test_config_with_secrets():
    """Test secret resolution."""
    import os
    os.environ["API_KEY"] = "secret-key-123"

    config_data = {
        "app": {"name": "test-app", "environment": "testing"},
        "database": {"host": "localhost", "port": 5432, "name": "testdb"},
        "your_library": {
            "feature_enabled": True,
            "timeout": 30,
            "api_endpoint": "https://test.example.com",
            "api_key": "REF::ENV::API_KEY"  # Secret reference
        }
    }

    config = YourLibraryPrismConfig.from_dict(config_data, resolve_secrets=True)

    assert config.your_library.api_key == "secret-key-123"

def test_config_validation():
    """Test that invalid config is rejected."""
    config_data = {
        "app": {"name": "test-app", "environment": "testing"},
        "database": {"host": "localhost", "port": "not-a-number", "name": "testdb"},
        "your_library": {
            "feature_enabled": True,
            "timeout": 30,
            "api_endpoint": "https://test.example.com",
            "api_key": "test-key"
        }
    }

    with pytest.raises(Exception):  # Will raise ConfigValidationError
        YourLibraryPrismConfig.from_dict(config_data)
```

### Step 6: Documentation for Your Users

Document configuration for your library's users:

```markdown
# Configuration

YourLibrary uses [prism-config](https://github.com/lukeudell/prism-config) for type-safe configuration management.

## Quick Start

Create `config.yaml`:

\`\`\`yaml
app:
  name: my-app
  environment: production

database:
  host: localhost
  port: 5432
  name: mydb
  password: REF::ENV::DB_PASSWORD

your_library:
  feature_enabled: true
  timeout: 60
  api_endpoint: https://api.example.com
  api_key: REF::FILE::/run/secrets/api_key
\`\`\`

Load in your code:

\`\`\`python
from your_library import YourLibraryPrismConfig

config = YourLibraryPrismConfig.from_file("config.yaml", resolve_secrets=True)
\`\`\`

## Configuration Options

### `your_library` Section

- `feature_enabled` (bool): Enable the main feature (default: true)
- `timeout` (int): Operation timeout in seconds (default: 30)
- `api_endpoint` (str): API endpoint URL (required)
- `api_key` (str): API authentication key (required)

### Environment Variables

Override any setting:

\`\`\`bash
export APP_YOUR_LIBRARY__TIMEOUT=120
export APP_YOUR_LIBRARY__FEATURE_ENABLED=false
\`\`\`

### Secrets

Use `REF::ENV::` or `REF::FILE::` for secrets:

\`\`\`yaml
your_library:
  api_key: REF::ENV::API_KEY          # From environment variable
  ssl_cert: REF::FILE::/run/secrets/cert  # From Docker secret
\`\`\`

See [prism-config documentation](https://github.com/lukeudell/prism-config) for more features.
```

### Key Integration Points

✅ **Extend BasePrismConfig**: Inherit all loading methods
✅ **Add Your Schema**: Create Pydantic models for your config section
✅ **Use ConfigRoot**: Combine app, database, and your config
✅ **Support Secrets**: Use REF:: syntax for sensitive values
✅ **Enable Overrides**: Support ENV and CLI overrides
✅ **Test Thoroughly**: Test loading, validation, and secrets
✅ **Document Well**: Show users how to configure your library

---

## 📊 Features Summary

### Core Features

| Feature | Status | Description |
|---------|--------|-------------|
| Dictionary Loading | ✅ | Load config from Python dicts |
| YAML File Loading | ✅ | Load config from YAML files |
| Environment Overrides | ✅ | Override with `APP_SECTION__KEY` env vars |
| CLI Arguments | ✅ | Override with `--section.key=value` args |
| Secret Resolution | ✅ | ENV and FILE providers with `REF::` syntax |
| Type Safety | ✅ | Pydantic v2 validation with type hints |
| Immutability | ✅ | Frozen models prevent runtime changes |
| Beautiful Display | ✅ | Vaporwave-inspired terminal output |
| Secret Redaction | ✅ | Auto-hide passwords in display/export |
| Export (YAML/JSON) | ✅ | Export to multiple formats |
| Configuration Diffing | ✅ | Compare configs, detect changes |
| PQC Support | ✅ | 16KB+ values for quantum-safe keys |
| Custom Exceptions | ✅ | Clear error messages with suggestions |
| Type Checking | ✅ | PEP 561 compliant with `py.typed` |

### Testing & Quality

- **101 unit tests** covering all features
- **1,100+ property-based tests** via Hypothesis
- **6 cross-language parity tests** for behavioral consistency
- **86% code coverage** with detailed reports
- **Zero linter errors** (Ruff)
- **Type-checked** (mypy, pyright)

---

## 📈 Project Status

**Version:** 2.1.1 (Production Ready)

**Completed:**
- ✅ All development iterations (100%)
- ✅ Custom schemas and flexible mode (v2.0.0)
- ✅ Secret unredaction option (v2.1.0)
- ✅ Comprehensive documentation with examples
- ✅ Structured error metadata for observability (v2.1.1)
- ✅ Full test coverage (318 tests)
- ✅ GitHub Actions CI/CD
- ✅ PyPI package published
- ✅ Production-ready code quality

---

## 🛠️ Development

### Setup

```bash
# Clone repository
git clone https://github.com/lukeudell/prism-config.git
cd prism-config

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -e ".[dev]"
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/prism/config --cov-report=term-missing

# Run specific test file
pytest tests/test_loader.py -v

# Run parity tests
python tests/parity/test_parity.py
```

### Run Benchmarks

```bash
# Performance benchmarks
python -m benchmarks.bench_loader

# Profiling
python -m benchmarks.profile_loader
```

### Project Structure

```
prism-config/
├── src/prism/config/
│   ├── __init__.py         # Public API
│   ├── loader.py           # PrismConfig class
│   ├── models.py           # Pydantic models
│   ├── providers.py        # Secret providers
│   ├── display.py          # Terminal display
│   ├── exceptions.py       # Custom exceptions
│   └── py.typed            # Type marker
├── tests/
│   ├── test_*.py           # 11 test files
│   └── parity/             # Cross-language parity tests
├── examples/               # 10 complete examples
├── docs/                   # Documentation
│   ├── CODEX.md            # Technical design guide
│   ├── RELEASE_NOTES.md    # Release announcements
│   └── migration-v2.md     # v1.x to v2.x migration guide
├── CHANGELOG.md            # Version history
└── pyproject.toml          # Project metadata
```

---

## 📚 Documentation

- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes
- **[docs/CODEX.md](docs/CODEX.md)** - Technical design and architecture guide
- **[docs/RELEASE_NOTES.md](docs/RELEASE_NOTES.md)** - Release announcements
- **[docs/migration-v2.md](docs/migration-v2.md)** - v1.x to v2.x migration guide
- **[examples/](examples/)** - 10 complete usage examples

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with:
- [Pydantic v2](https://docs.pydantic.dev/) - Data validation and settings management
- [PyYAML](https://pyyaml.org/) - YAML parsing
- [Hypothesis](https://hypothesis.readthedocs.io/) - Property-based testing

Inspired by:
- 12-factor app configuration principles
- Docker and Kubernetes secret management patterns
- Post-quantum cryptography readiness

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/lukeudell/prism-config/issues)
- **Discussions**: [GitHub Discussions](https://github.com/lukeudell/prism-config/discussions)
- **Documentation**: [README.md](README.md)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

---

<div align="center">

**🔮 Built with precision and care by the Prism Config team 🔮**

**Production-ready • Type-safe • Developer-friendly**

</div>
