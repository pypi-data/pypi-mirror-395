# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import (
    FileCreateBase64Response,
    FileCreateMultipartResponse,
    FileNoFileMultipartResponse,
    FileWithOptionalParamResponse,
    FileEverythingMultipartResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFiles:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create_base64(self, client: Sink) -> None:
        file = client.files.create_base64(
            file="U3RhaW5sZXNzIHJvY2tz",
            purpose="purpose",
        )
        assert_matches_type(FileCreateBase64Response, file, path=["response"])

    @parametrize
    def test_raw_response_create_base64(self, client: Sink) -> None:
        response = client.files.with_raw_response.create_base64(
            file="U3RhaW5sZXNzIHJvY2tz",
            purpose="purpose",
        )

        assert response.is_closed is True
        file = response.parse()
        assert_matches_type(FileCreateBase64Response, file, path=["response"])

    @parametrize
    def test_streaming_response_create_base64(self, client: Sink) -> None:
        with client.files.with_streaming_response.create_base64(
            file="U3RhaW5sZXNzIHJvY2tz",
            purpose="purpose",
        ) as response:
            assert not response.is_closed

            file = response.parse()
            assert_matches_type(FileCreateBase64Response, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_create_multipart(self, client: Sink) -> None:
        file = client.files.create_multipart(
            file=b"raw file contents",
            purpose="purpose",
        )
        assert_matches_type(FileCreateMultipartResponse, file, path=["response"])

    @parametrize
    def test_raw_response_create_multipart(self, client: Sink) -> None:
        response = client.files.with_raw_response.create_multipart(
            file=b"raw file contents",
            purpose="purpose",
        )

        assert response.is_closed is True
        file = response.parse()
        assert_matches_type(FileCreateMultipartResponse, file, path=["response"])

    @parametrize
    def test_streaming_response_create_multipart(self, client: Sink) -> None:
        with client.files.with_streaming_response.create_multipart(
            file=b"raw file contents",
            purpose="purpose",
        ) as response:
            assert not response.is_closed

            file = response.parse()
            assert_matches_type(FileCreateMultipartResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_everything_multipart(self, client: Sink) -> None:
        file = client.files.everything_multipart(
            b=True,
            e="a",
            f=0,
            file=b"raw file contents",
            i=0,
            purpose="purpose",
            s="s",
        )
        assert_matches_type(FileEverythingMultipartResponse, file, path=["response"])

    @parametrize
    def test_raw_response_everything_multipart(self, client: Sink) -> None:
        response = client.files.with_raw_response.everything_multipart(
            b=True,
            e="a",
            f=0,
            file=b"raw file contents",
            i=0,
            purpose="purpose",
            s="s",
        )

        assert response.is_closed is True
        file = response.parse()
        assert_matches_type(FileEverythingMultipartResponse, file, path=["response"])

    @parametrize
    def test_streaming_response_everything_multipart(self, client: Sink) -> None:
        with client.files.with_streaming_response.everything_multipart(
            b=True,
            e="a",
            f=0,
            file=b"raw file contents",
            i=0,
            purpose="purpose",
            s="s",
        ) as response:
            assert not response.is_closed

            file = response.parse()
            assert_matches_type(FileEverythingMultipartResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_no_file_multipart(self, client: Sink) -> None:
        file = client.files.no_file_multipart(
            purpose="purpose",
        )
        assert_matches_type(FileNoFileMultipartResponse, file, path=["response"])

    @parametrize
    def test_raw_response_no_file_multipart(self, client: Sink) -> None:
        response = client.files.with_raw_response.no_file_multipart(
            purpose="purpose",
        )

        assert response.is_closed is True
        file = response.parse()
        assert_matches_type(FileNoFileMultipartResponse, file, path=["response"])

    @parametrize
    def test_streaming_response_no_file_multipart(self, client: Sink) -> None:
        with client.files.with_streaming_response.no_file_multipart(
            purpose="purpose",
        ) as response:
            assert not response.is_closed

            file = response.parse()
            assert_matches_type(FileNoFileMultipartResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_with_optional_param(self, client: Sink) -> None:
        file = client.files.with_optional_param(
            image=b"raw file contents",
            prompt="A cute baby sea otter wearing a beret",
        )
        assert_matches_type(FileWithOptionalParamResponse, file, path=["response"])

    @parametrize
    def test_method_with_optional_param_with_all_params(self, client: Sink) -> None:
        file = client.files.with_optional_param(
            image=b"raw file contents",
            prompt="A cute baby sea otter wearing a beret",
            mask=b"raw file contents",
        )
        assert_matches_type(FileWithOptionalParamResponse, file, path=["response"])

    @parametrize
    def test_raw_response_with_optional_param(self, client: Sink) -> None:
        response = client.files.with_raw_response.with_optional_param(
            image=b"raw file contents",
            prompt="A cute baby sea otter wearing a beret",
        )

        assert response.is_closed is True
        file = response.parse()
        assert_matches_type(FileWithOptionalParamResponse, file, path=["response"])

    @parametrize
    def test_streaming_response_with_optional_param(self, client: Sink) -> None:
        with client.files.with_streaming_response.with_optional_param(
            image=b"raw file contents",
            prompt="A cute baby sea otter wearing a beret",
        ) as response:
            assert not response.is_closed

            file = response.parse()
            assert_matches_type(FileWithOptionalParamResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncFiles:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create_base64(self, async_client: AsyncSink) -> None:
        file = await async_client.files.create_base64(
            file="U3RhaW5sZXNzIHJvY2tz",
            purpose="purpose",
        )
        assert_matches_type(FileCreateBase64Response, file, path=["response"])

    @parametrize
    async def test_raw_response_create_base64(self, async_client: AsyncSink) -> None:
        response = await async_client.files.with_raw_response.create_base64(
            file="U3RhaW5sZXNzIHJvY2tz",
            purpose="purpose",
        )

        assert response.is_closed is True
        file = response.parse()
        assert_matches_type(FileCreateBase64Response, file, path=["response"])

    @parametrize
    async def test_streaming_response_create_base64(self, async_client: AsyncSink) -> None:
        async with async_client.files.with_streaming_response.create_base64(
            file="U3RhaW5sZXNzIHJvY2tz",
            purpose="purpose",
        ) as response:
            assert not response.is_closed

            file = await response.parse()
            assert_matches_type(FileCreateBase64Response, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_create_multipart(self, async_client: AsyncSink) -> None:
        file = await async_client.files.create_multipart(
            file=b"raw file contents",
            purpose="purpose",
        )
        assert_matches_type(FileCreateMultipartResponse, file, path=["response"])

    @parametrize
    async def test_raw_response_create_multipart(self, async_client: AsyncSink) -> None:
        response = await async_client.files.with_raw_response.create_multipart(
            file=b"raw file contents",
            purpose="purpose",
        )

        assert response.is_closed is True
        file = response.parse()
        assert_matches_type(FileCreateMultipartResponse, file, path=["response"])

    @parametrize
    async def test_streaming_response_create_multipart(self, async_client: AsyncSink) -> None:
        async with async_client.files.with_streaming_response.create_multipart(
            file=b"raw file contents",
            purpose="purpose",
        ) as response:
            assert not response.is_closed

            file = await response.parse()
            assert_matches_type(FileCreateMultipartResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_everything_multipart(self, async_client: AsyncSink) -> None:
        file = await async_client.files.everything_multipart(
            b=True,
            e="a",
            f=0,
            file=b"raw file contents",
            i=0,
            purpose="purpose",
            s="s",
        )
        assert_matches_type(FileEverythingMultipartResponse, file, path=["response"])

    @parametrize
    async def test_raw_response_everything_multipart(self, async_client: AsyncSink) -> None:
        response = await async_client.files.with_raw_response.everything_multipart(
            b=True,
            e="a",
            f=0,
            file=b"raw file contents",
            i=0,
            purpose="purpose",
            s="s",
        )

        assert response.is_closed is True
        file = response.parse()
        assert_matches_type(FileEverythingMultipartResponse, file, path=["response"])

    @parametrize
    async def test_streaming_response_everything_multipart(self, async_client: AsyncSink) -> None:
        async with async_client.files.with_streaming_response.everything_multipart(
            b=True,
            e="a",
            f=0,
            file=b"raw file contents",
            i=0,
            purpose="purpose",
            s="s",
        ) as response:
            assert not response.is_closed

            file = await response.parse()
            assert_matches_type(FileEverythingMultipartResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_no_file_multipart(self, async_client: AsyncSink) -> None:
        file = await async_client.files.no_file_multipart(
            purpose="purpose",
        )
        assert_matches_type(FileNoFileMultipartResponse, file, path=["response"])

    @parametrize
    async def test_raw_response_no_file_multipart(self, async_client: AsyncSink) -> None:
        response = await async_client.files.with_raw_response.no_file_multipart(
            purpose="purpose",
        )

        assert response.is_closed is True
        file = response.parse()
        assert_matches_type(FileNoFileMultipartResponse, file, path=["response"])

    @parametrize
    async def test_streaming_response_no_file_multipart(self, async_client: AsyncSink) -> None:
        async with async_client.files.with_streaming_response.no_file_multipart(
            purpose="purpose",
        ) as response:
            assert not response.is_closed

            file = await response.parse()
            assert_matches_type(FileNoFileMultipartResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_with_optional_param(self, async_client: AsyncSink) -> None:
        file = await async_client.files.with_optional_param(
            image=b"raw file contents",
            prompt="A cute baby sea otter wearing a beret",
        )
        assert_matches_type(FileWithOptionalParamResponse, file, path=["response"])

    @parametrize
    async def test_method_with_optional_param_with_all_params(self, async_client: AsyncSink) -> None:
        file = await async_client.files.with_optional_param(
            image=b"raw file contents",
            prompt="A cute baby sea otter wearing a beret",
            mask=b"raw file contents",
        )
        assert_matches_type(FileWithOptionalParamResponse, file, path=["response"])

    @parametrize
    async def test_raw_response_with_optional_param(self, async_client: AsyncSink) -> None:
        response = await async_client.files.with_raw_response.with_optional_param(
            image=b"raw file contents",
            prompt="A cute baby sea otter wearing a beret",
        )

        assert response.is_closed is True
        file = response.parse()
        assert_matches_type(FileWithOptionalParamResponse, file, path=["response"])

    @parametrize
    async def test_streaming_response_with_optional_param(self, async_client: AsyncSink) -> None:
        async with async_client.files.with_streaming_response.with_optional_param(
            image=b"raw file contents",
            prompt="A cute baby sea otter wearing a beret",
        ) as response:
            assert not response.is_closed

            file = await response.parse()
            assert_matches_type(FileWithOptionalParamResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True
