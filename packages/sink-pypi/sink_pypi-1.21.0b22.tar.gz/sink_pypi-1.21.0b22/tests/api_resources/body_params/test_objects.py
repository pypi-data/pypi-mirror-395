# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sink.api.sdk import Sink, AsyncSink

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestObjects:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_mixed_known_and_unknown(self, client: Sink) -> None:
        object_ = client.body_params.objects.mixed_known_and_unknown()
        assert object_ is None

    @parametrize
    def test_method_mixed_known_and_unknown_with_all_params(self, client: Sink) -> None:
        object_ = client.body_params.objects.mixed_known_and_unknown(
            mixed_prop={"my_known_prop": 0},
        )
        assert object_ is None

    @parametrize
    def test_raw_response_mixed_known_and_unknown(self, client: Sink) -> None:
        response = client.body_params.objects.with_raw_response.mixed_known_and_unknown()

        assert response.is_closed is True
        object_ = response.parse()
        assert object_ is None

    @parametrize
    def test_streaming_response_mixed_known_and_unknown(self, client: Sink) -> None:
        with client.body_params.objects.with_streaming_response.mixed_known_and_unknown() as response:
            assert not response.is_closed

            object_ = response.parse()
            assert object_ is None

        assert cast(Any, response.is_closed) is True


class TestAsyncObjects:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_mixed_known_and_unknown(self, async_client: AsyncSink) -> None:
        object_ = await async_client.body_params.objects.mixed_known_and_unknown()
        assert object_ is None

    @parametrize
    async def test_method_mixed_known_and_unknown_with_all_params(self, async_client: AsyncSink) -> None:
        object_ = await async_client.body_params.objects.mixed_known_and_unknown(
            mixed_prop={"my_known_prop": 0},
        )
        assert object_ is None

    @parametrize
    async def test_raw_response_mixed_known_and_unknown(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.objects.with_raw_response.mixed_known_and_unknown()

        assert response.is_closed is True
        object_ = response.parse()
        assert object_ is None

    @parametrize
    async def test_streaming_response_mixed_known_and_unknown(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.objects.with_streaming_response.mixed_known_and_unknown() as response:
            assert not response.is_closed

            object_ = await response.parse()
            assert object_ is None

        assert cast(Any, response.is_closed) is True
