# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from .. import _legacy_response
from ..types import (
    header_param_arrays_params,
    header_param_all_types_params,
    header_param_invalid_name_params,
    header_param_nullable_type_params,
    header_param_client_argument_params,
)
from .._types import Body, Omit, Query, Headers, NoneType, NotGiven, SequenceNotStr, omit, not_given
from .._utils import is_given, maybe_transform, strip_not_given, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from .._base_client import make_request_options

__all__ = ["HeaderParamsResource", "AsyncHeaderParamsResource"]


class HeaderParamsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> HeaderParamsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return HeaderParamsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> HeaderParamsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return HeaderParamsResourceWithStreamingResponse(self)

    def all_types(
        self,
        *,
        x_required_boolean: bool,
        x_required_integer: int,
        x_required_number: float,
        x_required_string: str,
        body_argument: str | Omit = omit,
        x_nullable_integer: int | Omit = omit,
        x_optional_boolean: bool | Omit = omit,
        x_optional_integer: int | Omit = omit,
        x_optional_number: float | Omit = omit,
        x_optional_string: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with all supported header param types.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers = {
            **strip_not_given(
                {
                    "X-Required-Boolean": ("true" if x_required_boolean else "false"),
                    "X-Required-Integer": str(x_required_integer),
                    "X-Required-Number": str(x_required_number),
                    "X-Required-String": x_required_string,
                    "X-Nullable-Integer": str(x_nullable_integer) if is_given(x_nullable_integer) else not_given,
                    "X-Optional-Boolean": ("true" if x_optional_boolean else "false")
                    if is_given(x_optional_boolean)
                    else not_given,
                    "X-Optional-Integer": str(x_optional_integer) if is_given(x_optional_integer) else not_given,
                    "X-Optional-Number": str(x_optional_number) if is_given(x_optional_number) else not_given,
                    "X-Optional-String": x_optional_string,
                }
            ),
            **(extra_headers or {}),
        }
        return self._post(
            "/header_params/all_types",
            body=maybe_transform(
                {"body_argument": body_argument}, header_param_all_types_params.HeaderParamAllTypesParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def arrays(
        self,
        *,
        x_required_int_array: Iterable[int],
        x_required_string_array: SequenceNotStr[str],
        body_argument: str | Omit = omit,
        x_optional_int_array: Iterable[int] | Omit = omit,
        x_optional_string_array: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `type: null` header param, which we should turn into a string
        type.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers = {
            **strip_not_given(
                {
                    "X-Required-Int-Array": ",".join(str(e) for e in x_required_int_array),
                    "X-Required-String-Array": ",".join(x_required_string_array),
                    "X-Optional-Int-Array": ",".join(str(e) for e in x_optional_int_array)
                    if is_given(x_optional_int_array)
                    else not_given,
                    "X-Optional-String-Array": ",".join(x_optional_string_array)
                    if is_given(x_optional_string_array)
                    else not_given,
                }
            ),
            **(extra_headers or {}),
        }
        return self._post(
            "/header_params/arrays",
            body=maybe_transform({"body_argument": body_argument}, header_param_arrays_params.HeaderParamArraysParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def client_argument(
        self,
        *,
        foo: str | Omit = omit,
        x_custom_endpoint_header: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        The `X-Client-Secret` header shouldn't be included in params definitions as it
        is already sent as a client argument.

        Whereas the `X-Custom-Endpoint-Header` should be included as it is only used
        here.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers = {
            **strip_not_given({"X-Custom-Endpoint-Header": x_custom_endpoint_header}),
            **(extra_headers or {}),
        }
        return self._post(
            "/header_params/client_argument",
            body=maybe_transform({"foo": foo}, header_param_client_argument_params.HeaderParamClientArgumentParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def invalid_name(
        self,
        *,
        foo: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        The header param with an empty name shouldn't cause codegen issues.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/header_params/invalid_name",
            body=maybe_transform({"foo": foo}, header_param_invalid_name_params.HeaderParamInvalidNameParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def nullable_type(
        self,
        *,
        body_argument: str | Omit = omit,
        x_null: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `type: null` header param, which we should turn into a string
        type.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers = {**strip_not_given({"X-Null": x_null}), **(extra_headers or {})}
        return self._post(
            "/header_params/nullable_type",
            body=maybe_transform(
                {"body_argument": body_argument}, header_param_nullable_type_params.HeaderParamNullableTypeParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )


class AsyncHeaderParamsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncHeaderParamsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncHeaderParamsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncHeaderParamsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncHeaderParamsResourceWithStreamingResponse(self)

    async def all_types(
        self,
        *,
        x_required_boolean: bool,
        x_required_integer: int,
        x_required_number: float,
        x_required_string: str,
        body_argument: str | Omit = omit,
        x_nullable_integer: int | Omit = omit,
        x_optional_boolean: bool | Omit = omit,
        x_optional_integer: int | Omit = omit,
        x_optional_number: float | Omit = omit,
        x_optional_string: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with all supported header param types.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers = {
            **strip_not_given(
                {
                    "X-Required-Boolean": ("true" if x_required_boolean else "false"),
                    "X-Required-Integer": str(x_required_integer),
                    "X-Required-Number": str(x_required_number),
                    "X-Required-String": x_required_string,
                    "X-Nullable-Integer": str(x_nullable_integer) if is_given(x_nullable_integer) else not_given,
                    "X-Optional-Boolean": ("true" if x_optional_boolean else "false")
                    if is_given(x_optional_boolean)
                    else not_given,
                    "X-Optional-Integer": str(x_optional_integer) if is_given(x_optional_integer) else not_given,
                    "X-Optional-Number": str(x_optional_number) if is_given(x_optional_number) else not_given,
                    "X-Optional-String": x_optional_string,
                }
            ),
            **(extra_headers or {}),
        }
        return await self._post(
            "/header_params/all_types",
            body=await async_maybe_transform(
                {"body_argument": body_argument}, header_param_all_types_params.HeaderParamAllTypesParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    async def arrays(
        self,
        *,
        x_required_int_array: Iterable[int],
        x_required_string_array: SequenceNotStr[str],
        body_argument: str | Omit = omit,
        x_optional_int_array: Iterable[int] | Omit = omit,
        x_optional_string_array: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `type: null` header param, which we should turn into a string
        type.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers = {
            **strip_not_given(
                {
                    "X-Required-Int-Array": ",".join(str(e) for e in x_required_int_array),
                    "X-Required-String-Array": ",".join(x_required_string_array),
                    "X-Optional-Int-Array": ",".join(str(e) for e in x_optional_int_array)
                    if is_given(x_optional_int_array)
                    else not_given,
                    "X-Optional-String-Array": ",".join(x_optional_string_array)
                    if is_given(x_optional_string_array)
                    else not_given,
                }
            ),
            **(extra_headers or {}),
        }
        return await self._post(
            "/header_params/arrays",
            body=await async_maybe_transform(
                {"body_argument": body_argument}, header_param_arrays_params.HeaderParamArraysParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    async def client_argument(
        self,
        *,
        foo: str | Omit = omit,
        x_custom_endpoint_header: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        The `X-Client-Secret` header shouldn't be included in params definitions as it
        is already sent as a client argument.

        Whereas the `X-Custom-Endpoint-Header` should be included as it is only used
        here.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers = {
            **strip_not_given({"X-Custom-Endpoint-Header": x_custom_endpoint_header}),
            **(extra_headers or {}),
        }
        return await self._post(
            "/header_params/client_argument",
            body=await async_maybe_transform(
                {"foo": foo}, header_param_client_argument_params.HeaderParamClientArgumentParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    async def invalid_name(
        self,
        *,
        foo: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        The header param with an empty name shouldn't cause codegen issues.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/header_params/invalid_name",
            body=await async_maybe_transform(
                {"foo": foo}, header_param_invalid_name_params.HeaderParamInvalidNameParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    async def nullable_type(
        self,
        *,
        body_argument: str | Omit = omit,
        x_null: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `type: null` header param, which we should turn into a string
        type.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers = {**strip_not_given({"X-Null": x_null}), **(extra_headers or {})}
        return await self._post(
            "/header_params/nullable_type",
            body=await async_maybe_transform(
                {"body_argument": body_argument}, header_param_nullable_type_params.HeaderParamNullableTypeParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )


class HeaderParamsResourceWithRawResponse:
    def __init__(self, header_params: HeaderParamsResource) -> None:
        self._header_params = header_params

        self.all_types = _legacy_response.to_raw_response_wrapper(
            header_params.all_types,
        )
        self.arrays = _legacy_response.to_raw_response_wrapper(
            header_params.arrays,
        )
        self.client_argument = _legacy_response.to_raw_response_wrapper(
            header_params.client_argument,
        )
        self.invalid_name = _legacy_response.to_raw_response_wrapper(
            header_params.invalid_name,
        )
        self.nullable_type = _legacy_response.to_raw_response_wrapper(
            header_params.nullable_type,
        )


class AsyncHeaderParamsResourceWithRawResponse:
    def __init__(self, header_params: AsyncHeaderParamsResource) -> None:
        self._header_params = header_params

        self.all_types = _legacy_response.async_to_raw_response_wrapper(
            header_params.all_types,
        )
        self.arrays = _legacy_response.async_to_raw_response_wrapper(
            header_params.arrays,
        )
        self.client_argument = _legacy_response.async_to_raw_response_wrapper(
            header_params.client_argument,
        )
        self.invalid_name = _legacy_response.async_to_raw_response_wrapper(
            header_params.invalid_name,
        )
        self.nullable_type = _legacy_response.async_to_raw_response_wrapper(
            header_params.nullable_type,
        )


class HeaderParamsResourceWithStreamingResponse:
    def __init__(self, header_params: HeaderParamsResource) -> None:
        self._header_params = header_params

        self.all_types = to_streamed_response_wrapper(
            header_params.all_types,
        )
        self.arrays = to_streamed_response_wrapper(
            header_params.arrays,
        )
        self.client_argument = to_streamed_response_wrapper(
            header_params.client_argument,
        )
        self.invalid_name = to_streamed_response_wrapper(
            header_params.invalid_name,
        )
        self.nullable_type = to_streamed_response_wrapper(
            header_params.nullable_type,
        )


class AsyncHeaderParamsResourceWithStreamingResponse:
    def __init__(self, header_params: AsyncHeaderParamsResource) -> None:
        self._header_params = header_params

        self.all_types = async_to_streamed_response_wrapper(
            header_params.all_types,
        )
        self.arrays = async_to_streamed_response_wrapper(
            header_params.arrays,
        )
        self.client_argument = async_to_streamed_response_wrapper(
            header_params.client_argument,
        )
        self.invalid_name = async_to_streamed_response_wrapper(
            header_params.invalid_name,
        )
        self.nullable_type = async_to_streamed_response_wrapper(
            header_params.nullable_type,
        )
