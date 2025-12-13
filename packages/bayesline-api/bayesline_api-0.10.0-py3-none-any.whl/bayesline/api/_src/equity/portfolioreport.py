import abc
import datetime as dt
import os
from functools import cached_property
from logging import getLogger
from typing import Sequence

import polars as pl

from bayesline.api._src._utils import docstrings_from_sync
from bayesline.api._src.equity.portfoliohierarchy_settings import (
    PortfolioHierarchySettings,
)
from bayesline.api._src.equity.report_settings import (
    ReportAccessorSettings,
    ReportSettings,
    ReportSettingsMenu,
)
from bayesline.api._src.registry import (
    AsyncReadOnlyRegistry,
    AsyncRegistryBasedApi,
    ReadOnlyRegistry,
    RegistryBasedApi,
)
from bayesline.api._src.tasks import AsyncTask, Task
from bayesline.api._src.types import DateLike, DNFFilterExpressions

logger = getLogger(__name__)


class IllegalPathError(Exception):
    """Exception raised for illegal path operations.

    This exception is raised when an illegal path operation is attempted
    in the portfolio report system.
    """

    pass


class BaseReportAccessorApi(abc.ABC):
    """Abstract base class for report accessor APIs.

    This class defines the interface for report accessor APIs that provide
    access to portfolio report data and metadata.
    """

    @property
    @abc.abstractmethod
    def axes(self) -> dict[str, list[str]]:
        """Get the axes configuration for the report.

        Returns
        -------
        dict[str, list[str]]
            A dictionary mapping axis names to their possible values.
        """
        ...

    @property
    @abc.abstractmethod
    def metric_cols(self) -> list[str]:
        """Get the metric column names for the report.

        Returns
        -------
        list[str]
            A list of metric column names.
        """
        ...

    @property
    @abc.abstractmethod
    def pivot_cols(self) -> list[str]:
        """Get the pivot column names for the report.

        Returns
        -------
        list[str]
            A list of pivot column names.
        """
        ...

    @cached_property
    def axis_lookup(self) -> dict[str, str]:
        """Get the axis lookup mapping.

        Returns
        -------
        dict[str, str]
            A dictionary mapping level names to their dimension names.
        """
        return {
            level: dimension
            for dimension, levels in self.axes.items()
            for level in levels
        }

    def is_path_valid(
        self,
        path_levels: list[str],
        *,
        expand: tuple[str, ...] = (),
    ) -> bool:
        """Check if a path is valid.

        Parameters
        ----------
        path_levels : list[str]
            The path levels to validate.
        expand : tuple[str, ...], default=()
            The expand tuple for validation.

        Returns
        -------
        bool
            True if the path is valid, False otherwise.
        """
        try:
            self.validate_path(path_levels, expand)
            return True
        except AssertionError:
            return False

    def _validate_path(self, path_levels: list[str]) -> list[str]:
        msgs = []
        unknown_levels = [
            level for level in path_levels if level not in self.axis_lookup
        ]
        if unknown_levels:
            msgs.append(f"Unknown levels: {unknown_levels}")

        seen_axes = set()
        prev_axis = ""
        for level in path_levels:
            axis = self.axis_lookup.get(level)
            if not axis:
                msgs.append(f"Level {level} does not exist")
                break

            if axis != prev_axis and axis in seen_axes:
                msgs.append(
                    "Mixed axis groups: "
                    f"{', '.join([self.axis_lookup[level] for level in path_levels])}",
                )
                break

            seen_axes.add(axis)
            prev_axis = axis

        # check that for each dimension the levels are in the right order
        for dimension, levels in self.axes.items():
            path_levels_for_dimension = [
                level for level in path_levels if self.axis_lookup[level] == dimension
            ]
            correct_order = [
                level for level in levels if level in path_levels_for_dimension
            ]
            if path_levels_for_dimension != correct_order:
                msgs.append(
                    f"Invalid order for {dimension}: "
                    f"{', '.join(path_levels_for_dimension)} "
                    f"should be in {', '.join(correct_order)}",
                )

        return msgs

    def validate_path(
        self,
        path_levels: list[str],
        expand: tuple[str, ...] = (),
    ) -> None:
        """Validate a path and expand tuple.

        Parameters
        ----------
        path_levels : list[str]
            The path levels to validate.
        expand : tuple[str, ...], default=()
            The expand tuple to validate.

        Raises
        ------
        IllegalPathError
            If the path or expand tuple is invalid.
        """
        self._validate_path(path_levels)
        msgs = []
        seen = set()
        for e in expand:
            if e in seen:
                msgs.append(f"Duplicate expand: {e}")
            msgs.extend(self._validate_path([*path_levels, e]))
            seen.add(e)

        if msgs:
            raise IllegalPathError(os.linesep.join(msgs))


