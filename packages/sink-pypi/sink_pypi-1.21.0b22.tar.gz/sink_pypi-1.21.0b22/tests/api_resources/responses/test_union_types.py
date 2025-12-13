# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Optional, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.responses import (
    UnionTypeNumbersResponse,
    UnionTypeObjectsResponse,
    UnionTypeMixedTypesResponse,
    UnionTypeNullableUnionResponse,
    UnionTypeUnknownVariantResponse,
    UnionTypeSuperMixedTypesResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUnionTypes:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_mixed_types(self, client: Sink) -> None:
        union_type = client.responses.union_types.mixed_types()
        assert_matches_type(UnionTypeMixedTypesResponse, union_type, path=["response"])

    @parametrize
    def test_raw_response_mixed_types(self, client: Sink) -> None:
        response = client.responses.union_types.with_raw_response.mixed_types()

        assert response.is_closed is True
        union_type = response.parse()
        assert_matches_type(UnionTypeMixedTypesResponse, union_type, path=["response"])

    @parametrize
    def test_streaming_response_mixed_types(self, client: Sink) -> None:
        with client.responses.union_types.with_streaming_response.mixed_types() as response:
            assert not response.is_closed

            union_type = response.parse()
            assert_matches_type(UnionTypeMixedTypesResponse, union_type, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_nullable_union(self, client: Sink) -> None:
        union_type = client.responses.union_types.nullable_union()
        assert_matches_type(Optional[UnionTypeNullableUnionResponse], union_type, path=["response"])

    @parametrize
    def test_raw_response_nullable_union(self, client: Sink) -> None:
        response = client.responses.union_types.with_raw_response.nullable_union()

        assert response.is_closed is True
        union_type = response.parse()
        assert_matches_type(Optional[UnionTypeNullableUnionResponse], union_type, path=["response"])

    @parametrize
    def test_streaming_response_nullable_union(self, client: Sink) -> None:
        with client.responses.union_types.with_streaming_response.nullable_union() as response:
            assert not response.is_closed

            union_type = response.parse()
            assert_matches_type(Optional[UnionTypeNullableUnionResponse], union_type, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_numbers(self, client: Sink) -> None:
        union_type = client.responses.union_types.numbers()
        assert_matches_type(UnionTypeNumbersResponse, union_type, path=["response"])

    @parametrize
    def test_raw_response_numbers(self, client: Sink) -> None:
        response = client.responses.union_types.with_raw_response.numbers()

        assert response.is_closed is True
        union_type = response.parse()
        assert_matches_type(UnionTypeNumbersResponse, union_type, path=["response"])

    @parametrize
    def test_streaming_response_numbers(self, client: Sink) -> None:
        with client.responses.union_types.with_streaming_response.numbers() as response:
            assert not response.is_closed

            union_type = response.parse()
            assert_matches_type(UnionTypeNumbersResponse, union_type, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_objects(self, client: Sink) -> None:
        union_type = client.responses.union_types.objects()
        assert_matches_type(UnionTypeObjectsResponse, union_type, path=["response"])

    @parametrize
    def test_raw_response_objects(self, client: Sink) -> None:
        response = client.responses.union_types.with_raw_response.objects()

        assert response.is_closed is True
        union_type = response.parse()
        assert_matches_type(UnionTypeObjectsResponse, union_type, path=["response"])

    @parametrize
    def test_streaming_response_objects(self, client: Sink) -> None:
        with client.responses.union_types.with_streaming_response.objects() as response:
            assert not response.is_closed

            union_type = response.parse()
            assert_matches_type(UnionTypeObjectsResponse, union_type, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_super_mixed_types(self, client: Sink) -> None:
        union_type = client.responses.union_types.super_mixed_types()
        assert_matches_type(UnionTypeSuperMixedTypesResponse, union_type, path=["response"])

    @parametrize
    def test_raw_response_super_mixed_types(self, client: Sink) -> None:
        response = client.responses.union_types.with_raw_response.super_mixed_types()

        assert response.is_closed is True
        union_type = response.parse()
        assert_matches_type(UnionTypeSuperMixedTypesResponse, union_type, path=["response"])

    @parametrize
    def test_streaming_response_super_mixed_types(self, client: Sink) -> None:
        with client.responses.union_types.with_streaming_response.super_mixed_types() as response:
            assert not response.is_closed

            union_type = response.parse()
            assert_matches_type(UnionTypeSuperMixedTypesResponse, union_type, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_unknown_variant(self, client: Sink) -> None:
        union_type = client.responses.union_types.unknown_variant()
        assert_matches_type(UnionTypeUnknownVariantResponse, union_type, path=["response"])

    @parametrize
    def test_raw_response_unknown_variant(self, client: Sink) -> None:
        response = client.responses.union_types.with_raw_response.unknown_variant()

        assert response.is_closed is True
        union_type = response.parse()
        assert_matches_type(UnionTypeUnknownVariantResponse, union_type, path=["response"])

    @parametrize
    def test_streaming_response_unknown_variant(self, client: Sink) -> None:
        with client.responses.union_types.with_streaming_response.unknown_variant() as response:
            assert not response.is_closed

            union_type = response.parse()
            assert_matches_type(UnionTypeUnknownVariantResponse, union_type, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncUnionTypes:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_mixed_types(self, async_client: AsyncSink) -> None:
        union_type = await async_client.responses.union_types.mixed_types()
        assert_matches_type(UnionTypeMixedTypesResponse, union_type, path=["response"])

    @parametrize
    async def test_raw_response_mixed_types(self, async_client: AsyncSink) -> None:
        response = await async_client.responses.union_types.with_raw_response.mixed_types()

        assert response.is_closed is True
        union_type = response.parse()
        assert_matches_type(UnionTypeMixedTypesResponse, union_type, path=["response"])

    @parametrize
    async def test_streaming_response_mixed_types(self, async_client: AsyncSink) -> None:
        async with async_client.responses.union_types.with_streaming_response.mixed_types() as response:
            assert not response.is_closed

            union_type = await response.parse()
            assert_matches_type(UnionTypeMixedTypesResponse, union_type, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_nullable_union(self, async_client: AsyncSink) -> None:
        union_type = await async_client.responses.union_types.nullable_union()
        assert_matches_type(Optional[UnionTypeNullableUnionResponse], union_type, path=["response"])

    @parametrize
    async def test_raw_response_nullable_union(self, async_client: AsyncSink) -> None:
        response = await async_client.responses.union_types.with_raw_response.nullable_union()

        assert response.is_closed is True
        union_type = response.parse()
        assert_matches_type(Optional[UnionTypeNullableUnionResponse], union_type, path=["response"])

    @parametrize
    async def test_streaming_response_nullable_union(self, async_client: AsyncSink) -> None:
        async with async_client.responses.union_types.with_streaming_response.nullable_union() as response:
            assert not response.is_closed

            union_type = await response.parse()
            assert_matches_type(Optional[UnionTypeNullableUnionResponse], union_type, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_numbers(self, async_client: AsyncSink) -> None:
        union_type = await async_client.responses.union_types.numbers()
        assert_matches_type(UnionTypeNumbersResponse, union_type, path=["response"])

    @parametrize
    async def test_raw_response_numbers(self, async_client: AsyncSink) -> None:
        response = await async_client.responses.union_types.with_raw_response.numbers()

        assert response.is_closed is True
        union_type = response.parse()
        assert_matches_type(UnionTypeNumbersResponse, union_type, path=["response"])

    @parametrize
    async def test_streaming_response_numbers(self, async_client: AsyncSink) -> None:
        async with async_client.responses.union_types.with_streaming_response.numbers() as response:
            assert not response.is_closed

            union_type = await response.parse()
            assert_matches_type(UnionTypeNumbersResponse, union_type, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_objects(self, async_client: AsyncSink) -> None:
        union_type = await async_client.responses.union_types.objects()
        assert_matches_type(UnionTypeObjectsResponse, union_type, path=["response"])

    @parametrize
    async def test_raw_response_objects(self, async_client: AsyncSink) -> None:
        response = await async_client.responses.union_types.with_raw_response.objects()

        assert response.is_closed is True
        union_type = response.parse()
        assert_matches_type(UnionTypeObjectsResponse, union_type, path=["response"])

    @parametrize
    async def test_streaming_response_objects(self, async_client: AsyncSink) -> None:
        async with async_client.responses.union_types.with_streaming_response.objects() as response:
            assert not response.is_closed

            union_type = await response.parse()
            assert_matches_type(UnionTypeObjectsResponse, union_type, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_super_mixed_types(self, async_client: AsyncSink) -> None:
        union_type = await async_client.responses.union_types.super_mixed_types()
        assert_matches_type(UnionTypeSuperMixedTypesResponse, union_type, path=["response"])

    @parametrize
    async def test_raw_response_super_mixed_types(self, async_client: AsyncSink) -> None:
        response = await async_client.responses.union_types.with_raw_response.super_mixed_types()

        assert response.is_closed is True
        union_type = response.parse()
        assert_matches_type(UnionTypeSuperMixedTypesResponse, union_type, path=["response"])

    @parametrize
    async def test_streaming_response_super_mixed_types(self, async_client: AsyncSink) -> None:
        async with async_client.responses.union_types.with_streaming_response.super_mixed_types() as response:
            assert not response.is_closed

            union_type = await response.parse()
            assert_matches_type(UnionTypeSuperMixedTypesResponse, union_type, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_unknown_variant(self, async_client: AsyncSink) -> None:
        union_type = await async_client.responses.union_types.unknown_variant()
        assert_matches_type(UnionTypeUnknownVariantResponse, union_type, path=["response"])

    @parametrize
    async def test_raw_response_unknown_variant(self, async_client: AsyncSink) -> None:
        response = await async_client.responses.union_types.with_raw_response.unknown_variant()

        assert response.is_closed is True
        union_type = response.parse()
        assert_matches_type(UnionTypeUnknownVariantResponse, union_type, path=["response"])

    @parametrize
    async def test_streaming_response_unknown_variant(self, async_client: AsyncSink) -> None:
        async with async_client.responses.union_types.with_streaming_response.unknown_variant() as response:
            assert not response.is_closed

            union_type = await response.parse()
            assert_matches_type(UnionTypeUnknownVariantResponse, union_type, path=["response"])

        assert cast(Any, response.is_closed) is True
