# Copyright (c) 2025 Itential, Inc
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import re

import pytest

from ipsdk import heuristics


class TestScannerSingleton:
    """Test Scanner singleton pattern behavior."""

    def setup_method(self):
        """Reset singleton before each test."""
        heuristics.Scanner.reset_singleton()

    def teardown_method(self):
        """Reset singleton after each test."""
        heuristics.Scanner.reset_singleton()

    def test_scanner_singleton_returns_same_instance(self):
        """Test that Scanner returns the same instance."""
        scanner1 = heuristics.Scanner()
        scanner2 = heuristics.Scanner()
        assert scanner1 is scanner2

    def test_scanner_singleton_initialization_once(self):
        """Test that Scanner only initializes patterns once."""
        scanner1 = heuristics.Scanner()
        initial_patterns = len(scanner1.list_patterns())

        # Create another instance - should not reinitialize
        scanner2 = heuristics.Scanner()
        assert len(scanner2.list_patterns()) == initial_patterns

    def test_scanner_reset_singleton(self):
        """Test that reset_singleton allows new instance creation."""
        scanner1 = heuristics.Scanner()
        id1 = id(scanner1)

        heuristics.Scanner.reset_singleton()

        scanner2 = heuristics.Scanner()
        id2 = id(scanner2)

        assert id1 != id2


class TestScannerInitialization:
    """Test Scanner initialization."""

    def setup_method(self):
        """Reset singleton before each test."""
        heuristics.Scanner.reset_singleton()

    def teardown_method(self):
        """Reset singleton after each test."""
        heuristics.Scanner.reset_singleton()

    def test_scanner_initialization_no_custom_patterns(self):
        """Test Scanner initializes with default patterns only."""
        scanner = heuristics.Scanner()
        patterns = scanner.list_patterns()

        # Should have default patterns
        assert len(patterns) > 0
        assert "api_key" in patterns
        assert "password" in patterns
        assert "bearer_token" in patterns

    def test_scanner_initialization_with_custom_patterns(self):
        """Test Scanner initializes with custom patterns."""
        custom_patterns = {
            "custom1": r"CUSTOM1:\s*(\w+)",
            "custom2": r"CUSTOM2:\s*(\w+)",
        }

        scanner = heuristics.Scanner(custom_patterns)
        patterns = scanner.list_patterns()

        # Should have default and custom patterns
        assert "api_key" in patterns
        assert "custom1" in patterns
        assert "custom2" in patterns

    def test_scanner_default_patterns_exist(self):
        """Test that all expected default patterns are initialized."""
        scanner = heuristics.Scanner()
        patterns = scanner.list_patterns()

        expected_patterns = [
            "api_key",
            "bearer_token",
            "jwt_token",
            "access_token",
            "password",
            "secret",
            "auth_url",
            "email_in_auth",
            "db_connection",
            "private_key",
        ]

        for pattern_name in expected_patterns:
            assert pattern_name in patterns, (
                f"Expected pattern '{pattern_name}' not found"
            )


class TestPatternManagement:
    """Test pattern add, remove, and list operations."""

    def setup_method(self):
        """Reset singleton before each test."""
        heuristics.Scanner.reset_singleton()

    def teardown_method(self):
        """Reset singleton after each test."""
        heuristics.Scanner.reset_singleton()

    def test_add_pattern_basic(self):
        """Test adding a new pattern."""
        scanner = heuristics.Scanner()
        initial_count = len(scanner.list_patterns())

        scanner.add_pattern("test_pattern", r"TEST:\s*(\w+)")

        assert len(scanner.list_patterns()) == initial_count + 1
        assert "test_pattern" in scanner.list_patterns()

    def test_add_pattern_with_custom_redaction(self):
        """Test adding a pattern with custom redaction function."""
        scanner = heuristics.Scanner()

        def custom_redaction(match):
            return "[CUSTOM_REDACT]"

        scanner.add_pattern("test_pattern", r"TEST:\s*(\w+)", custom_redaction)

        result = scanner.scan_and_redact("TEST: secret123")
        assert "[CUSTOM_REDACT]" in result

    def test_add_pattern_invalid_regex(self):
        """Test adding a pattern with invalid regex raises error."""
        scanner = heuristics.Scanner()

        with pytest.raises(re.error):
            scanner.add_pattern("bad_pattern", r"[invalid(regex")

    def test_remove_pattern_exists(self):
        """Test removing an existing pattern."""
        scanner = heuristics.Scanner()
        scanner.add_pattern("test_pattern", r"TEST:\s*(\w+)")

        result = scanner.remove_pattern("test_pattern")

        assert result is True
        assert "test_pattern" not in scanner.list_patterns()

    def test_remove_pattern_not_exists(self):
        """Test removing a non-existent pattern returns False."""
        scanner = heuristics.Scanner()

        result = scanner.remove_pattern("nonexistent")

        assert result is False

    def test_list_patterns_returns_list(self):
        """Test list_patterns returns a list of pattern names."""
        scanner = heuristics.Scanner()

        patterns = scanner.list_patterns()

        assert isinstance(patterns, list)
        assert len(patterns) > 0
        assert all(isinstance(p, str) for p in patterns)


