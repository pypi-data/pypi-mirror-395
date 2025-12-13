import abc
import datetime
from typing import Any

from pydantic import BaseModel

from bayesline.api._src._utils import docstrings_from_sync
from bayesline.api._src.types import DateLike


class IncidentSummaryItem(BaseModel):
    """A single incident summary item.

    Parameters
    ----------
    datetime : datetime.datetime
        The datetime when the incident occurred.
    incident_id : str
        The unique identifier for the incident.
    source : str
        The source system that reported the incident.
    """

    datetime: datetime.datetime
    incident_id: str
    source: str


class IncidentSummary(BaseModel):
    """A summary of incidents within a date and index range.

    Parameters
    ----------
    items : list[IncidentSummaryItem]
        List of incident summary items.
    start_date : datetime.datetime
        The start date of the range.
    end_date : datetime.datetime
        The end date of the range.
    n_start : int
        The starting index number.
    n_end : int
        The ending index number.
    n_more : int
        The number of additional incidents beyond the requested range.
    """

    items: list[IncidentSummaryItem]

    start_date: datetime.datetime
    end_date: datetime.datetime
    n_start: int
    n_end: int
    n_more: int


class IncidentsServiceApi(abc.ABC):
    """Gives access to system incidents.

    Includes failed requests, their logs and contextual information.
    """

    @abc.abstractmethod
    def submit_incident(
        self, incident_id: str, source: str, body: dict[str, Any]
    ) -> IncidentSummaryItem:
        r"""Submit an incident with the given ID and source.

        Parameters
        ----------
        incident_id : str
            The ID of the incident.
            Cannot contain any of the following characters: /\\:*?"<>|-
        source : str
            The source of the incident.
            Cannot contain any of the following characters: /\\:*?"<>|-
        body : dict[str, Any]
            The body of the incident.

        Returns
        -------
        IncidentSummaryItem
            The submitted incident item.
        """
        ...

    @abc.abstractmethod
    def get_incident_summary(
        self,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
        start_idx: int = 0,
        end_idx: int = 999999999,
    ) -> IncidentSummary:
        """Obtain incident summaries for the given date and index range.

        Parameters
        ----------
        start_date : DateLike | None, default=None
            The start date of the range. If None, the last 24 hours are used.
        end_date : DateLike | None, default=None
            The end date of the range. If None, `now` is used.
        start_idx : int, default=0
            The start index of the range, `0` being first.
        end_idx : int, default=999999999
            The end index of the range, `-1` being last.

        Returns
        -------
        IncidentSummary
            The incident summary.
        """
        ...

    @abc.abstractmethod
    def get_incident(self, incident_id: str) -> dict[str, dict[str, Any]]:
        r"""Obtain the incident with the given ID.

        Parameters
        ----------
        incident_id : str
            The ID of the incident.
            Cannot contain any of the following characters: /\\:*?"<>|-

        Returns
        -------
        dict[str, dict[str, Any]]
            The incident details.
        """
        ...


@docstrings_from_sync
class AsyncIncidentsServiceApi(abc.ABC):

    @abc.abstractmethod
    async def submit_incident(  # noqa: D102
        self, incident_id: str, source: str, body: dict[str, Any]
    ) -> IncidentSummaryItem: ...

    @abc.abstractmethod
    async def get_incident_summary(  # noqa: D102
        self,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
        start_idx: int = 0,
        end_idx: int = 999999999,
    ) -> IncidentSummary: ...

    @abc.abstractmethod
    async def get_incident(  # noqa: D102
        self, incident_id: str
    ) -> dict[str, dict[str, Any]]: ...
