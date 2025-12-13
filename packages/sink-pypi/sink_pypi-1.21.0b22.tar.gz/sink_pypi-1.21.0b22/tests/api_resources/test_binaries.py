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


class TestBinaries:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_return_binary(self, client: Sink, respx_mock: MockRouter) -> None:
        respx_mock.get("/binaries/return_binary").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        binary = client.binaries.return_binary()
        assert binary.is_closed
        assert binary.json() == {"foo": "bar"}
        assert cast(Any, binary.is_closed) is True
        assert isinstance(binary, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_return_binary(self, client: Sink, respx_mock: MockRouter) -> None:
        respx_mock.get("/binaries/return_binary").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        binary = client.binaries.with_raw_response.return_binary()

        assert binary.is_closed is True
        assert binary.json() == {"foo": "bar"}
        assert isinstance(binary, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_return_binary(self, client: Sink, respx_mock: MockRouter) -> None:
        respx_mock.get("/binaries/return_binary").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.binaries.with_streaming_response.return_binary() as binary:
            assert not binary.is_closed

            assert binary.json() == {"foo": "bar"}
            assert cast(Any, binary.is_closed) is True
            assert isinstance(binary, StreamedBinaryAPIResponse)

        assert cast(Any, binary.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_with_path_and_body_param(self, client: Sink, respx_mock: MockRouter) -> None:
        respx_mock.post("/binaries/with_path_and_body_param/id").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        binary = client.binaries.with_path_and_body_param(
            id="id",
        )
        assert binary.is_closed
        assert binary.json() == {"foo": "bar"}
        assert cast(Any, binary.is_closed) is True
        assert isinstance(binary, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_with_path_and_body_param_with_all_params(self, client: Sink, respx_mock: MockRouter) -> None:
        respx_mock.post("/binaries/with_path_and_body_param/id").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        binary = client.binaries.with_path_and_body_param(
            id="id",
            foo="foo",
        )
        assert binary.is_closed
        assert binary.json() == {"foo": "bar"}
        assert cast(Any, binary.is_closed) is True
        assert isinstance(binary, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_with_path_and_body_param(self, client: Sink, respx_mock: MockRouter) -> None:
        respx_mock.post("/binaries/with_path_and_body_param/id").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        binary = client.binaries.with_raw_response.with_path_and_body_param(
            id="id",
        )

        assert binary.is_closed is True
        assert binary.json() == {"foo": "bar"}
        assert isinstance(binary, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_with_path_and_body_param(self, client: Sink, respx_mock: MockRouter) -> None:
        respx_mock.post("/binaries/with_path_and_body_param/id").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.binaries.with_streaming_response.with_path_and_body_param(
            id="id",
        ) as binary:
            assert not binary.is_closed

            assert binary.json() == {"foo": "bar"}
            assert cast(Any, binary.is_closed) is True
            assert isinstance(binary, StreamedBinaryAPIResponse)

        assert cast(Any, binary.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_with_path_and_body_param(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.binaries.with_raw_response.with_path_and_body_param(
                id="",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_with_path_param(self, client: Sink, respx_mock: MockRouter) -> None:
        respx_mock.get("/binaries/with_path_param/id").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        binary = client.binaries.with_path_param(
            "id",
        )
        assert binary.is_closed
        assert binary.json() == {"foo": "bar"}
        assert cast(Any, binary.is_closed) is True
        assert isinstance(binary, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_with_path_param(self, client: Sink, respx_mock: MockRouter) -> None:
        respx_mock.get("/binaries/with_path_param/id").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        binary = client.binaries.with_raw_response.with_path_param(
            "id",
        )

        assert binary.is_closed is True
        assert binary.json() == {"foo": "bar"}
        assert isinstance(binary, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_with_path_param(self, client: Sink, respx_mock: MockRouter) -> None:
        respx_mock.get("/binaries/with_path_param/id").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.binaries.with_streaming_response.with_path_param(
            "id",
        ) as binary:
            assert not binary.is_closed

            assert binary.json() == {"foo": "bar"}
            assert cast(Any, binary.is_closed) is True
            assert isinstance(binary, StreamedBinaryAPIResponse)

        assert cast(Any, binary.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_with_path_param(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.binaries.with_raw_response.with_path_param(
                "",
            )


class TestAsyncBinaries:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_return_binary(self, async_client: AsyncSink, respx_mock: MockRouter) -> None:
        respx_mock.get("/binaries/return_binary").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        binary = await async_client.binaries.return_binary()
        assert binary.is_closed
        assert await binary.json() == {"foo": "bar"}
        assert cast(Any, binary.is_closed) is True
        assert isinstance(binary, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_return_binary(self, async_client: AsyncSink, respx_mock: MockRouter) -> None:
        respx_mock.get("/binaries/return_binary").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        binary = await async_client.binaries.with_raw_response.return_binary()

        assert binary.is_closed is True
        assert await binary.json() == {"foo": "bar"}
        assert isinstance(binary, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_return_binary(self, async_client: AsyncSink, respx_mock: MockRouter) -> None:
        respx_mock.get("/binaries/return_binary").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.binaries.with_streaming_response.return_binary() as binary:
            assert not binary.is_closed

            assert await binary.json() == {"foo": "bar"}
            assert cast(Any, binary.is_closed) is True
            assert isinstance(binary, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, binary.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_with_path_and_body_param(self, async_client: AsyncSink, respx_mock: MockRouter) -> None:
        respx_mock.post("/binaries/with_path_and_body_param/id").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        binary = await async_client.binaries.with_path_and_body_param(
            id="id",
        )
        assert binary.is_closed
        assert await binary.json() == {"foo": "bar"}
        assert cast(Any, binary.is_closed) is True
        assert isinstance(binary, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_with_path_and_body_param_with_all_params(
        self, async_client: AsyncSink, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/binaries/with_path_and_body_param/id").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        binary = await async_client.binaries.with_path_and_body_param(
            id="id",
            foo="foo",
        )
        assert binary.is_closed
        assert await binary.json() == {"foo": "bar"}
        assert cast(Any, binary.is_closed) is True
        assert isinstance(binary, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_with_path_and_body_param(self, async_client: AsyncSink, respx_mock: MockRouter) -> None:
        respx_mock.post("/binaries/with_path_and_body_param/id").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        binary = await async_client.binaries.with_raw_response.with_path_and_body_param(
            id="id",
        )

        assert binary.is_closed is True
        assert await binary.json() == {"foo": "bar"}
        assert isinstance(binary, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_with_path_and_body_param(
        self, async_client: AsyncSink, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/binaries/with_path_and_body_param/id").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.binaries.with_streaming_response.with_path_and_body_param(
            id="id",
        ) as binary:
            assert not binary.is_closed

            assert await binary.json() == {"foo": "bar"}
            assert cast(Any, binary.is_closed) is True
            assert isinstance(binary, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, binary.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_with_path_and_body_param(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.binaries.with_raw_response.with_path_and_body_param(
                id="",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_with_path_param(self, async_client: AsyncSink, respx_mock: MockRouter) -> None:
        respx_mock.get("/binaries/with_path_param/id").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        binary = await async_client.binaries.with_path_param(
            "id",
        )
        assert binary.is_closed
        assert await binary.json() == {"foo": "bar"}
        assert cast(Any, binary.is_closed) is True
        assert isinstance(binary, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_with_path_param(self, async_client: AsyncSink, respx_mock: MockRouter) -> None:
        respx_mock.get("/binaries/with_path_param/id").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        binary = await async_client.binaries.with_raw_response.with_path_param(
            "id",
        )

        assert binary.is_closed is True
        assert await binary.json() == {"foo": "bar"}
        assert isinstance(binary, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_with_path_param(self, async_client: AsyncSink, respx_mock: MockRouter) -> None:
        respx_mock.get("/binaries/with_path_param/id").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.binaries.with_streaming_response.with_path_param(
            "id",
        ) as binary:
            assert not binary.is_closed

            assert await binary.json() == {"foo": "bar"}
            assert cast(Any, binary.is_closed) is True
            assert isinstance(binary, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, binary.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_with_path_param(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.binaries.with_raw_response.with_path_param(
                "",
            )
