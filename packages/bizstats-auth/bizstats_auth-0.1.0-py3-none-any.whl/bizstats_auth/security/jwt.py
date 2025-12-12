"""
JWT token management utilities.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List
import uuid

from jose import jwt, JWTError as JoseJWTError, ExpiredSignatureError

from bizstats_auth.config import get_config, AuthConfig
from bizstats_auth.models.enums import TokenType
from bizstats_auth.models.schemas import TokenPayload, TokenResponse


class AuthJWTError(Exception):
    """JWT-related error."""

    pass


class TokenExpiredError(AuthJWTError):
    """Token has expired."""

    pass


class TokenInvalidError(AuthJWTError):
    """Token is invalid."""

    pass


class JWTManager:
    """JWT token management."""

    def __init__(self, config: Optional[AuthConfig] = None):
        """
        Initialize JWT manager.

        Args:
            config: Auth configuration (uses global config if not provided)
        """
        self.config = config or get_config()

    def create_access_token(
        self,
        subject: str,
        expires_delta: Optional[timedelta] = None,
        scope: Optional[List[str]] = None,
        organization_id: Optional[str] = None,
        roles: Optional[Dict[str, str]] = None,
        additional_claims: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Create an access token.

        Args:
            subject: Token subject (usually user ID)
            expires_delta: Custom expiration time
            scope: List of permission scopes
            organization_id: Organization context
            roles: Role assignments by scope
            additional_claims: Additional JWT claims

        Returns:
            Encoded JWT token string
        """
        if expires_delta is None:
            expires_delta = timedelta(minutes=self.config.access_token_expire_minutes)

        return self._create_token(
            subject=subject,
            token_type=TokenType.ACCESS,
            expires_delta=expires_delta,
            scope=scope,
            organization_id=organization_id,
            roles=roles,
            additional_claims=additional_claims,
        )

    def create_refresh_token(
        self,
        subject: str,
        expires_delta: Optional[timedelta] = None,
        organization_id: Optional[str] = None,
    ) -> str:
        """
        Create a refresh token.

        Args:
            subject: Token subject (usually user ID)
            expires_delta: Custom expiration time
            organization_id: Organization context

        Returns:
            Encoded JWT token string
        """
        if expires_delta is None:
            expires_delta = timedelta(days=self.config.refresh_token_expire_days)

        return self._create_token(
            subject=subject,
            token_type=TokenType.REFRESH,
            expires_delta=expires_delta,
            organization_id=organization_id,
        )

    def create_password_reset_token(
        self,
        subject: str,
        expires_minutes: int = 60,
    ) -> str:
        """
        Create a password reset token.

        Args:
            subject: Token subject (usually user ID or email)
            expires_minutes: Token validity in minutes

        Returns:
            Encoded JWT token string
        """
        return self._create_token(
            subject=subject,
            token_type=TokenType.PASSWORD_RESET,
            expires_delta=timedelta(minutes=expires_minutes),
        )

    def create_email_verification_token(
        self,
        subject: str,
        expires_hours: int = 24,
    ) -> str:
        """
        Create an email verification token.

        Args:
            subject: Token subject (usually user ID or email)
            expires_hours: Token validity in hours

        Returns:
            Encoded JWT token string
        """
        return self._create_token(
            subject=subject,
            token_type=TokenType.EMAIL_VERIFICATION,
            expires_delta=timedelta(hours=expires_hours),
        )

    def _create_token(
        self,
        subject: str,
        token_type: TokenType,
        expires_delta: timedelta,
        scope: Optional[List[str]] = None,
        organization_id: Optional[str] = None,
        roles: Optional[Dict[str, str]] = None,
        additional_claims: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Create a JWT token.

        Args:
            subject: Token subject
            token_type: Type of token
            expires_delta: Token expiration time
            scope: Permission scopes
            organization_id: Organization context
            roles: Role assignments
            additional_claims: Additional claims

        Returns:
            Encoded JWT token string
        """
        now = datetime.now(timezone.utc)
        expire = now + expires_delta

        claims = {
            "sub": subject,
            "exp": expire,
            "iat": now,
            "jti": str(uuid.uuid4()),
            "type": token_type.value,
        }

        if scope:
            claims["scope"] = scope
        if organization_id:
            claims["org_id"] = organization_id
        if roles:
            claims["roles"] = roles
        if additional_claims:
            claims.update(additional_claims)

        return jwt.encode(
            claims,
            self.config.jwt_secret_key,
            algorithm=self.config.jwt_algorithm,
        )

    def verify_token(
        self,
        token: str,
        expected_type: Optional[TokenType] = None,
    ) -> TokenPayload:
        """
        Verify and decode a token.

        Args:
            token: JWT token string
            expected_type: Expected token type (validates if provided)

        Returns:
            Decoded token payload

        Raises:
            TokenExpiredError: If token has expired
            TokenInvalidError: If token is invalid
        """
        try:
            payload = jwt.decode(
                token,
                self.config.jwt_secret_key,
                algorithms=[self.config.jwt_algorithm],
            )
        except ExpiredSignatureError:
            raise TokenExpiredError("Token has expired")
        except JoseJWTError as e:
            raise TokenInvalidError(f"Invalid token: {str(e)}")

        # Validate token type if expected
        if expected_type is not None:
            token_type = payload.get("type")
            if token_type != expected_type.value:
                raise TokenInvalidError(
                    f"Expected token type {expected_type.value}, got {token_type}"
                )

        # Parse into TokenPayload
        return TokenPayload(
            sub=payload["sub"],
            exp=datetime.fromtimestamp(payload["exp"], tz=timezone.utc),
            iat=datetime.fromtimestamp(payload["iat"], tz=timezone.utc),
            jti=payload.get("jti"),
            type=TokenType(payload.get("type", TokenType.ACCESS.value)),
            scope=payload.get("scope"),
            organization_id=payload.get("org_id"),
            roles=payload.get("roles"),
        )

    def decode_token(self, token: str, verify: bool = True) -> Dict[str, Any]:
        """
        Decode a token without full validation.

        Args:
            token: JWT token string
            verify: Whether to verify signature

        Returns:
            Raw token payload dictionary
        """
        options = {"verify_signature": verify}
        if not verify:
            options["verify_exp"] = False

        try:
            return jwt.decode(
                token,
                self.config.jwt_secret_key,
                algorithms=[self.config.jwt_algorithm],
                options=options,
            )
        except JoseJWTError as e:
            raise TokenInvalidError(f"Failed to decode token: {str(e)}")

    def create_token_response(
        self,
        subject: str,
        scope: Optional[List[str]] = None,
        organization_id: Optional[str] = None,
        roles: Optional[Dict[str, str]] = None,
        include_refresh: bool = True,
    ) -> TokenResponse:
        """
        Create a complete token response with access and refresh tokens.

        Args:
            subject: Token subject (user ID)
            scope: Permission scopes
            organization_id: Organization context
            roles: Role assignments
            include_refresh: Whether to include refresh token

        Returns:
            TokenResponse with access and optional refresh tokens
        """
        access_token = self.create_access_token(
            subject=subject,
            scope=scope,
            organization_id=organization_id,
            roles=roles,
        )

        refresh_token = None
        if include_refresh:
            refresh_token = self.create_refresh_token(
                subject=subject,
                organization_id=organization_id,
            )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
            expires_in=self.config.access_token_expire_minutes * 60,
            scope=scope,
        )


# Module-level convenience functions

_jwt_manager: Optional[JWTManager] = None


def _get_jwt_manager() -> JWTManager:
    """Get the default JWT manager instance."""
    global _jwt_manager
    if _jwt_manager is None:
        _jwt_manager = JWTManager()
    return _jwt_manager


def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None,
    scope: Optional[List[str]] = None,
    organization_id: Optional[str] = None,
    roles: Optional[Dict[str, str]] = None,
) -> str:
    """
    Create an access token using the default manager.

    Args:
        subject: Token subject (user ID)
        expires_delta: Custom expiration time
        scope: Permission scopes
        organization_id: Organization context
        roles: Role assignments

    Returns:
        Encoded JWT token string
    """
    return _get_jwt_manager().create_access_token(
        subject=subject,
        expires_delta=expires_delta,
        scope=scope,
        organization_id=organization_id,
        roles=roles,
    )


def create_refresh_token(
    subject: str,
    expires_delta: Optional[timedelta] = None,
    organization_id: Optional[str] = None,
) -> str:
    """
    Create a refresh token using the default manager.

    Args:
        subject: Token subject (user ID)
        expires_delta: Custom expiration time
        organization_id: Organization context

    Returns:
        Encoded JWT token string
    """
    return _get_jwt_manager().create_refresh_token(
        subject=subject,
        expires_delta=expires_delta,
        organization_id=organization_id,
    )


def verify_token(
    token: str,
    expected_type: Optional[TokenType] = None,
) -> TokenPayload:
    """
    Verify and decode a token using the default manager.

    Args:
        token: JWT token string
        expected_type: Expected token type

    Returns:
        Decoded token payload

    Raises:
        TokenExpiredError: If token has expired
        TokenInvalidError: If token is invalid
    """
    return _get_jwt_manager().verify_token(token, expected_type)


def decode_token(token: str, verify: bool = True) -> Dict[str, Any]:
    """
    Decode a token using the default manager.

    Args:
        token: JWT token string
        verify: Whether to verify signature

    Returns:
        Raw token payload dictionary
    """
    return _get_jwt_manager().decode_token(token, verify)
