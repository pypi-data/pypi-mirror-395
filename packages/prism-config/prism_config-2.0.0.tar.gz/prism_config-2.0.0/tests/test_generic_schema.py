"""
Tests for generic schema support (v2.0.0+).

These tests verify:
- Custom schema loading with BaseConfigSection and BaseConfigRoot
- Type safety with Generic[T] pattern
- __getattr__ dynamic attribute access
- Backward compatibility with default ConfigRoot schema
- Schema validation errors
"""

import pytest

from prism.config import (
    AppConfig,
    BaseConfigRoot,
    BaseConfigSection,
    ConfigRoot,
    ConfigValidationError,
    DatabaseConfig,
    PrismConfig,
)


# ============================================================================
# Custom Schema Fixtures
# ============================================================================


class AuthConfig(BaseConfigSection):
    """Custom auth configuration section."""
    jwt_secret: str
    token_expiry: int = 3600
    enable_refresh: bool = True


class RateLimitConfig(BaseConfigSection):
    """Custom rate limiting configuration section."""
    requests_per_minute: int = 100
    burst_size: int = 20


class RedisConfig(BaseConfigSection):
    """Custom Redis configuration section."""
    host: str = "localhost"
    port: int = 6379
    db: int = 0


class CustomAppConfig(BaseConfigRoot):
    """Custom root config with additional sections."""
    app: AppConfig
    database: DatabaseConfig
    auth: AuthConfig
    rate_limit: RateLimitConfig


class FlexibleConfig(BaseConfigRoot):
    """Flexible config that allows extra fields."""
    app: AppConfig
    database: DatabaseConfig

    model_config = {
        "extra": "allow",
        "frozen": True,
        "validate_assignment": True,
    }


class MinimalConfig(BaseConfigSection):
    """Minimal config with just one field."""
    name: str


# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def custom_data():
    """Test data with custom sections."""
    return {
        "app": {"name": "test-app", "environment": "prod"},
        "database": {"host": "db.example.com", "port": 5432, "name": "proddb"},
        "auth": {"jwt_secret": "super-secret-key", "token_expiry": 7200},
        "rate_limit": {"requests_per_minute": 200, "burst_size": 50},
    }


@pytest.fixture
def default_data():
    """Test data for default ConfigRoot schema."""
    return {
        "app": {"name": "default-app", "environment": "dev"},
        "database": {"host": "localhost", "port": 5432, "name": "testdb"},
    }


# ============================================================================
# Tests: Custom Schema Loading
# ============================================================================


def test_custom_schema_from_dict(custom_data):
    """
    Test 16.1.8a: Custom schema can be loaded via from_dict().

    Custom sections should be accessible with full type safety.
    """
    # ACT
    config = PrismConfig.from_dict(custom_data, schema=CustomAppConfig)

    # ASSERT: Built-in sections work
    assert config.app.name == "test-app"
    assert config.database.host == "db.example.com"

    # ASSERT: Custom sections work
    assert config.auth.jwt_secret == "super-secret-key"
    assert config.auth.token_expiry == 7200
    assert config.rate_limit.requests_per_minute == 200
    assert config.rate_limit.burst_size == 50


def test_custom_schema_default_values(custom_data):
    """
    Test 16.1.8b: Custom schema uses default values when not provided.

    Optional fields with defaults should use their default values.
    """
    # ARRANGE: Remove optional fields
    data = {
        "app": {"name": "test-app", "environment": "prod"},
        "database": {"host": "localhost", "port": 5432, "name": "testdb"},
        "auth": {"jwt_secret": "my-secret"},  # Only required field
        "rate_limit": {},  # All defaults
    }

    # ACT
    config = PrismConfig.from_dict(data, schema=CustomAppConfig)

    # ASSERT: Defaults are used
    assert config.auth.token_expiry == 3600  # Default
    assert config.auth.enable_refresh is True  # Default
    assert config.rate_limit.requests_per_minute == 100  # Default
    assert config.rate_limit.burst_size == 20  # Default


