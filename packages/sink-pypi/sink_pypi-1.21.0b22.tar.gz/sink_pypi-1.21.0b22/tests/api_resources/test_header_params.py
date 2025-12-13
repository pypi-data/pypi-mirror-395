# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sink.api.sdk import Sink, AsyncSink

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestHeaderParams:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_all_types(self, client: Sink) -> None:
        header_param = client.header_params.all_types(
            x_required_boolean=True,
            x_required_integer=0,
            x_required_number=0,
            x_required_string="X-Required-String",
        )
        assert header_param is None

    @parametrize
    def test_method_all_types_with_all_params(self, client: Sink) -> None:
        header_param = client.header_params.all_types(
            x_required_boolean=True,
            x_required_integer=0,
            x_required_number=0,
            x_required_string="X-Required-String",
            body_argument="body_argument",
            x_nullable_integer=0,
            x_optional_boolean=True,
            x_optional_integer=0,
            x_optional_number=0,
            x_optional_string="X-Optional-String",
        )
        assert header_param is None

    @parametrize
    def test_raw_response_all_types(self, client: Sink) -> None:
        response = client.header_params.with_raw_response.all_types(
            x_required_boolean=True,
            x_required_integer=0,
            x_required_number=0,
            x_required_string="X-Required-String",
        )

        assert response.is_closed is True
        header_param = response.parse()
        assert header_param is None

    @parametrize
    def test_streaming_response_all_types(self, client: Sink) -> None:
        with client.header_params.with_streaming_response.all_types(
            x_required_boolean=True,
            x_required_integer=0,
            x_required_number=0,
            x_required_string="X-Required-String",
        ) as response:
            assert not response.is_closed

            header_param = response.parse()
            assert header_param is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism doesn't support array headers")
    @parametrize
    def test_method_arrays(self, client: Sink) -> None:
        header_param = client.header_params.arrays(
            x_required_int_array=[0],
            x_required_string_array=["string"],
        )
        assert header_param is None

    @pytest.mark.skip(reason="prism doesn't support array headers")
    @parametrize
    def test_method_arrays_with_all_params(self, client: Sink) -> None:
        header_param = client.header_params.arrays(
            x_required_int_array=[0],
            x_required_string_array=["string"],
            body_argument="body_argument",
            x_optional_int_array=[0],
            x_optional_string_array=["string"],
        )
        assert header_param is None

    @pytest.mark.skip(reason="prism doesn't support array headers")
    @parametrize
    def test_raw_response_arrays(self, client: Sink) -> None:
        response = client.header_params.with_raw_response.arrays(
            x_required_int_array=[0],
            x_required_string_array=["string"],
        )

        assert response.is_closed is True
        header_param = response.parse()
        assert header_param is None

    @pytest.mark.skip(reason="prism doesn't support array headers")
    @parametrize
    def test_streaming_response_arrays(self, client: Sink) -> None:
        with client.header_params.with_streaming_response.arrays(
            x_required_int_array=[0],
            x_required_string_array=["string"],
        ) as response:
            assert not response.is_closed

            header_param = response.parse()
            assert header_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_client_argument(self, client: Sink) -> None:
        header_param = client.header_params.client_argument()
        assert header_param is None

    @parametrize
    def test_method_client_argument_with_all_params(self, client: Sink) -> None:
        header_param = client.header_params.client_argument(
            foo="foo",
            x_custom_endpoint_header="X-Custom-Endpoint-Header",
        )
        assert header_param is None

    @parametrize
    def test_raw_response_client_argument(self, client: Sink) -> None:
        response = client.header_params.with_raw_response.client_argument()

        assert response.is_closed is True
        header_param = response.parse()
        assert header_param is None

    @parametrize
    def test_streaming_response_client_argument(self, client: Sink) -> None:
        with client.header_params.with_streaming_response.client_argument() as response:
            assert not response.is_closed

            header_param = response.parse()
            assert header_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_invalid_name(self, client: Sink) -> None:
        header_param = client.header_params.invalid_name()
        assert header_param is None

    @parametrize
    def test_method_invalid_name_with_all_params(self, client: Sink) -> None:
        header_param = client.header_params.invalid_name(
            foo="foo",
        )
        assert header_param is None

    @parametrize
    def test_raw_response_invalid_name(self, client: Sink) -> None:
        response = client.header_params.with_raw_response.invalid_name()

        assert response.is_closed is True
        header_param = response.parse()
        assert header_param is None

    @parametrize
    def test_streaming_response_invalid_name(self, client: Sink) -> None:
        with client.header_params.with_streaming_response.invalid_name() as response:
            assert not response.is_closed

            header_param = response.parse()
            assert header_param is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism doesn't like us changing the header to a string")
    @parametrize
    def test_method_nullable_type(self, client: Sink) -> None:
        header_param = client.header_params.nullable_type()
        assert header_param is None

    @pytest.mark.skip(reason="prism doesn't like us changing the header to a string")
    @parametrize
    def test_method_nullable_type_with_all_params(self, client: Sink) -> None:
        header_param = client.header_params.nullable_type(
            body_argument="body_argument",
            x_null="X-Null",
        )
        assert header_param is None

    @pytest.mark.skip(reason="prism doesn't like us changing the header to a string")
    @parametrize
    def test_raw_response_nullable_type(self, client: Sink) -> None:
        response = client.header_params.with_raw_response.nullable_type()

        assert response.is_closed is True
        header_param = response.parse()
        assert header_param is None

    @pytest.mark.skip(reason="prism doesn't like us changing the header to a string")
    @parametrize
    def test_streaming_response_nullable_type(self, client: Sink) -> None:
        with client.header_params.with_streaming_response.nullable_type() as response:
            assert not response.is_closed

            header_param = response.parse()
            assert header_param is None

        assert cast(Any, response.is_closed) is True


