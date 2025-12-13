# Example 10: Catch-All Flexible Configuration (v2.0.0)

This example demonstrates prism-config's flexible mode, which accepts ANY configuration structure without requiring a predefined schema.

## Features Demonstrated

- Schema-free configuration loading
- Dot-notation access for any nested path
- DynamicConfig for arbitrary structures
- Hybrid mode (typed + flexible sections)
- Works with unknown configuration formats

## Files

- `config.yaml` - Configuration with arbitrary sections
- `flexible_example.py` - Python code demonstrating flexible mode

## Prerequisites

```bash
# Install prism-config
cd prism-config
pip install -e .

# Set environment variables for secrets
export SENDGRID_API_KEY=sg_test_key
export TWILIO_SID=AC123
export TWILIO_TOKEN=auth_token
export STRIPE_SECRET=sk_test_xxx
export STRIPE_WEBHOOK=whsec_xxx
```

## Running the Example

```bash
python examples/10-flexible/flexible_example.py
```

## Flexible Mode Usage

### strict=False Enables Flexible Mode

```python
from prism.config import PrismConfig

# Use strict=False for flexible mode
config = PrismConfig.from_file("config.yaml", strict=False)

# Access ANY section
config.my_custom_section.nested.value
config.analytics.providers.google.tracking_id
config.arbitrary.deeply.nested.path
```

### Works with Any Structure

```yaml
# config.yaml - any structure works!
my_service:
  endpoint: https://api.example.com
  retry:
    max_attempts: 3
    backoff: exponential

analytics:
  providers:
    google:
      tracking_id: UA-12345678
    mixpanel:
      project_token: abc123
```

```python
# All paths accessible via dot notation
config.my_service.endpoint
config.my_service.retry.max_attempts
config.analytics.providers.google.tracking_id
```

## DynamicConfig

For programmatic use, create DynamicConfig from any dict:

```python
from prism.config import DynamicConfig

data = {
    "server": {
        "host": "localhost",
        "ssl": {"enabled": True}
    }
}

dynamic = DynamicConfig(data)
dynamic.server.host          # "localhost"
dynamic.server.ssl.enabled   # True
```

## Hybrid Mode

Combine typed validation with flexible extras:

```python
from prism.config import BaseConfigRoot, AppConfig

class HybridConfig(BaseConfigRoot):
    app: AppConfig  # Validated

    model_config = {"extra": "allow"}  # Allow extra sections

config = PrismConfig.from_file("config.yaml", schema=HybridConfig)
config.app.name               # Typed, validated
config.my_custom_section      # Also works, flexible
```

## When to Use Each Mode

### Flexible Mode (No Schema)

Best for:
- Unknown configuration structures
- External/dynamic configurations
- Rapid prototyping
- Plugin systems with arbitrary config

### Typed Mode (With Schema)

Best for:
- Production applications
- Team projects needing conventions
- IDE autocomplete requirements
- Early error detection

### Hybrid Mode

Best for:
- Core typed + optional extensions
- Gradual migration to typed configs
- Third-party plugin configurations

## Configuration Example

```yaml
# Standard sections (emojis auto-detected)
app:
  name: flexible-app

# Custom sections (register emojis for display)
my_service:
  endpoint: https://api.example.com

# Deeply nested (any depth works)
analytics:
  providers:
    google:
      tracking_id: UA-12345678

# Lists of objects
notifications:
  channels:
    - type: email
      provider: sendgrid
    - type: sms
      provider: twilio

# Feature flags
feature_flags:
  dark_mode: true
  experiments:
    checkout_v2: 0.5
```

## Registering Emojis for Custom Sections

```python
from prism.config import register_emoji

# Register emojis for beautiful display output
register_emoji("my_service", "🔧")
register_emoji("analytics", "📊")
register_emoji("notifications", "🔔")
register_emoji("feature_flags", "🚩")
```

## Benefits

1. **Zero Configuration** - Works immediately with any YAML/JSON
2. **Full Access** - Any nested path accessible via dot notation
3. **Secret Resolution** - REF:: syntax still works
4. **Beautiful Display** - Neon dump with custom emojis
5. **Gradual Typing** - Start flexible, add schema later
