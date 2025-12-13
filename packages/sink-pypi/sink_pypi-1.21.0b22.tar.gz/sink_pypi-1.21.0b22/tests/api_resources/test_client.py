# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import APIStatus

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestClient:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_api_status(self, client: Sink) -> None:
        client_ = client.api_status()
        assert_matches_type(APIStatus, client_, path=["response"])

    @parametrize
    def test_raw_response_api_status(self, client: Sink) -> None:
        response = client.with_raw_response.api_status()

        assert response.is_closed is True
        client_ = response.parse()
        assert_matches_type(APIStatus, client_, path=["response"])

    @parametrize
    def test_streaming_response_api_status(self, client: Sink) -> None:
        with client.with_streaming_response.api_status() as response:
            assert not response.is_closed

            client_ = response.parse()
            assert_matches_type(APIStatus, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_api_status_alias(self, client: Sink) -> None:
        client_ = client.api_status_alias()
        assert_matches_type(APIStatus, client_, path=["response"])

    @parametrize
    def test_raw_response_api_status_alias(self, client: Sink) -> None:
        response = client.with_raw_response.api_status_alias()

        assert response.is_closed is True
        client_ = response.parse()
        assert_matches_type(APIStatus, client_, path=["response"])

    @parametrize
    def test_streaming_response_api_status_alias(self, client: Sink) -> None:
        with client.with_streaming_response.api_status_alias() as response:
            assert not response.is_closed

            client_ = response.parse()
            assert_matches_type(APIStatus, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_create_no_response(self, client: Sink) -> None:
        client_ = client.create_no_response()
        assert client_ is None

    @parametrize
    def test_raw_response_create_no_response(self, client: Sink) -> None:
        response = client.with_raw_response.create_no_response()

        assert response.is_closed is True
        client_ = response.parse()
        assert client_ is None

    @parametrize
    def test_streaming_response_create_no_response(self, client: Sink) -> None:
        with client.with_streaming_response.create_no_response() as response:
            assert not response.is_closed

            client_ = response.parse()
            assert client_ is None

        assert cast(Any, response.is_closed) is True


class TestAsyncClient:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_api_status(self, async_client: AsyncSink) -> None:
        client = await async_client.api_status()
        assert_matches_type(APIStatus, client, path=["response"])

    @parametrize
    async def test_raw_response_api_status(self, async_client: AsyncSink) -> None:
        response = await async_client.with_raw_response.api_status()

        assert response.is_closed is True
        client = response.parse()
        assert_matches_type(APIStatus, client, path=["response"])

    @parametrize
    async def test_streaming_response_api_status(self, async_client: AsyncSink) -> None:
        async with async_client.with_streaming_response.api_status() as response:
            assert not response.is_closed

            client = await response.parse()
            assert_matches_type(APIStatus, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_api_status_alias(self, async_client: AsyncSink) -> None:
        client = await async_client.api_status_alias()
        assert_matches_type(APIStatus, client, path=["response"])

    @parametrize
    async def test_raw_response_api_status_alias(self, async_client: AsyncSink) -> None:
        response = await async_client.with_raw_response.api_status_alias()

        assert response.is_closed is True
        client = response.parse()
        assert_matches_type(APIStatus, client, path=["response"])

    @parametrize
    async def test_streaming_response_api_status_alias(self, async_client: AsyncSink) -> None:
        async with async_client.with_streaming_response.api_status_alias() as response:
            assert not response.is_closed

            client = await response.parse()
            assert_matches_type(APIStatus, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_create_no_response(self, async_client: AsyncSink) -> None:
        client = await async_client.create_no_response()
        assert client is None

    @parametrize
    async def test_raw_response_create_no_response(self, async_client: AsyncSink) -> None:
        response = await async_client.with_raw_response.create_no_response()

        assert response.is_closed is True
        client = response.parse()
        assert client is None

    @parametrize
    async def test_streaming_response_create_no_response(self, async_client: AsyncSink) -> None:
        async with async_client.with_streaming_response.create_no_response() as response:
            assert not response.is_closed

            client = await response.parse()
            assert client is None

        assert cast(Any, response.is_closed) is True
