# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import Client

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestClients:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Sink) -> None:
        client_ = client.clients.create(
            account_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            name="name",
        )
        assert_matches_type(Client, client_, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Sink) -> None:
        response = client.clients.with_raw_response.create(
            account_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            name="name",
        )

        assert response.is_closed is True
        client_ = response.parse()
        assert_matches_type(Client, client_, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Sink) -> None:
        with client.clients.with_streaming_response.create(
            account_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            name="name",
        ) as response:
            assert not response.is_closed

            client_ = response.parse()
            assert_matches_type(Client, client_, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncClients:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSink) -> None:
        client = await async_client.clients.create(
            account_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            name="name",
        )
        assert_matches_type(Client, client, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSink) -> None:
        response = await async_client.clients.with_raw_response.create(
            account_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            name="name",
        )

        assert response.is_closed is True
        client = response.parse()
        assert_matches_type(Client, client, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSink) -> None:
        async with async_client.clients.with_streaming_response.create(
            account_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            name="name",
        ) as response:
            assert not response.is_closed

            client = await response.parse()
            assert_matches_type(Client, client, path=["response"])

        assert cast(Any, response.is_closed) is True
