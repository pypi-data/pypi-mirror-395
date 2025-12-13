# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ... import _legacy_response
from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ..._base_client import make_request_options
from ...types.shared.shared_self_recursion import SharedSelfRecursion

__all__ = ["SharedResponsesResource", "AsyncSharedResponsesResource"]


class SharedResponsesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SharedResponsesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return SharedResponsesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SharedResponsesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return SharedResponsesResourceWithStreamingResponse(self)

    def create_self(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> SharedSelfRecursion:
        return self._post(
            "/recursion/shared/responses/self",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=SharedSelfRecursion,
        )


class AsyncSharedResponsesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSharedResponsesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncSharedResponsesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSharedResponsesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncSharedResponsesResourceWithStreamingResponse(self)

    async def create_self(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> SharedSelfRecursion:
        return await self._post(
            "/recursion/shared/responses/self",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=SharedSelfRecursion,
        )


class SharedResponsesResourceWithRawResponse:
    def __init__(self, shared_responses: SharedResponsesResource) -> None:
        self._shared_responses = shared_responses

        self.create_self = _legacy_response.to_raw_response_wrapper(
            shared_responses.create_self,
        )


class AsyncSharedResponsesResourceWithRawResponse:
    def __init__(self, shared_responses: AsyncSharedResponsesResource) -> None:
        self._shared_responses = shared_responses

        self.create_self = _legacy_response.async_to_raw_response_wrapper(
            shared_responses.create_self,
        )


class SharedResponsesResourceWithStreamingResponse:
    def __init__(self, shared_responses: SharedResponsesResource) -> None:
        self._shared_responses = shared_responses

        self.create_self = to_streamed_response_wrapper(
            shared_responses.create_self,
        )


class AsyncSharedResponsesResourceWithStreamingResponse:
    def __init__(self, shared_responses: AsyncSharedResponsesResource) -> None:
        self._shared_responses = shared_responses

        self.create_self = async_to_streamed_response_wrapper(
            shared_responses.create_self,
        )
