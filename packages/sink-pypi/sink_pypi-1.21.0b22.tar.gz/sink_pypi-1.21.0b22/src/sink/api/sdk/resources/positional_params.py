# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from .. import _legacy_response
from ..types import (
    positional_param_body_params,
    positional_param_query_params,
    positional_param_basic_body_params,
    positional_param_basic_query_params,
    positional_param_kitchen_sink_params,
    positional_param_query_and_path_params,
    positional_param_query_multiple_params,
    positional_param_body_extra_param_params,
    positional_param_union_body_and_path_params,
    positional_param_multiple_path_params_params,
)
from .._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, not_given
from .._utils import maybe_transform, strip_not_given, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from .._base_client import make_request_options

__all__ = ["PositionalParamsResource", "AsyncPositionalParamsResource"]


class PositionalParamsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PositionalParamsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return PositionalParamsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PositionalParamsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return PositionalParamsResourceWithStreamingResponse(self)

    def basic_body(
        self,
        *,
        key1: str,
        options: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with no positional params and a body param.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/positional_params/basic_body",
            body=maybe_transform(
                {
                    "key1": key1,
                    "options": options,
                },
                positional_param_basic_body_params.PositionalParamBasicBodyParams,
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

    def basic_query(
        self,
        *,
        key1: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Endpoint with no positional params and a query object.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/positional_params/basic_query",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"key1": key1}, positional_param_basic_query_params.PositionalParamBasicQueryParams
                ),
            ),
            cast_to=NoneType,
        )

    def body(
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
        Endpoint with no positional params and a body object.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/positional_params/body",
            body=maybe_transform({"foo": foo}, positional_param_body_params.PositionalParamBodyParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def body_extra_param(
        self,
        *,
        extra_key: str,
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
        Endpoint with no positional params and a body object.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/positional_params/body_extra_param",
            body=maybe_transform(
                {
                    "extra_key": extra_key,
                    "foo": foo,
                },
                positional_param_body_extra_param_params.PositionalParamBodyExtraParamParams,
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

    def kitchen_sink(
        self,
        id: str,
        *,
        key: str,
        im_a_camel: str,
        option1: bool,
        camel_case: str,
        option2: str | Omit = omit,
        really_cool_snake: str | Omit = omit,
        bar: float | Omit = omit,
        options: str | Omit = omit,
        x_custom_header: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with everything under the sun (to excercise positional params).

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        if not key:
            raise ValueError(f"Expected a non-empty value for `key` but received {key!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers = {**strip_not_given({"X-Custom-Header": x_custom_header}), **(extra_headers or {})}
        return self._post(
            f"/positional_params/query/{id}/kitchen_sink/{key}",
            body=maybe_transform(
                {
                    "camel_case": camel_case,
                    "bar": bar,
                    "options": options,
                },
                positional_param_kitchen_sink_params.PositionalParamKitchenSinkParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
                query=maybe_transform(
                    {
                        "im_a_camel": im_a_camel,
                        "option1": option1,
                        "option2": option2,
                        "really_cool_snake": really_cool_snake,
                    },
                    positional_param_kitchen_sink_params.PositionalParamKitchenSinkParams,
                ),
            ),
            cast_to=NoneType,
        )

    def multiple_path_params(
        self,
        second: str,
        *,
        first: str,
        last: str,
        name: str,
        options: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a positional path parameter in the middle.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not first:
            raise ValueError(f"Expected a non-empty value for `first` but received {first!r}")
        if not second:
            raise ValueError(f"Expected a non-empty value for `second` but received {second!r}")
        if not last:
            raise ValueError(f"Expected a non-empty value for `last` but received {last!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/positional_params/{first}/{second}/{last}",
            body=maybe_transform(
                {
                    "name": name,
                    "options": options,
                },
                positional_param_multiple_path_params_params.PositionalParamMultiplePathParamsParams,
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

    def query(
        self,
        *,
        foo: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Endpoint with a positional query parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/positional_params/query",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"foo": foo}, positional_param_query_params.PositionalParamQueryParams),
            ),
            cast_to=NoneType,
        )

    def query_and_path(
        self,
        id: str,
        *,
        bar: float,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a positional path parameter and a query parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/positional_params/query/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
                query=maybe_transform(
                    {"bar": bar}, positional_param_query_and_path_params.PositionalParamQueryAndPathParams
                ),
            ),
            cast_to=NoneType,
        )

    def query_multiple(
        self,
        *,
        bar: str,
        foo: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Endpoint with a positional query parameter.

        Args:
          bar: Some description about bar.

          foo: Some description about foo.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/positional_params/query_multiple",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "bar": bar,
                        "foo": foo,
                    },
                    positional_param_query_multiple_params.PositionalParamQueryMultipleParams,
                ),
            ),
            cast_to=NoneType,
        )

    def single(
        self,
        single: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Endpoint with a single positional path parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not single:
            raise ValueError(f"Expected a non-empty value for `single` but received {single!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/positional_params/{single}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def union_body_and_path(
        self,
        id: str,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with no positional params and a body object.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/positional_params/body/union/{id}",
            body=maybe_transform(
                {"kind": kind}, positional_param_union_body_and_path_params.PositionalParamUnionBodyAndPathParams
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


class AsyncPositionalParamsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPositionalParamsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncPositionalParamsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPositionalParamsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncPositionalParamsResourceWithStreamingResponse(self)

    async def basic_body(
        self,
        *,
        key1: str,
        options: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with no positional params and a body param.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/positional_params/basic_body",
            body=await async_maybe_transform(
                {
                    "key1": key1,
                    "options": options,
                },
                positional_param_basic_body_params.PositionalParamBasicBodyParams,
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

    async def basic_query(
        self,
        *,
        key1: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Endpoint with no positional params and a query object.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/positional_params/basic_query",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"key1": key1}, positional_param_basic_query_params.PositionalParamBasicQueryParams
                ),
            ),
            cast_to=NoneType,
        )

    async def body(
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
        Endpoint with no positional params and a body object.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/positional_params/body",
            body=await async_maybe_transform({"foo": foo}, positional_param_body_params.PositionalParamBodyParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    async def body_extra_param(
        self,
        *,
        extra_key: str,
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
        Endpoint with no positional params and a body object.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/positional_params/body_extra_param",
            body=await async_maybe_transform(
                {
                    "extra_key": extra_key,
                    "foo": foo,
                },
                positional_param_body_extra_param_params.PositionalParamBodyExtraParamParams,
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

    async def kitchen_sink(
        self,
        id: str,
        *,
        key: str,
        im_a_camel: str,
        option1: bool,
        camel_case: str,
        option2: str | Omit = omit,
        really_cool_snake: str | Omit = omit,
        bar: float | Omit = omit,
        options: str | Omit = omit,
        x_custom_header: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with everything under the sun (to excercise positional params).

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        if not key:
            raise ValueError(f"Expected a non-empty value for `key` but received {key!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers = {**strip_not_given({"X-Custom-Header": x_custom_header}), **(extra_headers or {})}
        return await self._post(
            f"/positional_params/query/{id}/kitchen_sink/{key}",
            body=await async_maybe_transform(
                {
                    "camel_case": camel_case,
                    "bar": bar,
                    "options": options,
                },
                positional_param_kitchen_sink_params.PositionalParamKitchenSinkParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
                query=await async_maybe_transform(
                    {
                        "im_a_camel": im_a_camel,
                        "option1": option1,
                        "option2": option2,
                        "really_cool_snake": really_cool_snake,
                    },
                    positional_param_kitchen_sink_params.PositionalParamKitchenSinkParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def multiple_path_params(
        self,
        second: str,
        *,
        first: str,
        last: str,
        name: str,
        options: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a positional path parameter in the middle.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not first:
            raise ValueError(f"Expected a non-empty value for `first` but received {first!r}")
        if not second:
            raise ValueError(f"Expected a non-empty value for `second` but received {second!r}")
        if not last:
            raise ValueError(f"Expected a non-empty value for `last` but received {last!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/positional_params/{first}/{second}/{last}",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "options": options,
                },
                positional_param_multiple_path_params_params.PositionalParamMultiplePathParamsParams,
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

    async def query(
        self,
        *,
        foo: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Endpoint with a positional query parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/positional_params/query",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"foo": foo}, positional_param_query_params.PositionalParamQueryParams
                ),
            ),
            cast_to=NoneType,
        )

    async def query_and_path(
        self,
        id: str,
        *,
        bar: float,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a positional path parameter and a query parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/positional_params/query/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
                query=await async_maybe_transform(
                    {"bar": bar}, positional_param_query_and_path_params.PositionalParamQueryAndPathParams
                ),
            ),
            cast_to=NoneType,
        )

    async def query_multiple(
        self,
        *,
        bar: str,
        foo: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Endpoint with a positional query parameter.

        Args:
          bar: Some description about bar.

          foo: Some description about foo.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/positional_params/query_multiple",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "bar": bar,
                        "foo": foo,
                    },
                    positional_param_query_multiple_params.PositionalParamQueryMultipleParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def single(
        self,
        single: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Endpoint with a single positional path parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not single:
            raise ValueError(f"Expected a non-empty value for `single` but received {single!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/positional_params/{single}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def union_body_and_path(
        self,
        id: str,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with no positional params and a body object.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/positional_params/body/union/{id}",
            body=await async_maybe_transform(
                {"kind": kind}, positional_param_union_body_and_path_params.PositionalParamUnionBodyAndPathParams
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


class PositionalParamsResourceWithRawResponse:
    def __init__(self, positional_params: PositionalParamsResource) -> None:
        self._positional_params = positional_params

        self.basic_body = _legacy_response.to_raw_response_wrapper(
            positional_params.basic_body,
        )
        self.basic_query = _legacy_response.to_raw_response_wrapper(
            positional_params.basic_query,
        )
        self.body = _legacy_response.to_raw_response_wrapper(
            positional_params.body,
        )
        self.body_extra_param = _legacy_response.to_raw_response_wrapper(
            positional_params.body_extra_param,
        )
        self.kitchen_sink = _legacy_response.to_raw_response_wrapper(
            positional_params.kitchen_sink,
        )
        self.multiple_path_params = _legacy_response.to_raw_response_wrapper(
            positional_params.multiple_path_params,
        )
        self.query = _legacy_response.to_raw_response_wrapper(
            positional_params.query,
        )
        self.query_and_path = _legacy_response.to_raw_response_wrapper(
            positional_params.query_and_path,
        )
        self.query_multiple = _legacy_response.to_raw_response_wrapper(
            positional_params.query_multiple,
        )
        self.single = _legacy_response.to_raw_response_wrapper(
            positional_params.single,
        )
        self.union_body_and_path = _legacy_response.to_raw_response_wrapper(
            positional_params.union_body_and_path,
        )


class AsyncPositionalParamsResourceWithRawResponse:
    def __init__(self, positional_params: AsyncPositionalParamsResource) -> None:
        self._positional_params = positional_params

        self.basic_body = _legacy_response.async_to_raw_response_wrapper(
            positional_params.basic_body,
        )
        self.basic_query = _legacy_response.async_to_raw_response_wrapper(
            positional_params.basic_query,
        )
        self.body = _legacy_response.async_to_raw_response_wrapper(
            positional_params.body,
        )
        self.body_extra_param = _legacy_response.async_to_raw_response_wrapper(
            positional_params.body_extra_param,
        )
        self.kitchen_sink = _legacy_response.async_to_raw_response_wrapper(
            positional_params.kitchen_sink,
        )
        self.multiple_path_params = _legacy_response.async_to_raw_response_wrapper(
            positional_params.multiple_path_params,
        )
        self.query = _legacy_response.async_to_raw_response_wrapper(
            positional_params.query,
        )
        self.query_and_path = _legacy_response.async_to_raw_response_wrapper(
            positional_params.query_and_path,
        )
        self.query_multiple = _legacy_response.async_to_raw_response_wrapper(
            positional_params.query_multiple,
        )
        self.single = _legacy_response.async_to_raw_response_wrapper(
            positional_params.single,
        )
        self.union_body_and_path = _legacy_response.async_to_raw_response_wrapper(
            positional_params.union_body_and_path,
        )


class PositionalParamsResourceWithStreamingResponse:
    def __init__(self, positional_params: PositionalParamsResource) -> None:
        self._positional_params = positional_params

        self.basic_body = to_streamed_response_wrapper(
            positional_params.basic_body,
        )
        self.basic_query = to_streamed_response_wrapper(
            positional_params.basic_query,
        )
        self.body = to_streamed_response_wrapper(
            positional_params.body,
        )
        self.body_extra_param = to_streamed_response_wrapper(
            positional_params.body_extra_param,
        )
        self.kitchen_sink = to_streamed_response_wrapper(
            positional_params.kitchen_sink,
        )
        self.multiple_path_params = to_streamed_response_wrapper(
            positional_params.multiple_path_params,
        )
        self.query = to_streamed_response_wrapper(
            positional_params.query,
        )
        self.query_and_path = to_streamed_response_wrapper(
            positional_params.query_and_path,
        )
        self.query_multiple = to_streamed_response_wrapper(
            positional_params.query_multiple,
        )
        self.single = to_streamed_response_wrapper(
            positional_params.single,
        )
        self.union_body_and_path = to_streamed_response_wrapper(
            positional_params.union_body_and_path,
        )


class AsyncPositionalParamsResourceWithStreamingResponse:
    def __init__(self, positional_params: AsyncPositionalParamsResource) -> None:
        self._positional_params = positional_params

        self.basic_body = async_to_streamed_response_wrapper(
            positional_params.basic_body,
        )
        self.basic_query = async_to_streamed_response_wrapper(
            positional_params.basic_query,
        )
        self.body = async_to_streamed_response_wrapper(
            positional_params.body,
        )
        self.body_extra_param = async_to_streamed_response_wrapper(
            positional_params.body_extra_param,
        )
        self.kitchen_sink = async_to_streamed_response_wrapper(
            positional_params.kitchen_sink,
        )
        self.multiple_path_params = async_to_streamed_response_wrapper(
            positional_params.multiple_path_params,
        )
        self.query = async_to_streamed_response_wrapper(
            positional_params.query,
        )
        self.query_and_path = async_to_streamed_response_wrapper(
            positional_params.query_and_path,
        )
        self.query_multiple = async_to_streamed_response_wrapper(
            positional_params.query_multiple,
        )
        self.single = async_to_streamed_response_wrapper(
            positional_params.single,
        )
        self.union_body_and_path = async_to_streamed_response_wrapper(
            positional_params.union_body_and_path,
        )
