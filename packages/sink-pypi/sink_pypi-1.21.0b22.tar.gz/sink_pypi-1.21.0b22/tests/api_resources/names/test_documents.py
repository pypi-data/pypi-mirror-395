# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.names import Documents

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDocuments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve2(self, client: Sink) -> None:
        document = client.names.documents.retrieve2()
        assert_matches_type(Documents, document, path=["response"])

    @parametrize
    def test_raw_response_retrieve2(self, client: Sink) -> None:
        response = client.names.documents.with_raw_response.retrieve2()

        assert response.is_closed is True
        document = response.parse()
        assert_matches_type(Documents, document, path=["response"])

    @parametrize
    def test_streaming_response_retrieve2(self, client: Sink) -> None:
        with client.names.documents.with_streaming_response.retrieve2() as response:
            assert not response.is_closed

            document = response.parse()
            assert_matches_type(Documents, document, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDocuments:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve2(self, async_client: AsyncSink) -> None:
        document = await async_client.names.documents.retrieve2()
        assert_matches_type(Documents, document, path=["response"])

    @parametrize
    async def test_raw_response_retrieve2(self, async_client: AsyncSink) -> None:
        response = await async_client.names.documents.with_raw_response.retrieve2()

        assert response.is_closed is True
        document = response.parse()
        assert_matches_type(Documents, document, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve2(self, async_client: AsyncSink) -> None:
        async with async_client.names.documents.with_streaming_response.retrieve2() as response:
            assert not response.is_closed

            document = await response.parse()
            assert_matches_type(Documents, document, path=["response"])

        assert cast(Any, response.is_closed) is True
