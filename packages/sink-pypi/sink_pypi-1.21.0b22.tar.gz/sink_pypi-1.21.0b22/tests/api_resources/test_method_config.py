# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import (
    Card,
    MethodConfigSkippedTestsGoResponse,
    MethodConfigSkippedTestsAllResponse,
    MethodConfigSkippedTestsJavaResponse,
    MethodConfigSkippedTestsNodeResponse,
    MethodConfigSkippedTestsRubyResponse,
    MethodConfigSkippedTestsKotlinResponse,
    MethodConfigSkippedTestsPythonResponse,
    MethodConfigSkippedTestsNodeAndPythonResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMethodConfig:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_should_not_show_up_in_api_docs(self, client: Sink) -> None:
        method_config = client.method_config.should_not_show_up_in_api_docs(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Card, method_config, path=["response"])

    @parametrize
    def test_method_should_not_show_up_in_api_docs_with_all_params(self, client: Sink) -> None:
        method_config = client.method_config.should_not_show_up_in_api_docs(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            product_id="product_id",
            shipping_method="STANDARD",
            shipping_address={
                "address1": "5 Broad Street",
                "city": "NEW YORK",
                "country": "USA",
                "first_name": "Michael",
                "last_name": "Bluth",
                "postal_code": "10001-1809",
                "state": "NY",
                "address2": "Unit 25A",
                "email": "johnny@appleseed.com",
                "line2_text": "The Bluth Company",
                "phone_number": "+12124007676",
            },
        )
        assert_matches_type(Card, method_config, path=["response"])

    @parametrize
    def test_raw_response_should_not_show_up_in_api_docs(self, client: Sink) -> None:
        response = client.method_config.with_raw_response.should_not_show_up_in_api_docs(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        method_config = response.parse()
        assert_matches_type(Card, method_config, path=["response"])

    @parametrize
    def test_streaming_response_should_not_show_up_in_api_docs(self, client: Sink) -> None:
        with client.method_config.with_streaming_response.should_not_show_up_in_api_docs(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed

            method_config = response.parse()
            assert_matches_type(Card, method_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_should_not_show_up_in_api_docs(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_token` but received ''"):
            client.method_config.with_raw_response.should_not_show_up_in_api_docs(
                card_token="",
            )

    @pytest.mark.skip(reason="Because of this error")
    @parametrize
    def test_method_skipped_tests_all(self, client: Sink) -> None:
        method_config = client.method_config.skipped_tests_all(
            "id",
        )
        assert_matches_type(MethodConfigSkippedTestsAllResponse, method_config, path=["response"])

    @pytest.mark.skip(reason="Because of this error")
    @parametrize
    def test_raw_response_skipped_tests_all(self, client: Sink) -> None:
        response = client.method_config.with_raw_response.skipped_tests_all(
            "id",
        )

        assert response.is_closed is True
        method_config = response.parse()
        assert_matches_type(MethodConfigSkippedTestsAllResponse, method_config, path=["response"])

    @pytest.mark.skip(reason="Because of this error")
    @parametrize
    def test_streaming_response_skipped_tests_all(self, client: Sink) -> None:
        with client.method_config.with_streaming_response.skipped_tests_all(
            "id",
        ) as response:
            assert not response.is_closed

            method_config = response.parse()
            assert_matches_type(MethodConfigSkippedTestsAllResponse, method_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Because of this error")
    @parametrize
    def test_path_params_skipped_tests_all(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.method_config.with_raw_response.skipped_tests_all(
                "",
            )

    @parametrize
    def test_method_skipped_tests_go(self, client: Sink) -> None:
        method_config = client.method_config.skipped_tests_go(
            "id",
        )
        assert_matches_type(MethodConfigSkippedTestsGoResponse, method_config, path=["response"])

    @parametrize
    def test_raw_response_skipped_tests_go(self, client: Sink) -> None:
        response = client.method_config.with_raw_response.skipped_tests_go(
            "id",
        )

        assert response.is_closed is True
        method_config = response.parse()
        assert_matches_type(MethodConfigSkippedTestsGoResponse, method_config, path=["response"])

    @parametrize
    def test_streaming_response_skipped_tests_go(self, client: Sink) -> None:
        with client.method_config.with_streaming_response.skipped_tests_go(
            "id",
        ) as response:
            assert not response.is_closed

            method_config = response.parse()
            assert_matches_type(MethodConfigSkippedTestsGoResponse, method_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_skipped_tests_go(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.method_config.with_raw_response.skipped_tests_go(
                "",
            )

    @parametrize
    def test_method_skipped_tests_java(self, client: Sink) -> None:
        method_config = client.method_config.skipped_tests_java(
            "id",
        )
        assert_matches_type(MethodConfigSkippedTestsJavaResponse, method_config, path=["response"])

    @parametrize
    def test_raw_response_skipped_tests_java(self, client: Sink) -> None:
        response = client.method_config.with_raw_response.skipped_tests_java(
            "id",
        )

        assert response.is_closed is True
        method_config = response.parse()
        assert_matches_type(MethodConfigSkippedTestsJavaResponse, method_config, path=["response"])

    @parametrize
    def test_streaming_response_skipped_tests_java(self, client: Sink) -> None:
        with client.method_config.with_streaming_response.skipped_tests_java(
            "id",
        ) as response:
            assert not response.is_closed

            method_config = response.parse()
            assert_matches_type(MethodConfigSkippedTestsJavaResponse, method_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_skipped_tests_java(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.method_config.with_raw_response.skipped_tests_java(
                "",
            )

    @parametrize
    def test_method_skipped_tests_kotlin(self, client: Sink) -> None:
        method_config = client.method_config.skipped_tests_kotlin(
            "id",
        )
        assert_matches_type(MethodConfigSkippedTestsKotlinResponse, method_config, path=["response"])

    @parametrize
    def test_raw_response_skipped_tests_kotlin(self, client: Sink) -> None:
        response = client.method_config.with_raw_response.skipped_tests_kotlin(
            "id",
        )

        assert response.is_closed is True
        method_config = response.parse()
        assert_matches_type(MethodConfigSkippedTestsKotlinResponse, method_config, path=["response"])

    @parametrize
    def test_streaming_response_skipped_tests_kotlin(self, client: Sink) -> None:
        with client.method_config.with_streaming_response.skipped_tests_kotlin(
            "id",
        ) as response:
            assert not response.is_closed

            method_config = response.parse()
            assert_matches_type(MethodConfigSkippedTestsKotlinResponse, method_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_skipped_tests_kotlin(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.method_config.with_raw_response.skipped_tests_kotlin(
                "",
            )

    @parametrize
    def test_method_skipped_tests_node(self, client: Sink) -> None:
        method_config = client.method_config.skipped_tests_node(
            "id",
        )
        assert_matches_type(MethodConfigSkippedTestsNodeResponse, method_config, path=["response"])

    @parametrize
    def test_raw_response_skipped_tests_node(self, client: Sink) -> None:
        response = client.method_config.with_raw_response.skipped_tests_node(
            "id",
        )

        assert response.is_closed is True
        method_config = response.parse()
        assert_matches_type(MethodConfigSkippedTestsNodeResponse, method_config, path=["response"])

    @parametrize
    def test_streaming_response_skipped_tests_node(self, client: Sink) -> None:
        with client.method_config.with_streaming_response.skipped_tests_node(
            "id",
        ) as response:
            assert not response.is_closed

            method_config = response.parse()
            assert_matches_type(MethodConfigSkippedTestsNodeResponse, method_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_skipped_tests_node(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.method_config.with_raw_response.skipped_tests_node(
                "",
            )

    @pytest.mark.skip(reason="Because of this other error")
    @parametrize
    def test_method_skipped_tests_node_and_python(self, client: Sink) -> None:
        method_config = client.method_config.skipped_tests_node_and_python(
            "id",
        )
        assert_matches_type(MethodConfigSkippedTestsNodeAndPythonResponse, method_config, path=["response"])

    @pytest.mark.skip(reason="Because of this other error")
    @parametrize
    def test_raw_response_skipped_tests_node_and_python(self, client: Sink) -> None:
        response = client.method_config.with_raw_response.skipped_tests_node_and_python(
            "id",
        )

        assert response.is_closed is True
        method_config = response.parse()
        assert_matches_type(MethodConfigSkippedTestsNodeAndPythonResponse, method_config, path=["response"])

    @pytest.mark.skip(reason="Because of this other error")
    @parametrize
    def test_streaming_response_skipped_tests_node_and_python(self, client: Sink) -> None:
        with client.method_config.with_streaming_response.skipped_tests_node_and_python(
            "id",
        ) as response:
            assert not response.is_closed

            method_config = response.parse()
            assert_matches_type(MethodConfigSkippedTestsNodeAndPythonResponse, method_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Because of this other error")
    @parametrize
    def test_path_params_skipped_tests_node_and_python(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.method_config.with_raw_response.skipped_tests_node_and_python(
                "",
            )

    @pytest.mark.skip(reason="Because of this error")
    @parametrize
    def test_method_skipped_tests_python(self, client: Sink) -> None:
        method_config = client.method_config.skipped_tests_python(
            "id",
        )
        assert_matches_type(MethodConfigSkippedTestsPythonResponse, method_config, path=["response"])

    @pytest.mark.skip(reason="Because of this error")
    @parametrize
    def test_raw_response_skipped_tests_python(self, client: Sink) -> None:
        response = client.method_config.with_raw_response.skipped_tests_python(
            "id",
        )

        assert response.is_closed is True
        method_config = response.parse()
        assert_matches_type(MethodConfigSkippedTestsPythonResponse, method_config, path=["response"])

    @pytest.mark.skip(reason="Because of this error")
    @parametrize
    def test_streaming_response_skipped_tests_python(self, client: Sink) -> None:
        with client.method_config.with_streaming_response.skipped_tests_python(
            "id",
        ) as response:
            assert not response.is_closed

            method_config = response.parse()
            assert_matches_type(MethodConfigSkippedTestsPythonResponse, method_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Because of this error")
    @parametrize
    def test_path_params_skipped_tests_python(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.method_config.with_raw_response.skipped_tests_python(
                "",
            )

    @parametrize
    def test_method_skipped_tests_ruby(self, client: Sink) -> None:
        method_config = client.method_config.skipped_tests_ruby(
            "id",
        )
        assert_matches_type(MethodConfigSkippedTestsRubyResponse, method_config, path=["response"])

    @parametrize
    def test_raw_response_skipped_tests_ruby(self, client: Sink) -> None:
        response = client.method_config.with_raw_response.skipped_tests_ruby(
            "id",
        )

        assert response.is_closed is True
        method_config = response.parse()
        assert_matches_type(MethodConfigSkippedTestsRubyResponse, method_config, path=["response"])

    @parametrize
    def test_streaming_response_skipped_tests_ruby(self, client: Sink) -> None:
        with client.method_config.with_streaming_response.skipped_tests_ruby(
            "id",
        ) as response:
            assert not response.is_closed

            method_config = response.parse()
            assert_matches_type(MethodConfigSkippedTestsRubyResponse, method_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_skipped_tests_ruby(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.method_config.with_raw_response.skipped_tests_ruby(
                "",
            )


class TestAsyncMethodConfig:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_should_not_show_up_in_api_docs(self, async_client: AsyncSink) -> None:
        method_config = await async_client.method_config.should_not_show_up_in_api_docs(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Card, method_config, path=["response"])

    @parametrize
    async def test_method_should_not_show_up_in_api_docs_with_all_params(self, async_client: AsyncSink) -> None:
        method_config = await async_client.method_config.should_not_show_up_in_api_docs(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            product_id="product_id",
            shipping_method="STANDARD",
            shipping_address={
                "address1": "5 Broad Street",
                "city": "NEW YORK",
                "country": "USA",
                "first_name": "Michael",
                "last_name": "Bluth",
                "postal_code": "10001-1809",
                "state": "NY",
                "address2": "Unit 25A",
                "email": "johnny@appleseed.com",
                "line2_text": "The Bluth Company",
                "phone_number": "+12124007676",
            },
        )
        assert_matches_type(Card, method_config, path=["response"])

    @parametrize
    async def test_raw_response_should_not_show_up_in_api_docs(self, async_client: AsyncSink) -> None:
        response = await async_client.method_config.with_raw_response.should_not_show_up_in_api_docs(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        method_config = response.parse()
        assert_matches_type(Card, method_config, path=["response"])

    @parametrize
    async def test_streaming_response_should_not_show_up_in_api_docs(self, async_client: AsyncSink) -> None:
        async with async_client.method_config.with_streaming_response.should_not_show_up_in_api_docs(
            card_token="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed

            method_config = await response.parse()
            assert_matches_type(Card, method_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_should_not_show_up_in_api_docs(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `card_token` but received ''"):
            await async_client.method_config.with_raw_response.should_not_show_up_in_api_docs(
                card_token="",
            )

    @pytest.mark.skip(reason="Because of this error")
    @parametrize
    async def test_method_skipped_tests_all(self, async_client: AsyncSink) -> None:
        method_config = await async_client.method_config.skipped_tests_all(
            "id",
        )
        assert_matches_type(MethodConfigSkippedTestsAllResponse, method_config, path=["response"])

    @pytest.mark.skip(reason="Because of this error")
    @parametrize
    async def test_raw_response_skipped_tests_all(self, async_client: AsyncSink) -> None:
        response = await async_client.method_config.with_raw_response.skipped_tests_all(
            "id",
        )

        assert response.is_closed is True
        method_config = response.parse()
        assert_matches_type(MethodConfigSkippedTestsAllResponse, method_config, path=["response"])

    @pytest.mark.skip(reason="Because of this error")
    @parametrize
    async def test_streaming_response_skipped_tests_all(self, async_client: AsyncSink) -> None:
        async with async_client.method_config.with_streaming_response.skipped_tests_all(
            "id",
        ) as response:
            assert not response.is_closed

            method_config = await response.parse()
            assert_matches_type(MethodConfigSkippedTestsAllResponse, method_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Because of this error")
    @parametrize
    async def test_path_params_skipped_tests_all(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.method_config.with_raw_response.skipped_tests_all(
                "",
            )

    @parametrize
    async def test_method_skipped_tests_go(self, async_client: AsyncSink) -> None:
        method_config = await async_client.method_config.skipped_tests_go(
            "id",
        )
        assert_matches_type(MethodConfigSkippedTestsGoResponse, method_config, path=["response"])

    @parametrize
    async def test_raw_response_skipped_tests_go(self, async_client: AsyncSink) -> None:
        response = await async_client.method_config.with_raw_response.skipped_tests_go(
            "id",
        )

        assert response.is_closed is True
        method_config = response.parse()
        assert_matches_type(MethodConfigSkippedTestsGoResponse, method_config, path=["response"])

    @parametrize
    async def test_streaming_response_skipped_tests_go(self, async_client: AsyncSink) -> None:
        async with async_client.method_config.with_streaming_response.skipped_tests_go(
            "id",
        ) as response:
            assert not response.is_closed

            method_config = await response.parse()
            assert_matches_type(MethodConfigSkippedTestsGoResponse, method_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_skipped_tests_go(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.method_config.with_raw_response.skipped_tests_go(
                "",
            )

    @parametrize
    async def test_method_skipped_tests_java(self, async_client: AsyncSink) -> None:
        method_config = await async_client.method_config.skipped_tests_java(
            "id",
        )
        assert_matches_type(MethodConfigSkippedTestsJavaResponse, method_config, path=["response"])

    @parametrize
    async def test_raw_response_skipped_tests_java(self, async_client: AsyncSink) -> None:
        response = await async_client.method_config.with_raw_response.skipped_tests_java(
            "id",
        )

        assert response.is_closed is True
        method_config = response.parse()
        assert_matches_type(MethodConfigSkippedTestsJavaResponse, method_config, path=["response"])

    @parametrize
    async def test_streaming_response_skipped_tests_java(self, async_client: AsyncSink) -> None:
        async with async_client.method_config.with_streaming_response.skipped_tests_java(
            "id",
        ) as response:
            assert not response.is_closed

            method_config = await response.parse()
            assert_matches_type(MethodConfigSkippedTestsJavaResponse, method_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_skipped_tests_java(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.method_config.with_raw_response.skipped_tests_java(
                "",
            )

    @parametrize
    async def test_method_skipped_tests_kotlin(self, async_client: AsyncSink) -> None:
        method_config = await async_client.method_config.skipped_tests_kotlin(
            "id",
        )
        assert_matches_type(MethodConfigSkippedTestsKotlinResponse, method_config, path=["response"])

    @parametrize
    async def test_raw_response_skipped_tests_kotlin(self, async_client: AsyncSink) -> None:
        response = await async_client.method_config.with_raw_response.skipped_tests_kotlin(
            "id",
        )

        assert response.is_closed is True
        method_config = response.parse()
        assert_matches_type(MethodConfigSkippedTestsKotlinResponse, method_config, path=["response"])

    @parametrize
    async def test_streaming_response_skipped_tests_kotlin(self, async_client: AsyncSink) -> None:
        async with async_client.method_config.with_streaming_response.skipped_tests_kotlin(
            "id",
        ) as response:
            assert not response.is_closed

            method_config = await response.parse()
            assert_matches_type(MethodConfigSkippedTestsKotlinResponse, method_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_skipped_tests_kotlin(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.method_config.with_raw_response.skipped_tests_kotlin(
                "",
            )

    @parametrize
    async def test_method_skipped_tests_node(self, async_client: AsyncSink) -> None:
        method_config = await async_client.method_config.skipped_tests_node(
            "id",
        )
        assert_matches_type(MethodConfigSkippedTestsNodeResponse, method_config, path=["response"])

    @parametrize
    async def test_raw_response_skipped_tests_node(self, async_client: AsyncSink) -> None:
        response = await async_client.method_config.with_raw_response.skipped_tests_node(
            "id",
        )

        assert response.is_closed is True
        method_config = response.parse()
        assert_matches_type(MethodConfigSkippedTestsNodeResponse, method_config, path=["response"])

    @parametrize
    async def test_streaming_response_skipped_tests_node(self, async_client: AsyncSink) -> None:
        async with async_client.method_config.with_streaming_response.skipped_tests_node(
            "id",
        ) as response:
            assert not response.is_closed

            method_config = await response.parse()
            assert_matches_type(MethodConfigSkippedTestsNodeResponse, method_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_skipped_tests_node(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.method_config.with_raw_response.skipped_tests_node(
                "",
            )

    @pytest.mark.skip(reason="Because of this other error")
    @parametrize
    async def test_method_skipped_tests_node_and_python(self, async_client: AsyncSink) -> None:
        method_config = await async_client.method_config.skipped_tests_node_and_python(
            "id",
        )
        assert_matches_type(MethodConfigSkippedTestsNodeAndPythonResponse, method_config, path=["response"])

    @pytest.mark.skip(reason="Because of this other error")
    @parametrize
    async def test_raw_response_skipped_tests_node_and_python(self, async_client: AsyncSink) -> None:
        response = await async_client.method_config.with_raw_response.skipped_tests_node_and_python(
            "id",
        )

        assert response.is_closed is True
        method_config = response.parse()
        assert_matches_type(MethodConfigSkippedTestsNodeAndPythonResponse, method_config, path=["response"])

    @pytest.mark.skip(reason="Because of this other error")
    @parametrize
    async def test_streaming_response_skipped_tests_node_and_python(self, async_client: AsyncSink) -> None:
        async with async_client.method_config.with_streaming_response.skipped_tests_node_and_python(
            "id",
        ) as response:
            assert not response.is_closed

            method_config = await response.parse()
            assert_matches_type(MethodConfigSkippedTestsNodeAndPythonResponse, method_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Because of this other error")
    @parametrize
    async def test_path_params_skipped_tests_node_and_python(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.method_config.with_raw_response.skipped_tests_node_and_python(
                "",
            )

    @pytest.mark.skip(reason="Because of this error")
    @parametrize
    async def test_method_skipped_tests_python(self, async_client: AsyncSink) -> None:
        method_config = await async_client.method_config.skipped_tests_python(
            "id",
        )
        assert_matches_type(MethodConfigSkippedTestsPythonResponse, method_config, path=["response"])

    @pytest.mark.skip(reason="Because of this error")
    @parametrize
    async def test_raw_response_skipped_tests_python(self, async_client: AsyncSink) -> None:
        response = await async_client.method_config.with_raw_response.skipped_tests_python(
            "id",
        )

        assert response.is_closed is True
        method_config = response.parse()
        assert_matches_type(MethodConfigSkippedTestsPythonResponse, method_config, path=["response"])

    @pytest.mark.skip(reason="Because of this error")
    @parametrize
    async def test_streaming_response_skipped_tests_python(self, async_client: AsyncSink) -> None:
        async with async_client.method_config.with_streaming_response.skipped_tests_python(
            "id",
        ) as response:
            assert not response.is_closed

            method_config = await response.parse()
            assert_matches_type(MethodConfigSkippedTestsPythonResponse, method_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Because of this error")
    @parametrize
    async def test_path_params_skipped_tests_python(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.method_config.with_raw_response.skipped_tests_python(
                "",
            )

    @parametrize
    async def test_method_skipped_tests_ruby(self, async_client: AsyncSink) -> None:
        method_config = await async_client.method_config.skipped_tests_ruby(
            "id",
        )
        assert_matches_type(MethodConfigSkippedTestsRubyResponse, method_config, path=["response"])

    @parametrize
    async def test_raw_response_skipped_tests_ruby(self, async_client: AsyncSink) -> None:
        response = await async_client.method_config.with_raw_response.skipped_tests_ruby(
            "id",
        )

        assert response.is_closed is True
        method_config = response.parse()
        assert_matches_type(MethodConfigSkippedTestsRubyResponse, method_config, path=["response"])

    @parametrize
    async def test_streaming_response_skipped_tests_ruby(self, async_client: AsyncSink) -> None:
        async with async_client.method_config.with_streaming_response.skipped_tests_ruby(
            "id",
        ) as response:
            assert not response.is_closed

            method_config = await response.parse()
            assert_matches_type(MethodConfigSkippedTestsRubyResponse, method_config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_skipped_tests_ruby(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.method_config.with_raw_response.skipped_tests_ruby(
                "",
            )
