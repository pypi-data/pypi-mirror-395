# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.names.reserved_names import Import

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestImport:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_import(self, client: Sink) -> None:
        import_ = client.names.reserved_names.import_.import_()
        assert_matches_type(Import, import_, path=["response"])

    @parametrize
    def test_raw_response_import(self, client: Sink) -> None:
        response = client.names.reserved_names.import_.with_raw_response.import_()

        assert response.is_closed is True
        import_ = response.parse()
        assert_matches_type(Import, import_, path=["response"])

    @parametrize
    def test_streaming_response_import(self, client: Sink) -> None:
        with client.names.reserved_names.import_.with_streaming_response.import_() as response:
            assert not response.is_closed

            import_ = response.parse()
            assert_matches_type(Import, import_, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncImport:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_import(self, async_client: AsyncSink) -> None:
        import_ = await async_client.names.reserved_names.import_.import_()
        assert_matches_type(Import, import_, path=["response"])

    @parametrize
    async def test_raw_response_import(self, async_client: AsyncSink) -> None:
        response = await async_client.names.reserved_names.import_.with_raw_response.import_()

        assert response.is_closed is True
        import_ = response.parse()
        assert_matches_type(Import, import_, path=["response"])

    @parametrize
    async def test_streaming_response_import(self, async_client: AsyncSink) -> None:
        async with async_client.names.reserved_names.import_.with_streaming_response.import_() as response:
            assert not response.is_closed

            import_ = await response.parse()
            assert_matches_type(Import, import_, path=["response"])

        assert cast(Any, response.is_closed) is True
