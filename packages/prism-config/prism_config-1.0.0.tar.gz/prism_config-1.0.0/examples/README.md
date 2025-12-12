# prism-config Examples

This directory contains practical examples demonstrating all features of prism-config.

## Prerequisites

```bash
# Install prism-config in development mode
cd prism-config
pip install -e .
```

## Examples

### [01-basic](./01-basic/) - Basic Dictionary Configuration

Learn the fundamentals of prism-config by loading configuration from a Python dictionary.

**Topics covered:**
- Loading from Python dict
- Type-safe access
- Configuration immutability
- Beautiful display output
- Export to YAML/JSON

**Run:**
```bash
python examples/01-basic/basic_example.py
```

---

### [02-yaml](./02-yaml/) - YAML File Loading

Load configuration from YAML files - the recommended approach for most applications.

**Topics covered:**
- Loading from YAML files
- Using Path objects
- Error handling with clear messages
- Exporting to different formats
- Saving configuration to files

**Run:**
```bash
python examples/02-yaml/yaml_example.py
```

---

### [03-env-vars](./03-env-vars/) - Environment Variable Overrides

Override configuration using environment variables for 12-factor apps.

**Topics covered:**
- Environment variable naming convention (double underscore)
- Automatic type coercion
- Configuration precedence
- Custom prefixes
- Docker/Kubernetes integration

**Run:**
```bash
python examples/03-env-vars/env_example.py
```

---

### [04-secrets](./04-secrets/) - Secret Resolution

Manage sensitive data securely with secret references.

**Topics covered:**
- `REF::` syntax for secret references
- ENV provider (environment variables)
- FILE provider (Docker/Kubernetes secrets)
- Automatic secret redaction
- Security best practices

**Run:**
```bash
python examples/04-secrets/secrets_example.py
```

---

### [05-docker](./05-docker/) - Docker Integration

Complete production-ready Docker integration example.

**Topics covered:**
- Docker Compose multi-container setup
- Docker secrets with FILE provider
- Production deployment
- Kubernetes integration
- Security best practices

**Run:**
```bash
cd examples/05-docker
# Create secret files
mkdir -p secrets
echo "sk_live_abc123" > secrets/api_key.txt
echo "secret_password" > secrets/db_password.txt

# Build and run
docker-compose up
```

---

## Learning Path

### For Beginners

1. Start with **Example 01** (basic) to understand core concepts
2. Move to **Example 02** (YAML) for file-based configuration
3. Try **Example 03** (env-vars) to see override behavior

### For Production Use

1. Review **Example 03** (env-vars) for containerized environments
2. Study **Example 04** (secrets) for secure secret management
3. Implement **Example 05** (Docker) for full production setup

## Common Patterns

### Development Configuration

```python
# Load from file with defaults
config = PrismConfig.from_file("config.dev.yaml")
```

### Production Configuration

```python
import sys
from prism.config import PrismConfig

# Load with all overrides
config = PrismConfig.from_all(
    "/etc/app/config.yaml",
    cli_args=sys.argv[1:],
    resolve_secrets=True
)
```

### Docker/Kubernetes Configuration

```yaml
# config.yaml
app:
  name: my-app
  environment: production
  api_key: REF::FILE::/run/secrets/api_key

database:
  host: postgres
  port: 5432
  name: mydb
  password: REF::FILE::/run/secrets/db_password
```

```python
# app.py
config = PrismConfig.from_all(
    "config.yaml",
    resolve_secrets=True
)
```

## Configuration Precedence

All examples follow this precedence chain:

```
CLI Arguments (highest)
    ↓
Secrets (REF:: resolution)
    ↓
Environment Variables
    ↓
YAML/Config Files
    ↓
Defaults (lowest)
```

## Troubleshooting

### Module Not Found

```bash
# Install in development mode
cd prism-config
pip install -e .
```

### Unicode Encoding Issues (Windows)

If you see Unicode errors when running examples on Windows:

```bash
# Set UTF-8 encoding
set PYTHONIOENCODING=utf-8
python examples/01-basic/basic_example.py
```

Or use PowerShell:
```powershell
$env:PYTHONIOENCODING="utf-8"
python examples/01-basic/basic_example.py
```

### Permission Denied (Docker secrets)

```bash
# Fix file permissions
chmod 600 secrets/*.txt
```

## Next Steps

After completing these examples:

1. Read the main [README.md](../README.md) for comprehensive documentation
2. Check the [API documentation](../docs/api.md) for detailed method references
3. Review [best practices](../docs/best-practices.md) for production deployments
4. Explore the [test suite](../tests/) for more usage examples

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/lukeudell/prism-config/issues)
- **Discussions**: [GitHub Discussions](https://github.com/lukeudell/prism-config/discussions)
- **Documentation**: [Full Documentation](../README.md)

## Contributing

Found a bug in an example? Have an idea for a new example? Please open an issue or submit a pull request!
