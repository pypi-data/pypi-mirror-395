# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["MassCreateLinkExtractionParams"]


class MassCreateLinkExtractionParams(TypedDict, total=False):
    company_name: Required[str]

    n_pages: int

    results_per_page: int
