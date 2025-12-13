# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestObjects:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism crashes on this - https://github.com/stoplightio/prism/issues/2375")
    @parametrize
    def test_method_missing_items(self, client: Sink) -> None:
        object_ = client.invalid_schemas.objects.missing_items()
        assert_matches_type(object, object_, path=["response"])

    @pytest.mark.skip(reason="Prism crashes on this - https://github.com/stoplightio/prism/issues/2375")
    @parametrize
    def test_raw_response_missing_items(self, client: Sink) -> None:
        response = client.invalid_schemas.objects.with_raw_response.missing_items()

        assert response.is_closed is True
        object_ = response.parse()
        assert_matches_type(object, object_, path=["response"])

    @pytest.mark.skip(reason="Prism crashes on this - https://github.com/stoplightio/prism/issues/2375")
    @parametrize
    def test_streaming_response_missing_items(self, client: Sink) -> None:
        with client.invalid_schemas.objects.with_streaming_response.missing_items() as response:
            assert not response.is_closed

            object_ = response.parse()
            assert_matches_type(object, object_, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncObjects:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism crashes on this - https://github.com/stoplightio/prism/issues/2375")
    @parametrize
    async def test_method_missing_items(self, async_client: AsyncSink) -> None:
        object_ = await async_client.invalid_schemas.objects.missing_items()
        assert_matches_type(object, object_, path=["response"])

    @pytest.mark.skip(reason="Prism crashes on this - https://github.com/stoplightio/prism/issues/2375")
    @parametrize
    async def test_raw_response_missing_items(self, async_client: AsyncSink) -> None:
        response = await async_client.invalid_schemas.objects.with_raw_response.missing_items()

        assert response.is_closed is True
        object_ = response.parse()
        assert_matches_type(object, object_, path=["response"])

    @pytest.mark.skip(reason="Prism crashes on this - https://github.com/stoplightio/prism/issues/2375")
    @parametrize
    async def test_streaming_response_missing_items(self, async_client: AsyncSink) -> None:
        async with async_client.invalid_schemas.objects.with_streaming_response.missing_items() as response:
            assert not response.is_closed

            object_ = await response.parse()
            assert_matches_type(object, object_, path=["response"])

        assert cast(Any, response.is_closed) is True
