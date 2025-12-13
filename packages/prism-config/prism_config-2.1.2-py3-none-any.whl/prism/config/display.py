"""
Beautiful terminal output for configuration dumps.

The Neon Dump - Vaporwave-inspired config visualization.
"""

import os
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# PRISM ASCII art banner
PRISM_ASCII_ART = """\
    ██████╗ ██████╗ ██╗███████╗███╗   ███╗
    ██╔══██╗██╔══██╗██║██╔════╝████╗ ████║
    ██████╔╝██████╔╝██║███████╗██╔████╔██║
    ██╔═══╝ ██╔══██╗██║╚════██║██║╚██╔╝██║
    ██║     ██║  ██║██║███████║██║ ╚═╝ ██║
    ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝     ╚═╝\
"""


def display_width(text: str) -> int:
    """
    Calculate the display width of a string, accounting for wide characters.

    Most emojis and East Asian characters take 2 terminal columns.
    This function uses Unicode character width properties to calculate
    the actual display width.

    Handles special cases:
    - Variation selectors (VS1-VS16) are zero-width
    - Characters followed by emoji variation selector (VS16/U+FE0F) render as wide
    - Zero-width joiners, combining marks are zero-width

    Args:
        text: The string to measure

    Returns:
        The display width in terminal columns
    """
    # Zero-width characters that don't contribute to display width
    # - Variation selectors (VS1-VS16): U+FE00-U+FE0F
    # - Zero-width joiner/non-joiner: U+200C, U+200D
    zero_width_ranges = {
        (0xFE00, 0xFE0F),  # Variation Selectors
        (0x200B, 0x200D),  # Zero-width space, non-joiner, joiner
        (0x2060, 0x2064),  # Word joiner, invisible operators
    }

    # Emoji variation selector (VS16) - makes preceding char render as emoji (wide)
    emoji_vs = 0xFE0F

    width = 0
    chars = list(text)
    i = 0

    while i < len(chars):
        char = chars[i]
        code = ord(char)

        # Check if character is in zero-width ranges
        is_zero_width = False
        for start, end in zero_width_ranges:
            if start <= code <= end:
                is_zero_width = True
                break

        if is_zero_width:
            i += 1
            continue

        # Check Unicode category for combining marks (zero-width)
        category = unicodedata.category(char)
        if category in ('Mn', 'Mc', 'Me'):  # Mark, Nonspacing / Spacing Combining / Enclosing
            i += 1
            continue

        # Check if next character is emoji variation selector (VS16)
        # If so, this character renders as a wide emoji
        has_emoji_vs = (i + 1 < len(chars) and ord(chars[i + 1]) == emoji_vs)

        # Get the East Asian Width property
        ea_width = unicodedata.east_asian_width(char)
        if ea_width in ('F', 'W'):
            # Full-width or Wide characters take 2 columns
            width += 2
        elif ea_width == 'A':
            # Ambiguous characters - treat as wide (most terminals do this for emoji)
            width += 2
        elif has_emoji_vs:
            # Character followed by emoji VS16 renders as wide emoji
            width += 2
        else:
            # Narrow, Half-width, or Neutral
            width += 1

        i += 1

    return width


def pad_to_width(text: str, target_width: int) -> str:
    """
    Pad a string with spaces to reach target display width.

    Args:
        text: The string to pad
        target_width: The desired display width

    Returns:
        The string padded with spaces
    """
    current_width = display_width(text)
    padding_needed = target_width - current_width
    if padding_needed > 0:
        return text + ' ' * padding_needed
    return text


# ANSI color codes
def ansi_color(code: int, text: str, bg: bool = False) -> str:
    """Apply ANSI 256-color code to text."""
    prefix = 48 if bg else 38
    return f"\033[{prefix};5;{code}m{text}\033[0m"


def ansi_bold(text: str) -> str:
    """Apply bold formatting."""
    return f"\033[1m{text}\033[0m"


def ansi_reset() -> str:
    """Reset all formatting."""
    return "\033[0m"


