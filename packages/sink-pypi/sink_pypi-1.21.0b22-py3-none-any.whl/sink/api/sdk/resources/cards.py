# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions
from typing import Union
from datetime import datetime
from typing_extensions import Literal

import httpx

from .. import _legacy_response
from ..types import (
    card_list_params,
    card_create_params,
    card_update_params,
    card_reissue_params,
    card_provision_foo_params,
)
from .._types import Body, Omit, Query, Headers, NoneType, NotGiven, Base64FileInput, omit, not_given
from .._utils import is_given, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from .._constants import DEFAULT_TIMEOUT
from ..types.card import Card
from .._base_client import make_request_options
from ..types.card_list_response import CardListResponse
from ..types.card_provision_foo_response import CardProvisionFooResponse
from ..types.shared_params.shipping_address import ShippingAddress

__all__ = ["CardsResource", "AsyncCardsResource"]


class CardsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CardsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return CardsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CardsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return CardsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        type: Literal["MERCHANT_LOCKED", "PHYSICAL", "SINGLE_USE", "VIRTUAL"],
        account_token: str | Omit = omit,
        card_program_token: str | Omit = omit,
        exp_month: str | Omit = omit,
        exp_year: str | Omit = omit,
        funding_token: str | Omit = omit,
        memo: str | Omit = omit,
        not_: str | Omit = omit,
        pin: str | Omit = omit,
        product_id: str | Omit = omit,
        shipping_method: Literal["STANDARD", "STANDARD_WITH_TRACKING", "EXPEDITED"] | Omit = omit,
        shipping_address: ShippingAddress | Omit = omit,
        spend_limit: int | Omit = omit,
        spend_limit_duration: Literal["ANNUALLY", "FOREVER", "MONTHLY", "TRANSACTION"] | Omit = omit,
        state: Literal["OPEN", "PAUSED"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Card:
        """Create a new virtual or physical card.

        Parameters `pin`, `shippingAddress`, and
        `product_id` only apply to physical cards.

        Args:
          type:
              Card types:

              - `MERCHANT_LOCKED` - Card is locked to first merchant that successfully
                authorizes the card.
              - `PHYSICAL` - Manufactured and sent to the cardholder. We offer white label
                branding, credit, ATM, PIN debit, chip/EMV, NFC and magstripe functionality.
                Reach out at [lithic.com/contact](https://lithic.com/contact) for more
                information.
              - `SINGLE_USE` - Card will close shortly after the first transaction.
              - `VIRTUAL` - Card will authorize at any merchant and can be added to a digital
                wallet like Apple Pay or Google Pay (if the card program is digital
                wallet-enabled).

          account_token: Only required for multi-account users. Token identifying the account the card
              will be associated with. Only applicable if using account holder enrollment. See
              [Managing Your Program](https://docs.lithic.com/docs/managing-your-program) for
              more information.

          card_program_token: Identifies the card program under which to create the card. Different card
              programs may have their own configurations (e.g., digital wallet card art, BIN
              type). This must be configured with Lithic before use.

          exp_month: Two digit (MM) expiry month. If neither `exp_month` nor `exp_year` is provided,
              an expiration date will be generated.

          exp_year: Four digit (yyyy) expiry year. If neither `exp_month` nor `exp_year` is
              provided, an expiration date will be generated.

          funding_token: The token for the desired `FundingAccount` to use when making transactions with
              this card.

          memo: Friendly name to identify the card.

          not_: Used to test the PythonSDKs ability to handle reserved keywords as parameters

          pin: Encrypted PIN block (in base64). Only applies to cards of type `PHYSICAL` and
              `VIRTUAL`. See
              [Encrypted PIN Block](https://docs.lithic.com/docs/cards#encrypted-pin-block-enterprise).

          product_id: Specifies the configuration (e.g., physical card art) that the card should be
              manufactured with, and only applies to cards of type `PHYSICAL` [beta]. This
              must be configured with Lithic before use.

          shipping_method: Shipping method for the card. Only applies to cards of type PHYSICAL [beta]. Use
              of options besides `STANDARD` require additional permissions.

              - `STANDARD` - USPS regular mail or similar international option, with no
                tracking
              - `STANDARD_WITH_TRACKING` - USPS regular mail or similar international option,
                with tracking
              - `EXPEDITED` - FedEx Standard Overnight or similar international option, with
                tracking

          spend_limit: Amount (in cents) to limit approved authorizations. Transaction requests above
              the spend limit will be declined.

          spend_limit_duration:
              Spend limit duration values:

              - `ANNUALLY` - Card will authorize transactions up to spend limit in a calendar
                year.
              - `FOREVER` - Card will authorize only up to spend limit for the entire lifetime
                of the card.
              - `MONTHLY` - Card will authorize transactions up to spend limit for the
                trailing month. Month is calculated as this calendar date one month prior.
              - `TRANSACTION` - Card will authorizate multiple transactions if each individual
                transaction is under the spend limit.

          state:
              Card state values:

              - `OPEN` - Card will approve authorizations (if they match card and account
                parameters).
              - `PAUSED` - Card will decline authorizations, but can be resumed at a later
                time.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not is_given(timeout) and self._client.timeout == DEFAULT_TIMEOUT:
            timeout = 2
        return self._post(
            "/cards",
            body=maybe_transform(
                {
                    "type": type,
                    "account_token": account_token,
                    "card_program_token": card_program_token,
                    "exp_month": exp_month,
                    "exp_year": exp_year,
                    "funding_token": funding_token,
                    "memo": memo,
                    "not_": not_,
                    "pin": pin,
                    "product_id": product_id,
                    "shipping_method": shipping_method,
                    "shipping_address": shipping_address,
                    "spend_limit": spend_limit,
                    "spend_limit_duration": spend_limit_duration,
                    "state": state,
                },
                card_create_params.CardCreateParams,
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

    def retrieve(
        self,
        card_token: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Card:
        """
        Get card configuration such as spend limit and state.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not card_token:
            raise ValueError(f"Expected a non-empty value for `card_token` but received {card_token!r}")
        return self._get(
            f"/cards/{card_token}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Card,
        )

    def update(
        self,
        card_token: str,
        *,
        account_token: str | Omit = omit,
        auth_rule_token: str | Omit = omit,
        funding_token: str | Omit = omit,
        memo: str | Omit = omit,
        pin: str | Omit = omit,
        spend_limit: int | Omit = omit,
        spend_limit_duration: Literal["ANNUALLY", "FOREVER", "MONTHLY", "TRANSACTION"] | Omit = omit,
        state: Literal["CLOSED", "OPEN", "PAUSED"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Card:
        """Update the specified properties of the card.

        Unsupplied properties will remain
        unchanged. `pin` parameter only applies to physical cards.

        _Note: setting a card to a `CLOSED` state is a final action that cannot be
        undone._

        Args:
          account_token: Only required for multi-account users. Token identifying the account the card
              will be associated with. Only applicable if using account holder enrollment. See
              [Managing Your Program](https://docs.lithic.com/docs/managing-your-program) for
              more information.

          auth_rule_token: Identifier for any Auth Rules that will be applied to transactions taking place
              with the card.

          funding_token: The token for the desired `FundingAccount` to use when making transactions with
              this card.

          memo: Friendly name to identify the card.

          pin: Encrypted PIN block (in base64). Only applies to cards of type `PHYSICAL` and
              `VIRTUAL`. See
              [Encrypted PIN Block](https://docs.lithic.com/docs/cards#encrypted-pin-block-enterprise).

          spend_limit: Amount (in cents) to limit approved authorizations. Transaction requests above
              the spend limit will be declined.

          spend_limit_duration:
              Spend limit duration values:

              - `ANNUALLY` - Card will authorize transactions up to spend limit in a calendar
                year.
              - `FOREVER` - Card will authorize only up to spend limit for the entire lifetime
                of the card.
              - `MONTHLY` - Card will authorize transactions up to spend limit for the
                trailing month. Month is calculated as this calendar date one month prior.
              - `TRANSACTION` - Card will authorizate multiple transactions if each individual
                transaction is under the spend limit.

          state:
              Card state values:

              - `CLOSED` - Card will no longer approve authorizations. Closing a card cannot
                be undone.
              - `OPEN` - Card will approve authorizations (if they match card and account
                parameters).
              - `PAUSED` - Card will decline authorizations, but can be resumed at a later
                time.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not card_token:
            raise ValueError(f"Expected a non-empty value for `card_token` but received {card_token!r}")
        return self._patch(
            f"/cards/{card_token}",
            body=maybe_transform(
                {
                    "account_token": account_token,
                    "auth_rule_token": auth_rule_token,
                    "funding_token": funding_token,
                    "memo": memo,
                    "pin": pin,
                    "spend_limit": spend_limit,
                    "spend_limit_duration": spend_limit_duration,
                    "state": state,
                },
                card_update_params.CardUpdateParams,
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

    def list(
        self,
        *,
        begin: Union[str, datetime],
        end: Union[str, datetime],
        account_token: str | Omit = omit,
        page: int | Omit = omit,
        page_size: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CardListResponse:
        """List cards.

        Args:
          begin: Date string in 8601 format.

        Only entries created after the specified date will
              be included. UTC time zone.

          end: Date string in 8601 format. Only entries created before the specified date will
              be included. UTC time zone.

          account_token: Only required for multi-account users. Returns cards associated with this
              account. Only applicable if using account holder enrollment. See
              [Managing Your Program](https://docs.lithic.com/docs/managing-your-program) for
              more information.

          page: Page (for pagination).

          page_size: Page size (for pagination).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/cards",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "begin": begin,
                        "end": end,
                        "account_token": account_token,
                        "page": page,
                        "page_size": page_size,
                    },
                    card_list_params.CardListParams,
                ),
            ),
            cast_to=CardListResponse,
        )

    create_aliased = create

    @typing_extensions.deprecated("try with deprecation")
    def create_aliased_deprecated(
        self,
        *,
        type: Literal["MERCHANT_LOCKED", "PHYSICAL", "SINGLE_USE", "VIRTUAL"],
        account_token: str | Omit = omit,
        card_program_token: str | Omit = omit,
        exp_month: str | Omit = omit,
        exp_year: str | Omit = omit,
        funding_token: str | Omit = omit,
        memo: str | Omit = omit,
        not_: str | Omit = omit,
        pin: str | Omit = omit,
        product_id: str | Omit = omit,
        shipping_method: Literal["STANDARD", "STANDARD_WITH_TRACKING", "EXPEDITED"] | Omit = omit,
        shipping_address: ShippingAddress | Omit = omit,
        spend_limit: int | Omit = omit,
        spend_limit_duration: Literal["ANNUALLY", "FOREVER", "MONTHLY", "TRANSACTION"] | Omit = omit,
        state: Literal["OPEN", "PAUSED"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Card:
        """Create a new virtual or physical card.

        Parameters `pin`, `shippingAddress`, and
        `product_id` only apply to physical cards.

        Args:
          type:
              Card types:

              - `MERCHANT_LOCKED` - Card is locked to first merchant that successfully
                authorizes the card.
              - `PHYSICAL` - Manufactured and sent to the cardholder. We offer white label
                branding, credit, ATM, PIN debit, chip/EMV, NFC and magstripe functionality.
                Reach out at [lithic.com/contact](https://lithic.com/contact) for more
                information.
              - `SINGLE_USE` - Card will close shortly after the first transaction.
              - `VIRTUAL` - Card will authorize at any merchant and can be added to a digital
                wallet like Apple Pay or Google Pay (if the card program is digital
                wallet-enabled).

          account_token: Only required for multi-account users. Token identifying the account the card
              will be associated with. Only applicable if using account holder enrollment. See
              [Managing Your Program](https://docs.lithic.com/docs/managing-your-program) for
              more information.

          card_program_token: Identifies the card program under which to create the card. Different card
              programs may have their own configurations (e.g., digital wallet card art, BIN
              type). This must be configured with Lithic before use.

          exp_month: Two digit (MM) expiry month. If neither `exp_month` nor `exp_year` is provided,
              an expiration date will be generated.

          exp_year: Four digit (yyyy) expiry year. If neither `exp_month` nor `exp_year` is
              provided, an expiration date will be generated.

          funding_token: The token for the desired `FundingAccount` to use when making transactions with
              this card.

          memo: Friendly name to identify the card.

          not_: Used to test the PythonSDKs ability to handle reserved keywords as parameters

          pin: Encrypted PIN block (in base64). Only applies to cards of type `PHYSICAL` and
              `VIRTUAL`. See
              [Encrypted PIN Block](https://docs.lithic.com/docs/cards#encrypted-pin-block-enterprise).

          product_id: Specifies the configuration (e.g., physical card art) that the card should be
              manufactured with, and only applies to cards of type `PHYSICAL` [beta]. This
              must be configured with Lithic before use.

          shipping_method: Shipping method for the card. Only applies to cards of type PHYSICAL [beta]. Use
              of options besides `STANDARD` require additional permissions.

              - `STANDARD` - USPS regular mail or similar international option, with no
                tracking
              - `STANDARD_WITH_TRACKING` - USPS regular mail or similar international option,
                with tracking
              - `EXPEDITED` - FedEx Standard Overnight or similar international option, with
                tracking

          spend_limit: Amount (in cents) to limit approved authorizations. Transaction requests above
              the spend limit will be declined.

          spend_limit_duration:
              Spend limit duration values:

              - `ANNUALLY` - Card will authorize transactions up to spend limit in a calendar
                year.
              - `FOREVER` - Card will authorize only up to spend limit for the entire lifetime
                of the card.
              - `MONTHLY` - Card will authorize transactions up to spend limit for the
                trailing month. Month is calculated as this calendar date one month prior.
              - `TRANSACTION` - Card will authorizate multiple transactions if each individual
                transaction is under the spend limit.

          state:
              Card state values:

              - `OPEN` - Card will approve authorizations (if they match card and account
                parameters).
              - `PAUSED` - Card will decline authorizations, but can be resumed at a later
                time.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self.create(
            type=type,
            account_token=account_token,
            card_program_token=card_program_token,
            exp_month=exp_month,
            exp_year=exp_year,
            funding_token=funding_token,
            memo=memo,
            not_=not_,
            pin=pin,
            product_id=product_id,
            shipping_method=shipping_method,
            shipping_address=shipping_address,
            spend_limit=spend_limit,
            spend_limit_duration=spend_limit_duration,
            state=state,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )

    @typing_extensions.deprecated("do deprecate me not in go")
    def deprecated_all_but_go_diff_message(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint that represents a method that has been marked as deprecated in the
        stainless config for all languages, but with a different method in go.
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/deprecations/method_all_but_go_diff_message",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    @typing_extensions.deprecated("do deprecate me in python")
    def deprecated_all_diff_message(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint that represents a method that has been marked as deprecated in the
        stainless config for all languages, but with a different method in go.
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/deprecations/method_all_but_go_diff_message",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    @typing_extensions.deprecated("This method has been deprecated.\n\nIt will be removed in v0.99.0\n")
    def deprecated_method(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint that represents a method that has been marked as deprecated in the
        stainless config.
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/deprecations/method",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def deprecated_only_go(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint that represents a method that has been marked as deprecated in the
        stainless config for go only.
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/deprecations/method_only_go",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def list_not_paginated(
        self,
        card_token: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Card:
        """
        Get card configuration such as spend limit and state.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not card_token:
            raise ValueError(f"Expected a non-empty value for `card_token` but received {card_token!r}")
        return self._get(
            f"/cards/{card_token}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Card,
        )

    def provision_foo(
        self,
        card_token: str,
        *,
        account_token: str | Omit = omit,
        certificate: Union[str, Base64FileInput] | Omit = omit,
        digital_wallet: Literal["APPLE_PAY", "GOOGLE_PAY", "SAMSUNG_PAY"] | Omit = omit,
        nonce: Union[str, Base64FileInput] | Omit = omit,
        nonce_signature: Union[str, Base64FileInput] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> CardProvisionFooResponse:
        """
        Allow your cardholders to directly add payment cards to the device's digital
        wallet (e.g. Apple Pay) with one touch from your app.

        This requires some additional setup and configuration. Please
        [Contact Us](https://lithic.com/contact) or your Customer Success representative
        for more information.

        Args:
          account_token: Only required for multi-account users. Token identifying the account the card
              will be associated with. Only applicable if using account holder enrollment. See
              [Managing Your Program](https://docs.lithic.com/docs/managing-your-program) for
              more information.

          certificate: Required for `APPLE_PAY`. Apple's public leaf certificate. Base64 encoded in PEM
              format with headers `(-----BEGIN CERTIFICATE-----)` and trailers omitted.
              Provided by the device's wallet.

          digital_wallet: Name of digital wallet provider.

          nonce: Required for `APPLE_PAY`. Base64 cryptographic nonce provided by the device's
              wallet.

          nonce_signature: Required for `APPLE_PAY`. Base64 cryptographic nonce provided by the device's
              wallet.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not card_token:
            raise ValueError(f"Expected a non-empty value for `card_token` but received {card_token!r}")
        return self._post(
            f"/cards/{card_token}/provision",
            body=maybe_transform(
                {
                    "account_token": account_token,
                    "certificate": certificate,
                    "digital_wallet": digital_wallet,
                    "nonce": nonce,
                    "nonce_signature": nonce_signature,
                },
                card_provision_foo_params.CardProvisionFooParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=CardProvisionFooResponse,
        )

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
                card_reissue_params.CardReissueParams,
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


class AsyncCardsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCardsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncCardsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCardsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncCardsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        type: Literal["MERCHANT_LOCKED", "PHYSICAL", "SINGLE_USE", "VIRTUAL"],
        account_token: str | Omit = omit,
        card_program_token: str | Omit = omit,
        exp_month: str | Omit = omit,
        exp_year: str | Omit = omit,
        funding_token: str | Omit = omit,
        memo: str | Omit = omit,
        not_: str | Omit = omit,
        pin: str | Omit = omit,
        product_id: str | Omit = omit,
        shipping_method: Literal["STANDARD", "STANDARD_WITH_TRACKING", "EXPEDITED"] | Omit = omit,
        shipping_address: ShippingAddress | Omit = omit,
        spend_limit: int | Omit = omit,
        spend_limit_duration: Literal["ANNUALLY", "FOREVER", "MONTHLY", "TRANSACTION"] | Omit = omit,
        state: Literal["OPEN", "PAUSED"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Card:
        """Create a new virtual or physical card.

        Parameters `pin`, `shippingAddress`, and
        `product_id` only apply to physical cards.

        Args:
          type:
              Card types:

              - `MERCHANT_LOCKED` - Card is locked to first merchant that successfully
                authorizes the card.
              - `PHYSICAL` - Manufactured and sent to the cardholder. We offer white label
                branding, credit, ATM, PIN debit, chip/EMV, NFC and magstripe functionality.
                Reach out at [lithic.com/contact](https://lithic.com/contact) for more
                information.
              - `SINGLE_USE` - Card will close shortly after the first transaction.
              - `VIRTUAL` - Card will authorize at any merchant and can be added to a digital
                wallet like Apple Pay or Google Pay (if the card program is digital
                wallet-enabled).

          account_token: Only required for multi-account users. Token identifying the account the card
              will be associated with. Only applicable if using account holder enrollment. See
              [Managing Your Program](https://docs.lithic.com/docs/managing-your-program) for
              more information.

          card_program_token: Identifies the card program under which to create the card. Different card
              programs may have their own configurations (e.g., digital wallet card art, BIN
              type). This must be configured with Lithic before use.

          exp_month: Two digit (MM) expiry month. If neither `exp_month` nor `exp_year` is provided,
              an expiration date will be generated.

          exp_year: Four digit (yyyy) expiry year. If neither `exp_month` nor `exp_year` is
              provided, an expiration date will be generated.

          funding_token: The token for the desired `FundingAccount` to use when making transactions with
              this card.

          memo: Friendly name to identify the card.

          not_: Used to test the PythonSDKs ability to handle reserved keywords as parameters

          pin: Encrypted PIN block (in base64). Only applies to cards of type `PHYSICAL` and
              `VIRTUAL`. See
              [Encrypted PIN Block](https://docs.lithic.com/docs/cards#encrypted-pin-block-enterprise).

          product_id: Specifies the configuration (e.g., physical card art) that the card should be
              manufactured with, and only applies to cards of type `PHYSICAL` [beta]. This
              must be configured with Lithic before use.

          shipping_method: Shipping method for the card. Only applies to cards of type PHYSICAL [beta]. Use
              of options besides `STANDARD` require additional permissions.

              - `STANDARD` - USPS regular mail or similar international option, with no
                tracking
              - `STANDARD_WITH_TRACKING` - USPS regular mail or similar international option,
                with tracking
              - `EXPEDITED` - FedEx Standard Overnight or similar international option, with
                tracking

          spend_limit: Amount (in cents) to limit approved authorizations. Transaction requests above
              the spend limit will be declined.

          spend_limit_duration:
              Spend limit duration values:

              - `ANNUALLY` - Card will authorize transactions up to spend limit in a calendar
                year.
              - `FOREVER` - Card will authorize only up to spend limit for the entire lifetime
                of the card.
              - `MONTHLY` - Card will authorize transactions up to spend limit for the
                trailing month. Month is calculated as this calendar date one month prior.
              - `TRANSACTION` - Card will authorizate multiple transactions if each individual
                transaction is under the spend limit.

          state:
              Card state values:

              - `OPEN` - Card will approve authorizations (if they match card and account
                parameters).
              - `PAUSED` - Card will decline authorizations, but can be resumed at a later
                time.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not is_given(timeout) and self._client.timeout == DEFAULT_TIMEOUT:
            timeout = 2
        return await self._post(
            "/cards",
            body=await async_maybe_transform(
                {
                    "type": type,
                    "account_token": account_token,
                    "card_program_token": card_program_token,
                    "exp_month": exp_month,
                    "exp_year": exp_year,
                    "funding_token": funding_token,
                    "memo": memo,
                    "not_": not_,
                    "pin": pin,
                    "product_id": product_id,
                    "shipping_method": shipping_method,
                    "shipping_address": shipping_address,
                    "spend_limit": spend_limit,
                    "spend_limit_duration": spend_limit_duration,
                    "state": state,
                },
                card_create_params.CardCreateParams,
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

    async def retrieve(
        self,
        card_token: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Card:
        """
        Get card configuration such as spend limit and state.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not card_token:
            raise ValueError(f"Expected a non-empty value for `card_token` but received {card_token!r}")
        return await self._get(
            f"/cards/{card_token}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Card,
        )

    async def update(
        self,
        card_token: str,
        *,
        account_token: str | Omit = omit,
        auth_rule_token: str | Omit = omit,
        funding_token: str | Omit = omit,
        memo: str | Omit = omit,
        pin: str | Omit = omit,
        spend_limit: int | Omit = omit,
        spend_limit_duration: Literal["ANNUALLY", "FOREVER", "MONTHLY", "TRANSACTION"] | Omit = omit,
        state: Literal["CLOSED", "OPEN", "PAUSED"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Card:
        """Update the specified properties of the card.

        Unsupplied properties will remain
        unchanged. `pin` parameter only applies to physical cards.

        _Note: setting a card to a `CLOSED` state is a final action that cannot be
        undone._

        Args:
          account_token: Only required for multi-account users. Token identifying the account the card
              will be associated with. Only applicable if using account holder enrollment. See
              [Managing Your Program](https://docs.lithic.com/docs/managing-your-program) for
              more information.

          auth_rule_token: Identifier for any Auth Rules that will be applied to transactions taking place
              with the card.

          funding_token: The token for the desired `FundingAccount` to use when making transactions with
              this card.

          memo: Friendly name to identify the card.

          pin: Encrypted PIN block (in base64). Only applies to cards of type `PHYSICAL` and
              `VIRTUAL`. See
              [Encrypted PIN Block](https://docs.lithic.com/docs/cards#encrypted-pin-block-enterprise).

          spend_limit: Amount (in cents) to limit approved authorizations. Transaction requests above
              the spend limit will be declined.

          spend_limit_duration:
              Spend limit duration values:

              - `ANNUALLY` - Card will authorize transactions up to spend limit in a calendar
                year.
              - `FOREVER` - Card will authorize only up to spend limit for the entire lifetime
                of the card.
              - `MONTHLY` - Card will authorize transactions up to spend limit for the
                trailing month. Month is calculated as this calendar date one month prior.
              - `TRANSACTION` - Card will authorizate multiple transactions if each individual
                transaction is under the spend limit.

          state:
              Card state values:

              - `CLOSED` - Card will no longer approve authorizations. Closing a card cannot
                be undone.
              - `OPEN` - Card will approve authorizations (if they match card and account
                parameters).
              - `PAUSED` - Card will decline authorizations, but can be resumed at a later
                time.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not card_token:
            raise ValueError(f"Expected a non-empty value for `card_token` but received {card_token!r}")
        return await self._patch(
            f"/cards/{card_token}",
            body=await async_maybe_transform(
                {
                    "account_token": account_token,
                    "auth_rule_token": auth_rule_token,
                    "funding_token": funding_token,
                    "memo": memo,
                    "pin": pin,
                    "spend_limit": spend_limit,
                    "spend_limit_duration": spend_limit_duration,
                    "state": state,
                },
                card_update_params.CardUpdateParams,
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

    async def list(
        self,
        *,
        begin: Union[str, datetime],
        end: Union[str, datetime],
        account_token: str | Omit = omit,
        page: int | Omit = omit,
        page_size: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CardListResponse:
        """List cards.

        Args:
          begin: Date string in 8601 format.

        Only entries created after the specified date will
              be included. UTC time zone.

          end: Date string in 8601 format. Only entries created before the specified date will
              be included. UTC time zone.

          account_token: Only required for multi-account users. Returns cards associated with this
              account. Only applicable if using account holder enrollment. See
              [Managing Your Program](https://docs.lithic.com/docs/managing-your-program) for
              more information.

          page: Page (for pagination).

          page_size: Page size (for pagination).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/cards",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "begin": begin,
                        "end": end,
                        "account_token": account_token,
                        "page": page,
                        "page_size": page_size,
                    },
                    card_list_params.CardListParams,
                ),
            ),
            cast_to=CardListResponse,
        )

    create_aliased = create

    @typing_extensions.deprecated("try with deprecation")
    async def create_aliased_deprecated(
        self,
        *,
        type: Literal["MERCHANT_LOCKED", "PHYSICAL", "SINGLE_USE", "VIRTUAL"],
        account_token: str | Omit = omit,
        card_program_token: str | Omit = omit,
        exp_month: str | Omit = omit,
        exp_year: str | Omit = omit,
        funding_token: str | Omit = omit,
        memo: str | Omit = omit,
        not_: str | Omit = omit,
        pin: str | Omit = omit,
        product_id: str | Omit = omit,
        shipping_method: Literal["STANDARD", "STANDARD_WITH_TRACKING", "EXPEDITED"] | Omit = omit,
        shipping_address: ShippingAddress | Omit = omit,
        spend_limit: int | Omit = omit,
        spend_limit_duration: Literal["ANNUALLY", "FOREVER", "MONTHLY", "TRANSACTION"] | Omit = omit,
        state: Literal["OPEN", "PAUSED"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Card:
        """Create a new virtual or physical card.

        Parameters `pin`, `shippingAddress`, and
        `product_id` only apply to physical cards.

        Args:
          type:
              Card types:

              - `MERCHANT_LOCKED` - Card is locked to first merchant that successfully
                authorizes the card.
              - `PHYSICAL` - Manufactured and sent to the cardholder. We offer white label
                branding, credit, ATM, PIN debit, chip/EMV, NFC and magstripe functionality.
                Reach out at [lithic.com/contact](https://lithic.com/contact) for more
                information.
              - `SINGLE_USE` - Card will close shortly after the first transaction.
              - `VIRTUAL` - Card will authorize at any merchant and can be added to a digital
                wallet like Apple Pay or Google Pay (if the card program is digital
                wallet-enabled).

          account_token: Only required for multi-account users. Token identifying the account the card
              will be associated with. Only applicable if using account holder enrollment. See
              [Managing Your Program](https://docs.lithic.com/docs/managing-your-program) for
              more information.

          card_program_token: Identifies the card program under which to create the card. Different card
              programs may have their own configurations (e.g., digital wallet card art, BIN
              type). This must be configured with Lithic before use.

          exp_month: Two digit (MM) expiry month. If neither `exp_month` nor `exp_year` is provided,
              an expiration date will be generated.

          exp_year: Four digit (yyyy) expiry year. If neither `exp_month` nor `exp_year` is
              provided, an expiration date will be generated.

          funding_token: The token for the desired `FundingAccount` to use when making transactions with
              this card.

          memo: Friendly name to identify the card.

          not_: Used to test the PythonSDKs ability to handle reserved keywords as parameters

          pin: Encrypted PIN block (in base64). Only applies to cards of type `PHYSICAL` and
              `VIRTUAL`. See
              [Encrypted PIN Block](https://docs.lithic.com/docs/cards#encrypted-pin-block-enterprise).

          product_id: Specifies the configuration (e.g., physical card art) that the card should be
              manufactured with, and only applies to cards of type `PHYSICAL` [beta]. This
              must be configured with Lithic before use.

          shipping_method: Shipping method for the card. Only applies to cards of type PHYSICAL [beta]. Use
              of options besides `STANDARD` require additional permissions.

              - `STANDARD` - USPS regular mail or similar international option, with no
                tracking
              - `STANDARD_WITH_TRACKING` - USPS regular mail or similar international option,
                with tracking
              - `EXPEDITED` - FedEx Standard Overnight or similar international option, with
                tracking

          spend_limit: Amount (in cents) to limit approved authorizations. Transaction requests above
              the spend limit will be declined.

          spend_limit_duration:
              Spend limit duration values:

              - `ANNUALLY` - Card will authorize transactions up to spend limit in a calendar
                year.
              - `FOREVER` - Card will authorize only up to spend limit for the entire lifetime
                of the card.
              - `MONTHLY` - Card will authorize transactions up to spend limit for the
                trailing month. Month is calculated as this calendar date one month prior.
              - `TRANSACTION` - Card will authorizate multiple transactions if each individual
                transaction is under the spend limit.

          state:
              Card state values:

              - `OPEN` - Card will approve authorizations (if they match card and account
                parameters).
              - `PAUSED` - Card will decline authorizations, but can be resumed at a later
                time.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self.create(
            type=type,
            account_token=account_token,
            card_program_token=card_program_token,
            exp_month=exp_month,
            exp_year=exp_year,
            funding_token=funding_token,
            memo=memo,
            not_=not_,
            pin=pin,
            product_id=product_id,
            shipping_method=shipping_method,
            shipping_address=shipping_address,
            spend_limit=spend_limit,
            spend_limit_duration=spend_limit_duration,
            state=state,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )

    @typing_extensions.deprecated("do deprecate me not in go")
    async def deprecated_all_but_go_diff_message(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint that represents a method that has been marked as deprecated in the
        stainless config for all languages, but with a different method in go.
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/deprecations/method_all_but_go_diff_message",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    @typing_extensions.deprecated("do deprecate me in python")
    async def deprecated_all_diff_message(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint that represents a method that has been marked as deprecated in the
        stainless config for all languages, but with a different method in go.
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/deprecations/method_all_but_go_diff_message",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    @typing_extensions.deprecated("This method has been deprecated.\n\nIt will be removed in v0.99.0\n")
    async def deprecated_method(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint that represents a method that has been marked as deprecated in the
        stainless config.
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/deprecations/method",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    async def deprecated_only_go(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint that represents a method that has been marked as deprecated in the
        stainless config for go only.
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/deprecations/method_only_go",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    async def list_not_paginated(
        self,
        card_token: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Card:
        """
        Get card configuration such as spend limit and state.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not card_token:
            raise ValueError(f"Expected a non-empty value for `card_token` but received {card_token!r}")
        return await self._get(
            f"/cards/{card_token}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Card,
        )

    async def provision_foo(
        self,
        card_token: str,
        *,
        account_token: str | Omit = omit,
        certificate: Union[str, Base64FileInput] | Omit = omit,
        digital_wallet: Literal["APPLE_PAY", "GOOGLE_PAY", "SAMSUNG_PAY"] | Omit = omit,
        nonce: Union[str, Base64FileInput] | Omit = omit,
        nonce_signature: Union[str, Base64FileInput] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> CardProvisionFooResponse:
        """
        Allow your cardholders to directly add payment cards to the device's digital
        wallet (e.g. Apple Pay) with one touch from your app.

        This requires some additional setup and configuration. Please
        [Contact Us](https://lithic.com/contact) or your Customer Success representative
        for more information.

        Args:
          account_token: Only required for multi-account users. Token identifying the account the card
              will be associated with. Only applicable if using account holder enrollment. See
              [Managing Your Program](https://docs.lithic.com/docs/managing-your-program) for
              more information.

          certificate: Required for `APPLE_PAY`. Apple's public leaf certificate. Base64 encoded in PEM
              format with headers `(-----BEGIN CERTIFICATE-----)` and trailers omitted.
              Provided by the device's wallet.

          digital_wallet: Name of digital wallet provider.

          nonce: Required for `APPLE_PAY`. Base64 cryptographic nonce provided by the device's
              wallet.

          nonce_signature: Required for `APPLE_PAY`. Base64 cryptographic nonce provided by the device's
              wallet.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not card_token:
            raise ValueError(f"Expected a non-empty value for `card_token` but received {card_token!r}")
        return await self._post(
            f"/cards/{card_token}/provision",
            body=await async_maybe_transform(
                {
                    "account_token": account_token,
                    "certificate": certificate,
                    "digital_wallet": digital_wallet,
                    "nonce": nonce,
                    "nonce_signature": nonce_signature,
                },
                card_provision_foo_params.CardProvisionFooParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=CardProvisionFooResponse,
        )

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
                card_reissue_params.CardReissueParams,
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


class CardsResourceWithRawResponse:
    def __init__(self, cards: CardsResource) -> None:
        self._cards = cards

        self.create = _legacy_response.to_raw_response_wrapper(
            cards.create,
        )
        self.retrieve = _legacy_response.to_raw_response_wrapper(
            cards.retrieve,
        )
        self.update = _legacy_response.to_raw_response_wrapper(
            cards.update,
        )
        self.list = _legacy_response.to_raw_response_wrapper(
            cards.list,
        )
        self.create_aliased = _legacy_response.to_raw_response_wrapper(
            cards.create_aliased,
        )
        self.create_aliased_deprecated = (  # pyright: ignore[reportDeprecated]
            _legacy_response.to_raw_response_wrapper(
                cards.create_aliased_deprecated,  # pyright: ignore[reportDeprecated],
            )
        )
        self.deprecated_all_but_go_diff_message = (  # pyright: ignore[reportDeprecated]
            _legacy_response.to_raw_response_wrapper(
                cards.deprecated_all_but_go_diff_message,  # pyright: ignore[reportDeprecated],
            )
        )
        self.deprecated_all_diff_message = (  # pyright: ignore[reportDeprecated]
            _legacy_response.to_raw_response_wrapper(
                cards.deprecated_all_diff_message,  # pyright: ignore[reportDeprecated],
            )
        )
        self.deprecated_method = (  # pyright: ignore[reportDeprecated]
            _legacy_response.to_raw_response_wrapper(
                cards.deprecated_method,  # pyright: ignore[reportDeprecated],
            )
        )
        self.deprecated_only_go = _legacy_response.to_raw_response_wrapper(
            cards.deprecated_only_go,
        )
        self.list_not_paginated = _legacy_response.to_raw_response_wrapper(
            cards.list_not_paginated,
        )
        self.provision_foo = _legacy_response.to_raw_response_wrapper(
            cards.provision_foo,
        )
        self.reissue = _legacy_response.to_raw_response_wrapper(
            cards.reissue,
        )


class AsyncCardsResourceWithRawResponse:
    def __init__(self, cards: AsyncCardsResource) -> None:
        self._cards = cards

        self.create = _legacy_response.async_to_raw_response_wrapper(
            cards.create,
        )
        self.retrieve = _legacy_response.async_to_raw_response_wrapper(
            cards.retrieve,
        )
        self.update = _legacy_response.async_to_raw_response_wrapper(
            cards.update,
        )
        self.list = _legacy_response.async_to_raw_response_wrapper(
            cards.list,
        )
        self.create_aliased = _legacy_response.async_to_raw_response_wrapper(
            cards.create_aliased,
        )
        self.create_aliased_deprecated = (  # pyright: ignore[reportDeprecated]
            _legacy_response.async_to_raw_response_wrapper(
                cards.create_aliased_deprecated,  # pyright: ignore[reportDeprecated],
            )
        )
        self.deprecated_all_but_go_diff_message = (  # pyright: ignore[reportDeprecated]
            _legacy_response.async_to_raw_response_wrapper(
                cards.deprecated_all_but_go_diff_message,  # pyright: ignore[reportDeprecated],
            )
        )
        self.deprecated_all_diff_message = (  # pyright: ignore[reportDeprecated]
            _legacy_response.async_to_raw_response_wrapper(
                cards.deprecated_all_diff_message,  # pyright: ignore[reportDeprecated],
            )
        )
        self.deprecated_method = (  # pyright: ignore[reportDeprecated]
            _legacy_response.async_to_raw_response_wrapper(
                cards.deprecated_method,  # pyright: ignore[reportDeprecated],
            )
        )
        self.deprecated_only_go = _legacy_response.async_to_raw_response_wrapper(
            cards.deprecated_only_go,
        )
        self.list_not_paginated = _legacy_response.async_to_raw_response_wrapper(
            cards.list_not_paginated,
        )
        self.provision_foo = _legacy_response.async_to_raw_response_wrapper(
            cards.provision_foo,
        )
        self.reissue = _legacy_response.async_to_raw_response_wrapper(
            cards.reissue,
        )


class CardsResourceWithStreamingResponse:
    def __init__(self, cards: CardsResource) -> None:
        self._cards = cards

        self.create = to_streamed_response_wrapper(
            cards.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            cards.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            cards.update,
        )
        self.list = to_streamed_response_wrapper(
            cards.list,
        )
        self.create_aliased = to_streamed_response_wrapper(
            cards.create_aliased,
        )
        self.create_aliased_deprecated = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                cards.create_aliased_deprecated,  # pyright: ignore[reportDeprecated],
            )
        )
        self.deprecated_all_but_go_diff_message = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                cards.deprecated_all_but_go_diff_message,  # pyright: ignore[reportDeprecated],
            )
        )
        self.deprecated_all_diff_message = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                cards.deprecated_all_diff_message,  # pyright: ignore[reportDeprecated],
            )
        )
        self.deprecated_method = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                cards.deprecated_method,  # pyright: ignore[reportDeprecated],
            )
        )
        self.deprecated_only_go = to_streamed_response_wrapper(
            cards.deprecated_only_go,
        )
        self.list_not_paginated = to_streamed_response_wrapper(
            cards.list_not_paginated,
        )
        self.provision_foo = to_streamed_response_wrapper(
            cards.provision_foo,
        )
        self.reissue = to_streamed_response_wrapper(
            cards.reissue,
        )


class AsyncCardsResourceWithStreamingResponse:
    def __init__(self, cards: AsyncCardsResource) -> None:
        self._cards = cards

        self.create = async_to_streamed_response_wrapper(
            cards.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            cards.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            cards.update,
        )
        self.list = async_to_streamed_response_wrapper(
            cards.list,
        )
        self.create_aliased = async_to_streamed_response_wrapper(
            cards.create_aliased,
        )
        self.create_aliased_deprecated = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                cards.create_aliased_deprecated,  # pyright: ignore[reportDeprecated],
            )
        )
        self.deprecated_all_but_go_diff_message = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                cards.deprecated_all_but_go_diff_message,  # pyright: ignore[reportDeprecated],
            )
        )
        self.deprecated_all_diff_message = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                cards.deprecated_all_diff_message,  # pyright: ignore[reportDeprecated],
            )
        )
        self.deprecated_method = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                cards.deprecated_method,  # pyright: ignore[reportDeprecated],
            )
        )
        self.deprecated_only_go = async_to_streamed_response_wrapper(
            cards.deprecated_only_go,
        )
        self.list_not_paginated = async_to_streamed_response_wrapper(
            cards.list_not_paginated,
        )
        self.provision_foo = async_to_streamed_response_wrapper(
            cards.provision_foo,
        )
        self.reissue = async_to_streamed_response_wrapper(
            cards.reissue,
        )
