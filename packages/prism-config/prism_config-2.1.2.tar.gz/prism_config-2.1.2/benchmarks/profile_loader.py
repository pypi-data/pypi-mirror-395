"""
Profiling script to identify performance bottlenecks in prism-config.

This script uses cProfile to analyze where time is spent during config loading.
"""

import cProfile
import pstats
import os
from io import StringIO
from prism.config import PrismConfig


def profile_env_override():
    """Profile environment variable override performance."""
    print("\n" + "=" * 60)
    print("Profiling: Environment Variable Override")
    print("=" * 60)

    config_data = {
        "app": {"name": "profile-app", "environment": "production"},
        "database": {"host": "localhost", "port": 5432, "name": "profiledb"}
    }

    # Set environment variables
    os.environ["PRISM__DATABASE__HOST"] = "override-host"
    os.environ["PRISM__DATABASE__PORT"] = "9999"
    os.environ["PRISM__APP__NAME"] = "override-app"

    profiler = cProfile.Profile()
    profiler.enable()

    # Run multiple iterations
    for _ in range(1000):
        PrismConfig.from_dict(config_data, apply_env=True)

    profiler.disable()

    # Print stats
    s = StringIO()
    stats = pstats.Stats(profiler, stream=s)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions
    print(s.getvalue())

    # Cleanup
    del os.environ["PRISM__DATABASE__HOST"]
    del os.environ["PRISM__DATABASE__PORT"]
    del os.environ["PRISM__APP__NAME"]


def profile_secret_resolution():
    """Profile secret resolution performance."""
    print("\n" + "=" * 60)
    print("Profiling: Secret Resolution")
    print("=" * 60)

    os.environ["PROFILE_SECRET_1"] = "secret_value_1"
    os.environ["PROFILE_SECRET_2"] = "secret_value_2"

    config_data = {
        "app": {"name": "profile-app", "environment": "production"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "profiledb",
            "password": "REF::ENV::PROFILE_SECRET_1",
            "api_token": "REF::ENV::PROFILE_SECRET_2"
        }
    }

    profiler = cProfile.Profile()
    profiler.enable()

    # Run multiple iterations
    for _ in range(1000):
        PrismConfig.from_dict(config_data, resolve_secrets=True)

    profiler.disable()

    # Print stats
    s = StringIO()
    stats = pstats.Stats(profiler, stream=s)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions
    print(s.getvalue())

    # Cleanup
    del os.environ["PROFILE_SECRET_1"]
    del os.environ["PROFILE_SECRET_2"]


def profile_dump():
    """Profile dump() output generation."""
    print("\n" + "=" * 60)
    print("Profiling: dump() Output Generation")
    print("=" * 60)

    config_data = {
        "app": {"name": "profile-app", "environment": "production"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "profiledb",
            "password": "secret-password"
        }
    }

    config = PrismConfig.from_dict(config_data)

    profiler = cProfile.Profile()
    profiler.enable()

    # Run multiple iterations
    for _ in range(1000):
        config.dump(use_color=False)

    profiler.disable()

    # Print stats
    s = StringIO()
    stats = pstats.Stats(profiler, stream=s)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions
    print(s.getvalue())


if __name__ == "__main__":
    print("=" * 60)
    print("PRISM CONFIG - Performance Profiling")
    print("=" * 60)
    print("\nThis may take a minute...")

    profile_env_override()
    profile_secret_resolution()
    profile_dump()

    print("\n" + "=" * 60)
    print("Profiling complete!")
    print("=" * 60)
