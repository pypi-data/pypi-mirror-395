"""
Tests for advanced features in prism-config.

This module tests advanced functionality including:
- Config freezing (immutability)
- Config serialization (to_dict, to_yaml, to_json)
- Config diffing
"""

import json

import pytest

from prism.config import PrismConfig


def test_config_is_frozen(prism_env):
    """
    Test 9.1: Config is immutable after loading.

    Verify that configuration objects are frozen and cannot be modified
    after loading, preventing accidental configuration changes at runtime.
    """
    # ARRANGE: Load config
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb"
        }
    }

    config = PrismConfig.from_dict(config_data)

    # ACT & ASSERT: Attempting to modify should raise error
    # Pydantic ValidationError or AttributeError
    with pytest.raises((ValueError, AttributeError, TypeError)):
        config._config.app.name = "modified-app"

    with pytest.raises((ValueError, AttributeError, TypeError)):
        config._config.database.port = 9999


def test_to_dict_method(prism_env):
    """
    Test 9.2: Export config to dictionary.

    Verify that to_dict() exports the configuration as a plain Python dictionary.
    """
    # ARRANGE: Load config
    config_data = {
        "app": {"name": "test-app", "environment": "production"},
        "database": {
            "host": "db.example.com",
            "port": 5432,
            "name": "proddb",
            "password": "secret123"
        }
    }

    config = PrismConfig.from_dict(config_data)

    # ACT: Export to dict
    exported = config.to_dict()

    # ASSERT: Exported dict matches original data
    assert exported["app"]["name"] == "test-app"
    assert exported["app"]["environment"] == "production"
    assert exported["database"]["host"] == "db.example.com"
    assert exported["database"]["port"] == 5432
    assert exported["database"]["name"] == "proddb"
    assert exported["database"]["password"] == "secret123"


def test_to_dict_with_redaction(prism_env):
    """
    Test 9.3: Export to dict with secret redaction.

    Verify that to_dict(redact_secrets=True) redacts sensitive values.
    """
    # ARRANGE: Load config with secrets
    config_data = {
        "app": {"name": "test-app", "environment": "production"},
        "database": {
            "host": "db.example.com",
            "port": 5432,
            "name": "proddb",
            "password": "secret123"
        }
    }

    config = PrismConfig.from_dict(config_data)

    # ACT: Export with redaction
    exported = config.to_dict(redact_secrets=True)

    # ASSERT: Password is redacted
    assert exported["database"]["password"] == "[REDACTED]"
    # ASSERT: Non-secrets are visible
    assert exported["app"]["name"] == "test-app"
    assert exported["database"]["host"] == "db.example.com"


def test_to_yaml_method(prism_env):
    """
    Test 9.4: Export config to YAML string.

    Verify that to_yaml() exports the configuration as a YAML string.
    """
    # ARRANGE: Load config
    config_data = {
        "app": {"name": "test-app", "environment": "production"},
        "database": {
            "host": "db.example.com",
            "port": 5432,
            "name": "proddb"
        }
    }

    config = PrismConfig.from_dict(config_data)

    # ACT: Export to YAML
    yaml_output = config.to_yaml()

    # ASSERT: YAML string contains expected values
    assert "name: test-app" in yaml_output
    assert "environment: production" in yaml_output
    assert "host: db.example.com" in yaml_output
    assert "port: 5432" in yaml_output

    # ASSERT: Can reload from YAML
    yaml_file = prism_env["tmp_path"] / "exported.yaml"
    yaml_file.write_text(yaml_output)
    reloaded = PrismConfig.from_file(yaml_file)
    assert reloaded.app.name == "test-app"
    assert reloaded.database.port == 5432


def test_to_yaml_with_redaction(prism_env):
    """
    Test 9.5: Export to YAML with secret redaction.

    Verify that to_yaml(redact_secrets=True) redacts sensitive values.
    """
    # ARRANGE: Load config with secrets
    config_data = {
        "app": {"name": "test-app", "environment": "production"},
        "database": {
            "host": "db.example.com",
            "port": 5432,
            "name": "proddb",
            "password": "secret123"
        }
    }

    config = PrismConfig.from_dict(config_data)

    # ACT: Export to YAML with redaction
    yaml_output = config.to_yaml(redact_secrets=True)

    # ASSERT: Password is redacted
    assert "secret123" not in yaml_output
    assert "[REDACTED]" in yaml_output
    # ASSERT: Non-secrets are visible
    assert "test-app" in yaml_output


def test_to_json_method(prism_env):
    """
    Test 9.6: Export config to JSON string.

    Verify that to_json() exports the configuration as a JSON string.
    """
    # ARRANGE: Load config
    config_data = {
        "app": {"name": "test-app", "environment": "production"},
        "database": {
            "host": "db.example.com",
            "port": 5432,
            "name": "proddb"
        }
    }

    config = PrismConfig.from_dict(config_data)

    # ACT: Export to JSON
    json_output = config.to_json()

    # ASSERT: JSON is valid
    parsed = json.loads(json_output)
    assert parsed["app"]["name"] == "test-app"
    assert parsed["database"]["port"] == 5432

    # ASSERT: JSON is pretty-printed (has newlines)
    assert "\n" in json_output


