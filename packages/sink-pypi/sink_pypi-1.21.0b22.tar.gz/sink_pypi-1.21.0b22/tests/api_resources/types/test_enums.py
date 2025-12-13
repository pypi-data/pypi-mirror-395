# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.types import (
    EnumBasicResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEnums:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_array_unique_values(self, client: Sink) -> None:
        enum = client.types.enums.array_unique_values(
            body=["USD"],
        )
        assert enum is None

    @parametrize
    def test_raw_response_array_unique_values(self, client: Sink) -> None:
        response = client.types.enums.with_raw_response.array_unique_values(
            body=["USD"],
        )

        assert response.is_closed is True
        enum = response.parse()
        assert enum is None

    @parametrize
    def test_streaming_response_array_unique_values(self, client: Sink) -> None:
        with client.types.enums.with_streaming_response.array_unique_values(
            body=["USD"],
        ) as response:
            assert not response.is_closed

            enum = response.parse()
            assert enum is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_array_unique_values_2_values(self, client: Sink) -> None:
        enum = client.types.enums.array_unique_values_2_values(
            body=["USD"],
        )
        assert enum is None

    @parametrize
    def test_raw_response_array_unique_values_2_values(self, client: Sink) -> None:
        response = client.types.enums.with_raw_response.array_unique_values_2_values(
            body=["USD"],
        )

        assert response.is_closed is True
        enum = response.parse()
        assert enum is None

    @parametrize
    def test_streaming_response_array_unique_values_2_values(self, client: Sink) -> None:
        with client.types.enums.with_streaming_response.array_unique_values_2_values(
            body=["USD"],
        ) as response:
            assert not response.is_closed

            enum = response.parse()
            assert enum is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_array_unique_values_numbers(self, client: Sink) -> None:
        enum = client.types.enums.array_unique_values_numbers(
            body=[5],
        )
        assert enum is None

    @parametrize
    def test_raw_response_array_unique_values_numbers(self, client: Sink) -> None:
        response = client.types.enums.with_raw_response.array_unique_values_numbers(
            body=[5],
        )

        assert response.is_closed is True
        enum = response.parse()
        assert enum is None

    @parametrize
    def test_streaming_response_array_unique_values_numbers(self, client: Sink) -> None:
        with client.types.enums.with_streaming_response.array_unique_values_numbers(
            body=[5],
        ) as response:
            assert not response.is_closed

            enum = response.parse()
            assert enum is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_basic(self, client: Sink) -> None:
        enum = client.types.enums.basic()
        assert_matches_type(EnumBasicResponse, enum, path=["response"])

    @parametrize
    def test_method_basic_with_all_params(self, client: Sink) -> None:
        enum = client.types.enums.basic(
            input_currency="USD",
            problematic_enum="123_FOO",
            uses_const="my_const_enum_value",
        )
        assert_matches_type(EnumBasicResponse, enum, path=["response"])

    @parametrize
    def test_raw_response_basic(self, client: Sink) -> None:
        response = client.types.enums.with_raw_response.basic()

        assert response.is_closed is True
        enum = response.parse()
        assert_matches_type(EnumBasicResponse, enum, path=["response"])

    @parametrize
    def test_streaming_response_basic(self, client: Sink) -> None:
        with client.types.enums.with_streaming_response.basic() as response:
            assert not response.is_closed

            enum = response.parse()
            assert_matches_type(EnumBasicResponse, enum, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncEnums:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_array_unique_values(self, async_client: AsyncSink) -> None:
        enum = await async_client.types.enums.array_unique_values(
            body=["USD"],
        )
        assert enum is None

    @parametrize
    async def test_raw_response_array_unique_values(self, async_client: AsyncSink) -> None:
        response = await async_client.types.enums.with_raw_response.array_unique_values(
            body=["USD"],
        )

        assert response.is_closed is True
        enum = response.parse()
        assert enum is None

    @parametrize
    async def test_streaming_response_array_unique_values(self, async_client: AsyncSink) -> None:
        async with async_client.types.enums.with_streaming_response.array_unique_values(
            body=["USD"],
        ) as response:
            assert not response.is_closed

            enum = await response.parse()
            assert enum is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_array_unique_values_2_values(self, async_client: AsyncSink) -> None:
        enum = await async_client.types.enums.array_unique_values_2_values(
            body=["USD"],
        )
        assert enum is None

    @parametrize
    async def test_raw_response_array_unique_values_2_values(self, async_client: AsyncSink) -> None:
        response = await async_client.types.enums.with_raw_response.array_unique_values_2_values(
            body=["USD"],
        )

        assert response.is_closed is True
        enum = response.parse()
        assert enum is None

    @parametrize
    async def test_streaming_response_array_unique_values_2_values(self, async_client: AsyncSink) -> None:
        async with async_client.types.enums.with_streaming_response.array_unique_values_2_values(
            body=["USD"],
        ) as response:
            assert not response.is_closed

            enum = await response.parse()
            assert enum is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_array_unique_values_numbers(self, async_client: AsyncSink) -> None:
        enum = await async_client.types.enums.array_unique_values_numbers(
            body=[5],
        )
        assert enum is None

    @parametrize
    async def test_raw_response_array_unique_values_numbers(self, async_client: AsyncSink) -> None:
        response = await async_client.types.enums.with_raw_response.array_unique_values_numbers(
            body=[5],
        )

        assert response.is_closed is True
        enum = response.parse()
        assert enum is None

    @parametrize
    async def test_streaming_response_array_unique_values_numbers(self, async_client: AsyncSink) -> None:
        async with async_client.types.enums.with_streaming_response.array_unique_values_numbers(
            body=[5],
        ) as response:
            assert not response.is_closed

            enum = await response.parse()
            assert enum is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_basic(self, async_client: AsyncSink) -> None:
        enum = await async_client.types.enums.basic()
        assert_matches_type(EnumBasicResponse, enum, path=["response"])

    @parametrize
    async def test_method_basic_with_all_params(self, async_client: AsyncSink) -> None:
        enum = await async_client.types.enums.basic(
            input_currency="USD",
            problematic_enum="123_FOO",
            uses_const="my_const_enum_value",
        )
        assert_matches_type(EnumBasicResponse, enum, path=["response"])

    @parametrize
    async def test_raw_response_basic(self, async_client: AsyncSink) -> None:
        response = await async_client.types.enums.with_raw_response.basic()

        assert response.is_closed is True
        enum = response.parse()
        assert_matches_type(EnumBasicResponse, enum, path=["response"])

    @parametrize
    async def test_streaming_response_basic(self, async_client: AsyncSink) -> None:
        async with async_client.types.enums.with_streaming_response.basic() as response:
            assert not response.is_closed

            enum = await response.parse()
            assert_matches_type(EnumBasicResponse, enum, path=["response"])

        assert cast(Any, response.is_closed) is True
