# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .escaped_ref import (
    EscapedRefResource,
    AsyncEscapedRefResource,
    EscapedRefResourceWithRawResponse,
    AsyncEscapedRefResourceWithRawResponse,
    EscapedRefResourceWithStreamingResponse,
    AsyncEscapedRefResourceWithStreamingResponse,
)
from .parent.parent import (
    ParentResource,
    AsyncParentResource,
    ParentResourceWithRawResponse,
    AsyncParentResourceWithRawResponse,
    ParentResourceWithStreamingResponse,
    AsyncParentResourceWithStreamingResponse,
)

__all__ = ["ResourceRefsResource", "AsyncResourceRefsResource"]


class ResourceRefsResource(SyncAPIResource):
    @cached_property
    def parent(self) -> ParentResource:
        return ParentResource(self._client)

    @cached_property
    def escaped_ref(self) -> EscapedRefResource:
        return EscapedRefResource(self._client)

    @cached_property
    def with_raw_response(self) -> ResourceRefsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return ResourceRefsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ResourceRefsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return ResourceRefsResourceWithStreamingResponse(self)


class AsyncResourceRefsResource(AsyncAPIResource):
    @cached_property
    def parent(self) -> AsyncParentResource:
        return AsyncParentResource(self._client)

    @cached_property
    def escaped_ref(self) -> AsyncEscapedRefResource:
        return AsyncEscapedRefResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncResourceRefsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncResourceRefsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncResourceRefsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncResourceRefsResourceWithStreamingResponse(self)


class ResourceRefsResourceWithRawResponse:
    def __init__(self, resource_refs: ResourceRefsResource) -> None:
        self._resource_refs = resource_refs

    @cached_property
    def parent(self) -> ParentResourceWithRawResponse:
        return ParentResourceWithRawResponse(self._resource_refs.parent)

    @cached_property
    def escaped_ref(self) -> EscapedRefResourceWithRawResponse:
        return EscapedRefResourceWithRawResponse(self._resource_refs.escaped_ref)


class AsyncResourceRefsResourceWithRawResponse:
    def __init__(self, resource_refs: AsyncResourceRefsResource) -> None:
        self._resource_refs = resource_refs

    @cached_property
    def parent(self) -> AsyncParentResourceWithRawResponse:
        return AsyncParentResourceWithRawResponse(self._resource_refs.parent)

    @cached_property
    def escaped_ref(self) -> AsyncEscapedRefResourceWithRawResponse:
        return AsyncEscapedRefResourceWithRawResponse(self._resource_refs.escaped_ref)


class ResourceRefsResourceWithStreamingResponse:
    def __init__(self, resource_refs: ResourceRefsResource) -> None:
        self._resource_refs = resource_refs

    @cached_property
    def parent(self) -> ParentResourceWithStreamingResponse:
        return ParentResourceWithStreamingResponse(self._resource_refs.parent)

    @cached_property
    def escaped_ref(self) -> EscapedRefResourceWithStreamingResponse:
        return EscapedRefResourceWithStreamingResponse(self._resource_refs.escaped_ref)


class AsyncResourceRefsResourceWithStreamingResponse:
    def __init__(self, resource_refs: AsyncResourceRefsResource) -> None:
        self._resource_refs = resource_refs

    @cached_property
    def parent(self) -> AsyncParentResourceWithStreamingResponse:
        return AsyncParentResourceWithStreamingResponse(self._resource_refs.parent)

    @cached_property
    def escaped_ref(self) -> AsyncEscapedRefResourceWithStreamingResponse:
        return AsyncEscapedRefResourceWithStreamingResponse(self._resource_refs.escaped_ref)