# Box-drawing character sets
BOX_STYLES = {
    "single": {
        "horizontal": "\u2500",
        "vertical": "\u2502",
        "top_left": "\u250c",
        "top_right": "\u2510",
        "bottom_left": "\u2514",
        "bottom_right": "\u2518",
        "cross": "\u253c",
        "t_down": "\u252c",
        "t_up": "\u2534",
        "t_right": "\u251c",
        "t_left": "\u2524",
    },
    "double": {
        "horizontal": "\u2550",
        "vertical": "\u2551",
        "top_left": "\u2554",
        "top_right": "\u2557",
        "bottom_left": "\u255a",
        "bottom_right": "\u255d",
        "cross": "\u256c",
        "t_down": "\u2566",
        "t_up": "\u2569",
        "t_right": "\u2560",
        "t_left": "\u2563",
    },
    "rounded": {
        "horizontal": "\u2500",
        "vertical": "\u2502",
        "top_left": "\u256d",
        "top_right": "\u256e",
        "bottom_left": "\u2570",
        "bottom_right": "\u256f",
        "cross": "\u253c",
        "t_down": "\u252c",
        "t_up": "\u2534",
        "t_right": "\u251c",
        "t_left": "\u2524",
    },
    "bold": {
        "horizontal": "\u2501",
        "vertical": "\u2503",
        "top_left": "\u250f",
        "top_right": "\u2513",
        "bottom_left": "\u2517",
        "bottom_right": "\u251b",
        "cross": "\u254b",
        "t_down": "\u2533",
        "t_up": "\u253b",
        "t_right": "\u2523",
        "t_left": "\u252b",
    },
}


