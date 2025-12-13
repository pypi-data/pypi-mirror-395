# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Annotation"]


class Annotation(BaseModel):
    id: str
    """Unique identifier of the annotation"""

    created_at: datetime = FieldInfo(alias="createdAt")
    """When the annotation was created"""

    modified_at: datetime = FieldInfo(alias="modifiedAt")
    """When the annotation was last modified"""

    org_id: str = FieldInfo(alias="orgId")
    """Organization ID that owns this annotation"""

    title: str
    """Title of the annotation"""

    description: Optional[str] = None
    """What changed in the AI application"""
