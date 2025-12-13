# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .. import _legacy_response
from ..types import shared_query_param_delete_params, shared_query_param_retrieve_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from .._base_client import make_request_options

__all__ = ["SharedQueryParamsResource", "AsyncSharedQueryParamsResource"]


class SharedQueryParamsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SharedQueryParamsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return SharedQueryParamsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SharedQueryParamsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return SharedQueryParamsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        get1: str | Omit = omit,
        shared1: str | Omit = omit,
        shared2: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> str:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/shared-query-params",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "get1": get1,
                        "shared1": shared1,
                        "shared2": shared2,
                    },
                    shared_query_param_retrieve_params.SharedQueryParamRetrieveParams,
                ),
            ),
            cast_to=str,
        )

    def delete(
        self,
        *,
        get1: str | Omit = omit,
        shared1: str | Omit = omit,
        shared2: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> str:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._delete(
            "/shared-query-params",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
                query=maybe_transform(
                    {
                        "get1": get1,
                        "shared1": shared1,
                        "shared2": shared2,
                    },
                    shared_query_param_delete_params.SharedQueryParamDeleteParams,
                ),
            ),
            cast_to=str,
        )


class AsyncSharedQueryParamsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSharedQueryParamsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncSharedQueryParamsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSharedQueryParamsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncSharedQueryParamsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        get1: str | Omit = omit,
        shared1: str | Omit = omit,
        shared2: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> str:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/shared-query-params",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "get1": get1,
                        "shared1": shared1,
                        "shared2": shared2,
                    },
                    shared_query_param_retrieve_params.SharedQueryParamRetrieveParams,
                ),
            ),
            cast_to=str,
        )

    async def delete(
        self,
        *,
        get1: str | Omit = omit,
        shared1: str | Omit = omit,
        shared2: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> str:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._delete(
            "/shared-query-params",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
                query=await async_maybe_transform(
                    {
                        "get1": get1,
                        "shared1": shared1,
                        "shared2": shared2,
                    },
                    shared_query_param_delete_params.SharedQueryParamDeleteParams,
                ),
            ),
            cast_to=str,
        )


class SharedQueryParamsResourceWithRawResponse:
    def __init__(self, shared_query_params: SharedQueryParamsResource) -> None:
        self._shared_query_params = shared_query_params

        self.retrieve = _legacy_response.to_raw_response_wrapper(
            shared_query_params.retrieve,
        )
        self.delete = _legacy_response.to_raw_response_wrapper(
            shared_query_params.delete,
        )


class AsyncSharedQueryParamsResourceWithRawResponse:
    def __init__(self, shared_query_params: AsyncSharedQueryParamsResource) -> None:
        self._shared_query_params = shared_query_params

        self.retrieve = _legacy_response.async_to_raw_response_wrapper(
            shared_query_params.retrieve,
        )
        self.delete = _legacy_response.async_to_raw_response_wrapper(
            shared_query_params.delete,
        )


class SharedQueryParamsResourceWithStreamingResponse:
    def __init__(self, shared_query_params: SharedQueryParamsResource) -> None:
        self._shared_query_params = shared_query_params

        self.retrieve = to_streamed_response_wrapper(
            shared_query_params.retrieve,
        )
        self.delete = to_streamed_response_wrapper(
            shared_query_params.delete,
        )


class AsyncSharedQueryParamsResourceWithStreamingResponse:
    def __init__(self, shared_query_params: AsyncSharedQueryParamsResource) -> None:
        self._shared_query_params = shared_query_params

        self.retrieve = async_to_streamed_response_wrapper(
            shared_query_params.retrieve,
        )
        self.delete = async_to_streamed_response_wrapper(
            shared_query_params.delete,
        )
