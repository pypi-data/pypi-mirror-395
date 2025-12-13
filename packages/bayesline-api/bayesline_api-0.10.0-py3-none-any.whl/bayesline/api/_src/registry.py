from __future__ import annotations

import abc
import datetime as dt
import re
from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Callable, Generic, Literal, TypeVar

from pydantic import BaseModel, Field, ValidationError

from bayesline.api._src._utils import docstrings_from_sync


class InvalidSettingsError(ValueError):
    """Exception raised when settings are invalid."""

    pass


E = TypeVar("E")


@dataclass
class SettingsTypeMetaData(Generic[E]):
    """Metadata for settings type references."""

    references: type[Settings]
    # a function that extracts only the references from the settings
    extractor: Callable[[E], list[str | int]] | None = None

    def extract(self, v: E) -> list[str | int]:
        """
        Extract references from a value.

        Parameters
        ----------
        v : E
            The value to extract references from.

        Returns
        -------
        list[str | int]
            A list of extracted references.

        Raises
        ------
        ValueError
            If the value type cannot be extracted and no extractor is defined.
        """
        if self.extractor is None:
            if isinstance(v, str | int):
                return [v]
            elif isinstance(v, self.references):
                return []
            else:
                raise ValueError(
                    f"Cannot extract {v} of type {type(v)}. "
                    "Define an extractor in the pydantic model"
                )
        return self.extractor(v)


class RawSettings(BaseModel):
    """Raw settings data structure."""

    model_type: str
    name: str | None
    identifier: int | None
    exists: bool
    raw_json: dict[str, Any]
    references: list[RawSettings]
    extra: dict[str, Any] = Field(default_factory=dict)


T = TypeVar("T")
ModelType = str


class SettingsMetaData(BaseModel, frozen=True, extra="allow"):
    """Metadata for settings objects."""

    created_on: dt.datetime
    last_updated: dt.datetime


class SettingsMenu(
    abc.ABC,
    BaseModel,
    frozen=True,
    extra="forbid",
):
    """Abstract base class for settings menus."""

    @abc.abstractmethod
    def describe(self) -> str:
        """
        Describe the settings menu.

        Returns
        -------
        str
            A human readable description of the settings menu.
        """


class EmptySettingsMenu(SettingsMenu):
    """Empty settings menu implementation."""

    def describe(self) -> str:
        """
        Describe the empty settings menu.

        Returns
        -------
        str
            A description of the empty settings menu.
        """
        return "EmptySettingsMenu"


SettingsMenuType = TypeVar("SettingsMenuType", bound=SettingsMenu)


class Settings(BaseModel, Generic[SettingsMenuType], frozen=True, extra="forbid"):
    """Base class for all settings objects."""

    @property
    @abc.abstractmethod
    def menu_type(self) -> type[SettingsMenuType]:
        """Get the menu type for this settings object.

        Returns
        -------
        type[SettingsMenuType]
            The menu type for this settings object.
        """

    def references(
        self,
    ) -> dict[str, dict[type[Settings], list[str | int]]]:
        """
        Get all other settings that are referenced by this settings.

        For example, if a risk model references a universe.

        Returns
        -------
        dict[str, dict[type[Settings], list[str | int]]]
            A dict of the field name to a dict of the referenced settings type to the list
            of referenced settings (either by name or id).
        """
        result: dict[str, dict[type[Settings], list[str | int]]] = defaultdict(
            lambda: defaultdict(list)
        )

        for field_name, field_info in self.__class__.model_fields.items():
            for meta_data in field_info.metadata:
                if isinstance(meta_data, SettingsTypeMetaData):
                    ref_type = meta_data.references
                    field_value = getattr(self, field_name)
                    if field_value is not None:
                        result[field_name][ref_type].extend(
                            meta_data.extract(field_value)
                        )

        return result

    def get_references(self) -> Sequence[str | int]:
        """
        Get references for this settings object.

        Returns
        -------
        Sequence[str | int]
            A sequence of references (strings or integers) for this settings object.
        """
        return []

    def validate_settings(self, menu: SettingsMenuType | None) -> None:
        """
        Validate the settings against the given menu.

        Parameters
        ----------
        menu : SettingsMenuType | None
            The menu to validate against. If None, the settings are validated against
            without having the menu context. This means that less validation is done.

        Raises
        ------
        AttributeError
            If the menu type does not match the settings type.
        """
        if menu:
            # test that the menu matches the settings type
            if self.menu_type is not type(menu):
                raise AttributeError(
                    f"The menu type {type(menu).__qualname__} does not match the "
                    f"settings type {self.menu_type.__qualname__}."
                )

        self.model_validate(self.model_dump(), context=menu)

    def describe(self, menu: SettingsMenuType) -> str:
        """
        Describe the settings.

        Parameters
        ----------
        menu : SettingsMenuType
            The menu to use to describe the settings.

        Returns
        -------
        str
            A description of the settings.
        """
        del menu  # not used
        return self.model_dump_json(indent=2)