class TestScanAndRedact:
    """Test scan_and_redact functionality."""

    def setup_method(self):
        """Reset singleton before each test."""
        heuristics.Scanner.reset_singleton()

    def teardown_method(self):
        """Reset singleton after each test."""
        heuristics.Scanner.reset_singleton()

    def test_scan_and_redact_api_key(self):
        """Test redaction of API key."""
        scanner = heuristics.Scanner()

        text = "api_key=abc123def456ghi789"
        result = scanner.scan_and_redact(text)

        assert "abc123def456ghi789" not in result
        assert "[REDACTED_API_KEY]" in result

    def test_scan_and_redact_password(self):
        """Test redaction of password."""
        scanner = heuristics.Scanner()

        text = "password=mySecretPass123"
        result = scanner.scan_and_redact(text)

        assert "mySecretPass123" not in result
        assert "[REDACTED_PASSWORD]" in result

    def test_scan_and_redact_bearer_token(self):
        """Test redaction of bearer token."""
        scanner = heuristics.Scanner()

        text = "Bearer abcdefghijklmnopqrstuvwxyz123456"
        result = scanner.scan_and_redact(text)

        assert "abcdefghijklmnopqrstuvwxyz123456" not in result
        assert "[REDACTED_BEARER_TOKEN]" in result

    def test_scan_and_redact_jwt_token(self):
        """Test redaction of JWT token."""
        scanner = heuristics.Scanner()

        text = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"  # noqa: E501
        result = scanner.scan_and_redact(text)

        assert "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" not in result
        assert "[REDACTED_JWT_TOKEN]" in result

    def test_scan_and_redact_multiple_patterns(self):
        """Test redaction of multiple sensitive patterns in one text."""
        scanner = heuristics.Scanner()

        text = "api_key=secret1234567890abcd password=mypass456"
        result = scanner.scan_and_redact(text)

        assert "secret1234567890abcd" not in result
        assert "mypass456" not in result
        assert "[REDACTED_API_KEY]" in result
        assert "[REDACTED_PASSWORD]" in result

    def test_scan_and_redact_empty_string(self):
        """Test scan_and_redact with empty string."""
        scanner = heuristics.Scanner()

        result = scanner.scan_and_redact("")

        assert result == ""

    def test_scan_and_redact_none(self):
        """Test scan_and_redact with None."""
        scanner = heuristics.Scanner()

        result = scanner.scan_and_redact(None)

        assert result is None

    def test_scan_and_redact_no_sensitive_data(self):
        """Test scan_and_redact with clean text."""
        scanner = heuristics.Scanner()

        text = "This is a clean message with no secrets"
        result = scanner.scan_and_redact(text)

        assert result == text

    def test_scan_and_redact_auth_url(self):
        """Test redaction of authentication URL."""
        scanner = heuristics.Scanner()

        text = "https://user:password@example.com/path"
        result = scanner.scan_and_redact(text)

        assert "user:password@example.com" not in result
        assert "[REDACTED_AUTH_URL]" in result

    def test_scan_and_redact_db_connection(self):
        """Test redaction of database connection string."""
        scanner = heuristics.Scanner()

        text = "mongodb://admin:secret@localhost:27017/mydb"
        result = scanner.scan_and_redact(text)

        assert "admin:secret@localhost" not in result
        assert "[REDACTED_DB_CONNECTION]" in result

    def test_scan_and_redact_private_key(self):
        """Test redaction of private key."""
        scanner = heuristics.Scanner()

        text = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7VJTUt9Us8cKj
