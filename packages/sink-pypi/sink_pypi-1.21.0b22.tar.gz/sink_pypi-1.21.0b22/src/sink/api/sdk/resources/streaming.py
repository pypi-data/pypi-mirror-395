# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, overload

import httpx

from .. import _legacy_response
from ..types import (
    streaming_basic_params,
    streaming_nested_params_params,
    streaming_no_discriminator_params,
    streaming_query_param_discriminator_params,
    streaming_with_unrelated_default_param_params,
)
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import required_args, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from .._streaming import Stream, AsyncStream
from .._base_client import make_request_options
from ..types.streaming_basic_response import StreamingBasicResponse
from ..types.streaming_nested_params_response import StreamingNestedParamsResponse
from ..types.streaming_no_discriminator_response import StreamingNoDiscriminatorResponse
from ..types.streaming_query_param_discriminator_response import StreamingQueryParamDiscriminatorResponse
from ..types.streaming_with_unrelated_default_param_response import StreamingWithUnrelatedDefaultParamResponse

__all__ = ["StreamingResource", "AsyncStreamingResource"]


class StreamingResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> StreamingResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return StreamingResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> StreamingResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return StreamingResourceWithStreamingResponse(self)

    @overload
    def basic(
        self,
        *,
        model: str,
        prompt: str,
        stream: Literal[False] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> StreamingBasicResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    def basic(
        self,
        *,
        model: str,
        prompt: str,
        stream: Literal[True],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Stream[StreamingBasicResponse]:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    def basic(
        self,
        *,
        model: str,
        prompt: str,
        stream: bool,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> StreamingBasicResponse | Stream[StreamingBasicResponse]:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["model", "prompt"], ["model", "prompt", "stream"])
    def basic(
        self,
        *,
        model: str,
        prompt: str,
        stream: Literal[False] | Literal[True] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> StreamingBasicResponse | Stream[StreamingBasicResponse]:
        return self._post(
            "/streaming/basic",
            body=maybe_transform(
                {
                    "model": model,
                    "prompt": prompt,
                    "stream": stream,
                },
                streaming_basic_params.StreamingBasicParamsStreaming
                if stream
                else streaming_basic_params.StreamingBasicParamsNonStreaming,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=StreamingBasicResponse,
            stream=stream or False,
            stream_cls=Stream[StreamingBasicResponse],
        )

    @overload
    def nested_params(
        self,
        *,
        model: str,
        prompt: str,
        parent_object: streaming_nested_params_params.ParentObject | Omit = omit,
        stream: Literal[False] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> StreamingNestedParamsResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    def nested_params(
        self,
        *,
        model: str,
        prompt: str,
        stream: Literal[True],
        parent_object: streaming_nested_params_params.ParentObject | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Stream[StreamingNestedParamsResponse]:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    def nested_params(
        self,
        *,
        model: str,
        prompt: str,
        stream: bool,
        parent_object: streaming_nested_params_params.ParentObject | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> StreamingNestedParamsResponse | Stream[StreamingNestedParamsResponse]:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["model", "prompt"], ["model", "prompt", "stream"])
    def nested_params(
        self,
        *,
        model: str,
        prompt: str,
        parent_object: streaming_nested_params_params.ParentObject | Omit = omit,
        stream: Literal[False] | Literal[True] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> StreamingNestedParamsResponse | Stream[StreamingNestedParamsResponse]:
        return self._post(
            "/streaming/nested_params",
            body=maybe_transform(
                {
                    "model": model,
                    "prompt": prompt,
                    "parent_object": parent_object,
                    "stream": stream,
                },
                streaming_nested_params_params.StreamingNestedParamsParamsStreaming
                if stream
                else streaming_nested_params_params.StreamingNestedParamsParamsNonStreaming,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=StreamingNestedParamsResponse,
            stream=stream or False,
            stream_cls=Stream[StreamingNestedParamsResponse],
        )

    def no_discriminator(
        self,
        *,
        model: str,
        prompt: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Stream[StreamingNoDiscriminatorResponse]:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/streaming/no_discriminator",
            body=maybe_transform(
                {
                    "model": model,
                    "prompt": prompt,
                },
                streaming_no_discriminator_params.StreamingNoDiscriminatorParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=StreamingNoDiscriminatorResponse,
            stream=True,
            stream_cls=Stream[StreamingNoDiscriminatorResponse],
        )

    @overload
    def query_param_discriminator(
        self,
        *,
        prompt: str,
        should_stream: Literal[False] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StreamingQueryParamDiscriminatorResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def query_param_discriminator(
        self,
        *,
        prompt: str,
        should_stream: Literal[True],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Stream[StreamingQueryParamDiscriminatorResponse]:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def query_param_discriminator(
        self,
        *,
        prompt: str,
        should_stream: bool,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StreamingQueryParamDiscriminatorResponse | Stream[StreamingQueryParamDiscriminatorResponse]:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["prompt"], ["prompt", "should_stream"])
    def query_param_discriminator(
        self,
        *,
        prompt: str,
        should_stream: Literal[False] | Literal[True] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StreamingQueryParamDiscriminatorResponse | Stream[StreamingQueryParamDiscriminatorResponse]:
        return self._get(
            "/streaming/query_param_discriminator",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "prompt": prompt,
                        "should_stream": should_stream,
                    },
                    streaming_query_param_discriminator_params.StreamingQueryParamDiscriminatorParams,
                ),
            ),
            cast_to=StreamingQueryParamDiscriminatorResponse,
            stream=should_stream or False,
            stream_cls=Stream[StreamingQueryParamDiscriminatorResponse],
        )

    @overload
    def with_unrelated_default_param(
        self,
        *,
        model: str,
        param_with_default_value: Literal["my_enum_value"] = "my_enum_value",
        prompt: str,
        stream: Literal[False] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> StreamingWithUnrelatedDefaultParamResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    def with_unrelated_default_param(
        self,
        *,
        model: str,
        param_with_default_value: Literal["my_enum_value"] = "my_enum_value",
        prompt: str,
        stream: Literal[True],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Stream[StreamingWithUnrelatedDefaultParamResponse]:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    def with_unrelated_default_param(
        self,
        *,
        model: str,
        param_with_default_value: Literal["my_enum_value"] = "my_enum_value",
        prompt: str,
        stream: bool,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> StreamingWithUnrelatedDefaultParamResponse | Stream[StreamingWithUnrelatedDefaultParamResponse]:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["model", "prompt"], ["model", "prompt", "stream"])
    def with_unrelated_default_param(
        self,
        *,
        model: str,
        param_with_default_value: Literal["my_enum_value"] = "my_enum_value",
        prompt: str,
        stream: Literal[False] | Literal[True] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> StreamingWithUnrelatedDefaultParamResponse | Stream[StreamingWithUnrelatedDefaultParamResponse]:
        return self._post(
            "/streaming/with_unrelated_default_param",
            body=maybe_transform(
                {
                    "model": model,
                    "param_with_default_value": param_with_default_value,
                    "prompt": prompt,
                    "stream": stream,
                },
                streaming_with_unrelated_default_param_params.StreamingWithUnrelatedDefaultParamParamsStreaming
                if stream
                else streaming_with_unrelated_default_param_params.StreamingWithUnrelatedDefaultParamParamsNonStreaming,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=StreamingWithUnrelatedDefaultParamResponse,
            stream=stream or False,
            stream_cls=Stream[StreamingWithUnrelatedDefaultParamResponse],
        )


class AsyncStreamingResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncStreamingResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncStreamingResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncStreamingResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncStreamingResourceWithStreamingResponse(self)

    @overload
    async def basic(
        self,
        *,
        model: str,
        prompt: str,
        stream: Literal[False] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> StreamingBasicResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    async def basic(
        self,
        *,
        model: str,
        prompt: str,
        stream: Literal[True],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> AsyncStream[StreamingBasicResponse]:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    async def basic(
        self,
        *,
        model: str,
        prompt: str,
        stream: bool,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> StreamingBasicResponse | AsyncStream[StreamingBasicResponse]:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["model", "prompt"], ["model", "prompt", "stream"])
    async def basic(
        self,
        *,
        model: str,
        prompt: str,
        stream: Literal[False] | Literal[True] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> StreamingBasicResponse | AsyncStream[StreamingBasicResponse]:
        return await self._post(
            "/streaming/basic",
            body=await async_maybe_transform(
                {
                    "model": model,
                    "prompt": prompt,
                    "stream": stream,
                },
                streaming_basic_params.StreamingBasicParamsStreaming
                if stream
                else streaming_basic_params.StreamingBasicParamsNonStreaming,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=StreamingBasicResponse,
            stream=stream or False,
            stream_cls=AsyncStream[StreamingBasicResponse],
        )

    @overload
    async def nested_params(
        self,
        *,
        model: str,
        prompt: str,
        parent_object: streaming_nested_params_params.ParentObject | Omit = omit,
        stream: Literal[False] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> StreamingNestedParamsResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    async def nested_params(
        self,
        *,
        model: str,
        prompt: str,
        stream: Literal[True],
        parent_object: streaming_nested_params_params.ParentObject | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> AsyncStream[StreamingNestedParamsResponse]:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    async def nested_params(
        self,
        *,
        model: str,
        prompt: str,
        stream: bool,
        parent_object: streaming_nested_params_params.ParentObject | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> StreamingNestedParamsResponse | AsyncStream[StreamingNestedParamsResponse]:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["model", "prompt"], ["model", "prompt", "stream"])
    async def nested_params(
        self,
        *,
        model: str,
        prompt: str,
        parent_object: streaming_nested_params_params.ParentObject | Omit = omit,
        stream: Literal[False] | Literal[True] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> StreamingNestedParamsResponse | AsyncStream[StreamingNestedParamsResponse]:
        return await self._post(
            "/streaming/nested_params",
            body=await async_maybe_transform(
                {
                    "model": model,
                    "prompt": prompt,
                    "parent_object": parent_object,
                    "stream": stream,
                },
                streaming_nested_params_params.StreamingNestedParamsParamsStreaming
                if stream
                else streaming_nested_params_params.StreamingNestedParamsParamsNonStreaming,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=StreamingNestedParamsResponse,
            stream=stream or False,
            stream_cls=AsyncStream[StreamingNestedParamsResponse],
        )

    async def no_discriminator(
        self,
        *,
        model: str,
        prompt: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> AsyncStream[StreamingNoDiscriminatorResponse]:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/streaming/no_discriminator",
            body=await async_maybe_transform(
                {
                    "model": model,
                    "prompt": prompt,
                },
                streaming_no_discriminator_params.StreamingNoDiscriminatorParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=StreamingNoDiscriminatorResponse,
            stream=True,
            stream_cls=AsyncStream[StreamingNoDiscriminatorResponse],
        )

    @overload
    async def query_param_discriminator(
        self,
        *,
        prompt: str,
        should_stream: Literal[False] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StreamingQueryParamDiscriminatorResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def query_param_discriminator(
        self,
        *,
        prompt: str,
        should_stream: Literal[True],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncStream[StreamingQueryParamDiscriminatorResponse]:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def query_param_discriminator(
        self,
        *,
        prompt: str,
        should_stream: bool,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StreamingQueryParamDiscriminatorResponse | AsyncStream[StreamingQueryParamDiscriminatorResponse]:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["prompt"], ["prompt", "should_stream"])
    async def query_param_discriminator(
        self,
        *,
        prompt: str,
        should_stream: Literal[False] | Literal[True] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StreamingQueryParamDiscriminatorResponse | AsyncStream[StreamingQueryParamDiscriminatorResponse]:
        return await self._get(
            "/streaming/query_param_discriminator",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "prompt": prompt,
                        "should_stream": should_stream,
                    },
                    streaming_query_param_discriminator_params.StreamingQueryParamDiscriminatorParams,
                ),
            ),
            cast_to=StreamingQueryParamDiscriminatorResponse,
            stream=should_stream or False,
            stream_cls=AsyncStream[StreamingQueryParamDiscriminatorResponse],
        )

    @overload
    async def with_unrelated_default_param(
        self,
        *,
        model: str,
        param_with_default_value: Literal["my_enum_value"] = "my_enum_value",
        prompt: str,
        stream: Literal[False] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> StreamingWithUnrelatedDefaultParamResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    async def with_unrelated_default_param(
        self,
        *,
        model: str,
        param_with_default_value: Literal["my_enum_value"] = "my_enum_value",
        prompt: str,
        stream: Literal[True],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> AsyncStream[StreamingWithUnrelatedDefaultParamResponse]:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    async def with_unrelated_default_param(
        self,
        *,
        model: str,
        param_with_default_value: Literal["my_enum_value"] = "my_enum_value",
        prompt: str,
        stream: bool,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> StreamingWithUnrelatedDefaultParamResponse | AsyncStream[StreamingWithUnrelatedDefaultParamResponse]:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["model", "prompt"], ["model", "prompt", "stream"])
    async def with_unrelated_default_param(
        self,
        *,
        model: str,
        param_with_default_value: Literal["my_enum_value"] = "my_enum_value",
        prompt: str,
        stream: Literal[False] | Literal[True] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> StreamingWithUnrelatedDefaultParamResponse | AsyncStream[StreamingWithUnrelatedDefaultParamResponse]:
        return await self._post(
            "/streaming/with_unrelated_default_param",
            body=await async_maybe_transform(
                {
                    "model": model,
                    "param_with_default_value": param_with_default_value,
                    "prompt": prompt,
                    "stream": stream,
                },
                streaming_with_unrelated_default_param_params.StreamingWithUnrelatedDefaultParamParamsStreaming
                if stream
                else streaming_with_unrelated_default_param_params.StreamingWithUnrelatedDefaultParamParamsNonStreaming,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=StreamingWithUnrelatedDefaultParamResponse,
            stream=stream or False,
            stream_cls=AsyncStream[StreamingWithUnrelatedDefaultParamResponse],
        )


class StreamingResourceWithRawResponse:
    def __init__(self, streaming: StreamingResource) -> None:
        self._streaming = streaming

        self.basic = _legacy_response.to_raw_response_wrapper(
            streaming.basic,
        )
        self.nested_params = _legacy_response.to_raw_response_wrapper(
            streaming.nested_params,
        )
        self.no_discriminator = _legacy_response.to_raw_response_wrapper(
            streaming.no_discriminator,
        )
        self.query_param_discriminator = _legacy_response.to_raw_response_wrapper(
            streaming.query_param_discriminator,
        )
        self.with_unrelated_default_param = _legacy_response.to_raw_response_wrapper(
            streaming.with_unrelated_default_param,
        )


class AsyncStreamingResourceWithRawResponse:
    def __init__(self, streaming: AsyncStreamingResource) -> None:
        self._streaming = streaming

        self.basic = _legacy_response.async_to_raw_response_wrapper(
            streaming.basic,
        )
        self.nested_params = _legacy_response.async_to_raw_response_wrapper(
            streaming.nested_params,
        )
        self.no_discriminator = _legacy_response.async_to_raw_response_wrapper(
            streaming.no_discriminator,
        )
        self.query_param_discriminator = _legacy_response.async_to_raw_response_wrapper(
            streaming.query_param_discriminator,
        )
        self.with_unrelated_default_param = _legacy_response.async_to_raw_response_wrapper(
            streaming.with_unrelated_default_param,
        )


class StreamingResourceWithStreamingResponse:
    def __init__(self, streaming: StreamingResource) -> None:
        self._streaming = streaming

        self.basic = to_streamed_response_wrapper(
            streaming.basic,
        )
        self.nested_params = to_streamed_response_wrapper(
            streaming.nested_params,
        )
        self.no_discriminator = to_streamed_response_wrapper(
            streaming.no_discriminator,
        )
        self.query_param_discriminator = to_streamed_response_wrapper(
            streaming.query_param_discriminator,
        )
        self.with_unrelated_default_param = to_streamed_response_wrapper(
            streaming.with_unrelated_default_param,
        )


class AsyncStreamingResourceWithStreamingResponse:
    def __init__(self, streaming: AsyncStreamingResource) -> None:
        self._streaming = streaming

        self.basic = async_to_streamed_response_wrapper(
            streaming.basic,
        )
        self.nested_params = async_to_streamed_response_wrapper(
            streaming.nested_params,
        )
        self.no_discriminator = async_to_streamed_response_wrapper(
            streaming.no_discriminator,
        )
        self.query_param_discriminator = async_to_streamed_response_wrapper(
            streaming.query_param_discriminator,
        )
        self.with_unrelated_default_param = async_to_streamed_response_wrapper(
            streaming.with_unrelated_default_param,
        )
