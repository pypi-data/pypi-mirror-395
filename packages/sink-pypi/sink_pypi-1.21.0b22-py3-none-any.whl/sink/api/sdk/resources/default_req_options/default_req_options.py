# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ... import _legacy_response
from .child import (
    ChildResource,
    AsyncChildResource,
    ChildResourceWithRawResponse,
    AsyncChildResourceWithRawResponse,
    ChildResourceWithStreamingResponse,
    AsyncChildResourceWithStreamingResponse,
)
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import is_given, strip_not_given
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ..._base_client import make_request_options
from ...types.shared.basic_shared_model_object import BasicSharedModelObject

__all__ = ["DefaultReqOptionsResource", "AsyncDefaultReqOptionsResource"]


class DefaultReqOptionsResource(SyncAPIResource):
    @cached_property
    def child(self) -> ChildResource:
        return ChildResource(self._client)

    @cached_property
    def with_raw_response(self) -> DefaultReqOptionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return DefaultReqOptionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DefaultReqOptionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return DefaultReqOptionsResourceWithStreamingResponse(self)

    def example_method(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BasicSharedModelObject:
        """Testing resource level default request options."""
        extra_headers = {"X-My-Header": "true", "X-My-Other-Header": "false", **(extra_headers or {})}
        return self._get(
            "/default_req_options",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BasicSharedModelObject,
        )

    def with_param_override(
        self,
        *,
        x_my_header: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BasicSharedModelObject:
        """
        Resource level default request options for a header that is also included in
        `parameters`.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {"X-My-Header": ("true" if x_my_header else "false") if is_given(x_my_header) else not_given}
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"X-My-Header": "true", "X-My-Other-Header": "false", **(extra_headers or {})}
        return self._get(
            "/default_req_options/with_param_override",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BasicSharedModelObject,
        )


class AsyncDefaultReqOptionsResource(AsyncAPIResource):
    @cached_property
    def child(self) -> AsyncChildResource:
        return AsyncChildResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDefaultReqOptionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncDefaultReqOptionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDefaultReqOptionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncDefaultReqOptionsResourceWithStreamingResponse(self)

    async def example_method(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BasicSharedModelObject:
        """Testing resource level default request options."""
        extra_headers = {"X-My-Header": "true", "X-My-Other-Header": "false", **(extra_headers or {})}
        return await self._get(
            "/default_req_options",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BasicSharedModelObject,
        )

    async def with_param_override(
        self,
        *,
        x_my_header: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BasicSharedModelObject:
        """
        Resource level default request options for a header that is also included in
        `parameters`.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {"X-My-Header": ("true" if x_my_header else "false") if is_given(x_my_header) else not_given}
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"X-My-Header": "true", "X-My-Other-Header": "false", **(extra_headers or {})}
        return await self._get(
            "/default_req_options/with_param_override",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BasicSharedModelObject,
        )


class DefaultReqOptionsResourceWithRawResponse:
    def __init__(self, default_req_options: DefaultReqOptionsResource) -> None:
        self._default_req_options = default_req_options

        self.example_method = _legacy_response.to_raw_response_wrapper(
            default_req_options.example_method,
        )
        self.with_param_override = _legacy_response.to_raw_response_wrapper(
            default_req_options.with_param_override,
        )

    @cached_property
    def child(self) -> ChildResourceWithRawResponse:
        return ChildResourceWithRawResponse(self._default_req_options.child)


class AsyncDefaultReqOptionsResourceWithRawResponse:
    def __init__(self, default_req_options: AsyncDefaultReqOptionsResource) -> None:
        self._default_req_options = default_req_options

        self.example_method = _legacy_response.async_to_raw_response_wrapper(
            default_req_options.example_method,
        )
        self.with_param_override = _legacy_response.async_to_raw_response_wrapper(
            default_req_options.with_param_override,
        )

    @cached_property
    def child(self) -> AsyncChildResourceWithRawResponse:
        return AsyncChildResourceWithRawResponse(self._default_req_options.child)


class DefaultReqOptionsResourceWithStreamingResponse:
    def __init__(self, default_req_options: DefaultReqOptionsResource) -> None:
        self._default_req_options = default_req_options

        self.example_method = to_streamed_response_wrapper(
            default_req_options.example_method,
        )
        self.with_param_override = to_streamed_response_wrapper(
            default_req_options.with_param_override,
        )

    @cached_property
    def child(self) -> ChildResourceWithStreamingResponse:
        return ChildResourceWithStreamingResponse(self._default_req_options.child)


class AsyncDefaultReqOptionsResourceWithStreamingResponse:
    def __init__(self, default_req_options: AsyncDefaultReqOptionsResource) -> None:
        self._default_req_options = default_req_options

        self.example_method = async_to_streamed_response_wrapper(
            default_req_options.example_method,
        )
        self.with_param_override = async_to_streamed_response_wrapper(
            default_req_options.with_param_override,
        )

    @cached_property
    def child(self) -> AsyncChildResourceWithStreamingResponse:
        return AsyncChildResourceWithStreamingResponse(self._default_req_options.child)
