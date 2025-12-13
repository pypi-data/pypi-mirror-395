# prism-config v2.0.0 - Flexible Schema Support

**Target Version:** 2.0.0
**Codename:** "Spectrum"
**Status:** Planning
**Created:** 2025-12-05

---

## Overview

Version 2.0.0 introduces **flexible, pluggable configuration schemas** - allowing users to define their own configuration structure while maintaining type safety, beautiful Neon Dump output, and all existing features.

### Design Goals

1. **Maximum Flexibility** - Support any configuration structure users need
2. **Type Safety** - Preserve IDE autocomplete and runtime validation
3. **Beautiful Output** - Smart emoji detection for custom sections
4. **Backward Compatible** - Existing code continues to work unchanged
5. **Easy Migration** - Simple path from fixed to custom schemas

---

## Iteration 15: Expanded Built-in Support ✅ COMPLETE

### 15.1: Expand Emoji Mappings ✅

- [x] **15.1.1** Add auth/security section emojis (auth, jwt, oauth, session, cors, ssl, tls)
- [x] **15.1.2** Add caching section emojis (redis, memcached, cache)
- [x] **15.1.3** Add messaging section emojis (kafka, rabbitmq, celery, queue, pubsub)
- [x] **15.1.4** Add cloud provider emojis (aws, azure, gcp, s3, lambda, cloudflare)
- [x] **15.1.5** Add observability emojis (logging, log, metrics, tracing, sentry, datadog)
- [x] **15.1.6** Add infrastructure emojis (http, grpc, websocket, graphql, rest)
- [x] **15.1.7** Add feature/business emojis (feature, flags, payment, stripe, email, smtp)
- [x] **15.1.8** Add rate limiting emoji (rate_limit, throttle, quota)
- [x] **15.1.9** Write tests for new emoji mappings
- [x] **15.1.10** Update Palette dataclass with comprehensive defaults

### 15.2: Smart Emoji Detection ✅

- [x] **15.2.1** Implement partial matching (e.g., "jwt_config" matches "jwt")
- [x] **15.2.2** Implement keyword detection in section names
- [x] **15.2.3** Add fallback emoji categories (security-related -> lock, data-related -> disk)
- [x] **15.2.4** Write tests for smart detection
- [x] **15.2.5** Update detect_category() function

---

## Iteration 16: Generic Schema Support ✅ COMPLETE

### 16.1: Type Infrastructure ✅

- [x] **16.1.1** Add TypeVar for generic schema: `T = TypeVar('T', bound=BaseModel)`
- [x] **16.1.2** Make PrismConfig generic: `class PrismConfig(Generic[T])`
- [x] **16.1.3** Add `schema` parameter to from_dict()
- [x] **16.1.4** Add `schema` parameter to from_file()
- [x] **16.1.5** Add `schema` parameter to from_all()
- [x] **16.1.6** Implement __getattr__ for dynamic section access
- [x] **16.1.7** Maintain backward compatibility (default to ConfigRoot)
- [x] **16.1.8** Write comprehensive tests for generic support (18 tests)

### 16.2: Base Classes for Custom Schemas ✅

- [x] **16.2.1** Create `BaseConfigSection` class with frozen defaults
- [x] **16.2.2** Create `BaseConfigRoot` class for custom root schemas
- [x] **16.2.3** Document model_config best practices (in docstrings)
- [x] **16.2.4** Export base classes from __init__.py
- [x] **16.2.5** Write tests for custom schema creation

### 16.3: Schema Validation ✅

- [x] **16.3.1** Validate custom schema inherits from BaseModel
- [x] **16.3.2** Provide helpful error for invalid schemas
- [x] **16.3.3** Support both strict (extra="forbid") and flexible (extra="allow") modes
- [x] **16.3.4** Write tests for schema validation

---

## Iteration 17: Flexible/Catch-All Mode ✅ COMPLETE

### 17.1: Dynamic Configuration ✅

