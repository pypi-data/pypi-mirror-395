from __future__ import annotations

from abc import ABC
from typing import Annotated, ClassVar, Literal, Self, Type, TypeAlias, Union

from pydantic import BaseModel, Field, model_validator
from pydantic.config import ConfigDict
from pydantic.fields import FieldInfo
from typing_extensions import Unpack

from bayesline.api._src.equity.riskmodels_settings import FactorRiskModelSettings
from bayesline.api._src.registry import (
    EmptySettingsMenu,
    Settings,
    SettingsMenu,
    SettingsTypeMetaData,
)


class ReportAccessorSettings(Settings[EmptySettingsMenu]):
    """Settings for report accessor configuration.

    This class defines the configuration for accessing and processing reports,
    including axes, metrics, pivot columns, and additional report linking.
    """

    axes: dict[str, list[str]]
    metric_cols: list[str]
    pivot_cols: list[str]

    # can be used for multi accessors, one entry for each underlying report
    # for example: extra_cols = name, risk_model, date
    # for example: extra_paths = [["My Setting", "US-All", "2024-12-12"]]
    extra_paths: list[list[str]] = Field(default_factory=list)
    extra_cols: list[str] = Field(default_factory=list)

    linked_reports: list[int] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)

    @property
    def menu_type(self) -> type[EmptySettingsMenu]:  # noqa: D102
        return EmptySettingsMenu

    def describe(self, menu: EmptySettingsMenu) -> str:
        """Describe the report accessor settings.

        Parameters
        ----------
        menu : EmptySettingsMenu
            The menu to use to describe the settings.

        Returns
        -------
        str
            A description of the report accessor settings.
        """
        return f"Report accessor with {len(self.axes)} axes and {len(self.metric_cols)} metrics"


class MeasureSettings(BaseModel, ABC, frozen=True, extra="forbid"):
    """Defines settings for a measure."""

    type: str

    @property
    def columns(self) -> list[str]:
        """Get the column names for this measure.

        Returns
        -------
        list[str]
            The column names for this measure.
        """
        return [self.type]

    def __init_subclass__(cls, **kwargs: Unpack[ConfigDict]) -> None:
        """Initialize subclass and validate that all fields have default values.

        This method ensures that every field in the subclass has a default value,
        so settings can be instantiated without any arguments.

        Parameters
        ----------
        **kwargs : Unpack[ConfigDict]
            Configuration dictionary arguments.

        Raises
        ------
        AssertionError
            If any field does not have a default value.
        """
        super().__init_subclass__(**kwargs)
        # check that every field has a default value, so we can instantiate settings
        # without any argument. Fields defined as a: int = 1, a: int = Field(1), and
        # a: list[int] = Field(default_factory=list) are all valid.
        for f in cls.__annotations__:
            msg = f"{f} not does not have a default value"
            if f not in cls.__dict__:
                raise AssertionError(msg)  # fields without ... = Field(...)
            if isinstance(cls.__dict__[f], FieldInfo):
                if cls.__dict__[f].is_required():
                    raise AssertionError(msg)  # with = Field(...)


class PassThroughFactor2DMeasureSettings(MeasureSettings):
    """Settings for pass-through factor 2D measure.

    This class defines settings for a pass-through factor 2D measure,
    which allows passing through factor data in 2D format.
    """

    type: Literal["PassThroughFactor2D"] = Field("PassThroughFactor2D", repr=False)
    name: str = Field("PassThroughFactor2D", description="The name of the measure.")

    @property
    def columns(self) -> list[str]:
        """Get the column names for this measure.

        Returns
        -------
        list[str]
            The column names for this measure.
        """
        return [self.name]


class HoldingsMeasureSettings(MeasureSettings):
    """Settings for holdings measure.

    This class defines settings for a holdings measure,
    which provides portfolio, benchmark, and active holdings data.
    """

    type: Literal["Holdings"] = Field("Holdings", repr=False)

    @property
    def columns(self) -> list[str]:
        """Get the column names for this measure.

        Returns
        -------
        list[str]
            The column names for this measure.
        """
        return ["Portfolio", "Benchmark", "Active"]


class ExposureMeasureSettings(MeasureSettings):
    """Settings for exposure measure.

    This class defines settings for an exposure measure,
    which provides portfolio, benchmark, and active exposure data.
    """

    type: Literal["Exposure"] = Field("Exposure", repr=False)
    rescale_bench: bool = Field(
        True,
        description="Rescale the benchmark holdings to sum to the sum of the holdings.",
    )
    normalize_holdings: bool = Field(True, description="Make holdings sum to one.")

    @property
    def columns(self) -> list[str]:
        """Get the column names for this measure.

        Returns
        -------
        list[str]
            The column names for this measure.
        """
        return ["Portfolio", "Benchmark", "Active"]


class XSigmaRhoMeasureSettings(MeasureSettings):
    """Settings for X-Sigma-Rho measure.

    This class defines settings for an X-Sigma-Rho measure,
    which provides exposure, volatility, correlation, and contribution data.
    """

    type: Literal["XSigmaRho"] = Field("XSigmaRho", repr=False)
    rescale_bench: bool = Field(
        True,
        description="Rescale the benchmark holdings to sum to the sum of the holdings.",
    )
    normalize_holdings: bool = Field(True, description="Make holdings sum to one.")
    analytics_space: Literal["absolute", "active", "benchmark"] = Field(
        "absolute",
        description=(
            "Compute the analytics in `absolute` space, `active` space, or compute the "
            "analytics only on the `benchmark`."
        ),
    )

    @property
    def columns(self) -> list[str]:
        """Get the column names for this measure.

        Returns
        -------
        list[str]
            The column names for this measure.
        """
        return [
            "Exposure (X)",  # X
            "Volatility (\u03c3)",  # σ
            "Correlation (\u03c1)",  # ρ
            "Contribution (X\u03c3\u03c1)",  # Xσρ
        ]


class TimeSeriesXSigmaRhoMeasureSettings(MeasureSettings):
    """Settings for time series X-Sigma-Rho measure.

    This class defines settings for a time series X-Sigma-Rho measure,
    which provides time series data for exposure, volatility, correlation, and contribution.
    """

    type: Literal["TimeSeriesXSigmaRho"] = Field("TimeSeriesXSigmaRho", repr=False)
    rescale_bench: bool = Field(
        True,
        description="Rescale the benchmark holdings to sum to the sum of the holdings.",
    )
    normalize_holdings: bool = Field(True, description="Make holdings sum to one.")
    analytics_space: Literal["absolute", "active", "benchmark"] = Field(
        "absolute",
        description=(
            "Compute the anlytics in `absolute` space, `active` space, or compute the "
            "analytics only on the `benchmark`."
        ),
    )
    backfill_holdings: bool = Field(
        False,
        description="Backfill the latest holdings, accounting for listing/delisting.",
    )

    @property
    def columns(self) -> list[str]:
        """Get the column names for this measure.

        Returns
        -------
        list[str]
            The column names for this measure.
        """
        return [
            "Exposure (X)",  # X
            "Volatility (\u03c3)",  # σ
            "Correlation (\u03c1)",  # ρ
            "Contribution (X\u03c3\u03c1)",  # Xσρ
        ]


class RiskDecompositionMeasureSettings(MeasureSettings):
    """Settings for risk decomposition measure.

    This class defines settings for a risk decomposition measure. Currently exposure,
    stand-alone volatility and variance contribution are computed.
    """

    type: Literal["RiskDecomposition"] = Field("RiskDecomposition", repr=False)
    rescale_abs_bench: bool = Field(
        True,
        description=(
            "Rescale the benchmark holdings to absolute sum to the absolute sum of the "
            "holdings."
        ),
    )
    analytics_space: Literal["absolute", "active", "benchmark"] = Field(
        "absolute",
        description=(
            "Compute the anlytics in `absolute` space, `active` space, or compute the "
            "analytics only on the `benchmark`."
        ),
    )

    @property
    def columns(self) -> list[str]:
        """Get the column names for this measure.

        Returns
        -------
        list[str]
            The column names for this measure.
        """
        return [
            "Exposure",
            "StandaloneVolatility",
            "VarianceContribution",
        ]


