# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ... import _legacy_response
from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ..._base_client import make_request_options
from ...types.decorator_tests.skip_this_resource_i_never_appear_response import SkipThisResourceINeverAppearResponse

__all__ = ["SkipThisResourceResource", "AsyncSkipThisResourceResource"]


class SkipThisResourceResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SkipThisResourceResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return SkipThisResourceResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SkipThisResourceResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return SkipThisResourceResourceWithStreamingResponse(self)

    def i_never_appear(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SkipThisResourceINeverAppearResponse:
        """Nested method that should never render because its parent resource is skipped."""
        return self._get(
            "/decorator_tests/nested/i/never/appear",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SkipThisResourceINeverAppearResponse,
        )


class AsyncSkipThisResourceResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSkipThisResourceResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncSkipThisResourceResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSkipThisResourceResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncSkipThisResourceResourceWithStreamingResponse(self)

    async def i_never_appear(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SkipThisResourceINeverAppearResponse:
        """Nested method that should never render because its parent resource is skipped."""
        return await self._get(
            "/decorator_tests/nested/i/never/appear",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SkipThisResourceINeverAppearResponse,
        )


class SkipThisResourceResourceWithRawResponse:
    def __init__(self, skip_this_resource: SkipThisResourceResource) -> None:
        self._skip_this_resource = skip_this_resource

        self.i_never_appear = _legacy_response.to_raw_response_wrapper(
            skip_this_resource.i_never_appear,
        )


class AsyncSkipThisResourceResourceWithRawResponse:
    def __init__(self, skip_this_resource: AsyncSkipThisResourceResource) -> None:
        self._skip_this_resource = skip_this_resource

        self.i_never_appear = _legacy_response.async_to_raw_response_wrapper(
            skip_this_resource.i_never_appear,
        )


class SkipThisResourceResourceWithStreamingResponse:
    def __init__(self, skip_this_resource: SkipThisResourceResource) -> None:
        self._skip_this_resource = skip_this_resource

        self.i_never_appear = to_streamed_response_wrapper(
            skip_this_resource.i_never_appear,
        )


class AsyncSkipThisResourceResourceWithStreamingResponse:
    def __init__(self, skip_this_resource: AsyncSkipThisResourceResource) -> None:
        self._skip_this_resource = skip_this_resource

        self.i_never_appear = async_to_streamed_response_wrapper(
            skip_this_resource.i_never_appear,
        )
