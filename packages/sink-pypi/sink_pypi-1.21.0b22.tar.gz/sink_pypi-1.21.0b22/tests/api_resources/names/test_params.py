# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sink.api.sdk import Sink, AsyncSink

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestParams:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_options_param(self, client: Sink) -> None:
        param = client.names.params.options_param()
        assert param is None

    @parametrize
    def test_method_options_param_with_all_params(self, client: Sink) -> None:
        param = client.names.params.options_param(
            options="options",
        )
        assert param is None

    @parametrize
    def test_raw_response_options_param(self, client: Sink) -> None:
        response = client.names.params.with_raw_response.options_param()

        assert response.is_closed is True
        param = response.parse()
        assert param is None

    @parametrize
    def test_streaming_response_options_param(self, client: Sink) -> None:
        with client.names.params.with_streaming_response.options_param() as response:
            assert not response.is_closed

            param = response.parse()
            assert param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_timeout_param(self, client: Sink) -> None:
        param = client.names.params.timeout_param()
        assert param is None

    @parametrize
    def test_method_timeout_param_with_all_params(self, client: Sink) -> None:
        param = client.names.params.timeout_param(
            url_timeout=0,
        )
        assert param is None

    @parametrize
    def test_raw_response_timeout_param(self, client: Sink) -> None:
        response = client.names.params.with_raw_response.timeout_param()

        assert response.is_closed is True
        param = response.parse()
        assert param is None

    @parametrize
    def test_streaming_response_timeout_param(self, client: Sink) -> None:
        with client.names.params.with_streaming_response.timeout_param() as response:
            assert not response.is_closed

            param = response.parse()
            assert param is None

        assert cast(Any, response.is_closed) is True


class TestAsyncParams:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_options_param(self, async_client: AsyncSink) -> None:
        param = await async_client.names.params.options_param()
        assert param is None

    @parametrize
    async def test_method_options_param_with_all_params(self, async_client: AsyncSink) -> None:
        param = await async_client.names.params.options_param(
            options="options",
        )
        assert param is None

    @parametrize
    async def test_raw_response_options_param(self, async_client: AsyncSink) -> None:
        response = await async_client.names.params.with_raw_response.options_param()

        assert response.is_closed is True
        param = response.parse()
        assert param is None

    @parametrize
    async def test_streaming_response_options_param(self, async_client: AsyncSink) -> None:
        async with async_client.names.params.with_streaming_response.options_param() as response:
            assert not response.is_closed

            param = await response.parse()
            assert param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_timeout_param(self, async_client: AsyncSink) -> None:
        param = await async_client.names.params.timeout_param()
        assert param is None

    @parametrize
    async def test_method_timeout_param_with_all_params(self, async_client: AsyncSink) -> None:
        param = await async_client.names.params.timeout_param(
            url_timeout=0,
        )
        assert param is None

    @parametrize
    async def test_raw_response_timeout_param(self, async_client: AsyncSink) -> None:
        response = await async_client.names.params.with_raw_response.timeout_param()

        assert response.is_closed is True
        param = response.parse()
        assert param is None

    @parametrize
    async def test_streaming_response_timeout_param(self, async_client: AsyncSink) -> None:
        async with async_client.names.params.with_streaming_response.timeout_param() as response:
            assert not response.is_closed

            param = await response.parse()
            assert param is None

        assert cast(Any, response.is_closed) is True
