from bayesline.api._src.registry import Settings, SettingsMenu


class ReportSettingsMenu(SettingsMenu, frozen=True, extra="forbid"):
    """Defines the available report types and settings to create a report."""

    pass


class ReportSettings(Settings[ReportSettingsMenu]):
    """Concrete settings for a report."""

    @property
    def menu_type(self) -> type[ReportSettingsMenu]:
        """The menu type for this settings object."""
        return ReportSettingsMenu
