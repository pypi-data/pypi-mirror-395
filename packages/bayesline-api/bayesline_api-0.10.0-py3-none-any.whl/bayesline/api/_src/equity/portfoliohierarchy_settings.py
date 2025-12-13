from __future__ import annotations

from collections import Counter
from itertools import pairwise
from typing import Annotated, Any

import polars as pl
from pydantic import Field, ValidationInfo, field_validator, model_validator

from bayesline.api._src.equity.portfolio_settings import PortfolioOrganizerSettings
from bayesline.api._src.registry import Settings, SettingsMenu, SettingsTypeMetaData


class PortfolioHierarchySettingsMenu(SettingsMenu, frozen=True, extra="forbid"):
    """Specifies the set of available portfolios that can be used to create hierarchies."""

    sources: dict[str, list[str]] = Field(
        default_factory=dict,
        description=(
            "Mapping of sources to the available portfolio IDs for that source."
        ),
    )

    schemas: dict[str, list[str]] = Field(
        default_factory=dict,
        description=(
            "Set of available portfolio organizer schemas and their "
            "associated portfolio IDs."
        ),
    )

    def describe(self) -> str:
        """Describe the available portfolio schemas.

        Returns
        -------
        str
            A description of the available portfolio schemas.
        """
        sources = {k: sorted(v) for k, v in self.sources.items()}
        schemas = {k: sorted(v) for k, v in self.schemas.items()}
        return f"Available Portfolio Sources: {sources}\nAvailable Portfolio Schemas: {schemas}"


