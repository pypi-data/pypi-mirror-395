# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["AnnotationCreateParams"]


class AnnotationCreateParams(TypedDict, total=False):
    application_id: Required[Annotated[str, PropertyInfo(alias="applicationId")]]
    """The ID of the application this annotation belongs to"""

    title: Required[str]
    """Title of the annotation"""

    created_at: Annotated[Union[str, datetime], PropertyInfo(alias="createdAt", format="iso8601")]
    """Custom creation date for the annotation (ISO8601 format)"""

    description: Optional[str]
    """A description of what was changed in the application configuration"""
