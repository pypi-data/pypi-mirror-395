# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .. import _legacy_response
from ..types import client_param_with_query_param_params
from .._types import Body, Query, Headers, NotGiven, not_given
from .._utils import is_given, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from .._base_client import make_request_options
from ..types.client_param_with_path_param_response import ClientParamWithPathParamResponse
from ..types.client_param_with_query_param_response import ClientParamWithQueryParamResponse
from ..types.client_param_with_path_param_and_standard_response import ClientParamWithPathParamAndStandardResponse

__all__ = ["ClientParamsResource", "AsyncClientParamsResource"]


class ClientParamsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ClientParamsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return ClientParamsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ClientParamsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return ClientParamsResourceWithStreamingResponse(self)

    def with_path_param(
        self,
        *,
        client_path_param: str | None = None,
        client_path_or_query_param: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ClientParamWithPathParamResponse:
        """
        The operation takes a path param that is able to be set at the client level.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if client_path_param is None:
            client_path_param = self._client._get_client_path_param_path_param()
        if not client_path_param:
            raise ValueError(f"Expected a non-empty value for `client_path_param` but received {client_path_param!r}")
        if client_path_or_query_param is None:
            client_path_or_query_param = self._client._get_client_path_or_query_param_path_param()
        if not client_path_or_query_param:
            raise ValueError(
                f"Expected a non-empty value for `client_path_or_query_param` but received {client_path_or_query_param!r}"
            )
        return self._post(
            f"/client_params/path_params/{client_path_param}/{client_path_or_query_param}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ClientParamWithPathParamResponse,
        )

    def with_path_param_and_standard(
        self,
        id: str,
        *,
        camel_cased_path: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ClientParamWithPathParamAndStandardResponse:
        """
        The operation takes a path param that is able to be set at the client level
        alongside a standard path param.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if camel_cased_path is None:
            camel_cased_path = self._client._get_camel_case_path_path_param()
        if not camel_cased_path:
            raise ValueError(f"Expected a non-empty value for `camel_cased_path` but received {camel_cased_path!r}")
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/client_params/path_params/{camel_cased_path}/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ClientParamWithPathParamAndStandardResponse,
        )

    def with_query_param(
        self,
        *,
        client_path_or_query_param: str | NotGiven = not_given,
        client_query_param: str | NotGiven = not_given,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ClientParamWithQueryParamResponse:
        """
        The operation takes a query param that is able to be set at the client level.

        Args:
          client_path_or_query_param: Path/Query param that can defined on the client.

          client_query_param: Query param that can be defined on the client.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        client_client_path_or_query_param = self._client._get_client_path_or_query_param_query_param()
        if not is_given(client_path_or_query_param) and client_client_path_or_query_param is not None:
            client_path_or_query_param = client_client_path_or_query_param
        client_client_query_param = self._client._get_client_query_param_query_param()
        if not is_given(client_query_param) and client_client_query_param is not None:
            client_query_param = client_client_query_param
        return self._post(
            "/client_params/query_params",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
                query=maybe_transform(
                    {
                        "client_path_or_query_param": client_path_or_query_param,
                        "client_query_param": client_query_param,
                    },
                    client_param_with_query_param_params.ClientParamWithQueryParamParams,
                ),
            ),
            cast_to=ClientParamWithQueryParamResponse,
        )


class AsyncClientParamsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncClientParamsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncClientParamsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncClientParamsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncClientParamsResourceWithStreamingResponse(self)

    async def with_path_param(
        self,
        *,
        client_path_param: str | None = None,
        client_path_or_query_param: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ClientParamWithPathParamResponse:
        """
        The operation takes a path param that is able to be set at the client level.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if client_path_param is None:
            client_path_param = self._client._get_client_path_param_path_param()
        if not client_path_param:
            raise ValueError(f"Expected a non-empty value for `client_path_param` but received {client_path_param!r}")
        if client_path_or_query_param is None:
            client_path_or_query_param = self._client._get_client_path_or_query_param_path_param()
        if not client_path_or_query_param:
            raise ValueError(
                f"Expected a non-empty value for `client_path_or_query_param` but received {client_path_or_query_param!r}"
            )
        return await self._post(
            f"/client_params/path_params/{client_path_param}/{client_path_or_query_param}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ClientParamWithPathParamResponse,
        )

    async def with_path_param_and_standard(
        self,
        id: str,
        *,
        camel_cased_path: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ClientParamWithPathParamAndStandardResponse:
        """
        The operation takes a path param that is able to be set at the client level
        alongside a standard path param.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if camel_cased_path is None:
            camel_cased_path = self._client._get_camel_case_path_path_param()
        if not camel_cased_path:
            raise ValueError(f"Expected a non-empty value for `camel_cased_path` but received {camel_cased_path!r}")
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/client_params/path_params/{camel_cased_path}/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ClientParamWithPathParamAndStandardResponse,
        )

    async def with_query_param(
        self,
        *,
        client_path_or_query_param: str | NotGiven = not_given,
        client_query_param: str | NotGiven = not_given,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ClientParamWithQueryParamResponse:
        """
        The operation takes a query param that is able to be set at the client level.

        Args:
          client_path_or_query_param: Path/Query param that can defined on the client.

          client_query_param: Query param that can be defined on the client.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        client_client_path_or_query_param = self._client._get_client_path_or_query_param_query_param()
        if not is_given(client_path_or_query_param) and client_client_path_or_query_param is not None:
            client_path_or_query_param = client_client_path_or_query_param
        client_client_query_param = self._client._get_client_query_param_query_param()
        if not is_given(client_query_param) and client_client_query_param is not None:
            client_query_param = client_client_query_param
        return await self._post(
            "/client_params/query_params",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
                query=await async_maybe_transform(
                    {
                        "client_path_or_query_param": client_path_or_query_param,
                        "client_query_param": client_query_param,
                    },
                    client_param_with_query_param_params.ClientParamWithQueryParamParams,
                ),
            ),
            cast_to=ClientParamWithQueryParamResponse,
        )


class ClientParamsResourceWithRawResponse:
    def __init__(self, client_params: ClientParamsResource) -> None:
        self._client_params = client_params

        self.with_path_param = _legacy_response.to_raw_response_wrapper(
            client_params.with_path_param,
        )
        self.with_path_param_and_standard = _legacy_response.to_raw_response_wrapper(
            client_params.with_path_param_and_standard,
        )
        self.with_query_param = _legacy_response.to_raw_response_wrapper(
            client_params.with_query_param,
        )


class AsyncClientParamsResourceWithRawResponse:
    def __init__(self, client_params: AsyncClientParamsResource) -> None:
        self._client_params = client_params

        self.with_path_param = _legacy_response.async_to_raw_response_wrapper(
            client_params.with_path_param,
        )
        self.with_path_param_and_standard = _legacy_response.async_to_raw_response_wrapper(
            client_params.with_path_param_and_standard,
        )
        self.with_query_param = _legacy_response.async_to_raw_response_wrapper(
            client_params.with_query_param,
        )


class ClientParamsResourceWithStreamingResponse:
    def __init__(self, client_params: ClientParamsResource) -> None:
        self._client_params = client_params

        self.with_path_param = to_streamed_response_wrapper(
            client_params.with_path_param,
        )
        self.with_path_param_and_standard = to_streamed_response_wrapper(
            client_params.with_path_param_and_standard,
        )
        self.with_query_param = to_streamed_response_wrapper(
            client_params.with_query_param,
        )


class AsyncClientParamsResourceWithStreamingResponse:
    def __init__(self, client_params: AsyncClientParamsResource) -> None:
        self._client_params = client_params

        self.with_path_param = async_to_streamed_response_wrapper(
            client_params.with_path_param,
        )
        self.with_path_param_and_standard = async_to_streamed_response_wrapper(
            client_params.with_path_param_and_standard,
        )
        self.with_query_param = async_to_streamed_response_wrapper(
            client_params.with_query_param,
        )
