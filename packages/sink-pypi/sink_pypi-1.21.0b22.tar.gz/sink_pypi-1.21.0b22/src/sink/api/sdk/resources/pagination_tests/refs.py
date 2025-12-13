# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ... import _legacy_response
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ...pagination import (
    SyncPageCursorSharedRef,
    AsyncPageCursorSharedRef,
    SyncPageCursorNestedObjectRef,
    AsyncPageCursorNestedObjectRef,
)
from ..._base_client import AsyncPaginator, make_request_options
from ...types.my_model import MyModel
from ...types.pagination_tests import ref_nested_object_ref_params, ref_with_shared_model_ref_params

__all__ = ["RefsResource", "AsyncRefsResource"]


class RefsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RefsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return RefsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RefsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return RefsResourceWithStreamingResponse(self)

    def nested_object_ref(
        self,
        *,
        cursor: Optional[str] | Omit = omit,
        limit: int | Omit = omit,
        object_param: ref_nested_object_ref_params.ObjectParam | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursorNestedObjectRef[MyModel]:
        """
        Test case for pagination using an in-line nested object reference

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/nested_object_ref",
            page=SyncPageCursorNestedObjectRef[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "limit": limit,
                        "object_param": object_param,
                    },
                    ref_nested_object_ref_params.RefNestedObjectRefParams,
                ),
            ),
            model=MyModel,
        )

    def with_shared_model_ref(
        self,
        *,
        cursor: Optional[str] | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursorSharedRef[MyModel]:
        """
        Test case for pagination using a shared model reference

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/with_shared_model_ref",
            page=SyncPageCursorSharedRef[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "limit": limit,
                    },
                    ref_with_shared_model_ref_params.RefWithSharedModelRefParams,
                ),
            ),
            model=MyModel,
        )


class AsyncRefsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRefsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncRefsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRefsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncRefsResourceWithStreamingResponse(self)

    def nested_object_ref(
        self,
        *,
        cursor: Optional[str] | Omit = omit,
        limit: int | Omit = omit,
        object_param: ref_nested_object_ref_params.ObjectParam | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[MyModel, AsyncPageCursorNestedObjectRef[MyModel]]:
        """
        Test case for pagination using an in-line nested object reference

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/nested_object_ref",
            page=AsyncPageCursorNestedObjectRef[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "limit": limit,
                        "object_param": object_param,
                    },
                    ref_nested_object_ref_params.RefNestedObjectRefParams,
                ),
            ),
            model=MyModel,
        )

    def with_shared_model_ref(
        self,
        *,
        cursor: Optional[str] | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[MyModel, AsyncPageCursorSharedRef[MyModel]]:
        """
        Test case for pagination using a shared model reference

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/with_shared_model_ref",
            page=AsyncPageCursorSharedRef[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "limit": limit,
                    },
                    ref_with_shared_model_ref_params.RefWithSharedModelRefParams,
                ),
            ),
            model=MyModel,
        )


class RefsResourceWithRawResponse:
    def __init__(self, refs: RefsResource) -> None:
        self._refs = refs

        self.nested_object_ref = _legacy_response.to_raw_response_wrapper(
            refs.nested_object_ref,
        )
        self.with_shared_model_ref = _legacy_response.to_raw_response_wrapper(
            refs.with_shared_model_ref,
        )


class AsyncRefsResourceWithRawResponse:
    def __init__(self, refs: AsyncRefsResource) -> None:
        self._refs = refs

        self.nested_object_ref = _legacy_response.async_to_raw_response_wrapper(
            refs.nested_object_ref,
        )
        self.with_shared_model_ref = _legacy_response.async_to_raw_response_wrapper(
            refs.with_shared_model_ref,
        )


class RefsResourceWithStreamingResponse:
    def __init__(self, refs: RefsResource) -> None:
        self._refs = refs

        self.nested_object_ref = to_streamed_response_wrapper(
            refs.nested_object_ref,
        )
        self.with_shared_model_ref = to_streamed_response_wrapper(
            refs.with_shared_model_ref,
        )


class AsyncRefsResourceWithStreamingResponse:
    def __init__(self, refs: AsyncRefsResource) -> None:
        self._refs = refs

        self.nested_object_ref = async_to_streamed_response_wrapper(
            refs.nested_object_ref,
        )
        self.with_shared_model_ref = async_to_streamed_response_wrapper(
            refs.with_shared_model_ref,
        )
