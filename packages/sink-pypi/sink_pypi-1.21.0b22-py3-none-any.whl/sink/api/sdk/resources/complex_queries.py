# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union
from typing_extensions import Literal

import httpx

from .. import _legacy_response
from ..types import (
    complex_query_array_query_params,
    complex_query_union_query_params,
    complex_query_object_query_params,
)
from .._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from .._base_client import make_request_options
from ..types.complex_query_array_query_response import ComplexQueryArrayQueryResponse
from ..types.complex_query_union_query_response import ComplexQueryUnionQueryResponse
from ..types.complex_query_object_query_response import ComplexQueryObjectQueryResponse

__all__ = ["ComplexQueriesResource", "AsyncComplexQueriesResource"]


class ComplexQueriesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ComplexQueriesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return ComplexQueriesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ComplexQueriesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return ComplexQueriesResourceWithStreamingResponse(self)

    def array_query(
        self,
        *,
        include: List[Literal["users", "users.comments", "users.posts"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ComplexQueryArrayQueryResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/array_query",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"include": include}, complex_query_array_query_params.ComplexQueryArrayQueryParams
                ),
            ),
            cast_to=ComplexQueryArrayQueryResponse,
        )

    def object_query(
        self,
        *,
        include: Dict[str, str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ComplexQueryObjectQueryResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/object_query",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"include": include}, complex_query_object_query_params.ComplexQueryObjectQueryParams
                ),
            ),
            cast_to=ComplexQueryObjectQueryResponse,
        )

    def union_query(
        self,
        *,
        include: Union[str, float, SequenceNotStr[str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ComplexQueryUnionQueryResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/union_query",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"include": include}, complex_query_union_query_params.ComplexQueryUnionQueryParams
                ),
            ),
            cast_to=ComplexQueryUnionQueryResponse,
        )


class AsyncComplexQueriesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncComplexQueriesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncComplexQueriesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncComplexQueriesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncComplexQueriesResourceWithStreamingResponse(self)

    async def array_query(
        self,
        *,
        include: List[Literal["users", "users.comments", "users.posts"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ComplexQueryArrayQueryResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/array_query",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"include": include}, complex_query_array_query_params.ComplexQueryArrayQueryParams
                ),
            ),
            cast_to=ComplexQueryArrayQueryResponse,
        )

    async def object_query(
        self,
        *,
        include: Dict[str, str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ComplexQueryObjectQueryResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/object_query",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"include": include}, complex_query_object_query_params.ComplexQueryObjectQueryParams
                ),
            ),
            cast_to=ComplexQueryObjectQueryResponse,
        )

    async def union_query(
        self,
        *,
        include: Union[str, float, SequenceNotStr[str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ComplexQueryUnionQueryResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/union_query",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"include": include}, complex_query_union_query_params.ComplexQueryUnionQueryParams
                ),
            ),
            cast_to=ComplexQueryUnionQueryResponse,
        )


class ComplexQueriesResourceWithRawResponse:
    def __init__(self, complex_queries: ComplexQueriesResource) -> None:
        self._complex_queries = complex_queries

        self.array_query = _legacy_response.to_raw_response_wrapper(
            complex_queries.array_query,
        )
        self.object_query = _legacy_response.to_raw_response_wrapper(
            complex_queries.object_query,
        )
        self.union_query = _legacy_response.to_raw_response_wrapper(
            complex_queries.union_query,
        )


class AsyncComplexQueriesResourceWithRawResponse:
    def __init__(self, complex_queries: AsyncComplexQueriesResource) -> None:
        self._complex_queries = complex_queries

        self.array_query = _legacy_response.async_to_raw_response_wrapper(
            complex_queries.array_query,
        )
        self.object_query = _legacy_response.async_to_raw_response_wrapper(
            complex_queries.object_query,
        )
        self.union_query = _legacy_response.async_to_raw_response_wrapper(
            complex_queries.union_query,
        )


class ComplexQueriesResourceWithStreamingResponse:
    def __init__(self, complex_queries: ComplexQueriesResource) -> None:
        self._complex_queries = complex_queries

        self.array_query = to_streamed_response_wrapper(
            complex_queries.array_query,
        )
        self.object_query = to_streamed_response_wrapper(
            complex_queries.object_query,
        )
        self.union_query = to_streamed_response_wrapper(
            complex_queries.union_query,
        )


class AsyncComplexQueriesResourceWithStreamingResponse:
    def __init__(self, complex_queries: AsyncComplexQueriesResource) -> None:
        self._complex_queries = complex_queries

        self.array_query = async_to_streamed_response_wrapper(
            complex_queries.array_query,
        )
        self.object_query = async_to_streamed_response_wrapper(
            complex_queries.object_query,
        )
        self.union_query = async_to_streamed_response_wrapper(
            complex_queries.union_query,
        )
