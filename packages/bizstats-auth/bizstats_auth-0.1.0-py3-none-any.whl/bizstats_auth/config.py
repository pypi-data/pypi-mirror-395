"""
Configuration settings for BizStats Auth.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class AuthConfig(BaseSettings):
    """Authentication configuration settings."""

    # JWT Configuration
    jwt_secret_key: str = Field(
        default="change-me-in-production",
        description="Secret key for JWT token signing",
    )
    jwt_algorithm: str = Field(
        default="HS256",
        description="Algorithm for JWT token signing",
    )
    access_token_expire_minutes: int = Field(
        default=30,
        description="Access token expiration time in minutes",
    )
    refresh_token_expire_days: int = Field(
        default=7,
        description="Refresh token expiration time in days",
    )

    # Password Configuration
    password_min_length: int = Field(
        default=8,
        description="Minimum password length",
    )
    password_require_uppercase: bool = Field(
        default=True,
        description="Require uppercase letters in password",
    )
    password_require_lowercase: bool = Field(
        default=True,
        description="Require lowercase letters in password",
    )
    password_require_digit: bool = Field(
        default=True,
        description="Require digits in password",
    )
    password_require_special: bool = Field(
        default=True,
        description="Require special characters in password",
    )

    # Session Configuration
    session_max_age_hours: int = Field(
        default=24,
        description="Maximum session age in hours",
    )
    session_refresh_threshold_minutes: int = Field(
        default=30,
        description="Threshold before session expiry to allow refresh",
    )

    # API Key Configuration
    api_key_prefix: str = Field(
        default="biz_",
        description="Prefix for generated API keys",
    )
    api_key_length: int = Field(
        default=32,
        description="Length of generated API keys (excluding prefix)",
    )

    # Rate Limiting
    max_login_attempts: int = Field(
        default=5,
        description="Maximum login attempts before lockout",
    )
    lockout_duration_minutes: int = Field(
        default=15,
        description="Account lockout duration in minutes",
    )

    # Multi-tenant Configuration
    enable_multi_tenant: bool = Field(
        default=True,
        description="Enable multi-tenant support",
    )
    default_organization_role: str = Field(
        default="viewer",
        description="Default role for new organization members",
    )

    model_config = {
        "env_prefix": "AUTH_",
        "case_sensitive": False,
    }


# Global configuration instance
_config: Optional[AuthConfig] = None


def get_config() -> AuthConfig:
    """Get the global auth configuration."""
    global _config
    if _config is None:
        _config = AuthConfig()
    return _config


def configure(config: AuthConfig) -> None:
    """Set the global auth configuration."""
    global _config
    _config = config
