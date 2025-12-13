# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ... import _legacy_response
from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ..._base_client import make_request_options
from ...types.types.object_mixed_known_and_unknown_response import ObjectMixedKnownAndUnknownResponse
from ...types.types.object_multiple_properties_same_ref_response import ObjectMultiplePropertiesSameRefResponse
from ...types.types.object_multiple_properties_same_model_response import ObjectMultiplePropertiesSameModelResponse
from ...types.types.object_multiple_array_properties_same_ref_response import (
    ObjectMultipleArrayPropertiesSameRefResponse,
)
from ...types.types.object_two_dimensional_array_primitive_property_response import (
    ObjectTwoDimensionalArrayPrimitivePropertyResponse,
)

__all__ = ["ObjectsResource", "AsyncObjectsResource"]


class ObjectsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ObjectsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return ObjectsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ObjectsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return ObjectsResourceWithStreamingResponse(self)

    def mixed_known_and_unknown(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ObjectMixedKnownAndUnknownResponse:
        """
        Endpoint with a response schema object that contains a mix of known & unknown
        properties with the same value types.
        """
        return self._get(
            "/types/object/mixed_known_and_unknown",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectMixedKnownAndUnknownResponse,
        )

    def multiple_array_properties_same_ref(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ObjectMultipleArrayPropertiesSameRefResponse:
        """
        Endpoint with a response schema object that contains multiple properties that
        reference the same $ref in array items that is _not_ a model in the config.
        Three child types should be generated, one for each property.
        """
        return self._get(
            "/types/object/multiple_array_properties_same_ref",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectMultipleArrayPropertiesSameRefResponse,
        )

    def multiple_properties_same_model(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ObjectMultiplePropertiesSameModelResponse:
        """
        Endpoint with a response schema object that contains multiple properties that
        reference the same model.
        """
        return self._get(
            "/types/object/multiple_properties_same_model",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectMultiplePropertiesSameModelResponse,
        )

    def multiple_properties_same_ref(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ObjectMultiplePropertiesSameRefResponse:
        """
        Endpoint with a response schema object that contains multiple properties that
        reference the same $ref that is _not_ a model in the config. Three child types
        should be generated. One for each property.
        """
        return self._get(
            "/types/object/multiple_properties_same_ref",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectMultiplePropertiesSameRefResponse,
        )

    def two_dimensional_array_primitive_property(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ObjectTwoDimensionalArrayPrimitivePropertyResponse:
        """
        Endpoint with a response schema object that contains properties that are
        primitive 2d arrays
        """
        return self._get(
            "/types/object/2d_array_primitive_properties",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectTwoDimensionalArrayPrimitivePropertyResponse,
        )

    def unknown_object(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """Endpoint with a response schema object that does not define any properties"""
        return self._get(
            "/types/object/unknown_object",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncObjectsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncObjectsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncObjectsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncObjectsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncObjectsResourceWithStreamingResponse(self)

    async def mixed_known_and_unknown(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ObjectMixedKnownAndUnknownResponse:
        """
        Endpoint with a response schema object that contains a mix of known & unknown
        properties with the same value types.
        """
        return await self._get(
            "/types/object/mixed_known_and_unknown",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectMixedKnownAndUnknownResponse,
        )

    async def multiple_array_properties_same_ref(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ObjectMultipleArrayPropertiesSameRefResponse:
        """
        Endpoint with a response schema object that contains multiple properties that
        reference the same $ref in array items that is _not_ a model in the config.
        Three child types should be generated, one for each property.
        """
        return await self._get(
            "/types/object/multiple_array_properties_same_ref",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectMultipleArrayPropertiesSameRefResponse,
        )

    async def multiple_properties_same_model(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ObjectMultiplePropertiesSameModelResponse:
        """
        Endpoint with a response schema object that contains multiple properties that
        reference the same model.
        """
        return await self._get(
            "/types/object/multiple_properties_same_model",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectMultiplePropertiesSameModelResponse,
        )

    async def multiple_properties_same_ref(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ObjectMultiplePropertiesSameRefResponse:
        """
        Endpoint with a response schema object that contains multiple properties that
        reference the same $ref that is _not_ a model in the config. Three child types
        should be generated. One for each property.
        """
        return await self._get(
            "/types/object/multiple_properties_same_ref",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectMultiplePropertiesSameRefResponse,
        )

    async def two_dimensional_array_primitive_property(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ObjectTwoDimensionalArrayPrimitivePropertyResponse:
        """
        Endpoint with a response schema object that contains properties that are
        primitive 2d arrays
        """
        return await self._get(
            "/types/object/2d_array_primitive_properties",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectTwoDimensionalArrayPrimitivePropertyResponse,
        )

    async def unknown_object(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """Endpoint with a response schema object that does not define any properties"""
        return await self._get(
            "/types/object/unknown_object",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class ObjectsResourceWithRawResponse:
    def __init__(self, objects: ObjectsResource) -> None:
        self._objects = objects

        self.mixed_known_and_unknown = _legacy_response.to_raw_response_wrapper(
            objects.mixed_known_and_unknown,
        )
        self.multiple_array_properties_same_ref = _legacy_response.to_raw_response_wrapper(
            objects.multiple_array_properties_same_ref,
        )
        self.multiple_properties_same_model = _legacy_response.to_raw_response_wrapper(
            objects.multiple_properties_same_model,
        )
        self.multiple_properties_same_ref = _legacy_response.to_raw_response_wrapper(
            objects.multiple_properties_same_ref,
        )
        self.two_dimensional_array_primitive_property = _legacy_response.to_raw_response_wrapper(
            objects.two_dimensional_array_primitive_property,
        )
        self.unknown_object = _legacy_response.to_raw_response_wrapper(
            objects.unknown_object,
        )


class AsyncObjectsResourceWithRawResponse:
    def __init__(self, objects: AsyncObjectsResource) -> None:
        self._objects = objects

        self.mixed_known_and_unknown = _legacy_response.async_to_raw_response_wrapper(
            objects.mixed_known_and_unknown,
        )
        self.multiple_array_properties_same_ref = _legacy_response.async_to_raw_response_wrapper(
            objects.multiple_array_properties_same_ref,
        )
        self.multiple_properties_same_model = _legacy_response.async_to_raw_response_wrapper(
            objects.multiple_properties_same_model,
        )
        self.multiple_properties_same_ref = _legacy_response.async_to_raw_response_wrapper(
            objects.multiple_properties_same_ref,
        )
        self.two_dimensional_array_primitive_property = _legacy_response.async_to_raw_response_wrapper(
            objects.two_dimensional_array_primitive_property,
        )
        self.unknown_object = _legacy_response.async_to_raw_response_wrapper(
            objects.unknown_object,
        )


class ObjectsResourceWithStreamingResponse:
    def __init__(self, objects: ObjectsResource) -> None:
        self._objects = objects

        self.mixed_known_and_unknown = to_streamed_response_wrapper(
            objects.mixed_known_and_unknown,
        )
        self.multiple_array_properties_same_ref = to_streamed_response_wrapper(
            objects.multiple_array_properties_same_ref,
        )
        self.multiple_properties_same_model = to_streamed_response_wrapper(
            objects.multiple_properties_same_model,
        )
        self.multiple_properties_same_ref = to_streamed_response_wrapper(
            objects.multiple_properties_same_ref,
        )
        self.two_dimensional_array_primitive_property = to_streamed_response_wrapper(
            objects.two_dimensional_array_primitive_property,
        )
        self.unknown_object = to_streamed_response_wrapper(
            objects.unknown_object,
        )


class AsyncObjectsResourceWithStreamingResponse:
    def __init__(self, objects: AsyncObjectsResource) -> None:
        self._objects = objects

        self.mixed_known_and_unknown = async_to_streamed_response_wrapper(
            objects.mixed_known_and_unknown,
        )
        self.multiple_array_properties_same_ref = async_to_streamed_response_wrapper(
            objects.multiple_array_properties_same_ref,
        )
        self.multiple_properties_same_model = async_to_streamed_response_wrapper(
            objects.multiple_properties_same_model,
        )
        self.multiple_properties_same_ref = async_to_streamed_response_wrapper(
            objects.multiple_properties_same_ref,
        )
        self.two_dimensional_array_primitive_property = async_to_streamed_response_wrapper(
            objects.two_dimensional_array_primitive_property,
        )
        self.unknown_object = async_to_streamed_response_wrapper(
            objects.unknown_object,
        )
