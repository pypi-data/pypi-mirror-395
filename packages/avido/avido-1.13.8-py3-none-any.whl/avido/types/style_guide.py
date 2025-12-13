# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["StyleGuide", "Content"]


class Content(BaseModel):
    approved: bool
    """Whether or not the section has been approved"""

    content: str
    """The content of the section in markdown"""

    heading: str
    """The heading of the section"""


class StyleGuide(BaseModel):
    id: str
    """The unique identifier of the style guide"""

    application_id: str = FieldInfo(alias="applicationId")
    """The application ID this style guide belongs to"""

    content: List[Content]

    created_at: datetime = FieldInfo(alias="createdAt")
    """When the style guide was created"""

    modified_at: datetime = FieldInfo(alias="modifiedAt")
    """When the style guide was last modified"""

    org_id: str = FieldInfo(alias="orgId")
    """The organization ID this style guide belongs to"""

    quickstart_id: Optional[str] = FieldInfo(alias="quickstartId", default=None)
    """The ID of the associated quickstart if any"""
