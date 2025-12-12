# Example 03: Environment Variable Overrides

This example demonstrates how to override configuration values using environment variables - the recommended approach for 12-factor apps and containerized applications.

## What You'll Learn

- ✅ How to override config values with environment variables
- ✅ Understanding the double-underscore nesting convention
- ✅ Automatic type coercion from environment variables
- ✅ Configuration precedence (CLI > ENV > FILE)
- ✅ Using custom environment variable prefixes

## Files

- `config.yaml` - Base configuration file
- `env_example.py` - Main example script
- `README.md` - This file

## Running the Example

```bash
# From the prism-config root directory
python examples/03-env-vars/env_example.py
```

## Expected Output

```
🔮 Environment Variable Override Example
==================================================

📋 Base configuration (from YAML file):
  Environment: development
  Database Host: localhost
  Database Port: 5432

🌍 Setting environment variables:
  APP_APP__ENVIRONMENT=production
  APP_DATABASE__HOST=prod-db.example.com
  APP_DATABASE__PORT=3306

📋 Configuration with env overrides:
  Environment: production
  Database Host: prod-db.example.com
  Database Port: 3306

✨ Automatic type coercion:
  PORT env var is string: '3306'
  Config port is int: 3306 (type: int)

🌈 Beautiful Display:
[Colorful table output]

📊 Precedence demonstration:
  Env var: staging
  CLI arg: production
  Final value: production (CLI wins!)

🔧 Custom prefix example:
  Using prefix: MYAPP_
  MYAPP_DATABASE__HOST=custom-db.example.com
  Result: custom-db.example.com
```

## Key Concepts

### 1. Environment Variable Naming Convention

Use double underscores (`__`) to represent nested configuration:

```bash
APP_DATABASE__HOST=localhost           # → database.host
APP_DATABASE__PORT=5432                # → database.port
APP_APP__ENVIRONMENT=production        # → app.environment
```

The format is: `{PREFIX}{SECTION}__{FIELD}={VALUE}`

### 2. Automatic Type Coercion

Environment variables are strings, but prism-config automatically converts them to the correct type:

```python
os.environ["APP_DATABASE__PORT"] = "3306"  # String in env
config = PrismConfig.from_file("config.yaml", apply_env=True)
print(config.database.port)  # 3306 (int)
print(type(config.database.port))  # <class 'int'>
```

### 3. Configuration Precedence

When multiple sources provide the same value, prism-config follows this precedence:

```
CLI Args (highest)
    ↓
Secrets (REF:: resolution)
    ↓
Environment Variables
    ↓
YAML/Config Files
    ↓
Defaults (lowest)
```

Example:

```python
# YAML file says: environment: development
# ENV var says: APP_APP__ENVIRONMENT=staging
# CLI arg says: --app.environment=production

config = PrismConfig.from_file(
    "config.yaml",
    apply_env=True,
    cli_args=["--app.environment=production"]
)

print(config.app.environment)  # "production" (CLI wins)
```

### 4. Custom Prefixes

You can use custom prefixes to avoid conflicts:

```python
# Default prefix is "APP_"
config = PrismConfig.from_file("config.yaml", apply_env=True)

# Use custom prefix
config = PrismConfig.from_file(
    "config.yaml",
    apply_env=True,
    env_prefix="MYSERVICE_"
)

# Now use: MYSERVICE_DATABASE__HOST instead of APP_DATABASE__HOST
```

## Docker & Kubernetes Usage

This feature is perfect for containerized applications:

### Docker Compose

```yaml
# docker-compose.yml
services:
  app:
    image: my-app:latest
    environment:
      - APP_APP__ENVIRONMENT=production
      - APP_DATABASE__HOST=postgres
      - APP_DATABASE__PORT=5432
      - APP_DATABASE__NAME=mydb
```

### Kubernetes ConfigMap

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_APP__ENVIRONMENT: "production"
  APP_DATABASE__HOST: "postgres-service"
  APP_DATABASE__PORT: "5432"
```

### Application Code

```python
# app.py
import sys
from prism.config import PrismConfig

# Load config with env overrides (12-factor app style)
config = PrismConfig.from_all(
    "config.yaml",
    cli_args=sys.argv[1:]
)

# Config is now populated from:
# 1. config.yaml (base values)
# 2. Environment variables (container/K8s overrides)
# 3. CLI arguments (runtime overrides)
```

## Next Steps

- **Example 04**: Use secret references for sensitive data
- **Example 05**: Docker secrets and Kubernetes integration
