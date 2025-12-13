"""
🔮 Prism Config

Typed, tiered configuration with secret resolution and PQC support.

Custom Schemas (v2.0.0+):
    prism-config now supports custom configuration schemas. Define your own
    schema using BaseConfigSection and BaseConfigRoot:

    >>> from prism.config import PrismConfig, BaseConfigSection, BaseConfigRoot
    >>>
    >>> class AuthConfig(BaseConfigSection):
    ...     jwt_secret: str
    ...     token_expiry: int = 3600
    >>>
    >>> class MyAppConfig(BaseConfigRoot):
    ...     app: AppConfig
    ...     database: DatabaseConfig
    ...     auth: AuthConfig
    >>>
    >>> config = PrismConfig.from_dict(data, schema=MyAppConfig)
    >>> print(config.auth.jwt_secret)  # Full type safety!
"""

__version__ = "2.1.1"
__icon__ = "🔮"
__requires__ = []

from .display import (
    clear_registered_emojis,
    get_registered_emojis,
    register_emoji,
    unregister_emoji,
)
from .exceptions import (
    ConfigFileNotFoundError,
    ConfigParseError,
    ConfigValidationError,
    EnvironmentVariableError,
    ErrorCode,
    InvalidSecretReferenceError,
    PrismConfigError,
    SecretProviderNotFoundError,
    SecretResolutionError,
    Severity,
)
from .loader import PrismConfig
from .models import (
    AppConfig,
    BaseConfigRoot,
    BaseConfigSection,
    ConfigRoot,
    DatabaseConfig,
    DynamicConfig,
)

__all__ = [
    # Core
    "PrismConfig",
    # Base classes for custom schemas (v2.0.0+)
    "BaseConfigSection",
    "BaseConfigRoot",
    # Flexible mode (v2.0.0+)
    "DynamicConfig",
    # Emoji registration (v2.0.0+)
    "register_emoji",
    "unregister_emoji",
    "get_registered_emojis",
    "clear_registered_emojis",
    # Built-in models
    "AppConfig",
    "DatabaseConfig",
    "ConfigRoot",
    # Exceptions
    "PrismConfigError",
    "ConfigFileNotFoundError",
    "ConfigParseError",
    "ConfigValidationError",
    "SecretResolutionError",
    "SecretProviderNotFoundError",
    "InvalidSecretReferenceError",
    "EnvironmentVariableError",
    # Error metadata (v2.1.1+)
    "ErrorCode",
    "Severity",
]
