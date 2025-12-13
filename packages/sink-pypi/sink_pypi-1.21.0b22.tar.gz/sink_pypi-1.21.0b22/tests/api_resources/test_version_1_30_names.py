# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import Version1_30NameCreateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVersion1_30Names:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Sink) -> None:
        version_1_30_name = client.version_1_30_names.create(
            version_1_15="version_1_15",
        )
        assert_matches_type(Version1_30NameCreateResponse, version_1_30_name, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Sink) -> None:
        version_1_30_name = client.version_1_30_names.create(
            version_1_15="version_1_15",
            version_1_16="version_1_16",
            version_1_17="version_1_17",
            version_1_14="version_1_14",
        )
        assert_matches_type(Version1_30NameCreateResponse, version_1_30_name, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Sink) -> None:
        response = client.version_1_30_names.with_raw_response.create(
            version_1_15="version_1_15",
        )

        assert response.is_closed is True
        version_1_30_name = response.parse()
        assert_matches_type(Version1_30NameCreateResponse, version_1_30_name, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Sink) -> None:
        with client.version_1_30_names.with_streaming_response.create(
            version_1_15="version_1_15",
        ) as response:
            assert not response.is_closed

            version_1_30_name = response.parse()
            assert_matches_type(Version1_30NameCreateResponse, version_1_30_name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_1_15` but received ''"):
            client.version_1_30_names.with_raw_response.create(
                version_1_15="",
            )


class TestAsyncVersion1_30Names:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSink) -> None:
        version_1_30_name = await async_client.version_1_30_names.create(
            version_1_15="version_1_15",
        )
        assert_matches_type(Version1_30NameCreateResponse, version_1_30_name, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSink) -> None:
        version_1_30_name = await async_client.version_1_30_names.create(
            version_1_15="version_1_15",
            version_1_16="version_1_16",
            version_1_17="version_1_17",
            version_1_14="version_1_14",
        )
        assert_matches_type(Version1_30NameCreateResponse, version_1_30_name, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSink) -> None:
        response = await async_client.version_1_30_names.with_raw_response.create(
            version_1_15="version_1_15",
        )

        assert response.is_closed is True
        version_1_30_name = response.parse()
        assert_matches_type(Version1_30NameCreateResponse, version_1_30_name, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSink) -> None:
        async with async_client.version_1_30_names.with_streaming_response.create(
            version_1_15="version_1_15",
        ) as response:
            assert not response.is_closed

            version_1_30_name = await response.parse()
            assert_matches_type(Version1_30NameCreateResponse, version_1_30_name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_1_15` but received ''"):
            await async_client.version_1_30_names.with_raw_response.create(
                version_1_15="",
            )
