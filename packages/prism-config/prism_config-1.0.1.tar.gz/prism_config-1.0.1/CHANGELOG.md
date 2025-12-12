# Changelog

All notable changes to prism-config will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2025-12-05

### Fixed
- **Neon Dump table formatting** - Added minimum column widths to prevent cramped output when configuration keys and values are short. The table now displays with better proportions.

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
