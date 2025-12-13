from __future__ import annotations

import datetime as dt
import os
from collections.abc import Sequence
from itertools import zip_longest
from typing import Annotated, Any, Literal, cast

from pydantic import (
    BaseModel,
    BeforeValidator,
    Field,
    PositiveInt,
    ValidationInfo,
    field_validator,
    model_validator,
)

from bayesline.api._src.equity.calendar_settings import CalendarSettingsMenu
from bayesline.api._src.equity.exposure_settings import (
    ExposureSettings,
    ExposureSettingsMenu,
    HierarchyGroups,
)
from bayesline.api._src.equity.modelconstruction_settings import (
    ModelConstructionSettings,
    ModelConstructionSettingsMenu,
)
from bayesline.api._src.equity.universe_settings import (
    UniverseSettings,
    UniverseSettingsMenu,
)
from bayesline.api._src.registry import Settings, SettingsMenu, SettingsTypeMetaData

GetModelMode = Literal[
    "compute",
    "compute-and-persist",
    "get-or-compute",
    "get-or-compute-and-persist",
    "get-or-fail",
]


class FactorRiskModelMetadata(BaseModel):
    """Metadata for a factor risk model.

    Contains information about the model's configuration, status, and update history.
    """

    name: str
    id: int
    risk_dataset: str | None

    settings_created_on: dt.datetime
    settings_last_updated_on: dt.datetime

    model_last_updated_on: dt.datetime | None
    model_data_date: dt.date | None
    model_risk_dataset_digest: str | None

    can_update: bool
    current_data_date: dt.date | None
    current_risk_dataset_digest: str | None


def _ensure_list(value: Any) -> Any:
    if isinstance(value, list | tuple):
        return value
    return [value]


class FactorRiskModelSettingsMenu(SettingsMenu, frozen=True, extra="forbid"):
    """Define available settings to build a factor risk model."""

    exposure_settings_menu: ExposureSettingsMenu = Field(
        description="The exposure settings menu.",
    )
    modelconstruction_settings_menu: ModelConstructionSettingsMenu = Field(
        description="The model construction settings menu.",
    )

    @property
    def universe_settings_menu(self) -> UniverseSettingsMenu:
        """The universe settings menu from the exposure settings menu.

        Returns
        -------
        UniverseSettingsMenu
            The universe settings menu from the exposure settings menu.
        """
        return self.exposure_settings_menu.universe_settings_menu

    @property
    def calendar_settings_menu(self) -> CalendarSettingsMenu:
        """The calendar settings menu from the exposure settings menu.

        Returns
        -------
        CalendarSettingsMenu
            The calendar settings menu from the exposure settings menu.
        """
        return self.exposure_settings_menu.calendar_settings_menu

    def describe(self) -> str:
        """Describe the settings menu in a human-readable format.

        Returns
        -------
        str
            A human-readable description of the settings menu.
        """
        return "This settings menu has no description."


