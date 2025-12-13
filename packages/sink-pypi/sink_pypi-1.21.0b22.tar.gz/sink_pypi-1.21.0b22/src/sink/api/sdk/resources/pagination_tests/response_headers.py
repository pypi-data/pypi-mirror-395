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
from ...pagination import SyncPageCursorFromHeaders, AsyncPageCursorFromHeaders
from ..._base_client import AsyncPaginator, make_request_options
from ...types.my_model import MyModel
from ...types.pagination_tests import response_header_basic_cursor_params

__all__ = ["ResponseHeadersResource", "AsyncResponseHeadersResource"]


class ResponseHeadersResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ResponseHeadersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return ResponseHeadersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ResponseHeadersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return ResponseHeadersResourceWithStreamingResponse(self)

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
    ) -> SyncPageCursorFromHeaders[MyModel]:
        """
        Test case for response headers with cursor pagination

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/response_headers/basic_cursor",
            page=SyncPageCursorFromHeaders[MyModel],
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
                    response_header_basic_cursor_params.ResponseHeaderBasicCursorParams,
                ),
            ),
            model=MyModel,
        )


class AsyncResponseHeadersResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncResponseHeadersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncResponseHeadersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncResponseHeadersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncResponseHeadersResourceWithStreamingResponse(self)

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
    ) -> AsyncPaginator[MyModel, AsyncPageCursorFromHeaders[MyModel]]:
        """
        Test case for response headers with cursor pagination

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/response_headers/basic_cursor",
            page=AsyncPageCursorFromHeaders[MyModel],
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
                    response_header_basic_cursor_params.ResponseHeaderBasicCursorParams,
                ),
            ),
            model=MyModel,
        )


class ResponseHeadersResourceWithRawResponse:
    def __init__(self, response_headers: ResponseHeadersResource) -> None:
        self._response_headers = response_headers

        self.basic_cursor = _legacy_response.to_raw_response_wrapper(
            response_headers.basic_cursor,
        )


class AsyncResponseHeadersResourceWithRawResponse:
    def __init__(self, response_headers: AsyncResponseHeadersResource) -> None:
        self._response_headers = response_headers

        self.basic_cursor = _legacy_response.async_to_raw_response_wrapper(
            response_headers.basic_cursor,
        )


class ResponseHeadersResourceWithStreamingResponse:
    def __init__(self, response_headers: ResponseHeadersResource) -> None:
        self._response_headers = response_headers

        self.basic_cursor = to_streamed_response_wrapper(
            response_headers.basic_cursor,
        )


class AsyncResponseHeadersResourceWithStreamingResponse:
    def __init__(self, response_headers: AsyncResponseHeadersResource) -> None:
        self._response_headers = response_headers

        self.basic_cursor = async_to_streamed_response_wrapper(
            response_headers.basic_cursor,
        )
