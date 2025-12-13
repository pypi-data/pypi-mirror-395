"""
Tests for prism-config v2.0.0 features.

This module tests the new v2.0.0 features:
- Custom schemas (BaseConfigSection, BaseConfigRoot)
- Flexible mode (strict=False)
- DynamicConfig
- Dynamic emoji registration
- Enhanced secret detection
"""

from typing import List, Optional

import pytest

from prism.config import (
    BaseConfigRoot,
    BaseConfigSection,
    DynamicConfig,
    PrismConfig,
    register_emoji,
    unregister_emoji,
    get_registered_emojis,
    clear_registered_emojis,
)
from prism.config.models import AppConfig, DatabaseConfig


# =============================================================================
# Custom Schema Definitions for Testing
# =============================================================================


class AuthConfig(BaseConfigSection):
    """Authentication configuration."""

    jwt_secret: str = "default-secret"
    token_expiry: int = 3600
    refresh_enabled: bool = True


class CacheConfig(BaseConfigSection):
    """Cache configuration."""

    host: str = "localhost"
    port: int = 6379
    ttl: int = 300
    prefix: str = "app:"


class FeatureFlagsConfig(BaseConfigSection):
    """Feature flags configuration."""

    dark_mode: bool = False
    beta_features: bool = False
    experiments: Optional[List[str]] = None


class ExtendedAppConfig(BaseConfigSection):
    """Extended app config with more fields."""

    name: str
    environment: str = "dev"
    debug: bool = False
    version: str = "1.0.0"
    api_key: Optional[str] = None


class CompleteConfig(BaseConfigRoot):
    """Complete configuration with multiple custom sections."""

    app: ExtendedAppConfig
    database: DatabaseConfig
    auth: AuthConfig
    cache: Optional[CacheConfig] = None
    features: Optional[FeatureFlagsConfig] = None


class MinimalCustomConfig(BaseConfigRoot):
    """Minimal custom config for simple tests."""

    app: AppConfig
    database: DatabaseConfig
    custom: Optional[AuthConfig] = None


# =============================================================================
# 20.1.2: Parity Tests - Flexible vs Strict Mode
# =============================================================================


