"""
Tests for auth models and schemas.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import pytest
from datetime import datetime, timezone, timedelta
from pydantic import ValidationError

from bizstats_auth.models.enums import (
    UserRole,
    UserStatus,
    SessionStatus,
    TokenType,
    OrganizationRole,
    TeamRole,
    ProjectRole,
    RoleScope,
    InvitationStatus,
)
from bizstats_auth.models.schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    SessionCreate,
    SessionResponse,
    TokenPayload,
    TokenResponse,
    RefreshTokenRequest,
    PasswordChange,
    PasswordReset,
    PasswordResetRequest,
    ProfileUpdate,
)
from bizstats_auth.models.results import (
    AuthResult,
    TokenResult,
    SessionResult,
    PasswordResult,
)


class TestEnums:
    """Tests for enum values."""

    def test_user_role_values(self):
        """Test UserRole enum values."""
        assert UserRole.ADMIN.value == "admin"
        assert UserRole.USER.value == "user"
        assert UserRole.GUEST.value == "guest"

    def test_user_status_values(self):
        """Test UserStatus enum values."""
        assert UserStatus.ACTIVE.value == "active"
        assert UserStatus.SUSPENDED.value == "suspended"
        assert UserStatus.LOCKED.value == "locked"

    def test_session_status_values(self):
        """Test SessionStatus enum values."""
        assert SessionStatus.ACTIVE.value == "active"
        assert SessionStatus.EXPIRED.value == "expired"
        assert SessionStatus.REVOKED.value == "revoked"

    def test_token_type_values(self):
        """Test TokenType enum values."""
        assert TokenType.ACCESS.value == "access"
        assert TokenType.REFRESH.value == "refresh"
        assert TokenType.API_KEY.value == "api_key"

    def test_organization_role_values(self):
        """Test OrganizationRole enum values."""
        assert OrganizationRole.SUPER_ADMIN.value == "super_admin"
        assert OrganizationRole.ADMIN.value == "admin"
        assert OrganizationRole.BILLING.value == "billing"
        assert OrganizationRole.VIEWER.value == "viewer"

    def test_team_role_values(self):
        """Test TeamRole enum values."""
        assert TeamRole.LEAD.value == "lead"
        assert TeamRole.MEMBER.value == "member"
        assert TeamRole.VIEWER.value == "viewer"

    def test_project_role_values(self):
        """Test ProjectRole enum values."""
        assert ProjectRole.OWNER.value == "owner"
        assert ProjectRole.EDITOR.value == "editor"
        assert ProjectRole.CONTRIBUTOR.value == "contributor"
        assert ProjectRole.VIEWER.value == "viewer"


class TestUserCreate:
    """Tests for UserCreate schema."""

    def test_valid_user_create(self):
        """Test creating a valid user."""
        user = UserCreate(
            email="test@example.com",
            username="testuser",
            password="SecureP@ss123!",
            first_name="Test",
            last_name="User",
        )

        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.role == UserRole.USER  # Default

    def test_username_lowercase(self):
        """Test username is converted to lowercase."""
        user = UserCreate(
            email="test@example.com",
            username="TestUser",
            password="SecureP@ss123!",
        )

        assert user.username == "testuser"

    def test_invalid_email(self):
        """Test invalid email is rejected."""
        with pytest.raises(ValidationError):
            UserCreate(
                email="not-an-email",
                password="SecureP@ss123!",
            )

    def test_short_password(self):
        """Test short password is rejected."""
        with pytest.raises(ValidationError):
            UserCreate(
                email="test@example.com",
                password="short",
            )

    def test_invalid_username_chars(self):
        """Test invalid username characters are rejected."""
        with pytest.raises(ValidationError):
            UserCreate(
                email="test@example.com",
                username="test@user",  # @ not allowed
                password="SecureP@ss123!",
            )

    def test_username_too_short(self):
        """Test username too short is rejected."""
        with pytest.raises(ValidationError):
            UserCreate(
                email="test@example.com",
                username="ab",  # Must be at least 3 chars
                password="SecureP@ss123!",
            )


class TestUserLogin:
    """Tests for UserLogin schema."""

    def test_login_with_email(self):
        """Test login with email."""
        login = UserLogin(
            email="test@example.com",
            password="password123",
        )

        assert login.email == "test@example.com"

    def test_login_with_username(self):
        """Test login with username."""
        login = UserLogin(
            username="testuser",
            password="password123",
        )

        assert login.username == "testuser"

    def test_login_requires_identifier(self):
        """Test login requires email or username."""
        with pytest.raises(ValueError, match="Either email or username"):
            UserLogin(password="password123")


class TestPasswordSchemas:
    """Tests for password-related schemas."""

    def test_password_change_matching(self):
        """Test password change with matching passwords."""
        change = PasswordChange(
            current_password="oldpass123",
            new_password="NewP@ss123!",
            confirm_password="NewP@ss123!",
        )

        assert change.new_password == change.confirm_password

    def test_password_change_mismatch(self):
        """Test password change with mismatched passwords."""
        with pytest.raises(ValidationError, match="do not match"):
            PasswordChange(
                current_password="oldpass123",
                new_password="NewP@ss123!",
                confirm_password="DifferentP@ss!",
            )

    def test_password_reset_matching(self):
        """Test password reset with matching passwords."""
        reset = PasswordReset(
            token="reset_token_123",
            new_password="NewP@ss123!",
            confirm_password="NewP@ss123!",
        )

        assert reset.token == "reset_token_123"

    def test_password_reset_request(self):
        """Test password reset request."""
        request = PasswordResetRequest(email="test@example.com")

        assert request.email == "test@example.com"


class TestTokenSchemas:
    """Tests for token-related schemas."""

    def test_token_payload(self, sample_token_payload):
        """Test token payload creation."""
        assert sample_token_payload.sub == "user_123"
        assert sample_token_payload.type == TokenType.ACCESS
        assert sample_token_payload.scope == ["read", "write"]

    def test_token_response(self):
        """Test token response creation."""
        response = TokenResponse(
            access_token="access_123",
            refresh_token="refresh_456",
            expires_in=1800,
            scope=["read"],
        )

        assert response.access_token == "access_123"
        assert response.token_type == "Bearer"
        assert response.expires_in == 1800

    def test_refresh_token_request(self):
        """Test refresh token request."""
        request = RefreshTokenRequest(refresh_token="token_123")

        assert request.refresh_token == "token_123"


class TestResultTypes:
    """Tests for result types."""

    def test_auth_result_ok(self, sample_user_response):
        """Test successful auth result."""
        result = AuthResult.ok(
            user=sample_user_response,
        )

        assert result.success is True
        assert result.user is not None
        assert result.error_message is None

    def test_auth_result_fail(self):
        """Test failed auth result."""
        result = AuthResult.fail(
            error_message="Invalid credentials",
            error_code="INVALID_CREDENTIALS",
        )

        assert result.success is False
        assert result.error_message == "Invalid credentials"
        assert result.error_code == "INVALID_CREDENTIALS"

    def test_auth_result_mfa_required(self):
        """Test MFA required result."""
        result = AuthResult.mfa_required(mfa_token="mfa_123")

        assert result.success is False
        assert result.requires_mfa is True
        assert result.mfa_token == "mfa_123"

    def test_token_result_ok(self):
        """Test successful token result."""
        token_response = TokenResponse(
            access_token="access_123",
            expires_in=1800,
        )
        result = TokenResult.ok(tokens=token_response)

        assert result.success is True
        assert result.tokens is not None

    def test_token_result_fail_expired(self):
        """Test expired token result."""
        result = TokenResult.fail(
            error_message="Token expired",
            is_expired=True,
        )

        assert result.success is False
        assert result.is_expired is True

    def test_session_result_ok(self, sample_session_response):
        """Test successful session result."""
        result = SessionResult.ok(session=sample_session_response)

        assert result.success is True
        assert result.session is not None

    def test_password_result_changed(self):
        """Test password changed result."""
        result = PasswordResult.ok(password_changed=True)

        assert result.success is True
        assert result.password_changed is True

    def test_password_result_reset_sent(self):
        """Test password reset sent result."""
        result = PasswordResult.ok(reset_token_sent=True)

        assert result.success is True
        assert result.reset_token_sent is True


class TestUserResponse:
    """Tests for UserResponse schema."""

    def test_user_response_from_dict(self):
        """Test creating user response from dict."""
        data = {
            "id": "user_123",
            "email": "test@example.com",
            "username": "testuser",
            "role": UserRole.USER,
            "status": UserStatus.ACTIVE,
            "created_at": datetime.now(timezone.utc),
            "email_verified": True,
        }

        response = UserResponse(**data)

        assert response.id == "user_123"
        assert response.email == "test@example.com"


class TestProfileUpdate:
    """Tests for ProfileUpdate schema."""

    def test_profile_update_partial(self):
        """Test partial profile update."""
        update = ProfileUpdate(
            first_name="John",
            timezone="America/New_York",
        )

        assert update.first_name == "John"
        assert update.timezone == "America/New_York"
        assert update.last_name is None

    def test_profile_update_with_preferences(self):
        """Test profile update with preferences."""
        update = ProfileUpdate(
            preferences={
                "theme": "dark",
                "notifications": True,
            }
        )

        assert update.preferences["theme"] == "dark"