class TestAsyncHeaderParams:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_all_types(self, async_client: AsyncSink) -> None:
        header_param = await async_client.header_params.all_types(
            x_required_boolean=True,
            x_required_integer=0,
            x_required_number=0,
            x_required_string="X-Required-String",
        )
        assert header_param is None

    @parametrize
    async def test_method_all_types_with_all_params(self, async_client: AsyncSink) -> None:
        header_param = await async_client.header_params.all_types(
            x_required_boolean=True,
            x_required_integer=0,
            x_required_number=0,
            x_required_string="X-Required-String",
            body_argument="body_argument",
            x_nullable_integer=0,
            x_optional_boolean=True,
            x_optional_integer=0,
            x_optional_number=0,
            x_optional_string="X-Optional-String",
        )
        assert header_param is None

    @parametrize
    async def test_raw_response_all_types(self, async_client: AsyncSink) -> None:
        response = await async_client.header_params.with_raw_response.all_types(
            x_required_boolean=True,
            x_required_integer=0,
            x_required_number=0,
            x_required_string="X-Required-String",
        )

        assert response.is_closed is True
        header_param = response.parse()
        assert header_param is None

    @parametrize
    async def test_streaming_response_all_types(self, async_client: AsyncSink) -> None:
        async with async_client.header_params.with_streaming_response.all_types(
            x_required_boolean=True,
            x_required_integer=0,
            x_required_number=0,
            x_required_string="X-Required-String",
        ) as response:
            assert not response.is_closed

            header_param = await response.parse()
            assert header_param is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism doesn't support array headers")
    @parametrize
    async def test_method_arrays(self, async_client: AsyncSink) -> None:
        header_param = await async_client.header_params.arrays(
            x_required_int_array=[0],
            x_required_string_array=["string"],
        )
        assert header_param is None

    @pytest.mark.skip(reason="prism doesn't support array headers")
    @parametrize
    async def test_method_arrays_with_all_params(self, async_client: AsyncSink) -> None:
        header_param = await async_client.header_params.arrays(
            x_required_int_array=[0],
            x_required_string_array=["string"],
            body_argument="body_argument",
            x_optional_int_array=[0],
            x_optional_string_array=["string"],
        )
        assert header_param is None

    @pytest.mark.skip(reason="prism doesn't support array headers")
    @parametrize
    async def test_raw_response_arrays(self, async_client: AsyncSink) -> None:
        response = await async_client.header_params.with_raw_response.arrays(
            x_required_int_array=[0],
            x_required_string_array=["string"],
        )

        assert response.is_closed is True
        header_param = response.parse()
        assert header_param is None

    @pytest.mark.skip(reason="prism doesn't support array headers")
    @parametrize
    async def test_streaming_response_arrays(self, async_client: AsyncSink) -> None:
        async with async_client.header_params.with_streaming_response.arrays(
            x_required_int_array=[0],
            x_required_string_array=["string"],
        ) as response:
            assert not response.is_closed

            header_param = await response.parse()
            assert header_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_client_argument(self, async_client: AsyncSink) -> None:
        header_param = await async_client.header_params.client_argument()
        assert header_param is None

    @parametrize
    async def test_method_client_argument_with_all_params(self, async_client: AsyncSink) -> None:
        header_param = await async_client.header_params.client_argument(
            foo="foo",
            x_custom_endpoint_header="X-Custom-Endpoint-Header",
        )
        assert header_param is None

    @parametrize
    async def test_raw_response_client_argument(self, async_client: AsyncSink) -> None:
        response = await async_client.header_params.with_raw_response.client_argument()

        assert response.is_closed is True
        header_param = response.parse()
        assert header_param is None

    @parametrize
    async def test_streaming_response_client_argument(self, async_client: AsyncSink) -> None:
        async with async_client.header_params.with_streaming_response.client_argument() as response:
            assert not response.is_closed

            header_param = await response.parse()
            assert header_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_invalid_name(self, async_client: AsyncSink) -> None:
        header_param = await async_client.header_params.invalid_name()
        assert header_param is None

    @parametrize
    async def test_method_invalid_name_with_all_params(self, async_client: AsyncSink) -> None:
        header_param = await async_client.header_params.invalid_name(
            foo="foo",
        )
        assert header_param is None

    @parametrize
    async def test_raw_response_invalid_name(self, async_client: AsyncSink) -> None:
        response = await async_client.header_params.with_raw_response.invalid_name()

        assert response.is_closed is True
        header_param = response.parse()
        assert header_param is None

    @parametrize
    async def test_streaming_response_invalid_name(self, async_client: AsyncSink) -> None:
        async with async_client.header_params.with_streaming_response.invalid_name() as response:
            assert not response.is_closed

            header_param = await response.parse()
            assert header_param is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism doesn't like us changing the header to a string")
    @parametrize
    async def test_method_nullable_type(self, async_client: AsyncSink) -> None:
        header_param = await async_client.header_params.nullable_type()
        assert header_param is None

    @pytest.mark.skip(reason="prism doesn't like us changing the header to a string")
    @parametrize
    async def test_method_nullable_type_with_all_params(self, async_client: AsyncSink) -> None:
        header_param = await async_client.header_params.nullable_type(
            body_argument="body_argument",
            x_null="X-Null",
        )
        assert header_param is None

    @pytest.mark.skip(reason="prism doesn't like us changing the header to a string")
    @parametrize
    async def test_raw_response_nullable_type(self, async_client: AsyncSink) -> None:
        response = await async_client.header_params.with_raw_response.nullable_type()

        assert response.is_closed is True
        header_param = response.parse()
        assert header_param is None

    @pytest.mark.skip(reason="prism doesn't like us changing the header to a string")
    @parametrize
    async def test_streaming_response_nullable_type(self, async_client: AsyncSink) -> None:
        async with async_client.header_params.with_streaming_response.nullable_type() as response:
            assert not response.is_closed

            header_param = await response.parse()
            assert header_param is None

        assert cast(Any, response.is_closed) is True
