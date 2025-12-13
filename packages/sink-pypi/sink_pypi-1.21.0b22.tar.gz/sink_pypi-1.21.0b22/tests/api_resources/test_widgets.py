# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import Widget

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestWidgets:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve_with_filter(self, client: Sink) -> None:
        widget = client.widgets.retrieve_with_filter(
            filter_type="available",
            widget_id=0,
        )
        assert_matches_type(Widget, widget, path=["response"])

    @parametrize
    def test_raw_response_retrieve_with_filter(self, client: Sink) -> None:
        response = client.widgets.with_raw_response.retrieve_with_filter(
            filter_type="available",
            widget_id=0,
        )

        assert response.is_closed is True
        widget = response.parse()
        assert_matches_type(Widget, widget, path=["response"])

    @parametrize
    def test_streaming_response_retrieve_with_filter(self, client: Sink) -> None:
        with client.widgets.with_streaming_response.retrieve_with_filter(
            filter_type="available",
            widget_id=0,
        ) as response:
            assert not response.is_closed

            widget = response.parse()
            assert_matches_type(Widget, widget, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncWidgets:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve_with_filter(self, async_client: AsyncSink) -> None:
        widget = await async_client.widgets.retrieve_with_filter(
            filter_type="available",
            widget_id=0,
        )
        assert_matches_type(Widget, widget, path=["response"])

    @parametrize
    async def test_raw_response_retrieve_with_filter(self, async_client: AsyncSink) -> None:
        response = await async_client.widgets.with_raw_response.retrieve_with_filter(
            filter_type="available",
            widget_id=0,
        )

        assert response.is_closed is True
        widget = response.parse()
        assert_matches_type(Widget, widget, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve_with_filter(self, async_client: AsyncSink) -> None:
        async with async_client.widgets.with_streaming_response.retrieve_with_filter(
            filter_type="available",
            widget_id=0,
        ) as response:
            assert not response.is_closed

            widget = await response.parse()
            assert_matches_type(Widget, widget, path=["response"])

        assert cast(Any, response.is_closed) is True
