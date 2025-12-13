import abc
import datetime as dt

import polars as pl

from bayesline.api._src._utils import docstrings_from_sync
from bayesline.api._src.equity.portfoliohierarchy_settings import (
    PortfolioHierarchySettings,
    PortfolioHierarchySettingsMenu,
)
from bayesline.api._src.registry import AsyncRegistryBasedApi, RegistryBasedApi
from bayesline.api._src.tasks import AsyncTask, Task
from bayesline.api._src.types import DateLike, IdType


class PortfolioHierarchyApi(abc.ABC):
    """Abstract base class for portfolio hierarchy APIs.

    This class defines the interface for portfolio hierarchy APIs that provide
    access to portfolio hierarchy data and metadata.
    """

    @property
    @abc.abstractmethod
    def settings(self) -> PortfolioHierarchySettings:
        """Get the settings used to create this hierarchy.

        Returns
        -------
        PortfolioHierarchySettings
            The settings used to create this hierarchy.
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
            If a portfolio has a benchmark then the available id types are those
            that are available for both the portfolio and the benchmark.
        """

    @abc.abstractmethod
    def get_dates(self, *, collapse: bool = False) -> dict[str, list[dt.date]]:
        """Get the available dates for each portfolio.

        Parameters
        ----------
        collapse : bool, default=False
            If True, will calculate aggregations `any` and `all`, indicating
            of for a given date, any (or all) portfolios have holdings.

        Returns
        -------
        dict[str, list[dt.date]]
            A dict of portfolio-id to dates for which this hierarchy can be produced.
            For a given portfolio and date, the hierarchy can be produced if the
            portfolio has holdings for that date. If a benchmark is given then this
            benchmark also must have holdings for the given date.
        """

    @abc.abstractmethod
    def get(
        self,
        start_date: DateLike | None,
        end_date: DateLike | None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        """Get portfolio hierarchy data for the specified date range.

        Parameters
        ----------
        start_date : DateLike | None
            The start date for the data.
        end_date : DateLike | None
            The end date for the data.
        id_type : IdType | None, default=None
            The ID type to use for the data.

        Returns
        -------
        pl.DataFrame
            The portfolio hierarchy data.
        """
        ...

    @abc.abstractmethod
    def get_as_task(  # noqa: D102
        self,
        start_date: DateLike | None,
        end_date: DateLike | None,
        id_type: IdType | None = None,
    ) -> Task[pl.DataFrame]: ...


@docstrings_from_sync
class AsyncPortfolioHierarchyApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> PortfolioHierarchySettings: ...  # noqa: D102

    @abc.abstractmethod
    async def get_id_types(self) -> dict[str, list[IdType]]: ...  # noqa: D102

    @abc.abstractmethod
    async def get_dates(  # noqa: D102
        self, *, collapse: bool = False
    ) -> dict[str, list[dt.date]]: ...

    @abc.abstractmethod
    async def get(  # noqa: D102
        self,
        start_date: DateLike | None,
        end_date: DateLike | None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def get_as_task(  # noqa: D102
        self,
        start_date: DateLike | None,
        end_date: DateLike | None,
        id_type: IdType | None = None,
    ) -> AsyncTask[pl.DataFrame]: ...


class PortfolioHierarchyLoaderApi(
    RegistryBasedApi[
        PortfolioHierarchySettings,
        PortfolioHierarchySettingsMenu,
        PortfolioHierarchyApi,
    ]
):
    """API for loading portfolio hierarchies.

    This class provides functionality for loading portfolio hierarchies using
    registry-based API patterns.
    """

    ...


@docstrings_from_sync
class AsyncPortfolioHierarchyLoaderApi(
    AsyncRegistryBasedApi[
        PortfolioHierarchySettings,
        PortfolioHierarchySettingsMenu,
        AsyncPortfolioHierarchyApi,
    ]
): ...