class TimeSeriesBetaMeasureSettings(MeasureSettings):
    """Settings for time series beta measure.

    This class defines settings for a time series beta measure,
    which provides time series beta data for portfolio analysis.
    """

    type: Literal["TimeSeriesBeta"] = Field("TimeSeriesBeta", repr=False)
    rescale_bench: bool = Field(
        True,
        description="Rescale the benchmark holdings to sum to the sum of the holdings.",
    )

    @property
    def columns(self) -> list[str]:
        """Get the column names for this measure.

        Returns
        -------
        list[str]
            The column names for this measure.
        """
        return [
            "Beta (\u03b2)",  # β
        ]


class HVaRMeasureSettings(MeasureSettings):
    """Settings for historical VaR measure.

    This class defines settings for a historical Value at Risk (VaR) measure,
    which provides historical VaR calculations at specified confidence levels.
    """

    type: Literal["Historical VaR"] = Field("Historical VaR", repr=False)
    alpha: list[float] = Field([0.1, 0.05])

    @property
    def columns(self) -> list[str]:
        """Get the column names for this measure.

        Returns
        -------
        list[str]
            The column names for this measure.
        """
        return [f"HistVaR {a:.0%}" for a in self.alpha]


class AVaRMeasureSettings(MeasureSettings):
    """Settings for analytical VaR measure.

    This class defines settings for an analytical Value at Risk (VaR) measure,
    which provides analytical VaR calculations at specified confidence levels.
    """

    type: Literal["Analytical VaR"] = Field("Analytical VaR", repr=False)
    alpha: list[float] = Field([0.1, 0.05])

    @property
    def columns(self) -> list[str]:
        """Get the column names for this measure.

        Returns
        -------
        list[str]
            The column names for this measure.
        """
        return [f"AnVaR {a:.0%}" for a in self.alpha]


class TimeSeriesVolatilityMeasureSettings(MeasureSettings):
    """Settings for time series volatility measure.

    This class defines settings for a time series volatility measure,
    which provides time series volatility data using rolling windows.
    """

    type: Literal["TimeSeriesVolatility"] = Field("TimeSeriesVolatility", repr=False)
    window: str = Field("6mo", description="The size of the rolling window")
    ddof: int = Field(1, description="The degrees of freedom to use for the volality")


class CumsumMeasureSettings(MeasureSettings):
    """Settings for cumulative sum measure.

    This class defines settings for a cumulative sum measure,
    which provides cumulative sum calculations for time series data.
    """

    type: Literal["Cumsum"] = Field("Cumsum", repr=False)


class DrawdownMeasureSettings(MeasureSettings):
    """Settings for drawdown measure.

    This class defines settings for a drawdown measure,
    which provides drawdown calculations for portfolio analysis.
    """

    type: Literal["Drawdown"] = Field("Drawdown", repr=False)
    window: str = Field("6mo", description="The size of the rolling window")


class MovingAverageMeasureSettings(MeasureSettings):
    """Settings for moving average measure.

    This class defines settings for a moving average measure,
    which provides moving average calculations for time series data.
    """

    type: Literal["MovingAverage"] = Field("MovingAverage", repr=False)
    window: str = Field("6mo", description="The size of the rolling window")
    var: Literal["r2", "sigma2", "sigma", "aic", "bic"] = Field(
        "r2", description="The variable to average"
    )

    @property
    def columns(self) -> list[str]:
        """Get the column names for this measure.

        Returns
        -------
        list[str]
            The column names for this measure.
        """
        return [f"{self.type} {self.var}"]


class FactorMovingAverageMeasureSettings(MeasureSettings):
    """Settings for factor moving average measure.

    This class defines settings for a factor moving average measure,
    which provides moving average calculations for factor data.
    """

    type: Literal["FactorMovingAverage"] = Field("FactorMovingAverage", repr=False)
    window: str = Field("6mo", description="The size of the rolling window")
    var: Literal["abs_t", "p", "p1", "p5"] = Field(
        "p", description="The variable to average"
    )

    @property
    def columns(self) -> list[str]:
        """Get the column names for this measure.

        Returns
        -------
        list[str]
            The column names for this measure.
        """
        return [f"{self.type} {self.var}"]


class MovingAverageRSquaredMeasureSettings(MeasureSettings):
    """Settings for moving average R-squared measure.

    This class defines settings for a moving average R-squared measure,
    which provides moving average R-squared calculations for time series data.
    """

    type: Literal["MovingAverageRSquared"] = Field("MovingAverageRSquared", repr=False)
    rescale_bench: bool = Field(
        True,
        description="Rescale the benchmark holdings to sum to the sum of the holdings.",
    )
    normalize_holdings: bool = Field(True, description="Make holdings sum to one.")
    window: str = Field("6mo", description="The size of the rolling window")


class VolForecastMeasureSettings(MeasureSettings):
    """Settings for volatility forecast measure.

    This class defines settings for a volatility forecast measure,
    which provides volatility forecasting calculations and metrics.
    """

    type: Literal["VolForecast"] = Field("VolForecast", repr=False)
    window: str = Field("6mo", description="The size of the rolling window")
    metric: Literal["qlike", "mse", "mae", "bias"] = Field(
        "qlike", description="The metric to use"
    )
    ddof: int = Field(1, description="The degrees of freedom to use for the stability")

    @property
    def columns(self) -> list[str]:
        """Get the column names for this measure.

        Returns
        -------
        list[str]
            The column names for this measure.
        """
        return [
            "VolForecast",
            "VolForecastRealized",
            "VolForecastStability",
            "VolForecastLoss",
        ]


class FactorVolForecastMeasureSettings(MeasureSettings):
    """Settings for factor volatility forecast measure.

    This class defines settings for a factor volatility forecast measure,
    which provides factor volatility forecasting calculations and metrics.
    """

    type: Literal["FactorVolForecast"] = Field("FactorVolForecast", repr=False)
    window: str = Field("6mo", description="The size of the rolling window")
    metric: Literal["qlike", "mse", "mae", "bias"] = Field(
        "qlike", description="The metric to use"
    )
    ddof: int = Field(1, description="The degrees of freedom to use for the stability")

    @property
    def columns(self) -> list[str]:
        """Get the column names for this measure.

        Returns
        -------
        list[str]
            The column names for this measure.
        """
        return [
            "VolForecast",
            "VolForecastRealized",
            "VolForecastStability",
            "VolForecastLoss",
        ]


class FactorCovarianceMeasureSettings(MeasureSettings):
    """Settings for factor covariance measure.

    This class defines settings for a factor covariance measure,
    which provides factor covariance calculations.
    """

    type: Literal["FactorCovariance"] = Field("FactorCovariance", repr=False)


class IdiosyncraticReturnMeasureSettings(MeasureSettings):
    """Settings for idiosyncratic return measure.

    This class defines settings for an idiosyncratic return measure,
    which provides idiosyncratic return calculations.
    """

    type: Literal["IdiosyncraticReturn"] = Field("IdiosyncraticReturn", repr=False)


class IdiosyncraticVolatilityMeasureSettings(MeasureSettings):
    """Settings for idiosyncratic volatility measure.

    This class defines settings for an idiosyncratic volatility measure,
    which provides idiosyncratic volatility calculations.
    """

    type: Literal["IdiosyncraticVolatility"] = Field(
        "IdiosyncraticVolatility", repr=False
    )


class FactorIdioMeasureSettings(MeasureSettings):
    """Settings for factor idiosyncratic measure.

    This class defines settings for a factor idiosyncratic measure,
    which provides factor idiosyncratic calculations.
    """

    type: Literal["FactorIdio"] = Field("FactorIdio", repr=False)


class ForecastBacktestMeasureSettings(MeasureSettings):
    """Settings for forecast backtest measure.

    This class defines settings for a forecast backtest measure,
    which provides forecast backtest calculations and metrics.
    """

    type: Literal["ForecastBacktest"] = Field("ForecastBacktest", repr=False)
    window: str = Field("6mo", description="The size of the rolling window")
    ddof: int = Field(1, description="The degrees of freedom to use for the stability")

    @property
    def columns(self) -> list[str]:
        """Get the column names for this measure.

        Returns
        -------
        list[str]
            The column names for this measure.
        """
        return ["GlobalMinVolPortVolatility", "GlobalMinVolPortPredictedVolatility"]


