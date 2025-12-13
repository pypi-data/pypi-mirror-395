# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List

from ..._models import BaseModel
from .browser_selection_strategy import BrowserSelectionStrategy

__all__ = ["ScrapeGetBrowserStatsResponse"]


class ScrapeGetBrowserStatsResponse(BaseModel):
    active_browsers: List[str]

    average_jobs_per_browser: float

    browser_usage: Dict[str, int]

    current_strategy: BrowserSelectionStrategy

    total_browsers: int

    total_jobs_processed: int
