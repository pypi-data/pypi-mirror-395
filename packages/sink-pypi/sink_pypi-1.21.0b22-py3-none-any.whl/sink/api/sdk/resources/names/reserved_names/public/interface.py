# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..... import _legacy_response
from ....._types import Body, Query, Headers, NotGiven, not_given
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ....._base_client import make_request_options
from .....types.names.reserved_names.public.interface import Interface

__all__ = ["InterfaceResource", "AsyncInterfaceResource"]


class InterfaceResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> InterfaceResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return InterfaceResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> InterfaceResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return InterfaceResourceWithStreamingResponse(self)

    def interface(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Interface:
        return self._get(
            "/names/reserved_names/public/interface",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Interface,
        )


class AsyncInterfaceResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncInterfaceResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncInterfaceResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncInterfaceResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncInterfaceResourceWithStreamingResponse(self)

    async def interface(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Interface:
        return await self._get(
            "/names/reserved_names/public/interface",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Interface,
        )


class InterfaceResourceWithRawResponse:
    def __init__(self, interface: InterfaceResource) -> None:
        self._interface = interface

        self.interface = _legacy_response.to_raw_response_wrapper(
            interface.interface,
        )


class AsyncInterfaceResourceWithRawResponse:
    def __init__(self, interface: AsyncInterfaceResource) -> None:
        self._interface = interface

        self.interface = _legacy_response.async_to_raw_response_wrapper(
            interface.interface,
        )


class InterfaceResourceWithStreamingResponse:
    def __init__(self, interface: InterfaceResource) -> None:
        self._interface = interface

        self.interface = to_streamed_response_wrapper(
            interface.interface,
        )


class AsyncInterfaceResourceWithStreamingResponse:
    def __init__(self, interface: AsyncInterfaceResource) -> None:
        self._interface = interface

        self.interface = async_to_streamed_response_wrapper(
            interface.interface,
        )
