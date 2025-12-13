# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.types import MapUnknownItemsResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMaps:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_unknown_items(self, client: Sink) -> None:
        map = client.types.maps.unknown_items(
            any_map={"foo": "bar"},
            unknown_map={"foo": "bar"},
            unspecified_type_object_map={"foo": {}},
        )
        assert_matches_type(MapUnknownItemsResponse, map, path=["response"])

    @parametrize
    def test_raw_response_unknown_items(self, client: Sink) -> None:
        response = client.types.maps.with_raw_response.unknown_items(
            any_map={"foo": "bar"},
            unknown_map={"foo": "bar"},
            unspecified_type_object_map={"foo": {}},
        )

        assert response.is_closed is True
        map = response.parse()
        assert_matches_type(MapUnknownItemsResponse, map, path=["response"])

    @parametrize
    def test_streaming_response_unknown_items(self, client: Sink) -> None:
        with client.types.maps.with_streaming_response.unknown_items(
            any_map={"foo": "bar"},
            unknown_map={"foo": "bar"},
            unspecified_type_object_map={"foo": {}},
        ) as response:
            assert not response.is_closed

            map = response.parse()
            assert_matches_type(MapUnknownItemsResponse, map, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncMaps:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_unknown_items(self, async_client: AsyncSink) -> None:
        map = await async_client.types.maps.unknown_items(
            any_map={"foo": "bar"},
            unknown_map={"foo": "bar"},
            unspecified_type_object_map={"foo": {}},
        )
        assert_matches_type(MapUnknownItemsResponse, map, path=["response"])

    @parametrize
    async def test_raw_response_unknown_items(self, async_client: AsyncSink) -> None:
        response = await async_client.types.maps.with_raw_response.unknown_items(
            any_map={"foo": "bar"},
            unknown_map={"foo": "bar"},
            unspecified_type_object_map={"foo": {}},
        )

        assert response.is_closed is True
        map = response.parse()
        assert_matches_type(MapUnknownItemsResponse, map, path=["response"])

    @parametrize
    async def test_streaming_response_unknown_items(self, async_client: AsyncSink) -> None:
        async with async_client.types.maps.with_streaming_response.unknown_items(
            any_map={"foo": "bar"},
            unknown_map={"foo": "bar"},
            unspecified_type_object_map={"foo": {}},
        ) as response:
            assert not response.is_closed

            map = await response.parse()
            assert_matches_type(MapUnknownItemsResponse, map, path=["response"])

        assert cast(Any, response.is_closed) is True
