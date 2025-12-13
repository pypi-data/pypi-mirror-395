from __future__ import annotations

import json
import os
from collections.abc import Mapping
from typing import Annotated, Any, Literal

import polars as pl
from pydantic import (
    BaseModel,
    Field,
    NonNegativeFloat,
    ValidationInfo,
    field_validator,
    model_validator,
)

from bayesline.api._src.equity import settings as settings_tools
from bayesline.api._src.equity.calendar_settings import (
    CalendarSettings,
    CalendarSettingsMenu,
)
from bayesline.api._src.equity.portfolio_settings import PortfolioOrganizerSettings
from bayesline.api._src.registry import Settings, SettingsMenu, SettingsTypeMetaData
from bayesline.api._src.types import IdType

Hierarchy = settings_tools.Hierarchy


class CategoricalFilterSettings(BaseModel, frozen=True, extra="forbid"):
    """Specify include and exclude filters for categorical codes.

    Examples of categorical codes are industries or countries. Assets are included if
    they are part of at least one include and not part of any exclude.

    By default all codes for the given hierarchy are included.
    """

    hierarchy: str = Field(
        min_length=1,
        description="The categorical hierarchy to use.",
        examples=["trbc"],
    )

    include: list[str] | Literal["All"] = Field(
        default="All",
        description=(
            "Valid industry codes or labels for given hierarchy at any level. If "
            "labels are used which may be duplicated, then the code with the highest "
            "level is used. If 'All', all codes are included."
        ),
        examples=[["3571"], "All", ["Materials", "1010"], ["Europe", "CAN"]],
    )

    exclude: list[str] = Field(
        default_factory=list,
        description=(
            "Valid industry codes or labels for given hierarchy at any level. If "
            "labels are used which may be duplicated, then the code with the lowest "
            "level is used."
        ),
        examples=[["3571"], ["Materials", "1010"], ["JPN"]],
    )

    @model_validator(mode="after")
    def validate_filters(self, info: ValidationInfo) -> CategoricalFilterSettings:
        if isinstance(menu := info.context, UniverseSettingsMenu):
            settings_tools.validate_hierarchy_schema(
                menu.categorical_hierarchies, self.hierarchy
            )
            settings_tools.validate_hierarchy_filters(
                menu.categorical_hierarchies[self.hierarchy],
                self.include,
                self.exclude,
                menu.categorical_hierarchies_labels[self.hierarchy],
            )
        return self

    def validate_settings(self, menu: UniverseSettingsMenu | None) -> None:
        """Validate the categorical filter settings.

        Parameters
        ----------
        menu : UniverseSettingsMenu | None
            The menu to validate against. If None, the categorical filter settings is validated
            without having the menu context. This means that less validation is done.
        """
        self.model_validate(self.model_dump(), context=menu)


class MCapFilterSettings(BaseModel, frozen=True, extra="forbid"):
    """Specify the lower and upper bound for the market cap filter.

    By default the bounds are infinite.
    """

    lower: NonNegativeFloat = Field(
        default=0.0,
        ge=0.0,
        description="Lower bound of the cap filter in USD.",
        examples=[1e10],
    )

    upper: NonNegativeFloat = Field(
        default=1e20,
        gt=0.0,
        description="Upper bound of the cap filter in USD.",
        examples=[1e12],
    )

    @model_validator(mode="after")
    def check_upper_gt_lower(self) -> MCapFilterSettings:
        """Validate that the upper bound is greater than the lower bound.

        Returns
        -------
        MCapFilterSettings
            The validated instance.

        Raises
        ------
        ValueError
            If the upper bound is not greater than the lower bound.
        """
        if (lower := self.lower) >= (upper := self.upper):
            raise ValueError(
                f"upper bound {upper} must be greater than lower bound {lower}",
            )
        else:
            return self


