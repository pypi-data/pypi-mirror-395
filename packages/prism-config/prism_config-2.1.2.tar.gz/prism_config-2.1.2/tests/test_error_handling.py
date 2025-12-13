"""
Tests for error handling and custom exceptions.

This module tests that prism-config provides clear, actionable
error messages when things go wrong.

v2.1.1+: Tests for structured error metadata (error codes, severity,
timestamps, to_dict(), with_context()).
"""

import json
import pytest

from prism.config import PrismConfig, ErrorCode, Severity
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
    # v2.1.1: Available providers are now in context, not message
    assert "ENV" in error.available_providers
    assert "FILE" in error.available_providers


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
    # v2.1.1: Format guidance is now in suggestion field
    assert "REF::PROVIDER::KEY" in error.suggestion
    assert error.context["expected_format"] == "REF::PROVIDER::KEY"


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


# =============================================================================
# v2.1.1+ Structured Error Metadata Tests
# =============================================================================


class TestErrorCodes:
    """Test that exceptions have proper error codes (v2.1.1+)."""

    def test_file_not_found_has_error_code(self, prism_env):
        """ConfigFileNotFoundError should have FILE_NOT_FOUND error code."""
        with pytest.raises(ConfigFileNotFoundError) as exc_info:
            PrismConfig.from_file(prism_env["tmp_path"] / "missing.yaml")

        error = exc_info.value
        assert error.error_code == ErrorCode.FILE_NOT_FOUND
        assert "PRISM-1001" in str(error)

    def test_parse_error_has_error_code(self, prism_env):
        """ConfigParseError should have appropriate error codes."""
        bad_yaml = prism_env["tmp_path"] / "bad.yaml"
        bad_yaml.write_text("invalid: [yaml")

        with pytest.raises(ConfigParseError) as exc_info:
            PrismConfig.from_file(bad_yaml)

        error = exc_info.value
        assert error.error_code in (ErrorCode.FILE_PARSE_ERROR, ErrorCode.FILE_EMPTY)
        assert "PRISM-100" in str(error)  # 1001-1005

    def test_validation_error_has_error_code(self, prism_env):
        """ConfigValidationError should have validation error codes."""
        with pytest.raises(ConfigValidationError) as exc_info:
            PrismConfig.from_dict({
                "app": {"name": "test", "environment": "dev"},
                "database": {"host": "localhost", "port": "invalid", "name": "db"}
            })

        error = exc_info.value
        assert error.error_code.value.startswith("PRISM-2")

    def test_secret_error_has_error_code(self, prism_env):
        """SecretResolutionError should have secret error codes."""
        with pytest.raises(SecretResolutionError) as exc_info:
            PrismConfig.from_dict({
                "app": {"name": "test", "environment": "dev"},
                "database": {
                    "host": "localhost",
                    "port": 5432,
                    "name": "db",
                    "password": "REF::ENV::MISSING"
                }
            }, resolve_secrets=True)

        error = exc_info.value
        assert error.error_code.value.startswith("PRISM-3")


class TestSeverityLevels:
    """Test that exceptions have appropriate severity levels (v2.1.1+)."""

    def test_errors_have_severity(self, prism_env):
        """All errors should have a severity level."""
        with pytest.raises(ConfigFileNotFoundError) as exc_info:
            PrismConfig.from_file(prism_env["tmp_path"] / "missing.yaml")

        error = exc_info.value
        assert hasattr(error, "severity")
        assert error.severity == Severity.ERROR

    def test_severity_is_valid_level(self, prism_env):
        """Severity should be a valid Severity enum."""
        with pytest.raises(ConfigFileNotFoundError) as exc_info:
            PrismConfig.from_file(prism_env["tmp_path"] / "missing.yaml")

        error = exc_info.value
        assert error.severity in list(Severity)
        assert error.severity.value in ("debug", "info", "warning", "error", "critical")


class TestTimestamps:
    """Test that exceptions have timestamps (v2.1.1+)."""

    def test_errors_have_timestamp(self, prism_env):
        """All errors should have a UTC timestamp."""
        from datetime import datetime, timezone

        with pytest.raises(ConfigFileNotFoundError) as exc_info:
            PrismConfig.from_file(prism_env["tmp_path"] / "missing.yaml")

        error = exc_info.value
        assert hasattr(error, "timestamp")
        assert isinstance(error.timestamp, datetime)
        assert error.timestamp.tzinfo == timezone.utc

    def test_timestamp_is_recent(self, prism_env):
        """Timestamp should be close to current time."""
        from datetime import datetime, timezone, timedelta

        before = datetime.now(timezone.utc)

        with pytest.raises(ConfigFileNotFoundError) as exc_info:
            PrismConfig.from_file(prism_env["tmp_path"] / "missing.yaml")

        after = datetime.now(timezone.utc)
        error = exc_info.value

        assert before <= error.timestamp <= after + timedelta(seconds=1)


