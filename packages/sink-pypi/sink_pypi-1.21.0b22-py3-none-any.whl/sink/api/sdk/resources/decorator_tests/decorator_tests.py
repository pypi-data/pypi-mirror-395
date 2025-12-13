# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ... import _legacy_response
from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._compat import cached_property
from .languages import (
    LanguagesResource,
    AsyncLanguagesResource,
    LanguagesResourceWithRawResponse,
    AsyncLanguagesResourceWithRawResponse,
    LanguagesResourceWithStreamingResponse,
    AsyncLanguagesResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ..._base_client import make_request_options
from .keep_this_resource import (
    KeepThisResourceResource,
    AsyncKeepThisResourceResource,
    KeepThisResourceResourceWithRawResponse,
    AsyncKeepThisResourceResourceWithRawResponse,
    KeepThisResourceResourceWithStreamingResponse,
    AsyncKeepThisResourceResourceWithStreamingResponse,
)
from .skip_this_resource import (
    SkipThisResourceResource,
    AsyncSkipThisResourceResource,
    SkipThisResourceResourceWithRawResponse,
    AsyncSkipThisResourceResourceWithRawResponse,
    SkipThisResourceResourceWithStreamingResponse,
    AsyncSkipThisResourceResourceWithStreamingResponse,
)
from ...types.decorator_test_keep_me_response import DecoratorTestKeepMeResponse

__all__ = ["DecoratorTestsResource", "AsyncDecoratorTestsResource"]


class DecoratorTestsResource(SyncAPIResource):
    @cached_property
    def languages(self) -> LanguagesResource:
        return LanguagesResource(self._client)

    @cached_property
    def keep_this_resource(self) -> KeepThisResourceResource:
        return KeepThisResourceResource(self._client)

    @cached_property
    def skip_this_resource(self) -> SkipThisResourceResource:
        return SkipThisResourceResource(self._client)

    @cached_property
    def with_raw_response(self) -> DecoratorTestsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return DecoratorTestsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DecoratorTestsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return DecoratorTestsResourceWithStreamingResponse(self)

    def keep_me(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DecoratorTestKeepMeResponse:
        """Top-level method that should not be skipped."""
        return self._get(
            "/decorator_tests/keep/me",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DecoratorTestKeepMeResponse,
        )


class AsyncDecoratorTestsResource(AsyncAPIResource):
    @cached_property
    def languages(self) -> AsyncLanguagesResource:
        return AsyncLanguagesResource(self._client)

    @cached_property
    def keep_this_resource(self) -> AsyncKeepThisResourceResource:
        return AsyncKeepThisResourceResource(self._client)

    @cached_property
    def skip_this_resource(self) -> AsyncSkipThisResourceResource:
        return AsyncSkipThisResourceResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDecoratorTestsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncDecoratorTestsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDecoratorTestsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncDecoratorTestsResourceWithStreamingResponse(self)

    async def keep_me(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DecoratorTestKeepMeResponse:
        """Top-level method that should not be skipped."""
        return await self._get(
            "/decorator_tests/keep/me",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DecoratorTestKeepMeResponse,
        )


class DecoratorTestsResourceWithRawResponse:
    def __init__(self, decorator_tests: DecoratorTestsResource) -> None:
        self._decorator_tests = decorator_tests

        self.keep_me = _legacy_response.to_raw_response_wrapper(
            decorator_tests.keep_me,
        )

    @cached_property
    def languages(self) -> LanguagesResourceWithRawResponse:
        return LanguagesResourceWithRawResponse(self._decorator_tests.languages)

    @cached_property
    def keep_this_resource(self) -> KeepThisResourceResourceWithRawResponse:
        return KeepThisResourceResourceWithRawResponse(self._decorator_tests.keep_this_resource)

    @cached_property
    def skip_this_resource(self) -> SkipThisResourceResourceWithRawResponse:
        return SkipThisResourceResourceWithRawResponse(self._decorator_tests.skip_this_resource)


class AsyncDecoratorTestsResourceWithRawResponse:
    def __init__(self, decorator_tests: AsyncDecoratorTestsResource) -> None:
        self._decorator_tests = decorator_tests

        self.keep_me = _legacy_response.async_to_raw_response_wrapper(
            decorator_tests.keep_me,
        )

    @cached_property
    def languages(self) -> AsyncLanguagesResourceWithRawResponse:
        return AsyncLanguagesResourceWithRawResponse(self._decorator_tests.languages)

    @cached_property
    def keep_this_resource(self) -> AsyncKeepThisResourceResourceWithRawResponse:
        return AsyncKeepThisResourceResourceWithRawResponse(self._decorator_tests.keep_this_resource)

    @cached_property
    def skip_this_resource(self) -> AsyncSkipThisResourceResourceWithRawResponse:
        return AsyncSkipThisResourceResourceWithRawResponse(self._decorator_tests.skip_this_resource)


class DecoratorTestsResourceWithStreamingResponse:
    def __init__(self, decorator_tests: DecoratorTestsResource) -> None:
        self._decorator_tests = decorator_tests

        self.keep_me = to_streamed_response_wrapper(
            decorator_tests.keep_me,
        )

    @cached_property
    def languages(self) -> LanguagesResourceWithStreamingResponse:
        return LanguagesResourceWithStreamingResponse(self._decorator_tests.languages)

    @cached_property
    def keep_this_resource(self) -> KeepThisResourceResourceWithStreamingResponse:
        return KeepThisResourceResourceWithStreamingResponse(self._decorator_tests.keep_this_resource)

    @cached_property
    def skip_this_resource(self) -> SkipThisResourceResourceWithStreamingResponse:
        return SkipThisResourceResourceWithStreamingResponse(self._decorator_tests.skip_this_resource)


class AsyncDecoratorTestsResourceWithStreamingResponse:
    def __init__(self, decorator_tests: AsyncDecoratorTestsResource) -> None:
        self._decorator_tests = decorator_tests

        self.keep_me = async_to_streamed_response_wrapper(
            decorator_tests.keep_me,
        )

    @cached_property
    def languages(self) -> AsyncLanguagesResourceWithStreamingResponse:
        return AsyncLanguagesResourceWithStreamingResponse(self._decorator_tests.languages)

    @cached_property
    def keep_this_resource(self) -> AsyncKeepThisResourceResourceWithStreamingResponse:
        return AsyncKeepThisResourceResourceWithStreamingResponse(self._decorator_tests.keep_this_resource)

    @cached_property
    def skip_this_resource(self) -> AsyncSkipThisResourceResourceWithStreamingResponse:
        return AsyncSkipThisResourceResourceWithStreamingResponse(self._decorator_tests.skip_this_resource)
