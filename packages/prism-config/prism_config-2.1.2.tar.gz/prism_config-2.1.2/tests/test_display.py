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


# ============================================================================
# Iteration 15.1.9: Tests for expanded emoji mappings
# ============================================================================


def test_emoji_mappings_auth_security(prism_env):
    """
    Test 15.1.9a: Auth & security section emojis are defined.

    All auth/security related sections should have appropriate emojis.
    """
    # ARRANGE
    palette = display.load_palette()

    # ASSERT: Auth & security emojis exist
    auth_security_keys = [
        "auth", "jwt", "oauth", "session", "cors", "ssl", "tls",
        "credentials", "token", "password"
    ]

    for key in auth_security_keys:
        assert key in palette.emojis, f"Missing emoji for '{key}'"
        assert isinstance(palette.emojis[key], str), f"Emoji for '{key}' should be str"
        assert len(palette.emojis[key]) > 0, f"Emoji for '{key}' should not be empty"


def test_emoji_mappings_caching(prism_env):
    """
    Test 15.1.9b: Caching section emojis are defined.

    Redis, memcached and caching sections should have emojis.
    """
    # ARRANGE
    palette = display.load_palette()

    # ASSERT: Caching emojis exist
    caching_keys = ["redis", "memcached", "caching", "cache"]

    for key in caching_keys:
        assert key in palette.emojis, f"Missing emoji for '{key}'"


def test_emoji_mappings_messaging(prism_env):
    """
    Test 15.1.9c: Messaging section emojis are defined.

    Message queue and event-driven sections should have emojis.
    """
    # ARRANGE
    palette = display.load_palette()

    # ASSERT: Messaging emojis exist
    messaging_keys = [
        "kafka", "rabbitmq", "celery", "pubsub", "messaging",
        "events", "amqp", "sqs", "queue"
    ]

    for key in messaging_keys:
        assert key in palette.emojis, f"Missing emoji for '{key}'"


def test_emoji_mappings_cloud_providers(prism_env):
    """
    Test 15.1.9d: Cloud provider section emojis are defined.

    AWS, Azure, GCP and other cloud providers should have emojis.
    """
    # ARRANGE
    palette = display.load_palette()

    # ASSERT: Cloud provider emojis exist
    cloud_keys = [
        "aws", "azure", "gcp", "cloud", "s3", "lambda",
        "cloudflare", "digitalocean", "heroku"
    ]

    for key in cloud_keys:
        assert key in palette.emojis, f"Missing emoji for '{key}'"


def test_emoji_mappings_observability(prism_env):
    """
    Test 15.1.9e: Observability section emojis are defined.

    Logging, metrics, tracing and APM tools should have emojis.
    """
    # ARRANGE
    palette = display.load_palette()

    # ASSERT: Observability emojis exist
    observability_keys = [
        "logging", "log", "logs", "metrics", "tracing",
        "sentry", "datadog", "newrelic", "prometheus",
        "grafana", "opentelemetry", "otel", "monitoring"
    ]

    for key in observability_keys:
        assert key in palette.emojis, f"Missing emoji for '{key}'"


def test_emoji_mappings_infrastructure(prism_env):
    """
    Test 15.1.9f: HTTP/API infrastructure emojis are defined.

    HTTP, gRPC, websocket and API gateway sections should have emojis.
    """
    # ARRANGE
    palette = display.load_palette()

    # ASSERT: Infrastructure emojis exist
    infra_keys = [
        "http", "https", "grpc", "websocket", "graphql",
        "rest", "proxy", "gateway", "loadbalancer", "lb", "api"
    ]

    for key in infra_keys:
        assert key in palette.emojis, f"Missing emoji for '{key}'"


def test_emoji_mappings_business_features(prism_env):
    """
    Test 15.1.9g: Business/feature section emojis are defined.

    Feature flags, payments, email and notifications should have emojis.
    """
    # ARRANGE
    palette = display.load_palette()

    # ASSERT: Business/feature emojis exist
    business_keys = [
        "feature", "features", "flags", "payment", "payments",
        "stripe", "billing", "email", "smtp", "mail",
        "notifications", "sms", "push"
    ]

    for key in business_keys:
        assert key in palette.emojis, f"Missing emoji for '{key}'"


