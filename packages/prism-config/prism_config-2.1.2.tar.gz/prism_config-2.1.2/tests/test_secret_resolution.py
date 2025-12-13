"""
Tests for secret resolution functionality.

This module tests the REF::PROVIDER::KEY syntax for resolving secrets
from environment variables and files with proper error handling.
"""

import pytest

from prism.config import PrismConfig
from prism.config.exceptions import (
    InvalidSecretReferenceError,
    SecretProviderNotFoundError,
    SecretResolutionError,
)


def test_env_secret_basic(prism_env):
    """
    Test 5.1: REF::ENV::KEY resolves to environment variable.

    Basic secret resolution from environment variables.
    """
    # ARRANGE: Set secret in environment
    prism_env["monkeypatch"].setenv("DB_PASSWORD", "super-secret-pass")

    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": "REF::ENV::DB_PASSWORD"
        }
    }

    # ACT: Load config with secret resolution
    config = PrismConfig.from_dict(config_data, resolve_secrets=True)

    # ASSERT: Secret was resolved from env var
    assert config.database.password == "super-secret-pass"


def test_file_secret_basic(prism_env):
    """
    Test 5.2: REF::FILE::path reads secret from file.

    Basic secret resolution from files (Docker secrets pattern).
    """
    # ARRANGE: Create secret file
    secret_file = prism_env["tmp_path"] / "db_password"
    secret_file.write_text("file-secret-pass")

    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": f"REF::FILE::{secret_file}"
        }
    }

    # ACT: Load config with secret resolution
    config = PrismConfig.from_dict(config_data, resolve_secrets=True)

    # ASSERT: Secret was resolved from file
    assert config.database.password == "file-secret-pass"


def test_file_secret_strips_trailing_newline(prism_env):
    """
    Test 5.3: FILE provider strips trailing newlines.

    Many systems (like Docker secrets) add trailing newlines to files.
    These should be stripped automatically.
    """
    # ARRANGE: Create secret file with trailing newline
    secret_file = prism_env["tmp_path"] / "db_password"
    secret_file.write_text("my-password\n")

    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": f"REF::FILE::{secret_file}"
        }
    }

    # ACT
    config = PrismConfig.from_dict(config_data, resolve_secrets=True)

    # ASSERT: Trailing newline was stripped
    assert config.database.password == "my-password"
    assert "\n" not in config.database.password


def test_env_secret_missing_raises_error(prism_env):
    """
    Test 5.4: Missing environment variable raises clear error.

    Secret resolution should fail fast with helpful error message.
    """
    # ARRANGE: Config references non-existent env var
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": "REF::ENV::MISSING_VAR"
        }
    }

    # ACT & ASSERT: Should raise error about missing env var
    with pytest.raises(SecretResolutionError, match="MISSING_VAR"):
        PrismConfig.from_dict(config_data, resolve_secrets=True)


def test_file_secret_missing_raises_error(prism_env):
    """
    Test 5.5: Missing file raises clear error.

    Secret resolution should fail fast with helpful error message.
    """
    # ARRANGE: Config references non-existent file
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": "REF::FILE::/nonexistent/secret.txt"
        }
    }

    # ACT & ASSERT: Should raise error about missing file
    with pytest.raises(SecretResolutionError, match="not found"):
        PrismConfig.from_dict(config_data, resolve_secrets=True)


def test_invalid_ref_syntax_raises_error(prism_env):
    """
    Test 5.6: Invalid REF:: syntax raises clear error.

    Malformed secret references should be caught with helpful message.
    """
    # ARRANGE: Config with invalid REF syntax (missing provider)
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": "REF::INVALID"
        }
    }

    # ACT & ASSERT: Should raise error about invalid syntax
    with pytest.raises(InvalidSecretReferenceError):
        PrismConfig.from_dict(config_data, resolve_secrets=True)


def test_unknown_provider_raises_error(prism_env):
    """
    Test 5.7: Unknown provider raises clear error.

    Secret references must use known providers (ENV, FILE).
    """
    # ARRANGE: Config with unknown provider
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": "REF::VAULT::my-secret"
        }
    }

    # ACT & ASSERT: Should raise error about unknown provider
    with pytest.raises(SecretProviderNotFoundError, match="VAULT"):
        PrismConfig.from_dict(config_data, resolve_secrets=True)


