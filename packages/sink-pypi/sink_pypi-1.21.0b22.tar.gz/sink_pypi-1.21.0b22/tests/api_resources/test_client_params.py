# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import (
    ClientParamWithPathParamResponse,
    ClientParamWithQueryParamResponse,
    ClientParamWithPathParamAndStandardResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestClientParams:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_with_path_param(self, client: Sink) -> None:
        client_param = client.client_params.with_path_param(
            client_path_param="client_path_param",
            client_path_or_query_param="client_path_or_query_param",
        )
        assert_matches_type(ClientParamWithPathParamResponse, client_param, path=["response"])

    @parametrize
    def test_raw_response_with_path_param(self, client: Sink) -> None:
        response = client.client_params.with_raw_response.with_path_param(
            client_path_param="client_path_param",
            client_path_or_query_param="client_path_or_query_param",
        )

        assert response.is_closed is True
        client_param = response.parse()
        assert_matches_type(ClientParamWithPathParamResponse, client_param, path=["response"])

    @parametrize
    def test_streaming_response_with_path_param(self, client: Sink) -> None:
        with client.client_params.with_streaming_response.with_path_param(
            client_path_param="client_path_param",
            client_path_or_query_param="client_path_or_query_param",
        ) as response:
            assert not response.is_closed

            client_param = response.parse()
            assert_matches_type(ClientParamWithPathParamResponse, client_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_with_path_param(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `client_path_param` but received ''"):
            client.client_params.with_raw_response.with_path_param(
                client_path_param="",
                client_path_or_query_param="client_path_or_query_param",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `client_path_or_query_param` but received ''"
        ):
            client.client_params.with_raw_response.with_path_param(
                client_path_param="client_path_param",
                client_path_or_query_param="",
            )

    @parametrize
    def test_method_with_path_param_and_standard(self, client: Sink) -> None:
        client_param = client.client_params.with_path_param_and_standard(
            id="id",
            camel_cased_path="camelCasedPath",
        )
        assert_matches_type(ClientParamWithPathParamAndStandardResponse, client_param, path=["response"])

    @parametrize
    def test_raw_response_with_path_param_and_standard(self, client: Sink) -> None:
        response = client.client_params.with_raw_response.with_path_param_and_standard(
            id="id",
            camel_cased_path="camelCasedPath",
        )

        assert response.is_closed is True
        client_param = response.parse()
        assert_matches_type(ClientParamWithPathParamAndStandardResponse, client_param, path=["response"])

    @parametrize
    def test_streaming_response_with_path_param_and_standard(self, client: Sink) -> None:
        with client.client_params.with_streaming_response.with_path_param_and_standard(
            id="id",
            camel_cased_path="camelCasedPath",
        ) as response:
            assert not response.is_closed

            client_param = response.parse()
            assert_matches_type(ClientParamWithPathParamAndStandardResponse, client_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_with_path_param_and_standard(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `camel_cased_path` but received ''"):
            client.client_params.with_raw_response.with_path_param_and_standard(
                id="id",
                camel_cased_path="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.client_params.with_raw_response.with_path_param_and_standard(
                id="",
                camel_cased_path="camelCasedPath",
            )

    @parametrize
    def test_method_with_query_param(self, client: Sink) -> None:
        client_param = client.client_params.with_query_param(
            client_path_or_query_param="client_path_or_query_param",
            client_query_param="client_query_param",
        )
        assert_matches_type(ClientParamWithQueryParamResponse, client_param, path=["response"])

    @parametrize
    def test_raw_response_with_query_param(self, client: Sink) -> None:
        response = client.client_params.with_raw_response.with_query_param(
            client_path_or_query_param="client_path_or_query_param",
            client_query_param="client_query_param",
        )

        assert response.is_closed is True
        client_param = response.parse()
        assert_matches_type(ClientParamWithQueryParamResponse, client_param, path=["response"])

    @parametrize
    def test_streaming_response_with_query_param(self, client: Sink) -> None:
        with client.client_params.with_streaming_response.with_query_param(
            client_path_or_query_param="client_path_or_query_param",
            client_query_param="client_query_param",
        ) as response:
            assert not response.is_closed

            client_param = response.parse()
            assert_matches_type(ClientParamWithQueryParamResponse, client_param, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncClientParams:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_with_path_param(self, async_client: AsyncSink) -> None:
        client_param = await async_client.client_params.with_path_param(
            client_path_param="client_path_param",
            client_path_or_query_param="client_path_or_query_param",
        )
        assert_matches_type(ClientParamWithPathParamResponse, client_param, path=["response"])

    @parametrize
    async def test_raw_response_with_path_param(self, async_client: AsyncSink) -> None:
        response = await async_client.client_params.with_raw_response.with_path_param(
            client_path_param="client_path_param",
            client_path_or_query_param="client_path_or_query_param",
        )

        assert response.is_closed is True
        client_param = response.parse()
        assert_matches_type(ClientParamWithPathParamResponse, client_param, path=["response"])

    @parametrize
    async def test_streaming_response_with_path_param(self, async_client: AsyncSink) -> None:
        async with async_client.client_params.with_streaming_response.with_path_param(
            client_path_param="client_path_param",
            client_path_or_query_param="client_path_or_query_param",
        ) as response:
            assert not response.is_closed

            client_param = await response.parse()
            assert_matches_type(ClientParamWithPathParamResponse, client_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_with_path_param(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `client_path_param` but received ''"):
            await async_client.client_params.with_raw_response.with_path_param(
                client_path_param="",
                client_path_or_query_param="client_path_or_query_param",
            )

        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `client_path_or_query_param` but received ''"
        ):
            await async_client.client_params.with_raw_response.with_path_param(
                client_path_param="client_path_param",
                client_path_or_query_param="",
            )

    @parametrize
    async def test_method_with_path_param_and_standard(self, async_client: AsyncSink) -> None:
        client_param = await async_client.client_params.with_path_param_and_standard(
            id="id",
            camel_cased_path="camelCasedPath",
        )
        assert_matches_type(ClientParamWithPathParamAndStandardResponse, client_param, path=["response"])

    @parametrize
    async def test_raw_response_with_path_param_and_standard(self, async_client: AsyncSink) -> None:
        response = await async_client.client_params.with_raw_response.with_path_param_and_standard(
            id="id",
            camel_cased_path="camelCasedPath",
        )

        assert response.is_closed is True
        client_param = response.parse()
        assert_matches_type(ClientParamWithPathParamAndStandardResponse, client_param, path=["response"])

    @parametrize
    async def test_streaming_response_with_path_param_and_standard(self, async_client: AsyncSink) -> None:
        async with async_client.client_params.with_streaming_response.with_path_param_and_standard(
            id="id",
            camel_cased_path="camelCasedPath",
        ) as response:
            assert not response.is_closed

            client_param = await response.parse()
            assert_matches_type(ClientParamWithPathParamAndStandardResponse, client_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_with_path_param_and_standard(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `camel_cased_path` but received ''"):
            await async_client.client_params.with_raw_response.with_path_param_and_standard(
                id="id",
                camel_cased_path="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.client_params.with_raw_response.with_path_param_and_standard(
                id="",
                camel_cased_path="camelCasedPath",
            )

    @parametrize
    async def test_method_with_query_param(self, async_client: AsyncSink) -> None:
        client_param = await async_client.client_params.with_query_param(
            client_path_or_query_param="client_path_or_query_param",
            client_query_param="client_query_param",
        )
        assert_matches_type(ClientParamWithQueryParamResponse, client_param, path=["response"])

    @parametrize
    async def test_raw_response_with_query_param(self, async_client: AsyncSink) -> None:
        response = await async_client.client_params.with_raw_response.with_query_param(
            client_path_or_query_param="client_path_or_query_param",
            client_query_param="client_query_param",
        )

        assert response.is_closed is True
        client_param = response.parse()
        assert_matches_type(ClientParamWithQueryParamResponse, client_param, path=["response"])

    @parametrize
    async def test_streaming_response_with_query_param(self, async_client: AsyncSink) -> None:
        async with async_client.client_params.with_streaming_response.with_query_param(
            client_path_or_query_param="client_path_or_query_param",
            client_query_param="client_query_param",
        ) as response:
            assert not response.is_closed

            client_param = await response.parse()
            assert_matches_type(ClientParamWithQueryParamResponse, client_param, path=["response"])

        assert cast(Any, response.is_closed) is True
