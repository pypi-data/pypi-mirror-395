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
from ...pagination import SyncPageCursorTopLevelArray, AsyncPageCursorTopLevelArray
from ..._base_client import AsyncPaginator, make_request_options
from ...types.my_model import MyModel
from ...types.pagination_tests import top_level_array_basic_cursor_params

__all__ = ["TopLevelArraysResource", "AsyncTopLevelArraysResource"]


class TopLevelArraysResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TopLevelArraysResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return TopLevelArraysResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TopLevelArraysResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return TopLevelArraysResourceWithStreamingResponse(self)

    def basic_cursor(
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
    ) -> SyncPageCursorTopLevelArray[MyModel]:
        """
        Test case for top level arrays with cursor pagination

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/top_level_arrays/basic_cursor",
            page=SyncPageCursorTopLevelArray[MyModel],
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
                    top_level_array_basic_cursor_params.TopLevelArrayBasicCursorParams,
                ),
            ),
            model=MyModel,
        )


class AsyncTopLevelArraysResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTopLevelArraysResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncTopLevelArraysResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTopLevelArraysResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncTopLevelArraysResourceWithStreamingResponse(self)

    def basic_cursor(
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
    ) -> AsyncPaginator[MyModel, AsyncPageCursorTopLevelArray[MyModel]]:
        """
        Test case for top level arrays with cursor pagination

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/top_level_arrays/basic_cursor",
            page=AsyncPageCursorTopLevelArray[MyModel],
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
                    top_level_array_basic_cursor_params.TopLevelArrayBasicCursorParams,
                ),
            ),
            model=MyModel,
        )


class TopLevelArraysResourceWithRawResponse:
    def __init__(self, top_level_arrays: TopLevelArraysResource) -> None:
        self._top_level_arrays = top_level_arrays

        self.basic_cursor = _legacy_response.to_raw_response_wrapper(
            top_level_arrays.basic_cursor,
        )


class AsyncTopLevelArraysResourceWithRawResponse:
    def __init__(self, top_level_arrays: AsyncTopLevelArraysResource) -> None:
        self._top_level_arrays = top_level_arrays

        self.basic_cursor = _legacy_response.async_to_raw_response_wrapper(
            top_level_arrays.basic_cursor,
        )


class TopLevelArraysResourceWithStreamingResponse:
    def __init__(self, top_level_arrays: TopLevelArraysResource) -> None:
        self._top_level_arrays = top_level_arrays

        self.basic_cursor = to_streamed_response_wrapper(
            top_level_arrays.basic_cursor,
        )


class AsyncTopLevelArraysResourceWithStreamingResponse:
    def __init__(self, top_level_arrays: AsyncTopLevelArraysResource) -> None:
        self._top_level_arrays = top_level_arrays

        self.basic_cursor = async_to_streamed_response_wrapper(
            top_level_arrays.basic_cursor,
        )