class PortfolioHierarchySettings(Settings[PortfolioHierarchySettingsMenu]):
    """Specifies portfolio hierarchies with arbitrary groupings (e.g. manager, etc.)."""

    portfolio_schema: Annotated[
        str | int | PortfolioOrganizerSettings,
        Field(
            description=(
                "The portfolio organizer settings to use as an underlying schema of "
                "portfolios. The 'Default' schema is used by default."
            ),
        ),
        SettingsTypeMetaData[str | int | PortfolioOrganizerSettings](
            references=PortfolioOrganizerSettings
        ),
    ]

    groupings: dict[str, list[str]] = Field(default_factory=dict)
    portfolio_ids: list[str]
    benchmark_ids: list[str | None]

    @property
    def menu_type(self) -> type[PortfolioHierarchySettingsMenu]:  # noqa: D102
        return PortfolioHierarchySettingsMenu

    @classmethod
    def from_source(
        cls: type[PortfolioHierarchySettings],
        source: str,
        portfolio_ids: list[str],
        benchmark_ids: list[str | None] | None = None,
        groupings: dict[str, list[str]] | None = None,
        dataset: str | None = None,
    ) -> PortfolioHierarchySettings:
        """Create portfolio hierarchy settings from a source.

        Parameters
        ----------
        source : str
            The name of an upload from the portfolio uploader.
        portfolio_ids : list[str]
            The list of portfolio IDs.
        benchmark_ids : list[str | None] | None, default=None
            The list of benchmark IDs, defaults to None for each portfolio.
        groupings : dict[str, list[str]] | None, default=None
            The groupings dictionary, defaults to empty dict.
        dataset : str | None, default=None
            The risk dataset to use for the security master and asset returns. If None,
            the default dataset is used.

        Returns
        -------
        PortfolioHierarchySettings
            The created portfolio hierarchy settings.
        """
        return cls(
            portfolio_schema=PortfolioOrganizerSettings(
                enabled_portfolios=source, dataset=dataset
            ),
            portfolio_ids=portfolio_ids,
            benchmark_ids=benchmark_ids or [None] * len(portfolio_ids),
            groupings=groupings or {},
        )

    @classmethod
    def from_polars(
        cls: type[PortfolioHierarchySettings],
        df: pl.DataFrame,
        portfolio_schema: str | int | PortfolioOrganizerSettings = "Default",
        portfolio_source: str | None = None,
        dataset: str | None = None,
    ) -> PortfolioHierarchySettings:
        """Create a portfolio hierarchy from a dataframe.

        Must contain a column `portfolio_id` and optionally `benchmark_id`.
        Every other column is interpreted as a grouping. 0 groupings are allowed.
        Index is ignored.

        Parameters
        ----------
        df : pl.DataFrame
            The dataframe to create the hierarchy from.
        portfolio_schema : str | int | PortfolioOrganizerSettings, default="Default"
            The underlying portfolio schema to use.
        portfolio_source : str | None, default=None
            The source to use for the portfolio schema. If not provided then
            the portfolio schema is used. If provided then it will override the
            portfolio schema.
        dataset : str | None, default=None
            The dataset to use for the portfolio schema. If not provided then
            the default dataset is used. Will be ignored if `source` is not
            provided.

        Returns
        -------
        PortfolioHierarchySettings
            The created portfolio hierarchy settings.

        Raises
        ------
        ValueError
            If the portfolio_id column is not found in the dataframe.
        """
        if "portfolio_id" not in df.columns:
            raise ValueError("portfolio_id column not found in the dataframe.")

        groupings = {
            col: df.get_column(col).to_list()
            for col in df.columns
            if col not in {"portfolio_id", "benchmark_id"}
        }
        portfolio_ids = df.get_column("portfolio_id").to_list()

        if "benchmark_id" not in df.columns:
            benchmark_ids = [None] * len(portfolio_ids)
        else:
            benchmark_ids = df.get_column("benchmark_id").to_list()

        if portfolio_source is not None:
            portfolio_schema = PortfolioOrganizerSettings(
                enabled_portfolios=portfolio_source, dataset=dataset
            )

        return cls(
            portfolio_schema=portfolio_schema,
            groupings=groupings,
            portfolio_ids=portfolio_ids,
            benchmark_ids=benchmark_ids,
        )

    def to_polars(self) -> pl.DataFrame:
        """Convert the hierarchy to a polars dataframe.

        The last two columns are the portfolio and benchmark IDs.
        Every column before that is a grouping. 0 groupings are possible.

        Returns
        -------
        pl.DataFrame
            The dataframe representation of the hierarchy, sorted by portfolio ID.
        """
        return pl.DataFrame(self.groupings).with_columns(
            pl.Series("portfolio_id", self.portfolio_ids),
            pl.Series("benchmark_id", self.benchmark_ids),
        )

    @field_validator("portfolio_ids")
    @classmethod
    def _validate_portfolio_ids(
        cls: type[PortfolioHierarchySettings], v: list[str]
    ) -> list[str]:
        if not v:
            raise ValueError("Portfolio IDs must be non-empty.")

        duplicates = [item for item, count in Counter(v).items() if count > 1]
        if duplicates:
            raise ValueError(
                "Portfolio IDs must be unique. "
                f"Found duplicates: {', '.join(duplicates)}"
            )

        if any(p is None or p.strip() == "" for p in v):
            raise ValueError("Portfolio IDs must be non-empty strings.")

        return v

    @field_validator("portfolio_ids")
    @classmethod
    def _validate_benchmark_ids(
        cls: type[PortfolioHierarchySettings], v: list[str]
    ) -> list[str]:
        if not v:
            raise ValueError("Benchmark IDs must be non-empty.")
        return v

    @field_validator("groupings")
    @classmethod
    def _validate_groupings(
        cls: type[PortfolioHierarchySettings], v: dict[str, list[str]]
    ) -> dict[str, list[str]]:
        if not all(len(v1) == len(v2) for v1, v2 in pairwise(v.values())):
            raise ValueError(f"Groupings must have the same length. {v}")

        groups_with_nulls = []
        for group, values in v.items():
            if any(e is None for e in values):
                groups_with_nulls.append(group)
        if groups_with_nulls:
            raise ValueError(
                f"Groupings must not contain null values. Found in: {groups_with_nulls}"
            )

        return v

    @model_validator(mode="before")
    @classmethod
    def _fill_benchmark_ids(cls: type[PortfolioHierarchySettings], v: Any) -> Any:
        if isinstance(v, dict):
            if "benchmark_ids" not in v or v["benchmark_ids"] is None:
                v["benchmark_ids"] = [None] * len(v["portfolio_ids"])
        return v

    @model_validator(mode="after")
    def _validate_dimensions(self) -> PortfolioHierarchySettings:
        if len(self.portfolio_ids) != len(self.benchmark_ids):
            raise ValueError(
                "Portfolio IDs and benchmark IDs must have the same length."
            )

        n = len(self.portfolio_ids)
        mismatches = [g for g in self.groupings.values() if len(g) != n]
        if len(mismatches) > 0:
            raise ValueError(
                "Portfolio IDs, benchmark IDs and groups must have the same length. "
                f"Found mismatches: {mismatches}"
            )
        return self

    @field_validator("portfolio_schema", mode="after")
    @classmethod
    def _validate_portfolio_schema(
        cls,
        portfolio_schema: str | int | PortfolioOrganizerSettings,
        info: ValidationInfo,
    ) -> str | int | PortfolioOrganizerSettings:
        if isinstance(menu := info.context, PortfolioHierarchySettingsMenu):
            if (
                isinstance(portfolio_schema, str)
                and portfolio_schema not in menu.schemas
            ):
                raise ValueError(
                    f"Unknown schema: {portfolio_schema}, available: {menu.schemas.keys()}"
                )
        return portfolio_schema

    @model_validator(mode="after")
    def _validate_ids_with_rest(
        self, info: ValidationInfo
    ) -> PortfolioHierarchySettings:
        if isinstance(menu := info.context, PortfolioHierarchySettingsMenu):
            if isinstance(self.portfolio_schema, str):
                available_portfolio_ids = set(menu.schemas[self.portfolio_schema])
                available_portfolio_ids_with_rest = {
                    n.split(":")[0] + ":{REST}"
                    for n in available_portfolio_ids
                    if ":" in n
                } | available_portfolio_ids
                portfolio_ids = set(self.portfolio_ids)
                benchmark_ids = {b for b in self.benchmark_ids if b is not None}

                if not portfolio_ids.issubset(available_portfolio_ids_with_rest):
                    raise ValueError(
                        f"There are unknown portfolio ids. "
                        f"Unknown: {portfolio_ids - available_portfolio_ids}"
                    )

                if not benchmark_ids.issubset(available_portfolio_ids):
                    raise ValueError(
                        f"There are unknown benchmark ids. "
                        f"Unknown: {benchmark_ids - available_portfolio_ids}"
                    )
        return self

    def describe(self, menu: PortfolioHierarchySettingsMenu) -> str:
        """Describe the portfolio hierarchy settings.

        Parameters
        ----------
        menu : PortfolioHierarchySettingsMenu
            The menu to get context information from.

        Returns
        -------
        str
            The description of the portfolio hierarchy settings.
        """
        schema = self.portfolio_schema
        if isinstance(schema, str) and schema not in menu.schemas:
            return f"Unknown schema: {schema}"

        df = self.to_polars()
        if isinstance(schema, str):
            df = df.with_columns(
                pl.col("portfolio_id").map_elements(
                    lambda x: f"[{x}]" if x not in menu.schemas[schema] else x,
                    pl.String,
                ),
                pl.col("benchmark_id").map_elements(
                    lambda x: (
                        f"[{x}]"
                        if x is not None and x not in menu.schemas[schema]
                        else x
                    ),
                    pl.String,
                ),
            )
            return f"""Missing portfolios are enclosed in brackets.

{df.__repr__()}"""
        else:
            return df.__repr__()
