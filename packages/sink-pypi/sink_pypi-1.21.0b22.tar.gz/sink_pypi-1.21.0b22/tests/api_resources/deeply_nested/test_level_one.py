# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import Card

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestLevelOne:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_method_level_1(self, client: Sink) -> None:
        level_one = client.deeply_nested.level_one.method_level_1(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Card, level_one, path=["response"])

    @parametrize
    def test_raw_response_method_level_1(self, client: Sink) -> None:
        response = client.deeply_nested.level_one.with_raw_response.method_level_1(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        level_one = response.parse()
        assert_matches_type(Card, level_one, path=["response"])

    @parametrize
    def test_streaming_response_method_level_1(self, client: Sink) -> None:
        with client.deeply_nested.level_one.with_streaming_response.method_level_1(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed

            level_one = response.parse()
            assert_matches_type(Card, level_one, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_method_level_1(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_token` but received ''"):
            client.deeply_nested.level_one.with_raw_response.method_level_1(
                "",
            )


class TestAsyncLevelOne:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_method_level_1(self, async_client: AsyncSink) -> None:
        level_one = await async_client.deeply_nested.level_one.method_level_1(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Card, level_one, path=["response"])

    @parametrize
    async def test_raw_response_method_level_1(self, async_client: AsyncSink) -> None:
        response = await async_client.deeply_nested.level_one.with_raw_response.method_level_1(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        level_one = response.parse()
        assert_matches_type(Card, level_one, path=["response"])

    @parametrize
    async def test_streaming_response_method_level_1(self, async_client: AsyncSink) -> None:
        async with async_client.deeply_nested.level_one.with_streaming_response.method_level_1(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed

            level_one = await response.parse()
            assert_matches_type(Card, level_one, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_method_level_1(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_token` but received ''"):
            await async_client.deeply_nested.level_one.with_raw_response.method_level_1(
                "",
            )
