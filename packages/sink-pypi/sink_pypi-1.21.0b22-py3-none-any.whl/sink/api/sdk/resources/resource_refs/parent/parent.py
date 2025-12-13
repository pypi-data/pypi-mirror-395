# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .... import _legacy_response
from .child import (
    ChildResource,
    AsyncChildResource,
    ChildResourceWithRawResponse,
    AsyncChildResourceWithRawResponse,
    ChildResourceWithStreamingResponse,
    AsyncChildResourceWithStreamingResponse,
)
from ...._types import Body, Query, Headers, NotGiven, not_given
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ...._base_client import make_request_options
from ....types.resource_refs.parent_model_with_child_ref import ParentModelWithChildRef

__all__ = ["ParentResource", "AsyncParentResource"]


class ParentResource(SyncAPIResource):
    @cached_property
    def child(self) -> ChildResource:
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

    def returns_parent_model_with_child_ref(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ParentModelWithChildRef:
        """endpoint that returns a model that has a nested reference to a child model"""
        return self._get(
            "/resource_refs/parent_with_child_ref",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ParentModelWithChildRef,
        )


class AsyncParentResource(AsyncAPIResource):
    @cached_property
    def child(self) -> AsyncChildResource:
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

    async def returns_parent_model_with_child_ref(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ParentModelWithChildRef:
        """endpoint that returns a model that has a nested reference to a child model"""
        return await self._get(
            "/resource_refs/parent_with_child_ref",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ParentModelWithChildRef,
        )


class ParentResourceWithRawResponse:
    def __init__(self, parent: ParentResource) -> None:
        self._parent = parent

        self.returns_parent_model_with_child_ref = _legacy_response.to_raw_response_wrapper(
            parent.returns_parent_model_with_child_ref,
        )

    @cached_property
    def child(self) -> ChildResourceWithRawResponse:
        return ChildResourceWithRawResponse(self._parent.child)


class AsyncParentResourceWithRawResponse:
    def __init__(self, parent: AsyncParentResource) -> None:
        self._parent = parent

        self.returns_parent_model_with_child_ref = _legacy_response.async_to_raw_response_wrapper(
            parent.returns_parent_model_with_child_ref,
        )

    @cached_property
    def child(self) -> AsyncChildResourceWithRawResponse:
        return AsyncChildResourceWithRawResponse(self._parent.child)


class ParentResourceWithStreamingResponse:
    def __init__(self, parent: ParentResource) -> None:
        self._parent = parent

        self.returns_parent_model_with_child_ref = to_streamed_response_wrapper(
            parent.returns_parent_model_with_child_ref,
        )

    @cached_property
    def child(self) -> ChildResourceWithStreamingResponse:
        return ChildResourceWithStreamingResponse(self._parent.child)


class AsyncParentResourceWithStreamingResponse:
    def __init__(self, parent: AsyncParentResource) -> None:
        self._parent = parent

        self.returns_parent_model_with_child_ref = async_to_streamed_response_wrapper(
            parent.returns_parent_model_with_child_ref,
        )

    @cached_property
    def child(self) -> AsyncChildResourceWithStreamingResponse:
        return AsyncChildResourceWithStreamingResponse(self._parent.child)
