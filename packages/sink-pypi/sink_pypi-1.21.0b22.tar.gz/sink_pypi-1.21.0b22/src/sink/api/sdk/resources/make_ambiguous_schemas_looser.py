# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .. import _legacy_response
from .._types import Body, Query, Headers, NotGiven, not_given
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from .._base_client import make_request_options
from ..types.make_ambiguous_schemas_looser_make_ambiguous_schemas_looser_response import (
    MakeAmbiguousSchemasLooserMakeAmbiguousSchemasLooserResponse,
)

__all__ = ["MakeAmbiguousSchemasLooserResource", "AsyncMakeAmbiguousSchemasLooserResource"]


class MakeAmbiguousSchemasLooserResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MakeAmbiguousSchemasLooserResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return MakeAmbiguousSchemasLooserResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MakeAmbiguousSchemasLooserResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return MakeAmbiguousSchemasLooserResourceWithStreamingResponse(self)

    def make_ambiguous_schemas_looser(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MakeAmbiguousSchemasLooserMakeAmbiguousSchemasLooserResponse:
        """Test case for makeAmbiguousSchemasLooser"""
        return self._get(
            "/make-ambiguous-schemas-looser",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MakeAmbiguousSchemasLooserMakeAmbiguousSchemasLooserResponse,
        )


class AsyncMakeAmbiguousSchemasLooserResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMakeAmbiguousSchemasLooserResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncMakeAmbiguousSchemasLooserResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMakeAmbiguousSchemasLooserResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncMakeAmbiguousSchemasLooserResourceWithStreamingResponse(self)

    async def make_ambiguous_schemas_looser(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MakeAmbiguousSchemasLooserMakeAmbiguousSchemasLooserResponse:
        """Test case for makeAmbiguousSchemasLooser"""
        return await self._get(
            "/make-ambiguous-schemas-looser",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MakeAmbiguousSchemasLooserMakeAmbiguousSchemasLooserResponse,
        )


class MakeAmbiguousSchemasLooserResourceWithRawResponse:
    def __init__(self, make_ambiguous_schemas_looser: MakeAmbiguousSchemasLooserResource) -> None:
        self._make_ambiguous_schemas_looser = make_ambiguous_schemas_looser

        self.make_ambiguous_schemas_looser = _legacy_response.to_raw_response_wrapper(
            make_ambiguous_schemas_looser.make_ambiguous_schemas_looser,
        )


class AsyncMakeAmbiguousSchemasLooserResourceWithRawResponse:
    def __init__(self, make_ambiguous_schemas_looser: AsyncMakeAmbiguousSchemasLooserResource) -> None:
        self._make_ambiguous_schemas_looser = make_ambiguous_schemas_looser

        self.make_ambiguous_schemas_looser = _legacy_response.async_to_raw_response_wrapper(
            make_ambiguous_schemas_looser.make_ambiguous_schemas_looser,
        )


class MakeAmbiguousSchemasLooserResourceWithStreamingResponse:
    def __init__(self, make_ambiguous_schemas_looser: MakeAmbiguousSchemasLooserResource) -> None:
        self._make_ambiguous_schemas_looser = make_ambiguous_schemas_looser

        self.make_ambiguous_schemas_looser = to_streamed_response_wrapper(
            make_ambiguous_schemas_looser.make_ambiguous_schemas_looser,
        )


class AsyncMakeAmbiguousSchemasLooserResourceWithStreamingResponse:
    def __init__(self, make_ambiguous_schemas_looser: AsyncMakeAmbiguousSchemasLooserResource) -> None:
        self._make_ambiguous_schemas_looser = make_ambiguous_schemas_looser

        self.make_ambiguous_schemas_looser = async_to_streamed_response_wrapper(
            make_ambiguous_schemas_looser.make_ambiguous_schemas_looser,
        )
