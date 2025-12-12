"""
Example 06: FastAPI with Custom Schemas (v2.0.0)

This example demonstrates prism-config v2.0.0's custom schema support
for a FastAPI application with authentication and rate limiting.

Key v2.0.0 features demonstrated:
- Custom schema definitions with BaseConfigSection
- Type-safe configuration access
- Custom emoji registration for display
- Nested configuration sections
- Flexible mode for dynamic configs

Run this example:
    # Set environment variables for secrets
    export DB_PASSWORD=secret_db_pass
    export JWT_SECRET=super_secret_jwt_key
    export GOOGLE_CLIENT_ID=google_123
    export GITHUB_CLIENT_ID=github_456
    export REDIS_PASSWORD=redis_pass

    python examples/06-fastapi/fastapi_example.py
"""

import sys
from pathlib import Path
from typing import List, Optional

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from prism.config import (
    BaseConfigSection,
    BaseConfigRoot,
    DatabaseConfig,
    PrismConfig,
    register_emoji,
)


# =============================================================================
# Custom Schema Definitions (v2.0.0 Feature)
# =============================================================================


class MyAppConfig(BaseConfigSection):
    """Extended app configuration with additional fields."""

    name: str
    environment: str
    debug: bool = False
    version: str = "1.0.0"
    api_key: Optional[str] = None


class JWTConfig(BaseConfigSection):
    """JWT authentication configuration."""

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7


class SessionConfig(BaseConfigSection):
    """Session configuration."""

    cookie_name: str = "session_id"
    max_age_hours: int = 24
    secure: bool = True
    http_only: bool = True


class OAuthConfig(BaseConfigSection):
    """OAuth provider configuration."""

    enabled: bool = False
    providers: List[str] = []
    google_client_id: Optional[str] = None
    github_client_id: Optional[str] = None


class AuthConfig(BaseConfigSection):
    """Complete authentication configuration."""

    jwt: JWTConfig
    oauth: OAuthConfig
    session: SessionConfig


class RateLimitRule(BaseConfigSection):
    """Rate limit rule for an endpoint."""

    requests_per_minute: int = 60
    burst: int = 10


class RateLimitConfig(BaseConfigSection):
    """Rate limiting configuration."""

    enabled: bool = True
    default: RateLimitRule

    # Allow extra fields for endpoint-specific rules
    model_config = {"extra": "allow"}


class RedisConfig(BaseConfigSection):
    """Redis connection configuration."""

    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None


class LoggingConfig(BaseConfigSection):
    """Logging configuration."""

    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    handlers: List[str] = ["console"]
    file_path: Optional[str] = None


class CORSConfig(BaseConfigSection):
    """CORS configuration."""

    allowed_origins: List[str] = []
    allowed_methods: List[str] = ["GET", "POST"]
    allowed_headers: List[str] = ["*"]
    allow_credentials: bool = False


class FastAPIAppConfig(BaseConfigRoot):
    """
    Complete FastAPI application configuration.

    This demonstrates a fully custom schema where all sections
    are user-defined (auth, rate_limit, redis, etc.)
    """

    app: MyAppConfig
    database: DatabaseConfig
    auth: AuthConfig
    rate_limit: RateLimitConfig
    redis: RedisConfig
    logging: LoggingConfig
    cors: CORSConfig


# =============================================================================
# Main Example
# =============================================================================


