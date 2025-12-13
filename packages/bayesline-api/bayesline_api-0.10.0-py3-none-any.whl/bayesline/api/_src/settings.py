import abc
import datetime as dt
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any, Generic, Literal, TypeVar, cast

from pydantic import BaseModel, Field, field_serializer, field_validator

from bayesline.api._src._utils import docstrings_from_sync
from bayesline.api._src.registry import Settings
from bayesline.api._src.settings_types import SETTINGS_TYPES

_SETTINGS_TYPES_INDEX = {t.__name__: t for t in SETTINGS_TYPES}

T = TypeVar("T", bound=Settings)


class CouldNotSaveSettingsError(Exception):
    """Raised when a settings object could not be saved to the registry."""


class CouldNotDeleteSettingsError(Exception):
    """Raised when a settings object could not be deleted from the registry."""


class CouldNotPermissionSettingsError(Exception):
    """Raised when a settings object could not be permissioned."""


class SettingsRegistryError(Exception):
    """Raised when an unexpected error occurs in the settings registry."""


@dataclass(frozen=True)
class SettingNotFound:
    """A settings result that could not be found."""

    name: str | None
    id: int | None
    kind: Literal["not_found"] = "not_found"


@dataclass(frozen=True)
class SettingInvalid:
    """
    A settings result that exists but is invalid.

    Possible reasons for invalidity:
    - the underlying json is invalid
    - the setting has references to settings that do not exist
    - the setting has references to settings that are invalid
    - the setting does not validate against the settings menu
    """

    name: str
    id: int
    owner: str
    raw_json: Mapping[str, Any]
    issues: Sequence[str]
    missing_refs: Sequence[str | int] = ()
    kind: Literal["invalid"] = "invalid"


@dataclass(frozen=True)
class SettingNotPermissioned:
    """A settings result that exists but the current user does not have read permissions."""

    name: str
    id: int
    owner: str
    kind: Literal["forbidden"] = "forbidden"


@dataclass(frozen=True)
class SettingValid(Generic[T]):
    """A settings result that exists and is valid."""

    name: str
    id: int
    owner: str
    value: T
    created_on: dt.datetime
    last_updated_on: dt.datetime
    kind: Literal["valid"] = "valid"


SettingResult = (
    SettingValid[T] | SettingInvalid | SettingNotFound | SettingNotPermissioned
)


class ItemStatus(str, Enum):
    """The status of a single item operation, e.g. delete on a single settings object."""

    # order is important for error message construction
    not_found = "not_found"
    invalid_type = "invalid_type"
    forbidden = "forbidden"
    user_not_found = "user_not_found"
    group_not_found = "group_not_found"
    invalid = "invalid"
    conflict = "conflict"
    success = "success"


class ItemResult(BaseModel, extra="forbid", frozen=True):
    """The result of a single item operation, e.g. delete on a single settings object."""

    name_or_id: str | int = Field(
        description=(
            "The name or identifier of the item as it was provided to the operation."
        ),
    )
    status: ItemStatus = Field(description=("The status of the item operation."))
    message: str = Field(
        description="The human readable message of the item's operation result.",
        default="",
    )
    name: str | None = Field(
        description=(
            "The name of the item if available. Will always be available if the "
            "operation was successful."
        )
    )
    id: int | None = Field(
        description=(
            "The identifier of the item if available. Will always be available if the "
            "operation was successful."
        )
    )
    short_message: str = Field(
        description=(
            "A short message of the item's operation result which can be used for "
            "summary messages. E.g. if a user could not be found, the short message "
            "should be the input of the user that could not be found."
        ),
        default="",
    )

    @property
    def success(self) -> bool:
        """Whether the item operation was successful."""
        return self.status == ItemStatus.success


class SaveItemResult(ItemResult):
    """The result of a single save operation."""

    # nothing yet
    pass


class DeleteItemResult(ItemResult):
    """The result of a single delete operation."""

    # nothing yet
    pass


class PermissionItemResult(ItemResult):
    """The result of a single permission operation."""

    # nothing yet
    pass


E = TypeVar("E", bound=ItemResult)


class SettingsRegistryResult(BaseModel, Generic[E], extra="forbid", frozen=True):
    """The result of a batch operation, e.g. a batch delete operation."""

    operation: str = Field(
        description=(
            "The operation that was performed, e.g. 'delete', 'permission', etc."
        ),
    )
    items: list[E] = Field(
        description=(
            "Results of the operations for each settings object in the order they "
            "were provided."
        ),
    )

    @property
    def success(self) -> bool:
        """Whether the entire batch operation was successful."""
        return all(item.success for item in self.items)

    @property
    def name_to_id(self) -> Mapping[str, int]:
        """Mapping of names to identifiers."""
        return {
            item.name: item.id
            for item in self.items
            if item.name is not None and item.id is not None
        }

    @property
    def id_to_name(self) -> Mapping[int, str]:
        """Mapping of identifiers to names."""
        return {
            item.id: item.name
            for item in self.items
            if item.name is not None and item.id is not None
        }

    @property
    def error_message(self) -> str:
        """
        Produces a full error message of the batch operation.

        Will return an empty string if the operation was successful.

        Returns
        -------
        str
            The full error message of the batch operation if the operation was not
            successful or an empty string if the operation was successful.
        """
        if not self.success:
            # collect grouped errors
            grouped_errors: defaultdict[ItemStatus, list[int]] = defaultdict(list)
            for i, item in enumerate(self.items):
                if not item.success:
                    grouped_errors[item.status].append(i)
            msg = f"Could not {self.operation} the following settings: "
            for status, indices in grouped_errors.items():
                messages = [
                    (
                        f"{self.items[i].name_or_id} ({self.items[i].short_message})"
                        if self.items[i].short_message
                        else str(self.items[i].name_or_id)
                    )
                    for i in indices
                ]
                msg += f"\n{status.value}: {', '.join(messages)}"
            return msg
        return ""

    def __getitem__(self, index: int) -> E:  # noqa: D105
        return self.items[index]

    def __len__(self) -> int:  # noqa: D105
        return len(self.items)