class AsyncSettingsResolver(abc.ABC):
    """Abstract base class for async settings resolvers."""

    @classmethod
    @abc.abstractmethod
    def model_types(cls) -> dict[ModelType, type[Settings]]:
        """
        Get model types mapping.

        Returns
        -------
        dict[ModelType, type[Settings]]
            A dictionary of the model types (str) to their type instance.
            Typically this is e.g. `{UniverseSettings.__name__: UniverseSettings}`.
        """

    @abc.abstractmethod
    async def resolve_settings(self, settings: list[Settings]) -> list[RawSettings]:
        """
        Resolve the given references.

        Parameters
        ----------
        settings : list[Settings]
            The settings to resolve.

        Returns
        -------
        list[RawSettings]
            List of raw settings exactly in the same order as the input.
        """

    @abc.abstractmethod
    async def resolve_references(
        self, references: list[tuple[ModelType, str | int]]
    ) -> list[RawSettings]:
        """
        Resolve the given settings references.

        Parameters
        ----------
        references : list[tuple[ModelType, str | int]]
            The settings references to resolve.

        Returns
        -------
        list[RawSettings]
            List of raw settings exactly in the same order as the input.
        """

    async def to_settings_model(
        self, raw_settings: RawSettings, resolve: bool = False
    ) -> Settings:
        """
        Convert the given raw settings to a settings model.

        Parameters
        ----------
        raw_settings : RawSettings
            The raw settings to convert.
        resolve : bool, default=False
            If True, the references are resolved.

        Returns
        -------
        Settings
            The settings model.

        Raises
        ------
        InvalidSettingsError
            If the raw settings are invalid.
        NotImplementedError
            If resolve=True is not implemented.
        """
        if resolve:
            # resolve all references recursively
            raise NotImplementedError()
        if not await self.is_valid(raw_settings):
            raise InvalidSettingsError(raw_settings.raw_json)
        return self.model_types()[raw_settings.model_type].model_validate(
            raw_settings.raw_json
        )

    async def is_valid(self, raw_setting: RawSettings) -> bool:
        """
        Check if the given raw settings are valid.

        Parameters
        ----------
        raw_setting : RawSettings
            The raw settings to check.

        Returns
        -------
        bool
            True if the raw setting is valid, False otherwise.
        """
        valid = raw_setting.exists
        valid &= not self.is_corrupted(raw_setting)
        valid &= await self.has_all_references(raw_setting)

        if valid:
            settings_model = self.model_types()[raw_setting.model_type].model_validate(
                raw_setting.raw_json
            )
            valid &= not (await self.errors_against_settings_menu(settings_model))
        return valid

    def is_corrupted(self, raw_setting: RawSettings) -> bool:
        """
        Check if the given raw settings are corrupted.

        Parameters
        ----------
        raw_setting : RawSettings
            The raw settings to check.

        Returns
        -------
        bool
            True if the raw setting is corrupted, False otherwise.
        """
        if not raw_setting.raw_json:
            return True

        try:
            settings_type = self.model_types()[raw_setting.model_type]
            settings_type.model_validate(raw_setting.raw_json)
            return False
        except ValidationError:
            return True
        except KeyError:
            return True

    async def has_all_references(self, raw_settings: RawSettings) -> bool:
        """
        Check if the given settings have all their references.

        Parameters
        ----------
        raw_settings : RawSettings
            The raw settings to check.

        Returns
        -------
        bool
            True if the settings have all their references, False otherwise.
        """
        return all([await self.is_valid(ref) for ref in raw_settings.references])

    @abc.abstractmethod
    async def errors_against_settings_menu(self, settings: Settings) -> list[str]:
        """
        Get errors that the given settings have against the settings menu.

        Parameters
        ----------
        settings : Settings
            The settings to validate.

        Returns
        -------
        list[str]
            A list of error messages if the settings are invalid against the settings menu.
        """

    async def validation_messages(self, raw_settings: RawSettings) -> list[str]:
        """
        Get validation messages for raw settings.

        Parameters
        ----------
        raw_settings : RawSettings
            The raw settings to get validation messages for.

        Returns
        -------
        list[str]
            A list of validation messages for the raw settings.
        """
        messages = []
        corrupted = self.is_corrupted(raw_settings)
        missing = not raw_settings.exists
        if missing:
            messages.append("The setting does not exist.")
        elif corrupted:
            messages.append("The setting json is invalid.")
        if not missing and not corrupted:
            await self.errors_against_settings_menu(
                self.model_types()[raw_settings.model_type].model_validate(
                    raw_settings.raw_json
                )
            )
            messages.extend(
                (
                    await self.errors_against_settings_menu(
                        self.model_types()[raw_settings.model_type].model_validate(
                            raw_settings.raw_json
                        )
                    )
                )
            )
        for ref in raw_settings.references:
            ref_messages = [
                m.replace("The setting", f"The reference {ref.name!r}")
                for m in await self.validation_messages(ref)
            ]
            messages.extend(ref_messages)
        return messages


