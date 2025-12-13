# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .... import _legacy_response
from ...._types import Body, Query, Headers, NotGiven, not_given
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ...._base_client import make_request_options
from ....types.names.reserved_names.import_ import Import

__all__ = ["ImportResource", "AsyncImportResource"]


class ImportResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ImportResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return ImportResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ImportResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return ImportResourceWithStreamingResponse(self)

    def import_(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Import:
        """
        Endpoint that is named `import` in the config which can cause issues in certain
        languages.
        """
        return self._get(
            "/names/reserved_names/import",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Import,
        )


class AsyncImportResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncImportResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncImportResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncImportResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncImportResourceWithStreamingResponse(self)

    async def import_(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Import:
        """
        Endpoint that is named `import` in the config which can cause issues in certain
        languages.
        """
        return await self._get(
            "/names/reserved_names/import",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Import,
        )


class ImportResourceWithRawResponse:
    def __init__(self, import_: ImportResource) -> None:
        self._import_ = import_

        self.import_ = _legacy_response.to_raw_response_wrapper(
            import_.import_,
        )


class AsyncImportResourceWithRawResponse:
    def __init__(self, import_: AsyncImportResource) -> None:
        self._import_ = import_

        self.import_ = _legacy_response.async_to_raw_response_wrapper(
            import_.import_,
        )


class ImportResourceWithStreamingResponse:
    def __init__(self, import_: ImportResource) -> None:
        self._import_ = import_

        self.import_ = to_streamed_response_wrapper(
            import_.import_,
        )


class AsyncImportResourceWithStreamingResponse:
    def __init__(self, import_: AsyncImportResource) -> None:
        self._import_ = import_

        self.import_ = async_to_streamed_response_wrapper(
            import_.import_,
        )
