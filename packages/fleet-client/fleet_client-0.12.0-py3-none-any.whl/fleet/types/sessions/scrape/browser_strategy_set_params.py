# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from ..browser_selection_strategy import BrowserSelectionStrategy

__all__ = ["BrowserStrategySetParams"]


class BrowserStrategySetParams(TypedDict, total=False):
    strategy: Required[BrowserSelectionStrategy]
