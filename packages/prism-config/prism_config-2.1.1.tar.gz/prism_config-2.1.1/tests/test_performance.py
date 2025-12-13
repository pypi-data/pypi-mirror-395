"""
Performance benchmarks for prism-config.

These tests measure performance characteristics to ensure
the library remains fast as features are added.
"""

import time
from typing import Optional

import pytest

from prism.config import (
    BaseConfigRoot,
    BaseConfigSection,
    DynamicConfig,
    PrismConfig,
)


# =============================================================================
# Custom Schemas for Benchmarking
# =============================================================================


class BenchmarkSection(BaseConfigSection):
    """Simple section for benchmarks."""

    host: str = "localhost"
    port: int = 8080
    enabled: bool = True


class BenchmarkConfig(BaseConfigRoot):
    """Root config for benchmarks."""

    app: BenchmarkSection
    database: BenchmarkSection
    cache: Optional[BenchmarkSection] = None
    auth: Optional[BenchmarkSection] = None


# =============================================================================
# Performance Benchmarks
# =============================================================================


class TestLoadingPerformance:
    """Tests for configuration loading performance."""

    @pytest.fixture
    def simple_config(self):
        """Simple config for benchmarking."""
        return {
            "app": {"name": "benchmark-app", "environment": "test"},
            "database": {"host": "localhost", "port": 5432, "name": "testdb"}
        }

    @pytest.fixture
    def complex_config(self):
        """Complex config with many sections."""
        return {
            "app": {
                "name": "complex-app",
                "environment": "production",
                "api_key": "secret-key",
            },
            "database": {
                "host": "prod-db.example.com",
                "port": 5432,
                "name": "production_db",
                "password": "db-password",
            },
            "section1": {"host": "host1", "port": 1001, "enabled": True},
            "section2": {"host": "host2", "port": 1002, "enabled": True},
            "section3": {"host": "host3", "port": 1003, "enabled": True},
            "section4": {"host": "host4", "port": 1004, "enabled": True},
            "section5": {"host": "host5", "port": 1005, "enabled": True},
        }

    def test_from_dict_performance(self, simple_config):
        """Benchmark from_dict() performance."""
        iterations = 1000
        start = time.perf_counter()

        for _ in range(iterations):
            PrismConfig.from_dict(simple_config)

        elapsed = time.perf_counter() - start
        avg_ms = (elapsed / iterations) * 1000

        # Should load in under 5ms per iteration (CI runners are slower)
        assert avg_ms < 5.0, f"from_dict() took {avg_ms:.3f}ms average"

    def test_from_dict_with_schema_performance(self, simple_config):
        """Benchmark from_dict() with custom schema."""

        class SimpleSchema(BaseConfigRoot):
            app: BenchmarkSection
            database: BenchmarkSection

        config_data = {
            "app": {"host": "app-host", "port": 8080},
            "database": {"host": "db-host", "port": 5432}
        }

        iterations = 1000
        start = time.perf_counter()

        for _ in range(iterations):
            PrismConfig.from_dict(config_data, schema=SimpleSchema)

        elapsed = time.perf_counter() - start
        avg_ms = (elapsed / iterations) * 1000

        # Custom schema loading should be under 10ms per iteration (CI runners are slower)
        assert avg_ms < 10.0, f"from_dict(schema=) took {avg_ms:.3f}ms average"

    def test_flexible_mode_performance(self, simple_config):
        """Benchmark flexible mode (strict=False) performance."""
        iterations = 1000
        start = time.perf_counter()

        for _ in range(iterations):
            PrismConfig.from_dict(simple_config, strict=False)

        elapsed = time.perf_counter() - start
        avg_ms = (elapsed / iterations) * 1000

        # Flexible mode should be under 5ms per iteration (CI runners are slower)
        assert avg_ms < 5.0, f"from_dict(strict=False) took {avg_ms:.3f}ms average"

    def test_complex_config_performance(self, complex_config):
        """Benchmark loading complex config with many sections."""
        iterations = 500
        start = time.perf_counter()

        for _ in range(iterations):
            PrismConfig.from_dict(complex_config, strict=False)

        elapsed = time.perf_counter() - start
        avg_ms = (elapsed / iterations) * 1000

        # Complex config should load in under 10ms per iteration (CI runners are slower)
        assert avg_ms < 10.0, f"Complex config took {avg_ms:.3f}ms average"


class TestAccessPerformance:
    """Tests for configuration access performance."""

    @pytest.fixture
    def loaded_config(self):
        """Pre-loaded config for access benchmarks."""
        return PrismConfig.from_dict({
            "app": {"name": "access-app", "environment": "test"},
            "database": {"host": "localhost", "port": 5432, "name": "testdb"}
        })

    @pytest.fixture
    def flexible_config(self):
        """Pre-loaded flexible config for access benchmarks."""
        return PrismConfig.from_dict({
            "app": {"name": "flex-app", "environment": "test"},
            "database": {"host": "localhost", "port": 5432, "name": "testdb"},
            "custom": {"nested": {"deep": {"value": "found"}}}
        }, strict=False)

    def test_attribute_access_performance(self, loaded_config):
        """Benchmark attribute access on loaded config."""
        iterations = 10000
        start = time.perf_counter()

        for _ in range(iterations):
            _ = loaded_config.app.name
            _ = loaded_config.database.port

        elapsed = time.perf_counter() - start
        avg_us = (elapsed / iterations) * 1_000_000

        # Attribute access should be under 20 microseconds (CI runners are slower)
        assert avg_us < 20.0, f"Attribute access took {avg_us:.3f}µs average"

    def test_flexible_access_performance(self, flexible_config):
        """Benchmark attribute access in flexible mode."""
        iterations = 10000
        start = time.perf_counter()

        for _ in range(iterations):
            _ = flexible_config.app.name
            _ = flexible_config.database.port

        elapsed = time.perf_counter() - start
        avg_us = (elapsed / iterations) * 1_000_000

        # Flexible access should be under 50 microseconds (CI runners are slower)
        assert avg_us < 50.0, f"Flexible access took {avg_us:.3f}µs average"

    def test_deep_nested_access_performance(self, flexible_config):
        """Benchmark deep nested access in flexible mode."""
        iterations = 5000
        start = time.perf_counter()

        for _ in range(iterations):
            _ = flexible_config.custom.nested.deep.value

        elapsed = time.perf_counter() - start
        avg_us = (elapsed / iterations) * 1_000_000

        # Deep nested access should be under 100 microseconds (CI runners are slower)
        assert avg_us < 100.0, f"Deep nested access took {avg_us:.3f}µs average"


