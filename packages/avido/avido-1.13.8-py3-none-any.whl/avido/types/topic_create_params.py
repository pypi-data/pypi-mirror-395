# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["TopicCreateParams"]


class TopicCreateParams(TypedDict, total=False):
    title: Required[str]
    """Title of the topic"""

    baseline: Optional[float]
    """Optional baseline score for this topic"""
