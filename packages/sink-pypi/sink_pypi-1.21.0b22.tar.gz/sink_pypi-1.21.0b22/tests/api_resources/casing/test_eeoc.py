# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.pagination import SyncPageCursor, AsyncPageCursor
from sink.api.sdk.types.casing import EEOC

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEEOC:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Sink) -> None:
        eeoc = client.casing.eeoc.list()
        assert_matches_type(SyncPageCursor[EEOC], eeoc, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Sink) -> None:
        eeoc = client.casing.eeoc.list(
            cursor="cursor",
            limit=0,
        )
        assert_matches_type(SyncPageCursor[EEOC], eeoc, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Sink) -> None:
        response = client.casing.eeoc.with_raw_response.list()

        assert response.is_closed is True
        eeoc = response.parse()
        assert_matches_type(SyncPageCursor[EEOC], eeoc, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Sink) -> None:
        with client.casing.eeoc.with_streaming_response.list() as response:
            assert not response.is_closed

            eeoc = response.parse()
            assert_matches_type(SyncPageCursor[EEOC], eeoc, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncEEOC:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_list(self, async_client: AsyncSink) -> None:
        eeoc = await async_client.casing.eeoc.list()
        assert_matches_type(AsyncPageCursor[EEOC], eeoc, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSink) -> None:
        eeoc = await async_client.casing.eeoc.list(
            cursor="cursor",
            limit=0,
        )
        assert_matches_type(AsyncPageCursor[EEOC], eeoc, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSink) -> None:
        response = await async_client.casing.eeoc.with_raw_response.list()

        assert response.is_closed is True
        eeoc = response.parse()
        assert_matches_type(AsyncPageCursor[EEOC], eeoc, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSink) -> None:
        async with async_client.casing.eeoc.with_streaming_response.list() as response:
            assert not response.is_closed

            eeoc = await response.parse()
            assert_matches_type(AsyncPageCursor[EEOC], eeoc, path=["response"])

        assert cast(Any, response.is_closed) is True
