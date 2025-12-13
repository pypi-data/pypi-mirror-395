# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import MakeAmbiguousSchemasLooserMakeAmbiguousSchemasLooserResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMakeAmbiguousSchemasLooser:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_make_ambiguous_schemas_looser(self, client: Sink) -> None:
        make_ambiguous_schemas_looser = client.make_ambiguous_schemas_looser.make_ambiguous_schemas_looser()
        assert_matches_type(
            MakeAmbiguousSchemasLooserMakeAmbiguousSchemasLooserResponse,
            make_ambiguous_schemas_looser,
            path=["response"],
        )

    @parametrize
    def test_raw_response_make_ambiguous_schemas_looser(self, client: Sink) -> None:
        response = client.make_ambiguous_schemas_looser.with_raw_response.make_ambiguous_schemas_looser()

        assert response.is_closed is True
        make_ambiguous_schemas_looser = response.parse()
        assert_matches_type(
            MakeAmbiguousSchemasLooserMakeAmbiguousSchemasLooserResponse,
            make_ambiguous_schemas_looser,
            path=["response"],
        )

    @parametrize
    def test_streaming_response_make_ambiguous_schemas_looser(self, client: Sink) -> None:
        with client.make_ambiguous_schemas_looser.with_streaming_response.make_ambiguous_schemas_looser() as response:
            assert not response.is_closed

            make_ambiguous_schemas_looser = response.parse()
            assert_matches_type(
                MakeAmbiguousSchemasLooserMakeAmbiguousSchemasLooserResponse,
                make_ambiguous_schemas_looser,
                path=["response"],
            )

        assert cast(Any, response.is_closed) is True


class TestAsyncMakeAmbiguousSchemasLooser:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_make_ambiguous_schemas_looser(self, async_client: AsyncSink) -> None:
        make_ambiguous_schemas_looser = await async_client.make_ambiguous_schemas_looser.make_ambiguous_schemas_looser()
        assert_matches_type(
            MakeAmbiguousSchemasLooserMakeAmbiguousSchemasLooserResponse,
            make_ambiguous_schemas_looser,
            path=["response"],
        )

    @parametrize
    async def test_raw_response_make_ambiguous_schemas_looser(self, async_client: AsyncSink) -> None:
        response = await async_client.make_ambiguous_schemas_looser.with_raw_response.make_ambiguous_schemas_looser()

        assert response.is_closed is True
        make_ambiguous_schemas_looser = response.parse()
        assert_matches_type(
            MakeAmbiguousSchemasLooserMakeAmbiguousSchemasLooserResponse,
            make_ambiguous_schemas_looser,
            path=["response"],
        )

    @parametrize
    async def test_streaming_response_make_ambiguous_schemas_looser(self, async_client: AsyncSink) -> None:
        async with (
            async_client.make_ambiguous_schemas_looser.with_streaming_response.make_ambiguous_schemas_looser()
        ) as response:
            assert not response.is_closed

            make_ambiguous_schemas_looser = await response.parse()
            assert_matches_type(
                MakeAmbiguousSchemasLooserMakeAmbiguousSchemasLooserResponse,
                make_ambiguous_schemas_looser,
                path=["response"],
            )

        assert cast(Any, response.is_closed) is True
