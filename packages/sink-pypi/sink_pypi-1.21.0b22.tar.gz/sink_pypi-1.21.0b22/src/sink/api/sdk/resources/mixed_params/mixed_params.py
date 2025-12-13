# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, overload

import httpx

from ... import _legacy_response
from ...types import (
    mixed_param_query_and_body_params,
    mixed_param_query_body_and_path_params,
    mixed_param_body_with_top_level_one_of_and_path_params,
)
from ..._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, not_given
from ..._utils import required_args, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from .duplicates import (
    DuplicatesResource,
    AsyncDuplicatesResource,
    DuplicatesResourceWithRawResponse,
    AsyncDuplicatesResourceWithRawResponse,
    DuplicatesResourceWithStreamingResponse,
    AsyncDuplicatesResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ..._base_client import make_request_options
from ...types.shared.basic_shared_model_object import BasicSharedModelObject

__all__ = ["MixedParamsResource", "AsyncMixedParamsResource"]


class MixedParamsResource(SyncAPIResource):
    @cached_property
    def duplicates(self) -> DuplicatesResource:
        return DuplicatesResource(self._client)

    @cached_property
    def with_raw_response(self) -> MixedParamsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return MixedParamsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MixedParamsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return MixedParamsResourceWithStreamingResponse(self)

    @overload
    def body_with_top_level_one_of_and_path(
        self,
        path_param: str,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` making use of oneOf, and a path param.

        See
        https://linear.app/stainless/issue/STA-4902/orb-java-unresolved-reference-customerid-externalcustomerid

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    def body_with_top_level_one_of_and_path(
        self,
        path_param: str,
        *,
        bar: str,
        foo: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` making use of oneOf, and a path param.

        See
        https://linear.app/stainless/issue/STA-4902/orb-java-unresolved-reference-customerid-externalcustomerid

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["kind"], ["bar", "foo"])
    def body_with_top_level_one_of_and_path(
        self,
        path_param: str,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"] | Omit = omit,
        bar: str | Omit = omit,
        foo: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        if not path_param:
            raise ValueError(f"Expected a non-empty value for `path_param` but received {path_param!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/mixed_params/body_with_top_level_one_of_and_path/{path_param}",
            body=maybe_transform(
                {
                    "kind": kind,
                    "bar": bar,
                    "foo": foo,
                },
                mixed_param_body_with_top_level_one_of_and_path_params.MixedParamBodyWithTopLevelOneOfAndPathParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def query_and_body(
        self,
        *,
        query_param: str | Omit = omit,
        body_param: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BasicSharedModelObject:
        """
        Endpoint with a `requestBody` that defines both query and body params

        Args:
          query_param: Query param description

          body_param: Body param description

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/mixed_params/query_and_body",
            body=maybe_transform(
                {"body_param": body_param}, mixed_param_query_and_body_params.MixedParamQueryAndBodyParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
                query=maybe_transform(
                    {"query_param": query_param}, mixed_param_query_and_body_params.MixedParamQueryAndBodyParams
                ),
            ),
            cast_to=BasicSharedModelObject,
        )

    def query_body_and_path(
        self,
        path_param: str,
        *,
        query_param: str | Omit = omit,
        body_param: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BasicSharedModelObject:
        """
        Endpoint with a `requestBody` that defines query, body and path params

        Args:
          query_param: Query param description

          body_param: Body param description

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not path_param:
            raise ValueError(f"Expected a non-empty value for `path_param` but received {path_param!r}")
        return self._post(
            f"/mixed_params/query_body_and_path/{path_param}",
            body=maybe_transform(
                {"body_param": body_param}, mixed_param_query_body_and_path_params.MixedParamQueryBodyAndPathParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
                query=maybe_transform(
                    {"query_param": query_param},
                    mixed_param_query_body_and_path_params.MixedParamQueryBodyAndPathParams,
                ),
            ),
            cast_to=BasicSharedModelObject,
        )


class AsyncMixedParamsResource(AsyncAPIResource):
    @cached_property
    def duplicates(self) -> AsyncDuplicatesResource:
        return AsyncDuplicatesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncMixedParamsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncMixedParamsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMixedParamsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncMixedParamsResourceWithStreamingResponse(self)

    @overload
    async def body_with_top_level_one_of_and_path(
        self,
        path_param: str,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` making use of oneOf, and a path param.

        See
        https://linear.app/stainless/issue/STA-4902/orb-java-unresolved-reference-customerid-externalcustomerid

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    async def body_with_top_level_one_of_and_path(
        self,
        path_param: str,
        *,
        bar: str,
        foo: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` making use of oneOf, and a path param.

        See
        https://linear.app/stainless/issue/STA-4902/orb-java-unresolved-reference-customerid-externalcustomerid

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["kind"], ["bar", "foo"])
    async def body_with_top_level_one_of_and_path(
        self,
        path_param: str,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"] | Omit = omit,
        bar: str | Omit = omit,
        foo: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        if not path_param:
            raise ValueError(f"Expected a non-empty value for `path_param` but received {path_param!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/mixed_params/body_with_top_level_one_of_and_path/{path_param}",
            body=await async_maybe_transform(
                {
                    "kind": kind,
                    "bar": bar,
                    "foo": foo,
                },
                mixed_param_body_with_top_level_one_of_and_path_params.MixedParamBodyWithTopLevelOneOfAndPathParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    async def query_and_body(
        self,
        *,
        query_param: str | Omit = omit,
        body_param: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BasicSharedModelObject:
        """
        Endpoint with a `requestBody` that defines both query and body params

        Args:
          query_param: Query param description

          body_param: Body param description

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/mixed_params/query_and_body",
            body=await async_maybe_transform(
                {"body_param": body_param}, mixed_param_query_and_body_params.MixedParamQueryAndBodyParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
                query=await async_maybe_transform(
                    {"query_param": query_param}, mixed_param_query_and_body_params.MixedParamQueryAndBodyParams
                ),
            ),
            cast_to=BasicSharedModelObject,
        )

    async def query_body_and_path(
        self,
        path_param: str,
        *,
        query_param: str | Omit = omit,
        body_param: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BasicSharedModelObject:
        """
        Endpoint with a `requestBody` that defines query, body and path params

        Args:
          query_param: Query param description

          body_param: Body param description

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not path_param:
            raise ValueError(f"Expected a non-empty value for `path_param` but received {path_param!r}")
        return await self._post(
            f"/mixed_params/query_body_and_path/{path_param}",
            body=await async_maybe_transform(
                {"body_param": body_param}, mixed_param_query_body_and_path_params.MixedParamQueryBodyAndPathParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
                query=await async_maybe_transform(
                    {"query_param": query_param},
                    mixed_param_query_body_and_path_params.MixedParamQueryBodyAndPathParams,
                ),
            ),
            cast_to=BasicSharedModelObject,
        )


class MixedParamsResourceWithRawResponse:
    def __init__(self, mixed_params: MixedParamsResource) -> None:
        self._mixed_params = mixed_params

        self.body_with_top_level_one_of_and_path = _legacy_response.to_raw_response_wrapper(
            mixed_params.body_with_top_level_one_of_and_path,
        )
        self.query_and_body = _legacy_response.to_raw_response_wrapper(
            mixed_params.query_and_body,
        )
        self.query_body_and_path = _legacy_response.to_raw_response_wrapper(
            mixed_params.query_body_and_path,
        )

    @cached_property
    def duplicates(self) -> DuplicatesResourceWithRawResponse:
        return DuplicatesResourceWithRawResponse(self._mixed_params.duplicates)


class AsyncMixedParamsResourceWithRawResponse:
    def __init__(self, mixed_params: AsyncMixedParamsResource) -> None:
        self._mixed_params = mixed_params

        self.body_with_top_level_one_of_and_path = _legacy_response.async_to_raw_response_wrapper(
            mixed_params.body_with_top_level_one_of_and_path,
        )
        self.query_and_body = _legacy_response.async_to_raw_response_wrapper(
            mixed_params.query_and_body,
        )
        self.query_body_and_path = _legacy_response.async_to_raw_response_wrapper(
            mixed_params.query_body_and_path,
        )

    @cached_property
    def duplicates(self) -> AsyncDuplicatesResourceWithRawResponse:
        return AsyncDuplicatesResourceWithRawResponse(self._mixed_params.duplicates)


class MixedParamsResourceWithStreamingResponse:
    def __init__(self, mixed_params: MixedParamsResource) -> None:
        self._mixed_params = mixed_params

        self.body_with_top_level_one_of_and_path = to_streamed_response_wrapper(
            mixed_params.body_with_top_level_one_of_and_path,
        )
        self.query_and_body = to_streamed_response_wrapper(
            mixed_params.query_and_body,
        )
        self.query_body_and_path = to_streamed_response_wrapper(
            mixed_params.query_body_and_path,
        )

    @cached_property
    def duplicates(self) -> DuplicatesResourceWithStreamingResponse:
        return DuplicatesResourceWithStreamingResponse(self._mixed_params.duplicates)


class AsyncMixedParamsResourceWithStreamingResponse:
    def __init__(self, mixed_params: AsyncMixedParamsResource) -> None:
        self._mixed_params = mixed_params

        self.body_with_top_level_one_of_and_path = async_to_streamed_response_wrapper(
            mixed_params.body_with_top_level_one_of_and_path,
        )
        self.query_and_body = async_to_streamed_response_wrapper(
            mixed_params.query_and_body,
        )
        self.query_body_and_path = async_to_streamed_response_wrapper(
            mixed_params.query_body_and_path,
        )

    @cached_property
    def duplicates(self) -> AsyncDuplicatesResourceWithStreamingResponse:
        return AsyncDuplicatesResourceWithStreamingResponse(self._mixed_params.duplicates)