class SaveResult(SettingsRegistryResult[SaveItemResult]):
    """The result of a batch save operation."""

    # nothing yet
    pass


class DeleteResult(SettingsRegistryResult[DeleteItemResult]):
    """The result of a batch delete operation."""

    # nothing yet
    pass


class PermissionResult(SettingsRegistryResult[PermissionItemResult]):
    """The result of a batch permission operation."""

    # nothing yet
    pass


class SettingsTransferObject(BaseModel):
    """A settings transfer object."""

    kind: str
    name: str | None
    identifier: int | None
    value: dict[str, Any] = {}
    settings_type: str | None = None
    owner: str | None = None
    issues: Sequence[str] = []
    missing_refs: Sequence[str | int] = []
    created_on: dt.datetime | None = None
    last_updated_on: dt.datetime | None = None

    def to_settings(self, settings_types: list[type[Settings]]) -> SettingResult:
        """
        Convert the settings transfer object to a settings object.

        Parameters
        ----------
        settings_types : list[type[Settings]]
            The available types to use to convert the settings transfer object to.

        Raises
        ------
        ValueError
            If the settings type is not found.
        AssertionError
            If the settings transfer object is not of a known kind.

        Returns
        -------
        SettingResult
            The settings object.

        """
        if self.kind == "not_found":
            return SettingNotFound(name=self.name, id=self.identifier)
        elif self.kind == "invalid":
            return SettingInvalid(
                name=cast(str, self.name),
                id=cast(int, self.identifier),
                owner=cast(str, self.owner),
                raw_json=self.value,
                issues=self.issues,
                missing_refs=self.missing_refs,
            )
        elif self.kind == "forbidden":
            return SettingNotPermissioned(
                name=cast(str, self.name),
                id=cast(int, self.identifier),
                owner=cast(str, self.owner),
            )
        elif self.kind == "valid":
            for t in settings_types:
                if t.__name__ == self.settings_type:
                    break
            else:
                raise ValueError(f"Settings type {self.settings_type} not found")

            return SettingValid(
                name=cast(str, self.name),
                id=cast(int, self.identifier),
                owner=cast(str, self.owner),
                value=t.model_validate(self.value),
                created_on=cast(dt.datetime, self.created_on),
                last_updated_on=cast(dt.datetime, self.last_updated_on),
            )
        else:
            raise AssertionError(f"unknown kind {self.kind}")

    @classmethod
    def from_settings(cls, s: SettingResult) -> "SettingsTransferObject":
        """
        Convert the settings object to a settings transfer object.

        Parameters
        ----------
        s : SettingResult
            The settings object to convert.

        Raises
        ------
        AssertionError
            If the settings object is not of a known kind.

        Returns
        -------
        SettingsTransferObject
            The settings transfer object.
        """
        if s.kind == "not_found":
            return SettingsTransferObject(
                kind=s.kind,
                name=s.name,
                identifier=s.id,
            )
        elif s.kind == "invalid":
            return SettingsTransferObject(
                kind=s.kind,
                name=s.name,
                identifier=s.id,
                owner=s.owner,
                value=s.raw_json,
                issues=s.issues,
                missing_refs=s.missing_refs,
            )
        elif s.kind == "forbidden":
            return SettingsTransferObject(
                kind=s.kind,
                name=s.name,
                identifier=s.id,
                owner=s.owner,
            )
        elif s.kind == "valid":
            return SettingsTransferObject(
                kind=s.kind,
                name=s.name,
                identifier=s.id,
                settings_type=s.value.__class__.__name__,
                owner=s.owner,
                value=s.value.model_dump(),
                created_on=s.created_on,
                last_updated_on=s.last_updated_on,
            )
        else:
            raise AssertionError(f"unknown kind {s.kind}")


