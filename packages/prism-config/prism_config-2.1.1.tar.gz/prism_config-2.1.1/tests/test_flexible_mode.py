"""
Tests for flexible/catch-all mode (v2.0.0+).

These tests verify:
- DynamicConfig dot notation access
- strict=False parameter for from_dict, from_file, from_all
- Nested configuration access
- Immutability (frozen mode)
- Integration with dump() and to_dict()
- Error handling for missing attributes
"""

import pytest

from prism.config import DynamicConfig, PrismConfig


# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def flexible_data():
    """Test data for flexible mode."""
    return {
        "auth": {
            "jwt": {
                "secret": "super-secret-key",
                "expiry": 3600,
                "issuer": "my-app",
            },
            "oauth": {
                "enabled": True,
                "providers": ["google", "github"],
            },
        },
        "rate_limit": {
            "requests_per_minute": 100,
            "burst_size": 20,
        },
        "custom_section": {
            "nested": {
                "deeply": {
                    "value": "found it!",
                }
            }
        },
    }


@pytest.fixture
def simple_data():
    """Simple test data."""
    return {
        "name": "my-app",
        "version": "1.0.0",
        "debug": True,
    }


# ============================================================================
# Tests: DynamicConfig Class
# ============================================================================


class TestDynamicConfig:
    """Tests for the DynamicConfig class."""

    def test_basic_attribute_access(self, simple_data):
        """
        Test 17.1.1a: DynamicConfig provides dot notation access.

        Basic attributes should be accessible via dot notation.
        """
        # ACT
        config = DynamicConfig(simple_data)

        # ASSERT
        assert config.name == "my-app"
        assert config.version == "1.0.0"
        assert config.debug is True

    def test_nested_attribute_access(self, flexible_data):
        """
        Test 17.1.1b: DynamicConfig supports nested dot notation.

        Deeply nested values should be accessible via chained dot notation.
        """
        # ACT
        config = DynamicConfig(flexible_data)

        # ASSERT
        assert config.auth.jwt.secret == "super-secret-key"
        assert config.auth.jwt.expiry == 3600
        assert config.auth.oauth.enabled is True
        assert config.custom_section.nested.deeply.value == "found it!"

    def test_dict_like_access(self, flexible_data):
        """
        Test 17.1.1c: DynamicConfig supports dict-like access.

        Values should be accessible via bracket notation.
        """
        # ACT
        config = DynamicConfig(flexible_data)

        # ASSERT
        assert config["auth"]["jwt"]["secret"] == "super-secret-key"
        assert config["rate_limit"]["requests_per_minute"] == 100

    def test_list_values_preserved(self, flexible_data):
        """
        Test 17.1.1d: Lists are preserved in DynamicConfig.

        List values should remain as lists.
        """
        # ACT
        config = DynamicConfig(flexible_data)

        # ASSERT
        assert config.auth.oauth.providers == ["google", "github"]
        assert isinstance(config.auth.oauth.providers, list)

    def test_frozen_prevents_modification(self, simple_data):
        """
        Test 17.1.1e: DynamicConfig is frozen by default.

        Attempting to modify should raise AttributeError.
        """
        # ACT
        config = DynamicConfig(simple_data, frozen=True)

        # ASSERT
        with pytest.raises(AttributeError) as exc_info:
            config.name = "new-name"

        assert "frozen" in str(exc_info.value)
        assert "immutable" in str(exc_info.value)

    def test_iteration(self, simple_data):
        """
        Test 17.1.1f: DynamicConfig supports iteration.

        Iterating should yield keys.
        """
        # ACT
        config = DynamicConfig(simple_data)
        keys = list(config)

        # ASSERT
        assert "name" in keys
        assert "version" in keys
        assert "debug" in keys
        assert len(keys) == 3

    def test_contains(self, simple_data):
        """
        Test 17.1.1g: DynamicConfig supports 'in' operator.

        The 'in' operator should check for key presence.
        """
        # ACT
        config = DynamicConfig(simple_data)

        # ASSERT
        assert "name" in config
        assert "version" in config
        assert "nonexistent" not in config

    def test_len(self, simple_data):
        """
        Test 17.1.1h: DynamicConfig supports len().

        len() should return number of top-level keys.
        """
        # ACT
        config = DynamicConfig(simple_data)

        # ASSERT
        assert len(config) == 3

    def test_to_dict(self, flexible_data):
        """
        Test 17.1.1i: DynamicConfig.to_dict() converts back to dict.

        to_dict() should return a plain Python dictionary.
        """
        # ACT
        config = DynamicConfig(flexible_data)
        result = config.to_dict()

        # ASSERT
        assert isinstance(result, dict)
        assert result["auth"]["jwt"]["secret"] == "super-secret-key"
        assert not isinstance(result["auth"], DynamicConfig)

    def test_get_method(self, simple_data):
        """
        Test 17.1.1j: DynamicConfig.get() works with defaults.

        get() should return default if key doesn't exist.
        """
        # ACT
        config = DynamicConfig(simple_data)

        # ASSERT
        assert config.get("name") == "my-app"
        assert config.get("nonexistent") is None
        assert config.get("nonexistent", "default") == "default"

    def test_invalid_attribute_error(self, simple_data):
        """
        Test 17.1.1k: DynamicConfig raises helpful AttributeError.

        Accessing non-existent attribute should raise helpful error.
        """
        # ACT
        config = DynamicConfig(simple_data)

        # ASSERT
        with pytest.raises(AttributeError) as exc_info:
            _ = config.nonexistent

        assert "nonexistent" in str(exc_info.value)
        assert "Available keys" in str(exc_info.value)

    def test_repr(self, simple_data):
        """
        Test 17.1.1l: DynamicConfig has useful repr.

        repr() should show class name and keys.
        """
        # ACT
        config = DynamicConfig(simple_data)

        # ASSERT
        repr_str = repr(config)
        assert "DynamicConfig" in repr_str


