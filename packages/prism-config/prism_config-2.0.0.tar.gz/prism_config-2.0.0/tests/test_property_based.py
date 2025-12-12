"""
Property-based tests for prism-config using Hypothesis.

This module uses property-based testing to verify that prism-config
behaves correctly across a wide range of random inputs.
"""

from typing import List, Optional

from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st

from prism.config import (
    BaseConfigRoot,
    BaseConfigSection,
    DynamicConfig,
    PrismConfig,
)


# Hypothesis strategies for generating test data
@st.composite
def valid_config_dict(draw):
    """
    Generate a valid configuration dictionary.

    This strategy creates configs that match the expected schema
    with randomized values.
    """
    app_name = draw(st.text(min_size=1, max_size=50, alphabet=st.characters(
        whitelist_categories=("Lu", "Ll", "Nd"),
        whitelist_characters="-_"
    )))
    app_env = draw(st.sampled_from(["dev", "staging", "production", "test"]))

    db_host = draw(st.text(min_size=1, max_size=100, alphabet=st.characters(
        whitelist_categories=("Lu", "Ll", "Nd"),
        whitelist_characters=".-_"
    )))
    db_port = draw(st.integers(min_value=1, max_value=65535))
    db_name = draw(st.text(min_size=1, max_size=50, alphabet=st.characters(
        whitelist_categories=("Lu", "Ll", "Nd"),
        whitelist_characters="-_"
    )))

    return {
        "app": {
            "name": app_name,
            "environment": app_env
        },
        "database": {
            "host": db_host,
            "port": db_port,
            "name": db_name
        }
    }


@st.composite
def large_text_value(draw, min_size=1024, max_size=8192):
    """
    Generate large text values for stress testing.

    This tests PQC key sizes (1KB - 8KB).
    Note: Hypothesis has limits on text() strategy size.
    """
    size = draw(st.integers(min_value=min_size, max_value=max_size))
    # Generate repeated characters for efficiency
    char = draw(st.sampled_from("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"))
    return char * size


@st.composite
def env_var_override(draw):
    """
    Generate environment variable overrides.

    Returns tuple of (config_dict, env_vars_dict, expected_value)
    """
    base_config = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb"
        }
    }

    # Generate random override value
    override_port = draw(st.integers(min_value=1024, max_value=65535))

    env_vars = {
        "APP_DATABASE__PORT": str(override_port)
    }

    return (base_config, env_vars, override_port)


# Property Tests


@settings(max_examples=200)
@given(config_data=valid_config_dict())
def test_property_any_valid_dict_loads(config_data):
    """
    Test 8.1: Any valid dict with required fields loads successfully.

    Property: For all valid configuration dictionaries matching the schema,
    PrismConfig.from_dict() should load without errors.
    """
    # ACT: Load random valid config
    config = PrismConfig.from_dict(config_data)

    # ASSERT: Config loaded and values match
    assert config.app.name == config_data["app"]["name"]
    assert config.app.environment == config_data["app"]["environment"]
    assert config.database.host == config_data["database"]["host"]
    assert config.database.port == config_data["database"]["port"]
    assert config.database.name == config_data["database"]["name"]


@settings(max_examples=200, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(port_value=st.integers(min_value=1, max_value=65535))
def test_property_type_coercion_consistent(port_value, prism_env):
    """
    Test 8.2: Type coercion is consistent across loading methods.

    Property: The same value should be coerced to the same type
    whether loaded from dict, YAML, or environment variable.
    """
    # ARRANGE: Config with integer port
    config_dict = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": port_value,
            "name": "testdb"
        }
    }

    # Load from dict
    config_from_dict = PrismConfig.from_dict(config_dict)

    # Load from YAML file
    yaml_file = prism_env["tmp_path"] / "config.yaml"
    yaml_content = f"""
app:
  name: test-app
  environment: dev

database:
  host: localhost
  port: {port_value}
  name: testdb
"""
    yaml_file.write_text(yaml_content)
    config_from_yaml = PrismConfig.from_file(yaml_file)

    # Load from dict with env override (string → int coercion)
    prism_env["monkeypatch"].setenv("APP_DATABASE__PORT", str(port_value))
    config_from_env = PrismConfig.from_dict(
        {
            "app": {"name": "test-app", "environment": "dev"},
            "database": {
                "host": "localhost",
                "port": 9999,  # Will be overridden
                "name": "testdb"
            }
        },
        apply_env=True
    )

    # ASSERT: All three methods produce the same port value
    assert config_from_dict.database.port == port_value
    assert config_from_yaml.database.port == port_value
    assert config_from_env.database.port == port_value

    # ASSERT: All are integers
    assert isinstance(config_from_dict.database.port, int)
    assert isinstance(config_from_yaml.database.port, int)
    assert isinstance(config_from_env.database.port, int)


