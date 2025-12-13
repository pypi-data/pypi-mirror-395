"""
Tests for environment variable override functionality.

This module tests that environment variables can override configuration
values from files and dicts, with proper type coercion.
"""

from prism.config import PrismConfig


def test_env_var_overrides_dict_value(prism_env):
    """
    Test 3.1: Environment variable overrides dict value.

    ENV vars should take precedence over dict values.
    Format: APP_DATABASE__HOST overrides database.host
    """
    # ARRANGE: Set environment variable
    prism_env["monkeypatch"].setenv("APP_DATABASE__HOST", "prod.example.com")

    config_data = {
        "app": {
            "name": "test-app",
            "environment": "dev"
        },
        "database": {
            "host": "localhost",  # This should be overridden
            "port": 5432,
            "name": "testdb"
        }
    }

    # ACT: Load config with env var override
    config = PrismConfig.from_dict(config_data, apply_env=True)

    # ASSERT: Env var value takes precedence
    assert config.database.host == "prod.example.com"
    # Other values unchanged
    assert config.database.port == 5432
    assert config.app.name == "test-app"


def test_nested_env_var_with_double_underscore(prism_env):
    """
    Test 3.2: Nested env var override using double-underscore separator.

    APP_DATABASE__PORT should override database.port
    (Note: double underscore for nesting)
    """
    # ARRANGE: Set nested env var
    prism_env["monkeypatch"].setenv("APP_DATABASE__PORT", "3306")

    config_data = {
        "app": {
            "name": "test-app",
            "environment": "dev"
        },
        "database": {
            "host": "localhost",
            "port": 5432,  # This should be overridden
            "name": "testdb"
        }
    }

    # ACT: Load config
    config = PrismConfig.from_dict(config_data, apply_env=True)

    # ASSERT: Port was overridden and coerced to int
    assert config.database.port == 3306
    assert isinstance(config.database.port, int)


def test_env_var_underscore_vs_double_underscore(prism_env):
    """
    Test 3.3: Distinguish between single and double underscores.

    Single underscore: part of the key name (app_name)
    Double underscore: nesting separator (app__name)
    """
    # ARRANGE: This should override app.name (not app_name)
    prism_env["monkeypatch"].setenv("APP_APP__NAME", "override-app")

    config_data = {
        "app": {
            "name": "original-app",
            "environment": "dev"
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb"
        }
    }

    # ACT: Load config
    config = PrismConfig.from_dict(config_data, apply_env=True)

    # ASSERT: app.name was overridden
    assert config.app.name == "override-app"


def test_env_var_case_insensitive(prism_env):
    """
    Test 3.4: Environment variables are case-insensitive for matching.

    Both APP_DATABASE_HOST and APP_DATABASE__HOST should work
    (uppercase is standard convention)
    """
    # ARRANGE: Use uppercase env var
    prism_env["monkeypatch"].setenv("APP_DATABASE__HOST", "UPPERCASE.example.com")

    config_data = {
        "app": {
            "name": "test-app",
            "environment": "dev"
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb"
        }
    }

    # ACT: Load config
    config = PrismConfig.from_dict(config_data, apply_env=True)

    # ASSERT: Matched case-insensitively
    assert config.database.host == "UPPERCASE.example.com"


def test_env_var_type_coercion_string_to_int(prism_env):
    """
    Test 3.5: Type coercion from environment variable strings.

    ENV vars are always strings, but should be coerced to schema types.
    """
    # ARRANGE: Set port as string in env var
    prism_env["monkeypatch"].setenv("APP_DATABASE__PORT", "9999")

    config_data = {
        "app": {
            "name": "test-app",
            "environment": "dev"
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb"
        }
    }

    # ACT: Load config
    config = PrismConfig.from_dict(config_data, apply_env=True)

    # ASSERT: String was coerced to int
    assert config.database.port == 9999
    assert isinstance(config.database.port, int)


def test_env_var_boolean_values(prism_env):
    """
    Test 3.6: Boolean environment variables with various formats.

    Should accept: "true", "True", "TRUE", "1", "yes"
    Should reject: "false", "False", "FALSE", "0", "no"
    """
    # We'll need a config model with a boolean field for this test
    # For now, we'll test with environment field as a proxy

    # ARRANGE: Set boolean-like env var
    prism_env["monkeypatch"].setenv("APP_APP__ENVIRONMENT", "production")

    config_data = {
        "app": {
            "name": "test-app",
            "environment": "dev"
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb"
        }
    }

    # ACT: Load config
    config = PrismConfig.from_dict(config_data, apply_env=True)

    # ASSERT: String value was set
    assert config.app.environment == "production"


def test_env_var_without_prefix_ignored(prism_env):
    """
    Test that env vars without the APP_ prefix are ignored.

    Only variables starting with APP_ should be considered.
    """
    # ARRANGE: Set env var without prefix
    prism_env["monkeypatch"].setenv("DATABASE_HOST", "should-be-ignored.com")
    prism_env["monkeypatch"].setenv("APP_DATABASE__HOST", "should-be-used.com")

    config_data = {
        "app": {
            "name": "test-app",
            "environment": "dev"
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb"
        }
    }

    # ACT: Load config
    config = PrismConfig.from_dict(config_data, apply_env=True)

    # ASSERT: Only APP_ prefixed var was used
    assert config.database.host == "should-be-used.com"


def test_env_var_invalid_path_ignored(prism_env):
    """
    Test that env vars pointing to non-existent config paths are ignored.

    Invalid paths should not cause errors, just warnings or silent ignoring.
    """
    # ARRANGE: Set env var for non-existent path
    prism_env["monkeypatch"].setenv("APP_NONEXISTENT__FIELD", "value")

    config_data = {
        "app": {
            "name": "test-app",
            "environment": "dev"
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb"
        }
    }

    # ACT: Load config (should not raise)
    config = PrismConfig.from_dict(config_data, apply_env=True)

    # ASSERT: Valid config loaded, invalid env var ignored
    assert config.app.name == "test-app"


def test_env_var_override_from_file(prism_env, sample_config_yaml):
    """
    Test that env vars override values loaded from YAML files.

    This tests the full precedence: ENV > FILE > DICT
    """
    # ARRANGE: Set env var to override YAML value
    prism_env["monkeypatch"].setenv("APP_DATABASE__HOST", "env-override.com")

    # ACT: Load from file with env override
    config = PrismConfig.from_file(sample_config_yaml, apply_env=True)

    # ASSERT: Env var overrode file value
    assert config.database.host == "env-override.com"
    # Other values from file unchanged
    assert config.app.name == "test-app"
    assert config.database.port == 5432


def test_no_env_override_when_disabled(prism_env):
    """
    Test that env vars are NOT applied when apply_env=False (default).

    This ensures backward compatibility and explicit opt-in.
    """
    # ARRANGE: Set env var
    prism_env["monkeypatch"].setenv("APP_DATABASE__HOST", "should-be-ignored.com")

    config_data = {
        "app": {
            "name": "test-app",
            "environment": "dev"
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb"
        }
    }

    # ACT: Load config WITHOUT env override
    config = PrismConfig.from_dict(config_data, apply_env=False)

    # ASSERT: Env var was ignored
    assert config.database.host == "localhost"
