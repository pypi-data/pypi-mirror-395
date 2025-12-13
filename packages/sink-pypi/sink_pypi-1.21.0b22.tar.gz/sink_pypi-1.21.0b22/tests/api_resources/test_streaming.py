# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import (
    StreamingBasicResponse,
    StreamingNestedParamsResponse,
    StreamingQueryParamDiscriminatorResponse,
    StreamingWithUnrelatedDefaultParamResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestStreaming:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_basic_overload_1(self, client: Sink) -> None:
        streaming = client.streaming.basic(
            model="model",
            prompt="prompt",
        )
        assert_matches_type(StreamingBasicResponse, streaming, path=["response"])

    @parametrize
    def test_method_basic_with_all_params_overload_1(self, client: Sink) -> None:
        streaming = client.streaming.basic(
            model="model",
            prompt="prompt",
            stream=False,
        )
        assert_matches_type(StreamingBasicResponse, streaming, path=["response"])

    @parametrize
    def test_raw_response_basic_overload_1(self, client: Sink) -> None:
        response = client.streaming.with_raw_response.basic(
            model="model",
            prompt="prompt",
        )

        assert response.is_closed is True
        streaming = response.parse()
        assert_matches_type(StreamingBasicResponse, streaming, path=["response"])

    @parametrize
    def test_streaming_response_basic_overload_1(self, client: Sink) -> None:
        with client.streaming.with_streaming_response.basic(
            model="model",
            prompt="prompt",
        ) as response:
            assert not response.is_closed

            streaming = response.parse()
            assert_matches_type(StreamingBasicResponse, streaming, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_basic_overload_2(self, client: Sink) -> None:
        streaming_stream = client.streaming.basic(
            model="model",
            prompt="prompt",
            stream=True,
        )
        streaming_stream.response.close()

    @parametrize
    def test_raw_response_basic_overload_2(self, client: Sink) -> None:
        response = client.streaming.with_raw_response.basic(
            model="model",
            prompt="prompt",
            stream=True,
        )

        stream = response.parse()
        stream.close()

    @parametrize
    def test_streaming_response_basic_overload_2(self, client: Sink) -> None:
        with client.streaming.with_streaming_response.basic(
            model="model",
            prompt="prompt",
            stream=True,
        ) as response:
            assert not response.is_closed

            stream = response.parse()
            stream.close()

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_nested_params_overload_1(self, client: Sink) -> None:
        streaming = client.streaming.nested_params(
            model="model",
            prompt="prompt",
        )
        assert_matches_type(StreamingNestedParamsResponse, streaming, path=["response"])

    @parametrize
    def test_method_nested_params_with_all_params_overload_1(self, client: Sink) -> None:
        streaming = client.streaming.nested_params(
            model="model",
            prompt="prompt",
            parent_object={
                "array_prop": [{"from_array_items": True}],
                "child_prop": {"from_object": "from_object"},
            },
            stream=False,
        )
        assert_matches_type(StreamingNestedParamsResponse, streaming, path=["response"])

    @parametrize
    def test_raw_response_nested_params_overload_1(self, client: Sink) -> None:
        response = client.streaming.with_raw_response.nested_params(
            model="model",
            prompt="prompt",
        )

        assert response.is_closed is True
        streaming = response.parse()
        assert_matches_type(StreamingNestedParamsResponse, streaming, path=["response"])

    @parametrize
    def test_streaming_response_nested_params_overload_1(self, client: Sink) -> None:
        with client.streaming.with_streaming_response.nested_params(
            model="model",
            prompt="prompt",
        ) as response:
            assert not response.is_closed

            streaming = response.parse()
            assert_matches_type(StreamingNestedParamsResponse, streaming, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_nested_params_overload_2(self, client: Sink) -> None:
        streaming_stream = client.streaming.nested_params(
            model="model",
            prompt="prompt",
            stream=True,
        )
        streaming_stream.response.close()

    @parametrize
    def test_method_nested_params_with_all_params_overload_2(self, client: Sink) -> None:
        streaming_stream = client.streaming.nested_params(
            model="model",
            prompt="prompt",
            stream=True,
            parent_object={
                "array_prop": [{"from_array_items": True}],
                "child_prop": {"from_object": "from_object"},
            },
        )
        streaming_stream.response.close()

    @parametrize
    def test_raw_response_nested_params_overload_2(self, client: Sink) -> None:
        response = client.streaming.with_raw_response.nested_params(
            model="model",
            prompt="prompt",
            stream=True,
        )

        stream = response.parse()
        stream.close()

    @parametrize
    def test_streaming_response_nested_params_overload_2(self, client: Sink) -> None:
        with client.streaming.with_streaming_response.nested_params(
            model="model",
            prompt="prompt",
            stream=True,
        ) as response:
            assert not response.is_closed

            stream = response.parse()
            stream.close()

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_no_discriminator(self, client: Sink) -> None:
        streaming_stream = client.streaming.no_discriminator(
            model="model",
            prompt="prompt",
        )
        streaming_stream.response.close()

    @parametrize
    def test_raw_response_no_discriminator(self, client: Sink) -> None:
        response = client.streaming.with_raw_response.no_discriminator(
            model="model",
            prompt="prompt",
        )

        stream = response.parse()
        stream.close()

    @parametrize
    def test_streaming_response_no_discriminator(self, client: Sink) -> None:
        with client.streaming.with_streaming_response.no_discriminator(
            model="model",
            prompt="prompt",
        ) as response:
            assert not response.is_closed

            stream = response.parse()
            stream.close()

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_query_param_discriminator_overload_1(self, client: Sink) -> None:
        streaming = client.streaming.query_param_discriminator(
            prompt="prompt",
        )
        assert_matches_type(StreamingQueryParamDiscriminatorResponse, streaming, path=["response"])

    @parametrize
    def test_method_query_param_discriminator_with_all_params_overload_1(self, client: Sink) -> None:
        streaming = client.streaming.query_param_discriminator(
            prompt="prompt",
            should_stream=False,
        )
        assert_matches_type(StreamingQueryParamDiscriminatorResponse, streaming, path=["response"])

    @parametrize
    def test_raw_response_query_param_discriminator_overload_1(self, client: Sink) -> None:
        response = client.streaming.with_raw_response.query_param_discriminator(
            prompt="prompt",
        )

        assert response.is_closed is True
        streaming = response.parse()
        assert_matches_type(StreamingQueryParamDiscriminatorResponse, streaming, path=["response"])

    @parametrize
    def test_streaming_response_query_param_discriminator_overload_1(self, client: Sink) -> None:
        with client.streaming.with_streaming_response.query_param_discriminator(
            prompt="prompt",
        ) as response:
            assert not response.is_closed

            streaming = response.parse()
            assert_matches_type(StreamingQueryParamDiscriminatorResponse, streaming, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_query_param_discriminator_overload_2(self, client: Sink) -> None:
        streaming_stream = client.streaming.query_param_discriminator(
            prompt="prompt",
            should_stream=True,
        )
        streaming_stream.response.close()

    @parametrize
    def test_raw_response_query_param_discriminator_overload_2(self, client: Sink) -> None:
        response = client.streaming.with_raw_response.query_param_discriminator(
            prompt="prompt",
            should_stream=True,
        )

        stream = response.parse()
        stream.close()

    @parametrize
    def test_streaming_response_query_param_discriminator_overload_2(self, client: Sink) -> None:
        with client.streaming.with_streaming_response.query_param_discriminator(
            prompt="prompt",
            should_stream=True,
        ) as response:
            assert not response.is_closed

            stream = response.parse()
            stream.close()

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_with_unrelated_default_param_overload_1(self, client: Sink) -> None:
        streaming = client.streaming.with_unrelated_default_param(
            model="model",
            prompt="prompt",
        )
        assert_matches_type(StreamingWithUnrelatedDefaultParamResponse, streaming, path=["response"])

    @parametrize
    def test_method_with_unrelated_default_param_with_all_params_overload_1(self, client: Sink) -> None:
        streaming = client.streaming.with_unrelated_default_param(
            model="model",
            param_with_default_value="my_enum_value",
            prompt="prompt",
            stream=False,
        )
        assert_matches_type(StreamingWithUnrelatedDefaultParamResponse, streaming, path=["response"])

    @parametrize
    def test_raw_response_with_unrelated_default_param_overload_1(self, client: Sink) -> None:
        response = client.streaming.with_raw_response.with_unrelated_default_param(
            model="model",
            prompt="prompt",
        )

        assert response.is_closed is True
        streaming = response.parse()
        assert_matches_type(StreamingWithUnrelatedDefaultParamResponse, streaming, path=["response"])

    @parametrize
    def test_streaming_response_with_unrelated_default_param_overload_1(self, client: Sink) -> None:
        with client.streaming.with_streaming_response.with_unrelated_default_param(
            model="model",
            prompt="prompt",
        ) as response:
            assert not response.is_closed

            streaming = response.parse()
            assert_matches_type(StreamingWithUnrelatedDefaultParamResponse, streaming, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_with_unrelated_default_param_overload_2(self, client: Sink) -> None:
        streaming_stream = client.streaming.with_unrelated_default_param(
            model="model",
            prompt="prompt",
            stream=True,
        )
        streaming_stream.response.close()

    @parametrize
    def test_raw_response_with_unrelated_default_param_overload_2(self, client: Sink) -> None:
        response = client.streaming.with_raw_response.with_unrelated_default_param(
            model="model",
            prompt="prompt",
            stream=True,
        )

        stream = response.parse()
        stream.close()

    @parametrize
    def test_streaming_response_with_unrelated_default_param_overload_2(self, client: Sink) -> None:
        with client.streaming.with_streaming_response.with_unrelated_default_param(
            model="model",
            prompt="prompt",
            stream=True,
        ) as response:
            assert not response.is_closed

            stream = response.parse()
            stream.close()

        assert cast(Any, response.is_closed) is True


class TestAsyncStreaming:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_basic_overload_1(self, async_client: AsyncSink) -> None:
        streaming = await async_client.streaming.basic(
            model="model",
            prompt="prompt",
        )
        assert_matches_type(StreamingBasicResponse, streaming, path=["response"])

    @parametrize
    async def test_method_basic_with_all_params_overload_1(self, async_client: AsyncSink) -> None:
        streaming = await async_client.streaming.basic(
            model="model",
            prompt="prompt",
            stream=False,
        )
        assert_matches_type(StreamingBasicResponse, streaming, path=["response"])

    @parametrize
    async def test_raw_response_basic_overload_1(self, async_client: AsyncSink) -> None:
        response = await async_client.streaming.with_raw_response.basic(
            model="model",
            prompt="prompt",
        )

        assert response.is_closed is True
        streaming = response.parse()
        assert_matches_type(StreamingBasicResponse, streaming, path=["response"])

    @parametrize
    async def test_streaming_response_basic_overload_1(self, async_client: AsyncSink) -> None:
        async with async_client.streaming.with_streaming_response.basic(
            model="model",
            prompt="prompt",
        ) as response:
            assert not response.is_closed

            streaming = await response.parse()
            assert_matches_type(StreamingBasicResponse, streaming, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_basic_overload_2(self, async_client: AsyncSink) -> None:
        streaming_stream = await async_client.streaming.basic(
            model="model",
            prompt="prompt",
            stream=True,
        )
        await streaming_stream.response.aclose()

    @parametrize
    async def test_raw_response_basic_overload_2(self, async_client: AsyncSink) -> None:
        response = await async_client.streaming.with_raw_response.basic(
            model="model",
            prompt="prompt",
            stream=True,
        )

        stream = response.parse()
        await stream.close()

    @parametrize
    async def test_streaming_response_basic_overload_2(self, async_client: AsyncSink) -> None:
        async with async_client.streaming.with_streaming_response.basic(
            model="model",
            prompt="prompt",
            stream=True,
        ) as response:
            assert not response.is_closed

            stream = await response.parse()
            await stream.close()

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_nested_params_overload_1(self, async_client: AsyncSink) -> None:
        streaming = await async_client.streaming.nested_params(
            model="model",
            prompt="prompt",
        )
        assert_matches_type(StreamingNestedParamsResponse, streaming, path=["response"])

    @parametrize
    async def test_method_nested_params_with_all_params_overload_1(self, async_client: AsyncSink) -> None:
        streaming = await async_client.streaming.nested_params(
            model="model",
            prompt="prompt",
            parent_object={
                "array_prop": [{"from_array_items": True}],
                "child_prop": {"from_object": "from_object"},
            },
            stream=False,
        )
        assert_matches_type(StreamingNestedParamsResponse, streaming, path=["response"])

    @parametrize
    async def test_raw_response_nested_params_overload_1(self, async_client: AsyncSink) -> None:
        response = await async_client.streaming.with_raw_response.nested_params(
            model="model",
            prompt="prompt",
        )

        assert response.is_closed is True
        streaming = response.parse()
        assert_matches_type(StreamingNestedParamsResponse, streaming, path=["response"])

    @parametrize
    async def test_streaming_response_nested_params_overload_1(self, async_client: AsyncSink) -> None:
        async with async_client.streaming.with_streaming_response.nested_params(
            model="model",
            prompt="prompt",
        ) as response:
            assert not response.is_closed

            streaming = await response.parse()
            assert_matches_type(StreamingNestedParamsResponse, streaming, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_nested_params_overload_2(self, async_client: AsyncSink) -> None:
        streaming_stream = await async_client.streaming.nested_params(
            model="model",
            prompt="prompt",
            stream=True,
        )
        await streaming_stream.response.aclose()

    @parametrize
    async def test_method_nested_params_with_all_params_overload_2(self, async_client: AsyncSink) -> None:
        streaming_stream = await async_client.streaming.nested_params(
            model="model",
            prompt="prompt",
            stream=True,
            parent_object={
                "array_prop": [{"from_array_items": True}],
                "child_prop": {"from_object": "from_object"},
            },
        )
        await streaming_stream.response.aclose()

    @parametrize
    async def test_raw_response_nested_params_overload_2(self, async_client: AsyncSink) -> None:
        response = await async_client.streaming.with_raw_response.nested_params(
            model="model",
            prompt="prompt",
            stream=True,
        )

        stream = response.parse()
        await stream.close()

    @parametrize
    async def test_streaming_response_nested_params_overload_2(self, async_client: AsyncSink) -> None:
        async with async_client.streaming.with_streaming_response.nested_params(
            model="model",
            prompt="prompt",
            stream=True,
        ) as response:
            assert not response.is_closed

            stream = await response.parse()
            await stream.close()

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_no_discriminator(self, async_client: AsyncSink) -> None:
        streaming_stream = await async_client.streaming.no_discriminator(
            model="model",
            prompt="prompt",
        )
        await streaming_stream.response.aclose()

    @parametrize
    async def test_raw_response_no_discriminator(self, async_client: AsyncSink) -> None:
        response = await async_client.streaming.with_raw_response.no_discriminator(
            model="model",
            prompt="prompt",
        )

        stream = response.parse()
        await stream.close()

    @parametrize
    async def test_streaming_response_no_discriminator(self, async_client: AsyncSink) -> None:
        async with async_client.streaming.with_streaming_response.no_discriminator(
            model="model",
            prompt="prompt",
        ) as response:
            assert not response.is_closed

            stream = await response.parse()
            await stream.close()

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_query_param_discriminator_overload_1(self, async_client: AsyncSink) -> None:
        streaming = await async_client.streaming.query_param_discriminator(
            prompt="prompt",
        )
        assert_matches_type(StreamingQueryParamDiscriminatorResponse, streaming, path=["response"])

    @parametrize
    async def test_method_query_param_discriminator_with_all_params_overload_1(self, async_client: AsyncSink) -> None:
        streaming = await async_client.streaming.query_param_discriminator(
            prompt="prompt",
            should_stream=False,
        )
        assert_matches_type(StreamingQueryParamDiscriminatorResponse, streaming, path=["response"])

    @parametrize
    async def test_raw_response_query_param_discriminator_overload_1(self, async_client: AsyncSink) -> None:
        response = await async_client.streaming.with_raw_response.query_param_discriminator(
            prompt="prompt",
        )

        assert response.is_closed is True
        streaming = response.parse()
        assert_matches_type(StreamingQueryParamDiscriminatorResponse, streaming, path=["response"])

    @parametrize
    async def test_streaming_response_query_param_discriminator_overload_1(self, async_client: AsyncSink) -> None:
        async with async_client.streaming.with_streaming_response.query_param_discriminator(
            prompt="prompt",
        ) as response:
            assert not response.is_closed

            streaming = await response.parse()
            assert_matches_type(StreamingQueryParamDiscriminatorResponse, streaming, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_query_param_discriminator_overload_2(self, async_client: AsyncSink) -> None:
        streaming_stream = await async_client.streaming.query_param_discriminator(
            prompt="prompt",
            should_stream=True,
        )
        await streaming_stream.response.aclose()

    @parametrize
    async def test_raw_response_query_param_discriminator_overload_2(self, async_client: AsyncSink) -> None:
        response = await async_client.streaming.with_raw_response.query_param_discriminator(
            prompt="prompt",
            should_stream=True,
        )

        stream = response.parse()
        await stream.close()

    @parametrize
    async def test_streaming_response_query_param_discriminator_overload_2(self, async_client: AsyncSink) -> None:
        async with async_client.streaming.with_streaming_response.query_param_discriminator(
            prompt="prompt",
            should_stream=True,
        ) as response:
            assert not response.is_closed

            stream = await response.parse()
            await stream.close()

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_with_unrelated_default_param_overload_1(self, async_client: AsyncSink) -> None:
        streaming = await async_client.streaming.with_unrelated_default_param(
            model="model",
            prompt="prompt",
        )
        assert_matches_type(StreamingWithUnrelatedDefaultParamResponse, streaming, path=["response"])

    @parametrize
    async def test_method_with_unrelated_default_param_with_all_params_overload_1(
        self, async_client: AsyncSink
    ) -> None:
        streaming = await async_client.streaming.with_unrelated_default_param(
            model="model",
            param_with_default_value="my_enum_value",
            prompt="prompt",
            stream=False,
        )
        assert_matches_type(StreamingWithUnrelatedDefaultParamResponse, streaming, path=["response"])

    @parametrize
    async def test_raw_response_with_unrelated_default_param_overload_1(self, async_client: AsyncSink) -> None:
        response = await async_client.streaming.with_raw_response.with_unrelated_default_param(
            model="model",
            prompt="prompt",
        )

        assert response.is_closed is True
        streaming = response.parse()
        assert_matches_type(StreamingWithUnrelatedDefaultParamResponse, streaming, path=["response"])

    @parametrize
    async def test_streaming_response_with_unrelated_default_param_overload_1(self, async_client: AsyncSink) -> None:
        async with async_client.streaming.with_streaming_response.with_unrelated_default_param(
            model="model",
            prompt="prompt",
        ) as response:
            assert not response.is_closed

            streaming = await response.parse()
            assert_matches_type(StreamingWithUnrelatedDefaultParamResponse, streaming, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_with_unrelated_default_param_overload_2(self, async_client: AsyncSink) -> None:
        streaming_stream = await async_client.streaming.with_unrelated_default_param(
            model="model",
            prompt="prompt",
            stream=True,
        )
        await streaming_stream.response.aclose()

    @parametrize
    async def test_raw_response_with_unrelated_default_param_overload_2(self, async_client: AsyncSink) -> None:
        response = await async_client.streaming.with_raw_response.with_unrelated_default_param(
            model="model",
            prompt="prompt",
            stream=True,
        )

        stream = response.parse()
        await stream.close()

    @parametrize
    async def test_streaming_response_with_unrelated_default_param_overload_2(self, async_client: AsyncSink) -> None:
        async with async_client.streaming.with_streaming_response.with_unrelated_default_param(
            model="model",
            prompt="prompt",
            stream=True,
        ) as response:
            assert not response.is_closed

            stream = await response.parse()
            await stream.close()

        assert cast(Any, response.is_closed) is True
