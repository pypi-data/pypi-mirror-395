# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.types import ArrayFloatItemsResponse, ArrayObjectItemsResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestArrays:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_float_items(self, client: Sink) -> None:
        array = client.types.arrays.float_items()
        assert_matches_type(ArrayFloatItemsResponse, array, path=["response"])

    @parametrize
    def test_raw_response_float_items(self, client: Sink) -> None:
        response = client.types.arrays.with_raw_response.float_items()

        assert response.is_closed is True
        array = response.parse()
        assert_matches_type(ArrayFloatItemsResponse, array, path=["response"])

    @parametrize
    def test_streaming_response_float_items(self, client: Sink) -> None:
        with client.types.arrays.with_streaming_response.float_items() as response:
            assert not response.is_closed

            array = response.parse()
            assert_matches_type(ArrayFloatItemsResponse, array, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_nested_in_params(self, client: Sink) -> None:
        array = client.types.arrays.nested_in_params()
        assert array is None

    @parametrize
    def test_raw_response_nested_in_params(self, client: Sink) -> None:
        response = client.types.arrays.with_raw_response.nested_in_params()

        assert response.is_closed is True
        array = response.parse()
        assert array is None

    @parametrize
    def test_streaming_response_nested_in_params(self, client: Sink) -> None:
        with client.types.arrays.with_streaming_response.nested_in_params() as response:
            assert not response.is_closed

            array = response.parse()
            assert array is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_object_items(self, client: Sink) -> None:
        array = client.types.arrays.object_items()
        assert_matches_type(ArrayObjectItemsResponse, array, path=["response"])

    @parametrize
    def test_raw_response_object_items(self, client: Sink) -> None:
        response = client.types.arrays.with_raw_response.object_items()

        assert response.is_closed is True
        array = response.parse()
        assert_matches_type(ArrayObjectItemsResponse, array, path=["response"])

    @parametrize
    def test_streaming_response_object_items(self, client: Sink) -> None:
        with client.types.arrays.with_streaming_response.object_items() as response:
            assert not response.is_closed

            array = response.parse()
            assert_matches_type(ArrayObjectItemsResponse, array, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncArrays:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_float_items(self, async_client: AsyncSink) -> None:
        array = await async_client.types.arrays.float_items()
        assert_matches_type(ArrayFloatItemsResponse, array, path=["response"])

    @parametrize
    async def test_raw_response_float_items(self, async_client: AsyncSink) -> None:
        response = await async_client.types.arrays.with_raw_response.float_items()

        assert response.is_closed is True
        array = response.parse()
        assert_matches_type(ArrayFloatItemsResponse, array, path=["response"])

    @parametrize
    async def test_streaming_response_float_items(self, async_client: AsyncSink) -> None:
        async with async_client.types.arrays.with_streaming_response.float_items() as response:
            assert not response.is_closed

            array = await response.parse()
            assert_matches_type(ArrayFloatItemsResponse, array, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_nested_in_params(self, async_client: AsyncSink) -> None:
        array = await async_client.types.arrays.nested_in_params()
        assert array is None

    @parametrize
    async def test_raw_response_nested_in_params(self, async_client: AsyncSink) -> None:
        response = await async_client.types.arrays.with_raw_response.nested_in_params()

        assert response.is_closed is True
        array = response.parse()
        assert array is None

    @parametrize
    async def test_streaming_response_nested_in_params(self, async_client: AsyncSink) -> None:
        async with async_client.types.arrays.with_streaming_response.nested_in_params() as response:
            assert not response.is_closed

            array = await response.parse()
            assert array is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_object_items(self, async_client: AsyncSink) -> None:
        array = await async_client.types.arrays.object_items()
        assert_matches_type(ArrayObjectItemsResponse, array, path=["response"])

    @parametrize
    async def test_raw_response_object_items(self, async_client: AsyncSink) -> None:
        response = await async_client.types.arrays.with_raw_response.object_items()

        assert response.is_closed is True
        array = response.parse()
        assert_matches_type(ArrayObjectItemsResponse, array, path=["response"])

    @parametrize
    async def test_streaming_response_object_items(self, async_client: AsyncSink) -> None:
        async with async_client.types.arrays.with_streaming_response.object_items() as response:
            assert not response.is_closed

            array = await response.parse()
            assert_matches_type(ArrayObjectItemsResponse, array, path=["response"])

        assert cast(Any, response.is_closed) is True
