"""
Example 08: Microservice with Multiple Backends (v2.0.0)

This example demonstrates prism-config for a microservice architecture
with multiple database connections, cache backends, message queues,
and external service clients.

Key v2.0.0 features demonstrated:
- Multiple instances of similar configurations (databases, caches)
- Nested service configurations with circuit breaker settings
- Feature flags section
- Observability configuration
- Complex typed schemas

Run this example:
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

    python examples/08-microservice/microservice_example.py
"""

import sys
from pathlib import Path
from typing import List, Optional

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from prism.config import (
    BaseConfigSection,
    BaseConfigRoot,
    PrismConfig,
    register_emoji,
)


# =============================================================================
# Database Configuration Schemas
# =============================================================================


class DatabaseConnection(BaseConfigSection):
    """Single database connection configuration."""

    host: str
    port: int = 5432
    name: str
    username: str
    password: str
    pool_size: int = 10
    max_overflow: int = 20


class DatabasesConfig(BaseConfigSection):
    """Multiple database connections."""

    primary: DatabaseConnection
    replica: DatabaseConnection
    analytics: DatabaseConnection


# =============================================================================
# Cache Configuration Schemas
# =============================================================================


class CacheConnection(BaseConfigSection):
    """Single cache connection configuration."""

    backend: str = "redis"
    host: str
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    ttl: int = 300


class CachesConfig(BaseConfigSection):
    """Multiple cache backends."""

    session: CacheConnection
    data: CacheConnection
    rate_limit: CacheConnection


# =============================================================================
# Message Queue Schemas
# =============================================================================


class RabbitMQQueue(BaseConfigSection):
    """RabbitMQ queue configuration."""

    backend: str = "rabbitmq"
    host: str
    port: int = 5672
    vhost: str = "/"
    username: str
    password: str
    exchange: str
    routing_key: str


class KafkaQueue(BaseConfigSection):
    """Kafka queue configuration."""

    backend: str = "kafka"
    brokers: List[str]
    topic: str
    consumer_group: str


class QueuesConfig(BaseConfigSection):
    """Message queue configuration."""

    orders: RabbitMQQueue
    notifications: KafkaQueue


# =============================================================================
# External Service Schemas
# =============================================================================


class CircuitBreakerConfig(BaseConfigSection):
    """Circuit breaker settings."""

    threshold: int = 5
    timeout: int = 60


class ServiceClient(BaseConfigSection):
    """External service client configuration."""

    base_url: str
    api_key: str
    timeout_seconds: int = 30
    retry_count: int = 3
    circuit_breaker: CircuitBreakerConfig


class ServicesConfig(BaseConfigSection):
    """External service clients."""

    payment: ServiceClient
    inventory: ServiceClient
    shipping: ServiceClient


# =============================================================================
# Observability Schemas
# =============================================================================


class TracingConfig(BaseConfigSection):
    """Distributed tracing configuration."""

    enabled: bool = True
    exporter: str = "jaeger"
    endpoint: str
    sample_rate: float = 0.1


class MetricsConfig(BaseConfigSection):
    """Metrics configuration."""

    enabled: bool = True
    exporter: str = "prometheus"
    endpoint: str = "/metrics"
    port: int = 9090


class LoggingConfig(BaseConfigSection):
    """Logging configuration."""

    level: str = "INFO"
    format: str = "json"
    output: str = "stdout"


class ObservabilityConfig(BaseConfigSection):
    """Observability configuration."""

    tracing: TracingConfig
    metrics: MetricsConfig
    logging: LoggingConfig


# =============================================================================
# Feature Flags Schema
# =============================================================================


class FeaturesConfig(BaseConfigSection):
    """Feature flags configuration."""

    new_checkout_flow: bool = False
    async_notifications: bool = False
    inventory_v2: bool = False
    premium_shipping: bool = False


# =============================================================================
# App Configuration Schema
# =============================================================================


class AppConfig(BaseConfigSection):
    """Application metadata."""

    name: str
    environment: str
    version: str = "1.0.0"
    instance_id: Optional[str] = None


# =============================================================================
# Complete Microservice Configuration
# =============================================================================


class MicroserviceConfig(BaseConfigRoot):
    """
    Complete microservice configuration.

    Demonstrates a real-world microservice with:
    - Multiple database connections (primary, replica, analytics)
    - Multiple cache backends (session, data, rate limit)
    - Message queues (RabbitMQ, Kafka)
    - External service clients with circuit breakers
    - Observability (tracing, metrics, logging)
    - Feature flags
    """

    app: AppConfig
    databases: DatabasesConfig
    caches: CachesConfig
    queues: QueuesConfig
    services: ServicesConfig
    observability: ObservabilityConfig
    features: FeaturesConfig


# =============================================================================
# Main Example
# =============================================================================


