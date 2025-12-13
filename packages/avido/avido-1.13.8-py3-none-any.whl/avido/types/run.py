# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Run"]


class Run(BaseModel):
    id: str
    """Unique identifier of the run"""

    created_at: datetime = FieldInfo(alias="createdAt")
    """When the run was created"""

    modified_at: datetime = FieldInfo(alias="modifiedAt")
    """When the run was last modified"""

    type: Literal["MANUAL", "SCHEDULED", "EXPERIMENT"]

    experiment_variant_id: Optional[str] = FieldInfo(alias="experimentVariantId", default=None)
    """Optional ID of the experiment variant this run belongs to"""