@dataclass
class Palette:
    """
    Color palette for terminal output with comprehensive emoji mappings.

    The Palette class defines all visual styling for Neon Dump output:
    - ANSI 256-color codes for syntax highlighting
    - Box drawing character style
    - Section-to-emoji mappings for 90+ common configuration sections
    - Banner text and title
    - Maximum nesting depth for display (v2.0.0+)

    Emoji Categories (v2.0.0+):
        - Core: app, database, api, server, cache, queue, storage, network
        - Auth & Security: auth, jwt, oauth, ssl, tls, cors, credentials
        - Caching: redis, memcached
        - Messaging: kafka, rabbitmq, celery, pubsub, sqs, amqp
        - Cloud Providers: aws, azure, gcp, s3, lambda, cloudflare
        - Observability: logging, metrics, tracing, sentry, datadog, prometheus
        - HTTP/API: http, grpc, websocket, graphql, rest, gateway
        - Features: feature, flags, payment, stripe, email, notifications
        - Rate Limiting: rate_limit, throttle, quota
        - Databases: postgres, mysql, mongodb, elasticsearch, dynamodb
        - Misc: config, env, debug, test, dev, prod, staging, workers

    Attributes:
        header_bg: Background color for table headers (default: 197 hot pink)
        header_fg: Foreground color for headers (default: 231 white)
        key_color: Color for configuration keys (default: 51 cyan)
        value_color: Color for values (default: 183 light purple)
        border_color: Color for table borders (default: 213 pink)
        secret_color: Color for redacted secrets (default: 196 red)
        category_emoji: Color for section emojis (default: 51 cyan)
        box_style: Box drawing style ("single", "double", "rounded", "bold")
        emojis: Dict mapping section names to emoji characters
        banner_text: Custom ASCII art banner (uses PRISM_ASCII_ART if None)
        banner_title: Title displayed below banner
        max_depth: Maximum nesting depth for display (default: None = unlimited)

    Example:
        >>> palette = Palette()
        >>> palette.emojis["kafka"]
        '📬'
        >>> palette.emojis["auth"]
        '🔑'
        >>> palette.max_depth
        None
    """

    # Colors
    header_bg: int = 197  # Hot pink
    header_fg: int = 231  # White
    key_color: int = 51  # Cyan
    value_color: int = 183  # Light purple
    border_color: int = 213  # Pink
    secret_color: int = 196  # Red
    category_emoji: int = 51  # Cyan

    # Box style
    box_style: str = "double"

    # Emojis
    emojis: Dict[str, str] = None

    # Banner
    banner_text: Optional[str] = None
    banner_title: str = "CONFIGURATION LOADED"

    # Display options (v2.0.0+)
    max_depth: Optional[int] = None  # None = unlimited nesting depth

    # Secret detection (v2.0.0+)
    secret_keywords: Optional[List[str]] = None  # Additional secret keywords
    secret_patterns: Optional[List[str]] = None  # Regex patterns for secret detection

    def __post_init__(self):
        """Initialize default emojis if not provided."""
        if self.emojis is None:
            self.emojis = {
                # === Core (original) ===
                "app": "\U0001f310",  # 🌐
                "database": "\U0001f4be",  # 💾
                "db": "\U0001f4be",  # 💾 (alias)
                "api": "\U0001f50c",  # 🔌
                "server": "\U0001f5a5\ufe0f",  # 🖥️
                "cache": "\U0001f9e0",  # 🧠
                "queue": "\U0001f4e5",  # 📥
                "storage": "\U0001f4c1",  # 📁
                "network": "\U0001f4e1",  # 📡
                "security": "\U0001f510",  # 🔐
                "monitoring": "\U0001f4ca",  # 📊
                # === Auth & Security ===
                "auth": "\U0001f511",  # 🔑
                "jwt": "\U0001f3ab",  # 🎫
                "oauth": "\U0001f513",  # 🔓
                "session": "\U0001f39f\ufe0f",  # 🎟️
                "cors": "\U0001f30d",  # 🌍
                "ssl": "\U0001f512",  # 🔒
                "tls": "\U0001f512",  # 🔒
                "credentials": "\U0001f510",  # 🔐
                "token": "\U0001f3ab",  # 🎫
                "password": "\U0001f512",  # 🔒
                # === Caching ===
                "redis": "\U0001f534",  # 🔴
                "memcached": "\U0001f9e0",  # 🧠
                "caching": "\U0001f9e0",  # 🧠
                # === Messaging & Queues ===
                "kafka": "\U0001f4ec",  # 📬
                "rabbitmq": "\U0001f430",  # 🐰
                "celery": "\U0001f96c",  # 🥬
                "pubsub": "\U0001f4e2",  # 📢
                "messaging": "\U0001f4e8",  # 📨
                "events": "\U0001f4e2",  # 📢
                "amqp": "\U0001f4e8",  # 📨
                "sqs": "\U0001f4e5",  # 📥
                # === Cloud Providers ===
                "aws": "\u2601\ufe0f",  # ☁️
                "azure": "\U0001f537",  # 🔷
                "gcp": "\U0001f536",  # 🔶
                "cloud": "\u2601\ufe0f",  # ☁️
                "s3": "\U0001faa3",  # 🪣
                "lambda": "\u03bb",  # λ (Greek lambda)
                "cloudflare": "\U0001f7e0",  # 🟠
                "digitalocean": "\U0001f4a7",  # 💧
                "heroku": "\U0001f7e3",  # 🟣
                # === Observability ===
                "logging": "\U0001f4dd",  # 📝
                "log": "\U0001f4dd",  # 📝
                "logs": "\U0001f4dd",  # 📝
                "metrics": "\U0001f4c8",  # 📈
                "tracing": "\U0001f50d",  # 🔍
                "sentry": "\U0001f6e1\ufe0f",  # 🛡️
                "datadog": "\U0001f415",  # 🐕
                "newrelic": "\U0001f7e2",  # 🟢
                "prometheus": "\U0001f525",  # 🔥
                "grafana": "\U0001f4ca",  # 📊
                "opentelemetry": "\U0001f52d",  # 🔭
                "otel": "\U0001f52d",  # 🔭
                # === HTTP/API Infrastructure ===
                "http": "\U0001f310",  # 🌐
                "https": "\U0001f512",  # 🔒
                "grpc": "\u26a1",  # ⚡
                "websocket": "\U0001f50c",  # 🔌
                "graphql": "\u25fc\ufe0f",  # ◼️
                "rest": "\U0001f504",  # 🔄
                "proxy": "\U0001f6e1\ufe0f",  # 🛡️
                "gateway": "\U0001f6aa",  # 🚪
                "loadbalancer": "\u2696\ufe0f",  # ⚖️
                "lb": "\u2696\ufe0f",  # ⚖️
                # === Features & Business ===
                "feature": "\U0001f6a9",  # 🚩
                "features": "\U0001f6a9",  # 🚩
                "flags": "\U0001f3f3\ufe0f",  # 🏳️
                "payment": "\U0001f4b3",  # 💳
                "payments": "\U0001f4b3",  # 💳
                "stripe": "\U0001f4b0",  # 💰
                "billing": "\U0001f4b5",  # 💵
                "email": "\U0001f4e7",  # 📧
                "smtp": "\u2709\ufe0f",  # ✉️
                "mail": "\U0001f4e7",  # 📧
                "notifications": "\U0001f514",  # 🔔
                "sms": "\U0001f4f1",  # 📱
                "push": "\U0001f514",  # 🔔
                # === Rate Limiting ===
                "rate_limit": "\u23f1\ufe0f",  # ⏱️
                "ratelimit": "\u23f1\ufe0f",  # ⏱️
                "throttle": "\U0001f6a6",  # 🚦
                "quota": "\U0001f4ca",  # 📊
                "limits": "\U0001f6a7",  # 🚧
                # === Databases (extended) ===
                "postgres": "\U0001f418",  # 🐘
                "postgresql": "\U0001f418",  # 🐘
                "mysql": "\U0001f42c",  # 🐬
                "mongodb": "\U0001f343",  # 🍃
                "mongo": "\U0001f343",  # 🍃
                "elasticsearch": "\U0001f50d",  # 🔍
                "elastic": "\U0001f50d",  # 🔍
                "sqlite": "\U0001f4be",  # 💾
                "dynamodb": "\U0001f5c3\ufe0f",  # 🗃️
                # === Misc ===
                "config": "\u2699\ufe0f",  # ⚙️
                "settings": "\u2699\ufe0f",  # ⚙️
                "environment": "\U0001f30e",  # 🌎
                "env": "\U0001f30e",  # 🌎
                "debug": "\U0001f41b",  # 🐛
                "test": "\U0001f9ea",  # 🧪
                "testing": "\U0001f9ea",  # 🧪
                "development": "\U0001f6e0\ufe0f",  # 🛠️
                "dev": "\U0001f6e0\ufe0f",  # 🛠️
                "production": "\U0001f680",  # 🚀
                "prod": "\U0001f680",  # 🚀
                "staging": "\U0001f3ad",  # 🎭
                "workers": "\U0001f477",  # 👷
                "scheduler": "\U0001f4c5",  # 📅
                "cron": "\u23f0",  # ⏰
                "jobs": "\U0001f4cb",  # 📋
                "tasks": "\U0001f4cb",  # 📋
                # === Status indicators (used internally) ===
                "secret_redacted": "\U0001f512",  # 🔒
                "loaded": "\u2705",  # ✅
                "warning": "\u26a0\ufe0f",  # ⚠️
                "error": "\u274c",  # ❌
            }

    def get_box_chars(self) -> Dict[str, str]:
        """Get box-drawing characters for current style."""
        return BOX_STYLES.get(self.box_style, BOX_STYLES["double"])


