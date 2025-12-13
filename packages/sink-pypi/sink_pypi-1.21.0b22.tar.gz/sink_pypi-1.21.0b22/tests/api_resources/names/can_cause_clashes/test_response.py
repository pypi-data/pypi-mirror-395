# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import httpx
import pytest
from respx import MockRouter

from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
)

# pyright: reportDeprecated=false

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestResponse:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_binary_return(self, client: Sink, respx_mock: MockRouter) -> None:
        respx_mock.get("/binaries/return_binary").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        response = client.names.can_cause_clashes.response.binary_return()
        assert response.is_closed
        assert response.json() == {"foo": "bar"}
        assert cast(Any, response.is_closed) is True
        assert isinstance(response, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_binary_return(self, client: Sink, respx_mock: MockRouter) -> None:
        respx_mock.get("/binaries/return_binary").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        response = client.names.can_cause_clashes.response.with_raw_response.binary_return()

        assert response.is_closed is True
        assert response.json() == {"foo": "bar"}
        assert isinstance(response, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_binary_return(self, client: Sink, respx_mock: MockRouter) -> None:
        respx_mock.get("/binaries/return_binary").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.names.can_cause_clashes.response.with_streaming_response.binary_return() as response:
            assert not response.is_closed

            assert response.json() == {"foo": "bar"}
            assert cast(Any, response.is_closed) is True
            assert isinstance(response, StreamedBinaryAPIResponse)

        assert cast(Any, response.is_closed) is True


class TestAsyncResponse:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_binary_return(self, async_client: AsyncSink, respx_mock: MockRouter) -> None:
        respx_mock.get("/binaries/return_binary").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        response = await async_client.names.can_cause_clashes.response.binary_return()
        assert response.is_closed
        assert await response.json() == {"foo": "bar"}
        assert cast(Any, response.is_closed) is True
        assert isinstance(response, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_binary_return(self, async_client: AsyncSink, respx_mock: MockRouter) -> None:
        respx_mock.get("/binaries/return_binary").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        response = await async_client.names.can_cause_clashes.response.with_raw_response.binary_return()

        assert response.is_closed is True
        assert await response.json() == {"foo": "bar"}
        assert isinstance(response, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_binary_return(self, async_client: AsyncSink, respx_mock: MockRouter) -> None:
        respx_mock.get("/binaries/return_binary").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.names.can_cause_clashes.response.with_streaming_response.binary_return() as response:
            assert not response.is_closed

            assert await response.json() == {"foo": "bar"}
            assert cast(Any, response.is_closed) is True
            assert isinstance(response, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, response.is_closed) is True