- [x] **17.1.1** Add `strict=False` parameter for catch-all mode
- [x] **17.1.2** Implement DynamicConfig class for unknown structures
- [x] **17.1.3** Convert nested dicts to dot-accessible objects (DynamicConfig class)
- [x] **17.1.4** Preserve type coercion for known types
- [x] **17.1.5** Write tests for flexible mode (33 tests)

### 17.2: Hybrid Mode ✅

- [x] **17.2.1** Support mixing typed sections with flexible extras
- [x] **17.2.2** Implement `extra="allow"` support in custom schemas
- [x] **17.2.3** Document hybrid schema patterns (in docstrings and tests)
- [x] **17.2.4** Write tests for hybrid configurations (6 tests)

---

## Iteration 18: Enhanced Display System ✅ COMPLETE

### 18.1: Dynamic Emoji Registration ✅

- [x] **18.1.1** Add `register_emoji(section, emoji)` function
- [x] **18.1.2** Support emoji registration via palette TOML
- [x] **18.1.3** Allow users to customize section icons at runtime
- [x] **18.1.4** Write tests for dynamic emoji registration (19 tests)

### 18.2: Nested Section Support ✅

- [x] **18.2.1** Improve display for deeply nested configs
- [x] **18.2.2** Support hierarchical emoji detection (auth.jwt uses auth emoji)
- [x] **18.2.3** Configurable nesting depth for display (max_depth in Palette)
- [x] **18.2.4** Write tests for nested display (15 tests)

### 18.3: Extended Secret Detection ✅

- [x] **18.3.1** Allow custom secret keywords via config (secret_keywords in Palette)
- [x] **18.3.2** Support regex patterns for secret detection (secret_patterns in Palette)
- [x] **18.3.3** Document secret detection customization (in docstrings)
- [x] **18.3.4** Write tests for custom secret patterns (19 tests)

---

## Iteration 19: Documentation & Examples ✅ COMPLETE

### 19.1: Custom Schema Examples ✅

- [x] **19.1.1** Create example: FastAPI with auth, rate limiting
- [x] **19.1.2** Create example: Django-style settings
- [x] **19.1.3** Create example: Microservice with multiple backends
- [x] **19.1.4** Create example: Multi-environment config (dev/staging/prod)
- [x] **19.1.5** Create example: Catch-all flexible config

### 19.2: Migration Guide ✅

- [x] **19.2.1** Write v1.x to v2.0 migration guide
- [x] **19.2.2** Document breaking changes (if any)
- [x] **19.2.3** Provide code migration examples
- [x] **19.2.4** Document deprecation timeline

### 19.3: API Documentation ✅

- [x] **19.3.1** Update all docstrings for new parameters
- [x] **19.3.2** Document BaseConfigSection usage
- [x] **19.3.3** Document Generic[T] pattern for type hints
- [x] **19.3.4** Update README with custom schema section
- [x] **19.3.5** Update CODEX.md with architecture changes

---

## Iteration 20: Testing & Release

### 20.1: Comprehensive Testing

- [ ] **20.1.1** Add property tests for custom schemas
- [ ] **20.1.2** Add parity tests for flexible mode
- [ ] **20.1.3** Test backward compatibility with v1.x configs
- [ ] **20.1.4** Performance benchmarks for generic access
- [ ] **20.1.5** Integration tests with real-world config patterns

### 20.2: Release Preparation

- [ ] **20.2.1** Update version to 2.0.0
- [ ] **20.2.2** Update CHANGELOG.md
- [ ] **20.2.3** Create RELEASE_NOTES for v2.0.0
- [ ] **20.2.4** Update pyproject.toml metadata
- [ ] **20.2.5** Build and test package
- [ ] **20.2.6** Publish to PyPI

---

## API Preview

### Option 1: Built-in Flexible Schema (Default in v2)

```python
from prism.config import PrismConfig

# Works with ANY section names - no schema definition needed
config = PrismConfig.from_file("config.yaml")
config.auth.jwt.issuer        # Works!
config.rate_limit.requests    # Works!
config.my_custom_section.foo  # Works!
```

