# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sink.api.sdk import Sink, AsyncSink

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestReservedNames:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_common_reserved_params(self, client: Sink) -> None:
        reserved_name = client.names.reserved_names.common_reserved_params(
            from_="from",
            api_self=0,
        )
        assert reserved_name is None

    @parametrize
    def test_raw_response_common_reserved_params(self, client: Sink) -> None:
        response = client.names.reserved_names.with_raw_response.common_reserved_params(
            from_="from",
            api_self=0,
        )

        assert response.is_closed is True
        reserved_name = response.parse()
        assert reserved_name is None

    @parametrize
    def test_streaming_response_common_reserved_params(self, client: Sink) -> None:
        with client.names.reserved_names.with_streaming_response.common_reserved_params(
            from_="from",
            api_self=0,
        ) as response:
            assert not response.is_closed

            reserved_name = response.parse()
            assert reserved_name is None

        assert cast(Any, response.is_closed) is True


class TestAsyncReservedNames:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_common_reserved_params(self, async_client: AsyncSink) -> None:
        reserved_name = await async_client.names.reserved_names.common_reserved_params(
            from_="from",
            api_self=0,
        )
        assert reserved_name is None

    @parametrize
    async def test_raw_response_common_reserved_params(self, async_client: AsyncSink) -> None:
        response = await async_client.names.reserved_names.with_raw_response.common_reserved_params(
            from_="from",
            api_self=0,
        )

        assert response.is_closed is True
        reserved_name = response.parse()
        assert reserved_name is None

    @parametrize
    async def test_streaming_response_common_reserved_params(self, async_client: AsyncSink) -> None:
        async with async_client.names.reserved_names.with_streaming_response.common_reserved_params(
            from_="from",
            api_self=0,
        ) as response:
            assert not response.is_closed

            reserved_name = await response.parse()
            assert reserved_name is None

        assert cast(Any, response.is_closed) is True