class ReportAccessorApi(BaseReportAccessorApi):
    """Abstract base class for report accessor APIs.

    This class extends BaseReportAccessorApi with additional abstract methods
    for getting level values and data from portfolio reports.
    """

    @abc.abstractmethod
    def get_level_values(
        self,
        levels: tuple[str, ...] = (),
        include_totals: bool = False,
        filters: DNFFilterExpressions | None = None,
    ) -> pl.DataFrame:
        """Get level values for the specified levels.

        Parameters
        ----------
        levels : tuple[str, ...], default=()
            The levels to get values for.
        include_totals : bool, default=False
            Whether to include totals in the results.
        filters : DNFFilterExpressions | None, default=None
            Optional filters to apply.

        Returns
        -------
        pl.DataFrame
            A DataFrame containing the level values.
        """
        ...

    @abc.abstractmethod
    def get_data(
        self,
        path: list[tuple[str, str]],
        *,
        expand: tuple[str, ...] = (),
        pivot_cols: tuple[str, ...] = (),
        value_cols: tuple[str, ...] = (),
        filters: DNFFilterExpressions | None = None,
        pivot_total: bool = False,
    ) -> pl.DataFrame:
        """Get data for the specified path.

        Parameters
        ----------
        path : list[tuple[str, str]]
            The path to get data for.
        expand : tuple[str, ...], default=()
            The expand tuple for the path.
        pivot_cols : tuple[str, ...], default=()
            The columns to pivot on.
        value_cols : tuple[str, ...], default=()
            The value columns.
        filters : DNFFilterExpressions | None, default=None
            Optional filters to apply.
        pivot_total : bool, default=False
            Whether to include pivot totals.

        Returns
        -------
        pl.DataFrame
            A DataFrame containing the requested data.
        """
        ...

    @abc.abstractmethod
    def get_data_as_task(  # noqa: D102
        self,
        path: list[tuple[str, str]],
        *,
        expand: tuple[str, ...] = (),
        pivot_cols: tuple[str, ...] = (),
        value_cols: tuple[str, ...] = (),
        filters: DNFFilterExpressions | None = None,
        pivot_total: bool = False,
    ) -> Task[pl.DataFrame]: ...

    @abc.abstractmethod
    def persist(self, name: str) -> int:
        """Persist the given report for the given name.

        Parameters
        ----------
        name : str
            The name to persist the report under. Will throw if the name already exists.

        Returns
        -------
        int
            A globally unique identifier of the persisted report.
        """


@docstrings_from_sync
class AsyncReportAccessorApi(BaseReportAccessorApi):

    @abc.abstractmethod
    async def get_level_values(  # noqa: D102
        self,
        levels: tuple[str, ...] = (),
        include_totals: bool = False,
        filters: DNFFilterExpressions | None = None,
    ) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def get_data(  # noqa: D102
        self,
        path: list[tuple[str, str]],
        *,
        expand: tuple[str, ...] = (),
        pivot_cols: tuple[str, ...] = (),
        value_cols: tuple[str, ...] = (),
        filters: DNFFilterExpressions | None = None,
        pivot_total: bool = False,
    ) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def get_data_as_task(  # noqa: D102
        self,
        path: list[tuple[str, str]],
        *,
        expand: tuple[str, ...] = (),
        pivot_cols: tuple[str, ...] = (),
        value_cols: tuple[str, ...] = (),
        filters: DNFFilterExpressions | None = None,
        pivot_total: bool = False,
    ) -> AsyncTask[pl.DataFrame]: ...

    @abc.abstractmethod
    async def persist(self, name: str) -> int: ...  # noqa: D102


