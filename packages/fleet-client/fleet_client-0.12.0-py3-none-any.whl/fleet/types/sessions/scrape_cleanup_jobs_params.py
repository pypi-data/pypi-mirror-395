# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["ScrapeCleanupJobsParams"]


class ScrapeCleanupJobsParams(TypedDict, total=False):
    max_age_hours: int
    """Maximum age in hours for completed jobs"""
