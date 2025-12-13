# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.shared import BasicSharedModelObject

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDuplicates:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_body_and_path(self, client: Sink) -> None:
        duplicate = client.mixed_params.duplicates.body_and_path(
            path_id="id",
            body_id="id",
        )
        assert_matches_type(BasicSharedModelObject, duplicate, path=["response"])

    @parametrize
    def test_raw_response_body_and_path(self, client: Sink) -> None:
        response = client.mixed_params.duplicates.with_raw_response.body_and_path(
            path_id="id",
            body_id="id",
        )

        assert response.is_closed is True
        duplicate = response.parse()
        assert_matches_type(BasicSharedModelObject, duplicate, path=["response"])

    @parametrize
    def test_streaming_response_body_and_path(self, client: Sink) -> None:
        with client.mixed_params.duplicates.with_streaming_response.body_and_path(
            path_id="id",
            body_id="id",
        ) as response:
            assert not response.is_closed

            duplicate = response.parse()
            assert_matches_type(BasicSharedModelObject, duplicate, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_body_and_path(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_id` but received ''"):
            client.mixed_params.duplicates.with_raw_response.body_and_path(
                path_id="",
                body_id="id",
            )

    @parametrize
    def test_method_query_and_body(self, client: Sink) -> None:
        duplicate = client.mixed_params.duplicates.query_and_body(
            query_id="id",
            body_id="id",
        )
        assert_matches_type(BasicSharedModelObject, duplicate, path=["response"])

    @parametrize
    def test_raw_response_query_and_body(self, client: Sink) -> None:
        response = client.mixed_params.duplicates.with_raw_response.query_and_body(
            query_id="id",
            body_id="id",
        )

        assert response.is_closed is True
        duplicate = response.parse()
        assert_matches_type(BasicSharedModelObject, duplicate, path=["response"])

    @parametrize
    def test_streaming_response_query_and_body(self, client: Sink) -> None:
        with client.mixed_params.duplicates.with_streaming_response.query_and_body(
            query_id="id",
            body_id="id",
        ) as response:
            assert not response.is_closed

            duplicate = response.parse()
            assert_matches_type(BasicSharedModelObject, duplicate, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_query_and_body_different_casing(self, client: Sink) -> None:
        duplicate = client.mixed_params.duplicates.query_and_body_different_casing(
            query_correlation_id="correlation-id",
            body_correlation_id="correlation_id",
        )
        assert_matches_type(BasicSharedModelObject, duplicate, path=["response"])

    @parametrize
    def test_raw_response_query_and_body_different_casing(self, client: Sink) -> None:
        response = client.mixed_params.duplicates.with_raw_response.query_and_body_different_casing(
            query_correlation_id="correlation-id",
            body_correlation_id="correlation_id",
        )

        assert response.is_closed is True
        duplicate = response.parse()
        assert_matches_type(BasicSharedModelObject, duplicate, path=["response"])

    @parametrize
    def test_streaming_response_query_and_body_different_casing(self, client: Sink) -> None:
        with client.mixed_params.duplicates.with_streaming_response.query_and_body_different_casing(
            query_correlation_id="correlation-id",
            body_correlation_id="correlation_id",
        ) as response:
            assert not response.is_closed

            duplicate = response.parse()
            assert_matches_type(BasicSharedModelObject, duplicate, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_query_and_path(self, client: Sink) -> None:
        duplicate = client.mixed_params.duplicates.query_and_path(
            path_id="id",
            query_id="id",
        )
        assert_matches_type(BasicSharedModelObject, duplicate, path=["response"])

    @parametrize
    def test_raw_response_query_and_path(self, client: Sink) -> None:
        response = client.mixed_params.duplicates.with_raw_response.query_and_path(
            path_id="id",
            query_id="id",
        )

        assert response.is_closed is True
        duplicate = response.parse()
        assert_matches_type(BasicSharedModelObject, duplicate, path=["response"])

    @parametrize
    def test_streaming_response_query_and_path(self, client: Sink) -> None:
        with client.mixed_params.duplicates.with_streaming_response.query_and_path(
            path_id="id",
            query_id="id",
        ) as response:
            assert not response.is_closed

            duplicate = response.parse()
            assert_matches_type(BasicSharedModelObject, duplicate, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_query_and_path(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_id` but received ''"):
            client.mixed_params.duplicates.with_raw_response.query_and_path(
                path_id="",
                query_id="id",
            )


class TestAsyncDuplicates:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_body_and_path(self, async_client: AsyncSink) -> None:
        duplicate = await async_client.mixed_params.duplicates.body_and_path(
            path_id="id",
            body_id="id",
        )
        assert_matches_type(BasicSharedModelObject, duplicate, path=["response"])

    @parametrize
    async def test_raw_response_body_and_path(self, async_client: AsyncSink) -> None:
        response = await async_client.mixed_params.duplicates.with_raw_response.body_and_path(
            path_id="id",
            body_id="id",
        )

        assert response.is_closed is True
        duplicate = response.parse()
        assert_matches_type(BasicSharedModelObject, duplicate, path=["response"])

    @parametrize
    async def test_streaming_response_body_and_path(self, async_client: AsyncSink) -> None:
        async with async_client.mixed_params.duplicates.with_streaming_response.body_and_path(
            path_id="id",
            body_id="id",
        ) as response:
            assert not response.is_closed

            duplicate = await response.parse()
            assert_matches_type(BasicSharedModelObject, duplicate, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_body_and_path(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_id` but received ''"):
            await async_client.mixed_params.duplicates.with_raw_response.body_and_path(
                path_id="",
                body_id="id",
            )

    @parametrize
    async def test_method_query_and_body(self, async_client: AsyncSink) -> None:
        duplicate = await async_client.mixed_params.duplicates.query_and_body(
            query_id="id",
            body_id="id",
        )
        assert_matches_type(BasicSharedModelObject, duplicate, path=["response"])

    @parametrize
    async def test_raw_response_query_and_body(self, async_client: AsyncSink) -> None:
        response = await async_client.mixed_params.duplicates.with_raw_response.query_and_body(
            query_id="id",
            body_id="id",
        )

        assert response.is_closed is True
        duplicate = response.parse()
        assert_matches_type(BasicSharedModelObject, duplicate, path=["response"])

    @parametrize
    async def test_streaming_response_query_and_body(self, async_client: AsyncSink) -> None:
        async with async_client.mixed_params.duplicates.with_streaming_response.query_and_body(
            query_id="id",
            body_id="id",
        ) as response:
            assert not response.is_closed

            duplicate = await response.parse()
            assert_matches_type(BasicSharedModelObject, duplicate, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_query_and_body_different_casing(self, async_client: AsyncSink) -> None:
        duplicate = await async_client.mixed_params.duplicates.query_and_body_different_casing(
            query_correlation_id="correlation-id",
            body_correlation_id="correlation_id",
        )
        assert_matches_type(BasicSharedModelObject, duplicate, path=["response"])

    @parametrize
    async def test_raw_response_query_and_body_different_casing(self, async_client: AsyncSink) -> None:
        response = await async_client.mixed_params.duplicates.with_raw_response.query_and_body_different_casing(
            query_correlation_id="correlation-id",
            body_correlation_id="correlation_id",
        )

        assert response.is_closed is True
        duplicate = response.parse()
        assert_matches_type(BasicSharedModelObject, duplicate, path=["response"])

    @parametrize
    async def test_streaming_response_query_and_body_different_casing(self, async_client: AsyncSink) -> None:
        async with async_client.mixed_params.duplicates.with_streaming_response.query_and_body_different_casing(
            query_correlation_id="correlation-id",
            body_correlation_id="correlation_id",
        ) as response:
            assert not response.is_closed

            duplicate = await response.parse()
            assert_matches_type(BasicSharedModelObject, duplicate, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_query_and_path(self, async_client: AsyncSink) -> None:
        duplicate = await async_client.mixed_params.duplicates.query_and_path(
            path_id="id",
            query_id="id",
        )
        assert_matches_type(BasicSharedModelObject, duplicate, path=["response"])

    @parametrize
    async def test_raw_response_query_and_path(self, async_client: AsyncSink) -> None:
        response = await async_client.mixed_params.duplicates.with_raw_response.query_and_path(
            path_id="id",
            query_id="id",
        )

        assert response.is_closed is True
        duplicate = response.parse()
        assert_matches_type(BasicSharedModelObject, duplicate, path=["response"])

    @parametrize
    async def test_streaming_response_query_and_path(self, async_client: AsyncSink) -> None:
        async with async_client.mixed_params.duplicates.with_streaming_response.query_and_path(
            path_id="id",
            query_id="id",
        ) as response:
            assert not response.is_closed

            duplicate = await response.parse()
            assert_matches_type(BasicSharedModelObject, duplicate, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_query_and_path(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_id` but received ''"):
            await async_client.mixed_params.duplicates.with_raw_response.query_and_path(
                path_id="",
                query_id="id",
            )
