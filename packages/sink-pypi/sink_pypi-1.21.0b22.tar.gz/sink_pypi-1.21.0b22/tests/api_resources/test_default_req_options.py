# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.shared import BasicSharedModelObject

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDefaultReqOptions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_example_method(self, client: Sink) -> None:
        default_req_option = client.default_req_options.example_method()
        assert_matches_type(BasicSharedModelObject, default_req_option, path=["response"])

    @parametrize
    def test_raw_response_example_method(self, client: Sink) -> None:
        response = client.default_req_options.with_raw_response.example_method()

        assert response.is_closed is True
        default_req_option = response.parse()
        assert_matches_type(BasicSharedModelObject, default_req_option, path=["response"])

    @parametrize
    def test_streaming_response_example_method(self, client: Sink) -> None:
        with client.default_req_options.with_streaming_response.example_method() as response:
            assert not response.is_closed

            default_req_option = response.parse()
            assert_matches_type(BasicSharedModelObject, default_req_option, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_with_param_override(self, client: Sink) -> None:
        default_req_option = client.default_req_options.with_param_override()
        assert_matches_type(BasicSharedModelObject, default_req_option, path=["response"])

    @parametrize
    def test_method_with_param_override_with_all_params(self, client: Sink) -> None:
        default_req_option = client.default_req_options.with_param_override(
            x_my_header=True,
        )
        assert_matches_type(BasicSharedModelObject, default_req_option, path=["response"])

    @parametrize
    def test_raw_response_with_param_override(self, client: Sink) -> None:
        response = client.default_req_options.with_raw_response.with_param_override()

        assert response.is_closed is True
        default_req_option = response.parse()
        assert_matches_type(BasicSharedModelObject, default_req_option, path=["response"])

    @parametrize
    def test_streaming_response_with_param_override(self, client: Sink) -> None:
        with client.default_req_options.with_streaming_response.with_param_override() as response:
            assert not response.is_closed

            default_req_option = response.parse()
            assert_matches_type(BasicSharedModelObject, default_req_option, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDefaultReqOptions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_example_method(self, async_client: AsyncSink) -> None:
        default_req_option = await async_client.default_req_options.example_method()
        assert_matches_type(BasicSharedModelObject, default_req_option, path=["response"])

    @parametrize
    async def test_raw_response_example_method(self, async_client: AsyncSink) -> None:
        response = await async_client.default_req_options.with_raw_response.example_method()

        assert response.is_closed is True
        default_req_option = response.parse()
        assert_matches_type(BasicSharedModelObject, default_req_option, path=["response"])

    @parametrize
    async def test_streaming_response_example_method(self, async_client: AsyncSink) -> None:
        async with async_client.default_req_options.with_streaming_response.example_method() as response:
            assert not response.is_closed

            default_req_option = await response.parse()
            assert_matches_type(BasicSharedModelObject, default_req_option, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_with_param_override(self, async_client: AsyncSink) -> None:
        default_req_option = await async_client.default_req_options.with_param_override()
        assert_matches_type(BasicSharedModelObject, default_req_option, path=["response"])

    @parametrize
    async def test_method_with_param_override_with_all_params(self, async_client: AsyncSink) -> None:
        default_req_option = await async_client.default_req_options.with_param_override(
            x_my_header=True,
        )
        assert_matches_type(BasicSharedModelObject, default_req_option, path=["response"])

    @parametrize
    async def test_raw_response_with_param_override(self, async_client: AsyncSink) -> None:
        response = await async_client.default_req_options.with_raw_response.with_param_override()

        assert response.is_closed is True
        default_req_option = response.parse()
        assert_matches_type(BasicSharedModelObject, default_req_option, path=["response"])

    @parametrize
    async def test_streaming_response_with_param_override(self, async_client: AsyncSink) -> None:
        async with async_client.default_req_options.with_streaming_response.with_param_override() as response:
            assert not response.is_closed

            default_req_option = await response.parse()
            assert_matches_type(BasicSharedModelObject, default_req_option, path=["response"])

        assert cast(Any, response.is_closed) is True