def test_emoji_mappings_rate_limiting(prism_env):
    """
    Test 15.1.9h: Rate limiting section emojis are defined.

    Rate limit, throttle and quota sections should have emojis.
    """
    # ARRANGE
    palette = display.load_palette()

    # ASSERT: Rate limiting emojis exist
    rate_limit_keys = ["rate_limit", "ratelimit", "throttle", "quota", "limits"]

    for key in rate_limit_keys:
        assert key in palette.emojis, f"Missing emoji for '{key}'"


def test_emoji_mappings_databases(prism_env):
    """
    Test 15.1.9i: Extended database section emojis are defined.

    PostgreSQL, MySQL, MongoDB and other databases should have emojis.
    """
    # ARRANGE
    palette = display.load_palette()

    # ASSERT: Database emojis exist
    db_keys = [
        "postgres", "postgresql", "mysql", "mongodb", "mongo",
        "elasticsearch", "elastic", "sqlite", "dynamodb", "database", "db"
    ]

    for key in db_keys:
        assert key in palette.emojis, f"Missing emoji for '{key}'"


def test_emoji_mappings_misc(prism_env):
    """
    Test 15.1.9j: Miscellaneous section emojis are defined.

    Config, environment, debug, test and deployment sections should have emojis.
    """
    # ARRANGE
    palette = display.load_palette()

    # ASSERT: Misc emojis exist
    misc_keys = [
        "config", "settings", "environment", "env", "debug",
        "test", "testing", "development", "dev", "production",
        "prod", "staging", "workers", "scheduler", "cron", "jobs", "tasks"
    ]

    for key in misc_keys:
        assert key in palette.emojis, f"Missing emoji for '{key}'"


def test_emoji_mappings_status_indicators(prism_env):
    """
    Test 15.1.9k: Status indicator emojis are defined.

    Internal status indicators for redaction and status should have emojis.
    """
    # ARRANGE
    palette = display.load_palette()

    # ASSERT: Status indicator emojis exist
    status_keys = ["secret_redacted", "loaded", "warning", "error"]

    for key in status_keys:
        assert key in palette.emojis, f"Missing emoji for '{key}'"


def test_detect_category_expanded(prism_env):
    """
    Test 15.1.9l: detect_category works with expanded emoji mappings.

    New section names should resolve to their correct emojis.
    """
    # ARRANGE
    palette = display.load_palette()

    # ACT & ASSERT: Expanded sections return their emojis
    test_cases = [
        ("auth.jwt.secret", "auth"),
        ("redis.host", "redis"),
        ("kafka.brokers", "kafka"),
        ("aws.region", "aws"),
        ("logging.level", "logging"),
        ("grpc.port", "grpc"),
        ("payment.stripe_key", "payment"),
        ("rate_limit.requests", "rate_limit"),
        ("postgres.host", "postgres"),
        ("sentry.dsn", "sentry"),
    ]

    for key, expected_section in test_cases:
        result = display.detect_category(key, palette)
        assert result == palette.emojis[expected_section], (
            f"detect_category('{key}') should return emoji for '{expected_section}'"
        )


def test_emoji_count(prism_env):
    """
    Test 15.1.9m: Palette contains at least 90 emoji mappings.

    The expanded palette should have comprehensive coverage.
    """
    # ARRANGE
    palette = display.load_palette()

    # ASSERT: At least 90 emoji mappings
    assert len(palette.emojis) >= 90, (
        f"Expected at least 90 emoji mappings, got {len(palette.emojis)}"
    )


def test_default_palette_emoji_count(prism_env):
    """
    Test 15.1.9n: DEFAULT_PALETTE has at least 90 emoji mappings.

    The code defaults should match the expanded emoji set.
    """
    # ARRANGE - Use DEFAULT_PALETTE directly (not from file)
    palette = display.DEFAULT_PALETTE

    # ASSERT: At least 90 emoji mappings in code defaults
    assert len(palette.emojis) >= 90, (
        f"DEFAULT_PALETTE should have at least 90 emoji mappings, got {len(palette.emojis)}"
    )


# ============================================================================
# Iteration 15.2: Smart Emoji Detection Tests
# ============================================================================


