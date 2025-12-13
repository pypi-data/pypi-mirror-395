# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sink.api.sdk import Sink, AsyncSink

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestQueryParams:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_all_of(self, client: Sink) -> None:
        query_param = client.query_params.all_of()
        assert query_param is None

    @parametrize
    def test_method_all_of_with_all_params(self, client: Sink) -> None:
        query_param = client.query_params.all_of(
            foo_and_bar={
                "bar": 0,
                "foo": "foo",
            },
        )
        assert query_param is None

    @parametrize
    def test_raw_response_all_of(self, client: Sink) -> None:
        response = client.query_params.with_raw_response.all_of()

        assert response.is_closed is True
        query_param = response.parse()
        assert query_param is None

    @parametrize
    def test_streaming_response_all_of(self, client: Sink) -> None:
        with client.query_params.with_streaming_response.all_of() as response:
            assert not response.is_closed

            query_param = response.parse()
            assert query_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_any_of(self, client: Sink) -> None:
        query_param = client.query_params.any_of()
        assert query_param is None

    @parametrize
    def test_method_any_of_with_all_params(self, client: Sink) -> None:
        query_param = client.query_params.any_of(
            string_or_integer="string",
        )
        assert query_param is None

    @parametrize
    def test_raw_response_any_of(self, client: Sink) -> None:
        response = client.query_params.with_raw_response.any_of()

        assert response.is_closed is True
        query_param = response.parse()
        assert query_param is None

    @parametrize
    def test_streaming_response_any_of(self, client: Sink) -> None:
        with client.query_params.with_streaming_response.any_of() as response:
            assert not response.is_closed

            query_param = response.parse()
            assert query_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_any_of_string_or_array(self, client: Sink) -> None:
        query_param = client.query_params.any_of_string_or_array()
        assert query_param is None

    @parametrize
    def test_method_any_of_string_or_array_with_all_params(self, client: Sink) -> None:
        query_param = client.query_params.any_of_string_or_array(
            ids="string",
        )
        assert query_param is None

    @parametrize
    def test_raw_response_any_of_string_or_array(self, client: Sink) -> None:
        response = client.query_params.with_raw_response.any_of_string_or_array()

        assert response.is_closed is True
        query_param = response.parse()
        assert query_param is None

    @parametrize
    def test_streaming_response_any_of_string_or_array(self, client: Sink) -> None:
        with client.query_params.with_streaming_response.any_of_string_or_array() as response:
            assert not response.is_closed

            query_param = response.parse()
            assert query_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_array(self, client: Sink) -> None:
        query_param = client.query_params.array()
        assert query_param is None

    @parametrize
    def test_method_array_with_all_params(self, client: Sink) -> None:
        query_param = client.query_params.array(
            integer_array_param=[0],
            string_array_param=["string"],
        )
        assert query_param is None

    @parametrize
    def test_raw_response_array(self, client: Sink) -> None:
        response = client.query_params.with_raw_response.array()

        assert response.is_closed is True
        query_param = response.parse()
        assert query_param is None

    @parametrize
    def test_streaming_response_array(self, client: Sink) -> None:
        with client.query_params.with_streaming_response.array() as response:
            assert not response.is_closed

            query_param = response.parse()
            assert query_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_enum(self, client: Sink) -> None:
        query_param = client.query_params.enum()
        assert query_param is None

    @parametrize
    def test_method_enum_with_all_params(self, client: Sink) -> None:
        query_param = client.query_params.enum(
            integer_enum_param=100,
            nullable_integer_enum_param=100,
            nullable_number_enum_param=100,
            nullable_string_enum_param="foo",
            number_enum_param=100,
            string_enum_param="foo",
        )
        assert query_param is None

    @parametrize
    def test_raw_response_enum(self, client: Sink) -> None:
        response = client.query_params.with_raw_response.enum()

        assert response.is_closed is True
        query_param = response.parse()
        assert query_param is None

    @parametrize
    def test_streaming_response_enum(self, client: Sink) -> None:
        with client.query_params.with_streaming_response.enum() as response:
            assert not response.is_closed

            query_param = response.parse()
            assert query_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_object(self, client: Sink) -> None:
        query_param = client.query_params.object()
        assert query_param is None

    @parametrize
    def test_method_object_with_all_params(self, client: Sink) -> None:
        query_param = client.query_params.object(
            object_param={"foo": "foo"},
            object_ref_param={"item": "item"},
        )
        assert query_param is None

    @parametrize
    def test_raw_response_object(self, client: Sink) -> None:
        response = client.query_params.with_raw_response.object()

        assert response.is_closed is True
        query_param = response.parse()
        assert query_param is None

    @parametrize
    def test_streaming_response_object(self, client: Sink) -> None:
        with client.query_params.with_streaming_response.object() as response:
            assert not response.is_closed

            query_param = response.parse()
            assert query_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_one_of(self, client: Sink) -> None:
        query_param = client.query_params.one_of()
        assert query_param is None

    @parametrize
    def test_method_one_of_with_all_params(self, client: Sink) -> None:
        query_param = client.query_params.one_of(
            string_or_integer="string",
        )
        assert query_param is None

    @parametrize
    def test_raw_response_one_of(self, client: Sink) -> None:
        response = client.query_params.with_raw_response.one_of()

        assert response.is_closed is True
        query_param = response.parse()
        assert query_param is None

    @parametrize
    def test_streaming_response_one_of(self, client: Sink) -> None:
        with client.query_params.with_streaming_response.one_of() as response:
            assert not response.is_closed

            query_param = response.parse()
            assert query_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_primitives(self, client: Sink) -> None:
        query_param = client.query_params.primitives()
        assert query_param is None

    @parametrize
    def test_method_primitives_with_all_params(self, client: Sink) -> None:
        query_param = client.query_params.primitives(
            boolean_param=True,
            integer_param=0,
            number_param=0,
            string_param="string_param",
        )
        assert query_param is None

    @parametrize
    def test_raw_response_primitives(self, client: Sink) -> None:
        response = client.query_params.with_raw_response.primitives()

        assert response.is_closed is True
        query_param = response.parse()
        assert query_param is None

    @parametrize
    def test_streaming_response_primitives(self, client: Sink) -> None:
        with client.query_params.with_streaming_response.primitives() as response:
            assert not response.is_closed

            query_param = response.parse()
            assert query_param is None

        assert cast(Any, response.is_closed) is True


