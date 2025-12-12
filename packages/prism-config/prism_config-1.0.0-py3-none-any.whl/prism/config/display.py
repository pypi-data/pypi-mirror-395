"""
Beautiful terminal output for configuration dumps.

The Neon Dump - Vaporwave-inspired config visualization.
"""

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


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
    """Color palette for terminal output."""

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

    def __post_init__(self):
        """Initialize default emojis if not provided."""
        if self.emojis is None:
            self.emojis = {
                "app": "\U0001f310",  # 🌐
                "database": "\U0001f4be",  # 💾
                "api": "\U0001f50c",  # 🔌
                "server": "\U0001f5a5\ufe0f",  # 🖥️
                "cache": "\U0001f4ca",  # 📊
                "queue": "\U0001f4e5",  # 📥
                "storage": "\U0001f4c1",  # 📁
                "network": "\U0001f4e1",  # 📡
                "security": "\U0001f510",  # 🔐
                "monitoring": "\U0001f4ca",  # 📊
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
        )

        # Cache the loaded palette
        _PALETTE_CACHE[cache_key] = (mtime, palette)
        return palette
    except Exception:
        # If any error loading palette, return default
        return DEFAULT_PALETTE


def flatten_config(data: Dict[str, Any], parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    """
    Flatten nested dictionary to dot notation.

    Args:
        data: Nested dictionary
        parent_key: Parent key prefix
        sep: Separator (default: ".")

    Returns:
        Flattened dictionary with dot-notation keys
    """
    items = []
    for key, value in data.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_config(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


def detect_category(key: str, palette: Palette) -> str:
    """
    Detect category emoji from config key.

    Args:
        key: Config key (e.g., "database.host")
        palette: Palette with emoji mappings

    Returns:
        Category emoji
    """
    # Extract first part of key (section name)
    section = key.split(".")[0].lower()
    return palette.emojis.get(section, "\u2699\ufe0f")  # ⚙️ default


def is_secret_key(key: str) -> bool:
    """
    Check if config key contains a secret.

    Args:
        key: Config key

    Returns:
        True if key appears to contain a secret
    """
    secret_keywords = ["password", "secret", "token", "key", "credential", "auth"]
    key_lower = key.lower()
    return any(keyword in key_lower for keyword in secret_keywords)


def redact_value(key: str, value: Any, palette: Palette) -> str:
    """
    Redact secret values.

    Args:
        key: Config key
        value: Config value
        palette: Palette for styling

    Returns:
        Original value or redacted placeholder
    """
    if is_secret_key(key):
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

    # Calculate column widths
    max_key_width = max(len(row[0]) + 4 for row in rows)  # +4 for emoji and spaces
    max_value_width = max(len(row[1]) for row in rows)

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
        display_key = f"{emoji}  {key}".ljust(max_key_width)
        display_value = value.ljust(max_value_width)

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
    Render ASCII art banner.

    Args:
        palette: Palette with banner configuration
        use_color: Whether to use colors

    Returns:
        Formatted banner string
    """
    lines = []

    # Banner ASCII art
    if palette.banner_text:
        if use_color:
            # Apply gradient effect to banner
            colored_banner = ansi_color(palette.border_color, palette.banner_text)
            lines.append(colored_banner)
        else:
            lines.append(palette.banner_text)

    # Title
    title = f"    {palette.banner_title}    "
    if use_color:
        title = ansi_bold(ansi_color(palette.header_bg, title))
    lines.append("")
    lines.append(title)
    lines.append("")

    return "\n".join(lines)
