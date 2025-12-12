# Parity Test Specification

Version: 1.0.0
Last Updated: 2025-12-03

## Overview

This specification defines the test format and validation rules for prism-config cross-language parity tests. All language implementations (Python, Java, etc.) must pass these tests to ensure consistent behavior.

## Test File Format

### Structure

Each test is a JSON file with the following top-level fields:

```typescript
{
  "name": string,              // Test name (required)
  "description": string,       // What this test validates (required)
  "config": object,           // Configuration data (required)
  "config_file"?: string,     // Path to YAML config file (optional)
  "environment"?: object,     // Environment variables to set (optional)
  "secrets"?: object,         // Secret provider values (optional)
  "cli_args"?: string[],      // CLI arguments (optional)
  "options": {                // Loading options (required)
    "apply_env": boolean,
    "resolve_secrets": boolean,
    "env_prefix"?: string
  },
  "expected": object,         // Expected values after loading (required)
  "expected_error"?: {        // Expected error (optional)
    "type": string,
    "message_contains": string
  }
}
```

### Field Descriptions

#### `name` (required)
- Type: `string`
- A short, descriptive name for the test
- Example: `"basic_dict_loading"`

#### `description` (required)
- Type: `string`
- Detailed description of what the test validates
- Example: `"Validates that basic configuration loads correctly from a dictionary"`

#### `config` (required if no `config_file`)
- Type: `object`
- The configuration data as a nested object
- Must have `app` and `database` sections
- Example:
  ```json
  {
    "app": {"name": "test-app", "environment": "dev"},
    "database": {"host": "localhost", "port": 5432, "name": "db"}
  }
  ```

#### `config_file` (optional)
- Type: `string`
- Path to a YAML configuration file (relative to test file)
- Alternative to `config` field
- Example: `"fixtures/basic.yaml"`

#### `environment` (optional)
- Type: `object`
- Environment variables to set before loading config
- Keys are variable names, values are string values
- Example:
  ```json
  {
    "APP_DATABASE__PORT": "3306",
    "APP_APP__ENVIRONMENT": "production"
  }
  ```

#### `secrets` (optional)
- Type: `object`
- Secret provider values to make available
- Keys are in format `PROVIDER::KEY`, values are the secret values
- Example:
  ```json
  {
    "ENV::DB_PASSWORD": "secret123",
    "FILE::/tmp/api_key": "sk_live_abc123"
  }
  ```

#### `cli_args` (optional)
- Type: `string[]`
- Command-line arguments to pass
- Example: `["--database.host=prod.db.com", "--app.environment=staging"]`

#### `options` (required)
- Type: `object`
- Loading options that control behavior
- Fields:
  - `apply_env` (boolean): Whether to apply environment variable overrides
  - `resolve_secrets` (boolean): Whether to resolve REF:: secret references
  - `env_prefix` (string, optional): Environment variable prefix (default: "APP_")

#### `expected` (required if no `expected_error`)
- Type: `object`
- Expected configuration values after loading
- Keys are dot-notation paths, values are expected values
- Example:
  ```json
  {
    "app.name": "test-app",
    "app.environment": "dev",
    "database.port": 3306
  }
  ```

#### `expected_error` (optional)
- Type: `object`
- Expected error when loading should fail
- Fields:
  - `type` (string): Exception/error class name
  - `message_contains` (string): Substring that must appear in error message
- Example:
  ```json
  {
    "type": "ConfigValidationError",
    "message_contains": "database.port"
  }
  ```

## Validation Rules

### Rule 1: Type Coercion

Environment variables and CLI arguments are strings, but must be coerced to the correct type:

```json
{
  "environment": {"APP_DATABASE__PORT": "3306"},
  "expected": {"database.port": 3306}  // Note: integer, not string
}
```

Supported type coercions:
- String → Integer: `"123"` → `123`
- String → Boolean: `"true"`, `"True"`, `"1"` → `true`
- String → String: `"value"` → `"value"` (no change)

### Rule 2: Precedence Order

When multiple sources provide the same value, use this precedence (highest to lowest):

1. CLI arguments
2. Secrets (REF:: resolution)
3. Environment variables
4. Config file/dict
5. Default values

Example test:
```json
{
  "config": {"database": {"port": 5432}},
  "environment": {"APP_DATABASE__PORT": "3306"},
  "cli_args": ["--database.port=3307"],
  "options": {"apply_env": true},
  "expected": {"database.port": 3307}  // CLI wins
}
```

