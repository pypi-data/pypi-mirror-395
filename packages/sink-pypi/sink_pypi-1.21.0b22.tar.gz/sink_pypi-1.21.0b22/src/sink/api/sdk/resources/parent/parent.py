# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .child import (
    ChildResource,
    AsyncChildResource,
    ChildResourceWithRawResponse,
    AsyncChildResourceWithRawResponse,
    ChildResourceWithStreamingResponse,
    AsyncChildResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["ParentResource", "AsyncParentResource"]


class ParentResource(SyncAPIResource):
    @cached_property
    def child(self) -> ChildResource:
        """
        Some children can be very large
        For example, the children of Godzilla
        """
        return ChildResource(self._client)

    @cached_property
    def with_raw_response(self) -> ParentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return ParentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ParentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return ParentResourceWithStreamingResponse(self)


class AsyncParentResource(AsyncAPIResource):
    @cached_property
    def child(self) -> AsyncChildResource:
        """
        Some children can be very large
        For example, the children of Godzilla
        """
        return AsyncChildResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncParentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncParentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncParentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncParentResourceWithStreamingResponse(self)


class ParentResourceWithRawResponse:
    def __init__(self, parent: ParentResource) -> None:
        self._parent = parent

    @cached_property
    def child(self) -> ChildResourceWithRawResponse:
        """
        Some children can be very large
        For example, the children of Godzilla
        """
        return ChildResourceWithRawResponse(self._parent.child)


class AsyncParentResourceWithRawResponse:
    def __init__(self, parent: AsyncParentResource) -> None:
        self._parent = parent

    @cached_property
    def child(self) -> AsyncChildResourceWithRawResponse:
        """
        Some children can be very large
        For example, the children of Godzilla
        """
        return AsyncChildResourceWithRawResponse(self._parent.child)


class ParentResourceWithStreamingResponse:
    def __init__(self, parent: ParentResource) -> None:
        self._parent = parent

    @cached_property
    def child(self) -> ChildResourceWithStreamingResponse:
        """
        Some children can be very large
        For example, the children of Godzilla
        """
        return ChildResourceWithStreamingResponse(self._parent.child)


class AsyncParentResourceWithStreamingResponse:
    def __init__(self, parent: AsyncParentResource) -> None:
        self._parent = parent

    @cached_property
    def child(self) -> AsyncChildResourceWithStreamingResponse:
        """
        Some children can be very large
        For example, the children of Godzilla
        """
        return AsyncChildResourceWithStreamingResponse(self._parent.child)