class UniverseSettingsMenu(SettingsMenu, frozen=True, extra="forbid"):
    """Contain the available settings that can be used for the universe settings."""

    calendar_settings_menu: CalendarSettingsMenu = Field(
        description="The calendar settings menu to use for the universe.",
    )

    id_types: list[IdType] = Field(
        description="""
        A list of all the id types that are supported for the universe.
        """,
    )

    categorical_hierarchies: Mapping[str, Hierarchy] = Field(
        description="""
        A dictionary where the key is the name of the categorical hierarchy (e.g. 'trbc')
        and the value is a N-level nested dictionary structure of the categorical hierarchy
        codes.
        """,
    )

    categorical_hierarchies_labels: Mapping[str, Mapping[str, str]] = Field(
        description="""
        A dictionary where the key is the name of the categorical hierarchy and
        the value is a mapping from unique categorical code to a human readable name.
        """,
    )

    @field_validator("categorical_hierarchies")
    @classmethod
    def check_unique_hierarchy(
        cls: type[UniverseSettingsMenu], v: Mapping[str, Hierarchy]
    ) -> Mapping[str, Hierarchy]:
        return settings_tools.check_unique_hierarchy(v)

    @field_validator("categorical_hierarchies")
    @classmethod
    def check_no_empty_branches(
        cls,
        v: Mapping[str, Mapping[str, Hierarchy]],
    ) -> Mapping[str, Mapping[str, Hierarchy]]:
        for hierarchy_name, hierarchy in v.items():
            if not hierarchy:  # different error message at root level
                raise ValueError(f"Hierarchy '{hierarchy_name}' cannot be empty")
            settings_tools.assert_no_empty_branches(hierarchy, hierarchy_name)
        return v

    @model_validator(mode="after")
    def check_all_codes_have_labels(self) -> UniverseSettingsMenu:
        if errors := settings_tools.check_all_codes_have_labels(
            self.categorical_hierarchies,
            self.categorical_hierarchies_labels,
        ):
            raise ValueError(os.linesep.join(errors))
        else:
            return self

    def describe(self) -> str:
        """Generate a human-readable description of the universe settings.

        Returns
        -------
        str
            A formatted description of the universe settings menu.
        """
        hierarchies = self.categorical_hierarchies
        labels = self.categorical_hierarchies_labels
        hierarchies_str = json.dumps(
            {
                k: settings_tools.codes_to_labels(hierarchies[k], labels[k])
                for k in hierarchies
            },
            indent=2,
        )
        id_types = ", ".join(self.id_types)
        description = [
            f"ID Types: {id_types}",
            "Hierarchies:",
            hierarchies_str,
        ]

        return os.linesep.join(description)

    def effective_categories(
        self,
        settings: CategoricalFilterSettings,
        labels: bool = False,
    ) -> list[str]:
        """Get the effective leaf level categorical codes after categorical filtering.

        Parameters
        ----------
        settings : CategoricalFilterSettings
            The filter settings to get the effective categorical codes for.
        labels : bool, default=False
            Whether to return the labels or the codes.

        Returns
        -------
        list[str]
            The effective leaf level categorical codes for the given settings after the
            filters were applied.
        """
        settings.validate_settings(self)
        effective_codes = settings_tools.effective_leaves(
            self.categorical_hierarchies[settings.hierarchy],
            settings.include,
            settings.exclude,
            self.categorical_hierarchies_labels[settings.hierarchy],
        )
        if labels:
            return [
                self.categorical_hierarchies_labels[settings.hierarchy][code]
                for code in effective_codes
            ]
        else:
            return effective_codes

    def hierarchy_df(self, hierarchy: str) -> pl.DataFrame:
        """Return a dataframe of the given categorical hierarchy.

        Parameters
        ----------
        hierarchy : str
            The name of the categorical hierarchy to return.

        Returns
        -------
        pl.DataFrame
            The wide DataFrame representation of the hierarchy. The columns are:
            - level_1: The code of the root level.
            - level_1_label: The label of the root level.
            - level_2: The code of the second level.
            - level_2_label: The label of the second level.
            - ...
            - level_n: The code of the n-th level.
            - level_n_label: The label of the n-th level.
        """
        return settings_tools.hierarchy_df_to_wide(
            self.categorical_hierarchies[hierarchy],
            self.categorical_hierarchies_labels[hierarchy],
        )