@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(override_data=env_var_override())
def test_property_env_override_idempotent(override_data, prism_env):
    """
    Test 8.3: Environment variable override is idempotent.

    Property: Applying environment overrides multiple times
    produces the same result.
    """
    base_config, env_vars, expected_port = override_data

    # Set environment variables
    for key, value in env_vars.items():
        prism_env["monkeypatch"].setenv(key, value)

    # ACT: Apply env overrides multiple times
    config1 = PrismConfig.from_dict(base_config, apply_env=True)
    config2 = PrismConfig.from_dict(base_config, apply_env=True)
    config3 = PrismConfig.from_dict(base_config, apply_env=True)

    # ASSERT: All produce same result
    assert config1.database.port == expected_port
    assert config2.database.port == expected_port
    assert config3.database.port == expected_port


@settings(max_examples=50, deadline=2000)
@given(large_value=large_text_value(min_size=1024, max_size=8192))
def test_property_large_random_configs(large_value):
    """
    Test 8.4: Large random configs don't crash.

    Property: prism-config should handle large values (PQC key sizes)
    without crashing or data corruption.
    """
    # ARRANGE: Config with large value
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": large_value
        }
    }

    # ACT: Load config with large value
    config = PrismConfig.from_dict(config_data)

    # ASSERT: Value loaded correctly without corruption
    assert config.database.password == large_value
    assert len(config.database.password) == len(large_value)

    # ASSERT: dump() works with large values
    dump_output = config.dump(use_color=False)
    assert "REDACTED" in dump_output  # password should be redacted


@settings(
    max_examples=100,
    suppress_health_check=[HealthCheck.function_scoped_fixture]
)
@given(
    secret_value=st.text(
        min_size=10,
        max_size=100,
        alphabet=st.characters(blacklist_characters="\x00")
    )
)
def test_property_secret_resolution_secure(secret_value, prism_env):
    """
    Test 8.5: Secret resolution never exposes raw secrets.

    Property: When secrets are resolved, the dump() output should
    always redact them, never exposing raw values.
    """
    # Filter out empty secrets
    assume(len(secret_value.strip()) > 0)

    # Avoid values that happen to be substrings of field names/values in the config
    # (e.g., 'environment' would match 'dev' -> 'environment' field name)
    config_field_names = ["app", "name", "environment", "dev", "database", "host",
                          "localhost", "port", "testdb", "password", "test"]
    assume(not any(name in secret_value.lower() for name in config_field_names))
    assume(not any(secret_value.lower() in name for name in config_field_names))

    # ARRANGE: Set secret in environment
    prism_env["monkeypatch"].setenv("TEST_SECRET", secret_value)

    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": "REF::ENV::TEST_SECRET"
        }
    }

    # ACT: Load config with secret resolution
    config = PrismConfig.from_dict(config_data, resolve_secrets=True)

    # ASSERT: Secret is resolved internally
    assert config.database.password == secret_value

    # ASSERT: dump() never exposes the raw secret
    dump_output = config.dump(use_color=False)
    assert secret_value not in dump_output
    assert "REDACTED" in dump_output


