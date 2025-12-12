# Example 06: FastAPI with Custom Schemas (v2.0.0)

This example demonstrates prism-config v2.0.0's powerful custom schema support for building type-safe FastAPI applications with authentication and rate limiting.

## Features Demonstrated

### v2.0.0 Custom Schema Features

- **BaseConfigSection** - Create custom typed configuration sections
- **BaseConfigRoot** - Define complete application configuration schemas
- **Type Safety** - Full IDE autocomplete and type checking
- **Custom Emoji Registration** - Customize display output for custom sections
- **Nested Configurations** - Deep nesting with `auth.jwt.secret_key` style access

### Application Features

- JWT authentication configuration
- OAuth provider settings
- Rate limiting per endpoint
- Redis connection settings
- CORS configuration
- Logging settings

## Files

- `config.yaml` - Example configuration with auth, rate limiting, and more
- `fastapi_example.py` - Python code demonstrating custom schema usage

## Prerequisites

```bash
# Install prism-config in development mode
cd prism-config
pip install -e .

# Set required environment variables for secrets
export DB_PASSWORD=secret_db_pass
export JWT_SECRET=super_secret_jwt_key
export GOOGLE_CLIENT_ID=google_123
export GITHUB_CLIENT_ID=github_456
export REDIS_PASSWORD=redis_pass
```

## Running the Example

```bash
python examples/06-fastapi/fastapi_example.py
```

## Key Concepts

### Defining Custom Sections

```python
from prism.config import BaseConfigSection

class JWTConfig(BaseConfigSection):
    """JWT authentication configuration."""
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

class AuthConfig(BaseConfigSection):
    """Complete auth configuration with nested sections."""
    jwt: JWTConfig
    oauth: OAuthConfig
    session: SessionConfig
```

### Creating a Complete Schema

```python
from prism.config import BaseConfigRoot, AppConfig, DatabaseConfig

class FastAPIAppConfig(BaseConfigRoot):
    """Complete application configuration."""
    app: AppConfig           # Built-in section
    database: DatabaseConfig # Built-in section
    auth: AuthConfig         # Custom section!
    rate_limit: RateLimitConfig
    redis: RedisConfig
```

### Loading with Custom Schema

```python
from prism.config import PrismConfig

# Full type safety - IDE knows all types!
config = PrismConfig.from_file(
    "config.yaml",
    schema=FastAPIAppConfig,
    resolve_secrets=True,
)

# Type-checked access
config.auth.jwt.algorithm        # str
config.auth.jwt.access_token_expire_minutes  # int
config.rate_limit.enabled        # bool
```

### Custom Emoji Registration

```python
from prism.config import register_emoji

# Register emojis for your custom sections
register_emoji("endpoints", "🎯")
register_emoji("logging", "📋")

# Now display() will use these emojis
config.display()
```

## Configuration Structure

```yaml
app:
  name: fastapi-example
  environment: development

database:
  host: localhost
  port: 5432
  password: REF::ENV::DB_PASSWORD  # Secret reference

auth:
  jwt:
    secret_key: REF::ENV::JWT_SECRET
    algorithm: HS256
    access_token_expire_minutes: 30
  oauth:
    enabled: true
    providers:
      - google
      - github
  session:
    cookie_name: session_id
    secure: true

rate_limit:
  enabled: true
  default:
    requests_per_minute: 60
    burst: 10
  endpoints:
    "/api/v1/login":
      requests_per_minute: 5
      burst: 2
```

## Integration with FastAPI

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load configuration
config = PrismConfig.from_file("config.yaml", schema=FastAPIAppConfig)

# Create app
app = FastAPI(
    title=config.app.name,
    debug=config.app.debug,
)

# Configure CORS from config
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors.allowed_origins,
    allow_methods=config.cors.allowed_methods,
    allow_headers=config.cors.allowed_headers,
    allow_credentials=config.cors.allow_credentials,
)

# Use auth config for JWT
from jose import jwt

def create_access_token(data: dict):
    return jwt.encode(
        data,
        config.auth.jwt.secret_key,
        algorithm=config.auth.jwt.algorithm,
    )
```

## Benefits of Custom Schemas

1. **Type Safety** - Catch configuration errors at development time
2. **IDE Support** - Full autocomplete for all configuration fields
3. **Documentation** - Schema serves as documentation for configuration
4. **Validation** - Pydantic validates all values automatically
5. **Flexibility** - Mix built-in and custom sections as needed

## Next Steps

- See [07-django](../07-django/) for Django-style settings
- See [08-microservice](../08-microservice/) for multi-backend configs
- Read the [Migration Guide](../../docs/migration-v2.md) for upgrading from v1.x
