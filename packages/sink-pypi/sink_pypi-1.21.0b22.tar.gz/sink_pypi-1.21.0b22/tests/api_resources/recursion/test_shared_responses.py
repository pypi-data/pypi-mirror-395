# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.shared import SharedSelfRecursion

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSharedResponses:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create_self(self, client: Sink) -> None:
        shared_response = client.recursion.shared_responses.create_self()
        assert_matches_type(SharedSelfRecursion, shared_response, path=["response"])

    @parametrize
    def test_raw_response_create_self(self, client: Sink) -> None:
        response = client.recursion.shared_responses.with_raw_response.create_self()

        assert response.is_closed is True
        shared_response = response.parse()
        assert_matches_type(SharedSelfRecursion, shared_response, path=["response"])

    @parametrize
    def test_streaming_response_create_self(self, client: Sink) -> None:
        with client.recursion.shared_responses.with_streaming_response.create_self() as response:
            assert not response.is_closed

            shared_response = response.parse()
            assert_matches_type(SharedSelfRecursion, shared_response, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSharedResponses:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create_self(self, async_client: AsyncSink) -> None:
        shared_response = await async_client.recursion.shared_responses.create_self()
        assert_matches_type(SharedSelfRecursion, shared_response, path=["response"])

    @parametrize
    async def test_raw_response_create_self(self, async_client: AsyncSink) -> None:
        response = await async_client.recursion.shared_responses.with_raw_response.create_self()

        assert response.is_closed is True
        shared_response = response.parse()
        assert_matches_type(SharedSelfRecursion, shared_response, path=["response"])

    @parametrize
    async def test_streaming_response_create_self(self, async_client: AsyncSink) -> None:
        async with async_client.recursion.shared_responses.with_streaming_response.create_self() as response:
            assert not response.is_closed

            shared_response = await response.parse()
            assert_matches_type(SharedSelfRecursion, shared_response, path=["response"])

        assert cast(Any, response.is_closed) is True
