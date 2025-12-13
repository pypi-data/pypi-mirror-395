# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .test import Test
from .._models import BaseModel

__all__ = ["TestListResponse", "TestListResponseTask"]


class TestListResponseTask(BaseModel):
    __test__ = False
    id: str
    """The unique identifier of the task"""

    title: str
    """The title of the task"""

    topic_id: Optional[str] = FieldInfo(alias="topicId", default=None)
    """The ID of the topic this task belongs to"""


class TestListResponse(Test):
    __test__ = False
    task: TestListResponseTask
    """
    A task that represents a specific job-to-be-done by the LLM in the user
    application.
    """
