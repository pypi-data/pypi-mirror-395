"""
Tests for API key management.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import pytest
from datetime import datetime, timezone, timedelta

from bizstats_auth.tokens.api_key import (
    APIKeyManager,
    APIKey,
    APIKeyCreate,
    APIKeyValidationResult,
    generate_api_key,
    validate_api_key,
    hash_api_key,
)
from bizstats_auth.rbac.permissions import Permission


class TestAPIKeyManager:
    """Tests for APIKeyManager class."""

    def test_generate_key(self, api_key_manager, test_config):
        """Test generating an API key."""
        full_key, key_prefix, key_hash = api_key_manager.generate_key()

        # Check format
        assert full_key.startswith(test_config.api_key_prefix)
        assert key_prefix.startswith(test_config.api_key_prefix)
        assert len(key_prefix) == len(test_config.api_key_prefix) + 8

        # Check hash
        assert len(key_hash) == 64  # SHA-256 hex

    def test_generated_keys_are_unique(self, api_key_manager):
        """Test that generated keys are unique."""
        key1, _, hash1 = api_key_manager.generate_key()
        key2, _, hash2 = api_key_manager.generate_key()

        assert key1 != key2
        assert hash1 != hash2

    def test_validate_key_format_valid(self, api_key_manager, test_config):
        """Test validating a valid key format."""
        full_key, _, _ = api_key_manager.generate_key()

        assert api_key_manager.validate_key_format(full_key) is True

    def test_validate_key_format_wrong_prefix(self, api_key_manager):
        """Test validating key with wrong prefix."""
        assert api_key_manager.validate_key_format("wrong_prefix_abc123") is False

    def test_validate_key_format_empty(self, api_key_manager):
        """Test validating empty key."""
        assert api_key_manager.validate_key_format("") is False

    def test_validate_key_format_too_short(self, api_key_manager, test_config):
        """Test validating too short key."""
        assert api_key_manager.validate_key_format(test_config.api_key_prefix + "abc") is False

    def test_verify_key(self, api_key_manager):
        """Test verifying key against stored hash."""
        full_key, _, key_hash = api_key_manager.generate_key()

        assert api_key_manager.verify_key(full_key, key_hash) is True
        assert api_key_manager.verify_key("wrong_key", key_hash) is False

    def test_create_api_key(self, api_key_manager):
        """Test creating an API key."""
        create_data = APIKeyCreate(
            name="Test API Key",
            description="For testing",
            scopes=["read", "write"],
            permissions=[Permission.CHATBOT_READ],
            organization_id="org_123",
            rate_limit=1000,
        )

        full_key, api_key = api_key_manager.create_api_key(
            create_data=create_data,
            user_id="user_123",
        )

        assert full_key is not None
        assert api_key.name == "Test API Key"
        assert api_key.user_id == "user_123"
        assert api_key.organization_id == "org_123"
        assert api_key.scopes == ["read", "write"]
        assert Permission.CHATBOT_READ in api_key.permissions
        assert api_key.rate_limit == 1000
        assert api_key.is_active is True

    def test_validate_api_key_valid(self, api_key_manager):
        """Test validating a valid API key."""
        # Create a key
        full_key, _, key_hash = api_key_manager.generate_key()

        # Create stored key with matching hash
        stored_key = APIKey(
            id="key_123",
            name="Test Key",
            key_prefix=full_key[:16],
            key_hash=key_hash,
            user_id="user_123",
            organization_id="org_123",
            project_id=None,
            scopes=["read"],
            permissions=set(),
            created_at=datetime.now(timezone.utc),
            expires_at=datetime.now(timezone.utc) + timedelta(days=30),
            last_used_at=None,
            is_active=True,
            rate_limit=None,
            metadata=None,
        )

        result = api_key_manager.validate_api_key(full_key, stored_key)

        assert result.is_valid is True
        assert result.api_key is not None
        assert result.api_key["user_id"] == "user_123"

    def test_validate_api_key_wrong_key(self, api_key_manager):
        """Test validating wrong API key."""
        # Generate the correct key but use a different one for validation
        _, _, key_hash = api_key_manager.generate_key()
        wrong_key, _, _ = api_key_manager.generate_key()  # Different key

        stored_key = APIKey(
            id="key_123",
            name="Test Key",
            key_prefix="biz_test_xyz",
            key_hash=key_hash,
            user_id="user_123",
            organization_id=None,
            project_id=None,
            scopes=[],
            permissions=set(),
            created_at=datetime.now(timezone.utc),
            expires_at=None,
            last_used_at=None,
            is_active=True,
            rate_limit=None,
            metadata=None,
        )

        result = api_key_manager.validate_api_key(wrong_key, stored_key)

        assert result.is_valid is False
        assert result.error_code == "INVALID_KEY"

    def test_validate_api_key_deactivated(self, api_key_manager):
        """Test validating a deactivated API key."""
        full_key, _, key_hash = api_key_manager.generate_key()

        stored_key = APIKey(
            id="key_123",
            name="Test Key",
            key_prefix=full_key[:16],
            key_hash=key_hash,
            user_id="user_123",
            organization_id=None,
            project_id=None,
            scopes=[],
            permissions=set(),
            created_at=datetime.now(timezone.utc),
            expires_at=None,
            last_used_at=None,
            is_active=False,  # Deactivated
            rate_limit=None,
            metadata=None,
        )

        result = api_key_manager.validate_api_key(full_key, stored_key)

        assert result.is_valid is False
        assert result.error_code == "DEACTIVATED"

    def test_validate_api_key_expired(self, api_key_manager):
        """Test validating an expired API key."""
        full_key, _, key_hash = api_key_manager.generate_key()

        stored_key = APIKey(
            id="key_123",
            name="Test Key",
            key_prefix=full_key[:16],
            key_hash=key_hash,
            user_id="user_123",
            organization_id=None,
            project_id=None,
            scopes=[],
            permissions=set(),
            created_at=datetime.now(timezone.utc) - timedelta(days=60),
            expires_at=datetime.now(timezone.utc) - timedelta(days=1),  # Expired
            last_used_at=None,
            is_active=True,
            rate_limit=None,
            metadata=None,
        )

        result = api_key_manager.validate_api_key(full_key, stored_key)

        assert result.is_valid is False
        assert result.error_code == "EXPIRED"


class TestAPIKey:
    """Tests for APIKey dataclass."""

    def test_is_expired_false(self, sample_api_key):
        """Test is_expired returns false for valid key."""
        assert sample_api_key.is_expired() is False

    def test_is_expired_true(self, sample_api_key):
        """Test is_expired returns true for expired key."""
        sample_api_key.expires_at = datetime.now(timezone.utc) - timedelta(days=1)
        assert sample_api_key.is_expired() is True

    def test_is_expired_no_expiration(self, sample_api_key):
        """Test is_expired returns false when no expiration set."""
        sample_api_key.expires_at = None
        assert sample_api_key.is_expired() is False

    def test_is_valid_active_not_expired(self, sample_api_key):
        """Test is_valid for active non-expired key."""
        assert sample_api_key.is_valid() is True

    def test_is_valid_inactive(self, sample_api_key):
        """Test is_valid returns false for inactive key."""
        sample_api_key.is_active = False
        assert sample_api_key.is_valid() is False

    def test_is_valid_expired(self, sample_api_key):
        """Test is_valid returns false for expired key."""
        sample_api_key.expires_at = datetime.now(timezone.utc) - timedelta(days=1)
        assert sample_api_key.is_valid() is False


class TestAPIKeyCreate:
    """Tests for APIKeyCreate schema."""

    def test_create_minimal(self):
        """Test creating API key with minimal data."""
        create = APIKeyCreate(name="Test Key")

        assert create.name == "Test Key"
        assert create.scopes is None
        assert create.permissions is None

    def test_create_full(self):
        """Test creating API key with all fields."""
        create = APIKeyCreate(
            name="Full Test Key",
            description="A detailed description",
            scopes=["read", "write", "admin"],
            permissions=[Permission.CHATBOT_READ, Permission.CHATBOT_UPDATE],
            expires_at=datetime.now(timezone.utc) + timedelta(days=90),
            organization_id="org_456",
            project_id="proj_789",
            rate_limit=5000,
            metadata={"env": "production"},
        )

        assert create.name == "Full Test Key"
        assert len(create.scopes) == 3
        assert len(create.permissions) == 2
        assert create.rate_limit == 5000

    def test_name_validation_empty(self):
        """Test name cannot be empty."""
        with pytest.raises(ValueError):
            APIKeyCreate(name="")

    def test_name_validation_too_long(self):
        """Test name cannot be too long."""
        with pytest.raises(ValueError):
            APIKeyCreate(name="x" * 101)


class TestModuleFunctions:
    """Tests for module-level convenience functions."""

    def test_generate_api_key(self, test_config):
        """Test generate_api_key function."""
        full_key, prefix, key_hash = generate_api_key()

        assert full_key.startswith(test_config.api_key_prefix)
        assert len(key_hash) == 64

    def test_hash_api_key(self, test_config):
        """Test hash_api_key function."""
        key = "biz_test_somekey123"
        hashed = hash_api_key(key)

        assert len(hashed) == 64
        # Same input should produce same hash
        assert hash_api_key(key) == hashed

    def test_validate_api_key(self, test_config, api_key_manager):
        """Test validate_api_key function."""
        full_key, _, key_hash = api_key_manager.generate_key()

        stored_key = APIKey(
            id="key_123",
            name="Test Key",
            key_prefix=full_key[:16],
            key_hash=key_hash,
            user_id="user_123",
            organization_id=None,
            project_id=None,
            scopes=[],
            permissions=set(),
            created_at=datetime.now(timezone.utc),
            expires_at=None,
            last_used_at=None,
            is_active=True,
            rate_limit=None,
            metadata=None,
        )

        result = validate_api_key(full_key, stored_key)
        assert result.is_valid is True
