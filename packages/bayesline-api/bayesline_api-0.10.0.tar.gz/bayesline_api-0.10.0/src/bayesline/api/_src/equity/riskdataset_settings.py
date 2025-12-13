import datetime as dt
from typing import Annotated, Literal, cast

from pydantic import BaseModel, Field, field_validator

from bayesline.api._src.equity.calendar_settings import (
    CalendarSettings,
    CalendarSettingsMenu,
)
from bayesline.api._src.equity.exposure_settings import ExposureSettingsMenu
from bayesline.api._src.equity.modelconstruction_settings import (
    ModelConstructionSettingsMenu,
)
from bayesline.api._src.equity.riskmodels_settings import FactorRiskModelSettingsMenu
from bayesline.api._src.equity.universe_settings import UniverseSettingsMenu
from bayesline.api._src.registry import Settings, SettingsMenu


class RiskDatasetUpdateResult(BaseModel):
    """Result of a risk dataset update operation."""

    ...


class RiskDatasetMetadata(BaseModel):
    """Metadata for a risk dataset.

    Attributes
    ----------
    name : str
        The name of the risk dataset.
    status : Literal["ready", "available"]
        The status of the risk dataset.
    source : Literal["System", "User"]
        The source of the risk dataset.
    """

    name: str
    status: Literal["ready", "available"]
    source: Literal["System", "User"]


class RiskDatasetReferencedExposureSettings(BaseModel, frozen=True, extra="forbid"):
    """Settings for referenced exposure data in a risk dataset.

    This class defines settings for using exposure data from a reference dataset,
    allowing selective copying of continuous and categorical factor groups.
    """

    exposure_type: Literal["referenced"] = "referenced"

    continuous_factor_groups: list[str] | None = Field(
        None,
        description=(
            "The continuous factor groups from the reference dataset to carry over. If "
            "None (default), all continuous factor groups are carried over."
        ),
    )
    categorical_factor_groups: list[str] | None = Field(
        None,
        description=(
            "The categorical factor groups from the reference dataset to carry over. If "
            "None (default), all categorical factor groups are carried over."
        ),
    )

    @field_validator("continuous_factor_groups", "categorical_factor_groups")
    @classmethod
    def _ensure_list(cls, v: str | list[str] | None) -> list[str] | None:
        if isinstance(v, str):
            return [v]
        return v


class RiskDatasetUploadedExposureSettings(BaseModel, frozen=True, extra="forbid"):
    """Settings for uploaded exposure data in a risk dataset.

    This class defines settings for using exposure data from uploaded sources,
    with options for gaussianization, missing value filling, and factor group management.
    """

    exposure_type: Literal["uploaded"] = "uploaded"

    exposure_source: str = Field(description="The uploaded source of the exposures.")

    continuous_factor_groups: list[str] = Field(
        default_factory=list,
        description=(
            "The continuous factor groups from the uploaded dataset to carry over."
        ),
    )
    categorical_factor_groups: list[str] = Field(
        default_factory=list,
        description=(
            "The categorical factor groups from the uploaded dataset to carry over."
        ),
    )

    factor_groups_gaussianize: list[str] = Field(
        default_factory=list,
        description="For which continuous groups to gaussianize the exposures.",
    )
    factor_groups_gaussianize_maintain_zeros: list[str] = Field(
        default_factory=list,
        description=(
            "For which continuous groups to gaussianize the exposures and maintain zeros."
        ),
    )
    factor_groups_fill_miss: list[str] = Field(
        default_factory=list,
        description="For which continuous groups to fill missing values.",
    )