def test_smart_detection_partial_match(prism_env):
    """
    Test 15.2.1a: Partial matching detects emoji keys within section names.

    "jwt_config" should match "jwt", "redis_cache" should match "redis".
    """
    # ARRANGE
    palette = display.load_palette()

    # ACT & ASSERT: Partial matches work
    assert display.detect_category("jwt_config.secret", palette) == palette.emojis["jwt"]
    assert display.detect_category("redis_cache.host", palette) == palette.emojis["redis"]
    assert display.detect_category("kafka_producer.topic", palette) == palette.emojis["kafka"]
    assert display.detect_category("aws_s3.bucket", palette) == palette.emojis["aws"]


def test_smart_detection_prefix_suffix(prism_env):
    """
    Test 15.2.1b: Prefix and suffix matching works for section names.

    "auth_service" should match "auth", "my_database" should match "database".
    """
    # ARRANGE
    palette = display.load_palette()

    # ACT & ASSERT: Prefix matches
    assert display.detect_category("auth_service.timeout", palette) == palette.emojis["auth"]
    assert display.detect_category("database_primary.host", palette) == palette.emojis["database"]

    # ACT & ASSERT: Suffix matches
    assert display.detect_category("my_redis.port", palette) == palette.emojis["redis"]


def test_smart_detection_keyword_fallback(prism_env):
    """
    Test 15.2.2: Keyword detection uses fallback categories.

    "encryption_service" should fall back to "security" emoji.
    """
    # ARRANGE
    palette = display.load_palette()

    # ACT & ASSERT: Fallback keyword detection
    # Security-related
    assert display.detect_category("encryption_manager.key", palette) == palette.emojis["security"]

    # Auth-related
    assert display.detect_category("login_handler.timeout", palette) == palette.emojis["auth"]

    # Database-related
    assert display.detect_category("sql_executor.pool_size", palette) == palette.emojis["database"]


def test_smart_detection_exact_match_priority(prism_env):
    """
    Test 15.2.3: Exact match takes priority over partial match.

    "redis" should match exactly, not partially to something else.
    """
    # ARRANGE
    palette = display.load_palette()

    # ACT & ASSERT: Exact match should work first
    assert display.detect_category("redis.host", palette) == palette.emojis["redis"]
    assert display.detect_category("kafka.brokers", palette) == palette.emojis["kafka"]
    assert display.detect_category("auth.jwt.secret", palette) == palette.emojis["auth"]


def test_smart_detection_longest_match(prism_env):
    """
    Test 15.2.4: Longer matches take priority for partial matching.

    "postgresql" should match "postgresql" not just "postgres".
    """
    # ARRANGE
    palette = display.load_palette()

    # ACT & ASSERT: Longer matches should be preferred
    # Both "postgres" and "postgresql" are in the palette
    assert display.detect_category("postgresql.host", palette) == palette.emojis["postgresql"]
    assert display.detect_category("postgres_db.port", palette) == palette.emojis["postgres"]


def test_smart_detection_default_fallback(prism_env):
    """
    Test 15.2.5: Unknown sections return default gear emoji.

    Completely unknown sections should get ⚙️.
    """
    # ARRANGE
    palette = display.load_palette()
    default_emoji = "\u2699\ufe0f"  # ⚙️

    # ACT & ASSERT: Unknown sections get default
    assert display.detect_category("foobar.setting", palette) == default_emoji
    assert display.detect_category("xyz123.value", palette) == default_emoji
    assert display.detect_category("completely_random.field", palette) == default_emoji


def test_smart_detection_case_insensitive(prism_env):
    """
    Test 15.2.6: Smart detection is case insensitive.

    "REDIS", "Redis", and "redis" should all match.
    """
    # ARRANGE
    palette = display.load_palette()

    # ACT & ASSERT: Case insensitive matching
    result_lower = display.detect_category("redis.host", palette)
    result_upper = display.detect_category("REDIS.host", palette)
    result_mixed = display.detect_category("Redis.host", palette)

    assert result_lower == result_upper == result_mixed == palette.emojis["redis"]


def test_fallback_categories_defined(prism_env):
    """
    Test 15.2.7: FALLBACK_CATEGORIES constant is properly defined.

    Should have multiple categories with keyword lists.
    """
    # ASSERT: FALLBACK_CATEGORIES exists and has expected structure
    assert hasattr(display, 'FALLBACK_CATEGORIES')
    assert isinstance(display.FALLBACK_CATEGORIES, dict)
    assert len(display.FALLBACK_CATEGORIES) >= 5

    # ASSERT: Each category has a list of keywords
    for category, keywords in display.FALLBACK_CATEGORIES.items():
        assert isinstance(keywords, list), f"Category '{category}' should have list of keywords"
        assert len(keywords) > 0, f"Category '{category}' should have at least one keyword"


