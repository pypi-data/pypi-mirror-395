# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.types import PrimitiveStringsResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPrimitives:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_strings(self, client: Sink) -> None:
        primitive = client.types.primitives.strings()
        assert_matches_type(PrimitiveStringsResponse, primitive, path=["response"])

    @parametrize
    def test_method_strings_with_all_params(self, client: Sink) -> None:
        primitive = client.types.primitives.strings(
            string_param="string",
        )
        assert_matches_type(PrimitiveStringsResponse, primitive, path=["response"])

    @parametrize
    def test_raw_response_strings(self, client: Sink) -> None:
        response = client.types.primitives.with_raw_response.strings()

        assert response.is_closed is True
        primitive = response.parse()
        assert_matches_type(PrimitiveStringsResponse, primitive, path=["response"])

    @parametrize
    def test_streaming_response_strings(self, client: Sink) -> None:
        with client.types.primitives.with_streaming_response.strings() as response:
            assert not response.is_closed

            primitive = response.parse()
            assert_matches_type(PrimitiveStringsResponse, primitive, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncPrimitives:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_strings(self, async_client: AsyncSink) -> None:
        primitive = await async_client.types.primitives.strings()
        assert_matches_type(PrimitiveStringsResponse, primitive, path=["response"])

    @parametrize
    async def test_method_strings_with_all_params(self, async_client: AsyncSink) -> None:
        primitive = await async_client.types.primitives.strings(
            string_param="string",
        )
        assert_matches_type(PrimitiveStringsResponse, primitive, path=["response"])

    @parametrize
    async def test_raw_response_strings(self, async_client: AsyncSink) -> None:
        response = await async_client.types.primitives.with_raw_response.strings()

        assert response.is_closed is True
        primitive = response.parse()
        assert_matches_type(PrimitiveStringsResponse, primitive, path=["response"])

    @parametrize
    async def test_streaming_response_strings(self, async_client: AsyncSink) -> None:
        async with async_client.types.primitives.with_streaming_response.strings() as response:
            assert not response.is_closed

            primitive = await response.parse()
            assert_matches_type(PrimitiveStringsResponse, primitive, path=["response"])

        assert cast(Any, response.is_closed) is True
