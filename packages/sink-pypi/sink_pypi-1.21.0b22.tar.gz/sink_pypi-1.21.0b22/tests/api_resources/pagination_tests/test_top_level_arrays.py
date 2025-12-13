# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import MyModel
from sink.api.sdk.pagination import SyncPageCursorTopLevelArray, AsyncPageCursorTopLevelArray

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTopLevelArrays:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_basic_cursor(self, client: Sink) -> None:
        top_level_array = client.pagination_tests.top_level_arrays.basic_cursor()
        assert_matches_type(SyncPageCursorTopLevelArray[MyModel], top_level_array, path=["response"])

    @parametrize
    def test_method_basic_cursor_with_all_params(self, client: Sink) -> None:
        top_level_array = client.pagination_tests.top_level_arrays.basic_cursor(
            cursor="cursor",
            limit=0,
        )
        assert_matches_type(SyncPageCursorTopLevelArray[MyModel], top_level_array, path=["response"])

    @parametrize
    def test_raw_response_basic_cursor(self, client: Sink) -> None:
        response = client.pagination_tests.top_level_arrays.with_raw_response.basic_cursor()

        assert response.is_closed is True
        top_level_array = response.parse()
        assert_matches_type(SyncPageCursorTopLevelArray[MyModel], top_level_array, path=["response"])

    @parametrize
    def test_streaming_response_basic_cursor(self, client: Sink) -> None:
        with client.pagination_tests.top_level_arrays.with_streaming_response.basic_cursor() as response:
            assert not response.is_closed

            top_level_array = response.parse()
            assert_matches_type(SyncPageCursorTopLevelArray[MyModel], top_level_array, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTopLevelArrays:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_basic_cursor(self, async_client: AsyncSink) -> None:
        top_level_array = await async_client.pagination_tests.top_level_arrays.basic_cursor()
        assert_matches_type(AsyncPageCursorTopLevelArray[MyModel], top_level_array, path=["response"])

    @parametrize
    async def test_method_basic_cursor_with_all_params(self, async_client: AsyncSink) -> None:
        top_level_array = await async_client.pagination_tests.top_level_arrays.basic_cursor(
            cursor="cursor",
            limit=0,
        )
        assert_matches_type(AsyncPageCursorTopLevelArray[MyModel], top_level_array, path=["response"])

    @parametrize
    async def test_raw_response_basic_cursor(self, async_client: AsyncSink) -> None:
        response = await async_client.pagination_tests.top_level_arrays.with_raw_response.basic_cursor()

        assert response.is_closed is True
        top_level_array = response.parse()
        assert_matches_type(AsyncPageCursorTopLevelArray[MyModel], top_level_array, path=["response"])

    @parametrize
    async def test_streaming_response_basic_cursor(self, async_client: AsyncSink) -> None:
        async with async_client.pagination_tests.top_level_arrays.with_streaming_response.basic_cursor() as response:
            assert not response.is_closed

            top_level_array = await response.parse()
            assert_matches_type(AsyncPageCursorTopLevelArray[MyModel], top_level_array, path=["response"])

        assert cast(Any, response.is_closed) is True
