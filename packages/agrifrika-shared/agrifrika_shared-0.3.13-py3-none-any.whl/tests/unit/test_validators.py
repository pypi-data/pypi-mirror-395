"""Tests for validation utility functions."""

import pytest
from agrifrika_shared.utils.validators import (
    validate_email,
    validate_phone,
    validate_url,
    validate_uuid,
    sanitize_string,
    validate_password_strength,
)


@pytest.mark.unit
class TestValidateEmail:
    """Tests for email validation."""

    def test_valid_emails(self):
        """Test that valid email addresses are accepted."""
        valid_emails = [
            "test@example.com",
            "user.name@domain.com",
            "user+tag@example.co.uk",
            "firstname.lastname@company.org",
            "user_123@test-domain.com",
            "a@b.co",
        ]

        for email in valid_emails:
            assert validate_email(email) is True, f"Email {email} should be valid"

    def test_invalid_emails(self):
        """Test that invalid email addresses are rejected."""
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "user@",
            "user@domain",
            "user @domain.com",
            "user@domain .com",
            "",
            "user@.com",
            "@",
        ]

        for email in invalid_emails:
            assert validate_email(email) is False, f"Email {email} should be invalid"

    def test_empty_email(self):
        """Test that empty email is invalid."""
        assert validate_email("") is False
        assert validate_email(None) is False

    def test_email_with_special_characters(self):
        """Test email validation with special but valid characters."""
        assert validate_email("user+tag@example.com") is True
        assert validate_email("user.name@example.com") is True
        assert validate_email("user_name@example.com") is True
        assert validate_email("user-name@example.com") is True


@pytest.mark.unit
class TestValidatePhone:
    """Tests for phone number validation."""

    def test_valid_international_phones(self):
        """Test valid international phone numbers."""
        valid_phones = [
            "+237612345678",
            "+1234567890",
            "+44123456789",
            "1234567890",
        ]

        for phone in valid_phones:
            assert validate_phone(phone) is True, f"Phone {phone} should be valid"

    def test_invalid_phones(self):
        """Test invalid phone numbers."""
        invalid_phones = [
            "",
            "1",  # Too short (single digit)
            "abcdefghij",
            "+",
            "0123456789",  # Starts with 0
            "1234567890123456",  # Too long (16 digits)
        ]

        for phone in invalid_phones:
            assert validate_phone(phone) is False, f"Phone {phone} should be invalid"

    def test_cameroon_phone_numbers(self):
        """Test Cameroon-specific phone number validation."""
        # Valid Cameroon numbers
        assert validate_phone("+237612345678", "CM") is True
        assert validate_phone("237612345678", "CM") is True
        assert validate_phone("612345678", "CM") is True
        assert validate_phone("222345678", "CM") is True  # Landline

        # Invalid Cameroon numbers
        assert validate_phone("512345678", "CM") is False  # Wrong prefix
        assert validate_phone("12345678", "CM") is False  # Too short

    def test_phone_with_spaces_and_dashes(self):
        """Test that spaces and dashes are handled correctly."""
        assert validate_phone("+237 6 12 34 56 78", "CM") is True
        assert validate_phone("+237-6-12-34-56-78", "CM") is True
        assert validate_phone("+1-234-567-890") is True

    def test_empty_phone(self):
        """Test that empty phone is invalid."""
        assert validate_phone("") is False
        assert validate_phone(None) is False


@pytest.mark.unit
class TestValidateUrl:
    """Tests for URL validation."""

    def test_valid_urls(self):
        """Test that valid URLs are accepted."""
        valid_urls = [
            "http://example.com",
            "https://example.com",
            "https://www.example.com",
            "https://example.com/path",
            "https://example.com/path?query=value",
            "https://subdomain.example.com",
            "https://example.com:8080/path",
        ]

        for url in valid_urls:
            assert validate_url(url) is True, f"URL {url} should be valid"

    def test_invalid_urls(self):
        """Test that invalid URLs are rejected."""
        invalid_urls = [
            "",
            "not-a-url",
            "ftp://example.com",  # Not http/https
            "example.com",  # Missing protocol
            "http://",
            "https://",
        ]

        for url in invalid_urls:
            assert validate_url(url) is False, f"URL {url} should be invalid"

    def test_empty_url(self):
        """Test that empty URL is invalid."""
        assert validate_url("") is False
        assert validate_url(None) is False


@pytest.mark.unit
class TestValidateUuid:
    """Tests for UUID validation."""

    def test_valid_uuids(self):
        """Test that valid UUIDs are accepted."""
        valid_uuids = [
            "123e4567-e89b-12d3-a456-426614174000",
            "550e8400-e29b-41d4-a716-446655440000",
            "00000000-0000-0000-0000-000000000000",
            "AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE",  # Uppercase
        ]

        for uuid in valid_uuids:
            assert validate_uuid(uuid) is True, f"UUID {uuid} should be valid"

    def test_invalid_uuids(self):
        """Test that invalid UUIDs are rejected."""
        invalid_uuids = [
            "",
            "not-a-uuid",
            "123e4567-e89b-12d3-a456",  # Too short
            "123e4567-e89b-12d3-a456-426614174000-extra",  # Too long
            "123e4567e89b12d3a456426614174000",  # Missing dashes
            "gggggggg-gggg-gggg-gggg-gggggggggggg",  # Invalid hex
        ]

        for uuid in invalid_uuids:
            assert validate_uuid(uuid) is False, f"UUID {uuid} should be invalid"

    def test_empty_uuid(self):
        """Test that empty UUID is invalid."""
        assert validate_uuid("") is False
        assert validate_uuid(None) is False


