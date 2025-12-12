"""
Parity test runner for prism-config.

Executes cross-language parity tests to ensure consistent behavior across
all prism-config implementations (Python, Java, etc.).

Run with: pytest tests/parity/test_parity.py -v
"""

import json
import os
from pathlib import Path
from typing import Any, Dict

try:
    import pytest
    HAS_PYTEST = True
except ImportError:
    HAS_PYTEST = False

from prism.config import PrismConfig
from prism.config.exceptions import (
    ConfigFileNotFoundError,
    ConfigParseError,
    ConfigValidationError,
    SecretResolutionError,
)


class ParityTestRunner:
    """Runs parity tests from JSON test definitions."""

    def __init__(self, test_file: Path):
        """Load test definition from JSON file."""
        self.test_file = test_file
        with open(test_file, 'r') as f:
            self.test_data = json.load(f)

        self.name = self.test_data.get("name", "unknown")
        self.description = self.test_data.get("description", "")
        self.config = self.test_data.get("config", {})
        self.environment = self.test_data.get("environment", {})
        self.secrets = self.test_data.get("secrets", {})
        self.cli_args = self.test_data.get("cli_args", None)
        self.options = self.test_data.get("options", {})
        self.expected = self.test_data.get("expected", {})
        self.expected_error = self.test_data.get("expected_error", None)
        self.large_values = self.test_data.get("large_values", {})

    def setup_environment(self):
        """Set up environment variables for the test."""
        self._original_env = {}
        for key, value in self.environment.items():
            self._original_env[key] = os.environ.get(key)
            os.environ[key] = value

    def teardown_environment(self):
        """Restore original environment variables."""
        for key, original_value in self._original_env.items():
            if original_value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = original_value

    def setup_secrets(self):
        """Set up secret provider values."""
        # For ENV provider, set environment variables
        for secret_ref, value in self.secrets.items():
            if secret_ref.startswith("ENV::"):
                key = secret_ref[5:]  # Remove "ENV::" prefix
                os.environ[key] = value
            elif secret_ref.startswith("FILE::"):
                # For FILE provider, create temporary files
                # This would need implementation for file-based secrets
                pass

    def process_large_values(self):
        """Replace large value placeholders with actual large strings."""
        def replace_in_dict(d: Dict) -> Dict:
            result = {}
            for key, value in d.items():
                if isinstance(value, dict):
                    result[key] = replace_in_dict(value)
                elif isinstance(value, str) and value in self.large_values:
                    # Generate a string of the specified size
                    size = self.large_values[value]
                    result[key] = "A" * size
                else:
                    result[key] = value
            return result

        self.config = replace_in_dict(self.config)

    def get_nested_value(self, config: PrismConfig, path: str) -> Any:
        """Get a nested configuration value using dot notation."""
        parts = path.split(".")
        current = config

        for part in parts:
            if hasattr(current, part):
                current = getattr(current, part)
            else:
                raise AttributeError(f"Config has no attribute: {part}")

        return current

    def run(self):
        """Execute the parity test."""
        print(f"\nRunning parity test: {self.name}")
        print(f"Description: {self.description}")

        try:
            # Setup
            self.setup_environment()
            self.setup_secrets()
            self.process_large_values()

            # Load configuration
            config = PrismConfig.from_dict(
                self.config,
                apply_env=self.options.get("apply_env", False),
                env_prefix=self.options.get("env_prefix", "APP_"),
                cli_args=self.cli_args,
                resolve_secrets=self.options.get("resolve_secrets", False)
            )

            # If we expected an error but didn't get one, fail
            if self.expected_error:
                raise AssertionError(
                    f"Expected {self.expected_error['type']} but config loaded successfully"
                )

            # Validate expected values
            for path, expected_value in self.expected.items():
                # Special handling for length checks
                if path.endswith("_length"):
                    actual_path = path[:-7]  # Remove "_length" suffix
                    actual_value = self.get_nested_value(config, actual_path)
                    actual_length = len(actual_value) if actual_value else 0
                    assert actual_length == expected_value, \
                        f"{actual_path} length: expected {expected_value}, got {actual_length}"
                else:
                    actual_value = self.get_nested_value(config, path)
                    assert actual_value == expected_value, \
                        f"{path}: expected {expected_value!r}, got {actual_value!r}"

            print(f"[PASS] Test passed: {self.name}")

        except (
            ConfigValidationError,
            ConfigParseError,
            ConfigFileNotFoundError,
            SecretResolutionError
        ) as e:
            # If we expected this error, validate it
            if self.expected_error:
                error_type = type(e).__name__
                expected_type = self.expected_error["type"]
                message_contains = self.expected_error.get("message_contains", "")

                assert error_type == expected_type, \
                    f"Expected error type {expected_type}, got {error_type}"

                if message_contains:
                    assert message_contains in str(e), \
                        f"Expected error message to contain '{message_contains}', got: {e}"

                print(f"[PASS] Test passed: {self.name} (expected error caught)")
            else:
                # Unexpected error
                raise

        finally:
            # Cleanup
            self.teardown_environment()


# Discover all parity test files
PARITY_DIR = Path(__file__).parent
test_files = sorted(PARITY_DIR.glob("*.json"))

# Generate pytest test cases (only if pytest is available)
if HAS_PYTEST:
    @pytest.mark.parametrize("test_file", test_files, ids=lambda f: f.stem)
    def test_parity(test_file):
        """Run a parity test from JSON definition."""
        runner = ParityTestRunner(test_file)
        runner.run()


    def test_parity_test_discovery():
        """Verify that parity test files are discovered."""
        assert len(test_files) > 0, "No parity test files found"
        print(f"\nDiscovered {len(test_files)} parity test files:")
        for test_file in test_files:
            print(f"  - {test_file.name}")


if __name__ == "__main__":
    # Allow running directly for debugging
    print("Running parity tests...")
    print(f"Found {len(test_files)} test files\n")

    passed = 0
    failed = 0

    for test_file in test_files:
        try:
            runner = ParityTestRunner(test_file)
            runner.run()
            passed += 1
        except Exception as e:
            print(f"[FAIL] Test failed: {test_file.stem}")
            print(f"   Error: {e}")
            failed += 1

    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'='*60}")
