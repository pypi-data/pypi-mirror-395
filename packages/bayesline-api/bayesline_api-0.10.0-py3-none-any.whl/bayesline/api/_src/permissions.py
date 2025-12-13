import abc
from collections.abc import Sequence

from bayesline.api._src._utils import docstrings_from_sync
from bayesline.api._src.acl_models import (
    GroupMembership,
    PermissionLevel,
    PrincipalType,
    ResourceType,
    RoleType,
    UserGroup,
    UserPermissionsSummary,
    UserRole,
)


class PermissionsApi:
    """Abstract base class for synchronous ACL-based permissionining API operations."""

    # ===== Permission Queries =====

    @abc.abstractmethod
    def get_user_permissions(
        self,
        resource_type: ResourceType | None = None,
        resource_ids: Sequence[int] | None = None,
    ) -> UserPermissionsSummary:
        """
        Get the current user's permissions for resources.

        Parameters
        ----------
        resource_type : ResourceType | None, default=None
            Specific resource type to check. If None, returns permissions for all
            accessible resources.
        resource_ids : Sequence[int] | None, default=None
            Specific resource IDs to check. If None, returns permissions for all
            accessible resources.

        Returns
        -------
        UserPermissionsSummary
            Summary of the user's permissions.
        """

    @abc.abstractmethod
    def check_permission(
        self,
        resource_id: int,
        required_permission: PermissionLevel,
    ) -> bool:
        """
        Check if the current user has the required permission for a resource.

        Parameters
        ----------
        resource_id : int
            The ID of the resource to check.
        required_permission : PermissionLevel
            The required permission level.

        Returns
        -------
        bool
            True if the user has the required permission, False otherwise.
        """

    @abc.abstractmethod
    def get_accessible_resources(
        self,
        resource_type: ResourceType,
        required_permission: PermissionLevel,
    ) -> Sequence[int]:
        """
        Get all resources the current user can access with the required permission.

        Parameters
        ----------
        resource_type : ResourceType
            The type of resources to check.
        required_permission : PermissionLevel
            The minimum permission level required.

        Returns
        -------
        Sequence[int]
            List of resource IDs the user can access.
        """

    # ===== Permission Updates =====

    @abc.abstractmethod
    def grant_permission(
        self,
        resource_id: int,
        principal_type: PrincipalType,
        principal_id: str,
        permission_level: PermissionLevel,
    ) -> None:
        """
        Grant permission to a principal for a resource.

        The current user must have ADMIN permission on the resource.

        Parameters
        ----------
        resource_id : int
            The ID of the resource.
        principal_type : PrincipalType
            The type of principal (user, group, role).
        principal_id : str
            The ID of the principal.
        permission_level : PermissionLevel
            The permission level to grant.

        Raises
        ------
        PermissionDeniedError
            If the current user doesn't have ADMIN permission on the resource.
        """

    @abc.abstractmethod
    def revoke_permission(
        self,
        resource_id: int,
        principal_type: PrincipalType,
        principal_id: str,
    ) -> None:
        """
        Revoke permission from a principal for a resource.

        The current user must have ADMIN permission on the resource.

        Parameters
        ----------
        resource_id : int
            The ID of the resource.
        principal_type : PrincipalType
            The type of principal (user, group, role).
        principal_id : str
            The ID of the principal.

        Raises
        ------
        PermissionDeniedError
            If the current user doesn't have ADMIN permission on the resource.
        """

    @abc.abstractmethod
    def update_permission(
        self,
        resource_id: int,
        principal_type: PrincipalType,
        principal_id: str,
        permission_level: PermissionLevel,
    ) -> None:
        """
        Update permission level for a principal on a resource.

        The current user must have ADMIN permission on the resource.

        Parameters
        ----------
        resource_id : int
            The ID of the resource.
        principal_type : PrincipalType
            The type of principal (user, group, role).
        principal_id : str
            The ID of the principal.
        permission_level : PermissionLevel
            The new permission level.

        Raises
        ------
        PermissionDeniedError
            If the current user doesn't have ADMIN permission on the resource.
        """

    # ===== Group Management =====

    @abc.abstractmethod
    def create_group(
        self,
        name: str,
        description: str,
    ) -> int:
        """
        Create a new user group.

        Parameters
        ----------
        name : str
            The name of the group.
        description : str
            A description of the group.

        Returns
        -------
        int
            The ID of the created group.
        """

    @abc.abstractmethod
    def update_group(
        self,
        group_id: int,
        description: str,
    ) -> None:
        """
        Update a group's description.

        The current user must be the creator of the group or have admin role.

        Parameters
        ----------
        group_id : int
            The ID of the group.
        description : str
            The new description.

        Raises
        ------
        PermissionDeniedError
            If the current user doesn't have permission to update the group.
        """

    @abc.abstractmethod
    def delete_group(
        self,
        group_id: int,
    ) -> None:
        """
        Delete a user group.

        The current user must be the creator of the group or have admin role.

        Parameters
        ----------
        group_id : int
            The ID of the group to delete.

        Raises
        ------
        PermissionDeniedError
            If the current user doesn't have permission to delete the group.
        """

    @abc.abstractmethod
    def add_user_to_group(
        self,
        group_id: int,
        user_id: str,
    ) -> None:
        """
        Add a user to a group.

        The current user must be the creator of the group or have admin role.

        Parameters
        ----------
        group_id : int
            The ID of the group.
        user_id : str
            The ID of the user to add.

        Raises
        ------
        PermissionDeniedError
            If the current user doesn't have permission to manage the group.
        """

    @abc.abstractmethod
    def remove_user_from_group(
        self,
        group_id: int,
        user_id: str,
    ) -> None:
        """
        Remove a user from a group.

        The current user must be the creator of the group or have admin role.

        Parameters
        ----------
        group_id : int
            The ID of the group.
        user_id : str
            The ID of the user to remove.

        Raises
        ------
        PermissionDeniedError
            If the current user doesn't have permission to manage the group.
        """

    @abc.abstractmethod
    def list_groups(self) -> Sequence[UserGroup]:
        """
        List all groups the current user can see.

        Returns
        -------
        Sequence[UserGroup]
            List of groups the user can see (created by them or they're members of).
        """

    @abc.abstractmethod
    def list_group_members(
        self,
        group_id: int,
    ) -> Sequence[GroupMembership]:
        """
        List members of a group.

        The current user must be a member of the group, the creator, or have admin role.

        Parameters
        ----------
        group_id : int
            The ID of the group.

        Returns
        -------
        Sequence[GroupMembership]
            List of group memberships.

        Raises
        ------
        PermissionDeniedError
            If the current user doesn't have permission to view group members.
        """

    # ===== Role Management =====

    @abc.abstractmethod
    def assign_role(
        self,
        user_id: str,
        role_type: RoleType,
    ) -> None:
        """
        Assign a role to a user.

        Only users with ADMIN role can assign roles.

        Parameters
        ----------
        user_id : str
            The ID of the user.
        role_type : RoleType
            The role to assign.

        Raises
        ------
        PermissionDeniedError
            If the current user doesn't have ADMIN role.
        """

    @abc.abstractmethod
    def revoke_role(
        self,
        user_id: str,
        role_type: RoleType,
    ) -> None:
        """
        Revoke a role from a user.

        Only users with ADMIN role can revoke roles.

        Parameters
        ----------
        user_id : str
            The ID of the user.
        role_type : RoleType
            The role to revoke.

        Raises
        ------
        PermissionDeniedError
            If the current user doesn't have ADMIN role.
        """

    @abc.abstractmethod
    def list_user_roles(
        self,
        user_id: str | None = None,
    ) -> Sequence[UserRole]:
        """
        List roles assigned to a user.

        Parameters
        ----------
        user_id : str | None, default=None
            The ID of the user. If None, lists roles for the current user.

        Returns
        -------
        Sequence[UserRole]
            List of user role assignments.

        Raises
        ------
        PermissionDeniedError
            If trying to view another user's roles without ADMIN permission.
        """


