import abc

import polars as pl
from pydantic import Field

from bayesline.api._src._utils import docstrings_from_sync
from bayesline.api._src.equity.portfolioreport import (
    AsyncReportAccessorApi,
    ReportAccessorApi,
)
from bayesline.api._src.equity.report.accessor import (
    AsyncTypedReportAccessorApi,
    TypedReportAccessorApi,
)
from bayesline.api._src.equity.report.api import AsyncReportApi, ReportApi
from bayesline.api._src.equity.report.settings import ReportSettings
from bayesline.api._src.equity.universe_settings import UniverseSettings
from bayesline.api._src.types import DateLike, IdType


class UniverseCountReportSettings(ReportSettings):
    """Settings for a universe count report."""

    universe_settings: UniverseSettings = Field()
    filter_trade_days: bool = Field(
        default=True, description="Whether to filter trade days"
    )


class UniverseCountReportAccessor(TypedReportAccessorApi):
    """Specific accessor for a universe count report."""

    @abc.abstractmethod
    def get_counts(self) -> pl.DataFrame:
        """
        Get the counts for the universe.

        Returns
        -------
        pl.DataFrame
            A dataframe with `[date, count]` columns.
        """


@docstrings_from_sync
class AsyncUniverseCountReportAccessor(AsyncTypedReportAccessorApi):

    @abc.abstractmethod
    async def get_counts(self) -> pl.DataFrame: ...  # noqa: D102


class UniverseCountReportApi(
    ReportApi[
        [DateLike, DateLike], UniverseCountReportAccessor, UniverseCountReportSettings
    ]
):
    """API for a universe count report."""

    @abc.abstractmethod
    def calculate(
        self, start_date: DateLike, end_date: DateLike
    ) -> UniverseCountReportAccessor:
        """
        Calculate the universe count report.

        Parameters
        ----------
        start_date: DateLike
            The start date of the report.
        end_date: DateLike
            The end date of the report.

        Returns
        -------
        UniverseCountReportAccessor
            The universe count report accessor.
        """


@docstrings_from_sync
class AsyncUniverseCountReportApi(
    AsyncReportApi[
        [DateLike, DateLike],
        AsyncUniverseCountReportAccessor,
        UniverseCountReportSettings,
    ]
):

    @abc.abstractmethod
    async def calculate(  # noqa: D102
        self, start_date: DateLike, end_date: DateLike
    ) -> AsyncUniverseCountReportAccessor: ...


class UniverseCountReportAccessorImpl(UniverseCountReportAccessor):  # noqa: D101

    def __init__(self, accessor: ReportAccessorApi):
        self._accessor = accessor

    @property
    def accessor(self) -> ReportAccessorApi:  # noqa: D102
        return self._accessor

    def get_counts(self) -> pl.DataFrame:  # noqa: D102
        return self.accessor.get_data(
            [], expand=("date",), value_cols=("count_est", "count_cov")
        )


class AsyncUniverseCountReportAccessorImpl(  # noqa: D101
    AsyncUniverseCountReportAccessor
):

    def __init__(self, accessor: AsyncReportAccessorApi):
        self._accessor = accessor

    @property
    def accessor(self) -> AsyncReportAccessorApi:  # noqa: D102
        return self._accessor

    async def get_counts(self) -> pl.DataFrame:  # noqa: D102
        return await self.accessor.get_data(
            [], expand=("date",), value_cols=("count_est", "count_cov")
        )

    async def get_counts_old(  # noqa: D102
        self,
        dates: bool = True,
        categorical_hierarchy_levels: dict[str, int] | None = None,
        id_type: IdType | None = None,
        labels: bool = True,
    ) -> pl.DataFrame:
        # TODO: remove this method
        if not dates:
            raise NotImplementedError("Not implemented")
        if categorical_hierarchy_levels:
            raise NotImplementedError("Not implemented")
        if id_type:
            raise NotImplementedError("Not implemented")
        if not labels:
            raise NotImplementedError("Not implemented")
        df = await self.accessor.get_data(
            [], expand=("date",), value_cols=("count_est", "count_cov")
        )
        return df.unpivot(
            index="date", variable_name="estimation_universe", value_name="count"
        ).select(
            pl.col("estimation_universe") == "count_est",
            "date",
            pl.col("count").cast(pl.UInt32),
        )