### Option 2: Custom Typed Schema (Full Type Safety)

```python
from prism.config import PrismConfig, BaseConfigSection

class JWTConfig(BaseConfigSection):
    issuer: str
    secret: str
    expiry_hours: int = 24

class AuthConfig(BaseConfigSection):
    jwt: JWTConfig
    enable_oauth: bool = False

class RateLimitConfig(BaseConfigSection):
    requests_per_minute: int = 100
    burst: int = 20

class MyAppConfig(BaseConfigSection):
    app: AppConfig          # Built-in
    database: DatabaseConfig  # Built-in
    auth: AuthConfig        # Custom!
    rate_limit: RateLimitConfig

# Full type safety and IDE autocomplete
config = PrismConfig.from_file("config.yaml", schema=MyAppConfig)
config.auth.jwt.issuer  # str - IDE knows the type!
```

### Option 3: Hybrid (Typed + Flexible)

```python
from pydantic import BaseModel

class MyConfig(BaseModel):
    app: AppConfig
    database: DatabaseConfig
    # Allow any additional sections
    model_config = {"extra": "allow"}

config = PrismConfig.from_file("config.yaml", schema=MyConfig)
config.app.name           # Typed
config.unknown_section    # Also works (dict/namespace)
```

---

## Expanded Emoji Mapping (Preview)

```python
SECTION_EMOJIS = {
    # Core (existing)
    "app": "🌐",
    "database": "💾",
    "api": "🔌",
    "server": "🖥️",
    "cache": "📊",
    "queue": "📥",
    "storage": "📁",
    "network": "📡",
    "security": "🔐",
    "monitoring": "📊",

    # Auth & Security (new)
    "auth": "🔑",
    "jwt": "🎫",
    "oauth": "🔓",
    "session": "🎟️",
    "cors": "🌍",
    "ssl": "🔒",
    "tls": "🔒",

    # Caching (new)
    "redis": "🔴",
    "memcached": "🧠",

    # Messaging (new)
    "kafka": "📬",
    "rabbitmq": "🐰",
    "celery": "🥬",
    "pubsub": "📢",

    # Cloud (new)
    "aws": "☁️",
    "azure": "🔷",
    "gcp": "🔶",
    "s3": "🪣",
    "lambda": "λ",
    "cloudflare": "🟠",

    # Observability (new)
    "logging": "📝",
    "log": "📝",
    "metrics": "📈",
    "tracing": "🔍",
    "sentry": "🛡️",
    "datadog": "🐕",

    # HTTP/API (new)
    "http": "🌐",
    "grpc": "⚡",
    "websocket": "🔌",
    "graphql": "◼️",
    "rest": "🔄",

    # Business/Features (new)
    "feature": "🚩",
    "flags": "🏳️",
    "payment": "💳",
    "stripe": "💰",
    "email": "📧",
    "smtp": "✉️",

    # Rate Limiting (new)
    "rate_limit": "⏱️",
    "throttle": "🚦",
    "quota": "📊",
}
```

---

## Success Criteria

- [ ] All existing v1.x code works without modification
- [ ] Custom schemas provide full type safety
- [ ] Flexible mode accepts any configuration structure
- [ ] Neon Dump displays appropriate emojis for all sections
- [ ] 100% backward compatibility
- [ ] Comprehensive documentation and examples
- [ ] All tests passing (150+ expected)

---

## Progress Summary

```
Iteration 15: Expanded Built-in Support    [x] 15/15 tasks ✅
Iteration 16: Generic Schema Support       [x] 17/17 tasks ✅
Iteration 17: Flexible/Catch-All Mode      [x] 9/9 tasks ✅
Iteration 18: Enhanced Display System      [x] 12/12 tasks ✅
Iteration 19: Documentation & Examples     [x] 14/14 tasks ✅
Iteration 20: Testing & Release            [ ] 0/11 tasks
─────────────────────────────────────────────────────────
Total                                      [■■■■■■■■■□] 67/78 tasks (86%)
```

---

**Last Updated:** 2025-12-05
