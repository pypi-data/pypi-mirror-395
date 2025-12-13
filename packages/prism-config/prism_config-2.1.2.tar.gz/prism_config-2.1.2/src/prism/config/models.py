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

Custom Schemas (v2.0.0+):
    Users can define custom configuration schemas by subclassing BaseConfigSection
    and passing their schema to PrismConfig.from_dict(schema=MySchema).

    Example:
        >>> from prism.config import PrismConfig, BaseConfigSection
        >>>
        >>> class AuthConfig(BaseConfigSection):
        ...     jwt_secret: str
        ...     token_expiry: int = 3600
        >>>
        >>> class MyAppConfig(BaseConfigSection):
        ...     app: AppConfig
        ...     database: DatabaseConfig
        ...     auth: AuthConfig
        >>>
        >>> config = PrismConfig.from_dict(data, schema=MyAppConfig)
        >>> print(config.auth.jwt_secret)
"""

from typing import Any, Dict, Iterator, Optional, TypeVar

from pydantic import BaseModel, Field


# TypeVar for generic schema support (v2.0.0+)
# T is bound to BaseModel to ensure type safety
T = TypeVar("T", bound=BaseModel)


class DynamicConfig:
    """
    Dynamic configuration object with dot-accessible nested attributes.

    This class provides a flexible, schema-less configuration container that allows
    any nested structure to be accessed via dot notation. It's used when loading
    configuration with `strict=False` (flexible mode).

    Features:
    - Dot notation access: `config.auth.jwt.secret`
    - Recursive nesting: Nested dicts become DynamicConfig objects
    - Dict-like access: `config["auth"]["jwt"]["secret"]`
    - Iteration support: `for key in config: ...`
    - Immutable after creation (frozen)

    Example:
        >>> data = {
        ...     "auth": {"jwt": {"secret": "abc123", "expiry": 3600}},
        ...     "rate_limit": {"requests_per_minute": 100}
        ... }
        >>> config = DynamicConfig(data)
        >>> config.auth.jwt.secret
        'abc123'
        >>> config.auth.jwt.expiry
        3600
        >>> config.rate_limit.requests_per_minute
        100

    Note:
        This class is automatically used by PrismConfig when `strict=False`.
        Users typically don't instantiate it directly.
    """

    __slots__ = ("_data", "_frozen")

    def __init__(self, data: Dict[str, Any], frozen: bool = True):
        """
        Create a DynamicConfig from a dictionary.

        Args:
            data: Dictionary of configuration data
            frozen: If True, prevent modifications after creation (default: True)
        """
        # Use object.__setattr__ to bypass our __setattr__ during init
        object.__setattr__(self, "_frozen", False)
        object.__setattr__(self, "_data", {})

        # Convert nested dicts to DynamicConfig recursively
        for key, value in data.items():
            self._data[key] = self._convert_value(value, frozen)

        # Freeze after initialization
        object.__setattr__(self, "_frozen", frozen)

    @staticmethod
    def _convert_value(value: Any, frozen: bool = True) -> Any:
        """Convert nested dicts to DynamicConfig objects."""
        if isinstance(value, dict):
            return DynamicConfig(value, frozen=frozen)
        elif isinstance(value, list):
            return [DynamicConfig._convert_value(item, frozen) for item in value]
        else:
            return value

    def __getattr__(self, name: str) -> Any:
        """Enable dot notation access: config.section.key."""
        if name.startswith("_"):
            raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

        try:
            return self._data[name]
        except KeyError as e:
            raise AttributeError(
                f"'{type(self).__name__}' has no attribute '{name}'. "
                f"Available keys: {list(self._data.keys())}"
            ) from e

    def __setattr__(self, name: str, value: Any) -> None:
        """Prevent modification if frozen."""
        if name.startswith("_"):
            object.__setattr__(self, name, value)
            return

        if getattr(self, "_frozen", False):
            raise AttributeError(
                f"Cannot modify '{name}': DynamicConfig is frozen (immutable)"
            )
        self._data[name] = self._convert_value(value)

    def __getitem__(self, key: str) -> Any:
        """Enable dict-like access: config["section"]["key"]."""
        return self._data[key]

    def __contains__(self, key: str) -> bool:
        """Support 'in' operator: 'auth' in config."""
        return key in self._data

    def __iter__(self) -> Iterator[str]:
        """Enable iteration: for key in config."""
        return iter(self._data)

    def __len__(self) -> int:
        """Return number of top-level keys."""
        return len(self._data)

    def __repr__(self) -> str:
        """String representation."""
        keys = list(self._data.keys())
        if len(keys) > 5:
            keys_str = f"{keys[:5]}... ({len(keys)} total)"
        else:
            keys_str = str(keys)
        return f"DynamicConfig({keys_str})"

    def keys(self) -> Iterator[str]:
        """Return iterator over keys."""
        return iter(self._data.keys())

    def values(self) -> Iterator[Any]:
        """Return iterator over values."""
        return iter(self._data.values())

    def items(self) -> Iterator[tuple]:
        """Return iterator over (key, value) pairs."""
        return iter(self._data.items())

    def get(self, key: str, default: Any = None) -> Any:
        """Get value with optional default."""
        return self._data.get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert back to a plain dictionary.

        Recursively converts all nested DynamicConfig objects to dicts.

        Returns:
            Plain Python dictionary
        """
        result = {}
        for key, value in self._data.items():
            if isinstance(value, DynamicConfig):
                result[key] = value.to_dict()
            elif isinstance(value, list):
                result[key] = [
                    item.to_dict() if isinstance(item, DynamicConfig) else item
                    for item in value
                ]
            else:
                result[key] = value
        return result


