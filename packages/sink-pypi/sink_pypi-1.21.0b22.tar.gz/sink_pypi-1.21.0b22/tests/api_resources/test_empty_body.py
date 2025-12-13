# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.shared import BasicSharedModelObject

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEmptyBody:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_stainless_empty_object(self, client: Sink) -> None:
        empty_body = client.empty_body.stainless_empty_object(
            path_param="path_param",
        )
        assert_matches_type(BasicSharedModelObject, empty_body, path=["response"])

    @parametrize
    def test_method_stainless_empty_object_with_all_params(self, client: Sink) -> None:
        empty_body = client.empty_body.stainless_empty_object(
            path_param="path_param",
            query_param="query_param",
            second_query_param="second_query_param",
            body={},
        )
        assert_matches_type(BasicSharedModelObject, empty_body, path=["response"])

    @parametrize
    def test_raw_response_stainless_empty_object(self, client: Sink) -> None:
        response = client.empty_body.with_raw_response.stainless_empty_object(
            path_param="path_param",
        )

        assert response.is_closed is True
        empty_body = response.parse()
        assert_matches_type(BasicSharedModelObject, empty_body, path=["response"])

    @parametrize
    def test_streaming_response_stainless_empty_object(self, client: Sink) -> None:
        with client.empty_body.with_streaming_response.stainless_empty_object(
            path_param="path_param",
        ) as response:
            assert not response.is_closed

            empty_body = response.parse()
            assert_matches_type(BasicSharedModelObject, empty_body, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_stainless_empty_object(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_param` but received ''"):
            client.empty_body.with_raw_response.stainless_empty_object(
                path_param="",
            )

    @parametrize
    def test_method_typed_params(self, client: Sink) -> None:
        empty_body = client.empty_body.typed_params(
            path_param="path_param",
        )
        assert_matches_type(BasicSharedModelObject, empty_body, path=["response"])

    @parametrize
    def test_method_typed_params_with_all_params(self, client: Sink) -> None:
        empty_body = client.empty_body.typed_params(
            path_param="path_param",
            query_param="query_param",
            second_query_param="second_query_param",
            body={},
        )
        assert_matches_type(BasicSharedModelObject, empty_body, path=["response"])

    @parametrize
    def test_raw_response_typed_params(self, client: Sink) -> None:
        response = client.empty_body.with_raw_response.typed_params(
            path_param="path_param",
        )

        assert response.is_closed is True
        empty_body = response.parse()
        assert_matches_type(BasicSharedModelObject, empty_body, path=["response"])

    @parametrize
    def test_streaming_response_typed_params(self, client: Sink) -> None:
        with client.empty_body.with_streaming_response.typed_params(
            path_param="path_param",
        ) as response:
            assert not response.is_closed

            empty_body = response.parse()
            assert_matches_type(BasicSharedModelObject, empty_body, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_typed_params(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_param` but received ''"):
            client.empty_body.with_raw_response.typed_params(
                path_param="",
            )


class TestAsyncEmptyBody:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_stainless_empty_object(self, async_client: AsyncSink) -> None:
        empty_body = await async_client.empty_body.stainless_empty_object(
            path_param="path_param",
        )
        assert_matches_type(BasicSharedModelObject, empty_body, path=["response"])

    @parametrize
    async def test_method_stainless_empty_object_with_all_params(self, async_client: AsyncSink) -> None:
        empty_body = await async_client.empty_body.stainless_empty_object(
            path_param="path_param",
            query_param="query_param",
            second_query_param="second_query_param",
            body={},
        )
        assert_matches_type(BasicSharedModelObject, empty_body, path=["response"])

    @parametrize
    async def test_raw_response_stainless_empty_object(self, async_client: AsyncSink) -> None:
        response = await async_client.empty_body.with_raw_response.stainless_empty_object(
            path_param="path_param",
        )

        assert response.is_closed is True
        empty_body = response.parse()
        assert_matches_type(BasicSharedModelObject, empty_body, path=["response"])

    @parametrize
    async def test_streaming_response_stainless_empty_object(self, async_client: AsyncSink) -> None:
        async with async_client.empty_body.with_streaming_response.stainless_empty_object(
            path_param="path_param",
        ) as response:
            assert not response.is_closed

            empty_body = await response.parse()
            assert_matches_type(BasicSharedModelObject, empty_body, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_stainless_empty_object(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_param` but received ''"):
            await async_client.empty_body.with_raw_response.stainless_empty_object(
                path_param="",
            )

    @parametrize
    async def test_method_typed_params(self, async_client: AsyncSink) -> None:
        empty_body = await async_client.empty_body.typed_params(
            path_param="path_param",
        )
        assert_matches_type(BasicSharedModelObject, empty_body, path=["response"])

    @parametrize
    async def test_method_typed_params_with_all_params(self, async_client: AsyncSink) -> None:
        empty_body = await async_client.empty_body.typed_params(
            path_param="path_param",
            query_param="query_param",
            second_query_param="second_query_param",
            body={},
        )
        assert_matches_type(BasicSharedModelObject, empty_body, path=["response"])

    @parametrize
    async def test_raw_response_typed_params(self, async_client: AsyncSink) -> None:
        response = await async_client.empty_body.with_raw_response.typed_params(
            path_param="path_param",
        )

        assert response.is_closed is True
        empty_body = response.parse()
        assert_matches_type(BasicSharedModelObject, empty_body, path=["response"])

    @parametrize
    async def test_streaming_response_typed_params(self, async_client: AsyncSink) -> None:
        async with async_client.empty_body.with_streaming_response.typed_params(
            path_param="path_param",
        ) as response:
            assert not response.is_closed

            empty_body = await response.parse()
            assert_matches_type(BasicSharedModelObject, empty_body, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_typed_params(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_param` but received ''"):
            await async_client.empty_body.with_raw_response.typed_params(
                path_param="",
            )
