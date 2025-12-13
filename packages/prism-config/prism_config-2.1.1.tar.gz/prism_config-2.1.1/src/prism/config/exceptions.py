"""
Custom exceptions for prism-config.

These exceptions provide clear, actionable error messages to help
developers debug configuration issues quickly.

v2.1.1+: Enhanced with error codes, severity levels, timestamps,
and structured metadata for integration with logging systems like prism-view.
"""

from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional


class ErrorCode(str, Enum):
    """
    Standardized error codes for prism-config exceptions.

    These codes enable programmatic error handling and categorization
    in logging/monitoring systems.
    """
    # File errors (1xxx)
    FILE_NOT_FOUND = "PRISM-1001"
    FILE_PARSE_ERROR = "PRISM-1002"
    FILE_READ_ERROR = "PRISM-1003"
    FILE_EMPTY = "PRISM-1004"
    FILE_INVALID_FORMAT = "PRISM-1005"

    # Validation errors (2xxx)
    VALIDATION_TYPE_ERROR = "PRISM-2001"
    VALIDATION_MISSING_FIELD = "PRISM-2002"
    VALIDATION_INVALID_VALUE = "PRISM-2003"
    VALIDATION_SCHEMA_ERROR = "PRISM-2004"

    # Secret errors (3xxx)
    SECRET_NOT_FOUND = "PRISM-3001"
    SECRET_PROVIDER_NOT_FOUND = "PRISM-3002"
    SECRET_INVALID_REFERENCE = "PRISM-3003"
    SECRET_RESOLUTION_FAILED = "PRISM-3004"
    SECRET_PERMISSION_DENIED = "PRISM-3005"

    # Environment errors (4xxx)
    ENV_OVERRIDE_FAILED = "PRISM-4001"
    ENV_INVALID_VALUE = "PRISM-4002"

    # General errors (9xxx)
    UNKNOWN_ERROR = "PRISM-9999"