class FactorRiskModelSettings(Settings[FactorRiskModelSettingsMenu]):
    """Define all settings needed to build a factor risk model."""

    universe: Annotated[
        list[str | int | UniverseSettings],
        BeforeValidator(_ensure_list),
        Field(
            description="The universe to build the factor risk model on.",
            min_length=1,
            max_length=1,
        ),
        SettingsTypeMetaData[list[str | int | UniverseSettings]](
            references=UniverseSettings,
            extractor=lambda x: [r for r in x if not isinstance(r, UniverseSettings)],
        ),
    ]

    exposures: Annotated[
        list[str | int | ExposureSettings],
        BeforeValidator(_ensure_list),
        Field(
            description="The exposures to build the factor risk model on.",
            min_length=1,
        ),
        SettingsTypeMetaData[str | int | ExposureSettings](
            references=ExposureSettings,
            extractor=lambda x: [r for r in x if not isinstance(r, ExposureSettings)],
        ),
    ] = [ExposureSettings()]

    modelconstruction: Annotated[
        list[str | int | ModelConstructionSettings],
        BeforeValidator(_ensure_list),
        Field(
            description="The model construction settings to use for the factor risk model.",
            min_length=1,
        ),
        SettingsTypeMetaData[str | int | ModelConstructionSettings](
            references=ModelConstructionSettings,
            extractor=lambda x: [
                r for r in x if not isinstance(r, ModelConstructionSettings)
            ],
        ),
    ] = [ModelConstructionSettings()]

    halflife_idio_vra: PositiveInt | None = Field(
        None,
        description=(
            "The half-life for the idio adjustment. "
            "If None, no adjustment is applied."
        ),
    )

    def get_references(self) -> Sequence[str | int]:
        """
        Get references for this settings object.

        Returns
        -------
        Sequence[str | int]
            A sequence of references (strings or integers) for this settings object.
        """
        references: list[str | int] = []
        references.extend(
            [u for u in self.universe if not isinstance(u, UniverseSettings)]
        )
        references.extend(
            [e for e in self.exposures if not isinstance(e, ExposureSettings)]
        )
        references.extend(
            [
                m
                for m in self.modelconstruction
                if not isinstance(m, ModelConstructionSettings)
            ]
        )
        return references

    @property
    def menu_type(self) -> type[FactorRiskModelSettingsMenu]:  # noqa: D102
        return FactorRiskModelSettingsMenu

    @property
    def dataset(self) -> str | None:  # noqa: D102
        # just to make sure we can find the right menu when saving settings
        first_universe = self.universe[0]
        if isinstance(first_universe, UniverseSettings):
            return first_universe.dataset
        else:
            return None

    @model_validator(mode="after")
    def check_list_lengths(self) -> FactorRiskModelSettings:
        if len(self.universe) not in (self.n_stages, 1):
            raise ValueError(
                f"universe must be either one or {self.n_stages} settings."
            )
        if len(self.modelconstruction) not in (self.n_stages, 1):
            raise ValueError(
                f"modelconstruction must be either one or {self.n_stages} settings."
            )
        return self

    @field_validator("modelconstruction", mode="after")
    @classmethod
    def validate_modelconstruction(  # noqa: C901
        cls,
        modelconstruction: list[str | int | ModelConstructionSettings],
        info: ValidationInfo,
    ) -> list[str | int | ModelConstructionSettings]:
        if isinstance(menu := info.context, FactorRiskModelSettingsMenu):
            exposures = cast(list, info.data["exposures"])
            universe = cast(list, info.data["universe"])
            n_stages = len(exposures)
            if len(modelconstruction) == 1:
                modelconstruction = modelconstruction * n_stages
            if len(universe) == 1:
                universe = universe * n_stages
            for m, e, u in zip(modelconstruction, exposures, universe, strict=True):
                # only run this type of validation if the settings are resolved
                if (
                    not isinstance(m, ModelConstructionSettings)
                    or not isinstance(e, ExposureSettings)
                    or not isinstance(u, UniverseSettings)
                ):
                    continue
                # check that the estimation universe is valid
                if m.estimation_universe is not None and isinstance(
                    m.estimation_universe, UniverseSettings
                ):
                    if m.estimation_universe.dataset != u.dataset:
                        raise ValueError(
                            "The dataset in the estimation universe, "
                            f"{m.estimation_universe.dataset}, "
                            f"must match the dataset in the universe, {u.dataset}."
                        )
                    if m.estimation_universe.calendar != u.calendar:
                        raise ValueError(
                            "The calendar in the estimation universe, "
                            f"{m.estimation_universe.calendar}, "
                            f"must match the calendar in the universe, {u.calendar}."
                        )

                # check that the known_factor_map is valid
                e_normalized = e.normalize(u, menu.exposure_settings_menu)
                factor_dict: dict[str, list[str]] = {}
                for group_settings in e_normalized.exposures:
                    if group_settings.exposure_type == "continuous":
                        # get the output (post mapping) factors
                        factors = [
                            f
                            for h in group_settings.hierarchies
                            for f in cast(HierarchyGroups, h).groupings  # normalized
                        ]
                        factor_dict.setdefault(group_settings.factor_group, []).extend(
                            factors
                        )
                missing_groups = set()
                missing_factors = set()
                for g, f in m.known_factor_map:
                    if g not in factor_dict:
                        missing_groups.add(g)
                    else:
                        if f not in factor_dict[g]:
                            missing_factors.add(f)
                if missing_groups:
                    raise ValueError(
                        f"Factor groups {', '.join(missing_groups)} are in known_factor_map "
                        "but not found in any continuous exposure groups"
                    )
                if missing_factors:
                    raise ValueError(
                        f"Factors {', '.join(missing_factors)} are in known_factor_map but not "
                        "found in any corresponding continuous exposure groups"
                    )
                # check that the zero_sum_constraints are valid
                categorical_groups = {
                    g.factor_group
                    for g in e_normalized.exposures
                    if g.exposure_type == "categorical"
                }
                zero_sum_constraints = set(m.zero_sum_constraints)
                if missing_groups := categorical_groups - zero_sum_constraints:
                    raise ValueError(
                        f"Factor groups {', '.join(missing_groups)} do not have a zero sum "
                        "constraint"
                    )
                if missing_constraints := zero_sum_constraints - categorical_groups:
                    raise ValueError(
                        f"Zero sum constraints {', '.join(missing_constraints)} are in "
                        "zero_sum_constraints but not found in any categorical exposure groups "
                    )
        return modelconstruction

    @property
    def n_stages(self) -> int:
        """Get the number of stages.

        Returns
        -------
        int
            The number of stages.
        """
        return len(self.exposures)

    def describe(self, menu: FactorRiskModelSettingsMenu) -> str:
        """Describe the settings.

        Parameters
        ----------
        menu : FactorRiskModelSettingsMenu
            The settings menu to use to construct the description.

        Returns
        -------
        str
            A description of the settings.
        """
        n_stages = len(self.exposures)
        if n_stages == 1:
            result = [
                "Universe: " + str(self.universe[0]),
                "Exposures: " + str(self.exposures[0]),
                "Model Construction: " + str(self.modelconstruction[0]),
            ]
            return os.linesep.join(result)
        else:
            result = []
            for i, (universe, exposures, modelconstruction) in enumerate(
                zip_longest(
                    self.universe,
                    self.exposures,
                    self.modelconstruction,
                    fillvalue="same as previous stage",
                )
            ):
                result.append(f"Stage {i + 1}:")
                result.append("  Universe: " + str(universe))
                result.append("  Exposures: " + str(exposures))
                result.append("  Model Construction: " + str(modelconstruction))
            return os.linesep.join(result)
