from __future__ import annotations

import json
import os
from collections.abc import Mapping
from typing import Annotated, Any, Literal, overload

import polars as pl
from pydantic import (
    BaseModel,
    BeforeValidator,
    Field,
    ValidationInfo,
    field_validator,
    model_validator,
)

from bayesline.api._src.equity import settings as settings_tools
from bayesline.api._src.equity.calendar_settings import CalendarSettingsMenu
from bayesline.api._src.equity.universe_settings import (
    CategoricalFilterSettings,
    UniverseSettings,
    UniverseSettingsMenu,
)
from bayesline.api._src.registry import Settings, SettingsMenu

Hierarchy = settings_tools.Hierarchy


def _ensure_list(value: Any) -> Any:
    if isinstance(value, list | tuple):
        return value
    return [value]


class HierarchyDescription(BaseModel, frozen=True, extra="forbid"):
    """Base class for hierarchy descriptions."""

    hierarchy_type: Literal["level", "groups"]
    name: str = Field(
        min_length=1,
        description="""
        The name of the hierarchy to use, e.g. 'trbc' or 'continent'.
        If it is not given then the default hierarchy will be used.
        """,
        examples=["trbc", "continent"],
    )

    def validate_hierarchy_description(self, menu: ExposureSettingsMenu | None) -> None:
        """Validate the hierarchy description.

        Parameters
        ----------
        menu : ExposureSettingsMenu | None
            The menu to validate against. If None, the hierarchy description is validated
            without having the menu context. This means that less validation is done.
        """
        self.model_validate(self.model_dump(), context=menu)


class HierarchyLevel(HierarchyDescription):
    """The hierarchy decscription for a level in the hierarchy.

    E.g. for industries specifying level `1` would
    create top level sector factors.
    """

    hierarchy_type: Literal["level"] = "level"
    level: int = Field(
        description="""The level of the hierarchy to use, e.g. 1
        to use all level 1 names (i.e. sectors for industries or
        continents for regions) or 2 to use all level 2
        names (i.e. sub-sectors for industries and
        countries for regions).
        """,
        default=1,
        examples=[1, 2],
        ge=1,
    )

    @field_validator("level", mode="after")
    @classmethod
    def check_valid_level(cls, level: int, info: ValidationInfo) -> int:
        if isinstance(menu := info.context, ExposureSettingsMenu):
            if (name := info.data["name"]) not in menu.hierarchies:
                raise ValueError(f"Hierarchy {name} does not exist")
            max_level = settings_tools.get_depth(menu.hierarchies[name])
            if level > max_level:
                raise ValueError(f"Illegal level {level}, maximum level is {max_level}")
        return level


class HierarchyGroups(HierarchyDescription):
    """The hierarchy decscription for a custom nested grouping of the hierarchy.

    The top level groupings will turn into factors, whereas any nested
    groupings will be retained for other uses (e.g. risk decomposition).
    """

    hierarchy_type: Literal["groups"] = "groups"
    groupings: Mapping[str, Hierarchy] = Field(  # at least two levels deep
        description="""
        A nested structure of groupings where the keys are the group names
        and the leaf level is a list of hierarchy codes or labels (at any level)
        to include for this group.
        """,
    )

    @field_validator("groupings", mode="after")
    @classmethod
    def check_valid_groupings(
        cls, groupings: Mapping[str, Hierarchy], info: ValidationInfo
    ) -> Mapping[str, Hierarchy]:
        settings_tools.check_unique_hierarchy(groupings)
        settings_tools.assert_no_empty_branches(groupings)
        leaves = settings_tools.flatten(groupings, only_leaves=True)
        if len(leaves) != len(set(leaves)):
            raise ValueError(
                "Groupings must be unique in the sense that no code or label occurs "
                "under any group name."
            )

        if isinstance(menu := info.context, ExposureSettingsMenu):
            # validation dependent on the hierarchy type
            leaves_without_prefix = [  # strip the ~ prefix from the leaves
                g[1:] if g.startswith("~") else g
                for g in settings_tools.flatten(groupings, only_leaves=True)
            ]
            if non_leaves_with_prefix := [
                g
                for g in (
                    set(settings_tools.flatten(groupings))
                    - set(settings_tools.flatten(groupings, only_leaves=True))
                )
                if g.startswith("~")
            ]:
                raise ValueError(
                    "Only leaves can have the exlude prefix ~. The following "
                    f"non-leaves have a ~ prefix: {', '.join(non_leaves_with_prefix)}."
                )
            if (name := info.data["name"]) not in menu.hierarchies:
                raise ValueError(f"Hierarchy {name} does not exist")
            effective_codes = settings_tools.labels_to_codes(  # prefix not resolved
                leaves_without_prefix, menu.hierarchies_labels[name]
            )
            available_codes = settings_tools.flatten(
                menu.hierarchies[name], only_leaves=False
            )
            if missing := set(effective_codes) - set(available_codes):
                raise ValueError(
                    "The following codes are in the hierarchy but not in the hierarchy "
                    f"groups: {', '.join(missing)}"
                )
        return groupings


