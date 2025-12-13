# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Any, List, Type, Generic, Mapping, TypeVar, Optional, cast
from typing_extensions import Protocol, override, runtime_checkable

from httpx import Response

from ._utils import is_mapping
from ._models import BaseModel, GenericModel
from ._base_client import BasePage, PageInfo, BaseSyncPage, BaseAsyncPage
from .types.shared.page_cursor_shared_ref_pagination import PageCursorSharedRefPagination

__all__ = [
    "SyncPageCursor",
    "AsyncPageCursor",
    "SyncPageCursorWithReverse",
    "AsyncPageCursorWithReverse",
    "SyncPageCursorFromHeaders",
    "AsyncPageCursorFromHeaders",
    "SyncPageCursorTopLevelArray",
    "AsyncPageCursorTopLevelArray",
    "SyncPageCursorSharedRef",
    "AsyncPageCursorSharedRef",
    "SyncPageCursorWithHasMore",
    "AsyncPageCursorWithHasMore",
    "PageCursorWithNestedHasMoreMeta",
    "SyncPageCursorWithNestedHasMore",
    "AsyncPageCursorWithNestedHasMore",
    "PageCursorNestedObjectRefObjectProp",
    "SyncPageCursorNestedObjectRef",
    "AsyncPageCursorNestedObjectRef",
    "PageCursorNestedItemsData",
    "PageCursorNestedItemsObjectProp",
    "SyncPageCursorNestedItems",
    "AsyncPageCursorNestedItems",
    "SyncPagePageNumber",
    "AsyncPagePageNumber",
    "SyncPagePageNumberWithoutCurrentPageResponse",
    "AsyncPagePageNumberWithoutCurrentPageResponse",
    "SyncPageOffsetTotalCount",
    "AsyncPageOffsetTotalCount",
    "SyncPageOffset",
    "AsyncPageOffset",
    "SyncPageOffsetNoStartField",
    "AsyncPageOffsetNoStartField",
    "SyncPageCursorID",
    "AsyncPageCursorID",
    "SyncFakePage",
    "AsyncFakePage",
]

_BaseModelT = TypeVar("_BaseModelT", bound=BaseModel)

_T = TypeVar("_T")


@runtime_checkable
class PageCursorIDItem(Protocol):
    id: str


