# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Iterable, cast
from typing_extensions import Literal, overload

import httpx

from ... import _legacy_response
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import required_args, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ...types.types import (
    union_param_discriminated_by_property_name_params,
    union_param_discriminated_with_basic_mapping_params,
    union_array_param_discriminated_by_property_name_params,
    union_array_param_discriminated_with_basic_mapping_params,
)
from ..._base_client import make_request_options
from ...types.types.union_response_discriminated_by_property_name_response import (
    UnionResponseDiscriminatedByPropertyNameResponse,
)
from ...types.types.union_response_discriminated_with_basic_mapping_response import (
    UnionResponseDiscriminatedWithBasicMappingResponse,
)

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

    def array_param_discriminated_by_property_name(
        self,
        *,
        body: Iterable[union_array_param_discriminated_by_property_name_params.Body],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> str:
        """
        Endpoint with an array request param schema with items discriminated union that
        just defines the `propertyName` config

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/types/unions/array_param_discriminated_by_property_name",
            body=maybe_transform(body, Iterable[union_array_param_discriminated_by_property_name_params.Body]),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=str,
        )

    def array_param_discriminated_with_basic_mapping(
        self,
        *,
        body: Iterable[union_array_param_discriminated_with_basic_mapping_params.Body],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> str:
        """
        Endpoint with an array request param schema with items discriminated union that
        also defines the `mapping` config

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/types/unions/array_param_discriminated_with_basic_mapping",
            body=maybe_transform(body, Iterable[union_array_param_discriminated_with_basic_mapping_params.Body]),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=str,
        )

    @overload
    def param_discriminated_by_property_name(
        self,
        *,
        value: str,
        type: Literal["a"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> str:
        """
        Endpoint with a request param schema that is a discriminated union that just
        defines the `propertyName` config

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    def param_discriminated_by_property_name(
        self,
        *,
        value: str,
        type: Literal["b"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> str:
        """
        Endpoint with a request param schema that is a discriminated union that just
        defines the `propertyName` config

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["value"])
    def param_discriminated_by_property_name(
        self,
        *,
        value: str,
        type: Literal["a"] | Literal["b"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> str:
        return self._post(
            "/types/unions/param_discriminated_by_property_name",
            body=maybe_transform(
                {
                    "value": value,
                    "type": type,
                },
                union_param_discriminated_by_property_name_params.UnionParamDiscriminatedByPropertyNameParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=str,
        )

    @overload
    def param_discriminated_with_basic_mapping(
        self,
        *,
        value: str,
        type: Literal["a"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> str:
        """
        Endpoint with a request param schema that is a discriminated union that also
        defines the `mapping` config

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    def param_discriminated_with_basic_mapping(
        self,
        *,
        value: str,
        type: Literal["b"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> str:
        """
        Endpoint with a request param schema that is a discriminated union that also
        defines the `mapping` config

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["value"])
    def param_discriminated_with_basic_mapping(
        self,
        *,
        value: str,
        type: Literal["a"] | Literal["b"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> str:
        return self._post(
            "/types/unions/param_discriminated_with_basic_mapping",
            body=maybe_transform(
                {
                    "value": value,
                    "type": type,
                },
                union_param_discriminated_with_basic_mapping_params.UnionParamDiscriminatedWithBasicMappingParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=str,
        )

    def response_discriminated_by_property_name(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> UnionResponseDiscriminatedByPropertyNameResponse:
        """
        Endpoint with a response schema that is a discriminated union that just defines
        the `propertyName` config
        """
        return cast(
            UnionResponseDiscriminatedByPropertyNameResponse,
            self._get(
                "/types/unions/response_discriminated_by_property_name",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, UnionResponseDiscriminatedByPropertyNameResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def response_discriminated_with_basic_mapping(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> UnionResponseDiscriminatedWithBasicMappingResponse:
        """
        Endpoint with a response schema that is a discriminated union that also defines
        the `mapping` config
        """
        return cast(
            UnionResponseDiscriminatedWithBasicMappingResponse,
            self._get(
                "/types/unions/response_discriminated_with_basic_mapping",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, UnionResponseDiscriminatedWithBasicMappingResponse
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

    async def array_param_discriminated_by_property_name(
        self,
        *,
        body: Iterable[union_array_param_discriminated_by_property_name_params.Body],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> str:
        """
        Endpoint with an array request param schema with items discriminated union that
        just defines the `propertyName` config

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/types/unions/array_param_discriminated_by_property_name",
            body=await async_maybe_transform(
                body, Iterable[union_array_param_discriminated_by_property_name_params.Body]
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=str,
        )

    async def array_param_discriminated_with_basic_mapping(
        self,
        *,
        body: Iterable[union_array_param_discriminated_with_basic_mapping_params.Body],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> str:
        """
        Endpoint with an array request param schema with items discriminated union that
        also defines the `mapping` config

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/types/unions/array_param_discriminated_with_basic_mapping",
            body=await async_maybe_transform(
                body, Iterable[union_array_param_discriminated_with_basic_mapping_params.Body]
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=str,
        )

    @overload
    async def param_discriminated_by_property_name(
        self,
        *,
        value: str,
        type: Literal["a"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> str:
        """
        Endpoint with a request param schema that is a discriminated union that just
        defines the `propertyName` config

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    async def param_discriminated_by_property_name(
        self,
        *,
        value: str,
        type: Literal["b"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> str:
        """
        Endpoint with a request param schema that is a discriminated union that just
        defines the `propertyName` config

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["value"])
    async def param_discriminated_by_property_name(
        self,
        *,
        value: str,
        type: Literal["a"] | Literal["b"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> str:
        return await self._post(
            "/types/unions/param_discriminated_by_property_name",
            body=await async_maybe_transform(
                {
                    "value": value,
                    "type": type,
                },
                union_param_discriminated_by_property_name_params.UnionParamDiscriminatedByPropertyNameParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=str,
        )

    @overload
    async def param_discriminated_with_basic_mapping(
        self,
        *,
        value: str,
        type: Literal["a"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> str:
        """
        Endpoint with a request param schema that is a discriminated union that also
        defines the `mapping` config

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    async def param_discriminated_with_basic_mapping(
        self,
        *,
        value: str,
        type: Literal["b"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> str:
        """
        Endpoint with a request param schema that is a discriminated union that also
        defines the `mapping` config

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["value"])
    async def param_discriminated_with_basic_mapping(
        self,
        *,
        value: str,
        type: Literal["a"] | Literal["b"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> str:
        return await self._post(
            "/types/unions/param_discriminated_with_basic_mapping",
            body=await async_maybe_transform(
                {
                    "value": value,
                    "type": type,
                },
                union_param_discriminated_with_basic_mapping_params.UnionParamDiscriminatedWithBasicMappingParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=str,
        )

    async def response_discriminated_by_property_name(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> UnionResponseDiscriminatedByPropertyNameResponse:
        """
        Endpoint with a response schema that is a discriminated union that just defines
        the `propertyName` config
        """
        return cast(
            UnionResponseDiscriminatedByPropertyNameResponse,
            await self._get(
                "/types/unions/response_discriminated_by_property_name",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, UnionResponseDiscriminatedByPropertyNameResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def response_discriminated_with_basic_mapping(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> UnionResponseDiscriminatedWithBasicMappingResponse:
        """
        Endpoint with a response schema that is a discriminated union that also defines
        the `mapping` config
        """
        return cast(
            UnionResponseDiscriminatedWithBasicMappingResponse,
            await self._get(
                "/types/unions/response_discriminated_with_basic_mapping",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, UnionResponseDiscriminatedWithBasicMappingResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class UnionsResourceWithRawResponse:
    def __init__(self, unions: UnionsResource) -> None:
        self._unions = unions

        self.array_param_discriminated_by_property_name = _legacy_response.to_raw_response_wrapper(
            unions.array_param_discriminated_by_property_name,
        )
        self.array_param_discriminated_with_basic_mapping = _legacy_response.to_raw_response_wrapper(
            unions.array_param_discriminated_with_basic_mapping,
        )
        self.param_discriminated_by_property_name = _legacy_response.to_raw_response_wrapper(
            unions.param_discriminated_by_property_name,
        )
        self.param_discriminated_with_basic_mapping = _legacy_response.to_raw_response_wrapper(
            unions.param_discriminated_with_basic_mapping,
        )
        self.response_discriminated_by_property_name = _legacy_response.to_raw_response_wrapper(
            unions.response_discriminated_by_property_name,
        )
        self.response_discriminated_with_basic_mapping = _legacy_response.to_raw_response_wrapper(
            unions.response_discriminated_with_basic_mapping,
        )


class AsyncUnionsResourceWithRawResponse:
    def __init__(self, unions: AsyncUnionsResource) -> None:
        self._unions = unions

        self.array_param_discriminated_by_property_name = _legacy_response.async_to_raw_response_wrapper(
            unions.array_param_discriminated_by_property_name,
        )
        self.array_param_discriminated_with_basic_mapping = _legacy_response.async_to_raw_response_wrapper(
            unions.array_param_discriminated_with_basic_mapping,
        )
        self.param_discriminated_by_property_name = _legacy_response.async_to_raw_response_wrapper(
            unions.param_discriminated_by_property_name,
        )
        self.param_discriminated_with_basic_mapping = _legacy_response.async_to_raw_response_wrapper(
            unions.param_discriminated_with_basic_mapping,
        )
        self.response_discriminated_by_property_name = _legacy_response.async_to_raw_response_wrapper(
            unions.response_discriminated_by_property_name,
        )
        self.response_discriminated_with_basic_mapping = _legacy_response.async_to_raw_response_wrapper(
            unions.response_discriminated_with_basic_mapping,
        )


class UnionsResourceWithStreamingResponse:
    def __init__(self, unions: UnionsResource) -> None:
        self._unions = unions

        self.array_param_discriminated_by_property_name = to_streamed_response_wrapper(
            unions.array_param_discriminated_by_property_name,
        )
        self.array_param_discriminated_with_basic_mapping = to_streamed_response_wrapper(
            unions.array_param_discriminated_with_basic_mapping,
        )
        self.param_discriminated_by_property_name = to_streamed_response_wrapper(
            unions.param_discriminated_by_property_name,
        )
        self.param_discriminated_with_basic_mapping = to_streamed_response_wrapper(
            unions.param_discriminated_with_basic_mapping,
        )
        self.response_discriminated_by_property_name = to_streamed_response_wrapper(
            unions.response_discriminated_by_property_name,
        )
        self.response_discriminated_with_basic_mapping = to_streamed_response_wrapper(
            unions.response_discriminated_with_basic_mapping,
        )


class AsyncUnionsResourceWithStreamingResponse:
    def __init__(self, unions: AsyncUnionsResource) -> None:
        self._unions = unions

        self.array_param_discriminated_by_property_name = async_to_streamed_response_wrapper(
            unions.array_param_discriminated_by_property_name,
        )
        self.array_param_discriminated_with_basic_mapping = async_to_streamed_response_wrapper(
            unions.array_param_discriminated_with_basic_mapping,
        )
        self.param_discriminated_by_property_name = async_to_streamed_response_wrapper(
            unions.param_discriminated_by_property_name,
        )
        self.param_discriminated_with_basic_mapping = async_to_streamed_response_wrapper(
            unions.param_discriminated_with_basic_mapping,
        )
        self.response_discriminated_by_property_name = async_to_streamed_response_wrapper(
            unions.response_discriminated_by_property_name,
        )
        self.response_discriminated_with_basic_mapping = async_to_streamed_response_wrapper(
            unions.response_discriminated_with_basic_mapping,
        )
