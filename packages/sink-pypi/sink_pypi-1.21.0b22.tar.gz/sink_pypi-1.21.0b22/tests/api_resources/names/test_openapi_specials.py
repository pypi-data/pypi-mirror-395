# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.names import OpenAPISpecialUsedUsedAsPropertyNameResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestOpenAPISpecials:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_used_used_as_property_name(self, client: Sink) -> None:
        openapi_special = client.names.openapi_specials.used_used_as_property_name()
        assert_matches_type(OpenAPISpecialUsedUsedAsPropertyNameResponse, openapi_special, path=["response"])

    @parametrize
    def test_raw_response_used_used_as_property_name(self, client: Sink) -> None:
        response = client.names.openapi_specials.with_raw_response.used_used_as_property_name()

        assert response.is_closed is True
        openapi_special = response.parse()
        assert_matches_type(OpenAPISpecialUsedUsedAsPropertyNameResponse, openapi_special, path=["response"])

    @parametrize
    def test_streaming_response_used_used_as_property_name(self, client: Sink) -> None:
        with client.names.openapi_specials.with_streaming_response.used_used_as_property_name() as response:
            assert not response.is_closed

            openapi_special = response.parse()
            assert_matches_type(OpenAPISpecialUsedUsedAsPropertyNameResponse, openapi_special, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncOpenAPISpecials:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_used_used_as_property_name(self, async_client: AsyncSink) -> None:
        openapi_special = await async_client.names.openapi_specials.used_used_as_property_name()
        assert_matches_type(OpenAPISpecialUsedUsedAsPropertyNameResponse, openapi_special, path=["response"])

    @parametrize
    async def test_raw_response_used_used_as_property_name(self, async_client: AsyncSink) -> None:
        response = await async_client.names.openapi_specials.with_raw_response.used_used_as_property_name()

        assert response.is_closed is True
        openapi_special = response.parse()
        assert_matches_type(OpenAPISpecialUsedUsedAsPropertyNameResponse, openapi_special, path=["response"])

    @parametrize
    async def test_streaming_response_used_used_as_property_name(self, async_client: AsyncSink) -> None:
        async with async_client.names.openapi_specials.with_streaming_response.used_used_as_property_name() as response:
            assert not response.is_closed

            openapi_special = await response.parse()
            assert_matches_type(OpenAPISpecialUsedUsedAsPropertyNameResponse, openapi_special, path=["response"])

        assert cast(Any, response.is_closed) is True
