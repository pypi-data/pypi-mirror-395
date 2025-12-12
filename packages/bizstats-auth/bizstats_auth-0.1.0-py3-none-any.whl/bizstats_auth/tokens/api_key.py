"""
API key generation and management utilities.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import secrets
import hashlib
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Set, Dict, Any
from dataclasses import dataclass
from pydantic import BaseModel, Field

from bizstats_auth.config import get_config, AuthConfig
from bizstats_auth.rbac.permissions import Permission


class APIKeyCreate(BaseModel):
    """Schema for creating an API key."""

    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    scopes: Optional[List[str]] = None
    permissions: Optional[List[Permission]] = None
    expires_at: Optional[datetime] = None
    organization_id: Optional[str] = None
    project_id: Optional[str] = None
    rate_limit: Optional[int] = None  # Requests per hour
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class APIKey:
    """Represents an API key."""

    id: str
    name: str
    key_prefix: str  # First 8 chars of the key (for display)
    key_hash: str  # SHA-256 hash of the full key
    user_id: str
    organization_id: Optional[str]
    project_id: Optional[str]
    scopes: List[str]
    permissions: Set[Permission]
    created_at: datetime
    expires_at: Optional[datetime]
    last_used_at: Optional[datetime]
    is_active: bool
    rate_limit: Optional[int]
    metadata: Optional[Dict[str, Any]]

    def is_expired(self) -> bool:
        """Check if the API key has expired."""
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) > self.expires_at

    def is_valid(self) -> bool:
        """Check if the API key is valid (active and not expired)."""
        return self.is_active and not self.is_expired()


class APIKeyValidationResult(BaseModel):
    """Result of API key validation."""

    is_valid: bool = False
    api_key: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    error_code: Optional[str] = None


class APIKeyManager:
    """Manages API key operations."""

    def __init__(self, config: Optional[AuthConfig] = None):
        """
        Initialize API key manager.

        Args:
            config: Auth configuration (uses global config if not provided)
        """
        self.config = config or get_config()

    def generate_key(self) -> tuple[str, str, str]:
        """
        Generate a new API key.

        Returns:
            Tuple of (full_key, key_prefix, key_hash)
        """
        # Generate random key
        random_part = secrets.token_urlsafe(self.config.api_key_length)
        full_key = f"{self.config.api_key_prefix}{random_part}"

        # Get prefix for display (first 8 chars after the prefix)
        key_prefix = full_key[: len(self.config.api_key_prefix) + 8]

        # Hash for storage
        key_hash = self._hash_key(full_key)

        return full_key, key_prefix, key_hash

    def _hash_key(self, key: str) -> str:
        """
        Hash an API key for storage.

        Args:
            key: Full API key

        Returns:
            SHA-256 hash of the key
        """
        return hashlib.sha256(key.encode()).hexdigest()

    def validate_key_format(self, key: str) -> bool:
        """
        Validate API key format.

        Args:
            key: API key to validate

        Returns:
            True if format is valid
        """
        if not key:
            return False

        # Check prefix
        if not key.startswith(self.config.api_key_prefix):
            return False

        # Check length
        expected_length = len(self.config.api_key_prefix) + self.config.api_key_length + 5
        # URL-safe base64 adds some padding, so allow some flexibility
        if len(key) < expected_length - 10 or len(key) > expected_length + 10:
            return False

        return True

    def verify_key(self, key: str, stored_hash: str) -> bool:
        """
        Verify an API key against its stored hash.

        Args:
            key: Full API key
            stored_hash: Stored hash to compare against

        Returns:
            True if key matches hash
        """
        return secrets.compare_digest(self._hash_key(key), stored_hash)

    def create_api_key(
        self,
        create_data: APIKeyCreate,
        user_id: str,
    ) -> tuple[str, APIKey]:
        """
        Create a new API key.

        Args:
            create_data: API key creation data
            user_id: ID of the user creating the key

        Returns:
            Tuple of (full_key, api_key_object)
            Note: The full_key should only be shown once to the user
        """
        full_key, key_prefix, key_hash = self.generate_key()

        api_key = APIKey(
            id=secrets.token_urlsafe(16),
            name=create_data.name,
            key_prefix=key_prefix,
            key_hash=key_hash,
            user_id=user_id,
            organization_id=create_data.organization_id,
            project_id=create_data.project_id,
            scopes=create_data.scopes or [],
            permissions=set(create_data.permissions or []),
            created_at=datetime.now(timezone.utc),
            expires_at=create_data.expires_at,
            last_used_at=None,
            is_active=True,
            rate_limit=create_data.rate_limit,
            metadata=create_data.metadata,
        )

        return full_key, api_key

    def validate_api_key(
        self,
        key: str,
        stored_key: APIKey,
    ) -> APIKeyValidationResult:
        """
        Validate an API key against stored data.

        Args:
            key: Full API key from request
            stored_key: Stored API key data

        Returns:
            Validation result
        """
        # Check format
        if not self.validate_key_format(key):
            return APIKeyValidationResult(
                is_valid=False,
                error_message="Invalid API key format",
                error_code="INVALID_FORMAT",
            )

        # Verify hash
        if not self.verify_key(key, stored_key.key_hash):
            return APIKeyValidationResult(
                is_valid=False,
                error_message="Invalid API key",
                error_code="INVALID_KEY",
            )

        # Check if active
        if not stored_key.is_active:
            return APIKeyValidationResult(
                is_valid=False,
                error_message="API key is deactivated",
                error_code="DEACTIVATED",
            )

        # Check expiration
        if stored_key.is_expired():
            return APIKeyValidationResult(
                is_valid=False,
                error_message="API key has expired",
                error_code="EXPIRED",
            )

        return APIKeyValidationResult(
            is_valid=True,
            api_key={
                "id": stored_key.id,
                "name": stored_key.name,
                "user_id": stored_key.user_id,
                "organization_id": stored_key.organization_id,
                "project_id": stored_key.project_id,
                "scopes": stored_key.scopes,
                "permissions": [p.value for p in stored_key.permissions],
            },
        )


# Module-level convenience functions

_api_key_manager: Optional[APIKeyManager] = None


def _get_api_key_manager() -> APIKeyManager:
    """Get the default API key manager instance."""
    global _api_key_manager
    if _api_key_manager is None:
        _api_key_manager = APIKeyManager()
    return _api_key_manager


def generate_api_key() -> tuple[str, str, str]:
    """
    Generate a new API key.

    Returns:
        Tuple of (full_key, key_prefix, key_hash)
    """
    return _get_api_key_manager().generate_key()


def validate_api_key(key: str, stored_key: APIKey) -> APIKeyValidationResult:
    """
    Validate an API key.

    Args:
        key: Full API key from request
        stored_key: Stored API key data

    Returns:
        Validation result
    """
    return _get_api_key_manager().validate_api_key(key, stored_key)


def hash_api_key(key: str) -> str:
    """
    Hash an API key for storage.

    Args:
        key: Full API key

    Returns:
        SHA-256 hash of the key
    """
    return _get_api_key_manager()._hash_key(key)
