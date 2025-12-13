import abc

from bayesline.api._src._utils import docstrings_from_sync
from bayesline.api._src.equity.modelconstruction_settings import (
    ModelConstructionSettings,
    ModelConstructionSettingsMenu,
)
from bayesline.api._src.registry import AsyncRegistryBasedApi, RegistryBasedApi


class FactorModelConstructionApi(abc.ABC):
    """Abstract base class for factor model construction APIs.

    This class defines the interface for factor model construction APIs that provide
    access to model construction settings and functionality.
    """

    @property
    @abc.abstractmethod
    def settings(self) -> ModelConstructionSettings:
        """Get the model construction settings.

        Returns
        -------
        ModelConstructionSettings
            The model construction settings.
        """
        ...


@docstrings_from_sync
class AsyncFactorModelConstructionApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> ModelConstructionSettings: ...  # noqa: D102


class FactorModelConstructionLoaderApi(
    RegistryBasedApi[
        ModelConstructionSettings,
        ModelConstructionSettingsMenu,
        FactorModelConstructionApi,
    ],
):
    """API for loading factor model construction services.

    This class provides functionality for loading factor model construction services using
    registry-based API patterns.
    """

    ...


@docstrings_from_sync
class AsyncFactorModelConstructionLoaderApi(
    AsyncRegistryBasedApi[
        ModelConstructionSettings,
        ModelConstructionSettingsMenu,
        AsyncFactorModelConstructionApi,
    ],
): ...