# Default palette instance
DEFAULT_PALETTE = Palette()

# Cache for loaded palettes (path -> (mtime, Palette))
_PALETTE_CACHE: Dict[Optional[str], Tuple[float, Palette]] = {}

# Custom emoji registry (for runtime registration)
_CUSTOM_EMOJI_REGISTRY: Dict[str, str] = {}


def register_emoji(section: str, emoji: str) -> None:
    """
    Register a custom emoji for a configuration section.

    This function allows users to add custom emoji mappings at runtime.
    Custom emojis take precedence over built-in mappings.

    Args:
        section: Configuration section name (e.g., "auth", "my_custom_section")
        emoji: Emoji character or string (e.g., "🔑", "🚀")

    Example:
        >>> from prism.config.display import register_emoji
        >>> register_emoji("my_service", "🎯")
        >>> register_emoji("custom_auth", "🔐")

    Note:
        Custom emojis are stored globally and persist for the lifetime of the process.
        They apply to all PrismConfig instances.
    """
    _CUSTOM_EMOJI_REGISTRY[section.lower()] = emoji


def unregister_emoji(section: str) -> bool:
    """
    Remove a custom emoji registration.

    Args:
        section: Configuration section name to unregister

    Returns:
        True if the emoji was removed, False if it wasn't registered

    Example:
        >>> from prism.config.display import register_emoji, unregister_emoji
        >>> register_emoji("my_service", "🎯")
        >>> unregister_emoji("my_service")
        True
    """
    section_lower = section.lower()
    if section_lower in _CUSTOM_EMOJI_REGISTRY:
        del _CUSTOM_EMOJI_REGISTRY[section_lower]
        return True
    return False


def get_registered_emojis() -> Dict[str, str]:
    """
    Get all custom registered emojis.

    Returns:
        Dictionary mapping section names to emoji strings

    Example:
        >>> from prism.config.display import register_emoji, get_registered_emojis
        >>> register_emoji("my_service", "🎯")
        >>> get_registered_emojis()
        {'my_service': '🎯'}
    """
    return _CUSTOM_EMOJI_REGISTRY.copy()


def clear_registered_emojis() -> None:
    """
    Clear all custom emoji registrations.

    Example:
        >>> from prism.config.display import clear_registered_emojis
        >>> clear_registered_emojis()
    """
    _CUSTOM_EMOJI_REGISTRY.clear()


