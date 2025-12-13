# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sink.api.sdk import Sink, AsyncSink

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTests:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_run_codegen(self, client: Sink) -> None:
        test = client.tests.run_codegen()
        assert test is None

    @parametrize
    def test_raw_response_run_codegen(self, client: Sink) -> None:
        response = client.tests.with_raw_response.run_codegen()

        assert response.is_closed is True
        test = response.parse()
        assert test is None

    @parametrize
    def test_streaming_response_run_codegen(self, client: Sink) -> None:
        with client.tests.with_streaming_response.run_codegen() as response:
            assert not response.is_closed

            test = response.parse()
            assert test is None

        assert cast(Any, response.is_closed) is True


class TestAsyncTests:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_run_codegen(self, async_client: AsyncSink) -> None:
        test = await async_client.tests.run_codegen()
        assert test is None

    @parametrize
    async def test_raw_response_run_codegen(self, async_client: AsyncSink) -> None:
        response = await async_client.tests.with_raw_response.run_codegen()

        assert response.is_closed is True
        test = response.parse()
        assert test is None

    @parametrize
    async def test_streaming_response_run_codegen(self, async_client: AsyncSink) -> None:
        async with async_client.tests.with_streaming_response.run_codegen() as response:
            assert not response.is_closed

            test = await response.parse()
            assert test is None

        assert cast(Any, response.is_closed) is True
