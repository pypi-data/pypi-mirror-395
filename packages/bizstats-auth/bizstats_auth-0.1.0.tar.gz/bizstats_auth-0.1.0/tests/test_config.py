"""
Tests for auth configuration.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import pytest
from bizstats_auth.config import AuthConfig, get_config, configure


class TestAuthConfig:
    """Tests for AuthConfig class."""

    def test_default_values(self):
        """Test default configuration values."""
        config = AuthConfig()

        assert config.jwt_algorithm == "HS256"
        assert config.access_token_expire_minutes == 30
        assert config.refresh_token_expire_days == 7
        assert config.password_min_length == 8
        assert config.password_require_uppercase is True
        assert config.password_require_lowercase is True
        assert config.password_require_digit is True
        assert config.password_require_special is True
        assert config.api_key_prefix == "biz_"
        assert config.api_key_length == 32
        assert config.max_login_attempts == 5
        assert config.lockout_duration_minutes == 15
        assert config.enable_multi_tenant is True

    def test_custom_values(self):
        """Test configuration with custom values."""
        config = AuthConfig(
            jwt_secret_key="custom-secret",
            access_token_expire_minutes=60,
            password_min_length=12,
            api_key_prefix="custom_",
            max_login_attempts=3,
        )

        assert config.jwt_secret_key == "custom-secret"
        assert config.access_token_expire_minutes == 60
        assert config.password_min_length == 12
        assert config.api_key_prefix == "custom_"
        assert config.max_login_attempts == 3


class TestConfigFunctions:
    """Tests for configuration functions."""

    def test_get_config_returns_instance(self):
        """Test get_config returns a config instance."""
        config = get_config()

        assert isinstance(config, AuthConfig)

    def test_configure_sets_global(self):
        """Test configure sets global config."""
        custom_config = AuthConfig(
            jwt_secret_key="test-secret",
            access_token_expire_minutes=45,
        )

        configure(custom_config)
        config = get_config()

        assert config.jwt_secret_key == "test-secret"
        assert config.access_token_expire_minutes == 45