@settings(max_examples=100)
@given(
    app_name=st.text(min_size=1, max_size=50),
    app_env=st.sampled_from(["dev", "staging", "production"]),
    db_host=st.text(min_size=1, max_size=50),
    db_port=st.integers(min_value=1, max_value=65535)
)
def test_property_config_access_patterns(app_name, app_env, db_host, db_port):
    """
    Test 8.6: Config values are accessible in multiple ways.

    Property: After loading, config values should be accessible
    via both dot notation and dict-style access.
    """
    # Filter out strings that might cause issues
    assume(len(app_name.strip()) > 0)
    assume(len(db_host.strip()) > 0)

    # ARRANGE: Load config
    config_data = {
        "app": {"name": app_name, "environment": app_env},
        "database": {
            "host": db_host,
            "port": db_port,
            "name": "testdb"
        }
    }

    config = PrismConfig.from_dict(config_data)

    # ACT & ASSERT: Access via dot notation
    assert config.app.name == app_name
    assert config.app.environment == app_env
    assert config.database.host == db_host
    assert config.database.port == db_port

    # ASSERT: All values match original data
    assert config.app.name == config_data["app"]["name"]
    assert config.database.port == config_data["database"]["port"]


@settings(max_examples=100)
@given(config_data=valid_config_dict())
def test_property_dump_is_deterministic(config_data):
    """
    Test 8.7: dump() output is deterministic.

    Property: Calling dump() multiple times on the same config
    should produce identical output.
    """
    # ARRANGE: Load config
    config = PrismConfig.from_dict(config_data)

    # ACT: Call dump() multiple times
    dump1 = config.dump(use_color=False)
    dump2 = config.dump(use_color=False)
    dump3 = config.dump(use_color=False)

    # ASSERT: All outputs are identical
    assert dump1 == dump2 == dump3


@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(
    original_port=st.integers(min_value=1000, max_value=9999),
    override_port=st.integers(min_value=10000, max_value=65535)
)
def test_property_cli_override_precedence(original_port, override_port, prism_env):
    """
    Test 8.8: CLI args have highest precedence.

    Property: CLI arguments should always override environment variables
    and file values.
    """
    # ARRANGE: Config with original port
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": original_port,
            "name": "testdb"
        }
    }

    # Set env var override
    prism_env["monkeypatch"].setenv("APP_DATABASE__PORT", "5555")

    # Set CLI override
    cli_args = [f"--database.port={override_port}"]

    # ACT: Load with both env and CLI overrides
    config = PrismConfig.from_dict(config_data, apply_env=True, cli_args=cli_args)

    # ASSERT: CLI override wins (highest precedence)
    assert config.database.port == override_port


@settings(max_examples=50, suppress_health_check=[HealthCheck.large_base_example])
@given(
    large_value1=large_text_value(min_size=2048, max_size=4096),
    large_value2=large_text_value(min_size=2048, max_size=4096)
)
def test_property_multiple_large_values(large_value1, large_value2):
    """
    Test 8.9: Multiple large values in same config.

    Property: Config should handle multiple large values (PQC keys)
    without performance degradation or corruption.
    """
    # ARRANGE: Config with multiple large values
    config_data = {
        "app": {
            "name": "test-app",
            "environment": "dev",
            "api_key": large_value1
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": large_value2
        }
    }

    # ACT: Load config
    config = PrismConfig.from_dict(config_data)

    # ASSERT: Both large values loaded correctly
    assert config.app.api_key == large_value1
    assert config.database.password == large_value2
    assert len(config.app.api_key) == len(large_value1)
    assert len(config.database.password) == len(large_value2)


@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(config_data=valid_config_dict())
def test_property_roundtrip_consistency(config_data, prism_env):
    """
    Test 8.10: Config roundtrip maintains values.

    Property: Loading a config, dumping it to YAML, and reloading
    should produce the same values.
    """
    # ARRANGE: Load config from dict
    config1 = PrismConfig.from_dict(config_data)

    # ACT: Write to YAML and reload
    yaml_file = prism_env["tmp_path"] / "roundtrip.yaml"
    import yaml
    with open(yaml_file, "w") as f:
        yaml.safe_dump(config_data, f)

    config2 = PrismConfig.from_file(yaml_file)

    # ASSERT: Values are identical
    assert config1.app.name == config2.app.name
    assert config1.app.environment == config2.app.environment
    assert config1.database.host == config2.database.host
    assert config1.database.port == config2.database.port
    assert config1.database.name == config2.database.name