def main():
    """Demonstrate microservice configuration with multiple backends."""

    print("=" * 70)
    print("Microservice Configuration Example (prism-config v2.0.0)")
    print("=" * 70)
    print()

    # -------------------------------------------------------------------------
    # Step 1: Register microservice-specific emojis
    # -------------------------------------------------------------------------
    print("Step 1: Registering microservice-specific emojis...")
    register_emoji("databases", "🗄️")
    register_emoji("caches", "⚡")
    register_emoji("queues", "📨")
    register_emoji("services", "🔗")
    register_emoji("observability", "📊")
    register_emoji("features", "🚩")
    register_emoji("circuit_breaker", "🔌")
    print("  Registered custom emojis for microservice sections")
    print()

    # -------------------------------------------------------------------------
    # Step 2: Load configuration
    # -------------------------------------------------------------------------
    print("Step 2: Loading microservice configuration...")
    config_file = Path(__file__).parent / "config.yaml"

    config = PrismConfig.from_file(
        config_file,
        schema=MicroserviceConfig,
        resolve_secrets=True,
    )

    print(f"  Service: {config.app.name} v{config.app.version}")
    print(f"  Environment: {config.app.environment}")
    print()

    # -------------------------------------------------------------------------
    # Step 3: Access multiple database connections
    # -------------------------------------------------------------------------
    print("Step 3: Database connections...")
    print()

    print("  🗄️ Primary Database (writes):")
    print(f"     Host: {config.databases.primary.host}")
    print(f"     Pool Size: {config.databases.primary.pool_size}")
    print()

    print("  🗄️ Replica Database (reads):")
    print(f"     Host: {config.databases.replica.host}")
    print(f"     Pool Size: {config.databases.replica.pool_size}")
    print()

    print("  🗄️ Analytics Database:")
    print(f"     Host: {config.databases.analytics.host}")
    print(f"     Pool Size: {config.databases.analytics.pool_size}")
    print()

    # -------------------------------------------------------------------------
    # Step 4: Access cache backends
    # -------------------------------------------------------------------------
    print("Step 4: Cache backends...")
    print()

    print("  ⚡ Session Cache:")
    print(f"     Host: {config.caches.session.host}")
    print(f"     TTL: {config.caches.session.ttl}s")
    print()

    print("  ⚡ Data Cache:")
    print(f"     Host: {config.caches.data.host}")
    print(f"     TTL: {config.caches.data.ttl}s")
    print()

    print("  ⚡ Rate Limit Cache:")
    print(f"     Host: {config.caches.rate_limit.host}")
    print(f"     TTL: {config.caches.rate_limit.ttl}s")
    print()

    # -------------------------------------------------------------------------
    # Step 5: Access message queues
    # -------------------------------------------------------------------------
    print("Step 5: Message queues...")
    print()

    print("  📨 Orders Queue (RabbitMQ):")
    print(f"     Host: {config.queues.orders.host}")
    print(f"     Exchange: {config.queues.orders.exchange}")
    print()

    print("  📨 Notifications Queue (Kafka):")
    print(f"     Brokers: {', '.join(config.queues.notifications.brokers)}")
    print(f"     Topic: {config.queues.notifications.topic}")
    print()

    # -------------------------------------------------------------------------
    # Step 6: Access external service clients
    # -------------------------------------------------------------------------
    print("Step 6: External service clients...")
    print()

    for name, service in [
        ("Payment", config.services.payment),
        ("Inventory", config.services.inventory),
        ("Shipping", config.services.shipping),
    ]:
        print(f"  🔗 {name} Service:")
        print(f"     URL: {service.base_url}")
        print(f"     Timeout: {service.timeout_seconds}s")
        print(f"     Retries: {service.retry_count}")
        print(f"     Circuit Breaker: threshold={service.circuit_breaker.threshold}")
        print()

    # -------------------------------------------------------------------------
    # Step 7: Access observability configuration
    # -------------------------------------------------------------------------
    print("Step 7: Observability configuration...")
    print()

    print("  📊 Tracing:")
    print(f"     Exporter: {config.observability.tracing.exporter}")
    print(f"     Sample Rate: {config.observability.tracing.sample_rate}")
    print()

    print("  📊 Metrics:")
    print(f"     Exporter: {config.observability.metrics.exporter}")
    print(f"     Endpoint: {config.observability.metrics.endpoint}")
    print()

    # -------------------------------------------------------------------------
    # Step 8: Access feature flags
    # -------------------------------------------------------------------------
    print("Step 8: Feature flags...")
    print()

    print("  🚩 Feature Flags:")
    print(f"     new_checkout_flow: {config.features.new_checkout_flow}")
    print(f"     async_notifications: {config.features.async_notifications}")
    print(f"     inventory_v2: {config.features.inventory_v2}")
    print(f"     premium_shipping: {config.features.premium_shipping}")
    print()

    # -------------------------------------------------------------------------
    # Step 9: Display configuration
    # -------------------------------------------------------------------------
    print("Step 9: Full configuration display...")
    print()
    config.display()
    print()

    # -------------------------------------------------------------------------
    # Step 10: Usage example
    # -------------------------------------------------------------------------
    print("Step 10: Usage in microservice code:")
    print()
    print("""
    from sqlalchemy import create_engine
    from redis import Redis

    # Create database engines
    primary_engine = create_engine(
        f"postgresql://{config.databases.primary.username}:"
        f"{config.databases.primary.password}@"
        f"{config.databases.primary.host}:"
        f"{config.databases.primary.port}/"
        f"{config.databases.primary.name}",
        pool_size=config.databases.primary.pool_size,
        max_overflow=config.databases.primary.max_overflow,
    )

    # Create cache clients
    session_cache = Redis(
        host=config.caches.session.host,
        port=config.caches.session.port,
        db=config.caches.session.db,
        password=config.caches.session.password,
    )

    # Create service clients with circuit breakers
    from circuitbreaker import circuit

    @circuit(
        failure_threshold=config.services.payment.circuit_breaker.threshold,
        recovery_timeout=config.services.payment.circuit_breaker.timeout,
    )
    def call_payment_service(order_id: str):
        ...

    # Check feature flags
    if config.features.new_checkout_flow:
        use_new_checkout()
    else:
        use_legacy_checkout()
    """)

    print("=" * 70)
    print("Example complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
