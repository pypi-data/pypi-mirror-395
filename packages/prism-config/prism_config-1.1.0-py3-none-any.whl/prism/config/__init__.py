"""
🔮 Prism Config

Typed, tiered configuration with secret resolution and PQC support.
"""

__version__ = "0.1.0"
__icon__ = "🔮"
__requires__ = []

from .exceptions import (
    ConfigFileNotFoundError,
    ConfigParseError,
    ConfigValidationError,
    EnvironmentVariableError,
    InvalidSecretReferenceError,
    PrismConfigError,
    SecretProviderNotFoundError,
    SecretResolutionError,
)
from .loader import PrismConfig

__all__ = [
    "PrismConfig",
    "PrismConfigError",
    "ConfigFileNotFoundError",
    "ConfigParseError",
    "ConfigValidationError",
    "SecretResolutionError",
    "SecretProviderNotFoundError",
    "InvalidSecretReferenceError",
    "EnvironmentVariableError",
]
