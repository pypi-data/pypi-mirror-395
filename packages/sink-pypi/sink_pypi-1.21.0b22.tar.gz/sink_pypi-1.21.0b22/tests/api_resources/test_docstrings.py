# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import DocstringLeadingDoubleQuoteResponse, DocstringTrailingDoubleQuoteResponse
from sink.api.sdk.types.shared import BasicSharedModelObject

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDocstrings:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_description_contains_js_doc(self, client: Sink) -> None:
        docstring = client.docstrings.description_contains_js_doc()
        assert_matches_type(BasicSharedModelObject, docstring, path=["response"])

    @parametrize
    def test_raw_response_description_contains_js_doc(self, client: Sink) -> None:
        response = client.docstrings.with_raw_response.description_contains_js_doc()

        assert response.is_closed is True
        docstring = response.parse()
        assert_matches_type(BasicSharedModelObject, docstring, path=["response"])

    @parametrize
    def test_streaming_response_description_contains_js_doc(self, client: Sink) -> None:
        with client.docstrings.with_streaming_response.description_contains_js_doc() as response:
            assert not response.is_closed

            docstring = response.parse()
            assert_matches_type(BasicSharedModelObject, docstring, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_description_contains_js_doc_end(self, client: Sink) -> None:
        docstring = client.docstrings.description_contains_js_doc_end()
        assert_matches_type(BasicSharedModelObject, docstring, path=["response"])

    @parametrize
    def test_raw_response_description_contains_js_doc_end(self, client: Sink) -> None:
        response = client.docstrings.with_raw_response.description_contains_js_doc_end()

        assert response.is_closed is True
        docstring = response.parse()
        assert_matches_type(BasicSharedModelObject, docstring, path=["response"])

    @parametrize
    def test_streaming_response_description_contains_js_doc_end(self, client: Sink) -> None:
        with client.docstrings.with_streaming_response.description_contains_js_doc_end() as response:
            assert not response.is_closed

            docstring = response.parse()
            assert_matches_type(BasicSharedModelObject, docstring, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_leading_double_quote(self, client: Sink) -> None:
        docstring = client.docstrings.leading_double_quote()
        assert_matches_type(DocstringLeadingDoubleQuoteResponse, docstring, path=["response"])

    @parametrize
    def test_raw_response_leading_double_quote(self, client: Sink) -> None:
        response = client.docstrings.with_raw_response.leading_double_quote()

        assert response.is_closed is True
        docstring = response.parse()
        assert_matches_type(DocstringLeadingDoubleQuoteResponse, docstring, path=["response"])

    @parametrize
    def test_streaming_response_leading_double_quote(self, client: Sink) -> None:
        with client.docstrings.with_streaming_response.leading_double_quote() as response:
            assert not response.is_closed

            docstring = response.parse()
            assert_matches_type(DocstringLeadingDoubleQuoteResponse, docstring, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_trailing_double_quote(self, client: Sink) -> None:
        docstring = client.docstrings.trailing_double_quote()
        assert_matches_type(DocstringTrailingDoubleQuoteResponse, docstring, path=["response"])

    @parametrize
    def test_raw_response_trailing_double_quote(self, client: Sink) -> None:
        response = client.docstrings.with_raw_response.trailing_double_quote()

        assert response.is_closed is True
        docstring = response.parse()
        assert_matches_type(DocstringTrailingDoubleQuoteResponse, docstring, path=["response"])

    @parametrize
    def test_streaming_response_trailing_double_quote(self, client: Sink) -> None:
        with client.docstrings.with_streaming_response.trailing_double_quote() as response:
            assert not response.is_closed

            docstring = response.parse()
            assert_matches_type(DocstringTrailingDoubleQuoteResponse, docstring, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDocstrings:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_description_contains_js_doc(self, async_client: AsyncSink) -> None:
        docstring = await async_client.docstrings.description_contains_js_doc()
        assert_matches_type(BasicSharedModelObject, docstring, path=["response"])

    @parametrize
    async def test_raw_response_description_contains_js_doc(self, async_client: AsyncSink) -> None:
        response = await async_client.docstrings.with_raw_response.description_contains_js_doc()

        assert response.is_closed is True
        docstring = response.parse()
        assert_matches_type(BasicSharedModelObject, docstring, path=["response"])

    @parametrize
    async def test_streaming_response_description_contains_js_doc(self, async_client: AsyncSink) -> None:
        async with async_client.docstrings.with_streaming_response.description_contains_js_doc() as response:
            assert not response.is_closed

            docstring = await response.parse()
            assert_matches_type(BasicSharedModelObject, docstring, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_description_contains_js_doc_end(self, async_client: AsyncSink) -> None:
        docstring = await async_client.docstrings.description_contains_js_doc_end()
        assert_matches_type(BasicSharedModelObject, docstring, path=["response"])

    @parametrize
    async def test_raw_response_description_contains_js_doc_end(self, async_client: AsyncSink) -> None:
        response = await async_client.docstrings.with_raw_response.description_contains_js_doc_end()

        assert response.is_closed is True
        docstring = response.parse()
        assert_matches_type(BasicSharedModelObject, docstring, path=["response"])

    @parametrize
    async def test_streaming_response_description_contains_js_doc_end(self, async_client: AsyncSink) -> None:
        async with async_client.docstrings.with_streaming_response.description_contains_js_doc_end() as response:
            assert not response.is_closed

            docstring = await response.parse()
            assert_matches_type(BasicSharedModelObject, docstring, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_leading_double_quote(self, async_client: AsyncSink) -> None:
        docstring = await async_client.docstrings.leading_double_quote()
        assert_matches_type(DocstringLeadingDoubleQuoteResponse, docstring, path=["response"])

    @parametrize
    async def test_raw_response_leading_double_quote(self, async_client: AsyncSink) -> None:
        response = await async_client.docstrings.with_raw_response.leading_double_quote()

        assert response.is_closed is True
        docstring = response.parse()
        assert_matches_type(DocstringLeadingDoubleQuoteResponse, docstring, path=["response"])

    @parametrize
    async def test_streaming_response_leading_double_quote(self, async_client: AsyncSink) -> None:
        async with async_client.docstrings.with_streaming_response.leading_double_quote() as response:
            assert not response.is_closed

            docstring = await response.parse()
            assert_matches_type(DocstringLeadingDoubleQuoteResponse, docstring, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_trailing_double_quote(self, async_client: AsyncSink) -> None:
        docstring = await async_client.docstrings.trailing_double_quote()
        assert_matches_type(DocstringTrailingDoubleQuoteResponse, docstring, path=["response"])

    @parametrize
    async def test_raw_response_trailing_double_quote(self, async_client: AsyncSink) -> None:
        response = await async_client.docstrings.with_raw_response.trailing_double_quote()

        assert response.is_closed is True
        docstring = response.parse()
        assert_matches_type(DocstringTrailingDoubleQuoteResponse, docstring, path=["response"])

    @parametrize
    async def test_streaming_response_trailing_double_quote(self, async_client: AsyncSink) -> None:
        async with async_client.docstrings.with_streaming_response.trailing_double_quote() as response:
            assert not response.is_closed

            docstring = await response.parse()
            assert_matches_type(DocstringTrailingDoubleQuoteResponse, docstring, path=["response"])

        assert cast(Any, response.is_closed) is True
