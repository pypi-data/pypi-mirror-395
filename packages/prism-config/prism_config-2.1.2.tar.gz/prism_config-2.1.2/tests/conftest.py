"""
Shared pytest fixtures for prism-config tests.
"""

import os

import pytest


@pytest.fixture
def prism_env(monkeypatch, tmp_path):
    """
    Standard test environment for all Prism tests.

    Provides:
    - Isolated temporary directory
    - Clean environment variables
    - Automatic cleanup
    """
    # Store original env
    original_env = os.environ.copy()

    # Clear all env vars starting with APP_
    for key in list(os.environ.keys()):
        if key.startswith("APP_"):
            monkeypatch.delenv(key, raising=False)

    yield {
        "tmp_path": tmp_path,
        "monkeypatch": monkeypatch,
    }

    # Restore original env
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def sample_config_dict():
    """Basic configuration as a Python dict."""
    return {
        "app": {
            "name": "test-app",
            "environment": "dev",
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
        }
    }


@pytest.fixture
def sample_config_yaml(tmp_path):
    """Basic configuration as a YAML file."""
    config_content = """
app:
  name: test-app
  environment: dev

database:
  host: localhost
  port: 5432
  name: testdb
"""
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content)
    return config_file
