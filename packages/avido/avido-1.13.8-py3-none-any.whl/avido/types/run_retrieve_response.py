# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .run import Run
from .._models import BaseModel

__all__ = ["RunRetrieveResponse"]


class RunRetrieveResponse(BaseModel):
    run: Run
    """A Run represents a batch of tests triggered by a single task"""
