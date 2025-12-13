# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import MyModel
from sink.api.sdk.pagination import SyncPageCursor, AsyncPageCursor

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSchemaTypes:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_allofs(self, client: Sink) -> None:
        schema_type = client.pagination_tests.schema_types.allofs()
        assert_matches_type(SyncPageCursor[MyModel], schema_type, path=["response"])

    @parametrize
    def test_method_allofs_with_all_params(self, client: Sink) -> None:
        schema_type = client.pagination_tests.schema_types.allofs(
            cursor="cursor",
            limit=0,
        )
        assert_matches_type(SyncPageCursor[MyModel], schema_type, path=["response"])

    @parametrize
    def test_raw_response_allofs(self, client: Sink) -> None:
        response = client.pagination_tests.schema_types.with_raw_response.allofs()

        assert response.is_closed is True
        schema_type = response.parse()
        assert_matches_type(SyncPageCursor[MyModel], schema_type, path=["response"])

    @parametrize
    def test_streaming_response_allofs(self, client: Sink) -> None:
        with client.pagination_tests.schema_types.with_streaming_response.allofs() as response:
            assert not response.is_closed

            schema_type = response.parse()
            assert_matches_type(SyncPageCursor[MyModel], schema_type, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_unions(self, client: Sink) -> None:
        schema_type = client.pagination_tests.schema_types.unions()
        assert_matches_type(SyncPageCursor[MyModel], schema_type, path=["response"])

    @parametrize
    def test_method_unions_with_all_params(self, client: Sink) -> None:
        schema_type = client.pagination_tests.schema_types.unions(
            cursor="cursor",
            limit=0,
        )
        assert_matches_type(SyncPageCursor[MyModel], schema_type, path=["response"])

    @parametrize
    def test_raw_response_unions(self, client: Sink) -> None:
        response = client.pagination_tests.schema_types.with_raw_response.unions()

        assert response.is_closed is True
        schema_type = response.parse()
        assert_matches_type(SyncPageCursor[MyModel], schema_type, path=["response"])

    @parametrize
    def test_streaming_response_unions(self, client: Sink) -> None:
        with client.pagination_tests.schema_types.with_streaming_response.unions() as response:
            assert not response.is_closed

            schema_type = response.parse()
            assert_matches_type(SyncPageCursor[MyModel], schema_type, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSchemaTypes:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_allofs(self, async_client: AsyncSink) -> None:
        schema_type = await async_client.pagination_tests.schema_types.allofs()
        assert_matches_type(AsyncPageCursor[MyModel], schema_type, path=["response"])

    @parametrize
    async def test_method_allofs_with_all_params(self, async_client: AsyncSink) -> None:
        schema_type = await async_client.pagination_tests.schema_types.allofs(
            cursor="cursor",
            limit=0,
        )
        assert_matches_type(AsyncPageCursor[MyModel], schema_type, path=["response"])

    @parametrize
    async def test_raw_response_allofs(self, async_client: AsyncSink) -> None:
        response = await async_client.pagination_tests.schema_types.with_raw_response.allofs()

        assert response.is_closed is True
        schema_type = response.parse()
        assert_matches_type(AsyncPageCursor[MyModel], schema_type, path=["response"])

    @parametrize
    async def test_streaming_response_allofs(self, async_client: AsyncSink) -> None:
        async with async_client.pagination_tests.schema_types.with_streaming_response.allofs() as response:
            assert not response.is_closed

            schema_type = await response.parse()
            assert_matches_type(AsyncPageCursor[MyModel], schema_type, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_unions(self, async_client: AsyncSink) -> None:
        schema_type = await async_client.pagination_tests.schema_types.unions()
        assert_matches_type(AsyncPageCursor[MyModel], schema_type, path=["response"])

    @parametrize
    async def test_method_unions_with_all_params(self, async_client: AsyncSink) -> None:
        schema_type = await async_client.pagination_tests.schema_types.unions(
            cursor="cursor",
            limit=0,
        )
        assert_matches_type(AsyncPageCursor[MyModel], schema_type, path=["response"])

    @parametrize
    async def test_raw_response_unions(self, async_client: AsyncSink) -> None:
        response = await async_client.pagination_tests.schema_types.with_raw_response.unions()

        assert response.is_closed is True
        schema_type = response.parse()
        assert_matches_type(AsyncPageCursor[MyModel], schema_type, path=["response"])

    @parametrize
    async def test_streaming_response_unions(self, async_client: AsyncSink) -> None:
        async with async_client.pagination_tests.schema_types.with_streaming_response.unions() as response:
            assert not response.is_closed

            schema_type = await response.parse()
            assert_matches_type(AsyncPageCursor[MyModel], schema_type, path=["response"])

        assert cast(Any, response.is_closed) is True
