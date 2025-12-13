# Example 08: Microservice with Multiple Backends (v2.0.0)

This example demonstrates prism-config for a real-world microservice architecture with multiple database connections, cache backends, message queues, and external service clients.

## Features Demonstrated

- Multiple database connections (primary, replica, analytics)
- Multiple cache backends (session, data, rate limit)
- Message queues (RabbitMQ and Kafka)
- External service clients with circuit breakers
- Observability configuration (tracing, metrics, logging)
- Feature flags

## Files

- `config.yaml` - Complete microservice configuration
- `microservice_example.py` - Python code demonstrating the schema

## Prerequisites

```bash
# Install prism-config
cd prism-config
pip install -e .

# Set required environment variables
export INSTANCE_ID=order-service-1
export PRIMARY_DB_PASSWORD=primary_pass
export REPLICA_DB_PASSWORD=replica_pass
export ANALYTICS_DB_PASSWORD=analytics_pass
export SESSION_CACHE_PASSWORD=session_pass
export DATA_CACHE_PASSWORD=data_pass
export RATELIMIT_CACHE_PASSWORD=ratelimit_pass
export RABBITMQ_PASSWORD=rabbitmq_pass
export PAYMENT_API_KEY=pay_key
export INVENTORY_API_KEY=inv_key
export SHIPPING_API_KEY=ship_key
```

## Running the Example

```bash
python examples/08-microservice/microservice_example.py
```

## Configuration Structure

```yaml
app:
  name: order-service
  environment: development

databases:
  primary:
    host: primary-db.internal
    pool_size: 10
  replica:
    host: replica-db.internal
    pool_size: 20
  analytics:
    host: analytics-db.internal
    pool_size: 5

caches:
  session:
    host: session-cache.internal
    ttl: 3600
  data:
    host: data-cache.internal
    ttl: 300
  rate_limit:
    host: ratelimit-cache.internal
    ttl: 60

queues:
  orders:
    backend: rabbitmq
    host: rabbitmq.internal
    exchange: orders.events
  notifications:
    backend: kafka
    brokers:
      - kafka-1.internal:9092
      - kafka-2.internal:9092

services:
  payment:
    base_url: https://payment-api.internal
    circuit_breaker:
      threshold: 5
      timeout: 60

features:
  new_checkout_flow: true
  async_notifications: true
```

## Schema Design Patterns

### Multiple Instances of Same Type

```python
class DatabaseConnection(BaseConfigSection):
    host: str
    port: int = 5432
    pool_size: int = 10

class DatabasesConfig(BaseConfigSection):
    primary: DatabaseConnection
    replica: DatabaseConnection
    analytics: DatabaseConnection
```

### Nested Configuration with Defaults

```python
class CircuitBreakerConfig(BaseConfigSection):
    threshold: int = 5
    timeout: int = 60

class ServiceClient(BaseConfigSection):
    base_url: str
    timeout_seconds: int = 30
    circuit_breaker: CircuitBreakerConfig
```

### Feature Flags

```python
class FeaturesConfig(BaseConfigSection):
    new_checkout_flow: bool = False
    async_notifications: bool = False
```

## Usage Patterns

### Database Connection Pool

```python
from sqlalchemy import create_engine

primary_engine = create_engine(
    f"postgresql://{config.databases.primary.username}:"
    f"{config.databases.primary.password}@"
    f"{config.databases.primary.host}/"
    f"{config.databases.primary.name}",
    pool_size=config.databases.primary.pool_size,
)
```

### Circuit Breaker Integration

```python
from circuitbreaker import circuit

@circuit(
    failure_threshold=config.services.payment.circuit_breaker.threshold,
    recovery_timeout=config.services.payment.circuit_breaker.timeout,
)
def call_payment_service(order_id: str):
    response = httpx.post(
        f"{config.services.payment.base_url}/charge",
        timeout=config.services.payment.timeout_seconds,
    )
```

### Feature Flag Checking

```python
if config.features.new_checkout_flow:
    await process_checkout_v2(order)
else:
    await process_checkout_v1(order)
```

## Benefits

1. **Centralized Configuration** - All backend connections in one place
2. **Type Safety** - IDE autocomplete for all configuration paths
3. **Secret Management** - Passwords and API keys resolved securely
4. **Validation** - Pydantic validates all values at startup
5. **Environment Overrides** - Easy per-environment customization

## Next Steps

- See [09-multi-env](../09-multi-env/) for environment-specific configs
- See [10-flexible](../10-flexible/) for catch-all flexible mode
