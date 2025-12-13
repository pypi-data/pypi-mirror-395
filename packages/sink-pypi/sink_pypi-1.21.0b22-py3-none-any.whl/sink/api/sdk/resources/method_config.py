# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from .. import _legacy_response
from ..types import method_config_should_not_show_up_in_api_docs_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ..types.card import Card
from .._base_client import make_request_options
from ..types.shared_params.shipping_address import ShippingAddress
from ..types.method_config_skipped_tests_go_response import MethodConfigSkippedTestsGoResponse
from ..types.method_config_skipped_tests_all_response import MethodConfigSkippedTestsAllResponse
from ..types.method_config_skipped_tests_java_response import MethodConfigSkippedTestsJavaResponse
from ..types.method_config_skipped_tests_node_response import MethodConfigSkippedTestsNodeResponse
from ..types.method_config_skipped_tests_ruby_response import MethodConfigSkippedTestsRubyResponse
from ..types.method_config_skipped_tests_kotlin_response import MethodConfigSkippedTestsKotlinResponse
from ..types.method_config_skipped_tests_python_response import MethodConfigSkippedTestsPythonResponse
from ..types.method_config_skipped_tests_node_and_python_response import MethodConfigSkippedTestsNodeAndPythonResponse

__all__ = ["MethodConfigResource", "AsyncMethodConfigResource"]


class MethodConfigResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MethodConfigResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return MethodConfigResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MethodConfigResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return MethodConfigResourceWithStreamingResponse(self)

    def should_not_show_up_in_api_docs(
        self,
        card_token: str,
        *,
        product_id: str | Omit = omit,
        shipping_method: Literal["STANDARD", "STANDARD_WITH_TRACKING", "EXPEDITED"] | Omit = omit,
        shipping_address: ShippingAddress | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Card:
        """
        Initiate print and shipment of a duplicate card.

        Only applies to cards of type `PHYSICAL` [beta].

        Args:
          product_id: Specifies the configuration (e.g. physical card art) that the card should be
              manufactured with, and only applies to cards of type `PHYSICAL` [beta]. This
              must be configured with Lithic before use.

          shipping_method: Shipping method for the card. Use of options besides `STANDARD` require
              additional permissions.

              - `STANDARD` - USPS regular mail or similar international option, with no
                tracking
              - `STANDARD_WITH_TRACKING` - USPS regular mail or similar international option,
                with tracking
              - `EXPEDITED` - FedEx Standard Overnight or similar international option, with
                tracking

          shipping_address: If omitted, the previous shipping address will be used.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not card_token:
            raise ValueError(f"Expected a non-empty value for `card_token` but received {card_token!r}")
        return self._post(
            f"/cards/{card_token}/reissue",
            body=maybe_transform(
                {
                    "product_id": product_id,
                    "shipping_method": shipping_method,
                    "shipping_address": shipping_address,
                },
                method_config_should_not_show_up_in_api_docs_params.MethodConfigShouldNotShowUpInAPIDocsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=Card,
        )

    def skipped_tests_all(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MethodConfigSkippedTestsAllResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsAllResponse,
        )

    def skipped_tests_go(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MethodConfigSkippedTestsGoResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsGoResponse,
        )

    def skipped_tests_java(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MethodConfigSkippedTestsJavaResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsJavaResponse,
        )

    def skipped_tests_kotlin(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MethodConfigSkippedTestsKotlinResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsKotlinResponse,
        )

    def skipped_tests_node(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MethodConfigSkippedTestsNodeResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsNodeResponse,
        )

    def skipped_tests_node_and_python(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MethodConfigSkippedTestsNodeAndPythonResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsNodeAndPythonResponse,
        )

    def skipped_tests_python(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MethodConfigSkippedTestsPythonResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsPythonResponse,
        )

    def skipped_tests_ruby(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MethodConfigSkippedTestsRubyResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsRubyResponse,
        )


class AsyncMethodConfigResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMethodConfigResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncMethodConfigResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMethodConfigResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncMethodConfigResourceWithStreamingResponse(self)

    async def should_not_show_up_in_api_docs(
        self,
        card_token: str,
        *,
        product_id: str | Omit = omit,
        shipping_method: Literal["STANDARD", "STANDARD_WITH_TRACKING", "EXPEDITED"] | Omit = omit,
        shipping_address: ShippingAddress | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Card:
        """
        Initiate print and shipment of a duplicate card.

        Only applies to cards of type `PHYSICAL` [beta].

        Args:
          product_id: Specifies the configuration (e.g. physical card art) that the card should be
              manufactured with, and only applies to cards of type `PHYSICAL` [beta]. This
              must be configured with Lithic before use.

          shipping_method: Shipping method for the card. Use of options besides `STANDARD` require
              additional permissions.

              - `STANDARD` - USPS regular mail or similar international option, with no
                tracking
              - `STANDARD_WITH_TRACKING` - USPS regular mail or similar international option,
                with tracking
              - `EXPEDITED` - FedEx Standard Overnight or similar international option, with
                tracking

          shipping_address: If omitted, the previous shipping address will be used.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not card_token:
            raise ValueError(f"Expected a non-empty value for `card_token` but received {card_token!r}")
        return await self._post(
            f"/cards/{card_token}/reissue",
            body=await async_maybe_transform(
                {
                    "product_id": product_id,
                    "shipping_method": shipping_method,
                    "shipping_address": shipping_address,
                },
                method_config_should_not_show_up_in_api_docs_params.MethodConfigShouldNotShowUpInAPIDocsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=Card,
        )

    async def skipped_tests_all(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MethodConfigSkippedTestsAllResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsAllResponse,
        )

    async def skipped_tests_go(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MethodConfigSkippedTestsGoResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsGoResponse,
        )

    async def skipped_tests_java(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MethodConfigSkippedTestsJavaResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsJavaResponse,
        )

    async def skipped_tests_kotlin(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MethodConfigSkippedTestsKotlinResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsKotlinResponse,
        )

    async def skipped_tests_node(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MethodConfigSkippedTestsNodeResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsNodeResponse,
        )

    async def skipped_tests_node_and_python(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MethodConfigSkippedTestsNodeAndPythonResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsNodeAndPythonResponse,
        )

    async def skipped_tests_python(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MethodConfigSkippedTestsPythonResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsPythonResponse,
        )

    async def skipped_tests_ruby(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MethodConfigSkippedTestsRubyResponse:
        """
        Used to test skipping generated unit tests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/method_config/skipped_tests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MethodConfigSkippedTestsRubyResponse,
        )


class MethodConfigResourceWithRawResponse:
    def __init__(self, method_config: MethodConfigResource) -> None:
        self._method_config = method_config

        self.should_not_show_up_in_api_docs = _legacy_response.to_raw_response_wrapper(
            method_config.should_not_show_up_in_api_docs,
        )
        self.skipped_tests_all = _legacy_response.to_raw_response_wrapper(
            method_config.skipped_tests_all,
        )
        self.skipped_tests_go = _legacy_response.to_raw_response_wrapper(
            method_config.skipped_tests_go,
        )
        self.skipped_tests_java = _legacy_response.to_raw_response_wrapper(
            method_config.skipped_tests_java,
        )
        self.skipped_tests_kotlin = _legacy_response.to_raw_response_wrapper(
            method_config.skipped_tests_kotlin,
        )
        self.skipped_tests_node = _legacy_response.to_raw_response_wrapper(
            method_config.skipped_tests_node,
        )
        self.skipped_tests_node_and_python = _legacy_response.to_raw_response_wrapper(
            method_config.skipped_tests_node_and_python,
        )
        self.skipped_tests_python = _legacy_response.to_raw_response_wrapper(
            method_config.skipped_tests_python,
        )
        self.skipped_tests_ruby = _legacy_response.to_raw_response_wrapper(
            method_config.skipped_tests_ruby,
        )


class AsyncMethodConfigResourceWithRawResponse:
    def __init__(self, method_config: AsyncMethodConfigResource) -> None:
        self._method_config = method_config

        self.should_not_show_up_in_api_docs = _legacy_response.async_to_raw_response_wrapper(
            method_config.should_not_show_up_in_api_docs,
        )
        self.skipped_tests_all = _legacy_response.async_to_raw_response_wrapper(
            method_config.skipped_tests_all,
        )
        self.skipped_tests_go = _legacy_response.async_to_raw_response_wrapper(
            method_config.skipped_tests_go,
        )
        self.skipped_tests_java = _legacy_response.async_to_raw_response_wrapper(
            method_config.skipped_tests_java,
        )
        self.skipped_tests_kotlin = _legacy_response.async_to_raw_response_wrapper(
            method_config.skipped_tests_kotlin,
        )
        self.skipped_tests_node = _legacy_response.async_to_raw_response_wrapper(
            method_config.skipped_tests_node,
        )
        self.skipped_tests_node_and_python = _legacy_response.async_to_raw_response_wrapper(
            method_config.skipped_tests_node_and_python,
        )
        self.skipped_tests_python = _legacy_response.async_to_raw_response_wrapper(
            method_config.skipped_tests_python,
        )
        self.skipped_tests_ruby = _legacy_response.async_to_raw_response_wrapper(
            method_config.skipped_tests_ruby,
        )


class MethodConfigResourceWithStreamingResponse:
    def __init__(self, method_config: MethodConfigResource) -> None:
        self._method_config = method_config

        self.should_not_show_up_in_api_docs = to_streamed_response_wrapper(
            method_config.should_not_show_up_in_api_docs,
        )
        self.skipped_tests_all = to_streamed_response_wrapper(
            method_config.skipped_tests_all,
        )
        self.skipped_tests_go = to_streamed_response_wrapper(
            method_config.skipped_tests_go,
        )
        self.skipped_tests_java = to_streamed_response_wrapper(
            method_config.skipped_tests_java,
        )
        self.skipped_tests_kotlin = to_streamed_response_wrapper(
            method_config.skipped_tests_kotlin,
        )
        self.skipped_tests_node = to_streamed_response_wrapper(
            method_config.skipped_tests_node,
        )
        self.skipped_tests_node_and_python = to_streamed_response_wrapper(
            method_config.skipped_tests_node_and_python,
        )
        self.skipped_tests_python = to_streamed_response_wrapper(
            method_config.skipped_tests_python,
        )
        self.skipped_tests_ruby = to_streamed_response_wrapper(
            method_config.skipped_tests_ruby,
        )


class AsyncMethodConfigResourceWithStreamingResponse:
    def __init__(self, method_config: AsyncMethodConfigResource) -> None:
        self._method_config = method_config

        self.should_not_show_up_in_api_docs = async_to_streamed_response_wrapper(
            method_config.should_not_show_up_in_api_docs,
        )
        self.skipped_tests_all = async_to_streamed_response_wrapper(
            method_config.skipped_tests_all,
        )
        self.skipped_tests_go = async_to_streamed_response_wrapper(
            method_config.skipped_tests_go,
        )
        self.skipped_tests_java = async_to_streamed_response_wrapper(
            method_config.skipped_tests_java,
        )
        self.skipped_tests_kotlin = async_to_streamed_response_wrapper(
            method_config.skipped_tests_kotlin,
        )
        self.skipped_tests_node = async_to_streamed_response_wrapper(
            method_config.skipped_tests_node,
        )
        self.skipped_tests_node_and_python = async_to_streamed_response_wrapper(
            method_config.skipped_tests_node_and_python,
        )
        self.skipped_tests_python = async_to_streamed_response_wrapper(
            method_config.skipped_tests_python,
        )
        self.skipped_tests_ruby = async_to_streamed_response_wrapper(
            method_config.skipped_tests_ruby,
        )
