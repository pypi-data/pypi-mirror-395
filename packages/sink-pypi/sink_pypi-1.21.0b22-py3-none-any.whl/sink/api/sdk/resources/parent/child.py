# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ... import _legacy_response
from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ..._base_client import make_request_options
from ...types.parent.child_inlined_response_response import ChildInlinedResponseResponse

__all__ = ["ChildResource", "AsyncChildResource"]


class ChildResource(SyncAPIResource):
    """
    Some children can be very large
    For example, the children of Godzilla
    """

    @cached_property
    def with_raw_response(self) -> ChildResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return ChildResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ChildResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return ChildResourceWithStreamingResponse(self)

    def inlined_response(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ChildInlinedResponseResponse:
        """Method with inlined response model."""
        return self._get(
            "/inlined_response",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChildInlinedResponseResponse,
        )


class AsyncChildResource(AsyncAPIResource):
    """
    Some children can be very large
    For example, the children of Godzilla
    """

    @cached_property
    def with_raw_response(self) -> AsyncChildResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncChildResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncChildResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncChildResourceWithStreamingResponse(self)

    async def inlined_response(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ChildInlinedResponseResponse:
        """Method with inlined response model."""
        return await self._get(
            "/inlined_response",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChildInlinedResponseResponse,
        )


class ChildResourceWithRawResponse:
    def __init__(self, child: ChildResource) -> None:
        self._child = child

        self.inlined_response = _legacy_response.to_raw_response_wrapper(
            child.inlined_response,
        )


class AsyncChildResourceWithRawResponse:
    def __init__(self, child: AsyncChildResource) -> None:
        self._child = child

        self.inlined_response = _legacy_response.async_to_raw_response_wrapper(
            child.inlined_response,
        )


class ChildResourceWithStreamingResponse:
    def __init__(self, child: ChildResource) -> None:
        self._child = child

        self.inlined_response = to_streamed_response_wrapper(
            child.inlined_response,
        )


class AsyncChildResourceWithStreamingResponse:
    def __init__(self, child: AsyncChildResource) -> None:
        self._child = child

        self.inlined_response = async_to_streamed_response_wrapper(
            child.inlined_response,
        )