class SettingsIdentifiers(BaseModel):
    """Holds mappings of globally unique settings identifiers to other properties."""

    id_to_name: Mapping[int, str] = Field(
        description="Mapping of globally unique identifiers to their names.",
    )
    name_to_id: Mapping[str, int] = Field(
        description="Mapping of names to their globally unique identifiers.",
    )
    id_to_type: Mapping[int, type[Settings]] = Field(
        description="Mapping of globally unique identifiers to the settings type.",
    )
    id_to_user_email: Mapping[int, str] = Field(
        description=(
            "Mapping of globally unique identifiers to the user emails who own them."
        ),
    )

    def __getitem__(self, settings_type: type[Settings]) -> "SettingsIdentifiers":
        """
        Get the identifiers for a specific settings type.

        Parameters
        ----------
        settings_type : type[Settings]
            The settings type to get the identifiers for.

        Raises
        ------
        KeyError
            If the settings type is not covered in this registry.

        Returns
        -------
        SettingsIdentifiers
            The identifiers for the given settings type.
        """
        if not any(t.__name__ == settings_type.__name__ for t in SETTINGS_TYPES):
            raise KeyError(f"Settings type {settings_type.__name__} not found")
        ids_for_type = {k for k, v in self.id_to_type.items() if v == settings_type}
        return SettingsIdentifiers(
            id_to_name={k: v for k, v in self.id_to_name.items() if k in ids_for_type},
            name_to_id={k: v for k, v in self.name_to_id.items() if v in ids_for_type},
            id_to_type={k: v for k, v in self.id_to_type.items() if k in ids_for_type},
            id_to_user_email={
                k: v for k, v in self.id_to_user_email.items() if k in ids_for_type
            },
        )

    @field_validator("id_to_type", mode="before")
    @classmethod
    def parse_type(cls, v: Any) -> dict[int, type[Settings]]:
        if isinstance(v, dict):
            return {
                int(id): (
                    _SETTINGS_TYPES_INDEX[type_] if isinstance(type_, str) else type_
                )
                for id, type_ in v.items()
            }
        raise TypeError("id_to_type must be a dict of int to settings types")

    @field_serializer("id_to_type")
    def serialize_type(self, v: dict[int, type[Settings]]) -> dict[int, str]:
        return {id: type_.__name__ for id, type_ in v.items()}


