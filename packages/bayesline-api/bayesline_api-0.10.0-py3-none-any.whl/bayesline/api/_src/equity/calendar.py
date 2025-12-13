import abc
import datetime as dt

from bayesline.api._src._utils import docstrings_from_sync
from bayesline.api._src.equity.calendar_settings import (
    CalendarSettings,
    CalendarSettingsMenu,
)
from bayesline.api._src.registry import AsyncRegistryBasedApi, RegistryBasedApi
from bayesline.api._src.types import DateLike


class CalendarApi(abc.ABC):
    """Abstract base class for calendar API operations."""

    @property
    @abc.abstractmethod
    def settings(self) -> CalendarSettings:
        """
        Get the settings used to create this calendar.

        Returns
        -------
        CalendarSettings
            The settings used to create this calendar.
        """
        ...

    @abc.abstractmethod
    def get(
        self, *, start: DateLike | None = None, end: DateLike | None = None
    ) -> list[dt.date]:
        """
        Get trade dates for the specified date range.

        Parameters
        ----------
        start : DateLike | None, default=None
            The start date of the data to return, inclusive.
        end : DateLike | None, default=None
            The end date of the data to return, inclusive.

        Returns
        -------
        list[dt.date]
            A list of all trade dates this calendar covers, between the start and end
            dates, inclusive, if these are provided.
        """


@docstrings_from_sync
class AsyncCalendarApi(abc.ABC):
    """Abstract base class for async calendar API operations."""

    @property
    @abc.abstractmethod
    def settings(self) -> CalendarSettings: ...  # noqa: D102

    @abc.abstractmethod
    async def get(  # noqa: D102
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
    ) -> list[dt.date]: ...


class CalendarLoaderApi(
    RegistryBasedApi[CalendarSettings, CalendarSettingsMenu, CalendarApi],
):
    """Registry-based API for loading calendar data."""

    ...


@docstrings_from_sync
class AsyncCalendarLoaderApi(
    AsyncRegistryBasedApi[CalendarSettings, CalendarSettingsMenu, AsyncCalendarApi],
): ...