class TestAsyncQueryParams:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_all_of(self, async_client: AsyncSink) -> None:
        query_param = await async_client.query_params.all_of()
        assert query_param is None

    @parametrize
    async def test_method_all_of_with_all_params(self, async_client: AsyncSink) -> None:
        query_param = await async_client.query_params.all_of(
            foo_and_bar={
                "bar": 0,
                "foo": "foo",
            },
        )
        assert query_param is None

    @parametrize
    async def test_raw_response_all_of(self, async_client: AsyncSink) -> None:
        response = await async_client.query_params.with_raw_response.all_of()

        assert response.is_closed is True
        query_param = response.parse()
        assert query_param is None

    @parametrize
    async def test_streaming_response_all_of(self, async_client: AsyncSink) -> None:
        async with async_client.query_params.with_streaming_response.all_of() as response:
            assert not response.is_closed

            query_param = await response.parse()
            assert query_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_any_of(self, async_client: AsyncSink) -> None:
        query_param = await async_client.query_params.any_of()
        assert query_param is None

    @parametrize
    async def test_method_any_of_with_all_params(self, async_client: AsyncSink) -> None:
        query_param = await async_client.query_params.any_of(
            string_or_integer="string",
        )
        assert query_param is None

    @parametrize
    async def test_raw_response_any_of(self, async_client: AsyncSink) -> None:
        response = await async_client.query_params.with_raw_response.any_of()

        assert response.is_closed is True
        query_param = response.parse()
        assert query_param is None

    @parametrize
    async def test_streaming_response_any_of(self, async_client: AsyncSink) -> None:
        async with async_client.query_params.with_streaming_response.any_of() as response:
            assert not response.is_closed

            query_param = await response.parse()
            assert query_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_any_of_string_or_array(self, async_client: AsyncSink) -> None:
        query_param = await async_client.query_params.any_of_string_or_array()
        assert query_param is None

    @parametrize
    async def test_method_any_of_string_or_array_with_all_params(self, async_client: AsyncSink) -> None:
        query_param = await async_client.query_params.any_of_string_or_array(
            ids="string",
        )
        assert query_param is None

    @parametrize
    async def test_raw_response_any_of_string_or_array(self, async_client: AsyncSink) -> None:
        response = await async_client.query_params.with_raw_response.any_of_string_or_array()

        assert response.is_closed is True
        query_param = response.parse()
        assert query_param is None

    @parametrize
    async def test_streaming_response_any_of_string_or_array(self, async_client: AsyncSink) -> None:
        async with async_client.query_params.with_streaming_response.any_of_string_or_array() as response:
            assert not response.is_closed

            query_param = await response.parse()
            assert query_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_array(self, async_client: AsyncSink) -> None:
        query_param = await async_client.query_params.array()
        assert query_param is None

    @parametrize
    async def test_method_array_with_all_params(self, async_client: AsyncSink) -> None:
        query_param = await async_client.query_params.array(
            integer_array_param=[0],
            string_array_param=["string"],
        )
        assert query_param is None

    @parametrize
    async def test_raw_response_array(self, async_client: AsyncSink) -> None:
        response = await async_client.query_params.with_raw_response.array()

        assert response.is_closed is True
        query_param = response.parse()
        assert query_param is None

    @parametrize
    async def test_streaming_response_array(self, async_client: AsyncSink) -> None:
        async with async_client.query_params.with_streaming_response.array() as response:
            assert not response.is_closed

            query_param = await response.parse()
            assert query_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_enum(self, async_client: AsyncSink) -> None:
        query_param = await async_client.query_params.enum()
        assert query_param is None

    @parametrize
    async def test_method_enum_with_all_params(self, async_client: AsyncSink) -> None:
        query_param = await async_client.query_params.enum(
            integer_enum_param=100,
            nullable_integer_enum_param=100,
            nullable_number_enum_param=100,
            nullable_string_enum_param="foo",
            number_enum_param=100,
            string_enum_param="foo",
        )
        assert query_param is None

    @parametrize
    async def test_raw_response_enum(self, async_client: AsyncSink) -> None:
        response = await async_client.query_params.with_raw_response.enum()

        assert response.is_closed is True
        query_param = response.parse()
        assert query_param is None

    @parametrize
    async def test_streaming_response_enum(self, async_client: AsyncSink) -> None:
        async with async_client.query_params.with_streaming_response.enum() as response:
            assert not response.is_closed

            query_param = await response.parse()
            assert query_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_object(self, async_client: AsyncSink) -> None:
        query_param = await async_client.query_params.object()
        assert query_param is None

    @parametrize
    async def test_method_object_with_all_params(self, async_client: AsyncSink) -> None:
        query_param = await async_client.query_params.object(
            object_param={"foo": "foo"},
            object_ref_param={"item": "item"},
        )
        assert query_param is None

    @parametrize
    async def test_raw_response_object(self, async_client: AsyncSink) -> None:
        response = await async_client.query_params.with_raw_response.object()

        assert response.is_closed is True
        query_param = response.parse()
        assert query_param is None

    @parametrize
    async def test_streaming_response_object(self, async_client: AsyncSink) -> None:
        async with async_client.query_params.with_streaming_response.object() as response:
            assert not response.is_closed

            query_param = await response.parse()
            assert query_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_one_of(self, async_client: AsyncSink) -> None:
        query_param = await async_client.query_params.one_of()
        assert query_param is None

    @parametrize
    async def test_method_one_of_with_all_params(self, async_client: AsyncSink) -> None:
        query_param = await async_client.query_params.one_of(
            string_or_integer="string",
        )
        assert query_param is None

    @parametrize
    async def test_raw_response_one_of(self, async_client: AsyncSink) -> None:
        response = await async_client.query_params.with_raw_response.one_of()

        assert response.is_closed is True
        query_param = response.parse()
        assert query_param is None

    @parametrize
    async def test_streaming_response_one_of(self, async_client: AsyncSink) -> None:
        async with async_client.query_params.with_streaming_response.one_of() as response:
            assert not response.is_closed

            query_param = await response.parse()
            assert query_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_primitives(self, async_client: AsyncSink) -> None:
        query_param = await async_client.query_params.primitives()
        assert query_param is None

    @parametrize
    async def test_method_primitives_with_all_params(self, async_client: AsyncSink) -> None:
        query_param = await async_client.query_params.primitives(
            boolean_param=True,
            integer_param=0,
            number_param=0,
            string_param="string_param",
        )
        assert query_param is None

    @parametrize
    async def test_raw_response_primitives(self, async_client: AsyncSink) -> None:
        response = await async_client.query_params.with_raw_response.primitives()

        assert response.is_closed is True
        query_param = response.parse()
        assert query_param is None

    @parametrize
    async def test_streaming_response_primitives(self, async_client: AsyncSink) -> None:
        async with async_client.query_params.with_streaming_response.primitives() as response:
            assert not response.is_closed

            query_param = await response.parse()
            assert query_param is None

        assert cast(Any, response.is_closed) is True