# ============================================================================
# Iteration 18.1: Dynamic Emoji Registration Tests
# ============================================================================


class TestRegisterEmoji:
    """Tests for the register_emoji function."""

    def setup_method(self):
        """Clear emoji registry before each test."""
        display.clear_registered_emojis()

    def teardown_method(self):
        """Clear emoji registry after each test."""
        display.clear_registered_emojis()

    def test_register_emoji_basic(self, prism_env):
        """Test 18.1.4a: Basic emoji registration works."""
        display.register_emoji("my_service", "🎯")
        emojis = display.get_registered_emojis()
        assert emojis == {"my_service": "🎯"}

    def test_register_emoji_case_insensitive(self, prism_env):
        """Test 18.1.4b: Section names are normalized to lowercase."""
        display.register_emoji("MyService", "🎯")
        display.register_emoji("ANOTHER_SERVICE", "🚀")

        emojis = display.get_registered_emojis()
        assert "myservice" in emojis
        assert "another_service" in emojis

    def test_register_emoji_override(self, prism_env):
        """Test 18.1.4c: Registering same section overwrites."""
        display.register_emoji("my_service", "🎯")
        display.register_emoji("my_service", "🚀")

        emojis = display.get_registered_emojis()
        assert emojis["my_service"] == "🚀"

    def test_register_emoji_multiple(self, prism_env):
        """Test 18.1.4d: Multiple emoji registrations work."""
        display.register_emoji("service_a", "🅰️")
        display.register_emoji("service_b", "🅱️")
        display.register_emoji("service_c", "©️")

        emojis = display.get_registered_emojis()
        assert len(emojis) == 3

    def test_register_emoji_unicode_escape(self, prism_env):
        """Test 18.1.4e: Unicode escape sequences work."""
        display.register_emoji("target", "\U0001f3af")  # 🎯
        emojis = display.get_registered_emojis()
        assert emojis["target"] == "🎯"


class TestUnregisterEmoji:
    """Tests for the unregister_emoji function."""

    def setup_method(self):
        """Clear emoji registry before each test."""
        display.clear_registered_emojis()

    def teardown_method(self):
        """Clear emoji registry after each test."""
        display.clear_registered_emojis()

    def test_unregister_emoji_success(self, prism_env):
        """Test 18.1.4f: Successful emoji unregistration."""
        display.register_emoji("my_service", "🎯")
        result = display.unregister_emoji("my_service")

        assert result is True
        assert display.get_registered_emojis() == {}

    def test_unregister_emoji_not_found(self, prism_env):
        """Test 18.1.4g: Unregistering non-existent emoji returns False."""
        result = display.unregister_emoji("nonexistent")
        assert result is False

    def test_unregister_emoji_case_insensitive(self, prism_env):
        """Test 18.1.4h: Unregistration is case insensitive."""
        display.register_emoji("MyService", "🎯")
        result = display.unregister_emoji("MYSERVICE")

        assert result is True
        assert display.get_registered_emojis() == {}


class TestGetRegisteredEmojis:
    """Tests for the get_registered_emojis function."""

    def setup_method(self):
        """Clear emoji registry before each test."""
        display.clear_registered_emojis()

    def teardown_method(self):
        """Clear emoji registry after each test."""
        display.clear_registered_emojis()

    def test_get_registered_emojis_empty(self, prism_env):
        """Test 18.1.4i: Getting emojis when none registered."""
        emojis = display.get_registered_emojis()
        assert emojis == {}

    def test_get_registered_emojis_returns_copy(self, prism_env):
        """Test 18.1.4j: Returned dict is a copy, not the original."""
        display.register_emoji("my_service", "🎯")
        emojis = display.get_registered_emojis()

        # Modify the returned dict
        emojis["other"] = "🔥"

        # Original should be unchanged
        assert "other" not in display.get_registered_emojis()


class TestClearRegisteredEmojis:
    """Tests for the clear_registered_emojis function."""

    def teardown_method(self):
        """Clear emoji registry after each test."""
        display.clear_registered_emojis()

    def test_clear_registered_emojis(self, prism_env):
        """Test 18.1.4k: Clearing all registered emojis."""
        display.register_emoji("service_a", "🅰️")
        display.register_emoji("service_b", "🅱️")

        display.clear_registered_emojis()

        assert display.get_registered_emojis() == {}


