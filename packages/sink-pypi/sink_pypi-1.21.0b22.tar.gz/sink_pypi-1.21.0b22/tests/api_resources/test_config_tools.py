# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import ModelFromSchemasRef, ConfigToolModelRefFromNestedResponseBodyResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestConfigTools:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_model_ref_from_nested_response_body(self, client: Sink) -> None:
        config_tool = client.config_tools.model_ref_from_nested_response_body()
        assert_matches_type(ConfigToolModelRefFromNestedResponseBodyResponse, config_tool, path=["response"])

    @parametrize
    def test_raw_response_model_ref_from_nested_response_body(self, client: Sink) -> None:
        response = client.config_tools.with_raw_response.model_ref_from_nested_response_body()

        assert response.is_closed is True
        config_tool = response.parse()
        assert_matches_type(ConfigToolModelRefFromNestedResponseBodyResponse, config_tool, path=["response"])

    @parametrize
    def test_streaming_response_model_ref_from_nested_response_body(self, client: Sink) -> None:
        with client.config_tools.with_streaming_response.model_ref_from_nested_response_body() as response:
            assert not response.is_closed

            config_tool = response.parse()
            assert_matches_type(ConfigToolModelRefFromNestedResponseBodyResponse, config_tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_model_ref_from_schemas(self, client: Sink) -> None:
        config_tool = client.config_tools.model_ref_from_schemas()
        assert_matches_type(ModelFromSchemasRef, config_tool, path=["response"])

    @parametrize
    def test_raw_response_model_ref_from_schemas(self, client: Sink) -> None:
        response = client.config_tools.with_raw_response.model_ref_from_schemas()

        assert response.is_closed is True
        config_tool = response.parse()
        assert_matches_type(ModelFromSchemasRef, config_tool, path=["response"])

    @parametrize
    def test_streaming_response_model_ref_from_schemas(self, client: Sink) -> None:
        with client.config_tools.with_streaming_response.model_ref_from_schemas() as response:
            assert not response.is_closed

            config_tool = response.parse()
            assert_matches_type(ModelFromSchemasRef, config_tool, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncConfigTools:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_model_ref_from_nested_response_body(self, async_client: AsyncSink) -> None:
        config_tool = await async_client.config_tools.model_ref_from_nested_response_body()
        assert_matches_type(ConfigToolModelRefFromNestedResponseBodyResponse, config_tool, path=["response"])

    @parametrize
    async def test_raw_response_model_ref_from_nested_response_body(self, async_client: AsyncSink) -> None:
        response = await async_client.config_tools.with_raw_response.model_ref_from_nested_response_body()

        assert response.is_closed is True
        config_tool = response.parse()
        assert_matches_type(ConfigToolModelRefFromNestedResponseBodyResponse, config_tool, path=["response"])

    @parametrize
    async def test_streaming_response_model_ref_from_nested_response_body(self, async_client: AsyncSink) -> None:
        async with async_client.config_tools.with_streaming_response.model_ref_from_nested_response_body() as response:
            assert not response.is_closed

            config_tool = await response.parse()
            assert_matches_type(ConfigToolModelRefFromNestedResponseBodyResponse, config_tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_model_ref_from_schemas(self, async_client: AsyncSink) -> None:
        config_tool = await async_client.config_tools.model_ref_from_schemas()
        assert_matches_type(ModelFromSchemasRef, config_tool, path=["response"])

    @parametrize
    async def test_raw_response_model_ref_from_schemas(self, async_client: AsyncSink) -> None:
        response = await async_client.config_tools.with_raw_response.model_ref_from_schemas()

        assert response.is_closed is True
        config_tool = response.parse()
        assert_matches_type(ModelFromSchemasRef, config_tool, path=["response"])

    @parametrize
    async def test_streaming_response_model_ref_from_schemas(self, async_client: AsyncSink) -> None:
        async with async_client.config_tools.with_streaming_response.model_ref_from_schemas() as response:
            assert not response.is_closed

            config_tool = await response.parse()
            assert_matches_type(ModelFromSchemasRef, config_tool, path=["response"])

        assert cast(Any, response.is_closed) is True
