# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .. import _legacy_response
from ..types import version_1_30_name_create_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, strip_not_given, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from .._base_client import make_request_options
from ..types.version_1_30_name_create_response import Version1_30NameCreateResponse

__all__ = ["Version1_30NamesResource", "AsyncVersion1_30NamesResource"]


class Version1_30NamesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> Version1_30NamesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return Version1_30NamesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> Version1_30NamesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return Version1_30NamesResourceWithStreamingResponse(self)

    def create(
        self,
        version_1_15: str,
        *,
        version_1_16: str | Omit = omit,
        version_1_17: str | Omit = omit,
        version_1_14: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Version1_30NameCreateResponse:
        """
        The `X-Client-Secret` header shouldn't be included in params definitions as it
        is already sent as a client argument.

        Whereas the `X-Custom-Endpoint-Header` should be included as it is only used
        here.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not version_1_15:
            raise ValueError(f"Expected a non-empty value for `version_1_15` but received {version_1_15!r}")
        extra_headers = {**strip_not_given({"version_1_14": version_1_14}), **(extra_headers or {})}
        return self._post(
            f"/version_1_30_names/query/{version_1_15}",
            body=maybe_transform(
                {"version_1_17": version_1_17}, version_1_30_name_create_params.Version1_30NameCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
                query=maybe_transform(
                    {"version_1_16": version_1_16}, version_1_30_name_create_params.Version1_30NameCreateParams
                ),
            ),
            cast_to=Version1_30NameCreateResponse,
        )


class AsyncVersion1_30NamesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncVersion1_30NamesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncVersion1_30NamesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVersion1_30NamesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncVersion1_30NamesResourceWithStreamingResponse(self)

    async def create(
        self,
        version_1_15: str,
        *,
        version_1_16: str | Omit = omit,
        version_1_17: str | Omit = omit,
        version_1_14: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Version1_30NameCreateResponse:
        """
        The `X-Client-Secret` header shouldn't be included in params definitions as it
        is already sent as a client argument.

        Whereas the `X-Custom-Endpoint-Header` should be included as it is only used
        here.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not version_1_15:
            raise ValueError(f"Expected a non-empty value for `version_1_15` but received {version_1_15!r}")
        extra_headers = {**strip_not_given({"version_1_14": version_1_14}), **(extra_headers or {})}
        return await self._post(
            f"/version_1_30_names/query/{version_1_15}",
            body=await async_maybe_transform(
                {"version_1_17": version_1_17}, version_1_30_name_create_params.Version1_30NameCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
                query=await async_maybe_transform(
                    {"version_1_16": version_1_16}, version_1_30_name_create_params.Version1_30NameCreateParams
                ),
            ),
            cast_to=Version1_30NameCreateResponse,
        )


class Version1_30NamesResourceWithRawResponse:
    def __init__(self, version_1_30_names: Version1_30NamesResource) -> None:
        self._version_1_30_names = version_1_30_names

        self.create = _legacy_response.to_raw_response_wrapper(
            version_1_30_names.create,
        )


class AsyncVersion1_30NamesResourceWithRawResponse:
    def __init__(self, version_1_30_names: AsyncVersion1_30NamesResource) -> None:
        self._version_1_30_names = version_1_30_names

        self.create = _legacy_response.async_to_raw_response_wrapper(
            version_1_30_names.create,
        )


class Version1_30NamesResourceWithStreamingResponse:
    def __init__(self, version_1_30_names: Version1_30NamesResource) -> None:
        self._version_1_30_names = version_1_30_names

        self.create = to_streamed_response_wrapper(
            version_1_30_names.create,
        )


class AsyncVersion1_30NamesResourceWithStreamingResponse:
    def __init__(self, version_1_30_names: AsyncVersion1_30NamesResource) -> None:
        self._version_1_30_names = version_1_30_names

        self.create = async_to_streamed_response_wrapper(
            version_1_30_names.create,
        )
