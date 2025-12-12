"""
Pydantic schemas for authentication.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr, field_validator
import re

from bizstats_auth.models.enums import (
    UserRole,
    UserStatus,
    SessionStatus,
    TokenType,
    OrganizationRole,
    TeamRole,
    ProjectRole,
)


# User Schemas


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    email: EmailStr
    username: Optional[str] = None
    password: str = Field(..., min_length=8)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: UserRole = UserRole.USER
    organization_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError("Username can only contain letters, numbers, underscores, and hyphens")
        return v.lower()


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    email: Optional[EmailStr] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    metadata: Optional[Dict[str, Any]] = None


class UserResponse(BaseModel):
    """Schema for user response."""

    id: str
    email: EmailStr
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: UserRole
    status: UserStatus
    organization_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    email_verified: bool = False
    metadata: Optional[Dict[str, Any]] = None

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    """Schema for user login."""

    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: str

    @field_validator("email", "username")
    @classmethod
    def validate_identifier(cls, v: Optional[str], info) -> Optional[str]:
        # At least one identifier must be provided (validated at model level)
        return v

    def model_post_init(self, __context: Any) -> None:
        if not self.email and not self.username:
            raise ValueError("Either email or username must be provided")


# Session Schemas


class SessionCreate(BaseModel):
    """Schema for creating a session."""

    user_id: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    device_info: Optional[Dict[str, Any]] = None


class SessionResponse(BaseModel):
    """Schema for session response."""

    id: str
    user_id: str
    status: SessionStatus
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    device_info: Optional[Dict[str, Any]] = None
    created_at: datetime
    expires_at: datetime
    last_activity: Optional[datetime] = None

    model_config = {"from_attributes": True}


# Token Schemas


class TokenPayload(BaseModel):
    """Schema for JWT token payload."""

    sub: str  # Subject (user ID)
    exp: datetime  # Expiration time
    iat: datetime  # Issued at
    jti: Optional[str] = None  # JWT ID (for revocation)
    type: TokenType = TokenType.ACCESS
    scope: Optional[List[str]] = None
    organization_id: Optional[str] = None
    roles: Optional[Dict[str, str]] = None  # scope -> role mapping


class TokenResponse(BaseModel):
    """Schema for token response."""

    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: int  # Seconds until expiration
    scope: Optional[List[str]] = None


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request."""

    refresh_token: str


# Password Schemas


class PasswordChange(BaseModel):
    """Schema for changing password."""

    current_password: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        if "new_password" in info.data and v != info.data["new_password"]:
            raise ValueError("Passwords do not match")
        return v


class PasswordReset(BaseModel):
    """Schema for resetting password with token."""

    token: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        if "new_password" in info.data and v != info.data["new_password"]:
            raise ValueError("Passwords do not match")
        return v


class PasswordResetRequest(BaseModel):
    """Schema for requesting password reset."""

    email: EmailStr


# Profile Schemas


class ProfileUpdate(BaseModel):
    """Schema for updating user profile."""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    timezone: Optional[str] = None
    language: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None


# RBAC Schemas


class OrganizationMemberCreate(BaseModel):
    """Schema for adding organization member."""

    user_id: str
    role: OrganizationRole = OrganizationRole.VIEWER


class TeamMemberCreate(BaseModel):
    """Schema for adding team member."""

    user_id: str
    role: TeamRole = TeamRole.MEMBER


class ProjectMemberCreate(BaseModel):
    """Schema for adding project member."""

    user_id: str
    role: ProjectRole = ProjectRole.VIEWER
