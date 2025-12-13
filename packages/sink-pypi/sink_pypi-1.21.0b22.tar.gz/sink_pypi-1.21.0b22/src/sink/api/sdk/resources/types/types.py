# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import date, datetime

import httpx

from ... import _legacy_response
from .maps import (
    MapsResource,
    AsyncMapsResource,
    MapsResourceWithRawResponse,
    AsyncMapsResourceWithRawResponse,
    MapsResourceWithStreamingResponse,
    AsyncMapsResourceWithStreamingResponse,
)
from .enums import (
    EnumsResource,
    AsyncEnumsResource,
    EnumsResourceWithRawResponse,
    AsyncEnumsResourceWithRawResponse,
    EnumsResourceWithStreamingResponse,
    AsyncEnumsResourceWithStreamingResponse,
)
from .arrays import (
    ArraysResource,
    AsyncArraysResource,
    ArraysResourceWithRawResponse,
    AsyncArraysResourceWithRawResponse,
    ArraysResourceWithStreamingResponse,
    AsyncArraysResourceWithStreamingResponse,
)
from .unions import (
    UnionsResource,
    AsyncUnionsResource,
    UnionsResourceWithRawResponse,
    AsyncUnionsResourceWithRawResponse,
    UnionsResourceWithStreamingResponse,
    AsyncUnionsResourceWithStreamingResponse,
)
from ...types import type_dates_params, type_datetimes_params
from .objects import (
    ObjectsResource,
    AsyncObjectsResource,
    ObjectsResourceWithRawResponse,
    AsyncObjectsResourceWithRawResponse,
    ObjectsResourceWithStreamingResponse,
    AsyncObjectsResourceWithStreamingResponse,
)
from ..._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from .primitives import (
    PrimitivesResource,
    AsyncPrimitivesResource,
    PrimitivesResourceWithRawResponse,
    AsyncPrimitivesResourceWithRawResponse,
    PrimitivesResourceWithStreamingResponse,
    AsyncPrimitivesResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ..._base_client import make_request_options
from .read_only_params import (
    ReadOnlyParamsResource,
    AsyncReadOnlyParamsResource,
    ReadOnlyParamsResourceWithRawResponse,
    AsyncReadOnlyParamsResourceWithRawResponse,
    ReadOnlyParamsResourceWithStreamingResponse,
    AsyncReadOnlyParamsResourceWithStreamingResponse,
)
from .write_only_responses import (
    WriteOnlyResponsesResource,
    AsyncWriteOnlyResponsesResource,
    WriteOnlyResponsesResourceWithRawResponse,
    AsyncWriteOnlyResponsesResourceWithRawResponse,
    WriteOnlyResponsesResourceWithStreamingResponse,
    AsyncWriteOnlyResponsesResourceWithStreamingResponse,
)
from ...types.type_dates_response import TypeDatesResponse
from ...types.type_datetimes_response import TypeDatetimesResponse

__all__ = ["TypesResource", "AsyncTypesResource"]


class TypesResource(SyncAPIResource):
    @cached_property
    def primitives(self) -> PrimitivesResource:
        return PrimitivesResource(self._client)

    @cached_property
    def read_only_params(self) -> ReadOnlyParamsResource:
        return ReadOnlyParamsResource(self._client)

    @cached_property
    def write_only_responses(self) -> WriteOnlyResponsesResource:
        return WriteOnlyResponsesResource(self._client)

    @cached_property
    def maps(self) -> MapsResource:
        return MapsResource(self._client)

    @cached_property
    def enums(self) -> EnumsResource:
        return EnumsResource(self._client)

    @cached_property
    def unions(self) -> UnionsResource:
        return UnionsResource(self._client)

    @cached_property
    def objects(self) -> ObjectsResource:
        return ObjectsResource(self._client)

    @cached_property
    def arrays(self) -> ArraysResource:
        return ArraysResource(self._client)

    @cached_property
    def with_raw_response(self) -> TypesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return TypesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TypesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return TypesResourceWithStreamingResponse(self)

    def dates(
        self,
        *,
        required_date: Union[str, date],
        required_nullable_date: Union[str, date, None],
        list_date: SequenceNotStr[Union[str, date]] | Omit = omit,
        oneof_date: Union[Union[str, date], int] | Omit = omit,
        optional_date: Union[str, date] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> TypeDatesResponse:
        """
        Endpoint that has date types should generate params/responses with rich date
        types.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/types/dates",
            body=maybe_transform(
                {
                    "required_date": required_date,
                    "required_nullable_date": required_nullable_date,
                    "list_date": list_date,
                    "oneof_date": oneof_date,
                    "optional_date": optional_date,
                },
                type_dates_params.TypeDatesParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=TypeDatesResponse,
        )

    def datetimes(
        self,
        *,
        required_datetime: Union[str, datetime],
        required_nullable_datetime: Union[str, datetime, None],
        list_datetime: SequenceNotStr[Union[str, datetime]] | Omit = omit,
        oneof_datetime: Union[Union[str, datetime], int] | Omit = omit,
        optional_datetime: Union[str, datetime] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> TypeDatetimesResponse:
        """
        Endpoint that has date-time types.

        Args:
          oneof_datetime: union type coming from the `oneof_datetime` property

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/types/datetimes",
            body=maybe_transform(
                {
                    "required_datetime": required_datetime,
                    "required_nullable_datetime": required_nullable_datetime,
                    "list_datetime": list_datetime,
                    "oneof_datetime": oneof_datetime,
                    "optional_datetime": optional_datetime,
                },
                type_datetimes_params.TypeDatetimesParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=TypeDatetimesResponse,
        )


class AsyncTypesResource(AsyncAPIResource):
    @cached_property
    def primitives(self) -> AsyncPrimitivesResource:
        return AsyncPrimitivesResource(self._client)

    @cached_property
    def read_only_params(self) -> AsyncReadOnlyParamsResource:
        return AsyncReadOnlyParamsResource(self._client)

    @cached_property
    def write_only_responses(self) -> AsyncWriteOnlyResponsesResource:
        return AsyncWriteOnlyResponsesResource(self._client)

    @cached_property
    def maps(self) -> AsyncMapsResource:
        return AsyncMapsResource(self._client)

    @cached_property
    def enums(self) -> AsyncEnumsResource:
        return AsyncEnumsResource(self._client)

    @cached_property
    def unions(self) -> AsyncUnionsResource:
        return AsyncUnionsResource(self._client)

    @cached_property
    def objects(self) -> AsyncObjectsResource:
        return AsyncObjectsResource(self._client)

    @cached_property
    def arrays(self) -> AsyncArraysResource:
        return AsyncArraysResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncTypesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncTypesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTypesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncTypesResourceWithStreamingResponse(self)

    async def dates(
        self,
        *,
        required_date: Union[str, date],
        required_nullable_date: Union[str, date, None],
        list_date: SequenceNotStr[Union[str, date]] | Omit = omit,
        oneof_date: Union[Union[str, date], int] | Omit = omit,
        optional_date: Union[str, date] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> TypeDatesResponse:
        """
        Endpoint that has date types should generate params/responses with rich date
        types.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/types/dates",
            body=await async_maybe_transform(
                {
                    "required_date": required_date,
                    "required_nullable_date": required_nullable_date,
                    "list_date": list_date,
                    "oneof_date": oneof_date,
                    "optional_date": optional_date,
                },
                type_dates_params.TypeDatesParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=TypeDatesResponse,
        )

    async def datetimes(
        self,
        *,
        required_datetime: Union[str, datetime],
        required_nullable_datetime: Union[str, datetime, None],
        list_datetime: SequenceNotStr[Union[str, datetime]] | Omit = omit,
        oneof_datetime: Union[Union[str, datetime], int] | Omit = omit,
        optional_datetime: Union[str, datetime] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> TypeDatetimesResponse:
        """
        Endpoint that has date-time types.

        Args:
          oneof_datetime: union type coming from the `oneof_datetime` property

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/types/datetimes",
            body=await async_maybe_transform(
                {
                    "required_datetime": required_datetime,
                    "required_nullable_datetime": required_nullable_datetime,
                    "list_datetime": list_datetime,
                    "oneof_datetime": oneof_datetime,
                    "optional_datetime": optional_datetime,
                },
                type_datetimes_params.TypeDatetimesParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=TypeDatetimesResponse,
        )


class TypesResourceWithRawResponse:
    def __init__(self, types: TypesResource) -> None:
        self._types = types

        self.dates = _legacy_response.to_raw_response_wrapper(
            types.dates,
        )
        self.datetimes = _legacy_response.to_raw_response_wrapper(
            types.datetimes,
        )

    @cached_property
    def primitives(self) -> PrimitivesResourceWithRawResponse:
        return PrimitivesResourceWithRawResponse(self._types.primitives)

    @cached_property
    def read_only_params(self) -> ReadOnlyParamsResourceWithRawResponse:
        return ReadOnlyParamsResourceWithRawResponse(self._types.read_only_params)

    @cached_property
    def write_only_responses(self) -> WriteOnlyResponsesResourceWithRawResponse:
        return WriteOnlyResponsesResourceWithRawResponse(self._types.write_only_responses)

    @cached_property
    def maps(self) -> MapsResourceWithRawResponse:
        return MapsResourceWithRawResponse(self._types.maps)

    @cached_property
    def enums(self) -> EnumsResourceWithRawResponse:
        return EnumsResourceWithRawResponse(self._types.enums)

    @cached_property
    def unions(self) -> UnionsResourceWithRawResponse:
        return UnionsResourceWithRawResponse(self._types.unions)

    @cached_property
    def objects(self) -> ObjectsResourceWithRawResponse:
        return ObjectsResourceWithRawResponse(self._types.objects)

    @cached_property
    def arrays(self) -> ArraysResourceWithRawResponse:
        return ArraysResourceWithRawResponse(self._types.arrays)


class AsyncTypesResourceWithRawResponse:
    def __init__(self, types: AsyncTypesResource) -> None:
        self._types = types

        self.dates = _legacy_response.async_to_raw_response_wrapper(
            types.dates,
        )
        self.datetimes = _legacy_response.async_to_raw_response_wrapper(
            types.datetimes,
        )

    @cached_property
    def primitives(self) -> AsyncPrimitivesResourceWithRawResponse:
        return AsyncPrimitivesResourceWithRawResponse(self._types.primitives)

    @cached_property
    def read_only_params(self) -> AsyncReadOnlyParamsResourceWithRawResponse:
        return AsyncReadOnlyParamsResourceWithRawResponse(self._types.read_only_params)

    @cached_property
    def write_only_responses(self) -> AsyncWriteOnlyResponsesResourceWithRawResponse:
        return AsyncWriteOnlyResponsesResourceWithRawResponse(self._types.write_only_responses)

    @cached_property
    def maps(self) -> AsyncMapsResourceWithRawResponse:
        return AsyncMapsResourceWithRawResponse(self._types.maps)

    @cached_property
    def enums(self) -> AsyncEnumsResourceWithRawResponse:
        return AsyncEnumsResourceWithRawResponse(self._types.enums)

    @cached_property
    def unions(self) -> AsyncUnionsResourceWithRawResponse:
        return AsyncUnionsResourceWithRawResponse(self._types.unions)

    @cached_property
    def objects(self) -> AsyncObjectsResourceWithRawResponse:
        return AsyncObjectsResourceWithRawResponse(self._types.objects)

    @cached_property
    def arrays(self) -> AsyncArraysResourceWithRawResponse:
        return AsyncArraysResourceWithRawResponse(self._types.arrays)


class TypesResourceWithStreamingResponse:
    def __init__(self, types: TypesResource) -> None:
        self._types = types

        self.dates = to_streamed_response_wrapper(
            types.dates,
        )
        self.datetimes = to_streamed_response_wrapper(
            types.datetimes,
        )

    @cached_property
    def primitives(self) -> PrimitivesResourceWithStreamingResponse:
        return PrimitivesResourceWithStreamingResponse(self._types.primitives)

    @cached_property
    def read_only_params(self) -> ReadOnlyParamsResourceWithStreamingResponse:
        return ReadOnlyParamsResourceWithStreamingResponse(self._types.read_only_params)

    @cached_property
    def write_only_responses(self) -> WriteOnlyResponsesResourceWithStreamingResponse:
        return WriteOnlyResponsesResourceWithStreamingResponse(self._types.write_only_responses)

    @cached_property
    def maps(self) -> MapsResourceWithStreamingResponse:
        return MapsResourceWithStreamingResponse(self._types.maps)

    @cached_property
    def enums(self) -> EnumsResourceWithStreamingResponse:
        return EnumsResourceWithStreamingResponse(self._types.enums)

    @cached_property
    def unions(self) -> UnionsResourceWithStreamingResponse:
        return UnionsResourceWithStreamingResponse(self._types.unions)

    @cached_property
    def objects(self) -> ObjectsResourceWithStreamingResponse:
        return ObjectsResourceWithStreamingResponse(self._types.objects)

    @cached_property
    def arrays(self) -> ArraysResourceWithStreamingResponse:
        return ArraysResourceWithStreamingResponse(self._types.arrays)


class AsyncTypesResourceWithStreamingResponse:
    def __init__(self, types: AsyncTypesResource) -> None:
        self._types = types

        self.dates = async_to_streamed_response_wrapper(
            types.dates,
        )
        self.datetimes = async_to_streamed_response_wrapper(
            types.datetimes,
        )

    @cached_property
    def primitives(self) -> AsyncPrimitivesResourceWithStreamingResponse:
        return AsyncPrimitivesResourceWithStreamingResponse(self._types.primitives)

    @cached_property
    def read_only_params(self) -> AsyncReadOnlyParamsResourceWithStreamingResponse:
        return AsyncReadOnlyParamsResourceWithStreamingResponse(self._types.read_only_params)

    @cached_property
    def write_only_responses(self) -> AsyncWriteOnlyResponsesResourceWithStreamingResponse:
        return AsyncWriteOnlyResponsesResourceWithStreamingResponse(self._types.write_only_responses)

    @cached_property
    def maps(self) -> AsyncMapsResourceWithStreamingResponse:
        return AsyncMapsResourceWithStreamingResponse(self._types.maps)

    @cached_property
    def enums(self) -> AsyncEnumsResourceWithStreamingResponse:
        return AsyncEnumsResourceWithStreamingResponse(self._types.enums)

    @cached_property
    def unions(self) -> AsyncUnionsResourceWithStreamingResponse:
        return AsyncUnionsResourceWithStreamingResponse(self._types.unions)

    @cached_property
    def objects(self) -> AsyncObjectsResourceWithStreamingResponse:
        return AsyncObjectsResourceWithStreamingResponse(self._types.objects)

    @cached_property
    def arrays(self) -> AsyncArraysResourceWithStreamingResponse:
        return AsyncArraysResourceWithStreamingResponse(self._types.arrays)