# ============================================================================
# Tests: PrismConfig Flexible Mode (from_dict)
# ============================================================================


class TestPrismConfigFlexibleFromDict:
    """Tests for PrismConfig.from_dict with strict=False."""

    def test_basic_flexible_mode(self, flexible_data):
        """
        Test 17.1.2a: PrismConfig.from_dict(strict=False) works.

        Flexible mode should accept any structure.
        """
        # ACT
        config = PrismConfig.from_dict(flexible_data, strict=False)

        # ASSERT
        assert config.auth.jwt.secret == "super-secret-key"
        assert config.rate_limit.requests_per_minute == 100

    def test_flexible_mode_no_validation(self):
        """
        Test 17.1.2b: Flexible mode doesn't validate against schema.

        Any structure should be accepted without validation errors.
        """
        # ARRANGE: Data that doesn't match default schema
        data = {
            "completely": {"custom": {"structure": True}},
            "no_app_section": True,
            "no_database_section": True,
        }

        # ACT: Should not raise validation error
        config = PrismConfig.from_dict(data, strict=False)

        # ASSERT
        assert config.completely.custom.structure is True
        assert config.no_app_section is True

    def test_flexible_mode_with_env_override(self, monkeypatch, flexible_data):
        """
        Test 17.1.2c: Flexible mode works with env overrides.

        Environment overrides should still work in flexible mode.
        """
        # ARRANGE
        monkeypatch.setenv("APP_AUTH__JWT__EXPIRY", "7200")

        # ACT
        config = PrismConfig.from_dict(
            flexible_data, apply_env=True, strict=False
        )

        # ASSERT: Env override should be applied
        assert config.auth.jwt.expiry == "7200"

    def test_flexible_mode_with_cli_override(self, flexible_data):
        """
        Test 17.1.2d: Flexible mode works with CLI overrides.

        CLI overrides should still work in flexible mode.
        """
        # ACT
        config = PrismConfig.from_dict(
            flexible_data,
            cli_args=["--auth.jwt.secret=new-secret"],
            strict=False,
        )

        # ASSERT: CLI override should be applied
        assert config.auth.jwt.secret == "new-secret"

    def test_flexible_mode_dump(self, flexible_data):
        """
        Test 17.1.2e: dump() works with flexible mode.

        Configuration should be dumpable to formatted string.
        """
        # ACT
        config = PrismConfig.from_dict(flexible_data, strict=False)
        dump = config.dump(use_color=False)

        # ASSERT
        assert "auth.jwt.secret" in dump
        assert "rate_limit.requests_per_minute" in dump

    def test_flexible_mode_to_dict(self, flexible_data):
        """
        Test 17.1.2f: to_dict() works with flexible mode.

        Should return plain Python dictionary.
        """
        # ACT
        config = PrismConfig.from_dict(flexible_data, strict=False)
        result = config.to_dict()

        # ASSERT
        assert isinstance(result, dict)
        assert result["auth"]["jwt"]["secret"] == "super-secret-key"

    def test_flexible_mode_to_yaml(self, flexible_data):
        """
        Test 17.1.2g: to_yaml() works with flexible mode.

        Should return YAML string.
        """
        # ACT
        config = PrismConfig.from_dict(flexible_data, strict=False)
        yaml_str = config.to_yaml()

        # ASSERT
        assert "auth:" in yaml_str
        assert "jwt:" in yaml_str
        assert "secret:" in yaml_str

    def test_flexible_mode_to_json(self, flexible_data):
        """
        Test 17.1.2h: to_json() works with flexible mode.

        Should return JSON string.
        """
        # ACT
        config = PrismConfig.from_dict(flexible_data, strict=False)
        json_str = config.to_json()

        # ASSERT
        assert '"auth"' in json_str
        assert '"jwt"' in json_str
        assert '"secret"' in json_str

    def test_flexible_mode_repr(self, flexible_data):
        """
        Test 17.1.2i: repr() shows flexible mode.

        repr should indicate flexible mode.
        """
        # ACT
        config = PrismConfig.from_dict(flexible_data, strict=False)
        repr_str = repr(config)

        # ASSERT
        assert "flexible" in repr_str
        assert "PrismConfig" in repr_str