class TypedSettingsRegistry(abc.ABC, Generic[T]):
    """
    Abstract base class for typed settings registries.

    A typed settings registry covers exactly one settings type, e.g. `UniverseSettings`.
    """

    @property
    @abc.abstractmethod
    def settings_type(self) -> type[T]:
        """
        Get the settings type covered by this registry.

        Returns
        -------
        type[T]
            The settings type covered by this registry.
        """

    @abc.abstractmethod
    def get_identifiers(
        self, which: Literal["all", "mine"] = "all"
    ) -> SettingsIdentifiers:
        """
        Get all identifiers for the settings type covered by this registry.

        Parameters
        ----------
        which : Literal["all", "mine"], default="all"
            'mine' will only return those identfiers owned by the current user
            'all' will also return those identifiers that the current user is
            permissioned to READ.

        Returns
        -------
        SettingsIdentifiers
            All identifiers for the settings type covered by this registry.
        """

    @abc.abstractmethod
    def save(
        self,
        name_or_id: str | int,
        settings: T,
        *,
        overwrite: bool = False,
        raise_on_errors: bool = True,
    ) -> SaveItemResult:
        """
        Save (or update) a settings object to the registry.

        Parameters
        ----------
        name_or_id : str | int
            The name of the settings object to save or the global int id of the settings
            object to update.
            If int id is used, the settings objects must exist in the registry, which
            implies that overwrite must be True.
            The name is a user defined name for the settings object that must
            consist of only alphanumeric characters, underscores and hyphens and start
            with a letter.
            Other users' settings can be written/updated (if permissioned) by using
            either the global int identifier or prefixing the name with the user name,
            e.g. "sebastian.janisch@bayesline.com/SebastiansSettings".
        settings : T
            The settings object to save.
        overwrite : bool, default=False
            If True, overwrite the settings object if it already exists.
            If False, mark an error if the settings object already exists.
        raise_on_errors : bool, default=True
            If True, raise an exception if the settings object could not be saved.
            If False, return a SaveItemResult object with the errors.

        Raises
        ------
        CouldNotSaveSettingsError
            If an error captured by the item result is encountered and raise_on_errors
            is True
        SettingsRegistryError
            If an unexpected error occurs while saving the settings object.

        Returns
        -------
        SaveItemResult
            Result object for the save operation.
        """

    @abc.abstractmethod
    def save_many(
        self,
        settings: Mapping[str | int, T],
        *,
        overwrite: bool = False,
        raise_on_errors: bool = True,
    ) -> SaveResult:
        """
        Save multiple settings objects to the registry.

        This method is best effort. Partial execution is possible if some settings
        objects can be saved and others cannot.

        Parameters
        ----------
        settings : Mapping[str | int, T]
            The settings objects to save, keys being the names or global int ids of the
            settings objects.
            If int ids are used, the settings objects must exist in the registry, which
            implies that overwrite must be True.
            The name is a user defined name for the settings object that must
            consist of only alphanumeric characters, underscores and hyphens and start
            with a letter.
            Other users' settings can be written/updated (if permissioned) by using
            either the global int identifier or prefixing the name with the user name,
            e.g. "sebastian.janisch@bayesline.com/SebastiansSettings".
        overwrite : bool, default=False
            If True, overwrite the settings objects if they already exist.
            If False, mark an error for settings objects that already exist.
        raise_on_errors : bool, default=True
            If True, raise an exception if any of the settings objects could not be saved.
            If False, return a SaveResult object with the errors.

        Raises
        ------
        CouldNotSaveSettingsError
            If an error captured by the item result is encountered and raise_on_errors
            is True
        SettingsRegistryError
            If an unexpected error occurs while saving the settings objects.

        Returns
        -------
        SaveResult
            Result object for the save operation.
        """

    @abc.abstractmethod
    def read(self, name_or_id: str | int) -> SettingResult[T]:
        """
        Read a settings object from the registry for the given name or identifier.

        The setting must be of the correct type for this registry.

        Parameters
        ----------
        name_or_id : str | int
            The name or identifier of the settings object to read.
            The identifier is a globally unique integer that is assinged when
            a setting gets first saved to the registry.
            The name is a user defined name for the settings object that must
            consist of only alphanumeric characters, underscores and hyphens and start
            with a letter.
            Other users' settings can be read (if permissioned) by using either
            the global int identifier or prefixing the name with the user name and
            a forward slash, e.g. "sebastian.janisch@bayesline.com/SebastiansSettings".

        Returns
        -------
        SettingResult[T]
            The settings object.
        """

    @abc.abstractmethod
    def read_many(
        self, names_or_ids: Sequence[str | int]
    ) -> Sequence[SettingResult[T]]:
        """
        Read settings objects from the registry for the given names or identifiers.

        The settings must be of the correct type for this registry.

        Parameters
        ----------
        names_or_ids: Sequence[str | int]
            The names or identifiers of the settings objects to read.
            The identifiers are globally unique integers that is assinged when
            a setting gets first saved to the registry.
            The names are user defined names for the settings objects that must
            consist of only alphanumeric characters, underscores and hyphens and start
            with a letter.
            Other users' settings can be read (if permissioned) by using either
            the global int identifier or prefixing the name with the user name and
            a forward slash, e.g. "sebastian.janisch@bayesline.com/SebastiansSettings".

        Returns
        -------
        Sequence[SettingResult[T]]
            The settings objects in exact same order as the input.
        """

    @abc.abstractmethod
    def delete(
        self, name_or_id: str | int, *, raise_on_errors: bool = True
    ) -> DeleteItemResult:
        """
        Delete a settings object from the registry for the given name or identifier.

        The setting must be of the correct type for this registry.

        For a setting to be able to be deleted, it must exist, not be referenced by
        any other settings and the user must have delete permissions for the setting.

        Parameters
        ----------
        name_or_id : str | int
            The name or identifier of the settings object to delete.
            The identifiers are globally unique integers that is assinged when
            a setting gets first saved to the registry.
            The names are user defined names for the settings objects that must
            consist of only alphanumeric characters, underscores and hyphens and start
            with a letter.
            Other users' settings can be deleted (if permissioned) by using either
            the global int identifier or prefixing the name with the user name and
            a forward slash, e.g. "sebastian.janisch@bayesline.com/SebastiansSettings".
        raise_on_errors : bool, default=True
            If True, raise an exception if the settings object could not be deleted.
            If False, return a DeleteItemResult object with the errors.

        Raises
        ------
        CouldNotDeleteSettingsError
            If an error captured by the item result is encountered and raise_on_errors
            is True
        SettingsRegistryError
            If an unexpected error occurs while deleting the settings object.

        Returns
        -------
        DeleteItemResult
            Result object for the delete operation.
        """

    @abc.abstractmethod
    def delete_many(
        self, names_or_ids: Sequence[str | int], *, raise_on_errors: bool = True
    ) -> DeleteResult:
        """
        Delete settings objects from the registry for the given names or identifiers.

        This method is best effort. Partial deletions are possible if some settings
        objects can be deleted and others cannot.

        The settings must be of the correct type for this registry.

        For a setting to be able to be deleted, it must exist, not be referenced by
        any other settings and the user must have delete permissions for the setting.

        Parameters
        ----------
        names_or_ids : Sequence[str | int]
            The names or identifiers of the settings objects to delete.
            The identifier is a globally unique integer that is assinged when
            a setting gets first saved to the registry.
            The name is a user defined name for the settings object that must
            consist of only alphanumeric characters, underscores and hyphens and start
            with a letter.
            Other users' settings can be deleted (if permissioned) by using either
            the global int identifier or prefixing the name with the user name and
            a forward slash, e.g. "sebastian.janisch@bayesline.com/SebastiansSettings".
        raise_on_errors : bool, default=True
            If True, raise an exception if the settings object could not be deleted
            (any settings that could be deleted will be deleted).
            If False, return a DeleteResult object with the errors.

        Raises
        ------
        CouldNotDeleteSettingsError
            If an error captured by the item result is encountered and raise_on_errors
            is True
        SettingsRegistryError
            If an unexpected error occurs while deleting the settings objects.

        Returns
        -------
        DeleteResult
            Result object for the delete operation.
        """

    @abc.abstractmethod
    def grant(
        self,
        *,
        permission_to: Literal["read", "write", "delete", "admin"],
        for_setting: str | int,
        to_groups: list[str] | None = None,
        to_users: list[str] | None = None,
        including_references: bool = False,
        raise_on_errors: bool = True,
    ) -> PermissionItemResult:
        """
        Grant a permission to a group or user for given settings.

        The settings must be of the correct type for this registry.

        Parameters
        ----------
        permission_to: Literal["read", "write", "delete", "admin"]
            The type of permission to grant.
            An option includes permission to the preceding options,
            e.g. 'delete' includes 'read', 'write', and 'delete'.
        for_setting: str | int
            The name or identifier of the settings object to grant permissions to.
            The identifier is globally unique integers that is assinged when
            a setting gets first saved to the registry.
            The name is user defined for the settings object that must
            consist of only alphanumeric characters, underscores and hyphens and start
            with a letter.
            Other users' settings can be used (if permissioned) by using either
            the global int identifier or prefixing the name with the user name and
            a forward slash, e.g. "sebastian.janisch@bayesline.com/SebastiansSettings".
            To grant permissions of settings that belong to another user the grantor
            needs to have either 'admin' permissions for the
            setting in question.
        to_groups: list[str] | None, default=None
            The groups to grant the permission to.
        to_users: list[str] | None, default=None
            The users to grant the permission to (email address).
        including_references: bool, default=False
            If True, grant the permission to the settings objects and all settings
            objects that are referenced by the settings objects.
            If False, grant the permission to the settings objects only.
        raise_on_errors : bool, default=True
            If True, raise an exception if the permissions could not be granted.
            If False, return a PermissionItemResult object with the errors.

        Raises
        ------
        CouldNotPermissionSettingsError
            If an error captured by the item result is encountered and raise_on_errors
            is True
        SettingsRegistryError
            If an unexpected error occurs while permissioning the settings objects.

        Returns
        -------
        PermissionItemResult
            Result object for the permissioning operation.
        """

    @abc.abstractmethod
    def grant_many(
        self,
        *,
        permission_to: Literal["read", "write", "delete", "admin"],
        for_settings: list[str | int],
        to_groups: list[str] | None = None,
        to_users: list[str] | None = None,
        including_references: bool = False,
        raise_on_errors: bool = True,
    ) -> PermissionResult:
        """
        Grant a permission to a group or user for given settings.

        This method is best effort. Partial execution is possible if some settings
        objects can be granted permissions and others cannot.

        The settings must be of the correct type for this registry.

        Parameters
        ----------
        permission_to: Literal["read", "write", "delete", "admin"]
            The type of permission to grant.
            An option includes permission to the preceding options,
            e.g. 'delete' includes 'read', 'write', and 'delete'.
        for_settings: list[str | int]
            The names or identifiers of the settings objects to read.
            The identifiers are globally unique integers that is assinged when
            a setting gets first saved to the registry.
            The names are user defined names for the settings objects that must
            consist of only alphanumeric characters, underscores and hyphens and start
            with a letter.
            Other users' settings can be used (if permissioned) by using either
            the global int identifier or prefixing the name with the user name and
            a forward slash, e.g. "sebastian.janisch@bayesline.com/SebastiansSettings".
            To grant permissions of settings that belong to another user the grantor
            needs to have 'admin' permissions for the
            setting in question.
        to_groups: list[str] | None, default=None
            The groups to grant the permission to.
        to_users: list[str] | None, default=None
            The users to grant the permission to (email address).
        including_references: bool, default=False
            If True, grant the permission to the settings objects and all settings
            objects that are referenced by the settings objects.
            If False, grant the permission to the settings objects only.
        raise_on_errors : bool, default=True
            If True, raise an exception if the permissions could not be granted.
            If False, return a PermissionResult object with the errors.

        Raises
        ------
        CouldNotPermissionSettingsError
            If an error captured by the item result is encountered and raise_on_errors
            is True
        SettingsRegistryError
            If an unexpected error occurs while permissioning the settings objects.

        Returns
        -------
        PermissionResult
            Result object for the permissioning operation.
        """

    @abc.abstractmethod
    def revoke(
        self,
        *,
        for_setting: str | int,
        from_groups: list[str] | None = None,
        from_users: list[str] | None = None,
        including_references: bool = False,
        raise_on_errors: bool = True,
    ) -> PermissionItemResult:
        """
        Revoke a permission from a group or user for given settings.

        The settings must be of the correct type for this registry.

        Parameters
        ----------
        for_setting: str | int
            The names or identifiers of the settings objects to read.
            The identifiers are globally unique integers that is assinged when
            a setting gets first saved to the registry.
            The names are user defined names for the settings objects that must
            consist of only alphanumeric characters, underscores and hyphens and start
            with a letter.
            Other users' settings can be used (if permissioned) by using either
            the global int identifier or prefixing the name with the user name and
            a forward slash, e.g. "sebastian.janisch@bayesline.com/SebastiansSettings".
            To revoke permissions of settings that belong to another user the
            revoking user needs to have 'admin' permissions
            for the setting in question.
        from_groups: list[str] | None, default=None
            The groups to revoke the permission from.
        from_users: list[str] | None, default=None
            The users to revoke the permission from (email address).
        including_references: bool, default=False
            If True, revoke the permission from the settings objects and all settings
            objects that are referenced by the settings objects.
            If False, revoke the permission from the settings objects only.
        raise_on_errors : bool, default=True
            If True, raise an exception if the permissions could not be revoked.
            If False, return a PermissionItemResult object with the errors.

        Raises
        ------
        CouldNotPermissionSettingsError
            If an error captured by the item result is encountered and raise_on_errors
            is True
        SettingsRegistryError
            If an unexpected error occurs while permissioning the settings objects.

        Returns
        -------
        PermissionItemResult
            Result object for the permissioning operation.
        """

    @abc.abstractmethod
    def revoke_many(
        self,
        *,
        for_settings: list[str | int],
        from_groups: list[str] | None = None,
        from_users: list[str] | None = None,
        including_references: bool = False,
        raise_on_errors: bool = True,
    ) -> PermissionResult:
        """
        Revoke a permission from a group or user for given settings.

        This method is best effort. Partial execution is possible if some settings
        objects can be revoked permissions from and others cannot.

        The settings must be of the correct type for this registry.

        Parameters
        ----------
        for_settings: list[str | int]
            The names or identifiers of the settings objects to read.
            The identifiers are globally unique integers that is assinged when
            a setting gets first saved to the registry.
            The names are user defined names for the settings objects that must
            consist of only alphanumeric characters, underscores and hyphens and start
            with a letter.
            Other users' settings can be used (if permissioned) by using either
            the global int identifier or prefixing the name with the user name and
            a forward slash, e.g. "sebastian.janisch@bayesline.com/SebastiansSettings".
            To revoke permissions of settings that belong to another user the
            revoking user needs to have 'admin' permissions
            for the setting in question.
        from_groups: list[str] | None, default=None
            The groups to revoke the permission from.
        from_users: list[str] | None, default=None
            The users to revoke the permission from (email address).
        including_references: bool, default=False
            If True, revoke the permission from the settings objects and all settings
            objects that are referenced by the settings objects.
            If False, revoke the permission from the settings objects only.
        raise_on_errors : bool, default=True
            If True, raise an exception if the permissions could not be revoked.
            If False, return a PermissionResult object with the errors.

        Raises
        ------
        CouldNotPermissionSettingsError
            If an error captured by the item result is encountered and raise_on_errors
            is True
        SettingsRegistryError
            If an unexpected error occurs while permissioning the settings objects.

        Returns
        -------
        PermissionResult
            Result object for the permissioning operation.
        """

    @abc.abstractmethod
    def list_user_names(self) -> Mapping[str, str]:
        """
        List all users that settings can be granted permissions to.

        Returns
        -------
        Mapping[str, str]
            Mapping of unique user id (e.g. email) to their names.
        """


