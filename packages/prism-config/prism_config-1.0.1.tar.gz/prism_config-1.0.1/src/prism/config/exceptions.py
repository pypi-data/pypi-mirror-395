"""
Custom exceptions for prism-config.

These exceptions provide clear, actionable error messages to help
developers debug configuration issues quickly.
"""

from pathlib import Path
from typing import Any, Optional


class PrismConfigError(Exception):
    """Base exception for all prism-config errors."""
    pass


class ConfigFileNotFoundError(PrismConfigError):
    """Raised when a configuration file is not found."""

    def __init__(self, file_path: Path, message: Optional[str] = None):
        self.file_path = file_path
        if message is None:
            message = (
                f"Configuration file not found: {file_path}\n"
                f"  Searched at: {file_path.absolute()}\n"
                f"  Suggestion: Check if the file exists and the path is correct"
            )
        super().__init__(message)


class ConfigParseError(PrismConfigError):
    """Raised when configuration file parsing fails."""

    def __init__(
        self,
        file_path: Path,
        line_number: Optional[int] = None,
        reason: Optional[str] = None,
        original_error: Optional[Exception] = None
    ):
        self.file_path = file_path
        self.line_number = line_number
        self.reason = reason
        self.original_error = original_error

        message = f"Failed to parse configuration file: {file_path}"
        if line_number is not None:
            message += f"\n  Line {line_number}"
        if reason:
            message += f"\n  Reason: {reason}"
        if original_error:
            message += f"\n  Error: {original_error}"
        message += "\n  Suggestion: Check YAML/JSON syntax and file encoding"

        super().__init__(message)


class ConfigValidationError(PrismConfigError):
    """Raised when configuration validation fails."""

    def __init__(
        self,
        field_path: str,
        expected_type: Optional[str] = None,
        actual_value: Optional[Any] = None,
        reason: Optional[str] = None,
        original_error: Optional[Exception] = None
    ):
        self.field_path = field_path
        self.expected_type = expected_type
        self.actual_value = actual_value
        self.reason = reason
        self.original_error = original_error

        message = f"Configuration validation failed for field: {field_path}"

        if expected_type and actual_value is not None:
            actual_type = type(actual_value).__name__
            message += f"\n  Expected type: {expected_type}"
            message += f"\n  Actual type: {actual_type}"
            message += f"\n  Actual value: {repr(actual_value)}"

        if reason:
            message += f"\n  Reason: {reason}"

        if original_error:
            message += f"\n  Error: {original_error}"

        message += "\n  Suggestion: Check configuration schema and value types"

        super().__init__(message)


class SecretResolutionError(PrismConfigError):
    """Raised when secret resolution fails."""

    def __init__(
        self,
        provider: str,
        key: str,
        reason: Optional[str] = None,
        original_error: Optional[Exception] = None
    ):
        self.provider = provider
        self.key = key
        self.reason = reason
        self.original_error = original_error

        message = f"Failed to resolve secret: {provider}::{key}"

        if reason:
            message += f"\n  Reason: {reason}"

        if original_error:
            message += f"\n  Error: {original_error}"

        if provider == "ENV":
            message += f"\n  Suggestion: Set environment variable '{key}' or check variable name"
        elif provider == "FILE":
            message += f"\n  Suggestion: Check if file exists at path '{key}' and is readable"
        else:
            message += f"\n  Suggestion: Check provider '{provider}' is registered and configured"

        super().__init__(message)


class SecretProviderNotFoundError(PrismConfigError):
    """Raised when a secret provider is not registered."""

    def __init__(self, provider_name: str, available_providers: Optional[list] = None):
        self.provider_name = provider_name
        self.available_providers = available_providers

        message = f"Secret provider not found: {provider_name}"

        if available_providers:
            message += f"\n  Available providers: {', '.join(available_providers)}"

        message += "\n  Suggestion: Register the provider or check the REF:: syntax"

        super().__init__(message)


class InvalidSecretReferenceError(PrismConfigError):
    """Raised when a secret reference has invalid syntax."""

    def __init__(self, reference: str, reason: Optional[str] = None):
        self.reference = reference
        self.reason = reason

        message = f"Invalid secret reference: {reference}"

        if reason:
            message += f"\n  Reason: {reason}"

        message += "\n  Expected format: REF::PROVIDER::KEY"
        message += "\n  Example: REF::ENV::DATABASE_PASSWORD"

        super().__init__(message)


class EnvironmentVariableError(PrismConfigError):
    """Raised when environment variable override fails."""

    def __init__(
        self,
        env_var: str,
        config_path: Optional[str] = None,
        reason: Optional[str] = None
    ):
        self.env_var = env_var
        self.config_path = config_path
        self.reason = reason

        message = f"Failed to apply environment variable: {env_var}"

        if config_path:
            message += f"\n  Target config path: {config_path}"

        if reason:
            message += f"\n  Reason: {reason}"

        message += "\n  Suggestion: Check environment variable name and value format"

        super().__init__(message)