def load_palette(path: Optional[Path] = None) -> Palette:
    """
    Load palette from TOML file with caching.

    The palette is cached to avoid re-parsing the TOML file on every call.
    Cache is invalidated when the file is modified.

    Args:
        path: Path to palette TOML file (default: prism-palette.toml in repo root)

    Returns:
        Palette instance
    """
    if path is None:
        # Look for prism-palette.toml in current directory or parent directories
        current = Path.cwd()
        for _ in range(5):  # Check up to 5 levels up
            palette_file = current / "prism-palette.toml"
            if palette_file.exists():
                path = palette_file
                break
            current = current.parent

    if path is None or not path.exists():
        # Cache the default palette for None path
        cache_key = None
        if cache_key in _PALETTE_CACHE:
            return _PALETTE_CACHE[cache_key][1]
        _PALETTE_CACHE[cache_key] = (0, DEFAULT_PALETTE)
        return DEFAULT_PALETTE

    # Convert to string for cache key
    cache_key = str(path)

    # Check cache
    try:
        mtime = path.stat().st_mtime
        if cache_key in _PALETTE_CACHE:
            cached_mtime, cached_palette = _PALETTE_CACHE[cache_key]
            if cached_mtime == mtime:
                return cached_palette
    except OSError:
        # If stat fails, continue to load
        pass

    try:
        import tomllib  # Python 3.11+
    except ImportError:
        try:
            import tomli as tomllib  # Fallback for Python < 3.11
        except ImportError:
            # If no TOML library available, return default
            return DEFAULT_PALETTE

    try:
        with open(path, "rb") as f:
            data = tomllib.load(f)

        colors = data.get("colors", {})
        box_style_data = data.get("box_style", {})
        emoji_data = data.get("emojis", {})
        banner_data = data.get("banner", {})
        display_data = data.get("display", {})
        secrets_data = data.get("secrets", {})

        palette = Palette(
            header_bg=colors.get("header_bg", 197),
            header_fg=colors.get("header_fg", 231),
            key_color=colors.get("key_color", 51),
            value_color=colors.get("value_color", 183),
            border_color=colors.get("border_color", 213),
            secret_color=colors.get("secret_color", 196),
            category_emoji=colors.get("category_emoji", 51),
            box_style=box_style_data.get("style", "double"),
            emojis=emoji_data if emoji_data else None,
            banner_text=banner_data.get("text"),
            banner_title=banner_data.get("title", "CONFIGURATION LOADED"),
            max_depth=display_data.get("max_depth"),
            secret_keywords=secrets_data.get("keywords"),
            secret_patterns=secrets_data.get("patterns"),
        )

        # Cache the loaded palette
        _PALETTE_CACHE[cache_key] = (mtime, palette)
        return palette
    except Exception:
        # If any error loading palette, return default
        return DEFAULT_PALETTE


def flatten_config(
    data: Dict[str, Any],
    parent_key: str = "",
    sep: str = ".",
    max_depth: Optional[int] = None,
    _current_depth: int = 1,
) -> Dict[str, Any]:
    """
    Flatten nested dictionary to dot notation with optional depth limit.

    Args:
        data: Nested dictionary
        parent_key: Parent key prefix
        sep: Separator (default: ".")
        max_depth: Maximum nesting depth (None = unlimited, v2.0.0+).
            Depth 1 = only top level keys, depth 2 = one level of nesting, etc.
        _current_depth: Internal depth counter (do not set manually)

    Returns:
        Flattened dictionary with dot-notation keys

    Examples:
        >>> flatten_config({"a": {"b": {"c": 1}}})
        {"a.b.c": 1}
        >>> flatten_config({"a": {"b": {"c": 1}}}, max_depth=1)
        {"a": "{'b': {'c': 1}}"}  # Stops at depth 1, stringifies nested dict
        >>> flatten_config({"a": {"b": {"c": 1}}}, max_depth=2)
        {"a.b": "{'c': 1}"}  # Stops at depth 2
    """
    items = []
    for key, value in data.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key

        # Check if we've reached max depth
        if isinstance(value, dict):
            if max_depth is not None and _current_depth >= max_depth:
                # At max depth, don't flatten further - keep as nested dict representation
                items.append((new_key, str(value)))
            else:
                items.extend(
                    flatten_config(
                        value,
                        new_key,
                        sep=sep,
                        max_depth=max_depth,
                        _current_depth=_current_depth + 1,
                    ).items()
                )
        else:
            items.append((new_key, value))
    return dict(items)


