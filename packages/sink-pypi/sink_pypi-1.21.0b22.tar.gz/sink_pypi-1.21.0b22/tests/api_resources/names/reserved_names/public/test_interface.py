# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.names.reserved_names.public import Interface

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestInterface:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_interface(self, client: Sink) -> None:
        interface = client.names.reserved_names.public.interface.interface()
        assert_matches_type(Interface, interface, path=["response"])

    @parametrize
    def test_raw_response_interface(self, client: Sink) -> None:
        response = client.names.reserved_names.public.interface.with_raw_response.interface()

        assert response.is_closed is True
        interface = response.parse()
        assert_matches_type(Interface, interface, path=["response"])

    @parametrize
    def test_streaming_response_interface(self, client: Sink) -> None:
        with client.names.reserved_names.public.interface.with_streaming_response.interface() as response:
            assert not response.is_closed

            interface = response.parse()
            assert_matches_type(Interface, interface, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncInterface:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_interface(self, async_client: AsyncSink) -> None:
        interface = await async_client.names.reserved_names.public.interface.interface()
        assert_matches_type(Interface, interface, path=["response"])

    @parametrize
    async def test_raw_response_interface(self, async_client: AsyncSink) -> None:
        response = await async_client.names.reserved_names.public.interface.with_raw_response.interface()

        assert response.is_closed is True
        interface = response.parse()
        assert_matches_type(Interface, interface, path=["response"])

    @parametrize
    async def test_streaming_response_interface(self, async_client: AsyncSink) -> None:
        async with async_client.names.reserved_names.public.interface.with_streaming_response.interface() as response:
            assert not response.is_closed

            interface = await response.parse()
            assert_matches_type(Interface, interface, path=["response"])

        assert cast(Any, response.is_closed) is True