### Rule 3: Secret Resolution

Secret references must follow the format `REF::PROVIDER::KEY`:

```json
{
  "config": {
    "database": {"password": "REF::ENV::DB_PASSWORD"}
  },
  "secrets": {
    "ENV::DB_PASSWORD": "secret123"
  },
  "options": {"resolve_secrets": true},
  "expected": {
    "database.password": "secret123"
  }
}
```

### Rule 4: Large Value Support

All implementations must support values up to 16KB (for PQC keys):

```json
{
  "config": {
    "app": {"api_key": "<16KB_STRING>"}
  },
  "expected": {
    "app.api_key": "<16KB_STRING>"
  }
}
```

### Rule 5: Error Messages

Error messages must be clear and actionable:

```json
{
  "config": {"database": {"port": "not_a_number"}},
  "expected_error": {
    "type": "ConfigValidationError",
    "message_contains": "database.port"
  }
}
```

## Test Categories

### Category 1: Basic Loading

Tests fundamental loading from dict and YAML files.

Required tests:
- Load valid configuration
- Reject extra fields
- Validate required fields
- Type validation

### Category 2: Environment Overrides

Tests environment variable override behavior.

Required tests:
- Double-underscore nesting
- Type coercion
- Case insensitivity
- Custom prefix
- Precedence over config file

### Category 3: Secret Resolution

Tests secret reference resolution.

Required tests:
- ENV provider
- FILE provider
- Invalid reference format
- Missing secret
- Secret redaction in display

### Category 4: Large Values

Tests support for large configuration values.

Required tests:
- 1KB value
- 8KB value
- 16KB value (Kyber-1024 size)
- Multiple large values

## Implementation Requirements

### Required Behavior

All implementations MUST:
1. Pass all parity tests in the test suite
2. Follow the precedence order exactly
3. Coerce types consistently
4. Support values up to 16KB
5. Resolve secrets identically
6. Produce clear error messages

### Language-Specific Adaptations

Implementations MAY adapt to language idioms:
- Exception vs Result types for errors
- Snake_case vs camelCase naming
- Language-specific type systems

But MUST maintain behavioral equivalence.

### Error Handling

When a test specifies `expected_error`:
- The implementation must raise/throw the specified error type
- The error message must contain the specified substring
- The error must be raised at config loading time (not access time)

### Secret Redaction

When displaying or exporting configuration:
- Fields named `password`, `secret`, `token`, `key`, or `api_key` must be redacted
- Redacted values should show `[REDACTED]` or similar
- Original values remain accessible in code

## Test Execution

### Setup Phase

1. Set environment variables from `environment` field
2. Prepare secret providers with values from `secrets` field
3. Create temp files if needed for FILE provider

### Load Phase

1. Load configuration using specified method (dict or file)
2. Apply options (`apply_env`, `resolve_secrets`, etc.)
3. Pass `cli_args` if provided

### Validation Phase

1. If `expected_error` is set:
   - Verify the correct error type is raised
   - Verify error message contains expected substring
2. If `expected` is set:
   - For each key-value pair in `expected`:
     - Access the configuration value using dot notation
     - Assert it exactly matches the expected value (type and value)

### Cleanup Phase

1. Clear environment variables
2. Remove temp files
3. Reset secret providers

## Versioning

The parity test suite uses semantic versioning:

- **Major version**: Breaking changes to test format or required behavior
- **Minor version**: New test cases that don't break existing tests
- **Patch version**: Documentation updates or test clarifications

Current version: **1.0.0**

## Adding New Tests

To add a new parity test:

1. Create a JSON file following this specification
2. Name it descriptively: `##_feature_name.json`
3. Test it in the reference implementation (Python)
4. Document any edge cases
5. Submit a PR with the new test

## Reference Implementation

The Python implementation (`prism-config-python`) is the reference implementation. When in doubt about correct behavior, the Python implementation defines the expected behavior.

## FAQ

### Q: What if my language doesn't support 16KB strings?

A: All implementations must support values up to 16KB. This is a hard requirement for PQC compatibility.

### Q: Can I add implementation-specific tests?

A: Yes, but they should be in a separate directory (e.g., `tests/python_specific/`). Parity tests must work across all languages.

### Q: What about performance tests?

A: Performance tests are not part of parity testing. Each implementation may have its own performance benchmarks.

### Q: How do I handle platform differences (Windows vs Linux)?

A: Tests should be platform-agnostic. If platform-specific behavior is necessary, document it clearly.
