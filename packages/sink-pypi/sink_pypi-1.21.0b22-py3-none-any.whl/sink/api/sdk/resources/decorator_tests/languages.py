# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ... import _legacy_response
from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ..._base_client import make_request_options
from ...types.shared.simple_object import SimpleObject

__all__ = ["LanguagesResource", "AsyncLanguagesResource"]


class LanguagesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> LanguagesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return LanguagesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> LanguagesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return LanguagesResourceWithStreamingResponse(self)

    def skipped_for_node(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SimpleObject:
        """Endpoint that returns a $ref to SimpleObject.

        This is used to test shared
        response models.
        """
        return self._get(
            "/responses/shared_simple_object",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SimpleObject,
        )


class AsyncLanguagesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncLanguagesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncLanguagesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncLanguagesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncLanguagesResourceWithStreamingResponse(self)

    async def skipped_for_node(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SimpleObject:
        """Endpoint that returns a $ref to SimpleObject.

        This is used to test shared
        response models.
        """
        return await self._get(
            "/responses/shared_simple_object",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SimpleObject,
        )


class LanguagesResourceWithRawResponse:
    def __init__(self, languages: LanguagesResource) -> None:
        self._languages = languages

        self.skipped_for_node = _legacy_response.to_raw_response_wrapper(
            languages.skipped_for_node,
        )


class AsyncLanguagesResourceWithRawResponse:
    def __init__(self, languages: AsyncLanguagesResource) -> None:
        self._languages = languages

        self.skipped_for_node = _legacy_response.async_to_raw_response_wrapper(
            languages.skipped_for_node,
        )


class LanguagesResourceWithStreamingResponse:
    def __init__(self, languages: LanguagesResource) -> None:
        self._languages = languages

        self.skipped_for_node = to_streamed_response_wrapper(
            languages.skipped_for_node,
        )


class AsyncLanguagesResourceWithStreamingResponse:
    def __init__(self, languages: AsyncLanguagesResource) -> None:
        self._languages = languages

        self.skipped_for_node = async_to_streamed_response_wrapper(
            languages.skipped_for_node,
        )
