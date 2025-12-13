# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .... import _legacy_response
from .import_ import (
    ImportResource,
    AsyncImportResource,
    ImportResourceWithRawResponse,
    AsyncImportResourceWithRawResponse,
    ImportResourceWithStreamingResponse,
    AsyncImportResourceWithStreamingResponse,
)
from .methods import (
    MethodsResource,
    AsyncMethodsResource,
    MethodsResourceWithRawResponse,
    AsyncMethodsResourceWithRawResponse,
    MethodsResourceWithStreamingResponse,
    AsyncMethodsResourceWithStreamingResponse,
)
from ...._types import Body, Query, Headers, NoneType, NotGiven, not_given
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from .public.public import (
    PublicResource,
    AsyncPublicResource,
    PublicResourceWithRawResponse,
    AsyncPublicResourceWithRawResponse,
    PublicResourceWithStreamingResponse,
    AsyncPublicResourceWithStreamingResponse,
)
from ....types.names import reserved_name_common_reserved_params_params
from ...._base_client import make_request_options

__all__ = ["ReservedNamesResource", "AsyncReservedNamesResource"]


class ReservedNamesResource(SyncAPIResource):
    @cached_property
    def public(self) -> PublicResource:
        return PublicResource(self._client)

    @cached_property
    def import_(self) -> ImportResource:
        return ImportResource(self._client)

    @cached_property
    def methods(self) -> MethodsResource:
        return MethodsResource(self._client)

    @cached_property
    def with_raw_response(self) -> ReservedNamesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return ReservedNamesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ReservedNamesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return ReservedNamesResourceWithStreamingResponse(self)

    def common_reserved_params(
        self,
        *,
        from_: str,
        api_self: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that has a property name that can conflict with
        language keywords.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/names/reserved_names/common_reserved_params",
            body=maybe_transform(
                {
                    "from_": from_,
                    "api_self": api_self,
                },
                reserved_name_common_reserved_params_params.ReservedNameCommonReservedParamsParams,
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


class AsyncReservedNamesResource(AsyncAPIResource):
    @cached_property
    def public(self) -> AsyncPublicResource:
        return AsyncPublicResource(self._client)

    @cached_property
    def import_(self) -> AsyncImportResource:
        return AsyncImportResource(self._client)

    @cached_property
    def methods(self) -> AsyncMethodsResource:
        return AsyncMethodsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncReservedNamesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncReservedNamesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncReservedNamesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncReservedNamesResourceWithStreamingResponse(self)

    async def common_reserved_params(
        self,
        *,
        from_: str,
        api_self: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that has a property name that can conflict with
        language keywords.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/names/reserved_names/common_reserved_params",
            body=await async_maybe_transform(
                {
                    "from_": from_,
                    "api_self": api_self,
                },
                reserved_name_common_reserved_params_params.ReservedNameCommonReservedParamsParams,
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


class ReservedNamesResourceWithRawResponse:
    def __init__(self, reserved_names: ReservedNamesResource) -> None:
        self._reserved_names = reserved_names

        self.common_reserved_params = _legacy_response.to_raw_response_wrapper(
            reserved_names.common_reserved_params,
        )

    @cached_property
    def public(self) -> PublicResourceWithRawResponse:
        return PublicResourceWithRawResponse(self._reserved_names.public)

    @cached_property
    def import_(self) -> ImportResourceWithRawResponse:
        return ImportResourceWithRawResponse(self._reserved_names.import_)

    @cached_property
    def methods(self) -> MethodsResourceWithRawResponse:
        return MethodsResourceWithRawResponse(self._reserved_names.methods)


class AsyncReservedNamesResourceWithRawResponse:
    def __init__(self, reserved_names: AsyncReservedNamesResource) -> None:
        self._reserved_names = reserved_names

        self.common_reserved_params = _legacy_response.async_to_raw_response_wrapper(
            reserved_names.common_reserved_params,
        )

    @cached_property
    def public(self) -> AsyncPublicResourceWithRawResponse:
        return AsyncPublicResourceWithRawResponse(self._reserved_names.public)

    @cached_property
    def import_(self) -> AsyncImportResourceWithRawResponse:
        return AsyncImportResourceWithRawResponse(self._reserved_names.import_)

    @cached_property
    def methods(self) -> AsyncMethodsResourceWithRawResponse:
        return AsyncMethodsResourceWithRawResponse(self._reserved_names.methods)


class ReservedNamesResourceWithStreamingResponse:
    def __init__(self, reserved_names: ReservedNamesResource) -> None:
        self._reserved_names = reserved_names

        self.common_reserved_params = to_streamed_response_wrapper(
            reserved_names.common_reserved_params,
        )

    @cached_property
    def public(self) -> PublicResourceWithStreamingResponse:
        return PublicResourceWithStreamingResponse(self._reserved_names.public)

    @cached_property
    def import_(self) -> ImportResourceWithStreamingResponse:
        return ImportResourceWithStreamingResponse(self._reserved_names.import_)

    @cached_property
    def methods(self) -> MethodsResourceWithStreamingResponse:
        return MethodsResourceWithStreamingResponse(self._reserved_names.methods)


class AsyncReservedNamesResourceWithStreamingResponse:
    def __init__(self, reserved_names: AsyncReservedNamesResource) -> None:
        self._reserved_names = reserved_names

        self.common_reserved_params = async_to_streamed_response_wrapper(
            reserved_names.common_reserved_params,
        )

    @cached_property
    def public(self) -> AsyncPublicResourceWithStreamingResponse:
        return AsyncPublicResourceWithStreamingResponse(self._reserved_names.public)

    @cached_property
    def import_(self) -> AsyncImportResourceWithStreamingResponse:
        return AsyncImportResourceWithStreamingResponse(self._reserved_names.import_)

    @cached_property
    def methods(self) -> AsyncMethodsResourceWithStreamingResponse:
        return AsyncMethodsResourceWithStreamingResponse(self._reserved_names.methods)
