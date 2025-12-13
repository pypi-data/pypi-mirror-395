# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["TaskCreateParams"]


class TaskCreateParams(TypedDict, total=False):
    description: Required[str]
    """A short description of the task"""

    title: Required[str]
    """The title of the task"""

    metadata: Dict[str, object]
    """
    Optional metadata to associate with the task when creating it (e.g., external
    identifiers).
    """

    simulated_prompt_schema: Annotated[Dict[str, object], PropertyInfo(alias="simulatedPromptSchema")]
    """
    JSON schema that defines the structure for user prompts that should be generated
    for tests
    """

    topic_id: Annotated[str, PropertyInfo(alias="topicId")]
    """ID of the topic this task belongs to"""

    type: Literal["STATIC", "NORMAL"]
    """The type of task"""
