# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.pagination import SyncFakePage, AsyncFakePage
from sink.api.sdk.types.shared import SimpleObject

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFakePages:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Sink) -> None:
        fake_page = client.pagination_tests.fake_pages.list(
            my_fake_page_param="my_fake_page_param",
        )
        assert_matches_type(SyncFakePage[SimpleObject], fake_page, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Sink) -> None:
        response = client.pagination_tests.fake_pages.with_raw_response.list(
            my_fake_page_param="my_fake_page_param",
        )

        assert response.is_closed is True
        fake_page = response.parse()
        assert_matches_type(SyncFakePage[SimpleObject], fake_page, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Sink) -> None:
        with client.pagination_tests.fake_pages.with_streaming_response.list(
            my_fake_page_param="my_fake_page_param",
        ) as response:
            assert not response.is_closed

            fake_page = response.parse()
            assert_matches_type(SyncFakePage[SimpleObject], fake_page, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncFakePages:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_list(self, async_client: AsyncSink) -> None:
        fake_page = await async_client.pagination_tests.fake_pages.list(
            my_fake_page_param="my_fake_page_param",
        )
        assert_matches_type(AsyncFakePage[SimpleObject], fake_page, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSink) -> None:
        response = await async_client.pagination_tests.fake_pages.with_raw_response.list(
            my_fake_page_param="my_fake_page_param",
        )

        assert response.is_closed is True
        fake_page = response.parse()
        assert_matches_type(AsyncFakePage[SimpleObject], fake_page, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSink) -> None:
        async with async_client.pagination_tests.fake_pages.with_streaming_response.list(
            my_fake_page_param="my_fake_page_param",
        ) as response:
            assert not response.is_closed

            fake_page = await response.parse()
            assert_matches_type(AsyncFakePage[SimpleObject], fake_page, path=["response"])

        assert cast(Any, response.is_closed) is True