Mode = Literal["All", "Valid", "Invalid"]


class ReadOnlyRegistry(abc.ABC, Generic[T]):
    """Abstract base class for read-only registries."""

    @abc.abstractmethod
    def ids(self, mode: Mode = "Valid") -> dict[int, str]:
        """
        Get mapping of IDs to names.

        Parameters
        ----------
        mode : Mode, default="Valid"
            The mode to use when retrieving the ids.

        Returns
        -------
        dict[int, str]
            A dictionary of the unique identifiers to the unique names.
        """

    @abc.abstractmethod
    def names(self, mode: Mode = "Valid") -> dict[str, int]:
        """
        Get mapping of names to IDs.

        Parameters
        ----------
        mode : Mode, default="Valid"
            The mode to use when retrieving the names.

        Returns
        -------
        dict[str, int]
            A dictionary of the unique names to the unique identifiers.
        """

    @abc.abstractmethod
    def get_raw(self, name_or_id: list[str | int]) -> list[RawSettings]:
        """
        Get raw settings by names or IDs.

        Parameters
        ----------
        name_or_id : list[str | int]
            The unique names or int identifiers of the items to retrieve.

        Returns
        -------
        list[RawSettings]
            A list of `RawSettings` in the same order as input.
        """

    @abc.abstractmethod
    def get(self, name: str | int) -> T:
        """
        Get an item by name or ID.

        Parameters
        ----------
        name : str | int
            The unique name or int identifier of the item to retrieve.

        Raises
        ------
        KeyError
            If the item does not exist.
        InvalidSettingsError
            If the item exists but is invalid.

        Returns
        -------
        T
            The item for the given name.
        """

    @abc.abstractmethod
    def get_metadata(self, name: str | int) -> SettingsMetaData:
        """
        Get metadata for an item by name or ID.

        Parameters
        ----------
        name : str | int
            The unique name or int identifier of the item to retrieve.

        Raises
        ------
        KeyError
            If the item does not exist.

        Returns
        -------
        SettingsMetaData
            The metadata for the given name.
        """

    def get_all(self) -> dict[str, T]:
        """
        Get all valid available settings.

        Returns
        -------
        dict[str, T]
            A dictionary of all valid available settings.
        """
        return {name: self.get(name) for name in self.names()}

    def get_all_with_metadata(self) -> dict[str, tuple[T, SettingsMetaData]]:
        """
        Get all valid available settings with metadata.

        Returns
        -------
        dict[str, tuple[T, SettingsMetaData]]
            A dictionary of all valid available settings with metadata.
        """
        all_settings = self.get_all()
        all_metadata = self.get_all_metadata()

        return {
            name: (all_settings[name], all_metadata[name])
            for name in all_settings.keys()
        }

    def get_all_metadata(self) -> dict[str, SettingsMetaData]:
        """
        Get all available settings metadata.

        Returns
        -------
        dict[str, SettingsMetaData]
            A dictionary of all available settings metadata (valid or invalid).
        """
        return {name: self.get_metadata(name) for name in self.names()}


