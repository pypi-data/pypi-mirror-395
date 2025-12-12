"""
RBAC (Role-Based Access Control) module.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

from bizstats_auth.rbac.permissions import (
    Permission,
    PermissionChecker,
    RolePermissions,
    check_permission,
    get_role_permissions,
)
from bizstats_auth.rbac.roles import (
    RoleHierarchy,
    get_effective_permissions,
    can_manage_role,
)

__all__ = [
    # Permissions
    "Permission",
    "PermissionChecker",
    "RolePermissions",
    "check_permission",
    "get_role_permissions",
    # Roles
    "RoleHierarchy",
    "get_effective_permissions",
    "can_manage_role",
]
