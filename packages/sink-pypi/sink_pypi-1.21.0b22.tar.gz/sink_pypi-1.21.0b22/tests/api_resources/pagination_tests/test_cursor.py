# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import MyModel
from sink.api.sdk.pagination import (
    SyncPageCursor,
    AsyncPageCursor,
    SyncPageCursorWithHasMore,
    SyncPageCursorWithReverse,
    AsyncPageCursorWithHasMore,
    AsyncPageCursorWithReverse,
    SyncPageCursorWithNestedHasMore,
    AsyncPageCursorWithNestedHasMore,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCursor:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Sink) -> None:
        cursor = client.pagination_tests.cursor.list()
        assert_matches_type(SyncPageCursor[MyModel], cursor, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Sink) -> None:
        cursor = client.pagination_tests.cursor.list(
            cursor="cursor",
            limit=0,
        )
        assert_matches_type(SyncPageCursor[MyModel], cursor, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Sink) -> None:
        response = client.pagination_tests.cursor.with_raw_response.list()

        assert response.is_closed is True
        cursor = response.parse()
        assert_matches_type(SyncPageCursor[MyModel], cursor, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Sink) -> None:
        with client.pagination_tests.cursor.with_streaming_response.list() as response:
            assert not response.is_closed

            cursor = response.parse()
            assert_matches_type(SyncPageCursor[MyModel], cursor, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list_has_more(self, client: Sink) -> None:
        cursor = client.pagination_tests.cursor.list_has_more()
        assert_matches_type(SyncPageCursorWithHasMore[MyModel], cursor, path=["response"])

    @parametrize
    def test_method_list_has_more_with_all_params(self, client: Sink) -> None:
        cursor = client.pagination_tests.cursor.list_has_more(
            cursor="cursor",
            limit=0,
        )
        assert_matches_type(SyncPageCursorWithHasMore[MyModel], cursor, path=["response"])

    @parametrize
    def test_raw_response_list_has_more(self, client: Sink) -> None:
        response = client.pagination_tests.cursor.with_raw_response.list_has_more()

        assert response.is_closed is True
        cursor = response.parse()
        assert_matches_type(SyncPageCursorWithHasMore[MyModel], cursor, path=["response"])

    @parametrize
    def test_streaming_response_list_has_more(self, client: Sink) -> None:
        with client.pagination_tests.cursor.with_streaming_response.list_has_more() as response:
            assert not response.is_closed

            cursor = response.parse()
            assert_matches_type(SyncPageCursorWithHasMore[MyModel], cursor, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list_nested_has_more(self, client: Sink) -> None:
        cursor = client.pagination_tests.cursor.list_nested_has_more()
        assert_matches_type(SyncPageCursorWithNestedHasMore[MyModel], cursor, path=["response"])

    @parametrize
    def test_method_list_nested_has_more_with_all_params(self, client: Sink) -> None:
        cursor = client.pagination_tests.cursor.list_nested_has_more(
            cursor="cursor",
            limit=0,
        )
        assert_matches_type(SyncPageCursorWithNestedHasMore[MyModel], cursor, path=["response"])

    @parametrize
    def test_raw_response_list_nested_has_more(self, client: Sink) -> None:
        response = client.pagination_tests.cursor.with_raw_response.list_nested_has_more()

        assert response.is_closed is True
        cursor = response.parse()
        assert_matches_type(SyncPageCursorWithNestedHasMore[MyModel], cursor, path=["response"])

    @parametrize
    def test_streaming_response_list_nested_has_more(self, client: Sink) -> None:
        with client.pagination_tests.cursor.with_streaming_response.list_nested_has_more() as response:
            assert not response.is_closed

            cursor = response.parse()
            assert_matches_type(SyncPageCursorWithNestedHasMore[MyModel], cursor, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list_reverse(self, client: Sink) -> None:
        cursor = client.pagination_tests.cursor.list_reverse()
        assert_matches_type(SyncPageCursorWithReverse[MyModel], cursor, path=["response"])

    @parametrize
    def test_method_list_reverse_with_all_params(self, client: Sink) -> None:
        cursor = client.pagination_tests.cursor.list_reverse(
            after_id="after_id",
            before_id="before_id",
            limit=0,
        )
        assert_matches_type(SyncPageCursorWithReverse[MyModel], cursor, path=["response"])

    @parametrize
    def test_raw_response_list_reverse(self, client: Sink) -> None:
        response = client.pagination_tests.cursor.with_raw_response.list_reverse()

        assert response.is_closed is True
        cursor = response.parse()
        assert_matches_type(SyncPageCursorWithReverse[MyModel], cursor, path=["response"])

    @parametrize
    def test_streaming_response_list_reverse(self, client: Sink) -> None:
        with client.pagination_tests.cursor.with_streaming_response.list_reverse() as response:
            assert not response.is_closed

            cursor = response.parse()
            assert_matches_type(SyncPageCursorWithReverse[MyModel], cursor, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncCursor:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_list(self, async_client: AsyncSink) -> None:
        cursor = await async_client.pagination_tests.cursor.list()
        assert_matches_type(AsyncPageCursor[MyModel], cursor, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSink) -> None:
        cursor = await async_client.pagination_tests.cursor.list(
            cursor="cursor",
            limit=0,
        )
        assert_matches_type(AsyncPageCursor[MyModel], cursor, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSink) -> None:
        response = await async_client.pagination_tests.cursor.with_raw_response.list()

        assert response.is_closed is True
        cursor = response.parse()
        assert_matches_type(AsyncPageCursor[MyModel], cursor, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSink) -> None:
        async with async_client.pagination_tests.cursor.with_streaming_response.list() as response:
            assert not response.is_closed

            cursor = await response.parse()
            assert_matches_type(AsyncPageCursor[MyModel], cursor, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list_has_more(self, async_client: AsyncSink) -> None:
        cursor = await async_client.pagination_tests.cursor.list_has_more()
        assert_matches_type(AsyncPageCursorWithHasMore[MyModel], cursor, path=["response"])

    @parametrize
    async def test_method_list_has_more_with_all_params(self, async_client: AsyncSink) -> None:
        cursor = await async_client.pagination_tests.cursor.list_has_more(
            cursor="cursor",
            limit=0,
        )
        assert_matches_type(AsyncPageCursorWithHasMore[MyModel], cursor, path=["response"])

    @parametrize
    async def test_raw_response_list_has_more(self, async_client: AsyncSink) -> None:
        response = await async_client.pagination_tests.cursor.with_raw_response.list_has_more()

        assert response.is_closed is True
        cursor = response.parse()
        assert_matches_type(AsyncPageCursorWithHasMore[MyModel], cursor, path=["response"])

    @parametrize
    async def test_streaming_response_list_has_more(self, async_client: AsyncSink) -> None:
        async with async_client.pagination_tests.cursor.with_streaming_response.list_has_more() as response:
            assert not response.is_closed

            cursor = await response.parse()
            assert_matches_type(AsyncPageCursorWithHasMore[MyModel], cursor, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list_nested_has_more(self, async_client: AsyncSink) -> None:
        cursor = await async_client.pagination_tests.cursor.list_nested_has_more()
        assert_matches_type(AsyncPageCursorWithNestedHasMore[MyModel], cursor, path=["response"])

    @parametrize
    async def test_method_list_nested_has_more_with_all_params(self, async_client: AsyncSink) -> None:
        cursor = await async_client.pagination_tests.cursor.list_nested_has_more(
            cursor="cursor",
            limit=0,
        )
        assert_matches_type(AsyncPageCursorWithNestedHasMore[MyModel], cursor, path=["response"])

    @parametrize
    async def test_raw_response_list_nested_has_more(self, async_client: AsyncSink) -> None:
        response = await async_client.pagination_tests.cursor.with_raw_response.list_nested_has_more()

        assert response.is_closed is True
        cursor = response.parse()
        assert_matches_type(AsyncPageCursorWithNestedHasMore[MyModel], cursor, path=["response"])

    @parametrize
    async def test_streaming_response_list_nested_has_more(self, async_client: AsyncSink) -> None:
        async with async_client.pagination_tests.cursor.with_streaming_response.list_nested_has_more() as response:
            assert not response.is_closed

            cursor = await response.parse()
            assert_matches_type(AsyncPageCursorWithNestedHasMore[MyModel], cursor, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list_reverse(self, async_client: AsyncSink) -> None:
        cursor = await async_client.pagination_tests.cursor.list_reverse()
        assert_matches_type(AsyncPageCursorWithReverse[MyModel], cursor, path=["response"])

    @parametrize
    async def test_method_list_reverse_with_all_params(self, async_client: AsyncSink) -> None:
        cursor = await async_client.pagination_tests.cursor.list_reverse(
            after_id="after_id",
            before_id="before_id",
            limit=0,
        )
        assert_matches_type(AsyncPageCursorWithReverse[MyModel], cursor, path=["response"])

    @parametrize
    async def test_raw_response_list_reverse(self, async_client: AsyncSink) -> None:
        response = await async_client.pagination_tests.cursor.with_raw_response.list_reverse()

        assert response.is_closed is True
        cursor = response.parse()
        assert_matches_type(AsyncPageCursorWithReverse[MyModel], cursor, path=["response"])

    @parametrize
    async def test_streaming_response_list_reverse(self, async_client: AsyncSink) -> None:
        async with async_client.pagination_tests.cursor.with_streaming_response.list_reverse() as response:
            assert not response.is_closed

            cursor = await response.parse()
            assert_matches_type(AsyncPageCursorWithReverse[MyModel], cursor, path=["response"])

        assert cast(Any, response.is_closed) is True
