# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.shared import SimpleObject

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestLanguages:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_skipped_for_node(self, client: Sink) -> None:
        language = client.decorator_tests.languages.skipped_for_node()
        assert_matches_type(SimpleObject, language, path=["response"])

    @parametrize
    def test_raw_response_skipped_for_node(self, client: Sink) -> None:
        response = client.decorator_tests.languages.with_raw_response.skipped_for_node()

        assert response.is_closed is True
        language = response.parse()
        assert_matches_type(SimpleObject, language, path=["response"])

    @parametrize
    def test_streaming_response_skipped_for_node(self, client: Sink) -> None:
        with client.decorator_tests.languages.with_streaming_response.skipped_for_node() as response:
            assert not response.is_closed

            language = response.parse()
            assert_matches_type(SimpleObject, language, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncLanguages:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_skipped_for_node(self, async_client: AsyncSink) -> None:
        language = await async_client.decorator_tests.languages.skipped_for_node()
        assert_matches_type(SimpleObject, language, path=["response"])

    @parametrize
    async def test_raw_response_skipped_for_node(self, async_client: AsyncSink) -> None:
        response = await async_client.decorator_tests.languages.with_raw_response.skipped_for_node()

        assert response.is_closed is True
        language = response.parse()
        assert_matches_type(SimpleObject, language, path=["response"])

    @parametrize
    async def test_streaming_response_skipped_for_node(self, async_client: AsyncSink) -> None:
        async with async_client.decorator_tests.languages.with_streaming_response.skipped_for_node() as response:
            assert not response.is_closed

            language = await response.parse()
            assert_matches_type(SimpleObject, language, path=["response"])

        assert cast(Any, response.is_closed) is True
