import abc
from typing import overload

from bayesline.api._src._utils import docstrings_from_sync
from bayesline.api._src.equity.report.accessor import TypedReportAccessorApi
from bayesline.api._src.equity.report.api import (
    AsyncReportApi,
    AsyncTypedReportAccessorApi,
    ReportApi,
    S,
)
from bayesline.api._src.equity.report.exposure import (
    AsyncExposureReportApi,
    ExposureReportApi,
    ExposureReportSettings,
)
from bayesline.api._src.equity.report.factor_stats import (
    AsyncFactorStatsReportApi,
    FactorStatsReportApi,
    FactorStatsReportSettings,
)
from bayesline.api._src.equity.report.universe import (
    AsyncUniverseCountReportApi,
    UniverseCountReportApi,
    UniverseCountReportSettings,
)


class ReportLoaderApi(abc.ABC):
    """The main interface for loading different types of reports."""

    @overload
    def load(self, settings: UniverseCountReportSettings) -> UniverseCountReportApi: ...

    @overload
    def load(self, settings: ExposureReportSettings) -> ExposureReportApi: ...

    @overload
    def load(self, settings: FactorStatsReportSettings) -> FactorStatsReportApi: ...

    @abc.abstractmethod
    def load(self, settings: S) -> ReportApi[..., TypedReportAccessorApi, S]:
        """
        Load a report using the specified settings.

        Parameters
        ----------
        settings: S
            The settings to use to load the report.

        Returns
        -------
        ReportApi[..., TypedReportAccessorApi, S]
            The loaded report API.
        """


@docstrings_from_sync
class AsyncReportLoaderApi(abc.ABC):

    @overload
    async def load(  # noqa: D102
        self, settings: UniverseCountReportSettings
    ) -> AsyncUniverseCountReportApi: ...

    @overload
    async def load(  # noqa: D102
        self, settings: ExposureReportSettings
    ) -> AsyncExposureReportApi: ...

    @overload
    async def load(  # noqa: D102
        self, settings: FactorStatsReportSettings
    ) -> AsyncFactorStatsReportApi: ...

    @abc.abstractmethod
    async def load(  # noqa: D102
        self, settings: S
    ) -> AsyncReportApi[..., AsyncTypedReportAccessorApi, S]: ...