class SyncPageCursor(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    cursor: Optional[str] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        cursor = self.cursor
        if not cursor:
            return None

        return PageInfo(params={"cursor": cursor})


class AsyncPageCursor(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    cursor: Optional[str] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        cursor = self.cursor
        if not cursor:
            return None

        return PageInfo(params={"cursor": cursor})


class SyncPageCursorWithReverse(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    first_id: Optional[str] = None
    last_id: Optional[str] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        if self._options.params.get("before_id"):
            first_id = self.first_id
            if not first_id:
                return None

            return PageInfo(params={"before_id": first_id})

        last_id = self.last_id
        if not last_id:
            return None

        return PageInfo(params={"after_id": last_id})


class AsyncPageCursorWithReverse(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    first_id: Optional[str] = None
    last_id: Optional[str] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        if self._options.params.get("before_id"):
            first_id = self.first_id
            if not first_id:
                return None

            return PageInfo(params={"before_id": first_id})

        last_id = self.last_id
        if not last_id:
            return None

        return PageInfo(params={"after_id": last_id})


class SyncPageCursorFromHeaders(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    my_cursor: Optional[str] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        my_cursor = self.my_cursor
        if not my_cursor:
            return None

        return PageInfo(params={"cursor": my_cursor})

    @classmethod
    def build(cls: Type[_BaseModelT], *, response: Response, data: object) -> _BaseModelT:  # noqa: ARG003
        return cls.construct(
            None,
            **{
                **(cast(Mapping[str, Any], data) if is_mapping(data) else {}),
                "my_cursor": response.headers.get("X-My-Cursor"),
            },
        )


class AsyncPageCursorFromHeaders(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    my_cursor: Optional[str] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        my_cursor = self.my_cursor
        if not my_cursor:
            return None

        return PageInfo(params={"cursor": my_cursor})

    @classmethod
    def build(cls: Type[_BaseModelT], *, response: Response, data: object) -> _BaseModelT:  # noqa: ARG003
        return cls.construct(
            None,
            **{
                **(cast(Mapping[str, Any], data) if is_mapping(data) else {}),
                "my_cursor": response.headers.get("X-My-Cursor"),
            },
        )


class SyncPageCursorTopLevelArray(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    my_cursor: Optional[str] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        my_cursor = self.my_cursor
        if not my_cursor:
            return None

        return PageInfo(params={"cursor": my_cursor})

    @classmethod
    def build(cls: Type[_BaseModelT], *, response: Response, data: object) -> _BaseModelT:  # noqa: ARG003
        return cls.construct(
            None,
            **{
                **(cast(Mapping[str, Any], data) if is_mapping(data) else {"data": data}),
                "my_cursor": response.headers.get("X-My-Cursor"),
            },
        )


class AsyncPageCursorTopLevelArray(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    my_cursor: Optional[str] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        my_cursor = self.my_cursor
        if not my_cursor:
            return None

        return PageInfo(params={"cursor": my_cursor})

    @classmethod
    def build(cls: Type[_BaseModelT], *, response: Response, data: object) -> _BaseModelT:  # noqa: ARG003
        return cls.construct(
            None,
            **{
                **(cast(Mapping[str, Any], data) if is_mapping(data) else {"data": data}),
                "my_cursor": response.headers.get("X-My-Cursor"),
            },
        )


class SyncPageCursorSharedRef(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    pagination: Optional[PageCursorSharedRefPagination] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        cursor = None
        if self.pagination is not None:
            if self.pagination.cursor is not None:  # pyright: ignore[reportUnnecessaryComparison]
                cursor = self.pagination.cursor
        if not cursor:
            return None

        return PageInfo(params={"cursor": cursor})


class AsyncPageCursorSharedRef(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    pagination: Optional[PageCursorSharedRefPagination] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        cursor = None
        if self.pagination is not None:
            if self.pagination.cursor is not None:  # pyright: ignore[reportUnnecessaryComparison]
                cursor = self.pagination.cursor
        if not cursor:
            return None

        return PageInfo(params={"cursor": cursor})


class SyncPageCursorWithHasMore(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    cursor: Optional[str] = None
    has_more: Optional[bool] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        cursor = self.cursor
        if not cursor:
            return None

        return PageInfo(params={"cursor": cursor})


class AsyncPageCursorWithHasMore(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    cursor: Optional[str] = None
    has_more: Optional[bool] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        cursor = self.cursor
        if not cursor:
            return None

        return PageInfo(params={"cursor": cursor})


class PageCursorWithNestedHasMoreMeta(BaseModel):
    has_more: bool
    """whether or not there are more pages"""


class SyncPageCursorWithNestedHasMore(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    cursor: Optional[str] = None
    meta: Optional[PageCursorWithNestedHasMoreMeta] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def has_next_page(self) -> bool:
        has_more = None
        if self.meta is not None:
            if self.meta.has_more is not None:  # pyright: ignore[reportUnnecessaryComparison]
                has_more = self.meta.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        cursor = self.cursor
        if not cursor:
            return None

        return PageInfo(params={"cursor": cursor})


class AsyncPageCursorWithNestedHasMore(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    cursor: Optional[str] = None
    meta: Optional[PageCursorWithNestedHasMoreMeta] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def has_next_page(self) -> bool:
        has_more = None
        if self.meta is not None:
            if self.meta.has_more is not None:  # pyright: ignore[reportUnnecessaryComparison]
                has_more = self.meta.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        cursor = self.cursor
        if not cursor:
            return None

        return PageInfo(params={"cursor": cursor})


class PageCursorNestedObjectRefObjectProp(BaseModel):
    foo: Optional[str] = None


class SyncPageCursorNestedObjectRef(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    nested_object_cursor: Optional[str] = None
    object_prop: Optional[PageCursorNestedObjectRefObjectProp] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        nested_object_cursor = self.nested_object_cursor
        if not nested_object_cursor:
            return None

        return PageInfo(params={"cursor": nested_object_cursor})


class AsyncPageCursorNestedObjectRef(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    nested_object_cursor: Optional[str] = None
    object_prop: Optional[PageCursorNestedObjectRefObjectProp] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        nested_object_cursor = self.nested_object_cursor
        if not nested_object_cursor:
            return None

        return PageInfo(params={"cursor": nested_object_cursor})


class PageCursorNestedItemsData(GenericModel, Generic[_T]):
    items: Optional[List[_T]] = None


class PageCursorNestedItemsObjectProp(BaseModel):
    foo: Optional[str] = None


class SyncPageCursorNestedItems(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    data: Optional[PageCursorNestedItemsData[_T]] = None
    cursor: Optional[str] = None
    object_prop: Optional[PageCursorNestedItemsObjectProp] = None

    @override
    def _get_page_items(self) -> List[_T]:
        items = None
        if self.data is not None:
            if self.data.items is not None:
                items = self.data.items
        if not items:
            return []
        return items

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        cursor = self.cursor
        if not cursor:
            return None

        return PageInfo(params={"cursor": cursor})


class AsyncPageCursorNestedItems(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    data: Optional[PageCursorNestedItemsData[_T]] = None
    cursor: Optional[str] = None
    object_prop: Optional[PageCursorNestedItemsObjectProp] = None

    @override
    def _get_page_items(self) -> List[_T]:
        items = None
        if self.data is not None:
            if self.data.items is not None:
                items = self.data.items
        if not items:
            return []
        return items

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        cursor = self.cursor
        if not cursor:
            return None

        return PageInfo(params={"cursor": cursor})


class SyncPagePageNumber(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    page: Optional[int] = None
    last_page: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        current_page = self.page
        if current_page is None:
            current_page = 1

        total_pages = self.last_page
        if total_pages is not None and current_page >= total_pages:
            return None

        return PageInfo(params={"page": current_page + 1})


class AsyncPagePageNumber(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    page: Optional[int] = None
    last_page: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        current_page = self.page
        if current_page is None:
            current_page = 1

        total_pages = self.last_page
        if total_pages is not None and current_page >= total_pages:
            return None

        return PageInfo(params={"page": current_page + 1})


class SyncPagePageNumberWithoutCurrentPageResponse(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        last_page = cast("int | None", self._options.params.get("page")) or 1

        return PageInfo(params={"page": last_page + 1})


class AsyncPagePageNumberWithoutCurrentPageResponse(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        last_page = cast("int | None", self._options.params.get("page")) or 1

        return PageInfo(params={"page": last_page + 1})


class SyncPageOffsetTotalCount(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    total_count: Optional[int] = None
    offset: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        offset = self.offset
        if offset is None:
            return None  # type: ignore[unreachable]

        length = len(self._get_page_items())
        current_count = offset + length

        total_count = self.total_count
        if total_count is None:
            return None

        if current_count < total_count:
            return PageInfo(params={"offset": current_count})

        return None


class AsyncPageOffsetTotalCount(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    total_count: Optional[int] = None
    offset: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        offset = self.offset
        if offset is None:
            return None  # type: ignore[unreachable]

        length = len(self._get_page_items())
        current_count = offset + length

        total_count = self.total_count
        if total_count is None:
            return None

        if current_count < total_count:
            return PageInfo(params={"offset": current_count})

        return None


class SyncPageOffset(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    offset: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        offset = self.offset
        if offset is None:
            return None  # type: ignore[unreachable]

        length = len(self._get_page_items())
        current_count = offset + length

        return PageInfo(params={"offset": current_count})


class AsyncPageOffset(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]
    offset: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        offset = self.offset
        if offset is None:
            return None  # type: ignore[unreachable]

        length = len(self._get_page_items())
        current_count = offset + length

        return PageInfo(params={"offset": current_count})


class SyncPageOffsetNoStartField(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        offset = self._options.params.get("offset") or 0
        if not isinstance(offset, int):
            raise ValueError(f'Expected "offset" param to be an integer but got {offset}')

        length = len(self._get_page_items())
        current_count = offset + length

        return PageInfo(params={"offset": current_count})


class AsyncPageOffsetNoStartField(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        offset = self._options.params.get("offset") or 0
        if not isinstance(offset, int):
            raise ValueError(f'Expected "offset" param to be an integer but got {offset}')

        length = len(self._get_page_items())
        current_count = offset + length

        return PageInfo(params={"offset": current_count})


class SyncPageCursorID(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        data = self.data
        if not data:
            return None

        item = cast(Any, data[-1])
        if not isinstance(item, PageCursorIDItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
            # TODO emit warning log
            return None

        return PageInfo(params={"next_id": item.id})


class AsyncPageCursorID(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    data: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        data = self.data
        if not data:
            return None

        item = cast(Any, data[-1])
        if not isinstance(item, PageCursorIDItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
            # TODO emit warning log
            return None

        return PageInfo(params={"next_id": item.id})


class SyncFakePage(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    items: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        items = self.items
        if not items:
            return []
        return items

    @override
    def next_page_info(self) -> None:
        """
        This page represents a response that isn't actually paginated at the API level
        so there will never be a next page.
        """
        return None

    @classmethod
    def build(cls: Type[_BaseModelT], *, response: Response, data: object) -> _BaseModelT:  # noqa: ARG003
        return cls.construct(
            None,
            **{
                **(cast(Mapping[str, Any], data) if is_mapping(data) else {"items": data}),
            },
        )


class AsyncFakePage(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    items: List[_T]

    @override
    def _get_page_items(self) -> List[_T]:
        items = self.items
        if not items:
            return []
        return items

    @override
    def next_page_info(self) -> None:
        """
        This page represents a response that isn't actually paginated at the API level
        so there will never be a next page.
        """
        return None

    @classmethod
    def build(cls: Type[_BaseModelT], *, response: Response, data: object) -> _BaseModelT:  # noqa: ARG003
        return cls.construct(
            None,
            **{
                **(cast(Mapping[str, Any], data) if is_mapping(data) else {"items": data}),
            },
        )