class TestDetectCategoryWithCustomEmojis:
    """Tests for detect_category with custom emoji registry."""

    def setup_method(self):
        """Clear emoji registry before each test."""
        display.clear_registered_emojis()

    def teardown_method(self):
        """Clear emoji registry after each test."""
        display.clear_registered_emojis()

    def test_custom_emoji_takes_priority(self, prism_env):
        """Test 18.1.4l: Custom emojis override built-in mappings."""
        palette = display.load_palette()

        # auth has a built-in emoji (🔑)
        builtin_emoji = display.detect_category("auth.enabled", palette)
        assert builtin_emoji == "🔑"

        # Register custom emoji for auth
        display.register_emoji("auth", "🔐")

        # Now should use custom emoji
        custom_emoji = display.detect_category("auth.enabled", palette)
        assert custom_emoji == "🔐"

    def test_custom_emoji_for_new_section(self, prism_env):
        """Test 18.1.4m: Custom emoji for section without built-in mapping."""
        palette = display.load_palette()
        display.register_emoji("my_custom_section", "🎯")

        emoji = display.detect_category("my_custom_section.value", palette)
        assert emoji == "🎯"

    def test_custom_emoji_case_insensitive_detection(self, prism_env):
        """Test 18.1.4n: Detection is case insensitive."""
        palette = display.load_palette()
        display.register_emoji("myservice", "🎯")

        # Key with different casing
        emoji = display.detect_category("MyService.timeout", palette)
        assert emoji == "🎯"

    def test_fallback_to_builtin_when_no_custom(self, prism_env):
        """Test 18.1.4o: Fallback to built-in emoji when no custom registered."""
        palette = display.load_palette()
        display.register_emoji("other_section", "🔥")

        # Database should still use built-in
        emoji = display.detect_category("database.host", palette)
        assert emoji == "💾"


class TestEmojiRegistrationIntegration:
    """Integration tests for emoji registration with PrismConfig."""

    def setup_method(self):
        """Clear emoji registry before each test."""
        display.clear_registered_emojis()

    def teardown_method(self):
        """Clear emoji registry after each test."""
        display.clear_registered_emojis()

    def test_dump_uses_custom_emoji(self, prism_env):
        """Test 18.1.4p: dump() uses custom registered emojis."""
        # Register custom emoji
        display.register_emoji("my_service", "🎯")

        # Create config with custom section
        config = PrismConfig.from_dict(
            {
                "app": {"name": "test", "environment": "dev"},
                "database": {"name": "testdb"},
                "my_service": {"timeout": 30},
            },
            strict=False,
        )

        # Dump should include our custom emoji
        output = config.dump(use_color=False)

        # Check that the section is in the output
        assert "my_service" in output
        assert "🎯" in output

    def test_multiple_custom_emojis_in_dump(self, prism_env):
        """Test 18.1.4q: dump with multiple custom emojis."""
        display.register_emoji("service_a", "🅰️")
        display.register_emoji("service_b", "🅱️")

        config = PrismConfig.from_dict(
            {
                "app": {"name": "test", "environment": "dev"},
                "database": {"name": "testdb"},
                "service_a": {"enabled": True},
                "service_b": {"enabled": False},
            },
            strict=False,
        )

        output = config.dump(use_color=False)

        assert "🅰️" in output
        assert "🅱️" in output


class TestEmojiRegistrationFromInit:
    """Tests for emoji registration functions exported from __init__.py."""

    def setup_method(self):
        """Clear emoji registry before each test."""
        from prism.config import clear_registered_emojis
        clear_registered_emojis()

    def teardown_method(self):
        """Clear emoji registry after each test."""
        from prism.config import clear_registered_emojis
        clear_registered_emojis()

    def test_register_emoji_from_init(self, prism_env):
        """Test 18.1.4r: register_emoji is accessible from prism.config."""
        from prism.config import register_emoji, get_registered_emojis

        register_emoji("my_section", "🎯")
        emojis = get_registered_emojis()
        assert "my_section" in emojis

    def test_all_emoji_functions_exported(self, prism_env):
        """Test 18.1.4s: All emoji functions are exported from __init__.py."""
        from prism.config import (
            register_emoji,
            unregister_emoji,
            get_registered_emojis,
            clear_registered_emojis,
        )

        # Should not raise ImportError
        assert callable(register_emoji)
        assert callable(unregister_emoji)
        assert callable(get_registered_emojis)
        assert callable(clear_registered_emojis)


