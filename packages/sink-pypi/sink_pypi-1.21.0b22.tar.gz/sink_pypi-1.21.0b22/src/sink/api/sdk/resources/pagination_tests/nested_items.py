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
from ...pagination import SyncPageCursorNestedItems, AsyncPageCursorNestedItems
from ..._base_client import AsyncPaginator, make_request_options
from ...types.my_model import MyModel
from ...types.pagination_tests import nested_item_list_params

__all__ = ["NestedItemsResource", "AsyncNestedItemsResource"]


class NestedItemsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> NestedItemsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return NestedItemsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> NestedItemsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return NestedItemsResourceWithStreamingResponse(self)

    def list(
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
    ) -> SyncPageCursorNestedItems[MyModel]:
        """
        Test case for response headers with cursor pagination

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/nested_items",
            page=SyncPageCursorNestedItems[MyModel],
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
                    nested_item_list_params.NestedItemListParams,
                ),
            ),
            model=MyModel,
        )


class AsyncNestedItemsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncNestedItemsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncNestedItemsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncNestedItemsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncNestedItemsResourceWithStreamingResponse(self)

    def list(
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
    ) -> AsyncPaginator[MyModel, AsyncPageCursorNestedItems[MyModel]]:
        """
        Test case for response headers with cursor pagination

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/nested_items",
            page=AsyncPageCursorNestedItems[MyModel],
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
                    nested_item_list_params.NestedItemListParams,
                ),
            ),
            model=MyModel,
        )


class NestedItemsResourceWithRawResponse:
    def __init__(self, nested_items: NestedItemsResource) -> None:
        self._nested_items = nested_items

        self.list = _legacy_response.to_raw_response_wrapper(
            nested_items.list,
        )


class AsyncNestedItemsResourceWithRawResponse:
    def __init__(self, nested_items: AsyncNestedItemsResource) -> None:
        self._nested_items = nested_items

        self.list = _legacy_response.async_to_raw_response_wrapper(
            nested_items.list,
        )


class NestedItemsResourceWithStreamingResponse:
    def __init__(self, nested_items: NestedItemsResource) -> None:
        self._nested_items = nested_items

        self.list = to_streamed_response_wrapper(
            nested_items.list,
        )


class AsyncNestedItemsResourceWithStreamingResponse:
    def __init__(self, nested_items: AsyncNestedItemsResource) -> None:
        self._nested_items = nested_items

        self.list = async_to_streamed_response_wrapper(
            nested_items.list,
        )
