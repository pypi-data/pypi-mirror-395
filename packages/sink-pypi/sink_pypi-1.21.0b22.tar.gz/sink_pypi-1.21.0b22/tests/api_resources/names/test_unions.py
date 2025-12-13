# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import ObjectWithUnionProperties
from sink.api.sdk.types.names import DiscriminatedUnion, VariantsSinglePropObjects

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUnions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_discriminated(self, client: Sink) -> None:
        union = client.names.unions.discriminated()
        assert_matches_type(DiscriminatedUnion, union, path=["response"])

    @parametrize
    def test_raw_response_discriminated(self, client: Sink) -> None:
        response = client.names.unions.with_raw_response.discriminated()

        assert response.is_closed is True
        union = response.parse()
        assert_matches_type(DiscriminatedUnion, union, path=["response"])

    @parametrize
    def test_streaming_response_discriminated(self, client: Sink) -> None:
        with client.names.unions.with_streaming_response.discriminated() as response:
            assert not response.is_closed

            union = response.parse()
            assert_matches_type(DiscriminatedUnion, union, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_variants_object_with_union_properties(self, client: Sink) -> None:
        union = client.names.unions.variants_object_with_union_properties()
        assert_matches_type(ObjectWithUnionProperties, union, path=["response"])

    @parametrize
    def test_raw_response_variants_object_with_union_properties(self, client: Sink) -> None:
        response = client.names.unions.with_raw_response.variants_object_with_union_properties()

        assert response.is_closed is True
        union = response.parse()
        assert_matches_type(ObjectWithUnionProperties, union, path=["response"])

    @parametrize
    def test_streaming_response_variants_object_with_union_properties(self, client: Sink) -> None:
        with client.names.unions.with_streaming_response.variants_object_with_union_properties() as response:
            assert not response.is_closed

            union = response.parse()
            assert_matches_type(ObjectWithUnionProperties, union, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_variants_single_prop_objects(self, client: Sink) -> None:
        union = client.names.unions.variants_single_prop_objects()
        assert_matches_type(VariantsSinglePropObjects, union, path=["response"])

    @parametrize
    def test_raw_response_variants_single_prop_objects(self, client: Sink) -> None:
        response = client.names.unions.with_raw_response.variants_single_prop_objects()

        assert response.is_closed is True
        union = response.parse()
        assert_matches_type(VariantsSinglePropObjects, union, path=["response"])

    @parametrize
    def test_streaming_response_variants_single_prop_objects(self, client: Sink) -> None:
        with client.names.unions.with_streaming_response.variants_single_prop_objects() as response:
            assert not response.is_closed

            union = response.parse()
            assert_matches_type(VariantsSinglePropObjects, union, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncUnions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_discriminated(self, async_client: AsyncSink) -> None:
        union = await async_client.names.unions.discriminated()
        assert_matches_type(DiscriminatedUnion, union, path=["response"])

    @parametrize
    async def test_raw_response_discriminated(self, async_client: AsyncSink) -> None:
        response = await async_client.names.unions.with_raw_response.discriminated()

        assert response.is_closed is True
        union = response.parse()
        assert_matches_type(DiscriminatedUnion, union, path=["response"])

    @parametrize
    async def test_streaming_response_discriminated(self, async_client: AsyncSink) -> None:
        async with async_client.names.unions.with_streaming_response.discriminated() as response:
            assert not response.is_closed

            union = await response.parse()
            assert_matches_type(DiscriminatedUnion, union, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_variants_object_with_union_properties(self, async_client: AsyncSink) -> None:
        union = await async_client.names.unions.variants_object_with_union_properties()
        assert_matches_type(ObjectWithUnionProperties, union, path=["response"])

    @parametrize
    async def test_raw_response_variants_object_with_union_properties(self, async_client: AsyncSink) -> None:
        response = await async_client.names.unions.with_raw_response.variants_object_with_union_properties()

        assert response.is_closed is True
        union = response.parse()
        assert_matches_type(ObjectWithUnionProperties, union, path=["response"])

    @parametrize
    async def test_streaming_response_variants_object_with_union_properties(self, async_client: AsyncSink) -> None:
        async with (
            async_client.names.unions.with_streaming_response.variants_object_with_union_properties()
        ) as response:
            assert not response.is_closed

            union = await response.parse()
            assert_matches_type(ObjectWithUnionProperties, union, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_variants_single_prop_objects(self, async_client: AsyncSink) -> None:
        union = await async_client.names.unions.variants_single_prop_objects()
        assert_matches_type(VariantsSinglePropObjects, union, path=["response"])

    @parametrize
    async def test_raw_response_variants_single_prop_objects(self, async_client: AsyncSink) -> None:
        response = await async_client.names.unions.with_raw_response.variants_single_prop_objects()

        assert response.is_closed is True
        union = response.parse()
        assert_matches_type(VariantsSinglePropObjects, union, path=["response"])

    @parametrize
    async def test_streaming_response_variants_single_prop_objects(self, async_client: AsyncSink) -> None:
        async with async_client.names.unions.with_streaming_response.variants_single_prop_objects() as response:
            assert not response.is_closed

            union = await response.parse()
            assert_matches_type(VariantsSinglePropObjects, union, path=["response"])

        assert cast(Any, response.is_closed) is True
