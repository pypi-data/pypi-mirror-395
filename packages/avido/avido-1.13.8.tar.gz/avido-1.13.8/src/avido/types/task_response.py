# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .task import Task
from .._models import BaseModel

__all__ = ["TaskResponse"]


class TaskResponse(BaseModel):
    task: Task
    """
    A task that represents a specific job-to-be-done by the LLM in the user
    application.
    """
