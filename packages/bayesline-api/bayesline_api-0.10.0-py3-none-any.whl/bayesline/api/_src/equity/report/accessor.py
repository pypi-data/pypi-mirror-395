import abc

from bayesline.api._src._utils import docstrings_from_sync
from bayesline.api._src.equity.portfolioreport import (
    AsyncReportAccessorApi,
    ReportAccessorApi,
)


class TypedReportAccessorApi(abc.ABC):
    """
    A base interface for typed report accessor APIs.

    It is meant to be extended by concrete report implementations, e.g.
    a `FactorCovarianceReportAccessorApi` which adds concrete functions that
    operate on the underyling low level report accessor and slice report data
    to specific representations, e.g. `def fcov` which returns the correct
    dataframe representation of the factor covariance matrix instead the raw
    report dataframe.
    """

    @property
    @abc.abstractmethod
    def accessor(self) -> ReportAccessorApi:
        """
        The underlying report accessor API.

        Returns
        -------
        ReportAccessorApi
            The underlying report accessor API.
        """


@docstrings_from_sync
class AsyncTypedReportAccessorApi(abc.ABC):

    @property
    @abc.abstractmethod
    def accessor(self) -> AsyncReportAccessorApi: ...  # noqa: D102
