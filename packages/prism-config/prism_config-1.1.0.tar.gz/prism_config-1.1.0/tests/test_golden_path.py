"""
The Golden Path Test - The ONE test that proves prism-config works end-to-end.

This test validates the entire happy path:
1. Load config from dict/file
2. Access via typed models
3. Override with environment variables
4. Resolve secrets via REF:: syntax
5. Render the Neon Dump

All other tests are variations/edge cases of this.
"""


import pytest

from prism.config import PrismConfig
from prism.config.exceptions import ConfigValidationError


def test_golden_path_dict_loading(sample_config_dict):
    """
    Phase 1: Load config from a Python dict and access via typed properties.

    This is the SIMPLEST possible test - just proving the core mechanic works.
    """
    # ARRANGE: We have a config dict (from fixture)

    # ACT: Load it into PrismConfig
    config = PrismConfig.from_dict(sample_config_dict)

    # ASSERT: Can access values via dot notation with correct types
    assert config.app.name == "test-app"
    assert config.app.environment == "dev"
    assert config.database.host == "localhost"
    assert config.database.port == 5432
    assert isinstance(config.database.port, int)  # Type validation!
    assert config.database.name == "testdb"


def test_golden_path_preserves_types(sample_config_dict):
    """Verify that Pydantic correctly enforces types."""
    config = PrismConfig.from_dict(sample_config_dict)

    # Port should be int, not string
    assert isinstance(config.database.port, int)
    assert config.database.port == 5432


def test_golden_path_missing_required_field():
    """Config should fail fast if required fields are missing."""
    incomplete_config = {
        "app": {
            "name": "test-app",
            # Missing 'environment'
        }
    }

    with pytest.raises(ConfigValidationError, match="environment"):
        PrismConfig.from_dict(incomplete_config)
