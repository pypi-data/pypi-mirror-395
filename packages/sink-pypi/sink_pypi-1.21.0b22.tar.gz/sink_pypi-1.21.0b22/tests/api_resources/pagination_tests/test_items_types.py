# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.pagination import SyncPagePageNumber, AsyncPagePageNumber

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestItemsTypes:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list_unknown(self, client: Sink) -> None:
        items_type = client.pagination_tests.items_types.list_unknown()
        assert_matches_type(SyncPagePageNumber[object], items_type, path=["response"])

    @parametrize
    def test_method_list_unknown_with_all_params(self, client: Sink) -> None:
        items_type = client.pagination_tests.items_types.list_unknown(
            page=0,
            page_size=0,
        )
        assert_matches_type(SyncPagePageNumber[object], items_type, path=["response"])

    @parametrize
    def test_raw_response_list_unknown(self, client: Sink) -> None:
        response = client.pagination_tests.items_types.with_raw_response.list_unknown()

        assert response.is_closed is True
        items_type = response.parse()
        assert_matches_type(SyncPagePageNumber[object], items_type, path=["response"])

    @parametrize
    def test_streaming_response_list_unknown(self, client: Sink) -> None:
        with client.pagination_tests.items_types.with_streaming_response.list_unknown() as response:
            assert not response.is_closed

            items_type = response.parse()
            assert_matches_type(SyncPagePageNumber[object], items_type, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncItemsTypes:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_list_unknown(self, async_client: AsyncSink) -> None:
        items_type = await async_client.pagination_tests.items_types.list_unknown()
        assert_matches_type(AsyncPagePageNumber[object], items_type, path=["response"])

    @parametrize
    async def test_method_list_unknown_with_all_params(self, async_client: AsyncSink) -> None:
        items_type = await async_client.pagination_tests.items_types.list_unknown(
            page=0,
            page_size=0,
        )
        assert_matches_type(AsyncPagePageNumber[object], items_type, path=["response"])

    @parametrize
    async def test_raw_response_list_unknown(self, async_client: AsyncSink) -> None:
        response = await async_client.pagination_tests.items_types.with_raw_response.list_unknown()

        assert response.is_closed is True
        items_type = response.parse()
        assert_matches_type(AsyncPagePageNumber[object], items_type, path=["response"])

    @parametrize
    async def test_streaming_response_list_unknown(self, async_client: AsyncSink) -> None:
        async with async_client.pagination_tests.items_types.with_streaming_response.list_unknown() as response:
            assert not response.is_closed

            items_type = await response.parse()
            assert_matches_type(AsyncPagePageNumber[object], items_type, path=["response"])

        assert cast(Any, response.is_closed) is True
