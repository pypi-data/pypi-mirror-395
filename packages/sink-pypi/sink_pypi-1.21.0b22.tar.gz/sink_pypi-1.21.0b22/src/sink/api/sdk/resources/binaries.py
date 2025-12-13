# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import binary_with_path_and_body_param_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_custom_raw_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from .._base_client import make_request_options

__all__ = ["BinariesResource", "AsyncBinariesResource"]


class BinariesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BinariesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return BinariesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BinariesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return BinariesResourceWithStreamingResponse(self)

    def return_binary(
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

    def with_path_and_body_param(
        self,
        id: str,
        *,
        foo: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BinaryAPIResponse:
        """
        Return a binary response.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "audio/mpeg", **(extra_headers or {})}
        return self._post(
            f"/binaries/with_path_and_body_param/{id}",
            body=maybe_transform({"foo": foo}, binary_with_path_and_body_param_params.BinaryWithPathAndBodyParamParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BinaryAPIResponse,
        )

    def with_path_param(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BinaryAPIResponse:
        """
        Return a binary response.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "audio/mpeg", **(extra_headers or {})}
        return self._get(
            f"/binaries/with_path_param/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncBinariesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBinariesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncBinariesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBinariesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncBinariesResourceWithStreamingResponse(self)

    async def return_binary(
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

    async def with_path_and_body_param(
        self,
        id: str,
        *,
        foo: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> AsyncBinaryAPIResponse:
        """
        Return a binary response.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "audio/mpeg", **(extra_headers or {})}
        return await self._post(
            f"/binaries/with_path_and_body_param/{id}",
            body=await async_maybe_transform(
                {"foo": foo}, binary_with_path_and_body_param_params.BinaryWithPathAndBodyParamParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def with_path_param(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncBinaryAPIResponse:
        """
        Return a binary response.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "audio/mpeg", **(extra_headers or {})}
        return await self._get(
            f"/binaries/with_path_param/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class BinariesResourceWithRawResponse:
    def __init__(self, binaries: BinariesResource) -> None:
        self._binaries = binaries

        self.return_binary = to_custom_raw_response_wrapper(
            binaries.return_binary,
            BinaryAPIResponse,
        )
        self.with_path_and_body_param = to_custom_raw_response_wrapper(
            binaries.with_path_and_body_param,
            BinaryAPIResponse,
        )
        self.with_path_param = to_custom_raw_response_wrapper(
            binaries.with_path_param,
            BinaryAPIResponse,
        )


class AsyncBinariesResourceWithRawResponse:
    def __init__(self, binaries: AsyncBinariesResource) -> None:
        self._binaries = binaries

        self.return_binary = async_to_custom_raw_response_wrapper(
            binaries.return_binary,
            AsyncBinaryAPIResponse,
        )
        self.with_path_and_body_param = async_to_custom_raw_response_wrapper(
            binaries.with_path_and_body_param,
            AsyncBinaryAPIResponse,
        )
        self.with_path_param = async_to_custom_raw_response_wrapper(
            binaries.with_path_param,
            AsyncBinaryAPIResponse,
        )


class BinariesResourceWithStreamingResponse:
    def __init__(self, binaries: BinariesResource) -> None:
        self._binaries = binaries

        self.return_binary = to_custom_streamed_response_wrapper(
            binaries.return_binary,
            StreamedBinaryAPIResponse,
        )
        self.with_path_and_body_param = to_custom_streamed_response_wrapper(
            binaries.with_path_and_body_param,
            StreamedBinaryAPIResponse,
        )
        self.with_path_param = to_custom_streamed_response_wrapper(
            binaries.with_path_param,
            StreamedBinaryAPIResponse,
        )


class AsyncBinariesResourceWithStreamingResponse:
    def __init__(self, binaries: AsyncBinariesResource) -> None:
        self._binaries = binaries

        self.return_binary = async_to_custom_streamed_response_wrapper(
            binaries.return_binary,
            AsyncStreamedBinaryAPIResponse,
        )
        self.with_path_and_body_param = async_to_custom_streamed_response_wrapper(
            binaries.with_path_and_body_param,
            AsyncStreamedBinaryAPIResponse,
        )
        self.with_path_param = async_to_custom_streamed_response_wrapper(
            binaries.with_path_param,
            AsyncStreamedBinaryAPIResponse,
        )
