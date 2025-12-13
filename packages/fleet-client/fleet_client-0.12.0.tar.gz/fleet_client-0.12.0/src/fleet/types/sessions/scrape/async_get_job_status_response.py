# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ...._models import BaseModel
from .job_status import JobStatus

__all__ = ["AsyncGetJobStatusResponse"]


class AsyncGetJobStatusResponse(BaseModel):
    job_id: str

    message: str

    status: JobStatus

    url: str

    browser_status_code: Optional[int] = None

    completed_at: Optional[float] = None

    content: Optional[str] = None

    created_at: Optional[float] = None

    error: Optional[str] = None
