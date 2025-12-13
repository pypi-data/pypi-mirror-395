# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.types import (
    ObjectMixedKnownAndUnknownResponse,
    ObjectMultiplePropertiesSameRefResponse,
    ObjectMultiplePropertiesSameModelResponse,
    ObjectMultipleArrayPropertiesSameRefResponse,
    ObjectTwoDimensionalArrayPrimitivePropertyResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestObjects:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_mixed_known_and_unknown(self, client: Sink) -> None:
        object_ = client.types.objects.mixed_known_and_unknown()
        assert_matches_type(ObjectMixedKnownAndUnknownResponse, object_, path=["response"])

    @parametrize
    def test_raw_response_mixed_known_and_unknown(self, client: Sink) -> None:
        response = client.types.objects.with_raw_response.mixed_known_and_unknown()

        assert response.is_closed is True
        object_ = response.parse()
        assert_matches_type(ObjectMixedKnownAndUnknownResponse, object_, path=["response"])

    @parametrize
    def test_streaming_response_mixed_known_and_unknown(self, client: Sink) -> None:
        with client.types.objects.with_streaming_response.mixed_known_and_unknown() as response:
            assert not response.is_closed

            object_ = response.parse()
            assert_matches_type(ObjectMixedKnownAndUnknownResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_multiple_array_properties_same_ref(self, client: Sink) -> None:
        object_ = client.types.objects.multiple_array_properties_same_ref()
        assert_matches_type(ObjectMultipleArrayPropertiesSameRefResponse, object_, path=["response"])

    @parametrize
    def test_raw_response_multiple_array_properties_same_ref(self, client: Sink) -> None:
        response = client.types.objects.with_raw_response.multiple_array_properties_same_ref()

        assert response.is_closed is True
        object_ = response.parse()
        assert_matches_type(ObjectMultipleArrayPropertiesSameRefResponse, object_, path=["response"])

    @parametrize
    def test_streaming_response_multiple_array_properties_same_ref(self, client: Sink) -> None:
        with client.types.objects.with_streaming_response.multiple_array_properties_same_ref() as response:
            assert not response.is_closed

            object_ = response.parse()
            assert_matches_type(ObjectMultipleArrayPropertiesSameRefResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_multiple_properties_same_model(self, client: Sink) -> None:
        object_ = client.types.objects.multiple_properties_same_model()
        assert_matches_type(ObjectMultiplePropertiesSameModelResponse, object_, path=["response"])

    @parametrize
    def test_raw_response_multiple_properties_same_model(self, client: Sink) -> None:
        response = client.types.objects.with_raw_response.multiple_properties_same_model()

        assert response.is_closed is True
        object_ = response.parse()
        assert_matches_type(ObjectMultiplePropertiesSameModelResponse, object_, path=["response"])

    @parametrize
    def test_streaming_response_multiple_properties_same_model(self, client: Sink) -> None:
        with client.types.objects.with_streaming_response.multiple_properties_same_model() as response:
            assert not response.is_closed

            object_ = response.parse()
            assert_matches_type(ObjectMultiplePropertiesSameModelResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_multiple_properties_same_ref(self, client: Sink) -> None:
        object_ = client.types.objects.multiple_properties_same_ref()
        assert_matches_type(ObjectMultiplePropertiesSameRefResponse, object_, path=["response"])

    @parametrize
    def test_raw_response_multiple_properties_same_ref(self, client: Sink) -> None:
        response = client.types.objects.with_raw_response.multiple_properties_same_ref()

        assert response.is_closed is True
        object_ = response.parse()
        assert_matches_type(ObjectMultiplePropertiesSameRefResponse, object_, path=["response"])

    @parametrize
    def test_streaming_response_multiple_properties_same_ref(self, client: Sink) -> None:
        with client.types.objects.with_streaming_response.multiple_properties_same_ref() as response:
            assert not response.is_closed

            object_ = response.parse()
            assert_matches_type(ObjectMultiplePropertiesSameRefResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_two_dimensional_array_primitive_property(self, client: Sink) -> None:
        object_ = client.types.objects.two_dimensional_array_primitive_property()
        assert_matches_type(ObjectTwoDimensionalArrayPrimitivePropertyResponse, object_, path=["response"])

    @parametrize
    def test_raw_response_two_dimensional_array_primitive_property(self, client: Sink) -> None:
        response = client.types.objects.with_raw_response.two_dimensional_array_primitive_property()

        assert response.is_closed is True
        object_ = response.parse()
        assert_matches_type(ObjectTwoDimensionalArrayPrimitivePropertyResponse, object_, path=["response"])

    @parametrize
    def test_streaming_response_two_dimensional_array_primitive_property(self, client: Sink) -> None:
        with client.types.objects.with_streaming_response.two_dimensional_array_primitive_property() as response:
            assert not response.is_closed

            object_ = response.parse()
            assert_matches_type(ObjectTwoDimensionalArrayPrimitivePropertyResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_unknown_object(self, client: Sink) -> None:
        object_ = client.types.objects.unknown_object()
        assert_matches_type(object, object_, path=["response"])

    @parametrize
    def test_raw_response_unknown_object(self, client: Sink) -> None:
        response = client.types.objects.with_raw_response.unknown_object()

        assert response.is_closed is True
        object_ = response.parse()
        assert_matches_type(object, object_, path=["response"])

    @parametrize
    def test_streaming_response_unknown_object(self, client: Sink) -> None:
        with client.types.objects.with_streaming_response.unknown_object() as response:
            assert not response.is_closed

            object_ = response.parse()
            assert_matches_type(object, object_, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncObjects:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_mixed_known_and_unknown(self, async_client: AsyncSink) -> None:
        object_ = await async_client.types.objects.mixed_known_and_unknown()
        assert_matches_type(ObjectMixedKnownAndUnknownResponse, object_, path=["response"])

    @parametrize
    async def test_raw_response_mixed_known_and_unknown(self, async_client: AsyncSink) -> None:
        response = await async_client.types.objects.with_raw_response.mixed_known_and_unknown()

        assert response.is_closed is True
        object_ = response.parse()
        assert_matches_type(ObjectMixedKnownAndUnknownResponse, object_, path=["response"])

    @parametrize
    async def test_streaming_response_mixed_known_and_unknown(self, async_client: AsyncSink) -> None:
        async with async_client.types.objects.with_streaming_response.mixed_known_and_unknown() as response:
            assert not response.is_closed

            object_ = await response.parse()
            assert_matches_type(ObjectMixedKnownAndUnknownResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_multiple_array_properties_same_ref(self, async_client: AsyncSink) -> None:
        object_ = await async_client.types.objects.multiple_array_properties_same_ref()
        assert_matches_type(ObjectMultipleArrayPropertiesSameRefResponse, object_, path=["response"])

    @parametrize
    async def test_raw_response_multiple_array_properties_same_ref(self, async_client: AsyncSink) -> None:
        response = await async_client.types.objects.with_raw_response.multiple_array_properties_same_ref()

        assert response.is_closed is True
        object_ = response.parse()
        assert_matches_type(ObjectMultipleArrayPropertiesSameRefResponse, object_, path=["response"])

    @parametrize
    async def test_streaming_response_multiple_array_properties_same_ref(self, async_client: AsyncSink) -> None:
        async with async_client.types.objects.with_streaming_response.multiple_array_properties_same_ref() as response:
            assert not response.is_closed

            object_ = await response.parse()
            assert_matches_type(ObjectMultipleArrayPropertiesSameRefResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_multiple_properties_same_model(self, async_client: AsyncSink) -> None:
        object_ = await async_client.types.objects.multiple_properties_same_model()
        assert_matches_type(ObjectMultiplePropertiesSameModelResponse, object_, path=["response"])

    @parametrize
    async def test_raw_response_multiple_properties_same_model(self, async_client: AsyncSink) -> None:
        response = await async_client.types.objects.with_raw_response.multiple_properties_same_model()

        assert response.is_closed is True
        object_ = response.parse()
        assert_matches_type(ObjectMultiplePropertiesSameModelResponse, object_, path=["response"])

    @parametrize
    async def test_streaming_response_multiple_properties_same_model(self, async_client: AsyncSink) -> None:
        async with async_client.types.objects.with_streaming_response.multiple_properties_same_model() as response:
            assert not response.is_closed

            object_ = await response.parse()
            assert_matches_type(ObjectMultiplePropertiesSameModelResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_multiple_properties_same_ref(self, async_client: AsyncSink) -> None:
        object_ = await async_client.types.objects.multiple_properties_same_ref()
        assert_matches_type(ObjectMultiplePropertiesSameRefResponse, object_, path=["response"])

    @parametrize
    async def test_raw_response_multiple_properties_same_ref(self, async_client: AsyncSink) -> None:
        response = await async_client.types.objects.with_raw_response.multiple_properties_same_ref()

        assert response.is_closed is True
        object_ = response.parse()
        assert_matches_type(ObjectMultiplePropertiesSameRefResponse, object_, path=["response"])

    @parametrize
    async def test_streaming_response_multiple_properties_same_ref(self, async_client: AsyncSink) -> None:
        async with async_client.types.objects.with_streaming_response.multiple_properties_same_ref() as response:
            assert not response.is_closed

            object_ = await response.parse()
            assert_matches_type(ObjectMultiplePropertiesSameRefResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_two_dimensional_array_primitive_property(self, async_client: AsyncSink) -> None:
        object_ = await async_client.types.objects.two_dimensional_array_primitive_property()
        assert_matches_type(ObjectTwoDimensionalArrayPrimitivePropertyResponse, object_, path=["response"])

    @parametrize
    async def test_raw_response_two_dimensional_array_primitive_property(self, async_client: AsyncSink) -> None:
        response = await async_client.types.objects.with_raw_response.two_dimensional_array_primitive_property()

        assert response.is_closed is True
        object_ = response.parse()
        assert_matches_type(ObjectTwoDimensionalArrayPrimitivePropertyResponse, object_, path=["response"])

    @parametrize
    async def test_streaming_response_two_dimensional_array_primitive_property(self, async_client: AsyncSink) -> None:
        async with (
            async_client.types.objects.with_streaming_response.two_dimensional_array_primitive_property()
        ) as response:
            assert not response.is_closed

            object_ = await response.parse()
            assert_matches_type(ObjectTwoDimensionalArrayPrimitivePropertyResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_unknown_object(self, async_client: AsyncSink) -> None:
        object_ = await async_client.types.objects.unknown_object()
        assert_matches_type(object, object_, path=["response"])

    @parametrize
    async def test_raw_response_unknown_object(self, async_client: AsyncSink) -> None:
        response = await async_client.types.objects.with_raw_response.unknown_object()

        assert response.is_closed is True
        object_ = response.parse()
        assert_matches_type(object, object_, path=["response"])

    @parametrize
    async def test_streaming_response_unknown_object(self, async_client: AsyncSink) -> None:
        async with async_client.types.objects.with_streaming_response.unknown_object() as response:
            assert not response.is_closed

            object_ = await response.parse()
            assert_matches_type(object, object_, path=["response"])

        assert cast(Any, response.is_closed) is True