# ============================================================================
# Iteration 18.2: Nested Section Support Tests
# ============================================================================


class TestHierarchicalEmojiDetection:
    """Tests for hierarchical emoji detection in nested configs."""

    def test_hierarchical_fallback_first_level(self, prism_env):
        """Test 18.2.4a: First level section takes priority."""
        palette = display.load_palette()

        # "database.host" - database is first, should match
        emoji = display.detect_category("database.host", palette)
        assert emoji == "💾"

    def test_hierarchical_fallback_second_level(self, prism_env):
        """Test 18.2.4b: Falls back to second level if first doesn't match."""
        palette = display.load_palette()

        # "services.auth.jwt.secret" - services doesn't match, auth should
        emoji = display.detect_category("services.auth.jwt.secret", palette)
        assert emoji == "🔑"  # auth emoji

    def test_hierarchical_fallback_third_level(self, prism_env):
        """Test 18.2.4c: Falls back to third level if needed."""
        palette = display.load_palette()

        # "services.config.redis.host" - services doesn't match, config is generic, redis should
        emoji = display.detect_category("unknown.foobar.redis.host", palette)
        assert emoji == "🔴"  # redis emoji

    def test_hierarchical_first_match_wins(self, prism_env):
        """Test 18.2.4d: First matching level wins over later levels."""
        palette = display.load_palette()

        # "auth.redis.host" - auth matches first, even though redis also exists
        emoji = display.detect_category("auth.redis.host", palette)
        assert emoji == "🔑"  # auth emoji, not redis

    def test_hierarchical_all_levels_unknown(self, prism_env):
        """Test 18.2.4e: Returns default if no level matches."""
        palette = display.load_palette()
        default_emoji = "\u2699\ufe0f"  # ⚙️

        emoji = display.detect_category("foo.bar.baz.qux", palette)
        assert emoji == default_emoji

    def test_hierarchical_deeply_nested(self, prism_env):
        """Test 18.2.4f: Works with very deeply nested keys."""
        palette = display.load_palette()

        # 6 levels deep, kafka should match
        emoji = display.detect_category("a.b.c.d.kafka.config", palette)
        assert emoji == "📬"  # kafka emoji


class TestFlattenConfigMaxDepth:
    """Tests for flatten_config with max_depth parameter."""

    def test_flatten_unlimited_depth(self, prism_env):
        """Test 18.2.4g: Unlimited depth flattens all levels."""
        data = {"a": {"b": {"c": {"d": 1}}}}
        result = display.flatten_config(data)

        assert "a.b.c.d" in result
        assert result["a.b.c.d"] == 1

    def test_flatten_depth_1(self, prism_env):
        """Test 18.2.4h: max_depth=1 stops after first level."""
        data = {"a": {"b": {"c": 1}}}
        result = display.flatten_config(data, max_depth=1)

        # At depth 1, nested dicts are stringified at the first level
        assert "a" in result
        # The nested dict should be stringified
        assert "b" in str(result["a"])

    def test_flatten_depth_2(self, prism_env):
        """Test 18.2.4i: max_depth=2 stops after second level."""
        data = {"a": {"b": {"c": {"d": 1}}}}
        result = display.flatten_config(data, max_depth=2)

        # At depth 2, we get a.b with stringified nested value
        assert "a.b" in result
        # c should be in the stringified result
        assert "c" in str(result["a.b"])

    def test_flatten_depth_respects_shallow_values(self, prism_env):
        """Test 18.2.4j: max_depth doesn't affect shallow values."""
        data = {"a": 1, "b": {"c": 2}}
        result = display.flatten_config(data, max_depth=1)

        # Shallow value a is preserved
        assert result["a"] == 1
        # b is at depth 1, so it gets stringified
        assert "b" in result
        assert "c" in str(result["b"])


class TestPaletteMaxDepth:
    """Tests for Palette max_depth configuration."""

    def test_palette_default_max_depth(self, prism_env):
        """Test 18.2.4k: Palette defaults to unlimited max_depth."""
        palette = display.Palette()
        assert palette.max_depth is None

    def test_palette_custom_max_depth(self, prism_env):
        """Test 18.2.4l: Palette accepts custom max_depth."""
        palette = display.Palette(max_depth=3)
        assert palette.max_depth == 3

    def test_default_palette_max_depth(self, prism_env):
        """Test 18.2.4m: DEFAULT_PALETTE has unlimited max_depth."""
        assert display.DEFAULT_PALETTE.max_depth is None


