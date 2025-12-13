import abc

from bayesline.api._src._utils import docstrings_from_sync
from bayesline.api._src.equity.api import AsyncBayeslineEquityApi, BayeslineEquityApi
from bayesline.api._src.permissions import AsyncPermissionsApi, PermissionsApi
from bayesline.api._src.settings import (
    AsyncSettingsRegistry as NewAsyncSettingsRegistry,
)
from bayesline.api._src.settings import SettingsRegistry as NewSettingsRegistry
from bayesline.api._src.tasks import AsyncTasksApi, TasksApi


class BayeslineApi(abc.ABC):
    """Abstract base class for Bayesline API operations."""

    @property
    @abc.abstractmethod
    def equity(self) -> BayeslineEquityApi:
        """
        Get the equity API.

        Returns
        -------
        BayeslineEquityApi
            The equity API.
        """
        ...

    @property
    @abc.abstractmethod
    def settings_registry(self) -> NewSettingsRegistry:
        """
        Gets the top level settings registry.

        The top level settings registry gives access to all settings used throughout
        the system.

        Returns
        -------
        NewSettingsRegistry
        """

    @property
    @abc.abstractmethod
    def permissions(self) -> PermissionsApi:
        """
        Get the user permissions API.

        Returns
        -------
        PermissionsApi
            The user permissions API.
        """
        ...

    @property
    @abc.abstractmethod
    def tasks(self) -> TasksApi:
        """
        Get the tasks API.

        Returns
        -------
        TasksApi
            The tasks API.
        """
        ...


@docstrings_from_sync
class AsyncBayeslineApi(abc.ABC):

    @property
    @abc.abstractmethod
    def equity(self) -> AsyncBayeslineEquityApi: ...  # noqa: D102

    @property
    @abc.abstractmethod
    def settings_registry(self) -> NewAsyncSettingsRegistry: ...  # noqa: D102

    @property
    @abc.abstractmethod
    def permissions(self) -> AsyncPermissionsApi: ...  # noqa: D102

    @property
    @abc.abstractmethod
    def tasks(self) -> AsyncTasksApi: ...  # noqa: D102
