# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["DocumentChunk"]


class DocumentChunk(BaseModel):
    chunk_index: int = FieldInfo(alias="chunkIndex")
    """The index of the chunk"""

    content: str
    """The content of the chunk"""

    document_id: str = FieldInfo(alias="documentId")
    """The ID of the document"""

    document_name: str = FieldInfo(alias="documentName")
    """The name/title of the document version"""

    title: str
    """The title of the chunk"""

    version_id: str = FieldInfo(alias="versionId")
    """The ID of the document version this chunk belongs to"""

    embedding: Optional[List[int]] = None
    """The embedding of the chunk"""
