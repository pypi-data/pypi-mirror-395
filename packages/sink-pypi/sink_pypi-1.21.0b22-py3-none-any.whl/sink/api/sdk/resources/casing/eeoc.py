# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ... import _legacy_response
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ...pagination import SyncPageCursor, AsyncPageCursor
from ..._base_client import AsyncPaginator, make_request_options
from ...types.casing import eeoc_list_params
from ...types.casing.eeoc import EEOC

__all__ = ["EEOCResource", "AsyncEEOCResource"]


class EEOCResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EEOCResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return EEOCResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EEOCResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return EEOCResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        cursor: str | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[EEOC]:
        """
        Test case for paginated initialism model

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/casing/eeoc",
            page=SyncPageCursor[EEOC],
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
                    eeoc_list_params.EEOCListParams,
                ),
            ),
            model=EEOC,
        )


class AsyncEEOCResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEEOCResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncEEOCResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEEOCResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncEEOCResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        cursor: str | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[EEOC, AsyncPageCursor[EEOC]]:
        """
        Test case for paginated initialism model

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/casing/eeoc",
            page=AsyncPageCursor[EEOC],
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
                    eeoc_list_params.EEOCListParams,
                ),
            ),
            model=EEOC,
        )


class EEOCResourceWithRawResponse:
    def __init__(self, eeoc: EEOCResource) -> None:
        self._eeoc = eeoc

        self.list = _legacy_response.to_raw_response_wrapper(
            eeoc.list,
        )


class AsyncEEOCResourceWithRawResponse:
    def __init__(self, eeoc: AsyncEEOCResource) -> None:
        self._eeoc = eeoc

        self.list = _legacy_response.async_to_raw_response_wrapper(
            eeoc.list,
        )


class EEOCResourceWithStreamingResponse:
    def __init__(self, eeoc: EEOCResource) -> None:
        self._eeoc = eeoc

        self.list = to_streamed_response_wrapper(
            eeoc.list,
        )


class AsyncEEOCResourceWithStreamingResponse:
    def __init__(self, eeoc: AsyncEEOCResource) -> None:
        self._eeoc = eeoc

        self.list = async_to_streamed_response_wrapper(
            eeoc.list,
        )
