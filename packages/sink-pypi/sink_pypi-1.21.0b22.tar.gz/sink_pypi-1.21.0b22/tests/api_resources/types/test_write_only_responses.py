# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.types import WriteOnlyResponseSimpleResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestWriteOnlyResponses:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_simple(self, client: Sink) -> None:
        write_only_response = client.types.write_only_responses.simple()
        assert_matches_type(WriteOnlyResponseSimpleResponse, write_only_response, path=["response"])

    @parametrize
    def test_raw_response_simple(self, client: Sink) -> None:
        response = client.types.write_only_responses.with_raw_response.simple()

        assert response.is_closed is True
        write_only_response = response.parse()
        assert_matches_type(WriteOnlyResponseSimpleResponse, write_only_response, path=["response"])

    @parametrize
    def test_streaming_response_simple(self, client: Sink) -> None:
        with client.types.write_only_responses.with_streaming_response.simple() as response:
            assert not response.is_closed

            write_only_response = response.parse()
            assert_matches_type(WriteOnlyResponseSimpleResponse, write_only_response, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncWriteOnlyResponses:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_simple(self, async_client: AsyncSink) -> None:
        write_only_response = await async_client.types.write_only_responses.simple()
        assert_matches_type(WriteOnlyResponseSimpleResponse, write_only_response, path=["response"])

    @parametrize
    async def test_raw_response_simple(self, async_client: AsyncSink) -> None:
        response = await async_client.types.write_only_responses.with_raw_response.simple()

        assert response.is_closed is True
        write_only_response = response.parse()
        assert_matches_type(WriteOnlyResponseSimpleResponse, write_only_response, path=["response"])

    @parametrize
    async def test_streaming_response_simple(self, async_client: AsyncSink) -> None:
        async with async_client.types.write_only_responses.with_streaming_response.simple() as response:
            assert not response.is_closed

            write_only_response = await response.parse()
            assert_matches_type(WriteOnlyResponseSimpleResponse, write_only_response, path=["response"])

        assert cast(Any, response.is_closed) is True
