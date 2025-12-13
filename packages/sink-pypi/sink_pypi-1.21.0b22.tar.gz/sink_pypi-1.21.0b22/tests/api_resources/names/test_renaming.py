# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.names import RenamingExplicitResponsePropertyResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRenaming:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_explicit_response_property(self, client: Sink) -> None:
        renaming = client.names.renaming.explicit_response_property()
        assert_matches_type(RenamingExplicitResponsePropertyResponse, renaming, path=["response"])

    @parametrize
    def test_raw_response_explicit_response_property(self, client: Sink) -> None:
        response = client.names.renaming.with_raw_response.explicit_response_property()

        assert response.is_closed is True
        renaming = response.parse()
        assert_matches_type(RenamingExplicitResponsePropertyResponse, renaming, path=["response"])

    @parametrize
    def test_streaming_response_explicit_response_property(self, client: Sink) -> None:
        with client.names.renaming.with_streaming_response.explicit_response_property() as response:
            assert not response.is_closed

            renaming = response.parse()
            assert_matches_type(RenamingExplicitResponsePropertyResponse, renaming, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncRenaming:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_explicit_response_property(self, async_client: AsyncSink) -> None:
        renaming = await async_client.names.renaming.explicit_response_property()
        assert_matches_type(RenamingExplicitResponsePropertyResponse, renaming, path=["response"])

    @parametrize
    async def test_raw_response_explicit_response_property(self, async_client: AsyncSink) -> None:
        response = await async_client.names.renaming.with_raw_response.explicit_response_property()

        assert response.is_closed is True
        renaming = response.parse()
        assert_matches_type(RenamingExplicitResponsePropertyResponse, renaming, path=["response"])

    @parametrize
    async def test_streaming_response_explicit_response_property(self, async_client: AsyncSink) -> None:
        async with async_client.names.renaming.with_streaming_response.explicit_response_property() as response:
            assert not response.is_closed

            renaming = await response.parse()
            assert_matches_type(RenamingExplicitResponsePropertyResponse, renaming, path=["response"])

        assert cast(Any, response.is_closed) is True
