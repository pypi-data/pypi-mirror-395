# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.names.reserved_names import Export

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMethods:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_export(self, client: Sink) -> None:
        method = client.names.reserved_names.methods.export(
            class_="class",
        )
        assert_matches_type(Export, method, path=["response"])

    @parametrize
    def test_method_export_with_all_params(self, client: Sink) -> None:
        method = client.names.reserved_names.methods.export(
            class_="class",
            let="let",
            const="const",
        )
        assert_matches_type(Export, method, path=["response"])

    @parametrize
    def test_raw_response_export(self, client: Sink) -> None:
        response = client.names.reserved_names.methods.with_raw_response.export(
            class_="class",
        )

        assert response.is_closed is True
        method = response.parse()
        assert_matches_type(Export, method, path=["response"])

    @parametrize
    def test_streaming_response_export(self, client: Sink) -> None:
        with client.names.reserved_names.methods.with_streaming_response.export(
            class_="class",
        ) as response:
            assert not response.is_closed

            method = response.parse()
            assert_matches_type(Export, method, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_export(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `class_` but received ''"):
            client.names.reserved_names.methods.with_raw_response.export(
                class_="",
            )


class TestAsyncMethods:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_export(self, async_client: AsyncSink) -> None:
        method = await async_client.names.reserved_names.methods.export(
            class_="class",
        )
        assert_matches_type(Export, method, path=["response"])

    @parametrize
    async def test_method_export_with_all_params(self, async_client: AsyncSink) -> None:
        method = await async_client.names.reserved_names.methods.export(
            class_="class",
            let="let",
            const="const",
        )
        assert_matches_type(Export, method, path=["response"])

    @parametrize
    async def test_raw_response_export(self, async_client: AsyncSink) -> None:
        response = await async_client.names.reserved_names.methods.with_raw_response.export(
            class_="class",
        )

        assert response.is_closed is True
        method = response.parse()
        assert_matches_type(Export, method, path=["response"])

    @parametrize
    async def test_streaming_response_export(self, async_client: AsyncSink) -> None:
        async with async_client.names.reserved_names.methods.with_streaming_response.export(
            class_="class",
        ) as response:
            assert not response.is_closed

            method = await response.parse()
            assert_matches_type(Export, method, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_export(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `class_` but received ''"):
            await async_client.names.reserved_names.methods.with_raw_response.export(
                class_="",
            )