@pytest.mark.unit
class TestSanitizeString:
    """Tests for string sanitization."""

    def test_removes_extra_whitespace(self):
        """Test that extra whitespace is removed."""
        assert sanitize_string("  Hello   World  ") == "Hello World"
        assert sanitize_string("Multiple   spaces    here") == "Multiple spaces here"
        assert sanitize_string("\t\tTabs\t\there\t") == "Tabs here"
        assert sanitize_string("\n\nNewlines\n\nhere\n") == "Newlines here"

    def test_truncates_to_max_length(self):
        """Test that strings are truncated to max length."""
        result = sanitize_string("This is a long string", max_length=10)
        assert len(result) <= 10
        assert result == "This is a"

    def test_handles_empty_strings(self):
        """Test that empty strings are handled correctly."""
        assert sanitize_string("") == ""
        assert sanitize_string(None) == ""
        assert sanitize_string("   ") == ""

    def test_preserves_single_spaces(self):
        """Test that single spaces between words are preserved."""
        assert sanitize_string("Normal text here") == "Normal text here"

    def test_no_truncation_when_under_max_length(self):
        """Test that strings under max_length are not truncated."""
        text = "Short text"
        assert sanitize_string(text, max_length=50) == text

    def test_truncation_removes_trailing_whitespace(self):
        """Test that truncation doesn't leave trailing whitespace."""
        result = sanitize_string("Word boundary test", max_length=13)
        assert not result.endswith(" ")


@pytest.mark.unit
class TestValidatePasswordStrength:
    """Tests for password strength validation."""

    def test_valid_strong_passwords(self):
        """Test that strong passwords are accepted."""
        valid_passwords = [
            "SecureP@ss123",
            "MyP@ssw0rd!",
            "C0mpl3x!Pass",
            "Str0ng&Secure#",
        ]

        for password in valid_passwords:
            valid, error = validate_password_strength(password)
            assert valid is True, f"Password {password} should be valid"
            assert error is None

    def test_password_too_short(self):
        """Test that short passwords are rejected."""
        valid, error = validate_password_strength("Sh0rt!")
        assert valid is False
        assert error == "Password must be at least 8 characters"

    def test_password_missing_lowercase(self):
        """Test that passwords without lowercase are rejected."""
        valid, error = validate_password_strength("PASSWORD123!")
        assert valid is False
        assert error == "Password must contain at least one lowercase letter"

    def test_password_missing_uppercase(self):
        """Test that passwords without uppercase are rejected."""
        valid, error = validate_password_strength("password123!")
        assert valid is False
        assert error == "Password must contain at least one uppercase letter"

    def test_password_missing_digit(self):
        """Test that passwords without digits are rejected."""
        valid, error = validate_password_strength("Password!")
        assert valid is False
        assert error == "Password must contain at least one digit"

    def test_password_missing_special_character(self):
        """Test that passwords without special characters are rejected."""
        valid, error = validate_password_strength("Password123")
        assert valid is False
        assert error == "Password must contain at least one special character"

    def test_empty_password(self):
        """Test that empty passwords are rejected."""
        valid, error = validate_password_strength("")
        assert valid is False
        assert error == "Password is required"

        valid, error = validate_password_strength(None)
        assert valid is False
        assert error == "Password is required"

    def test_password_with_all_special_characters(self):
        """Test passwords with various special characters."""
        special_chars = "!@#$%^&*(),.?\":{}|<>"
        for char in special_chars:
            password = f"Pass123{char}word"
            valid, error = validate_password_strength(password)
            assert valid is True, f"Password with '{char}' should be valid"


@pytest.mark.unit
class TestValidatorsEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_validators_handle_none_gracefully(self):
        """Test that validators handle None values gracefully."""
        assert validate_email(None) is False
        assert validate_phone(None) is False
        assert validate_url(None) is False
        assert validate_uuid(None) is False

    def test_sanitize_handles_none(self):
        """Test that sanitize_string handles None."""
        assert sanitize_string(None) == ""
        assert sanitize_string(None, max_length=10) == ""

    def test_very_long_inputs(self):
        """Test validators with very long inputs."""
        long_string = "a" * 10000

        # Should handle gracefully without errors
        validate_email(long_string + "@example.com")
        validate_phone(long_string)
        validate_url("https://" + long_string + ".com")

        # Sanitize should truncate
        result = sanitize_string(long_string, max_length=100)
        assert len(result) == 100
