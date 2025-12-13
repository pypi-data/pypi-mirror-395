# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import MyModel
from sink.api.sdk.pagination import (
    SyncPagePageNumber,
    AsyncPagePageNumber,
    SyncPagePageNumberWithoutCurrentPageResponse,
    AsyncPagePageNumberWithoutCurrentPageResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPageNumberWithoutCurrentPageResponse:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Sink) -> None:
        page_number_without_current_page_response = (
            client.pagination_tests.page_number_without_current_page_response.list()
        )
        assert_matches_type(SyncPagePageNumber[MyModel], page_number_without_current_page_response, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Sink) -> None:
        page_number_without_current_page_response = (
            client.pagination_tests.page_number_without_current_page_response.list(
                page=0,
                page_size=0,
            )
        )
        assert_matches_type(SyncPagePageNumber[MyModel], page_number_without_current_page_response, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Sink) -> None:
        response = client.pagination_tests.page_number_without_current_page_response.with_raw_response.list()

        assert response.is_closed is True
        page_number_without_current_page_response = response.parse()
        assert_matches_type(SyncPagePageNumber[MyModel], page_number_without_current_page_response, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Sink) -> None:
        with (
            client.pagination_tests.page_number_without_current_page_response.with_streaming_response.list()
        ) as response:
            assert not response.is_closed

            page_number_without_current_page_response = response.parse()
            assert_matches_type(
                SyncPagePageNumber[MyModel], page_number_without_current_page_response, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list_without_current_page_response(self, client: Sink) -> None:
        page_number_without_current_page_response = (
            client.pagination_tests.page_number_without_current_page_response.list_without_current_page_response()
        )
        assert_matches_type(
            SyncPagePageNumberWithoutCurrentPageResponse[MyModel],
            page_number_without_current_page_response,
            path=["response"],
        )

    @parametrize
    def test_method_list_without_current_page_response_with_all_params(self, client: Sink) -> None:
        page_number_without_current_page_response = (
            client.pagination_tests.page_number_without_current_page_response.list_without_current_page_response(
                page=0,
                page_size=0,
                prop_to_not_mess_with_infer_for_other_pages=True,
            )
        )
        assert_matches_type(
            SyncPagePageNumberWithoutCurrentPageResponse[MyModel],
            page_number_without_current_page_response,
            path=["response"],
        )

    @parametrize
    def test_raw_response_list_without_current_page_response(self, client: Sink) -> None:
        response = client.pagination_tests.page_number_without_current_page_response.with_raw_response.list_without_current_page_response()

        assert response.is_closed is True
        page_number_without_current_page_response = response.parse()
        assert_matches_type(
            SyncPagePageNumberWithoutCurrentPageResponse[MyModel],
            page_number_without_current_page_response,
            path=["response"],
        )

    @parametrize
    def test_streaming_response_list_without_current_page_response(self, client: Sink) -> None:
        with client.pagination_tests.page_number_without_current_page_response.with_streaming_response.list_without_current_page_response() as response:
            assert not response.is_closed

            page_number_without_current_page_response = response.parse()
            assert_matches_type(
                SyncPagePageNumberWithoutCurrentPageResponse[MyModel],
                page_number_without_current_page_response,
                path=["response"],
            )

        assert cast(Any, response.is_closed) is True


class TestAsyncPageNumberWithoutCurrentPageResponse:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_list(self, async_client: AsyncSink) -> None:
        page_number_without_current_page_response = (
            await async_client.pagination_tests.page_number_without_current_page_response.list()
        )
        assert_matches_type(AsyncPagePageNumber[MyModel], page_number_without_current_page_response, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSink) -> None:
        page_number_without_current_page_response = (
            await async_client.pagination_tests.page_number_without_current_page_response.list(
                page=0,
                page_size=0,
            )
        )
        assert_matches_type(AsyncPagePageNumber[MyModel], page_number_without_current_page_response, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSink) -> None:
        response = (
            await async_client.pagination_tests.page_number_without_current_page_response.with_raw_response.list()
        )

        assert response.is_closed is True
        page_number_without_current_page_response = response.parse()
        assert_matches_type(AsyncPagePageNumber[MyModel], page_number_without_current_page_response, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSink) -> None:
        async with (
            async_client.pagination_tests.page_number_without_current_page_response.with_streaming_response.list()
        ) as response:
            assert not response.is_closed

            page_number_without_current_page_response = await response.parse()
            assert_matches_type(
                AsyncPagePageNumber[MyModel], page_number_without_current_page_response, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list_without_current_page_response(self, async_client: AsyncSink) -> None:
        page_number_without_current_page_response = await async_client.pagination_tests.page_number_without_current_page_response.list_without_current_page_response()
        assert_matches_type(
            AsyncPagePageNumberWithoutCurrentPageResponse[MyModel],
            page_number_without_current_page_response,
            path=["response"],
        )

    @parametrize
    async def test_method_list_without_current_page_response_with_all_params(self, async_client: AsyncSink) -> None:
        page_number_without_current_page_response = await async_client.pagination_tests.page_number_without_current_page_response.list_without_current_page_response(
            page=0,
            page_size=0,
            prop_to_not_mess_with_infer_for_other_pages=True,
        )
        assert_matches_type(
            AsyncPagePageNumberWithoutCurrentPageResponse[MyModel],
            page_number_without_current_page_response,
            path=["response"],
        )

    @parametrize
    async def test_raw_response_list_without_current_page_response(self, async_client: AsyncSink) -> None:
        response = await async_client.pagination_tests.page_number_without_current_page_response.with_raw_response.list_without_current_page_response()

        assert response.is_closed is True
        page_number_without_current_page_response = response.parse()
        assert_matches_type(
            AsyncPagePageNumberWithoutCurrentPageResponse[MyModel],
            page_number_without_current_page_response,
            path=["response"],
        )

    @parametrize
    async def test_streaming_response_list_without_current_page_response(self, async_client: AsyncSink) -> None:
        async with async_client.pagination_tests.page_number_without_current_page_response.with_streaming_response.list_without_current_page_response() as response:
            assert not response.is_closed

            page_number_without_current_page_response = await response.parse()
            assert_matches_type(
                AsyncPagePageNumberWithoutCurrentPageResponse[MyModel],
                page_number_without_current_page_response,
                path=["response"],
            )

        assert cast(Any, response.is_closed) is True
