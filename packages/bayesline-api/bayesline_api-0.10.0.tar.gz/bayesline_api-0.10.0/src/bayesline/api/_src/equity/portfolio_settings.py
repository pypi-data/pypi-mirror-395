from typing import Annotated, Literal

from pydantic import Field, ValidationInfo, field_validator

from bayesline.api._src.registry import Settings, SettingsMenu, SettingsTypeMetaData


class PortfolioOrganizerSettingsMenu(SettingsMenu, frozen=True, extra="forbid"):
    """Menu for portfolio organizer settings.

    This class provides a menu interface for managing portfolio organizer settings
    and available portfolio sources.
    """

    sources: dict[str, list[str]] = Field(
        description=(
            "Mapping of sources to the available portfolio IDs for that source."
        )
    )

    def describe(self) -> str:
        """Describe the available sources.

        Returns
        -------
        str
            A description of the available sources.
        """
        return f"Sources: {self.sources}"


class PortfolioOrganizerSettings(Settings[PortfolioOrganizerSettingsMenu]):
    """
    Specifies which portfolios to enable (from different sources).

    Different sources (e.g. uploaded portfolios) can provide the same portfolio
    identifiers. These settings allow to specify which portfolios to enable from
    which sources.
    """

    dataset: str | None = Field(
        default=None,
        description=(
            "The name of the underlying dataset to use for price data needed to "
            "forward fill portfolios, obtain corporate actions, etc."
            "If none is given then the configured default dataset is used."
        ),
        examples=["Bayesline-US"],
    )

    enabled_portfolios: str | dict[str, str] = Field(
        description=(
            "The enabled portfolios from different sources. "
            "The key is the portfolio ID, and the value is the source "
            "(name of the underlying portfolio service). "
            "Pass a str to reference an entire portfolio source (e.g. all portfolios "
            "from an upload)."
        ),
    )

    @property
    def menu_type(self) -> type[PortfolioOrganizerSettingsMenu]:  # noqa: D102
        return PortfolioOrganizerSettingsMenu

    @field_validator("enabled_portfolios")
    @classmethod
    def validate_enabled_portfolios(
        cls, enabled_portfolios: str | dict[str, str], info: ValidationInfo
    ) -> str | dict[str, str]:
        if isinstance(menu := info.context, PortfolioOrganizerSettingsMenu):
            messages = []
            if isinstance(enabled_portfolios, str):
                if enabled_portfolios not in menu.sources:
                    messages.append(
                        f"Invalid source: {enabled_portfolios}. "
                        f"Available sources: {', '.join(menu.sources.keys())}. "
                    )
            else:
                for portfolio_id, source in enabled_portfolios.items():
                    if source not in menu.sources:
                        messages.append(
                            f"Invalid source: {source}. "
                            f"Available sources: {', '.join(menu.sources.keys())}. "
                        )
                    elif portfolio_id not in menu.sources[source]:
                        messages.append(
                            f"Invalid portfolio ID: {portfolio_id} for source {source}. "
                        )
            if messages:
                raise ValueError("".join(messages))
        return enabled_portfolios

    def describe(self, menu: PortfolioOrganizerSettingsMenu) -> str:
        """Describe the settings.

        Parameters
        ----------
        menu : PortfolioOrganizerSettingsMenu
            The menu to get context information from.

        Returns
        -------
        str
            A description of the settings.
        """
        del menu  # not used
        return f"Enabled Portfolios: {self.enabled_portfolios}"