class SettingsRegistry(abc.ABC):
    """
    Abstract base class for settings registries.

    This settings registry covers all available settings types, e.g. `UniverseSettings`,
    `PortfolioSettings`, etc.
    """

    def get_settings_types(self) -> Sequence[type[Settings]]:
        """
        Get all settings types covered in this registry.

        Returns
        -------
        Sequence[type[Settings]]
            A sequence of the settings types covered in this registry.
        """
        return SETTINGS_TYPES

    @abc.abstractmethod
    def __getitem__(self, settings_type: type[T]) -> TypedSettingsRegistry[T]:
        """
        Get the typed settings registry for the given settings type.

        Parameters
        ----------
        settings_type : type[T]
            The settings type to get the registry for.

        Raises
        ------
        KeyError
            If the settings type is not covered in this registry.

        Returns
        -------
        TypedSettingsRegistry[T]
            The typed settings registry for the given settings type.
        """

    @abc.abstractmethod
    def get_identifiers(
        self, which: Literal["all", "mine"] = "all"
    ) -> SettingsIdentifiers:
        """
        Get all identifiers for all settings types covered in this registry.

        Parameters
        ----------
        which : Literal["all", "mine"], default="all"
            'mine' will only return those identfiers owned by the current user
            'all' will also return those identifiers that the current user is
            permissioned to READ.

        Returns
        -------
        SettingsIdentifiers
            The identifiers for all settings types covered in this registry.
        """

    @abc.abstractmethod
    def save_many(
        self,
        settings: Mapping[str | int, Settings],
        *,
        overwrite: bool = False,
        raise_on_errors: bool = True,
    ) -> SaveResult:
        """
        Save multiple settings objects to the registry.

        This method is best effort. Partial execution is possible if some settings
        objects can be saved and others cannot.

        Parameters
        ----------
        settings : Mapping[str | int, Settings]
            The settings objects to save, keys being the names or global int ids of the
            settings objects.
            If int ids are used, the settings objects must exist in the registry, which
            implies that overwrite must be True.
            The name is a user defined name for the settings object that must
            consist of only alphanumeric characters, underscores and hyphens and start
            with a letter.
            Other users' settings can be written/updated (if permissioned) by using
            either the global int identifier or prefixing the name with the user name,
            e.g. "sebastian.janisch@bayesline.com/SebastiansSettings".
        overwrite : bool, default=False
            If True, overwrite the settings objects if they already exist.
            If False, mark an error for settings objects that already exist.
        raise_on_errors : bool, default=True
            If True, raise an exception if any of the settings objects could not be saved.
            If False, return a SaveResult object with the errors.

        Raises
        ------
        CouldNotSaveSettingsError
            If an error captured by the item result is encountered and raise_on_errors
            is True
        SettingsRegistryError
            If an unexpected error occurs while saving the settings objects.

        Returns
        -------
        SaveResult
            Result object for the save operation.
        """

    @abc.abstractmethod
    def read_many(
        self, names_or_ids: Sequence[str | int]
    ) -> Sequence[SettingResult[Settings[Any]]]:
        """
        Read settings objects from the registry for the given names or identifiers.

        Parameters
        ----------
        names_or_ids: Sequence[str | int]
            The names or identifiers of the settings objects to read.
            The identifiers are globally unique integers that is assinged when
            a setting gets first saved to the registry.
            The names are user defined names for the settings objects that must
            consist of only alphanumeric characters, underscores and hyphens and start
            with a letter.
            Other users' settings can be read (if permissioned) by using either
            the global int identifier or prefixing the name with the user name and
            a forward slash, e.g. "sebastian.janisch@bayesline.com/SebastiansSettings".

        Returns
        -------
        Sequence[SettingResult[Settings[Any]]]
            The settings objects in exact same order as the input.
        """

    @abc.abstractmethod
    def delete_many(
        self, names_or_ids: Sequence[str | int], *, raise_on_errors: bool = True
    ) -> DeleteResult:
        """
        Delete settings objects from the registry for the given names or identifiers.

        This method is best effort. Partial deletions are possible if some settings
        objects can be deleted and others cannot.

        For a setting to be able to be deleted, it must exist, not be referenced by
        any other settings and the user must have delete permissions for the setting.

        Parameters
        ----------
        names_or_ids : Sequence[str | int]
            The names or identifiers of the settings objects to delete.
            The identifier is a globally unique integer that is assinged when
            a setting gets first saved to the registry.
            The name is a user defined name for the settings object that must
            consist of only alphanumeric characters, underscores and hyphens and start
            with a letter.
            Other users' settings can be deleted (if permissioned) by using either
            the global int identifier or prefixing the name with the user name and
            a forward slash, e.g. "sebastian.janisch@bayesline.com/SebastiansSettings".
        raise_on_errors : bool, default=True
            If True, raise an exception if the settings object could not be deleted
            (any settings that could be deleted will be deleted).
            If False, return a DeleteResult object with the errors.

        Raises
        ------
        CouldNotDeleteSettingsError
            If an error captured by the item result is encountered and raise_on_errors
            is True
        SettingsRegistryError
            If an unexpected error occurs while deleting the settings objects.

        Returns
        -------
        DeleteResult
            Result object for the delete operation.
        """

    @abc.abstractmethod
    def grant_many(
        self,
        *,
        permission_to: Literal["read", "write", "delete", "admin"],
        for_settings: list[str | int],
        to_groups: list[str] | None = None,
        to_users: list[str] | None = None,
        including_references: bool = False,
        raise_on_errors: bool = True,
    ) -> PermissionResult:
        """
        Grant a permission to a group or user for given settings.

        This method is best effort. Partial execution is possible if some settings
        objects can be granted permissions and others cannot.

        Parameters
        ----------
        permission_to: Literal["read", "write", "delete", "admin"]
            The type of permission to grant.
            An option includes permission to the preceding options,
            e.g. 'delete' includes 'read', 'write', and 'delete'.
        for_settings: list[str | int]
            The names or identifiers of the settings objects to read.
            The identifiers are globally unique integers that is assinged when
            a setting gets first saved to the registry.
            The names are user defined names for the settings objects that must
            consist of only alphanumeric characters, underscores and hyphens and start
            with a letter.
            Other users' settings can be used (if permissioned) by using either
            the global int identifier or prefixing the name with the user name and
            a forward slash, e.g. "sebastian.janisch@bayesline.com/SebastiansSettings".
            To grant permissions of settings that belong to another user the grantor
            needs to have 'admin' permissions for the
            setting in question.
        to_groups: list[str] | None, default=None
            The groups to grant the permission to.
        to_users: list[str] | None, default=None
            The users to grant the permission to (email address).
        including_references: bool, default=False
            If True, grant the permission to the settings objects and all settings
            objects that are referenced by the settings objects.
            If False, grant the permission to the settings objects only.
        raise_on_errors: bool, default=True
            If True, raise an exception if the permissions could not be granted.
            If False, return a PermissionResult object with the errors.

        Raises
        ------
        CouldNotPermissionSettingsError
            If an error captured by the item result is encountered and raise_on_errors
            is True
        SettingsRegistryError
            If an unexpected error occurs while permissioning the settings objects.

        Returns
        -------
        PermissionResult
            Result objects for the permissioning operation.
        """

    @abc.abstractmethod
    def revoke_many(
        self,
        *,
        for_settings: list[str | int],
        from_groups: list[str] | None = None,
        from_users: list[str] | None = None,
        including_references: bool = False,
        raise_on_errors: bool = True,
    ) -> PermissionResult:
        """
        Revoke a permission from a group or user for given settings.

        This method is best effort. Partial execution is possible if some settings
        objects can be revoked permissions from and others cannot.

        Parameters
        ----------
        for_settings: list[str | int]
            The names or identifiers of the settings objects to read.
            The identifiers are globally unique integers that is assinged when
            a setting gets first saved to the registry.
            The names are user defined names for the settings objects that must
            consist of only alphanumeric characters, underscores and hyphens and start
            with a letter.
            Other users' settings can be used (if permissioned) by using either
            the global int identifier or prefixing the name with the user name and
            a forward slash, e.g. "sebastian.janisch@bayesline.com/SebastiansSettings".
            To revoke permissions of settings that belong to another user the
            revoking user needs to have 'admin' permissions
            for the setting in question.
        from_groups: list[str] | None, default=None
            The groups to revoke the permission from.
        from_users: list[str] | None, default=None
            The users to revoke the permission from (email address).
        including_references: bool, default=False
            If True, revoke the permission from the settings objects and all settings
            objects that are referenced by the settings objects.
            If False, revoke the permission from the settings objects only.
        raise_on_errors: bool, default=True
            If True, raise an exception if the permissions could not be revoked.
            If False, return a PermissionResult object with the errors.

        Raises
        ------
        CouldNotPermissionSettingsError
            If an error captured by the item result is encountered and raise_on_errors
            is True
        SettingsRegistryError
            If an unexpected error occurs while permissioning the settings objects.

        Returns
        -------
        PermissionResult
            Result objects for the permissioning operation.
        """

    @abc.abstractmethod
    def list_user_names(self) -> Mapping[str, str]:
        """
        List all users that settings can be granted permissions to.

        Returns
        -------
        Mapping[str, str]
            Mapping of unique user id (e.g. email) to their names.
        """


