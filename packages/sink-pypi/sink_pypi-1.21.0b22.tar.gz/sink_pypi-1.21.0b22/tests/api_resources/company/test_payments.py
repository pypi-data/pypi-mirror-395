# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.company import CompanyPayment

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPayments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Sink) -> None:
        payment = client.company.payments.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(CompanyPayment, payment, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Sink) -> None:
        response = client.company.payments.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        payment = response.parse()
        assert_matches_type(CompanyPayment, payment, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Sink) -> None:
        with client.company.payments.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed

            payment = response.parse()
            assert_matches_type(CompanyPayment, payment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `payment_id` but received ''"):
            client.company.payments.with_raw_response.retrieve(
                "",
            )


class TestAsyncPayments:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSink) -> None:
        payment = await async_client.company.payments.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(CompanyPayment, payment, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSink) -> None:
        response = await async_client.company.payments.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        payment = response.parse()
        assert_matches_type(CompanyPayment, payment, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSink) -> None:
        async with async_client.company.payments.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed

            payment = await response.parse()
            assert_matches_type(CompanyPayment, payment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `payment_id` but received ''"):
            await async_client.company.payments.with_raw_response.retrieve(
                "",
            )
