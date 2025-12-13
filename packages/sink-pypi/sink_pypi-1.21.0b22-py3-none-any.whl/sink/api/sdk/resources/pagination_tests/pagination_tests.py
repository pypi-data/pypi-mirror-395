# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .refs import (
    RefsResource,
    AsyncRefsResource,
    RefsResourceWithRawResponse,
    AsyncRefsResourceWithRawResponse,
    RefsResourceWithStreamingResponse,
    AsyncRefsResourceWithStreamingResponse,
)
from .cursor import (
    CursorResource,
    AsyncCursorResource,
    CursorResourceWithRawResponse,
    AsyncCursorResourceWithRawResponse,
    CursorResourceWithStreamingResponse,
    AsyncCursorResourceWithStreamingResponse,
)
from .offset import (
    OffsetResource,
    AsyncOffsetResource,
    OffsetResourceWithRawResponse,
    AsyncOffsetResourceWithRawResponse,
    OffsetResourceWithStreamingResponse,
    AsyncOffsetResourceWithStreamingResponse,
)
from ..._compat import cached_property
from .cursor_id import (
    CursorIDResource,
    AsyncCursorIDResource,
    CursorIDResourceWithRawResponse,
    AsyncCursorIDResourceWithRawResponse,
    CursorIDResourceWithStreamingResponse,
    AsyncCursorIDResourceWithStreamingResponse,
)
from .fake_pages import (
    FakePagesResource,
    AsyncFakePagesResource,
    FakePagesResourceWithRawResponse,
    AsyncFakePagesResourceWithRawResponse,
    FakePagesResourceWithStreamingResponse,
    AsyncFakePagesResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from .items_types import (
    ItemsTypesResource,
    AsyncItemsTypesResource,
    ItemsTypesResourceWithRawResponse,
    AsyncItemsTypesResourceWithRawResponse,
    ItemsTypesResourceWithStreamingResponse,
    AsyncItemsTypesResourceWithStreamingResponse,
)
from .page_number import (
    PageNumberResource,
    AsyncPageNumberResource,
    PageNumberResourceWithRawResponse,
    AsyncPageNumberResourceWithRawResponse,
    PageNumberResourceWithStreamingResponse,
    AsyncPageNumberResourceWithStreamingResponse,
)
from .nested_items import (
    NestedItemsResource,
    AsyncNestedItemsResource,
    NestedItemsResourceWithRawResponse,
    AsyncNestedItemsResourceWithRawResponse,
    NestedItemsResourceWithStreamingResponse,
    AsyncNestedItemsResourceWithStreamingResponse,
)
from .schema_types import (
    SchemaTypesResource,
    AsyncSchemaTypesResource,
    SchemaTypesResourceWithRawResponse,
    AsyncSchemaTypesResourceWithRawResponse,
    SchemaTypesResourceWithStreamingResponse,
    AsyncSchemaTypesResourceWithStreamingResponse,
)
from .response_headers import (
    ResponseHeadersResource,
    AsyncResponseHeadersResource,
    ResponseHeadersResourceWithRawResponse,
    AsyncResponseHeadersResourceWithRawResponse,
    ResponseHeadersResourceWithStreamingResponse,
    AsyncResponseHeadersResourceWithStreamingResponse,
)
from .top_level_arrays import (
    TopLevelArraysResource,
    AsyncTopLevelArraysResource,
    TopLevelArraysResourceWithRawResponse,
    AsyncTopLevelArraysResourceWithRawResponse,
    TopLevelArraysResourceWithStreamingResponse,
    AsyncTopLevelArraysResourceWithStreamingResponse,
)
from .page_number_without_current_page_response import (
    PageNumberWithoutCurrentPageResponseResource,
    AsyncPageNumberWithoutCurrentPageResponseResource,
    PageNumberWithoutCurrentPageResponseResourceWithRawResponse,
    AsyncPageNumberWithoutCurrentPageResponseResourceWithRawResponse,
    PageNumberWithoutCurrentPageResponseResourceWithStreamingResponse,
    AsyncPageNumberWithoutCurrentPageResponseResourceWithStreamingResponse,
)

__all__ = ["PaginationTestsResource", "AsyncPaginationTestsResource"]


class PaginationTestsResource(SyncAPIResource):
    @cached_property
    def schema_types(self) -> SchemaTypesResource:
        return SchemaTypesResource(self._client)

    @cached_property
    def items_types(self) -> ItemsTypesResource:
        return ItemsTypesResource(self._client)

    @cached_property
    def page_number(self) -> PageNumberResource:
        return PageNumberResource(self._client)

    @cached_property
    def page_number_without_current_page_response(self) -> PageNumberWithoutCurrentPageResponseResource:
        return PageNumberWithoutCurrentPageResponseResource(self._client)

    @cached_property
    def refs(self) -> RefsResource:
        return RefsResource(self._client)

    @cached_property
    def response_headers(self) -> ResponseHeadersResource:
        return ResponseHeadersResource(self._client)

    @cached_property
    def top_level_arrays(self) -> TopLevelArraysResource:
        return TopLevelArraysResource(self._client)

    @cached_property
    def cursor(self) -> CursorResource:
        return CursorResource(self._client)

    @cached_property
    def cursor_id(self) -> CursorIDResource:
        return CursorIDResource(self._client)

    @cached_property
    def offset(self) -> OffsetResource:
        return OffsetResource(self._client)

    @cached_property
    def fake_pages(self) -> FakePagesResource:
        return FakePagesResource(self._client)

    @cached_property
    def nested_items(self) -> NestedItemsResource:
        return NestedItemsResource(self._client)

    @cached_property
    def with_raw_response(self) -> PaginationTestsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return PaginationTestsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PaginationTestsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return PaginationTestsResourceWithStreamingResponse(self)


class AsyncPaginationTestsResource(AsyncAPIResource):
    @cached_property
    def schema_types(self) -> AsyncSchemaTypesResource:
        return AsyncSchemaTypesResource(self._client)

    @cached_property
    def items_types(self) -> AsyncItemsTypesResource:
        return AsyncItemsTypesResource(self._client)

    @cached_property
    def page_number(self) -> AsyncPageNumberResource:
        return AsyncPageNumberResource(self._client)

    @cached_property
    def page_number_without_current_page_response(self) -> AsyncPageNumberWithoutCurrentPageResponseResource:
        return AsyncPageNumberWithoutCurrentPageResponseResource(self._client)

    @cached_property
    def refs(self) -> AsyncRefsResource:
        return AsyncRefsResource(self._client)

    @cached_property
    def response_headers(self) -> AsyncResponseHeadersResource:
        return AsyncResponseHeadersResource(self._client)

    @cached_property
    def top_level_arrays(self) -> AsyncTopLevelArraysResource:
        return AsyncTopLevelArraysResource(self._client)

    @cached_property
    def cursor(self) -> AsyncCursorResource:
        return AsyncCursorResource(self._client)

    @cached_property
    def cursor_id(self) -> AsyncCursorIDResource:
        return AsyncCursorIDResource(self._client)

    @cached_property
    def offset(self) -> AsyncOffsetResource:
        return AsyncOffsetResource(self._client)

    @cached_property
    def fake_pages(self) -> AsyncFakePagesResource:
        return AsyncFakePagesResource(self._client)

    @cached_property
    def nested_items(self) -> AsyncNestedItemsResource:
        return AsyncNestedItemsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncPaginationTestsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncPaginationTestsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPaginationTestsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncPaginationTestsResourceWithStreamingResponse(self)


class PaginationTestsResourceWithRawResponse:
    def __init__(self, pagination_tests: PaginationTestsResource) -> None:
        self._pagination_tests = pagination_tests

    @cached_property
    def schema_types(self) -> SchemaTypesResourceWithRawResponse:
        return SchemaTypesResourceWithRawResponse(self._pagination_tests.schema_types)

    @cached_property
    def items_types(self) -> ItemsTypesResourceWithRawResponse:
        return ItemsTypesResourceWithRawResponse(self._pagination_tests.items_types)

    @cached_property
    def page_number(self) -> PageNumberResourceWithRawResponse:
        return PageNumberResourceWithRawResponse(self._pagination_tests.page_number)

    @cached_property
    def page_number_without_current_page_response(self) -> PageNumberWithoutCurrentPageResponseResourceWithRawResponse:
        return PageNumberWithoutCurrentPageResponseResourceWithRawResponse(
            self._pagination_tests.page_number_without_current_page_response
        )

    @cached_property
    def refs(self) -> RefsResourceWithRawResponse:
        return RefsResourceWithRawResponse(self._pagination_tests.refs)

    @cached_property
    def response_headers(self) -> ResponseHeadersResourceWithRawResponse:
        return ResponseHeadersResourceWithRawResponse(self._pagination_tests.response_headers)

    @cached_property
    def top_level_arrays(self) -> TopLevelArraysResourceWithRawResponse:
        return TopLevelArraysResourceWithRawResponse(self._pagination_tests.top_level_arrays)

    @cached_property
    def cursor(self) -> CursorResourceWithRawResponse:
        return CursorResourceWithRawResponse(self._pagination_tests.cursor)

    @cached_property
    def cursor_id(self) -> CursorIDResourceWithRawResponse:
        return CursorIDResourceWithRawResponse(self._pagination_tests.cursor_id)

    @cached_property
    def offset(self) -> OffsetResourceWithRawResponse:
        return OffsetResourceWithRawResponse(self._pagination_tests.offset)

    @cached_property
    def fake_pages(self) -> FakePagesResourceWithRawResponse:
        return FakePagesResourceWithRawResponse(self._pagination_tests.fake_pages)

    @cached_property
    def nested_items(self) -> NestedItemsResourceWithRawResponse:
        return NestedItemsResourceWithRawResponse(self._pagination_tests.nested_items)


class AsyncPaginationTestsResourceWithRawResponse:
    def __init__(self, pagination_tests: AsyncPaginationTestsResource) -> None:
        self._pagination_tests = pagination_tests

    @cached_property
    def schema_types(self) -> AsyncSchemaTypesResourceWithRawResponse:
        return AsyncSchemaTypesResourceWithRawResponse(self._pagination_tests.schema_types)

    @cached_property
    def items_types(self) -> AsyncItemsTypesResourceWithRawResponse:
        return AsyncItemsTypesResourceWithRawResponse(self._pagination_tests.items_types)

    @cached_property
    def page_number(self) -> AsyncPageNumberResourceWithRawResponse:
        return AsyncPageNumberResourceWithRawResponse(self._pagination_tests.page_number)

    @cached_property
    def page_number_without_current_page_response(
        self,
    ) -> AsyncPageNumberWithoutCurrentPageResponseResourceWithRawResponse:
        return AsyncPageNumberWithoutCurrentPageResponseResourceWithRawResponse(
            self._pagination_tests.page_number_without_current_page_response
        )

    @cached_property
    def refs(self) -> AsyncRefsResourceWithRawResponse:
        return AsyncRefsResourceWithRawResponse(self._pagination_tests.refs)

    @cached_property
    def response_headers(self) -> AsyncResponseHeadersResourceWithRawResponse:
        return AsyncResponseHeadersResourceWithRawResponse(self._pagination_tests.response_headers)

    @cached_property
    def top_level_arrays(self) -> AsyncTopLevelArraysResourceWithRawResponse:
        return AsyncTopLevelArraysResourceWithRawResponse(self._pagination_tests.top_level_arrays)

    @cached_property
    def cursor(self) -> AsyncCursorResourceWithRawResponse:
        return AsyncCursorResourceWithRawResponse(self._pagination_tests.cursor)

    @cached_property
    def cursor_id(self) -> AsyncCursorIDResourceWithRawResponse:
        return AsyncCursorIDResourceWithRawResponse(self._pagination_tests.cursor_id)

    @cached_property
    def offset(self) -> AsyncOffsetResourceWithRawResponse:
        return AsyncOffsetResourceWithRawResponse(self._pagination_tests.offset)

    @cached_property
    def fake_pages(self) -> AsyncFakePagesResourceWithRawResponse:
        return AsyncFakePagesResourceWithRawResponse(self._pagination_tests.fake_pages)

    @cached_property
    def nested_items(self) -> AsyncNestedItemsResourceWithRawResponse:
        return AsyncNestedItemsResourceWithRawResponse(self._pagination_tests.nested_items)


class PaginationTestsResourceWithStreamingResponse:
    def __init__(self, pagination_tests: PaginationTestsResource) -> None:
        self._pagination_tests = pagination_tests

    @cached_property
    def schema_types(self) -> SchemaTypesResourceWithStreamingResponse:
        return SchemaTypesResourceWithStreamingResponse(self._pagination_tests.schema_types)

    @cached_property
    def items_types(self) -> ItemsTypesResourceWithStreamingResponse:
        return ItemsTypesResourceWithStreamingResponse(self._pagination_tests.items_types)

    @cached_property
    def page_number(self) -> PageNumberResourceWithStreamingResponse:
        return PageNumberResourceWithStreamingResponse(self._pagination_tests.page_number)

    @cached_property
    def page_number_without_current_page_response(
        self,
    ) -> PageNumberWithoutCurrentPageResponseResourceWithStreamingResponse:
        return PageNumberWithoutCurrentPageResponseResourceWithStreamingResponse(
            self._pagination_tests.page_number_without_current_page_response
        )

    @cached_property
    def refs(self) -> RefsResourceWithStreamingResponse:
        return RefsResourceWithStreamingResponse(self._pagination_tests.refs)

    @cached_property
    def response_headers(self) -> ResponseHeadersResourceWithStreamingResponse:
        return ResponseHeadersResourceWithStreamingResponse(self._pagination_tests.response_headers)

    @cached_property
    def top_level_arrays(self) -> TopLevelArraysResourceWithStreamingResponse:
        return TopLevelArraysResourceWithStreamingResponse(self._pagination_tests.top_level_arrays)

    @cached_property
    def cursor(self) -> CursorResourceWithStreamingResponse:
        return CursorResourceWithStreamingResponse(self._pagination_tests.cursor)

    @cached_property
    def cursor_id(self) -> CursorIDResourceWithStreamingResponse:
        return CursorIDResourceWithStreamingResponse(self._pagination_tests.cursor_id)

    @cached_property
    def offset(self) -> OffsetResourceWithStreamingResponse:
        return OffsetResourceWithStreamingResponse(self._pagination_tests.offset)

    @cached_property
    def fake_pages(self) -> FakePagesResourceWithStreamingResponse:
        return FakePagesResourceWithStreamingResponse(self._pagination_tests.fake_pages)

    @cached_property
    def nested_items(self) -> NestedItemsResourceWithStreamingResponse:
        return NestedItemsResourceWithStreamingResponse(self._pagination_tests.nested_items)


class AsyncPaginationTestsResourceWithStreamingResponse:
    def __init__(self, pagination_tests: AsyncPaginationTestsResource) -> None:
        self._pagination_tests = pagination_tests

    @cached_property
    def schema_types(self) -> AsyncSchemaTypesResourceWithStreamingResponse:
        return AsyncSchemaTypesResourceWithStreamingResponse(self._pagination_tests.schema_types)

    @cached_property
    def items_types(self) -> AsyncItemsTypesResourceWithStreamingResponse:
        return AsyncItemsTypesResourceWithStreamingResponse(self._pagination_tests.items_types)

    @cached_property
    def page_number(self) -> AsyncPageNumberResourceWithStreamingResponse:
        return AsyncPageNumberResourceWithStreamingResponse(self._pagination_tests.page_number)

    @cached_property
    def page_number_without_current_page_response(
        self,
    ) -> AsyncPageNumberWithoutCurrentPageResponseResourceWithStreamingResponse:
        return AsyncPageNumberWithoutCurrentPageResponseResourceWithStreamingResponse(
            self._pagination_tests.page_number_without_current_page_response
        )

    @cached_property
    def refs(self) -> AsyncRefsResourceWithStreamingResponse:
        return AsyncRefsResourceWithStreamingResponse(self._pagination_tests.refs)

    @cached_property
    def response_headers(self) -> AsyncResponseHeadersResourceWithStreamingResponse:
        return AsyncResponseHeadersResourceWithStreamingResponse(self._pagination_tests.response_headers)

    @cached_property
    def top_level_arrays(self) -> AsyncTopLevelArraysResourceWithStreamingResponse:
        return AsyncTopLevelArraysResourceWithStreamingResponse(self._pagination_tests.top_level_arrays)

    @cached_property
    def cursor(self) -> AsyncCursorResourceWithStreamingResponse:
        return AsyncCursorResourceWithStreamingResponse(self._pagination_tests.cursor)

    @cached_property
    def cursor_id(self) -> AsyncCursorIDResourceWithStreamingResponse:
        return AsyncCursorIDResourceWithStreamingResponse(self._pagination_tests.cursor_id)

    @cached_property
    def offset(self) -> AsyncOffsetResourceWithStreamingResponse:
        return AsyncOffsetResourceWithStreamingResponse(self._pagination_tests.offset)

    @cached_property
    def fake_pages(self) -> AsyncFakePagesResourceWithStreamingResponse:
        return AsyncFakePagesResourceWithStreamingResponse(self._pagination_tests.fake_pages)

    @cached_property
    def nested_items(self) -> AsyncNestedItemsResourceWithStreamingResponse:
        return AsyncNestedItemsResourceWithStreamingResponse(self._pagination_tests.nested_items)