class BaseConfigSection(BaseModel):
    """
    Base class for custom configuration sections.

    Provides sensible defaults for configuration sections:
    - frozen=True: Makes the section immutable after creation
    - validate_assignment=True: Validates any attribute changes

    Users should inherit from this class when defining custom config sections.

    Example:
        >>> class AuthConfig(BaseConfigSection):
        ...     jwt_secret: str
        ...     token_expiry: int = 3600
        ...     enable_refresh: bool = True
        >>>
        >>> class RateLimitConfig(BaseConfigSection):
        ...     requests_per_minute: int = 100
        ...     burst_size: int = 20

    Attributes:
        All attributes are defined by the subclass.

    Configuration:
        - frozen=True: Prevents modification after creation
        - validate_assignment=True: Validates changes (if unfrozen)
    """

    model_config = {
        "frozen": True,
        "validate_assignment": True,
    }


class BaseConfigRoot(BaseModel):
    """
    Base class for custom root configuration schemas.

    Provides sensible defaults for root configuration:
    - extra="forbid": Rejects unknown fields (strict mode)
    - validate_assignment=True: Validates any attribute changes
    - frozen=True: Makes config immutable after creation

    For flexible schemas that allow unknown fields, set extra="allow":

    Example (Strict - rejects unknown fields):
        >>> class MyAppConfig(BaseConfigRoot):
        ...     app: AppConfig
        ...     database: DatabaseConfig
        ...     auth: AuthConfig

    Example (Flexible - allows unknown fields):
        >>> class FlexibleConfig(BaseConfigRoot):
        ...     app: AppConfig
        ...     database: DatabaseConfig
        ...
        ...     model_config = {
        ...         "extra": "allow",  # Allow additional sections
        ...         "frozen": True,
        ...         "validate_assignment": True,
        ...     }

    Attributes:
        All attributes are defined by the subclass.

    Configuration:
        - extra="forbid": Rejects unknown fields (override with "allow" for flexible mode)
        - validate_assignment=True: Validates changes
        - frozen=True: Prevents modification after creation
    """

    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
        "frozen": True,
    }


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
