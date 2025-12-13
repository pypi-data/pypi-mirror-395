# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ... import _legacy_response
from .child import (
    ChildResource,
    AsyncChildResource,
    ChildResourceWithRawResponse,
    AsyncChildResourceWithRawResponse,
    ChildResourceWithStreamingResponse,
    AsyncChildResourceWithStreamingResponse,
)
from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ..._base_client import make_request_options
from ...types.model_referenced_in_parent_and_child.model_referenced_in_parent_and_child import (
    ModelReferencedInParentAndChild,
)

__all__ = ["ModelReferencedInParentAndChildResource", "AsyncModelReferencedInParentAndChildResource"]


class ModelReferencedInParentAndChildResource(SyncAPIResource):
    @cached_property
    def child(self) -> ChildResource:
        return ChildResource(self._client)

    @cached_property
    def with_raw_response(self) -> ModelReferencedInParentAndChildResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return ModelReferencedInParentAndChildResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ModelReferencedInParentAndChildResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return ModelReferencedInParentAndChildResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelReferencedInParentAndChild:
        return self._get(
            "/model_referenced_in_parent_and_child",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelReferencedInParentAndChild,
        )


class AsyncModelReferencedInParentAndChildResource(AsyncAPIResource):
    @cached_property
    def child(self) -> AsyncChildResource:
        return AsyncChildResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncModelReferencedInParentAndChildResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncModelReferencedInParentAndChildResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncModelReferencedInParentAndChildResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncModelReferencedInParentAndChildResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelReferencedInParentAndChild:
        return await self._get(
            "/model_referenced_in_parent_and_child",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelReferencedInParentAndChild,
        )


class ModelReferencedInParentAndChildResourceWithRawResponse:
    def __init__(self, model_referenced_in_parent_and_child: ModelReferencedInParentAndChildResource) -> None:
        self._model_referenced_in_parent_and_child = model_referenced_in_parent_and_child

        self.retrieve = _legacy_response.to_raw_response_wrapper(
            model_referenced_in_parent_and_child.retrieve,
        )

    @cached_property
    def child(self) -> ChildResourceWithRawResponse:
        return ChildResourceWithRawResponse(self._model_referenced_in_parent_and_child.child)


class AsyncModelReferencedInParentAndChildResourceWithRawResponse:
    def __init__(self, model_referenced_in_parent_and_child: AsyncModelReferencedInParentAndChildResource) -> None:
        self._model_referenced_in_parent_and_child = model_referenced_in_parent_and_child

        self.retrieve = _legacy_response.async_to_raw_response_wrapper(
            model_referenced_in_parent_and_child.retrieve,
        )

    @cached_property
    def child(self) -> AsyncChildResourceWithRawResponse:
        return AsyncChildResourceWithRawResponse(self._model_referenced_in_parent_and_child.child)


class ModelReferencedInParentAndChildResourceWithStreamingResponse:
    def __init__(self, model_referenced_in_parent_and_child: ModelReferencedInParentAndChildResource) -> None:
        self._model_referenced_in_parent_and_child = model_referenced_in_parent_and_child

        self.retrieve = to_streamed_response_wrapper(
            model_referenced_in_parent_and_child.retrieve,
        )

    @cached_property
    def child(self) -> ChildResourceWithStreamingResponse:
        return ChildResourceWithStreamingResponse(self._model_referenced_in_parent_and_child.child)


class AsyncModelReferencedInParentAndChildResourceWithStreamingResponse:
    def __init__(self, model_referenced_in_parent_and_child: AsyncModelReferencedInParentAndChildResource) -> None:
        self._model_referenced_in_parent_and_child = model_referenced_in_parent_and_child

        self.retrieve = async_to_streamed_response_wrapper(
            model_referenced_in_parent_and_child.retrieve,
        )

    @cached_property
    def child(self) -> AsyncChildResourceWithStreamingResponse:
        return AsyncChildResourceWithStreamingResponse(self._model_referenced_in_parent_and_child.child)