class PortfolioSettingsMenu(SettingsMenu, frozen=True, extra="forbid"):
    """Specifies the set of available options that can be used to create portfolio settings."""

    sources: list[str] = Field(
        description=(
            "The available sources (i.e. user uploaded portfolios or system "
            "uploaded portfolios)."
        ),
        default_factory=list,
    )

    schemas: list[str] = Field(
        description=(
            "The available schemas (i.e. names from the portfolio organizer)."
        ),
        default_factory=list,
    )

    def describe(self) -> str:
        """Describe the available options.

        Returns
        -------
        str
            A description of the available options.
        """
        return (
            f"Sources: {', '.join(self.sources)}\n"
            f"Schemas: {', '.join(self.schemas)}\n"
            "Forward Fill Options: 'no-ffill', 'ffill-with-drift'\n"
            "Unpack Options: 'no-unpack', 'unpack"
        )


class PortfolioSettings(Settings[PortfolioSettingsMenu]):
    """Specifies different options of obtaining portfolios."""

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
    ffill: Literal["no-ffill", "ffill-with-drift"] = "no-ffill"
    unpack: Literal["no-unpack", "unpack"] = "no-unpack"

    @property
    def menu_type(self) -> type[PortfolioSettingsMenu]:  # noqa: D102
        return PortfolioSettingsMenu

    @classmethod
    def from_source(
        cls: type["PortfolioSettings"],
        source: str,
        ffill: Literal["no-ffill", "ffill-with-drift"] = "no-ffill",
        unpack: Literal["no-unpack", "unpack"] = "no-unpack",
        dataset: str | None = None,
    ) -> "PortfolioSettings":
        """Create portfolio settings from a source.

        Parameters
        ----------
        source : str
            The name of an upload from the portfolio uploader.
        ffill : Literal["no-ffill", "ffill-with-drift"], default="no-ffill"
            The forward fill option.
        unpack : Literal["no-unpack", "unpack"], default="no-unpack"
            The unpack option.
        dataset : str | None, default=None
            The risk dataset to use for the security master and asset returns. If None,
            the default dataset is used.

        Returns
        -------
        PortfolioSettings
            The created portfolio settings.
        """
        return cls(
            portfolio_schema=PortfolioOrganizerSettings(
                enabled_portfolios=source, dataset=dataset
            ),
            ffill=ffill,
            unpack=unpack,
        )

    @field_validator("portfolio_schema")
    @classmethod
    def validate_portfolio_schema(
        cls,
        portfolio_schema: str | int | PortfolioOrganizerSettings,
        info: ValidationInfo,
    ) -> str | int | PortfolioOrganizerSettings:
        if isinstance(menu := info.context, PortfolioSettingsMenu):
            if isinstance(portfolio_schema, str):
                if portfolio_schema not in menu.schemas:
                    raise ValueError(
                        f"Invalid schema: {portfolio_schema}. "
                        f"Available schemas are: {', '.join(menu.schemas)}"
                    )
            if isinstance(portfolio_schema, PortfolioOrganizerSettings):
                if isinstance(portfolio_schema.enabled_portfolios, str):
                    if portfolio_schema.enabled_portfolios not in menu.sources:
                        raise ValueError(
                            f"Invalid source: {portfolio_schema.enabled_portfolios}. "
                            f"Available sources: {', '.join(menu.sources)}"
                        )
                else:
                    invalid_sources = [
                        source
                        for source in portfolio_schema.enabled_portfolios.values()
                        if source not in menu.sources
                    ]
                    if invalid_sources:
                        raise ValueError(
                            f"Invalid sources: {invalid_sources}. "
                            f"Available sources: {', '.join(menu.sources)}"
                        )
        return portfolio_schema

    def describe(self, menu: PortfolioSettingsMenu) -> str:
        """Describe the settings.

        Parameters
        ----------
        menu : PortfolioSettingsMenu
            The menu to get context information from.

        Returns
        -------
        str
            A description of the settings.
        """
        del menu  # not used
        if isinstance(self.portfolio_schema, PortfolioOrganizerSettings):
            schema_str = self.portfolio_schema.enabled_portfolios
        else:
            schema_str = str(self.portfolio_schema)
        return (
            f"Forward Fill: {self.ffill}\nUnpack: {self.unpack}\nSchema: {schema_str}"
        )
