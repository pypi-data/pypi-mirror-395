# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Type, cast

import httpx

from .. import _legacy_response
from .._types import Body, Query, Headers, NotGiven, not_given
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from .._wrappers import DataWrapper, ItemsWrapper
from .._base_client import make_request_options
from ..types.address import Address
from ..types.envelope_wrapped_array_response import EnvelopeWrappedArrayResponse
from ..types.envelope_inline_response_response import EnvelopeInlineResponseResponse

__all__ = ["EnvelopesResource", "AsyncEnvelopesResource"]


class EnvelopesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EnvelopesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return EnvelopesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EnvelopesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return EnvelopesResourceWithStreamingResponse(self)

    def explicit(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Address:
        """Endpoint with a response wrapped within a `data` property."""
        return self._get(
            "/envelopes/data",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=DataWrapper[Address]._unwrapper,
            ),
            cast_to=cast(Type[Address], DataWrapper[Address]),
        )

    def implicit(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Address:
        """Endpoint with a response wrapped within a `items` property."""
        return self._get(
            "/envelopes/items",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ItemsWrapper[Address]._unwrapper,
            ),
            cast_to=cast(Type[Address], ItemsWrapper[Address]),
        )

    def inline_response(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EnvelopeInlineResponseResponse:
        """
        Endpoint with a response wrapped within a `items` property that doesn't use a
        $ref.
        """
        return self._get(
            "/envelopes/items/inline_response",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ItemsWrapper[EnvelopeInlineResponseResponse]._unwrapper,
            ),
            cast_to=cast(Type[EnvelopeInlineResponseResponse], ItemsWrapper[EnvelopeInlineResponseResponse]),
        )

    def wrapped_array(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EnvelopeWrappedArrayResponse:
        """
        Endpoint with a response wrapped within a `items` property that is an array
        type.
        """
        return self._get(
            "/envelopes/items/wrapped_array",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ItemsWrapper[EnvelopeWrappedArrayResponse]._unwrapper,
            ),
            cast_to=cast(Type[EnvelopeWrappedArrayResponse], ItemsWrapper[EnvelopeWrappedArrayResponse]),
        )


class AsyncEnvelopesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEnvelopesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncEnvelopesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEnvelopesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncEnvelopesResourceWithStreamingResponse(self)

    async def explicit(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Address:
        """Endpoint with a response wrapped within a `data` property."""
        return await self._get(
            "/envelopes/data",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=DataWrapper[Address]._unwrapper,
            ),
            cast_to=cast(Type[Address], DataWrapper[Address]),
        )

    async def implicit(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Address:
        """Endpoint with a response wrapped within a `items` property."""
        return await self._get(
            "/envelopes/items",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ItemsWrapper[Address]._unwrapper,
            ),
            cast_to=cast(Type[Address], ItemsWrapper[Address]),
        )

    async def inline_response(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EnvelopeInlineResponseResponse:
        """
        Endpoint with a response wrapped within a `items` property that doesn't use a
        $ref.
        """
        return await self._get(
            "/envelopes/items/inline_response",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ItemsWrapper[EnvelopeInlineResponseResponse]._unwrapper,
            ),
            cast_to=cast(Type[EnvelopeInlineResponseResponse], ItemsWrapper[EnvelopeInlineResponseResponse]),
        )

    async def wrapped_array(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EnvelopeWrappedArrayResponse:
        """
        Endpoint with a response wrapped within a `items` property that is an array
        type.
        """
        return await self._get(
            "/envelopes/items/wrapped_array",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ItemsWrapper[EnvelopeWrappedArrayResponse]._unwrapper,
            ),
            cast_to=cast(Type[EnvelopeWrappedArrayResponse], ItemsWrapper[EnvelopeWrappedArrayResponse]),
        )


class EnvelopesResourceWithRawResponse:
    def __init__(self, envelopes: EnvelopesResource) -> None:
        self._envelopes = envelopes

        self.explicit = _legacy_response.to_raw_response_wrapper(
            envelopes.explicit,
        )
        self.implicit = _legacy_response.to_raw_response_wrapper(
            envelopes.implicit,
        )
        self.inline_response = _legacy_response.to_raw_response_wrapper(
            envelopes.inline_response,
        )
        self.wrapped_array = _legacy_response.to_raw_response_wrapper(
            envelopes.wrapped_array,
        )


class AsyncEnvelopesResourceWithRawResponse:
    def __init__(self, envelopes: AsyncEnvelopesResource) -> None:
        self._envelopes = envelopes

        self.explicit = _legacy_response.async_to_raw_response_wrapper(
            envelopes.explicit,
        )
        self.implicit = _legacy_response.async_to_raw_response_wrapper(
            envelopes.implicit,
        )
        self.inline_response = _legacy_response.async_to_raw_response_wrapper(
            envelopes.inline_response,
        )
        self.wrapped_array = _legacy_response.async_to_raw_response_wrapper(
            envelopes.wrapped_array,
        )


class EnvelopesResourceWithStreamingResponse:
    def __init__(self, envelopes: EnvelopesResource) -> None:
        self._envelopes = envelopes

        self.explicit = to_streamed_response_wrapper(
            envelopes.explicit,
        )
        self.implicit = to_streamed_response_wrapper(
            envelopes.implicit,
        )
        self.inline_response = to_streamed_response_wrapper(
            envelopes.inline_response,
        )
        self.wrapped_array = to_streamed_response_wrapper(
            envelopes.wrapped_array,
        )


class AsyncEnvelopesResourceWithStreamingResponse:
    def __init__(self, envelopes: AsyncEnvelopesResource) -> None:
        self._envelopes = envelopes

        self.explicit = async_to_streamed_response_wrapper(
            envelopes.explicit,
        )
        self.implicit = async_to_streamed_response_wrapper(
            envelopes.implicit,
        )
        self.inline_response = async_to_streamed_response_wrapper(
            envelopes.inline_response,
        )
        self.wrapped_array = async_to_streamed_response_wrapper(
            envelopes.wrapped_array,
        )