-----END PRIVATE KEY-----"""
        result = scanner.scan_and_redact(text)

        assert (
            "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7VJTUt9Us8cKj"
            not in result
        )
        assert "[REDACTED_PRIVATE_KEY]" in result


class TestHasSensitiveData:
    """Test has_sensitive_data detection."""

    def setup_method(self):
        """Reset singleton before each test."""
        heuristics.Scanner.reset_singleton()

    def teardown_method(self):
        """Reset singleton after each test."""
        heuristics.Scanner.reset_singleton()

    def test_has_sensitive_data_api_key(self):
        """Test detection of API key."""
        scanner = heuristics.Scanner()

        text = "api_key=abc123def456ghi789"
        result = scanner.has_sensitive_data(text)

        assert result is True

    def test_has_sensitive_data_password(self):
        """Test detection of password."""
        scanner = heuristics.Scanner()

        text = "password=mySecretPass123"
        result = scanner.has_sensitive_data(text)

        assert result is True

    def test_has_sensitive_data_clean_text(self):
        """Test no detection on clean text."""
        scanner = heuristics.Scanner()

        text = "This is a clean message"
        result = scanner.has_sensitive_data(text)

        assert result is False

    def test_has_sensitive_data_empty_string(self):
        """Test has_sensitive_data with empty string."""
        scanner = heuristics.Scanner()

        result = scanner.has_sensitive_data("")

        assert result is False

    def test_has_sensitive_data_none(self):
        """Test has_sensitive_data with None."""
        scanner = heuristics.Scanner()

        result = scanner.has_sensitive_data(None)

        assert result is False


class TestGetSensitiveDataTypes:
    """Test get_sensitive_data_types detection."""

    def setup_method(self):
        """Reset singleton before each test."""
        heuristics.Scanner.reset_singleton()

    def teardown_method(self):
        """Reset singleton after each test."""
        heuristics.Scanner.reset_singleton()

    def test_get_sensitive_data_types_api_key(self):
        """Test detection returns API key type."""
        scanner = heuristics.Scanner()

        text = "api_key=abc123def456ghi789"
        result = scanner.get_sensitive_data_types(text)

        assert isinstance(result, list)
        assert "api_key" in result

    def test_get_sensitive_data_types_multiple(self):
        """Test detection of multiple types."""
        scanner = heuristics.Scanner()

        text = "api_key=secret1234567890abcd password=mypass456"
        result = scanner.get_sensitive_data_types(text)

        assert isinstance(result, list)
        assert "api_key" in result
        assert "password" in result
        assert len(result) >= 2

    def test_get_sensitive_data_types_clean_text(self):
        """Test returns empty list for clean text."""
        scanner = heuristics.Scanner()

        text = "This is a clean message"
        result = scanner.get_sensitive_data_types(text)

        assert isinstance(result, list)
        assert len(result) == 0

    def test_get_sensitive_data_types_empty_string(self):
        """Test returns empty list for empty string."""
        scanner = heuristics.Scanner()

        result = scanner.get_sensitive_data_types("")

        assert isinstance(result, list)
        assert len(result) == 0

    def test_get_sensitive_data_types_none(self):
        """Test returns empty list for None."""
        scanner = heuristics.Scanner()

        result = scanner.get_sensitive_data_types(None)

        assert isinstance(result, list)
        assert len(result) == 0


class TestModuleFunctions:
    """Test module-level convenience functions."""

    def setup_method(self):
        """Reset singleton before each test."""
        heuristics.Scanner.reset_singleton()

    def teardown_method(self):
        """Reset singleton after each test."""
        heuristics.Scanner.reset_singleton()

    def test_get_scanner_returns_singleton(self):
        """Test get_scanner returns Scanner singleton."""
        scanner1 = heuristics.get_scanner()
        scanner2 = heuristics.get_scanner()

        assert scanner1 is scanner2
        assert isinstance(scanner1, heuristics.Scanner)

    def test_configure_scanner_with_custom_patterns(self):
        """Test configure_scanner adds custom patterns."""
        custom_patterns = {"custom": r"CUSTOM:\s*(\w+)"}

        scanner = heuristics.configure_scanner(custom_patterns)

        assert isinstance(scanner, heuristics.Scanner)
        assert "custom" in scanner.list_patterns()

    def test_configure_scanner_resets_singleton(self):
        """Test configure_scanner resets singleton."""
        scanner1 = heuristics.get_scanner()
        scanner1.add_pattern("temp", r"TEMP")

        scanner2 = heuristics.configure_scanner()

        assert "temp" not in scanner2.list_patterns()

    def test_configure_scanner_with_none(self):
        """Test configure_scanner with None patterns."""
        scanner = heuristics.configure_scanner(None)

        assert isinstance(scanner, heuristics.Scanner)
        # Should still have default patterns
        assert len(scanner.list_patterns()) > 0

    def test_scan_and_redact_module_function(self):
        """Test module-level scan_and_redact function."""
        heuristics.Scanner.reset_singleton()  # Reset for clean test
        text = "api_key=secret1234567890abcd"
        result = heuristics.scan_and_redact(text)

        assert "secret1234567890abcd" not in result
        assert "[REDACTED_API_KEY]" in result

    def test_has_sensitive_data_module_function(self):
        """Test module-level has_sensitive_data function."""
        heuristics.Scanner.reset_singleton()  # Reset for clean test
        text = "api_key=secret1234567890abcd"
        result = heuristics.has_sensitive_data(text)

        assert result is True

    def test_has_sensitive_data_module_function_clean(self):
        """Test module-level has_sensitive_data with clean text."""
        text = "This is clean"
        result = heuristics.has_sensitive_data(text)

        assert result is False


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def setup_method(self):
        """Reset singleton before each test."""
        heuristics.Scanner.reset_singleton()

    def teardown_method(self):
        """Reset singleton after each test."""
        heuristics.Scanner.reset_singleton()

    def test_add_pattern_replaces_existing(self):
        """Test adding a pattern with existing name replaces it."""
        scanner = heuristics.Scanner()

        scanner.add_pattern("test", r"TEST1")
        scanner.add_pattern("test", r"TEST2")  # Should replace

        # Pattern count should not increase
        patterns = scanner.list_patterns()
        assert patterns.count("test") == 1

    def test_scan_and_redact_case_insensitive_api_key(self):
        """Test case insensitive matching for api_key."""
        scanner = heuristics.Scanner()

        # Test various case combinations (api_key requires 16+ chars)
        texts = [
            "API_KEY=secret1234567890abcd",
            "Api_Key=secret1234567890abcd",
            "api-key=secret1234567890abcd",
            "APIKEY=secret1234567890abcd",
        ]

        for text in texts:
            result = scanner.scan_and_redact(text)
            assert "secret1234567890abcd" not in result
            assert "[REDACTED_API_KEY]" in result

    def test_scan_and_redact_preserves_non_sensitive(self):
        """Test that non-sensitive parts of text are preserved."""
        scanner = heuristics.Scanner()

        text = "Hello api_key=secret1234567890abcd World"
        result = scanner.scan_and_redact(text)

        assert "Hello" in result
        assert "World" in result
        assert "secret1234567890abcd" not in result

    def test_scanner_with_complex_custom_pattern(self):
        """Test scanner with complex regex pattern."""
        scanner = heuristics.Scanner()

        # Complex pattern with groups and alternation
        pattern = r"(?:SSN|social[_-]?security):\s*(\d{3}-\d{2}-\d{4})"
        scanner.add_pattern("ssn", pattern)

        text = "SSN: 123-45-6789"
        result = scanner.scan_and_redact(text)

        assert "123-45-6789" not in result
        assert "[REDACTED_SSN]" in result

    def test_redaction_function_receives_full_match(self):
        """Test that custom redaction function receives the full match."""
        scanner = heuristics.Scanner()

        captured_match = []

        def capture_redaction(match):
            captured_match.append(match)
            return "[REDACTED]"

        scanner.add_pattern("test", r"SECRET:\s*(\w+)", capture_redaction)
        scanner.scan_and_redact("SECRET: password123")

        assert len(captured_match) == 1
        assert "SECRET:" in captured_match[0]
        assert "password123" in captured_match[0]


class TestRealWorldScenarios:
    """Test real-world usage scenarios."""

    def setup_method(self):
        """Reset singleton before each test."""
        heuristics.Scanner.reset_singleton()

    def teardown_method(self):
        """Reset singleton after each test."""
        heuristics.Scanner.reset_singleton()

    def test_log_message_with_credentials(self):
        """Test redacting credentials from a log message."""
        scanner = heuristics.Scanner()

        log_msg = "Failed to authenticate with password=Secr3t! for user admin"
        result = scanner.scan_and_redact(log_msg)

        assert "Secr3t!" not in result
        assert "Failed to authenticate" in result
        assert "for user admin" in result

    def test_config_file_content(self):
        """Test redacting sensitive data from config-like content."""
        scanner = heuristics.Scanner()

        config = """
        [database]
        host=localhost
        user=admin
        password=SuperSecret123

        [api]
        api_key=abcdef123456789012345678
        """

        result = scanner.scan_and_redact(config)

        assert "SuperSecret123" not in result
        assert "abcdef123456789012345678" not in result
        assert "host=localhost" in result
        assert "user=admin" in result

    def test_json_like_structure(self):
        """Test redacting sensitive data from config-like structure."""
        scanner = heuristics.Scanner()

        # Config-style format (not quoted JSON keys) that patterns can match
        config_str = (
            "username: admin, password: secret123, api_key: key_abcdef1234567890"
        )
        result = scanner.scan_and_redact(config_str)

        assert "secret123" not in result
        assert "key_abcdef1234567890" not in result
        assert "username" in result

    def test_multiple_secrets_same_line(self):
        """Test redacting multiple secrets on the same line."""
        scanner = heuristics.Scanner()

        text = "Credentials: password=pass123 api_key=key1234567890abcdef secret=sec1234567890abcdef"  # noqa: E501
        result = scanner.scan_and_redact(text)

        assert "pass123" not in result
        assert "key1234567890abcdef" not in result
        assert "sec1234567890abcdef" not in result
        assert result.count("[REDACTED_") >= 3
