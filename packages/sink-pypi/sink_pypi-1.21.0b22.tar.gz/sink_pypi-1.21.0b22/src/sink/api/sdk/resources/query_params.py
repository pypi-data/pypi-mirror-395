# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from typing_extensions import Literal

import httpx

from .. import _legacy_response
from ..types import (
    query_param_enum_params,
    query_param_array_params,
    query_param_all_of_params,
    query_param_any_of_params,
    query_param_object_params,
    query_param_one_of_params,
    query_param_primitives_params,
    query_param_any_of_string_or_array_params,
)
from .._types import Body, Omit, Query, Headers, NoneType, NotGiven, SequenceNotStr, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from .._base_client import make_request_options

__all__ = ["QueryParamsResource", "AsyncQueryParamsResource"]


class QueryParamsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> QueryParamsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return QueryParamsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> QueryParamsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return QueryParamsResourceWithStreamingResponse(self)

    def all_of(
        self,
        *,
        foo_and_bar: query_param_all_of_params.FooAndBar | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Endpoint with allOf query params

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/query_params/allOf",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"foo_and_bar": foo_and_bar}, query_param_all_of_params.QueryParamAllOfParams),
            ),
            cast_to=NoneType,
        )

    def any_of(
        self,
        *,
        string_or_integer: Union[str, int] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Endpoint with anyOf query params

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/query_params/anyOf",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"string_or_integer": string_or_integer}, query_param_any_of_params.QueryParamAnyOfParams
                ),
            ),
            cast_to=NoneType,
        )

    def any_of_string_or_array(
        self,
        *,
        ids: Union[str, SequenceNotStr[str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Endpoint with anyOf query param that's string or array of strings

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/query_params/anyOfStringOrArray",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"ids": ids}, query_param_any_of_string_or_array_params.QueryParamAnyOfStringOrArrayParams
                ),
            ),
            cast_to=NoneType,
        )

    def array(
        self,
        *,
        integer_array_param: Iterable[int] | Omit = omit,
        string_array_param: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Endpoint with array query params

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/query_params/array",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "integer_array_param": integer_array_param,
                        "string_array_param": string_array_param,
                    },
                    query_param_array_params.QueryParamArrayParams,
                ),
            ),
            cast_to=NoneType,
        )

    def enum(
        self,
        *,
        integer_enum_param: Literal[100, 200] | Omit = omit,
        nullable_integer_enum_param: Optional[Literal[100, 200]] | Omit = omit,
        nullable_number_enum_param: Optional[Literal[100, 200]] | Omit = omit,
        nullable_string_enum_param: Optional[Literal["foo", "bar"]] | Omit = omit,
        number_enum_param: Literal[100, 200] | Omit = omit,
        string_enum_param: Literal["foo", "bar"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Endpoint with enum query params

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/query_params/enum",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "integer_enum_param": integer_enum_param,
                        "nullable_integer_enum_param": nullable_integer_enum_param,
                        "nullable_number_enum_param": nullable_number_enum_param,
                        "nullable_string_enum_param": nullable_string_enum_param,
                        "number_enum_param": number_enum_param,
                        "string_enum_param": string_enum_param,
                    },
                    query_param_enum_params.QueryParamEnumParams,
                ),
            ),
            cast_to=NoneType,
        )

    def object(
        self,
        *,
        object_param: query_param_object_params.ObjectParam | Omit = omit,
        object_ref_param: query_param_object_params.ObjectRefParam | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Endpoint with object query params

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/query_params/object",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "object_param": object_param,
                        "object_ref_param": object_ref_param,
                    },
                    query_param_object_params.QueryParamObjectParams,
                ),
            ),
            cast_to=NoneType,
        )

    def one_of(
        self,
        *,
        string_or_integer: Union[str, int] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Endpoint with oneOf query params

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/query_params/oneOf",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"string_or_integer": string_or_integer}, query_param_one_of_params.QueryParamOneOfParams
                ),
            ),
            cast_to=NoneType,
        )

    def primitives(
        self,
        *,
        boolean_param: bool | Omit = omit,
        integer_param: int | Omit = omit,
        number_param: float | Omit = omit,
        string_param: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Endpoint with a set of primitive type query params

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/query_params/primitives",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "boolean_param": boolean_param,
                        "integer_param": integer_param,
                        "number_param": number_param,
                        "string_param": string_param,
                    },
                    query_param_primitives_params.QueryParamPrimitivesParams,
                ),
            ),
            cast_to=NoneType,
        )


class AsyncQueryParamsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncQueryParamsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncQueryParamsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncQueryParamsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncQueryParamsResourceWithStreamingResponse(self)

    async def all_of(
        self,
        *,
        foo_and_bar: query_param_all_of_params.FooAndBar | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Endpoint with allOf query params

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/query_params/allOf",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"foo_and_bar": foo_and_bar}, query_param_all_of_params.QueryParamAllOfParams
                ),
            ),
            cast_to=NoneType,
        )

    async def any_of(
        self,
        *,
        string_or_integer: Union[str, int] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Endpoint with anyOf query params

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/query_params/anyOf",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"string_or_integer": string_or_integer}, query_param_any_of_params.QueryParamAnyOfParams
                ),
            ),
            cast_to=NoneType,
        )

    async def any_of_string_or_array(
        self,
        *,
        ids: Union[str, SequenceNotStr[str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Endpoint with anyOf query param that's string or array of strings

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/query_params/anyOfStringOrArray",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"ids": ids}, query_param_any_of_string_or_array_params.QueryParamAnyOfStringOrArrayParams
                ),
            ),
            cast_to=NoneType,
        )

    async def array(
        self,
        *,
        integer_array_param: Iterable[int] | Omit = omit,
        string_array_param: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Endpoint with array query params

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/query_params/array",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "integer_array_param": integer_array_param,
                        "string_array_param": string_array_param,
                    },
                    query_param_array_params.QueryParamArrayParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def enum(
        self,
        *,
        integer_enum_param: Literal[100, 200] | Omit = omit,
        nullable_integer_enum_param: Optional[Literal[100, 200]] | Omit = omit,
        nullable_number_enum_param: Optional[Literal[100, 200]] | Omit = omit,
        nullable_string_enum_param: Optional[Literal["foo", "bar"]] | Omit = omit,
        number_enum_param: Literal[100, 200] | Omit = omit,
        string_enum_param: Literal["foo", "bar"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Endpoint with enum query params

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/query_params/enum",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "integer_enum_param": integer_enum_param,
                        "nullable_integer_enum_param": nullable_integer_enum_param,
                        "nullable_number_enum_param": nullable_number_enum_param,
                        "nullable_string_enum_param": nullable_string_enum_param,
                        "number_enum_param": number_enum_param,
                        "string_enum_param": string_enum_param,
                    },
                    query_param_enum_params.QueryParamEnumParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def object(
        self,
        *,
        object_param: query_param_object_params.ObjectParam | Omit = omit,
        object_ref_param: query_param_object_params.ObjectRefParam | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Endpoint with object query params

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/query_params/object",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "object_param": object_param,
                        "object_ref_param": object_ref_param,
                    },
                    query_param_object_params.QueryParamObjectParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def one_of(
        self,
        *,
        string_or_integer: Union[str, int] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Endpoint with oneOf query params

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/query_params/oneOf",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"string_or_integer": string_or_integer}, query_param_one_of_params.QueryParamOneOfParams
                ),
            ),
            cast_to=NoneType,
        )

    async def primitives(
        self,
        *,
        boolean_param: bool | Omit = omit,
        integer_param: int | Omit = omit,
        number_param: float | Omit = omit,
        string_param: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Endpoint with a set of primitive type query params

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/query_params/primitives",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "boolean_param": boolean_param,
                        "integer_param": integer_param,
                        "number_param": number_param,
                        "string_param": string_param,
                    },
                    query_param_primitives_params.QueryParamPrimitivesParams,
                ),
            ),
            cast_to=NoneType,
        )


