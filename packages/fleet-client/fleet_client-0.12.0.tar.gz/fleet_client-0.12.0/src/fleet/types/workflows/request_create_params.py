# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from .wait_until import WaitUntil

__all__ = ["RequestCreateParams"]


class RequestCreateParams(TypedDict, total=False):
    url: Required[str]

    agentic: bool

    camo: bool

    enable_xvfb: bool

    ephemeral_browser: bool

    proxy_password: Optional[str]

    proxy_url: Optional[str]

    proxy_username: Optional[str]

    stealth: bool

    wait_until: WaitUntil
