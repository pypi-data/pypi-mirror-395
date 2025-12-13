"""
Configuration loader - the core of prism-config.

Handles tiered loading, secret resolution, and validation.

Custom Schemas (v2.0.0+):
    PrismConfig now supports custom schemas via the `schema` parameter:

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
    >>> print(config.auth.jwt_secret)  # Type-safe access!
"""

import os
import re
from pathlib import Path
from typing import Any, Dict, Generic, List, Literal, Optional, Type, Union, overload

import yaml
from pydantic import BaseModel

from .exceptions import (
    ConfigFileNotFoundError,
    ConfigParseError,
    ConfigValidationError,
    InvalidSecretReferenceError,
    SecretProviderNotFoundError,
    SecretResolutionError,
)
from .models import ConfigRoot, DynamicConfig, T
from .providers import get_provider


class PrismConfig(Generic[T]):
    """
    Main configuration class for prism-config.

    PrismConfig provides a type-safe, validated configuration system with support for:
    - Multiple loading methods (dict, YAML files)
    - Environment variable overrides
    - CLI argument overrides
    - Secret resolution (ENV and FILE providers)
    - Beautiful terminal output with the Neon Dump
    - Config freezing, serialization, and diffing
    - Custom schemas for flexible configuration structures (v2.0.0+)

    The configuration follows a precedence chain:
        CLI args > Secrets > Environment variables > File/Dict values

    Basic Usage:
        >>> # Load from dict (uses default ConfigRoot schema)
        >>> config = PrismConfig.from_dict({
        ...     "app": {"name": "my-app", "environment": "dev"},
        ...     "database": {"host": "localhost", "port": 5432, "name": "mydb"}
        ... })
        >>> print(config.app.name)  # "my-app"
        >>> print(config.database.port)  # 5432

        >>> # Load from YAML file
        >>> config = PrismConfig.from_file("config.yaml")

        >>> # Load with environment variable overrides
        >>> # Set APP_DATABASE__PORT=3306
        >>> config = PrismConfig.from_file("config.yaml", apply_env=True)

        >>> # Load with all overrides (recommended for production)
        >>> import sys
        >>> config = PrismConfig.from_all(
        ...     "config.yaml",
        ...     cli_args=sys.argv[1:],
        ...     resolve_secrets=True
        ... )

        >>> # Beautiful terminal output
        >>> config.display()  # Prints colorful table

    Custom Schemas (v2.0.0+):
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

    Attributes:
        app: Application configuration section (AppConfig) - when using default schema
        database: Database configuration section (DatabaseConfig) - when using default schema

    See Also:
        - from_dict(): Load from Python dictionary
        - from_file(): Load from YAML file
        - from_all(): Convenience method with all overrides
        - dump(): Get formatted configuration table
        - display(): Print configuration with banner
        - BaseConfigSection: Base class for custom config sections
        - BaseConfigRoot: Base class for custom root schemas
    """

    def __init__(self, config_root: T):
        self._config: T = config_root

    def __getattr__(self, name: str) -> Any:
        """
        Dynamic attribute access for custom schema fields.

        This allows accessing any field defined in the schema via dot notation.
        For custom schemas, this provides seamless access to all sections.
        For flexible mode (DynamicConfig), provides dot notation access to all nested data.

        Args:
            name: Attribute name to access

        Returns:
            The value of the attribute from the underlying config

        Raises:
            AttributeError: If the attribute doesn't exist in the config

        Example:
            >>> config = PrismConfig.from_dict(data, schema=MySchema)
            >>> config.custom_section.some_field  # Works via __getattr__

            >>> config = PrismConfig.from_dict(data, strict=False)
            >>> config.any_section.nested.value  # Works via __getattr__
        """
        # Avoid infinite recursion for special attributes
        if name.startswith("_"):
            raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

        # Try to get from the underlying config
        try:
            return getattr(self._config, name)
        except AttributeError as e:
            # For DynamicConfig, the error message is already helpful
            if isinstance(self._config, DynamicConfig):
                raise

            # Access model_fields from the class, not the instance (Pydantic v2.11+)
            model_class = type(self._config)
            raise AttributeError(
                f"'{type(self).__name__}' has no attribute '{name}'. "
                f"Available sections: {list(model_class.model_fields.keys())}"
            ) from e

    @overload
    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
        apply_env: bool = False,
        env_prefix: str = "APP_",
        cli_args: Optional[List[str]] = None,
        resolve_secrets: bool = False,
        schema: None = None,
        strict: bool = True,
    ) -> "PrismConfig[ConfigRoot]": ...

    @overload
    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
        apply_env: bool = False,
        env_prefix: str = "APP_",
        cli_args: Optional[List[str]] = None,
        resolve_secrets: bool = False,
        schema: Type[T] = ...,
        strict: bool = True,
    ) -> "PrismConfig[T]": ...

    @overload
    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
        apply_env: bool = False,
        env_prefix: str = "APP_",
        cli_args: Optional[List[str]] = None,
        resolve_secrets: bool = False,
        schema: None = None,
        *,
        strict: "Literal[False]",
    ) -> "PrismConfig[DynamicConfig]": ...

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
        apply_env: bool = False,
        env_prefix: str = "APP_",
        cli_args: Optional[List[str]] = None,
        resolve_secrets: bool = False,
        schema: Optional[Type[T]] = None,
        strict: bool = True,
    ) -> "PrismConfig[T]":
        """
        Load configuration from a Python dictionary.

        This method validates the configuration data using Pydantic models and
        optionally applies environment variable overrides, CLI argument overrides,
        and secret resolution.

        Args:
            data: Configuration as nested dict matching your schema structure
            apply_env: Whether to apply environment variable overrides (default: False)
            env_prefix: Prefix for environment variables (default: "APP_")
            cli_args: Optional list of CLI arguments to override config (default: None)
            resolve_secrets: Whether to resolve REF:: secret references (default: False)
            schema: Custom Pydantic model class for validation (default: ConfigRoot).
                    Use BaseConfigSection or BaseConfigRoot subclasses for custom schemas.
                    Ignored when strict=False.
            strict: Whether to validate against a schema (default: True).
                    Set to False for flexible mode - accepts any structure without validation.

        Returns:
            PrismConfig[T]: Validated and type-safe configuration instance
            PrismConfig[DynamicConfig]: When strict=False, dynamic config with dot-access

        Raises:
            ConfigValidationError: If validation fails (missing fields, type errors).
                Only raised in strict mode.
            SecretResolutionError: If secret resolution fails
            EnvironmentVariableError: If env var override fails

        Precedence order (highest to lowest):
            CLI args > Secrets > Environment variables > Dict values

        Examples:
            >>> # Basic usage (default schema)
            >>> config = PrismConfig.from_dict({
            ...     "app": {
            ...         "name": "my-app",
            ...         "environment": "dev"
            ...     },
            ...     "database": {
            ...         "host": "localhost",
            ...         "port": 5432,
            ...         "name": "mydb"
            ...     }
            ... })
            >>> print(config.app.name)
            'my-app'

            >>> # Flexible mode - no schema required (v2.0.0+)
            >>> config = PrismConfig.from_dict({
            ...     "auth": {"jwt": {"secret": "abc123", "expiry": 3600}},
            ...     "rate_limit": {"requests_per_minute": 100}
            ... }, strict=False)
            >>> print(config.auth.jwt.secret)  # Dot notation access!
            'abc123'
            >>> print(config.rate_limit.requests_per_minute)
            100

            >>> # With custom schema (v2.0.0+)
            >>> from prism.config import BaseConfigSection, BaseConfigRoot
            >>>
            >>> class AuthConfig(BaseConfigSection):
            ...     jwt_secret: str
            ...     token_expiry: int = 3600
            >>>
            >>> class MyConfig(BaseConfigRoot):
            ...     app: AppConfig
            ...     database: DatabaseConfig
            ...     auth: AuthConfig
            >>>
            >>> config = PrismConfig.from_dict(data, schema=MyConfig)
            >>> print(config.auth.jwt_secret)  # Full type safety!

            >>> # With environment variable overrides
            >>> import os
            >>> os.environ["APP_DATABASE__PORT"] = "3306"
            >>> config = PrismConfig.from_dict(data, apply_env=True)
            >>> print(config.database.port)
            3306

            >>> # With CLI argument overrides
            >>> config = PrismConfig.from_dict(
            ...     data,
            ...     cli_args=["--database.host=prod.db.com"]
            ... )
            >>> print(config.database.host)
            'prod.db.com'

            >>> # With secret resolution
            >>> config_with_secrets = {
            ...     "app": {"name": "my-app", "environment": "prod"},
            ...     "database": {
            ...         "host": "prod.db.com",
            ...         "port": 5432,
            ...         "name": "mydb",
            ...         "password": "REF::ENV::DB_PASSWORD"
            ...     }
            ... }
            >>> config = PrismConfig.from_dict(config_with_secrets, resolve_secrets=True)

        See Also:
            - from_file(): Load from YAML file instead of dict
            - from_all(): Convenience method with all overrides enabled
            - BaseConfigSection: Base class for custom config sections
            - BaseConfigRoot: Base class for custom root schemas
            - DynamicConfig: Dynamic config class used in flexible mode
        """
        # Apply environment variable overrides if requested
        if apply_env:
            data = cls._apply_env_overrides(data, env_prefix)

        # Apply CLI argument overrides if provided
        if cli_args:
            data = cls._apply_cli_overrides(data, cli_args)

        # Resolve secrets if requested (after env and before validation)
        if resolve_secrets:
            data = cls._resolve_secrets(data)

        # Flexible mode: return DynamicConfig without schema validation
        if not strict:
            dynamic_config = DynamicConfig(data, frozen=True)
            return cls(dynamic_config)  # type: ignore[arg-type]

        # Use provided schema or default to ConfigRoot
        schema_class: Type[BaseModel] = schema if schema is not None else ConfigRoot

        # Validate schema is a BaseModel subclass
        if not (isinstance(schema_class, type) and issubclass(schema_class, BaseModel)):
            raise ConfigValidationError(
                field_path="schema",
                reason=f"Schema must be a Pydantic BaseModel subclass, got {type(schema_class)}"
            )

        try:
            config_root = schema_class(**data)
            return cls(config_root)
        except Exception as e:
            # Extract field path and type information from Pydantic error
            error_msg = str(e)
            field_path = "unknown"

            # Try to extract field name from Pydantic v2 error message
            # Format: "1 validation error for ConfigRoot\ndatabase.port\n  ..."
            lines = error_msg.split("\n")
            for i, line in enumerate(lines):
                # Look for lines that look like field paths (contain dots or are simple names)
                stripped = line.strip()
                starts_input = stripped.startswith("Input")
                starts_for = stripped.startswith("For further")
                if stripped and not starts_input and not starts_for:
                    # Check if this line looks like a field path
                    if "." in stripped or (i > 0 and "validation error" in lines[i-1].lower()):
                        # This might be our field path
                        is_validation = stripped.startswith("validation")
                        has_validation_error = "validation error" in stripped
                        if stripped and not is_validation and not has_validation_error:
                            field_path = stripped
                            break

            raise ConfigValidationError(
                field_path=field_path,
                reason=error_msg,
                original_error=e
            ) from e

    @overload
    @classmethod
    def from_file(
        cls,
        path: Union[Path, str],
        apply_env: bool = False,
        env_prefix: str = "APP_",
        cli_args: Optional[List[str]] = None,
        resolve_secrets: bool = False,
        schema: None = None,
        strict: bool = True,
    ) -> "PrismConfig[ConfigRoot]": ...

    @overload
    @classmethod
    def from_file(
        cls,
        path: Union[Path, str],
        apply_env: bool = False,
        env_prefix: str = "APP_",
        cli_args: Optional[List[str]] = None,
        resolve_secrets: bool = False,
        schema: Type[T] = ...,
        strict: bool = True,
    ) -> "PrismConfig[T]": ...

    @overload
    @classmethod
    def from_file(
        cls,
        path: Union[Path, str],
        apply_env: bool = False,
        env_prefix: str = "APP_",
        cli_args: Optional[List[str]] = None,
        resolve_secrets: bool = False,
        schema: None = None,
        *,
        strict: "Literal[False]",
    ) -> "PrismConfig[DynamicConfig]": ...

    @classmethod
    def from_file(
        cls,
        path: Union[Path, str],
        apply_env: bool = False,
        env_prefix: str = "APP_",
        cli_args: Optional[List[str]] = None,
        resolve_secrets: bool = False,
        schema: Optional[Type[T]] = None,
        strict: bool = True,
    ) -> "PrismConfig[T]":
        """
        Load configuration from a YAML file.

        This method reads and parses a YAML file, validates the configuration,
        and optionally applies environment variable overrides, CLI argument
        overrides, and secret resolution.

        Args:
            path: Path to YAML configuration file (Path object or string)
            apply_env: Whether to apply environment variable overrides (default: False)
            env_prefix: Prefix for environment variables (default: "APP_")
            cli_args: Optional list of CLI arguments to override config (default: None)
            resolve_secrets: Whether to resolve REF:: secret references (default: False)
            schema: Custom Pydantic model class for validation (default: ConfigRoot).
                    Use BaseConfigSection or BaseConfigRoot subclasses for custom schemas.
                    Ignored when strict=False.
            strict: Whether to validate against a schema (default: True).
                    Set to False for flexible mode - accepts any structure without validation.

        Returns:
            PrismConfig[T]: Validated and type-safe configuration instance
            PrismConfig[DynamicConfig]: When strict=False, dynamic config with dot-access

        Raises:
            ConfigFileNotFoundError: If the file doesn't exist
            ConfigParseError: If YAML parsing fails (includes line numbers)
            ConfigValidationError: If validation fails (missing fields, type errors).
                Only raised in strict mode.
            SecretResolutionError: If secret resolution fails

        Precedence order (highest to lowest):
            CLI args > Secrets > Environment variables > File values

        Examples:
            >>> # Basic usage
            >>> config = PrismConfig.from_file("config.yaml")
            >>> print(config.app.name)

            >>> # Flexible mode - any YAML structure (v2.0.0+)
            >>> config = PrismConfig.from_file("config.yaml", strict=False)
            >>> print(config.any_section.any_key)  # Works!

            >>> # With custom schema (v2.0.0+)
            >>> config = PrismConfig.from_file("config.yaml", schema=MyAppConfig)
            >>> print(config.auth.jwt_secret)

            >>> # With environment variable overrides
            >>> config = PrismConfig.from_file(
            ...     "config.yaml",
            ...     apply_env=True,
            ...     env_prefix="MYAPP_"
            ... )

            >>> # With CLI overrides (production usage)
            >>> import sys
            >>> config = PrismConfig.from_file(
            ...     "config.yaml",
            ...     apply_env=True,
            ...     cli_args=sys.argv[1:]
            ... )

            >>> # With secret resolution for Docker/Kubernetes
            >>> config = PrismConfig.from_file(
            ...     "/etc/app/config.yaml",
            ...     resolve_secrets=True
            ... )

            >>> # Using Path object
            >>> from pathlib import Path
            >>> config = PrismConfig.from_file(
            ...     Path(__file__).parent / "config.yaml"
            ... )

        YAML File Format:
            ```yaml
            app:
              name: my-app
              environment: production

            database:
              host: db.example.com
              port: 5432
              name: mydb
              password: REF::ENV::DB_PASSWORD  # Secret reference
            ```

        See Also:
            - from_dict(): Load from Python dictionary
            - from_all(): Convenience method with all overrides enabled
            - BaseConfigSection: Base class for custom config sections
            - BaseConfigRoot: Base class for custom root schemas
        """
        # Convert string path to Path object
        file_path = Path(path) if isinstance(path, str) else path

        # Check if file exists
        if not file_path.exists():
            raise ConfigFileNotFoundError(file_path)

        # Read and parse YAML file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            # Extract line number if available
            line_number = None
            if hasattr(e, 'problem_mark'):
                line_number = e.problem_mark.line + 1  # Convert 0-indexed to 1-indexed

            raise ConfigParseError(
                file_path=file_path,
                line_number=line_number,
                reason="YAML syntax error",
                original_error=e
            ) from e
        except Exception as e:
            raise ConfigParseError(
                file_path=file_path,
                reason=f"Error reading file: {e}",
                original_error=e
            ) from e

        # Handle empty file (yaml.safe_load returns None)
        if data is None:
            raise ConfigParseError(
                file_path=file_path,
                reason="Configuration file is empty"
            )

        # Validate it's a dictionary
        if not isinstance(data, dict):
            msg = (
                f"Configuration file must contain a YAML object (dict), "
                f"got {type(data).__name__}"
            )
            raise ConfigParseError(file_path=file_path, reason=msg)

        # Use from_dict to validate and load
        return cls.from_dict(
            data,
            apply_env=apply_env,
            env_prefix=env_prefix,
            cli_args=cli_args,
            resolve_secrets=resolve_secrets,
            schema=schema,
            strict=strict,
        )

    @overload
    @classmethod
    def from_all(
        cls,
        file_path: Union[Path, str],
        env_prefix: str = "APP_",
        cli_args: Optional[List[str]] = None,
        resolve_secrets: bool = False,
        schema: None = None,
        strict: bool = True,
    ) -> "PrismConfig[ConfigRoot]": ...

    @overload
    @classmethod
    def from_all(
        cls,
        file_path: Union[Path, str],
        env_prefix: str = "APP_",
        cli_args: Optional[List[str]] = None,
        resolve_secrets: bool = False,
        schema: Type[T] = ...,
        strict: bool = True,
    ) -> "PrismConfig[T]": ...

    @overload
    @classmethod
    def from_all(
        cls,
        file_path: Union[Path, str],
        env_prefix: str = "APP_",
        cli_args: Optional[List[str]] = None,
        resolve_secrets: bool = False,
        schema: None = None,
        *,
        strict: "Literal[False]",
    ) -> "PrismConfig[DynamicConfig]": ...

    @classmethod
    def from_all(
        cls,
        file_path: Union[Path, str],
        env_prefix: str = "APP_",
        cli_args: Optional[List[str]] = None,
        resolve_secrets: bool = False,
        schema: Optional[Type[T]] = None,
        strict: bool = True,
    ) -> "PrismConfig[T]":
        """
        Convenience method to load from file with env and CLI overrides.

        This method automatically applies both environment variable and CLI
        argument overrides in the correct precedence order.

        Args:
            file_path: Path to YAML configuration file
            env_prefix: Prefix for environment variables (default: "APP_")
            cli_args: Optional list of CLI arguments to override config (default: None)
            resolve_secrets: Whether to resolve REF:: secret references (default: False)
            schema: Custom Pydantic model class for validation (default: ConfigRoot).
                    Use BaseConfigSection or BaseConfigRoot subclasses for custom schemas.
                    Ignored when strict=False.
            strict: Whether to validate against a schema (default: True).
                    Set to False for flexible mode - accepts any structure without validation.

        Returns:
            PrismConfig[T] instance with validated data
            PrismConfig[DynamicConfig]: When strict=False, dynamic config with dot-access

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If YAML parsing or validation fails (strict mode only)

        Precedence order (highest to lowest):
            CLI args > Secrets > Environment variables > File values

        Example:
            >>> # With custom schema (v2.0.0+)
            >>> config = PrismConfig.from_all(
            ...     "config.yaml",
            ...     cli_args=sys.argv[1:],
            ...     resolve_secrets=True,
            ...     schema=MyAppConfig
            ... )

            >>> # Flexible mode (v2.0.0+)
            >>> config = PrismConfig.from_all("config.yaml", strict=False)
            >>> print(config.any_section.any_key)
        """
        return cls.from_file(
            file_path,
            apply_env=True,
            env_prefix=env_prefix,
            cli_args=cli_args,
            resolve_secrets=resolve_secrets,
            schema=schema,
            strict=strict,
        )

    @property
    def app(self):
        """Access app configuration section."""
        return self._config.app

    @property
    def database(self):
        """Access database configuration section."""
        return self._config.database

    def dump(
        self,
        use_color: Optional[bool] = None,
        palette: Optional["display.Palette"] = None,
        redact_secrets: bool = True
    ) -> str:
        """
        Dump configuration as a beautiful formatted table.

        Args:
            use_color: Whether to use ANSI colors (default: auto-detect based on TTY and NO_COLOR)
            palette: Custom color palette (default: load from prism-palette.toml or use default)
            redact_secrets: Whether to redact secret values (default: True).
                Set to False to show actual secret values (useful for debugging).

        Returns:
            Formatted table string with box-drawing characters and colors

        Example:
            ```python
            config = PrismConfig.from_file("config.yaml")
            print(config.dump())

            # Show secrets (for debugging only!)
            print(config.dump(redact_secrets=False))
            ```
        """
        from . import display

        # Auto-detect color support if not specified
        if use_color is None:
            use_color = display.should_use_color()

        # Load palette
        if palette is None:
            palette = display.load_palette()

        # Convert config to dict (handle both Pydantic and DynamicConfig)
        if isinstance(self._config, DynamicConfig):
            config_dict = self._config.to_dict()
        else:
            config_dict = self._config.model_dump()

        # Flatten nested config to dot notation
        flat_config = display.flatten_config(config_dict)

        # Prepare rows (optionally redacting secrets)
        rows = []
        for key, value in sorted(flat_config.items()):
            if redact_secrets:
                display_value = display.redact_value(key, value, palette)
            else:
                display_value = str(value)
            rows.append((key, display_value))

        # Render table
        return display.render_table(rows, palette, use_color)

    def display(
        self,
        use_color: Optional[bool] = None,
        palette: Optional["display.Palette"] = None,
        redact_secrets: bool = True
    ) -> None:
        """
        Display configuration with beautiful ASCII art banner.

        Prints the config dump with a neon vaporwave banner to stdout.
        Respects NO_COLOR environment variable and TTY detection.

        Args:
            use_color: Whether to use ANSI colors (default: auto-detect)
            palette: Custom color palette (default: load from prism-palette.toml)
            redact_secrets: Whether to redact secret values (default: True).
                Set to False to show actual secret values (useful for debugging).
                WARNING: Only use redact_secrets=False in secure environments!

        Example:
            ```python
            config = PrismConfig.from_file("config.yaml")
            config.display()  # Shows banner + config table (secrets redacted)

            # Show secrets (for debugging only!)
            config.display(redact_secrets=False)
            ```
        """
        from . import display

        # Auto-detect color support if not specified
        if use_color is None:
            use_color = display.should_use_color()

        # Load palette
        if palette is None:
            palette = display.load_palette()

        # Render and print banner
        banner = display.render_banner(palette, use_color)
        print(banner)

        # Render and print config table
        table = self.dump(use_color, palette, redact_secrets=redact_secrets)
        print(table)
        print()  # Extra newline for spacing

    def __repr__(self) -> str:
        if isinstance(self._config, DynamicConfig):
            keys = list(self._config.keys())
            if len(keys) > 3:
                keys_str = f"{keys[:3]}... ({len(keys)} sections)"
            else:
                keys_str = str(keys)
            return f"PrismConfig(sections={keys_str}, mode='flexible')"
        return f"PrismConfig(app={self.app.name}, env={self.app.environment})"

    @staticmethod
    def _apply_env_overrides(data: Dict[str, Any], env_prefix: str = "APP_") -> Dict[str, Any]:
        """
        Apply environment variable overrides to configuration data.

        Environment variables are matched using the pattern:
        {env_prefix}{SECTION}__{KEY} -> section.key

        Examples:
            APP_DATABASE__HOST -> database.host
            APP_APP__NAME -> app.name

        Args:
            data: Configuration dictionary to override
            env_prefix: Prefix for environment variables (default: "APP_")

        Returns:
            Configuration dictionary with environment overrides applied
        """
        import copy
        result = copy.deepcopy(data)

        # Iterate through environment variables
        for env_key, env_value in os.environ.items():
            # Check if env var starts with our prefix
            if not env_key.startswith(env_prefix):
                continue

            # Remove prefix
            key_path = env_key[len(env_prefix):]

            # Split by double underscore for nesting
            # APP_DATABASE__PORT -> ['DATABASE', 'PORT']
            parts = key_path.split("__")

            if len(parts) < 2:
                # Skip invalid paths (need at least section and key)
                continue

            # Convert to lowercase for case-insensitive matching
            parts = [p.lower() for p in parts]

            # Navigate to the nested location
            current = result
            for _, part in enumerate(parts[:-1]):
                if part not in current:
                    # Path doesn't exist in config, skip this env var
                    break
                current = current[part]
            else:
                # Set the value (last part is the key)
                final_key = parts[-1]
                if final_key in current:
                    # Type coercion will happen during Pydantic validation
                    current[final_key] = env_value

        return result

    @staticmethod
    def _apply_cli_overrides(data: Dict[str, Any], cli_args: List[str]) -> Dict[str, Any]:
        """
        Apply CLI argument overrides to configuration data.

        CLI arguments are matched using the patterns:
        --database.host=value -> database.host
        --database-host=value -> database.host

        Both dot notation and dash notation are supported. Dashes are converted
        to dots for nested path resolution.

        Args:
            data: Configuration dictionary to override
            cli_args: List of CLI arguments in format --key.path=value or --key-path=value

        Returns:
            Configuration dictionary with CLI overrides applied
        """
        import copy
        result = copy.deepcopy(data)

        for arg in cli_args:
            # Skip if not in expected format
            if not arg.startswith("--"):
                continue

            # Remove leading --
            arg = arg[2:]

            # Check for equals sign
            if "=" not in arg:
                continue

            # Split on first equals sign
            key_path, value = arg.split("=", 1)

            # Convert dashes to dots for consistent handling
            # --database-host -> database.host
            key_path = key_path.replace("-", ".")

            # Split by dots for nesting
            parts = key_path.split(".")

            if len(parts) < 2:
                # Skip invalid paths (need at least section and key)
                continue

            # Convert to lowercase for case-insensitive matching
            parts = [p.lower() for p in parts]

            # Navigate to the nested location
            current = result
            for _, part in enumerate(parts[:-1]):
                if part not in current:
                    # Path doesn't exist in config, skip this arg
                    break
                current = current[part]
            else:
                # Set the value (last part is the key)
                final_key = parts[-1]
                if final_key in current:
                    # Type coercion will happen during Pydantic validation
                    current[final_key] = value

        return result

    @staticmethod
    def _resolve_secrets(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolve REF:: secret references in configuration data.

        Secret references use the format: REF::PROVIDER::KEY_PATH

        Supported providers:
        - ENV: Environment variables (REF::ENV::DB_PASSWORD)
        - FILE: File-based secrets (REF::FILE::/run/secrets/db_pass)

        Args:
            data: Configuration dictionary with potential secret references

        Returns:
            Configuration dictionary with secrets resolved

        Raises:
            ValueError: If secret reference is invalid or resolution fails
        """
        import copy
        result = copy.deepcopy(data)

        # Regex to match REF::PROVIDER::KEY_PATH
        # Matches: REF::ENV::DB_PASSWORD or REF::FILE::/path/to/secret
        ref_pattern = re.compile(r'^REF::([A-Z]+)::(.+)$')
        # Matches REF::INVALID (missing second ::)
        invalid_ref_pattern = re.compile(r'^REF::[^:]+$')

        def resolve_value(value: Any) -> Any:
            """Recursively resolve secrets in a value."""
            if isinstance(value, str):
                # Check for invalid REF syntax first
                if invalid_ref_pattern.match(value):
                    raise InvalidSecretReferenceError(
                        reference=value,
                        reason="Missing second '::' separator"
                    )

                match = ref_pattern.match(value)
                if match:
                    provider_name = match.group(1)
                    key_path = match.group(2)

                    # Validate syntax
                    if not key_path:
                        raise InvalidSecretReferenceError(
                            reference=value,
                            reason="Empty key path"
                        )

                    # Get provider and resolve secret
                    try:
                        provider = get_provider(provider_name)
                    except ValueError as e:
                        # Provider not found
                        raise SecretProviderNotFoundError(
                            provider_name=provider_name,
                            available_providers=["ENV", "FILE"]
                        ) from e

                    try:
                        return provider.resolve(key_path)
                    except Exception as e:
                        # Secret resolution failed
                        raise SecretResolutionError(
                            provider=provider_name,
                            key=key_path,
                            reason=str(e),
                            original_error=e
                        ) from e
                return value
            elif isinstance(value, dict):
                return {k: resolve_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [resolve_value(item) for item in value]
            else:
                return value

        # Resolve all secrets in the config
        result = resolve_value(result)
        return result

    def to_dict(self, redact_secrets: bool = False) -> dict:
        """
        Export configuration to a Python dictionary.

        Args:
            redact_secrets: If True, redact secret values (default: False)

        Returns:
            Dictionary representation of configuration

        Example:
            >>> config = PrismConfig.from_file("config.yaml")
            >>> config_dict = config.to_dict()
            >>> config_dict = config.to_dict(redact_secrets=True)
        """
        from . import display

        # Convert to dict (handle both Pydantic and DynamicConfig)
        if isinstance(self._config, DynamicConfig):
            result = self._config.to_dict()
        else:
            result = self._config.model_dump()

        # Redact secrets if requested
        if redact_secrets:
            def redact_value(key: str, value: any) -> any:
                """Redact secret values in nested dicts."""
                if isinstance(value, dict):
                    return {k: redact_value(f"{key}.{k}", v) for k, v in value.items()}
                elif display.is_secret_key(key):
                    return "[REDACTED]"
                else:
                    return value

            result = {k: redact_value(k, v) for k, v in result.items()}

        return result

    def to_yaml(self, redact_secrets: bool = False) -> str:
        """
        Export configuration to a YAML string.

        Args:
            redact_secrets: If True, redact secret values (default: False)

        Returns:
            YAML string representation of configuration

        Example:
            >>> config = PrismConfig.from_file("config.yaml")
            >>> yaml_str = config.to_yaml()
            >>> yaml_str = config.to_yaml(redact_secrets=True)
        """
        import yaml

        config_dict = self.to_dict(redact_secrets=redact_secrets)
        return yaml.safe_dump(config_dict, default_flow_style=False, sort_keys=False)

    def to_yaml_file(self, path: Path | str, redact_secrets: bool = False) -> None:
        """
        Export configuration to a YAML file.

        Args:
            path: Path to output YAML file
            redact_secrets: If True, redact secret values (default: False)

        Example:
            >>> config = PrismConfig.from_file("config.yaml")
            >>> config.to_yaml_file("exported.yaml")
        """
        if isinstance(path, str):
            path = Path(path)

        yaml_content = self.to_yaml(redact_secrets=redact_secrets)
        path.write_text(yaml_content, encoding="utf-8")

    def to_json(self, redact_secrets: bool = False) -> str:
        """
        Export configuration to a JSON string.

        Args:
            redact_secrets: If True, redact secret values (default: False)

        Returns:
            JSON string representation of configuration

        Example:
            >>> config = PrismConfig.from_file("config.yaml")
            >>> json_str = config.to_json()
            >>> json_str = config.to_json(redact_secrets=True)
        """
        import json

        config_dict = self.to_dict(redact_secrets=redact_secrets)
        return json.dumps(config_dict, indent=2, sort_keys=False)

    def to_json_file(self, path: Path | str, redact_secrets: bool = False) -> None:
        """
        Export configuration to a JSON file.

        Args:
            path: Path to output JSON file
            redact_secrets: If True, redact secret values (default: False)

        Example:
            >>> config = PrismConfig.from_file("config.yaml")
            >>> config.to_json_file("exported.json")
        """
        if isinstance(path, str):
            path = Path(path)

        json_content = self.to_json(redact_secrets=redact_secrets)
        path.write_text(json_content, encoding="utf-8")

    def diff(self, other: "PrismConfig") -> dict:
        """
        Compare this configuration with another and return differences.

        Args:
            other: Another PrismConfig instance to compare against

        Returns:
            Dictionary mapping changed keys to {"old": value, "new": value}
            Empty dict if configurations are identical

        Example:
            >>> config1 = PrismConfig.from_file("config-v1.yaml")
            >>> config2 = PrismConfig.from_file("config-v2.yaml")
            >>> diff = config1.diff(config2)
            >>> print(diff)
            {
                "app.name": {"old": "app-v1", "new": "app-v2"},
                "database.host": {"old": "localhost", "new": "prod.example.com"}
            }
        """
        from . import display

        # Flatten both configs
        dict1 = self.to_dict()
        dict2 = other.to_dict()

        flat1 = display.flatten_config(dict1)
        flat2 = display.flatten_config(dict2)

        # Find differences
        differences = {}

        # Check all keys from both configs
        all_keys = set(flat1.keys()) | set(flat2.keys())

        for key in sorted(all_keys):
            val1 = flat1.get(key)
            val2 = flat2.get(key)

            if val1 != val2:
                differences[key] = {
                    "old": val1,
                    "new": val2
                }

        return differences

    def diff_str(self, other: "PrismConfig") -> str:
        """
        Compare this configuration with another and return human-readable diff.

        Args:
            other: Another PrismConfig instance to compare against

        Returns:
            Human-readable string showing differences

        Example:
            >>> config1 = PrismConfig.from_file("config-v1.yaml")
            >>> config2 = PrismConfig.from_file("config-v2.yaml")
            >>> print(config1.diff_str(config2))
            Configuration Differences:

            app.name:
              - Old: app-v1
              + New: app-v2

            database.host:
              - Old: localhost
              + New: prod.example.com
        """
        diff = self.diff(other)

        if not diff:
            return "No differences found."

        lines = ["Configuration Differences:", ""]

        for key, change in diff.items():
            lines.append(f"{key}:")
            lines.append(f"  - Old: {change['old']}")
            lines.append(f"  + New: {change['new']}")
            lines.append("")

        return "\n".join(lines)
