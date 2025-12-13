# Example 04: Secret Resolution

This example demonstrates how to use secret references in your configuration for secure handling of sensitive data like API keys, passwords, and tokens.

## What You'll Learn

- ✅ How to use secret references with `REF::` syntax
- ✅ ENV provider for environment variable secrets
- ✅ FILE provider for file-based secrets (Docker/K8s)
- ✅ Automatic secret redaction in display and export
- ✅ Secure secret handling best practices

## Files

- `config.yaml` - Configuration with secret references
- `secrets_example.py` - Main example script
- `README.md` - This file

## Running the Example

```bash
# From the prism-config root directory
python examples/04-secrets/secrets_example.py
```

## Expected Output

```
🔮 Secret Resolution Example
==================================================

🔐 Setting secrets in environment:
  API_KEY=sk_live_***
  DB_PASSWORD=super_secret_***

📄 Configuration file contains references:
  app:
    name: secrets-example-app
    api_key: REF::ENV::API_KEY

✨ Loading configuration with secret resolution...
  ✅ Secrets resolved successfully!

📋 Configuration values (secrets resolved):
  App Name: secrets-example-app
  API Key: sk_live_ab*** (resolved from ENV)
  DB Password: super_secr*** (resolved from ENV)

🌈 Beautiful Display (secrets automatically redacted):
[Table with secrets shown as [🔒 REDACTED]]

📤 Export with secret redaction:
YAML (secrets redacted):
app:
  api_key: '[REDACTED]'
database:
  password: '[REDACTED]'
```

## Key Concepts

### 1. Secret Reference Syntax

Use the `REF::PROVIDER::KEY` syntax to reference secrets:

```yaml
# config.yaml
app:
  api_key: REF::ENV::API_KEY

database:
  password: REF::ENV::DB_PASSWORD
  ssl_cert: REF::FILE::/run/secrets/db_cert
```

Format: `REF::{PROVIDER}::{KEY_OR_PATH}`

### 2. ENV Provider

Resolves secrets from environment variables:

```yaml
# In config.yaml
database:
  password: REF::ENV::DB_PASSWORD
```

```bash
# Set environment variable
export DB_PASSWORD=my_secret_password
```

```python
# Load config
config = PrismConfig.from_file("config.yaml", resolve_secrets=True)
print(config.database.password)  # "my_secret_password"
```

### 3. FILE Provider

Resolves secrets from files (perfect for Docker/Kubernetes secrets):

```yaml
# In config.yaml
database:
  password: REF::FILE::/run/secrets/db_password
```

```bash
# Create secret file
echo "my_secret_password" > /run/secrets/db_password
```

```python
# Load config
config = PrismConfig.from_file("config.yaml", resolve_secrets=True)
print(config.database.password)  # "my_secret_password" (newlines stripped)
```

### 4. Automatic Secret Redaction

Secrets are automatically redacted in display and export operations:

```python
config = PrismConfig.from_file("config.yaml", resolve_secrets=True)

# Display redacts secrets automatically
config.display()  # Shows [🔒 REDACTED] for passwords

# Export with redaction (default)
yaml_str = config.to_yaml(redact_secrets=True)
# Output: password: '[REDACTED]'

# Export without redaction (use with caution!)
yaml_str = config.to_yaml(redact_secrets=False)
# Output: password: 'actual_password_here'
```

## Production Usage

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    image: my-app:latest
    environment:
      - API_KEY=sk_live_abc123
      - DB_PASSWORD=super_secret
    # Config file uses REF::ENV::API_KEY
```

### Kubernetes Secrets

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  DB_PASSWORD: super_secret_password
---
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  template:
    spec:
      containers:
      - name: app
        image: my-app:latest
        env:
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: DB_PASSWORD
```

### Docker Swarm Secrets

```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    image: my-app:latest
    secrets:
      - db_password
    # Config file uses REF::FILE::/run/secrets/db_password

secrets:
  db_password:
    external: true
```

```bash
# Create secret
echo "my_password" | docker secret create db_password -
```

## Security Best Practices

1. **Never commit secrets to version control**
   ```yaml
   # ✅ Good - use references
   password: REF::ENV::DB_PASSWORD

   # ❌ Bad - hardcoded secret
   password: actual_password_here
   ```

2. **Use secret redaction when sharing configs**
   ```python
   # Share config with team (secrets redacted)
   config.to_yaml_file("config_template.yaml", redact_secrets=True)
   ```

3. **Use FILE provider for containerized apps**
   ```yaml
   # Docker/Kubernetes best practice
   database:
     password: REF::FILE::/run/secrets/db_password
   ```

4. **Rotate secrets regularly**
   - Secret resolution happens at runtime
   - Update environment variables or secret files
   - Restart application to pick up new secrets

## Error Handling

```python
from prism.config import PrismConfig
from prism.config.exceptions import SecretResolutionError

try:
    config = PrismConfig.from_file("config.yaml", resolve_secrets=True)
except SecretResolutionError as e:
    print(f"Failed to resolve secret: {e}")
    # "Failed to resolve secret: ENV::MISSING_KEY
    #   Reason: Environment variable not set
    #   Suggestion: Set environment variable 'MISSING_KEY' or check variable name"
```

## Next Steps

- **Example 05**: Complete Docker and Kubernetes integration example
