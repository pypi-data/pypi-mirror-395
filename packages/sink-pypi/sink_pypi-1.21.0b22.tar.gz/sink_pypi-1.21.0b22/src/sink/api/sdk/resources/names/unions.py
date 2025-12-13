# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, cast

import httpx

from ... import _legacy_response
from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ..._base_client import make_request_options
from ...types.names.discriminated_union import DiscriminatedUnion
from ...types.object_with_union_properties import ObjectWithUnionProperties
from ...types.names.variants_single_prop_objects import VariantsSinglePropObjects

__all__ = ["UnionsResource", "AsyncUnionsResource"]


class UnionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> UnionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return UnionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UnionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return UnionsResourceWithStreamingResponse(self)

    def discriminated(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DiscriminatedUnion:
        return cast(
            DiscriminatedUnion,
            self._get(
                "/names/unions/discriminated_union",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, DiscriminatedUnion
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def variants_object_with_union_properties(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ObjectWithUnionProperties:
        return self._get(
            "/names/unions/variants_object_with_union_properties",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectWithUnionProperties,
        )

    def variants_single_prop_objects(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VariantsSinglePropObjects:
        return cast(
            VariantsSinglePropObjects,
            self._get(
                "/names/unions/variants_single_prop_objects",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, VariantsSinglePropObjects
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class AsyncUnionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncUnionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncUnionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUnionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncUnionsResourceWithStreamingResponse(self)

    async def discriminated(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DiscriminatedUnion:
        return cast(
            DiscriminatedUnion,
            await self._get(
                "/names/unions/discriminated_union",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, DiscriminatedUnion
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def variants_object_with_union_properties(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ObjectWithUnionProperties:
        return await self._get(
            "/names/unions/variants_object_with_union_properties",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectWithUnionProperties,
        )

    async def variants_single_prop_objects(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VariantsSinglePropObjects:
        return cast(
            VariantsSinglePropObjects,
            await self._get(
                "/names/unions/variants_single_prop_objects",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, VariantsSinglePropObjects
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class UnionsResourceWithRawResponse:
    def __init__(self, unions: UnionsResource) -> None:
        self._unions = unions

        self.discriminated = _legacy_response.to_raw_response_wrapper(
            unions.discriminated,
        )
        self.variants_object_with_union_properties = _legacy_response.to_raw_response_wrapper(
            unions.variants_object_with_union_properties,
        )
        self.variants_single_prop_objects = _legacy_response.to_raw_response_wrapper(
            unions.variants_single_prop_objects,
        )


class AsyncUnionsResourceWithRawResponse:
    def __init__(self, unions: AsyncUnionsResource) -> None:
        self._unions = unions

        self.discriminated = _legacy_response.async_to_raw_response_wrapper(
            unions.discriminated,
        )
        self.variants_object_with_union_properties = _legacy_response.async_to_raw_response_wrapper(
            unions.variants_object_with_union_properties,
        )
        self.variants_single_prop_objects = _legacy_response.async_to_raw_response_wrapper(
            unions.variants_single_prop_objects,
        )


class UnionsResourceWithStreamingResponse:
    def __init__(self, unions: UnionsResource) -> None:
        self._unions = unions

        self.discriminated = to_streamed_response_wrapper(
            unions.discriminated,
        )
        self.variants_object_with_union_properties = to_streamed_response_wrapper(
            unions.variants_object_with_union_properties,
        )
        self.variants_single_prop_objects = to_streamed_response_wrapper(
            unions.variants_single_prop_objects,
        )


class AsyncUnionsResourceWithStreamingResponse:
    def __init__(self, unions: AsyncUnionsResource) -> None:
        self._unions = unions

        self.discriminated = async_to_streamed_response_wrapper(
            unions.discriminated,
        )
        self.variants_object_with_union_properties = async_to_streamed_response_wrapper(
            unions.variants_object_with_union_properties,
        )
        self.variants_single_prop_objects = async_to_streamed_response_wrapper(
            unions.variants_single_prop_objects,
        )
