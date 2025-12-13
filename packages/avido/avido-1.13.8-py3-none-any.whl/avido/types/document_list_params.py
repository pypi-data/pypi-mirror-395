# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Literal, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo
from .document_status import DocumentStatus

__all__ = ["DocumentListParams"]


class DocumentListParams(TypedDict, total=False):
    assignee: str
    """Filter by assignee user ID"""

    end_date: Annotated[Union[str, datetime], PropertyInfo(alias="endDate", format="iso8601")]
    """Filter documents created before this date (inclusive)."""

    limit: int
    """Number of items to include in the result set."""

    order_by: Annotated[str, PropertyInfo(alias="orderBy")]
    """Field to order by in the result set."""

    order_dir: Annotated[Literal["asc", "desc"], PropertyInfo(alias="orderDir")]
    """Order direction."""

    scrape_job_id: Annotated[str, PropertyInfo(alias="scrapeJobId")]
    """Filter by scrape job ID"""

    search: str
    """Search in document version title and content"""

    skip: int
    """Number of items to skip before starting to collect the result set."""

    start_date: Annotated[Union[str, datetime], PropertyInfo(alias="startDate", format="iso8601")]
    """Filter documents created after this date (inclusive)."""

    status: DocumentStatus
    """Status of the document. Valid options: DRAFT, REVIEW, APPROVED, ARCHIVED."""

    tag_id: Annotated[SequenceNotStr[str], PropertyInfo(alias="tagId")]
    """Filter documents by tag ID"""
