# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import MyModel
from sink.api.sdk.pagination import (
    SyncPageOffset,
    AsyncPageOffset,
    SyncPageOffsetTotalCount,
    AsyncPageOffsetTotalCount,
    SyncPageOffsetNoStartField,
    AsyncPageOffsetNoStartField,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestOffset:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Sink) -> None:
        offset = client.pagination_tests.offset.list()
        assert_matches_type(SyncPageOffset[MyModel], offset, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Sink) -> None:
        offset = client.pagination_tests.offset.list(
            limit=0,
            offset=0,
        )
        assert_matches_type(SyncPageOffset[MyModel], offset, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Sink) -> None:
        response = client.pagination_tests.offset.with_raw_response.list()

        assert response.is_closed is True
        offset = response.parse()
        assert_matches_type(SyncPageOffset[MyModel], offset, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Sink) -> None:
        with client.pagination_tests.offset.with_streaming_response.list() as response:
            assert not response.is_closed

            offset = response.parse()
            assert_matches_type(SyncPageOffset[MyModel], offset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list_no_start_field(self, client: Sink) -> None:
        offset = client.pagination_tests.offset.list_no_start_field()
        assert_matches_type(SyncPageOffsetNoStartField[MyModel], offset, path=["response"])

    @parametrize
    def test_method_list_no_start_field_with_all_params(self, client: Sink) -> None:
        offset = client.pagination_tests.offset.list_no_start_field(
            limit=0,
            offset=0,
        )
        assert_matches_type(SyncPageOffsetNoStartField[MyModel], offset, path=["response"])

    @parametrize
    def test_raw_response_list_no_start_field(self, client: Sink) -> None:
        response = client.pagination_tests.offset.with_raw_response.list_no_start_field()

        assert response.is_closed is True
        offset = response.parse()
        assert_matches_type(SyncPageOffsetNoStartField[MyModel], offset, path=["response"])

    @parametrize
    def test_streaming_response_list_no_start_field(self, client: Sink) -> None:
        with client.pagination_tests.offset.with_streaming_response.list_no_start_field() as response:
            assert not response.is_closed

            offset = response.parse()
            assert_matches_type(SyncPageOffsetNoStartField[MyModel], offset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_with_total_count(self, client: Sink) -> None:
        offset = client.pagination_tests.offset.with_total_count()
        assert_matches_type(SyncPageOffsetTotalCount[MyModel], offset, path=["response"])

    @parametrize
    def test_method_with_total_count_with_all_params(self, client: Sink) -> None:
        offset = client.pagination_tests.offset.with_total_count(
            limit=0,
            offset=0,
        )
        assert_matches_type(SyncPageOffsetTotalCount[MyModel], offset, path=["response"])

    @parametrize
    def test_raw_response_with_total_count(self, client: Sink) -> None:
        response = client.pagination_tests.offset.with_raw_response.with_total_count()

        assert response.is_closed is True
        offset = response.parse()
        assert_matches_type(SyncPageOffsetTotalCount[MyModel], offset, path=["response"])

    @parametrize
    def test_streaming_response_with_total_count(self, client: Sink) -> None:
        with client.pagination_tests.offset.with_streaming_response.with_total_count() as response:
            assert not response.is_closed

            offset = response.parse()
            assert_matches_type(SyncPageOffsetTotalCount[MyModel], offset, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncOffset:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_list(self, async_client: AsyncSink) -> None:
        offset = await async_client.pagination_tests.offset.list()
        assert_matches_type(AsyncPageOffset[MyModel], offset, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSink) -> None:
        offset = await async_client.pagination_tests.offset.list(
            limit=0,
            offset=0,
        )
        assert_matches_type(AsyncPageOffset[MyModel], offset, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSink) -> None:
        response = await async_client.pagination_tests.offset.with_raw_response.list()

        assert response.is_closed is True
        offset = response.parse()
        assert_matches_type(AsyncPageOffset[MyModel], offset, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSink) -> None:
        async with async_client.pagination_tests.offset.with_streaming_response.list() as response:
            assert not response.is_closed

            offset = await response.parse()
            assert_matches_type(AsyncPageOffset[MyModel], offset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list_no_start_field(self, async_client: AsyncSink) -> None:
        offset = await async_client.pagination_tests.offset.list_no_start_field()
        assert_matches_type(AsyncPageOffsetNoStartField[MyModel], offset, path=["response"])

    @parametrize
    async def test_method_list_no_start_field_with_all_params(self, async_client: AsyncSink) -> None:
        offset = await async_client.pagination_tests.offset.list_no_start_field(
            limit=0,
            offset=0,
        )
        assert_matches_type(AsyncPageOffsetNoStartField[MyModel], offset, path=["response"])

    @parametrize
    async def test_raw_response_list_no_start_field(self, async_client: AsyncSink) -> None:
        response = await async_client.pagination_tests.offset.with_raw_response.list_no_start_field()

        assert response.is_closed is True
        offset = response.parse()
        assert_matches_type(AsyncPageOffsetNoStartField[MyModel], offset, path=["response"])

    @parametrize
    async def test_streaming_response_list_no_start_field(self, async_client: AsyncSink) -> None:
        async with async_client.pagination_tests.offset.with_streaming_response.list_no_start_field() as response:
            assert not response.is_closed

            offset = await response.parse()
            assert_matches_type(AsyncPageOffsetNoStartField[MyModel], offset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_with_total_count(self, async_client: AsyncSink) -> None:
        offset = await async_client.pagination_tests.offset.with_total_count()
        assert_matches_type(AsyncPageOffsetTotalCount[MyModel], offset, path=["response"])

    @parametrize
    async def test_method_with_total_count_with_all_params(self, async_client: AsyncSink) -> None:
        offset = await async_client.pagination_tests.offset.with_total_count(
            limit=0,
            offset=0,
        )
        assert_matches_type(AsyncPageOffsetTotalCount[MyModel], offset, path=["response"])

    @parametrize
    async def test_raw_response_with_total_count(self, async_client: AsyncSink) -> None:
        response = await async_client.pagination_tests.offset.with_raw_response.with_total_count()

        assert response.is_closed is True
        offset = response.parse()
        assert_matches_type(AsyncPageOffsetTotalCount[MyModel], offset, path=["response"])

    @parametrize
    async def test_streaming_response_with_total_count(self, async_client: AsyncSink) -> None:
        async with async_client.pagination_tests.offset.with_streaming_response.with_total_count() as response:
            assert not response.is_closed

            offset = await response.parse()
            assert_matches_type(AsyncPageOffsetTotalCount[MyModel], offset, path=["response"])

        assert cast(Any, response.is_closed) is True
