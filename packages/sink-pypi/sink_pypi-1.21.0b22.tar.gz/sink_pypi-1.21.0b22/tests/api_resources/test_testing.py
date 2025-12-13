# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import RootResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTesting:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_root(self, client: Sink) -> None:
        testing = client.testing.root()
        assert_matches_type(RootResponse, testing, path=["response"])

    @parametrize
    def test_raw_response_root(self, client: Sink) -> None:
        response = client.testing.with_raw_response.root()

        assert response.is_closed is True
        testing = response.parse()
        assert_matches_type(RootResponse, testing, path=["response"])

    @parametrize
    def test_streaming_response_root(self, client: Sink) -> None:
        with client.testing.with_streaming_response.root() as response:
            assert not response.is_closed

            testing = response.parse()
            assert_matches_type(RootResponse, testing, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTesting:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_root(self, async_client: AsyncSink) -> None:
        testing = await async_client.testing.root()
        assert_matches_type(RootResponse, testing, path=["response"])

    @parametrize
    async def test_raw_response_root(self, async_client: AsyncSink) -> None:
        response = await async_client.testing.with_raw_response.root()

        assert response.is_closed is True
        testing = response.parse()
        assert_matches_type(RootResponse, testing, path=["response"])

    @parametrize
    async def test_streaming_response_root(self, async_client: AsyncSink) -> None:
        async with async_client.testing.with_streaming_response.root() as response:
            assert not response.is_closed

            testing = await response.parse()
            assert_matches_type(RootResponse, testing, path=["response"])

        assert cast(Any, response.is_closed) is True
