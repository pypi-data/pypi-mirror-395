import abc
from typing import Generic, ParamSpec, TypeVar

from bayesline.api._src._utils import docstrings_from_sync
from bayesline.api._src.equity.report.accessor import (
    AsyncTypedReportAccessorApi,
    TypedReportAccessorApi,
)
from bayesline.api._src.equity.report.settings import ReportSettings

T = TypeVar("T", bound=TypedReportAccessorApi, covariant=True)
AT = TypeVar("AT", bound=AsyncTypedReportAccessorApi, covariant=True)
S = TypeVar("S", bound=ReportSettings)
P = ParamSpec("P")


class ReportApi(abc.ABC, Generic[P, T, S]):
    """
    A base interface for report APIs.

    It is meant to be extended by several more concrete interfaces which
    narrow down the set of possible args and kwargs to a more specific set,
    e.g. for the subset of possible reports that require a start and end date.
    """

    @property
    @abc.abstractmethod
    def settings(self) -> S:
        """
        The settings used to create this report.

        Returns
        -------
        S
            The settings used to create this report.
        """

    @abc.abstractmethod
    def calculate(self, *args: P.args, **kwargs: P.kwargs) -> T:
        """
        Triggers the calculation of the report and returns an accessor API.

        Parameters
        ----------
        *args: P.args
            The arguments to the report calculation.
        **kwargs: P.kwargs
            The keyword arguments to the report calculation.

        Returns
        -------
        T
            The accessor API for the report result.
        """

    @abc.abstractmethod
    def to_mermaid(self) -> str:
        """
        Get a Mermaid diagram of the report execution graph.

        Returns
        -------
        str
            The Mermaid diagram of the report.
        """


@docstrings_from_sync
class AsyncReportApi(abc.ABC, Generic[P, AT, S]):
    @property
    @abc.abstractmethod
    def settings(self) -> S: ...  # noqa: D102

    @abc.abstractmethod
    async def calculate(  # noqa: D102
        self, *args: P.args, **kwargs: P.kwargs
    ) -> AT: ...

    @abc.abstractmethod
    async def to_mermaid(self) -> str: ...  # noqa: D102