def _hierarchy_name_to_hierarchy_level(
    v: HierarchyLevel | HierarchyGroups | str,
) -> HierarchyLevel | HierarchyGroups:
    # accept strings and turn them into a level-1 HierarchyLevel
    if isinstance(v, str):
        return HierarchyLevel(name=v, level=1)
    return v


HierarchyType = Annotated[
    HierarchyLevel | HierarchyGroups,
    Field(discriminator="hierarchy_type"),
    BeforeValidator(_hierarchy_name_to_hierarchy_level),
]


class BaseExposureGroupSettings(BaseModel, frozen=True, extra="forbid"):
    """Base class for exposure group settings."""

    def validate_exposure_group_settings(
        self, menu: ExposureSettingsMenu | None
    ) -> None:
        """Validate the exposure group settings.

        Parameters
        ----------
        menu : ExposureSettingsMenu | None
            The menu to validate against. If None, the exposure group settings is validated
            without having the menu context. This means that less validation is done.
        """
        self.model_validate(self.model_dump(), context=menu)


class ContinuousExposureGroupSettings(BaseExposureGroupSettings):
    """The settings for a continuous exposure group.

    Continuous exposures are exposures that are measured on a continuous scale,
    e.g. market, size, momentum, etc., and are typically available for most assets.
    """

    exposure_type: Literal["continuous"] = "continuous"
    hierarchy: Annotated[
        HierarchyType,
        Field(
            description=(
                "The hierarchy to use for the continuous exposures. This is either a"
                "HierarchyLevel or HierarchyGroups object. If a string is passed, the "
                "value is converted to a HierarchyLevel of that hierarchy with level=1."
            ),
            examples=[
                "market",
                HierarchyLevel(name="style", level=2),
                HierarchyGroups(
                    name="style",
                    groupings={
                        "momentum": ["mom6"],
                        "size": ["size"],
                    },
                ),
            ],
        ),
    ]
    factor_group: str = Field(
        "",  # temporary value that does not pass validation
        description=(
            "By default, the name of the factor group will be the name of the hierarchy. "
            "But we can override this by specifying an alias here."
        ),
        examples=["style", "some_style_group"],
    )
    include: Literal["All"] | list[str] = Field(
        default="All",
        description=(
            "Valid industry codes or labels for given hierarchy at any level. If "
            "labels are used which may be duplicated, then the code with the highest "
            "level is used. If 'All', all codes are included."
        ),
        examples=[["momentum"], "All", ["Size", "value"]],
    )
    exclude: list[str] = Field(
        default_factory=list,
        description=(
            "Valid industry codes or labels for given hierarchy at any level. If "
            "labels are used which may be duplicated, then the code with the lowest "
            "level is used."
        ),
        examples=[["momentum"], ["Size", "value"]],
    )
    standardize_method: Literal["none", "equal_weighted"] = Field(
        "none",
        description=(
            "The method to use for standardizing the exposures. If 'none', no "
            "standardization is applied. If 'equal_weighted', then the exposures are "
            "standardized with the mean and standard deviation of the estimation "
            "universe."
        ),
        examples=["none", "equal_weighted"],
    )

    @model_validator(mode="before")
    @classmethod
    def set_factor_group(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "factor_group" not in data or data["factor_group"] is None:
                if isinstance(data["hierarchy"], HierarchyLevel | HierarchyGroups):
                    data["factor_group"] = data["hierarchy"].name
                elif isinstance(data["hierarchy"], str):
                    data["factor_group"] = data["hierarchy"]
                else:
                    raise ValueError(
                        f"Invalid hierarchy type: {type(data['hierarchy'])}"
                    )
        return data

    @field_validator("factor_group")
    @classmethod
    def check_valid_factor_group(cls, v: str) -> str:
        if v == "":
            raise ValueError("factor_group cannot be empty")
        return v

    @model_validator(mode="after")
    def validate_filters(self, info: ValidationInfo) -> ContinuousExposureGroupSettings:
        if isinstance(menu := info.context, ExposureSettingsMenu):
            # validate that the hierarchies exist
            settings_tools.validate_hierarchy_schema(
                menu.continuous_hierarchies, self.hierarchy.name
            )
            # common validation
            settings_tools.validate_hierarchy_filters(
                menu.hierarchies[self.hierarchy.name],
                self.include,
                self.exclude,
                menu.hierarchies_labels[self.hierarchy.name],
            )
            # validate the hierarchy
            self.hierarchy.validate_hierarchy_description(menu)
        return self

    @property
    def hierarchies(self) -> list[HierarchyType]:
        """The list of hierarchies for the exposure group.

        Returns
        -------
        list[HierarchyType]
            The list of hierarchies for the exposure group.
        """
        return [self.hierarchy]

    def effective_exposure_group_factors(
        self,
        menu: ExposureSettingsMenu,
    ) -> list[str]:
        """Get the effective factors.

        Effective factors are the factors that are included and not excluded in the
        exposure group settings.

        Parameters
        ----------
        menu : ExposureSettingsMenu
            The menu to get the total factors from.

        Returns
        -------
        list[str]
            The list of effective factors.
        """
        return _effective_exposure_group_factors(self, menu)

    def normalize_group_settings(
        self,
        menu: ExposureSettingsMenu,
        universe_filter_dict: Mapping[str, CategoricalFilterSettings] | None,
    ) -> ContinuousExposureGroupSettings:
        """Normalize the exposure group settings.

        Normalized group settings have all hierarchies replaced by HierarchyGroups with
        two levels, the factor names and the leaf codes. All includes and excludes are
        resolved.

        This means that if the universe_filter_dict has a filter that trims down to just
        the North American region, and the ExposureSettings include factors from the
        same country hierarchy, then the factors will be trimmed down to just include
        the ones corresponding to the North American region.

        Parameters
        ----------
        menu : ExposureSettingsMenu
            The menu to get the total factors from.
        universe_filter_dict : Mapping[str, CategoricalFilterSettings] | None
            The universe filter dictionary to potentially further cut the factors down.
            The keys are the hierarchy names and the values are the filter settings.
            If None, then no filtering is performed.

        Returns
        -------
        ContinuousExposureGroupSettings
            The normalized exposure group settings.
        """
        return _normalize_group_settings(self, menu, universe_filter_dict)


class CategoricalExposureGroupSettings(BaseExposureGroupSettings):
    """The settings for a categorical exposure group.

    Categorical exposures are exposures to a categorical variable, e.g. industry,
    country, etc. For example, an asset exposure may be to a single industry factor,
    and we say the exposure is to the industry category factor "Materials". The exposure
    itself may be continuous (e.g. not 0.0 or 1.0), and an asset may be exposed to
    multiple industry factors (but typically not all of them). The distinction with
    continuous exposures is primarily in the settings that are available.
    """

    exposure_type: Literal["categorical"] = "categorical"
    hierarchy: Annotated[
        HierarchyType,
        Field(
            description=(
                "The hierarchy to use for the categorical exposures. This is either a"
                "HierarchyLevel or HierarchyGroups object. If a string is passed, the "
                "value is converted to a HierarchyLevel of that hierarchy with level=1."
            ),
            examples=[
                "trbc",
                HierarchyLevel(name="trbc", level=2),
                HierarchyGroups(
                    name="style",
                    groupings={
                        "MyGroup1": ["Energy"],
                        "MyGroup2": ["Materials", "Chemicals"],
                    },
                ),
            ],
        ),
    ]
    factor_group: str = Field(
        "",  # temporary value that does not pass validation
        description=(
            "By default, the name of the factor group will be the name of the hierarchy. "
            "But we can override this by specifying an alias here."
        ),
        examples=["industry", "some_country_group"],
    )
    include: Literal["All"] | list[str] = Field(
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

    @model_validator(mode="before")
    @classmethod
    def set_factor_group(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "factor_group" not in data or data["factor_group"] is None:
                if isinstance(data["hierarchy"], HierarchyLevel | HierarchyGroups):
                    data["factor_group"] = data["hierarchy"].name
                elif isinstance(data["hierarchy"], str):
                    data["factor_group"] = data["hierarchy"]
                else:
                    raise ValueError(
                        f"Invalid hierarchy type: {type(data['hierarchy'])}"
                    )
        return data

    @field_validator("factor_group")
    @classmethod
    def check_valid_factor_group(cls, v: str) -> str:
        if v == "":
            raise ValueError("factor_group cannot be empty")
        return v

    @model_validator(mode="after")
    def validate_filters(
        self, info: ValidationInfo
    ) -> CategoricalExposureGroupSettings:
        if isinstance(menu := info.context, ExposureSettingsMenu):
            # validate that the hierarchies exist
            settings_tools.validate_hierarchy_schema(
                menu.categorical_hierarchies, self.hierarchy.name
            )
            # common validation
            settings_tools.validate_hierarchy_filters(
                menu.hierarchies[self.hierarchy.name],
                self.include,
                self.exclude,
                menu.hierarchies_labels[self.hierarchy.name],
            )
            # validate the hierarchy
            self.hierarchy.validate_hierarchy_description(menu)
        return self

    @property
    def hierarchies(self) -> list[HierarchyType]:
        """The list of hierarchies for the exposure group.

        Returns
        -------
        list[HierarchyType]
            The list of hierarchies for the exposure group.
        """
        return [self.hierarchy]

    def effective_exposure_group_factors(
        self,
        menu: ExposureSettingsMenu,
    ) -> list[str]:
        """Get the effective factors.

        Effective factors are the factors that are included and not excluded in the
        exposure group settings.

        Parameters
        ----------
        menu : ExposureSettingsMenu
            The menu to get the total factors from.

        Returns
        -------
        list[str]
            The list of effective factors.
        """
        return _effective_exposure_group_factors(self, menu)

    def normalize_group_settings(  # same as ContinuousExposureGroupSettings
        self,
        menu: ExposureSettingsMenu,
        universe_filter_dict: Mapping[str, CategoricalFilterSettings] | None,
    ) -> CategoricalExposureGroupSettings:
        """Normalize the exposure group settings.

        Normalized group settings have all hierarchies replaced by HierarchyGroups with
        two levels, the factor names and the leaf codes. All includes and excludes are
        resolved.

        This means that if the universe_filter_dict has a filter that trims down to just
        the North American region, and the ExposureSettings include factors from the
        same country hierarchy, then the factors will be trimmed down to just include
        the ones corresponding to the North American region.

        Parameters
        ----------
        menu : ExposureSettingsMenu
            The menu to get the total factors from.
        universe_filter_dict : Mapping[str, CategoricalFilterSettings] | None
            The universe filter dictionary to potentially further cut the factors down.
            The keys are the hierarchy names and the values are the filter settings.
            If None, then no filtering is performed.

        Returns
        -------
        CategoricalExposureGroupSettings
            The normalized exposure group settings.
        """
        return _normalize_group_settings(self, menu, universe_filter_dict)


class InteractionExposureGroupSettings(
    BaseExposureGroupSettings, frozen=True, extra="forbid"
):
    """The settings for an interaction exposure group.

    Interaction exposures are exposures that are a combination of two or more
    exposure groups. For example, we may want to create industry-specific style factors.
    """

    exposure_type: Literal["interaction"] = "interaction"
    exposure_groups: list[
        ContinuousExposureGroupSettings | CategoricalExposureGroupSettings
    ] = Field(
        [],
        description="The exposure groups to use for the Cartesian product.",
        min_length=2,
    )
    factor_group: str = Field(
        "",  # temporary value that does not pass validation
        description=(
            "By default, the name of the factor group will be a concatenation of the "
            "names of the exposure groups separated by the a colon."
        ),
        examples=["industry:style"],
    )

    @model_validator(mode="before")
    @classmethod
    def set_factor_group(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "factor_group" not in data or data["factor_group"] is None:
                factor_groups = [g.factor_group for g in data["exposure_groups"]]
                data["factor_group"] = ":".join(factor_groups)
        return data

    @field_validator("factor_group")
    @classmethod
    def check_valid_factor_group(cls, v: str) -> str:
        if v == "":
            raise ValueError("factor_group cannot be empty")
        return v

    @field_validator("exposure_groups", mode="after")
    @classmethod
    def validate_exposure_groups(
        cls, v: list[ExposureGroupSettings], info: ValidationInfo
    ) -> list[ExposureGroupSettings]:
        if isinstance(menu := info.context, ExposureSettingsMenu):
            for group_settings in v:
                group_settings.validate_exposure_group_settings(menu)
        return v

    @property
    def hierarchies(self) -> list[HierarchyType]:
        """The list of hierarchies for the exposure group.

        Returns
        -------
        list[HierarchyType]
            The list of hierarchies for the exposure group.
        """
        return [h for g in self.exposure_groups for h in g.hierarchies]

    def effective_exposure_group_factors(
        self,
        menu: ExposureSettingsMenu,
    ) -> list[str]:
        """Get the effective factors.

        Effective factors are the factors that are included and not excluded in the
        exposure group settings.

        Parameters
        ----------
        menu : ExposureSettingsMenu
            The menu to get the total factors from.

        Returns
        -------
        list[str]
            The list of effective factors.
        """
        return [
            f
            for g in self.exposure_groups
            for f in g.effective_exposure_group_factors(menu)
        ]

    def normalize_group_settings(
        self,
        menu: ExposureSettingsMenu,
        universe_filter_dict: Mapping[str, CategoricalFilterSettings] | None,
    ) -> InteractionExposureGroupSettings:
        """Normalize the exposure group settings.

        Normalized group settings have all hierarchies replaced by HierarchyGroups with
        two levels, the factor names and the leaf codes. All includes and excludes are
        resolved.

        This means that if the universe_filter_dict has a filter that trims down to just
        the North American region, and the ExposureSettings include factors from the
        same country hierarchy, then the factors will be trimmed down to just include
        the ones corresponding to the North American region.

        Parameters
        ----------
        menu : ExposureSettingsMenu
            The menu to get the total factors from.
        universe_filter_dict : Mapping[str, CategoricalFilterSettings] | None
            The universe filter dictionary to potentially further cut the factors down.
            The keys are the hierarchy names and the values are the filter settings.
            If None, then no filtering is performed.

        Returns
        -------
        InteractionExposureGroupSettings
            The normalized exposure group settings.
        """
        return self.model_copy(
            update={
                "exposure_groups": [
                    exposure_group.normalize_group_settings(menu, universe_filter_dict)
                    for exposure_group in self.exposure_groups
                ]
            },
            deep=True,
        )


ExposureGroupSettings = Annotated[
    ContinuousExposureGroupSettings
    | CategoricalExposureGroupSettings
    | InteractionExposureGroupSettings,
    Field(discriminator="exposure_type"),
]


def _normalize_hierarchy(
    hierarchy: HierarchyLevel | HierarchyGroups,
    reference_hierarchy: Hierarchy,
    reference_labels: Mapping[str, str],
) -> HierarchyGroups:
    groupings: dict[str, list[str]] = {}
    if isinstance(hierarchy, HierarchyLevel):
        keys = settings_tools.flatten(
            settings_tools.trim_to_depth(reference_hierarchy, hierarchy.level),
            only_leaves=True,
        )
        for k in keys:
            sub_hierarchy = settings_tools.find_in_hierarchy(reference_hierarchy, k)
            if sub_hierarchy is not None:
                k = reference_labels.get(k, k)  # convert top level to label if possible
                groupings[k] = settings_tools.flatten(
                    sub_hierarchy,
                    only_leaves=True,
                )
    else:  # HierarchyGroups
        for k, v in hierarchy.groupings.items():
            groupings[k] = []
            # v is a Hierarchy, first map the codes to labels (with ~ prefix)
            v = settings_tools.labels_to_codes(v, reference_labels, prefix="~")
            # then process the excludes
            v = settings_tools.process_excludes(v, reference_hierarchy)
            # then flatten the hierarchy
            for code in v:
                sub_hierarchy = settings_tools.find_in_hierarchy(
                    reference_hierarchy, code
                )
                if sub_hierarchy is not None:
                    groupings[k].extend(
                        settings_tools.flatten(sub_hierarchy, only_leaves=True)
                    )
    return HierarchyGroups(name=hierarchy.name, groupings=groupings)


def _effective_exposure_group_factors(
    delegate: ContinuousExposureGroupSettings | CategoricalExposureGroupSettings,
    menu: ExposureSettingsMenu,
) -> list[str]:
    delegate.validate_exposure_group_settings(menu)
    hierarchy_name = delegate.hierarchy.name
    hierarchy_groups = _normalize_hierarchy(
        delegate.hierarchy,
        menu.hierarchies[hierarchy_name],
        menu.hierarchies_labels[hierarchy_name],
    )
    # filter based on include and exclude
    effective_groupings = settings_tools.effective_hierarchy(
        hierarchy_groups.groupings,
        delegate.include,
        delegate.exclude,
        menu.hierarchies_labels[hierarchy_name],
    )
    # just return the keys of effective_groupings
    return list(effective_groupings)


@overload
def _normalize_group_settings(
    delegate: ContinuousExposureGroupSettings,
    menu: ExposureSettingsMenu,
    universe_filter_dict: Mapping[str, CategoricalFilterSettings] | None,
) -> ContinuousExposureGroupSettings: ...


@overload
def _normalize_group_settings(
    delegate: CategoricalExposureGroupSettings,
    menu: ExposureSettingsMenu,
    universe_filter_dict: Mapping[str, CategoricalFilterSettings] | None,
) -> CategoricalExposureGroupSettings: ...


def _normalize_group_settings(
    delegate: ContinuousExposureGroupSettings | CategoricalExposureGroupSettings,
    menu: ExposureSettingsMenu,
    universe_filter_dict: Mapping[str, CategoricalFilterSettings] | None,
) -> ContinuousExposureGroupSettings | CategoricalExposureGroupSettings:
    # first normalize the hierarchy to Mapping[str, list[str]] with all leaf codes
    name = delegate.hierarchy.name
    hierarchy_groups = _normalize_hierarchy(
        delegate.hierarchy,
        menu.hierarchies[name],
        menu.hierarchies_labels[name],
    )
    # filter based on include and exclude
    new_groupings = settings_tools.effective_hierarchy(
        hierarchy_groups.groupings,
        delegate.include,
        delegate.exclude,
        menu.hierarchies_labels[name],
    )
    hierarchy_groups = hierarchy_groups.model_copy(
        update={"groupings": new_groupings}, deep=True
    )
    if universe_filter_dict:
        # filter the hierarchy groupings down if the universe has filters
        if name in universe_filter_dict:  # filter the hierarchy groupings down
            filter_settings = universe_filter_dict[name]
            effective_leaves = settings_tools.effective_leaves(
                menu.hierarchies[name],
                filter_settings.include,
                filter_settings.exclude,
                menu.hierarchies_labels[name],
            )
            new_groupings = {
                k: filtered_leaves
                for k, v in hierarchy_groups.groupings.items()
                if (filtered_leaves := [w for w in v if w in effective_leaves])
            }
            hierarchy_groups = hierarchy_groups.model_copy(
                update={"groupings": new_groupings}, deep=True
            )

    # normalized group settings should not have includes / excludes
    return delegate.model_copy(
        update={"hierarchy": hierarchy_groups, "include": "All", "exclude": []},
        deep=True,
    )


class ExposureSettingsMenu(SettingsMenu, frozen=True, extra="forbid"):
    """Contains the available settings that can be used to define exposures."""

    universe_settings_menu: UniverseSettingsMenu = Field(
        description="The universe settings menu to use to define the exposures.",
    )

    continuous_hierarchies: Mapping[str, Hierarchy] = Field(
        description="""
        A dictionary where the key is the name of the continuous hierarchy (e.g. 'style')
        and the value is a N-level nested dictionary structure of the continuous hierarchy
        codes.
        """,
    )

    continuous_hierarchies_labels: Mapping[str, Mapping[str, str]] = Field(
        description="""
        A dictionary where the key is the name of the continuous hierarchy and
        the value is a mapping from unique continuous code to a human readable name.
        """,
    )

    @property
    def calendar_settings_menu(self) -> CalendarSettingsMenu:
        """The calendar settings menu from the universe settings menu.

        Returns
        -------
        CalendarSettingsMenu
            The calendar settings menu from the universe settings menu.
        """
        return self.universe_settings_menu.calendar_settings_menu

    @property
    def categorical_hierarchies(self) -> Mapping[str, Hierarchy]:
        """
        The categorical hierarchies from the universe settings menu.

        Returns
        -------
        Mapping[str, Hierarchy]
            A dictionary where the key is the name of the categorical hierarchy (e.g. 'trbc')
            and the value is a N-level nested dictionary structure of the categorical hierarchy
            codes.
        """
        return self.universe_settings_menu.categorical_hierarchies

    @property
    def categorical_hierarchies_labels(self) -> Mapping[str, Mapping[str, str]]:
        """
        The categorical hierarchies labels from the universe settings menu.

        Returns
        -------
        Mapping[str, Mapping[str, str]]
            A dictionary where the key is the name of the categorical hierarchy and
            the value is a mapping from unique categorical code to a human readable name.
        """
        return self.universe_settings_menu.categorical_hierarchies_labels

    @property
    def hierarchies(self) -> Mapping[str, Hierarchy]:
        """The combined hierarchies from the continuous and categorical hierarchies.

        Returns
        -------
        Mapping[str, Hierarchy]
            A dictionary where the key is the name of the hierarchy and
            the value is the hierarchy.
        """
        return {**self.continuous_hierarchies, **self.categorical_hierarchies}

    @property
    def hierarchies_labels(self) -> Mapping[str, Mapping[str, str]]:
        """The combined hierarchies labels from the continuous and categorical hierarchies.

        Returns
        -------
        Mapping[str, Mapping[str, str]]
            A dictionary where the key is the name of the hierarchy and
            the value is a mapping from unique code to a human readable name.
        """
        return {
            **self.continuous_hierarchies_labels,
            **self.categorical_hierarchies_labels,
        }

    def describe(self) -> str:
        """Describe the exposure settings menu.

        Returns
        -------
        str
            The description of the exposure settings menu.
        """
        # only describe continuous hierarchies for now
        hierarchies = self.continuous_hierarchies
        labels = self.continuous_hierarchies_labels

        hierarchies_str = json.dumps(
            {
                k: settings_tools.codes_to_labels(hierarchies[k], labels[k])
                for k in hierarchies
            },
            indent=2,
        )
        description = [
            "Hierarchies:",
            hierarchies_str,
        ]

        return os.linesep.join(description)

    @field_validator("continuous_hierarchies")
    @classmethod
    def check_unique_hierarchy(
        cls, v: Mapping[str, Hierarchy]
    ) -> Mapping[str, Hierarchy]:
        return settings_tools.check_unique_hierarchy(v)

    @field_validator("continuous_hierarchies")
    @classmethod
    def check_no_empty_branches(
        cls, v: Mapping[str, Hierarchy]
    ) -> Mapping[str, Hierarchy]:
        for hierarchy_name, hierarchy in v.items():
            if not hierarchy:  # different error message at root level
                raise ValueError(f"Hierarchy '{hierarchy_name}' cannot be empty")
            settings_tools.assert_no_empty_branches(hierarchy, hierarchy_name)
        return v

    @model_validator(mode="after")
    def check_all_codes_have_labels(self) -> ExposureSettingsMenu:
        if errors := settings_tools.check_all_codes_have_labels(
            self.hierarchies, self.hierarchies_labels
        ):
            raise ValueError(os.linesep.join(errors))
        else:
            return self

    def hierarchy_df(self, hierarchy: str) -> pl.DataFrame:
        """Return a dataframe of the given hierarchy.

        Parameters
        ----------
        hierarchy: str
            the name of the hierarchy to return.

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
            self.hierarchies[hierarchy], self.hierarchies_labels[hierarchy]
        )


class ExposureSettings(Settings[ExposureSettingsMenu]):
    """Defines exposures as hierarchy of selected styles and substyles."""

    exposures: Annotated[
        list[ExposureGroupSettings],
        BeforeValidator(_ensure_list),
        Field(
            description="The exposures to build the factor risk model on.",
        ),
    ] = []

    @property
    def menu_type(self) -> type[ExposureSettingsMenu]:  # noqa: D102
        return ExposureSettingsMenu

    def describe(self, menu: ExposureSettingsMenu) -> str:
        """Describe the exposure settings.

        Parameters
        ----------
        menu : ExposureSettingsMenu
            The menu to get context information from.

        Returns
        -------
        str
            The description of the exposure settings.
        """
        # only describe continuous hierarchies for now
        hierarchies = menu.continuous_hierarchies
        labels = menu.continuous_hierarchies_labels

        self.validate_settings(menu)  # TODO: needed?
        self_normalized = self.normalize(None, menu)
        description = []
        for group_settings in self_normalized.exposures:
            if group_settings.exposure_type == "continuous":  # only continuous
                hierarchy_name = group_settings.hierarchy.name
                hierarchy = settings_tools.codes_to_labels(
                    hierarchies[hierarchy_name], labels[hierarchy_name]
                )
                description.extend(
                    [
                        f"Hierarchy ({hierarchy_name}):",
                        json.dumps(hierarchy, indent=2),
                    ]
                )
        return os.linesep.join(description)

    @field_validator("exposures", mode="after")
    @classmethod
    def validate_exposure_groups(
        cls, exposures: list[ExposureGroupSettings], info: ValidationInfo
    ) -> list[ExposureGroupSettings]:
        if isinstance(menu := info.context, ExposureSettingsMenu):
            factor_dict: dict[str, list[str]] = {}  # collect factors per factor_group
            for group_settings in exposures:
                group_settings.validate_exposure_group_settings(menu)
                factor_dict.setdefault(group_settings.factor_group, []).extend(
                    group_settings.effective_exposure_group_factors(menu)
                )
            # check that output factor_group-factor combinations are unique
            settings_tools.check_unique_hierarchy(factor_dict)

        return exposures

    def normalize(
        self,
        universe_settings: UniverseSettings | None,
        exposure_settings_menu: ExposureSettingsMenu,
    ) -> ExposureSettings:
        """Normalize the given exposure settings.

        Normalize the given exposure settings by converting all exposure hierarchies
        to a HierarchyGroups object, and then filtering the hierarchy groupings based
        on the include and exclude statements in the exposure settings, and possibly
        the universe filters.

        This means that if the UniverseSettings have a filter that trims down to just
        the North American region, and the ExposureSettings include factors from the
        same country hierarchy, then the factors will be trimmed down to just include
        the ones corresponding to the North American region.

        Parameters
        ----------
        universe_settings: UniverseSettings | None
            the universe settings to use for normalization. If None, then no
            normalization is performed in relation to the filters in the universe.
        exposure_settings_menu: ExposureSettingsMenu
            The menu to get the total factors from.

        Returns
        -------
        ExposureSettings
            A new exposure settings object with all exposure hierarchies converted to
            HierarchyGroups objects, and the hierarchy groupings filtered based on the
            include and exclude statements in the exposure settings, and possibly the
            universe filters. This normalized object is also validated.
        """
        if universe_settings:
            universe_filter_dict = {
                filter_settings.hierarchy: filter_settings  # hierarchy is unique
                for filter_settings in universe_settings.categorical_filters
            }
        else:
            universe_filter_dict = None

        self_normalized = self.model_copy(
            update={
                "exposures": [
                    group_settings.normalize_group_settings(
                        exposure_settings_menu, universe_filter_dict
                    )
                    for group_settings in self.exposures
                ]
            },
            deep=True,
        )

        # we may have produced an invalid settings object with the copy/update calls
        # so we need to validate again (validate_settings does pydantic validation)
        self_normalized.validate_settings(exposure_settings_menu)

        return self_normalized
