# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import Address, EnvelopeWrappedArrayResponse, EnvelopeInlineResponseResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEnvelopes:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_explicit(self, client: Sink) -> None:
        envelope = client.envelopes.explicit()
        assert_matches_type(Address, envelope, path=["response"])

    @parametrize
    def test_raw_response_explicit(self, client: Sink) -> None:
        response = client.envelopes.with_raw_response.explicit()

        assert response.is_closed is True
        envelope = response.parse()
        assert_matches_type(Address, envelope, path=["response"])

    @parametrize
    def test_streaming_response_explicit(self, client: Sink) -> None:
        with client.envelopes.with_streaming_response.explicit() as response:
            assert not response.is_closed

            envelope = response.parse()
            assert_matches_type(Address, envelope, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_implicit(self, client: Sink) -> None:
        envelope = client.envelopes.implicit()
        assert_matches_type(Address, envelope, path=["response"])

    @parametrize
    def test_raw_response_implicit(self, client: Sink) -> None:
        response = client.envelopes.with_raw_response.implicit()

        assert response.is_closed is True
        envelope = response.parse()
        assert_matches_type(Address, envelope, path=["response"])

    @parametrize
    def test_streaming_response_implicit(self, client: Sink) -> None:
        with client.envelopes.with_streaming_response.implicit() as response:
            assert not response.is_closed

            envelope = response.parse()
            assert_matches_type(Address, envelope, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_inline_response(self, client: Sink) -> None:
        envelope = client.envelopes.inline_response()
        assert_matches_type(EnvelopeInlineResponseResponse, envelope, path=["response"])

    @parametrize
    def test_raw_response_inline_response(self, client: Sink) -> None:
        response = client.envelopes.with_raw_response.inline_response()

        assert response.is_closed is True
        envelope = response.parse()
        assert_matches_type(EnvelopeInlineResponseResponse, envelope, path=["response"])

    @parametrize
    def test_streaming_response_inline_response(self, client: Sink) -> None:
        with client.envelopes.with_streaming_response.inline_response() as response:
            assert not response.is_closed

            envelope = response.parse()
            assert_matches_type(EnvelopeInlineResponseResponse, envelope, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_wrapped_array(self, client: Sink) -> None:
        envelope = client.envelopes.wrapped_array()
        assert_matches_type(EnvelopeWrappedArrayResponse, envelope, path=["response"])

    @parametrize
    def test_raw_response_wrapped_array(self, client: Sink) -> None:
        response = client.envelopes.with_raw_response.wrapped_array()

        assert response.is_closed is True
        envelope = response.parse()
        assert_matches_type(EnvelopeWrappedArrayResponse, envelope, path=["response"])

    @parametrize
    def test_streaming_response_wrapped_array(self, client: Sink) -> None:
        with client.envelopes.with_streaming_response.wrapped_array() as response:
            assert not response.is_closed

            envelope = response.parse()
            assert_matches_type(EnvelopeWrappedArrayResponse, envelope, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncEnvelopes:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_explicit(self, async_client: AsyncSink) -> None:
        envelope = await async_client.envelopes.explicit()
        assert_matches_type(Address, envelope, path=["response"])

    @parametrize
    async def test_raw_response_explicit(self, async_client: AsyncSink) -> None:
        response = await async_client.envelopes.with_raw_response.explicit()

        assert response.is_closed is True
        envelope = response.parse()
        assert_matches_type(Address, envelope, path=["response"])

    @parametrize
    async def test_streaming_response_explicit(self, async_client: AsyncSink) -> None:
        async with async_client.envelopes.with_streaming_response.explicit() as response:
            assert not response.is_closed

            envelope = await response.parse()
            assert_matches_type(Address, envelope, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_implicit(self, async_client: AsyncSink) -> None:
        envelope = await async_client.envelopes.implicit()
        assert_matches_type(Address, envelope, path=["response"])

    @parametrize
    async def test_raw_response_implicit(self, async_client: AsyncSink) -> None:
        response = await async_client.envelopes.with_raw_response.implicit()

        assert response.is_closed is True
        envelope = response.parse()
        assert_matches_type(Address, envelope, path=["response"])

    @parametrize
    async def test_streaming_response_implicit(self, async_client: AsyncSink) -> None:
        async with async_client.envelopes.with_streaming_response.implicit() as response:
            assert not response.is_closed

            envelope = await response.parse()
            assert_matches_type(Address, envelope, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_inline_response(self, async_client: AsyncSink) -> None:
        envelope = await async_client.envelopes.inline_response()
        assert_matches_type(EnvelopeInlineResponseResponse, envelope, path=["response"])

    @parametrize
    async def test_raw_response_inline_response(self, async_client: AsyncSink) -> None:
        response = await async_client.envelopes.with_raw_response.inline_response()

        assert response.is_closed is True
        envelope = response.parse()
        assert_matches_type(EnvelopeInlineResponseResponse, envelope, path=["response"])

    @parametrize
    async def test_streaming_response_inline_response(self, async_client: AsyncSink) -> None:
        async with async_client.envelopes.with_streaming_response.inline_response() as response:
            assert not response.is_closed

            envelope = await response.parse()
            assert_matches_type(EnvelopeInlineResponseResponse, envelope, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_wrapped_array(self, async_client: AsyncSink) -> None:
        envelope = await async_client.envelopes.wrapped_array()
        assert_matches_type(EnvelopeWrappedArrayResponse, envelope, path=["response"])

    @parametrize
    async def test_raw_response_wrapped_array(self, async_client: AsyncSink) -> None:
        response = await async_client.envelopes.with_raw_response.wrapped_array()

        assert response.is_closed is True
        envelope = response.parse()
        assert_matches_type(EnvelopeWrappedArrayResponse, envelope, path=["response"])

    @parametrize
    async def test_streaming_response_wrapped_array(self, async_client: AsyncSink) -> None:
        async with async_client.envelopes.with_streaming_response.wrapped_array() as response:
            assert not response.is_closed

            envelope = await response.parse()
            assert_matches_type(EnvelopeWrappedArrayResponse, envelope, path=["response"])

        assert cast(Any, response.is_closed) is True