@docstrings_from_sync
class AsyncPermissionsApi:
    """
    Abstract base class for asynchronous ACL-based permissionining API operations.
    """

    @abc.abstractmethod
    async def get_user_permissions(  # noqa: D102
        self,
        resource_type: ResourceType | None = None,
        resource_ids: Sequence[int] | None = None,
    ) -> UserPermissionsSummary: ...

    @abc.abstractmethod
    async def check_permission(  # noqa: D102
        self,
        resource_id: int,
        required_permission: PermissionLevel,
    ) -> bool: ...

    @abc.abstractmethod
    async def get_accessible_resources(  # noqa: D102
        self,
        resource_type: ResourceType,
        required_permission: PermissionLevel,
    ) -> Sequence[int]: ...

    @abc.abstractmethod
    async def grant_permission(  # noqa: D102
        self,
        resource_id: int,
        principal_type: PrincipalType,
        principal_id: str,
        permission_level: PermissionLevel,
    ) -> None: ...

    @abc.abstractmethod
    async def revoke_permission(  # noqa: D102
        self,
        resource_id: int,
        principal_type: PrincipalType,
        principal_id: str,
    ) -> None: ...

    @abc.abstractmethod
    async def update_permission(  # noqa: D102
        self,
        resource_id: int,
        principal_type: PrincipalType,
        principal_id: str,
        permission_level: PermissionLevel,
    ) -> None: ...

    @abc.abstractmethod
    async def create_group(  # noqa: D102
        self,
        name: str,
        description: str,
    ) -> int: ...

    @abc.abstractmethod
    async def update_group(  # noqa: D102
        self,
        group_id: int,
        description: str,
    ) -> None: ...

    @abc.abstractmethod
    async def delete_group(  # noqa: D102
        self,
        group_id: int,
    ) -> None: ...

    @abc.abstractmethod
    async def add_user_to_group(  # noqa: D102
        self,
        group_id: int,
        user_id: str,
    ) -> None: ...

    @abc.abstractmethod
    async def remove_user_from_group(  # noqa: D102
        self,
        group_id: int,
        user_id: str,
    ) -> None: ...

    @abc.abstractmethod
    async def list_groups(self) -> Sequence[UserGroup]: ...  # noqa: D102

    @abc.abstractmethod
    async def list_group_members(  # noqa: D102
        self,
        group_id: int,
    ) -> Sequence[GroupMembership]: ...

    @abc.abstractmethod
    async def assign_role(  # noqa: D102
        self,
        user_id: str,
        role_type: RoleType,
    ) -> None: ...

    @abc.abstractmethod
    async def revoke_role(  # noqa: D102
        self,
        user_id: str,
        role_type: RoleType,
    ) -> None: ...

    @abc.abstractmethod
    async def list_user_roles(  # noqa: D102
        self,
        user_id: str | None = None,
    ) -> Sequence[UserRole]: ...
