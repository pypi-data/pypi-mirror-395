# Parity Test Suite

This directory contains cross-language parity tests to ensure consistent behavior across all prism-config implementations (Python, Java, etc.).

## Purpose

The parity tests ensure that:
- All language implementations load configuration identically
- Environment variable overrides work the same way
- Secret resolution behaves consistently
- Large value support is uniform
- Error handling is predictable

## Test Format

Each test is defined in a JSON file with this structure:

```json
{
  "name": "Test name",
  "description": "What this test validates",
  "config": {
    "app": {"name": "test-app", "environment": "dev"},
    "database": {"host": "localhost", "port": 5432, "name": "db"}
  },
  "environment": {
    "APP_DATABASE__PORT": "3306"
  },
  "secrets": {
    "ENV::DB_PASSWORD": "secret123"
  },
  "options": {
    "apply_env": true,
    "resolve_secrets": true
  },
  "expected": {
    "app.name": "test-app",
    "app.environment": "dev",
    "database.host": "localhost",
    "database.port": 3306,
    "database.name": "db"
  }
}
```

## Test Files

- `01_basic_loading.json` - Basic configuration loading
- `02_env_override.json` - Environment variable overrides
- `03_secret_resolution.json` - Secret resolution
- `04_large_values.json` - Large value handling (16KB)
- `spec.md` - Detailed specification

## Running Tests

### Python

```bash
pytest tests/parity/test_parity.py -v
```

### Java (future)

```bash
mvn test -Dtest=ParityTest
```

## Adding New Tests

1. Create a new JSON file in `tests/parity/`
2. Follow the test format specification
3. Add expected values for all fields
4. Run tests in all language implementations
5. Document any language-specific behavior

## Test Categories

### Basic Loading (01)
- Load from dict
- Load from YAML file
- Type validation
- Required fields

### Environment Overrides (02)
- Double-underscore nesting
- Type coercion
- Case insensitivity
- Precedence order

### Secret Resolution (03)
- ENV provider
- FILE provider
- Invalid references
- Missing secrets

### Large Values (04)
- 1KB values
- 8KB values
- 16KB values (PQC key size)
- Multiple large values

## Validation Rules

All implementations must:
1. Load configuration identically
2. Apply overrides in the same order
3. Coerce types consistently
4. Handle errors with clear messages
5. Support values up to 16KB
6. Resolve secrets identically

## Version Compatibility

The parity tests define the contract between versions:
- Tests must pass for all supported versions
- Breaking changes require new test suite version
- Backwards compatibility is validated via tests

## Contributing

When adding features to any implementation:
1. Add parity test first
2. Implement in all languages
3. Verify all tests pass
4. Document any differences