# ============================================================================
# v2.0.0 Property Tests: Custom Schemas, Flexible Mode, DynamicConfig
# ============================================================================


# Custom schema definitions for property testing
class CustomSectionConfig(BaseConfigSection):
    """Custom section for property testing."""

    host: str = "localhost"
    port: int = 8080
    enabled: bool = True
    tags: Optional[List[str]] = None


class AppConfigExtended(BaseConfigSection):
    """Extended app config with additional fields."""

    name: str
    environment: str = "dev"
    debug: bool = False
    version: str = "1.0.0"


class DatabaseConfigExtended(BaseConfigSection):
    """Extended database config."""

    host: str = "localhost"
    port: int = 5432
    name: str = "testdb"
    password: Optional[str] = None
    pool_size: int = 10


class CustomRootConfig(BaseConfigRoot):
    """Custom root config for property testing."""

    app: AppConfigExtended
    database: DatabaseConfigExtended
    custom: Optional[CustomSectionConfig] = None


@st.composite
def custom_schema_config_dict(draw):
    """
    Generate a configuration dictionary matching CustomRootConfig schema.

    This strategy creates configs that match the custom schema structure.
    """
    app_name = draw(st.text(min_size=1, max_size=30, alphabet=st.characters(
        whitelist_categories=("Lu", "Ll", "Nd"),
        whitelist_characters="-_"
    )))
    app_env = draw(st.sampled_from(["dev", "staging", "production", "test"]))
    app_debug = draw(st.booleans())
    app_version = draw(st.from_regex(r"[0-9]+\.[0-9]+\.[0-9]+", fullmatch=True))

    db_host = draw(st.text(min_size=1, max_size=50, alphabet=st.characters(
        whitelist_categories=("Lu", "Ll", "Nd"),
        whitelist_characters=".-_"
    )))
    db_port = draw(st.integers(min_value=1, max_value=65535))
    db_name = draw(st.text(min_size=1, max_size=30, alphabet=st.characters(
        whitelist_categories=("Lu", "Ll", "Nd"),
        whitelist_characters="-_"
    )))
    db_pool_size = draw(st.integers(min_value=1, max_value=100))

    # Optionally include custom section
    include_custom = draw(st.booleans())

    result = {
        "app": {
            "name": app_name,
            "environment": app_env,
            "debug": app_debug,
            "version": app_version
        },
        "database": {
            "host": db_host,
            "port": db_port,
            "name": db_name,
            "pool_size": db_pool_size
        }
    }

    if include_custom:
        custom_host = draw(st.text(min_size=1, max_size=30, alphabet=st.characters(
            whitelist_categories=("Lu", "Ll", "Nd"),
            whitelist_characters=".-_"
        )))
        custom_port = draw(st.integers(min_value=1, max_value=65535))
        custom_enabled = draw(st.booleans())
        result["custom"] = {
            "host": custom_host,
            "port": custom_port,
            "enabled": custom_enabled
        }

    return result


@st.composite
def arbitrary_nested_dict(draw, max_depth=3, current_depth=0):
    """
    Generate arbitrary nested dictionaries for flexible mode testing.

    Creates random structures of varying depth.
    """
    if current_depth >= max_depth:
        # At max depth, only generate leaf values
        return draw(st.one_of(
            st.text(min_size=1, max_size=20, alphabet=st.characters(
                whitelist_categories=("Lu", "Ll", "Nd"),
                whitelist_characters="-_"
            )),
            st.integers(min_value=-1000, max_value=1000),
            st.booleans(),
            st.floats(min_value=-100.0, max_value=100.0, allow_nan=False)
        ))

    # Generate a dict with 1-5 keys
    num_keys = draw(st.integers(min_value=1, max_value=5))
    result = {}

    for _ in range(num_keys):
        # Generate keys that don't start with underscore (Python reserved)
        key = draw(st.text(min_size=1, max_size=15, alphabet=st.characters(
            whitelist_categories=("Ll",)
        )))
        if not key or key.startswith("_"):
            continue

        # Decide if this key has a nested dict or a leaf value
        is_nested = draw(st.booleans()) and current_depth < max_depth - 1

        if is_nested:
            result[key] = draw(arbitrary_nested_dict(
                max_depth=max_depth,
                current_depth=current_depth + 1
            ))
        else:
            result[key] = draw(st.one_of(
                st.text(min_size=1, max_size=20, alphabet=st.characters(
                    whitelist_categories=("Lu", "Ll", "Nd"),
                    whitelist_characters="-_"
                )),
                st.integers(min_value=-1000, max_value=1000),
                st.booleans()
            ))

    return result if result else {"default": "value"}


