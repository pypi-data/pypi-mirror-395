import abc
import datetime as dt
from typing import Literal

import polars as pl

from bayesline.api._src._utils import docstrings_from_sync
from bayesline.api._src.equity.universe_settings import (
    UniverseSettings,
    UniverseSettingsMenu,
)
from bayesline.api._src.registry import AsyncRegistryBasedApi, RegistryBasedApi
from bayesline.api._src.tasks import AsyncTask, Task
from bayesline.api._src.types import DateLike, IdType


class UniverseApi(abc.ABC):
    """Provide access to universe data and operations.

    A universe represents a filtered set of assets with specific properties.
    """

    @property
    @abc.abstractmethod
    def settings(self) -> UniverseSettings:
        """Get the settings used to create this universe.

        Returns
        -------
        UniverseSettings
            The settings used to create this universe.
        """
        ...

    @property
    @abc.abstractmethod
    def id_types(self) -> list[IdType]:
        """Get the supported ID types for this universe.

        Returns
        -------
        list[IdType]
            Supported ID types for this universe.
        """
        ...

    @abc.abstractmethod
    def coverage(self, id_type: IdType | None = None) -> list[str]:
        """Get the list of all asset IDs this universe covers.

        Parameters
        ----------
        id_type : IdType | None, default=None
            The ID type to return asset IDs in, e.g. `ticker`.

        Raises
        ------
        ValueError
            If the given ID type is not supported.

        Returns
        -------
        list[str]
            List of all asset IDs this universe covers, in the given ID type.
        """
        ...

    @abc.abstractmethod
    def coverage_as_task(  # noqa: D102
        self, id_type: IdType | None = None
    ) -> Task[list[str]]: ...

    @abc.abstractmethod
    def dates(
        self, *, range_only: bool = False, trade_only: bool = False
    ) -> list[dt.date]:
        """Get the list of all dates this universe covers.

        Parameters
        ----------
        range_only : bool, default=False
            If True, returns the first and last date only.
        trade_only : bool, default=False
            If True, filter down the dates to trade dates only.

        Returns
        -------
        list[dt.date]
            List of all dates this universe covers.
        """

    @abc.abstractmethod
    def counts(
        self,
        dates: bool = True,
        categorical_hierarchy_levels: dict[str, int] | None = None,
        id_type: IdType | None = None,
        labels: bool = True,
    ) -> pl.DataFrame:
        """Get universe counts with optional grouping and aggregation.

        Parameters
        ----------
        dates : bool, default=True
            If True, groups by dates.
        categorical_hierarchy_levels : dict[str, int] | None, default=None
            The level of categorical aggregation to group by.
            The key is the hierarchy name, the value is the level.
            If None, no categorical aggregation is done. A level of -1 means
            to use all levels.
        id_type : IdType | None, default=None
            The ID type to calculate the daily stats for, e.g. `ticker`,
            which is relevant as the coverage may differ by ID type.
            The given ID type must be supported, i.e. in `id_types`.
        labels : bool, default=True
            If True, return labels for the counts, otherwise use the codes.

        Returns
        -------
        pl.DataFrame
            Universe counts.
            If grouped by dates then the count will be given.
            If not grouped by dates then the mean/min/max across
            all dates will be given.
        """
        ...

    @abc.abstractmethod
    def counts_as_task(  # noqa: D102
        self,
        dates: bool = True,
        categorical_hierarchy_levels: dict[str, int] | None = None,
        id_type: IdType | None = None,
        labels: bool = True,
    ) -> Task[pl.DataFrame]: ...

    @abc.abstractmethod
    def input_id_mapping(
        self,
        *,
        id_type: IdType | None = None,
        filter_mode: Literal["all", "mapped", "unmapped"] = "all",
        mode: Literal[
            "all", "daily-counts", "input-asset-counts", "latest-name"
        ] = "all",
    ) -> pl.DataFrame:
        """Get input ID mappings with various filtering and output modes.

        Parameters
        ----------
        id_type : IdType | None, default=None
            The ID type to return asset IDs in, e.g. `ticker`, or the default
            ID type of the universe if `None`.
        filter_mode : Literal["all", "mapped", "unmapped"], default="all"
            If `mapped` will only consider assets that could be mapped.
            If `unmapped` will only consider assets that could not be mapped.
        mode : Literal["all", "daily-counts", "input-asset-counts", "latest-name"], default="all"  # noqa: B950
            If `all`, returns all dated mappings.
            If `daily-counts`, returns the daily counts of mapped assets.
            If `input-asset-counts`, returns the total counts of input assets.
            If `latest-name`, returns the latest name of mapped assets.

        Returns
        -------
        pl.DataFrame
            If mode is `all`, a DataFrame with `date`, `input_asset_id`,
            `input_asset_id_type`, `output_asset_id`, `output_asset_id_type` and
            `name` columns.
            It contains the original input ID space and the mapped IDs.
            The mapped IDs will be `None` if for the given date and input ID the
            asset cannot be mapped.
            If mode is `daily-counts`, a DataFrame with `date` and `count`
            columns.
            If mode is `input-asset-counts`, a DataFrame with `input_asset_id` and `count`
            columns.
            If mode is `latest-name`, a DataFrame with `asset_id` and `name` columns.
        """
        ...

    @abc.abstractmethod
    def get(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        filter_tradedays: bool = False,
    ) -> pl.DataFrame:
        """Get universe data for a specific date range.

        Parameters
        ----------
        start : DateLike | None, default=None
            The start date of the universe to return, inclusive.
        end : DateLike | None, default=None
            The end date of the data to return, inclusive.
        id_type : IdType | None, default=None
            The ID type to return asset IDs in, e.g. `ticker`.
            The given ID type must be supported, i.e. in `id_types`.
        filter_tradedays : bool, default=False
            If True, filter down the data to trade dates only.

        Raises
        ------
        ValueError
            If the given ID type is not supported or date range is invalid.

        Returns
        -------
        pl.DataFrame
            The data for the given date range.
        """
        ...

    @abc.abstractmethod
    def get_as_task(  # noqa: D102
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        filter_tradedays: bool = False,
    ) -> Task[pl.DataFrame]: ...


