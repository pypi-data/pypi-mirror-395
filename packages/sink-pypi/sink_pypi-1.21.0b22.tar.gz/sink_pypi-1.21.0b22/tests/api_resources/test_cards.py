# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import (
    Card,
    CardListResponse,
    CardProvisionFooResponse,
)
from sink.api.sdk._utils import parse_datetime

# pyright: reportDeprecated=false

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCards:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Sink) -> None:
        card = client.cards.create(
            type="SINGLE_USE",
        )
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Sink) -> None:
        card = client.cards.create(
            type="SINGLE_USE",
            account_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            card_program_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            exp_month="06",
            exp_year="2027",
            funding_token="514aa2b7-898f-4ce7-bc05-c2fe993713e8",
            memo="New Card",
            not_="not",
            pin="pin",
            product_id="1",
            shipping_method="STANDARD",
            shipping_address={
                "address1": "5 Broad Street",
                "city": "NEW YORK",
                "country": "USA",
                "first_name": "Michael",
                "last_name": "Bluth",
                "postal_code": "10001-1809",
                "state": "NY",
                "address2": "Unit 25A",
                "email": "johnny@appleseed.com",
                "line2_text": "The Bluth Company",
                "phone_number": "+12124007676",
            },
            spend_limit=0,
            spend_limit_duration="TRANSACTION",
            state="OPEN",
        )
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Sink) -> None:
        response = client.cards.with_raw_response.create(
            type="SINGLE_USE",
        )

        assert response.is_closed is True
        card = response.parse()
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Sink) -> None:
        with client.cards.with_streaming_response.create(
            type="SINGLE_USE",
        ) as response:
            assert not response.is_closed

            card = response.parse()
            assert_matches_type(Card, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Sink) -> None:
        card = client.cards.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Sink) -> None:
        response = client.cards.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        card = response.parse()
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Sink) -> None:
        with client.cards.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed

            card = response.parse()
            assert_matches_type(Card, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_token` but received ''"):
            client.cards.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Sink) -> None:
        card = client.cards.update(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Sink) -> None:
        card = client.cards.update(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            auth_rule_token="auth_rule_token",
            funding_token="ecbd1d58-0299-48b3-84da-6ed7f5bf9ec1",
            memo="Updated Name",
            pin="pin",
            spend_limit=100,
            spend_limit_duration="FOREVER",
            state="OPEN",
        )
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Sink) -> None:
        response = client.cards.with_raw_response.update(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        card = response.parse()
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Sink) -> None:
        with client.cards.with_streaming_response.update(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed

            card = response.parse()
            assert_matches_type(Card, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_token` but received ''"):
            client.cards.with_raw_response.update(
                card_token="",
            )

    @parametrize
    def test_method_list(self, client: Sink) -> None:
        card = client.cards.list(
            begin=parse_datetime("2022-02-01T05:00:00Z"),
            end=parse_datetime("2022-02-01T05:00:00Z"),
        )
        assert_matches_type(CardListResponse, card, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Sink) -> None:
        card = client.cards.list(
            begin=parse_datetime("2022-02-01T05:00:00Z"),
            end=parse_datetime("2022-02-01T05:00:00Z"),
            account_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            page=0,
            page_size=1,
        )
        assert_matches_type(CardListResponse, card, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Sink) -> None:
        response = client.cards.with_raw_response.list(
            begin=parse_datetime("2022-02-01T05:00:00Z"),
            end=parse_datetime("2022-02-01T05:00:00Z"),
        )

        assert response.is_closed is True
        card = response.parse()
        assert_matches_type(CardListResponse, card, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Sink) -> None:
        with client.cards.with_streaming_response.list(
            begin=parse_datetime("2022-02-01T05:00:00Z"),
            end=parse_datetime("2022-02-01T05:00:00Z"),
        ) as response:
            assert not response.is_closed

            card = response.parse()
            assert_matches_type(CardListResponse, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_create_aliased(self, client: Sink) -> None:
        card = client.cards.create_aliased(
            type="SINGLE_USE",
        )
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    def test_method_create_aliased_with_all_params(self, client: Sink) -> None:
        card = client.cards.create_aliased(
            type="SINGLE_USE",
            account_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            card_program_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            exp_month="06",
            exp_year="2027",
            funding_token="514aa2b7-898f-4ce7-bc05-c2fe993713e8",
            memo="New Card",
            not_="not",
            pin="pin",
            product_id="1",
            shipping_method="STANDARD",
            shipping_address={
                "address1": "5 Broad Street",
                "city": "NEW YORK",
                "country": "USA",
                "first_name": "Michael",
                "last_name": "Bluth",
                "postal_code": "10001-1809",
                "state": "NY",
                "address2": "Unit 25A",
                "email": "johnny@appleseed.com",
                "line2_text": "The Bluth Company",
                "phone_number": "+12124007676",
            },
            spend_limit=0,
            spend_limit_duration="TRANSACTION",
            state="OPEN",
        )
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    def test_raw_response_create_aliased(self, client: Sink) -> None:
        response = client.cards.with_raw_response.create_aliased(
            type="SINGLE_USE",
        )

        assert response.is_closed is True
        card = response.parse()
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    def test_streaming_response_create_aliased(self, client: Sink) -> None:
        with client.cards.with_streaming_response.create_aliased(
            type="SINGLE_USE",
        ) as response:
            assert not response.is_closed

            card = response.parse()
            assert_matches_type(Card, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_create_aliased_deprecated(self, client: Sink) -> None:
        with pytest.warns(DeprecationWarning):
            card = client.cards.create_aliased_deprecated(
                type="SINGLE_USE",
            )

        assert_matches_type(Card, card, path=["response"])

    @parametrize
    def test_method_create_aliased_deprecated_with_all_params(self, client: Sink) -> None:
        with pytest.warns(DeprecationWarning):
            card = client.cards.create_aliased_deprecated(
                type="SINGLE_USE",
                account_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                card_program_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                exp_month="06",
                exp_year="2027",
                funding_token="514aa2b7-898f-4ce7-bc05-c2fe993713e8",
                memo="New Card",
                not_="not",
                pin="pin",
                product_id="1",
                shipping_method="STANDARD",
                shipping_address={
                    "address1": "5 Broad Street",
                    "city": "NEW YORK",
                    "country": "USA",
                    "first_name": "Michael",
                    "last_name": "Bluth",
                    "postal_code": "10001-1809",
                    "state": "NY",
                    "address2": "Unit 25A",
                    "email": "johnny@appleseed.com",
                    "line2_text": "The Bluth Company",
                    "phone_number": "+12124007676",
                },
                spend_limit=0,
                spend_limit_duration="TRANSACTION",
                state="OPEN",
            )

        assert_matches_type(Card, card, path=["response"])

    @parametrize
    def test_raw_response_create_aliased_deprecated(self, client: Sink) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.cards.with_raw_response.create_aliased_deprecated(
                type="SINGLE_USE",
            )

        assert response.is_closed is True
        card = response.parse()
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    def test_streaming_response_create_aliased_deprecated(self, client: Sink) -> None:
        with pytest.warns(DeprecationWarning):
            with client.cards.with_streaming_response.create_aliased_deprecated(
                type="SINGLE_USE",
            ) as response:
                assert not response.is_closed

                card = response.parse()
                assert_matches_type(Card, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_deprecated_all_but_go_diff_message(self, client: Sink) -> None:
        with pytest.warns(DeprecationWarning):
            card = client.cards.deprecated_all_but_go_diff_message()

        assert card is None

    @parametrize
    def test_raw_response_deprecated_all_but_go_diff_message(self, client: Sink) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.cards.with_raw_response.deprecated_all_but_go_diff_message()

        assert response.is_closed is True
        card = response.parse()
        assert card is None

    @parametrize
    def test_streaming_response_deprecated_all_but_go_diff_message(self, client: Sink) -> None:
        with pytest.warns(DeprecationWarning):
            with client.cards.with_streaming_response.deprecated_all_but_go_diff_message() as response:
                assert not response.is_closed

                card = response.parse()
                assert card is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_deprecated_all_diff_message(self, client: Sink) -> None:
        with pytest.warns(DeprecationWarning):
            card = client.cards.deprecated_all_diff_message()

        assert card is None

    @parametrize
    def test_raw_response_deprecated_all_diff_message(self, client: Sink) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.cards.with_raw_response.deprecated_all_diff_message()

        assert response.is_closed is True
        card = response.parse()
        assert card is None

    @parametrize
    def test_streaming_response_deprecated_all_diff_message(self, client: Sink) -> None:
        with pytest.warns(DeprecationWarning):
            with client.cards.with_streaming_response.deprecated_all_diff_message() as response:
                assert not response.is_closed

                card = response.parse()
                assert card is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_deprecated_method(self, client: Sink) -> None:
        with pytest.warns(DeprecationWarning):
            card = client.cards.deprecated_method()

        assert card is None

    @parametrize
    def test_raw_response_deprecated_method(self, client: Sink) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.cards.with_raw_response.deprecated_method()

        assert response.is_closed is True
        card = response.parse()
        assert card is None

    @parametrize
    def test_streaming_response_deprecated_method(self, client: Sink) -> None:
        with pytest.warns(DeprecationWarning):
            with client.cards.with_streaming_response.deprecated_method() as response:
                assert not response.is_closed

                card = response.parse()
                assert card is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_deprecated_only_go(self, client: Sink) -> None:
        card = client.cards.deprecated_only_go()
        assert card is None

    @parametrize
    def test_raw_response_deprecated_only_go(self, client: Sink) -> None:
        response = client.cards.with_raw_response.deprecated_only_go()

        assert response.is_closed is True
        card = response.parse()
        assert card is None

    @parametrize
    def test_streaming_response_deprecated_only_go(self, client: Sink) -> None:
        with client.cards.with_streaming_response.deprecated_only_go() as response:
            assert not response.is_closed

            card = response.parse()
            assert card is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list_not_paginated(self, client: Sink) -> None:
        card = client.cards.list_not_paginated(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    def test_raw_response_list_not_paginated(self, client: Sink) -> None:
        response = client.cards.with_raw_response.list_not_paginated(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        card = response.parse()
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    def test_streaming_response_list_not_paginated(self, client: Sink) -> None:
        with client.cards.with_streaming_response.list_not_paginated(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed

            card = response.parse()
            assert_matches_type(Card, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list_not_paginated(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_token` but received ''"):
            client.cards.with_raw_response.list_not_paginated(
                "",
            )

    @parametrize
    def test_method_provision_foo(self, client: Sink) -> None:
        card = client.cards.provision_foo(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(CardProvisionFooResponse, card, path=["response"])

    @parametrize
    def test_method_provision_foo_with_all_params(self, client: Sink) -> None:
        card = client.cards.provision_foo(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            certificate="U3RhaW5sZXNzIHJvY2tz",
            digital_wallet="GOOGLE_PAY",
            nonce="U3RhaW5sZXNzIHJvY2tz",
            nonce_signature="U3RhaW5sZXNzIHJvY2tz",
        )
        assert_matches_type(CardProvisionFooResponse, card, path=["response"])

    @parametrize
    def test_raw_response_provision_foo(self, client: Sink) -> None:
        response = client.cards.with_raw_response.provision_foo(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        card = response.parse()
        assert_matches_type(CardProvisionFooResponse, card, path=["response"])

    @parametrize
    def test_streaming_response_provision_foo(self, client: Sink) -> None:
        with client.cards.with_streaming_response.provision_foo(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed

            card = response.parse()
            assert_matches_type(CardProvisionFooResponse, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_provision_foo(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_token` but received ''"):
            client.cards.with_raw_response.provision_foo(
                card_token="",
            )

    @parametrize
    def test_method_reissue(self, client: Sink) -> None:
        card = client.cards.reissue(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    def test_method_reissue_with_all_params(self, client: Sink) -> None:
        card = client.cards.reissue(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            product_id="product_id",
            shipping_method="STANDARD",
            shipping_address={
                "address1": "5 Broad Street",
                "city": "NEW YORK",
                "country": "USA",
                "first_name": "Michael",
                "last_name": "Bluth",
                "postal_code": "10001-1809",
                "state": "NY",
                "address2": "Unit 25A",
                "email": "johnny@appleseed.com",
                "line2_text": "The Bluth Company",
                "phone_number": "+12124007676",
            },
        )
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    def test_raw_response_reissue(self, client: Sink) -> None:
        response = client.cards.with_raw_response.reissue(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        card = response.parse()
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    def test_streaming_response_reissue(self, client: Sink) -> None:
        with client.cards.with_streaming_response.reissue(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed

            card = response.parse()
            assert_matches_type(Card, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_reissue(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_token` but received ''"):
            client.cards.with_raw_response.reissue(
                card_token="",
            )


class TestAsyncCards:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSink) -> None:
        card = await async_client.cards.create(
            type="SINGLE_USE",
        )
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSink) -> None:
        card = await async_client.cards.create(
            type="SINGLE_USE",
            account_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            card_program_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            exp_month="06",
            exp_year="2027",
            funding_token="514aa2b7-898f-4ce7-bc05-c2fe993713e8",
            memo="New Card",
            not_="not",
            pin="pin",
            product_id="1",
            shipping_method="STANDARD",
            shipping_address={
                "address1": "5 Broad Street",
                "city": "NEW YORK",
                "country": "USA",
                "first_name": "Michael",
                "last_name": "Bluth",
                "postal_code": "10001-1809",
                "state": "NY",
                "address2": "Unit 25A",
                "email": "johnny@appleseed.com",
                "line2_text": "The Bluth Company",
                "phone_number": "+12124007676",
            },
            spend_limit=0,
            spend_limit_duration="TRANSACTION",
            state="OPEN",
        )
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSink) -> None:
        response = await async_client.cards.with_raw_response.create(
            type="SINGLE_USE",
        )

        assert response.is_closed is True
        card = response.parse()
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSink) -> None:
        async with async_client.cards.with_streaming_response.create(
            type="SINGLE_USE",
        ) as response:
            assert not response.is_closed

            card = await response.parse()
            assert_matches_type(Card, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSink) -> None:
        card = await async_client.cards.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSink) -> None:
        response = await async_client.cards.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        card = response.parse()
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSink) -> None:
        async with async_client.cards.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed

            card = await response.parse()
            assert_matches_type(Card, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_token` but received ''"):
            await async_client.cards.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSink) -> None:
        card = await async_client.cards.update(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSink) -> None:
        card = await async_client.cards.update(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            auth_rule_token="auth_rule_token",
            funding_token="ecbd1d58-0299-48b3-84da-6ed7f5bf9ec1",
            memo="Updated Name",
            pin="pin",
            spend_limit=100,
            spend_limit_duration="FOREVER",
            state="OPEN",
        )
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSink) -> None:
        response = await async_client.cards.with_raw_response.update(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        card = response.parse()
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSink) -> None:
        async with async_client.cards.with_streaming_response.update(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed

            card = await response.parse()
            assert_matches_type(Card, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_token` but received ''"):
            await async_client.cards.with_raw_response.update(
                card_token="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSink) -> None:
        card = await async_client.cards.list(
            begin=parse_datetime("2022-02-01T05:00:00Z"),
            end=parse_datetime("2022-02-01T05:00:00Z"),
        )
        assert_matches_type(CardListResponse, card, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSink) -> None:
        card = await async_client.cards.list(
            begin=parse_datetime("2022-02-01T05:00:00Z"),
            end=parse_datetime("2022-02-01T05:00:00Z"),
            account_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            page=0,
            page_size=1,
        )
        assert_matches_type(CardListResponse, card, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSink) -> None:
        response = await async_client.cards.with_raw_response.list(
            begin=parse_datetime("2022-02-01T05:00:00Z"),
            end=parse_datetime("2022-02-01T05:00:00Z"),
        )

        assert response.is_closed is True
        card = response.parse()
        assert_matches_type(CardListResponse, card, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSink) -> None:
        async with async_client.cards.with_streaming_response.list(
            begin=parse_datetime("2022-02-01T05:00:00Z"),
            end=parse_datetime("2022-02-01T05:00:00Z"),
        ) as response:
            assert not response.is_closed

            card = await response.parse()
            assert_matches_type(CardListResponse, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_create_aliased(self, async_client: AsyncSink) -> None:
        card = await async_client.cards.create_aliased(
            type="SINGLE_USE",
        )
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    async def test_method_create_aliased_with_all_params(self, async_client: AsyncSink) -> None:
        card = await async_client.cards.create_aliased(
            type="SINGLE_USE",
            account_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            card_program_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            exp_month="06",
            exp_year="2027",
            funding_token="514aa2b7-898f-4ce7-bc05-c2fe993713e8",
            memo="New Card",
            not_="not",
            pin="pin",
            product_id="1",
            shipping_method="STANDARD",
            shipping_address={
                "address1": "5 Broad Street",
                "city": "NEW YORK",
                "country": "USA",
                "first_name": "Michael",
                "last_name": "Bluth",
                "postal_code": "10001-1809",
                "state": "NY",
                "address2": "Unit 25A",
                "email": "johnny@appleseed.com",
                "line2_text": "The Bluth Company",
                "phone_number": "+12124007676",
            },
            spend_limit=0,
            spend_limit_duration="TRANSACTION",
            state="OPEN",
        )
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    async def test_raw_response_create_aliased(self, async_client: AsyncSink) -> None:
        response = await async_client.cards.with_raw_response.create_aliased(
            type="SINGLE_USE",
        )

        assert response.is_closed is True
        card = response.parse()
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    async def test_streaming_response_create_aliased(self, async_client: AsyncSink) -> None:
        async with async_client.cards.with_streaming_response.create_aliased(
            type="SINGLE_USE",
        ) as response:
            assert not response.is_closed

            card = await response.parse()
            assert_matches_type(Card, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_create_aliased_deprecated(self, async_client: AsyncSink) -> None:
        with pytest.warns(DeprecationWarning):
            card = await async_client.cards.create_aliased_deprecated(
                type="SINGLE_USE",
            )

        assert_matches_type(Card, card, path=["response"])

    @parametrize
    async def test_method_create_aliased_deprecated_with_all_params(self, async_client: AsyncSink) -> None:
        with pytest.warns(DeprecationWarning):
            card = await async_client.cards.create_aliased_deprecated(
                type="SINGLE_USE",
                account_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                card_program_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                exp_month="06",
                exp_year="2027",
                funding_token="514aa2b7-898f-4ce7-bc05-c2fe993713e8",
                memo="New Card",
                not_="not",
                pin="pin",
                product_id="1",
                shipping_method="STANDARD",
                shipping_address={
                    "address1": "5 Broad Street",
                    "city": "NEW YORK",
                    "country": "USA",
                    "first_name": "Michael",
                    "last_name": "Bluth",
                    "postal_code": "10001-1809",
                    "state": "NY",
                    "address2": "Unit 25A",
                    "email": "johnny@appleseed.com",
                    "line2_text": "The Bluth Company",
                    "phone_number": "+12124007676",
                },
                spend_limit=0,
                spend_limit_duration="TRANSACTION",
                state="OPEN",
            )

        assert_matches_type(Card, card, path=["response"])

    @parametrize
    async def test_raw_response_create_aliased_deprecated(self, async_client: AsyncSink) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.cards.with_raw_response.create_aliased_deprecated(
                type="SINGLE_USE",
            )

        assert response.is_closed is True
        card = response.parse()
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    async def test_streaming_response_create_aliased_deprecated(self, async_client: AsyncSink) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.cards.with_streaming_response.create_aliased_deprecated(
                type="SINGLE_USE",
            ) as response:
                assert not response.is_closed

                card = await response.parse()
                assert_matches_type(Card, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_deprecated_all_but_go_diff_message(self, async_client: AsyncSink) -> None:
        with pytest.warns(DeprecationWarning):
            card = await async_client.cards.deprecated_all_but_go_diff_message()

        assert card is None

    @parametrize
    async def test_raw_response_deprecated_all_but_go_diff_message(self, async_client: AsyncSink) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.cards.with_raw_response.deprecated_all_but_go_diff_message()

        assert response.is_closed is True
        card = response.parse()
        assert card is None

    @parametrize
    async def test_streaming_response_deprecated_all_but_go_diff_message(self, async_client: AsyncSink) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.cards.with_streaming_response.deprecated_all_but_go_diff_message() as response:
                assert not response.is_closed

                card = await response.parse()
                assert card is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_deprecated_all_diff_message(self, async_client: AsyncSink) -> None:
        with pytest.warns(DeprecationWarning):
            card = await async_client.cards.deprecated_all_diff_message()

        assert card is None

    @parametrize
    async def test_raw_response_deprecated_all_diff_message(self, async_client: AsyncSink) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.cards.with_raw_response.deprecated_all_diff_message()

        assert response.is_closed is True
        card = response.parse()
        assert card is None

    @parametrize
    async def test_streaming_response_deprecated_all_diff_message(self, async_client: AsyncSink) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.cards.with_streaming_response.deprecated_all_diff_message() as response:
                assert not response.is_closed

                card = await response.parse()
                assert card is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_deprecated_method(self, async_client: AsyncSink) -> None:
        with pytest.warns(DeprecationWarning):
            card = await async_client.cards.deprecated_method()

        assert card is None

    @parametrize
    async def test_raw_response_deprecated_method(self, async_client: AsyncSink) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.cards.with_raw_response.deprecated_method()

        assert response.is_closed is True
        card = response.parse()
        assert card is None

    @parametrize
    async def test_streaming_response_deprecated_method(self, async_client: AsyncSink) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.cards.with_streaming_response.deprecated_method() as response:
                assert not response.is_closed

                card = await response.parse()
                assert card is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_deprecated_only_go(self, async_client: AsyncSink) -> None:
        card = await async_client.cards.deprecated_only_go()
        assert card is None

    @parametrize
    async def test_raw_response_deprecated_only_go(self, async_client: AsyncSink) -> None:
        response = await async_client.cards.with_raw_response.deprecated_only_go()

        assert response.is_closed is True
        card = response.parse()
        assert card is None

    @parametrize
    async def test_streaming_response_deprecated_only_go(self, async_client: AsyncSink) -> None:
        async with async_client.cards.with_streaming_response.deprecated_only_go() as response:
            assert not response.is_closed

            card = await response.parse()
            assert card is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list_not_paginated(self, async_client: AsyncSink) -> None:
        card = await async_client.cards.list_not_paginated(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    async def test_raw_response_list_not_paginated(self, async_client: AsyncSink) -> None:
        response = await async_client.cards.with_raw_response.list_not_paginated(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        card = response.parse()
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    async def test_streaming_response_list_not_paginated(self, async_client: AsyncSink) -> None:
        async with async_client.cards.with_streaming_response.list_not_paginated(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed

            card = await response.parse()
            assert_matches_type(Card, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list_not_paginated(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_token` but received ''"):
            await async_client.cards.with_raw_response.list_not_paginated(
                "",
            )

    @parametrize
    async def test_method_provision_foo(self, async_client: AsyncSink) -> None:
        card = await async_client.cards.provision_foo(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(CardProvisionFooResponse, card, path=["response"])

    @parametrize
    async def test_method_provision_foo_with_all_params(self, async_client: AsyncSink) -> None:
        card = await async_client.cards.provision_foo(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            certificate="U3RhaW5sZXNzIHJvY2tz",
            digital_wallet="GOOGLE_PAY",
            nonce="U3RhaW5sZXNzIHJvY2tz",
            nonce_signature="U3RhaW5sZXNzIHJvY2tz",
        )
        assert_matches_type(CardProvisionFooResponse, card, path=["response"])

    @parametrize
    async def test_raw_response_provision_foo(self, async_client: AsyncSink) -> None:
        response = await async_client.cards.with_raw_response.provision_foo(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        card = response.parse()
        assert_matches_type(CardProvisionFooResponse, card, path=["response"])

    @parametrize
    async def test_streaming_response_provision_foo(self, async_client: AsyncSink) -> None:
        async with async_client.cards.with_streaming_response.provision_foo(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed

            card = await response.parse()
            assert_matches_type(CardProvisionFooResponse, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_provision_foo(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_token` but received ''"):
            await async_client.cards.with_raw_response.provision_foo(
                card_token="",
            )

    @parametrize
    async def test_method_reissue(self, async_client: AsyncSink) -> None:
        card = await async_client.cards.reissue(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    async def test_method_reissue_with_all_params(self, async_client: AsyncSink) -> None:
        card = await async_client.cards.reissue(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            product_id="product_id",
            shipping_method="STANDARD",
            shipping_address={
                "address1": "5 Broad Street",
                "city": "NEW YORK",
                "country": "USA",
                "first_name": "Michael",
                "last_name": "Bluth",
                "postal_code": "10001-1809",
                "state": "NY",
                "address2": "Unit 25A",
                "email": "johnny@appleseed.com",
                "line2_text": "The Bluth Company",
                "phone_number": "+12124007676",
            },
        )
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    async def test_raw_response_reissue(self, async_client: AsyncSink) -> None:
        response = await async_client.cards.with_raw_response.reissue(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        card = response.parse()
        assert_matches_type(Card, card, path=["response"])

    @parametrize
    async def test_streaming_response_reissue(self, async_client: AsyncSink) -> None:
        async with async_client.cards.with_streaming_response.reissue(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed

            card = await response.parse()
            assert_matches_type(Card, card, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_reissue(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_token` but received ''"):
            await async_client.cards.with_raw_response.reissue(
                card_token="",
            )
