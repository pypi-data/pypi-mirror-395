# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.types import ReadOnlyParamSimpleResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestReadOnlyParams:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_simple(self, client: Sink) -> None:
        read_only_param = client.types.read_only_params.simple()
        assert_matches_type(ReadOnlyParamSimpleResponse, read_only_param, path=["response"])

    @parametrize
    def test_method_simple_with_all_params(self, client: Sink) -> None:
        read_only_param = client.types.read_only_params.simple(
            should_show_up="should_show_up",
        )
        assert_matches_type(ReadOnlyParamSimpleResponse, read_only_param, path=["response"])

    @parametrize
    def test_raw_response_simple(self, client: Sink) -> None:
        response = client.types.read_only_params.with_raw_response.simple()

        assert response.is_closed is True
        read_only_param = response.parse()
        assert_matches_type(ReadOnlyParamSimpleResponse, read_only_param, path=["response"])

    @parametrize
    def test_streaming_response_simple(self, client: Sink) -> None:
        with client.types.read_only_params.with_streaming_response.simple() as response:
            assert not response.is_closed

            read_only_param = response.parse()
            assert_matches_type(ReadOnlyParamSimpleResponse, read_only_param, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncReadOnlyParams:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_simple(self, async_client: AsyncSink) -> None:
        read_only_param = await async_client.types.read_only_params.simple()
        assert_matches_type(ReadOnlyParamSimpleResponse, read_only_param, path=["response"])

    @parametrize
    async def test_method_simple_with_all_params(self, async_client: AsyncSink) -> None:
        read_only_param = await async_client.types.read_only_params.simple(
            should_show_up="should_show_up",
        )
        assert_matches_type(ReadOnlyParamSimpleResponse, read_only_param, path=["response"])

    @parametrize
    async def test_raw_response_simple(self, async_client: AsyncSink) -> None:
        response = await async_client.types.read_only_params.with_raw_response.simple()

        assert response.is_closed is True
        read_only_param = response.parse()
        assert_matches_type(ReadOnlyParamSimpleResponse, read_only_param, path=["response"])

    @parametrize
    async def test_streaming_response_simple(self, async_client: AsyncSink) -> None:
        async with async_client.types.read_only_params.with_streaming_response.simple() as response:
            assert not response.is_closed

            read_only_param = await response.parse()
            assert_matches_type(ReadOnlyParamSimpleResponse, read_only_param, path=["response"])

        assert cast(Any, response.is_closed) is True