def test_to_json_with_redaction(prism_env):
    """
    Test 9.7: Export to JSON with secret redaction.

    Verify that to_json(redact_secrets=True) redacts sensitive values.
    """
    # ARRANGE: Load config with secrets
    config_data = {
        "app": {"name": "test-app", "environment": "production"},
        "database": {
            "host": "db.example.com",
            "port": 5432,
            "name": "proddb",
            "password": "secret123",
            "api_token": "token-abc-123"
        }
    }

    config = PrismConfig.from_dict(config_data)

    # ACT: Export to JSON with redaction
    json_output = config.to_json(redact_secrets=True)

    # ASSERT: Secrets are redacted
    assert "secret123" not in json_output
    assert "token-abc-123" not in json_output
    assert "[REDACTED]" in json_output

    # ASSERT: Non-secrets are visible
    parsed = json.loads(json_output)
    assert parsed["app"]["name"] == "test-app"
    assert parsed["database"]["host"] == "db.example.com"


def test_diff_configs_basic(prism_env):
    """
    Test 9.8: Diff two configurations.

    Verify that diff() identifies differences between two configs.
    """
    # ARRANGE: Create two configs
    config1_data = {
        "app": {"name": "app-v1", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb"
        }
    }

    config2_data = {
        "app": {"name": "app-v2", "environment": "production"},
        "database": {
            "host": "prod.example.com",
            "port": 5432,
            "name": "proddb"
        }
    }

    config1 = PrismConfig.from_dict(config1_data)
    config2 = PrismConfig.from_dict(config2_data)

    # ACT: Diff the configs
    diff = config1.diff(config2)

    # ASSERT: Diff contains changes
    assert "app.name" in diff
    assert diff["app.name"]["old"] == "app-v1"
    assert diff["app.name"]["new"] == "app-v2"

    assert "app.environment" in diff
    assert diff["app.environment"]["old"] == "dev"
    assert diff["app.environment"]["new"] == "production"

    assert "database.host" in diff
    assert diff["database.host"]["old"] == "localhost"
    assert diff["database.host"]["new"] == "prod.example.com"

    assert "database.name" in diff
    assert diff["database.name"]["old"] == "testdb"
    assert diff["database.name"]["new"] == "proddb"

    # ASSERT: Unchanged values not in diff
    assert "database.port" not in diff


def test_diff_configs_no_changes(prism_env):
    """
    Test 9.9: Diff identical configurations.

    Verify that diff() returns empty dict for identical configs.
    """
    # ARRANGE: Create identical configs
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb"
        }
    }

    config1 = PrismConfig.from_dict(config_data)
    config2 = PrismConfig.from_dict(config_data)

    # ACT: Diff identical configs
    diff = config1.diff(config2)

    # ASSERT: No differences
    assert diff == {}


def test_diff_human_readable_output(prism_env):
    """
    Test 9.10: Diff output is human-readable.

    Verify that diff() can produce a human-readable string output.
    """
    # ARRANGE: Create two configs
    config1_data = {
        "app": {"name": "app-v1", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb"
        }
    }

    config2_data = {
        "app": {"name": "app-v2", "environment": "dev"},
        "database": {
            "host": "prod.example.com",
            "port": 5432,
            "name": "testdb"
        }
    }

    config1 = PrismConfig.from_dict(config1_data)
    config2 = PrismConfig.from_dict(config2_data)

    # ACT: Get human-readable diff
    diff_str = config1.diff_str(config2)

    # ASSERT: Output is readable string
    assert isinstance(diff_str, str)
    assert "app.name" in diff_str
    assert "app-v1" in diff_str
    assert "app-v2" in diff_str
    assert "database.host" in diff_str
    assert "localhost" in diff_str
    assert "prod.example.com" in diff_str


def test_serialization_roundtrip(prism_env):
    """
    Test 9.11: Serialization roundtrip preserves data.

    Verify that exporting and reloading preserves all values.
    """
    # ARRANGE: Original config
    config_data = {
        "app": {"name": "test-app", "environment": "production"},
        "database": {
            "host": "db.example.com",
            "port": 5432,
            "name": "proddb"
        }
    }

    config1 = PrismConfig.from_dict(config_data)

    # ACT: Export to dict and reload
    exported_dict = config1.to_dict()
    config2 = PrismConfig.from_dict(exported_dict)

    # ASSERT: All values preserved
    assert config1.app.name == config2.app.name
    assert config1.app.environment == config2.app.environment
    assert config1.database.host == config2.database.host
    assert config1.database.port == config2.database.port
    assert config1.database.name == config2.database.name


def test_to_yaml_file(prism_env):
    """
    Test 9.12: Export config to YAML file.

    Verify that to_yaml_file() writes config to a file.
    """
    # ARRANGE: Create config
    config_data = {
        "app": {"name": "test-app", "environment": "production"},
        "database": {
            "host": "db.example.com",
            "port": 5432,
            "name": "proddb"
        }
    }

    config = PrismConfig.from_dict(config_data)
    output_file = prism_env["tmp_path"] / "exported_config.yaml"

    # ACT: Export to YAML file
    config.to_yaml_file(output_file)

    # ASSERT: File was created
    assert output_file.exists()

    # ASSERT: Can reload from file
    reloaded = PrismConfig.from_file(output_file)
    assert reloaded.app.name == "test-app"
    assert reloaded.database.port == 5432


def test_to_json_file(prism_env):
    """
    Test 9.13: Export config to JSON file.

    Verify that to_json_file() writes config to a file.
    """
    # ARRANGE: Create config
    config_data = {
        "app": {"name": "test-app", "environment": "production"},
        "database": {
            "host": "db.example.com",
            "port": 5432,
            "name": "proddb"
        }
    }

    config = PrismConfig.from_dict(config_data)
    output_file = prism_env["tmp_path"] / "exported_config.json"

    # ACT: Export to JSON file
    config.to_json_file(output_file)

    # ASSERT: File was created
    assert output_file.exists()

    # ASSERT: JSON is valid
    with open(output_file) as f:
        parsed = json.load(f)
    assert parsed["app"]["name"] == "test-app"
    assert parsed["database"]["port"] == 5432
