# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .shared_responses import (
    SharedResponsesResource,
    AsyncSharedResponsesResource,
    SharedResponsesResourceWithRawResponse,
    AsyncSharedResponsesResourceWithRawResponse,
    SharedResponsesResourceWithStreamingResponse,
    AsyncSharedResponsesResourceWithStreamingResponse,
)

__all__ = ["RecursionResource", "AsyncRecursionResource"]


class RecursionResource(SyncAPIResource):
    @cached_property
    def shared_responses(self) -> SharedResponsesResource:
        return SharedResponsesResource(self._client)

    @cached_property
    def with_raw_response(self) -> RecursionResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return RecursionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RecursionResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return RecursionResourceWithStreamingResponse(self)


class AsyncRecursionResource(AsyncAPIResource):
    @cached_property
    def shared_responses(self) -> AsyncSharedResponsesResource:
        return AsyncSharedResponsesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncRecursionResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncRecursionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRecursionResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncRecursionResourceWithStreamingResponse(self)


class RecursionResourceWithRawResponse:
    def __init__(self, recursion: RecursionResource) -> None:
        self._recursion = recursion

    @cached_property
    def shared_responses(self) -> SharedResponsesResourceWithRawResponse:
        return SharedResponsesResourceWithRawResponse(self._recursion.shared_responses)


class AsyncRecursionResourceWithRawResponse:
    def __init__(self, recursion: AsyncRecursionResource) -> None:
        self._recursion = recursion

    @cached_property
    def shared_responses(self) -> AsyncSharedResponsesResourceWithRawResponse:
        return AsyncSharedResponsesResourceWithRawResponse(self._recursion.shared_responses)


class RecursionResourceWithStreamingResponse:
    def __init__(self, recursion: RecursionResource) -> None:
        self._recursion = recursion

    @cached_property
    def shared_responses(self) -> SharedResponsesResourceWithStreamingResponse:
        return SharedResponsesResourceWithStreamingResponse(self._recursion.shared_responses)


class AsyncRecursionResourceWithStreamingResponse:
    def __init__(self, recursion: AsyncRecursionResource) -> None:
        self._recursion = recursion

    @cached_property
    def shared_responses(self) -> AsyncSharedResponsesResourceWithStreamingResponse:
        return AsyncSharedResponsesResourceWithStreamingResponse(self._recursion.shared_responses)
