# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import MyModel
from sink.api.sdk.pagination import SyncPageCursorID, AsyncPageCursorID

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCursorID:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Sink) -> None:
        cursor_id = client.pagination_tests.cursor_id.list()
        assert_matches_type(SyncPageCursorID[MyModel], cursor_id, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Sink) -> None:
        cursor_id = client.pagination_tests.cursor_id.list(
            limit=0,
            next_id="next_id",
        )
        assert_matches_type(SyncPageCursorID[MyModel], cursor_id, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Sink) -> None:
        response = client.pagination_tests.cursor_id.with_raw_response.list()

        assert response.is_closed is True
        cursor_id = response.parse()
        assert_matches_type(SyncPageCursorID[MyModel], cursor_id, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Sink) -> None:
        with client.pagination_tests.cursor_id.with_streaming_response.list() as response:
            assert not response.is_closed

            cursor_id = response.parse()
            assert_matches_type(SyncPageCursorID[MyModel], cursor_id, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncCursorID:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_list(self, async_client: AsyncSink) -> None:
        cursor_id = await async_client.pagination_tests.cursor_id.list()
        assert_matches_type(AsyncPageCursorID[MyModel], cursor_id, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSink) -> None:
        cursor_id = await async_client.pagination_tests.cursor_id.list(
            limit=0,
            next_id="next_id",
        )
        assert_matches_type(AsyncPageCursorID[MyModel], cursor_id, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSink) -> None:
        response = await async_client.pagination_tests.cursor_id.with_raw_response.list()

        assert response.is_closed is True
        cursor_id = response.parse()
        assert_matches_type(AsyncPageCursorID[MyModel], cursor_id, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSink) -> None:
        async with async_client.pagination_tests.cursor_id.with_streaming_response.list() as response:
            assert not response.is_closed

            cursor_id = await response.parse()
            assert_matches_type(AsyncPageCursorID[MyModel], cursor_id, path=["response"])

        assert cast(Any, response.is_closed) is True