# ============================================================================
# Tests: PrismConfig Flexible Mode (from_file)
# ============================================================================


class TestPrismConfigFlexibleFromFile:
    """Tests for PrismConfig.from_file with strict=False."""

    def test_from_file_flexible_mode(self, tmp_path):
        """
        Test 17.1.3a: from_file works with strict=False.

        Should load any YAML structure without validation.
        """
        # ARRANGE
        config_file = tmp_path / "config.yaml"
        config_file.write_text("""
auth:
  jwt:
    secret: file-secret
    expiry: 1800
rate_limit:
  requests: 50
""")

        # ACT
        config = PrismConfig.from_file(config_file, strict=False)

        # ASSERT
        assert config.auth.jwt.secret == "file-secret"
        assert config.rate_limit.requests == 50

    def test_from_all_flexible_mode(self, tmp_path):
        """
        Test 17.1.3b: from_all works with strict=False.

        Should load file with env overrides in flexible mode.
        """
        # ARRANGE
        config_file = tmp_path / "config.yaml"
        config_file.write_text("""
auth:
  jwt:
    secret: original
""")

        # ACT
        config = PrismConfig.from_all(config_file, strict=False)

        # ASSERT
        assert config.auth.jwt.secret == "original"


# ============================================================================
# Tests: Backward Compatibility
# ============================================================================


class TestBackwardCompatibility:
    """Tests to ensure strict mode still works correctly."""

    def test_default_is_strict_mode(self):
        """
        Test 17.1.4a: Default behavior is strict mode.

        Without strict parameter, should use schema validation.
        """
        # ARRANGE: Invalid data for default schema
        data = {"invalid": "structure"}

        # ACT & ASSERT: Should fail validation
        from prism.config import ConfigValidationError

        with pytest.raises(ConfigValidationError):
            PrismConfig.from_dict(data)

    def test_strict_true_validates(self):
        """
        Test 17.1.4b: strict=True validates against schema.

        Explicitly passing strict=True should validate.
        """
        # ARRANGE
        valid_data = {
            "app": {"name": "test", "environment": "dev"},
            "database": {"host": "localhost", "port": 5432, "name": "testdb"},
        }

        # ACT
        config = PrismConfig.from_dict(valid_data, strict=True)

        # ASSERT
        assert config.app.name == "test"

    def test_schema_ignored_in_flexible_mode(self, flexible_data):
        """
        Test 17.1.4c: schema parameter is ignored when strict=False.

        Passing schema with strict=False should not affect behavior.
        """
        from prism.config import ConfigRoot

        # ACT: Pass schema but also strict=False
        config = PrismConfig.from_dict(
            flexible_data, schema=ConfigRoot, strict=False
        )

        # ASSERT: Should work with flexible data
        assert config.auth.jwt.secret == "super-secret-key"


# ============================================================================
# Tests: Edge Cases
# ============================================================================


class TestEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_empty_dict(self):
        """
        Test 17.1.5a: Empty dict works in flexible mode.

        Empty configuration should be allowed.
        """
        # ACT
        config = PrismConfig.from_dict({}, strict=False)

        # ASSERT
        assert len(list(config._config.keys())) == 0

    def test_single_level_config(self):
        """
        Test 17.1.5b: Single-level config works.

        Non-nested configuration should work.
        """
        # ACT
        config = PrismConfig.from_dict(
            {"key1": "value1", "key2": "value2"}, strict=False
        )

        # ASSERT
        assert config.key1 == "value1"
        assert config.key2 == "value2"

    def test_special_characters_in_keys(self):
        """
        Test 17.1.5c: Keys with underscores work.

        Keys with underscores should be accessible.
        """
        # ACT
        config = PrismConfig.from_dict(
            {"rate_limit": {"max_requests": 100}}, strict=False
        )

        # ASSERT
        assert config.rate_limit.max_requests == 100

    def test_numeric_values_preserved(self):
        """
        Test 17.1.5d: Numeric values are preserved.

        Int and float values should maintain their types.
        """
        # ACT
        config = PrismConfig.from_dict(
            {"count": 42, "rate": 3.14, "enabled": True}, strict=False
        )

        # ASSERT
        assert config.count == 42
        assert isinstance(config.count, int)
        assert config.rate == 3.14
        assert isinstance(config.rate, float)
        assert config.enabled is True
        assert isinstance(config.enabled, bool)

    def test_none_values(self):
        """
        Test 17.1.5e: None values are handled.

        None values should be preserved.
        """
        # ACT
        config = PrismConfig.from_dict(
            {"nullable": None}, strict=False
        )

        # ASSERT
        assert config.nullable is None

    def test_deeply_nested_config(self):
        """
        Test 17.1.5f: Very deep nesting works.

        Multiple levels of nesting should work.
        """
        # ARRANGE
        data = {
            "level1": {
                "level2": {
                    "level3": {
                        "level4": {
                            "level5": {
                                "value": "deep"
                            }
                        }
                    }
                }
            }
        }

        # ACT
        config = PrismConfig.from_dict(data, strict=False)

        # ASSERT
        assert config.level1.level2.level3.level4.level5.value == "deep"

    def test_list_of_dicts(self):
        """
        Test 17.1.5g: List of dicts converts nested dicts.

        Dicts inside lists should also become DynamicConfig.
        """
        # ARRANGE
        data = {
            "servers": [
                {"host": "server1.com", "port": 8080},
                {"host": "server2.com", "port": 8081},
            ]
        }

        # ACT
        config = PrismConfig.from_dict(data, strict=False)

        # ASSERT
        assert config.servers[0].host == "server1.com"
        assert config.servers[1].port == 8081


# ============================================================================
# Tests: Hybrid Mode (Typed + Flexible)
# ============================================================================


