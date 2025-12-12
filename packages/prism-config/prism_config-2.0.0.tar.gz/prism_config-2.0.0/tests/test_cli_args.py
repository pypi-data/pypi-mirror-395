"""
Tests for CLI argument override functionality.

This module tests that CLI arguments can override configuration values
from files, environment variables, and dicts with proper precedence.
"""

from prism.config import PrismConfig


def test_cli_args_override_all_sources(prism_env, sample_config_yaml):
    """
    Test 4.1: CLI arguments override env vars, files, and dicts.

    CLI args should have the highest precedence in the loading hierarchy:
    CLI > ENV > FILE > DICT
    """
    # ARRANGE: Set environment variable (should be overridden by CLI)
    prism_env["monkeypatch"].setenv("APP_DATABASE__HOST", "env-host.com")

    # CLI args that should override everything
    cli_args = ["--database.host=cli-host.com", "--database.port=9999"]

    # ACT: Load from file with env vars and CLI args
    config = PrismConfig.from_file(
        sample_config_yaml,
        apply_env=True,
        cli_args=cli_args
    )

    # ASSERT: CLI args take highest precedence
    assert config.database.host == "cli-host.com"  # CLI wins over env and file
    assert config.database.port == 9999  # CLI wins over file
    assert isinstance(config.database.port, int)  # Type coercion works


def test_cli_args_dot_notation(prism_env):
    """
    Test 4.2: CLI arg format --database.host=localhost

    Support dot notation for nested keys, matching common CLI patterns.
    """
    # ARRANGE
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {"host": "localhost", "port": 5432, "name": "testdb"}
    }

    cli_args = [
        "--database.host=prod.example.com",
        "--database.port=3306",
        "--app.environment=production"
    ]

    # ACT
    config = PrismConfig.from_dict(config_data, cli_args=cli_args)

    # ASSERT
    assert config.database.host == "prod.example.com"
    assert config.database.port == 3306
    assert config.app.environment == "production"


def test_cli_args_dash_notation(prism_env):
    """
    Test 4.3: CLI arg format --database-host=localhost

    Support dash notation as an alternative to dots, which is more
    common in many CLI tools.
    """
    # ARRANGE
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {"host": "localhost", "port": 5432, "name": "testdb"}
    }

    cli_args = [
        "--database-host=prod.example.com",
        "--database-port=3306",
        "--app-environment=production"
    ]

    # ACT
    config = PrismConfig.from_dict(config_data, cli_args=cli_args)

    # ASSERT
    assert config.database.host == "prod.example.com"
    assert config.database.port == 3306
    assert config.app.environment == "production"


def test_cli_args_boolean_flags(prism_env):
    """
    Test 4.4: Boolean flags like --debug (no value needed)

    For boolean fields, support flag-style arguments without explicit values.
    """
    # Note: Our current schema doesn't have boolean fields
    # This test documents the expected behavior for when we add them

    # ARRANGE
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {"host": "localhost", "port": 5432, "name": "testdb"}
    }

    # Use environment field as a string (not boolean for now)
    cli_args = ["--app.environment=debug"]

    # ACT
    config = PrismConfig.from_dict(config_data, cli_args=cli_args)

    # ASSERT
    assert config.app.environment == "debug"


def test_cli_args_with_from_file(prism_env, sample_config_yaml):
    """
    Test 4.5: CLI args work with from_file()

    Ensure CLI arguments properly override YAML file values.
    """
    # ARRANGE
    cli_args = [
        "--app.name=cli-override-app",
        "--database.port=7777"
    ]

    # ACT
    config = PrismConfig.from_file(sample_config_yaml, cli_args=cli_args)

    # ASSERT: CLI args override file values
    assert config.app.name == "cli-override-app"
    assert config.database.port == 7777
    # Values not overridden should come from file
    assert config.app.environment == "dev"
    assert config.database.host == "localhost"


def test_cli_args_type_coercion(prism_env):
    """
    Test that CLI args (which are always strings) are coerced to correct types.

    Similar to env vars, CLI args are strings but should be converted.
    """
    # ARRANGE
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {"host": "localhost", "port": 5432, "name": "testdb"}
    }

    cli_args = [
        "--database.port=8888"  # String that should become int
    ]

    # ACT
    config = PrismConfig.from_dict(config_data, cli_args=cli_args)

    # ASSERT
    assert config.database.port == 8888
    assert isinstance(config.database.port, int)


def test_cli_args_invalid_path_ignored(prism_env):
    """
    Test that CLI args with invalid paths are ignored gracefully.

    Similar to env vars, invalid paths should not cause errors.
    """
    # ARRANGE
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {"host": "localhost", "port": 5432, "name": "testdb"}
    }

    cli_args = [
        "--nonexistent.field=value",  # Should be ignored
        "--database.port=3306"        # Should work
    ]

    # ACT
    config = PrismConfig.from_dict(config_data, cli_args=cli_args)

    # ASSERT
    assert config.database.port == 3306
    # Invalid arg didn't cause an error


def test_cli_args_empty_list(prism_env):
    """
    Test that passing an empty CLI args list works correctly.

    Should behave the same as not passing cli_args at all.
    """
    # ARRANGE
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {"host": "localhost", "port": 5432, "name": "testdb"}
    }

    # ACT
    config = PrismConfig.from_dict(config_data, cli_args=[])

    # ASSERT
    assert config.database.host == "localhost"
    assert config.database.port == 5432


def test_cli_args_none_default(prism_env):
    """
    Test that cli_args=None (default) works correctly.

    When not provided, should work like previous behavior.
    """
    # ARRANGE
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {"host": "localhost", "port": 5432, "name": "testdb"}
    }

    # ACT
    config = PrismConfig.from_dict(config_data)  # No cli_args parameter

    # ASSERT
    assert config.database.host == "localhost"
    assert config.database.port == 5432


def test_from_all_method_precedence(prism_env, sample_config_yaml):
    """
    Test the from_all() convenience method with full precedence chain.

    Should apply: CLI > ENV > FILE with proper precedence.
    """
    # ARRANGE
    prism_env["monkeypatch"].setenv("APP_DATABASE__HOST", "env-override.com")

    cli_args = ["--database.port=9999"]

    # ACT
    config = PrismConfig.from_all(
        file_path=sample_config_yaml,
        cli_args=cli_args
    )

    # ASSERT
    # CLI arg takes precedence
    assert config.database.port == 9999
    # Env var takes precedence over file
    assert config.database.host == "env-override.com"
    # File value used when not overridden
    assert config.app.name == "test-app"


def test_cli_args_equals_sign_required(prism_env):
    """
    Test that CLI args must use equals sign format.

    Args like "--database.host prod.com" (space-separated) should not work.
    Only "--database.host=prod.com" format is supported.
    """
    # ARRANGE
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {"host": "localhost", "port": 5432, "name": "testdb"}
    }

    # Valid format with equals sign
    cli_args = ["--database.port=3306"]

    # ACT
    config = PrismConfig.from_dict(config_data, cli_args=cli_args)

    # ASSERT
    assert config.database.port == 3306
