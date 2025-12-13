# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import MakeAmbiguousSchemasExplicitMakeAmbiguousSchemasExplicitResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMakeAmbiguousSchemasExplicit:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_make_ambiguous_schemas_explicit(self, client: Sink) -> None:
        make_ambiguous_schemas_explicit = client.make_ambiguous_schemas_explicit.make_ambiguous_schemas_explicit()
        assert_matches_type(
            MakeAmbiguousSchemasExplicitMakeAmbiguousSchemasExplicitResponse,
            make_ambiguous_schemas_explicit,
            path=["response"],
        )

    @parametrize
    def test_raw_response_make_ambiguous_schemas_explicit(self, client: Sink) -> None:
        response = client.make_ambiguous_schemas_explicit.with_raw_response.make_ambiguous_schemas_explicit()

        assert response.is_closed is True
        make_ambiguous_schemas_explicit = response.parse()
        assert_matches_type(
            MakeAmbiguousSchemasExplicitMakeAmbiguousSchemasExplicitResponse,
            make_ambiguous_schemas_explicit,
            path=["response"],
        )

    @parametrize
    def test_streaming_response_make_ambiguous_schemas_explicit(self, client: Sink) -> None:
        with (
            client.make_ambiguous_schemas_explicit.with_streaming_response.make_ambiguous_schemas_explicit()
        ) as response:
            assert not response.is_closed

            make_ambiguous_schemas_explicit = response.parse()
            assert_matches_type(
                MakeAmbiguousSchemasExplicitMakeAmbiguousSchemasExplicitResponse,
                make_ambiguous_schemas_explicit,
                path=["response"],
            )

        assert cast(Any, response.is_closed) is True


class TestAsyncMakeAmbiguousSchemasExplicit:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_make_ambiguous_schemas_explicit(self, async_client: AsyncSink) -> None:
        make_ambiguous_schemas_explicit = (
            await async_client.make_ambiguous_schemas_explicit.make_ambiguous_schemas_explicit()
        )
        assert_matches_type(
            MakeAmbiguousSchemasExplicitMakeAmbiguousSchemasExplicitResponse,
            make_ambiguous_schemas_explicit,
            path=["response"],
        )

    @parametrize
    async def test_raw_response_make_ambiguous_schemas_explicit(self, async_client: AsyncSink) -> None:
        response = (
            await async_client.make_ambiguous_schemas_explicit.with_raw_response.make_ambiguous_schemas_explicit()
        )

        assert response.is_closed is True
        make_ambiguous_schemas_explicit = response.parse()
        assert_matches_type(
            MakeAmbiguousSchemasExplicitMakeAmbiguousSchemasExplicitResponse,
            make_ambiguous_schemas_explicit,
            path=["response"],
        )

    @parametrize
    async def test_streaming_response_make_ambiguous_schemas_explicit(self, async_client: AsyncSink) -> None:
        async with (
            async_client.make_ambiguous_schemas_explicit.with_streaming_response.make_ambiguous_schemas_explicit()
        ) as response:
            assert not response.is_closed

            make_ambiguous_schemas_explicit = await response.parse()
            assert_matches_type(
                MakeAmbiguousSchemasExplicitMakeAmbiguousSchemasExplicitResponse,
                make_ambiguous_schemas_explicit,
                path=["response"],
            )

        assert cast(Any, response.is_closed) is True
