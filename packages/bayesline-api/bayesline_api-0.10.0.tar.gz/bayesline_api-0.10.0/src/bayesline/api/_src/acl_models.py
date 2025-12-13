import datetime as dt
import enum
from collections.abc import Sequence

from pydantic import BaseModel, ConfigDict, Field


class PermissionLevel(str, enum.Enum):
    """Permission levels for resource access."""

    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"  # Full control including permission management


class ResourceType(str, enum.Enum):
    """Types of resources that can be protected by ACL."""

    SETTING = "setting"
    # Future resource types can be added here:
    # DATASET, MODEL, REPORT, etc.


class PrincipalType(str, enum.Enum):
    """Types of principals that can be granted permissions."""

    USER = "user"
    GROUP = "group"
    ROLE = "role"


class RoleType(str, enum.Enum):
    """Built-in system roles with predefined permissions."""

    ADMIN = "admin"  # Can access and modify all resources
    USER = "user"  # Standard user with no special privileges


# strip-hints: off


class ACLEntry(BaseModel):
    """An individual ACL entry granting specific permissions to a principal for a resource."""

    model_config = ConfigDict(frozen=True)

    id: int
    resource_type: ResourceType
    resource_id: int  # The ID of the specific resource (e.g., settings.id)
    principal_type: PrincipalType
    principal_id: str  # User ID, group name, or role name
    permission_level: PermissionLevel
    granted_by: str  # User ID of who granted this permission
    granted_at: dt.datetime
    expires_at: dt.datetime | None = None  # Optional expiration
    created_at: dt.datetime
    updated_at: dt.datetime


class CreateACLEntry(BaseModel):
    """Request model for creating a new ACL entry."""

    model_config = ConfigDict(frozen=True)

    resource_type: ResourceType
    resource_id: int
    principal_type: PrincipalType
    principal_id: str
    permission_level: PermissionLevel
    granted_by: str
    expires_at: dt.datetime | None = None


class UpdateACLEntry(BaseModel):
    """Request model for updating an existing ACL entry."""

    model_config = ConfigDict(frozen=True)

    id: int
    permission_level: PermissionLevel | None = None
    expires_at: dt.datetime | None = None
    updated_by: str


class UserGroup(BaseModel):
    """A group of users for simplified permission management."""

    model_config = ConfigDict(frozen=True)

    id: int
    name: str = Field(pattern=r"^[A-Za-z0-9_-]+$")
    description: str
    created_by: str
    created_at: dt.datetime
    updated_at: dt.datetime


class CreateUserGroup(BaseModel):
    """Request model for creating a new user group."""

    model_config = ConfigDict(frozen=True)

    name: str = Field(pattern=r"^[A-Za-z0-9_-]+$")
    description: str
    created_by: str


class UpdateUserGroup(BaseModel):
    """Request model for updating an existing user group."""

    model_config = ConfigDict(frozen=True)

    id: int
    description: str | None = None
    updated_by: str


class GroupMembership(BaseModel):
    """Represents a user's membership in a group."""

    model_config = ConfigDict(frozen=True)

    id: int
    group_id: int
    user_id: str
    added_by: str
    added_at: dt.datetime


class CreateGroupMembership(BaseModel):
    """Request model for adding a user to a group."""

    model_config = ConfigDict(frozen=True)

    group_id: int
    user_id: str
    added_by: str


class UserRole(BaseModel):
    """Represents a user's system role assignment."""

    model_config = ConfigDict(frozen=True)

    id: int
    user_id: str
    role_type: RoleType
    assigned_by: str
    assigned_at: dt.datetime
    expires_at: dt.datetime | None = None


class CreateUserRole(BaseModel):
    """Request model for assigning a role to a user."""

    model_config = ConfigDict(frozen=True)

    user_id: str
    role_type: RoleType
    assigned_by: str
    expires_at: dt.datetime | None = None


class ResourcePermissionSummary(BaseModel):
    """Summary of a user's permissions for a specific resource."""

    model_config = ConfigDict(frozen=True)

    resource_type: ResourceType
    resource_id: int
    resource_name: str | None = None  # Human-readable name if available
    resource_owner: str | None = None  # Owner of the resource
    effective_permission: PermissionLevel
    permission_sources: Sequence[str]  # How permission was granted


class UserPermissionsSummary(BaseModel):
    """Complete summary of a user's permissions across all resources."""

    model_config = ConfigDict(frozen=True)

    user_id: str
    roles: Sequence[RoleType]
    groups: Sequence[str]  # Group names
    resources: Sequence[ResourcePermissionSummary]


# strip-hints: on


class ACLError(Exception):
    """Base exception for ACL-related errors."""

    pass


class PermissionDeniedError(ACLError):
    """Raised when a user attempts an action they don't have permission for."""

    pass


class ResourceNotFoundError(ACLError):
    """Raised when a resource referenced in ACL operations doesn't exist."""

    pass


class PrincipalNotFoundError(ACLError):
    """Raised when a principal (user/group/role) referenced in ACL operations doesn't exist."""

    pass


class ACLValidationError(ACLError):
    """Raised when ACL data fails validation."""

    pass


class PermissionGrantError(ACLError):
    """Raised when granting a permission fails."""

    pass


class GroupCreationError(ACLError):
    """Raised when creating a group fails."""

    pass


class GroupUpdateError(ACLError):
    """Raised when updating a group fails."""

    pass


class GroupDeletionError(ACLError):
    """Raised when deleting a group fails."""

    pass


class GroupMembershipError(ACLError):
    """Raised when adding or removing users from groups fails."""

    pass


class RoleAssignmentError(ACLError):
    """Raised when assigning or revoking roles fails."""

    pass
