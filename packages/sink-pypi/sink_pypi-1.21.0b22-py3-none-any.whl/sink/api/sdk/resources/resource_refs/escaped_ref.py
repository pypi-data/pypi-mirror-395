# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ... import _legacy_response
from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ..._base_client import make_request_options
from ...types.resource_refs.model_with_escaped_name import ModelWithEscapedName

__all__ = ["EscapedRefResource", "AsyncEscapedRefResource"]


class EscapedRefResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EscapedRefResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return EscapedRefResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EscapedRefResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return EscapedRefResourceWithStreamingResponse(self)

    def get(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelWithEscapedName:
        """endpoint that returns a model with escaped slashes in its ref"""
        return self._get(
            "/resource_refs/escaped_ref",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelWithEscapedName,
        )


class AsyncEscapedRefResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEscapedRefResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncEscapedRefResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEscapedRefResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncEscapedRefResourceWithStreamingResponse(self)

    async def get(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelWithEscapedName:
        """endpoint that returns a model with escaped slashes in its ref"""
        return await self._get(
            "/resource_refs/escaped_ref",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelWithEscapedName,
        )


class EscapedRefResourceWithRawResponse:
    def __init__(self, escaped_ref: EscapedRefResource) -> None:
        self._escaped_ref = escaped_ref

        self.get = _legacy_response.to_raw_response_wrapper(
            escaped_ref.get,
        )


class AsyncEscapedRefResourceWithRawResponse:
    def __init__(self, escaped_ref: AsyncEscapedRefResource) -> None:
        self._escaped_ref = escaped_ref

        self.get = _legacy_response.async_to_raw_response_wrapper(
            escaped_ref.get,
        )


class EscapedRefResourceWithStreamingResponse:
    def __init__(self, escaped_ref: EscapedRefResource) -> None:
        self._escaped_ref = escaped_ref

        self.get = to_streamed_response_wrapper(
            escaped_ref.get,
        )


class AsyncEscapedRefResourceWithStreamingResponse:
    def __init__(self, escaped_ref: AsyncEscapedRefResource) -> None:
        self._escaped_ref = escaped_ref

        self.get = async_to_streamed_response_wrapper(
            escaped_ref.get,
        )
