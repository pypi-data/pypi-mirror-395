from collections.abc import Sequence

from bayesline.api._src.equity.calendar_settings import CalendarSettings
from bayesline.api._src.equity.exposure_settings import ExposureSettings
from bayesline.api._src.equity.modelconstruction_settings import (
    ModelConstructionSettings,
)
from bayesline.api._src.equity.portfolio_settings import PortfolioSettings
from bayesline.api._src.equity.portfoliohierarchy_settings import (
    PortfolioHierarchySettings,
)
from bayesline.api._src.equity.report_settings import ReportSettings
from bayesline.api._src.equity.riskdataset_settings import RiskDatasetSettings
from bayesline.api._src.equity.riskmodels_settings import FactorRiskModelSettings
from bayesline.api._src.equity.universe_settings import UniverseSettings
from bayesline.api._src.registry import Settings

SETTINGS_TYPES: Sequence[type[Settings]] = [
    UniverseSettings,
    RiskDatasetSettings,
    FactorRiskModelSettings,
    ModelConstructionSettings,
    PortfolioSettings,
    PortfolioHierarchySettings,
    ReportSettings,
    CalendarSettings,
    ExposureSettings,
]
