"""
BizStats Auth - Enterprise authentication with JWT, RBAC, and multi-tenant support.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

from bizstats_auth.config import AuthConfig, get_config, configure
from bizstats_auth.models.schemas import (
    # User schemas
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    # Session schemas
    SessionCreate,
    SessionResponse,
    # Token schemas
    TokenPayload,
    TokenResponse,
    RefreshTokenRequest,
    # Password schemas
    PasswordChange,
    PasswordReset,
    PasswordResetRequest,
    # Profile schemas
    ProfileUpdate,
)
from bizstats_auth.models.enums import (
    UserRole,
    UserStatus,
    SessionStatus,
    TokenType,
    # RBAC enums
    OrganizationRole,
    TeamRole,
    ProjectRole,
    RoleScope,
    InvitationStatus,
)
from bizstats_auth.models.results import (
    AuthResult,
    TokenResult,
    SessionResult,
    PasswordResult,
)
from bizstats_auth.security.password import (
    PasswordHasher,
    hash_password,
    verify_password,
    check_password_strength,
    PasswordStrength,
)
from bizstats_auth.security.jwt import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    verify_token,
    decode_token,
)
from bizstats_auth.rbac.permissions import (
    Permission,
    PermissionChecker,
    RolePermissions,
    check_permission,
    get_role_permissions,
)
from bizstats_auth.rbac.roles import (
    RoleHierarchy,
    get_effective_permissions,
    can_manage_role,
)
from bizstats_auth.tokens.api_key import (
    APIKeyManager,
    APIKey,
    APIKeyCreate,
    generate_api_key,
    validate_api_key,
    hash_api_key,
)

__version__ = "0.1.0"
__all__ = [
    # Config
    "AuthConfig",
    "get_config",
    "configure",
    # User schemas
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    # Session schemas
    "SessionCreate",
    "SessionResponse",
    # Token schemas
    "TokenPayload",
    "TokenResponse",
    "RefreshTokenRequest",
    # Password schemas
    "PasswordChange",
    "PasswordReset",
    "PasswordResetRequest",
    # Profile schemas
    "ProfileUpdate",
    # Enums
    "UserRole",
    "UserStatus",
    "SessionStatus",
    "TokenType",
    "OrganizationRole",
    "TeamRole",
    "ProjectRole",
    "RoleScope",
    "InvitationStatus",
    # Results
    "AuthResult",
    "TokenResult",
    "SessionResult",
    "PasswordResult",
    # Password security
    "PasswordHasher",
    "hash_password",
    "verify_password",
    "check_password_strength",
    "PasswordStrength",
    # JWT
    "JWTManager",
    "create_access_token",
    "create_refresh_token",
    "verify_token",
    "decode_token",
    # RBAC
    "Permission",
    "PermissionChecker",
    "RolePermissions",
    "check_permission",
    "get_role_permissions",
    "RoleHierarchy",
    "get_effective_permissions",
    "can_manage_role",
    # API Keys
    "APIKeyManager",
    "APIKey",
    "APIKeyCreate",
    "generate_api_key",
    "validate_api_key",
    "hash_api_key",
]
