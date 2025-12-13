# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ... import _legacy_response
from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ..._base_client import make_request_options
from ...types.names.renaming_explicit_response_property_response import RenamingExplicitResponsePropertyResponse

__all__ = ["RenamingResource", "AsyncRenamingResource"]


class RenamingResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RenamingResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return RenamingResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RenamingResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return RenamingResourceWithStreamingResponse(self)

    def explicit_response_property(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RenamingExplicitResponsePropertyResponse:
        """Endpoint with a renamed response property in each language."""
        return self._get(
            "/names/renaming/explicit_response_property",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RenamingExplicitResponsePropertyResponse,
        )


class AsyncRenamingResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRenamingResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncRenamingResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRenamingResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncRenamingResourceWithStreamingResponse(self)

    async def explicit_response_property(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RenamingExplicitResponsePropertyResponse:
        """Endpoint with a renamed response property in each language."""
        return await self._get(
            "/names/renaming/explicit_response_property",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RenamingExplicitResponsePropertyResponse,
        )


class RenamingResourceWithRawResponse:
    def __init__(self, renaming: RenamingResource) -> None:
        self._renaming = renaming

        self.explicit_response_property = _legacy_response.to_raw_response_wrapper(
            renaming.explicit_response_property,
        )


class AsyncRenamingResourceWithRawResponse:
    def __init__(self, renaming: AsyncRenamingResource) -> None:
        self._renaming = renaming

        self.explicit_response_property = _legacy_response.async_to_raw_response_wrapper(
            renaming.explicit_response_property,
        )


class RenamingResourceWithStreamingResponse:
    def __init__(self, renaming: RenamingResource) -> None:
        self._renaming = renaming

        self.explicit_response_property = to_streamed_response_wrapper(
            renaming.explicit_response_property,
        )


class AsyncRenamingResourceWithStreamingResponse:
    def __init__(self, renaming: AsyncRenamingResource) -> None:
        self._renaming = renaming

        self.explicit_response_property = async_to_streamed_response_wrapper(
            renaming.explicit_response_property,
        )
