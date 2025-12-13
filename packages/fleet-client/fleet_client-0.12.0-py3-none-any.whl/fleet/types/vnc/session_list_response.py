# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel
from .vnc_session import VncSession

__all__ = ["SessionListResponse"]


class SessionListResponse(BaseModel):
    active_pods: int

    last_updated: float

    sessions: List[VncSession]

    total_sessions: int