@settings(max_examples=100)
@given(config_data=custom_schema_config_dict())
def test_property_custom_schema_loads(config_data):
    """
    Test 8.11: Custom schemas load correctly with all field types.

    Property: For all valid configuration dicts matching a custom schema,
    PrismConfig.from_dict() with schema= should load without errors.
    """
    # ACT: Load with custom schema
    config = PrismConfig.from_dict(config_data, schema=CustomRootConfig)

    # ASSERT: App section matches
    assert config.app.name == config_data["app"]["name"]
    assert config.app.environment == config_data["app"]["environment"]
    assert config.app.debug == config_data["app"]["debug"]
    assert config.app.version == config_data["app"]["version"]

    # ASSERT: Database section matches
    assert config.database.host == config_data["database"]["host"]
    assert config.database.port == config_data["database"]["port"]
    assert config.database.name == config_data["database"]["name"]
    assert config.database.pool_size == config_data["database"]["pool_size"]

    # ASSERT: Custom section matches if present
    if "custom" in config_data:
        assert config.custom is not None
        assert config.custom.host == config_data["custom"]["host"]
        assert config.custom.port == config_data["custom"]["port"]
        assert config.custom.enabled == config_data["custom"]["enabled"]


@settings(max_examples=100)
@given(config_data=custom_schema_config_dict())
def test_property_custom_schema_type_preservation(config_data):
    """
    Test 8.12: Custom schemas preserve field types.

    Property: After loading, all fields should have their declared types.
    """
    # ACT: Load with custom schema
    config = PrismConfig.from_dict(config_data, schema=CustomRootConfig)

    # ASSERT: Types are preserved
    assert isinstance(config.app.name, str)
    assert isinstance(config.app.environment, str)
    assert isinstance(config.app.debug, bool)
    assert isinstance(config.app.version, str)

    assert isinstance(config.database.host, str)
    assert isinstance(config.database.port, int)
    assert isinstance(config.database.name, str)
    assert isinstance(config.database.pool_size, int)

    if config.custom is not None:
        assert isinstance(config.custom.host, str)
        assert isinstance(config.custom.port, int)
        assert isinstance(config.custom.enabled, bool)


@settings(max_examples=50, deadline=5000)
@given(nested_data=arbitrary_nested_dict(max_depth=3))
def test_property_flexible_mode_any_structure(nested_data):
    """
    Test 8.13: Flexible mode accepts any valid structure.

    Property: With strict=False, any nested dict structure should load.
    """
    # ARRANGE: Ensure we have app and database to meet base requirements
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {"host": "localhost", "port": 5432, "name": "testdb"},
        "dynamic": nested_data
    }

    # ACT: Load in flexible mode
    config = PrismConfig.from_dict(config_data, strict=False)

    # ASSERT: Config loads without error
    assert config.app.name == "test-app"
    assert config.database.port == 5432

    # ASSERT: Dynamic section is accessible
    assert hasattr(config, "dynamic") or config.dynamic is not None


@settings(max_examples=100)
@given(nested_data=arbitrary_nested_dict(max_depth=2))
def test_property_dynamic_config_access(nested_data):
    """
    Test 8.14: DynamicConfig provides dot-notation access to any structure.

    Property: DynamicConfig should allow access to any nested path.
    """
    # ACT: Create DynamicConfig
    dynamic = DynamicConfig(nested_data)

    # ASSERT: Root keys are accessible
    for key in nested_data.keys():
        assert hasattr(dynamic, key)
        value = getattr(dynamic, key)

        # If value is a dict, it should be wrapped in DynamicConfig
        if isinstance(nested_data[key], dict):
            assert isinstance(value, DynamicConfig)
        else:
            assert value == nested_data[key]


