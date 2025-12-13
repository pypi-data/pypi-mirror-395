# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict

import httpx

from ... import _legacy_response
from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ...types.types import map_unknown_items_params
from ..._base_client import make_request_options
from ...types.types.map_unknown_items_response import MapUnknownItemsResponse

__all__ = ["MapsResource", "AsyncMapsResource"]


class MapsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MapsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return MapsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MapsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return MapsResourceWithStreamingResponse(self)

    def unknown_items(
        self,
        *,
        any_map: Dict[str, object],
        unknown_map: Dict[str, object],
        unspecified_type_object_map: Dict[str, object],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> MapUnknownItemsResponse:
        """
        Endpoint with a response schema object that contains properties that use
        `additionalProperties` with an unknown or a 'type: object' schema without any
        additional definitions.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/types/map/unknown_items",
            body=maybe_transform(
                {
                    "any_map": any_map,
                    "unknown_map": unknown_map,
                    "unspecified_type_object_map": unspecified_type_object_map,
                },
                map_unknown_items_params.MapUnknownItemsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=MapUnknownItemsResponse,
        )


class AsyncMapsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMapsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncMapsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMapsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncMapsResourceWithStreamingResponse(self)

    async def unknown_items(
        self,
        *,
        any_map: Dict[str, object],
        unknown_map: Dict[str, object],
        unspecified_type_object_map: Dict[str, object],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> MapUnknownItemsResponse:
        """
        Endpoint with a response schema object that contains properties that use
        `additionalProperties` with an unknown or a 'type: object' schema without any
        additional definitions.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/types/map/unknown_items",
            body=await async_maybe_transform(
                {
                    "any_map": any_map,
                    "unknown_map": unknown_map,
                    "unspecified_type_object_map": unspecified_type_object_map,
                },
                map_unknown_items_params.MapUnknownItemsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=MapUnknownItemsResponse,
        )


class MapsResourceWithRawResponse:
    def __init__(self, maps: MapsResource) -> None:
        self._maps = maps

        self.unknown_items = _legacy_response.to_raw_response_wrapper(
            maps.unknown_items,
        )


class AsyncMapsResourceWithRawResponse:
    def __init__(self, maps: AsyncMapsResource) -> None:
        self._maps = maps

        self.unknown_items = _legacy_response.async_to_raw_response_wrapper(
            maps.unknown_items,
        )


class MapsResourceWithStreamingResponse:
    def __init__(self, maps: MapsResource) -> None:
        self._maps = maps

        self.unknown_items = to_streamed_response_wrapper(
            maps.unknown_items,
        )


class AsyncMapsResourceWithStreamingResponse:
    def __init__(self, maps: AsyncMapsResource) -> None:
        self._maps = maps

        self.unknown_items = async_to_streamed_response_wrapper(
            maps.unknown_items,
        )
