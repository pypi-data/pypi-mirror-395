"""
Pydantic models for configuration structure.

These models define the schema, validation rules, and type information for
prism-config. All models are frozen (immutable) for safety and predictability.

The configuration structure is:
    ConfigRoot
    ├── app: AppConfig
    └── database: DatabaseConfig

You typically don't instantiate these models directly - use PrismConfig.from_dict()
or PrismConfig.from_file() instead.
"""

from typing import Optional

from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    """
    Application-level configuration.

    Contains application metadata and settings like name, environment, and API keys.
    This model is frozen (immutable) to prevent accidental modifications at runtime.

    Attributes:
        name (str): Application name (required)
        environment (str): Environment name like 'dev', 'staging', 'prod' (required)
        api_key (Optional[str]): Optional API key for external services

    Examples:
        >>> # Typically created via PrismConfig.from_dict()
        >>> config = PrismConfig.from_dict({
        ...     "app": {
        ...         "name": "my-service",
        ...         "environment": "production",
        ...         "api_key": "sk_live_..."
        ...     },
        ...     "database": {...}
        ... })
        >>> print(config.app.name)
        'my-service'
        >>> print(config.app.environment)
        'production'

        >>> # Immutability prevents accidental changes
        >>> config.app.name = "new-name"  # Raises ValidationError
    """

    model_config = {"frozen": True}  # Make immutable

    name: str = Field(..., description="Application name")
    environment: str = Field(..., description="Environment (dev, staging, prod)")
    api_key: Optional[str] = Field(default=None, description="Optional API key")


class DatabaseConfig(BaseModel):
    """
    Database connection configuration.

    Contains all settings needed to connect to a database, including host, port,
    database name, and optional password. This model is frozen (immutable) to
    prevent accidental modifications at runtime.

    Attributes:
        host (str): Database hostname or IP address (default: "localhost")
        port (int): Database port number (default: 5432 for PostgreSQL)
        name (str): Database name (required)
        password (Optional[str]): Database password, supports secret references

    Examples:
        >>> # Basic database config
        >>> config = PrismConfig.from_dict({
        ...     "app": {...},
        ...     "database": {
        ...         "host": "db.example.com",
        ...         "port": 3306,
        ...         "name": "production_db",
        ...         "password": "secret123"
        ...     }
        ... })
        >>> print(config.database.host)
        'db.example.com'
        >>> print(config.database.port)
        3306

        >>> # With secret reference (recommended for production)
        >>> config = PrismConfig.from_dict({
        ...     "app": {...},
        ...     "database": {
        ...         "host": "db.example.com",
        ...         "port": 5432,
        ...         "name": "mydb",
        ...         "password": "REF::ENV::DB_PASSWORD"
        ...     }
        ... }, resolve_secrets=True)

        >>> # Default values for development
        >>> config = PrismConfig.from_dict({
        ...     "app": {...},
        ...     "database": {
        ...         "name": "dev_db"  # host and port use defaults
        ...     }
        ... })
        >>> print(config.database.host)
        'localhost'
        >>> print(config.database.port)
        5432
    """

    model_config = {"frozen": True}  # Make immutable

    host: str = Field(default="localhost", description="Database host")
    port: int = Field(default=5432, description="Database port")
    name: str = Field(..., description="Database name")
    password: Optional[str] = Field(default=None, description="Optional database password")


class ConfigRoot(BaseModel):
    """
    Root configuration model.

    This is the top-level structure that holds all configuration sections.
    It enforces strict validation: unknown fields are rejected, all assignments
    are validated, and the config is frozen (immutable) after creation.

    Attributes:
        app (AppConfig): Application configuration section
        database (DatabaseConfig): Database configuration section

    Configuration:
        - extra="forbid": Rejects unknown fields to catch typos and mistakes
        - validate_assignment=True: Validates any attribute changes
        - frozen=True: Makes config immutable after creation

    Examples:
        >>> # Typically created via PrismConfig.from_dict()
        >>> config = PrismConfig.from_dict({
        ...     "app": {
        ...         "name": "my-app",
        ...         "environment": "production"
        ...     },
        ...     "database": {
        ...         "host": "db.example.com",
        ...         "port": 5432,
        ...         "name": "mydb"
        ...     }
        ... })
        >>> type(config._config)  # Internal ConfigRoot instance
        <class 'prism.config.models.ConfigRoot'>

        >>> # Unknown fields are rejected
        >>> PrismConfig.from_dict({
        ...     "app": {...},
        ...     "database": {...},
        ...     "cache": {...}  # ERROR: 'cache' is not a valid field
        ... })
        Traceback (most recent call last):
        ...
        ConfigValidationError: Extra inputs are not permitted

    Note:
        You typically don't instantiate ConfigRoot directly. Use the PrismConfig
        factory methods instead: from_dict(), from_file(), or from_all().
    """

    app: AppConfig
    database: DatabaseConfig

    model_config = {
        "extra": "forbid",  # Fail on unknown fields
        "validate_assignment": True,  # Validate on attribute changes
        "frozen": True,  # Make immutable
    }
