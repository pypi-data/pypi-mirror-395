# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Optional, cast

import httpx

from ... import _legacy_response
from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ..._base_client import make_request_options
from ...types.responses.union_type_numbers_response import UnionTypeNumbersResponse
from ...types.responses.union_type_objects_response import UnionTypeObjectsResponse
from ...types.responses.union_type_mixed_types_response import UnionTypeMixedTypesResponse
from ...types.responses.union_type_nullable_union_response import UnionTypeNullableUnionResponse
from ...types.responses.union_type_unknown_variant_response import UnionTypeUnknownVariantResponse
from ...types.responses.union_type_super_mixed_types_response import UnionTypeSuperMixedTypesResponse

__all__ = ["UnionTypesResource", "AsyncUnionTypesResource"]


class UnionTypesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> UnionTypesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return UnionTypesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UnionTypesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return UnionTypesResourceWithStreamingResponse(self)

    def mixed_types(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> UnionTypeMixedTypesResponse:
        """Endpoint with a top level union response of different types."""
        return cast(
            UnionTypeMixedTypesResponse,
            self._post(
                "/responses/unions/mixed_types",
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    idempotency_key=idempotency_key,
                ),
                cast_to=cast(
                    Any, UnionTypeMixedTypesResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def nullable_union(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Optional[UnionTypeNullableUnionResponse]:
        """Endpoint with a top level union response of floats and integers."""
        return cast(
            Optional[UnionTypeNullableUnionResponse],
            self._post(
                "/responses/unions/nullable",
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    idempotency_key=idempotency_key,
                ),
                cast_to=cast(
                    Any, UnionTypeNullableUnionResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def numbers(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> UnionTypeNumbersResponse:
        """Endpoint with a top level union response of floats and integers."""
        return self._post(
            "/responses/unions/numbers",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=float,
        )

    def objects(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> UnionTypeObjectsResponse:
        """Endpoint with a top level union response of just object variants."""
        return cast(
            UnionTypeObjectsResponse,
            self._post(
                "/responses/unions/objects",
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    idempotency_key=idempotency_key,
                ),
                cast_to=cast(
                    Any, UnionTypeObjectsResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def super_mixed_types(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> UnionTypeSuperMixedTypesResponse:
        """Endpoint with a top level union response of different types."""
        return cast(
            UnionTypeSuperMixedTypesResponse,
            self._post(
                "/responses/unions/super_mixed_types",
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    idempotency_key=idempotency_key,
                ),
                cast_to=cast(
                    Any, UnionTypeSuperMixedTypesResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def unknown_variant(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> UnionTypeUnknownVariantResponse:
        """Endpoint with a top level union response with a variant that is `type: unknown`"""
        return cast(
            UnionTypeUnknownVariantResponse,
            self._post(
                "/responses/unions/unknown_variant",
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    idempotency_key=idempotency_key,
                ),
                cast_to=cast(
                    Any, UnionTypeUnknownVariantResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class AsyncUnionTypesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncUnionTypesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncUnionTypesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUnionTypesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncUnionTypesResourceWithStreamingResponse(self)

    async def mixed_types(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> UnionTypeMixedTypesResponse:
        """Endpoint with a top level union response of different types."""
        return cast(
            UnionTypeMixedTypesResponse,
            await self._post(
                "/responses/unions/mixed_types",
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    idempotency_key=idempotency_key,
                ),
                cast_to=cast(
                    Any, UnionTypeMixedTypesResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def nullable_union(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Optional[UnionTypeNullableUnionResponse]:
        """Endpoint with a top level union response of floats and integers."""
        return cast(
            Optional[UnionTypeNullableUnionResponse],
            await self._post(
                "/responses/unions/nullable",
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    idempotency_key=idempotency_key,
                ),
                cast_to=cast(
                    Any, UnionTypeNullableUnionResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def numbers(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> UnionTypeNumbersResponse:
        """Endpoint with a top level union response of floats and integers."""
        return await self._post(
            "/responses/unions/numbers",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=float,
        )

    async def objects(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> UnionTypeObjectsResponse:
        """Endpoint with a top level union response of just object variants."""
        return cast(
            UnionTypeObjectsResponse,
            await self._post(
                "/responses/unions/objects",
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    idempotency_key=idempotency_key,
                ),
                cast_to=cast(
                    Any, UnionTypeObjectsResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def super_mixed_types(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> UnionTypeSuperMixedTypesResponse:
        """Endpoint with a top level union response of different types."""
        return cast(
            UnionTypeSuperMixedTypesResponse,
            await self._post(
                "/responses/unions/super_mixed_types",
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    idempotency_key=idempotency_key,
                ),
                cast_to=cast(
                    Any, UnionTypeSuperMixedTypesResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def unknown_variant(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> UnionTypeUnknownVariantResponse:
        """Endpoint with a top level union response with a variant that is `type: unknown`"""
        return cast(
            UnionTypeUnknownVariantResponse,
            await self._post(
                "/responses/unions/unknown_variant",
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    idempotency_key=idempotency_key,
                ),
                cast_to=cast(
                    Any, UnionTypeUnknownVariantResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class UnionTypesResourceWithRawResponse:
    def __init__(self, union_types: UnionTypesResource) -> None:
        self._union_types = union_types

        self.mixed_types = _legacy_response.to_raw_response_wrapper(
            union_types.mixed_types,
        )
        self.nullable_union = _legacy_response.to_raw_response_wrapper(
            union_types.nullable_union,
        )
        self.numbers = _legacy_response.to_raw_response_wrapper(
            union_types.numbers,
        )
        self.objects = _legacy_response.to_raw_response_wrapper(
            union_types.objects,
        )
        self.super_mixed_types = _legacy_response.to_raw_response_wrapper(
            union_types.super_mixed_types,
        )
        self.unknown_variant = _legacy_response.to_raw_response_wrapper(
            union_types.unknown_variant,
        )


class AsyncUnionTypesResourceWithRawResponse:
    def __init__(self, union_types: AsyncUnionTypesResource) -> None:
        self._union_types = union_types

        self.mixed_types = _legacy_response.async_to_raw_response_wrapper(
            union_types.mixed_types,
        )
        self.nullable_union = _legacy_response.async_to_raw_response_wrapper(
            union_types.nullable_union,
        )
        self.numbers = _legacy_response.async_to_raw_response_wrapper(
            union_types.numbers,
        )
        self.objects = _legacy_response.async_to_raw_response_wrapper(
            union_types.objects,
        )
        self.super_mixed_types = _legacy_response.async_to_raw_response_wrapper(
            union_types.super_mixed_types,
        )
        self.unknown_variant = _legacy_response.async_to_raw_response_wrapper(
            union_types.unknown_variant,
        )


class UnionTypesResourceWithStreamingResponse:
    def __init__(self, union_types: UnionTypesResource) -> None:
        self._union_types = union_types

        self.mixed_types = to_streamed_response_wrapper(
            union_types.mixed_types,
        )
        self.nullable_union = to_streamed_response_wrapper(
            union_types.nullable_union,
        )
        self.numbers = to_streamed_response_wrapper(
            union_types.numbers,
        )
        self.objects = to_streamed_response_wrapper(
            union_types.objects,
        )
        self.super_mixed_types = to_streamed_response_wrapper(
            union_types.super_mixed_types,
        )
        self.unknown_variant = to_streamed_response_wrapper(
            union_types.unknown_variant,
        )


class AsyncUnionTypesResourceWithStreamingResponse:
    def __init__(self, union_types: AsyncUnionTypesResource) -> None:
        self._union_types = union_types

        self.mixed_types = async_to_streamed_response_wrapper(
            union_types.mixed_types,
        )
        self.nullable_union = async_to_streamed_response_wrapper(
            union_types.nullable_union,
        )
        self.numbers = async_to_streamed_response_wrapper(
            union_types.numbers,
        )
        self.objects = async_to_streamed_response_wrapper(
            union_types.objects,
        )
        self.super_mixed_types = async_to_streamed_response_wrapper(
            union_types.super_mixed_types,
        )
        self.unknown_variant = async_to_streamed_response_wrapper(
            union_types.unknown_variant,
        )
