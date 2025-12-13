# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo
from .document_status import DocumentStatus

__all__ = ["DocumentCreateParams"]


class DocumentCreateParams(TypedDict, total=False):
    assignee: Required[str]
    """User ID of the person assigned to this document"""

    content: Required[str]
    """Content of the initial document version"""

    title: Required[str]
    """Title of the initial document version"""

    language: str
    """Language of the initial document version"""

    metadata: Dict[str, object]
    """Optional metadata for the initial document version"""

    original_sentences: Annotated[SequenceNotStr[str], PropertyInfo(alias="originalSentences")]
    """Array of original sentences from the source"""

    scrape_job_id: Annotated[str, PropertyInfo(alias="scrapeJobId")]
    """Optional ID of the scrape job that generated this document"""

    status: DocumentStatus
    """Status of the document. Valid options: DRAFT, REVIEW, APPROVED, ARCHIVED."""