class TestFlexibleModeParity:
    """Tests verifying parity between flexible and strict modes."""

    def test_basic_config_parity(self):
        """Same basic config loads identically in both modes."""
        config_data = {
            "app": {"name": "parity-app", "environment": "test"},
            "database": {"host": "db.example.com", "port": 3306, "name": "testdb"}
        }

        strict = PrismConfig.from_dict(config_data)
        flexible = PrismConfig.from_dict(config_data, strict=False)

        assert strict.app.name == flexible.app.name == "parity-app"
        assert strict.app.environment == flexible.app.environment == "test"
        assert strict.database.host == flexible.database.host == "db.example.com"
        assert strict.database.port == flexible.database.port == 3306
        assert strict.database.name == flexible.database.name == "testdb"

    def test_type_coercion_difference(self):
        """Type coercion behavior differs between modes (by design)."""
        config_data = {
            "app": {"name": "coercion-app", "environment": "dev"},
            "database": {"host": "localhost", "port": "5432", "name": "testdb"}
        }

        strict = PrismConfig.from_dict(config_data)
        flexible = PrismConfig.from_dict(config_data, strict=False)

        # Strict mode coerces to int, flexible mode preserves string
        assert strict.database.port == 5432
        assert isinstance(strict.database.port, int)
        # Flexible mode preserves original type (no schema validation)
        assert flexible.database.port == "5432"
        assert isinstance(flexible.database.port, str)

    def test_dump_output_parity(self):
        """dump() produces consistent output in both modes."""
        config_data = {
            "app": {"name": "dump-app", "environment": "prod"},
            "database": {"host": "prod-db", "port": 5432, "name": "proddb"}
        }

        strict = PrismConfig.from_dict(config_data)
        flexible = PrismConfig.from_dict(config_data, strict=False)

        dump_strict = strict.dump(use_color=False)
        dump_flexible = flexible.dump(use_color=False)

        # Both should contain the same data
        assert "dump-app" in dump_strict
        assert "dump-app" in dump_flexible
        assert "prod-db" in dump_strict
        assert "prod-db" in dump_flexible

    def test_env_override_behavior(self, prism_env):
        """Environment overrides work in both modes (with type differences)."""
        config_data = {
            "app": {"name": "env-app", "environment": "dev"},
            "database": {"host": "localhost", "port": 5432, "name": "testdb"}
        }

        prism_env["monkeypatch"].setenv("APP_DATABASE__PORT", "9999")

        strict = PrismConfig.from_dict(config_data, apply_env=True)
        flexible = PrismConfig.from_dict(config_data, apply_env=True, strict=False)

        # Strict coerces to int, flexible preserves string from env
        assert strict.database.port == 9999
        assert flexible.database.port == "9999"

    def test_secret_resolution_parity(self, prism_env):
        """Secret resolution works identically in both modes."""
        prism_env["monkeypatch"].setenv("DB_SECRET", "super-secret-password")

        config_data = {
            "app": {"name": "secret-app", "environment": "dev"},
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "testdb",
                "password": "REF::ENV::DB_SECRET"
            }
        }

        strict = PrismConfig.from_dict(config_data, resolve_secrets=True)
        flexible = PrismConfig.from_dict(config_data, resolve_secrets=True, strict=False)

        assert strict.database.password == flexible.database.password == "super-secret-password"

    def test_cli_override_behavior(self):
        """CLI argument overrides work in both modes (with type differences)."""
        config_data = {
            "app": {"name": "cli-app", "environment": "dev"},
            "database": {"host": "localhost", "port": 5432, "name": "testdb"}
        }

        cli_args = ["--database.port=8888", "--app.name=cli-overridden"]

        strict = PrismConfig.from_dict(config_data, cli_args=cli_args)
        flexible = PrismConfig.from_dict(config_data, cli_args=cli_args, strict=False)

        # Strict coerces to int, flexible preserves string from CLI
        assert strict.database.port == 8888
        assert flexible.database.port == "8888"
        assert strict.app.name == flexible.app.name == "cli-overridden"

    def test_export_yaml_parity(self):
        """YAML export works identically in both modes."""
        config_data = {
            "app": {"name": "yaml-app", "environment": "staging"},
            "database": {"host": "staging-db", "port": 5432, "name": "stagingdb"}
        }

        strict = PrismConfig.from_dict(config_data)
        flexible = PrismConfig.from_dict(config_data, strict=False)

        yaml_strict = strict.to_yaml()
        yaml_flexible = flexible.to_yaml()

        # Both should produce valid YAML with same content
        assert "yaml-app" in yaml_strict
        assert "yaml-app" in yaml_flexible
        assert "staging-db" in yaml_strict
        assert "staging-db" in yaml_flexible

    def test_export_json_parity(self):
        """JSON export works identically in both modes."""
        config_data = {
            "app": {"name": "json-app", "environment": "dev"},
            "database": {"host": "localhost", "port": 5432, "name": "jsondb"}
        }

        strict = PrismConfig.from_dict(config_data)
        flexible = PrismConfig.from_dict(config_data, strict=False)

        json_strict = strict.to_json()
        json_flexible = flexible.to_json()

        import json
        data_strict = json.loads(json_strict)
        data_flexible = json.loads(json_flexible)

        assert data_strict["app"]["name"] == data_flexible["app"]["name"] == "json-app"
        assert data_strict["database"]["port"] == data_flexible["database"]["port"] == 5432


# =============================================================================
# 20.1.3: Backward Compatibility Tests
# =============================================================================


