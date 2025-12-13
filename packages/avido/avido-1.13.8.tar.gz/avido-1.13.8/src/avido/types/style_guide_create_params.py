# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

__all__ = ["StyleGuideCreateParams", "Content"]


class StyleGuideCreateParams(TypedDict, total=False):
    content: Required[Iterable[Content]]


class Content(TypedDict, total=False):
    content: Required[str]
    """The content of the section in markdown"""

    heading: Required[str]
    """The heading of the section"""

    approved: bool
    """Whether or not the section has been approved"""
