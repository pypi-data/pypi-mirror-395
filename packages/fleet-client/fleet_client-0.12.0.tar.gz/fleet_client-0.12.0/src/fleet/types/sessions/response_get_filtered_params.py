# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["ResponseGetFilteredParams"]


class ResponseGetFilteredParams(TypedDict, total=False):
    status_code: int
    """Filter by status code"""

    url_pattern: str
    """Filter by URL pattern"""
