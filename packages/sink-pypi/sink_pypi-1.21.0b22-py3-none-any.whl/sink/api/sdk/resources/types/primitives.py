# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ... import _legacy_response
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ...types.types import ModelString, primitive_strings_params
from ..._base_client import make_request_options
from ...types.types.model_string import ModelString
from ...types.types.primitive_strings_response import PrimitiveStringsResponse

__all__ = ["PrimitivesResource", "AsyncPrimitivesResource"]


class PrimitivesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PrimitivesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return PrimitivesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PrimitivesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return PrimitivesResourceWithStreamingResponse(self)

    def strings(
        self,
        *,
        string_param: ModelString | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> PrimitiveStringsResponse:
        """
        Endpoint that has a request body property that points to a string model &
        returns an object with a string model prop

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/types/primitives/strings",
            body=maybe_transform({"string_param": string_param}, primitive_strings_params.PrimitiveStringsParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=PrimitiveStringsResponse,
        )


class AsyncPrimitivesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPrimitivesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncPrimitivesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPrimitivesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncPrimitivesResourceWithStreamingResponse(self)

    async def strings(
        self,
        *,
        string_param: ModelString | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> PrimitiveStringsResponse:
        """
        Endpoint that has a request body property that points to a string model &
        returns an object with a string model prop

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/types/primitives/strings",
            body=await async_maybe_transform(
                {"string_param": string_param}, primitive_strings_params.PrimitiveStringsParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=PrimitiveStringsResponse,
        )


class PrimitivesResourceWithRawResponse:
    def __init__(self, primitives: PrimitivesResource) -> None:
        self._primitives = primitives

        self.strings = _legacy_response.to_raw_response_wrapper(
            primitives.strings,
        )


class AsyncPrimitivesResourceWithRawResponse:
    def __init__(self, primitives: AsyncPrimitivesResource) -> None:
        self._primitives = primitives

        self.strings = _legacy_response.async_to_raw_response_wrapper(
            primitives.strings,
        )


class PrimitivesResourceWithStreamingResponse:
    def __init__(self, primitives: PrimitivesResource) -> None:
        self._primitives = primitives

        self.strings = to_streamed_response_wrapper(
            primitives.strings,
        )


class AsyncPrimitivesResourceWithStreamingResponse:
    def __init__(self, primitives: AsyncPrimitivesResource) -> None:
        self._primitives = primitives

        self.strings = async_to_streamed_response_wrapper(
            primitives.strings,
        )
