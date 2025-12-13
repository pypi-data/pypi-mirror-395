import abc
import datetime as dt
from typing import Literal

import polars as pl

from bayesline.api._src._utils import docstrings_from_sync
from bayesline.api._src.equity.portfolio_settings import (
    PortfolioOrganizerSettings,
    PortfolioOrganizerSettingsMenu,
    PortfolioSettings,
    PortfolioSettingsMenu,
)
from bayesline.api._src.equity.upload import (
    AsyncDataTypeUploaderApi,
    DataTypeUploaderApi,
)
from bayesline.api._src.registry import (
    AsyncRegistryBasedApi,
    AsyncSettingsRegistry,
    RegistryBasedApi,
    SettingsRegistry,
)
from bayesline.api._src.tasks import AsyncTask, Task
from bayesline.api._src.types import DateLike, IdType


class PortfolioApi(abc.ABC):
    """Abstract base class for portfolio APIs.

    This class defines the interface for portfolio APIs that provide
    access to portfolio data and metadata.
    """

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Get the name of the portfolio.

        Returns
        -------
        str
            The name of the portfolio.
        """
        ...

    @abc.abstractmethod
    def get_id_types(self) -> dict[str, list[IdType]]:
        """Get the available ID types for each portfolio.

        Returns
        -------
        dict[str, list[IdType]]
            The available ID types that at least a portion of assets can be mapped
            to for each portfolio.
        """

    @abc.abstractmethod
    def get_coverage(
        self,
        names: str | list[str] | None = None,
        *,
        by: Literal["date", "asset"] = "date",
        metric: Literal["count", "holding"] = "count",
        stats: list[str] | None = None,
    ) -> pl.DataFrame:
        """Get coverage information for portfolios.

        Parameters
        ----------
        names : str | list[str] | None, default=None
            The names of the portfolios. If not given all portfolios will be calculated.
        by : Literal["date", "asset"], default="date"
            The coverage aggregation, either by date or by asset.
        metric : Literal["count", "holding"], default="count"
            The metric to calculate, either count of observations
            or sum of holding values.
        stats : list[str] | None, default=None
            List of 'min', 'max', 'mean', collapses `by` into these stats.

        Returns
        -------
        pl.DataFrame
            The dated coverage count for each id type. `portfolio_group` and
            `portfolio` are the first two columns. If `stats` given, collapses the `by`
            index to the given aggregations.
        """

    @abc.abstractmethod
    def get_coverage_as_task(  # noqa: D102
        self,
        names: str | list[str] | None = None,
        *,
        by: Literal["date", "asset"] = "date",
        metric: Literal["count", "holding"] = "count",
        stats: list[str] | None = None,
    ) -> Task[pl.DataFrame]: ...

    @abc.abstractmethod
    def get_portfolio_names(self) -> list[str]:
        """Get the list of portfolio names.

        Returns
        -------
        list[str]
            The list of portfolio names.
        """
        ...

    @abc.abstractmethod
    def get_portfolio_groups(self) -> dict[str, list[str]]:
        """Get the portfolio groups.

        Returns
        -------
        dict[str, list[str]]
            A dictionary mapping group names to lists of portfolio names.
        """
        ...

    @abc.abstractmethod
    def get_dates(
        self, names: list[str] | str | None = None, *, collapse: bool = False
    ) -> dict[str, list[dt.date]]:
        """Get the available dates for portfolios.

        Parameters
        ----------
        names : list[str] | str | None, default=None
            The portfolio names to get dates for.
        collapse : bool, default=False
            Whether to collapse the results.

        Returns
        -------
        dict[str, list[dt.date]]
            A dictionary mapping portfolio names to lists of available dates.
        """
        ...

    @abc.abstractmethod
    def get_portfolio(
        self,
        names: list[str] | str,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        """Get portfolios for the given names between given start and end dates.

        Parameters
        ----------
        names : list[str] | str
            The list of portfolio names.
        start_date : DateLike | None, default=None
            The start date of the data to return, inclusive.
        end_date : DateLike | None, default=None
            The end date of the data to return, inclusive.
        id_type : IdType | None, default=None
            ID type to return the portfolio holdings in.

        Returns
        -------
        pl.DataFrame
            A dataframe with columns `portfolio_group`, `portfolio`, `date`,
            `input_asset_id`, `input_asset_id_type`, `asset_id`, `asset_id_type` and
            `value`.

            If no `id_type` is given then the input ID space will be used unmapped. In
            this case the columns `asset_id`, `asset_id_type` will not be returned.
        """

    @abc.abstractmethod
    def get_portfolio_as_task(  # noqa: D102
        self,
        names: list[str] | str,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> Task[pl.DataFrame]: ...


@docstrings_from_sync
class AsyncPortfolioApi(abc.ABC):

    @property
    @abc.abstractmethod
    def name(self) -> str: ...  # noqa: D102

    @abc.abstractmethod
    async def get_id_types(self) -> dict[str, list[IdType]]: ...  # noqa: D102

    @abc.abstractmethod
    async def get_coverage(  # noqa: D102
        self,
        names: str | list[str] | None = None,
        *,
        by: Literal["date", "asset"] = "date",
        metric: Literal["count", "holding"] = "count",
        stats: list[str] | None = None,
    ) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def get_coverage_as_task(  # noqa: D102
        self,
        names: str | list[str] | None = None,
        *,
        by: Literal["date", "asset"] = "date",
        metric: Literal["count", "holding"] = "count",
        stats: list[str] | None = None,
    ) -> AsyncTask[pl.DataFrame]: ...

    @abc.abstractmethod
    async def get_portfolio_names(self) -> list[str]: ...  # noqa: D102

    @abc.abstractmethod
    async def get_portfolio_groups(self) -> dict[str, list[str]]: ...  # noqa: D102

    @abc.abstractmethod
    async def get_dates(  # noqa: D102
        self, names: list[str] | str | None = None, *, collapse: bool = False
    ) -> dict[str, list[dt.date]]: ...

    @abc.abstractmethod
    async def get_portfolio(  # noqa: D102
        self,
        names: list[str] | str,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def get_portfolio_as_task(  # noqa: D102
        self,
        names: list[str] | str,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> AsyncTask[pl.DataFrame]: ...


class PortfolioLoaderApi(
    RegistryBasedApi[
        PortfolioSettings,
        PortfolioSettingsMenu,
        PortfolioApi,
    ]
):
    """API for loading portfolios.

    This class provides functionality for loading portfolios using
    registry-based API patterns.
    """

    @property
    @abc.abstractmethod
    def uploader(self) -> DataTypeUploaderApi:
        """Get the data type uploader API.

        Returns
        -------
        DataTypeUploaderApi
            The data type uploader API.
        """
        ...

    @property
    @abc.abstractmethod
    def organizer_settings(
        self,
    ) -> SettingsRegistry[PortfolioOrganizerSettings, PortfolioOrganizerSettingsMenu]:
        """Get the organizer settings registry.

        Returns
        -------
        SettingsRegistry[PortfolioOrganizerSettings, PortfolioOrganizerSettingsMenu]
            The organizer settings registry.
        """
        ...


@docstrings_from_sync
class AsyncPortfolioLoaderApi(
    AsyncRegistryBasedApi[
        PortfolioSettings,
        PortfolioSettingsMenu,
        AsyncPortfolioApi,
    ]
):
    @property
    @abc.abstractmethod
    def uploader(self) -> AsyncDataTypeUploaderApi: ...  # noqa: D102

    @property
    @abc.abstractmethod
    def organizer_settings(  # noqa: D102
        self,
    ) -> AsyncSettingsRegistry[
        PortfolioOrganizerSettings, PortfolioOrganizerSettingsMenu
    ]: ...
