"""
Permission definitions and checking utilities.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

from enum import Enum
from typing import Set, Dict, List, Optional, Union
from dataclasses import dataclass

from bizstats_auth.models.enums import (
    OrganizationRole,
    TeamRole,
    ProjectRole,
    RoleScope,
)


class Permission(str, Enum):
    """Available permissions in the system."""

    # Organization permissions
    ORG_READ = "org:read"
    ORG_UPDATE = "org:update"
    ORG_DELETE = "org:delete"
    ORG_MANAGE_MEMBERS = "org:manage_members"
    ORG_MANAGE_TEAMS = "org:manage_teams"
    ORG_MANAGE_BILLING = "org:manage_billing"
    ORG_VIEW_ANALYTICS = "org:view_analytics"
    ORG_MANAGE_SETTINGS = "org:manage_settings"

    # Team permissions
    TEAM_CREATE = "team:create"
    TEAM_READ = "team:read"
    TEAM_UPDATE = "team:update"
    TEAM_DELETE = "team:delete"
    TEAM_MANAGE_MEMBERS = "team:manage_members"
    TEAM_MANAGE_PROJECTS = "team:manage_projects"

    # Project permissions
    PROJECT_CREATE = "project:create"
    PROJECT_READ = "project:read"
    PROJECT_UPDATE = "project:update"
    PROJECT_DELETE = "project:delete"
    PROJECT_MANAGE_MEMBERS = "project:manage_members"
    PROJECT_MANAGE_SETTINGS = "project:manage_settings"

    # Chatbot permissions
    CHATBOT_CREATE = "chatbot:create"
    CHATBOT_READ = "chatbot:read"
    CHATBOT_UPDATE = "chatbot:update"
    CHATBOT_DELETE = "chatbot:delete"
    CHATBOT_TRAIN = "chatbot:train"
    CHATBOT_DEPLOY = "chatbot:deploy"
    CHATBOT_VIEW_ANALYTICS = "chatbot:view_analytics"

    # Document permissions
    DOCUMENT_CREATE = "document:create"
    DOCUMENT_READ = "document:read"
    DOCUMENT_UPDATE = "document:update"
    DOCUMENT_DELETE = "document:delete"

    # API Key permissions
    API_KEY_CREATE = "api_key:create"
    API_KEY_READ = "api_key:read"
    API_KEY_DELETE = "api_key:delete"

    # Admin permissions
    ADMIN_ALL = "admin:all"
    ADMIN_USERS = "admin:users"
    ADMIN_BILLING = "admin:billing"
    ADMIN_SYSTEM = "admin:system"


@dataclass
class RolePermissions:
    """Permission set for a role."""

    role: Union[OrganizationRole, TeamRole, ProjectRole]
    scope: RoleScope
    permissions: Set[Permission]


# Organization role permission mappings
ORGANIZATION_ROLE_PERMISSIONS: Dict[OrganizationRole, Set[Permission]] = {
    OrganizationRole.SUPER_ADMIN: {
        Permission.ADMIN_ALL,
        Permission.ORG_READ,
        Permission.ORG_UPDATE,
        Permission.ORG_DELETE,
        Permission.ORG_MANAGE_MEMBERS,
        Permission.ORG_MANAGE_TEAMS,
        Permission.ORG_MANAGE_BILLING,
        Permission.ORG_VIEW_ANALYTICS,
        Permission.ORG_MANAGE_SETTINGS,
        Permission.TEAM_CREATE,
        Permission.TEAM_READ,
        Permission.TEAM_UPDATE,
        Permission.TEAM_DELETE,
        Permission.TEAM_MANAGE_MEMBERS,
        Permission.TEAM_MANAGE_PROJECTS,
        Permission.PROJECT_CREATE,
        Permission.PROJECT_READ,
        Permission.PROJECT_UPDATE,
        Permission.PROJECT_DELETE,
        Permission.PROJECT_MANAGE_MEMBERS,
        Permission.PROJECT_MANAGE_SETTINGS,
        Permission.CHATBOT_CREATE,
        Permission.CHATBOT_READ,
        Permission.CHATBOT_UPDATE,
        Permission.CHATBOT_DELETE,
        Permission.CHATBOT_TRAIN,
        Permission.CHATBOT_DEPLOY,
        Permission.CHATBOT_VIEW_ANALYTICS,
        Permission.DOCUMENT_CREATE,
        Permission.DOCUMENT_READ,
        Permission.DOCUMENT_UPDATE,
        Permission.DOCUMENT_DELETE,
        Permission.API_KEY_CREATE,
        Permission.API_KEY_READ,
        Permission.API_KEY_DELETE,
    },
    OrganizationRole.ADMIN: {
        Permission.ORG_READ,
        Permission.ORG_UPDATE,
        Permission.ORG_MANAGE_MEMBERS,
        Permission.ORG_MANAGE_TEAMS,
        Permission.ORG_VIEW_ANALYTICS,
        Permission.ORG_MANAGE_SETTINGS,
        Permission.TEAM_CREATE,
        Permission.TEAM_READ,
        Permission.TEAM_UPDATE,
        Permission.TEAM_DELETE,
        Permission.TEAM_MANAGE_MEMBERS,
        Permission.TEAM_MANAGE_PROJECTS,
        Permission.PROJECT_CREATE,
        Permission.PROJECT_READ,
        Permission.PROJECT_UPDATE,
        Permission.PROJECT_DELETE,
        Permission.PROJECT_MANAGE_MEMBERS,
        Permission.PROJECT_MANAGE_SETTINGS,
        Permission.CHATBOT_CREATE,
        Permission.CHATBOT_READ,
        Permission.CHATBOT_UPDATE,
        Permission.CHATBOT_DELETE,
        Permission.CHATBOT_TRAIN,
        Permission.CHATBOT_DEPLOY,
        Permission.CHATBOT_VIEW_ANALYTICS,
        Permission.DOCUMENT_CREATE,
        Permission.DOCUMENT_READ,
        Permission.DOCUMENT_UPDATE,
        Permission.DOCUMENT_DELETE,
        Permission.API_KEY_CREATE,
        Permission.API_KEY_READ,
        Permission.API_KEY_DELETE,
    },
    OrganizationRole.BILLING: {
        Permission.ORG_READ,
        Permission.ORG_MANAGE_BILLING,
        Permission.ORG_VIEW_ANALYTICS,
        Permission.TEAM_READ,
        Permission.PROJECT_READ,
        Permission.CHATBOT_READ,
        Permission.CHATBOT_VIEW_ANALYTICS,
    },
    OrganizationRole.VIEWER: {
        Permission.ORG_READ,
        Permission.TEAM_READ,
        Permission.PROJECT_READ,
        Permission.CHATBOT_READ,
        Permission.DOCUMENT_READ,
    },
}

# Team role permission mappings
TEAM_ROLE_PERMISSIONS: Dict[TeamRole, Set[Permission]] = {
    TeamRole.LEAD: {
        Permission.TEAM_READ,
        Permission.TEAM_UPDATE,
        Permission.TEAM_MANAGE_MEMBERS,
        Permission.TEAM_MANAGE_PROJECTS,
        Permission.PROJECT_CREATE,
        Permission.PROJECT_READ,
        Permission.PROJECT_UPDATE,
        Permission.PROJECT_DELETE,
        Permission.PROJECT_MANAGE_MEMBERS,
        Permission.PROJECT_MANAGE_SETTINGS,
        Permission.CHATBOT_CREATE,
        Permission.CHATBOT_READ,
        Permission.CHATBOT_UPDATE,
        Permission.CHATBOT_DELETE,
        Permission.CHATBOT_TRAIN,
        Permission.CHATBOT_DEPLOY,
        Permission.CHATBOT_VIEW_ANALYTICS,
        Permission.DOCUMENT_CREATE,
        Permission.DOCUMENT_READ,
        Permission.DOCUMENT_UPDATE,
        Permission.DOCUMENT_DELETE,
        Permission.API_KEY_CREATE,
        Permission.API_KEY_READ,
        Permission.API_KEY_DELETE,
    },
    TeamRole.MEMBER: {
        Permission.TEAM_READ,
        Permission.PROJECT_READ,
        Permission.PROJECT_UPDATE,
        Permission.CHATBOT_CREATE,
        Permission.CHATBOT_READ,
        Permission.CHATBOT_UPDATE,
        Permission.CHATBOT_TRAIN,
        Permission.CHATBOT_VIEW_ANALYTICS,
        Permission.DOCUMENT_CREATE,
        Permission.DOCUMENT_READ,
        Permission.DOCUMENT_UPDATE,
    },
    TeamRole.VIEWER: {
        Permission.TEAM_READ,
        Permission.PROJECT_READ,
        Permission.CHATBOT_READ,
        Permission.DOCUMENT_READ,
    },
}

# Project role permission mappings
PROJECT_ROLE_PERMISSIONS: Dict[ProjectRole, Set[Permission]] = {
    ProjectRole.OWNER: {
        Permission.PROJECT_READ,
        Permission.PROJECT_UPDATE,
        Permission.PROJECT_DELETE,
        Permission.PROJECT_MANAGE_MEMBERS,
        Permission.PROJECT_MANAGE_SETTINGS,
        Permission.CHATBOT_CREATE,
        Permission.CHATBOT_READ,
        Permission.CHATBOT_UPDATE,
        Permission.CHATBOT_DELETE,
        Permission.CHATBOT_TRAIN,
        Permission.CHATBOT_DEPLOY,
        Permission.CHATBOT_VIEW_ANALYTICS,
        Permission.DOCUMENT_CREATE,
        Permission.DOCUMENT_READ,
        Permission.DOCUMENT_UPDATE,
        Permission.DOCUMENT_DELETE,
        Permission.API_KEY_CREATE,
        Permission.API_KEY_READ,
        Permission.API_KEY_DELETE,
    },
    ProjectRole.EDITOR: {
        Permission.PROJECT_READ,
        Permission.PROJECT_UPDATE,
        Permission.CHATBOT_READ,
        Permission.CHATBOT_UPDATE,
        Permission.CHATBOT_TRAIN,
        Permission.CHATBOT_VIEW_ANALYTICS,
        Permission.DOCUMENT_CREATE,
        Permission.DOCUMENT_READ,
        Permission.DOCUMENT_UPDATE,
        Permission.DOCUMENT_DELETE,
    },
    ProjectRole.CONTRIBUTOR: {
        Permission.PROJECT_READ,
        Permission.CHATBOT_READ,
        Permission.CHATBOT_TRAIN,
        Permission.DOCUMENT_CREATE,
        Permission.DOCUMENT_READ,
        Permission.DOCUMENT_UPDATE,
    },
    ProjectRole.VIEWER: {
        Permission.PROJECT_READ,
        Permission.CHATBOT_READ,
        Permission.DOCUMENT_READ,
    },
}


class PermissionChecker:
    """Utility class for checking permissions."""

    def __init__(
        self,
        organization_role: Optional[OrganizationRole] = None,
        team_role: Optional[TeamRole] = None,
        project_role: Optional[ProjectRole] = None,
    ):
        """
        Initialize permission checker with user's roles.

        Args:
            organization_role: User's organization role
            team_role: User's team role
            project_role: User's project role
        """
        self.organization_role = organization_role
        self.team_role = team_role
        self.project_role = project_role
        self._permissions = self._compute_permissions()

    def _compute_permissions(self) -> Set[Permission]:
        """Compute effective permissions from all roles."""
        permissions: Set[Permission] = set()

        if self.organization_role:
            permissions.update(
                ORGANIZATION_ROLE_PERMISSIONS.get(self.organization_role, set())
            )

        if self.team_role:
            permissions.update(TEAM_ROLE_PERMISSIONS.get(self.team_role, set()))

        if self.project_role:
            permissions.update(PROJECT_ROLE_PERMISSIONS.get(self.project_role, set()))

        return permissions

    def has_permission(self, permission: Permission) -> bool:
        """
        Check if user has a specific permission.

        Args:
            permission: Permission to check

        Returns:
            True if user has the permission
        """
        # Super admin has all permissions
        if Permission.ADMIN_ALL in self._permissions:
            return True
        return permission in self._permissions

    def has_any_permission(self, permissions: List[Permission]) -> bool:
        """
        Check if user has any of the specified permissions.

        Args:
            permissions: List of permissions to check

        Returns:
            True if user has at least one permission
        """
        if Permission.ADMIN_ALL in self._permissions:
            return True
        return bool(self._permissions.intersection(permissions))

    def has_all_permissions(self, permissions: List[Permission]) -> bool:
        """
        Check if user has all specified permissions.

        Args:
            permissions: List of permissions to check

        Returns:
            True if user has all permissions
        """
        if Permission.ADMIN_ALL in self._permissions:
            return True
        return all(p in self._permissions for p in permissions)

    def get_permissions(self) -> Set[Permission]:
        """Get all effective permissions."""
        return self._permissions.copy()


def get_role_permissions(
    role: Union[OrganizationRole, TeamRole, ProjectRole],
    scope: RoleScope,
) -> Set[Permission]:
    """
    Get permissions for a specific role.

    Args:
        role: The role to get permissions for
        scope: The scope of the role

    Returns:
        Set of permissions for the role
    """
    if scope == RoleScope.ORGANIZATION:
        return ORGANIZATION_ROLE_PERMISSIONS.get(role, set()).copy()  # type: ignore
    elif scope == RoleScope.TEAM:
        return TEAM_ROLE_PERMISSIONS.get(role, set()).copy()  # type: ignore
    elif scope == RoleScope.PROJECT:
        return PROJECT_ROLE_PERMISSIONS.get(role, set()).copy()  # type: ignore
    return set()


def check_permission(
    permission: Permission,
    organization_role: Optional[OrganizationRole] = None,
    team_role: Optional[TeamRole] = None,
    project_role: Optional[ProjectRole] = None,
) -> bool:
    """
    Quick check if a user has a specific permission.

    Args:
        permission: Permission to check
        organization_role: User's organization role
        team_role: User's team role
        project_role: User's project role

    Returns:
        True if user has the permission
    """
    checker = PermissionChecker(
        organization_role=organization_role,
        team_role=team_role,
        project_role=project_role,
    )
    return checker.has_permission(permission)
