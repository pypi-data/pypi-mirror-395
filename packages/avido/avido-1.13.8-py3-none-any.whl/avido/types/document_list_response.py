# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .document import Document

__all__ = ["DocumentListResponse", "DocumentListResponseTag"]


class DocumentListResponseTag(BaseModel):
    id: str
    """Unique identifier of the tag"""

    color: str
    """Hex color code for the tag"""

    name: str
    """Name of the tag"""


class DocumentListResponse(Document):
    tags: List[DocumentListResponseTag]
