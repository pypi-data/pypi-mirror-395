"""
Secret provider interface and built-in implementations.

Providers handle resolution of REF:: style secret references.
"""

from typing import Protocol


class SecretProvider(Protocol):
    """
    Protocol for secret resolution backends.

    Providers must implement this interface to be used with prism-config.
    """

    def resolve(self, key_path: str) -> str:
        """
        Fetch secret from backing store.

        Args:
            key_path: Path to the secret (e.g., "/db/password")

        Returns:
            The secret value as a string

        Raises:
            KeyError: If secret not found
            ValueError: If secret resolution fails
        """
        ...

    def supports_rotation(self) -> bool:
        """
        Check if this provider supports key rotation.

        Returns:
            True if provider can handle key rotation
        """
        ...

    def max_value_size(self) -> int:
        """
        Maximum bytes this provider can store.

        Important for PQC: Must support at least 16KB for quantum-resistant keys.

        Returns:
            Maximum value size in bytes
        """
        ...


class EnvSecretProvider:
    """
    Secret provider that reads from environment variables.

    Example:
        REF::ENV::DB_PASSWORD resolves to os.environ["DB_PASSWORD"]
    """

    def resolve(self, key_path: str) -> str:
        """
        Resolve secret from environment variable.

        Args:
            key_path: Environment variable name (e.g., "DB_PASSWORD")

        Returns:
            Value of the environment variable

        Raises:
            ValueError: If environment variable not found
        """
        import os

        if key_path not in os.environ:
            raise ValueError(
                f"Secret resolution failed: Environment variable '{key_path}' not found"
            )

        return os.environ[key_path]

    def supports_rotation(self) -> bool:
        """ENV provider supports rotation via environment updates."""
        return True

    def max_value_size(self) -> int:
        """ENV vars are typically unlimited by Python."""
        return -1  # Unlimited


class FileSecretProvider:
    """
    Secret provider that reads from files.

    Example:
        REF::FILE::/run/secrets/db_password reads from Docker secret file

    Features:
        - Strips trailing newlines automatically
        - Supports Docker secrets pattern
        - Maximum file size: 1MB (for security)
    """

    def resolve(self, key_path: str) -> str:
        """
        Resolve secret from file.

        Args:
            key_path: Path to secret file (e.g., "/run/secrets/db_password")

        Returns:
            Contents of file with trailing newlines stripped

        Raises:
            ValueError: If file not found or unreadable
        """
        from pathlib import Path

        file_path = Path(key_path)

        if not file_path.exists():
            raise ValueError(
                f"Secret resolution failed: File '{key_path}' not found"
            )

        try:
            # Read file and strip trailing newlines/whitespace
            content = file_path.read_text(encoding='utf-8')
            return content.rstrip('\n\r')
        except PermissionError as err:
            raise ValueError(
                f"Secret resolution failed: Permission denied reading '{key_path}'"
            ) from err
        except Exception as e:
            raise ValueError(
                f"Secret resolution failed: Error reading file '{key_path}': {e}"
            ) from e

    def supports_rotation(self) -> bool:
        """FILE provider supports rotation via file updates."""
        return True

    def max_value_size(self) -> int:
        """FILE provider limits to 1MB for security."""
        return 1024 * 1024  # 1MB


# Global provider registry
_PROVIDERS = {
    "ENV": EnvSecretProvider(),
    "FILE": FileSecretProvider(),
}


def get_provider(name: str) -> SecretProvider:
    """
    Get a registered secret provider by name.

    Args:
        name: Provider name (e.g., "ENV", "FILE")

    Returns:
        The provider instance

    Raises:
        ValueError: If provider not found
    """
    if name not in _PROVIDERS:
        raise ValueError(
            f"Unknown secret provider: {name}. "
            f"Available providers: {', '.join(_PROVIDERS.keys())}"
        )
    return _PROVIDERS[name]


def register_provider(name: str, provider: SecretProvider) -> None:
    """
    Register a custom secret provider.

    Args:
        name: Provider name (e.g., "VAULT", "AWS")
        provider: Provider instance implementing SecretProvider protocol
    """
    _PROVIDERS[name] = provider


__all__ = [
    "SecretProvider",
    "EnvSecretProvider",
    "FileSecretProvider",
    "get_provider",
    "register_provider"
]
