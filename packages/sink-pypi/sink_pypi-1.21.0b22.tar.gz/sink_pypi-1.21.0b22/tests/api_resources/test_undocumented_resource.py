# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import Card

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUndocumentedResource:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_reissue(self, client: Sink) -> None:
        undocumented_resource = client.undocumented_resource.reissue(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Card, undocumented_resource, path=["response"])

    @parametrize
    def test_method_reissue_with_all_params(self, client: Sink) -> None:
        undocumented_resource = client.undocumented_resource.reissue(
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
        assert_matches_type(Card, undocumented_resource, path=["response"])

    @parametrize
    def test_raw_response_reissue(self, client: Sink) -> None:
        response = client.undocumented_resource.with_raw_response.reissue(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        undocumented_resource = response.parse()
        assert_matches_type(Card, undocumented_resource, path=["response"])

    @parametrize
    def test_streaming_response_reissue(self, client: Sink) -> None:
        with client.undocumented_resource.with_streaming_response.reissue(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed

            undocumented_resource = response.parse()
            assert_matches_type(Card, undocumented_resource, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_reissue(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_token` but received ''"):
            client.undocumented_resource.with_raw_response.reissue(
                card_token="",
            )


class TestAsyncUndocumentedResource:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_reissue(self, async_client: AsyncSink) -> None:
        undocumented_resource = await async_client.undocumented_resource.reissue(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Card, undocumented_resource, path=["response"])

    @parametrize
    async def test_method_reissue_with_all_params(self, async_client: AsyncSink) -> None:
        undocumented_resource = await async_client.undocumented_resource.reissue(
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
        assert_matches_type(Card, undocumented_resource, path=["response"])

    @parametrize
    async def test_raw_response_reissue(self, async_client: AsyncSink) -> None:
        response = await async_client.undocumented_resource.with_raw_response.reissue(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        undocumented_resource = response.parse()
        assert_matches_type(Card, undocumented_resource, path=["response"])

    @parametrize
    async def test_streaming_response_reissue(self, async_client: AsyncSink) -> None:
        async with async_client.undocumented_resource.with_streaming_response.reissue(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed

            undocumented_resource = await response.parse()
            assert_matches_type(Card, undocumented_resource, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_reissue(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_token` but received ''"):
            await async_client.undocumented_resource.with_raw_response.reissue(
                card_token="",
            )
