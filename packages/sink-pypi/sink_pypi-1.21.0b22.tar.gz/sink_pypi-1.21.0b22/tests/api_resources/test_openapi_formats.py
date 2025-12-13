# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Optional, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import (
    OpenAPIFormatArrayTypeOneEntryResponse,
    OpenAPIFormatArrayTypeOneEntryWithNullResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestOpenAPIFormats:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_array_type_one_entry(self, client: Sink) -> None:
        openapi_format = client.openapi_formats.array_type_one_entry(
            enable_debug_logging=True,
        )
        assert_matches_type(OpenAPIFormatArrayTypeOneEntryResponse, openapi_format, path=["response"])

    @parametrize
    def test_raw_response_array_type_one_entry(self, client: Sink) -> None:
        response = client.openapi_formats.with_raw_response.array_type_one_entry(
            enable_debug_logging=True,
        )

        assert response.is_closed is True
        openapi_format = response.parse()
        assert_matches_type(OpenAPIFormatArrayTypeOneEntryResponse, openapi_format, path=["response"])

    @parametrize
    def test_streaming_response_array_type_one_entry(self, client: Sink) -> None:
        with client.openapi_formats.with_streaming_response.array_type_one_entry(
            enable_debug_logging=True,
        ) as response:
            assert not response.is_closed

            openapi_format = response.parse()
            assert_matches_type(OpenAPIFormatArrayTypeOneEntryResponse, openapi_format, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_array_type_one_entry_with_null(self, client: Sink) -> None:
        openapi_format = client.openapi_formats.array_type_one_entry_with_null()
        assert_matches_type(Optional[OpenAPIFormatArrayTypeOneEntryWithNullResponse], openapi_format, path=["response"])

    @parametrize
    def test_method_array_type_one_entry_with_null_with_all_params(self, client: Sink) -> None:
        openapi_format = client.openapi_formats.array_type_one_entry_with_null(
            enable_debug_logging=True,
        )
        assert_matches_type(Optional[OpenAPIFormatArrayTypeOneEntryWithNullResponse], openapi_format, path=["response"])

    @parametrize
    def test_raw_response_array_type_one_entry_with_null(self, client: Sink) -> None:
        response = client.openapi_formats.with_raw_response.array_type_one_entry_with_null()

        assert response.is_closed is True
        openapi_format = response.parse()
        assert_matches_type(Optional[OpenAPIFormatArrayTypeOneEntryWithNullResponse], openapi_format, path=["response"])

    @parametrize
    def test_streaming_response_array_type_one_entry_with_null(self, client: Sink) -> None:
        with client.openapi_formats.with_streaming_response.array_type_one_entry_with_null() as response:
            assert not response.is_closed

            openapi_format = response.parse()
            assert_matches_type(
                Optional[OpenAPIFormatArrayTypeOneEntryWithNullResponse], openapi_format, path=["response"]
            )

        assert cast(Any, response.is_closed) is True


class TestAsyncOpenAPIFormats:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_array_type_one_entry(self, async_client: AsyncSink) -> None:
        openapi_format = await async_client.openapi_formats.array_type_one_entry(
            enable_debug_logging=True,
        )
        assert_matches_type(OpenAPIFormatArrayTypeOneEntryResponse, openapi_format, path=["response"])

    @parametrize
    async def test_raw_response_array_type_one_entry(self, async_client: AsyncSink) -> None:
        response = await async_client.openapi_formats.with_raw_response.array_type_one_entry(
            enable_debug_logging=True,
        )

        assert response.is_closed is True
        openapi_format = response.parse()
        assert_matches_type(OpenAPIFormatArrayTypeOneEntryResponse, openapi_format, path=["response"])

    @parametrize
    async def test_streaming_response_array_type_one_entry(self, async_client: AsyncSink) -> None:
        async with async_client.openapi_formats.with_streaming_response.array_type_one_entry(
            enable_debug_logging=True,
        ) as response:
            assert not response.is_closed

            openapi_format = await response.parse()
            assert_matches_type(OpenAPIFormatArrayTypeOneEntryResponse, openapi_format, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_array_type_one_entry_with_null(self, async_client: AsyncSink) -> None:
        openapi_format = await async_client.openapi_formats.array_type_one_entry_with_null()
        assert_matches_type(Optional[OpenAPIFormatArrayTypeOneEntryWithNullResponse], openapi_format, path=["response"])

    @parametrize
    async def test_method_array_type_one_entry_with_null_with_all_params(self, async_client: AsyncSink) -> None:
        openapi_format = await async_client.openapi_formats.array_type_one_entry_with_null(
            enable_debug_logging=True,
        )
        assert_matches_type(Optional[OpenAPIFormatArrayTypeOneEntryWithNullResponse], openapi_format, path=["response"])

    @parametrize
    async def test_raw_response_array_type_one_entry_with_null(self, async_client: AsyncSink) -> None:
        response = await async_client.openapi_formats.with_raw_response.array_type_one_entry_with_null()

        assert response.is_closed is True
        openapi_format = response.parse()
        assert_matches_type(Optional[OpenAPIFormatArrayTypeOneEntryWithNullResponse], openapi_format, path=["response"])

    @parametrize
    async def test_streaming_response_array_type_one_entry_with_null(self, async_client: AsyncSink) -> None:
        async with async_client.openapi_formats.with_streaming_response.array_type_one_entry_with_null() as response:
            assert not response.is_closed

            openapi_format = await response.parse()
            assert_matches_type(
                Optional[OpenAPIFormatArrayTypeOneEntryWithNullResponse], openapi_format, path=["response"]
            )

        assert cast(Any, response.is_closed) is True
