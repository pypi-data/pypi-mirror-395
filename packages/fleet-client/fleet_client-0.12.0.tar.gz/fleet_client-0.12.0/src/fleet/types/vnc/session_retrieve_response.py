# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["SessionRetrieveResponse"]


class SessionRetrieveResponse(BaseModel):
    active: bool

    browser_id: str

    created_at: float

    display: str

    pod_name: str

    vnc_url: str
