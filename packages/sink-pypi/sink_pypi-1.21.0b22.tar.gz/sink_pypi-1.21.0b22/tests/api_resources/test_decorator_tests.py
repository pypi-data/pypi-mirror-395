# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import DecoratorTestKeepMeResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDecoratorTests:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_keep_me(self, client: Sink) -> None:
        decorator_test = client.decorator_tests.keep_me()
        assert_matches_type(DecoratorTestKeepMeResponse, decorator_test, path=["response"])

    @parametrize
    def test_raw_response_keep_me(self, client: Sink) -> None:
        response = client.decorator_tests.with_raw_response.keep_me()

        assert response.is_closed is True
        decorator_test = response.parse()
        assert_matches_type(DecoratorTestKeepMeResponse, decorator_test, path=["response"])

    @parametrize
    def test_streaming_response_keep_me(self, client: Sink) -> None:
        with client.decorator_tests.with_streaming_response.keep_me() as response:
            assert not response.is_closed

            decorator_test = response.parse()
            assert_matches_type(DecoratorTestKeepMeResponse, decorator_test, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDecoratorTests:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_keep_me(self, async_client: AsyncSink) -> None:
        decorator_test = await async_client.decorator_tests.keep_me()
        assert_matches_type(DecoratorTestKeepMeResponse, decorator_test, path=["response"])

    @parametrize
    async def test_raw_response_keep_me(self, async_client: AsyncSink) -> None:
        response = await async_client.decorator_tests.with_raw_response.keep_me()

        assert response.is_closed is True
        decorator_test = response.parse()
        assert_matches_type(DecoratorTestKeepMeResponse, decorator_test, path=["response"])

    @parametrize
    async def test_streaming_response_keep_me(self, async_client: AsyncSink) -> None:
        async with async_client.decorator_tests.with_streaming_response.keep_me() as response:
            assert not response.is_closed

            decorator_test = await response.parse()
            assert_matches_type(DecoratorTestKeepMeResponse, decorator_test, path=["response"])

        assert cast(Any, response.is_closed) is True