@docstrings_from_sync
class AsyncTypedSettingsRegistry(abc.ABC, Generic[T]):

    @property
    @abc.abstractmethod
    def settings_type(self) -> type[T]: ...  # noqa: D102

    @abc.abstractmethod
    async def get_identifiers(  # noqa: D102
        self, which: Literal["all", "mine"] = "all"
    ) -> SettingsIdentifiers: ...

    @abc.abstractmethod
    async def save(  # noqa: D102
        self,
        name_or_id: str | int,
        settings: T,
        *,
        overwrite: bool = False,
        raise_on_errors: bool = True,
    ) -> SaveItemResult: ...

    @abc.abstractmethod
    async def save_many(  # noqa: D102
        self,
        settings: Mapping[str | int, T],
        *,
        overwrite: bool = False,
        raise_on_errors: bool = True,
    ) -> SaveResult: ...

    @abc.abstractmethod
    async def read(self, name_or_id: str | int) -> SettingResult[T]: ...  # noqa: D102

    @abc.abstractmethod
    async def read_many(  # noqa: D102
        self, names_or_ids: Sequence[str | int]
    ) -> Sequence[SettingResult[T]]: ...

    @abc.abstractmethod
    async def delete(  # noqa: D102
        self, name_or_id: str | int, *, raise_on_errors: bool = True
    ) -> DeleteItemResult: ...

    @abc.abstractmethod
    async def delete_many(  # noqa: D102
        self, names_or_ids: Sequence[str | int], *, raise_on_errors: bool = True
    ) -> DeleteResult: ...

    @abc.abstractmethod
    async def grant(  # noqa: D102
        self,
        *,
        permission_to: Literal["read", "write", "delete", "admin"],
        for_setting: str | int,
        to_groups: list[str] | None = None,
        to_users: list[str] | None = None,
        including_references: bool = False,
        raise_on_errors: bool = True,
    ) -> PermissionItemResult: ...

    @abc.abstractmethod
    async def grant_many(  # noqa: D102
        self,
        *,
        permission_to: Literal["read", "write", "delete", "admin"],
        for_settings: list[str | int],
        to_groups: list[str] | None = None,
        to_users: list[str] | None = None,
        including_references: bool = False,
        raise_on_errors: bool = True,
    ) -> PermissionResult: ...

    @abc.abstractmethod
    async def revoke(  # noqa: D102
        self,
        *,
        for_setting: str | int,
        from_groups: list[str] | None = None,
        from_users: list[str] | None = None,
        including_references: bool = False,
        raise_on_errors: bool = True,
    ) -> PermissionItemResult: ...

    @abc.abstractmethod
    async def revoke_many(  # noqa: D102
        self,
        *,
        for_settings: list[str | int],
        from_groups: list[str] | None = None,
        from_users: list[str] | None = None,
        including_references: bool = False,
        raise_on_errors: bool = True,
    ) -> PermissionResult: ...

    @abc.abstractmethod
    async def list_user_names(self) -> Mapping[str, str]: ...  # noqa: D102


