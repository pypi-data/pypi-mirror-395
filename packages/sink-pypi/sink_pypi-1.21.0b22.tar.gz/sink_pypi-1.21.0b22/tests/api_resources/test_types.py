# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import TypeDatesResponse, TypeDatetimesResponse
from sink.api.sdk._utils import parse_date, parse_datetime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTypes:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_dates(self, client: Sink) -> None:
        type = client.types.dates(
            required_date=parse_date("2019-12-27"),
            required_nullable_date=parse_date("2019-12-27"),
        )
        assert_matches_type(TypeDatesResponse, type, path=["response"])

    @parametrize
    def test_method_dates_with_all_params(self, client: Sink) -> None:
        type = client.types.dates(
            required_date=parse_date("2019-12-27"),
            required_nullable_date=parse_date("2019-12-27"),
            list_date=[parse_date("2019-12-27")],
            oneof_date=parse_date("2019-12-27"),
            optional_date=parse_date("2019-12-27"),
        )
        assert_matches_type(TypeDatesResponse, type, path=["response"])

    @parametrize
    def test_raw_response_dates(self, client: Sink) -> None:
        response = client.types.with_raw_response.dates(
            required_date=parse_date("2019-12-27"),
            required_nullable_date=parse_date("2019-12-27"),
        )

        assert response.is_closed is True
        type = response.parse()
        assert_matches_type(TypeDatesResponse, type, path=["response"])

    @parametrize
    def test_streaming_response_dates(self, client: Sink) -> None:
        with client.types.with_streaming_response.dates(
            required_date=parse_date("2019-12-27"),
            required_nullable_date=parse_date("2019-12-27"),
        ) as response:
            assert not response.is_closed

            type = response.parse()
            assert_matches_type(TypeDatesResponse, type, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_datetimes(self, client: Sink) -> None:
        type = client.types.datetimes(
            required_datetime=parse_datetime("2019-12-27T18:11:19.117Z"),
            required_nullable_datetime=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(TypeDatetimesResponse, type, path=["response"])

    @parametrize
    def test_method_datetimes_with_all_params(self, client: Sink) -> None:
        type = client.types.datetimes(
            required_datetime=parse_datetime("2019-12-27T18:11:19.117Z"),
            required_nullable_datetime=parse_datetime("2019-12-27T18:11:19.117Z"),
            list_datetime=[parse_datetime("2019-12-27T18:11:19.117Z")],
            oneof_datetime=parse_datetime("2019-12-27T18:11:19.117Z"),
            optional_datetime=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(TypeDatetimesResponse, type, path=["response"])

    @parametrize
    def test_raw_response_datetimes(self, client: Sink) -> None:
        response = client.types.with_raw_response.datetimes(
            required_datetime=parse_datetime("2019-12-27T18:11:19.117Z"),
            required_nullable_datetime=parse_datetime("2019-12-27T18:11:19.117Z"),
        )

        assert response.is_closed is True
        type = response.parse()
        assert_matches_type(TypeDatetimesResponse, type, path=["response"])

    @parametrize
    def test_streaming_response_datetimes(self, client: Sink) -> None:
        with client.types.with_streaming_response.datetimes(
            required_datetime=parse_datetime("2019-12-27T18:11:19.117Z"),
            required_nullable_datetime=parse_datetime("2019-12-27T18:11:19.117Z"),
        ) as response:
            assert not response.is_closed

            type = response.parse()
            assert_matches_type(TypeDatetimesResponse, type, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTypes:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_dates(self, async_client: AsyncSink) -> None:
        type = await async_client.types.dates(
            required_date=parse_date("2019-12-27"),
            required_nullable_date=parse_date("2019-12-27"),
        )
        assert_matches_type(TypeDatesResponse, type, path=["response"])

    @parametrize
    async def test_method_dates_with_all_params(self, async_client: AsyncSink) -> None:
        type = await async_client.types.dates(
            required_date=parse_date("2019-12-27"),
            required_nullable_date=parse_date("2019-12-27"),
            list_date=[parse_date("2019-12-27")],
            oneof_date=parse_date("2019-12-27"),
            optional_date=parse_date("2019-12-27"),
        )
        assert_matches_type(TypeDatesResponse, type, path=["response"])

    @parametrize
    async def test_raw_response_dates(self, async_client: AsyncSink) -> None:
        response = await async_client.types.with_raw_response.dates(
            required_date=parse_date("2019-12-27"),
            required_nullable_date=parse_date("2019-12-27"),
        )

        assert response.is_closed is True
        type = response.parse()
        assert_matches_type(TypeDatesResponse, type, path=["response"])

    @parametrize
    async def test_streaming_response_dates(self, async_client: AsyncSink) -> None:
        async with async_client.types.with_streaming_response.dates(
            required_date=parse_date("2019-12-27"),
            required_nullable_date=parse_date("2019-12-27"),
        ) as response:
            assert not response.is_closed

            type = await response.parse()
            assert_matches_type(TypeDatesResponse, type, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_datetimes(self, async_client: AsyncSink) -> None:
        type = await async_client.types.datetimes(
            required_datetime=parse_datetime("2019-12-27T18:11:19.117Z"),
            required_nullable_datetime=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(TypeDatetimesResponse, type, path=["response"])

    @parametrize
    async def test_method_datetimes_with_all_params(self, async_client: AsyncSink) -> None:
        type = await async_client.types.datetimes(
            required_datetime=parse_datetime("2019-12-27T18:11:19.117Z"),
            required_nullable_datetime=parse_datetime("2019-12-27T18:11:19.117Z"),
            list_datetime=[parse_datetime("2019-12-27T18:11:19.117Z")],
            oneof_datetime=parse_datetime("2019-12-27T18:11:19.117Z"),
            optional_datetime=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(TypeDatetimesResponse, type, path=["response"])

    @parametrize
    async def test_raw_response_datetimes(self, async_client: AsyncSink) -> None:
        response = await async_client.types.with_raw_response.datetimes(
            required_datetime=parse_datetime("2019-12-27T18:11:19.117Z"),
            required_nullable_datetime=parse_datetime("2019-12-27T18:11:19.117Z"),
        )

        assert response.is_closed is True
        type = response.parse()
        assert_matches_type(TypeDatetimesResponse, type, path=["response"])

    @parametrize
    async def test_streaming_response_datetimes(self, async_client: AsyncSink) -> None:
        async with async_client.types.with_streaming_response.datetimes(
            required_datetime=parse_datetime("2019-12-27T18:11:19.117Z"),
            required_nullable_datetime=parse_datetime("2019-12-27T18:11:19.117Z"),
        ) as response:
            assert not response.is_closed

            type = await response.parse()
            assert_matches_type(TypeDatetimesResponse, type, path=["response"])

        assert cast(Any, response.is_closed) is True
