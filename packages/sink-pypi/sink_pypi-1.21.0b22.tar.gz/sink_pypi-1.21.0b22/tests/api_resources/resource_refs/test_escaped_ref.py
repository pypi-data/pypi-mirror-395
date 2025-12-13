# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.resource_refs import ModelWithEscapedName

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEscapedRef:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_get(self, client: Sink) -> None:
        escaped_ref = client.resource_refs.escaped_ref.get()
        assert_matches_type(ModelWithEscapedName, escaped_ref, path=["response"])

    @parametrize
    def test_raw_response_get(self, client: Sink) -> None:
        response = client.resource_refs.escaped_ref.with_raw_response.get()

        assert response.is_closed is True
        escaped_ref = response.parse()
        assert_matches_type(ModelWithEscapedName, escaped_ref, path=["response"])

    @parametrize
    def test_streaming_response_get(self, client: Sink) -> None:
        with client.resource_refs.escaped_ref.with_streaming_response.get() as response:
            assert not response.is_closed

            escaped_ref = response.parse()
            assert_matches_type(ModelWithEscapedName, escaped_ref, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncEscapedRef:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_get(self, async_client: AsyncSink) -> None:
        escaped_ref = await async_client.resource_refs.escaped_ref.get()
        assert_matches_type(ModelWithEscapedName, escaped_ref, path=["response"])

    @parametrize
    async def test_raw_response_get(self, async_client: AsyncSink) -> None:
        response = await async_client.resource_refs.escaped_ref.with_raw_response.get()

        assert response.is_closed is True
        escaped_ref = response.parse()
        assert_matches_type(ModelWithEscapedName, escaped_ref, path=["response"])

    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncSink) -> None:
        async with async_client.resource_refs.escaped_ref.with_streaming_response.get() as response:
            assert not response.is_closed

            escaped_ref = await response.parse()
            assert_matches_type(ModelWithEscapedName, escaped_ref, path=["response"])

        assert cast(Any, response.is_closed) is True