class Registry(Generic[T], ReadOnlyRegistry[T]):
    """Abstract base class for writable registries."""

    @abc.abstractmethod
    def save(self, name: str, settings: T) -> int:
        """
        Save an item to the registry.

        Parameters
        ----------
        name : str
            The unique name of the item to save.
            The name cannot be all numbers.
        settings : T
            The item to save.

        Raises
        ------
        ValueError
            If the item name already exists or is all numbers.

        Returns
        -------
        int
            A unique identifier for the saved item.
        """

    @abc.abstractmethod
    def update(self, name: str | int, settings: T) -> RawSettings:
        """
        Update an existing item in the registry.

        Parameters
        ----------
        name : str | int
            The unique name or int identifier of the item to update.
        settings : T
            The item to update.

        Raises
        ------
        KeyError
            If the item does not exist.

        Returns
        -------
        RawSettings
            The previous raw settings item for the given name.
        """

    @abc.abstractmethod
    def delete(self, name: str | int) -> RawSettings:
        """
        Delete an item from the registry.

        Parameters
        ----------
        name : str | int
            The unique name or int identifier of the settings to delete.

        Raises
        ------
        KeyError
            If the item does not exist.

        Returns
        -------
        RawSettings
            The deleted raw settings item for the given name.
        """


@docstrings_from_sync
class AsyncReadOnlyRegistry(abc.ABC, Generic[T]):

    @abc.abstractmethod
    async def ids(self, mode: Mode = "Valid") -> dict[int, str]: ...  # noqa: D102

    @abc.abstractmethod
    async def names(self, mode: Mode = "Valid") -> dict[str, int]: ...  # noqa: D102

    @abc.abstractmethod
    async def get_raw(  # noqa: D102
        self, name_or_id: list[str | int]
    ) -> list[RawSettings]: ...

    @abc.abstractmethod
    async def get(self, name: str | int) -> T: ...  # noqa: D102

    @abc.abstractmethod
    async def get_metadata(self, name: str | int) -> SettingsMetaData: ...  # noqa: D102

    async def get_all(self) -> dict[str, T]:  # noqa: D102
        return {name: await self.get(name) for name in await self.names()}

    async def get_all_with_metadata(  # noqa: D102
        self,
    ) -> dict[str, tuple[T, SettingsMetaData]]:
        all_settings = await self.get_all()
        all_metadata = await self.get_all_metadata()

        return {
            name: (all_settings[name], all_metadata[name])
            for name in all_settings.keys()
        }

    async def get_all_metadata(self) -> dict[str, SettingsMetaData]:  # noqa: D102
        return {name: await self.get_metadata(name) for name in await self.names()}


class AsyncRegistry(Generic[T], AsyncReadOnlyRegistry[T]):
    """Abstract base class for async writable registries."""

    @abc.abstractmethod
    async def save(self, name: str, settings: T) -> int: ...  # noqa: D102

    @abc.abstractmethod
    async def update(  # noqa: D102
        self, name: str | int, settings: T
    ) -> RawSettings: ...

    @abc.abstractmethod
    async def delete(self, name: str | int) -> RawSettings: ...  # noqa: D102


SettingsType = TypeVar("SettingsType", bound=Settings)


