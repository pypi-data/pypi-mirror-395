# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from .. import _legacy_response
from .._types import Body, Query, Headers, NotGiven, not_given
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from .._base_client import make_request_options
from ..types.widget import Widget

__all__ = ["WidgetsResource", "AsyncWidgetsResource"]


class WidgetsResource(SyncAPIResource):
    """
    Widget is love
    Widget is life
    """

    @cached_property
    def with_raw_response(self) -> WidgetsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return WidgetsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WidgetsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return WidgetsResourceWithStreamingResponse(self)

    def retrieve_with_filter(
        self,
        filter_type: Literal["available", "archived", "out_of_stock"],
        *,
        widget_id: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Widget:
        """
        Endpoint that tests using an integer and enum in the pathParams

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not filter_type:
            raise ValueError(f"Expected a non-empty value for `filter_type` but received {filter_type!r}")
        return self._get(
            f"/widgets/{widget_id}/filter/{filter_type}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Widget,
        )


class AsyncWidgetsResource(AsyncAPIResource):
    """
    Widget is love
    Widget is life
    """

    @cached_property
    def with_raw_response(self) -> AsyncWidgetsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncWidgetsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWidgetsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncWidgetsResourceWithStreamingResponse(self)

    async def retrieve_with_filter(
        self,
        filter_type: Literal["available", "archived", "out_of_stock"],
        *,
        widget_id: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Widget:
        """
        Endpoint that tests using an integer and enum in the pathParams

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not filter_type:
            raise ValueError(f"Expected a non-empty value for `filter_type` but received {filter_type!r}")
        return await self._get(
            f"/widgets/{widget_id}/filter/{filter_type}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Widget,
        )


class WidgetsResourceWithRawResponse:
    def __init__(self, widgets: WidgetsResource) -> None:
        self._widgets = widgets

        self.retrieve_with_filter = _legacy_response.to_raw_response_wrapper(
            widgets.retrieve_with_filter,
        )


class AsyncWidgetsResourceWithRawResponse:
    def __init__(self, widgets: AsyncWidgetsResource) -> None:
        self._widgets = widgets

        self.retrieve_with_filter = _legacy_response.async_to_raw_response_wrapper(
            widgets.retrieve_with_filter,
        )


class WidgetsResourceWithStreamingResponse:
    def __init__(self, widgets: WidgetsResource) -> None:
        self._widgets = widgets

        self.retrieve_with_filter = to_streamed_response_wrapper(
            widgets.retrieve_with_filter,
        )


class AsyncWidgetsResourceWithStreamingResponse:
    def __init__(self, widgets: AsyncWidgetsResource) -> None:
        self._widgets = widgets

        self.retrieve_with_filter = async_to_streamed_response_wrapper(
            widgets.retrieve_with_filter,
        )
