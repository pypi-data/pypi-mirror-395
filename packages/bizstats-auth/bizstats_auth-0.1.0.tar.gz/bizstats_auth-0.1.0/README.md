# @bizstats/auth

Enterprise authentication with JWT, RBAC, and multi-tenant support for BizStats applications.

## Features

- **JWT Token Management**: Access and refresh tokens with configurable expiration
- **Password Security**: Bcrypt hashing with strength validation
- **RBAC System**: 3-tier role hierarchy (Organization → Team → Project)
- **API Key Management**: Secure API key generation and validation
- **Multi-tenant Support**: Organization-scoped authentication

## Installation

```bash
pip install bizstats-auth
```

## Quick Start

### Password Hashing

```python
from bizstats_auth import hash_password, verify_password, check_password_strength

# Hash a password
hashed = hash_password("SecureP@ss123!")

# Verify a password
is_valid = verify_password("SecureP@ss123!", hashed)

# Check password strength
result = check_password_strength("MyP@ssw0rd!")
print(f"Strength: {result.strength}, Valid: {result.is_valid}")
```

### JWT Tokens

```python
from bizstats_auth import create_access_token, verify_token, TokenType

# Create an access token
token = create_access_token(
    subject="user_123",
    scope=["read", "write"],
    organization_id="org_456",
)

# Verify the token
payload = verify_token(token, TokenType.ACCESS)
print(f"User ID: {payload.sub}")
```

### RBAC Permissions

```python
from bizstats_auth import (
    Permission,
    PermissionChecker,
    OrganizationRole,
    TeamRole,
)

# Check permissions for a user
checker = PermissionChecker(
    organization_role=OrganizationRole.ADMIN,
    team_role=TeamRole.LEAD,
)

if checker.has_permission(Permission.PROJECT_CREATE):
    print("User can create projects")
```

### API Keys

```python
from bizstats_auth import APIKeyManager, APIKeyCreate

manager = APIKeyManager()

# Generate a new API key
create_data = APIKeyCreate(
    name="Production API Key",
    scopes=["read", "write"],
    organization_id="org_123",
)

full_key, api_key = manager.create_api_key(create_data, user_id="user_456")
print(f"API Key: {full_key}")  # Show only once!
```

## Configuration

Configure via environment variables (prefix `AUTH_`) or programmatically:

```python
from bizstats_auth import AuthConfig, configure

config = AuthConfig(
    jwt_secret_key="your-secret-key",
    access_token_expire_minutes=30,
    password_min_length=10,
)
configure(config)
```

### Available Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `jwt_secret_key` | - | Secret key for JWT signing (required in production) |
| `jwt_algorithm` | HS256 | JWT signing algorithm |
| `access_token_expire_minutes` | 30 | Access token expiration |
| `refresh_token_expire_days` | 7 | Refresh token expiration |
| `password_min_length` | 8 | Minimum password length |
| `password_require_uppercase` | True | Require uppercase letters |
| `password_require_lowercase` | True | Require lowercase letters |
| `password_require_digit` | True | Require digits |
| `password_require_special` | True | Require special characters |
| `api_key_prefix` | biz_ | Prefix for generated API keys |
| `max_login_attempts` | 5 | Max failed login attempts |
| `lockout_duration_minutes` | 15 | Account lockout duration |

## RBAC Role Hierarchy

### Organization Roles
- `super_admin` - Full system access
- `admin` - Organization management
- `billing` - Billing and subscription access
- `viewer` - Read-only access

### Team Roles
- `lead` - Team management and project creation
- `member` - Standard team member
- `viewer` - Read-only team access

### Project Roles
- `owner` - Full project control
- `editor` - Edit project content
- `contributor` - Limited editing
- `viewer` - Read-only project access

## License

Proprietary - Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