class Severity(str, Enum):
    """
    Severity levels for errors, compatible with standard logging levels.
    """
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class PrismConfigError(Exception):
    """
    Base exception for all prism-config errors.

    Provides structured error information for logging and monitoring:
    - error_code: Unique identifier for the error type
    - severity: Log level (error, warning, etc.)
    - timestamp: When the error occurred (UTC)
    - context: Additional metadata for debugging
    - suggestion: Human-readable fix suggestion

    Example:
        ```python
        try:
            config = PrismConfig.from_file("missing.yaml")
        except PrismConfigError as e:
            # Structured logging
            logger.error(e.to_dict())

            # Or access individual fields
            print(f"[{e.error_code}] {e.message}")
            print(f"Suggestion: {e.suggestion}")
        ```
    """

    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.UNKNOWN_ERROR,
        severity: Severity = Severity.ERROR,
        suggestion: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        original_error: Optional[Exception] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.severity = severity
        self.suggestion = suggestion
        self.context = context or {}
        self.original_error = original_error
        self.timestamp = datetime.now(timezone.utc)

        # Build the full message
        full_message = f"[{error_code.value}] {message}"
        if suggestion:
            full_message += f"\n  Suggestion: {suggestion}"

        super().__init__(full_message)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert exception to a dictionary for structured logging.

        Returns:
            Dictionary with all error details, suitable for JSON serialization.

        Example:
            ```python
            except PrismConfigError as e:
                import json
                print(json.dumps(e.to_dict(), indent=2, default=str))
            ```
        """
        result = {
            "error_code": self.error_code.value,
            "error_name": self.error_code.name,
            "severity": self.severity.value,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "exception_type": self.__class__.__name__,
        }

        if self.suggestion:
            result["suggestion"] = self.suggestion

        if self.context:
            result["context"] = self.context

        if self.original_error:
            result["original_error"] = {
                "type": type(self.original_error).__name__,
                "message": str(self.original_error),
            }

        return result

    def with_context(self, **kwargs: Any) -> "PrismConfigError":
        """
        Add additional context to the error.

        Args:
            **kwargs: Key-value pairs to add to context

        Returns:
            Self for chaining

        Example:
            ```python
            raise ConfigValidationError(...).with_context(
                correlation_id="abc-123",
                request_id="req-456"
            )
            ```
        """
        self.context.update(kwargs)
        return self


class ConfigFileNotFoundError(PrismConfigError):
    """Raised when a configuration file is not found."""

    def __init__(self, file_path: Path, message: Optional[str] = None):
        self.file_path = file_path

        if message is None:
            message = f"Configuration file not found: {file_path}"

        super().__init__(
            message=message,
            error_code=ErrorCode.FILE_NOT_FOUND,
            severity=Severity.ERROR,
            suggestion="Check if the file exists and the path is correct",
            context={
                "file_path": str(file_path),
                "absolute_path": str(file_path.absolute()),
                "parent_exists": file_path.parent.exists() if file_path.parent else False,
            },
        )


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

        message = f"Failed to parse configuration file: {file_path}"
        if line_number is not None:
            message += f" (line {line_number})"
        if reason:
            message += f" - {reason}"

        # Determine specific error code
        if reason and "empty" in reason.lower():
            error_code = ErrorCode.FILE_EMPTY
        elif reason and "dict" in reason.lower():
            error_code = ErrorCode.FILE_INVALID_FORMAT
        else:
            error_code = ErrorCode.FILE_PARSE_ERROR

        context: Dict[str, Any] = {
            "file_path": str(file_path),
        }
        if line_number is not None:
            context["line_number"] = line_number
        if reason:
            context["reason"] = reason

        super().__init__(
            message=message,
            error_code=error_code,
            severity=Severity.ERROR,
            suggestion="Check YAML/JSON syntax and file encoding",
            context=context,
            original_error=original_error,
        )


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

        message = f"Configuration validation failed for field: {field_path}"

        if expected_type and actual_value is not None:
            actual_type = type(actual_value).__name__
            message += f" (expected {expected_type}, got {actual_type})"

        if reason:
            message += f" - {reason}"

        # Determine specific error code
        if "missing" in (reason or "").lower() or "required" in (reason or "").lower():
            error_code = ErrorCode.VALIDATION_MISSING_FIELD
        elif expected_type:
            error_code = ErrorCode.VALIDATION_TYPE_ERROR
        elif "schema" in (reason or "").lower():
            error_code = ErrorCode.VALIDATION_SCHEMA_ERROR
        else:
            error_code = ErrorCode.VALIDATION_INVALID_VALUE

        context: Dict[str, Any] = {
            "field_path": field_path,
        }
        if expected_type:
            context["expected_type"] = expected_type
        if actual_value is not None:
            context["actual_type"] = type(actual_value).__name__
            # Don't include actual value if it might be sensitive
            if not any(kw in field_path.lower() for kw in ["password", "secret", "key", "token"]):
                context["actual_value"] = repr(actual_value)[:100]  # Truncate for safety

        super().__init__(
            message=message,
            error_code=error_code,
            severity=Severity.ERROR,
            suggestion="Check configuration schema and value types",
            context=context,
            original_error=original_error,
        )


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

        message = f"Failed to resolve secret: {provider}::{key}"
        if reason:
            message += f" - {reason}"

        # Determine suggestion based on provider
        if provider == "ENV":
            suggestion = f"Set environment variable '{key}' or check variable name"
            error_code = ErrorCode.SECRET_NOT_FOUND
        elif provider == "FILE":
            suggestion = f"Check if file exists at path '{key}' and is readable"
            if reason and "permission" in reason.lower():
                error_code = ErrorCode.SECRET_PERMISSION_DENIED
            else:
                error_code = ErrorCode.SECRET_NOT_FOUND
        else:
            suggestion = f"Check provider '{provider}' is registered and configured"
            error_code = ErrorCode.SECRET_RESOLUTION_FAILED

        super().__init__(
            message=message,
            error_code=error_code,
            severity=Severity.ERROR,
            suggestion=suggestion,
            context={
                "provider": provider,
                "key": key,
                "reference": f"REF::{provider}::{key}",
            },
            original_error=original_error,
        )


class SecretProviderNotFoundError(PrismConfigError):
    """Raised when a secret provider is not registered."""

    def __init__(self, provider_name: str, available_providers: Optional[list] = None):
        self.provider_name = provider_name
        self.available_providers = available_providers or []

        message = f"Secret provider not found: {provider_name}"

        super().__init__(
            message=message,
            error_code=ErrorCode.SECRET_PROVIDER_NOT_FOUND,
            severity=Severity.ERROR,
            suggestion="Register the provider or check the REF:: syntax",
            context={
                "provider_name": provider_name,
                "available_providers": self.available_providers,
            },
        )


class InvalidSecretReferenceError(PrismConfigError):
    """Raised when a secret reference has invalid syntax."""

    def __init__(self, reference: str, reason: Optional[str] = None):
        self.reference = reference
        self.reason = reason

        message = f"Invalid secret reference: {reference}"
        if reason:
            message += f" - {reason}"

        super().__init__(
            message=message,
            error_code=ErrorCode.SECRET_INVALID_REFERENCE,
            severity=Severity.ERROR,
            suggestion="Use format REF::PROVIDER::KEY (e.g., REF::ENV::DATABASE_PASSWORD)",
            context={
                "reference": reference,
                "expected_format": "REF::PROVIDER::KEY",
            },
        )


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
            message += f" -> {config_path}"
        if reason:
            message += f" - {reason}"

        # Determine error code
        if reason and "invalid" in reason.lower():
            error_code = ErrorCode.ENV_INVALID_VALUE
        else:
            error_code = ErrorCode.ENV_OVERRIDE_FAILED

        context: Dict[str, Any] = {
            "env_var": env_var,
        }
        if config_path:
            context["config_path"] = config_path

        super().__init__(
            message=message,
            error_code=error_code,
            severity=Severity.WARNING,  # ENV issues are often recoverable
            suggestion="Check environment variable name and value format",
            context=context,
        )
