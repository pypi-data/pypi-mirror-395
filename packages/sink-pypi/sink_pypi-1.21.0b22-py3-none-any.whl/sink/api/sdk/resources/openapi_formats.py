# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from .. import _legacy_response
from ..types import openapi_format_array_type_one_entry_params, openapi_format_array_type_one_entry_with_null_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from .._base_client import make_request_options
from ..types.openapi_format_array_type_one_entry_response import OpenAPIFormatArrayTypeOneEntryResponse
from ..types.openapi_format_array_type_one_entry_with_null_response import (
    OpenAPIFormatArrayTypeOneEntryWithNullResponse,
)

__all__ = ["OpenAPIFormatsResource", "AsyncOpenAPIFormatsResource"]


class OpenAPIFormatsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> OpenAPIFormatsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return OpenAPIFormatsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OpenAPIFormatsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return OpenAPIFormatsResourceWithStreamingResponse(self)

    def array_type_one_entry(
        self,
        *,
        enable_debug_logging: bool,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> OpenAPIFormatArrayTypeOneEntryResponse:
        """
        See https://linear.app/stainless/issue/STA-569/support-for-type-[object-null]

        Args:
          enable_debug_logging

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/openapi_formats/array_type_one_entry",
            body=maybe_transform(
                {"enable_debug_logging": enable_debug_logging},
                openapi_format_array_type_one_entry_params.OpenAPIFormatArrayTypeOneEntryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=OpenAPIFormatArrayTypeOneEntryResponse,
        )

    def array_type_one_entry_with_null(
        self,
        *,
        enable_debug_logging: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Optional[OpenAPIFormatArrayTypeOneEntryWithNullResponse]:
        """
        The `type` property being set to [T, null] should result in an optional response
        return type in generated SDKs.

        See https://linear.app/stainless/issue/STA-569/support-for-type-[object-null]

        Args:
          enable_debug_logging

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/openapi_formats/array_type_one_entry_with_null",
            body=maybe_transform(
                {"enable_debug_logging": enable_debug_logging},
                openapi_format_array_type_one_entry_with_null_params.OpenAPIFormatArrayTypeOneEntryWithNullParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=OpenAPIFormatArrayTypeOneEntryWithNullResponse,
        )


class AsyncOpenAPIFormatsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncOpenAPIFormatsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncOpenAPIFormatsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOpenAPIFormatsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncOpenAPIFormatsResourceWithStreamingResponse(self)

    async def array_type_one_entry(
        self,
        *,
        enable_debug_logging: bool,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> OpenAPIFormatArrayTypeOneEntryResponse:
        """
        See https://linear.app/stainless/issue/STA-569/support-for-type-[object-null]

        Args:
          enable_debug_logging

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/openapi_formats/array_type_one_entry",
            body=await async_maybe_transform(
                {"enable_debug_logging": enable_debug_logging},
                openapi_format_array_type_one_entry_params.OpenAPIFormatArrayTypeOneEntryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=OpenAPIFormatArrayTypeOneEntryResponse,
        )

    async def array_type_one_entry_with_null(
        self,
        *,
        enable_debug_logging: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Optional[OpenAPIFormatArrayTypeOneEntryWithNullResponse]:
        """
        The `type` property being set to [T, null] should result in an optional response
        return type in generated SDKs.

        See https://linear.app/stainless/issue/STA-569/support-for-type-[object-null]

        Args:
          enable_debug_logging

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/openapi_formats/array_type_one_entry_with_null",
            body=await async_maybe_transform(
                {"enable_debug_logging": enable_debug_logging},
                openapi_format_array_type_one_entry_with_null_params.OpenAPIFormatArrayTypeOneEntryWithNullParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=OpenAPIFormatArrayTypeOneEntryWithNullResponse,
        )


class OpenAPIFormatsResourceWithRawResponse:
    def __init__(self, openapi_formats: OpenAPIFormatsResource) -> None:
        self._openapi_formats = openapi_formats

        self.array_type_one_entry = _legacy_response.to_raw_response_wrapper(
            openapi_formats.array_type_one_entry,
        )
        self.array_type_one_entry_with_null = _legacy_response.to_raw_response_wrapper(
            openapi_formats.array_type_one_entry_with_null,
        )


class AsyncOpenAPIFormatsResourceWithRawResponse:
    def __init__(self, openapi_formats: AsyncOpenAPIFormatsResource) -> None:
        self._openapi_formats = openapi_formats

        self.array_type_one_entry = _legacy_response.async_to_raw_response_wrapper(
            openapi_formats.array_type_one_entry,
        )
        self.array_type_one_entry_with_null = _legacy_response.async_to_raw_response_wrapper(
            openapi_formats.array_type_one_entry_with_null,
        )


class OpenAPIFormatsResourceWithStreamingResponse:
    def __init__(self, openapi_formats: OpenAPIFormatsResource) -> None:
        self._openapi_formats = openapi_formats

        self.array_type_one_entry = to_streamed_response_wrapper(
            openapi_formats.array_type_one_entry,
        )
        self.array_type_one_entry_with_null = to_streamed_response_wrapper(
            openapi_formats.array_type_one_entry_with_null,
        )


class AsyncOpenAPIFormatsResourceWithStreamingResponse:
    def __init__(self, openapi_formats: AsyncOpenAPIFormatsResource) -> None:
        self._openapi_formats = openapi_formats

        self.array_type_one_entry = async_to_streamed_response_wrapper(
            openapi_formats.array_type_one_entry,
        )
        self.array_type_one_entry_with_null = async_to_streamed_response_wrapper(
            openapi_formats.array_type_one_entry_with_null,
        )
