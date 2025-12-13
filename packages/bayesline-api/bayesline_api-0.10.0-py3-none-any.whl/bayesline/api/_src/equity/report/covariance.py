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


class FactorCovarianceReportSettings(ReportSettings):
    """Settings for a exposure report."""

    factor_model_settings: FactorRiskModelSettings = Field()
    lambda_ewma: float = Field()


class FactorCovarianceReportAccessor(TypedReportAccessorApi):
    """Specific accessor for a exposure report."""

    @abc.abstractmethod
    def get_covariance(self) -> pl.DataFrame:
        """
        Get the time-series of factor covariances for the factors.

        Returns
        -------
        pl.DataFrame
            A dataframe with a `date` and `factor` columns and columns for each factor
            with their respective factor covariances.
        """

    @abc.abstractmethod
    def get_correlation(self) -> pl.DataFrame:
        """
        Get the time-series of factor correlations for the factors.

        Returns
        -------
        pl.DataFrame
            A dataframe with a `date` and `factor` columns and columns for each factor
            with their respective factor correlations.
        """


@docstrings_from_sync
class AsyncFactorCovarianceReportAccessor(AsyncTypedReportAccessorApi):

    @abc.abstractmethod
    async def get_covariance(self) -> pl.DataFrame: ...  # noqa: D102

    @abc.abstractmethod
    async def get_correlation(self) -> pl.DataFrame: ...  # noqa: D102


class FactorCovarianceReportApi(
    ReportApi[
        [DateLike, DateLike],
        FactorCovarianceReportAccessor,
        FactorCovarianceReportSettings,
    ]
):
    """API for a exposure report."""

    @abc.abstractmethod
    def calculate(
        self, start_date: DateLike, end_date: DateLike
    ) -> FactorCovarianceReportAccessor:
        """
        Calculate the factor covariance report.

        Parameters
        ----------
        start_date: DateLike
            The start date of the report.
        end_date: DateLike
            The end date of the report.

        Returns
        -------
        FactorCovarianceReportAccessor
            The exposure report accessor.
        """


@docstrings_from_sync
class AsyncFactorCovarianceReportApi(
    AsyncReportApi[
        [DateLike, DateLike],
        AsyncFactorCovarianceReportAccessor,
        FactorCovarianceReportSettings,
    ]
):

    @abc.abstractmethod
    async def calculate(  # noqa: D102
        self, start_date: DateLike, end_date: DateLike
    ) -> AsyncFactorCovarianceReportAccessor: ...


class FactorCovarianceReportAccessorImpl(FactorCovarianceReportAccessor):  # noqa: D101

    def __init__(self, accessor: ReportAccessorApi):
        self._accessor = accessor

    @property
    def accessor(self) -> ReportAccessorApi:  # noqa: D102
        return self._accessor

    def get_covariance(self) -> pl.DataFrame:  # noqa: D102
        df = self.accessor.get_data(
            [],
            expand=("date", "factor"),
            value_cols=("correlation",),
            pivot_cols=("factor_col",),
        )
        return df.rename(lambda x: x.removesuffix("^covariance"))

    def get_correlation(self) -> pl.DataFrame:  # noqa: D102
        df = self.accessor.get_data(
            [],
            expand=("date", "factor"),
            value_cols=("correlation",),
            pivot_cols=("factor_col",),
        )
        return df.rename(lambda x: x.removesuffix("^correlation"))


class AsyncFactorCovarianceReportAccessorImpl(  # noqa: D101
    AsyncFactorCovarianceReportAccessor
):

    def __init__(self, accessor: AsyncReportAccessorApi):
        self._accessor = accessor

    @property
    def accessor(self) -> AsyncReportAccessorApi:  # noqa: D102
        return self._accessor

    async def get_covariance(self) -> pl.DataFrame:  # noqa: D102
        df = await self.accessor.get_data(
            [],
            expand=("date", "factor"),
            value_cols=("correlation",),
            pivot_cols=("factor_col",),
        )
        return df.rename(lambda x: x.removesuffix("^covariance"))

    async def get_correlation(self) -> pl.DataFrame:  # noqa: D102
        df = await self.accessor.get_data(
            [],
            expand=("date", "factor"),
            value_cols=("correlation",),
            pivot_cols=("factor_col",),
        )
        return df.rename(lambda x: x.removesuffix("^correlation"))