class SettingsRegistry(Registry[SettingsType], Generic[SettingsType, SettingsMenuType]):
    """Registry for settings with validation against a settings menu."""

    @abc.abstractmethod
    def available_settings(self, dataset_name: str | None = None) -> SettingsMenuType:
        """
        Get available settings menu for this registry.

        Parameters
        ----------
        dataset_name : str | None, default=None
            The name of the dataset to use when retrieving the settings menu.
            If not provided, the settings menu will be retrieved for the
            default dataset.

        Returns
        -------
        SettingsMenuType
            A description of valid settings for this registry.
        """

    def save(self, name: str, settings: SettingsType) -> int:
        """
        Save settings with validation.

        Parameters
        ----------
        name : str
            The name for the settings.
        settings : SettingsType
            The settings to save.

        Returns
        -------
        int
            The unique identifier for the saved settings.

        Raises
        ------
        ValueError
            If the name consists only of numbers or if validation fails.
        """
        if re.sub(r"\d", "", name) == "":
            raise ValueError(
                f"The model model name cannot consist of only numbers: {name}",
            )
        # TODO not ideal to do a hasattr check here. think of more robust way.
        if hasattr(settings, "dataset"):
            dataset_name = settings.dataset
        else:
            dataset_name = None
        settings.validate_settings(self.available_settings(dataset_name))
        return self._do_save(name, settings)

    @abc.abstractmethod
    def _do_save(self, name: str, settings: SettingsType) -> int: ...

    def update(self, name: str | int, settings: SettingsType) -> RawSettings:
        """
        Update settings with validation.

        Parameters
        ----------
        name : str | int
            The name or identifier of the settings to update.
        settings : SettingsType
            The new settings to update with.

        Returns
        -------
        RawSettings
            The previous raw settings before the update.

        Raises
        ------
        ValueError
            If validation fails.
        """
        # TODO not ideal to do a hasattr check here. think of more robust way.
        if hasattr(settings, "dataset"):
            dataset_name = settings.dataset
        else:
            dataset_name = None
        settings.validate_settings(self.available_settings(dataset_name))
        return self._do_update(name, settings)

    @abc.abstractmethod
    def _do_update(self, name: str | int, settings: SettingsType) -> RawSettings: ...


@docstrings_from_sync
class AsyncSettingsRegistry(
    AsyncRegistry[SettingsType], Generic[SettingsType, SettingsMenuType]
):

    @abc.abstractmethod
    async def available_settings(  # noqa: D102
        self, dataset_name: str | None = None
    ) -> SettingsMenuType: ...

    async def save(self, name: str, settings: SettingsType) -> int:  # noqa: D102
        if re.sub(r"\d", "", name) == "":
            raise ValueError(
                f"The model model name cannot consist of only numbers: {name}",
            )
        if name in await self.names():
            raise ValueError(f"Name {name} already exists.")

        # TODO not ideal to do a hasattr check here. think of more robust way.
        if hasattr(settings, "dataset"):
            dataset_name = settings.dataset
        else:
            dataset_name = None

        settings.validate_settings(await self.available_settings(dataset_name))
        return await self._do_save(name, settings)

    @abc.abstractmethod
    async def _do_save(self, name: str, settings: SettingsType) -> int: ...

    async def update(  # noqa: D102
        self, name: str | int, settings: SettingsType
    ) -> RawSettings:
        # TODO not ideal to do a hasattr check here. think of more robust way.
        if hasattr(settings, "dataset"):
            dataset_name = settings.dataset
        else:
            dataset_name = None
        settings.validate_settings(await self.available_settings(dataset_name))
        return await self._do_update(name, settings)

    @abc.abstractmethod
    async def _do_update(
        self, name: str | int, settings: SettingsType
    ) -> RawSettings: ...


ApiType = TypeVar("ApiType")


class RegistryBasedApi(abc.ABC, Generic[SettingsType, SettingsMenuType, ApiType]):
    """Abstract base class for APIs based on registries."""

    @property
    @abc.abstractmethod
    def settings(self) -> SettingsRegistry[SettingsType, SettingsMenuType]:
        """Get the settings registry.

        Returns
        -------
        SettingsRegistry[SettingsType, SettingsMenuType]
            The settings registry instance.
        """
        ...

    @abc.abstractmethod
    def load(
        self, ref_or_settings: str | int | SettingsType, *args: Any, **kwargs: Any
    ) -> ApiType:
        """Load an API instance from settings or reference.

        Parameters
        ----------
        ref_or_settings : str | int | SettingsType
            Reference identifier, numeric ID, or settings object to load from.
        *args : Any
            Additional positional arguments passed to the loader.
        **kwargs : Any
            Additional keyword arguments passed to the loader.

        Returns
        -------
        ApiType
            The loaded API instance.
        """
        ...


@docstrings_from_sync
class AsyncRegistryBasedApi(abc.ABC, Generic[SettingsType, SettingsMenuType, ApiType]):

    @property
    @abc.abstractmethod
    def settings(  # noqa: D102
        self,
    ) -> AsyncSettingsRegistry[SettingsType, SettingsMenuType]: ...

    @abc.abstractmethod
    async def load(  # noqa: D102
        self, ref_or_settings: str | int | SettingsType, *args: Any, **kwargs: Any
    ) -> ApiType: ...
