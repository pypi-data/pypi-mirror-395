"""
Tests for error handling and custom exceptions.

This module tests that prism-config provides clear, actionable
error messages when things go wrong.
"""

import pytest

from prism.config import PrismConfig
from prism.config.exceptions import (
    ConfigFileNotFoundError,
    ConfigParseError,
    ConfigValidationError,
    InvalidSecretReferenceError,
    SecretProviderNotFoundError,
    SecretResolutionError,
)


def test_config_file_not_found_error(prism_env):
    """
    Test 11.1: Missing file error includes full path.

    Verify that ConfigFileNotFoundError provides helpful information
    about the missing file and its expected location.
    """
    # ARRANGE: Non-existent file path
    missing_file = prism_env["tmp_path"] / "does_not_exist.yaml"

    # ACT & ASSERT: Should raise ConfigFileNotFoundError
    with pytest.raises(ConfigFileNotFoundError) as exc_info:
        PrismConfig.from_file(missing_file)

    error = exc_info.value
    assert error.file_path == missing_file
    assert "Configuration file not found" in str(error)
    assert str(missing_file) in str(error)
    assert "Suggestion" in str(error)


def test_yaml_syntax_error_shows_context(prism_env):
    """
    Test 11.2: YAML syntax error shows helpful context.

    Verify that ConfigParseError provides line numbers and suggestions
    when YAML parsing fails.
    """
    # ARRANGE: Invalid YAML file
    yaml_file = prism_env["tmp_path"] / "invalid.yaml"
    yaml_file.write_text("app:\n  name: test\n  invalid: [unclosed")

    # ACT & ASSERT: Should raise ConfigParseError
    with pytest.raises(ConfigParseError) as exc_info:
        PrismConfig.from_file(yaml_file)

    error = exc_info.value
    assert error.file_path == yaml_file
    assert "Failed to parse configuration file" in str(error)
    assert "YAML" in str(error) or "syntax" in str(error).lower()
    assert "Suggestion" in str(error)


def test_validation_error_shows_field_and_type(prism_env):
    """
    Test 11.3: Validation error shows field name and type mismatch.

    Verify that ConfigValidationError provides clear information
    about which field failed validation and why.
    """
    # ARRANGE: Config with invalid type
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": "not_a_number",  # Should be int
            "name": "testdb"
        }
    }

    # ACT & ASSERT: Should raise ConfigValidationError
    with pytest.raises(ConfigValidationError) as exc_info:
        PrismConfig.from_dict(config_data)

    error = exc_info.value
    assert "database.port" in error.field_path or "port" in error.field_path
    assert "Configuration validation failed" in str(error)
    assert "Suggestion" in str(error)


def test_secret_resolution_error_shows_provider_and_key(prism_env):
    """
    Test 11.4: Secret resolution error shows provider and key.

    Verify that SecretResolutionError provides clear information
    about which secret failed to resolve.
    """
    # ARRANGE: Config with missing secret
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": "REF::ENV::MISSING_SECRET"
        }
    }

    # ACT & ASSERT: Should raise SecretResolutionError
    with pytest.raises(SecretResolutionError) as exc_info:
        PrismConfig.from_dict(config_data, resolve_secrets=True)

    error = exc_info.value
    assert error.provider == "ENV"
    assert error.key == "MISSING_SECRET"
    assert "Failed to resolve secret" in str(error)
    assert "ENV" in str(error)
    assert "MISSING_SECRET" in str(error)
    assert "Suggestion" in str(error)


def test_secret_provider_not_found_error(prism_env):
    """
    Test 11.5: Unknown provider error shows available providers.

    Verify that SecretProviderNotFoundError lists available providers.
    """
    # ARRANGE: Config with unknown provider
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": "REF::VAULT::secret"  # VAULT provider doesn't exist
        }
    }

    # ACT & ASSERT: Should raise SecretProviderNotFoundError
    with pytest.raises(SecretProviderNotFoundError) as exc_info:
        PrismConfig.from_dict(config_data, resolve_secrets=True)

    error = exc_info.value
    assert error.provider_name == "VAULT"
    assert "Secret provider not found" in str(error)
    assert "VAULT" in str(error)
    assert "Available providers" in str(error)
    assert "ENV" in str(error)  # Should list available providers
    assert "FILE" in str(error)


