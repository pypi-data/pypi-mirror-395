from typing import Annotated, Any

from pydantic import AfterValidator, Field, ValidationInfo, field_validator

from bayesline.api._src.registry import Settings, SettingsMenu


def require_sorted_unique(v: Any) -> Any:
    """
    Validate that the given list is sorted and unique.

    Parameters
    ----------
    v : Any
        The list to validate.

    Returns
    -------
    Any
        The validated list.

    Raises
    ------
    ValueError
        If the list is not unique or not sorted.
    """
    if len(v) != len(set(v)):
        raise ValueError("The list must be unique.")
    if v != sorted(v):
        raise ValueError("The list must be sorted.")
    return v


class CalendarSettingsMenu(SettingsMenu, frozen=True, extra="forbid"):
    """Contain the available settings that can be used for the calendar settings."""

    exchanges: Annotated[list[str], AfterValidator(require_sorted_unique)] = Field(
        description="""
        A list of mic codes of all exchanges. Must be sorted and unique.
        """,
    )

    def describe(self) -> str:
        """
        Describe the calendar settings menu.

        Returns
        -------
        str
            Description of the settings menu.
        """
        return f"Exchanges (MIC): {', '.join(self.exchanges)}"


class CalendarSettings(Settings[CalendarSettingsMenu]):
    """Define the settings for the calendar."""

    dataset: str | None = Field(
        default=None,
        description=(
            "The name of the underlying dataset to use. If none is given then the "
            "configured default dataset is used."
        ),
        examples=["Bayesline-US"],
    )

    filters: list[list[str]] = Field(
        default=[["XNYS"]],
        min_length=1,
        description=(
            "The filters to apply. Each filter is a list of exchange MIC codes. The "
            "outer list will be treated as an OR conditions, while the inner lists "
            "will be treated as an AND conditions. For example, `[['A', 'B'], ['C']]` "
            "means that the holidays are the days where either A and B are both "
            "holidays, or C is a holiday."
        ),
        examples=[[["XNYS"]], [["XNYS", "XNAS"]], [["XNYS"], ["XNAS"]]],
    )

    @property
    def menu_type(self) -> type[CalendarSettingsMenu]:  # noqa: D102
        return CalendarSettingsMenu

    @field_validator("filters", mode="after")
    @classmethod
    def validate_filters(
        cls, value: list[list[str]], info: ValidationInfo
    ) -> list[list[str]]:
        if isinstance(menu := info.context, CalendarSettingsMenu):
            not_found = set()
            for filter_or in value:
                for filter_and in filter_or:
                    if filter_and not in menu.exchanges:
                        not_found.add(filter_and)
            if not_found:
                raise ValueError(
                    f"""
                    The following exchanges do not exist: {', '.join(not_found)}.
                    Only {', '.join(menu.exchanges)} exist.
                    """,
                )
        return value

    def describe(self, menu: CalendarSettingsMenu) -> str:
        """Describe the calendar settings.

        Parameters
        ----------
        menu : CalendarSettingsMenu
            The settings menu to use to describe the settings.

        Returns
        -------
        str
            A description of the calendar settings.
        """
        del menu  # not used
        filter_str = " or ".join(
            (
                f"({' and '.join(and_terms)})"
                if len(self.filters) > 1 and len(and_terms) > 1
                else f"{' and '.join(and_terms)}"
            )
            for and_terms in self.filters
        )
        return f"Holidays where holidays on {filter_str}."
