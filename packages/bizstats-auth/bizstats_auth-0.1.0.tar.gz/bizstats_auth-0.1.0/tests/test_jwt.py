"""
Tests for JWT token management.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import pytest
from datetime import datetime, timezone, timedelta
import time

from bizstats_auth.security.jwt import (
    JWTManager,
    TokenExpiredError,
    TokenInvalidError,
    create_access_token,
    create_refresh_token,
    verify_token,
    decode_token,
)
from bizstats_auth.models.enums import TokenType


class TestJWTManager:
    """Tests for JWTManager class."""

    def test_create_access_token(self, jwt_manager):
        """Test creating an access token."""
        token = jwt_manager.create_access_token(
            subject="user_123",
            scope=["read", "write"],
            organization_id="org_123",
        )

        assert token is not None
        assert isinstance(token, str)
        assert len(token.split(".")) == 3  # JWT has 3 parts

    def test_create_refresh_token(self, jwt_manager):
        """Test creating a refresh token."""
        token = jwt_manager.create_refresh_token(
            subject="user_123",
            organization_id="org_123",
        )

        assert token is not None
        assert isinstance(token, str)

    def test_create_password_reset_token(self, jwt_manager):
        """Test creating a password reset token."""
        token = jwt_manager.create_password_reset_token(
            subject="user_123",
            expires_minutes=60,
        )

        payload = jwt_manager.verify_token(token, TokenType.PASSWORD_RESET)
        assert payload.type == TokenType.PASSWORD_RESET

    def test_create_email_verification_token(self, jwt_manager):
        """Test creating an email verification token."""
        token = jwt_manager.create_email_verification_token(
            subject="user_123",
            expires_hours=24,
        )

        payload = jwt_manager.verify_token(token, TokenType.EMAIL_VERIFICATION)
        assert payload.type == TokenType.EMAIL_VERIFICATION

    def test_verify_access_token(self, jwt_manager):
        """Test verifying an access token."""
        token = jwt_manager.create_access_token(
            subject="user_123",
            scope=["read", "write"],
            organization_id="org_123",
            roles={"organization": "admin"},
        )

        payload = jwt_manager.verify_token(token, TokenType.ACCESS)

        assert payload.sub == "user_123"
        assert payload.type == TokenType.ACCESS
        assert payload.scope == ["read", "write"]
        assert payload.organization_id == "org_123"
        assert payload.roles == {"organization": "admin"}

    def test_verify_refresh_token(self, jwt_manager):
        """Test verifying a refresh token."""
        token = jwt_manager.create_refresh_token(subject="user_123")

        payload = jwt_manager.verify_token(token, TokenType.REFRESH)

        assert payload.sub == "user_123"
        assert payload.type == TokenType.REFRESH

    def test_verify_wrong_token_type(self, jwt_manager):
        """Test verifying with wrong expected type."""
        token = jwt_manager.create_access_token(subject="user_123")

        with pytest.raises(TokenInvalidError) as exc_info:
            jwt_manager.verify_token(token, TokenType.REFRESH)

        assert "Expected token type" in str(exc_info.value)

    def test_verify_expired_token(self, jwt_manager):
        """Test verifying an expired token."""
        token = jwt_manager.create_access_token(
            subject="user_123",
            expires_delta=timedelta(seconds=-1),  # Already expired
        )

        with pytest.raises(TokenExpiredError):
            jwt_manager.verify_token(token)

    def test_verify_invalid_token(self, jwt_manager):
        """Test verifying an invalid token."""
        with pytest.raises(TokenInvalidError):
            jwt_manager.verify_token("invalid.token.here")

    def test_verify_tampered_token(self, jwt_manager):
        """Test verifying a tampered token."""
        token = jwt_manager.create_access_token(subject="user_123")
        # Tamper with the token
        parts = token.split(".")
        parts[1] = parts[1][:-5] + "xxxxx"  # Modify payload
        tampered_token = ".".join(parts)

        with pytest.raises(TokenInvalidError):
            jwt_manager.verify_token(tampered_token)

    def test_decode_token_with_verify(self, jwt_manager):
        """Test decoding a token with verification."""
        token = jwt_manager.create_access_token(
            subject="user_123",
            organization_id="org_123",
        )

        payload = jwt_manager.decode_token(token, verify=True)

        assert payload["sub"] == "user_123"
        assert payload["org_id"] == "org_123"

    def test_decode_token_without_verify(self, jwt_manager):
        """Test decoding a token without verification."""
        token = jwt_manager.create_access_token(
            subject="user_123",
            expires_delta=timedelta(seconds=-1),  # Expired
        )

        # Should work even though token is expired
        payload = jwt_manager.decode_token(token, verify=False)

        assert payload["sub"] == "user_123"

    def test_token_has_unique_jti(self, jwt_manager):
        """Test that each token has unique JTI."""
        token1 = jwt_manager.create_access_token(subject="user_123")
        token2 = jwt_manager.create_access_token(subject="user_123")

        payload1 = jwt_manager.decode_token(token1)
        payload2 = jwt_manager.decode_token(token2)

        assert payload1["jti"] != payload2["jti"]

    def test_create_token_response(self, jwt_manager):
        """Test creating a complete token response."""
        response = jwt_manager.create_token_response(
            subject="user_123",
            scope=["read", "write"],
            organization_id="org_123",
            include_refresh=True,
        )

        assert response.access_token is not None
        assert response.refresh_token is not None
        assert response.token_type == "Bearer"
        assert response.expires_in > 0
        assert response.scope == ["read", "write"]

    def test_create_token_response_without_refresh(self, jwt_manager):
        """Test creating token response without refresh token."""
        response = jwt_manager.create_token_response(
            subject="user_123",
            include_refresh=False,
        )

        assert response.access_token is not None
        assert response.refresh_token is None


class TestModuleFunctions:
    """Tests for module-level convenience functions."""

    def test_create_access_token(self, test_config):
        """Test create_access_token function."""
        token = create_access_token(
            subject="user_123",
            scope=["read"],
        )

        assert token is not None
        payload = verify_token(token)
        assert payload.sub == "user_123"

    def test_create_refresh_token(self, test_config):
        """Test create_refresh_token function."""
        token = create_refresh_token(subject="user_123")

        payload = verify_token(token, TokenType.REFRESH)
        assert payload.sub == "user_123"
        assert payload.type == TokenType.REFRESH

    def test_verify_token(self, test_config):
        """Test verify_token function."""
        token = create_access_token(subject="user_123")

        payload = verify_token(token)
        assert payload.sub == "user_123"

    def test_decode_token(self, test_config):
        """Test decode_token function."""
        token = create_access_token(subject="user_123")

        payload = decode_token(token)
        assert payload["sub"] == "user_123"


class TestTokenExpiration:
    """Tests for token expiration handling."""

    def test_access_token_default_expiration(self, jwt_manager, test_config):
        """Test access token has correct default expiration."""
        token = jwt_manager.create_access_token(subject="user_123")
        payload = jwt_manager.decode_token(token)

        expected_exp = datetime.now(timezone.utc) + timedelta(
            minutes=test_config.access_token_expire_minutes
        )
        actual_exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)

        # Allow 5 second tolerance
        assert abs((expected_exp - actual_exp).total_seconds()) < 5

    def test_refresh_token_default_expiration(self, jwt_manager, test_config):
        """Test refresh token has correct default expiration."""
        token = jwt_manager.create_refresh_token(subject="user_123")
        payload = jwt_manager.decode_token(token)

        expected_exp = datetime.now(timezone.utc) + timedelta(
            days=test_config.refresh_token_expire_days
        )
        actual_exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)

        # Allow 5 second tolerance
        assert abs((expected_exp - actual_exp).total_seconds()) < 5

    def test_custom_expiration(self, jwt_manager):
        """Test custom token expiration."""
        custom_delta = timedelta(hours=2)
        token = jwt_manager.create_access_token(
            subject="user_123",
            expires_delta=custom_delta,
        )
        payload = jwt_manager.decode_token(token)

        expected_exp = datetime.now(timezone.utc) + custom_delta
        actual_exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)

        # Allow 5 second tolerance
        assert abs((expected_exp - actual_exp).total_seconds()) < 5
