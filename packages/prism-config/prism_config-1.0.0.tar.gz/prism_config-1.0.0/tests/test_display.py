"""
Tests for beautiful terminal display functionality.

This module tests the dump() and display() methods for rendering
configuration as beautiful tables with ANSI colors and box-drawing.
"""

from prism.config import PrismConfig, display


def test_dump_basic(prism_env):
    """
    Test 6.1: dump() returns formatted table string.

    Should render configuration as a beautiful table with box-drawing characters.
    """
    # ARRANGE
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb"
        }
    }

    config = PrismConfig.from_dict(config_data)

    # ACT
    output = config.dump(use_color=False)

    # ASSERT: Contains config values
    assert "test-app" in output
    assert "localhost" in output
    assert "5432" in output

    # ASSERT: Contains table structure
    assert "Configuration Key" in output
    assert "Value" in output


def test_secret_redaction(prism_env):
    """
    Test 6.2: Secrets are automatically redacted in dump().

    Keys containing 'password', 'secret', 'token', etc. should be redacted.
    """
    # ARRANGE
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "password": "super-secret-pass"
        }
    }

    config = PrismConfig.from_dict(config_data)

    # ACT
    output = config.dump(use_color=False)

    # ASSERT: Password is redacted
    assert "super-secret-pass" not in output
    assert "REDACTED" in output

    # ASSERT: Other values not redacted
    assert "localhost" in output
    assert "5432" in output


def test_flatten_config(prism_env):
    """
    Test 6.3: flatten_config converts nested dict to dot notation.

    Should flatten nested dictionaries for display in table format.
    """
    # ARRANGE
    nested = {
        "app": {
            "name": "test-app",
            "server": {
                "host": "localhost",
                "port": 8000
            }
        }
    }

    # ACT
    flat = display.flatten_config(nested)

    # ASSERT
    assert flat["app.name"] == "test-app"
    assert flat["app.server.host"] == "localhost"
    assert flat["app.server.port"] == 8000


def test_is_secret_key(prism_env):
    """
    Test 6.4: is_secret_key detects secret-like keys.

    Should identify keys containing password, secret, token, key, credential, auth.
    """
    # ASSERT: Secret keys detected
    assert display.is_secret_key("database.password") is True
    assert display.is_secret_key("api_secret") is True
    assert display.is_secret_key("auth_token") is True
    assert display.is_secret_key("encryption_key") is True
    assert display.is_secret_key("user_credentials") is True

    # ASSERT: Normal keys not detected
    assert display.is_secret_key("app.name") is False
    assert display.is_secret_key("database.host") is False
    assert display.is_secret_key("server.port") is False


def test_detect_category(prism_env):
    """
    Test 6.5: detect_category extracts emoji from config key.

    Should map config section names to category emojis.
    """
    # ARRANGE
    palette = display.load_palette()

    # ACT & ASSERT: Known sections return their emojis
    assert display.detect_category("app.name", palette) == palette.emojis["app"]
    assert display.detect_category("database.host", palette) == palette.emojis["database"]

    # Unknown sections should return a default emoji
    result = display.detect_category("unknown.field", palette)
    assert result is not None
    assert isinstance(result, str)


def test_should_use_color_no_color_env(prism_env):
    """
    Test 6.6: should_use_color respects NO_COLOR environment variable.

    NO_COLOR=1 should disable colors (standard convention).
    """
    # ARRANGE
    prism_env["monkeypatch"].setenv("NO_COLOR", "1")

    # ACT
    use_color = display.should_use_color()

    # ASSERT
    assert use_color is False


def test_should_use_color_prism_no_color(prism_env):
    """
    Test 6.7: should_use_color respects PRISM_NO_COLOR environment variable.

    PRISM_NO_COLOR=1 should disable colors (prism-specific override).
    """
    # ARRANGE
    prism_env["monkeypatch"].setenv("PRISM_NO_COLOR", "1")

    # ACT
    use_color = display.should_use_color()

    # ASSERT
    assert use_color is False


def test_render_table_basic(prism_env):
    """
    Test 6.8: render_table produces box-drawing table.

    Should use box-drawing characters for borders.
    """
    # ARRANGE
    rows = [
        ("app.name", "test-app"),
        ("database.host", "localhost"),
    ]
    palette = display.load_palette()

    # ACT
    table = display.render_table(rows, palette, use_color=False)

    # ASSERT: Contains data
    assert "test-app" in table
    assert "localhost" in table

    # ASSERT: Contains headers
    assert "Configuration Key" in table
    assert "Value" in table


def test_display_method(prism_env, capsys):
    """
    Test 6.9: display() prints banner and table to stdout.

    Should print both banner and config table.
    """
    # ARRANGE
    config_data = {
        "app": {"name": "test-app", "environment": "dev"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb"
        }
    }

    config = PrismConfig.from_dict(config_data)

    # ACT
    config.display(use_color=False)

    # ASSERT: Captured stdout
    captured = capsys.readouterr()
    assert "CONFIGURATION LOADED" in captured.out
    assert "test-app" in captured.out
    assert "localhost" in captured.out


def test_palette_load_default(prism_env):
    """
    Test 6.10: load_palette returns default palette if no file found.

    Should gracefully fall back to DEFAULT_PALETTE.
    """
    # ACT
    palette = display.load_palette()

    # ASSERT: Returns valid palette
    assert palette.header_bg == 197
    assert palette.key_color == 51
    assert palette.border_color == 213
    assert palette.box_style in ["single", "double", "rounded", "bold"]


def test_box_styles(prism_env):
    """
    Test 6.11: All box styles are properly defined.

    Should have complete character sets for all styles.
    """
    # ASSERT: All styles exist
    assert "single" in display.BOX_STYLES
    assert "double" in display.BOX_STYLES
    assert "rounded" in display.BOX_STYLES
    assert "bold" in display.BOX_STYLES

    # ASSERT: Each style has required characters
    for _, chars in display.BOX_STYLES.items():
        assert "horizontal" in chars
        assert "vertical" in chars
        assert "top_left" in chars
        assert "top_right" in chars
        assert "bottom_left" in chars
        assert "bottom_right" in chars
