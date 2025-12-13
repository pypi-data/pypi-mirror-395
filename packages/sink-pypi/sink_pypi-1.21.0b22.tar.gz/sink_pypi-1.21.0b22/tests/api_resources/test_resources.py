# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sink.api.sdk import Sink, AsyncSink

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestResources:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_foo(self, client: Sink) -> None:
        resource = client.resources.foo()
        assert resource is None

    @parametrize
    def test_raw_response_foo(self, client: Sink) -> None:
        response = client.resources.with_raw_response.foo()

        assert response.is_closed is True
        resource = response.parse()
        assert resource is None

    @parametrize
    def test_streaming_response_foo(self, client: Sink) -> None:
        with client.resources.with_streaming_response.foo() as response:
            assert not response.is_closed

            resource = response.parse()
            assert resource is None

        assert cast(Any, response.is_closed) is True


class TestAsyncResources:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_foo(self, async_client: AsyncSink) -> None:
        resource = await async_client.resources.foo()
        assert resource is None

    @parametrize
    async def test_raw_response_foo(self, async_client: AsyncSink) -> None:
        response = await async_client.resources.with_raw_response.foo()

        assert response.is_closed is True
        resource = response.parse()
        assert resource is None

    @parametrize
    async def test_streaming_response_foo(self, async_client: AsyncSink) -> None:
        async with async_client.resources.with_streaming_response.foo() as response:
            assert not response.is_closed

            resource = await response.parse()
            assert resource is None

        assert cast(Any, response.is_closed) is True
