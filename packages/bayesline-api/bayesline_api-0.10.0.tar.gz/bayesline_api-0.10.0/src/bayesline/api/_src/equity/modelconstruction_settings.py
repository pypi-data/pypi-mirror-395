import os
from typing import Literal, Mapping

from pydantic import (
    Field,
    NonNegativeFloat,
    NonPositiveFloat,
    ValidationInfo,
    field_validator,
)

from bayesline.api._src.equity.universe_settings import UniverseSettings
from bayesline.api._src.registry import Settings, SettingsMenu

WeightingScheme = Literal["SqrtCap", "InvIdioVar"]


class ModelConstructionSettingsMenu(SettingsMenu, frozen=True, extra="forbid"):
    """Defines available modelconstruction settings to build a factor risk model."""

    weights: list[WeightingScheme] = Field(
        description="""
        The available regression weights that can be used for the factor risk model.
        """,
    )

    def describe(self) -> str:
        """Describe the available settings.

        Returns
        -------
        str
            A description of the available settings.
        """
        lines = [f"Weights: {', '.join(self.weights)}"]
        return os.linesep.join(lines)


class ModelConstructionSettings(Settings[ModelConstructionSettingsMenu]):
    """Defines settings to build a factor risk model."""

    currency: str = Field(
        description="The currency of the factor risk model.",
        default="USD",
        examples=["USD", "EUR"],
    )
    weights: WeightingScheme = Field(
        description="The regression weights used for the factor risk model.",
        default="SqrtCap",
        examples=["SqrtCap", "InvIdioVar"],
    )
    estimation_universe: str | int | UniverseSettings | None = Field(
        None,
        description="The universe settings to use for the estimation universe.",
    )
    return_clip_bounds: tuple[NonPositiveFloat | None, NonNegativeFloat | None] = Field(
        description="The bounds for the return clipping.",
        default=(-0.1, 0.1),
        examples=[(-0.1, 0.1), (None, None)],
    )
    thin_category_shrinkage: Mapping[str, NonNegativeFloat] = Field(
        default_factory=dict,
        description=(
            "The ridge-shrinkage penalty for categorical factors with the than 10 "
            "assets with strictly positive exposure. Interpolation is used to scale "
            "the shrinkage strength (for zero assets) to 0.0 (for 10 assets). The keys "
            "are the (categorical) factor groups and the values are the shrinkage "
            "penalty."
        ),
    )
    thin_category_shrinkage_overrides: Mapping[tuple[str, str], NonNegativeFloat] = (
        Field(
            default_factory=dict,
            description=(
                "The shrinkage strength override for the factor risk model. The keys are "
                "the tuples of (categorical) factor groups and factor names and the values "
                "are the shrinkage penalty overrides."
            ),
        )
    )
    zero_sum_constraints: Mapping[
        str, Literal["none", "equal_weights", "mcap_weighted"]
    ] = Field(
        default_factory=dict,
        description=(
            "Whether to apply a zero-sum constraint to the categorical exposures. If the "
            "category exposures are exhaustive and sum to one, then implicitly a dummy "
            "variable trap is present. This can be avoided by creating a constraint on "
            "the factor returns. This means the interpretation of the categorical "
            "factor returns is 'in excess of' the market. If 'none', no constraint is "
            "applied (for example if we do not have a market factor). If "
            "'equal_weights' or 'mcap_weighted', then the categorical factor returns "
            "are constrained to sum to zero, either market-cap weighted or not. For "
            "all categorical factor groups, a value must be provided."
        ),
        examples=[
            {"industry": ["none"]},
            {"industry": ["equal_weights"], "country": ["mcap_weighted"]},
        ],
    )
    known_factor_map: Mapping[tuple[str, str], str] = Field(
        default_factory=dict,
        description=(
            "A mapping from tuple of factor groups and factor names (labels) to known "
            "series. These factors will have fixed returns derived from the series."
        ),
    )
    fx_convert_returns: bool = Field(
        default=True,
        description=(
            "Whether to convert the asset returns to the currency of the factor model."
        ),
    )

    @property
    def menu_type(self) -> type[ModelConstructionSettingsMenu]:  # noqa: D102
        return ModelConstructionSettingsMenu

    @field_validator("weights")
    @classmethod
    def check_valid_weights(
        cls, weights: WeightingScheme, info: ValidationInfo
    ) -> WeightingScheme:
        if isinstance(menu := info.context, ModelConstructionSettingsMenu):
            if weights not in menu.weights:
                raise ValueError(f"Invalid weights: {weights}")
        return weights

    def describe(self, menu: ModelConstructionSettingsMenu) -> str:
        """Describe the available settings.

        Parameters
        ----------
        menu : ModelConstructionSettingsMenu
            The menu to get context information from.

        Returns
        -------
        str
            The description of the model construction settings.
        """
        del menu  # not used
        lines = [
            f"Currency: {self.currency}",
            f"Weights: {self.weights}",
            f"Return Clip Bounds: {self.return_clip_bounds}",
        ]
        return os.linesep.join(lines)