class RiskDatasetHuberRegressionExposureSettings(
    BaseModel, frozen=True, extra="forbid"
):
    """Settings for Huber regression-based exposure data in a risk dataset.

    This class defines settings for generating exposure data using Huber regression
    on time series factors, with options for windowing, regularization, and statistical testing.
    """

    exposure_type: Literal["huber_regression"] = "huber_regression"

    tsfactors_source: str = Field(description="The source of the timeseries factors.")
    factor_group: str = Field(
        "huber_style", description="The factor group name to use for the regression."
    )
    include: list[str] | Literal["All"] = Field(
        "All", description="The factors to include in the regression."
    )
    exclude: list[str] = Field(
        default_factory=list,
        description="The factors to exclude from the regression.",
    )
    fill_miss: bool = Field(True)
    window: int = Field(126, description="The window for the rolling regressions.")
    epsilon: float = Field(1.35, description="The epsilon for the huber regression.")
    alpha: float = Field(0.0001, description="The alpha for the huber regression.")
    alpha_start: float = Field(10.0, description="The alpha when no data is available.")
    student_t_level: float | None = Field(
        None,
        description=(
            "The level for the student t-test. If a test for the significance of the "
            "factor exposure is not rejected, the factor exposure is set to zero. If "
            "None, no test is run and the factor exposure is not set to zero."
        ),
        ge=0.0,
        le=1.0,
    )
    clip: tuple[float | None, float | None] = Field(
        (None, None),
        description=(
            "The clipping lower and upper bounds for the resulting exposures, before "
            "potential huberization."
        ),
    )
    gaussianize: bool = Field(
        True,
        description="Whether to gaussianize the resulting exposures.",
    )
    gaussianize_maintain_zeros: bool = Field(
        False,
        description="Whether to maintain zeros when huberizing the exposures.",
    )
    impute: bool = Field(
        True,
        description="Whether to impute missing values for the resulting exposures.",
    )
    currency: str = Field("USD", description="The currency to convert all returns to.")
    calendar: CalendarSettings = Field(
        default_factory=CalendarSettings,
        description="The calendar to use for the rolling regressions.",
    )


class RiskDatasetUnitExposureSettings(BaseModel, frozen=True, extra="forbid"):
    """Settings for unit exposure data in a risk dataset.

    This class defines settings for creating unit exposures (exposures of 1.0)
    for specific factors in a risk dataset.
    """

    exposure_type: Literal["unit"] = "unit"

    factor_group: str = Field(
        description="The factor group to use for the unit exposures."
    )
    factor: str = Field(description="The factor to use for the unit exposures.")
    factor_type: Literal["continuous", "categorical"] = Field(
        "continuous", description="The type of factor to use for the unit exposures."
    )


RiskDatasetExposureSettings = Annotated[
    RiskDatasetReferencedExposureSettings
    | RiskDatasetUploadedExposureSettings
    | RiskDatasetHuberRegressionExposureSettings
    | RiskDatasetUnitExposureSettings,
    Field(discriminator="exposure_type"),
]


class RiskDatasetSettingsMenu(SettingsMenu, frozen=True, extra="forbid"):
    """Menu for managing risk dataset settings.

    This class provides a menu interface for managing risk dataset settings,
    including validation and description functionality.
    """

    def describe(self) -> str:
        """Describe the risk dataset settings.

        Returns
        -------
        str
            A description of the risk dataset settings.
        """
        return ""


class RiskDatasetProperties(BaseModel):
    """Properties and configuration menus for a risk dataset.

    This class contains the various settings menus and configuration options
    available for a risk dataset, including calendar, universe, exposure,
    and model construction settings.
    """

    factor_risk_model_settings_menu: FactorRiskModelSettingsMenu

    @property
    def exposure_settings_menu(self) -> ExposureSettingsMenu:
        """Get the exposure settings menu.

        Returns
        -------
        ExposureSettingsMenu
            The exposure settings menu.
        """
        return self.factor_risk_model_settings_menu.exposure_settings_menu

    @property
    def modelconstruction_settings_menu(self) -> ModelConstructionSettingsMenu:
        """The model construction settings menu.

        Returns
        -------
        ModelConstructionSettingsMenu
            The model construction settings menu.
        """
        return self.factor_risk_model_settings_menu.modelconstruction_settings_menu

    @property
    def universe_settings_menu(self) -> UniverseSettingsMenu:
        """The universe settings menu.

        Returns
        -------
        UniverseSettingsMenu
            The universe settings menu.
        """
        return self.exposure_settings_menu.universe_settings_menu

    @property
    def calendar_settings_menu(self) -> CalendarSettingsMenu:
        """The calendar settings menu.

        Returns
        -------
        CalendarSettingsMenu
            The calendar settings menu.
        """
        return self.universe_settings_menu.calendar_settings_menu