class TestToDict:
    """Test exception to_dict() method for structured logging (v2.1.1+)."""

    def test_to_dict_returns_dict(self, prism_env):
        """to_dict() should return a dictionary."""
        with pytest.raises(ConfigFileNotFoundError) as exc_info:
            PrismConfig.from_file(prism_env["tmp_path"] / "missing.yaml")

        error = exc_info.value
        result = error.to_dict()
        assert isinstance(result, dict)

    def test_to_dict_includes_error_code(self, prism_env):
        """to_dict() should include error_code."""
        with pytest.raises(ConfigFileNotFoundError) as exc_info:
            PrismConfig.from_file(prism_env["tmp_path"] / "missing.yaml")

        result = exc_info.value.to_dict()
        assert "error_code" in result
        assert result["error_code"] == "PRISM-1001"
        assert "error_name" in result
        assert result["error_name"] == "FILE_NOT_FOUND"

    def test_to_dict_includes_severity(self, prism_env):
        """to_dict() should include severity."""
        with pytest.raises(ConfigFileNotFoundError) as exc_info:
            PrismConfig.from_file(prism_env["tmp_path"] / "missing.yaml")

        result = exc_info.value.to_dict()
        assert "severity" in result
        assert result["severity"] == "error"

    def test_to_dict_includes_timestamp(self, prism_env):
        """to_dict() should include ISO timestamp."""
        with pytest.raises(ConfigFileNotFoundError) as exc_info:
            PrismConfig.from_file(prism_env["tmp_path"] / "missing.yaml")

        result = exc_info.value.to_dict()
        assert "timestamp" in result
        # Should be ISO format
        assert "T" in result["timestamp"]

    def test_to_dict_includes_context(self, prism_env):
        """to_dict() should include context metadata."""
        with pytest.raises(ConfigFileNotFoundError) as exc_info:
            PrismConfig.from_file(prism_env["tmp_path"] / "missing.yaml")

        result = exc_info.value.to_dict()
        assert "context" in result
        assert "file_path" in result["context"]
        assert "absolute_path" in result["context"]

    def test_to_dict_is_json_serializable(self, prism_env):
        """to_dict() should be JSON serializable."""
        with pytest.raises(ConfigFileNotFoundError) as exc_info:
            PrismConfig.from_file(prism_env["tmp_path"] / "missing.yaml")

        result = exc_info.value.to_dict()
        # Should not raise
        json_str = json.dumps(result, default=str)
        assert isinstance(json_str, str)

    def test_to_dict_includes_original_error(self, prism_env):
        """to_dict() should include original_error if present."""
        bad_yaml = prism_env["tmp_path"] / "bad.yaml"
        bad_yaml.write_text("invalid: [yaml")

        with pytest.raises(ConfigParseError) as exc_info:
            PrismConfig.from_file(bad_yaml)

        result = exc_info.value.to_dict()
        if exc_info.value.original_error:
            assert "original_error" in result
            assert "type" in result["original_error"]
            assert "message" in result["original_error"]


class TestWithContext:
    """Test exception with_context() method (v2.1.1+)."""

    def test_with_context_adds_metadata(self, prism_env):
        """with_context() should add additional metadata."""
        with pytest.raises(ConfigFileNotFoundError) as exc_info:
            PrismConfig.from_file(prism_env["tmp_path"] / "missing.yaml")

        error = exc_info.value
        error.with_context(correlation_id="abc-123", request_id="req-456")

        assert "correlation_id" in error.context
        assert error.context["correlation_id"] == "abc-123"
        assert error.context["request_id"] == "req-456"

    def test_with_context_returns_self(self, prism_env):
        """with_context() should return self for chaining."""
        with pytest.raises(ConfigFileNotFoundError) as exc_info:
            PrismConfig.from_file(prism_env["tmp_path"] / "missing.yaml")

        error = exc_info.value
        result = error.with_context(foo="bar")
        assert result is error

    def test_with_context_appears_in_to_dict(self, prism_env):
        """Context added via with_context() should appear in to_dict()."""
        with pytest.raises(ConfigFileNotFoundError) as exc_info:
            PrismConfig.from_file(prism_env["tmp_path"] / "missing.yaml")

        error = exc_info.value
        error.with_context(trace_id="trace-789")

        result = error.to_dict()
        assert result["context"]["trace_id"] == "trace-789"


class TestErrorCodeEnumExport:
    """Test that ErrorCode and Severity are properly exported (v2.1.1+)."""

    def test_error_code_exported(self):
        """ErrorCode enum should be importable from prism.config."""
        from prism.config import ErrorCode
        assert ErrorCode.FILE_NOT_FOUND.value == "PRISM-1001"

    def test_severity_exported(self):
        """Severity enum should be importable from prism.config."""
        from prism.config import Severity
        assert Severity.ERROR.value == "error"

    def test_all_error_codes_have_values(self):
        """All ErrorCode enum members should have PRISM-xxxx format."""
        for code in ErrorCode:
            assert code.value.startswith("PRISM-")
            assert len(code.value) == 10  # PRISM-XXXX
