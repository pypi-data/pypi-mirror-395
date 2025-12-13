# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import Body, Query, Headers, NotGiven, not_given
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_custom_raw_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ...._base_client import make_request_options

__all__ = ["ResponseResource", "AsyncResponseResource"]


class ResponseResource(SyncAPIResource):
    """The `Response` class name can cause clashes with imports."""

    @cached_property
    def with_raw_response(self) -> ResponseResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return ResponseResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ResponseResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return ResponseResourceWithStreamingResponse(self)

    def binary_return(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BinaryAPIResponse:
        """Return a binary response."""
        extra_headers = {"Accept": "audio/mpeg", **(extra_headers or {})}
        return self._get(
            "/binaries/return_binary",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncResponseResource(AsyncAPIResource):
    """The `Response` class name can cause clashes with imports."""

    @cached_property
    def with_raw_response(self) -> AsyncResponseResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncResponseResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncResponseResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncResponseResourceWithStreamingResponse(self)

    async def binary_return(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncBinaryAPIResponse:
        """Return a binary response."""
        extra_headers = {"Accept": "audio/mpeg", **(extra_headers or {})}
        return await self._get(
            "/binaries/return_binary",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class ResponseResourceWithRawResponse:
    def __init__(self, response: ResponseResource) -> None:
        self._response = response

        self.binary_return = to_custom_raw_response_wrapper(
            response.binary_return,
            BinaryAPIResponse,
        )


class AsyncResponseResourceWithRawResponse:
    def __init__(self, response: AsyncResponseResource) -> None:
        self._response = response

        self.binary_return = async_to_custom_raw_response_wrapper(
            response.binary_return,
            AsyncBinaryAPIResponse,
        )


class ResponseResourceWithStreamingResponse:
    def __init__(self, response: ResponseResource) -> None:
        self._response = response

        self.binary_return = to_custom_streamed_response_wrapper(
            response.binary_return,
            StreamedBinaryAPIResponse,
        )


class AsyncResponseResourceWithStreamingResponse:
    def __init__(self, response: AsyncResponseResource) -> None:
        self._response = response

        self.binary_return = async_to_custom_streamed_response_wrapper(
            response.binary_return,
            AsyncStreamedBinaryAPIResponse,
        )
