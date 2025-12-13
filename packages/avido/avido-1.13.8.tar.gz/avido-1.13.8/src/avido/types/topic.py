# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Topic"]


class Topic(BaseModel):
    id: str
    """Unique identifier of the topic"""

    baseline: Optional[float] = None
    """Optional baseline score for this topic"""

    created_at: datetime = FieldInfo(alias="createdAt")
    """When the topic was created"""

    modified_at: datetime = FieldInfo(alias="modifiedAt")
    """When the topic was last modified"""

    org_id: str = FieldInfo(alias="orgId")
    """Organization ID that owns this topic"""

    title: str
    """Title of the topic"""