@docstrings_from_sync
class AsyncUniverseApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> UniverseSettings: ...  # noqa: D102

    @property
    @abc.abstractmethod
    def id_types(self) -> list[IdType]: ...  # noqa: D102

    @abc.abstractmethod
    async def coverage(  # noqa: D102
        self, id_type: IdType | None = None
    ) -> list[str]: ...

    @abc.abstractmethod
    async def coverage_as_task(  # noqa: D102
        self, id_type: IdType | None = None
    ) -> AsyncTask[list[str]]: ...

    @abc.abstractmethod
    async def dates(  # noqa: D102
        self, *, range_only: bool = False, trade_only: bool = False
    ) -> list[dt.date]: ...

    @abc.abstractmethod
    async def counts(  # noqa: D102
        self,
        dates: bool = True,
        categorical_hierarchy_levels: dict[str, int] | None = None,
        id_type: IdType | None = None,
        labels: bool = True,
    ) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def counts_as_task(  # noqa: D102
        self,
        dates: bool = True,
        categorical_hierarchy_levels: dict[str, int] | None = None,
        id_type: IdType | None = None,
        labels: bool = True,
    ) -> AsyncTask[pl.DataFrame]: ...

    @abc.abstractmethod
    async def input_id_mapping(  # noqa: D102
        self,
        *,
        id_type: IdType | None = None,
        filter_mode: Literal["all", "mapped", "unmapped"] = "all",
        mode: Literal[
            "all", "daily-counts", "input-asset-counts", "latest-name"
        ] = "all",
    ) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def get(  # noqa: D102
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        filter_tradedays: bool = False,
    ) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def get_as_task(  # noqa: D102
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        filter_tradedays: bool = False,
    ) -> AsyncTask[pl.DataFrame]: ...


class UniverseLoaderApi(
    RegistryBasedApi[UniverseSettings, UniverseSettingsMenu, UniverseApi],
):
    """Provide access to universe loaders through the registry system.

    This class allows loading universe APIs based on settings and available options.
    """


@docstrings_from_sync
class AsyncUniverseLoaderApi(
    AsyncRegistryBasedApi[UniverseSettings, UniverseSettingsMenu, AsyncUniverseApi],
): ...