class TestNestedConfigDisplay:
    """Integration tests for displaying deeply nested configurations."""

    def setup_method(self):
        """Clear emoji registry before each test."""
        display.clear_registered_emojis()

    def teardown_method(self):
        """Clear emoji registry after each test."""
        display.clear_registered_emojis()

    def test_deeply_nested_config_dump(self, prism_env):
        """Test 18.2.4n: dump() works with deeply nested configs."""
        config = PrismConfig.from_dict(
            {
                "app": {"name": "test", "environment": "dev"},
                "database": {"name": "testdb"},
                "services": {
                    "email": {
                        "smtp": {
                            "host": "mail.example.com",
                            "port": 587,
                        }
                    }
                },
            },
            strict=False,
        )

        output = config.dump(use_color=False)

        # Should contain the nested values
        assert "services.email.smtp.host" in output
        assert "mail.example.com" in output
        assert "services.email.smtp.port" in output
        assert "587" in output

    def test_nested_section_gets_hierarchical_emoji(self, prism_env):
        """Test 18.2.4o: Nested sections use hierarchical emoji detection."""
        # Register a custom emoji for a nested section
        display.register_emoji("myservice", "🎯")

        config = PrismConfig.from_dict(
            {
                "app": {"name": "test", "environment": "dev"},
                "database": {"name": "testdb"},
                "myservice": {
                    "auth": {
                        "enabled": True,
                    }
                },
            },
            strict=False,
        )

        output = config.dump(use_color=False)

        # myservice should use the custom emoji
        assert "🎯" in output


# ============================================================================
# Iteration 18.3: Extended Secret Detection Tests
# ============================================================================


class TestIsSecretKeyBuiltIn:
    """Tests for built-in secret detection."""

    def test_detects_password(self, prism_env):
        """Test 18.3.4a: Detects password in key."""
        assert display.is_secret_key("database.password") is True
        assert display.is_secret_key("PASSWORD") is True
        assert display.is_secret_key("db_password_hash") is True

    def test_detects_secret(self, prism_env):
        """Test 18.3.4b: Detects secret in key."""
        assert display.is_secret_key("jwt.secret") is True
        assert display.is_secret_key("SECRET_KEY") is True
        assert display.is_secret_key("client_secret") is True

    def test_detects_token(self, prism_env):
        """Test 18.3.4c: Detects token in key."""
        assert display.is_secret_key("api.token") is True
        assert display.is_secret_key("access_token") is True
        assert display.is_secret_key("TOKEN_VALUE") is True

    def test_detects_api_key_with_boundary(self, prism_env):
        """Test 18.3.4d: Detects key only at word boundaries."""
        assert display.is_secret_key("api_key") is True
        assert display.is_secret_key("stripe.key") is True
        assert display.is_secret_key("aws_access_key") is True
        # Should NOT match key as substring
        assert display.is_secret_key("expiry") is False
        assert display.is_secret_key("turkey") is False
        assert display.is_secret_key("monkey") is False

    def test_detects_credential(self, prism_env):
        """Test 18.3.4e: Detects credential in key."""
        assert display.is_secret_key("credentials") is True
        assert display.is_secret_key("user_credential") is True

    def test_non_secret_keys(self, prism_env):
        """Test 18.3.4f: Non-secret keys are not detected."""
        assert display.is_secret_key("database.host") is False
        assert display.is_secret_key("app.name") is False
        assert display.is_secret_key("server.port") is False
        assert display.is_secret_key("environment") is False


class TestCustomSecretKeywords:
    """Tests for custom secret keywords via Palette."""

    def test_custom_keyword_detected(self, prism_env):
        """Test 18.3.4g: Custom keywords are detected."""
        palette = display.Palette(secret_keywords=["private", "confidential"])

        assert display.is_secret_key("private_data", palette) is True
        assert display.is_secret_key("confidential_info", palette) is True
        # Non-matching keys still not detected
        assert display.is_secret_key("public_data", palette) is False

    def test_custom_keyword_case_insensitive(self, prism_env):
        """Test 18.3.4h: Custom keywords are case insensitive."""
        palette = display.Palette(secret_keywords=["PRIVATE"])

        assert display.is_secret_key("private_key", palette) is True
        assert display.is_secret_key("PRIVATE_KEY", palette) is True
        assert display.is_secret_key("Private_Key", palette) is True

    def test_custom_keyword_with_builtin(self, prism_env):
        """Test 18.3.4i: Custom keywords work with built-in."""
        palette = display.Palette(secret_keywords=["ssn"])

        # Built-in still works
        assert display.is_secret_key("password", palette) is True
        # Custom also works
        assert display.is_secret_key("user_ssn", palette) is True


