# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal

import httpx

from ... import _legacy_response
from ..._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ..._base_client import make_request_options
from ...types.body_params import union_param_union_enum_new_type_params
from ...types.body_params.model_new_type_string import ModelNewTypeString

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

    def param_union_enum_new_type(
        self,
        *,
        model: Union[ModelNewTypeString, Literal["gpt-4", "gpt-3"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Defines a request parameter that is configured to generate a `NewType` type in
        Python and is used in a union type alongside an enum.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/body_params/unions/param_union_enum_new_type",
            body=maybe_transform(
                {"model": model}, union_param_union_enum_new_type_params.UnionParamUnionEnumNewTypeParams
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

    async def param_union_enum_new_type(
        self,
        *,
        model: Union[ModelNewTypeString, Literal["gpt-4", "gpt-3"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Defines a request parameter that is configured to generate a `NewType` type in
        Python and is used in a union type alongside an enum.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/body_params/unions/param_union_enum_new_type",
            body=await async_maybe_transform(
                {"model": model}, union_param_union_enum_new_type_params.UnionParamUnionEnumNewTypeParams
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


class UnionsResourceWithRawResponse:
    def __init__(self, unions: UnionsResource) -> None:
        self._unions = unions

        self.param_union_enum_new_type = _legacy_response.to_raw_response_wrapper(
            unions.param_union_enum_new_type,
        )


class AsyncUnionsResourceWithRawResponse:
    def __init__(self, unions: AsyncUnionsResource) -> None:
        self._unions = unions

        self.param_union_enum_new_type = _legacy_response.async_to_raw_response_wrapper(
            unions.param_union_enum_new_type,
        )


class UnionsResourceWithStreamingResponse:
    def __init__(self, unions: UnionsResource) -> None:
        self._unions = unions

        self.param_union_enum_new_type = to_streamed_response_wrapper(
            unions.param_union_enum_new_type,
        )


class AsyncUnionsResourceWithStreamingResponse:
    def __init__(self, unions: AsyncUnionsResource) -> None:
        self._unions = unions

        self.param_union_enum_new_type = async_to_streamed_response_wrapper(
            unions.param_union_enum_new_type,
        )