class ReportPersister(abc.ABC):
    """Abstract base class for report persisters.

    This class defines the interface for persisting and loading portfolio reports.
    """

    @abc.abstractmethod
    def persist(
        self,
        name: str,
        settings: ReportAccessorSettings,
        accessors: Sequence[ReportAccessorApi],
    ) -> int:
        """Persist a report with the given name and settings.

        Parameters
        ----------
        name : str
            The name to persist the report under.
        settings : ReportAccessorSettings
            The settings for the report.
        accessors : Sequence[ReportAccessorApi]
            The accessors for the report.

        Returns
        -------
        int
            A globally unique identifier of the persisted report.
        """
        ...

    @abc.abstractmethod
    def load_persisted(self, name_or_id: str | int) -> ReportAccessorApi:
        """Load a persisted report by name or ID.

        Parameters
        ----------
        name_or_id : str | int
            The name or ID of the persisted report.

        Returns
        -------
        ReportAccessorApi
            The loaded report accessor API.
        """
        ...

    @abc.abstractmethod
    def delete_persisted(self, name_or_id: list[str | int]) -> None:
        """Delete persisted reports by name or ID.

        Parameters
        ----------
        name_or_id : list[str | int]
            The names or IDs of the persisted reports to delete.
        """
        ...


@docstrings_from_sync
class AsyncReportPersister(abc.ABC):

    @abc.abstractmethod
    async def persist(  # noqa: D102
        self,
        name: str,
        settings: ReportAccessorSettings,
        accessors: Sequence[AsyncReportAccessorApi],
    ) -> int: ...

    @abc.abstractmethod
    async def load_persisted(  # noqa: D102
        self, name_or_id: str | int
    ) -> AsyncReportAccessorApi: ...

    @abc.abstractmethod
    async def delete_persisted(  # noqa: D102
        self, name_or_id: list[str | int]
    ) -> None: ...


class ReportApi(abc.ABC):
    """Abstract base class for report APIs.

    This class defines the interface for portfolio report APIs that provide
    access to report data and metadata.
    """

    @property
    @abc.abstractmethod
    def settings(self) -> ReportSettings:
        """Get the settings used to create this report.

        Returns
        -------
        ReportSettings
            The settings used to create this report.
        """
        ...

    @abc.abstractmethod
    def dates(self) -> list[dt.date]:
        """Get the available dates for this report.

        Returns
        -------
        list[dt.date]
            A list of available dates for this report.
        """
        ...

    @abc.abstractmethod
    def get_report(
        self,
        order: dict[str, list[str]],
        *,
        date: DateLike | None = None,
        date_start: DateLike | None = None,
        date_end: DateLike | None = None,
        subtotals: list[str] | None = None,
    ) -> ReportAccessorApi:
        """Get a report accessor for the specified parameters.

        Parameters
        ----------
        order : dict[str, list[str]]
            The ordering configuration for the report.
        date : DateLike | None, default=None
            The specific date for the report.
        date_start : DateLike | None, default=None
            The start date for the report.
        date_end : DateLike | None, default=None
            The end date for the report.
        subtotals : list[str] | None, default=None
            The subtotals to include in the report.

        Returns
        -------
        ReportAccessorApi
            A report accessor API for the specified parameters.
        """
        ...

    @abc.abstractmethod
    def get_report_as_task(
        self,
        order: dict[str, list[str]],
        *,
        date: DateLike | None = None,
        date_start: DateLike | None = None,
        date_end: DateLike | None = None,
        subtotals: list[str] | None = None,
    ) -> Task[ReportAccessorApi]:
        """Get a report accessor for the specified parameters as a task.

        Parameters
        ----------
        order : dict[str, list[str]]
            The ordering configuration for the report.
        date : DateLike | None, default=None
            The specific date for the report.
        date_start : DateLike | None, default=None
            The start date for the report.
        date_end : DateLike | None, default=None
            The end date for the report.
        subtotals : list[str] | None, default=None
            The subtotals to include in the report.

        Returns
        -------
        Task[ReportAccessorApi]
            A task that returns a report accessor API for the
            specified parameters.
        """
        ...


