# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .eval import Eval
from .._models import BaseModel

__all__ = ["Test"]


class Test(BaseModel):
    __test__ = False
    id: str
    """Unique identifier of the run"""

    created_at: datetime = FieldInfo(alias="createdAt")
    """When the test was created"""

    evals: List[Eval]
    """Array of evaluations in this run"""

    modified_at: datetime = FieldInfo(alias="modifiedAt")
    """When the test was last modified"""

    run_id: str = FieldInfo(alias="runId")
    """The unique identifier of the run"""

    status: Literal["PENDING", "IN_PROGRESS", "COMPLETED", "FAILED"]
    """Status of the evaluation/test"""

    task_id: str = FieldInfo(alias="taskId")
    """The unique identifier of the task"""

    trace_id: Optional[str] = FieldInfo(alias="traceId", default=None)
    """Optional ID of the trace this run is associated with"""