@docstrings_from_sync
class AsyncSettingsRegistry(abc.ABC):

    async def get_settings_types(self) -> Sequence[type[Settings]]:
        """
        Get all settings types covered in this registry.

        Returns
        -------
        Sequence[type[Settings]]
            A sequence of the settings types covered in this registry.
        """
        return SETTINGS_TYPES

    @abc.abstractmethod
    def __getitem__(  # noqa: D105
        self, settings_type: type[T]
    ) -> AsyncTypedSettingsRegistry[T]: ...

    @abc.abstractmethod
    async def get_identifiers(  # noqa: D102
        self, which: Literal["all", "mine"] = "all"
    ) -> SettingsIdentifiers: ...

    @abc.abstractmethod
    async def save_many(  # noqa: D102
        self,
        settings: Mapping[str | int, Settings],
        *,
        overwrite: bool = False,
        raise_on_errors: bool = True,
    ) -> SaveResult: ...

    @abc.abstractmethod
    async def read_many(  # noqa: D102
        self, names_or_ids: Sequence[str | int]
    ) -> Sequence[SettingResult[Settings[Any]]]: ...

    @abc.abstractmethod
    async def delete_many(  # noqa: D102
        self, names_or_ids: Sequence[str | int], *, raise_on_errors: bool = True
    ) -> DeleteResult: ...

    @abc.abstractmethod
    async def grant_many(  # noqa: D102
        self,
        *,
        permission_to: Literal["read", "write", "delete", "admin"],
        for_settings: list[str | int],
        to_groups: list[str] | None = None,
        to_users: list[str] | None = None,
        including_references: bool = False,
        raise_on_errors: bool = True,
    ) -> PermissionResult: ...

    @abc.abstractmethod
    async def revoke_many(  # noqa: D102
        self,
        *,
        for_settings: list[str | int],
        from_groups: list[str] | None = None,
        from_users: list[str] | None = None,
        including_references: bool = False,
        raise_on_errors: bool = True,
    ) -> PermissionResult: ...

    @abc.abstractmethod
    async def list_user_names(self) -> Mapping[str, str]: ...  # noqa: D102
