# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from ..._types import SequenceNotStr
from .search_engine import SearchEngine

__all__ = ["RequestCreateBusinessOwnerParams"]


class RequestCreateBusinessOwnerParams(TypedDict, total=False):
    company_name: Required[str]
    """The name of the business"""

    addresses: Optional[SequenceNotStr[str]]
    """Optional list of addresses associated with the business"""

    camo: bool
    """Whether to use CAMO for scraping (if available)"""

    company_url: Optional[str]
    """The URL of the business to find the owner for"""

    emails: Optional[SequenceNotStr[str]]
    """Optional list of emails associated with the business"""

    max_steps: Optional[int]
    """Maximum number of steps the agent can take"""

    n_contact_pages: int
    """
    Number of additional pages to visit to find contact info after identifying the
    owner
    """

    n_pages: int
    """Number of pages to scrape for owner information"""

    n_search_engine_links: int
    """Number of search engine links to consider if needed"""

    personnel_names: Optional[SequenceNotStr[str]]
    """List of people associated with the business"""

    proxy_password: Optional[str]
    """Optional proxy password"""

    proxy_url: Optional[str]
    """Optional proxy URL to use for web requests"""

    proxy_username: Optional[str]
    """Optional proxy username"""

    search_engine: SearchEngine
    """Search engine to use for finding links"""

    workflow_id: Optional[str]
    """Optional workflow ID for tracking"""
