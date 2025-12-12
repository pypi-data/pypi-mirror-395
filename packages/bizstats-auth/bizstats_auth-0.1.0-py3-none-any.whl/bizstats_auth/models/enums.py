"""
Enum definitions for authentication and authorization.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

from enum import Enum


class UserRole(str, Enum):
    """Basic user roles for system-level access."""

    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class UserStatus(str, Enum):
    """User account status."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"
    LOCKED = "locked"


class SessionStatus(str, Enum):
    """User session status."""

    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    LOGGED_OUT = "logged_out"


class TokenType(str, Enum):
    """JWT token types."""

    ACCESS = "access"
    REFRESH = "refresh"
    API_KEY = "api_key"
    PASSWORD_RESET = "password_reset"
    EMAIL_VERIFICATION = "email_verification"


# RBAC Enums for Multi-Tenant Support


class OrganizationRole(str, Enum):
    """Roles within an organization (highest level)."""

    SUPER_ADMIN = "super_admin"  # Full access to everything
    ADMIN = "admin"  # Admin access, can manage teams and projects
    BILLING = "billing"  # Billing and subscription management
    VIEWER = "viewer"  # Read-only access


class TeamRole(str, Enum):
    """Roles within a team (mid level)."""

    LEAD = "lead"  # Team lead, can manage team members and projects
    MEMBER = "member"  # Regular team member
    VIEWER = "viewer"  # Read-only access to team resources


class ProjectRole(str, Enum):
    """Roles within a project (lowest level)."""

    OWNER = "owner"  # Project owner, full control
    EDITOR = "editor"  # Can edit project content
    CONTRIBUTOR = "contributor"  # Can contribute but limited editing
    VIEWER = "viewer"  # Read-only access


class RoleScope(str, Enum):
    """Scope level for role assignments."""

    ORGANIZATION = "organization"
    TEAM = "team"
    PROJECT = "project"


class InvitationStatus(str, Enum):
    """Status of role invitations."""

    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