class TestDynamicConfigPerformance:
    """Tests for DynamicConfig performance."""

    def test_dynamic_config_creation(self):
        """Benchmark DynamicConfig creation."""
        data = {
            "level1": {
                "level2": {
                    "level3": {"value": "nested"}
                }
            },
            "flat": "value",
            "list": [1, 2, 3]
        }

        iterations = 5000
        start = time.perf_counter()

        for _ in range(iterations):
            DynamicConfig(data)

        elapsed = time.perf_counter() - start
        avg_us = (elapsed / iterations) * 1_000_000

        # DynamicConfig creation should be under 50 microseconds (CI runners are slower)
        assert avg_us < 50.0, f"DynamicConfig creation took {avg_us:.3f}µs average"

    def test_dynamic_config_access(self):
        """Benchmark DynamicConfig attribute access."""
        data = {
            "level1": {
                "level2": {
                    "level3": {"value": "nested"}
                }
            }
        }
        dynamic = DynamicConfig(data)

        iterations = 10000
        start = time.perf_counter()

        for _ in range(iterations):
            _ = dynamic.level1.level2.level3.value

        elapsed = time.perf_counter() - start
        avg_us = (elapsed / iterations) * 1_000_000

        # Nested access should be under 100 microseconds (CI runners are slower)
        assert avg_us < 100.0, f"DynamicConfig access took {avg_us:.3f}µs average"


class TestDumpPerformance:
    """Tests for dump/display performance."""

    @pytest.fixture
    def config_with_secrets(self):
        """Config with secrets for dump benchmarks."""
        return PrismConfig.from_dict({
            "app": {
                "name": "dump-app",
                "environment": "production",
                "api_key": "secret-api-key"
            },
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "testdb",
                "password": "secret-password"
            }
        })

    def test_dump_performance(self, config_with_secrets):
        """Benchmark dump() performance."""
        iterations = 500
        start = time.perf_counter()

        for _ in range(iterations):
            config_with_secrets.dump(use_color=False)

        elapsed = time.perf_counter() - start
        avg_ms = (elapsed / iterations) * 1000

        # dump() should complete in under 20ms (CI runners are slower)
        assert avg_ms < 20.0, f"dump() took {avg_ms:.3f}ms average"

    def test_to_yaml_performance(self, config_with_secrets):
        """Benchmark to_yaml() performance."""
        iterations = 500
        start = time.perf_counter()

        for _ in range(iterations):
            config_with_secrets.to_yaml()

        elapsed = time.perf_counter() - start
        avg_ms = (elapsed / iterations) * 1000

        # to_yaml() should complete in under 10ms (CI runners are slower)
        assert avg_ms < 10.0, f"to_yaml() took {avg_ms:.3f}ms average"

    def test_to_json_performance(self, config_with_secrets):
        """Benchmark to_json() performance."""
        iterations = 500
        start = time.perf_counter()

        for _ in range(iterations):
            config_with_secrets.to_json()

        elapsed = time.perf_counter() - start
        avg_ms = (elapsed / iterations) * 1000

        # to_json() should complete in under 5ms (CI runners are slower)
        assert avg_ms < 5.0, f"to_json() took {avg_ms:.3f}ms average"


class TestMemoryEfficiency:
    """Tests for memory efficiency (smoke tests, not precise measurements)."""

    def test_large_config_loads(self):
        """Large config with many values loads without issues."""
        # Generate a config with many keys
        config_data = {
            "app": {"name": "large-app", "environment": "test"},
            "database": {"host": "localhost", "port": 5432, "name": "testdb"}
        }

        # Add 100 additional sections
        for i in range(100):
            config_data[f"section_{i}"] = {
                "key1": f"value_{i}_1",
                "key2": f"value_{i}_2",
                "nested": {
                    "inner1": f"nested_{i}_1",
                    "inner2": f"nested_{i}_2"
                }
            }

        # Should load without memory issues
        config = PrismConfig.from_dict(config_data, strict=False)

        assert config.app.name == "large-app"
        assert config.section_50.key1 == "value_50_1"
        assert config.section_99.nested.inner2 == "nested_99_2"

    def test_repeated_loading(self):
        """Repeated loading doesn't cause memory leaks (smoke test)."""
        config_data = {
            "app": {"name": "repeat-app", "environment": "test"},
            "database": {"host": "localhost", "port": 5432, "name": "testdb"}
        }

        # Load many times
        configs = []
        for _ in range(100):
            configs.append(PrismConfig.from_dict(config_data))

        assert len(configs) == 100
        assert configs[0].app.name == "repeat-app"
        assert configs[99].database.port == 5432