class BrinsonAttributionMeasureSettings(MeasureSettings):
    """Settings for Brinson attribution measure.

    This class defines settings for a Brinson attribution measure,
    which provides Brinson attribution calculations for portfolio analysis.
    """

    type: Literal["BrinsonAttribution"] = Field("BrinsonAttribution", repr=False)
    rescale_bench: bool = Field(
        True,
        description="Rescale the benchmark holdings to sum to the sum of the holdings.",
    )
    normalize_holdings: bool = Field(True, description="Make holdings sum to one.")
    multiperiod_aggregation: Literal["none", "optimized"] = Field("none")
    return_aggregation_type: Literal["arithmetic", "geometric"] = Field("geometric")

    @property
    def columns(self) -> list[str]:
        """Get the column names for this measure.

        Returns
        -------
        list[str]
            The column names for this measure.
        """
        return ["Allocation", "Selection", "Interaction", "Active"]


class FactorAttributionMeasureSettings(MeasureSettings):
    """Settings for factor attribution measure.

    This class defines settings for a factor attribution measure,
    which provides factor attribution calculations for portfolio analysis.
    """

    type: Literal["FactorAttribution"] = Field("FactorAttribution", repr=False)
    rescale_bench: bool = Field(
        True,
        description="Rescale the benchmark holdings to sum to the sum of the holdings.",
    )
    normalize_holdings: bool = Field(True, description="Make holdings sum to one.")
    multiperiod_aggregation: Literal["none", "optimized"] = Field("none")
    return_aggregation_type: Literal["arithmetic", "geometric"] = Field("geometric")

    @property
    def columns(self) -> list[str]:
        """Get the column names for this measure.

        Returns
        -------
        list[str]
            The column names for this measure.
        """
        return ["Portfolio", "Benchmark", "Active"]


class FactorAttributionDrilldownMeasureSettings(MeasureSettings):
    """Settings for factor attribution drilldown measure.

    This class defines settings for a factor attribution drilldown measure,
    which provides factor attribution drilldown calculations for portfolio analysis.
    """

    type: Literal["FactorAttributionDrilldown"] = Field(
        "FactorAttributionDrilldown", repr=False
    )
    rescale_bench: bool = Field(
        True,
        description="Rescale the benchmark holdings to sum to the sum of the holdings.",
    )
    normalize_holdings: bool = Field(True, description="Make holdings sum to one.")
    multiperiod_aggregation: Literal["none", "optimized"] = Field("none")
    return_aggregation_type: Literal["arithmetic", "geometric"] = Field("geometric")

    @property
    def columns(self) -> list[str]:
        """Get the column names for this measure.

        Returns
        -------
        list[str]
            The column names for this measure.
        """
        if self.normalize_holdings:
            return ["Return", "BenchmarkReturn", "ActiveReturn"]
        else:
            return ["PnL", "BenchmarkPnL", "ActivePnL"]

    @model_validator(mode="after")
    def validate_settings(self) -> Self:
        if not self.normalize_holdings and self.return_aggregation_type == "geometric":
            raise ValueError(
                "Geometric return aggregation is not supported when holdings are not "
                "normalized."
            )
        return self


class PortfolioStressTestMeasureSettings(MeasureSettings):
    """Settings for portfolio stress test measure.

    This class defines settings for a portfolio stress test measure,
    which provides portfolio stress test calculations.
    """

    type: Literal["PortfolioStressTest"] = Field("PortfolioStressTest", repr=False)
    shock_size: float = Field(0.1, description="The size of the shock to apply.")

    @property
    def columns(self) -> list[str]:
        """Get the column names for this measure.

        Returns
        -------
        list[str]
            The column names for this measure.
        """
        return ["Impact"]


class AssetStressTestMeasureSettings(MeasureSettings):
    """Settings for asset stress test measure.

    This class defines settings for an asset stress test measure,
    which provides asset stress test calculations.
    """

    type: Literal["AssetStressTest"] = Field("AssetStressTest", repr=False)
    shock_size: float = Field(
        1.0, description="The size of the shock to apply in standard deviations."
    )

    @property
    def columns(self) -> list[str]:
        """Get the column names for this measure.

        Returns
        -------
        list[str]
            The column names for this measure.
        """
        return ["Impact"]


class AssetHoldingsMeasureSettings(MeasureSettings):
    """Settings for asset holdings measure.

    This class defines settings for an asset holdings measure,
    which provides asset holdings calculations and comparisons.
    """

    type: Literal["AssetHoldings"] = Field("AssetHoldings", repr=False)

    @property
    def columns(self) -> list[str]:
        """Get the column names for this measure.

        Returns
        -------
        list[str]
            The column names for this measure.
        """
        return [
            *["Position", "Position Bench", "Position Diff"],
            *["Holdings", "Holdings Bench", "Holdings Diff"],
            *["Weight", "Weight Bench", "Weight Diff"],
            *["Rank", "Rank Bench", "Rank Diff"],
        ]


MeasureSettingsType: TypeAlias = Union[tuple(MeasureSettings.__subclasses__())]  # type: ignore
MeasureSettingsClassType = Type[MeasureSettingsType]

ALL_HOLDINGS_MEASURE_TYPES = [
    HoldingsMeasureSettings,
]
ALL_EXPOSURE_MEASURE_TYPES = [
    ExposureMeasureSettings,
]
ALL_XSR_MEASURE_TYPES = [
    XSigmaRhoMeasureSettings,
]
ALL_TSXSR_MEASURE_TYPES = [
    TimeSeriesXSigmaRhoMeasureSettings,
]
ALL_RISK_DECOMPOSITION_MEASURE_TYPES = [
    RiskDecompositionMeasureSettings,
]
ALL_TS_BETA_MEASURE_TYPES = [
    TimeSeriesBetaMeasureSettings,
]
ALL_VAR_MEASURE_TYPES = [
    HVaRMeasureSettings,
    AVaRMeasureSettings,
]
ALL_FACTOR_TS_MEASURE_TYPES = [
    TimeSeriesVolatilityMeasureSettings,
    CumsumMeasureSettings,
    DrawdownMeasureSettings,
]
ALL_RISK_MODEL_FIT_MEASURE_TYPES = [
    MovingAverageMeasureSettings,
]
ALL_RISK_MODEL_FIT_FACTOR_MEASURE_TYPES = [
    FactorMovingAverageMeasureSettings,
]
ALL_RISK_MODEL_PORTFOLIO_FIT_MEASURE_TYPES = [
    MovingAverageRSquaredMeasureSettings,
]
ALL_FACTOR_FORECAST_LOSS_MEASURE_TYPES = [
    FactorVolForecastMeasureSettings,
]
ALL_FORECAST_LOSS_MEASURE_TYPES = [
    VolForecastMeasureSettings,
]
ALL_FACTOR_COVARIANCE_MEASURE_TYPES = [
    FactorCovarianceMeasureSettings,
]
ALL_IDIOSYNCRATIC_VOLATILITY_MEASURE_TYPES = [
    IdiosyncraticVolatilityMeasureSettings,
]
ALL_IDIOSYNCRATIC_RETURN_MEASURE_TYPES = [
    IdiosyncraticReturnMeasureSettings,
]
ALL_FACTOR_IDIO_MEASURE_TYPES = [
    FactorIdioMeasureSettings,
]
ALL_STYLE_CORRELATION_MEASURE_TYPES = [
    PassThroughFactor2DMeasureSettings,
]
ALL_STYLE_INDUSTRY_EXPOSURE_MEASURE_TYPES = [
    PassThroughFactor2DMeasureSettings,
]
ALL_FORECAST_BACKTEST_MEASURE_TYPES = [
    ForecastBacktestMeasureSettings,
]
ALL_BRINSON_ATTRIBUTION_MEASURE_TYPES = [
    BrinsonAttributionMeasureSettings,
]
ALL_FACTOR_ATTRIBUTION_MEASURE_TYPES = [
    FactorAttributionMeasureSettings,
]
ALL_FACTOR_ATTRIBUTION_DRILLDOWN_MEASURE_TYPES = [
    FactorAttributionDrilldownMeasureSettings,
]
ALL_PORTFOLIO_STRESS_TEST_MEASURE_TYPES = [
    PortfolioStressTestMeasureSettings,
]
ALL_ASSET_STRESS_TEST_MEASURE_TYPES = [
    AssetStressTestMeasureSettings,
]
ALL_ASSET_HOLDINGS_MEASURE_TYPES = [
    AssetHoldingsMeasureSettings,
]


def _get_default_measures(
    measure_types: list[MeasureSettingsClassType],
) -> list[MeasureSettingsType]:
    return [m() for m in measure_types]


