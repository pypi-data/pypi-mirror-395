import abc

import polars as pl
from pydantic import Field

from bayesline.api._src._utils import docstrings_from_sync
from bayesline.api._src.equity.exposure_settings import ExposureSettings
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
from bayesline.api._src.types import DateLike


class ExposureReportSettings(ReportSettings):
    """Settings for a exposure report."""

    universe_settings: UniverseSettings = Field()
    exposure_settings: ExposureSettings = Field()
    filter_trade_days: bool = Field(
        default=True, description="Whether to filter trade days"
    )


class ExposureReportAccessor(TypedReportAccessorApi):
    """Specific accessor for a exposure report."""

    @abc.abstractmethod
    def get(self) -> pl.DataFrame:
        """
        Get the exposures for the report.

        Returns
        -------
        pl.DataFrame
            The exposures for the report, with a date column and all factors as columns.
            The factor column names are of the form `factor_group^factor`.
        """


@docstrings_from_sync
class AsyncExposureReportAccessor(AsyncTypedReportAccessorApi):

    @abc.abstractmethod
    async def get(self) -> pl.DataFrame: ...  # noqa: D102


class ExposureReportApi(
    ReportApi[[DateLike, DateLike], ExposureReportAccessor, ExposureReportSettings]
):
    """API for a exposure report."""

    @abc.abstractmethod
    def calculate(
        self, start_date: DateLike, end_date: DateLike
    ) -> ExposureReportAccessor:
        """
        Calculate the exposure report.

        Parameters
        ----------
        start_date: DateLike
            The start date of the report.
        end_date: DateLike
            The end date of the report.

        Returns
        -------
        ExposureReportAccessor
            The exposure report accessor.
        """


@docstrings_from_sync
class AsyncExposureReportApi(
    AsyncReportApi[
        [DateLike, DateLike],
        AsyncExposureReportAccessor,
        ExposureReportSettings,
    ]
):

    @abc.abstractmethod
    async def calculate(  # noqa: D102
        self, start_date: DateLike, end_date: DateLike
    ) -> AsyncExposureReportAccessor: ...


class ExposureReportAccessorImpl(ExposureReportAccessor):  # noqa: D101

    def __init__(self, accessor: ReportAccessorApi):
        self._accessor = accessor

    @property
    def accessor(self) -> ReportAccessorApi:  # noqa: D102
        return self._accessor

    def get(self) -> pl.DataFrame:  # noqa: D102
        df = self.accessor.get_data(
            [],
            expand=("date", "asset_id"),
            value_cols=("exposure",),
            pivot_cols=("factor_group", "factor"),
        )
        return df.rename(lambda x: x.removesuffix("^exposure"))


class AsyncExposureReportAccessorImpl(AsyncExposureReportAccessor):  # noqa: D101

    def __init__(self, accessor: AsyncReportAccessorApi):
        self._accessor = accessor

    @property
    def accessor(self) -> AsyncReportAccessorApi:  # noqa: D102
        return self._accessor

    async def get(self) -> pl.DataFrame:  # noqa: D102
        df = await self.accessor.get_data(
            [],
            expand=("date", "asset_id"),
            value_cols=("exposure",),
            pivot_cols=("factor_group", "factor"),
        )
        return df.rename(lambda x: x.removesuffix("^exposure"))
