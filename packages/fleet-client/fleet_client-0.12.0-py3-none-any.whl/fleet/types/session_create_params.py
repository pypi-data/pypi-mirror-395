# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .browser_configuration_param import BrowserConfigurationParam

__all__ = ["SessionCreateParams"]


class SessionCreateParams(TypedDict, total=False):
    browser_configuration: Required[BrowserConfigurationParam]
    """Browser configuration."""

    agentic: bool

    enable_xvfb: bool

    n_responses_to_track: int

    proxy_password: str

    proxy_url: str

    proxy_username: str

    vnc_password: str
