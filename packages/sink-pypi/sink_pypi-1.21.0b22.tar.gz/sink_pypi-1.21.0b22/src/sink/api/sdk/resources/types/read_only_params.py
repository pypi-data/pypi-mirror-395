# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ... import _legacy_response
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ...types.types import read_only_param_simple_params
from ..._base_client import make_request_options
from ...types.types.read_only_param_simple_response import ReadOnlyParamSimpleResponse

__all__ = ["ReadOnlyParamsResource", "AsyncReadOnlyParamsResource"]


class ReadOnlyParamsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ReadOnlyParamsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return ReadOnlyParamsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ReadOnlyParamsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return ReadOnlyParamsResourceWithStreamingResponse(self)

    def simple(
        self,
        *,
        should_show_up: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ReadOnlyParamSimpleResponse:
        """
        Endpoint with a request params schema object that contains a `readOnly`
        property.

        Args:
          should_show_up: This should be generated in the request params type.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/types/read_only_params/simple",
            body=maybe_transform(
                {"should_show_up": should_show_up}, read_only_param_simple_params.ReadOnlyParamSimpleParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ReadOnlyParamSimpleResponse,
        )


class AsyncReadOnlyParamsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncReadOnlyParamsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncReadOnlyParamsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncReadOnlyParamsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncReadOnlyParamsResourceWithStreamingResponse(self)

    async def simple(
        self,
        *,
        should_show_up: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ReadOnlyParamSimpleResponse:
        """
        Endpoint with a request params schema object that contains a `readOnly`
        property.

        Args:
          should_show_up: This should be generated in the request params type.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/types/read_only_params/simple",
            body=await async_maybe_transform(
                {"should_show_up": should_show_up}, read_only_param_simple_params.ReadOnlyParamSimpleParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ReadOnlyParamSimpleResponse,
        )


class ReadOnlyParamsResourceWithRawResponse:
    def __init__(self, read_only_params: ReadOnlyParamsResource) -> None:
        self._read_only_params = read_only_params

        self.simple = _legacy_response.to_raw_response_wrapper(
            read_only_params.simple,
        )


class AsyncReadOnlyParamsResourceWithRawResponse:
    def __init__(self, read_only_params: AsyncReadOnlyParamsResource) -> None:
        self._read_only_params = read_only_params

        self.simple = _legacy_response.async_to_raw_response_wrapper(
            read_only_params.simple,
        )


class ReadOnlyParamsResourceWithStreamingResponse:
    def __init__(self, read_only_params: ReadOnlyParamsResource) -> None:
        self._read_only_params = read_only_params

        self.simple = to_streamed_response_wrapper(
            read_only_params.simple,
        )


class AsyncReadOnlyParamsResourceWithStreamingResponse:
    def __init__(self, read_only_params: AsyncReadOnlyParamsResource) -> None:
        self._read_only_params = read_only_params

        self.simple = async_to_streamed_response_wrapper(
            read_only_params.simple,
        )