def test_multiple_secrets_resolved(prism_env):
    """
    Test 5.8: Multiple secrets in same config are all resolved.

    Should handle multiple REF:: references in different fields.
    """
    # ARRANGE: Set multiple secrets
    prism_env["monkeypatch"].setenv("DB_PASSWORD", "db-pass")
    prism_env["monkeypatch"].setenv("API_KEY", "api-key-123")

    config_data = {
        "app": {
            "name": "test-app",
            "environment": "dev",
            "api_key": "REF::ENV::API_KEY"
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": "REF::ENV::DB_PASSWORD"
        }
    }

    # ACT
    config = PrismConfig.from_dict(config_data, resolve_secrets=True)

    # ASSERT: All secrets resolved
    assert config.database.password == "db-pass"
    assert config.app.api_key == "api-key-123"


def test_mixed_env_and_file_secrets(prism_env):
    """
    Test 5.9: Can mix ENV and FILE providers in same config.

    Should support different providers for different secrets.
    """
    # ARRANGE
    prism_env["monkeypatch"].setenv("API_KEY", "env-api-key")

    secret_file = prism_env["tmp_path"] / "db_password"
    secret_file.write_text("file-db-pass")

    config_data = {
        "app": {
            "name": "test-app",
            "environment": "dev",
            "api_key": "REF::ENV::API_KEY"
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": f"REF::FILE::{secret_file}"
        }
    }

    # ACT
    config = PrismConfig.from_dict(config_data, resolve_secrets=True)

    # ASSERT
    assert config.app.api_key == "env-api-key"
    assert config.database.password == "file-db-pass"


def test_secret_resolution_disabled_by_default(prism_env):
    """
    Test 5.10: Secret resolution is opt-in via resolve_secrets=True.

    By default, REF:: strings should be left as-is for backward compatibility.
    """
    # ARRANGE
    prism_env["monkeypatch"].setenv("DB_PASSWORD", "actual-secret")

    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": "REF::ENV::DB_PASSWORD"
        }
    }

    # ACT: Load without resolve_secrets flag
    config = PrismConfig.from_dict(config_data)

    # ASSERT: REF:: string NOT resolved
    assert config.database.password == "REF::ENV::DB_PASSWORD"


def test_no_secrets_to_resolve(prism_env):
    """
    Test 5.11: Config without secrets works with resolve_secrets=True.

    Should gracefully handle configs that don't use REF:: syntax.
    """
    # ARRANGE: Config with no secrets
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb"
        }
    }

    # ACT
    config = PrismConfig.from_dict(config_data, resolve_secrets=True)

    # ASSERT: Config loaded successfully
    assert config.app.name == "test-app"
    assert config.database.host == "localhost"


def test_secret_resolution_with_from_file(prism_env, sample_config_yaml):
    """
    Test 5.12: Secret resolution works with from_file().

    Should integrate with YAML file loading.
    """
    # ARRANGE: Update YAML file to include secret reference
    prism_env["monkeypatch"].setenv("DB_PASSWORD", "yaml-secret")

    yaml_with_secret = """
app:
  name: test-app
  environment: dev

database:
  host: localhost
  port: 5432
  name: testdb
  password: REF::ENV::DB_PASSWORD
"""

    yaml_file = prism_env["tmp_path"] / "config_secrets.yaml"
    yaml_file.write_text(yaml_with_secret)

    # ACT
    config = PrismConfig.from_file(yaml_file, resolve_secrets=True)

    # ASSERT
    assert config.database.password == "yaml-secret"


def test_secret_precedence_with_cli_override(prism_env):
    """
    Test 5.13: CLI args can override secret references.

    Precedence: CLI > SECRET > ENV > FILE
    CLI override of a secret reference should use the CLI value directly.
    """
    # ARRANGE
    prism_env["monkeypatch"].setenv("DB_PASSWORD", "env-secret")

    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": "REF::ENV::DB_PASSWORD"
        }
    }

    cli_args = ["--database.password=cli-override"]

    # ACT: CLI should override secret reference
    config = PrismConfig.from_dict(
        config_data,
        resolve_secrets=True,
        cli_args=cli_args
    )

    # ASSERT: CLI value used, not resolved secret
    assert config.database.password == "cli-override"
