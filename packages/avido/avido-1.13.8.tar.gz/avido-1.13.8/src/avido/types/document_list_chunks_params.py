# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo
from .document_status import DocumentStatus

__all__ = ["DocumentListChunksParams"]


class DocumentListChunksParams(TypedDict, total=False):
    document_id: Annotated[str, PropertyInfo(alias="documentId")]
    """Filter by document ID"""

    limit: int
    """Number of items to include in the result set."""

    order_by: Annotated[str, PropertyInfo(alias="orderBy")]
    """Field to order by in the result set."""

    order_dir: Annotated[Literal["asc", "desc"], PropertyInfo(alias="orderDir")]
    """Order direction."""

    skip: int
    """Number of items to skip before starting to collect the result set."""

    status: DocumentStatus
    """Status of the document. Valid options: DRAFT, REVIEW, APPROVED, ARCHIVED."""

    version_id: Annotated[str, PropertyInfo(alias="versionId")]
    """Filter by specific document version ID"""
