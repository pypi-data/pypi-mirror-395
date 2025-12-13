# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.shared import BasicSharedModelObject

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMixedParams:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_body_with_top_level_one_of_and_path_overload_1(self, client: Sink) -> None:
        mixed_param = client.mixed_params.body_with_top_level_one_of_and_path(
            path_param="path_param",
            kind="VIRTUAL",
        )
        assert mixed_param is None

    @parametrize
    def test_raw_response_body_with_top_level_one_of_and_path_overload_1(self, client: Sink) -> None:
        response = client.mixed_params.with_raw_response.body_with_top_level_one_of_and_path(
            path_param="path_param",
            kind="VIRTUAL",
        )

        assert response.is_closed is True
        mixed_param = response.parse()
        assert mixed_param is None

    @parametrize
    def test_streaming_response_body_with_top_level_one_of_and_path_overload_1(self, client: Sink) -> None:
        with client.mixed_params.with_streaming_response.body_with_top_level_one_of_and_path(
            path_param="path_param",
            kind="VIRTUAL",
        ) as response:
            assert not response.is_closed

            mixed_param = response.parse()
            assert mixed_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_body_with_top_level_one_of_and_path_overload_1(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_param` but received ''"):
            client.mixed_params.with_raw_response.body_with_top_level_one_of_and_path(
                path_param="",
                kind="VIRTUAL",
            )

    @parametrize
    def test_method_body_with_top_level_one_of_and_path_overload_2(self, client: Sink) -> None:
        mixed_param = client.mixed_params.body_with_top_level_one_of_and_path(
            path_param="path_param",
            bar="bar",
            foo="foo",
        )
        assert mixed_param is None

    @parametrize
    def test_raw_response_body_with_top_level_one_of_and_path_overload_2(self, client: Sink) -> None:
        response = client.mixed_params.with_raw_response.body_with_top_level_one_of_and_path(
            path_param="path_param",
            bar="bar",
            foo="foo",
        )

        assert response.is_closed is True
        mixed_param = response.parse()
        assert mixed_param is None

    @parametrize
    def test_streaming_response_body_with_top_level_one_of_and_path_overload_2(self, client: Sink) -> None:
        with client.mixed_params.with_streaming_response.body_with_top_level_one_of_and_path(
            path_param="path_param",
            bar="bar",
            foo="foo",
        ) as response:
            assert not response.is_closed

            mixed_param = response.parse()
            assert mixed_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_body_with_top_level_one_of_and_path_overload_2(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_param` but received ''"):
            client.mixed_params.with_raw_response.body_with_top_level_one_of_and_path(
                path_param="",
                bar="bar",
                foo="foo",
            )

    @parametrize
    def test_method_query_and_body(self, client: Sink) -> None:
        mixed_param = client.mixed_params.query_and_body()
        assert_matches_type(BasicSharedModelObject, mixed_param, path=["response"])

    @parametrize
    def test_method_query_and_body_with_all_params(self, client: Sink) -> None:
        mixed_param = client.mixed_params.query_and_body(
            query_param="query_param",
            body_param="body_param",
        )
        assert_matches_type(BasicSharedModelObject, mixed_param, path=["response"])

    @parametrize
    def test_raw_response_query_and_body(self, client: Sink) -> None:
        response = client.mixed_params.with_raw_response.query_and_body()

        assert response.is_closed is True
        mixed_param = response.parse()
        assert_matches_type(BasicSharedModelObject, mixed_param, path=["response"])

    @parametrize
    def test_streaming_response_query_and_body(self, client: Sink) -> None:
        with client.mixed_params.with_streaming_response.query_and_body() as response:
            assert not response.is_closed

            mixed_param = response.parse()
            assert_matches_type(BasicSharedModelObject, mixed_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_query_body_and_path(self, client: Sink) -> None:
        mixed_param = client.mixed_params.query_body_and_path(
            path_param="path_param",
        )
        assert_matches_type(BasicSharedModelObject, mixed_param, path=["response"])

    @parametrize
    def test_method_query_body_and_path_with_all_params(self, client: Sink) -> None:
        mixed_param = client.mixed_params.query_body_and_path(
            path_param="path_param",
            query_param="query_param",
            body_param="body_param",
        )
        assert_matches_type(BasicSharedModelObject, mixed_param, path=["response"])

    @parametrize
    def test_raw_response_query_body_and_path(self, client: Sink) -> None:
        response = client.mixed_params.with_raw_response.query_body_and_path(
            path_param="path_param",
        )

        assert response.is_closed is True
        mixed_param = response.parse()
        assert_matches_type(BasicSharedModelObject, mixed_param, path=["response"])

    @parametrize
    def test_streaming_response_query_body_and_path(self, client: Sink) -> None:
        with client.mixed_params.with_streaming_response.query_body_and_path(
            path_param="path_param",
        ) as response:
            assert not response.is_closed

            mixed_param = response.parse()
            assert_matches_type(BasicSharedModelObject, mixed_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_query_body_and_path(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_param` but received ''"):
            client.mixed_params.with_raw_response.query_body_and_path(
                path_param="",
            )


class TestAsyncMixedParams:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_body_with_top_level_one_of_and_path_overload_1(self, async_client: AsyncSink) -> None:
        mixed_param = await async_client.mixed_params.body_with_top_level_one_of_and_path(
            path_param="path_param",
            kind="VIRTUAL",
        )
        assert mixed_param is None

    @parametrize
    async def test_raw_response_body_with_top_level_one_of_and_path_overload_1(self, async_client: AsyncSink) -> None:
        response = await async_client.mixed_params.with_raw_response.body_with_top_level_one_of_and_path(
            path_param="path_param",
            kind="VIRTUAL",
        )

        assert response.is_closed is True
        mixed_param = response.parse()
        assert mixed_param is None

    @parametrize
    async def test_streaming_response_body_with_top_level_one_of_and_path_overload_1(
        self, async_client: AsyncSink
    ) -> None:
        async with async_client.mixed_params.with_streaming_response.body_with_top_level_one_of_and_path(
            path_param="path_param",
            kind="VIRTUAL",
        ) as response:
            assert not response.is_closed

            mixed_param = await response.parse()
            assert mixed_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_body_with_top_level_one_of_and_path_overload_1(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_param` but received ''"):
            await async_client.mixed_params.with_raw_response.body_with_top_level_one_of_and_path(
                path_param="",
                kind="VIRTUAL",
            )

    @parametrize
    async def test_method_body_with_top_level_one_of_and_path_overload_2(self, async_client: AsyncSink) -> None:
        mixed_param = await async_client.mixed_params.body_with_top_level_one_of_and_path(
            path_param="path_param",
            bar="bar",
            foo="foo",
        )
        assert mixed_param is None

    @parametrize
    async def test_raw_response_body_with_top_level_one_of_and_path_overload_2(self, async_client: AsyncSink) -> None:
        response = await async_client.mixed_params.with_raw_response.body_with_top_level_one_of_and_path(
            path_param="path_param",
            bar="bar",
            foo="foo",
        )

        assert response.is_closed is True
        mixed_param = response.parse()
        assert mixed_param is None

    @parametrize
    async def test_streaming_response_body_with_top_level_one_of_and_path_overload_2(
        self, async_client: AsyncSink
    ) -> None:
        async with async_client.mixed_params.with_streaming_response.body_with_top_level_one_of_and_path(
            path_param="path_param",
            bar="bar",
            foo="foo",
        ) as response:
            assert not response.is_closed

            mixed_param = await response.parse()
            assert mixed_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_body_with_top_level_one_of_and_path_overload_2(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_param` but received ''"):
            await async_client.mixed_params.with_raw_response.body_with_top_level_one_of_and_path(
                path_param="",
                bar="bar",
                foo="foo",
            )

    @parametrize
    async def test_method_query_and_body(self, async_client: AsyncSink) -> None:
        mixed_param = await async_client.mixed_params.query_and_body()
        assert_matches_type(BasicSharedModelObject, mixed_param, path=["response"])

    @parametrize
    async def test_method_query_and_body_with_all_params(self, async_client: AsyncSink) -> None:
        mixed_param = await async_client.mixed_params.query_and_body(
            query_param="query_param",
            body_param="body_param",
        )
        assert_matches_type(BasicSharedModelObject, mixed_param, path=["response"])

    @parametrize
    async def test_raw_response_query_and_body(self, async_client: AsyncSink) -> None:
        response = await async_client.mixed_params.with_raw_response.query_and_body()

        assert response.is_closed is True
        mixed_param = response.parse()
        assert_matches_type(BasicSharedModelObject, mixed_param, path=["response"])

    @parametrize
    async def test_streaming_response_query_and_body(self, async_client: AsyncSink) -> None:
        async with async_client.mixed_params.with_streaming_response.query_and_body() as response:
            assert not response.is_closed

            mixed_param = await response.parse()
            assert_matches_type(BasicSharedModelObject, mixed_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_query_body_and_path(self, async_client: AsyncSink) -> None:
        mixed_param = await async_client.mixed_params.query_body_and_path(
            path_param="path_param",
        )
        assert_matches_type(BasicSharedModelObject, mixed_param, path=["response"])

    @parametrize
    async def test_method_query_body_and_path_with_all_params(self, async_client: AsyncSink) -> None:
        mixed_param = await async_client.mixed_params.query_body_and_path(
            path_param="path_param",
            query_param="query_param",
            body_param="body_param",
        )
        assert_matches_type(BasicSharedModelObject, mixed_param, path=["response"])

    @parametrize
    async def test_raw_response_query_body_and_path(self, async_client: AsyncSink) -> None:
        response = await async_client.mixed_params.with_raw_response.query_body_and_path(
            path_param="path_param",
        )

        assert response.is_closed is True
        mixed_param = response.parse()
        assert_matches_type(BasicSharedModelObject, mixed_param, path=["response"])

    @parametrize
    async def test_streaming_response_query_body_and_path(self, async_client: AsyncSink) -> None:
        async with async_client.mixed_params.with_streaming_response.query_body_and_path(
            path_param="path_param",
        ) as response:
            assert not response.is_closed

            mixed_param = await response.parse()
            assert_matches_type(BasicSharedModelObject, mixed_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_query_body_and_path(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_param` but received ''"):
            await async_client.mixed_params.with_raw_response.query_body_and_path(
                path_param="",
            )
