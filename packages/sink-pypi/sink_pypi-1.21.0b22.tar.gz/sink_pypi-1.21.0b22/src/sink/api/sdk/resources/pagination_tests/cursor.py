# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ... import _legacy_response
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ...pagination import (
    SyncPageCursor,
    AsyncPageCursor,
    SyncPageCursorWithHasMore,
    SyncPageCursorWithReverse,
    AsyncPageCursorWithHasMore,
    AsyncPageCursorWithReverse,
    SyncPageCursorWithNestedHasMore,
    AsyncPageCursorWithNestedHasMore,
)
from ..._base_client import AsyncPaginator, make_request_options
from ...types.my_model import MyModel
from ...types.pagination_tests import (
    cursor_list_params,
    cursor_list_reverse_params,
    cursor_list_has_more_params,
    cursor_list_nested_has_more_params,
)

__all__ = ["CursorResource", "AsyncCursorResource"]


class CursorResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CursorResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return CursorResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CursorResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return CursorResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        cursor: Optional[str] | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[MyModel]:
        """
        Test case for cursor pagination

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/cursor",
            page=SyncPageCursor[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "limit": limit,
                    },
                    cursor_list_params.CursorListParams,
                ),
            ),
            model=MyModel,
        )

    def list_has_more(
        self,
        *,
        cursor: Optional[str] | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursorWithHasMore[MyModel]:
        """
        Test case for cursor pagination with a `has_more` indicator

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/cursor_with_has_more",
            page=SyncPageCursorWithHasMore[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "limit": limit,
                    },
                    cursor_list_has_more_params.CursorListHasMoreParams,
                ),
            ),
            model=MyModel,
        )

    def list_nested_has_more(
        self,
        *,
        cursor: Optional[str] | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursorWithNestedHasMore[MyModel]:
        """
        Test case for cursor pagination with a `has_more` indicator inside an object

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/cursor_with_nested_has_more",
            page=SyncPageCursorWithNestedHasMore[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "limit": limit,
                    },
                    cursor_list_nested_has_more_params.CursorListNestedHasMoreParams,
                ),
            ),
            model=MyModel,
        )

    def list_reverse(
        self,
        *,
        after_id: Optional[str] | Omit = omit,
        before_id: Optional[str] | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursorWithReverse[MyModel]:
        """
        Test case for cursor pagination with reverse support

        Args:
          after_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately after this object.

          before_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately before this object.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/cursor_with_reverse",
            page=SyncPageCursorWithReverse[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after_id": after_id,
                        "before_id": before_id,
                        "limit": limit,
                    },
                    cursor_list_reverse_params.CursorListReverseParams,
                ),
            ),
            model=MyModel,
        )


class AsyncCursorResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCursorResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncCursorResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCursorResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncCursorResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        cursor: Optional[str] | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[MyModel, AsyncPageCursor[MyModel]]:
        """
        Test case for cursor pagination

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/cursor",
            page=AsyncPageCursor[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "limit": limit,
                    },
                    cursor_list_params.CursorListParams,
                ),
            ),
            model=MyModel,
        )

    def list_has_more(
        self,
        *,
        cursor: Optional[str] | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[MyModel, AsyncPageCursorWithHasMore[MyModel]]:
        """
        Test case for cursor pagination with a `has_more` indicator

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/cursor_with_has_more",
            page=AsyncPageCursorWithHasMore[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "limit": limit,
                    },
                    cursor_list_has_more_params.CursorListHasMoreParams,
                ),
            ),
            model=MyModel,
        )

    def list_nested_has_more(
        self,
        *,
        cursor: Optional[str] | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[MyModel, AsyncPageCursorWithNestedHasMore[MyModel]]:
        """
        Test case for cursor pagination with a `has_more` indicator inside an object

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/cursor_with_nested_has_more",
            page=AsyncPageCursorWithNestedHasMore[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "limit": limit,
                    },
                    cursor_list_nested_has_more_params.CursorListNestedHasMoreParams,
                ),
            ),
            model=MyModel,
        )

    def list_reverse(
        self,
        *,
        after_id: Optional[str] | Omit = omit,
        before_id: Optional[str] | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[MyModel, AsyncPageCursorWithReverse[MyModel]]:
        """
        Test case for cursor pagination with reverse support

        Args:
          after_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately after this object.

          before_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately before this object.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/cursor_with_reverse",
            page=AsyncPageCursorWithReverse[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after_id": after_id,
                        "before_id": before_id,
                        "limit": limit,
                    },
                    cursor_list_reverse_params.CursorListReverseParams,
                ),
            ),
            model=MyModel,
        )


class CursorResourceWithRawResponse:
    def __init__(self, cursor: CursorResource) -> None:
        self._cursor = cursor

        self.list = _legacy_response.to_raw_response_wrapper(
            cursor.list,
        )
        self.list_has_more = _legacy_response.to_raw_response_wrapper(
            cursor.list_has_more,
        )
        self.list_nested_has_more = _legacy_response.to_raw_response_wrapper(
            cursor.list_nested_has_more,
        )
        self.list_reverse = _legacy_response.to_raw_response_wrapper(
            cursor.list_reverse,
        )


class AsyncCursorResourceWithRawResponse:
    def __init__(self, cursor: AsyncCursorResource) -> None:
        self._cursor = cursor

        self.list = _legacy_response.async_to_raw_response_wrapper(
            cursor.list,
        )
        self.list_has_more = _legacy_response.async_to_raw_response_wrapper(
            cursor.list_has_more,
        )
        self.list_nested_has_more = _legacy_response.async_to_raw_response_wrapper(
            cursor.list_nested_has_more,
        )
        self.list_reverse = _legacy_response.async_to_raw_response_wrapper(
            cursor.list_reverse,
        )


class CursorResourceWithStreamingResponse:
    def __init__(self, cursor: CursorResource) -> None:
        self._cursor = cursor

        self.list = to_streamed_response_wrapper(
            cursor.list,
        )
        self.list_has_more = to_streamed_response_wrapper(
            cursor.list_has_more,
        )
        self.list_nested_has_more = to_streamed_response_wrapper(
            cursor.list_nested_has_more,
        )
        self.list_reverse = to_streamed_response_wrapper(
            cursor.list_reverse,
        )


class AsyncCursorResourceWithStreamingResponse:
    def __init__(self, cursor: AsyncCursorResource) -> None:
        self._cursor = cursor

        self.list = async_to_streamed_response_wrapper(
            cursor.list,
        )
        self.list_has_more = async_to_streamed_response_wrapper(
            cursor.list_has_more,
        )
        self.list_nested_has_more = async_to_streamed_response_wrapper(
            cursor.list_nested_has_more,
        )
        self.list_reverse = async_to_streamed_response_wrapper(
            cursor.list_reverse,
        )
