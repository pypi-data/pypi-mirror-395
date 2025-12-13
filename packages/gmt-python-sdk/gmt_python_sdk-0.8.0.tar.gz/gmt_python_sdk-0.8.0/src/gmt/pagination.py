# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Generic, TypeVar, Optional
from typing_extensions import override

from ._models import BaseModel
from ._base_client import BasePage, PageInfo, BaseSyncPage, BaseAsyncPage

__all__ = ["PageNumberPagination", "SyncPageNumber", "AsyncPageNumber"]

_T = TypeVar("_T")


class PageNumberPagination(BaseModel):
    current_page: int

    has_next: bool

    total_pages: int


class SyncPageNumber(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    items: List[_T]
    pagination: Optional[PageNumberPagination] = None

    @override
    def _get_page_items(self) -> List[_T]:
        items = self.items
        if not items:
            return []
        return items

    @override
    def has_next_page(self) -> bool:
        has_next = None
        if self.pagination is not None:
            if self.pagination.has_next is not None:  # pyright: ignore[reportUnnecessaryComparison]
                has_next = self.pagination.has_next
        if has_next is not None and has_next is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        current_page = None
        if self.pagination is not None:
            if self.pagination.current_page is not None:  # pyright: ignore[reportUnnecessaryComparison]
                current_page = self.pagination.current_page
        if current_page is None:
            current_page = 1

        total_pages = None
        if self.pagination is not None:
            if self.pagination.total_pages is not None:  # pyright: ignore[reportUnnecessaryComparison]
                total_pages = self.pagination.total_pages
        if total_pages is not None and current_page >= total_pages:
            return None

        return PageInfo(params={"page": current_page + 1})


class AsyncPageNumber(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    items: List[_T]
    pagination: Optional[PageNumberPagination] = None

    @override
    def _get_page_items(self) -> List[_T]:
        items = self.items
        if not items:
            return []
        return items

    @override
    def has_next_page(self) -> bool:
        has_next = None
        if self.pagination is not None:
            if self.pagination.has_next is not None:  # pyright: ignore[reportUnnecessaryComparison]
                has_next = self.pagination.has_next
        if has_next is not None and has_next is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        current_page = None
        if self.pagination is not None:
            if self.pagination.current_page is not None:  # pyright: ignore[reportUnnecessaryComparison]
                current_page = self.pagination.current_page
        if current_page is None:
            current_page = 1

        total_pages = None
        if self.pagination is not None:
            if self.pagination.total_pages is not None:  # pyright: ignore[reportUnnecessaryComparison]
                total_pages = self.pagination.total_pages
        if total_pages is not None and current_page >= total_pages:
            return None

        return PageInfo(params={"page": current_page + 1})
