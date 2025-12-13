# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import MyModel
from sink.api.sdk.pagination import (
    SyncPageCursorSharedRef,
    AsyncPageCursorSharedRef,
    SyncPageCursorNestedObjectRef,
    AsyncPageCursorNestedObjectRef,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRefs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_nested_object_ref(self, client: Sink) -> None:
        ref = client.pagination_tests.refs.nested_object_ref()
        assert_matches_type(SyncPageCursorNestedObjectRef[MyModel], ref, path=["response"])

    @parametrize
    def test_method_nested_object_ref_with_all_params(self, client: Sink) -> None:
        ref = client.pagination_tests.refs.nested_object_ref(
            cursor="cursor",
            limit=0,
            object_param={"foo": "foo"},
        )
        assert_matches_type(SyncPageCursorNestedObjectRef[MyModel], ref, path=["response"])

    @parametrize
    def test_raw_response_nested_object_ref(self, client: Sink) -> None:
        response = client.pagination_tests.refs.with_raw_response.nested_object_ref()

        assert response.is_closed is True
        ref = response.parse()
        assert_matches_type(SyncPageCursorNestedObjectRef[MyModel], ref, path=["response"])

    @parametrize
    def test_streaming_response_nested_object_ref(self, client: Sink) -> None:
        with client.pagination_tests.refs.with_streaming_response.nested_object_ref() as response:
            assert not response.is_closed

            ref = response.parse()
            assert_matches_type(SyncPageCursorNestedObjectRef[MyModel], ref, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_with_shared_model_ref(self, client: Sink) -> None:
        ref = client.pagination_tests.refs.with_shared_model_ref()
        assert_matches_type(SyncPageCursorSharedRef[MyModel], ref, path=["response"])

    @parametrize
    def test_method_with_shared_model_ref_with_all_params(self, client: Sink) -> None:
        ref = client.pagination_tests.refs.with_shared_model_ref(
            cursor="cursor",
            limit=0,
        )
        assert_matches_type(SyncPageCursorSharedRef[MyModel], ref, path=["response"])

    @parametrize
    def test_raw_response_with_shared_model_ref(self, client: Sink) -> None:
        response = client.pagination_tests.refs.with_raw_response.with_shared_model_ref()

        assert response.is_closed is True
        ref = response.parse()
        assert_matches_type(SyncPageCursorSharedRef[MyModel], ref, path=["response"])

    @parametrize
    def test_streaming_response_with_shared_model_ref(self, client: Sink) -> None:
        with client.pagination_tests.refs.with_streaming_response.with_shared_model_ref() as response:
            assert not response.is_closed

            ref = response.parse()
            assert_matches_type(SyncPageCursorSharedRef[MyModel], ref, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncRefs:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_nested_object_ref(self, async_client: AsyncSink) -> None:
        ref = await async_client.pagination_tests.refs.nested_object_ref()
        assert_matches_type(AsyncPageCursorNestedObjectRef[MyModel], ref, path=["response"])

    @parametrize
    async def test_method_nested_object_ref_with_all_params(self, async_client: AsyncSink) -> None:
        ref = await async_client.pagination_tests.refs.nested_object_ref(
            cursor="cursor",
            limit=0,
            object_param={"foo": "foo"},
        )
        assert_matches_type(AsyncPageCursorNestedObjectRef[MyModel], ref, path=["response"])

    @parametrize
    async def test_raw_response_nested_object_ref(self, async_client: AsyncSink) -> None:
        response = await async_client.pagination_tests.refs.with_raw_response.nested_object_ref()

        assert response.is_closed is True
        ref = response.parse()
        assert_matches_type(AsyncPageCursorNestedObjectRef[MyModel], ref, path=["response"])

    @parametrize
    async def test_streaming_response_nested_object_ref(self, async_client: AsyncSink) -> None:
        async with async_client.pagination_tests.refs.with_streaming_response.nested_object_ref() as response:
            assert not response.is_closed

            ref = await response.parse()
            assert_matches_type(AsyncPageCursorNestedObjectRef[MyModel], ref, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_with_shared_model_ref(self, async_client: AsyncSink) -> None:
        ref = await async_client.pagination_tests.refs.with_shared_model_ref()
        assert_matches_type(AsyncPageCursorSharedRef[MyModel], ref, path=["response"])

    @parametrize
    async def test_method_with_shared_model_ref_with_all_params(self, async_client: AsyncSink) -> None:
        ref = await async_client.pagination_tests.refs.with_shared_model_ref(
            cursor="cursor",
            limit=0,
        )
        assert_matches_type(AsyncPageCursorSharedRef[MyModel], ref, path=["response"])

    @parametrize
    async def test_raw_response_with_shared_model_ref(self, async_client: AsyncSink) -> None:
        response = await async_client.pagination_tests.refs.with_raw_response.with_shared_model_ref()

        assert response.is_closed is True
        ref = response.parse()
        assert_matches_type(AsyncPageCursorSharedRef[MyModel], ref, path=["response"])

    @parametrize
    async def test_streaming_response_with_shared_model_ref(self, async_client: AsyncSink) -> None:
        async with async_client.pagination_tests.refs.with_streaming_response.with_shared_model_ref() as response:
            assert not response.is_closed

            ref = await response.parse()
            assert_matches_type(AsyncPageCursorSharedRef[MyModel], ref, path=["response"])

        assert cast(Any, response.is_closed) is True
