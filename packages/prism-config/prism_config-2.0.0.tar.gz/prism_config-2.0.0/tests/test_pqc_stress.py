"""
Tests for PQC (Post-Quantum Cryptography) stress testing.

This module tests prism-config's ability to handle large configuration values,
particularly for post-quantum cryptographic keys which can be up to 16KB.

Background:
- Classic RSA-2048 keys: ~2KB
- Kyber-512 (NIST Level 1): ~1KB
- Kyber-768 (NIST Level 3): ~2KB
- Kyber-1024 (NIST Level 5): ~16KB
- Future PQC algorithms: potentially 32KB+
"""

from prism.config import PrismConfig


def test_load_1kb_value(prism_env):
    """
    Test 7.1: Load config value of 1KB.

    Verify that prism-config can handle Kyber-512 sized keys (~1KB).
    """
    # ARRANGE: Create 1KB value (1024 bytes)
    large_value = "A" * 1024

    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": large_value
        }
    }

    # ACT: Load config with 1KB value
    config = PrismConfig.from_dict(config_data)

    # ASSERT: Value loaded correctly
    assert config.database.password == large_value
    assert len(config.database.password) == 1024


def test_load_8kb_value(prism_env):
    """
    Test 7.2: Load config value of 8KB.

    Verify that prism-config can handle medium-sized PQC keys.
    """
    # ARRANGE: Create 8KB value (8192 bytes)
    large_value = "B" * 8192

    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": large_value
        }
    }

    # ACT: Load config with 8KB value
    config = PrismConfig.from_dict(config_data)

    # ASSERT: Value loaded correctly
    assert config.database.password == large_value
    assert len(config.database.password) == 8192


def test_load_16kb_value_kyber1024(prism_env):
    """
    Test 7.3: Load config value of 16KB (Kyber-1024 size).

    Verify that prism-config can handle Kyber-1024 sized keys (~16KB).
    This is the NIST Level 5 security parameter.
    """
    # ARRANGE: Create 16KB value (16384 bytes)
    large_value = "C" * 16384

    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": large_value
        }
    }

    # ACT: Load config with 16KB value
    config = PrismConfig.from_dict(config_data)

    # ASSERT: Value loaded correctly
    assert config.database.password == large_value
    assert len(config.database.password) == 16384


def test_load_32kb_value_future_proof(prism_env):
    """
    Test 7.4: Load config value of 32KB (future-proofing).

    Verify that prism-config can handle even larger future PQC algorithms.
    """
    # ARRANGE: Create 32KB value (32768 bytes)
    large_value = "D" * 32768

    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": large_value
        }
    }

    # ACT: Load config with 32KB value
    config = PrismConfig.from_dict(config_data)

    # ASSERT: Value loaded correctly
    assert config.database.password == large_value
    assert len(config.database.password) == 32768


def test_file_provider_16kb_secret(prism_env):
    """
    Test 7.5: FILE provider reads 16KB secret file.

    Verify that the FILE secret provider can handle large secrets
    like PQC keys stored in Docker secrets.
    """
    # ARRANGE: Create 16KB secret file
    large_secret = "E" * 16384
    secret_file = prism_env["tmp_path"] / "large_secret"
    secret_file.write_text(large_secret)

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

    # ASSERT: Large secret loaded correctly
    assert config.database.password == large_secret
    assert len(config.database.password) == 16384


def test_env_provider_16kb_value(prism_env):
    """
    Test 7.6: ENV provider handles 16KB environment variable.

    Verify that the ENV secret provider can handle large secrets
    from environment variables.
    """
    # ARRANGE: Set 16KB environment variable
    large_secret = "F" * 16384
    prism_env["monkeypatch"].setenv("LARGE_SECRET", large_secret)

    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": "REF::ENV::LARGE_SECRET"
        }
    }

    # ACT: Load config with secret resolution
    config = PrismConfig.from_dict(config_data, resolve_secrets=True)

    # ASSERT: Large secret loaded correctly
    assert config.database.password == large_secret
    assert len(config.database.password) == 16384


def test_yaml_file_16kb_value(prism_env):
    """
    Test 7.7: YAML file with 16KB value parses correctly.

    Verify that YAML loading can handle large values for PQC keys.
    """
    # ARRANGE: Create YAML file with 16KB value
    large_value = "G" * 16384

    yaml_content = f"""
app:
  name: test-app
  environment: dev

database:
  host: localhost
  port: 5432
  name: testdb
  password: {large_value}
"""

    yaml_file = prism_env["tmp_path"] / "large_config.yaml"
    yaml_file.write_text(yaml_content)

    # ACT: Load config from YAML file
    config = PrismConfig.from_file(yaml_file)

    # ASSERT: Large value loaded correctly
    assert config.database.password == large_value
    assert len(config.database.password) == 16384


def test_multiple_large_values(prism_env):
    """
    Test 7.8: Multiple large values in same config.

    Verify that prism-config can handle multiple PQC keys
    in the same configuration.
    """
    # ARRANGE: Create multiple 8KB values
    api_key = "H" * 8192
    db_password = "I" * 8192

    config_data = {
        "app": {
            "name": "test-app",
            "environment": "dev",
            "api_key": api_key
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": db_password
        }
    }

    # ACT: Load config with multiple large values
    config = PrismConfig.from_dict(config_data)

    # ASSERT: All large values loaded correctly
    assert config.app.api_key == api_key
    assert len(config.app.api_key) == 8192
    assert config.database.password == db_password
    assert len(config.database.password) == 8192


def test_large_value_with_env_override(prism_env):
    """
    Test 7.9: Large value can be overridden via environment variable.

    Verify that environment variable overrides work with large values.
    """
    # ARRANGE: Original 1KB value, override with 2KB value
    original_value = "J" * 1024
    override_value = "K" * 2048

    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": original_value
        }
    }

    # Set environment variable with large override
    prism_env["monkeypatch"].setenv("APP_DATABASE__PASSWORD", override_value)

    # ACT: Load config with env override
    config = PrismConfig.from_dict(config_data, apply_env=True)

    # ASSERT: Override value used
    assert config.database.password == override_value
    assert len(config.database.password) == 2048


def test_large_value_with_cli_override(prism_env):
    """
    Test 7.10: Large value can be overridden via CLI argument.

    Verify that CLI argument overrides work with large values.
    """
    # ARRANGE: Original 1KB value, override with 4KB value
    original_value = "L" * 1024
    override_value = "M" * 4096

    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": original_value
        }
    }

    cli_args = [f"--database.password={override_value}"]

    # ACT: Load config with CLI override
    config = PrismConfig.from_dict(config_data, cli_args=cli_args)

    # ASSERT: Override value used
    assert config.database.password == override_value
    assert len(config.database.password) == 4096
