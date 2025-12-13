# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.body_params import ModelNewTypeString

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUnions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_param_union_enum_new_type(self, client: Sink) -> None:
        union = client.body_params.unions.param_union_enum_new_type()
        assert union is None

    @parametrize
    def test_method_param_union_enum_new_type_with_all_params(self, client: Sink) -> None:
        union = client.body_params.unions.param_union_enum_new_type(
            model=ModelNewTypeString("my-custom-model"),
        )
        assert union is None

    @parametrize
    def test_raw_response_param_union_enum_new_type(self, client: Sink) -> None:
        response = client.body_params.unions.with_raw_response.param_union_enum_new_type()

        assert response.is_closed is True
        union = response.parse()
        assert union is None

    @parametrize
    def test_streaming_response_param_union_enum_new_type(self, client: Sink) -> None:
        with client.body_params.unions.with_streaming_response.param_union_enum_new_type() as response:
            assert not response.is_closed

            union = response.parse()
            assert union is None

        assert cast(Any, response.is_closed) is True


class TestAsyncUnions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_param_union_enum_new_type(self, async_client: AsyncSink) -> None:
        union = await async_client.body_params.unions.param_union_enum_new_type()
        assert union is None

    @parametrize
    async def test_method_param_union_enum_new_type_with_all_params(self, async_client: AsyncSink) -> None:
        union = await async_client.body_params.unions.param_union_enum_new_type(
            model=ModelNewTypeString("my-custom-model"),
        )
        assert union is None

    @parametrize
    async def test_raw_response_param_union_enum_new_type(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.unions.with_raw_response.param_union_enum_new_type()

        assert response.is_closed is True
        union = response.parse()
        assert union is None

    @parametrize
    async def test_streaming_response_param_union_enum_new_type(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.unions.with_streaming_response.param_union_enum_new_type() as response:
            assert not response.is_closed

            union = await response.parse()
            assert union is None

        assert cast(Any, response.is_closed) is True
