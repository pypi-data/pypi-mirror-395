"""
Result types for authentication operations.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

from typing import Generic, TypeVar, Optional, Any, Dict
from pydantic import BaseModel, Field

from bizstats_auth.models.schemas import UserResponse, SessionResponse, TokenResponse

T = TypeVar("T")


class BaseResult(BaseModel, Generic[T]):
    """Base result type for all operations."""

    success: bool = False
    data: Optional[T] = None
    error_message: Optional[str] = None
    error_code: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    @classmethod
    def ok(cls, data: T, metadata: Optional[Dict[str, Any]] = None) -> "BaseResult[T]":
        """Create a successful result."""
        return cls(success=True, data=data, metadata=metadata)

    @classmethod
    def fail(
        cls,
        error_message: str,
        error_code: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "BaseResult[T]":
        """Create a failed result."""
        return cls(
            success=False,
            error_message=error_message,
            error_code=error_code,
            metadata=metadata,
        )


class AuthResult(BaseModel):
    """Result of authentication operations."""

    success: bool = False
    user: Optional[UserResponse] = None
    tokens: Optional[TokenResponse] = None
    session: Optional[SessionResponse] = None
    error_message: Optional[str] = None
    error_code: Optional[str] = None
    requires_mfa: bool = False
    mfa_token: Optional[str] = None

    @classmethod
    def ok(
        cls,
        user: UserResponse,
        tokens: Optional[TokenResponse] = None,
        session: Optional[SessionResponse] = None,
    ) -> "AuthResult":
        """Create a successful auth result."""
        return cls(success=True, user=user, tokens=tokens, session=session)

    @classmethod
    def fail(cls, error_message: str, error_code: Optional[str] = None) -> "AuthResult":
        """Create a failed auth result."""
        return cls(success=False, error_message=error_message, error_code=error_code)

    @classmethod
    def mfa_required(cls, mfa_token: str) -> "AuthResult":
        """Create an MFA required result."""
        return cls(success=False, requires_mfa=True, mfa_token=mfa_token)


class TokenResult(BaseModel):
    """Result of token operations."""

    success: bool = False
    tokens: Optional[TokenResponse] = None
    error_message: Optional[str] = None
    error_code: Optional[str] = None
    is_expired: bool = False
    is_revoked: bool = False

    @classmethod
    def ok(cls, tokens: TokenResponse) -> "TokenResult":
        """Create a successful token result."""
        return cls(success=True, tokens=tokens)

    @classmethod
    def fail(
        cls,
        error_message: str,
        error_code: Optional[str] = None,
        is_expired: bool = False,
        is_revoked: bool = False,
    ) -> "TokenResult":
        """Create a failed token result."""
        return cls(
            success=False,
            error_message=error_message,
            error_code=error_code,
            is_expired=is_expired,
            is_revoked=is_revoked,
        )


class SessionResult(BaseModel):
    """Result of session operations."""

    success: bool = False
    session: Optional[SessionResponse] = None
    error_message: Optional[str] = None
    error_code: Optional[str] = None

    @classmethod
    def ok(cls, session: SessionResponse) -> "SessionResult":
        """Create a successful session result."""
        return cls(success=True, session=session)

    @classmethod
    def fail(cls, error_message: str, error_code: Optional[str] = None) -> "SessionResult":
        """Create a failed session result."""
        return cls(success=False, error_message=error_message, error_code=error_code)


class PasswordResult(BaseModel):
    """Result of password operations."""

    success: bool = False
    error_message: Optional[str] = None
    error_code: Optional[str] = None
    password_changed: bool = False
    reset_token_sent: bool = False

    @classmethod
    def ok(cls, password_changed: bool = False, reset_token_sent: bool = False) -> "PasswordResult":
        """Create a successful password result."""
        return cls(success=True, password_changed=password_changed, reset_token_sent=reset_token_sent)

    @classmethod
    def fail(cls, error_message: str, error_code: Optional[str] = None) -> "PasswordResult":
        """Create a failed password result."""
        return cls(success=False, error_message=error_message, error_code=error_code)
