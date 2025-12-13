# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.names.reserved_names.public import Private

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPrivate:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_private(self, client: Sink) -> None:
        private = client.names.reserved_names.public.private.private()
        assert_matches_type(Private, private, path=["response"])

    @parametrize
    def test_raw_response_private(self, client: Sink) -> None:
        response = client.names.reserved_names.public.private.with_raw_response.private()

        assert response.is_closed is True
        private = response.parse()
        assert_matches_type(Private, private, path=["response"])

    @parametrize
    def test_streaming_response_private(self, client: Sink) -> None:
        with client.names.reserved_names.public.private.with_streaming_response.private() as response:
            assert not response.is_closed

            private = response.parse()
            assert_matches_type(Private, private, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncPrivate:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_private(self, async_client: AsyncSink) -> None:
        private = await async_client.names.reserved_names.public.private.private()
        assert_matches_type(Private, private, path=["response"])

    @parametrize
    async def test_raw_response_private(self, async_client: AsyncSink) -> None:
        response = await async_client.names.reserved_names.public.private.with_raw_response.private()

        assert response.is_closed is True
        private = response.parse()
        assert_matches_type(Private, private, path=["response"])

    @parametrize
    async def test_streaming_response_private(self, async_client: AsyncSink) -> None:
        async with async_client.names.reserved_names.public.private.with_streaming_response.private() as response:
            assert not response.is_closed

            private = await response.parse()
            assert_matches_type(Private, private, path=["response"])

        assert cast(Any, response.is_closed) is True