class RiskDatasetSettings(Settings[RiskDatasetSettingsMenu]):
    """Settings for creating and configuring a risk dataset.

    This class defines the configuration for creating a new risk dataset,
    including reference dataset selection, exposure settings, asset filtering,
    and date trimming options.
    """

    reference_dataset: str | int = Field(
        description=(
            "The dataset (either name or global int identifier) to use as a basis "
            "for the new dataset. All data will be sourced from this dataset."
        ),
        examples=["Bayesline-Global", 1],
    )

    exposures: list[RiskDatasetExposureSettings] = Field(
        default_factory=lambda: [
            cast(RiskDatasetExposureSettings, RiskDatasetReferencedExposureSettings())
        ],
        description=(
            "The exposures to use for the new dataset. By default the reference dataset "
            "is copied as a basis for the new dataset."
        ),
        min_length=1,
    )
    exchange_codes: list[str] | None = Field(
        default=None,
        description="The exchange codes to filter the reference dataset down to.",
    )
    trim_assets: Literal["none", "asset_union", "ccy_union"] = Field(
        "none",
        description=(
            "Whether to trim the assets based on the uploaded exposures. "
            "If 'none', the assets are not trimmed. "
            "If 'asset_union', the assets are trimmed to the union of the asset ids in "
            "the uploaded exposures. "
            "If 'ccy_union', the assets are trimmed to the union of all currencies in "
            "the uploaded exposures."
        ),
    )
    trim_start_date: Literal["none", "earliest_start", "latest_start"] | dt.date = (
        Field(
            "earliest_start",
            description=(
                "Whether to trim the start date based on the uploaded exposures. "
                "If 'none', the start date is not trimmed. "
                "If 'earliest_start', the start date is trimmed to the earliest start "
                "date of the uploaded exposures, or the updoaded exposures and the "
                "reference dateset when referenced exposures are provided. "
                "If 'latest_start', the start date is trimmed to the latest start date "
                "the uploaded exposures, or the updoaded exposures and the reference "
                "dateset when referenced exposures are provided. "
                "If a date is provided, the start date is trimmed to the provided date."
            ),
        )
    )
    trim_end_date: Literal["none", "earliest_end", "latest_end"] | dt.date = Field(
        "latest_end",
        description=(
            "Whether to trim the end date based on the uploaded exposures. "
            "If 'none', the end date is not trimmed. "
            "If 'earliest_end', the end date is trimmed to the earliest end "
            "date of the uploaded exposures, or the updoaded exposures and the "
            "reference dateset when referenced exposures are provided. "
            "If 'latest_end', the end date is trimmed to the latest end date of "
            "the uploaded exposures, or the updoaded exposures and the reference "
            "dateset when referenced exposures are provided. "
            "If a date is provided, the end date is trimmed to the provided date."
        ),
    )

    @property
    def menu_type(self) -> type[RiskDatasetSettingsMenu]:  # noqa: D102
        return RiskDatasetSettingsMenu

    def describe(self, menu: RiskDatasetSettingsMenu) -> str:
        """Describe the risk dataset settings.

        Parameters
        ----------
        menu : RiskDatasetSettingsMenu
            The settings menu to use to describe the settings.

        Returns
        -------
        str
            A description of the risk dataset settings.
        """
        del menu  # not used
        return ""
