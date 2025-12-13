# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["TraceListParams"]


class TraceListParams(TypedDict, total=False):
    application_id: Required[Annotated[str, PropertyInfo(alias="applicationId")]]
    """Filter traces by application ID"""

    end_date: Annotated[Union[str, datetime], PropertyInfo(alias="endDate", format="iso8601")]
    """End date (ISO8601) for filtering traces."""

    limit: int
    """Number of items to include in the result set."""

    skip: int
    """Number of items to skip before starting to collect the result set."""

    start_date: Annotated[Union[str, datetime], PropertyInfo(alias="startDate", format="iso8601")]
    """Start date (ISO8601) for filtering traces."""
