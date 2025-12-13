# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from .._models import BaseModel

__all__ = ["SessionVisitPageResponse", "Response"]


class Response(BaseModel):
    timestamp: float

    url: str

    error: Optional[str] = None

    headers: Optional[Dict[str, str]] = None

    ok: Optional[bool] = None

    request_method: Optional[str] = None

    resource_type: Optional[str] = None

    status_code: Optional[int] = None

    status_text: Optional[str] = None


class SessionVisitPageResponse(BaseModel):
    browser_id: str

    message: str

    url: str

    response: Optional[Response] = None
    """Response data for a navigation request."""
