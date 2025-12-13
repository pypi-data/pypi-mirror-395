# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.types import (
    UnionResponseDiscriminatedByPropertyNameResponse,
    UnionResponseDiscriminatedWithBasicMappingResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUnions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_array_param_discriminated_by_property_name(self, client: Sink) -> None:
        union = client.types.unions.array_param_discriminated_by_property_name(
            body=[
                {
                    "value": "value",
                    "type": "a",
                }
            ],
        )
        assert_matches_type(str, union, path=["response"])

    @parametrize
    def test_raw_response_array_param_discriminated_by_property_name(self, client: Sink) -> None:
        response = client.types.unions.with_raw_response.array_param_discriminated_by_property_name(
            body=[
                {
                    "value": "value",
                    "type": "a",
                }
            ],
        )

        assert response.is_closed is True
        union = response.parse()
        assert_matches_type(str, union, path=["response"])

    @parametrize
    def test_streaming_response_array_param_discriminated_by_property_name(self, client: Sink) -> None:
        with client.types.unions.with_streaming_response.array_param_discriminated_by_property_name(
            body=[
                {
                    "value": "value",
                    "type": "a",
                }
            ],
        ) as response:
            assert not response.is_closed

            union = response.parse()
            assert_matches_type(str, union, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_array_param_discriminated_with_basic_mapping(self, client: Sink) -> None:
        union = client.types.unions.array_param_discriminated_with_basic_mapping(
            body=[
                {
                    "value": "value",
                    "type": "a",
                }
            ],
        )
        assert_matches_type(str, union, path=["response"])

    @parametrize
    def test_raw_response_array_param_discriminated_with_basic_mapping(self, client: Sink) -> None:
        response = client.types.unions.with_raw_response.array_param_discriminated_with_basic_mapping(
            body=[
                {
                    "value": "value",
                    "type": "a",
                }
            ],
        )

        assert response.is_closed is True
        union = response.parse()
        assert_matches_type(str, union, path=["response"])

    @parametrize
    def test_streaming_response_array_param_discriminated_with_basic_mapping(self, client: Sink) -> None:
        with client.types.unions.with_streaming_response.array_param_discriminated_with_basic_mapping(
            body=[
                {
                    "value": "value",
                    "type": "a",
                }
            ],
        ) as response:
            assert not response.is_closed

            union = response.parse()
            assert_matches_type(str, union, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_param_discriminated_by_property_name_overload_1(self, client: Sink) -> None:
        union = client.types.unions.param_discriminated_by_property_name(
            value="value",
        )
        assert_matches_type(str, union, path=["response"])

    @parametrize
    def test_method_param_discriminated_by_property_name_with_all_params_overload_1(self, client: Sink) -> None:
        union = client.types.unions.param_discriminated_by_property_name(
            value="value",
            type="a",
        )
        assert_matches_type(str, union, path=["response"])

    @parametrize
    def test_raw_response_param_discriminated_by_property_name_overload_1(self, client: Sink) -> None:
        response = client.types.unions.with_raw_response.param_discriminated_by_property_name(
            value="value",
        )

        assert response.is_closed is True
        union = response.parse()
        assert_matches_type(str, union, path=["response"])

    @parametrize
    def test_streaming_response_param_discriminated_by_property_name_overload_1(self, client: Sink) -> None:
        with client.types.unions.with_streaming_response.param_discriminated_by_property_name(
            value="value",
        ) as response:
            assert not response.is_closed

            union = response.parse()
            assert_matches_type(str, union, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_param_discriminated_by_property_name_overload_2(self, client: Sink) -> None:
        union = client.types.unions.param_discriminated_by_property_name(
            value="value",
        )
        assert_matches_type(str, union, path=["response"])

    @parametrize
    def test_method_param_discriminated_by_property_name_with_all_params_overload_2(self, client: Sink) -> None:
        union = client.types.unions.param_discriminated_by_property_name(
            value="value",
            type="b",
        )
        assert_matches_type(str, union, path=["response"])

    @parametrize
    def test_raw_response_param_discriminated_by_property_name_overload_2(self, client: Sink) -> None:
        response = client.types.unions.with_raw_response.param_discriminated_by_property_name(
            value="value",
        )

        assert response.is_closed is True
        union = response.parse()
        assert_matches_type(str, union, path=["response"])

    @parametrize
    def test_streaming_response_param_discriminated_by_property_name_overload_2(self, client: Sink) -> None:
        with client.types.unions.with_streaming_response.param_discriminated_by_property_name(
            value="value",
        ) as response:
            assert not response.is_closed

            union = response.parse()
            assert_matches_type(str, union, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_param_discriminated_with_basic_mapping_overload_1(self, client: Sink) -> None:
        union = client.types.unions.param_discriminated_with_basic_mapping(
            value="value",
        )
        assert_matches_type(str, union, path=["response"])

    @parametrize
    def test_method_param_discriminated_with_basic_mapping_with_all_params_overload_1(self, client: Sink) -> None:
        union = client.types.unions.param_discriminated_with_basic_mapping(
            value="value",
            type="a",
        )
        assert_matches_type(str, union, path=["response"])

    @parametrize
    def test_raw_response_param_discriminated_with_basic_mapping_overload_1(self, client: Sink) -> None:
        response = client.types.unions.with_raw_response.param_discriminated_with_basic_mapping(
            value="value",
        )

        assert response.is_closed is True
        union = response.parse()
        assert_matches_type(str, union, path=["response"])

    @parametrize
    def test_streaming_response_param_discriminated_with_basic_mapping_overload_1(self, client: Sink) -> None:
        with client.types.unions.with_streaming_response.param_discriminated_with_basic_mapping(
            value="value",
        ) as response:
            assert not response.is_closed

            union = response.parse()
            assert_matches_type(str, union, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_param_discriminated_with_basic_mapping_overload_2(self, client: Sink) -> None:
        union = client.types.unions.param_discriminated_with_basic_mapping(
            value="value",
        )
        assert_matches_type(str, union, path=["response"])

    @parametrize
    def test_method_param_discriminated_with_basic_mapping_with_all_params_overload_2(self, client: Sink) -> None:
        union = client.types.unions.param_discriminated_with_basic_mapping(
            value="value",
            type="b",
        )
        assert_matches_type(str, union, path=["response"])

    @parametrize
    def test_raw_response_param_discriminated_with_basic_mapping_overload_2(self, client: Sink) -> None:
        response = client.types.unions.with_raw_response.param_discriminated_with_basic_mapping(
            value="value",
        )

        assert response.is_closed is True
        union = response.parse()
        assert_matches_type(str, union, path=["response"])

    @parametrize
    def test_streaming_response_param_discriminated_with_basic_mapping_overload_2(self, client: Sink) -> None:
        with client.types.unions.with_streaming_response.param_discriminated_with_basic_mapping(
            value="value",
        ) as response:
            assert not response.is_closed

            union = response.parse()
            assert_matches_type(str, union, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_response_discriminated_by_property_name(self, client: Sink) -> None:
        union = client.types.unions.response_discriminated_by_property_name()
        assert_matches_type(UnionResponseDiscriminatedByPropertyNameResponse, union, path=["response"])

    @parametrize
    def test_raw_response_response_discriminated_by_property_name(self, client: Sink) -> None:
        response = client.types.unions.with_raw_response.response_discriminated_by_property_name()

        assert response.is_closed is True
        union = response.parse()
        assert_matches_type(UnionResponseDiscriminatedByPropertyNameResponse, union, path=["response"])

    @parametrize
    def test_streaming_response_response_discriminated_by_property_name(self, client: Sink) -> None:
        with client.types.unions.with_streaming_response.response_discriminated_by_property_name() as response:
            assert not response.is_closed

            union = response.parse()
            assert_matches_type(UnionResponseDiscriminatedByPropertyNameResponse, union, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_response_discriminated_with_basic_mapping(self, client: Sink) -> None:
        union = client.types.unions.response_discriminated_with_basic_mapping()
        assert_matches_type(UnionResponseDiscriminatedWithBasicMappingResponse, union, path=["response"])

    @parametrize
    def test_raw_response_response_discriminated_with_basic_mapping(self, client: Sink) -> None:
        response = client.types.unions.with_raw_response.response_discriminated_with_basic_mapping()

        assert response.is_closed is True
        union = response.parse()
        assert_matches_type(UnionResponseDiscriminatedWithBasicMappingResponse, union, path=["response"])

    @parametrize
    def test_streaming_response_response_discriminated_with_basic_mapping(self, client: Sink) -> None:
        with client.types.unions.with_streaming_response.response_discriminated_with_basic_mapping() as response:
            assert not response.is_closed

            union = response.parse()
            assert_matches_type(UnionResponseDiscriminatedWithBasicMappingResponse, union, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncUnions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_array_param_discriminated_by_property_name(self, async_client: AsyncSink) -> None:
        union = await async_client.types.unions.array_param_discriminated_by_property_name(
            body=[
                {
                    "value": "value",
                    "type": "a",
                }
            ],
        )
        assert_matches_type(str, union, path=["response"])

    @parametrize
    async def test_raw_response_array_param_discriminated_by_property_name(self, async_client: AsyncSink) -> None:
        response = await async_client.types.unions.with_raw_response.array_param_discriminated_by_property_name(
            body=[
                {
                    "value": "value",
                    "type": "a",
                }
            ],
        )

        assert response.is_closed is True
        union = response.parse()
        assert_matches_type(str, union, path=["response"])

    @parametrize
    async def test_streaming_response_array_param_discriminated_by_property_name(self, async_client: AsyncSink) -> None:
        async with async_client.types.unions.with_streaming_response.array_param_discriminated_by_property_name(
            body=[
                {
                    "value": "value",
                    "type": "a",
                }
            ],
        ) as response:
            assert not response.is_closed

            union = await response.parse()
            assert_matches_type(str, union, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_array_param_discriminated_with_basic_mapping(self, async_client: AsyncSink) -> None:
        union = await async_client.types.unions.array_param_discriminated_with_basic_mapping(
            body=[
                {
                    "value": "value",
                    "type": "a",
                }
            ],
        )
        assert_matches_type(str, union, path=["response"])

    @parametrize
    async def test_raw_response_array_param_discriminated_with_basic_mapping(self, async_client: AsyncSink) -> None:
        response = await async_client.types.unions.with_raw_response.array_param_discriminated_with_basic_mapping(
            body=[
                {
                    "value": "value",
                    "type": "a",
                }
            ],
        )

        assert response.is_closed is True
        union = response.parse()
        assert_matches_type(str, union, path=["response"])

    @parametrize
    async def test_streaming_response_array_param_discriminated_with_basic_mapping(
        self, async_client: AsyncSink
    ) -> None:
        async with async_client.types.unions.with_streaming_response.array_param_discriminated_with_basic_mapping(
            body=[
                {
                    "value": "value",
                    "type": "a",
                }
            ],
        ) as response:
            assert not response.is_closed

            union = await response.parse()
            assert_matches_type(str, union, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_param_discriminated_by_property_name_overload_1(self, async_client: AsyncSink) -> None:
        union = await async_client.types.unions.param_discriminated_by_property_name(
            value="value",
        )
        assert_matches_type(str, union, path=["response"])

    @parametrize
    async def test_method_param_discriminated_by_property_name_with_all_params_overload_1(
        self, async_client: AsyncSink
    ) -> None:
        union = await async_client.types.unions.param_discriminated_by_property_name(
            value="value",
            type="a",
        )
        assert_matches_type(str, union, path=["response"])

    @parametrize
    async def test_raw_response_param_discriminated_by_property_name_overload_1(self, async_client: AsyncSink) -> None:
        response = await async_client.types.unions.with_raw_response.param_discriminated_by_property_name(
            value="value",
        )

        assert response.is_closed is True
        union = response.parse()
        assert_matches_type(str, union, path=["response"])

    @parametrize
    async def test_streaming_response_param_discriminated_by_property_name_overload_1(
        self, async_client: AsyncSink
    ) -> None:
        async with async_client.types.unions.with_streaming_response.param_discriminated_by_property_name(
            value="value",
        ) as response:
            assert not response.is_closed

            union = await response.parse()
            assert_matches_type(str, union, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_param_discriminated_by_property_name_overload_2(self, async_client: AsyncSink) -> None:
        union = await async_client.types.unions.param_discriminated_by_property_name(
            value="value",
        )
        assert_matches_type(str, union, path=["response"])

    @parametrize
    async def test_method_param_discriminated_by_property_name_with_all_params_overload_2(
        self, async_client: AsyncSink
    ) -> None:
        union = await async_client.types.unions.param_discriminated_by_property_name(
            value="value",
            type="b",
        )
        assert_matches_type(str, union, path=["response"])

    @parametrize
    async def test_raw_response_param_discriminated_by_property_name_overload_2(self, async_client: AsyncSink) -> None:
        response = await async_client.types.unions.with_raw_response.param_discriminated_by_property_name(
            value="value",
        )

        assert response.is_closed is True
        union = response.parse()
        assert_matches_type(str, union, path=["response"])

    @parametrize
    async def test_streaming_response_param_discriminated_by_property_name_overload_2(
        self, async_client: AsyncSink
    ) -> None:
        async with async_client.types.unions.with_streaming_response.param_discriminated_by_property_name(
            value="value",
        ) as response:
            assert not response.is_closed

            union = await response.parse()
            assert_matches_type(str, union, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_param_discriminated_with_basic_mapping_overload_1(self, async_client: AsyncSink) -> None:
        union = await async_client.types.unions.param_discriminated_with_basic_mapping(
            value="value",
        )
        assert_matches_type(str, union, path=["response"])

    @parametrize
    async def test_method_param_discriminated_with_basic_mapping_with_all_params_overload_1(
        self, async_client: AsyncSink
    ) -> None:
        union = await async_client.types.unions.param_discriminated_with_basic_mapping(
            value="value",
            type="a",
        )
        assert_matches_type(str, union, path=["response"])

    @parametrize
    async def test_raw_response_param_discriminated_with_basic_mapping_overload_1(
        self, async_client: AsyncSink
    ) -> None:
        response = await async_client.types.unions.with_raw_response.param_discriminated_with_basic_mapping(
            value="value",
        )

        assert response.is_closed is True
        union = response.parse()
        assert_matches_type(str, union, path=["response"])

    @parametrize
    async def test_streaming_response_param_discriminated_with_basic_mapping_overload_1(
        self, async_client: AsyncSink
    ) -> None:
        async with async_client.types.unions.with_streaming_response.param_discriminated_with_basic_mapping(
            value="value",
        ) as response:
            assert not response.is_closed

            union = await response.parse()
            assert_matches_type(str, union, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_param_discriminated_with_basic_mapping_overload_2(self, async_client: AsyncSink) -> None:
        union = await async_client.types.unions.param_discriminated_with_basic_mapping(
            value="value",
        )
        assert_matches_type(str, union, path=["response"])

    @parametrize
    async def test_method_param_discriminated_with_basic_mapping_with_all_params_overload_2(
        self, async_client: AsyncSink
    ) -> None:
        union = await async_client.types.unions.param_discriminated_with_basic_mapping(
            value="value",
            type="b",
        )
        assert_matches_type(str, union, path=["response"])

    @parametrize
    async def test_raw_response_param_discriminated_with_basic_mapping_overload_2(
        self, async_client: AsyncSink
    ) -> None:
        response = await async_client.types.unions.with_raw_response.param_discriminated_with_basic_mapping(
            value="value",
        )

        assert response.is_closed is True
        union = response.parse()
        assert_matches_type(str, union, path=["response"])

    @parametrize
    async def test_streaming_response_param_discriminated_with_basic_mapping_overload_2(
        self, async_client: AsyncSink
    ) -> None:
        async with async_client.types.unions.with_streaming_response.param_discriminated_with_basic_mapping(
            value="value",
        ) as response:
            assert not response.is_closed

            union = await response.parse()
            assert_matches_type(str, union, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_response_discriminated_by_property_name(self, async_client: AsyncSink) -> None:
        union = await async_client.types.unions.response_discriminated_by_property_name()
        assert_matches_type(UnionResponseDiscriminatedByPropertyNameResponse, union, path=["response"])

    @parametrize
    async def test_raw_response_response_discriminated_by_property_name(self, async_client: AsyncSink) -> None:
        response = await async_client.types.unions.with_raw_response.response_discriminated_by_property_name()

        assert response.is_closed is True
        union = response.parse()
        assert_matches_type(UnionResponseDiscriminatedByPropertyNameResponse, union, path=["response"])

    @parametrize
    async def test_streaming_response_response_discriminated_by_property_name(self, async_client: AsyncSink) -> None:
        async with (
            async_client.types.unions.with_streaming_response.response_discriminated_by_property_name()
        ) as response:
            assert not response.is_closed

            union = await response.parse()
            assert_matches_type(UnionResponseDiscriminatedByPropertyNameResponse, union, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_response_discriminated_with_basic_mapping(self, async_client: AsyncSink) -> None:
        union = await async_client.types.unions.response_discriminated_with_basic_mapping()
        assert_matches_type(UnionResponseDiscriminatedWithBasicMappingResponse, union, path=["response"])

    @parametrize
    async def test_raw_response_response_discriminated_with_basic_mapping(self, async_client: AsyncSink) -> None:
        response = await async_client.types.unions.with_raw_response.response_discriminated_with_basic_mapping()

        assert response.is_closed is True
        union = response.parse()
        assert_matches_type(UnionResponseDiscriminatedWithBasicMappingResponse, union, path=["response"])

    @parametrize
    async def test_streaming_response_response_discriminated_with_basic_mapping(self, async_client: AsyncSink) -> None:
        async with (
            async_client.types.unions.with_streaming_response.response_discriminated_with_basic_mapping()
        ) as response:
            assert not response.is_closed

            union = await response.parse()
            assert_matches_type(UnionResponseDiscriminatedWithBasicMappingResponse, union, path=["response"])

        assert cast(Any, response.is_closed) is True