class QueryParamsResourceWithRawResponse:
    def __init__(self, query_params: QueryParamsResource) -> None:
        self._query_params = query_params

        self.all_of = _legacy_response.to_raw_response_wrapper(
            query_params.all_of,
        )
        self.any_of = _legacy_response.to_raw_response_wrapper(
            query_params.any_of,
        )
        self.any_of_string_or_array = _legacy_response.to_raw_response_wrapper(
            query_params.any_of_string_or_array,
        )
        self.array = _legacy_response.to_raw_response_wrapper(
            query_params.array,
        )
        self.enum = _legacy_response.to_raw_response_wrapper(
            query_params.enum,
        )
        self.object = _legacy_response.to_raw_response_wrapper(
            query_params.object,
        )
        self.one_of = _legacy_response.to_raw_response_wrapper(
            query_params.one_of,
        )
        self.primitives = _legacy_response.to_raw_response_wrapper(
            query_params.primitives,
        )


class AsyncQueryParamsResourceWithRawResponse:
    def __init__(self, query_params: AsyncQueryParamsResource) -> None:
        self._query_params = query_params

        self.all_of = _legacy_response.async_to_raw_response_wrapper(
            query_params.all_of,
        )
        self.any_of = _legacy_response.async_to_raw_response_wrapper(
            query_params.any_of,
        )
        self.any_of_string_or_array = _legacy_response.async_to_raw_response_wrapper(
            query_params.any_of_string_or_array,
        )
        self.array = _legacy_response.async_to_raw_response_wrapper(
            query_params.array,
        )
        self.enum = _legacy_response.async_to_raw_response_wrapper(
            query_params.enum,
        )
        self.object = _legacy_response.async_to_raw_response_wrapper(
            query_params.object,
        )
        self.one_of = _legacy_response.async_to_raw_response_wrapper(
            query_params.one_of,
        )
        self.primitives = _legacy_response.async_to_raw_response_wrapper(
            query_params.primitives,
        )


class QueryParamsResourceWithStreamingResponse:
    def __init__(self, query_params: QueryParamsResource) -> None:
        self._query_params = query_params

        self.all_of = to_streamed_response_wrapper(
            query_params.all_of,
        )
        self.any_of = to_streamed_response_wrapper(
            query_params.any_of,
        )
        self.any_of_string_or_array = to_streamed_response_wrapper(
            query_params.any_of_string_or_array,
        )
        self.array = to_streamed_response_wrapper(
            query_params.array,
        )
        self.enum = to_streamed_response_wrapper(
            query_params.enum,
        )
        self.object = to_streamed_response_wrapper(
            query_params.object,
        )
        self.one_of = to_streamed_response_wrapper(
            query_params.one_of,
        )
        self.primitives = to_streamed_response_wrapper(
            query_params.primitives,
        )


class AsyncQueryParamsResourceWithStreamingResponse:
    def __init__(self, query_params: AsyncQueryParamsResource) -> None:
        self._query_params = query_params

        self.all_of = async_to_streamed_response_wrapper(
            query_params.all_of,
        )
        self.any_of = async_to_streamed_response_wrapper(
            query_params.any_of,
        )
        self.any_of_string_or_array = async_to_streamed_response_wrapper(
            query_params.any_of_string_or_array,
        )
        self.array = async_to_streamed_response_wrapper(
            query_params.array,
        )
        self.enum = async_to_streamed_response_wrapper(
            query_params.enum,
        )
        self.object = async_to_streamed_response_wrapper(
            query_params.object,
        )
        self.one_of = async_to_streamed_response_wrapper(
            query_params.one_of,
        )
        self.primitives = async_to_streamed_response_wrapper(
            query_params.primitives,
        )
