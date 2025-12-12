"""
Test fixtures for bizstats-auth tests.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import pytest
from datetime import datetime, timezone, timedelta

from bizstats_auth.config import AuthConfig, configure
from bizstats_auth.models.enums import (
    UserRole,
    UserStatus,
    SessionStatus,
    TokenType,
    OrganizationRole,
    TeamRole,
    ProjectRole,
)
from bizstats_auth.models.schemas import (
    UserCreate,
    UserResponse,
    SessionCreate,
    SessionResponse,
    TokenPayload,
)
from bizstats_auth.security.password import PasswordHasher
from bizstats_auth.security.jwt import JWTManager
from bizstats_auth.rbac.permissions import Permission, PermissionChecker
from bizstats_auth.tokens.api_key import APIKeyManager, APIKey


@pytest.fixture
def test_config():
    """Create test auth configuration."""
    config = AuthConfig(
        jwt_secret_key="test-secret-key-for-testing-only",
        jwt_algorithm="HS256",
        access_token_expire_minutes=30,
        refresh_token_expire_days=7,
        password_min_length=8,
        password_require_uppercase=True,
        password_require_lowercase=True,
        password_require_digit=True,
        password_require_special=True,
        api_key_prefix="biz_test_",
        api_key_length=32,
        max_login_attempts=5,
        lockout_duration_minutes=15,
    )
    configure(config)
    return config


@pytest.fixture
def password_hasher():
    """Create password hasher instance."""
    return PasswordHasher(rounds=4)  # Lower rounds for faster tests


@pytest.fixture
def jwt_manager(test_config):
    """Create JWT manager instance."""
    return JWTManager(test_config)


@pytest.fixture
def api_key_manager(test_config):
    """Create API key manager instance."""
    return APIKeyManager(test_config)


@pytest.fixture
def sample_user_create():
    """Create sample user creation request."""
    return UserCreate(
        email="test@example.com",
        username="testuser",
        password="SecureP@ss123!",
        first_name="Test",
        last_name="User",
        role=UserRole.USER,
        organization_id="org_123",
    )


@pytest.fixture
def sample_user_response():
    """Create sample user response."""
    return UserResponse(
        id="user_123",
        email="test@example.com",
        username="testuser",
        first_name="Test",
        last_name="User",
        role=UserRole.USER,
        status=UserStatus.ACTIVE,
        organization_id="org_123",
        created_at=datetime.now(timezone.utc),
        email_verified=True,
    )


@pytest.fixture
def sample_session_create():
    """Create sample session creation request."""
    return SessionCreate(
        user_id="user_123",
        ip_address="192.168.1.1",
        user_agent="Mozilla/5.0",
        device_info={"type": "desktop", "os": "macOS"},
    )


@pytest.fixture
def sample_session_response():
    """Create sample session response."""
    return SessionResponse(
        id="session_123",
        user_id="user_123",
        status=SessionStatus.ACTIVE,
        ip_address="192.168.1.1",
        user_agent="Mozilla/5.0",
        created_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
    )


@pytest.fixture
def sample_token_payload():
    """Create sample token payload."""
    return TokenPayload(
        sub="user_123",
        exp=datetime.now(timezone.utc) + timedelta(minutes=30),
        iat=datetime.now(timezone.utc),
        jti="token_123",
        type=TokenType.ACCESS,
        scope=["read", "write"],
        organization_id="org_123",
        roles={"organization": "admin"},
    )


@pytest.fixture
def org_admin_checker():
    """Create permission checker for org admin."""
    return PermissionChecker(
        organization_role=OrganizationRole.ADMIN,
    )


@pytest.fixture
def team_lead_checker():
    """Create permission checker for team lead."""
    return PermissionChecker(
        organization_role=OrganizationRole.VIEWER,
        team_role=TeamRole.LEAD,
    )


@pytest.fixture
def project_viewer_checker():
    """Create permission checker for project viewer."""
    return PermissionChecker(
        organization_role=OrganizationRole.VIEWER,
        team_role=TeamRole.VIEWER,
        project_role=ProjectRole.VIEWER,
    )


@pytest.fixture
def super_admin_checker():
    """Create permission checker for super admin."""
    return PermissionChecker(
        organization_role=OrganizationRole.SUPER_ADMIN,
    )


@pytest.fixture
def sample_api_key(api_key_manager):
    """Create a sample API key."""
    now = datetime.now(timezone.utc)
    return APIKey(
        id="key_123",
        name="Test API Key",
        key_prefix="biz_test_abc12345",
        key_hash="fake_hash_for_testing",
        user_id="user_123",
        organization_id="org_123",
        project_id=None,
        scopes=["read", "write"],
        permissions={Permission.CHATBOT_READ, Permission.CHATBOT_UPDATE},
        created_at=now,
        expires_at=now + timedelta(days=30),
        last_used_at=None,
        is_active=True,
        rate_limit=1000,
        metadata={"created_by": "test"},
    )