@docstrings_from_sync
class AsyncReportApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> ReportSettings: ...  # noqa: D102

    @abc.abstractmethod
    async def dates(self) -> list[dt.date]: ...  # noqa: D102

    @abc.abstractmethod
    async def get_report(  # noqa: D102
        self,
        order: dict[str, list[str]],
        *,
        date: DateLike | None = None,
        date_start: DateLike | None = None,
        date_end: DateLike | None = None,
        subtotals: list[str] | None = None,
    ) -> AsyncReportAccessorApi: ...

    @abc.abstractmethod
    async def get_report_as_task(  # noqa: D102
        self,
        order: dict[str, list[str]],
        *,
        date: DateLike | None = None,
        date_start: DateLike | None = None,
        date_end: DateLike | None = None,
        subtotals: list[str] | None = None,
    ) -> AsyncTask[AsyncReportAccessorApi]: ...


class ReportLoaderApi(
    RegistryBasedApi[ReportSettings, ReportSettingsMenu, ReportApi],
):
    """API for loading portfolio reports.

    This class provides functionality for loading portfolio reports using
    registry-based API patterns.
    """

    @abc.abstractmethod
    def load(
        self,
        ref_or_settings: str | int | ReportSettings,
        *,
        hierarchy_ref_or_settings: str | int | PortfolioHierarchySettings | None = None,
    ) -> ReportApi:
        """Load a report using the specified reference or settings.

        Parameters
        ----------
        ref_or_settings : str | int | ReportSettings
            The reference or settings to load the report with.
        hierarchy_ref_or_settings : str | int | PortfolioHierarchySettings | None, default=None
            Optional hierarchy reference or settings.

        Returns
        -------
        ReportApi
            The loaded report API.
        """
        ...

    @abc.abstractmethod
    def load_as_task(  # noqa: D102
        self,
        ref_or_settings: str | int | ReportSettings,
        *,
        hierarchy_ref_or_settings: str | int | PortfolioHierarchySettings | None = None,
    ) -> Task[ReportApi]: ...

    @property
    @abc.abstractmethod
    def persisted_report_settings(
        self,
    ) -> ReadOnlyRegistry[ReportAccessorSettings]:
        """Get the persisted report settings registry.

        Returns
        -------
        ReadOnlyRegistry[ReportAccessorSettings]
            A read-only registry of persisted report settings.
        """
        ...

    @abc.abstractmethod
    def load_persisted(self, name_or_id: str | int) -> ReportAccessorApi:
        """Load a persisted report by name or ID.

        Parameters
        ----------
        name_or_id : str | int
            The name or ID of the persisted report.

        Returns
        -------
        ReportAccessorApi
            The loaded report accessor API.
        """
        ...

    @abc.abstractmethod
    def delete_persisted(self, name_or_id: list[str | int]) -> None:
        """Delete persisted reports by name or ID.

        Parameters
        ----------
        name_or_id : list[str | int]
            The names or IDs of the persisted reports to delete.
        """
        ...


@docstrings_from_sync
class AsyncReportLoaderApi(
    AsyncRegistryBasedApi[ReportSettings, ReportSettingsMenu, AsyncReportApi],
):

    @abc.abstractmethod
    async def load(  # noqa: D102
        self,
        ref_or_settings: str | int | ReportSettings,
        *,
        hierarchy_ref_or_settings: str | int | PortfolioHierarchySettings | None = None,
    ) -> AsyncReportApi: ...

    @abc.abstractmethod
    async def load_as_task(  # noqa: D102
        self,
        ref_or_settings: str | int | ReportSettings,
        *,
        hierarchy_ref_or_settings: str | int | PortfolioHierarchySettings | None = None,
    ) -> AsyncTask[AsyncReportApi]: ...

    @property
    @abc.abstractmethod
    def persisted_report_settings(  # noqa: D102
        self,
    ) -> AsyncReadOnlyRegistry[ReportAccessorSettings]: ...

    @abc.abstractmethod
    async def load_persisted(  # noqa: D102
        self, name_or_id: str | int
    ) -> AsyncReportAccessorApi: ...

    @abc.abstractmethod
    async def delete_persisted(  # noqa: D102
        self, name_or_id: list[str | int]
    ) -> None: ...
