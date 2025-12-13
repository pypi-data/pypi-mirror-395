import abc

from bayesline.api._src._utils import docstrings_from_sync
from bayesline.api._src.equity.calendar import AsyncCalendarLoaderApi, CalendarLoaderApi
from bayesline.api._src.equity.exposure import (
    AsyncExposureLoaderApi,
    ExposureLoaderApi,
)
from bayesline.api._src.equity.ids import (
    AssetIdApi,
    AsyncAssetIdApi,
)
from bayesline.api._src.equity.modelconstruction import (
    AsyncFactorModelConstructionLoaderApi,
    FactorModelConstructionLoaderApi,
)
from bayesline.api._src.equity.portfolio import (
    AsyncPortfolioLoaderApi,
    PortfolioLoaderApi,
)
from bayesline.api._src.equity.portfoliohierarchy import (
    AsyncPortfolioHierarchyLoaderApi,
    PortfolioHierarchyLoaderApi,
)
from bayesline.api._src.equity.portfolioreport import (
    AsyncReportLoaderApi,
    ReportLoaderApi,
)
from bayesline.api._src.equity.riskdataset import (
    AsyncRiskDatasetLoaderApi,
    RiskDatasetLoaderApi,
)
from bayesline.api._src.equity.riskmodels import (
    AsyncFactorModelLoaderApi,
    FactorModelLoaderApi,
)
from bayesline.api._src.equity.universe import (
    AsyncUniverseLoaderApi,
    UniverseLoaderApi,
)
from bayesline.api._src.equity.upload import AsyncUploadersApi, UploadersApi


class BayeslineEquityApi(abc.ABC):
    """Abstract base class for Bayesline equity API operations."""

    @property
    @abc.abstractmethod
    def riskdatasets(self) -> RiskDatasetLoaderApi:
        """
        Get the risk datasets API.

        Returns
        -------
        RiskDatasetLoaderApi
            The risk datasets API.
        """
        ...

    @property
    @abc.abstractmethod
    def uploaders(self) -> UploadersApi:
        """
        Get the uploaders API.

        Returns
        -------
        UploadersApi
            The uploaders API.
        """
        ...

    @property
    @abc.abstractmethod
    def ids(self) -> AssetIdApi:
        """
        Get the asset ID API.

        Returns
        -------
        AssetIdApi
            The asset ID API.
        """
        ...

    @property
    @abc.abstractmethod
    def calendars(self) -> CalendarLoaderApi:
        """
        Get the calendar API.

        Returns
        -------
        CalendarLoaderApi
            The calendar API.
        """
        ...

    @property
    @abc.abstractmethod
    def universes(self) -> UniverseLoaderApi:
        """
        Get the universe API.

        Returns
        -------
        UniverseLoaderApi
            The universe API.
        """
        ...

    @property
    @abc.abstractmethod
    def exposures(self) -> ExposureLoaderApi:
        """
        Get the exposure API.

        Returns
        -------
        ExposureLoaderApi
            The exposure API.
        """
        ...

    @property
    @abc.abstractmethod
    def modelconstruction(self) -> FactorModelConstructionLoaderApi:
        """
        Get the model construction API.

        Returns
        -------
        FactorModelConstructionLoaderApi
            The model construction API.
        """
        ...

    @property
    @abc.abstractmethod
    def riskmodels(self) -> FactorModelLoaderApi:
        """
        Get the risk models API.

        Returns
        -------
        FactorModelLoaderApi
            The risk models API.
        """
        ...

    @property
    @abc.abstractmethod
    def portfoliohierarchies(self) -> PortfolioHierarchyLoaderApi:
        """
        Get the portfolio hierarchy API.

        Returns
        -------
        PortfolioHierarchyLoaderApi
            The portfolio hierarchy API.
        """
        ...

    @property
    @abc.abstractmethod
    def portfolioreport(self) -> ReportLoaderApi:
        """
        Get the portfolio report API.

        Returns
        -------
        ReportLoaderApi
            The portfolio report API.
        """
        ...

    @property
    @abc.abstractmethod
    def portfolios(self) -> PortfolioLoaderApi:
        """
        Get the portfolio API.

        Returns
        -------
        PortfolioLoaderApi
            The portfolio API.
        """
        ...


@docstrings_from_sync
class AsyncBayeslineEquityApi(abc.ABC):

    @property
    @abc.abstractmethod
    def riskdatasets(self) -> AsyncRiskDatasetLoaderApi: ...  # noqa: D102

    @property
    @abc.abstractmethod
    def uploaders(self) -> AsyncUploadersApi: ...  # noqa: D102

    @property
    @abc.abstractmethod
    def ids(self) -> AsyncAssetIdApi: ...  # noqa: D102

    @property
    @abc.abstractmethod
    def calendars(self) -> AsyncCalendarLoaderApi: ...  # noqa: D102

    @property
    @abc.abstractmethod
    def universes(self) -> AsyncUniverseLoaderApi: ...  # noqa: D102

    @property
    @abc.abstractmethod
    def exposures(self) -> AsyncExposureLoaderApi: ...  # noqa: D102

    @property
    @abc.abstractmethod
    def modelconstruction(  # noqa: D102
        self,
    ) -> AsyncFactorModelConstructionLoaderApi: ...

    @property
    @abc.abstractmethod
    def riskmodels(self) -> AsyncFactorModelLoaderApi: ...  # noqa: D102

    @property
    @abc.abstractmethod
    def portfoliohierarchies(  # noqa: D102
        self,
    ) -> AsyncPortfolioHierarchyLoaderApi: ...

    @property
    @abc.abstractmethod
    def portfolioreport(self) -> AsyncReportLoaderApi: ...  # noqa: D102

    @property
    @abc.abstractmethod
    def portfolios(self) -> AsyncPortfolioLoaderApi: ...  # noqa: D102
