# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["StyleGuideListParams"]


class StyleGuideListParams(TypedDict, total=False):
    application_slug: Annotated[str, PropertyInfo(alias="applicationSlug")]
    """Filter style guides by application slug"""

    limit: int
    """Number of items to include in the result set."""

    order_by: Annotated[str, PropertyInfo(alias="orderBy")]
    """Field to order by in the result set."""

    order_dir: Annotated[Literal["asc", "desc"], PropertyInfo(alias="orderDir")]
    """Order direction."""

    skip: int
    """Number of items to skip before starting to collect the result set."""
