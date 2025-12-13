# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ... import _legacy_response
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ...pagination import SyncPagePageNumber, AsyncPagePageNumber
from ..._base_client import AsyncPaginator, make_request_options
from ...types.my_model import MyModel
from ...types.pagination_tests import page_number_list_params, page_number_list_without_current_page_response_params

__all__ = ["PageNumberResource", "AsyncPageNumberResource"]


class PageNumberResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PageNumberResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return PageNumberResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PageNumberResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return PageNumberResourceWithStreamingResponse(self)

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
                    page_number_list_params.PageNumberListParams,
                ),
            ),
            model=MyModel,
        )

    def list_without_current_page_response(
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
                    page_number_list_without_current_page_response_params.PageNumberListWithoutCurrentPageResponseParams,
                ),
            ),
            model=MyModel,
        )


class AsyncPageNumberResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPageNumberResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncPageNumberResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPageNumberResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncPageNumberResourceWithStreamingResponse(self)

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
                    page_number_list_params.PageNumberListParams,
                ),
            ),
            model=MyModel,
        )

    def list_without_current_page_response(
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
                    page_number_list_without_current_page_response_params.PageNumberListWithoutCurrentPageResponseParams,
                ),
            ),
            model=MyModel,
        )


class PageNumberResourceWithRawResponse:
    def __init__(self, page_number: PageNumberResource) -> None:
        self._page_number = page_number

        self.list = _legacy_response.to_raw_response_wrapper(
            page_number.list,
        )
        self.list_without_current_page_response = _legacy_response.to_raw_response_wrapper(
            page_number.list_without_current_page_response,
        )


class AsyncPageNumberResourceWithRawResponse:
    def __init__(self, page_number: AsyncPageNumberResource) -> None:
        self._page_number = page_number

        self.list = _legacy_response.async_to_raw_response_wrapper(
            page_number.list,
        )
        self.list_without_current_page_response = _legacy_response.async_to_raw_response_wrapper(
            page_number.list_without_current_page_response,
        )


class PageNumberResourceWithStreamingResponse:
    def __init__(self, page_number: PageNumberResource) -> None:
        self._page_number = page_number

        self.list = to_streamed_response_wrapper(
            page_number.list,
        )
        self.list_without_current_page_response = to_streamed_response_wrapper(
            page_number.list_without_current_page_response,
        )


class AsyncPageNumberResourceWithStreamingResponse:
    def __init__(self, page_number: AsyncPageNumberResource) -> None:
        self._page_number = page_number

        self.list = async_to_streamed_response_wrapper(
            page_number.list,
        )
        self.list_without_current_page_response = async_to_streamed_response_wrapper(
            page_number.list_without_current_page_response,
        )
