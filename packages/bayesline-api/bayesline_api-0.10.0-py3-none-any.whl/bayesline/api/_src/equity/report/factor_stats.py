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
from bayesline.api._src.equity.riskmodels_settings import FactorRiskModelSettings
from bayesline.api._src.types import DateLike


class FactorStatsReportSettings(ReportSettings):
    """Settings for a exposure report."""

    factor_model_settings: FactorRiskModelSettings = Field()


class FactorStatsReportAccessor(TypedReportAccessorApi):
    """Specific accessor for a exposure report."""

    @abc.abstractmethod
    def get_factor_returns(self) -> pl.DataFrame:
        """
        Get the time-series of factor returns for the factors.

        Returns
        -------
        pl.DataFrame
            A dataframe with a `date` column and columns for each factor with their
            respective factor returns, in factor_group^factor format.
        """

    @abc.abstractmethod
    def get_t_stats(self) -> pl.DataFrame:
        """
        Get the time-series of t-statistics for the factors.

        Returns
        -------
        pl.DataFrame
            A dataframe with a `date` column and columns for each factor with their
            respective t-statistics, in factor_group^factor format.
        """

    @abc.abstractmethod
    def get_p_values(self) -> pl.DataFrame:
        """
        Get the time-series of p-values for the factors.

        Returns
        -------
        pl.DataFrame
            A dataframe with a `date` column and columns for each factor with their
            respective p-values, in factor_group^factor format.
        """


@docstrings_from_sync
class AsyncFactorStatsReportAccessor(AsyncTypedReportAccessorApi):

    @abc.abstractmethod
    async def get_factor_returns(self) -> pl.DataFrame: ...  # noqa: D102

    @abc.abstractmethod
    async def get_t_stats(self) -> pl.DataFrame: ...  # noqa: D102

    @abc.abstractmethod
    async def get_p_values(self) -> pl.DataFrame: ...  # noqa: D102


class FactorStatsReportApi(
    ReportApi[
        [DateLike, DateLike], FactorStatsReportAccessor, FactorStatsReportSettings
    ]
):
    """API for a exposure report."""

    @abc.abstractmethod
    def calculate(
        self, start_date: DateLike, end_date: DateLike
    ) -> FactorStatsReportAccessor:
        """
        Calculate the factor stats report.

        Parameters
        ----------
        start_date: DateLike
            The start date of the report.
        end_date: DateLike
            The end date of the report.

        Returns
        -------
        FactorStatsReportAccessor
            The exposure report accessor.
        """


@docstrings_from_sync
class AsyncFactorStatsReportApi(
    AsyncReportApi[
        [DateLike, DateLike],
        AsyncFactorStatsReportAccessor,
        FactorStatsReportSettings,
    ]
):

    @abc.abstractmethod
    async def calculate(  # noqa: D102
        self, start_date: DateLike, end_date: DateLike
    ) -> AsyncFactorStatsReportAccessor: ...


class FactorStatsReportAccessorImpl(FactorStatsReportAccessor):  # noqa: D101

    def __init__(self, accessor: ReportAccessorApi):
        self._accessor = accessor

    @property
    def accessor(self) -> ReportAccessorApi:  # noqa: D102
        return self._accessor

    def get_factor_returns(self) -> pl.DataFrame:  # noqa: D102
        df = self.accessor.get_data(
            [],
            expand=("date",),
            value_cols=("factor_return",),
            pivot_cols=("factor_group", "factor"),
        )
        return df.rename(lambda x: x.removesuffix("^factor_return"))

    def get_t_stats(self) -> pl.DataFrame:  # noqa: D102
        df = self.accessor.get_data(
            [],
            expand=("date",),
            value_cols=("t_statistic",),
            pivot_cols=("factor_group", "factor"),
        )
        return df.rename(lambda x: x.removesuffix("^t_statistic"))

    def get_p_values(self) -> pl.DataFrame:  # noqa: D102
        df = self.accessor.get_data(
            [],
            expand=("date",),
            value_cols=("p_value",),
            pivot_cols=("factor_group", "factor"),
        )
        return df.rename(lambda x: x.removesuffix("^p_value"))


class AsyncFactorStatsReportAccessorImpl(AsyncFactorStatsReportAccessor):  # noqa: D101

    def __init__(self, accessor: AsyncReportAccessorApi):
        self._accessor = accessor

    @property
    def accessor(self) -> AsyncReportAccessorApi:  # noqa: D102
        return self._accessor

    async def get_factor_returns(self) -> pl.DataFrame:  # noqa: D102
        df = await self.accessor.get_data(
            [],
            expand=("date",),
            value_cols=("factor_return",),
            pivot_cols=("factor_group", "factor"),
        )
        return df.rename(lambda x: x.removesuffix("^factor_return"))

    async def get_t_stats(self) -> pl.DataFrame:  # noqa: D102
        df = await self.accessor.get_data(
            [],
            expand=("date",),
            value_cols=("t_statistic",),
            pivot_cols=("factor_group", "factor"),
        )
        return df.rename(lambda x: x.removesuffix("^t_statistic"))

    async def get_p_values(self) -> pl.DataFrame:  # noqa: D102
        df = await self.accessor.get_data(
            [],
            expand=("date",),
            value_cols=("p_value",),
            pivot_cols=("factor_group", "factor"),
        )
        return df.rename(lambda x: x.removesuffix("^p_value"))
