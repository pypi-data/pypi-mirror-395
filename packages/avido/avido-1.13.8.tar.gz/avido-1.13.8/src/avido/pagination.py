# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Generic, TypeVar, Optional
from typing_extensions import override

from pydantic import Field as FieldInfo

from ._models import BaseModel
from ._base_client import BasePage, PageInfo, BaseSyncPage, BaseAsyncPage

__all__ = ["OffsetPaginationPagination", "SyncOffsetPagination", "AsyncOffsetPagination"]

_T = TypeVar("_T")


class OffsetPaginationPagination(BaseModel):
    limit: Optional[int] = None

    skip: Optional[int] = None

    total: Optional[int] = None

    total_pages: Optional[int] = FieldInfo(alias="totalPages", default=None)


class SyncOffsetPagination(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    """The array of returned items"""
    pagination: Optional[OffsetPaginationPagination] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        skip = None
        if self.pagination is not None:
            if self.pagination.skip is not None:
                skip = self.pagination.skip
        if skip is None:
            return None  # type: ignore[unreachable]

        length = len(self._get_page_items())
        current_count = skip + length

        total = None
        if self.pagination is not None:
            if self.pagination.total is not None:
                total = self.pagination.total
        if total is None:
            return None

        if current_count < total:
            return PageInfo(params={"skip": current_count})

        return None


class AsyncOffsetPagination(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    """The array of returned items"""
    pagination: Optional[OffsetPaginationPagination] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        skip = None
        if self.pagination is not None:
            if self.pagination.skip is not None:
                skip = self.pagination.skip
        if skip is None:
            return None  # type: ignore[unreachable]

        length = len(self._get_page_items())
        current_count = skip + length

        total = None
        if self.pagination is not None:
            if self.pagination.total is not None:
                total = self.pagination.total
        if total is None:
            return None

        if current_count < total:
            return PageInfo(params={"skip": current_count})

        return None
