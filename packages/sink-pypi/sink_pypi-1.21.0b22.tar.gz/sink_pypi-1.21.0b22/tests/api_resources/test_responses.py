# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import (
    ModelWithNestedModel,
    ObjectWithAnyOfNullProperty,
    ObjectWithOneOfNullProperty,
    ResponseAllofSimpleResponse,
    ResponseNestedArrayResponse,
    ResponseArrayResponseResponse,
    ResponseMissingRequiredResponse,
    ResponseAllofCrossResourceResponse,
    ResponseObjectNoPropertiesResponse,
    ResponseObjectAllPropertiesResponse,
    ResponseAdditionalPropertiesResponse,
    ResponseOnlyReadOnlyPropertiesResponse,
    ResponseArrayObjectWithUnionPropertiesResponse,
    ResponseObjectWithAdditionalPropertiesPropResponse,
    ResponseAdditionalPropertiesNestedModelReferenceResponse,
)
from sink.api.sdk.types.shared import SimpleObject

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestResponses:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_additional_properties(self, client: Sink) -> None:
        response = client.responses.additional_properties()
        assert_matches_type(ResponseAdditionalPropertiesResponse, response, path=["response"])

    @parametrize
    def test_raw_response_additional_properties(self, client: Sink) -> None:
        http_response = client.responses.with_raw_response.additional_properties()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ResponseAdditionalPropertiesResponse, response, path=["response"])

    @parametrize
    def test_streaming_response_additional_properties(self, client: Sink) -> None:
        with client.responses.with_streaming_response.additional_properties() as http_response:
            assert not http_response.is_closed

            response = http_response.parse()
            assert_matches_type(ResponseAdditionalPropertiesResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    def test_method_additional_properties_nested_model_reference(self, client: Sink) -> None:
        response = client.responses.additional_properties_nested_model_reference()
        assert_matches_type(ResponseAdditionalPropertiesNestedModelReferenceResponse, response, path=["response"])

    @parametrize
    def test_raw_response_additional_properties_nested_model_reference(self, client: Sink) -> None:
        http_response = client.responses.with_raw_response.additional_properties_nested_model_reference()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ResponseAdditionalPropertiesNestedModelReferenceResponse, response, path=["response"])

    @parametrize
    def test_streaming_response_additional_properties_nested_model_reference(self, client: Sink) -> None:
        with client.responses.with_streaming_response.additional_properties_nested_model_reference() as http_response:
            assert not http_response.is_closed

            response = http_response.parse()
            assert_matches_type(ResponseAdditionalPropertiesNestedModelReferenceResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    def test_method_allof_cross_resource(self, client: Sink) -> None:
        response = client.responses.allof_cross_resource()
        assert_matches_type(ResponseAllofCrossResourceResponse, response, path=["response"])

    @parametrize
    def test_raw_response_allof_cross_resource(self, client: Sink) -> None:
        http_response = client.responses.with_raw_response.allof_cross_resource()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ResponseAllofCrossResourceResponse, response, path=["response"])

    @parametrize
    def test_streaming_response_allof_cross_resource(self, client: Sink) -> None:
        with client.responses.with_streaming_response.allof_cross_resource() as http_response:
            assert not http_response.is_closed

            response = http_response.parse()
            assert_matches_type(ResponseAllofCrossResourceResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    def test_method_allof_simple(self, client: Sink) -> None:
        response = client.responses.allof_simple()
        assert_matches_type(ResponseAllofSimpleResponse, response, path=["response"])

    @parametrize
    def test_raw_response_allof_simple(self, client: Sink) -> None:
        http_response = client.responses.with_raw_response.allof_simple()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ResponseAllofSimpleResponse, response, path=["response"])

    @parametrize
    def test_streaming_response_allof_simple(self, client: Sink) -> None:
        with client.responses.with_streaming_response.allof_simple() as http_response:
            assert not http_response.is_closed

            response = http_response.parse()
            assert_matches_type(ResponseAllofSimpleResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    def test_method_anyof_null(self, client: Sink) -> None:
        response = client.responses.anyof_null()
        assert_matches_type(ObjectWithAnyOfNullProperty, response, path=["response"])

    @parametrize
    def test_raw_response_anyof_null(self, client: Sink) -> None:
        http_response = client.responses.with_raw_response.anyof_null()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ObjectWithAnyOfNullProperty, response, path=["response"])

    @parametrize
    def test_streaming_response_anyof_null(self, client: Sink) -> None:
        with client.responses.with_streaming_response.anyof_null() as http_response:
            assert not http_response.is_closed

            response = http_response.parse()
            assert_matches_type(ObjectWithAnyOfNullProperty, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    def test_method_array_object_with_union_properties(self, client: Sink) -> None:
        response = client.responses.array_object_with_union_properties()
        assert_matches_type(ResponseArrayObjectWithUnionPropertiesResponse, response, path=["response"])

    @parametrize
    def test_raw_response_array_object_with_union_properties(self, client: Sink) -> None:
        http_response = client.responses.with_raw_response.array_object_with_union_properties()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ResponseArrayObjectWithUnionPropertiesResponse, response, path=["response"])

    @parametrize
    def test_streaming_response_array_object_with_union_properties(self, client: Sink) -> None:
        with client.responses.with_streaming_response.array_object_with_union_properties() as http_response:
            assert not http_response.is_closed

            response = http_response.parse()
            assert_matches_type(ResponseArrayObjectWithUnionPropertiesResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    def test_method_array_response(self, client: Sink) -> None:
        response = client.responses.array_response()
        assert_matches_type(ResponseArrayResponseResponse, response, path=["response"])

    @parametrize
    def test_raw_response_array_response(self, client: Sink) -> None:
        http_response = client.responses.with_raw_response.array_response()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ResponseArrayResponseResponse, response, path=["response"])

    @parametrize
    def test_streaming_response_array_response(self, client: Sink) -> None:
        with client.responses.with_streaming_response.array_response() as http_response:
            assert not http_response.is_closed

            response = http_response.parse()
            assert_matches_type(ResponseArrayResponseResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    def test_method_empty_response(self, client: Sink) -> None:
        response = client.responses.empty_response()
        assert response is None

    @parametrize
    def test_raw_response_empty_response(self, client: Sink) -> None:
        http_response = client.responses.with_raw_response.empty_response()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert response is None

    @parametrize
    def test_streaming_response_empty_response(self, client: Sink) -> None:
        with client.responses.with_streaming_response.empty_response() as http_response:
            assert not http_response.is_closed

            response = http_response.parse()
            assert response is None

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    def test_method_missing_required(self, client: Sink) -> None:
        response = client.responses.missing_required()
        assert_matches_type(ResponseMissingRequiredResponse, response, path=["response"])

    @parametrize
    def test_raw_response_missing_required(self, client: Sink) -> None:
        http_response = client.responses.with_raw_response.missing_required()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ResponseMissingRequiredResponse, response, path=["response"])

    @parametrize
    def test_streaming_response_missing_required(self, client: Sink) -> None:
        with client.responses.with_streaming_response.missing_required() as http_response:
            assert not http_response.is_closed

            response = http_response.parse()
            assert_matches_type(ResponseMissingRequiredResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    def test_method_nested_array(self, client: Sink) -> None:
        response = client.responses.nested_array()
        assert_matches_type(ResponseNestedArrayResponse, response, path=["response"])

    @parametrize
    def test_raw_response_nested_array(self, client: Sink) -> None:
        http_response = client.responses.with_raw_response.nested_array()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ResponseNestedArrayResponse, response, path=["response"])

    @parametrize
    def test_streaming_response_nested_array(self, client: Sink) -> None:
        with client.responses.with_streaming_response.nested_array() as http_response:
            assert not http_response.is_closed

            response = http_response.parse()
            assert_matches_type(ResponseNestedArrayResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    def test_method_object_all_properties(self, client: Sink) -> None:
        response = client.responses.object_all_properties()
        assert_matches_type(ResponseObjectAllPropertiesResponse, response, path=["response"])

    @parametrize
    def test_raw_response_object_all_properties(self, client: Sink) -> None:
        http_response = client.responses.with_raw_response.object_all_properties()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ResponseObjectAllPropertiesResponse, response, path=["response"])

    @parametrize
    def test_streaming_response_object_all_properties(self, client: Sink) -> None:
        with client.responses.with_streaming_response.object_all_properties() as http_response:
            assert not http_response.is_closed

            response = http_response.parse()
            assert_matches_type(ResponseObjectAllPropertiesResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    def test_method_object_no_properties(self, client: Sink) -> None:
        response = client.responses.object_no_properties()
        assert_matches_type(ResponseObjectNoPropertiesResponse, response, path=["response"])

    @parametrize
    def test_raw_response_object_no_properties(self, client: Sink) -> None:
        http_response = client.responses.with_raw_response.object_no_properties()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ResponseObjectNoPropertiesResponse, response, path=["response"])

    @parametrize
    def test_streaming_response_object_no_properties(self, client: Sink) -> None:
        with client.responses.with_streaming_response.object_no_properties() as http_response:
            assert not http_response.is_closed

            response = http_response.parse()
            assert_matches_type(ResponseObjectNoPropertiesResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    def test_method_object_with_additional_properties_prop(self, client: Sink) -> None:
        response = client.responses.object_with_additional_properties_prop()
        assert_matches_type(ResponseObjectWithAdditionalPropertiesPropResponse, response, path=["response"])

    @parametrize
    def test_raw_response_object_with_additional_properties_prop(self, client: Sink) -> None:
        http_response = client.responses.with_raw_response.object_with_additional_properties_prop()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ResponseObjectWithAdditionalPropertiesPropResponse, response, path=["response"])

    @parametrize
    def test_streaming_response_object_with_additional_properties_prop(self, client: Sink) -> None:
        with client.responses.with_streaming_response.object_with_additional_properties_prop() as http_response:
            assert not http_response.is_closed

            response = http_response.parse()
            assert_matches_type(ResponseObjectWithAdditionalPropertiesPropResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    def test_method_oneof_null(self, client: Sink) -> None:
        response = client.responses.oneof_null()
        assert_matches_type(ObjectWithOneOfNullProperty, response, path=["response"])

    @parametrize
    def test_raw_response_oneof_null(self, client: Sink) -> None:
        http_response = client.responses.with_raw_response.oneof_null()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ObjectWithOneOfNullProperty, response, path=["response"])

    @parametrize
    def test_streaming_response_oneof_null(self, client: Sink) -> None:
        with client.responses.with_streaming_response.oneof_null() as http_response:
            assert not http_response.is_closed

            response = http_response.parse()
            assert_matches_type(ObjectWithOneOfNullProperty, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    def test_method_only_read_only_properties(self, client: Sink) -> None:
        response = client.responses.only_read_only_properties()
        assert_matches_type(ResponseOnlyReadOnlyPropertiesResponse, response, path=["response"])

    @parametrize
    def test_raw_response_only_read_only_properties(self, client: Sink) -> None:
        http_response = client.responses.with_raw_response.only_read_only_properties()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ResponseOnlyReadOnlyPropertiesResponse, response, path=["response"])

    @parametrize
    def test_streaming_response_only_read_only_properties(self, client: Sink) -> None:
        with client.responses.with_streaming_response.only_read_only_properties() as http_response:
            assert not http_response.is_closed

            response = http_response.parse()
            assert_matches_type(ResponseOnlyReadOnlyPropertiesResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    def test_method_shared_simple_object(self, client: Sink) -> None:
        response = client.responses.shared_simple_object()
        assert_matches_type(SimpleObject, response, path=["response"])

    @parametrize
    def test_raw_response_shared_simple_object(self, client: Sink) -> None:
        http_response = client.responses.with_raw_response.shared_simple_object()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(SimpleObject, response, path=["response"])

    @parametrize
    def test_streaming_response_shared_simple_object(self, client: Sink) -> None:
        with client.responses.with_streaming_response.shared_simple_object() as http_response:
            assert not http_response.is_closed

            response = http_response.parse()
            assert_matches_type(SimpleObject, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    def test_method_string_response(self, client: Sink) -> None:
        response = client.responses.string_response()
        assert_matches_type(str, response, path=["response"])

    @parametrize
    def test_raw_response_string_response(self, client: Sink) -> None:
        http_response = client.responses.with_raw_response.string_response()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(str, response, path=["response"])

    @parametrize
    def test_streaming_response_string_response(self, client: Sink) -> None:
        with client.responses.with_streaming_response.string_response() as http_response:
            assert not http_response.is_closed

            response = http_response.parse()
            assert_matches_type(str, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    def test_method_unknown_object(self, client: Sink) -> None:
        response = client.responses.unknown_object()
        assert_matches_type(object, response, path=["response"])

    @parametrize
    def test_raw_response_unknown_object(self, client: Sink) -> None:
        http_response = client.responses.with_raw_response.unknown_object()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(object, response, path=["response"])

    @parametrize
    def test_streaming_response_unknown_object(self, client: Sink) -> None:
        with client.responses.with_streaming_response.unknown_object() as http_response:
            assert not http_response.is_closed

            response = http_response.parse()
            assert_matches_type(object, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    def test_method_with_model_in_nested_path(self, client: Sink) -> None:
        response = client.responses.with_model_in_nested_path()
        assert_matches_type(ModelWithNestedModel, response, path=["response"])

    @parametrize
    def test_raw_response_with_model_in_nested_path(self, client: Sink) -> None:
        http_response = client.responses.with_raw_response.with_model_in_nested_path()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ModelWithNestedModel, response, path=["response"])

    @parametrize
    def test_streaming_response_with_model_in_nested_path(self, client: Sink) -> None:
        with client.responses.with_streaming_response.with_model_in_nested_path() as http_response:
            assert not http_response.is_closed

            response = http_response.parse()
            assert_matches_type(ModelWithNestedModel, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True


class TestAsyncResponses:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_additional_properties(self, async_client: AsyncSink) -> None:
        response = await async_client.responses.additional_properties()
        assert_matches_type(ResponseAdditionalPropertiesResponse, response, path=["response"])

    @parametrize
    async def test_raw_response_additional_properties(self, async_client: AsyncSink) -> None:
        http_response = await async_client.responses.with_raw_response.additional_properties()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ResponseAdditionalPropertiesResponse, response, path=["response"])

    @parametrize
    async def test_streaming_response_additional_properties(self, async_client: AsyncSink) -> None:
        async with async_client.responses.with_streaming_response.additional_properties() as http_response:
            assert not http_response.is_closed

            response = await http_response.parse()
            assert_matches_type(ResponseAdditionalPropertiesResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    async def test_method_additional_properties_nested_model_reference(self, async_client: AsyncSink) -> None:
        response = await async_client.responses.additional_properties_nested_model_reference()
        assert_matches_type(ResponseAdditionalPropertiesNestedModelReferenceResponse, response, path=["response"])

    @parametrize
    async def test_raw_response_additional_properties_nested_model_reference(self, async_client: AsyncSink) -> None:
        http_response = await async_client.responses.with_raw_response.additional_properties_nested_model_reference()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ResponseAdditionalPropertiesNestedModelReferenceResponse, response, path=["response"])

    @parametrize
    async def test_streaming_response_additional_properties_nested_model_reference(
        self, async_client: AsyncSink
    ) -> None:
        async with (
            async_client.responses.with_streaming_response.additional_properties_nested_model_reference()
        ) as http_response:
            assert not http_response.is_closed

            response = await http_response.parse()
            assert_matches_type(ResponseAdditionalPropertiesNestedModelReferenceResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    async def test_method_allof_cross_resource(self, async_client: AsyncSink) -> None:
        response = await async_client.responses.allof_cross_resource()
        assert_matches_type(ResponseAllofCrossResourceResponse, response, path=["response"])

    @parametrize
    async def test_raw_response_allof_cross_resource(self, async_client: AsyncSink) -> None:
        http_response = await async_client.responses.with_raw_response.allof_cross_resource()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ResponseAllofCrossResourceResponse, response, path=["response"])

    @parametrize
    async def test_streaming_response_allof_cross_resource(self, async_client: AsyncSink) -> None:
        async with async_client.responses.with_streaming_response.allof_cross_resource() as http_response:
            assert not http_response.is_closed

            response = await http_response.parse()
            assert_matches_type(ResponseAllofCrossResourceResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    async def test_method_allof_simple(self, async_client: AsyncSink) -> None:
        response = await async_client.responses.allof_simple()
        assert_matches_type(ResponseAllofSimpleResponse, response, path=["response"])

    @parametrize
    async def test_raw_response_allof_simple(self, async_client: AsyncSink) -> None:
        http_response = await async_client.responses.with_raw_response.allof_simple()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ResponseAllofSimpleResponse, response, path=["response"])

    @parametrize
    async def test_streaming_response_allof_simple(self, async_client: AsyncSink) -> None:
        async with async_client.responses.with_streaming_response.allof_simple() as http_response:
            assert not http_response.is_closed

            response = await http_response.parse()
            assert_matches_type(ResponseAllofSimpleResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    async def test_method_anyof_null(self, async_client: AsyncSink) -> None:
        response = await async_client.responses.anyof_null()
        assert_matches_type(ObjectWithAnyOfNullProperty, response, path=["response"])

    @parametrize
    async def test_raw_response_anyof_null(self, async_client: AsyncSink) -> None:
        http_response = await async_client.responses.with_raw_response.anyof_null()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ObjectWithAnyOfNullProperty, response, path=["response"])

    @parametrize
    async def test_streaming_response_anyof_null(self, async_client: AsyncSink) -> None:
        async with async_client.responses.with_streaming_response.anyof_null() as http_response:
            assert not http_response.is_closed

            response = await http_response.parse()
            assert_matches_type(ObjectWithAnyOfNullProperty, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    async def test_method_array_object_with_union_properties(self, async_client: AsyncSink) -> None:
        response = await async_client.responses.array_object_with_union_properties()
        assert_matches_type(ResponseArrayObjectWithUnionPropertiesResponse, response, path=["response"])

    @parametrize
    async def test_raw_response_array_object_with_union_properties(self, async_client: AsyncSink) -> None:
        http_response = await async_client.responses.with_raw_response.array_object_with_union_properties()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ResponseArrayObjectWithUnionPropertiesResponse, response, path=["response"])

    @parametrize
    async def test_streaming_response_array_object_with_union_properties(self, async_client: AsyncSink) -> None:
        async with async_client.responses.with_streaming_response.array_object_with_union_properties() as http_response:
            assert not http_response.is_closed

            response = await http_response.parse()
            assert_matches_type(ResponseArrayObjectWithUnionPropertiesResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    async def test_method_array_response(self, async_client: AsyncSink) -> None:
        response = await async_client.responses.array_response()
        assert_matches_type(ResponseArrayResponseResponse, response, path=["response"])

    @parametrize
    async def test_raw_response_array_response(self, async_client: AsyncSink) -> None:
        http_response = await async_client.responses.with_raw_response.array_response()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ResponseArrayResponseResponse, response, path=["response"])

    @parametrize
    async def test_streaming_response_array_response(self, async_client: AsyncSink) -> None:
        async with async_client.responses.with_streaming_response.array_response() as http_response:
            assert not http_response.is_closed

            response = await http_response.parse()
            assert_matches_type(ResponseArrayResponseResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    async def test_method_empty_response(self, async_client: AsyncSink) -> None:
        response = await async_client.responses.empty_response()
        assert response is None

    @parametrize
    async def test_raw_response_empty_response(self, async_client: AsyncSink) -> None:
        http_response = await async_client.responses.with_raw_response.empty_response()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert response is None

    @parametrize
    async def test_streaming_response_empty_response(self, async_client: AsyncSink) -> None:
        async with async_client.responses.with_streaming_response.empty_response() as http_response:
            assert not http_response.is_closed

            response = await http_response.parse()
            assert response is None

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    async def test_method_missing_required(self, async_client: AsyncSink) -> None:
        response = await async_client.responses.missing_required()
        assert_matches_type(ResponseMissingRequiredResponse, response, path=["response"])

    @parametrize
    async def test_raw_response_missing_required(self, async_client: AsyncSink) -> None:
        http_response = await async_client.responses.with_raw_response.missing_required()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ResponseMissingRequiredResponse, response, path=["response"])

    @parametrize
    async def test_streaming_response_missing_required(self, async_client: AsyncSink) -> None:
        async with async_client.responses.with_streaming_response.missing_required() as http_response:
            assert not http_response.is_closed

            response = await http_response.parse()
            assert_matches_type(ResponseMissingRequiredResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    async def test_method_nested_array(self, async_client: AsyncSink) -> None:
        response = await async_client.responses.nested_array()
        assert_matches_type(ResponseNestedArrayResponse, response, path=["response"])

    @parametrize
    async def test_raw_response_nested_array(self, async_client: AsyncSink) -> None:
        http_response = await async_client.responses.with_raw_response.nested_array()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ResponseNestedArrayResponse, response, path=["response"])

    @parametrize
    async def test_streaming_response_nested_array(self, async_client: AsyncSink) -> None:
        async with async_client.responses.with_streaming_response.nested_array() as http_response:
            assert not http_response.is_closed

            response = await http_response.parse()
            assert_matches_type(ResponseNestedArrayResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    async def test_method_object_all_properties(self, async_client: AsyncSink) -> None:
        response = await async_client.responses.object_all_properties()
        assert_matches_type(ResponseObjectAllPropertiesResponse, response, path=["response"])

    @parametrize
    async def test_raw_response_object_all_properties(self, async_client: AsyncSink) -> None:
        http_response = await async_client.responses.with_raw_response.object_all_properties()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ResponseObjectAllPropertiesResponse, response, path=["response"])

    @parametrize
    async def test_streaming_response_object_all_properties(self, async_client: AsyncSink) -> None:
        async with async_client.responses.with_streaming_response.object_all_properties() as http_response:
            assert not http_response.is_closed

            response = await http_response.parse()
            assert_matches_type(ResponseObjectAllPropertiesResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    async def test_method_object_no_properties(self, async_client: AsyncSink) -> None:
        response = await async_client.responses.object_no_properties()
        assert_matches_type(ResponseObjectNoPropertiesResponse, response, path=["response"])

    @parametrize
    async def test_raw_response_object_no_properties(self, async_client: AsyncSink) -> None:
        http_response = await async_client.responses.with_raw_response.object_no_properties()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ResponseObjectNoPropertiesResponse, response, path=["response"])

    @parametrize
    async def test_streaming_response_object_no_properties(self, async_client: AsyncSink) -> None:
        async with async_client.responses.with_streaming_response.object_no_properties() as http_response:
            assert not http_response.is_closed

            response = await http_response.parse()
            assert_matches_type(ResponseObjectNoPropertiesResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    async def test_method_object_with_additional_properties_prop(self, async_client: AsyncSink) -> None:
        response = await async_client.responses.object_with_additional_properties_prop()
        assert_matches_type(ResponseObjectWithAdditionalPropertiesPropResponse, response, path=["response"])

    @parametrize
    async def test_raw_response_object_with_additional_properties_prop(self, async_client: AsyncSink) -> None:
        http_response = await async_client.responses.with_raw_response.object_with_additional_properties_prop()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ResponseObjectWithAdditionalPropertiesPropResponse, response, path=["response"])

    @parametrize
    async def test_streaming_response_object_with_additional_properties_prop(self, async_client: AsyncSink) -> None:
        async with (
            async_client.responses.with_streaming_response.object_with_additional_properties_prop()
        ) as http_response:
            assert not http_response.is_closed

            response = await http_response.parse()
            assert_matches_type(ResponseObjectWithAdditionalPropertiesPropResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    async def test_method_oneof_null(self, async_client: AsyncSink) -> None:
        response = await async_client.responses.oneof_null()
        assert_matches_type(ObjectWithOneOfNullProperty, response, path=["response"])

    @parametrize
    async def test_raw_response_oneof_null(self, async_client: AsyncSink) -> None:
        http_response = await async_client.responses.with_raw_response.oneof_null()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ObjectWithOneOfNullProperty, response, path=["response"])

    @parametrize
    async def test_streaming_response_oneof_null(self, async_client: AsyncSink) -> None:
        async with async_client.responses.with_streaming_response.oneof_null() as http_response:
            assert not http_response.is_closed

            response = await http_response.parse()
            assert_matches_type(ObjectWithOneOfNullProperty, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    async def test_method_only_read_only_properties(self, async_client: AsyncSink) -> None:
        response = await async_client.responses.only_read_only_properties()
        assert_matches_type(ResponseOnlyReadOnlyPropertiesResponse, response, path=["response"])

    @parametrize
    async def test_raw_response_only_read_only_properties(self, async_client: AsyncSink) -> None:
        http_response = await async_client.responses.with_raw_response.only_read_only_properties()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ResponseOnlyReadOnlyPropertiesResponse, response, path=["response"])

    @parametrize
    async def test_streaming_response_only_read_only_properties(self, async_client: AsyncSink) -> None:
        async with async_client.responses.with_streaming_response.only_read_only_properties() as http_response:
            assert not http_response.is_closed

            response = await http_response.parse()
            assert_matches_type(ResponseOnlyReadOnlyPropertiesResponse, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    async def test_method_shared_simple_object(self, async_client: AsyncSink) -> None:
        response = await async_client.responses.shared_simple_object()
        assert_matches_type(SimpleObject, response, path=["response"])

    @parametrize
    async def test_raw_response_shared_simple_object(self, async_client: AsyncSink) -> None:
        http_response = await async_client.responses.with_raw_response.shared_simple_object()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(SimpleObject, response, path=["response"])

    @parametrize
    async def test_streaming_response_shared_simple_object(self, async_client: AsyncSink) -> None:
        async with async_client.responses.with_streaming_response.shared_simple_object() as http_response:
            assert not http_response.is_closed

            response = await http_response.parse()
            assert_matches_type(SimpleObject, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    async def test_method_string_response(self, async_client: AsyncSink) -> None:
        response = await async_client.responses.string_response()
        assert_matches_type(str, response, path=["response"])

    @parametrize
    async def test_raw_response_string_response(self, async_client: AsyncSink) -> None:
        http_response = await async_client.responses.with_raw_response.string_response()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(str, response, path=["response"])

    @parametrize
    async def test_streaming_response_string_response(self, async_client: AsyncSink) -> None:
        async with async_client.responses.with_streaming_response.string_response() as http_response:
            assert not http_response.is_closed

            response = await http_response.parse()
            assert_matches_type(str, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    async def test_method_unknown_object(self, async_client: AsyncSink) -> None:
        response = await async_client.responses.unknown_object()
        assert_matches_type(object, response, path=["response"])

    @parametrize
    async def test_raw_response_unknown_object(self, async_client: AsyncSink) -> None:
        http_response = await async_client.responses.with_raw_response.unknown_object()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(object, response, path=["response"])

    @parametrize
    async def test_streaming_response_unknown_object(self, async_client: AsyncSink) -> None:
        async with async_client.responses.with_streaming_response.unknown_object() as http_response:
            assert not http_response.is_closed

            response = await http_response.parse()
            assert_matches_type(object, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True

    @parametrize
    async def test_method_with_model_in_nested_path(self, async_client: AsyncSink) -> None:
        response = await async_client.responses.with_model_in_nested_path()
        assert_matches_type(ModelWithNestedModel, response, path=["response"])

    @parametrize
    async def test_raw_response_with_model_in_nested_path(self, async_client: AsyncSink) -> None:
        http_response = await async_client.responses.with_raw_response.with_model_in_nested_path()

        assert http_response.is_closed is True
        response = http_response.parse()
        assert_matches_type(ModelWithNestedModel, response, path=["response"])

    @parametrize
    async def test_streaming_response_with_model_in_nested_path(self, async_client: AsyncSink) -> None:
        async with async_client.responses.with_streaming_response.with_model_in_nested_path() as http_response:
            assert not http_response.is_closed

            response = await http_response.parse()
            assert_matches_type(ModelWithNestedModel, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True
