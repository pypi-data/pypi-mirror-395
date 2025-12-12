"""
Role hierarchy and management utilities.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

from typing import Set, Dict, List, Optional, Union, Any
from dataclasses import dataclass

from bizstats_auth.models.enums import (
    OrganizationRole,
    TeamRole,
    ProjectRole,
    RoleScope,
)
from bizstats_auth.rbac.permissions import (
    Permission,
    ORGANIZATION_ROLE_PERMISSIONS,
    TEAM_ROLE_PERMISSIONS,
    PROJECT_ROLE_PERMISSIONS,
)


@dataclass
class RoleAssignment:
    """Represents a role assignment at a specific scope."""

    scope: RoleScope
    role: Union[OrganizationRole, TeamRole, ProjectRole]
    resource_id: str  # org_id, team_id, or project_id


class RoleHierarchy:
    """
    Manages role hierarchy and inheritance.

    Role hierarchy (highest to lowest):
    - Organization: super_admin > admin > billing > viewer
    - Team: lead > member > viewer
    - Project: owner > editor > contributor > viewer

    Higher organization roles inherit permissions at lower scopes.
    """

    # Organization role hierarchy (index = power level, higher = more power)
    ORG_HIERARCHY: List[OrganizationRole] = [
        OrganizationRole.VIEWER,
        OrganizationRole.BILLING,
        OrganizationRole.ADMIN,
        OrganizationRole.SUPER_ADMIN,
    ]

    # Team role hierarchy
    TEAM_HIERARCHY: List[TeamRole] = [
        TeamRole.VIEWER,
        TeamRole.MEMBER,
        TeamRole.LEAD,
    ]

    # Project role hierarchy
    PROJECT_HIERARCHY: List[ProjectRole] = [
        ProjectRole.VIEWER,
        ProjectRole.CONTRIBUTOR,
        ProjectRole.EDITOR,
        ProjectRole.OWNER,
    ]

    @classmethod
    def get_role_level(
        cls,
        role: Union[OrganizationRole, TeamRole, ProjectRole],
    ) -> int:
        """
        Get the hierarchy level of a role (higher = more powerful).

        Args:
            role: Role to check

        Returns:
            Hierarchy level (0 = lowest)
        """
        if isinstance(role, OrganizationRole):
            return cls.ORG_HIERARCHY.index(role)
        elif isinstance(role, TeamRole):
            return cls.TEAM_HIERARCHY.index(role)
        elif isinstance(role, ProjectRole):
            return cls.PROJECT_HIERARCHY.index(role)
        return 0

    @classmethod
    def is_role_higher_or_equal(
        cls,
        role1: Union[OrganizationRole, TeamRole, ProjectRole],
        role2: Union[OrganizationRole, TeamRole, ProjectRole],
    ) -> bool:
        """
        Check if role1 is higher or equal to role2 in hierarchy.

        Args:
            role1: First role to compare
            role2: Second role to compare

        Returns:
            True if role1 >= role2 in hierarchy

        Raises:
            ValueError: If roles are from different scopes
        """
        if type(role1) != type(role2):
            raise ValueError("Cannot compare roles from different scopes")

        return cls.get_role_level(role1) >= cls.get_role_level(role2)

    @classmethod
    def get_roles_above(
        cls,
        role: Union[OrganizationRole, TeamRole, ProjectRole],
    ) -> List[Union[OrganizationRole, TeamRole, ProjectRole]]:
        """
        Get all roles higher than the given role in hierarchy.

        Args:
            role: Reference role

        Returns:
            List of roles above the given role
        """
        level = cls.get_role_level(role)

        if isinstance(role, OrganizationRole):
            return cls.ORG_HIERARCHY[level + 1 :]
        elif isinstance(role, TeamRole):
            return cls.TEAM_HIERARCHY[level + 1 :]
        elif isinstance(role, ProjectRole):
            return cls.PROJECT_HIERARCHY[level + 1 :]
        return []

    @classmethod
    def get_roles_at_or_above(
        cls,
        role: Union[OrganizationRole, TeamRole, ProjectRole],
    ) -> List[Union[OrganizationRole, TeamRole, ProjectRole]]:
        """
        Get all roles at or above the given role in hierarchy.

        Args:
            role: Reference role

        Returns:
            List of roles at or above the given role
        """
        level = cls.get_role_level(role)

        if isinstance(role, OrganizationRole):
            return cls.ORG_HIERARCHY[level:]
        elif isinstance(role, TeamRole):
            return cls.TEAM_HIERARCHY[level:]
        elif isinstance(role, ProjectRole):
            return cls.PROJECT_HIERARCHY[level:]
        return []


def get_effective_permissions(
    assignments: List[RoleAssignment],
) -> Set[Permission]:
    """
    Calculate effective permissions from multiple role assignments.

    Permissions are accumulated from all assignments, with higher
    organization roles providing cascading permissions to lower scopes.

    Args:
        assignments: List of role assignments

    Returns:
        Set of effective permissions
    """
    permissions: Set[Permission] = set()

    for assignment in assignments:
        if assignment.scope == RoleScope.ORGANIZATION:
            org_perms = ORGANIZATION_ROLE_PERMISSIONS.get(
                assignment.role, set()  # type: ignore
            )
            permissions.update(org_perms)

        elif assignment.scope == RoleScope.TEAM:
            team_perms = TEAM_ROLE_PERMISSIONS.get(
                assignment.role, set()  # type: ignore
            )
            permissions.update(team_perms)

        elif assignment.scope == RoleScope.PROJECT:
            project_perms = PROJECT_ROLE_PERMISSIONS.get(
                assignment.role, set()  # type: ignore
            )
            permissions.update(project_perms)

    return permissions


def can_manage_role(
    manager_role: Union[OrganizationRole, TeamRole, ProjectRole],
    target_role: Union[OrganizationRole, TeamRole, ProjectRole],
) -> bool:
    """
    Check if a manager can assign/modify a target role.

    Rules:
    - Can only manage roles at the same scope
    - Can only assign roles lower than own role
    - super_admin can manage all roles

    Args:
        manager_role: Role of the person trying to manage
        target_role: Role being assigned/modified

    Returns:
        True if manager can manage the target role
    """
    # Different scopes - check if manager scope is higher
    if type(manager_role) != type(target_role):
        # Organization roles can manage team/project roles
        if isinstance(manager_role, OrganizationRole):
            if manager_role in [OrganizationRole.SUPER_ADMIN, OrganizationRole.ADMIN]:
                return True
        # Team leads can manage project roles
        if isinstance(manager_role, TeamRole) and isinstance(target_role, ProjectRole):
            if manager_role == TeamRole.LEAD:
                return True
        return False

    # Same scope - must be higher in hierarchy
    return RoleHierarchy.is_role_higher_or_equal(manager_role, target_role) and manager_role != target_role


def get_manageable_roles(
    manager_role: Union[OrganizationRole, TeamRole, ProjectRole],
    scope: RoleScope,
) -> List[Union[OrganizationRole, TeamRole, ProjectRole]]:
    """
    Get list of roles that a manager can assign.

    Args:
        manager_role: Role of the manager
        scope: Scope of roles to get

    Returns:
        List of assignable roles
    """
    manageable: List[Union[OrganizationRole, TeamRole, ProjectRole]] = []

    if scope == RoleScope.ORGANIZATION and isinstance(manager_role, OrganizationRole):
        # Can assign roles below own level
        level = RoleHierarchy.get_role_level(manager_role)
        manageable = RoleHierarchy.ORG_HIERARCHY[:level]

    elif scope == RoleScope.TEAM:
        if isinstance(manager_role, OrganizationRole):
            if manager_role in [OrganizationRole.SUPER_ADMIN, OrganizationRole.ADMIN]:
                manageable = list(RoleHierarchy.TEAM_HIERARCHY)
        elif isinstance(manager_role, TeamRole):
            level = RoleHierarchy.get_role_level(manager_role)
            manageable = RoleHierarchy.TEAM_HIERARCHY[:level]

    elif scope == RoleScope.PROJECT:
        if isinstance(manager_role, OrganizationRole):
            if manager_role in [OrganizationRole.SUPER_ADMIN, OrganizationRole.ADMIN]:
                manageable = list(RoleHierarchy.PROJECT_HIERARCHY)
        elif isinstance(manager_role, TeamRole):
            if manager_role == TeamRole.LEAD:
                manageable = list(RoleHierarchy.PROJECT_HIERARCHY)
        elif isinstance(manager_role, ProjectRole):
            level = RoleHierarchy.get_role_level(manager_role)
            manageable = RoleHierarchy.PROJECT_HIERARCHY[:level]

    return manageable
