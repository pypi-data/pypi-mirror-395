import abc
from typing import Literal

from bayesline.api._src._utils import docstrings_from_sync
from bayesline.api._src.equity.riskdataset_settings import (
    RiskDatasetMetadata,
    RiskDatasetProperties,
    RiskDatasetSettings,
    RiskDatasetSettingsMenu,
    RiskDatasetUpdateResult,
)
from bayesline.api._src.registry import (
    AsyncRegistryBasedApi,
    RawSettings,
    RegistryBasedApi,
)
from bayesline.api._src.tasks import AsyncTask, Task


class DatasetError(Exception):
    """Exception raised for dataset-related errors."""

    ...


class RiskDatasetApi(abc.ABC):
    """API for managing risk datasets.

    This abstract base class defines the interface for risk dataset operations,
    including updating datasets and retrieving their properties.
    """

    @property
    @abc.abstractmethod
    def settings(self) -> RiskDatasetSettings:
        """Get the settings for this risk dataset.

        Returns
        -------
        RiskDatasetSettings
            The settings for this risk dataset.
        """
        ...

    @abc.abstractmethod
    def describe(self) -> RiskDatasetProperties:
        """Get the properties of this risk dataset.

        Returns
        -------
        RiskDatasetProperties
            The properties of this risk dataset.
        """
        ...

    @abc.abstractmethod
    def update(self, force: bool = False) -> RiskDatasetUpdateResult:
        """Check underlying datasets for updates and update this dataset to latest versions.

        Parameters
        ----------
        force : bool, default=False
            If true, the update will be forced even if the dataset is up to date.

        Raises
        ------
        DatasetError
            If an error occurs.

        Returns
        -------
        RiskDatasetUpdateResult
            The result of the update operation.
        """

    @abc.abstractmethod
    def update_as_task(self) -> Task[RiskDatasetUpdateResult]: ...  # noqa: D102


class RiskDatasetLoaderApi(
    RegistryBasedApi[RiskDatasetSettings, RiskDatasetSettingsMenu, RiskDatasetApi],
):
    """API for loading and managing risk datasets.

    This class provides functionality for loading, creating, and managing risk datasets
    through a registry-based approach.
    """

    @abc.abstractmethod
    def get_default_dataset_name(self) -> str:
        """Get the default dataset name.

        Returns
        -------
        str
            The default dataset name that will be populated into settings if no
            dataset name is provided.
        """

    @abc.abstractmethod
    def get_dataset_names(
        self,
        *,
        mode: Literal["System", "User", "All"] = "All",
        status: Literal["ready", "available"] = "ready",
    ) -> list[str]:
        """Get the names of all available datasets.

        Parameters
        ----------
        mode : Literal["System", "User", "All"], default="All"
            System: only system wide datasets (available to all users and provided
            by the system).
            User: only user specific datasets (available to the current user).
            All: all datasets (system wide and user specific).
        status : Literal["ready", "available"], default="ready"
            ready: only datasets that are ready to be used.
            available: all datasets including those that need to be updated first.

        Returns
        -------
        list[str]
            The names of all available datasets.
        """

    @abc.abstractmethod
    def list_riskdatasets(self) -> list[RiskDatasetMetadata]:
        """List all available risk datasets.

        Returns
        -------
        list[RiskDatasetMetadata]
            The metadata of all available datasets.
        """

    def create_or_replace_dataset(
        self, name: str, settings: RiskDatasetSettings
    ) -> RiskDatasetApi:
        """Create a new dataset or replace an existing one.

        Parameters
        ----------
        name : str
            The name of the dataset to create or replace.
        settings : RiskDatasetSettings
            The settings for the dataset.

        Returns
        -------
        RiskDatasetApi
            The API for the created or replaced dataset.
        """
        self.delete_dataset_if_exists(name)
        return self.create_dataset(name, settings)

    @abc.abstractmethod
    def create_dataset(
        self, name: str, settings: RiskDatasetSettings
    ) -> RiskDatasetApi:
        """Create a new dataset with the given name and settings.

        Parameters
        ----------
        name : str
            The name of the dataset to create.
        settings : RiskDatasetSettings
            The settings for the dataset to create.

        Raises
        ------
        DatasetError
            If a dataset with the given name already exists
            or if the settings are otherwise invalid.

        Returns
        -------
        RiskDatasetApi
            The API of the newly created dataset.
        """

    @abc.abstractmethod
    def create_dataset_as_task(  # noqa: D102
        self, name: str, settings: RiskDatasetSettings
    ) -> Task[RiskDatasetApi]: ...

    @abc.abstractmethod
    def delete_dataset(self, name: str) -> RawSettings:
        """Delete the given dataset.

        Parameters
        ----------
        name : str
            The name of the dataset to delete.

        Raises
        ------
        KeyError
            If the dataset does not exist.
        DatasetError
            If the dataset could not be deleted.

        Returns
        -------
        RawSettings
            The raw settings of the deleted dataset.
        """

    def delete_dataset_if_exists(self, name: str) -> RawSettings | None:
        """Delete the given dataset if it exists.

        Parameters
        ----------
        name : str
            The name of the dataset to delete.

        Raises
        ------
        DatasetError
            If the dataset could not be deleted.

        Returns
        -------
        RawSettings | None
            The raw settings of the deleted dataset if dataset existed.
        """
        if name in self.settings.names(mode="All"):
            return self.delete_dataset(name)
        return None


@docstrings_from_sync
class AsyncRiskDatasetApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> RiskDatasetSettings: ...  # noqa: D102

    @abc.abstractmethod
    async def describe(self) -> RiskDatasetProperties: ...  # noqa: D102

    @abc.abstractmethod
    async def update(  # noqa: D102
        self, force: bool = False
    ) -> RiskDatasetUpdateResult: ...

    @abc.abstractmethod
    async def update_as_task(  # noqa: D102
        self, force: bool = False
    ) -> AsyncTask[RiskDatasetUpdateResult]: ...


@docstrings_from_sync
class AsyncRiskDatasetLoaderApi(
    AsyncRegistryBasedApi[
        RiskDatasetSettings, RiskDatasetSettingsMenu, AsyncRiskDatasetApi
    ],
):

    @abc.abstractmethod
    async def get_default_dataset_name(self) -> str: ...  # noqa: D102

    @abc.abstractmethod
    async def get_dataset_names(  # noqa: D102
        self,
        *,
        mode: Literal["System", "User", "All"] = "All",
        status: Literal["ready", "available"] = "ready",
    ) -> list[str]: ...

    @abc.abstractmethod
    async def list_riskdatasets(self) -> list[RiskDatasetMetadata]: ...  # noqa: D102

    async def create_or_replace_dataset(  # noqa: D102
        self, name: str, settings: RiskDatasetSettings
    ) -> AsyncRiskDatasetApi:
        await self.delete_dataset_if_exists(name)
        return await self.create_dataset(name, settings)

    @abc.abstractmethod
    async def create_dataset(  # noqa: D102
        self, name: str, settings: RiskDatasetSettings
    ) -> AsyncRiskDatasetApi: ...

    @abc.abstractmethod
    async def create_dataset_as_task(  # noqa: D102
        self, name: str, settings: RiskDatasetSettings
    ) -> AsyncTask[AsyncRiskDatasetApi]: ...

    @abc.abstractmethod
    async def delete_dataset(self, name: str) -> RawSettings: ...  # noqa: D102

    async def delete_dataset_if_exists(  # noqa: D102
        self, name: str
    ) -> RawSettings | None:
        if name in await self.settings.names(mode="All"):
            return await self.delete_dataset(name)
        return None
