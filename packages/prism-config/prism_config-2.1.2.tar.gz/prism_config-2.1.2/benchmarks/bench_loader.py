"""
Performance benchmarks for prism-config loader operations.

This module benchmarks:
- Small config loading (<1KB)
- Large config loading (>1MB)
- Secret resolution overhead
- YAML parsing performance
- Environment variable override performance
"""

import time
import tempfile
import os
from pathlib import Path
from typing import Callable
from prism.config import PrismConfig


def benchmark(func: Callable, iterations: int = 100) -> dict:
    """
    Run a benchmark function multiple times and return statistics.

    Args:
        func: Function to benchmark (should return None)
        iterations: Number of times to run the function

    Returns:
        dict with min, max, mean, total times in milliseconds
    """
    times = []

    for _ in range(iterations):
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convert to milliseconds

    return {
        "min_ms": min(times),
        "max_ms": max(times),
        "mean_ms": sum(times) / len(times),
        "total_ms": sum(times),
        "iterations": iterations
    }


def bench_small_config_dict():
    """Benchmark 10.2: Load small config from dict (<1KB)."""
    config_data = {
        "app": {
            "name": "benchmark-app",
            "environment": "production"
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "benchdb"
        }
    }

    def load():
        PrismConfig.from_dict(config_data)

    results = benchmark(load, iterations=1000)
    print("\nBenchmark 10.2: Small Config from Dict (<1KB)")
    print(f"  Min:  {results['min_ms']:.3f} ms")
    print(f"  Max:  {results['max_ms']:.3f} ms")
    print(f"  Mean: {results['mean_ms']:.3f} ms")
    print(f"  Total: {results['total_ms']:.2f} ms ({results['iterations']} iterations)")
    return results


