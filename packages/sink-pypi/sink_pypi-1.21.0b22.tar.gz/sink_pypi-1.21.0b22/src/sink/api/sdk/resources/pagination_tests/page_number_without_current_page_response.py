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
    SyncPagePageNumber,
    AsyncPagePageNumber,
    SyncPagePageNumberWithoutCurrentPageResponse,
    AsyncPagePageNumberWithoutCurrentPageResponse,
)
from ..._base_client import AsyncPaginator, make_request_options
from ...types.my_model import MyModel
from ...types.pagination_tests import (
    page_number_without_current_page_response_list_params,
    page_number_without_current_page_response_list_without_current_page_response_params,
)

__all__ = ["PageNumberWithoutCurrentPageResponseResource", "AsyncPageNumberWithoutCurrentPageResponseResource"]


class PageNumberWithoutCurrentPageResponseResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PageNumberWithoutCurrentPageResponseResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return PageNumberWithoutCurrentPageResponseResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PageNumberWithoutCurrentPageResponseResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return PageNumberWithoutCurrentPageResponseResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        page: int | Omit = omit,
        page_size: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPagePageNumber[MyModel]:
        """
        Test case for page_number pagination

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/page_number",
            page=SyncPagePageNumber[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "page": page,
                        "page_size": page_size,
                    },
                    page_number_without_current_page_response_list_params.PageNumberWithoutCurrentPageResponseListParams,
                ),
            ),
            model=MyModel,
        )

    def list_without_current_page_response(
        self,
        *,
        page: int | Omit = omit,
        page_size: int | Omit = omit,
        prop_to_not_mess_with_infer_for_other_pages: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPagePageNumberWithoutCurrentPageResponse[MyModel]:
        """
        Test case for page_number pagination without a `page` response property

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/page_number_without_current_page_response",
            page=SyncPagePageNumberWithoutCurrentPageResponse[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "page": page,
                        "page_size": page_size,
                        "prop_to_not_mess_with_infer_for_other_pages": prop_to_not_mess_with_infer_for_other_pages,
                    },
                    page_number_without_current_page_response_list_without_current_page_response_params.PageNumberWithoutCurrentPageResponseListWithoutCurrentPageResponseParams,
                ),
            ),
            model=MyModel,
        )


class AsyncPageNumberWithoutCurrentPageResponseResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPageNumberWithoutCurrentPageResponseResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncPageNumberWithoutCurrentPageResponseResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPageNumberWithoutCurrentPageResponseResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncPageNumberWithoutCurrentPageResponseResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        page: int | Omit = omit,
        page_size: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[MyModel, AsyncPagePageNumber[MyModel]]:
        """
        Test case for page_number pagination

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/page_number",
            page=AsyncPagePageNumber[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "page": page,
                        "page_size": page_size,
                    },
                    page_number_without_current_page_response_list_params.PageNumberWithoutCurrentPageResponseListParams,
                ),
            ),
            model=MyModel,
        )

    def list_without_current_page_response(
        self,
        *,
        page: int | Omit = omit,
        page_size: int | Omit = omit,
        prop_to_not_mess_with_infer_for_other_pages: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[MyModel, AsyncPagePageNumberWithoutCurrentPageResponse[MyModel]]:
        """
        Test case for page_number pagination without a `page` response property

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/page_number_without_current_page_response",
            page=AsyncPagePageNumberWithoutCurrentPageResponse[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "page": page,
                        "page_size": page_size,
                        "prop_to_not_mess_with_infer_for_other_pages": prop_to_not_mess_with_infer_for_other_pages,
                    },
                    page_number_without_current_page_response_list_without_current_page_response_params.PageNumberWithoutCurrentPageResponseListWithoutCurrentPageResponseParams,
                ),
            ),
            model=MyModel,
        )


class PageNumberWithoutCurrentPageResponseResourceWithRawResponse:
    def __init__(self, page_number_without_current_page_response: PageNumberWithoutCurrentPageResponseResource) -> None:
        self._page_number_without_current_page_response = page_number_without_current_page_response

        self.list = _legacy_response.to_raw_response_wrapper(
            page_number_without_current_page_response.list,
        )
        self.list_without_current_page_response = _legacy_response.to_raw_response_wrapper(
            page_number_without_current_page_response.list_without_current_page_response,
        )


class AsyncPageNumberWithoutCurrentPageResponseResourceWithRawResponse:
    def __init__(
        self, page_number_without_current_page_response: AsyncPageNumberWithoutCurrentPageResponseResource
    ) -> None:
        self._page_number_without_current_page_response = page_number_without_current_page_response

        self.list = _legacy_response.async_to_raw_response_wrapper(
            page_number_without_current_page_response.list,
        )
        self.list_without_current_page_response = _legacy_response.async_to_raw_response_wrapper(
            page_number_without_current_page_response.list_without_current_page_response,
        )


class PageNumberWithoutCurrentPageResponseResourceWithStreamingResponse:
    def __init__(self, page_number_without_current_page_response: PageNumberWithoutCurrentPageResponseResource) -> None:
        self._page_number_without_current_page_response = page_number_without_current_page_response

        self.list = to_streamed_response_wrapper(
            page_number_without_current_page_response.list,
        )
        self.list_without_current_page_response = to_streamed_response_wrapper(
            page_number_without_current_page_response.list_without_current_page_response,
        )


class AsyncPageNumberWithoutCurrentPageResponseResourceWithStreamingResponse:
    def __init__(
        self, page_number_without_current_page_response: AsyncPageNumberWithoutCurrentPageResponseResource
    ) -> None:
        self._page_number_without_current_page_response = page_number_without_current_page_response

        self.list = async_to_streamed_response_wrapper(
            page_number_without_current_page_response.list,
        )
        self.list_without_current_page_response = async_to_streamed_response_wrapper(
            page_number_without_current_page_response.list_without_current_page_response,
        )
