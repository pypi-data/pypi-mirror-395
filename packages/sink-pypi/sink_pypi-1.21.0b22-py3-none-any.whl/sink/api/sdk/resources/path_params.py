# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import date, datetime
from typing_extensions import Literal

import httpx

from .. import _legacy_response
from ..types import path_param_nullable_params_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from .._base_client import make_request_options
from ..types.path_param_multiple_response import PathParamMultipleResponse
from ..types.path_param_singular_response import PathParamSingularResponse
from ..types.path_param_query_param_response import PathParamQueryParamResponse
from ..types.path_param_colon_suffix_response import PathParamColonSuffixResponse
from ..types.shared.basic_shared_model_object import BasicSharedModelObject
from ..types.path_param_file_extension_response import PathParamFileExtensionResponse

__all__ = ["PathParamsResource", "AsyncPathParamsResource"]


class PathParamsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PathParamsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return PathParamsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PathParamsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return PathParamsResourceWithStreamingResponse(self)

    def colon_suffix(
        self,
        with_verb: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> PathParamColonSuffixResponse:
        """
        Endpoint with a path param followed by a verb.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            f"/path_params/{with_verb}:initiate",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=PathParamColonSuffixResponse,
        )

    def dashed_param(
        self,
        dashed_param: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BasicSharedModelObject:
        """
        Endpoint with a singular path parameter that uses a `dash` separator.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not dashed_param:
            raise ValueError(f"Expected a non-empty value for `dashed_param` but received {dashed_param!r}")
        return self._post(
            f"/path_params/{dashed_param}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BasicSharedModelObject,
        )

    def date_param(
        self,
        date_param: Union[str, date],
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BasicSharedModelObject:
        """
        Endpoint with a singular path parameter that is a date type.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not date_param:
            raise ValueError(f"Expected a non-empty value for `date_param` but received {date_param!r}")
        return self._post(
            f"/path_params/dates/{date_param}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BasicSharedModelObject,
        )

    def datetime_param(
        self,
        datetime_param: Union[str, datetime],
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BasicSharedModelObject:
        """
        Endpoint with a singular path parameter that is a date-time type.

        Args:
          datetime_param: An ISO 8601 timestamp for when the card was created. UTC time zone.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not datetime_param:
            raise ValueError(f"Expected a non-empty value for `datetime_param` but received {datetime_param!r}")
        return self._post(
            f"/path_params/date_times/{datetime_param}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BasicSharedModelObject,
        )

    def enum_param(
        self,
        enum_param: Literal["A", "B", "C"],
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BasicSharedModelObject:
        """
        Endpoint with a singular path parameter that is an enum type.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not enum_param:
            raise ValueError(f"Expected a non-empty value for `enum_param` but received {enum_param!r}")
        return self._post(
            f"/path_params/enums/{enum_param}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BasicSharedModelObject,
        )

    def file_extension(
        self,
        with_file_extension: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> PathParamFileExtensionResponse:
        """
        Endpoint with a path param followed by a file extension.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            f"/path_params/{with_file_extension}.json",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=PathParamFileExtensionResponse,
        )

    def integer_param(
        self,
        integer_param: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BasicSharedModelObject:
        """
        Endpoint with a singular path parameter that is of an integer type.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            f"/path_params/{integer_param}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BasicSharedModelObject,
        )

    def multiple(
        self,
        last: str,
        *,
        first: str,
        second: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> PathParamMultipleResponse:
        """
        Endpoint with multiple path parameters.

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
        return self._post(
            f"/path_params/{first}/{second}/{last}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=PathParamMultipleResponse,
        )

    def nullable_params(
        self,
        nullable_param_3: Literal["foo"],
        *,
        nullable_param_1: str,
        nullable_param_2: str,
        foo: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BasicSharedModelObject:
        """
        Endpoint with nullable path parameters.

        In a spec file nullable path params are ambiguous and likely to be a mistake.
        They are transformed to non-nullable as part of the spec normalization and a
        diagnostic is emitted.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not nullable_param_1:
            raise ValueError(f"Expected a non-empty value for `nullable_param_1` but received {nullable_param_1!r}")
        if not nullable_param_2:
            raise ValueError(f"Expected a non-empty value for `nullable_param_2` but received {nullable_param_2!r}")
        if not nullable_param_3:
            raise ValueError(f"Expected a non-empty value for `nullable_param_3` but received {nullable_param_3!r}")
        return self._post(
            f"/path_params/nullable/{nullable_param_1}/{nullable_param_2}/{nullable_param_3}",
            body=maybe_transform({"foo": foo}, path_param_nullable_params_params.PathParamNullableParamsParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BasicSharedModelObject,
        )

    def params_mixed_types(
        self,
        string_param: str,
        *,
        integer_param: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BasicSharedModelObject:
        """Endpoint with multiple path parameters that are of different types, e.g.

        one
        integer type and the other string type.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not string_param:
            raise ValueError(f"Expected a non-empty value for `string_param` but received {string_param!r}")
        return self._post(
            f"/path_params/mixed/{integer_param}/{string_param}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BasicSharedModelObject,
        )

    def query_param(
        self,
        with_query_param: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> PathParamQueryParamResponse:
        """
        Endpoint with a path param followed by a query param in the path itself.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            f"/path_params/{with_query_param}?beta=true",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=PathParamQueryParamResponse,
        )

    def singular(
        self,
        singular: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> PathParamSingularResponse:
        """
        Endpoint with a singular path parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not singular:
            raise ValueError(f"Expected a non-empty value for `singular` but received {singular!r}")
        return self._post(
            f"/path_params/{singular}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=PathParamSingularResponse,
        )


class AsyncPathParamsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPathParamsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncPathParamsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPathParamsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncPathParamsResourceWithStreamingResponse(self)

    async def colon_suffix(
        self,
        with_verb: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> PathParamColonSuffixResponse:
        """
        Endpoint with a path param followed by a verb.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            f"/path_params/{with_verb}:initiate",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=PathParamColonSuffixResponse,
        )

    async def dashed_param(
        self,
        dashed_param: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BasicSharedModelObject:
        """
        Endpoint with a singular path parameter that uses a `dash` separator.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not dashed_param:
            raise ValueError(f"Expected a non-empty value for `dashed_param` but received {dashed_param!r}")
        return await self._post(
            f"/path_params/{dashed_param}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BasicSharedModelObject,
        )

    async def date_param(
        self,
        date_param: Union[str, date],
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BasicSharedModelObject:
        """
        Endpoint with a singular path parameter that is a date type.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not date_param:
            raise ValueError(f"Expected a non-empty value for `date_param` but received {date_param!r}")
        return await self._post(
            f"/path_params/dates/{date_param}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BasicSharedModelObject,
        )

    async def datetime_param(
        self,
        datetime_param: Union[str, datetime],
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BasicSharedModelObject:
        """
        Endpoint with a singular path parameter that is a date-time type.

        Args:
          datetime_param: An ISO 8601 timestamp for when the card was created. UTC time zone.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not datetime_param:
            raise ValueError(f"Expected a non-empty value for `datetime_param` but received {datetime_param!r}")
        return await self._post(
            f"/path_params/date_times/{datetime_param}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BasicSharedModelObject,
        )

    async def enum_param(
        self,
        enum_param: Literal["A", "B", "C"],
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BasicSharedModelObject:
        """
        Endpoint with a singular path parameter that is an enum type.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not enum_param:
            raise ValueError(f"Expected a non-empty value for `enum_param` but received {enum_param!r}")
        return await self._post(
            f"/path_params/enums/{enum_param}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BasicSharedModelObject,
        )

    async def file_extension(
        self,
        with_file_extension: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> PathParamFileExtensionResponse:
        """
        Endpoint with a path param followed by a file extension.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            f"/path_params/{with_file_extension}.json",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=PathParamFileExtensionResponse,
        )

    async def integer_param(
        self,
        integer_param: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BasicSharedModelObject:
        """
        Endpoint with a singular path parameter that is of an integer type.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            f"/path_params/{integer_param}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BasicSharedModelObject,
        )

    async def multiple(
        self,
        last: str,
        *,
        first: str,
        second: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> PathParamMultipleResponse:
        """
        Endpoint with multiple path parameters.

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
        return await self._post(
            f"/path_params/{first}/{second}/{last}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=PathParamMultipleResponse,
        )

    async def nullable_params(
        self,
        nullable_param_3: Literal["foo"],
        *,
        nullable_param_1: str,
        nullable_param_2: str,
        foo: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BasicSharedModelObject:
        """
        Endpoint with nullable path parameters.

        In a spec file nullable path params are ambiguous and likely to be a mistake.
        They are transformed to non-nullable as part of the spec normalization and a
        diagnostic is emitted.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not nullable_param_1:
            raise ValueError(f"Expected a non-empty value for `nullable_param_1` but received {nullable_param_1!r}")
        if not nullable_param_2:
            raise ValueError(f"Expected a non-empty value for `nullable_param_2` but received {nullable_param_2!r}")
        if not nullable_param_3:
            raise ValueError(f"Expected a non-empty value for `nullable_param_3` but received {nullable_param_3!r}")
        return await self._post(
            f"/path_params/nullable/{nullable_param_1}/{nullable_param_2}/{nullable_param_3}",
            body=await async_maybe_transform(
                {"foo": foo}, path_param_nullable_params_params.PathParamNullableParamsParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BasicSharedModelObject,
        )

    async def params_mixed_types(
        self,
        string_param: str,
        *,
        integer_param: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BasicSharedModelObject:
        """Endpoint with multiple path parameters that are of different types, e.g.

        one
        integer type and the other string type.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not string_param:
            raise ValueError(f"Expected a non-empty value for `string_param` but received {string_param!r}")
        return await self._post(
            f"/path_params/mixed/{integer_param}/{string_param}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BasicSharedModelObject,
        )

    async def query_param(
        self,
        with_query_param: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> PathParamQueryParamResponse:
        """
        Endpoint with a path param followed by a query param in the path itself.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            f"/path_params/{with_query_param}?beta=true",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=PathParamQueryParamResponse,
        )

    async def singular(
        self,
        singular: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> PathParamSingularResponse:
        """
        Endpoint with a singular path parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not singular:
            raise ValueError(f"Expected a non-empty value for `singular` but received {singular!r}")
        return await self._post(
            f"/path_params/{singular}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=PathParamSingularResponse,
        )


class PathParamsResourceWithRawResponse:
    def __init__(self, path_params: PathParamsResource) -> None:
        self._path_params = path_params

        self.colon_suffix = _legacy_response.to_raw_response_wrapper(
            path_params.colon_suffix,
        )
        self.dashed_param = _legacy_response.to_raw_response_wrapper(
            path_params.dashed_param,
        )
        self.date_param = _legacy_response.to_raw_response_wrapper(
            path_params.date_param,
        )
        self.datetime_param = _legacy_response.to_raw_response_wrapper(
            path_params.datetime_param,
        )
        self.enum_param = _legacy_response.to_raw_response_wrapper(
            path_params.enum_param,
        )
        self.file_extension = _legacy_response.to_raw_response_wrapper(
            path_params.file_extension,
        )
        self.integer_param = _legacy_response.to_raw_response_wrapper(
            path_params.integer_param,
        )
        self.multiple = _legacy_response.to_raw_response_wrapper(
            path_params.multiple,
        )
        self.nullable_params = _legacy_response.to_raw_response_wrapper(
            path_params.nullable_params,
        )
        self.params_mixed_types = _legacy_response.to_raw_response_wrapper(
            path_params.params_mixed_types,
        )
        self.query_param = _legacy_response.to_raw_response_wrapper(
            path_params.query_param,
        )
        self.singular = _legacy_response.to_raw_response_wrapper(
            path_params.singular,
        )


class AsyncPathParamsResourceWithRawResponse:
    def __init__(self, path_params: AsyncPathParamsResource) -> None:
        self._path_params = path_params

        self.colon_suffix = _legacy_response.async_to_raw_response_wrapper(
            path_params.colon_suffix,
        )
        self.dashed_param = _legacy_response.async_to_raw_response_wrapper(
            path_params.dashed_param,
        )
        self.date_param = _legacy_response.async_to_raw_response_wrapper(
            path_params.date_param,
        )
        self.datetime_param = _legacy_response.async_to_raw_response_wrapper(
            path_params.datetime_param,
        )
        self.enum_param = _legacy_response.async_to_raw_response_wrapper(
            path_params.enum_param,
        )
        self.file_extension = _legacy_response.async_to_raw_response_wrapper(
            path_params.file_extension,
        )
        self.integer_param = _legacy_response.async_to_raw_response_wrapper(
            path_params.integer_param,
        )
        self.multiple = _legacy_response.async_to_raw_response_wrapper(
            path_params.multiple,
        )
        self.nullable_params = _legacy_response.async_to_raw_response_wrapper(
            path_params.nullable_params,
        )
        self.params_mixed_types = _legacy_response.async_to_raw_response_wrapper(
            path_params.params_mixed_types,
        )
        self.query_param = _legacy_response.async_to_raw_response_wrapper(
            path_params.query_param,
        )
        self.singular = _legacy_response.async_to_raw_response_wrapper(
            path_params.singular,
        )


class PathParamsResourceWithStreamingResponse:
    def __init__(self, path_params: PathParamsResource) -> None:
        self._path_params = path_params

        self.colon_suffix = to_streamed_response_wrapper(
            path_params.colon_suffix,
        )
        self.dashed_param = to_streamed_response_wrapper(
            path_params.dashed_param,
        )
        self.date_param = to_streamed_response_wrapper(
            path_params.date_param,
        )
        self.datetime_param = to_streamed_response_wrapper(
            path_params.datetime_param,
        )
        self.enum_param = to_streamed_response_wrapper(
            path_params.enum_param,
        )
        self.file_extension = to_streamed_response_wrapper(
            path_params.file_extension,
        )
        self.integer_param = to_streamed_response_wrapper(
            path_params.integer_param,
        )
        self.multiple = to_streamed_response_wrapper(
            path_params.multiple,
        )
        self.nullable_params = to_streamed_response_wrapper(
            path_params.nullable_params,
        )
        self.params_mixed_types = to_streamed_response_wrapper(
            path_params.params_mixed_types,
        )
        self.query_param = to_streamed_response_wrapper(
            path_params.query_param,
        )
        self.singular = to_streamed_response_wrapper(
            path_params.singular,
        )


class AsyncPathParamsResourceWithStreamingResponse:
    def __init__(self, path_params: AsyncPathParamsResource) -> None:
        self._path_params = path_params

        self.colon_suffix = async_to_streamed_response_wrapper(
            path_params.colon_suffix,
        )
        self.dashed_param = async_to_streamed_response_wrapper(
            path_params.dashed_param,
        )
        self.date_param = async_to_streamed_response_wrapper(
            path_params.date_param,
        )
        self.datetime_param = async_to_streamed_response_wrapper(
            path_params.datetime_param,
        )
        self.enum_param = async_to_streamed_response_wrapper(
            path_params.enum_param,
        )
        self.file_extension = async_to_streamed_response_wrapper(
            path_params.file_extension,
        )
        self.integer_param = async_to_streamed_response_wrapper(
            path_params.integer_param,
        )
        self.multiple = async_to_streamed_response_wrapper(
            path_params.multiple,
        )
        self.nullable_params = async_to_streamed_response_wrapper(
            path_params.nullable_params,
        )
        self.params_mixed_types = async_to_streamed_response_wrapper(
            path_params.params_mixed_types,
        )
        self.query_param = async_to_streamed_response_wrapper(
            path_params.query_param,
        )
        self.singular = async_to_streamed_response_wrapper(
            path_params.singular,
        )