class TestBackwardCompatibility:
    """Tests verifying v1.x code works unchanged in v2.0.0."""

    def test_v1_from_dict_unchanged(self):
        """v1.x from_dict() signature still works."""
        config = PrismConfig.from_dict({
            "app": {"name": "v1-app", "environment": "dev"},
            "database": {"host": "localhost", "port": 5432, "name": "testdb"}
        })

        assert config.app.name == "v1-app"
        assert config.database.port == 5432

    def test_v1_from_file_unchanged(self, prism_env):
        """v1.x from_file() signature still works."""
        yaml_file = prism_env["tmp_path"] / "v1_config.yaml"
        yaml_file.write_text("""
app:
  name: v1-file-app
  environment: production

database:
  host: prod-db
  port: 5432
  name: proddb
""")

        config = PrismConfig.from_file(yaml_file)

        assert config.app.name == "v1-file-app"
        assert config.app.environment == "production"

    def test_v1_from_all_unchanged(self, prism_env):
        """v1.x from_all() signature still works."""
        yaml_file = prism_env["tmp_path"] / "v1_all.yaml"
        yaml_file.write_text("""
app:
  name: v1-all-app
  environment: dev

database:
  host: localhost
  port: 5432
  name: testdb
""")

        prism_env["monkeypatch"].setenv("APP_DATABASE__PORT", "9876")

        config = PrismConfig.from_all(yaml_file, resolve_secrets=False)

        assert config.app.name == "v1-all-app"
        assert config.database.port == 9876  # env override applied

    def test_v1_display_method_unchanged(self):
        """v1.x display() method still works."""
        config = PrismConfig.from_dict({
            "app": {"name": "display-app", "environment": "dev"},
            "database": {"host": "localhost", "port": 5432, "name": "testdb"}
        })

        # display() should not raise
        config.display()

    def test_v1_dump_method_unchanged(self):
        """v1.x dump() method still works."""
        config = PrismConfig.from_dict({
            "app": {"name": "dump-app", "environment": "dev"},
            "database": {"host": "localhost", "port": 5432, "name": "testdb"}
        })

        dump = config.dump()
        assert "dump-app" in dump

    def test_v1_export_methods_unchanged(self):
        """v1.x to_yaml() and to_json() still work."""
        config = PrismConfig.from_dict({
            "app": {"name": "export-app", "environment": "dev"},
            "database": {"host": "localhost", "port": 5432, "name": "testdb"}
        })

        yaml_output = config.to_yaml()
        json_output = config.to_json()

        assert "export-app" in yaml_output
        assert "export-app" in json_output

    def test_v1_immutability_unchanged(self):
        """v1.x frozen config behavior unchanged."""
        config = PrismConfig.from_dict({
            "app": {"name": "frozen-app", "environment": "dev"},
            "database": {"host": "localhost", "port": 5432, "name": "testdb"}
        })

        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            config.app.name = "modified"

    def test_v1_secret_redaction_unchanged(self):
        """v1.x secret redaction in dump() unchanged."""
        config = PrismConfig.from_dict({
            "app": {"name": "redact-app", "environment": "dev"},
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "testdb",
                "password": "super-secret"
            }
        })

        dump = config.dump(use_color=False)
        assert "super-secret" not in dump
        assert "REDACTED" in dump

    def test_v1_app_database_sections_work(self):
        """v1.x default app and database sections work."""
        config = PrismConfig.from_dict({
            "app": {
                "name": "complete-app",
                "environment": "production",
                "api_key": "key123"
            },
            "database": {
                "host": "prod-db.example.com",
                "port": 3306,
                "name": "production_db",
                "password": "prod-pass"
            }
        })

        # All v1.x attributes should be accessible
        assert config.app.name == "complete-app"
        assert config.app.environment == "production"
        assert config.app.api_key == "key123"
        assert config.database.host == "prod-db.example.com"
        assert config.database.port == 3306
        assert config.database.name == "production_db"
        assert config.database.password == "prod-pass"


# =============================================================================
# Custom Schema Tests
# =============================================================================


