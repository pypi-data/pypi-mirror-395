# 🔮 prism-config v1.0.0 Release Notes

**Release Date:** December 3, 2025

We're thrilled to announce the first stable release of **prism-config**, a modern Python configuration library with type safety, tiered loading, and secret resolution!

## ✨ Highlights

### Type-Safe Configuration
Built on Pydantic v2 for runtime validation and IDE autocomplete:
```python
config = PrismConfig.from_file("config.yaml")
print(config.app.name)  # Type-safe access
print(config.database.port)  # Autocomplete works!
```

### Tiered Loading & Precedence
Load configuration from multiple sources with clear precedence:
```
CLI Arguments  (highest priority)
    ↓
Secrets (REF:: resolution)
    ↓
Environment Variables
    ↓
YAML Files
    ↓
Defaults  (lowest priority)
```

### Secret Resolution
Secure secret management with ENV and FILE providers:
```yaml
database:
  password: REF::ENV::DB_PASSWORD  # From environment
  ssl_cert: REF::FILE::/run/secrets/cert  # From Docker secret
```

### Beautiful Terminal Output
The "Neon Dump" with automatic secret redaction:
```python
config.display()  # Gorgeous ANSI color output
```

### Production-Ready
- **101 tests** with 86% coverage
- **Docker & Kubernetes** examples
- **12-factor app** compatible
- **PQC support** (values up to 16KB)
- **Clear error messages** with actionable suggestions

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

# Access configuration
print(f"App: {config.app.name}")
print(f"DB: {config.database.host}:{config.database.port}")

# Beautiful display
config.display()
```

### With All Features
```python
import sys
from prism.config import PrismConfig

# Load with environment overrides, CLI args, and secrets
config = PrismConfig.from_all(
    "config.yaml",
    cli_args=sys.argv[1:],
    resolve_secrets=True
)
```

## 📚 What's Included

### Core Features
- ✅ Type-safe configuration with Pydantic v2
- ✅ Multiple loading methods (dict, YAML, combined)
- ✅ Environment variable overrides (`APP_DATABASE__PORT`)
- ✅ CLI argument overrides (`--database.port=3306`)
- ✅ Secret resolution (ENV and FILE providers)
- ✅ Immutable configuration (frozen models)
- ✅ Post-Quantum Cryptography support (16KB values)

### Developer Experience
- ✅ Custom exceptions with clear error messages
- ✅ Comprehensive docstrings with examples
- ✅ Type hints throughout (PEP 561)
- ✅ IDE autocomplete support

### Display & Export
- ✅ Beautiful terminal output with colors
- ✅ Automatic secret redaction
- ✅ Export to YAML, JSON, dict
- ✅ Configuration diffing

### Testing
- ✅ 101 unit tests (86% coverage)
- ✅ Property-based tests (1,100+ cases)
- ✅ PQC stress tests
- ✅ Cross-language parity tests

### Documentation
- ✅ Comprehensive README
- ✅ 5 practical examples
- ✅ API documentation
- ✅ Docker/Kubernetes guides

## 📦 Package Information

- **Package Name:** `prism-config`
- **Version:** 1.0.0
- **Python:** >=3.10
- **Dependencies:** Pydantic >=2.0.0, PyYAML >=6.0.0
- **License:** MIT

## 🎯 Use Cases

### Docker & Kubernetes
```yaml
# config.yaml
app:
  api_key: REF::FILE::/run/secrets/api_key
database:
  password: REF::FILE::/run/secrets/db_password
```

### 12-Factor Apps
```python
# Automatic environment variable overrides
config = PrismConfig.from_file(
    "config.yaml",
    apply_env=True  # APP_DATABASE__PORT=3306
)
```

### Development vs Production
```python
# Development
config = PrismConfig.from_file("config.dev.yaml")

# Production with all overrides
config = PrismConfig.from_all(
    "/etc/app/config.yaml",
    cli_args=sys.argv[1:],
    resolve_secrets=True
)
```

## 🔧 Configuration File Format

```yaml
app:
  name: my-app
  environment: production
  api_key: REF::ENV::API_KEY  # Optional secret

database:
  host: db.example.com
  port: 5432
  name: mydb
  password: REF::FILE::/run/secrets/db_password  # Optional secret
```

## 🐛 Known Issues

- **Windows Console**: May have Unicode display issues. Set `PYTHONIOENCODING=utf-8` if needed.
- **Fixed Schema**: Currently supports `app` and `database` sections only.

## 🔮 What's Next

Future releases may include:
- Pluggable configuration schemas
- Additional secret providers (AWS Secrets Manager, Vault, etc.)
- Hot-reload support
- Configuration validation UI
- TOML file support

## 📖 Documentation

- **GitHub**: https://github.com/lukeudell/prism-config
- **Documentation**: https://github.com/lukeudell/prism-config#readme
- **Examples**: https://github.com/lukeudell/prism-config/tree/main/examples
- **Changelog**: https://github.com/lukeudell/prism-config/blob/main/CHANGELOG.md

## 🙏 Acknowledgments

Built with:
- [Pydantic](https://docs.pydantic.dev/) - Data validation
- [PyYAML](https://pyyaml.org/) - YAML parsing
- [Hypothesis](https://hypothesis.readthedocs.io/) - Property-based testing

## 🤝 Contributing

We welcome contributions! See our [GitHub repository](https://github.com/lukeudell/prism-config) for:
- Issue tracker
- Pull request guidelines
- Development setup
- Parity test suite

## 📊 Stats

- **Iterations Completed:** 14/14 (100%)
- **Lines of Code:** ~2,200 (production + tests)
- **Test Coverage:** 86%
- **Tests Passing:** 101/101
- **Examples:** 5 complete examples
- **Documentation:** Comprehensive guides and API docs

## 💬 Feedback

Found a bug? Have a feature request? We'd love to hear from you!

- **Issues**: https://github.com/lukeudell/prism-config/issues
- **Discussions**: https://github.com/lukeudell/prism-config/discussions

---

**Happy Configuring!** 🔮

The prism-config Team
