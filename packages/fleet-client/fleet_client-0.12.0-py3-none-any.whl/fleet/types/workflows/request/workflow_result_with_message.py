# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ...._models import BaseModel

__all__ = ["WorkflowResultWithMessage"]


class WorkflowResultWithMessage(BaseModel):
    message: str

    workflow_id: str