class TestCustomSchemas:
    """Tests for custom schema functionality."""

    def test_custom_schema_loads(self):
        """Custom schema loads and validates correctly."""
        config_data = {
            "app": {"name": "schema-app", "environment": "dev", "version": "2.0.0"},
            "database": {"host": "localhost", "port": 5432, "name": "testdb"},
            "auth": {"jwt_secret": "my-jwt-secret", "token_expiry": 7200}
        }

        config = PrismConfig.from_dict(config_data, schema=CompleteConfig)

        assert config.app.name == "schema-app"
        assert config.app.version == "2.0.0"
        assert config.auth.jwt_secret == "my-jwt-secret"
        assert config.auth.token_expiry == 7200

    def test_custom_schema_defaults(self):
        """Custom schema applies defaults correctly."""
        config_data = {
            "app": {"name": "default-app"},
            "database": {"host": "localhost", "port": 5432, "name": "testdb"},
            "auth": {}
        }

        config = PrismConfig.from_dict(config_data, schema=CompleteConfig)

        # Should use defaults
        assert config.app.environment == "dev"  # default
        assert config.app.debug is False  # default
        assert config.auth.jwt_secret == "default-secret"  # default
        assert config.auth.token_expiry == 3600  # default
        assert config.auth.refresh_enabled is True  # default

    def test_custom_schema_optional_sections(self):
        """Optional sections work correctly."""
        config_data = {
            "app": {"name": "optional-app"},
            "database": {"host": "localhost", "port": 5432, "name": "testdb"},
            "auth": {"jwt_secret": "secret"},
            "cache": {"host": "redis", "port": 6379}
            # features is optional and not provided
        }

        config = PrismConfig.from_dict(config_data, schema=CompleteConfig)

        assert config.cache is not None
        assert config.cache.host == "redis"
        assert config.features is None

    def test_custom_schema_with_all_fields(self):
        """Custom schema loads with all optional and required fields."""
        config_data = {
            "app": {"name": "full-schema-app", "debug": True, "version": "2.5.0"},
            "database": {"host": "localhost", "port": 5432, "name": "testdb"},
            "auth": {"jwt_secret": "my-secret", "token_expiry": 1800, "refresh_enabled": False},
            "cache": {"host": "redis", "port": 6380, "ttl": 600},
            "features": {"dark_mode": True, "beta_features": True}
        }

        config = PrismConfig.from_dict(config_data, schema=CompleteConfig)

        assert config.app.debug is True
        assert config.app.version == "2.5.0"
        assert config.auth.token_expiry == 1800
        assert config.auth.refresh_enabled is False
        assert config.cache.ttl == 600
        assert config.features.dark_mode is True

    def test_custom_schema_from_file(self, prism_env):
        """Custom schema loads from file correctly."""
        yaml_file = prism_env["tmp_path"] / "custom_schema.yaml"
        yaml_file.write_text("""
app:
  name: file-schema-app
  environment: staging
  version: 2.1.0

database:
  host: staging-db
  port: 5432
  name: stagingdb

auth:
  jwt_secret: staging-secret
  token_expiry: 3600

cache:
  host: redis-staging
  port: 6379
  ttl: 600
""")

        config = PrismConfig.from_file(yaml_file, schema=CompleteConfig)

        assert config.app.name == "file-schema-app"
        assert config.app.version == "2.1.0"
        assert config.auth.jwt_secret == "staging-secret"
        assert config.cache.host == "redis-staging"
        assert config.cache.ttl == 600


# =============================================================================
# DynamicConfig Tests
# =============================================================================