def bench_small_config_yaml():
    """Benchmark 10.2b: Load small config from YAML file."""
    yaml_content = """
app:
  name: benchmark-app
  environment: production

database:
  host: localhost
  port: 5432
  name: benchdb
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(yaml_content)
        yaml_path = f.name

    try:
        def load():
            PrismConfig.from_file(yaml_path)

        results = benchmark(load, iterations=1000)
        print("\nBenchmark 10.2b: Small Config from YAML File")
        print(f"  Min:  {results['min_ms']:.3f} ms")
        print(f"  Max:  {results['max_ms']:.3f} ms")
        print(f"  Mean: {results['mean_ms']:.3f} ms")
        print(f"  Total: {results['total_ms']:.2f} ms ({results['iterations']} iterations)")
        return results
    finally:
        os.unlink(yaml_path)


def bench_large_config():
    """Benchmark 10.3: Load large config (>1MB)."""
    # Generate large config with many keys
    config_data = {
        "app": {
            "name": "benchmark-app",
            "environment": "production"
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "benchdb",
            # Add large value to exceed 1MB
            "large_key": "A" * (1024 * 1024 + 1000)  # ~1MB + overhead
        }
    }

    def load():
        PrismConfig.from_dict(config_data)

    results = benchmark(load, iterations=100)  # Fewer iterations for large config
    print("\nBenchmark 10.3: Large Config (>1MB)")
    print(f"  Min:  {results['min_ms']:.3f} ms")
    print(f"  Max:  {results['max_ms']:.3f} ms")
    print(f"  Mean: {results['mean_ms']:.3f} ms")
    print(f"  Total: {results['total_ms']:.2f} ms ({results['iterations']} iterations)")
    return results


def bench_secret_resolution():
    """Benchmark 10.4: Secret resolution overhead."""
    # Set up environment secrets
    os.environ["BENCH_SECRET_1"] = "secret_value_1"
    os.environ["BENCH_SECRET_2"] = "secret_value_2"
    os.environ["BENCH_SECRET_3"] = "secret_value_3"

    config_data = {
        "app": {
            "name": "benchmark-app",
            "environment": "production",
            "api_key": "REF::ENV::BENCH_SECRET_1"
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "benchdb",
            "password": "REF::ENV::BENCH_SECRET_2",
            "api_token": "REF::ENV::BENCH_SECRET_3"
        }
    }

    def load_with_secrets():
        PrismConfig.from_dict(config_data, resolve_secrets=True)

    def load_without_secrets():
        PrismConfig.from_dict(config_data, resolve_secrets=False)

    results_with = benchmark(load_with_secrets, iterations=1000)
    results_without = benchmark(load_without_secrets, iterations=1000)

    overhead = results_with["mean_ms"] - results_without["mean_ms"]
    overhead_pct = (overhead / results_without["mean_ms"]) * 100

    print("\nBenchmark 10.4: Secret Resolution Overhead")
    print(f"  Without secrets: {results_without['mean_ms']:.3f} ms")
    print(f"  With secrets:    {results_with['mean_ms']:.3f} ms")
    print(f"  Overhead:        {overhead:.3f} ms ({overhead_pct:.1f}%)")

    # Cleanup
    del os.environ["BENCH_SECRET_1"]
    del os.environ["BENCH_SECRET_2"]
    del os.environ["BENCH_SECRET_3"]

    return {
        "without_secrets": results_without,
        "with_secrets": results_with,
        "overhead_ms": overhead,
        "overhead_pct": overhead_pct
    }


def bench_env_override():
    """Benchmark 10.5: Environment variable override performance."""
    config_data = {
        "app": {
            "name": "benchmark-app",
            "environment": "production"
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "benchdb"
        }
    }

    # Set environment variables
    os.environ["PRISM__DATABASE__HOST"] = "override-host"
    os.environ["PRISM__DATABASE__PORT"] = "9999"

    def load_with_env():
        PrismConfig.from_dict(config_data, apply_env=True)

    def load_without_env():
        PrismConfig.from_dict(config_data, apply_env=False)

    results_with = benchmark(load_with_env, iterations=1000)
    results_without = benchmark(load_without_env, iterations=1000)

    overhead = results_with["mean_ms"] - results_without["mean_ms"]
    overhead_pct = (overhead / results_without["mean_ms"]) * 100

    print("\nBenchmark 10.5: Environment Override Overhead")
    print(f"  Without env:  {results_without['mean_ms']:.3f} ms")
    print(f"  With env:     {results_with['mean_ms']:.3f} ms")
    print(f"  Overhead:     {overhead:.3f} ms ({overhead_pct:.1f}%)")

    # Cleanup
    del os.environ["PRISM__DATABASE__HOST"]
    del os.environ["PRISM__DATABASE__PORT"]

    return {
        "without_env": results_without,
        "with_env": results_with,
        "overhead_ms": overhead,
        "overhead_pct": overhead_pct
    }


def bench_dump_output():
    """Benchmark 10.6: dump() output generation performance."""
    config_data = {
        "app": {
            "name": "benchmark-app",
            "environment": "production",
            "api_key": "secret-key-123"
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "benchdb",
            "password": "secret-pass-456"
        }
    }

    config = PrismConfig.from_dict(config_data)

    def dump_with_color():
        config.dump(use_color=True)

    def dump_without_color():
        config.dump(use_color=False)

    results_with = benchmark(dump_with_color, iterations=1000)
    results_without = benchmark(dump_without_color, iterations=1000)

    print("\nBenchmark 10.6: dump() Output Performance")
    print(f"  With color:    {results_with['mean_ms']:.3f} ms")
    print(f"  Without color: {results_without['mean_ms']:.3f} ms")

    return {
        "with_color": results_with,
        "without_color": results_without
    }


def run_all_benchmarks():
    """Run all benchmarks and print summary."""
    print("=" * 60)
    print("PRISM CONFIG - Performance Benchmarks")
    print("=" * 60)

    results = {}

    # Run all benchmarks
    results["small_dict"] = bench_small_config_dict()
    results["small_yaml"] = bench_small_config_yaml()
    results["large_config"] = bench_large_config()
    results["secret_resolution"] = bench_secret_resolution()
    results["env_override"] = bench_env_override()
    results["dump_output"] = bench_dump_output()

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"\nSmall config (dict):  {results['small_dict']['mean_ms']:.3f} ms")
    print(f"Small config (YAML):  {results['small_yaml']['mean_ms']:.3f} ms")
    print(f"Large config (>1MB):  {results['large_config']['mean_ms']:.3f} ms")
    print(f"Secret overhead:      {results['secret_resolution']['overhead_ms']:.3f} ms ({results['secret_resolution']['overhead_pct']:.1f}%)")
    print(f"Env override overhead: {results['env_override']['overhead_ms']:.3f} ms ({results['env_override']['overhead_pct']:.1f}%)")
    print(f"dump() with color:    {results['dump_output']['with_color']['mean_ms']:.3f} ms")
    print(f"dump() no color:      {results['dump_output']['without_color']['mean_ms']:.3f} ms")

    print("\nAll benchmarks complete!")
    print("=" * 60)

    return results


if __name__ == "__main__":
    run_all_benchmarks()
