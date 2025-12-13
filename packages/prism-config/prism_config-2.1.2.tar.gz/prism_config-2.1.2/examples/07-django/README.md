# Example 07: Django-style Settings (v2.0.0)

This example demonstrates using prism-config with Django applications, mapping familiar Django settings patterns to typed configuration.

## Features Demonstrated

- Django-compatible configuration structure
- Typed settings matching Django's conventions
- Environment-specific configuration
- Secret resolution for sensitive settings
- Settings.py generation from YAML config

## Files

- `config.yaml` - Django-style configuration with all common settings
- `django_example.py` - Python code demonstrating Django schema usage

## Prerequisites

```bash
# Install prism-config
cd prism-config
pip install -e .

# Set required environment variables
export DJANGO_SECRET_KEY=django-insecure-change-me
export DB_PASSWORD=secret_db_pass
export EMAIL_HOST_USER=user@example.com
export EMAIL_HOST_PASSWORD=email_pass
export SENTRY_DSN=https://example@sentry.io/123
```

## Running the Example

```bash
python examples/07-django/django_example.py
```

## Configuration Structure

The configuration maps to familiar Django settings:

```yaml
django:
  secret_key: REF::ENV::DJANGO_SECRET_KEY
  debug: true
  allowed_hosts:
    - localhost
    - 127.0.0.1

database:
  host: localhost
  port: 5432
  name: django_db
  password: REF::ENV::DB_PASSWORD

email:
  backend: smtp
  host: smtp.gmail.com
  port: 587
  use_tls: true

security:
  csrf_cookie_secure: true
  x_frame_options: DENY
  hsts_seconds: 31536000
```

## Using with Django

### Option 1: Direct Import in settings.py

```python
# settings.py
from prism.config import PrismConfig
from your_app.schemas import DjangoSettingsConfig

config = PrismConfig.from_file(
    "config.yaml",
    schema=DjangoSettingsConfig,
    resolve_secrets=True
)

# Use typed config values
SECRET_KEY = config.django.secret_key
DEBUG = config.django.debug
ALLOWED_HOSTS = config.django.allowed_hosts

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config.database.name,
        'HOST': config.database.host,
        'PORT': str(config.database.port),
        'PASSWORD': config.database.password,
    }
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config.email.host
EMAIL_PORT = config.email.port
EMAIL_USE_TLS = config.email.use_tls
```

### Option 2: Environment-Specific Configs

```python
# settings.py
import os
from prism.config import PrismConfig

env = os.getenv('DJANGO_ENV', 'development')
config = PrismConfig.from_file(f"config/{env}.yaml", resolve_secrets=True)
```

### Option 3: Use from_all() for Full Override Chain

```python
# settings.py
import sys
from prism.config import PrismConfig

config = PrismConfig.from_all(
    "config/base.yaml",
    cli_args=sys.argv[1:],
    resolve_secrets=True,
)
```

## Schema Definition

```python
from prism.config import BaseConfigSection, BaseConfigRoot, DatabaseConfig

class DjangoConfig(BaseConfigSection):
    secret_key: str
    debug: bool = False
    allowed_hosts: List[str] = ["localhost"]
    language_code: str = "en-us"
    time_zone: str = "UTC"

class EmailConfig(BaseConfigSection):
    backend: str = "smtp"
    host: str = "localhost"
    port: int = 25
    use_tls: bool = False
    host_user: Optional[str] = None
    host_password: Optional[str] = None

class SecurityConfig(BaseConfigSection):
    csrf_cookie_secure: bool = False
    x_frame_options: str = "DENY"
    hsts_seconds: int = 0

class DjangoSettingsConfig(BaseConfigRoot):
    django: DjangoConfig
    database: DatabaseConfig
    email: EmailConfig
    security: SecurityConfig
    # ... more sections
```

## Benefits

1. **Type Safety** - Catch configuration errors before deployment
2. **IDE Support** - Autocomplete for all Django settings
3. **Secret Management** - Secure handling of SECRET_KEY, passwords
4. **Environment Overrides** - Easy dev/staging/prod configuration
5. **Validation** - Pydantic validates all settings at load time
6. **Documentation** - Schema serves as settings documentation

## Next Steps

- See [08-microservice](../08-microservice/) for multi-backend configs
- See [09-multi-env](../09-multi-env/) for environment-specific setups