def test_invalid_secret_reference_error(prism_env):
    """
    Test 11.6: Invalid secret syntax shows expected format.

    Verify that InvalidSecretReferenceError provides the correct syntax.
    """
    # ARRANGE: Config with invalid secret syntax
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": "REF::INVALID"  # Missing second ::
        }
    }

    # ACT & ASSERT: Should raise InvalidSecretReferenceError
    with pytest.raises(InvalidSecretReferenceError) as exc_info:
        PrismConfig.from_dict(config_data, resolve_secrets=True)

    error = exc_info.value
    assert error.reference == "REF::INVALID"
    assert "Invalid secret reference" in str(error)
    assert "Expected format: REF::PROVIDER::KEY" in str(error)
    assert "Example:" in str(error)


def test_file_secret_not_found_error(prism_env):
    """
    Test 11.7: File secret error shows file path.

    Verify that file-based secrets provide clear error messages.
    """
    # ARRANGE: Config with missing file secret
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": "REF::FILE::/nonexistent/secret.txt"
        }
    }

    # ACT & ASSERT: Should raise SecretResolutionError
    with pytest.raises(SecretResolutionError) as exc_info:
        PrismConfig.from_dict(config_data, resolve_secrets=True)

    error = exc_info.value
    assert error.provider == "FILE"
    assert error.key == "/nonexistent/secret.txt"
    assert "Failed to resolve secret" in str(error)
    assert "/nonexistent/secret.txt" in str(error)
    assert "file exists" in str(error).lower()


def test_error_messages_are_actionable(prism_env):
    """
    Test 11.8: All error messages include actionable suggestions.

    Verify that every error type provides a "Suggestion" to help
    developers fix the problem.
    """
    # Test ConfigFileNotFoundError
    try:
        PrismConfig.from_file(prism_env["tmp_path"] / "missing.yaml")
    except ConfigFileNotFoundError as e:
        assert "Suggestion" in str(e)

    # Test ConfigParseError
    bad_yaml = prism_env["tmp_path"] / "bad.yaml"
    bad_yaml.write_text("invalid: yaml: syntax:")
    try:
        PrismConfig.from_file(bad_yaml)
    except ConfigParseError as e:
        assert "Suggestion" in str(e)

    # Test ConfigValidationError
    try:
        PrismConfig.from_dict({
            "app": {"name": "test", "environment": "dev"},
            "database": {"host": "localhost", "port": "invalid", "name": "db"}
        })
    except ConfigValidationError as e:
        assert "Suggestion" in str(e)

    # Test SecretResolutionError
    try:
        PrismConfig.from_dict({
            "app": {"name": "test", "environment": "dev"},
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "db",
                "password": "REF::ENV::MISSING"
            }
        }, resolve_secrets=True)
    except SecretResolutionError as e:
        assert "Suggestion" in str(e)


def test_error_preserves_original_exception(prism_env):
    """
    Test 11.9: Errors preserve original exception for debugging.

    Verify that custom exceptions preserve the original error
    for developers who need to debug deeper.
    """
    # ARRANGE: Invalid YAML
    bad_yaml = prism_env["tmp_path"] / "bad.yaml"
    bad_yaml.write_text("invalid: [yaml")

    # ACT & ASSERT: Original exception should be preserved
    with pytest.raises(ConfigParseError) as exc_info:
        PrismConfig.from_file(bad_yaml)

    error = exc_info.value
    assert error.original_error is not None
    assert hasattr(error, "original_error")


def test_error_includes_file_path(prism_env):
    """
    Test 11.10: File-related errors include absolute path.

    Verify that errors related to files show the full absolute path
    to help developers locate the issue.
    """
    # Test missing file
    missing = prism_env["tmp_path"] / "missing.yaml"
    try:
        PrismConfig.from_file(missing)
    except ConfigFileNotFoundError as e:
        assert str(missing.absolute()) in str(e) or str(missing) in str(e)

    # Test parse error
    bad_yaml = prism_env["tmp_path"] / "bad.yaml"
    bad_yaml.write_text("invalid yaml content {{{")
    try:
        PrismConfig.from_file(bad_yaml)
    except ConfigParseError as e:
        assert bad_yaml.name in str(e) or str(bad_yaml) in str(e)
