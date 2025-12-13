"""
Tests for PrismConfig file loading functionality.

This module tests YAML file loading, error handling, and edge cases.
"""


import pytest

from prism.config import PrismConfig
from prism.config.exceptions import ConfigFileNotFoundError, ConfigParseError, ConfigValidationError


def test_yaml_loading_basic(sample_config_yaml):
    """
    Test 2.1: Load config from a YAML file.

    This validates that we can load configuration from a YAML file
    and access it the same way as dict-based configs.
    """
    # ACT: Load config from YAML file
    config = PrismConfig.from_file(sample_config_yaml)

    # ASSERT: Can access values via dot notation with correct types
    assert config.app.name == "test-app"
    assert config.app.environment == "dev"
    assert config.database.host == "localhost"
    assert config.database.port == 5432
    assert isinstance(config.database.port, int)  # Type preservation
    assert config.database.name == "testdb"


def test_yaml_loading_with_path_string(sample_config_yaml):
    """Test that from_file() accepts both Path and str."""
    # ACT: Load using string path
    config = PrismConfig.from_file(str(sample_config_yaml))

    # ASSERT: Works the same as Path
    assert config.app.name == "test-app"
    assert config.database.port == 5432


def test_yaml_file_not_found(tmp_path):
    """
    Test 2.2: Handle file not found error gracefully.

    When a config file doesn't exist, we should get a clear error message
    that includes the full path.
    """
    # ARRANGE: Non-existent file path
    missing_file = tmp_path / "does_not_exist.yaml"

    # ACT & ASSERT: Should raise ConfigFileNotFoundError with helpful message
    with pytest.raises(ConfigFileNotFoundError) as exc_info:
        PrismConfig.from_file(missing_file)

    # Verify error message includes the path
    assert str(missing_file) in str(exc_info.value)


def test_yaml_invalid_syntax(tmp_path):
    """
    Test 2.3: Handle invalid YAML syntax with clear error.

    If YAML is malformed, we should get a parse error that helps
    the user identify the problem.
    """
    # ARRANGE: Create file with invalid YAML
    bad_yaml = tmp_path / "bad.yaml"
    bad_yaml.write_text("""
app:
  name: test-app
  environment: dev
database:
  host: localhost
  port: [this is not valid YAML syntax}
  name: testdb
""")

    # ACT & ASSERT: Should raise ConfigParseError with YAML parse error
    with pytest.raises(ConfigParseError) as exc_info:
        PrismConfig.from_file(bad_yaml)

    # Error should mention YAML parsing issue
    assert "YAML" in str(exc_info.value) or "parse" in str(exc_info.value).lower()


def test_yaml_empty_file(tmp_path):
    """
    Test 2.4: Handle empty YAML file.

    An empty config file should fail validation (missing required fields).
    """
    # ARRANGE: Create empty YAML file
    empty_yaml = tmp_path / "empty.yaml"
    empty_yaml.write_text("")

    # ACT & ASSERT: Should raise ConfigParseError (validation error)
    with pytest.raises(ConfigParseError) as exc_info:
        PrismConfig.from_file(empty_yaml)

    # Should indicate the file is empty
    error_msg = str(exc_info.value).lower()
    assert "empty" in error_msg


def test_yaml_with_comments(tmp_path):
    """
    Test 2.5: YAML with comments should parse correctly.

    Comments are a key feature of YAML - they should be preserved
    (or at least not cause errors during parsing).
    """
    # ARRANGE: Create YAML file with comments
    yaml_with_comments = tmp_path / "commented.yaml"
    yaml_with_comments.write_text("""
# Application configuration
app:
  name: test-app  # The application identifier
  environment: dev  # dev, staging, or prod

# Database configuration
database:
  host: localhost  # DB server hostname
  port: 5432       # PostgreSQL default port
  name: testdb     # Database name
""")

    # ACT: Load config
    config = PrismConfig.from_file(yaml_with_comments)

    # ASSERT: Comments should be ignored, data should load correctly
    assert config.app.name == "test-app"
    assert config.app.environment == "dev"
    assert config.database.host == "localhost"
    assert config.database.port == 5432
    assert config.database.name == "testdb"


def test_yaml_with_null_values(tmp_path):
    """
    Test that YAML null values are handled appropriately.

    Null/missing values should trigger validation errors for required fields.
    """
    # ARRANGE: Create YAML with null value for required field
    yaml_with_null = tmp_path / "null_values.yaml"
    yaml_with_null.write_text("""
app:
  name: test-app
  environment: null  # Required field set to null

database:
  host: localhost
  port: 5432
  name: testdb
""")

    # ACT & ASSERT: Should fail validation
    with pytest.raises(ConfigValidationError):
        PrismConfig.from_file(yaml_with_null)


def test_yaml_preserves_types(sample_config_yaml):
    """
    Verify that types from YAML are correctly coerced to schema types.

    YAML parses numbers correctly, but we should verify Pydantic
    validates and coerces them properly.
    """
    # ACT: Load config
    config = PrismConfig.from_file(sample_config_yaml)

    # ASSERT: Types should match the model definitions
    assert isinstance(config.app.name, str)
    assert isinstance(config.app.environment, str)
    assert isinstance(config.database.host, str)
    assert isinstance(config.database.port, int)  # Integer, not string
    assert isinstance(config.database.name, str)


def test_yaml_with_extra_fields(tmp_path):
    """
    Test that extra fields in YAML are rejected.

    ConfigRoot has extra="forbid", so unknown fields should cause errors.
    """
    # ARRANGE: Create YAML with unknown field
    yaml_with_extra = tmp_path / "extra_fields.yaml"
    yaml_with_extra.write_text("""
app:
  name: test-app
  environment: dev

database:
  host: localhost
  port: 5432
  name: testdb

unknown_section:  # This should not be allowed
  foo: bar
""")

    # ACT & ASSERT: Should fail validation
    with pytest.raises(ConfigValidationError) as exc_info:
        PrismConfig.from_file(yaml_with_extra)

    # Error should mention the forbidden field
    error_msg = str(exc_info.value).lower()
    assert "unknown_section" in error_msg or "extra" in error_msg


def test_yaml_non_dict_content(tmp_path):
    """
    Test that YAML files containing non-dict content (like lists) are rejected.

    The config file must be a YAML object/dict, not a list or scalar.
    """
    # ARRANGE: Create YAML file with list at root
    yaml_with_list = tmp_path / "list_content.yaml"
    yaml_with_list.write_text("""
- item1
- item2
- item3
""")

    # ACT & ASSERT: Should fail with clear error
    with pytest.raises(ConfigParseError) as exc_info:
        PrismConfig.from_file(yaml_with_list)

    # Error should indicate it must be a dict
    error_msg = str(exc_info.value).lower()
    assert "dict" in error_msg or "object" in error_msg
