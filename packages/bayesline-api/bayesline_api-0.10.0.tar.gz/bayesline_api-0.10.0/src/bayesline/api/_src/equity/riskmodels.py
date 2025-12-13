import abc
import datetime as dt

import polars as pl

from bayesline.api._src._utils import docstrings_from_sync
from bayesline.api._src.equity.riskmodels_settings import (
    FactorRiskModelMetadata,
    FactorRiskModelSettings,
    FactorRiskModelSettingsMenu,
    GetModelMode,
)
from bayesline.api._src.registry import AsyncRegistryBasedApi, RegistryBasedApi
from bayesline.api._src.tasks import AsyncTask, Task
from bayesline.api._src.types import DateLike, IdType


class FactorModelApi(abc.ABC):
    """Provide access to factor risk model data and operations.

    A factor risk model provides exposure data, factor returns, and other risk metrics
    for a set of assets based on predefined factors.
    """

    @abc.abstractmethod
    def dates(self) -> list[dt.date]:
        """Get all dates covered by this risk model.

        Returns
        -------
        list[dt.date]
            All dates covered by this risk model.
        """
        pass

    @abc.abstractmethod
    def factors(self) -> dict[str, list[str]]:
        """Get the factor groups and their factors.

        Returns
        -------
        dict[str, list[str]]
            Dict where the keys are the included factor groups, and the values are the
            factors in that group.
        """
        ...

    @abc.abstractmethod
    def exposures(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        stage: int = 1,
    ) -> pl.DataFrame:
        """
        Get the risk model exposures for this risk model.

        Parameters
        ----------
        start : DateLike | None, default=None
            The start date of the data to return, inclusive.
        end : DateLike | None, default=None
            The end date of the data to return, inclusive.
        id_type : IdType | None, default=None
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.
        stage : int, default=1
            The stage of the factor model to return exposures for, of the potentially
            multi-stage regression. Default to 1 (the first stage).

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pl.DataFrame
            The data for the given date range with the first two column as the date and
            asset id. The remaining columns are the individual styles.
        """
        ...

    @abc.abstractmethod
    def exposures_as_task(  # noqa: D102
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        stage: int = 1,
    ) -> Task[pl.DataFrame]: ...

    @abc.abstractmethod
    def universe(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        stage: int = 1,
    ) -> pl.DataFrame:
        """
        Get the risk model universe for this risk model.

        Parameters
        ----------
        start : DateLike | None, default=None
            The start date of the data to return, inclusive.
        end : DateLike | None, default=None
            The end date of the data to return, inclusive.
        id_type : IdType | None, default=None
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.
        stage : int, default=1
            The stage of the factor model to return universe for, of the potentially
            multi-stage regression. Default to 1 (the first stage).

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pl.DataFrame
            The data for the given date range where the first column is the date and the
            remaining columns are the asset ids. The values are the universe inclusion.
        """
        ...

    @abc.abstractmethod
    def universe_as_task(  # noqa: D102
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        stage: int = 1,
    ) -> Task[pl.DataFrame]: ...

    @abc.abstractmethod
    def estimation_universe(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        stage: int = 1,
    ) -> pl.DataFrame:
        """
        Get the risk model estimation universe for this risk model.

        Parameters
        ----------
        start : DateLike | None, default=None
            The start date of the data to return, inclusive.
        end : DateLike | None, default=None
            The end date of the data to return, inclusive.
        id_type : IdType | None, default=None
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.
        stage : int, default=1
            The stage of the factor model to return universe for, of the potentially
            multi-stage regression. Default to 1 (the first stage).

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pl.DataFrame
            The data for the given date range where the first column is the date and the
            remaining columns are the asset ids. The values are the estimation universe
            inclusion.
        """
        ...

    @abc.abstractmethod
    def estimation_universe_as_task(  # noqa: D102
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        stage: int = 1,
    ) -> Task[pl.DataFrame]: ...

    @abc.abstractmethod
    def market_caps(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        """
        Get the exposure-weighted market caps for this risk model.

        Parameters
        ----------
        start : DateLike | None, default=None
            The start date of the data to return, inclusive.
        end : DateLike | None, default=None
            The end date of the data to return, inclusive.
        id_type : IdType | None, default=None
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pl.DataFrame
            The data for the given date range where the rows are the total market cap
            for each date, weighted by the exposure of each asset. For industry factors,
            this specifically means that the value is the sum of all assets in the
            estimation universe in that industry.
        """
        ...

    @abc.abstractmethod
    def market_caps_as_task(  # noqa: D102
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> Task[pl.DataFrame]: ...

    @abc.abstractmethod
    def weights(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        """
        Get the idiosyncratic volatility weights for this risk model.

        Parameters
        ----------
        start : DateLike | None, default=None
            The start date of the data to return, inclusive.
        end : DateLike | None, default=None
            The end date of the data to return, inclusive.
        id_type : IdType | None, default=None
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pl.DataFrame
            The data for the given date range where the rows are the idiosyncratic
            volatility for each date.
        """
        ...

    @abc.abstractmethod
    def weights_as_task(  # noqa: D102
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> Task[pl.DataFrame]: ...

    @abc.abstractmethod
    def future_asset_returns(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        """
        Get the asset returns for this risk model on the next day.

        Parameters
        ----------
        start : DateLike | None, default=None
            The start date of the data to return, inclusive.
        end : DateLike | None, default=None
            The end date of the data to return, inclusive.
        id_type : IdType | None, default=None
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pl.DataFrame
            The data for the given date range where the index is the date
            and the columns are the asset id. The values are the asset returns.
        """
        ...

    @abc.abstractmethod
    def future_asset_returns_as_task(  # noqa: D102
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> Task[pl.DataFrame]: ...

    @abc.abstractmethod
    def fret(
        self,
        *,
        freq: str | None = None,
        cumulative: bool = False,
        start: DateLike | None = None,
        end: DateLike | None = None,
    ) -> pl.DataFrame:
        """Get factor returns for the given date range.

        Parameters
        ----------
        freq : str | None, default=None
            The frequency of the return aggregation, e.g. `D` for daily.
            Defaults to daily (i.e. unaggregated).
        cumulative : bool, default=False
            If True, returns the cumulative returns.
        start : DateLike | None, default=None
            The start date of the data to return, inclusive.
        end : DateLike | None, default=None
            The end date of the data to return, inclusive.

        Returns
        -------
        pl.DataFrame
            The factor returns for the given date range.
        """
        ...

    @abc.abstractmethod
    def fret_as_task(  # noqa: D102
        self,
        *,
        freq: str | None = None,
        cumulative: bool = False,
        start: DateLike | None = None,
        end: DateLike | None = None,
    ) -> Task[pl.DataFrame]: ...

    @abc.abstractmethod
    def t_stats(self) -> pl.DataFrame:
        """Get t-statistics for the factor model.

        Returns
        -------
        pl.DataFrame
            The t-statistics for the factor model.
        """
        ...

    @abc.abstractmethod
    def t_stats_as_task(self) -> Task[pl.DataFrame]: ...  # noqa: D102

    @abc.abstractmethod
    def p_values(self) -> pl.DataFrame:
        """Get p-values for the risk model factors.

        Returns
        -------
        pl.DataFrame
            The p-values for the risk model factors.
        """
        ...

    @abc.abstractmethod
    def p_values_as_task(self) -> Task[pl.DataFrame]: ...  # noqa: D102

    @abc.abstractmethod
    def r2(self) -> pl.DataFrame:
        """Get R-squared values for the factor model.

        Returns
        -------
        pl.DataFrame
            The R-squared values for the factor model.
        """
        ...

    @abc.abstractmethod
    def r2_as_task(self) -> Task[pl.DataFrame]: ...  # noqa: D102

    @abc.abstractmethod
    def sigma2(self) -> pl.DataFrame:
        """Get sigma squared values for the factor model.

        Returns
        -------
        pl.DataFrame
            The sigma squared values for the factor model.
        """
        ...

    @abc.abstractmethod
    def sigma2_as_task(self) -> Task[pl.DataFrame]: ...  # noqa: D102


@docstrings_from_sync
class AsyncFactorModelApi(abc.ABC):

    @abc.abstractmethod
    async def dates(self) -> list[dt.date]: ...  # noqa: D102

    @abc.abstractmethod
    async def factors(self) -> dict[str, list[str]]: ...  # noqa: D102

    @abc.abstractmethod
    async def exposures(  # noqa: D102
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        stage: int = 1,
    ) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def exposures_as_task(  # noqa: D102
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        stage: int = 1,
    ) -> AsyncTask[pl.DataFrame]: ...

    @abc.abstractmethod
    async def universe(  # noqa: D102
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        stage: int = 1,
    ) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def universe_as_task(  # noqa: D102
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        stage: int = 1,
    ) -> AsyncTask[pl.DataFrame]: ...

    @abc.abstractmethod
    async def estimation_universe(  # noqa: D102
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        stage: int = 1,
    ) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def estimation_universe_as_task(  # noqa: D102
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        stage: int = 1,
    ) -> AsyncTask[pl.DataFrame]: ...

    @abc.abstractmethod
    async def market_caps(  # noqa: D102
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def market_caps_as_task(  # noqa: D102
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> AsyncTask[pl.DataFrame]: ...

    @abc.abstractmethod
    async def weights(  # noqa: D102
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def weights_as_task(  # noqa: D102
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> AsyncTask[pl.DataFrame]: ...

    @abc.abstractmethod
    async def future_asset_returns(  # noqa: D102
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def future_asset_returns_as_task(  # noqa: D102
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> AsyncTask[pl.DataFrame]: ...

    @abc.abstractmethod
    async def fret(  # noqa: D102
        self,
        *,
        freq: str | None = None,
        cumulative: bool = False,
        start: DateLike | None = None,
        end: DateLike | None = None,
    ) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def fret_as_task(  # noqa: D102
        self,
        *,
        freq: str | None = None,
        cumulative: bool = False,
        start: DateLike | None = None,
        end: DateLike | None = None,
    ) -> AsyncTask[pl.DataFrame]: ...

    @abc.abstractmethod
    async def t_stats(self) -> pl.DataFrame: ...  # noqa: D102

    @abc.abstractmethod
    async def t_stats_as_task(self) -> AsyncTask[pl.DataFrame]: ...  # noqa: D102

    @abc.abstractmethod
    async def p_values(self) -> pl.DataFrame: ...  # noqa: D102

    @abc.abstractmethod
    async def p_values_as_task(self) -> AsyncTask[pl.DataFrame]: ...  # noqa: D102

    @abc.abstractmethod
    async def r2(self) -> pl.DataFrame: ...  # noqa: D102

    @abc.abstractmethod
    async def r2_as_task(self) -> AsyncTask[pl.DataFrame]: ...  # noqa: D102

    @abc.abstractmethod
    async def sigma2(self) -> pl.DataFrame: ...  # noqa: D102

    @abc.abstractmethod
    async def sigma2_as_task(self) -> AsyncTask[pl.DataFrame]: ...  # noqa: D102


class FactorModelEngineApi(abc.ABC):
    """Provide access to factor risk model engine operations.

    A factor model engine is responsible for building and managing factor risk models
    based on provided settings.
    """

    @property
    @abc.abstractmethod
    def settings(self) -> FactorRiskModelSettings:
        """Get the settings used to create this risk model.

        Returns
        -------
        FactorRiskModelSettings
            The settings used to create this risk model.
        """
        ...

    @abc.abstractmethod
    def get_model(
        self, mode: GetModelMode = "get-or-compute-and-persist"
    ) -> FactorModelApi:
        """Get a built factor model instance for the given settings.

        Parameters
        ----------
        mode : GetModelMode, default="get-or-compute-and-persist"
            The mode to use to get the model.
            If `compute`, will compute the model from scratch and return it, without
            persisting it.
            If `get-or-compute-and-persist`, will check if the model is already
            persisted (and up to date) and return it if so, or else compute it
            from scratch and persist it.
            If `get-or-compute`, will check if the model is already
            persisted and return it if so, or else compute it from scratch and return
            it without persisting it.
            If `compute-and-persist`, will compute the model from scratch and persist it.
            If `get-or-fail`, will return the model if it is already persisted, or else
            raise an error if the model is not persisted.

        Returns
        -------
        FactorModelApi
            A built factor model instance for the given settings.
        """

    @abc.abstractmethod
    def get_model_as_task(
        self, mode: GetModelMode = "get-or-compute-and-persist"
    ) -> Task[FactorModelApi]:
        """Get a built factor model instance as a task.

        Parameters
        ----------
        mode : GetModelMode, default="get-or-compute-and-persist"
            The mode to use to get the model.
            If `compute`, will compute the model from scratch and return it, without
            persisting it.
            If `get-or-compute-and-persist`, will check if the model is already
            persisted (and up to date) and return it if so, or else compute it
            from scratch and persist it.
            If `get-or-compute`, will check if the model is already
            persisted and return it if so, or else compute it from scratch and return
            it without persisting it.
            If `compute-and-persist`, will compute the model from scratch and persist it.
            If `get-or-fail`, will return the model if it is already persisted, or else
            raise an error if the model is not persisted.

        Returns
        -------
        Task[FactorModelApi]
            A task that will return a built factor model instance
            for the given settings.
        """
        ...


@docstrings_from_sync
class AsyncFactorModelEngineApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> FactorRiskModelSettings: ...  # noqa: D102

    @abc.abstractmethod
    async def get_model(  # noqa: D102
        self, mode: GetModelMode = "get-or-compute-and-persist"
    ) -> AsyncFactorModelApi: ...

    @abc.abstractmethod
    async def get_model_as_task(  # noqa: D102
        self, mode: GetModelMode = "get-or-compute-and-persist"
    ) -> AsyncTask[AsyncFactorModelApi]: ...


class FactorModelLoaderApi(
    RegistryBasedApi[
        FactorRiskModelSettings, FactorRiskModelSettingsMenu, FactorModelEngineApi
    ]
):
    """Provide access to factor risk model loading and registry operations.

    A factor model loader manages the registry of factor risk models and provides
    access to existing models.
    """

    @abc.abstractmethod
    def list_riskmodels(
        self, risk_dataset: str | None = None
    ) -> list[FactorRiskModelMetadata]:
        """List all risk models in the registry.

        Parameters
        ----------
        risk_dataset : str | None, default=None
            The risk dataset to filter by.
            If not given, all risk models are returned.

        Returns
        -------
        list[FactorRiskModelMetadata]
            List of all risk models in the registry.
        """


@docstrings_from_sync
class AsyncFactorModelLoaderApi(
    AsyncRegistryBasedApi[
        FactorRiskModelSettings, FactorRiskModelSettingsMenu, AsyncFactorModelEngineApi
    ]
):

    @abc.abstractmethod
    async def list_riskmodels(  # noqa: D102
        self, risk_dataset: str | None = None
    ) -> list[FactorRiskModelMetadata]: ...