class TestCustomSecretPatterns:
    """Tests for custom secret regex patterns via Palette."""

    def test_custom_pattern_detected(self, prism_env):
        """Test 18.3.4j: Custom regex patterns are detected."""
        # Match any key ending in _id
        palette = display.Palette(secret_patterns=[r"_id$"])

        assert display.is_secret_key("user_id", palette) is True
        assert display.is_secret_key("customer_id", palette) is True
        # Doesn't match
        assert display.is_secret_key("identifier", palette) is False

    def test_custom_pattern_complex_regex(self, prism_env):
        """Test 18.3.4k: Complex regex patterns work."""
        # Match patterns like env_ABC_secret or prod_XYZ_token
        palette = display.Palette(secret_patterns=[r"(env|prod|dev)_\w+_(secret|token)"])

        assert display.is_secret_key("env_stripe_secret", palette) is True
        assert display.is_secret_key("prod_api_token", palette) is True
        # Doesn't match
        assert display.is_secret_key("staging_config", palette) is False

    def test_custom_pattern_invalid_regex(self, prism_env):
        """Test 18.3.4l: Invalid regex patterns are skipped gracefully."""
        # Invalid regex pattern
        palette = display.Palette(secret_patterns=["[invalid"])

        # Should not raise, just skip the invalid pattern
        # Note: use a key that doesn't match any built-in patterns
        assert display.is_secret_key("database.host", palette) is False
        # Built-in still works
        assert display.is_secret_key("password", palette) is True

    def test_multiple_patterns(self, prism_env):
        """Test 18.3.4m: Multiple patterns work."""
        palette = display.Palette(secret_patterns=[
            r"_ssn$",
            r"^pin_",
            r"cvv",
        ])

        assert display.is_secret_key("user_ssn", palette) is True
        assert display.is_secret_key("pin_code", palette) is True
        assert display.is_secret_key("card_cvv", palette) is True


class TestPaletteSecretSettings:
    """Tests for Palette secret detection settings."""

    def test_palette_default_secret_settings(self, prism_env):
        """Test 18.3.4n: Palette defaults to no custom secret settings."""
        palette = display.Palette()
        assert palette.secret_keywords is None
        assert palette.secret_patterns is None

    def test_palette_custom_secret_keywords(self, prism_env):
        """Test 18.3.4o: Palette accepts custom secret keywords."""
        palette = display.Palette(secret_keywords=["private", "internal"])
        assert palette.secret_keywords == ["private", "internal"]

    def test_palette_custom_secret_patterns(self, prism_env):
        """Test 18.3.4p: Palette accepts custom secret patterns."""
        palette = display.Palette(secret_patterns=[r"_id$", r"^api_"])
        assert palette.secret_patterns == [r"_id$", r"^api_"]


class TestRedactValueWithCustomSecrets:
    """Tests for redact_value with custom secret detection."""

    def test_redact_with_custom_keyword(self, prism_env):
        """Test 18.3.4q: redact_value uses custom keywords."""
        palette = display.Palette(secret_keywords=["ssn"])

        result = display.redact_value("user_ssn", "123-45-6789", palette)
        assert "REDACTED" in result
        assert "123-45-6789" not in result

    def test_redact_with_custom_pattern(self, prism_env):
        """Test 18.3.4r: redact_value uses custom patterns."""
        palette = display.Palette(secret_patterns=[r"pin_\d+"])

        result = display.redact_value("pin_123", "4567", palette)
        assert "REDACTED" in result
        assert "4567" not in result

    def test_no_redact_without_match(self, prism_env):
        """Test 18.3.4s: No redaction when key doesn't match."""
        palette = display.Palette(secret_keywords=["ssn"])

        result = display.redact_value("user_name", "John Doe", palette)
        assert result == "John Doe"
