# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types.resource_refs import ParentModelWithChildRef

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestParent:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_returns_parent_model_with_child_ref(self, client: Sink) -> None:
        parent = client.resource_refs.parent.returns_parent_model_with_child_ref()
        assert_matches_type(ParentModelWithChildRef, parent, path=["response"])

    @parametrize
    def test_raw_response_returns_parent_model_with_child_ref(self, client: Sink) -> None:
        response = client.resource_refs.parent.with_raw_response.returns_parent_model_with_child_ref()

        assert response.is_closed is True
        parent = response.parse()
        assert_matches_type(ParentModelWithChildRef, parent, path=["response"])

    @parametrize
    def test_streaming_response_returns_parent_model_with_child_ref(self, client: Sink) -> None:
        with client.resource_refs.parent.with_streaming_response.returns_parent_model_with_child_ref() as response:
            assert not response.is_closed

            parent = response.parse()
            assert_matches_type(ParentModelWithChildRef, parent, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncParent:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_returns_parent_model_with_child_ref(self, async_client: AsyncSink) -> None:
        parent = await async_client.resource_refs.parent.returns_parent_model_with_child_ref()
        assert_matches_type(ParentModelWithChildRef, parent, path=["response"])

    @parametrize
    async def test_raw_response_returns_parent_model_with_child_ref(self, async_client: AsyncSink) -> None:
        response = await async_client.resource_refs.parent.with_raw_response.returns_parent_model_with_child_ref()

        assert response.is_closed is True
        parent = response.parse()
        assert_matches_type(ParentModelWithChildRef, parent, path=["response"])

    @parametrize
    async def test_streaming_response_returns_parent_model_with_child_ref(self, async_client: AsyncSink) -> None:
        async with (
            async_client.resource_refs.parent.with_streaming_response.returns_parent_model_with_child_ref()
        ) as response:
            assert not response.is_closed

            parent = await response.parse()
            assert_matches_type(ParentModelWithChildRef, parent, path=["response"])

        assert cast(Any, response.is_closed) is True