# Fallback emoji categories for smart detection
FALLBACK_CATEGORIES = {
    # Security-related keywords -> lock emoji
    "security": ["secure", "encrypt", "decrypt", "cipher", "hash", "sign", "verify"],
    # Auth-related keywords -> key emoji
    "auth": ["login", "logout", "user", "account", "permission", "role", "acl"],
    # Database-related keywords -> disk emoji
    "database": ["sql", "query", "table", "schema", "migration", "model", "orm"],
    # Network-related keywords -> network emoji
    "network": ["host", "port", "url", "endpoint", "connection", "socket", "tcp"],
    # Storage-related keywords -> folder emoji
    "storage": ["file", "path", "directory", "folder", "upload", "download", "asset"],
    # Logging-related keywords -> log emoji
    "logging": ["logger", "trace", "span", "telemetry", "audit"],
    # Config-related keywords -> gear emoji
    "config": ["option", "preference", "parameter", "default", "override"],
}


def _detect_section_emoji(section: str, palette: Palette) -> Optional[str]:
    """
    Detect emoji for a single section name.

    This is the core matching logic used by detect_category.
    Returns None if no match is found.

    Args:
        section: A single section name (lowercase)
        palette: Palette with emoji mappings

    Returns:
        Emoji string if matched, None otherwise
    """
    # Stage 0: Check custom emoji registry first (highest priority)
    if section in _CUSTOM_EMOJI_REGISTRY:
        return _CUSTOM_EMOJI_REGISTRY[section]

    # Generic terms that shouldn't match via prefix/suffix/substring
    # These are too common and would cause false positives
    generic_terms = {
        "config", "settings", "env", "environment", "options", "params",
        "dev", "prod", "staging", "test", "debug", "log", "logs"
    }

    # Stage 1: Exact match
    if section in palette.emojis:
        return palette.emojis[section]

    # Sort by length (longest first) to prefer more specific matches
    sorted_keys = sorted(palette.emojis.keys(), key=len, reverse=True)

    # Stage 2: Prefix match - section starts with emoji key
    for emoji_key in sorted_keys:
        if emoji_key in generic_terms:
            continue
        if section.startswith(emoji_key + "_") or section.startswith(emoji_key + "-"):
            return palette.emojis[emoji_key]

    # Stage 3: Suffix match - section ends with emoji key
    for emoji_key in sorted_keys:
        if emoji_key in generic_terms:
            continue
        if section.endswith("_" + emoji_key) or section.endswith("-" + emoji_key):
            return palette.emojis[emoji_key]

    # Stage 4: Substring match - section contains emoji key (with delimiters)
    for emoji_key in sorted_keys:
        if emoji_key in generic_terms:
            continue
        # Check for the emoji key as a word within the section
        if f"_{emoji_key}_" in section or f"-{emoji_key}-" in section:
            return palette.emojis[emoji_key]
        # Also match at boundaries
        if f"_{emoji_key}" in section or f"-{emoji_key}" in section:
            return palette.emojis[emoji_key]
        if f"{emoji_key}_" in section or f"{emoji_key}-" in section:
            return palette.emojis[emoji_key]

    # Stage 5: Fallback categories - broader keyword matching
    for category, keywords in FALLBACK_CATEGORIES.items():
        if category in palette.emojis:
            for keyword in keywords:
                if keyword in section:
                    return palette.emojis[category]

    return None


