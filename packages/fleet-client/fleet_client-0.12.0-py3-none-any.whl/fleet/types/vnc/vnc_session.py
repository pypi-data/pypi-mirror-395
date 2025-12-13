# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["VncSession"]


class VncSession(BaseModel):
    browser_id: str

    created_at: float

    display: str

    pod_ip: str

    pod_name: str

    vnc_port: int

    active: Optional[bool] = None

    last_seen: Optional[float] = None
