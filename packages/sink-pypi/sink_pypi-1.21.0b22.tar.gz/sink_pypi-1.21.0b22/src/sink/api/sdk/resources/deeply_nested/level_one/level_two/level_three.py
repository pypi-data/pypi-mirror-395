# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..... import _legacy_response
from ....._types import Body, Query, Headers, NotGiven, not_given
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from .....types.card import Card
from ....._base_client import make_request_options

__all__ = ["LevelThreeResource", "AsyncLevelThreeResource"]


class LevelThreeResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> LevelThreeResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return LevelThreeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> LevelThreeResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return LevelThreeResourceWithStreamingResponse(self)

    def method_level_3(
        self,
        card_token: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Card:
        """
        Get card configuration such as spend limit and state.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not card_token:
            raise ValueError(f"Expected a non-empty value for `card_token` but received {card_token!r}")
        return self._get(
            f"/cards/{card_token}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Card,
        )


class AsyncLevelThreeResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncLevelThreeResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncLevelThreeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncLevelThreeResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncLevelThreeResourceWithStreamingResponse(self)

    async def method_level_3(
        self,
        card_token: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Card:
        """
        Get card configuration such as spend limit and state.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not card_token:
            raise ValueError(f"Expected a non-empty value for `card_token` but received {card_token!r}")
        return await self._get(
            f"/cards/{card_token}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Card,
        )


class LevelThreeResourceWithRawResponse:
    def __init__(self, level_three: LevelThreeResource) -> None:
        self._level_three = level_three

        self.method_level_3 = _legacy_response.to_raw_response_wrapper(
            level_three.method_level_3,
        )


class AsyncLevelThreeResourceWithRawResponse:
    def __init__(self, level_three: AsyncLevelThreeResource) -> None:
        self._level_three = level_three

        self.method_level_3 = _legacy_response.async_to_raw_response_wrapper(
            level_three.method_level_3,
        )


class LevelThreeResourceWithStreamingResponse:
    def __init__(self, level_three: LevelThreeResource) -> None:
        self._level_three = level_three

        self.method_level_3 = to_streamed_response_wrapper(
            level_three.method_level_3,
        )


class AsyncLevelThreeResourceWithStreamingResponse:
    def __init__(self, level_three: AsyncLevelThreeResource) -> None:
        self._level_three = level_three

        self.method_level_3 = async_to_streamed_response_wrapper(
            level_three.method_level_3,
        )
