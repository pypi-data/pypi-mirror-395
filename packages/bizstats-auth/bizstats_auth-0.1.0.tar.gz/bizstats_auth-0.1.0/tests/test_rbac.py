"""
Tests for RBAC (Role-Based Access Control) system.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import pytest
from bizstats_auth.models.enums import (
    OrganizationRole,
    TeamRole,
    ProjectRole,
    RoleScope,
)
from bizstats_auth.rbac.permissions import (
    Permission,
    PermissionChecker,
    get_role_permissions,
    check_permission,
    ORGANIZATION_ROLE_PERMISSIONS,
    TEAM_ROLE_PERMISSIONS,
    PROJECT_ROLE_PERMISSIONS,
)
from bizstats_auth.rbac.roles import (
    RoleHierarchy,
    RoleAssignment,
    get_effective_permissions,
    can_manage_role,
    get_manageable_roles,
)


class TestPermissions:
    """Tests for Permission enum."""

    def test_permission_values(self):
        """Test permission enum values."""
        assert Permission.ORG_READ.value == "org:read"
        assert Permission.PROJECT_CREATE.value == "project:create"
        assert Permission.CHATBOT_DEPLOY.value == "chatbot:deploy"
        assert Permission.ADMIN_ALL.value == "admin:all"

    def test_permission_is_string(self):
        """Test permissions can be used as strings."""
        assert Permission.ORG_READ.value == "org:read"


class TestPermissionChecker:
    """Tests for PermissionChecker class."""

    def test_super_admin_has_all_permissions(self, super_admin_checker):
        """Test super admin has all permissions."""
        assert super_admin_checker.has_permission(Permission.ORG_DELETE)
        assert super_admin_checker.has_permission(Permission.ADMIN_ALL)
        assert super_admin_checker.has_permission(Permission.CHATBOT_DEPLOY)
        assert super_admin_checker.has_permission(Permission.PROJECT_DELETE)

    def test_org_admin_permissions(self, org_admin_checker):
        """Test org admin has correct permissions."""
        # Should have
        assert org_admin_checker.has_permission(Permission.ORG_READ)
        assert org_admin_checker.has_permission(Permission.ORG_UPDATE)
        assert org_admin_checker.has_permission(Permission.ORG_MANAGE_MEMBERS)
        assert org_admin_checker.has_permission(Permission.TEAM_CREATE)

        # Should not have
        assert not org_admin_checker.has_permission(Permission.ORG_DELETE)  # Only super_admin

    def test_team_lead_permissions(self, team_lead_checker):
        """Test team lead has correct permissions."""
        # Should have from team lead role
        assert team_lead_checker.has_permission(Permission.TEAM_UPDATE)
        assert team_lead_checker.has_permission(Permission.TEAM_MANAGE_MEMBERS)
        assert team_lead_checker.has_permission(Permission.PROJECT_CREATE)

        # Should have from org viewer role
        assert team_lead_checker.has_permission(Permission.ORG_READ)

        # Should not have
        assert not team_lead_checker.has_permission(Permission.ORG_MANAGE_MEMBERS)

    def test_project_viewer_permissions(self, project_viewer_checker):
        """Test project viewer has limited permissions."""
        # Should have
        assert project_viewer_checker.has_permission(Permission.PROJECT_READ)
        assert project_viewer_checker.has_permission(Permission.CHATBOT_READ)
        assert project_viewer_checker.has_permission(Permission.DOCUMENT_READ)

        # Should not have
        assert not project_viewer_checker.has_permission(Permission.PROJECT_UPDATE)
        assert not project_viewer_checker.has_permission(Permission.CHATBOT_UPDATE)
        assert not project_viewer_checker.has_permission(Permission.DOCUMENT_CREATE)

    def test_has_any_permission(self, org_admin_checker):
        """Test has_any_permission method."""
        assert org_admin_checker.has_any_permission([
            Permission.ORG_DELETE,  # No
            Permission.ORG_READ,    # Yes
        ])

        assert not org_admin_checker.has_any_permission([
            Permission.ADMIN_ALL,   # No
            Permission.ORG_DELETE,  # No
        ])

    def test_has_all_permissions(self, org_admin_checker):
        """Test has_all_permissions method."""
        assert org_admin_checker.has_all_permissions([
            Permission.ORG_READ,
            Permission.ORG_UPDATE,
        ])

        assert not org_admin_checker.has_all_permissions([
            Permission.ORG_READ,
            Permission.ORG_DELETE,  # Only super_admin
        ])

    def test_get_permissions(self, team_lead_checker):
        """Test get_permissions returns all permissions."""
        permissions = team_lead_checker.get_permissions()

        assert Permission.TEAM_UPDATE in permissions
        assert Permission.ORG_READ in permissions  # From org viewer
        assert isinstance(permissions, set)


class TestRolePermissionMappings:
    """Tests for role permission mappings."""

    def test_super_admin_has_admin_all(self):
        """Test super admin has ADMIN_ALL permission."""
        perms = ORGANIZATION_ROLE_PERMISSIONS[OrganizationRole.SUPER_ADMIN]
        assert Permission.ADMIN_ALL in perms

    def test_billing_role_permissions(self):
        """Test billing role has correct permissions."""
        perms = ORGANIZATION_ROLE_PERMISSIONS[OrganizationRole.BILLING]

        assert Permission.ORG_READ in perms
        assert Permission.ORG_MANAGE_BILLING in perms
        assert Permission.ORG_VIEW_ANALYTICS in perms

        # Should not have
        assert Permission.ORG_DELETE not in perms
        assert Permission.TEAM_CREATE not in perms

    def test_team_member_permissions(self):
        """Test team member has correct permissions."""
        perms = TEAM_ROLE_PERMISSIONS[TeamRole.MEMBER]

        assert Permission.TEAM_READ in perms
        assert Permission.CHATBOT_CREATE in perms
        assert Permission.CHATBOT_UPDATE in perms

        # Should not have
        assert Permission.TEAM_DELETE not in perms
        assert Permission.CHATBOT_DELETE not in perms

    def test_project_contributor_permissions(self):
        """Test project contributor has correct permissions."""
        perms = PROJECT_ROLE_PERMISSIONS[ProjectRole.CONTRIBUTOR]

        assert Permission.PROJECT_READ in perms
        assert Permission.CHATBOT_READ in perms
        assert Permission.DOCUMENT_CREATE in perms

        # Should not have
        assert Permission.CHATBOT_DELETE not in perms
        assert Permission.PROJECT_DELETE not in perms


class TestGetRolePermissions:
    """Tests for get_role_permissions function."""

    def test_organization_scope(self):
        """Test getting organization role permissions."""
        perms = get_role_permissions(
            OrganizationRole.ADMIN,
            RoleScope.ORGANIZATION,
        )

        assert Permission.ORG_UPDATE in perms
        assert Permission.TEAM_CREATE in perms

    def test_team_scope(self):
        """Test getting team role permissions."""
        perms = get_role_permissions(
            TeamRole.LEAD,
            RoleScope.TEAM,
        )

        assert Permission.TEAM_UPDATE in perms
        assert Permission.PROJECT_CREATE in perms

    def test_project_scope(self):
        """Test getting project role permissions."""
        perms = get_role_permissions(
            ProjectRole.EDITOR,
            RoleScope.PROJECT,
        )

        assert Permission.PROJECT_UPDATE in perms
        assert Permission.CHATBOT_UPDATE in perms


class TestCheckPermission:
    """Tests for check_permission function."""

    def test_check_single_permission(self):
        """Test checking a single permission."""
        assert check_permission(
            Permission.ORG_READ,
            organization_role=OrganizationRole.VIEWER,
        )

        assert not check_permission(
            Permission.ORG_DELETE,
            organization_role=OrganizationRole.VIEWER,
        )

    def test_check_with_multiple_roles(self):
        """Test checking with multiple role levels."""
        # Team lead with org viewer role
        assert check_permission(
            Permission.TEAM_MANAGE_MEMBERS,
            organization_role=OrganizationRole.VIEWER,
            team_role=TeamRole.LEAD,
        )


class TestRoleHierarchy:
    """Tests for RoleHierarchy class."""

    def test_org_role_levels(self):
        """Test organization role hierarchy levels."""
        assert RoleHierarchy.get_role_level(OrganizationRole.VIEWER) == 0
        assert RoleHierarchy.get_role_level(OrganizationRole.BILLING) == 1
        assert RoleHierarchy.get_role_level(OrganizationRole.ADMIN) == 2
        assert RoleHierarchy.get_role_level(OrganizationRole.SUPER_ADMIN) == 3

    def test_team_role_levels(self):
        """Test team role hierarchy levels."""
        assert RoleHierarchy.get_role_level(TeamRole.VIEWER) == 0
        assert RoleHierarchy.get_role_level(TeamRole.MEMBER) == 1
        assert RoleHierarchy.get_role_level(TeamRole.LEAD) == 2

    def test_project_role_levels(self):
        """Test project role hierarchy levels."""
        assert RoleHierarchy.get_role_level(ProjectRole.VIEWER) == 0
        assert RoleHierarchy.get_role_level(ProjectRole.CONTRIBUTOR) == 1
        assert RoleHierarchy.get_role_level(ProjectRole.EDITOR) == 2
        assert RoleHierarchy.get_role_level(ProjectRole.OWNER) == 3

    def test_is_role_higher_or_equal(self):
        """Test role comparison."""
        assert RoleHierarchy.is_role_higher_or_equal(
            OrganizationRole.ADMIN,
            OrganizationRole.VIEWER,
        )
        assert RoleHierarchy.is_role_higher_or_equal(
            OrganizationRole.ADMIN,
            OrganizationRole.ADMIN,
        )
        assert not RoleHierarchy.is_role_higher_or_equal(
            OrganizationRole.VIEWER,
            OrganizationRole.ADMIN,
        )

    def test_is_role_higher_different_scopes(self):
        """Test role comparison fails for different scopes."""
        with pytest.raises(ValueError, match="different scopes"):
            RoleHierarchy.is_role_higher_or_equal(
                OrganizationRole.ADMIN,
                TeamRole.LEAD,
            )

    def test_get_roles_above(self):
        """Test getting roles above a given role."""
        above_viewer = RoleHierarchy.get_roles_above(OrganizationRole.VIEWER)

        assert OrganizationRole.BILLING in above_viewer
        assert OrganizationRole.ADMIN in above_viewer
        assert OrganizationRole.SUPER_ADMIN in above_viewer
        assert OrganizationRole.VIEWER not in above_viewer

    def test_get_roles_at_or_above(self):
        """Test getting roles at or above a given role."""
        at_or_above = RoleHierarchy.get_roles_at_or_above(TeamRole.MEMBER)

        assert TeamRole.MEMBER in at_or_above
        assert TeamRole.LEAD in at_or_above
        assert TeamRole.VIEWER not in at_or_above


class TestGetEffectivePermissions:
    """Tests for get_effective_permissions function."""

    def test_single_assignment(self):
        """Test permissions from single assignment."""
        assignments = [
            RoleAssignment(
                scope=RoleScope.ORGANIZATION,
                role=OrganizationRole.ADMIN,
                resource_id="org_123",
            )
        ]

        perms = get_effective_permissions(assignments)

        assert Permission.ORG_UPDATE in perms
        assert Permission.TEAM_CREATE in perms

    def test_multiple_assignments(self):
        """Test permissions accumulate from multiple assignments."""
        assignments = [
            RoleAssignment(
                scope=RoleScope.ORGANIZATION,
                role=OrganizationRole.VIEWER,
                resource_id="org_123",
            ),
            RoleAssignment(
                scope=RoleScope.TEAM,
                role=TeamRole.LEAD,
                resource_id="team_123",
            ),
        ]

        perms = get_effective_permissions(assignments)

        # From org viewer
        assert Permission.ORG_READ in perms
        # From team lead
        assert Permission.TEAM_UPDATE in perms
        assert Permission.PROJECT_CREATE in perms


class TestCanManageRole:
    """Tests for can_manage_role function."""

    def test_super_admin_can_manage_all(self):
        """Test super admin can manage all roles."""
        assert can_manage_role(OrganizationRole.SUPER_ADMIN, OrganizationRole.ADMIN)
        assert can_manage_role(OrganizationRole.SUPER_ADMIN, TeamRole.LEAD)
        assert can_manage_role(OrganizationRole.SUPER_ADMIN, ProjectRole.OWNER)

    def test_admin_can_manage_lower(self):
        """Test admin can manage lower org roles."""
        assert can_manage_role(OrganizationRole.ADMIN, OrganizationRole.VIEWER)
        assert can_manage_role(OrganizationRole.ADMIN, OrganizationRole.BILLING)
        assert can_manage_role(OrganizationRole.ADMIN, TeamRole.LEAD)

    def test_cannot_manage_same_level(self):
        """Test cannot manage same level role."""
        assert not can_manage_role(OrganizationRole.ADMIN, OrganizationRole.ADMIN)

    def test_cannot_manage_higher(self):
        """Test cannot manage higher level role."""
        assert not can_manage_role(OrganizationRole.VIEWER, OrganizationRole.ADMIN)
        assert not can_manage_role(TeamRole.MEMBER, TeamRole.LEAD)

    def test_team_lead_can_manage_project_roles(self):
        """Test team lead can manage project roles."""
        assert can_manage_role(TeamRole.LEAD, ProjectRole.OWNER)
        assert can_manage_role(TeamRole.LEAD, ProjectRole.EDITOR)


class TestGetManageableRoles:
    """Tests for get_manageable_roles function."""

    def test_admin_manageable_org_roles(self):
        """Test org admin can manage viewer and billing."""
        roles = get_manageable_roles(
            OrganizationRole.ADMIN,
            RoleScope.ORGANIZATION,
        )

        assert OrganizationRole.VIEWER in roles
        assert OrganizationRole.BILLING in roles
        assert OrganizationRole.ADMIN not in roles
        assert OrganizationRole.SUPER_ADMIN not in roles

    def test_admin_manageable_team_roles(self):
        """Test org admin can manage all team roles."""
        roles = get_manageable_roles(
            OrganizationRole.ADMIN,
            RoleScope.TEAM,
        )

        assert TeamRole.VIEWER in roles
        assert TeamRole.MEMBER in roles
        assert TeamRole.LEAD in roles

    def test_team_lead_manageable_project_roles(self):
        """Test team lead can manage all project roles."""
        roles = get_manageable_roles(
            TeamRole.LEAD,
            RoleScope.PROJECT,
        )

        assert ProjectRole.VIEWER in roles
        assert ProjectRole.CONTRIBUTOR in roles
        assert ProjectRole.EDITOR in roles
        assert ProjectRole.OWNER in roles
