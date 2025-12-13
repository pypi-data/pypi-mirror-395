# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import (
    ComplexQueryArrayQueryResponse,
    ComplexQueryUnionQueryResponse,
    ComplexQueryObjectQueryResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestComplexQueries:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_array_query(self, client: Sink) -> None:
        complex_query = client.complex_queries.array_query()
        assert_matches_type(ComplexQueryArrayQueryResponse, complex_query, path=["response"])

    @parametrize
    def test_method_array_query_with_all_params(self, client: Sink) -> None:
        complex_query = client.complex_queries.array_query(
            include=["users"],
        )
        assert_matches_type(ComplexQueryArrayQueryResponse, complex_query, path=["response"])

    @parametrize
    def test_raw_response_array_query(self, client: Sink) -> None:
        response = client.complex_queries.with_raw_response.array_query()

        assert response.is_closed is True
        complex_query = response.parse()
        assert_matches_type(ComplexQueryArrayQueryResponse, complex_query, path=["response"])

    @parametrize
    def test_streaming_response_array_query(self, client: Sink) -> None:
        with client.complex_queries.with_streaming_response.array_query() as response:
            assert not response.is_closed

            complex_query = response.parse()
            assert_matches_type(ComplexQueryArrayQueryResponse, complex_query, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_object_query(self, client: Sink) -> None:
        complex_query = client.complex_queries.object_query()
        assert_matches_type(ComplexQueryObjectQueryResponse, complex_query, path=["response"])

    @parametrize
    def test_method_object_query_with_all_params(self, client: Sink) -> None:
        complex_query = client.complex_queries.object_query(
            include={"foo": "string"},
        )
        assert_matches_type(ComplexQueryObjectQueryResponse, complex_query, path=["response"])

    @parametrize
    def test_raw_response_object_query(self, client: Sink) -> None:
        response = client.complex_queries.with_raw_response.object_query()

        assert response.is_closed is True
        complex_query = response.parse()
        assert_matches_type(ComplexQueryObjectQueryResponse, complex_query, path=["response"])

    @parametrize
    def test_streaming_response_object_query(self, client: Sink) -> None:
        with client.complex_queries.with_streaming_response.object_query() as response:
            assert not response.is_closed

            complex_query = response.parse()
            assert_matches_type(ComplexQueryObjectQueryResponse, complex_query, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_union_query(self, client: Sink) -> None:
        complex_query = client.complex_queries.union_query()
        assert_matches_type(ComplexQueryUnionQueryResponse, complex_query, path=["response"])

    @parametrize
    def test_method_union_query_with_all_params(self, client: Sink) -> None:
        complex_query = client.complex_queries.union_query(
            include="string",
        )
        assert_matches_type(ComplexQueryUnionQueryResponse, complex_query, path=["response"])

    @parametrize
    def test_raw_response_union_query(self, client: Sink) -> None:
        response = client.complex_queries.with_raw_response.union_query()

        assert response.is_closed is True
        complex_query = response.parse()
        assert_matches_type(ComplexQueryUnionQueryResponse, complex_query, path=["response"])

    @parametrize
    def test_streaming_response_union_query(self, client: Sink) -> None:
        with client.complex_queries.with_streaming_response.union_query() as response:
            assert not response.is_closed

            complex_query = response.parse()
            assert_matches_type(ComplexQueryUnionQueryResponse, complex_query, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncComplexQueries:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_array_query(self, async_client: AsyncSink) -> None:
        complex_query = await async_client.complex_queries.array_query()
        assert_matches_type(ComplexQueryArrayQueryResponse, complex_query, path=["response"])

    @parametrize
    async def test_method_array_query_with_all_params(self, async_client: AsyncSink) -> None:
        complex_query = await async_client.complex_queries.array_query(
            include=["users"],
        )
        assert_matches_type(ComplexQueryArrayQueryResponse, complex_query, path=["response"])

    @parametrize
    async def test_raw_response_array_query(self, async_client: AsyncSink) -> None:
        response = await async_client.complex_queries.with_raw_response.array_query()

        assert response.is_closed is True
        complex_query = response.parse()
        assert_matches_type(ComplexQueryArrayQueryResponse, complex_query, path=["response"])

    @parametrize
    async def test_streaming_response_array_query(self, async_client: AsyncSink) -> None:
        async with async_client.complex_queries.with_streaming_response.array_query() as response:
            assert not response.is_closed

            complex_query = await response.parse()
            assert_matches_type(ComplexQueryArrayQueryResponse, complex_query, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_object_query(self, async_client: AsyncSink) -> None:
        complex_query = await async_client.complex_queries.object_query()
        assert_matches_type(ComplexQueryObjectQueryResponse, complex_query, path=["response"])

    @parametrize
    async def test_method_object_query_with_all_params(self, async_client: AsyncSink) -> None:
        complex_query = await async_client.complex_queries.object_query(
            include={"foo": "string"},
        )
        assert_matches_type(ComplexQueryObjectQueryResponse, complex_query, path=["response"])

    @parametrize
    async def test_raw_response_object_query(self, async_client: AsyncSink) -> None:
        response = await async_client.complex_queries.with_raw_response.object_query()

        assert response.is_closed is True
        complex_query = response.parse()
        assert_matches_type(ComplexQueryObjectQueryResponse, complex_query, path=["response"])

    @parametrize
    async def test_streaming_response_object_query(self, async_client: AsyncSink) -> None:
        async with async_client.complex_queries.with_streaming_response.object_query() as response:
            assert not response.is_closed

            complex_query = await response.parse()
            assert_matches_type(ComplexQueryObjectQueryResponse, complex_query, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_union_query(self, async_client: AsyncSink) -> None:
        complex_query = await async_client.complex_queries.union_query()
        assert_matches_type(ComplexQueryUnionQueryResponse, complex_query, path=["response"])

    @parametrize
    async def test_method_union_query_with_all_params(self, async_client: AsyncSink) -> None:
        complex_query = await async_client.complex_queries.union_query(
            include="string",
        )
        assert_matches_type(ComplexQueryUnionQueryResponse, complex_query, path=["response"])

    @parametrize
    async def test_raw_response_union_query(self, async_client: AsyncSink) -> None:
        response = await async_client.complex_queries.with_raw_response.union_query()

        assert response.is_closed is True
        complex_query = response.parse()
        assert_matches_type(ComplexQueryUnionQueryResponse, complex_query, path=["response"])

    @parametrize
    async def test_streaming_response_union_query(self, async_client: AsyncSink) -> None:
        async with async_client.complex_queries.with_streaming_response.union_query() as response:
            assert not response.is_closed

            complex_query = await response.parse()
            assert_matches_type(ComplexQueryUnionQueryResponse, complex_query, path=["response"])

        assert cast(Any, response.is_closed) is True