@settings(max_examples=100)
@given(config_data=custom_schema_config_dict())
def test_property_custom_schema_dump_deterministic(config_data):
    """
    Test 8.15: Custom schema dump() is deterministic.

    Property: dump() on custom schema configs produces identical output.
    """
    # ARRANGE: Load config
    config = PrismConfig.from_dict(config_data, schema=CustomRootConfig)

    # ACT: Call dump() multiple times
    dump1 = config.dump(use_color=False)
    dump2 = config.dump(use_color=False)
    dump3 = config.dump(use_color=False)

    # ASSERT: All outputs are identical
    assert dump1 == dump2 == dump3


@settings(max_examples=50, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(config_data=custom_schema_config_dict())
def test_property_custom_schema_roundtrip(config_data, prism_env):
    """
    Test 8.16: Custom schema config roundtrip maintains values.

    Property: Loading from dict, writing to YAML, and reloading produces same values.
    """
    import yaml

    # ARRANGE: Load from dict
    config1 = PrismConfig.from_dict(config_data, schema=CustomRootConfig)

    # ACT: Write to YAML and reload
    yaml_file = prism_env["tmp_path"] / "custom_roundtrip.yaml"
    with open(yaml_file, "w") as f:
        yaml.safe_dump(config_data, f)

    config2 = PrismConfig.from_file(yaml_file, schema=CustomRootConfig)

    # ASSERT: Values match
    assert config1.app.name == config2.app.name
    assert config1.app.environment == config2.app.environment
    assert config1.app.debug == config2.app.debug
    assert config1.database.host == config2.database.host
    assert config1.database.port == config2.database.port


@settings(max_examples=50, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(
    override_value=st.integers(min_value=1, max_value=100)
)
def test_property_custom_schema_env_override(override_value, prism_env):
    """
    Test 8.17: Environment overrides work with custom schemas.

    Property: ENV vars should override custom schema fields correctly.
    """
    # ARRANGE: Base config
    config_data = {
        "app": {"name": "test-app", "environment": "dev", "debug": False, "version": "1.0.0"},
        "database": {"host": "localhost", "port": 5432, "name": "testdb", "pool_size": 10}
    }

    # Set env override
    prism_env["monkeypatch"].setenv("APP_DATABASE__POOL_SIZE", str(override_value))

    # ACT: Load with env override
    config = PrismConfig.from_dict(config_data, schema=CustomRootConfig, apply_env=True)

    # ASSERT: Override applied
    assert config.database.pool_size == override_value


@settings(max_examples=50)
@given(
    app_name=st.text(min_size=1, max_size=30, alphabet=st.characters(
        whitelist_categories=("Lu", "Ll", "Nd"),
        whitelist_characters="-_"
    )),
    db_port=st.integers(min_value=1, max_value=65535)
)
def test_property_flexible_vs_strict_parity(app_name, db_port):
    """
    Test 8.18: Flexible and strict modes produce equivalent access for same data.

    Property: For the same config dict, both modes should yield identical values.
    """
    assume(len(app_name.strip()) > 0)

    # ARRANGE: Standard config
    config_data = {
        "app": {"name": app_name, "environment": "dev"},
        "database": {"host": "localhost", "port": db_port, "name": "testdb"}
    }

    # ACT: Load in both modes
    config_strict = PrismConfig.from_dict(config_data)  # Default strict mode
    config_flexible = PrismConfig.from_dict(config_data, strict=False)

    # ASSERT: Both produce same values
    assert config_strict.app.name == config_flexible.app.name
    assert config_strict.app.environment == config_flexible.app.environment
    assert config_strict.database.host == config_flexible.database.host
    assert config_strict.database.port == config_flexible.database.port
    assert config_strict.database.name == config_flexible.database.name