class UniverseSettings(Settings[UniverseSettingsMenu]):
    """Define an asset universe as a set of regional, industry and market cap filters."""

    dataset: str = Field(
        description=(
            "The name of the underlying dataset to use. If none is given then the "
            "configured default dataset is used."
        ),
        examples=["Bayesline-Global"],
    )

    id_type: IdType = Field(
        default="bayesid",
        description="The default id type to use for the universe.",
        examples=["cusip9", "bayesid"],
    )

    calendar: CalendarSettings = Field(
        default_factory=CalendarSettings,
        description="The calendar settings to use for the universe.",
    )

    categorical_filters: list[CategoricalFilterSettings] = Field(
        default_factory=list,
        description="""
        Filters that determine which categorical codes to include and exclude in the universe.
        """,
    )

    portfolio_filter: Annotated[
        str | int | PortfolioOrganizerSettings | None,
        Field(
            description=(
                "The portfolio organizer settings to use as an underlying schema of "
                "portfolios. Universe will be filtered across the superset of all "
                "portfolios."
            ),
            default=None,
        ),
        SettingsTypeMetaData[str | int | PortfolioOrganizerSettings](
            references=PortfolioOrganizerSettings
        ),
    ] = None

    mcap_filter: MCapFilterSettings = Field(
        default_factory=MCapFilterSettings,
        description="""
        Filters that determine which market caps to include and exclude in the universe.
        """,
    )

    @property
    def menu_type(self) -> type[UniverseSettingsMenu]:  # noqa: D102
        return UniverseSettingsMenu

    @field_validator("categorical_filters")
    @classmethod
    def check_unique_filters(
        cls: type[UniverseSettings], v: list[CategoricalFilterSettings]
    ) -> list[CategoricalFilterSettings]:
        factor_groups = [filter_settings.hierarchy for filter_settings in v]
        if len(factor_groups) != len(set(factor_groups)):
            raise ValueError("categorical_filters must reference unique hierarchies")
        return v

    @model_validator(mode="before")
    @classmethod
    def propagate_dataset(cls: type[UniverseSettings], data: Any) -> Any:
        if isinstance(data, dict) and "dataset" in data:
            if "calendar" not in data:
                data["calendar"] = {}
            if isinstance(data["calendar"], dict):
                if data["calendar"].get("dataset") is None:
                    data["calendar"]["dataset"] = data["dataset"]
        return data

    @field_validator("id_type", mode="after")
    @classmethod
    def validate_id_type(cls, id_type: IdType, info: ValidationInfo) -> IdType:
        if isinstance(menu := info.context, UniverseSettingsMenu):
            if id_type not in menu.id_types:
                raise ValueError(
                    f"Id type {id_type} does not exist. Only "
                    f"{', '.join(menu.id_types)} exist."
                )
        return id_type

    @field_validator("calendar", mode="after")
    @classmethod
    def validate_calendar(
        cls, calendar_settings: CalendarSettings, info: ValidationInfo
    ) -> CalendarSettings:
        if isinstance(menu := info.context, UniverseSettingsMenu):
            calendar_settings.validate_settings(menu.calendar_settings_menu)
        return calendar_settings

    @field_validator("categorical_filters", mode="after")
    @classmethod
    def validate_categorical_filters(
        cls, filter_settings: list[CategoricalFilterSettings], info: ValidationInfo
    ) -> list[CategoricalFilterSettings]:
        if isinstance(menu := info.context, UniverseSettingsMenu):
            for filter_setting in filter_settings:
                filter_setting.model_validate(filter_setting.model_dump(), context=menu)
        return filter_settings

    @field_validator("portfolio_filter", mode="after")
    @classmethod
    def validate_portfolio_filter(
        cls,
        portfolio_filter: str | int | PortfolioOrganizerSettings | None,
        info: ValidationInfo,
    ) -> str | int | PortfolioOrganizerSettings | None:
        if isinstance(portfolio_filter, PortfolioOrganizerSettings):
            dataset = info.data["dataset"]
            if portfolio_filter.dataset is None:
                portfolio_filter = portfolio_filter.model_copy(
                    update={"dataset": dataset}
                )
            if portfolio_filter.dataset != dataset:
                raise ValueError(
                    f"The dataset in the portfolio filter, {portfolio_filter.dataset} "
                    f"must match the dataset, {dataset}."
                )
        return portfolio_filter

    def describe(self, menu: UniverseSettingsMenu) -> str:
        """Describe the universe settings.

        Parameters
        ----------
        menu : UniverseSettingsMenu
            The settings menu to use to describe the settings.

        Returns
        -------
        str
            A description of the universe settings.
        """
        hierarchies = menu.categorical_hierarchies
        labels = menu.categorical_hierarchies_labels

        self.validate_settings(menu)  # TODO: needed?
        description = [f"Default ID Type: {self.id_type!r}"]

        for filter_settings in self.categorical_filters:
            hierarchy_name = filter_settings.hierarchy
            effective_hierarchy = settings_tools.effective_hierarchy(
                hierarchies[hierarchy_name],
                filter_settings.include,
                filter_settings.exclude,
                labels[hierarchy_name],
            )
            effective_hierarchy = settings_tools.codes_to_labels(
                effective_hierarchy, labels[hierarchy_name]
            )
            description.extend(
                [
                    f"Hierarchy ({hierarchy_name}):",
                    json.dumps(effective_hierarchy, indent=2),
                ]
            )

        description.extend(
            [
                "Market Cap:",
                self.mcap_filter.model_dump_json(indent=2),
            ]
        )
        return os.linesep.join(description)
