# Example 01: Basic Dictionary Configuration

This example demonstrates the simplest way to use prism-config: loading configuration from a Python dictionary.

## What You'll Learn

- ✅ How to load configuration from a Python dict
- ✅ How to access configuration values with type safety
- ✅ How configuration immutability works
- ✅ How to display configuration beautifully
- ✅ How to export configuration to YAML/JSON

## Files

- `basic_example.py` - Main example script
- `README.md` - This file

## Running the Example

```bash
# From the prism-config root directory
python examples/01-basic/basic_example.py
```

## Expected Output

```
🔮 Basic Configuration Example
==================================================
App Name: hello-world-app
Environment: development
API Key: dev_key_12345

Database Host: localhost
Database Port: 5432
Database Name: development_db

📌 Configuration is immutable:
  ✅ Prevented mutation: ValidationError

🌈 Beautiful Display:

[Colorful table output]

📤 Export to different formats:

As YAML:
app:
  name: hello-world-app
  environment: development
  api_key: dev_key_12345
database:
  host: localhost
  port: 5432
  name: development_db
  password: dev_password_123

As JSON:
{
  "app": {
    "name": "hello-world-app",
    ...
  }
}
```

## Key Concepts

### 1. Type-Safe Access

```python
config = PrismConfig.from_dict(config_data)
print(config.app.name)          # ✅ Type-safe, IDE autocomplete works
print(config.database.port)      # ✅ Returns int, not str
```

### 2. Immutability

All configuration is frozen (immutable) by default. This prevents accidental modifications and makes your config predictable:

```python
config.app.name = "new-name"  # ❌ Raises ValidationError
```

### 3. Validation

Pydantic validates your configuration automatically:

```python
config_data = {
    "app": {"name": "test", "environment": "dev"},
    "database": {"port": "not_a_number"}  # ❌ Wrong type
}
config = PrismConfig.from_dict(config_data)  # Raises ConfigValidationError
```

## Next Steps

- **Example 02**: Load from YAML files
- **Example 03**: Override with environment variables
- **Example 04**: Use secret references
