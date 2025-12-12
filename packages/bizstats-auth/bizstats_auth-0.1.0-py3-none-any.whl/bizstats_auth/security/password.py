"""
Password hashing and validation utilities.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import re
import hashlib
from typing import Optional, List
from dataclasses import dataclass
from enum import Enum
import bcrypt

from bizstats_auth.config import get_config


class PasswordStrength(str, Enum):
    """Password strength levels."""

    WEAK = "weak"
    FAIR = "fair"
    GOOD = "good"
    STRONG = "strong"
    VERY_STRONG = "very_strong"


@dataclass
class PasswordValidationResult:
    """Result of password validation."""

    is_valid: bool
    strength: PasswordStrength
    score: int  # 0-100
    issues: List[str]
    suggestions: List[str]


class PasswordHasher:
    """Password hashing utility using bcrypt."""

    def __init__(
        self,
        rounds: int = 12,
    ):
        """
        Initialize password hasher.

        Args:
            rounds: Number of bcrypt rounds (log2, default 12 = 4096 iterations)
        """
        self.rounds = rounds

    def _prepare_password(self, password: str) -> bytes:
        """
        Prepare password for bcrypt (handles >72 byte passwords).

        Bcrypt has a 72-byte limit. For longer passwords, we use
        SHA-256 hash (base64 encoded) which is always 44 bytes.

        Args:
            password: Plain text password

        Returns:
            Password bytes ready for bcrypt
        """
        password_bytes = password.encode("utf-8")
        if len(password_bytes) > 72:
            # Hash long passwords with SHA-256 first
            password_bytes = hashlib.sha256(password_bytes).hexdigest().encode("utf-8")
        return password_bytes

    def hash(self, password: str) -> str:
        """
        Hash a password.

        Args:
            password: Plain text password

        Returns:
            Hashed password string
        """
        password_bytes = self._prepare_password(password)
        salt = bcrypt.gensalt(rounds=self.rounds)
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode("utf-8")

    def verify(self, password: str, password_hash: str) -> bool:
        """
        Verify a password against its hash.

        Args:
            password: Plain text password
            password_hash: Hashed password

        Returns:
            True if password matches hash
        """
        try:
            password_bytes = self._prepare_password(password)
            hash_bytes = password_hash.encode("utf-8")
            return bcrypt.checkpw(password_bytes, hash_bytes)
        except Exception:
            return False

    def needs_rehash(self, password_hash: str) -> bool:
        """
        Check if a hash needs to be rehashed (e.g., rounds changed).

        Args:
            password_hash: Hashed password

        Returns:
            True if hash should be updated
        """
        try:
            # Extract cost from hash (format: $2b$XX$...)
            parts = password_hash.split("$")
            if len(parts) >= 3:
                current_rounds = int(parts[2])
                return current_rounds != self.rounds
        except (ValueError, IndexError):
            pass
        return True  # If we can't parse, assume rehash needed

    def check_strength(
        self,
        password: str,
        min_length: Optional[int] = None,
        require_uppercase: Optional[bool] = None,
        require_lowercase: Optional[bool] = None,
        require_digit: Optional[bool] = None,
        require_special: Optional[bool] = None,
    ) -> PasswordValidationResult:
        """
        Check password strength and validate requirements.

        Args:
            password: Password to check
            min_length: Minimum length (uses config default if not provided)
            require_uppercase: Require uppercase letters
            require_lowercase: Require lowercase letters
            require_digit: Require digits
            require_special: Require special characters

        Returns:
            PasswordValidationResult with validation details
        """
        config = get_config()

        # Use config defaults if not specified
        min_length = min_length if min_length is not None else config.password_min_length
        require_uppercase = (
            require_uppercase if require_uppercase is not None else config.password_require_uppercase
        )
        require_lowercase = (
            require_lowercase if require_lowercase is not None else config.password_require_lowercase
        )
        require_digit = require_digit if require_digit is not None else config.password_require_digit
        require_special = (
            require_special if require_special is not None else config.password_require_special
        )

        issues: List[str] = []
        suggestions: List[str] = []
        score = 0

        # Length check
        length = len(password)
        if length < min_length:
            issues.append(f"Password must be at least {min_length} characters")
        else:
            # Score based on length
            if length >= 8:
                score += 10
            if length >= 12:
                score += 10
            if length >= 16:
                score += 10
            if length >= 20:
                score += 10

        # Character type checks
        has_uppercase = bool(re.search(r"[A-Z]", password))
        has_lowercase = bool(re.search(r"[a-z]", password))
        has_digit = bool(re.search(r"\d", password))
        has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\;\'`~]', password))

        if require_uppercase and not has_uppercase:
            issues.append("Password must contain at least one uppercase letter")
        elif has_uppercase:
            score += 15

        if require_lowercase and not has_lowercase:
            issues.append("Password must contain at least one lowercase letter")
        elif has_lowercase:
            score += 15

        if require_digit and not has_digit:
            issues.append("Password must contain at least one digit")
        elif has_digit:
            score += 15

        if require_special and not has_special:
            issues.append("Password must contain at least one special character")
        elif has_special:
            score += 15

        # Check for common patterns (reduce score)
        common_patterns = [
            r"(.)\1{2,}",  # Repeated characters
            r"123|234|345|456|567|678|789|890",  # Sequential numbers
            r"abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz",  # Sequential letters
            r"password|qwerty|admin|login|welcome|monkey|dragon|master|letmein",  # Common passwords
        ]

        for pattern in common_patterns:
            if re.search(pattern, password.lower()):
                score = max(0, score - 10)
                suggestions.append("Avoid common patterns and sequences")
                break

        # Suggestions for improvement
        if not has_uppercase:
            suggestions.append("Add uppercase letters for stronger password")
        if not has_lowercase:
            suggestions.append("Add lowercase letters for stronger password")
        if not has_digit:
            suggestions.append("Add numbers for stronger password")
        if not has_special:
            suggestions.append("Add special characters for stronger password")
        if length < 12:
            suggestions.append("Consider using a longer password (12+ characters)")

        # Determine strength level
        if score < 30:
            strength = PasswordStrength.WEAK
        elif score < 50:
            strength = PasswordStrength.FAIR
        elif score < 70:
            strength = PasswordStrength.GOOD
        elif score < 85:
            strength = PasswordStrength.STRONG
        else:
            strength = PasswordStrength.VERY_STRONG

        return PasswordValidationResult(
            is_valid=len(issues) == 0,
            strength=strength,
            score=min(100, score),
            issues=issues,
            suggestions=suggestions[:3],  # Limit to 3 suggestions
        )


# Module-level convenience functions

_hasher: Optional[PasswordHasher] = None


def _get_hasher() -> PasswordHasher:
    """Get the default password hasher instance."""
    global _hasher
    if _hasher is None:
        _hasher = PasswordHasher()
    return _hasher


def hash_password(password: str) -> str:
    """
    Hash a password using the default hasher.

    Args:
        password: Plain text password

    Returns:
        Hashed password string
    """
    return _get_hasher().hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        password: Plain text password
        password_hash: Hashed password

    Returns:
        True if password matches hash
    """
    return _get_hasher().verify(password, password_hash)


def check_password_strength(password: str) -> PasswordValidationResult:
    """
    Check password strength using default configuration.

    Args:
        password: Password to check

    Returns:
        PasswordValidationResult with validation details
    """
    return _get_hasher().check_strength(password)
