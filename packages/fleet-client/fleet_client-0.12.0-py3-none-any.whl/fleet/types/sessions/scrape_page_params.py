# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from ..workflows.wait_until import WaitUntil

__all__ = ["ScrapePageParams"]


class ScrapePageParams(TypedDict, total=False):
    url: Required[str]

    wait_until: WaitUntil