class TestHybridMode:
    """Tests for hybrid mode - typed sections with flexible extras."""

    def test_hybrid_schema_with_extra_allow(self):
        """
        Test 17.2.1a: Schema with extra='allow' accepts unknown fields.

        Typed fields should be validated, extras should be accepted.
        """
        from pydantic import BaseModel

        from prism.config import AppConfig, DatabaseConfig

        # ARRANGE
        class HybridConfig(BaseModel):
            app: AppConfig
            database: DatabaseConfig

            model_config = {
                "extra": "allow",
                "frozen": True,
            }

        data = {
            "app": {"name": "hybrid-app", "environment": "dev"},
            "database": {"host": "localhost", "port": 5432, "name": "testdb"},
            "custom_section": {"key": "value"},  # Extra field
            "another_extra": {"nested": {"deep": True}},
        }

        # ACT
        config = PrismConfig.from_dict(data, schema=HybridConfig)

        # ASSERT: Typed sections work
        assert config.app.name == "hybrid-app"
        assert config.database.host == "localhost"

        # ASSERT: Extra sections are accessible as dicts
        # (Pydantic stores extras as-is, not as DynamicConfig)
        assert config._config.custom_section == {"key": "value"}

    def test_hybrid_schema_validates_typed_fields(self):
        """
        Test 17.2.1b: Hybrid schema validates typed fields.

        Invalid typed fields should raise validation error.
        """
        from pydantic import BaseModel

        from prism.config import AppConfig, ConfigValidationError, DatabaseConfig

        # ARRANGE
        class HybridConfig(BaseModel):
            app: AppConfig
            database: DatabaseConfig
            model_config = {"extra": "allow"}

        data = {
            "app": {"name": "test"},  # Missing 'environment'
            "database": {"host": "localhost", "port": 5432, "name": "testdb"},
            "custom": {"anything": "goes"},
        }

        # ACT & ASSERT
        with pytest.raises(ConfigValidationError):
            PrismConfig.from_dict(data, schema=HybridConfig)

    def test_hybrid_dump_includes_extras(self):
        """
        Test 17.2.1c: dump() includes extra fields in output.

        Extra fields should appear in the dump output.
        """
        from pydantic import BaseModel

        from prism.config import AppConfig, DatabaseConfig

        # ARRANGE
        class HybridConfig(BaseModel):
            app: AppConfig
            database: DatabaseConfig
            model_config = {"extra": "allow", "frozen": True}

        data = {
            "app": {"name": "test-app", "environment": "dev"},
            "database": {"host": "localhost", "port": 5432, "name": "testdb"},
            "metrics": {"enabled": True, "interval": 60},
        }

        # ACT
        config = PrismConfig.from_dict(data, schema=HybridConfig)
        dump = config.dump(use_color=False)

        # ASSERT
        assert "app.name" in dump
        assert "metrics.enabled" in dump
        assert "metrics.interval" in dump

    def test_hybrid_to_dict_includes_extras(self):
        """
        Test 17.2.1d: to_dict() includes extra fields.

        Extra fields should be included in dictionary export.
        """
        from pydantic import BaseModel

        from prism.config import AppConfig, DatabaseConfig

        # ARRANGE
        class HybridConfig(BaseModel):
            app: AppConfig
            database: DatabaseConfig
            model_config = {"extra": "allow", "frozen": True}

        data = {
            "app": {"name": "test-app", "environment": "dev"},
            "database": {"host": "localhost", "port": 5432, "name": "testdb"},
            "logging": {"level": "DEBUG"},
        }

        # ACT
        config = PrismConfig.from_dict(data, schema=HybridConfig)
        result = config.to_dict()

        # ASSERT
        assert "logging" in result
        assert result["logging"]["level"] == "DEBUG"

    def test_base_config_root_with_extra_allow(self):
        """
        Test 17.2.2a: BaseConfigRoot can be customized with extra='allow'.

        Users can override BaseConfigRoot to allow extras.
        """
        from prism.config import AppConfig, BaseConfigRoot, DatabaseConfig

        # ARRANGE
        class FlexibleRoot(BaseConfigRoot):
            app: AppConfig
            database: DatabaseConfig

            model_config = {
                "extra": "allow",  # Override to allow extras
                "frozen": True,
                "validate_assignment": True,
            }

        data = {
            "app": {"name": "flex-app", "environment": "prod"},
            "database": {"host": "db.example.com", "port": 5432, "name": "proddb"},
            "cache": {"redis": {"host": "redis.example.com", "port": 6379}},
        }

        # ACT
        config = PrismConfig.from_dict(data, schema=FlexibleRoot)

        # ASSERT
        assert config.app.name == "flex-app"
        assert config._config.cache == {"redis": {"host": "redis.example.com", "port": 6379}}

    def test_nested_typed_sections(self):
        """
        Test 17.2.2b: Nested typed sections work in hybrid mode.

        Complex nested typed structures should work.
        """
        from prism.config import AppConfig, BaseConfigRoot, BaseConfigSection, DatabaseConfig

        # ARRANGE
        class JWTConfig(BaseConfigSection):
            secret: str
            expiry: int = 3600

        class AuthConfig(BaseConfigSection):
            jwt: JWTConfig
            enabled: bool = True

        class MyConfig(BaseConfigRoot):
            app: AppConfig
            database: DatabaseConfig
            auth: AuthConfig

            model_config = {
                "extra": "allow",
                "frozen": True,
                "validate_assignment": True,
            }

        data = {
            "app": {"name": "nested-app", "environment": "dev"},
            "database": {"host": "localhost", "port": 5432, "name": "testdb"},
            "auth": {"jwt": {"secret": "my-secret", "expiry": 7200}, "enabled": True},
            "extra_section": {"key": "value"},
        }

        # ACT
        config = PrismConfig.from_dict(data, schema=MyConfig)

        # ASSERT
        assert config.auth.jwt.secret == "my-secret"
        assert config.auth.jwt.expiry == 7200
        assert config._config.extra_section == {"key": "value"}