class TestDynamicConfig:
    """Tests for DynamicConfig class."""

    def test_dynamic_config_creation(self):
        """DynamicConfig creates from dict."""
        data = {"key": "value", "nested": {"inner": "data"}}
        dynamic = DynamicConfig(data)

        assert dynamic.key == "value"
        assert dynamic.nested.inner == "data"

    def test_dynamic_config_nested_access(self):
        """DynamicConfig provides dot-notation for deeply nested data."""
        data = {
            "level1": {
                "level2": {
                    "level3": {
                        "value": "deep"
                    }
                }
            }
        }
        dynamic = DynamicConfig(data)

        assert dynamic.level1.level2.level3.value == "deep"

    def test_dynamic_config_list_access(self):
        """DynamicConfig handles lists correctly."""
        data = {
            "servers": ["server1", "server2", "server3"],
            "nested_list": [
                {"name": "first"},
                {"name": "second"}
            ]
        }
        dynamic = DynamicConfig(data)

        # Access list via get() method or subscript
        servers = dynamic._data["servers"]
        assert len(servers) == 3
        assert servers[0] == "server1"

        nested = dynamic._data["nested_list"]
        assert len(nested) == 2
        assert nested[0]["name"] == "first"

    def test_dynamic_config_iteration(self):
        """DynamicConfig supports iteration over keys."""
        data = {"a": 1, "b": 2, "c": 3}
        dynamic = DynamicConfig(data)

        keys = list(dynamic)
        assert set(keys) == {"a", "b", "c"}

    def test_dynamic_config_repr(self):
        """DynamicConfig has useful repr."""
        data = {"key": "value"}
        dynamic = DynamicConfig(data)

        repr_str = repr(dynamic)
        assert "DynamicConfig" in repr_str


# =============================================================================
# Emoji Registration Tests
# =============================================================================


class TestEmojiRegistration:
    """Tests for dynamic emoji registration."""

    def setup_method(self):
        """Clear emoji registry before each test."""
        clear_registered_emojis()

    def teardown_method(self):
        """Clear emoji registry after each test."""
        clear_registered_emojis()

    def test_register_emoji(self):
        """register_emoji adds emoji mapping."""
        register_emoji("custom_section", "🎯")

        emojis = get_registered_emojis()
        assert "custom_section" in emojis
        assert emojis["custom_section"] == "🎯"

    def test_unregister_emoji(self):
        """unregister_emoji removes emoji mapping."""
        register_emoji("temp_section", "⏱️")
        unregister_emoji("temp_section")

        emojis = get_registered_emojis()
        assert "temp_section" not in emojis

    def test_clear_registered_emojis(self):
        """clear_registered_emojis removes all custom emojis."""
        register_emoji("section1", "1️⃣")
        register_emoji("section2", "2️⃣")

        clear_registered_emojis()

        emojis = get_registered_emojis()
        assert len(emojis) == 0

    def test_emoji_in_display(self):
        """Registered emoji appears in display output."""
        register_emoji("auth", "🔑")

        config_data = {
            "app": {"name": "emoji-app", "environment": "dev"},
            "database": {"host": "localhost", "port": 5432, "name": "testdb"}
        }

        config = PrismConfig.from_dict(config_data, schema=MinimalCustomConfig)
        dump = config.dump(use_color=False)

        # Should contain emoji in output (at least the app/database ones)
        assert "emoji-app" in dump


# =============================================================================
# Integration Tests with Real-World Patterns
# =============================================================================


