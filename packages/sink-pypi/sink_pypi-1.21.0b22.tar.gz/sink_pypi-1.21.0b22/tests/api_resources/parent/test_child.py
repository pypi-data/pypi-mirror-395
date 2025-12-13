# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.parent import ChildInlinedResponseResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestChild:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_inlined_response(self, client: Sink) -> None:
        child = client.parent.child.inlined_response()
        assert_matches_type(ChildInlinedResponseResponse, child, path=["response"])

    @parametrize
    def test_raw_response_inlined_response(self, client: Sink) -> None:
        response = client.parent.child.with_raw_response.inlined_response()

        assert response.is_closed is True
        child = response.parse()
        assert_matches_type(ChildInlinedResponseResponse, child, path=["response"])

    @parametrize
    def test_streaming_response_inlined_response(self, client: Sink) -> None:
        with client.parent.child.with_streaming_response.inlined_response() as response:
            assert not response.is_closed

            child = response.parse()
            assert_matches_type(ChildInlinedResponseResponse, child, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncChild:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_inlined_response(self, async_client: AsyncSink) -> None:
        child = await async_client.parent.child.inlined_response()
        assert_matches_type(ChildInlinedResponseResponse, child, path=["response"])

    @parametrize
    async def test_raw_response_inlined_response(self, async_client: AsyncSink) -> None:
        response = await async_client.parent.child.with_raw_response.inlined_response()

        assert response.is_closed is True
        child = response.parse()
        assert_matches_type(ChildInlinedResponseResponse, child, path=["response"])

    @parametrize
    async def test_streaming_response_inlined_response(self, async_client: AsyncSink) -> None:
        async with async_client.parent.child.with_streaming_response.inlined_response() as response:
            assert not response.is_closed

            child = await response.parse()
            assert_matches_type(ChildInlinedResponseResponse, child, path=["response"])

        assert cast(Any, response.is_closed) is True