def main():
    """Demonstrate FastAPI configuration with custom schemas."""

    print("=" * 60)
    print("FastAPI Configuration Example (prism-config v2.0.0)")
    print("=" * 60)
    print()

    # -------------------------------------------------------------------------
    # Step 1: Register custom emojis for better display (v2.0.0 feature)
    # -------------------------------------------------------------------------
    print("Step 1: Registering custom emojis...")
    register_emoji("logging", "📋")  # Override default if desired
    register_emoji("endpoints", "🎯")
    print("  Registered: logging -> 📋, endpoints -> 🎯")
    print()

    # -------------------------------------------------------------------------
    # Step 2: Load configuration with custom schema
    # -------------------------------------------------------------------------
    print("Step 2: Loading configuration with custom schema...")
    config_file = Path(__file__).parent / "config.yaml"

    # Load with full type safety using custom schema
    config = PrismConfig.from_file(
        config_file,
        schema=FastAPIAppConfig,
        resolve_secrets=True,  # Resolve REF:: references
    )

    print(f"  Loaded from: {config_file}")
    print("  Schema: FastAPIAppConfig")
    print()

    # -------------------------------------------------------------------------
    # Step 3: Access typed configuration values
    # -------------------------------------------------------------------------
    print("Step 3: Accessing typed configuration values...")
    print()

    # App config (built-in)
    print("  🌐 App Configuration:")
    print(f"     Name: {config.app.name}")
    print(f"     Environment: {config.app.environment}")
    print(f"     Debug: {config.app.debug}")
    print()

    # Database config (built-in)
    print("  💾 Database Configuration:")
    print(f"     Host: {config.database.host}")
    print(f"     Port: {config.database.port}")
    print(f"     Name: {config.database.name}")
    print()

    # Auth config (custom!)
    print("  🔑 Auth Configuration:")
    print(f"     JWT Algorithm: {config.auth.jwt.algorithm}")
    print(f"     Access Token Expiry: {config.auth.jwt.access_token_expire_minutes} min")
    print(f"     OAuth Enabled: {config.auth.oauth.enabled}")
    print(f"     OAuth Providers: {', '.join(config.auth.oauth.providers)}")
    print(f"     Session Cookie: {config.auth.session.cookie_name}")
    print()

    # Rate limit config (custom!)
    print("  ⏱️ Rate Limit Configuration:")
    print(f"     Enabled: {config.rate_limit.enabled}")
    print(f"     Default: {config.rate_limit.default.requests_per_minute} req/min")
    print(f"     Default Burst: {config.rate_limit.default.burst}")
    print()

    # Redis config (custom!)
    print("  🔴 Redis Configuration:")
    print(f"     Host: {config.redis.host}")
    print(f"     Port: {config.redis.port}")
    print(f"     DB: {config.redis.db}")
    print()

    # CORS config (custom!)
    print("  🌍 CORS Configuration:")
    print(f"     Origins: {', '.join(config.cors.allowed_origins)}")
    print(f"     Methods: {', '.join(config.cors.allowed_methods)}")
    print(f"     Credentials: {config.cors.allow_credentials}")
    print()

    # -------------------------------------------------------------------------
    # Step 4: Display beautiful output with auto-detected emojis
    # -------------------------------------------------------------------------
    print("Step 4: Beautiful display with auto-detected emojis...")
    print()
    config.display()
    print()

    # -------------------------------------------------------------------------
    # Step 5: Export configuration (secrets redacted)
    # -------------------------------------------------------------------------
    print("Step 5: Export configuration (YAML format):")
    print("-" * 40)
    yaml_output = config.to_yaml()
    # Only show first 30 lines for brevity
    lines = yaml_output.split("\n")[:30]
    print("\n".join(lines))
    if len(yaml_output.split("\n")) > 30:
        print("... (truncated)")
    print("-" * 40)
    print()

    # -------------------------------------------------------------------------
    # Step 6: Example of using config in FastAPI (pseudo-code)
    # -------------------------------------------------------------------------
    print("Step 6: FastAPI integration example (pseudo-code):")
    print()
    print("""
    from fastapi import FastAPI
    from slowapi import Limiter
    from slowapi.util import get_remote_address

    # Create FastAPI app using config
    app = FastAPI(
        title=config.app.name,
        debug=config.app.debug,
    )

    # Configure rate limiter
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[
            f"{config.rate_limit.default.requests_per_minute}/minute"
        ],
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors.allowed_origins,
        allow_methods=config.cors.allowed_methods,
        allow_headers=config.cors.allowed_headers,
        allow_credentials=config.cors.allow_credentials,
    )

    # JWT configuration available for auth
    JWT_SECRET = config.auth.jwt.secret_key
    JWT_ALGORITHM = config.auth.jwt.algorithm
    """)

    print("=" * 60)
    print("Example complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
