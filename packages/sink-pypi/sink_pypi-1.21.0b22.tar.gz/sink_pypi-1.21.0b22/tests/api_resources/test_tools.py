# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import ObjectSkippedProps

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTools:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_skipped_params(self, client: Sink) -> None:
        tool = client.tools.skipped_params()
        assert_matches_type(ObjectSkippedProps, tool, path=["response"])

    @parametrize
    def test_method_skipped_params_with_all_params(self, client: Sink) -> None:
        tool = client.tools.skipped_params(
            skipped_go="skipped_go",
            skipped_java="skipped_java",
            skipped_node="skipped_node",
        )
        assert_matches_type(ObjectSkippedProps, tool, path=["response"])

    @parametrize
    def test_raw_response_skipped_params(self, client: Sink) -> None:
        response = client.tools.with_raw_response.skipped_params()

        assert response.is_closed is True
        tool = response.parse()
        assert_matches_type(ObjectSkippedProps, tool, path=["response"])

    @parametrize
    def test_streaming_response_skipped_params(self, client: Sink) -> None:
        with client.tools.with_streaming_response.skipped_params() as response:
            assert not response.is_closed

            tool = response.parse()
            assert_matches_type(ObjectSkippedProps, tool, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTools:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_skipped_params(self, async_client: AsyncSink) -> None:
        tool = await async_client.tools.skipped_params()
        assert_matches_type(ObjectSkippedProps, tool, path=["response"])

    @parametrize
    async def test_method_skipped_params_with_all_params(self, async_client: AsyncSink) -> None:
        tool = await async_client.tools.skipped_params(
            skipped_go="skipped_go",
            skipped_java="skipped_java",
            skipped_node="skipped_node",
        )
        assert_matches_type(ObjectSkippedProps, tool, path=["response"])

    @parametrize
    async def test_raw_response_skipped_params(self, async_client: AsyncSink) -> None:
        response = await async_client.tools.with_raw_response.skipped_params()

        assert response.is_closed is True
        tool = response.parse()
        assert_matches_type(ObjectSkippedProps, tool, path=["response"])

    @parametrize
    async def test_streaming_response_skipped_params(self, async_client: AsyncSink) -> None:
        async with async_client.tools.with_streaming_response.skipped_params() as response:
            assert not response.is_closed

            tool = await response.parse()
            assert_matches_type(ObjectSkippedProps, tool, path=["response"])

        assert cast(Any, response.is_closed) is True