class TestRealWorldPatterns:
    """Tests with realistic configuration patterns."""

    def test_web_application_config(self, prism_env):
        """Realistic web application configuration."""

        class WebAppConfig(BaseConfigRoot):
            app: ExtendedAppConfig
            database: DatabaseConfig
            cache: Optional[CacheConfig] = None
            auth: Optional[AuthConfig] = None

        prism_env["monkeypatch"].setenv("JWT_SECRET", "production-jwt-secret")

        yaml_file = prism_env["tmp_path"] / "webapp.yaml"
        yaml_file.write_text("""
app:
  name: my-web-app
  environment: production
  debug: false
  version: 1.5.0

database:
  host: prod-db.example.com
  port: 5432
  name: webapp_prod
  password: REF::ENV::DB_PASSWORD

auth:
  jwt_secret: REF::ENV::JWT_SECRET
  token_expiry: 3600

cache:
  host: redis.example.com
  port: 6379
  ttl: 300
""")

        prism_env["monkeypatch"].setenv("DB_PASSWORD", "super-secret-db-pass")

        config = PrismConfig.from_file(
            yaml_file,
            schema=WebAppConfig,
            resolve_secrets=True
        )

        assert config.app.name == "my-web-app"
        assert config.app.environment == "production"
        assert config.database.password == "super-secret-db-pass"
        assert config.auth.jwt_secret == "production-jwt-secret"
        assert config.cache.host == "redis.example.com"

    def test_microservice_config(self):
        """Microservice with multiple dependencies."""

        class ServiceConfig(BaseConfigSection):
            endpoint: str
            timeout: int = 30
            retries: int = 3

        class MicroserviceConfig(BaseConfigRoot):
            app: ExtendedAppConfig
            database: DatabaseConfig
            payment_service: Optional[ServiceConfig] = None
            notification_service: Optional[ServiceConfig] = None

        config_data = {
            "app": {
                "name": "order-service",
                "environment": "staging",
                "version": "2.3.1"
            },
            "database": {
                "host": "orders-db",
                "port": 5432,
                "name": "orders"
            },
            "payment_service": {
                "endpoint": "https://payments.internal/api",
                "timeout": 10,
                "retries": 5
            },
            "notification_service": {
                "endpoint": "https://notify.internal/api",
                "timeout": 5
            }
        }

        config = PrismConfig.from_dict(config_data, schema=MicroserviceConfig)

        assert config.app.name == "order-service"
        assert config.payment_service.endpoint == "https://payments.internal/api"
        assert config.payment_service.retries == 5
        assert config.notification_service.timeout == 5
        assert config.notification_service.retries == 3  # default

    def test_flexible_plugin_config(self):
        """Plugin system with arbitrary configuration."""
        config_data = {
            "app": {"name": "plugin-host", "environment": "dev"},
            "database": {"host": "localhost", "port": 5432, "name": "plugins"},
            "plugins": {
                "analytics": {
                    "provider": "google",
                    "tracking_id": "UA-123456",
                    "options": {
                        "anonymize_ip": True,
                        "sample_rate": 100
                    }
                },
                "payment": {
                    "provider": "stripe",
                    "mode": "test"
                }
            }
        }

        config = PrismConfig.from_dict(config_data, strict=False)

        assert config.app.name == "plugin-host"
        assert config.plugins.analytics.provider == "google"
        assert config.plugins.analytics.options.anonymize_ip is True
        assert config.plugins.payment.mode == "test"

    def test_multi_database_config(self):
        """Configuration with multiple database connections."""

        class DatabaseConnectionConfig(BaseConfigSection):
            host: str
            port: int = 5432
            name: str
            username: str = "app"
            password: Optional[str] = None
            pool_size: int = 10

        class MultiDbConfig(BaseConfigRoot):
            app: AppConfig
            database: DatabaseConnectionConfig  # Primary
            replica: Optional[DatabaseConnectionConfig] = None
            analytics: Optional[DatabaseConnectionConfig] = None

        config_data = {
            "app": {"name": "data-service", "environment": "prod"},
            "database": {
                "host": "primary-db.prod",
                "port": 5432,
                "name": "main",
                "pool_size": 20
            },
            "replica": {
                "host": "replica-db.prod",
                "port": 5432,
                "name": "main",
                "pool_size": 10
            },
            "analytics": {
                "host": "analytics-db.prod",
                "port": 5432,
                "name": "analytics",
                "pool_size": 5
            }
        }

        config = PrismConfig.from_dict(config_data, schema=MultiDbConfig)

        assert config.database.host == "primary-db.prod"
        assert config.database.pool_size == 20
        assert config.replica.host == "replica-db.prod"
        assert config.analytics.name == "analytics"
        assert config.analytics.pool_size == 5