class ConcreteReportSettingsMenu(SettingsMenu, ABC):
    """Abstract base class for concrete report settings menus.

    This class defines the interface for concrete report settings menus
    that provide specific measure types for different report categories.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = []

    def describe(self) -> str:
        """Describe the available report settings.

        Returns
        -------
        str
            A description of the available report settings.
        """
        # TODO implement
        return "NA"


class HoldingsReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for holdings reports.

    This class defines the available measure types for holdings reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = ALL_HOLDINGS_MEASURE_TYPES


class ExposureReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for exposure reports.

    This class defines the available measure types for exposure reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = ALL_EXPOSURE_MEASURE_TYPES


class XSRReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for X-Sigma-Rho reports.

    This class defines the available measure types for X-Sigma-Rho reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = ALL_XSR_MEASURE_TYPES


class TSXSRReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for time series X-Sigma-Rho reports.

    This class defines the available measure types for time series X-Sigma-Rho reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = ALL_TSXSR_MEASURE_TYPES


class RiskDecompositionReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for a risk decomposition reports.

    This class defines the available measure types for a risk decomposition reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_RISK_DECOMPOSITION_MEASURE_TYPES
    )


class TSBetaReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for time series beta reports.

    This class defines the available measure types for time series beta reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = ALL_TS_BETA_MEASURE_TYPES


class VaRReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for VaR reports.

    This class defines the available measure types for VaR reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = ALL_VAR_MEASURE_TYPES


class FactorTSReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for factor time series reports.

    This class defines the available measure types for factor time series reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_FACTOR_TS_MEASURE_TYPES  # type: ignore
    )


class RiskModelFitReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for risk model fit reports.

    This class defines the available measure types for risk model fit reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_RISK_MODEL_FIT_MEASURE_TYPES
    )


class RiskModelFitFactorReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for risk model fit factor reports.

    This class defines the available measure types for risk model fit factor reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_RISK_MODEL_FIT_FACTOR_MEASURE_TYPES
    )


class RiskModelPortfolioFitReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for risk model portfolio fit reports.

    This class defines the available measure types for risk model portfolio fit reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_RISK_MODEL_FIT_MEASURE_TYPES
    )


class FactorForecastLossReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for factor forecast loss reports.

    This class defines the available measure types for factor forecast loss reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_FORECAST_LOSS_MEASURE_TYPES
    )


class AssetForecastLossReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for asset forecast loss reports.

    This class defines the available measure types for asset forecast loss reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_FORECAST_LOSS_MEASURE_TYPES
    )


class FactorCovarianceReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for factor covariance reports.

    This class defines the available measure types for factor covariance reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_FACTOR_COVARIANCE_MEASURE_TYPES
    )


class IdiosyncraticReturnReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for idiosyncratic return reports.

    This class defines the available measure types for idiosyncratic return reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_IDIOSYNCRATIC_RETURN_MEASURE_TYPES
    )


class IdiosyncraticVolatilityReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for idiosyncratic volatility reports.

    This class defines the available measure types for idiosyncratic volatility reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_IDIOSYNCRATIC_VOLATILITY_MEASURE_TYPES
    )


class FactorIdioReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for factor idiosyncratic reports.

    This class defines the available measure types for factor idiosyncratic reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_FACTOR_IDIO_MEASURE_TYPES
    )


class StyleCorrelationReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for style correlation reports.

    This class defines the available measure types for style correlation reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_STYLE_CORRELATION_MEASURE_TYPES
    )


class StyleIndustryExposureReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for style industry exposure reports.

    This class defines the available measure types for style industry exposure reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_STYLE_INDUSTRY_EXPOSURE_MEASURE_TYPES
    )


class ForecastBacktestReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for forecast backtest reports.

    This class defines the available measure types for forecast backtest reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_FORECAST_BACKTEST_MEASURE_TYPES
    )


class BrinsonAttributionReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for Brinson attribution reports.

    This class defines the available measure types for Brinson attribution reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_BRINSON_ATTRIBUTION_MEASURE_TYPES
    )


class FactorAttributionReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for factor attribution reports.

    This class defines the available measure types for factor attribution reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_FACTOR_ATTRIBUTION_MEASURE_TYPES
    )


class FactorAttributionDrilldownReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for factor attribution drilldown reports.

    This class defines the available measure types for factor attribution drilldown
    reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_FACTOR_ATTRIBUTION_DRILLDOWN_MEASURE_TYPES
    )


class PortfolioStressTestReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for portfolio stress test reports.

    This class defines the available measure types for portfolio stress test reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_PORTFOLIO_STRESS_TEST_MEASURE_TYPES
    )


class AssetStressTestReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for asset stress test reports.

    This class defines the available measure types for asset stress test reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_ASSET_STRESS_TEST_MEASURE_TYPES
    )


class AssetHoldingsReportSettingsMenu(ConcreteReportSettingsMenu):
    """Settings menu for asset holdings reports.

    This class defines the available measure types for asset holdings reports.
    """

    measure_types: ClassVar[list[MeasureSettingsClassType]] = (
        ALL_ASSET_HOLDINGS_MEASURE_TYPES
    )


class ReportSettingsMenu(SettingsMenu):
    """Defines available report settings to build a report."""

    hld: ConcreteReportSettingsMenu = HoldingsReportSettingsMenu()
    exp: ConcreteReportSettingsMenu = ExposureReportSettingsMenu()
    xsr: ConcreteReportSettingsMenu = XSRReportSettingsMenu()
    tsx: ConcreteReportSettingsMenu = TSXSRReportSettingsMenu()
    rdc: ConcreteReportSettingsMenu = RiskDecompositionReportSettingsMenu()
    bet: ConcreteReportSettingsMenu = TSBetaReportSettingsMenu()
    var: ConcreteReportSettingsMenu = VaRReportSettingsMenu()
    fts: ConcreteReportSettingsMenu = FactorTSReportSettingsMenu()
    rmf: ConcreteReportSettingsMenu = RiskModelFitReportSettingsMenu()
    rms: ConcreteReportSettingsMenu = RiskModelFitFactorReportSettingsMenu()
    rmp: ConcreteReportSettingsMenu = RiskModelPortfolioFitReportSettingsMenu()
    ffl: ConcreteReportSettingsMenu = FactorForecastLossReportSettingsMenu()
    afl: ConcreteReportSettingsMenu = AssetForecastLossReportSettingsMenu()
    fcr: ConcreteReportSettingsMenu = FactorCovarianceReportSettingsMenu()
    irr: ConcreteReportSettingsMenu = IdiosyncraticReturnReportSettingsMenu()
    ivr: ConcreteReportSettingsMenu = IdiosyncraticVolatilityReportSettingsMenu()
    fni: ConcreteReportSettingsMenu = FactorIdioReportSettingsMenu()
    scr: ConcreteReportSettingsMenu = StyleCorrelationReportSettingsMenu()
    six: ConcreteReportSettingsMenu = StyleIndustryExposureReportSettingsMenu()
    fbt: ConcreteReportSettingsMenu = ForecastBacktestReportSettingsMenu()
    bat: ConcreteReportSettingsMenu = BrinsonAttributionReportSettingsMenu()
    fat: ConcreteReportSettingsMenu = FactorAttributionReportSettingsMenu()
    fad: ConcreteReportSettingsMenu = FactorAttributionDrilldownReportSettingsMenu()
    pst: ConcreteReportSettingsMenu = PortfolioStressTestReportSettingsMenu()
    ast: ConcreteReportSettingsMenu = AssetStressTestReportSettingsMenu()
    ahd: ConcreteReportSettingsMenu = AssetHoldingsReportSettingsMenu()

    def describe(self) -> str:
        """Describe the report settings.

        Returns
        -------
        str
            A description of the report settings menu.
        """
        return "NA"


class ReportSettings(Settings[ReportSettingsMenu]):
    """Defines settings to build a report."""

    report: ConcreteReportSettingsType
    risk_model: Annotated[
        str | int | FactorRiskModelSettings,
        Field(
            description="The risk model to use for the report.",
        ),
        SettingsTypeMetaData[str | int | FactorRiskModelSettings](
            references=FactorRiskModelSettings
        ),
    ]

    def describe(self, menu: ReportSettingsMenu) -> str:
        """Describe the report settings.

        Parameters
        ----------
        menu : ReportSettingsMenu
            The menu to get context information from.

        Returns
        -------
        str
            A description of the report settings.
        """
        return "NA"

    @property
    def menu_type(self) -> type[ReportSettingsMenu]:  # noqa: D102
        return ReportSettingsMenu


class ConcreteReportSettings(BaseModel, ABC, frozen=True, extra="forbid"):
    """Abstract base class for concrete report settings.

    This class defines the interface for concrete report settings
    that provide specific configuration for different report types.
    """

    report_type: str
    lagged_holdings: ClassVar[bool] = False
    measures: list[MeasureSettingsType] = Field(
        description="The measures to include in the report.",
    )


class HoldingsReportSettings(ConcreteReportSettings):
    """Defines settings to build a holdings report."""

    report_type: Literal["Holdings report"] = Field("Holdings report", repr=False)
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(ALL_HOLDINGS_MEASURE_TYPES),
        description="The measures to include in the report.",
    )

    @property
    def menu_type(self) -> type[HoldingsReportSettingsMenu]:  # noqa: D102
        return HoldingsReportSettingsMenu


class ExposureReportSettings(ConcreteReportSettings):
    """Defines settings to build an exposure report."""

    report_type: Literal["Exposure report"] = Field("Exposure report", repr=False)
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(ALL_EXPOSURE_MEASURE_TYPES),
        description="The measures to include in the report.",
    )

    @property
    def menu_type(self) -> type[ExposureReportSettingsMenu]:  # noqa: D102
        return ExposureReportSettingsMenu


class XSRReportSettings(ConcreteReportSettings):
    """Defines settings to build an XSR report."""

    report_type: Literal["XSR report"] = Field("XSR report", repr=False)
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(ALL_XSR_MEASURE_TYPES),
        description="The measures to include in the report.",
    )
    halflife_factor_vol: int = Field(
        42, description="The half-life for the factor volatility."
    )
    halflife_factor_vra: int | None = Field(
        None,
        description=(
            "The half-life for the factor volatility regime adjustment. "
            "If None, no adjustment is applied."
        ),
    )
    halflife_factor_cor: int = Field(
        126, description="The half-life for the factor correlation."
    )
    halflife_idio_vol: int = Field(
        42, description="The half-life for the idiosyncratic volatility."
    )
    shrink_factor_cor_method: Literal["LIS", "QIS", "GIS"] | None = Field(
        None,
        description=(
            "The method to use for the shrinkage of the factor correlation. If None, "
            "don't shrink."
        ),
    )
    shrink_factor_cor_length: int | None = Field(
        1008,
        description=(
            "If a shrinkage method is provided, the length of the shrinkage for the "
            "factor correlation."
        ),
    )
    shrink_factor_cor_standardized: bool = Field(
        False,
        description=(
            "If True, the correlation matrix is combined with an estimate based on the "
            "standardized returns. The halflife_factor_vra is used for the weights."
        ),
    )
    nw_lags_factor_vol: int = Field(
        0, description="The Newey-West lags of the factor volatility."
    )
    nw_lags_factor_vol_halflife_override: int | None = Field(
        None,
        description=(
            "The Newey-West lags override for the factor volatility for lagged returns."
        ),
    )
    nw_lags_factor_cor: int = Field(
        0, description="The Newey-West lags of the factor correlation."
    )
    nw_lags_idio_vol: int = Field(
        0, description="The Newey-West lags of the idiosyncratic volatility."
    )
    nw_lags_idio_vol_halflife_override: int | None = Field(
        None,
        description=(
            "The Newey-West lags override for the idiosyncratic volatility for lagged returns."
        ),
    )
    shrink_idio_vol: float = Field(
        0.0, description="The shrinkage factor for the idiosyncratic volatility."
    )

    @property
    def menu_type(self) -> type[XSRReportSettingsMenu]:  # noqa: D102
        return XSRReportSettingsMenu


class TSXSRReportSettings(ConcreteReportSettings):
    """Defines settings to build a time-series XSR report."""

    report_type: Literal["TSXSR report"] = Field("TSXSR report", repr=False)
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(ALL_TSXSR_MEASURE_TYPES),
        description="The measures to include in the report.",
    )
    halflife_factor_vol: int = Field(
        42, description="The half-life for the factor volatility."
    )
    halflife_factor_vra: int | None = Field(
        None,
        description=(
            "The half-life for the factor volatility regime adjustment. "
            "If None, no adjustment is applied."
        ),
    )
    halflife_factor_cor: int = Field(
        126, description="The half-life for the factor correlation."
    )
    halflife_idio_vol: int = Field(
        42, description="The half-life for the idiosyncratic volatility."
    )
    shrink_factor_cor_method: Literal["LIS", "QIS", "GIS"] | None = Field(
        None,
        description=(
            "The method to use for the shrinkage of the factor correlation. If None, "
            "don't shrink."
        ),
    )
    shrink_factor_cor_length: int | None = Field(
        1008,
        description=(
            "If a shrinkage method is provided, the length of the shrinkage for the "
            "factor correlation."
        ),
    )
    shrink_factor_cor_standardized: bool = Field(
        False,
        description=(
            "If True, the correlation matrix is combined with an estimate based on the "
            "standardized returns. The halflife_factor_vra is used for the weights."
        ),
    )
    nw_lags_factor_vol: int = Field(
        0, description="The Newey-West lags of the factor volatility."
    )
    nw_lags_factor_vol_halflife_override: int | None = Field(
        None,
        description=(
            "The Newey-West lags override for the factor volatility for lagged returns."
        ),
    )
    nw_lags_factor_cor: int = Field(
        0, description="The Newey-West lags of the factor correlation."
    )
    nw_lags_idio_vol: int = Field(
        0, description="The Newey-West lags of the idiosyncratic volatility."
    )
    nw_lags_idio_vol_halflife_override: int | None = Field(
        None,
        description=(
            "The Newey-West lags override for the idiosyncratic volatility for lagged returns."
        ),
    )
    shrink_idio_vol: float = Field(
        0.0, description="The shrinkage factor for the idiosyncratic volatility."
    )


class RiskDecompositionReportSettings(ConcreteReportSettings):
    """Defines settings to build a risk decomposition report."""

    report_type: Literal["Risk decomposition report"] = Field(
        "Risk decomposition report", repr=False
    )
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(
            ALL_RISK_DECOMPOSITION_MEASURE_TYPES
        ),
        description="The measures to include in the report.",
    )
    halflife_factor_vol: int = Field(
        42, description="The half-life for the factor volatility."
    )
    halflife_factor_vra: int | None = Field(
        None,
        description=(
            "The half-life for the factor volatility regime adjustment. "
            "If None, no adjustment is applied."
        ),
    )
    halflife_factor_cor: int = Field(
        126, description="The half-life for the factor correlation."
    )
    halflife_idio_vol: int = Field(
        42, description="The half-life for the idiosyncratic volatility."
    )
    shrink_factor_cor_method: Literal["LIS", "QIS", "GIS"] | None = Field(
        None,
        description=(
            "The method to use for the shrinkage of the factor correlation. If None, "
            "don't shrink."
        ),
    )
    shrink_factor_cor_length: int | None = Field(
        1008,
        description=(
            "If a shrinkage method is provided, the length of the shrinkage for the "
            "factor correlation."
        ),
    )
    shrink_factor_cor_standardized: bool = Field(
        False,
        description=(
            "If True, the correlation matrix is combined with an estimate based on the "
            "standardized returns. The halflife_factor_vra is used for the weights."
        ),
    )
    nw_lags_factor_vol: int = Field(
        0, description="The Newey-West lags of the factor volatility."
    )
    nw_lags_factor_vol_halflife_override: int | None = Field(
        None,
        description=(
            "The Newey-West lags override for the factor volatility for lagged returns."
        ),
    )
    nw_lags_factor_cor: int = Field(
        0, description="The Newey-West lags of the factor correlation."
    )
    nw_lags_idio_vol: int = Field(
        0, description="The Newey-West lags of the idiosyncratic volatility."
    )
    nw_lags_idio_vol_halflife_override: int | None = Field(
        None,
        description=(
            "The Newey-West lags override for the idiosyncratic volatility for lagged returns."
        ),
    )
    shrink_idio_vol: float = Field(
        0.0, description="The shrinkage factor for the idiosyncratic volatility."
    )


class TSBetaReportSettings(ConcreteReportSettings):
    """Defines settings to build a time-series Beta report."""

    report_type: Literal["TS Beta report"] = Field("TS Beta report", repr=False)
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(ALL_TS_BETA_MEASURE_TYPES),
        description="The measures to include in the report.",
    )
    halflife_factor_vol: int = Field(
        42, description="The half-life for the factor volatility."
    )
    halflife_factor_vra: int | None = Field(
        None,
        description=(
            "The half-life for the factor volatility regime adjustment. "
            "If None, no adjustment is applied."
        ),
    )
    halflife_factor_cor: int = Field(
        126, description="The half-life for the factor correlation."
    )
    halflife_idio_vol: int = Field(
        42, description="The half-life for the idiosyncratic volatility."
    )
    shrink_factor_cor_method: Literal["LIS", "QIS", "GIS"] | None = Field(
        None,
        description=(
            "The method to use for the shrinkage of the factor correlation. If None, "
            "don't shrink."
        ),
    )
    shrink_factor_cor_length: int | None = Field(
        1008,
        description=(
            "If a shrinkage method is provided, the length of the shrinkage for the "
            "factor correlation."
        ),
    )
    shrink_factor_cor_standardized: bool = Field(
        False,
        description=(
            "If True, the correlation matrix is combined with an estimate based on the "
            "standardized returns. The halflife_factor_vra is used for the weights."
        ),
    )
    nw_lags_factor_vol: int = Field(
        0, description="The Newey-West lags of the factor volatility."
    )
    nw_lags_factor_vol_halflife_override: int | None = Field(
        None,
        description=(
            "The Newey-West lags override for the factor volatility for lagged returns."
        ),
    )
    nw_lags_factor_cor: int = Field(
        0, description="The Newey-West lags of the factor correlation."
    )
    nw_lags_idio_vol: int = Field(
        0, description="The Newey-West lags of the idiosyncratic volatility."
    )
    nw_lags_idio_vol_halflife_override: int | None = Field(
        None,
        description=(
            "The Newey-West lags override for the idiosyncratic volatility for lagged returns."
        ),
    )
    shrink_idio_vol: float = Field(
        0.0, description="The shrinkage factor for the idiosyncratic volatility."
    )

    @property
    def menu_type(self) -> type[TSXSRReportSettingsMenu]:  # noqa: D102
        return TSXSRReportSettingsMenu


class VaRReportSettings(ConcreteReportSettings):
    """Defines settings to build a VaR report."""

    report_type: Literal["VaR report"] = Field("VaR report", repr=False)
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(ALL_VAR_MEASURE_TYPES),
        description="The measures to include in the report.",
    )
    lookback: int = Field(1000, description="The lookback period for the estimation.")

    @property
    def menu_type(self) -> type[VaRReportSettingsMenu]:  # noqa: D102
        return VaRReportSettingsMenu


class FactorTSReportSettings(ConcreteReportSettings):
    """Defines settings to build a factor time-series report."""

    report_type: Literal["Factor TS report"] = Field("Factor TS report", repr=False)
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(ALL_FACTOR_TS_MEASURE_TYPES),  # type: ignore
        description="The measures to include in the report.",
    )

    @property
    def menu_type(self) -> type[FactorTSReportSettingsMenu]:  # noqa: D102
        return FactorTSReportSettingsMenu


class RiskModelFitReportSettings(ConcreteReportSettings):
    """Defines settings to build a risk model fit report."""

    report_type: Literal["Risk Model Fit report"] = Field(
        "Risk Model Fit report", repr=False
    )
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(ALL_RISK_MODEL_FIT_MEASURE_TYPES),
        description="The measures to include in the report.",
    )

    @property
    def menu_type(self) -> type[RiskModelFitReportSettingsMenu]:  # noqa: D102
        return RiskModelFitReportSettingsMenu


class RiskModelFitFactorReportSettings(ConcreteReportSettings):
    """Defines settings to build a risk model fit report at the factor level."""

    report_type: Literal["Risk Model Fit Factor report"] = Field(
        "Risk Model Fit Factor report", repr=False
    )
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(
            ALL_RISK_MODEL_FIT_FACTOR_MEASURE_TYPES
        ),
        description="The measures to include in the report.",
    )

    @property
    def menu_type(self) -> type[RiskModelFitFactorReportSettingsMenu]:  # noqa: D102
        return RiskModelFitFactorReportSettingsMenu


class RiskModelPortfolioFitReportSettings(ConcreteReportSettings):
    """Defines settings to build a risk model fit report at the portfolio level."""

    report_type: Literal["Risk Model Portfolio Fit report"] = Field(
        "Risk Model Portfolio Fit report", repr=False
    )
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(
            ALL_RISK_MODEL_PORTFOLIO_FIT_MEASURE_TYPES
        ),
        description="The measures to include in the report.",
    )

    @property
    def menu_type(self) -> type[RiskModelPortfolioFitReportSettingsMenu]:  # noqa: D102
        return RiskModelPortfolioFitReportSettingsMenu


class FactorForecastLossReportSettings(ConcreteReportSettings):
    """Defines settings to build a forecast loss report."""

    report_type: Literal["Factor Forecast Loss report"] = Field(
        "Factor Forecast Loss report", repr=False
    )
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(
            ALL_FACTOR_FORECAST_LOSS_MEASURE_TYPES
        ),
        description="The measures to include in the report.",
    )
    horizons: list[int] = Field([1, 5, 21], description="The forecast horizons to use.")
    halflife_factor_vol: int = Field(
        42, description="The half-life for the factor volatility."
    )
    halflife_factor_vra: int | None = Field(
        None,
        description=(
            "The half-life for the factor volatility regime adjustment. "
            "If None, no adjustment is applied."
        ),
    )
    nw_lags_factor_vol: int = Field(
        0, description="The Newey-West lags of the factor volatility."
    )
    nw_lags_factor_vol_halflife_override: int | None = Field(
        None,
        description=(
            "The Newey-West lags override for the factor volatility for lagged returns."
        ),
    )

    @property
    def menu_type(self) -> type[FactorForecastLossReportSettingsMenu]:  # noqa: D102
        return FactorForecastLossReportSettingsMenu


class AssetForecastLossReportSettings(ConcreteReportSettings):
    """Defines settings to build a forecast loss report."""

    report_type: Literal["Forecast Loss report"] = Field(
        "Forecast Loss report", repr=False
    )
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(ALL_FORECAST_LOSS_MEASURE_TYPES),
        description="The measures to include in the report.",
    )
    horizons: list[int] = Field([1, 5, 21], description="The forecast horizons to use.")
    halflife_factor_vol: int = Field(
        42, description="The half-life for the factor volatility."
    )
    halflife_factor_vra: int | None = Field(
        None,
        description=(
            "The half-life for the factor volatility regime adjustment. "
            "If None, no adjustment is applied."
        ),
    )
    halflife_factor_cor: int = Field(
        126, description="The half-life for the factor correlation."
    )
    halflife_idio_vol: int = Field(
        42, description="The half-life for the idiosyncratic volatility."
    )
    shrink_factor_cor_method: Literal["LIS", "QIS", "GIS"] | None = Field(
        None,
        description=(
            "The method to use for the shrinkage of the factor correlation. If None, "
            "don't shrink."
        ),
    )
    shrink_factor_cor_length: int | None = Field(
        1008,
        description=(
            "If a shrinkage method is provided, the length of the shrinkage for the "
            "factor correlation."
        ),
    )
    shrink_factor_cor_standardized: bool = Field(
        False,
        description=(
            "If True, the correlation matrix is combined with an estimate based on the "
            "standardized returns. The halflife_factor_vra is used for the weights."
        ),
    )
    nw_lags_factor_vol: int = Field(
        0, description="The Newey-West lags of the factor volatility."
    )
    nw_lags_factor_vol_halflife_override: int | None = Field(
        None,
        description=(
            "The Newey-West lags override for the factor volatility for lagged returns."
        ),
    )
    nw_lags_factor_cor: int = Field(
        0, description="The Newey-West lags of the factor correlation."
    )
    nw_lags_idio_vol: int = Field(
        0, description="The Newey-West lags of the idiosyncratic volatility."
    )
    nw_lags_idio_vol_halflife_override: int | None = Field(
        None,
        description=(
            "The Newey-West lags override for the idiosyncratic volatility for lagged returns."
        ),
    )
    shrink_idio_vol: float = Field(
        0.0, description="The shrinkage factor for the idiosyncratic volatility."
    )

    @property
    def menu_type(self) -> type[AssetForecastLossReportSettingsMenu]:  # noqa: D102
        return AssetForecastLossReportSettingsMenu


class FactorCovarianceReportSettings(ConcreteReportSettings):
    """Defines settings to build a factor covariance report."""

    report_type: Literal["Factor Covariance report"] = Field(
        "Factor Covariance report", repr=False
    )
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(
            ALL_FACTOR_COVARIANCE_MEASURE_TYPES
        ),
        description="The measures to include in the report.",
    )
    halflife_factor_vol: int = Field(
        42, description="The half-life for the factor volatility."
    )
    halflife_factor_vra: int | None = Field(
        None,
        description=(
            "The half-life for the factor volatility regime adjustment. "
            "If None, no adjustment is applied."
        ),
    )
    halflife_factor_cor: int = Field(
        126, description="The half-life for the factor correlation."
    )
    shrink_factor_cor_method: Literal["LIS", "QIS", "GIS"] | None = Field(
        None,
        description=(
            "The method to use for the shrinkage of the factor correlation. If None, "
            "don't shrink."
        ),
    )
    shrink_factor_cor_length: int | None = Field(
        1008,
        description=(
            "If a shrinkage method is provided, the length of the shrinkage for the "
            "factor correlation."
        ),
    )
    shrink_factor_cor_standardized: bool = Field(
        False,
        description=(
            "If True, the correlation matrix is combined with an estimate based on the "
            "standardized returns. The halflife_factor_vra is used for the weights."
        ),
    )
    nw_lags_factor_vol: int = Field(
        0, description="The Newey-West lags of the factor volatility."
    )
    nw_lags_factor_vol_halflife_override: int | None = Field(
        None,
        description=(
            "The Newey-West lags override for the factor volatility for lagged returns."
        ),
    )
    nw_lags_factor_cor: int = Field(
        0, description="The Newey-West lags of the factor correlation."
    )

    @property
    def menu_type(self) -> type[FactorCovarianceReportSettingsMenu]:  # noqa: D102
        return FactorCovarianceReportSettingsMenu


class IdiosyncraticReturnReportSettings(ConcreteReportSettings):
    """Defines settings to build an idiosyncratic return report."""

    report_type: Literal["Idiosyncratic Return report"] = Field(
        "Idiosyncratic Return report", repr=False
    )
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(
            ALL_IDIOSYNCRATIC_RETURN_MEASURE_TYPES
        ),
        description="The measures to include in the report.",
    )

    @property
    def menu_type(self) -> type[IdiosyncraticReturnReportSettingsMenu]:  # noqa: D102
        return IdiosyncraticReturnReportSettingsMenu


class IdiosyncraticVolatilityReportSettings(ConcreteReportSettings):
    """Defines settings to build an idiosyncratic volatility report."""

    report_type: Literal["Idiosyncratic Volatility report"] = Field(
        "Idiosyncratic Volatility report", repr=False
    )
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(
            ALL_IDIOSYNCRATIC_VOLATILITY_MEASURE_TYPES
        ),
        description="The measures to include in the report.",
    )
    halflife_idio_vol: int = Field(
        42, description="The half-life for the idiosyncratic volatility."
    )
    nw_lags_idio_vol: int = Field(
        0, description="The Newey-West lags of the idiosyncratic volatility."
    )
    nw_lags_idio_vol_halflife_override: int | None = Field(
        None,
        description=(
            "The Newey-West lags override for the idiosyncratic volatility for lagged returns."
        ),
    )
    shrink_idio_vol: float = Field(
        0.0, description="The shrinkage factor for the idiosyncratic volatility."
    )

    @property
    def menu_type(  # noqa: D102
        self,
    ) -> type[IdiosyncraticVolatilityReportSettingsMenu]:
        return IdiosyncraticVolatilityReportSettingsMenu


class FactorIdioReportSettings(ConcreteReportSettings):
    """Defines settings to build a factor vcov and idio report."""

    report_type: Literal["Factor Idio report"] = Field("Factor Idio report", repr=False)
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(ALL_FACTOR_IDIO_MEASURE_TYPES),
        description="The measures to include in the report.",
    )
    halflife_factor_vol: int = Field(
        42, description="The half-life for the factor volatility."
    )
    halflife_factor_vra: int | None = Field(
        None,
        description=(
            "The half-life for the factor volatility regime adjustment. "
            "If None, no adjustment is applied."
        ),
    )
    halflife_factor_cor: int = Field(
        126, description="The half-life for the factor correlation."
    )
    halflife_idio_vol: int = Field(
        42, description="The half-life for the idiosyncratic volatility."
    )
    shrink_factor_cor_method: Literal["LIS", "QIS", "GIS"] | None = Field(
        None,
        description=(
            "The method to use for the shrinkage of the factor correlation. If None, "
            "don't shrink."
        ),
    )
    shrink_factor_cor_length: int | None = Field(
        1008,
        description=(
            "If a shrinkage method is provided, the length of the shrinkage for the "
            "factor correlation."
        ),
    )
    shrink_factor_cor_standardized: bool = Field(
        False,
        description=(
            "If True, the correlation matrix is combined with an estimate based on the "
            "standardized returns. The halflife_factor_vra is used for the weights."
        ),
    )
    nw_lags_factor_vol: int = Field(
        0, description="The Newey-West lags of the factor volatility."
    )
    nw_lags_factor_vol_halflife_override: int | None = Field(
        None,
        description=(
            "The Newey-West lags override for the factor volatility for lagged returns."
        ),
    )
    nw_lags_factor_cor: int = Field(
        0, description="The Newey-West lags of the factor correlation."
    )
    nw_lags_idio_vol: int = Field(
        0, description="The Newey-West lags of the idiosyncratic volatility."
    )
    nw_lags_idio_vol_halflife_override: int | None = Field(
        None,
        description=(
            "The Newey-West lags override for the idiosyncratic volatility for lagged returns."
        ),
    )
    shrink_idio_vol: float = Field(
        0.0, description="The shrinkage factor for the idiosyncratic volatility."
    )

    @property
    def menu_type(self) -> type[FactorIdioReportSettingsMenu]:  # noqa: D102
        return FactorIdioReportSettingsMenu


class StyleCorrelationReportSettings(ConcreteReportSettings):
    """Defines settings to build a style correlation report."""

    report_type: Literal["Style Correlation report"] = Field(
        "Style Correlation report", repr=False
    )
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(
            ALL_STYLE_CORRELATION_MEASURE_TYPES
        ),
        description="The measures to include in the report.",
    )

    @property
    def menu_type(self) -> type[StyleCorrelationReportSettingsMenu]:  # noqa: D102
        return StyleCorrelationReportSettingsMenu


class StyleIndustryExposureReportSettings(ConcreteReportSettings):
    """Defines settings to build a style industry exposure report."""

    report_type: Literal["Style Industry Exposure report"] = Field(
        "Style Industry Exposure report", repr=False
    )
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(
            ALL_STYLE_INDUSTRY_EXPOSURE_MEASURE_TYPES
        ),
        description="The measures to include in the report.",
    )

    @property
    def menu_type(self) -> type[StyleIndustryExposureReportSettingsMenu]:  # noqa: D102
        return StyleIndustryExposureReportSettingsMenu


class ForecastBacktestReportSettings(ConcreteReportSettings):
    """Defines settings to build a forecast backtest report."""

    report_type: Literal["Forecast Backtest report"] = Field(
        "Forecast Backtest report", repr=False
    )
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(
            ALL_FORECAST_BACKTEST_MEASURE_TYPES
        ),
        description="The measures to include in the report.",
    )
    horizons: list[int] = Field([1, 5, 21], description="The forecast horizons to use.")
    halflife_factor_vol: int = Field(
        42, description="The half-life for the factor volatility."
    )
    halflife_factor_vra: int | None = Field(
        None,
        description=(
            "The half-life for the factor volatility regime adjustment. "
            "If None, no adjustment is applied."
        ),
    )
    halflife_factor_cor: int = Field(
        126, description="The half-life for the factor correlation."
    )
    halflife_idio_vol: int = Field(
        42, description="The half-life for the idiosyncratic volatility."
    )
    shrink_factor_cor_method: Literal["LIS", "QIS", "GIS"] | None = Field(
        None,
        description=(
            "The method to use for the shrinkage of the factor correlation. If None, "
            "don't shrink."
        ),
    )
    shrink_factor_cor_length: int | None = Field(
        1008,
        description=(
            "If a shrinkage method is provided, the length of the shrinkage for the "
            "factor correlation."
        ),
    )
    shrink_factor_cor_standardized: bool = Field(
        False,
        description=(
            "If True, the correlation matrix is combined with an estimate based on the "
            "standardized returns. The halflife_factor_vra is used for the weights."
        ),
    )
    nw_lags_factor_vol: int = Field(
        0, description="The Newey-West lags of the factor volatility."
    )
    nw_lags_factor_vol_halflife_override: int | None = Field(
        None,
        description=(
            "The Newey-West lags override for the factor volatility for lagged returns."
        ),
    )
    nw_lags_factor_cor: int = Field(
        0, description="The Newey-West lags of the factor correlation."
    )
    nw_lags_idio_vol: int = Field(
        0, description="The Newey-West lags of the idiosyncratic volatility."
    )
    nw_lags_idio_vol_halflife_override: int | None = Field(
        None,
        description=(
            "The Newey-West lags override for the idiosyncratic volatility for lagged returns."
        ),
    )
    shrink_idio_vol: float = Field(
        0.0, description="The shrinkage factor for the idiosyncratic volatility."
    )

    @property
    def menu_type(self) -> type[ForecastBacktestReportSettingsMenu]:  # noqa: D102
        return ForecastBacktestReportSettingsMenu


class BrinsonAttributionReportSettings(ConcreteReportSettings):
    """Defines settings to build a Brinson attribution report."""

    report_type: Literal["Brinson Attribution report"] = Field(
        "Brinson Attribution report", repr=False
    )
    lagged_holdings: ClassVar[bool] = True
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(
            ALL_BRINSON_ATTRIBUTION_MEASURE_TYPES
        ),
        description="The measures to include in the report.",
    )

    @property
    def menu_type(self) -> type[BrinsonAttributionReportSettingsMenu]:  # noqa: D102
        return BrinsonAttributionReportSettingsMenu


class FactorAttributionReportSettings(ConcreteReportSettings):
    """Defines settings to build a factor attribution report."""

    report_type: Literal["Factor Attribution report"] = Field(
        "Factor Attribution report", repr=False
    )
    lagged_holdings: ClassVar[bool] = True
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(
            ALL_FACTOR_ATTRIBUTION_MEASURE_TYPES
        ),
        description="The measures to include in the report.",
    )

    @property
    def menu_type(self) -> type[FactorAttributionReportSettingsMenu]:  # noqa: D102
        return FactorAttributionReportSettingsMenu


class FactorAttributionDrilldownReportSettings(ConcreteReportSettings):
    """Defines settings to build a factor attribution drilldown report."""

    report_type: Literal["Factor Attribution Drilldown report"] = Field(
        "Factor Attribution Drilldown report", repr=False
    )
    lagged_holdings: ClassVar[bool] = True
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(
            ALL_FACTOR_ATTRIBUTION_DRILLDOWN_MEASURE_TYPES
        ),
        description="The measures to include in the report.",
    )

    @property
    def menu_type(  # noqa: D102
        self,
    ) -> type[FactorAttributionDrilldownReportSettingsMenu]:
        return FactorAttributionDrilldownReportSettingsMenu


class PortfolioStressTestReportSettings(ConcreteReportSettings):
    """Defines settings to build a portfolio stress test report."""

    report_type: Literal["Portfolio Stress Test report"] = Field(
        "Portfolio Stress Test report", repr=False
    )
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(
            ALL_PORTFOLIO_STRESS_TEST_MEASURE_TYPES
        ),
        description="The measures to include in the report.",
    )
    halflife_factor_vol: int = Field(
        42, description="The half-life for the factor volatility."
    )
    halflife_factor_vra: int | None = Field(
        None,
        description=(
            "The half-life for the factor volatility regime adjustment. "
            "If None, no adjustment is applied."
        ),
    )
    halflife_factor_cor: int = Field(
        126, description="The half-life for the factor correlation."
    )
    halflife_idio_vol: int = Field(
        42, description="The half-life for the idiosyncratic volatility."
    )
    shrink_factor_cor_method: Literal["LIS", "QIS", "GIS"] | None = Field(
        None,
        description=(
            "The method to use for the shrinkage of the factor correlation. If None, "
            "don't shrink."
        ),
    )
    shrink_factor_cor_length: int | None = Field(
        1008,
        description=(
            "If a shrinkage method is provided, the length of the shrinkage for the "
            "factor correlation."
        ),
    )
    shrink_factor_cor_standardized: bool = Field(
        False,
        description=(
            "If True, the correlation matrix is combined with an estimate based on the "
            "standardized returns. The halflife_factor_vra is used for the weights."
        ),
    )
    nw_lags_factor_vol: int = Field(
        0, description="The Newey-West lags of the factor volatility."
    )
    nw_lags_factor_vol_halflife_override: int | None = Field(
        None,
        description=(
            "The Newey-West lags override for the factor volatility for lagged returns."
        ),
    )
    nw_lags_factor_cor: int = Field(
        0, description="The Newey-West lags of the factor correlation."
    )
    nw_lags_idio_vol: int = Field(
        0, description="The Newey-West lags of the idiosyncratic volatility."
    )
    nw_lags_idio_vol_halflife_override: int | None = Field(
        None,
        description=(
            "The Newey-West lags override for the idiosyncratic volatility for lagged returns."
        ),
    )
    shrink_idio_vol: float = Field(
        0.0, description="The shrinkage factor for the idiosyncratic volatility."
    )

    @property
    def menu_type(self) -> type[PortfolioStressTestReportSettingsMenu]:  # noqa: D102
        return PortfolioStressTestReportSettingsMenu


class AssetStressTestReportSettings(ConcreteReportSettings):
    """Defines settings to build an asset stress test report."""

    report_type: Literal["Asset Stress Test report"] = Field(
        "Asset Stress Test report", repr=False
    )
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(
            ALL_ASSET_STRESS_TEST_MEASURE_TYPES
        ),
        description="The measures to include in the report.",
    )
    halflife_factor_vol: int = Field(
        42, description="The half-life for the factor volatility."
    )
    halflife_factor_vra: int | None = Field(
        None,
        description=(
            "The half-life for the factor volatility regime adjustment. "
            "If None, no adjustment is applied."
        ),
    )
    halflife_factor_cor: int = Field(
        126, description="The half-life for the factor correlation."
    )
    halflife_idio_vol: int = Field(
        42, description="The half-life for the idiosyncratic volatility."
    )
    shrink_factor_cor_method: Literal["LIS", "QIS", "GIS"] | None = Field(
        None,
        description=(
            "The method to use for the shrinkage of the factor correlation. If None, "
            "don't shrink."
        ),
    )
    shrink_factor_cor_length: int | None = Field(
        1008,
        description=(
            "If a shrinkage method is provided, the length of the shrinkage for the "
            "factor correlation."
        ),
    )
    shrink_factor_cor_standardized: bool = Field(
        False,
        description=(
            "If True, the correlation matrix is combined with an estimate based on the "
            "standardized returns. The halflife_factor_vra is used for the weights."
        ),
    )
    nw_lags_factor_vol: int = Field(
        0, description="The Newey-West lags of the factor volatility."
    )
    nw_lags_factor_vol_halflife_override: int | None = Field(
        None,
        description=(
            "The Newey-West lags override for the factor volatility for lagged returns."
        ),
    )
    nw_lags_factor_cor: int = Field(
        0, description="The Newey-West lags of the factor correlation."
    )
    nw_lags_idio_vol: int = Field(
        0, description="The Newey-West lags of the idiosyncratic volatility."
    )
    nw_lags_idio_vol_halflife_override: int | None = Field(
        None,
        description=(
            "The Newey-West lags override for the idiosyncratic volatility for lagged returns."
        ),
    )
    shrink_idio_vol: float = Field(
        0.0, description="The shrinkage factor for the idiosyncratic volatility."
    )

    @property
    def menu_type(self) -> type[AssetStressTestReportSettingsMenu]:  # noqa: D102
        return AssetStressTestReportSettingsMenu


class AssetHoldingsReportSettings(ConcreteReportSettings):
    """Defines settings to build an asset holdings report."""

    report_type: Literal["Asset Holdings report"] = Field(
        "Asset Holdings report", repr=False
    )
    measures: list[MeasureSettingsType] = Field(
        default_factory=lambda: _get_default_measures(ALL_ASSET_HOLDINGS_MEASURE_TYPES),
        description="The measures to include in the report.",
    )

    @property
    def menu_type(self) -> type[AssetHoldingsReportSettingsMenu]:  # noqa: D102
        return AssetHoldingsReportSettingsMenu


ConcreteReportSettingsType: TypeAlias = Union[tuple(ConcreteReportSettings.__subclasses__())]  # type: ignore
