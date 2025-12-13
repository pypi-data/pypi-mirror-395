# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from .. import _legacy_response
from ..types import undocumented_resource_reissue_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ..types.card import Card
from .._base_client import make_request_options
from ..types.shared_params.shipping_address import ShippingAddress

__all__ = ["UndocumentedResourceResource", "AsyncUndocumentedResourceResource"]


class UndocumentedResourceResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> UndocumentedResourceResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return UndocumentedResourceResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UndocumentedResourceResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return UndocumentedResourceResourceWithStreamingResponse(self)

    def reissue(
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
                undocumented_resource_reissue_params.UndocumentedResourceReissueParams,
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


class AsyncUndocumentedResourceResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncUndocumentedResourceResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncUndocumentedResourceResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUndocumentedResourceResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncUndocumentedResourceResourceWithStreamingResponse(self)

    async def reissue(
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
                undocumented_resource_reissue_params.UndocumentedResourceReissueParams,
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


class UndocumentedResourceResourceWithRawResponse:
    def __init__(self, undocumented_resource: UndocumentedResourceResource) -> None:
        self._undocumented_resource = undocumented_resource

        self.reissue = _legacy_response.to_raw_response_wrapper(
            undocumented_resource.reissue,
        )


class AsyncUndocumentedResourceResourceWithRawResponse:
    def __init__(self, undocumented_resource: AsyncUndocumentedResourceResource) -> None:
        self._undocumented_resource = undocumented_resource

        self.reissue = _legacy_response.async_to_raw_response_wrapper(
            undocumented_resource.reissue,
        )


class UndocumentedResourceResourceWithStreamingResponse:
    def __init__(self, undocumented_resource: UndocumentedResourceResource) -> None:
        self._undocumented_resource = undocumented_resource

        self.reissue = to_streamed_response_wrapper(
            undocumented_resource.reissue,
        )


class AsyncUndocumentedResourceResourceWithStreamingResponse:
    def __init__(self, undocumented_resource: AsyncUndocumentedResourceResource) -> None:
        self._undocumented_resource = undocumented_resource

        self.reissue = async_to_streamed_response_wrapper(
            undocumented_resource.reissue,
        )
