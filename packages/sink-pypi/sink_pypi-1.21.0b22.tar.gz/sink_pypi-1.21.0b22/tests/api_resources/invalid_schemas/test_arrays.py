# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.invalid_schemas import ArrayMissingItemsResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestArrays:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_missing_items(self, client: Sink) -> None:
        array = client.invalid_schemas.arrays.missing_items()
        assert_matches_type(ArrayMissingItemsResponse, array, path=["response"])

    @parametrize
    def test_raw_response_missing_items(self, client: Sink) -> None:
        response = client.invalid_schemas.arrays.with_raw_response.missing_items()

        assert response.is_closed is True
        array = response.parse()
        assert_matches_type(ArrayMissingItemsResponse, array, path=["response"])

    @parametrize
    def test_streaming_response_missing_items(self, client: Sink) -> None:
        with client.invalid_schemas.arrays.with_streaming_response.missing_items() as response:
            assert not response.is_closed

            array = response.parse()
            assert_matches_type(ArrayMissingItemsResponse, array, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncArrays:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_missing_items(self, async_client: AsyncSink) -> None:
        array = await async_client.invalid_schemas.arrays.missing_items()
        assert_matches_type(ArrayMissingItemsResponse, array, path=["response"])

    @parametrize
    async def test_raw_response_missing_items(self, async_client: AsyncSink) -> None:
        response = await async_client.invalid_schemas.arrays.with_raw_response.missing_items()

        assert response.is_closed is True
        array = response.parse()
        assert_matches_type(ArrayMissingItemsResponse, array, path=["response"])

    @parametrize
    async def test_streaming_response_missing_items(self, async_client: AsyncSink) -> None:
        async with async_client.invalid_schemas.arrays.with_streaming_response.missing_items() as response:
            assert not response.is_closed

            array = await response.parse()
            assert_matches_type(ArrayMissingItemsResponse, array, path=["response"])

        assert cast(Any, response.is_closed) is True