def detect_category(key: str, palette: Palette) -> str:
    """
    Detect category emoji from config key with smart hierarchical matching.

    Uses a multi-stage detection algorithm with hierarchical fallback:
    0. Custom registry: check runtime-registered emojis first (highest priority)
    1. Exact match: section name matches emoji key exactly
    2. Prefix match: section name starts with a known emoji key (e.g., "jwt_config" -> "jwt")
    3. Suffix match: section name ends with a known emoji key (e.g., "my_redis" -> "redis")
    4. Substring match: section name contains a known emoji key
    5. Fallback categories: broader keyword matching for related terms
    6. Hierarchical fallback: try parent sections (e.g., "services.auth.jwt" -> "auth")
    7. Default: returns ⚙️ if no match found

    Hierarchical matching (v2.0.0+):
        For deeply nested keys like "services.auth.jwt.secret", the algorithm tries:
        1. First, match "services" using all stages
        2. If no match, try "auth" using all stages
        3. If no match, try "jwt" using all stages
        4. Return default ⚙️ only if all levels fail

    Note: Generic terms like "config", "settings", "env" are excluded from prefix/suffix/
    substring matching to avoid false positives (e.g., "jwt_config" matching "config").

    Args:
        key: Config key (e.g., "database.host", "jwt_config.secret", "services.auth.jwt.secret")
        palette: Palette with emoji mappings

    Returns:
        Category emoji string

    Examples:
        >>> palette = Palette()
        >>> detect_category("database.host", palette)
        '💾'
        >>> detect_category("jwt_config.secret", palette)
        '🎫'
        >>> detect_category("auth_service.timeout", palette)
        '🔑'
        >>> detect_category("services.auth.jwt.secret", palette)  # Hierarchical
        '🔑'  # Matches 'auth' since 'services' doesn't match
    """
    default_emoji = "\u2699\ufe0f"  # ⚙️

    # Split key into parts for hierarchical matching
    parts = key.split(".")

    # Try each part from the beginning, looking for a match
    # This gives priority to outer sections (first part), but falls back to inner ones
    for part in parts:
        section = part.lower()
        emoji = _detect_section_emoji(section, palette)
        if emoji is not None:
            return emoji

    # No match found at any level
    return default_emoji


def is_secret_key(key: str, palette: Optional[Palette] = None) -> bool:
    """
    Check if config key contains a secret.

    Uses word boundary matching to avoid false positives. For example:
    - "api_key" matches (key is a word)
    - "expiry" does NOT match (key is not a word, just substring)
    - "password" matches
    - "secret_token" matches

    Custom secret detection (v2.0.0+):
        The palette can specify additional secret keywords and regex patterns:
        - palette.secret_keywords: List of additional keywords to check
        - palette.secret_patterns: List of regex patterns to match

    Args:
        key: Config key
        palette: Optional palette with custom secret detection settings

    Returns:
        True if key appears to contain a secret

    Examples:
        >>> is_secret_key("database.password")
        True
        >>> is_secret_key("api_key")
        True
        >>> is_secret_key("expiry")  # No false positive
        False
    """
    import re

    # Keywords that indicate secret values (can match anywhere)
    secret_keywords = ["password", "secret", "token", "credential", "passwd"]

    # Keywords that need word boundary matching to avoid false positives
    # e.g., "key" shouldn't match "expiry", "turkey", "monkey"
    boundary_keywords = ["key", "auth"]

    key_lower = key.lower()

    # Check simple keywords (can match anywhere)
    for keyword in secret_keywords:
        if keyword in key_lower:
            return True

    # Check boundary keywords (must be at word boundary)
    for keyword in boundary_keywords:
        # Match keyword at word boundaries (_, -, ., start, end)
        pattern = rf"(^|[_.\-]){keyword}([_.\-]|$)"
        if re.search(pattern, key_lower):
            return True

    # Check custom secret keywords from palette (v2.0.0+)
    if palette and palette.secret_keywords:
        for keyword in palette.secret_keywords:
            if keyword.lower() in key_lower:
                return True

    # Check custom regex patterns from palette (v2.0.0+)
    if palette and palette.secret_patterns:
        for pattern in palette.secret_patterns:
            try:
                if re.search(pattern, key_lower, re.IGNORECASE):
                    return True
            except re.error:
                # Skip invalid regex patterns
                pass

    return False


def redact_value(key: str, value: Any, palette: Palette) -> str:
    """
    Redact secret values.

    Args:
        key: Config key
        value: Config value
        palette: Palette for styling (also used for custom secret detection)

    Returns:
        Original value or redacted placeholder
    """
    if is_secret_key(key, palette):
        secret_emoji = palette.emojis.get("secret_redacted", "\U0001f512")  # 🔒
        return f"[{secret_emoji} REDACTED]"
    return str(value)