def test_custom_schema_immutable(custom_data):
    """
    Test 16.1.8c: Custom schema sections are immutable (frozen).

    Attempting to modify frozen sections should raise an error.
    """
    # ARRANGE
    config = PrismConfig.from_dict(custom_data, schema=CustomAppConfig)

    # ACT & ASSERT: Modification should fail (frozen model)
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        config.auth.jwt_secret = "new-secret"


# ============================================================================
# Tests: Backward Compatibility
# ============================================================================


def test_default_schema_backward_compatible(default_data):
    """
    Test 16.1.8d: Default schema works without specifying schema parameter.

    Existing code without schema parameter should continue to work.
    """
    # ACT
    config = PrismConfig.from_dict(default_data)

    # ASSERT: Works as before
    assert config.app.name == "default-app"
    assert config.database.host == "localhost"


def test_explicit_default_schema(default_data):
    """
    Test 16.1.8e: Explicitly passing ConfigRoot works.

    Passing schema=ConfigRoot should work the same as not passing it.
    """
    # ACT
    config = PrismConfig.from_dict(default_data, schema=ConfigRoot)

    # ASSERT: Works the same
    assert config.app.name == "default-app"
    assert config.database.host == "localhost"


def test_default_schema_rejects_extra_fields(custom_data):
    """
    Test 16.1.8f: Default schema rejects unknown fields.

    ConfigRoot has extra="forbid", so it should reject auth and rate_limit.
    """
    # ACT & ASSERT: Should fail with validation error
    with pytest.raises(ConfigValidationError):
        PrismConfig.from_dict(custom_data)  # No schema, uses ConfigRoot


# ============================================================================
# Tests: __getattr__ Dynamic Access
# ============================================================================


def test_getattr_custom_sections(custom_data):
    """
    Test 16.1.8g: __getattr__ provides access to custom sections.

    Custom sections should be accessible via dot notation.
    """
    # ARRANGE
    config = PrismConfig.from_dict(custom_data, schema=CustomAppConfig)

    # ASSERT: __getattr__ works for custom sections
    auth = config.auth
    assert auth.jwt_secret == "super-secret-key"

    rate_limit = config.rate_limit
    assert rate_limit.requests_per_minute == 200


def test_getattr_invalid_attribute():
    """
    Test 16.1.8h: __getattr__ raises AttributeError for invalid attributes.

    Accessing non-existent sections should raise helpful error.
    """
    # ARRANGE
    data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {"host": "localhost", "port": 5432, "name": "testdb"},
    }
    config = PrismConfig.from_dict(data)

    # ACT & ASSERT: Invalid attribute should raise error
    with pytest.raises(AttributeError) as exc_info:
        _ = config.nonexistent_section

    # ASSERT: Error message is helpful
    assert "nonexistent_section" in str(exc_info.value)
    assert "Available sections" in str(exc_info.value)


def test_getattr_private_attribute():
    """
    Test 16.1.8i: __getattr__ handles private attributes correctly.

    Private attributes (starting with _) should raise AttributeError.
    """
    # ARRANGE
    data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {"host": "localhost", "port": 5432, "name": "testdb"},
    }
    config = PrismConfig.from_dict(data)

    # ACT & ASSERT: Private attributes raise error
    with pytest.raises(AttributeError):
        _ = config._nonexistent


# ============================================================================
# Tests: Schema Validation
# ============================================================================


def test_invalid_schema_type():
    """
    Test 16.1.8j: Invalid schema type raises ConfigValidationError.

    Passing a non-BaseModel class should fail with helpful error.
    """
    # ARRANGE
    data = {"name": "test"}

    class NotAModel:
        pass

    # ACT & ASSERT: Should fail with validation error
    with pytest.raises(ConfigValidationError) as exc_info:
        PrismConfig.from_dict(data, schema=NotAModel)

    assert "BaseModel" in str(exc_info.value)


