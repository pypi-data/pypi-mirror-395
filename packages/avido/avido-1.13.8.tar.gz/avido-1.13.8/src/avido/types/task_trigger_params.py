# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["TaskTriggerParams"]


class TaskTriggerParams(TypedDict, total=False):
    task_ids: Required[Annotated[SequenceNotStr[str], PropertyInfo(alias="taskIds")]]
    """Array of task IDs to trigger"""
