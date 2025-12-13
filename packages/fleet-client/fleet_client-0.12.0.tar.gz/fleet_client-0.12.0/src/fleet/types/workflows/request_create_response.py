# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["RequestCreateResponse"]


class RequestCreateResponse(BaseModel):
    url: str

    workflow_id: str