def test_missing_required_fields():
    """
    Test 16.1.8k: Missing required fields raise ConfigValidationError.

    Custom schema with missing required fields should fail.
    """
    # ARRANGE: Missing jwt_secret which is required
    data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {"host": "localhost", "port": 5432, "name": "testdb"},
        "auth": {"token_expiry": 3600},  # Missing jwt_secret
        "rate_limit": {},
    }

    # ACT & ASSERT: Should fail with validation error
    with pytest.raises(ConfigValidationError):
        PrismConfig.from_dict(data, schema=CustomAppConfig)


def test_type_validation_error():
    """
    Test 16.1.8l: Type errors raise ConfigValidationError.

    Passing wrong types should fail validation.
    """
    # ARRANGE: token_expiry should be int, not string
    data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {"host": "localhost", "port": 5432, "name": "testdb"},
        "auth": {"jwt_secret": "secret", "token_expiry": "not-an-int"},
        "rate_limit": {},
    }

    # ACT & ASSERT: Should fail with validation error
    with pytest.raises(ConfigValidationError):
        PrismConfig.from_dict(data, schema=CustomAppConfig)


# ============================================================================
# Tests: Flexible Schema (extra="allow")
# ============================================================================


def test_flexible_schema_allows_extra(custom_data):
    """
    Test 16.1.8m: Flexible schema allows extra fields.

    Schema with extra="allow" should accept unknown fields.
    """
    # ACT: FlexibleConfig allows extra fields
    config = PrismConfig.from_dict(custom_data, schema=FlexibleConfig)

    # ASSERT: Known sections work
    assert config.app.name == "test-app"
    assert config.database.host == "db.example.com"


# ============================================================================
# Tests: Display with Custom Schema
# ============================================================================


def test_dump_with_custom_schema(custom_data):
    """
    Test 16.1.8n: dump() works with custom schemas.

    Custom sections should appear in the dump output.
    """
    # ARRANGE
    config = PrismConfig.from_dict(custom_data, schema=CustomAppConfig)

    # ACT
    dump = config.dump(use_color=False)

    # ASSERT: Custom sections appear in output
    assert "auth.jwt_secret" in dump
    assert "auth.token_expiry" in dump
    assert "rate_limit.requests_per_minute" in dump


def test_to_dict_with_custom_schema(custom_data):
    """
    Test 16.1.8o: to_dict() works with custom schemas.

    All sections should be exported to dict.
    """
    # ARRANGE
    config = PrismConfig.from_dict(custom_data, schema=CustomAppConfig)

    # ACT
    result = config.to_dict()

    # ASSERT: All sections present
    assert "app" in result
    assert "database" in result
    assert "auth" in result
    assert "rate_limit" in result
    assert result["auth"]["jwt_secret"] == "super-secret-key"


# ============================================================================
# Tests: BaseConfigSection and BaseConfigRoot
# ============================================================================


def test_base_config_section_defaults():
    """
    Test 16.1.8p: BaseConfigSection has correct model_config.

    Should be frozen and validate_assignment.
    """
    # ASSERT: Check model_config
    assert BaseConfigSection.model_config.get("frozen") is True
    assert BaseConfigSection.model_config.get("validate_assignment") is True


def test_base_config_root_defaults():
    """
    Test 16.1.8q: BaseConfigRoot has correct model_config.

    Should be frozen, validate_assignment, and extra="forbid".
    """
    # ASSERT: Check model_config
    assert BaseConfigRoot.model_config.get("frozen") is True
    assert BaseConfigRoot.model_config.get("validate_assignment") is True
    assert BaseConfigRoot.model_config.get("extra") == "forbid"


def test_minimal_schema():
    """
    Test 16.1.8r: Minimal schema with single field works.

    Even simple schemas should work correctly.
    """
    # ARRANGE
    data = {"name": "minimal-config"}

    # ACT
    config = PrismConfig.from_dict(data, schema=MinimalConfig)

    # ASSERT
    assert config.name == "minimal-config"
