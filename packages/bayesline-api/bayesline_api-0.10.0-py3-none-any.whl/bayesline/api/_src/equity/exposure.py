import abc
import datetime as dt
from typing import Literal

import polars as pl

from bayesline.api._src._utils import docstrings_from_sync
from bayesline.api._src.equity.exposure_settings import (
    ExposureSettings,
    ExposureSettingsMenu,
)
from bayesline.api._src.equity.universe import AsyncUniverseApi, UniverseApi
from bayesline.api._src.equity.universe_settings import UniverseSettings
from bayesline.api._src.registry import AsyncRegistryBasedApi, RegistryBasedApi
from bayesline.api._src.tasks import AsyncTask, Task
from bayesline.api._src.types import DateLike, IdType


class ExposureApi(abc.ABC):
    """Abstract base class for exposure API operations."""

    @property
    @abc.abstractmethod
    def settings(self) -> ExposureSettings:
        """
        Get the settings used to create these exposures.

        Returns
        -------
        ExposureSettings
            The settings used to create these exposures.
        """
        ...

    @abc.abstractmethod
    def dates(
        self,
        universe: str | int | UniverseSettings | UniverseApi,
        *,
        range_only: bool = False,
    ) -> list[dt.date]:
        """
        Get the dates covered by the exposure data.

        Parameters
        ----------
        universe : str | int | UniverseSettings | UniverseApi
            The universe to use for the exposure calculation.
        range_only : bool, default=False
            If True, returns the first and last date only.

        Returns
        -------
        list[dt.date]
            List of all covered dates.
        """

    @abc.abstractmethod
    def coverage_stats(
        self,
        universe: str | int | UniverseSettings | UniverseApi,
        *,
        id_type: IdType | None = None,
        by: Literal["date", "asset"] = "date",
    ) -> pl.DataFrame:
        """
        Get coverage statistics for the exposure data.

        Parameters
        ----------
        universe : str | int | UniverseSettings | UniverseApi
            The universe to use for the exposure calculation.
        id_type : IdType | None, default=None
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.
        by : Literal["date", "asset"], default="date"
            The aggregation, either by date or by asset.

        Returns
        -------
        pl.DataFrame
            A dataframe with date as the first column, where the remaining columns
            names are the styles and substyles (concatenated with a dot). The values
            are the counts of the underlying data before it was imputed.
        """

    @abc.abstractmethod
    def coverage_stats_as_task(
        self,
        universe: str | int | UniverseSettings | UniverseApi,
        *,
        id_type: IdType | None = None,
        by: Literal["date", "asset"] = "date",
    ) -> Task[pl.DataFrame]:
        """
        Get coverage statistics as a task.

        Parameters
        ----------
        universe : str | int | UniverseSettings | UniverseApi
            The universe to use for the exposure calculation.
        id_type : IdType | None, default=None
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.
        by : Literal["date", "asset"], default="date"
            The aggregation, either by date or by asset.

        Returns
        -------
        Task[pl.DataFrame]
            A task that returns coverage statistics.
        """
        ...

    @abc.abstractmethod
    def get(
        self,
        universe: str | int | UniverseSettings | UniverseApi,
        *,
        standardize_universe: str | int | UniverseSettings | UniverseApi | None,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        filter_tradedays: bool = False,
    ) -> pl.DataFrame:
        """
        Get exposure data for the specified universe and date range.

        Parameters
        ----------
        universe : str | int | UniverseSettings | UniverseApi
            The universe to use for the exposure calculation.
        standardize_universe : str | int | UniverseSettings | UniverseApi | None
            The universe to use for the standardization of the exposure data. If None,
            the standardization is uses the entire universe.
        start : DateLike | None, default=None
            The start date of the universe to return, inclusive.
        end : DateLike | None, default=None
            The end date of the data to return, inclusive.
        id_type : IdType | None, default=None
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.
        filter_tradedays : bool, default=False
            If True, only returns data for tradedays.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pl.DataFrame
            The data for the given date range with a where the date is the first column
            and the asset id is the second column. The remaining columns are the
            individual styles.
        """
        ...

    @abc.abstractmethod
    def get_as_task(
        self,
        universe: str | int | UniverseSettings | UniverseApi,
        *,
        standardize_universe: str | int | UniverseSettings | UniverseApi | None,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        filter_tradedays: bool = False,
    ) -> Task[pl.DataFrame]:
        """
        Get exposure data as a task.

        Parameters
        ----------
        universe : str | int | UniverseSettings | UniverseApi
            The universe to use for the exposure calculation.
        standardize_universe : str | int | UniverseSettings | UniverseApi | None
            The universe to use for the standardization of the exposure data. If None,
            the standardization is uses the entire universe.
        start : DateLike | None, default=None
            The start date of the universe to return, inclusive.
        end : DateLike | None, default=None
            The end date of the data to return, inclusive.
        id_type : IdType | None, default=None
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.
        filter_tradedays : bool, default=False
            If True, only returns data for tradedays.

        Returns
        -------
        Task[pl.DataFrame]
            A task that returns exposure data.
        """
        ...


@docstrings_from_sync
class AsyncExposureApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> ExposureSettings: ...  # noqa: D102

    @abc.abstractmethod
    async def dates(  # noqa: D102
        self,
        universe: str | int | UniverseSettings | AsyncUniverseApi,
        *,
        range_only: bool = False,
    ) -> list[dt.date]: ...

    @abc.abstractmethod
    async def coverage_stats(  # noqa: D102
        self,
        universe: str | int | UniverseSettings | AsyncUniverseApi,
        *,
        id_type: IdType | None = None,
        by: Literal["date", "asset"] = "date",
    ) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def coverage_stats_as_task(  # noqa: D102
        self,
        universe: str | int | UniverseSettings | AsyncUniverseApi,
        *,
        id_type: IdType | None = None,
        by: Literal["date", "asset"] = "date",
    ) -> AsyncTask[pl.DataFrame]: ...

    @abc.abstractmethod
    async def get(  # noqa: D102
        self,
        universe: str | int | UniverseSettings | AsyncUniverseApi,
        *,
        standardize_universe: str | int | UniverseSettings | AsyncUniverseApi | None,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        filter_tradedays: bool = False,
    ) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def get_as_task(  # noqa: D102
        self,
        universe: str | int | UniverseSettings | AsyncUniverseApi,
        *,
        standardize_universe: str | int | UniverseSettings | AsyncUniverseApi | None,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        filter_tradedays: bool = False,
    ) -> AsyncTask[pl.DataFrame]: ...


class ExposureLoaderApi(
    RegistryBasedApi[ExposureSettings, ExposureSettingsMenu, ExposureApi],
):
    """Registry-based API for loading exposure data."""

    ...


@docstrings_from_sync
class AsyncExposureLoaderApi(
    AsyncRegistryBasedApi[ExposureSettings, ExposureSettingsMenu, AsyncExposureApi],
): ...
