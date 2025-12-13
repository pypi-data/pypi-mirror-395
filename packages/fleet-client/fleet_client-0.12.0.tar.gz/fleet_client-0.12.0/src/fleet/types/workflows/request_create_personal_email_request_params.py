# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from ..._types import SequenceNotStr
from .search_engine import SearchEngine

__all__ = ["RequestCreatePersonalEmailRequestParams"]


class RequestCreatePersonalEmailRequestParams(TypedDict, total=False):
    person_name: Required[str]
    """The name of the person to find email for"""

    additional_context: Optional[str]
    """Any additional context that might help find the person's email"""

    camo: bool
    """Whether to use CAMO for scraping"""

    company_name: Optional[str]
    """Optional company name associated with the person"""

    job_title: Optional[str]
    """Optional job title of the person"""

    known_websites: Optional[SequenceNotStr[str]]
    """Optional list of websites associated with the person"""

    linkedin_url: Optional[str]
    """Optional LinkedIn URL of the person"""

    location: Optional[str]
    """Optional location (city, state) of the person"""

    max_steps: Optional[int]
    """Maximum number of steps the agent can take"""

    n_pages: int
    """Number of pages to visit while searching for email"""

    n_search_engine_links: int
    """Number of search engine results to explore"""

    proxy_password: Optional[str]
    """Optional proxy password"""

    proxy_url: Optional[str]
    """Optional proxy URL to use for web requests"""

    proxy_username: Optional[str]
    """Optional proxy username"""

    search_engine: SearchEngine
    """Search engine to use for finding email"""

    workflow_id: Optional[str]
    """Optional workflow ID for tracking"""
