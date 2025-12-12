"""
Tests for password hashing and validation.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import pytest
from bizstats_auth.security.password import (
    PasswordHasher,
    hash_password,
    verify_password,
    check_password_strength,
    PasswordStrength,
)


class TestPasswordHasher:
    """Tests for PasswordHasher class."""

    def test_hash_creates_bcrypt_hash(self, password_hasher):
        """Test that hashing creates a bcrypt hash."""
        password = "SecureP@ss123!"
        hashed = password_hasher.hash(password)

        assert hashed.startswith("$2")  # bcrypt prefix
        assert len(hashed) == 60  # bcrypt hash length

    def test_verify_correct_password(self, password_hasher):
        """Test verifying correct password."""
        password = "SecureP@ss123!"
        hashed = password_hasher.hash(password)

        assert password_hasher.verify(password, hashed) is True

    def test_verify_wrong_password(self, password_hasher):
        """Test verifying wrong password."""
        password = "SecureP@ss123!"
        wrong_password = "WrongP@ss456!"
        hashed = password_hasher.hash(password)

        assert password_hasher.verify(wrong_password, hashed) is False

    def test_verify_invalid_hash(self, password_hasher):
        """Test verifying with invalid hash."""
        password = "SecureP@ss123!"
        invalid_hash = "not_a_valid_hash"

        assert password_hasher.verify(password, invalid_hash) is False

    def test_same_password_different_hashes(self, password_hasher):
        """Test that same password produces different hashes."""
        password = "SecureP@ss123!"
        hash1 = password_hasher.hash(password)
        hash2 = password_hasher.hash(password)

        assert hash1 != hash2  # Different salts
        assert password_hasher.verify(password, hash1)
        assert password_hasher.verify(password, hash2)

    def test_needs_rehash_returns_false_for_current(self, password_hasher):
        """Test needs_rehash for current settings."""
        password = "SecureP@ss123!"
        hashed = password_hasher.hash(password)

        # Should not need rehash with same settings
        assert password_hasher.needs_rehash(hashed) is False


class TestPasswordStrength:
    """Tests for password strength checking."""

    def test_weak_password(self, password_hasher):
        """Test weak password detection."""
        result = password_hasher.check_strength("123")

        assert result.is_valid is False
        assert result.strength == PasswordStrength.WEAK
        assert len(result.issues) > 0

    def test_password_too_short(self, password_hasher):
        """Test password length validation."""
        result = password_hasher.check_strength("Aa1!")

        assert result.is_valid is False
        assert any("at least" in issue for issue in result.issues)

    def test_password_missing_uppercase(self, password_hasher):
        """Test uppercase requirement."""
        result = password_hasher.check_strength("secure@pass123")

        assert result.is_valid is False
        assert any("uppercase" in issue.lower() for issue in result.issues)

    def test_password_missing_lowercase(self, password_hasher):
        """Test lowercase requirement."""
        result = password_hasher.check_strength("SECURE@PASS123")

        assert result.is_valid is False
        assert any("lowercase" in issue.lower() for issue in result.issues)

    def test_password_missing_digit(self, password_hasher):
        """Test digit requirement."""
        result = password_hasher.check_strength("Secure@Pass!!")

        assert result.is_valid is False
        assert any("digit" in issue.lower() for issue in result.issues)

    def test_password_missing_special(self, password_hasher):
        """Test special character requirement."""
        result = password_hasher.check_strength("SecurePass123")

        assert result.is_valid is False
        assert any("special" in issue.lower() for issue in result.issues)

    def test_strong_password(self, password_hasher):
        """Test strong password detection."""
        result = password_hasher.check_strength("Str0ng&SecureP@ss!")

        assert result.is_valid is True
        assert result.strength in [PasswordStrength.GOOD, PasswordStrength.STRONG, PasswordStrength.VERY_STRONG]
        assert len(result.issues) == 0

    def test_very_strong_password(self, password_hasher):
        """Test very strong password."""
        result = password_hasher.check_strength("Super$tr0ng&V3ryS3cure!P@ssw0rd")

        assert result.is_valid is True
        assert result.strength in [PasswordStrength.STRONG, PasswordStrength.VERY_STRONG]
        assert result.score >= 70

    def test_common_pattern_detection(self, password_hasher):
        """Test detection of common patterns."""
        result = password_hasher.check_strength("Password123!")

        # Should still be valid but with reduced score
        assert "patterns" in " ".join(result.suggestions).lower() or result.score < 85

    def test_suggestions_provided(self, password_hasher):
        """Test that suggestions are provided for weak passwords."""
        result = password_hasher.check_strength("weak")

        assert len(result.suggestions) > 0


class TestModuleFunctions:
    """Tests for module-level convenience functions."""

    def test_hash_password(self, test_config):
        """Test hash_password function."""
        password = "SecureP@ss123!"
        hashed = hash_password(password)

        assert hashed.startswith("$2")
        assert verify_password(password, hashed)

    def test_verify_password(self, test_config):
        """Test verify_password function."""
        password = "SecureP@ss123!"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True
        assert verify_password("wrong", hashed) is False

    def test_check_password_strength(self, test_config):
        """Test check_password_strength function."""
        result = check_password_strength("Str0ng&SecureP@ss!")

        assert result.is_valid is True
        assert result.strength in [PasswordStrength.GOOD, PasswordStrength.STRONG, PasswordStrength.VERY_STRONG]