def render_table(rows: List[Tuple[str, str]], palette: Palette, use_color: bool = True) -> str:
    """
    Render a beautiful table with box-drawing characters.

    Args:
        rows: List of (key, value) tuples
        palette: Color palette
        use_color: Whether to use ANSI colors

    Returns:
        Formatted table string
    """
    if not rows:
        return ""

    # Calculate column widths with minimum widths for better formatting
    # Use display_width to account for double-width emoji characters
    min_key_width = 22  # "Configuration Key" + padding
    min_value_width = 20  # "Value" + padding
    # +4 for emoji (2 display cols) and spaces (2 chars)
    max_key_width = max(min_key_width, max(display_width(row[0]) + 4 for row in rows))
    max_value_width = max(min_value_width, max(display_width(row[1]) for row in rows))

    # Box characters
    box = palette.get_box_chars()
    h = box["horizontal"]
    v = box["vertical"]

    # Build table
    lines = []

    # Top border
    top_line = (
        box["top_left"]
        + h * max_key_width
        + box["t_down"]
        + h * max_value_width
        + box["top_right"]
    )
    if use_color:
        top_line = ansi_color(palette.border_color, top_line)
    lines.append(top_line)

    # Header
    header_key = "Configuration Key".ljust(max_key_width)
    header_value = "Value".ljust(max_value_width)

    if use_color:
        header_key = ansi_color(palette.header_fg, header_key, bg=False)
        header_key = ansi_color(palette.header_bg, header_key, bg=True)
        header_value = ansi_color(palette.header_fg, header_value, bg=False)
        header_value = ansi_color(palette.header_bg, header_value, bg=True)
        v_colored = ansi_color(palette.border_color, v)
        header_line = v_colored + header_key + v_colored + header_value + v_colored
    else:
        header_line = v + header_key + v + header_value + v

    lines.append(header_line)

    # Header separator
    sep_line = (
        box["t_right"]
        + h * max_key_width
        + box["cross"]
        + h * max_value_width
        + box["t_left"]
    )
    if use_color:
        sep_line = ansi_color(palette.border_color, sep_line)
    lines.append(sep_line)

    # Data rows
    for key, value in rows:
        # Add category emoji
        emoji = detect_category(key, palette)
        # Use pad_to_width to account for double-width emoji characters
        display_key = pad_to_width(f"{emoji}  {key}", max_key_width)
        display_value = pad_to_width(value, max_value_width)

        if use_color:
            # Color the key and value
            display_key = ansi_color(palette.key_color, display_key)
            # Color redacted values differently
            if "REDACTED" in value:
                display_value = ansi_color(palette.secret_color, display_value)
            else:
                display_value = ansi_color(palette.value_color, display_value)

            v_colored = ansi_color(palette.border_color, v)
            row_line = v_colored + display_key + v_colored + display_value + v_colored
        else:
            row_line = v + display_key + v + display_value + v

        lines.append(row_line)

    # Bottom border
    bottom_line = (
        box["bottom_left"]
        + h * max_key_width
        + box["t_up"]
        + h * max_value_width
        + box["bottom_right"]
    )
    if use_color:
        bottom_line = ansi_color(palette.border_color, bottom_line)
    lines.append(bottom_line)

    return "\n".join(lines)


def should_use_color() -> bool:
    """
    Determine if colored output should be used.

    Respects NO_COLOR environment variable and TTY detection.

    Returns:
        True if color should be used
    """
    # Check NO_COLOR environment variable (standard)
    if os.environ.get("NO_COLOR"):
        return False

    # Check PRISM_NO_COLOR for prism-specific override
    if os.environ.get("PRISM_NO_COLOR"):
        return False

    # Check if stdout is a TTY
    if not sys.stdout.isatty():
        return False

    return True


def render_banner(palette: Palette, use_color: bool = True) -> str:
    """
    Render ASCII art banner with vaporwave gradient.

    Args:
        palette: Palette with banner configuration
        use_color: Whether to use colors

    Returns:
        Formatted banner string
    """
    # Import version here to avoid circular imports
    from . import __version__

    lines = []

    # Use custom banner text if provided, otherwise use default PRISM ASCII art
    banner_text = palette.banner_text if palette.banner_text else PRISM_ASCII_ART
    banner_lines = banner_text.split('\n')

    if use_color:
        # Vaporwave gradient colors (pink -> cyan)
        gradient_colors = [213, 207, 171, 135, 99, 63, 51]  # Pink to cyan

        for i, line in enumerate(banner_lines):
            if line.strip():  # Only color non-empty lines
                # Calculate color index based on line position
                color_idx = min(i, len(gradient_colors) - 1)
                colored_line = ansi_color(gradient_colors[color_idx], line)
                lines.append(colored_line)
            else:
                lines.append(line)
    else:
        lines.extend(banner_lines)

    # Title with version
    title = f"    {palette.banner_title}  (v{__version__})    "
    if use_color:
        title = ansi_bold(ansi_color(palette.header_bg, title))
    lines.append("")
    lines.append(title)
    lines.append("")

    return "\n".join(lines)
