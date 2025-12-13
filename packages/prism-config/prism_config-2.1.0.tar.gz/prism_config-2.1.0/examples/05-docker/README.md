# Example 05: Docker Integration

This example demonstrates a complete Dockerized application using prism-config with Docker secrets, environment variables, and multi-container orchestration.

## What You'll Learn

- ✅ Complete Docker integration with prism-config
- ✅ Using Docker secrets with the FILE provider
- ✅ Docker Compose multi-container setup
- ✅ Production-ready configuration management
- ✅ Security best practices for containerized apps

## Files

- `app.py` - Main application entry point
- `config.yaml` - Configuration with secret references
- `Dockerfile` - Container image definition
- `docker-compose.yml` - Multi-container orchestration
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Prerequisites

- Docker installed
- Docker Compose installed

## Running the Example

### Step 1: Create Secret Files

```bash
cd examples/05-docker

# Create secrets directory
mkdir -p secrets

# Create secret files
echo "sk_live_abc123xyz789_super_secret_api_key" > secrets/api_key.txt
echo "super_secret_db_password_456" > secrets/db_password.txt

# Secure the secrets (optional but recommended)
chmod 600 secrets/*.txt
```

### Step 2: Build and Run

```bash
# Build the Docker image
docker-compose build

# Start the services
docker-compose up

# In another terminal, view logs
docker-compose logs -f app
```

### Step 3: Test Configuration Overrides

```bash
# Override environment via CLI args
docker-compose run app python app.py --app.environment=staging

# Override via environment variables
docker-compose run -e APP_APP__ENVIRONMENT=testing app python app.py
```

### Step 4: Cleanup

```bash
docker-compose down -v
```

## Architecture

```
┌─────────────────────────────────────────────┐
│ Docker Compose                              │
│                                             │
│  ┌──────────────┐      ┌────────────────┐  │
│  │ App Container│      │ PostgreSQL     │  │
│  │              │─────▶│ Container      │  │
│  │ - app.py     │      │                │  │
│  │ - config.yaml│      │ Secrets:       │  │
│  │              │      │ - db_password  │  │
│  │ Secrets:     │      └────────────────┘  │
│  │ - api_key    │                           │
│  │ - db_password│                           │
│  └──────────────┘                           │
│                                             │
│  Secrets mounted at: /run/secrets/          │
└─────────────────────────────────────────────┘
```

## Configuration Flow

### 1. Config File (config.yaml)

```yaml
app:
  name: dockerized-app
  environment: production
  api_key: REF::FILE::/run/secrets/api_key

database:
  host: postgres
  port: 5432
  name: production_db
  password: REF::FILE::/run/secrets/db_password
```

### 2. Docker Secrets

Docker Compose mounts secret files at `/run/secrets/`:

```
/run/secrets/
├── api_key       → "sk_live_abc123..."
└── db_password   → "super_secret_..."
```

### 3. prism-config Resolution

```python
config = PrismConfig.from_all(
    "config.yaml",
    cli_args=sys.argv[1:],
    resolve_secrets=True
)

# Secrets are resolved at runtime:
# REF::FILE::/run/secrets/api_key → actual API key value
# REF::FILE::/run/secrets/db_password → actual password value
```

### 4. Precedence Chain

```
CLI Arguments (highest)
    ↓
Secrets (FILE:/run/secrets/*)
    ↓
Environment Variables
    ↓
config.yaml
    ↓
Defaults (lowest)
```

## Production Deployment

### Kubernetes Deployment

For Kubernetes, use Kubernetes Secrets instead of Docker secrets:

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  api_key: sk_live_abc123xyz789
  db_password: super_secret_password

---
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prism-app
spec:
  template:
    spec:
      containers:
      - name: app
        image: prism-config-example:latest
        volumeMounts:
        - name: secrets
          mountPath: /run/secrets
          readOnly: true
        - name: config
          mountPath: /app/config.yaml
          subPath: config.yaml
      volumes:
      - name: secrets
        secret:
          secretName: app-secrets
          items:
          - key: api_key
            path: api_key
          - key: db_password
            path: db_password
      - name: config
        configMap:
          name: app-config
```

### Docker Swarm

```bash
# Create secrets
echo "sk_live_abc123..." | docker secret create api_key -
echo "super_secret..." | docker secret create db_password -

# Deploy stack
docker stack deploy -c docker-compose.yml prism-app
```

## Security Best Practices

### 1. Never Commit Secrets

```bash
# Add to .gitignore
secrets/
*.secret
*.key
.env
```

### 2. Use Secret Scanning

```bash
# Use tools like git-secrets or truffleHog
git secrets --scan
```

### 3. Rotate Secrets Regularly

```bash
# Update secret file
echo "new_password_here" > secrets/db_password.txt

# Restart container to pick up new secret
docker-compose restart app
```

### 4. Least Privilege

```dockerfile
# Run as non-root user
RUN useradd -m -u 1000 appuser
USER appuser
```

### 5. Secret Redaction

```python
# Never log secrets
config.display()  # Automatically redacts secrets

# Share config templates without secrets
config.to_yaml_file("template.yaml", redact_secrets=True)
```

## Troubleshooting

### Secret File Not Found

```
Error: Failed to resolve secret: FILE::/run/secrets/api_key
  Reason: [Errno 2] No such file or directory: '/run/secrets/api_key'
  Suggestion: Check that the secret file exists and the path is correct
```

**Solution**: Ensure secrets are defined in `docker-compose.yml` and secret files exist.

### Permission Denied

```
Error: Failed to resolve secret: FILE::/run/secrets/api_key
  Reason: [Errno 13] Permission denied: '/run/secrets/api_key'
```

**Solution**: Check file permissions and ensure container user has read access.

### Database Connection Fails

```
Error: could not connect to server
```

**Solution**: Ensure:
1. Database service is running (`docker-compose ps`)
2. Host is set to service name (`postgres`, not `localhost`)
3. Network is configured correctly

## Environment-Specific Configs

### Development

```bash
# Use environment variables instead of secrets
docker-compose run -e APP_APP__API_KEY=dev_key app python app.py
```

### Staging

```yaml
# docker-compose.staging.yml
services:
  app:
    environment:
      - APP_APP__ENVIRONMENT=staging
      - APP_DATABASE__HOST=staging-db.example.com
```

### Production

```bash
# Use external secrets
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

## Next Steps

- Deploy to Kubernetes
- Integrate with secret management systems (Vault, AWS Secrets Manager)
- Add health checks and monitoring
- Set up CI/CD pipeline
