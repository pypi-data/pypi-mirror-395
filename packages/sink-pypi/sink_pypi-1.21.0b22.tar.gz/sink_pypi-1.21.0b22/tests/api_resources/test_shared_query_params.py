# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSharedQueryParams:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Sink) -> None:
        shared_query_param = client.shared_query_params.retrieve()
        assert_matches_type(str, shared_query_param, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Sink) -> None:
        shared_query_param = client.shared_query_params.retrieve(
            get1="get1",
            shared1="shared1",
            shared2="shared2",
        )
        assert_matches_type(str, shared_query_param, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Sink) -> None:
        response = client.shared_query_params.with_raw_response.retrieve()

        assert response.is_closed is True
        shared_query_param = response.parse()
        assert_matches_type(str, shared_query_param, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Sink) -> None:
        with client.shared_query_params.with_streaming_response.retrieve() as response:
            assert not response.is_closed

            shared_query_param = response.parse()
            assert_matches_type(str, shared_query_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Sink) -> None:
        shared_query_param = client.shared_query_params.delete()
        assert_matches_type(str, shared_query_param, path=["response"])

    @parametrize
    def test_method_delete_with_all_params(self, client: Sink) -> None:
        shared_query_param = client.shared_query_params.delete(
            get1="get1",
            shared1="shared1",
            shared2="shared2",
        )
        assert_matches_type(str, shared_query_param, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Sink) -> None:
        response = client.shared_query_params.with_raw_response.delete()

        assert response.is_closed is True
        shared_query_param = response.parse()
        assert_matches_type(str, shared_query_param, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Sink) -> None:
        with client.shared_query_params.with_streaming_response.delete() as response:
            assert not response.is_closed

            shared_query_param = response.parse()
            assert_matches_type(str, shared_query_param, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSharedQueryParams:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSink) -> None:
        shared_query_param = await async_client.shared_query_params.retrieve()
        assert_matches_type(str, shared_query_param, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSink) -> None:
        shared_query_param = await async_client.shared_query_params.retrieve(
            get1="get1",
            shared1="shared1",
            shared2="shared2",
        )
        assert_matches_type(str, shared_query_param, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSink) -> None:
        response = await async_client.shared_query_params.with_raw_response.retrieve()

        assert response.is_closed is True
        shared_query_param = response.parse()
        assert_matches_type(str, shared_query_param, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSink) -> None:
        async with async_client.shared_query_params.with_streaming_response.retrieve() as response:
            assert not response.is_closed

            shared_query_param = await response.parse()
            assert_matches_type(str, shared_query_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSink) -> None:
        shared_query_param = await async_client.shared_query_params.delete()
        assert_matches_type(str, shared_query_param, path=["response"])

    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncSink) -> None:
        shared_query_param = await async_client.shared_query_params.delete(
            get1="get1",
            shared1="shared1",
            shared2="shared2",
        )
        assert_matches_type(str, shared_query_param, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSink) -> None:
        response = await async_client.shared_query_params.with_raw_response.delete()

        assert response.is_closed is True
        shared_query_param = response.parse()
        assert_matches_type(str, shared_query_param, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSink) -> None:
        async with async_client.shared_query_params.with_streaming_response.delete() as response:
            assert not response.is_closed

            shared_query_param = await response.parse()
            assert_matches_type(str, shared_query_param, path=["response"])

        assert cast(Any, response.is_closed) is True
