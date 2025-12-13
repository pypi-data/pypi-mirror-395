# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ... import _legacy_response
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ...pagination import (
    SyncPageOffset,
    AsyncPageOffset,
    SyncPageOffsetTotalCount,
    AsyncPageOffsetTotalCount,
    SyncPageOffsetNoStartField,
    AsyncPageOffsetNoStartField,
)
from ..._base_client import AsyncPaginator, make_request_options
from ...types.my_model import MyModel
from ...types.pagination_tests import (
    offset_list_params,
    offset_with_total_count_params,
    offset_list_no_start_field_params,
)

__all__ = ["OffsetResource", "AsyncOffsetResource"]


class OffsetResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> OffsetResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return OffsetResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OffsetResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return OffsetResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageOffset[MyModel]:
        """
        Test case for offset pagination

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/offset",
            page=SyncPageOffset[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                    },
                    offset_list_params.OffsetListParams,
                ),
            ),
            model=MyModel,
        )

    def list_no_start_field(
        self,
        *,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageOffsetNoStartField[MyModel]:
        """
        Test case for offset pagination with no start response field

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/offset/no_start_field",
            page=SyncPageOffsetNoStartField[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                    },
                    offset_list_no_start_field_params.OffsetListNoStartFieldParams,
                ),
            ),
            model=MyModel,
        )

    def with_total_count(
        self,
        *,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageOffsetTotalCount[MyModel]:
        """
        Test case for offset pagination with a total count response property

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/offset/with_total_count",
            page=SyncPageOffsetTotalCount[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                    },
                    offset_with_total_count_params.OffsetWithTotalCountParams,
                ),
            ),
            model=MyModel,
        )


class AsyncOffsetResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncOffsetResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncOffsetResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOffsetResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncOffsetResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[MyModel, AsyncPageOffset[MyModel]]:
        """
        Test case for offset pagination

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/offset",
            page=AsyncPageOffset[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                    },
                    offset_list_params.OffsetListParams,
                ),
            ),
            model=MyModel,
        )

    def list_no_start_field(
        self,
        *,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[MyModel, AsyncPageOffsetNoStartField[MyModel]]:
        """
        Test case for offset pagination with no start response field

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/offset/no_start_field",
            page=AsyncPageOffsetNoStartField[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                    },
                    offset_list_no_start_field_params.OffsetListNoStartFieldParams,
                ),
            ),
            model=MyModel,
        )

    def with_total_count(
        self,
        *,
        limit: int | Omit = omit,
        offset: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[MyModel, AsyncPageOffsetTotalCount[MyModel]]:
        """
        Test case for offset pagination with a total count response property

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/offset/with_total_count",
            page=AsyncPageOffsetTotalCount[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                    },
                    offset_with_total_count_params.OffsetWithTotalCountParams,
                ),
            ),
            model=MyModel,
        )


class OffsetResourceWithRawResponse:
    def __init__(self, offset: OffsetResource) -> None:
        self._offset = offset

        self.list = _legacy_response.to_raw_response_wrapper(
            offset.list,
        )
        self.list_no_start_field = _legacy_response.to_raw_response_wrapper(
            offset.list_no_start_field,
        )
        self.with_total_count = _legacy_response.to_raw_response_wrapper(
            offset.with_total_count,
        )


class AsyncOffsetResourceWithRawResponse:
    def __init__(self, offset: AsyncOffsetResource) -> None:
        self._offset = offset

        self.list = _legacy_response.async_to_raw_response_wrapper(
            offset.list,
        )
        self.list_no_start_field = _legacy_response.async_to_raw_response_wrapper(
            offset.list_no_start_field,
        )
        self.with_total_count = _legacy_response.async_to_raw_response_wrapper(
            offset.with_total_count,
        )


class OffsetResourceWithStreamingResponse:
    def __init__(self, offset: OffsetResource) -> None:
        self._offset = offset

        self.list = to_streamed_response_wrapper(
            offset.list,
        )
        self.list_no_start_field = to_streamed_response_wrapper(
            offset.list_no_start_field,
        )
        self.with_total_count = to_streamed_response_wrapper(
            offset.with_total_count,
        )


class AsyncOffsetResourceWithStreamingResponse:
    def __init__(self, offset: AsyncOffsetResource) -> None:
        self._offset = offset

        self.list = async_to_streamed_response_wrapper(
            offset.list,
        )
        self.list_no_start_field = async_to_streamed_response_wrapper(
            offset.list_no_start_field,
        )
        self.with_total_count = async_to_streamed_response_wrapper(
            offset.with_total_count,
        )
