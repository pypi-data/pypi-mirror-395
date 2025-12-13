# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .. import _legacy_response
from .._types import Body, Query, Headers, NotGiven, not_given
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from .._base_client import make_request_options
from ..types.root_response import RootResponse

__all__ = ["TestingResource", "AsyncTestingResource"]


class TestingResource(SyncAPIResource):
    __test__ = False

    @cached_property
    def with_raw_response(self) -> TestingResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return TestingResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TestingResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return TestingResourceWithStreamingResponse(self)

    def root(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RootResponse:
        return self._get(
            "/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RootResponse,
        )


class AsyncTestingResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTestingResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncTestingResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTestingResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncTestingResourceWithStreamingResponse(self)

    async def root(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RootResponse:
        return await self._get(
            "/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RootResponse,
        )


class TestingResourceWithRawResponse:
    __test__ = False

    def __init__(self, testing: TestingResource) -> None:
        self._testing = testing

        self.root = _legacy_response.to_raw_response_wrapper(
            testing.root,
        )


class AsyncTestingResourceWithRawResponse:
    def __init__(self, testing: AsyncTestingResource) -> None:
        self._testing = testing

        self.root = _legacy_response.async_to_raw_response_wrapper(
            testing.root,
        )


class TestingResourceWithStreamingResponse:
    __test__ = False

    def __init__(self, testing: TestingResource) -> None:
        self._testing = testing

        self.root = to_streamed_response_wrapper(
            testing.root,
        )


class AsyncTestingResourceWithStreamingResponse:
    def __init__(self, testing: AsyncTestingResource) -> None:
        self._testing = testing

        self.root = async_to_streamed_response_wrapper(
            testing.root,
        )
