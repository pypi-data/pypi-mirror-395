# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.decorator_tests import KeepThisResourceKeepThisMethodResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestKeepThisResource:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_keep_this_method(self, client: Sink) -> None:
        keep_this_resource = client.decorator_tests.keep_this_resource.keep_this_method()
        assert_matches_type(KeepThisResourceKeepThisMethodResponse, keep_this_resource, path=["response"])

    @parametrize
    def test_raw_response_keep_this_method(self, client: Sink) -> None:
        response = client.decorator_tests.keep_this_resource.with_raw_response.keep_this_method()

        assert response.is_closed is True
        keep_this_resource = response.parse()
        assert_matches_type(KeepThisResourceKeepThisMethodResponse, keep_this_resource, path=["response"])

    @parametrize
    def test_streaming_response_keep_this_method(self, client: Sink) -> None:
        with client.decorator_tests.keep_this_resource.with_streaming_response.keep_this_method() as response:
            assert not response.is_closed

            keep_this_resource = response.parse()
            assert_matches_type(KeepThisResourceKeepThisMethodResponse, keep_this_resource, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncKeepThisResource:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_keep_this_method(self, async_client: AsyncSink) -> None:
        keep_this_resource = await async_client.decorator_tests.keep_this_resource.keep_this_method()
        assert_matches_type(KeepThisResourceKeepThisMethodResponse, keep_this_resource, path=["response"])

    @parametrize
    async def test_raw_response_keep_this_method(self, async_client: AsyncSink) -> None:
        response = await async_client.decorator_tests.keep_this_resource.with_raw_response.keep_this_method()

        assert response.is_closed is True
        keep_this_resource = response.parse()
        assert_matches_type(KeepThisResourceKeepThisMethodResponse, keep_this_resource, path=["response"])

    @parametrize
    async def test_streaming_response_keep_this_method(self, async_client: AsyncSink) -> None:
        async with (
            async_client.decorator_tests.keep_this_resource.with_streaming_response.keep_this_method()
        ) as response:
            assert not response.is_closed

            keep_this_resource = await response.parse()
            assert_matches_type(KeepThisResourceKeepThisMethodResponse, keep_this_resource, path=["response"])

        assert cast(Any, response.is_closed) is True
