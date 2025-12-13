# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import (
    ModelWithNestedModel,
    BodyParamTopLevelAllOfResponse,
    BodyParamTopLevelAnyOfResponse,
    BodyParamTopLevelOneOfResponse,
    BodyParamUnionOverlappingPropResponse,
)
from sink.api.sdk.types.shared import BasicSharedModelObject

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBodyParams:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_duplicate_subproperty(self, client: Sink) -> None:
        body_param = client.body_params.duplicate_subproperty()
        assert_matches_type(ModelWithNestedModel, body_param, path=["response"])

    @parametrize
    def test_method_duplicate_subproperty_with_all_params(self, client: Sink) -> None:
        body_param = client.body_params.duplicate_subproperty(
            baz={"bar": {"hello": "hello"}},
            foo={"bar": {"hello": "hello"}},
            foo_bar={"hello": "hello"},
            mapping={"hello": "hello"},
            mappings=[{"hello": "hello"}],
        )
        assert_matches_type(ModelWithNestedModel, body_param, path=["response"])

    @parametrize
    def test_raw_response_duplicate_subproperty(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.duplicate_subproperty()

        assert response.is_closed is True
        body_param = response.parse()
        assert_matches_type(ModelWithNestedModel, body_param, path=["response"])

    @parametrize
    def test_streaming_response_duplicate_subproperty(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.duplicate_subproperty() as response:
            assert not response.is_closed

            body_param = response.parse()
            assert_matches_type(ModelWithNestedModel, body_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_enum_properties(self, client: Sink) -> None:
        body_param = client.body_params.enum_properties()
        assert body_param is None

    @parametrize
    def test_method_enum_properties_with_all_params(self, client: Sink) -> None:
        body_param = client.body_params.enum_properties(
            code=1,
            enabled=True,
            kind="failed",
        )
        assert body_param is None

    @parametrize
    def test_raw_response_enum_properties(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.enum_properties()

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    def test_streaming_response_enum_properties(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.enum_properties() as response:
            assert not response.is_closed

            body_param = response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_nested_request_models(self, client: Sink) -> None:
        body_param = client.body_params.nested_request_models()
        assert_matches_type(ModelWithNestedModel, body_param, path=["response"])

    @parametrize
    def test_method_nested_request_models_with_all_params(self, client: Sink) -> None:
        body_param = client.body_params.nested_request_models(
            data={"foo": {"bar": {"baz": {"hello": "hello"}}}},
        )
        assert_matches_type(ModelWithNestedModel, body_param, path=["response"])

    @parametrize
    def test_raw_response_nested_request_models(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.nested_request_models()

        assert response.is_closed is True
        body_param = response.parse()
        assert_matches_type(ModelWithNestedModel, body_param, path=["response"])

    @parametrize
    def test_streaming_response_nested_request_models(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.nested_request_models() as response:
            assert not response.is_closed

            body_param = response.parse()
            assert_matches_type(ModelWithNestedModel, body_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_object_map_model_ref(self, client: Sink) -> None:
        body_param = client.body_params.object_map_model_ref(
            model_ref={"foo": {}},
            name="name",
        )
        assert body_param is None

    @parametrize
    def test_raw_response_object_map_model_ref(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.object_map_model_ref(
            model_ref={"foo": {}},
            name="name",
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    def test_streaming_response_object_map_model_ref(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.object_map_model_ref(
            model_ref={"foo": {}},
            name="name",
        ) as response:
            assert not response.is_closed

            body_param = response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_object_with_array_of_objects(self, client: Sink) -> None:
        body_param = client.body_params.object_with_array_of_objects()
        assert body_param is None

    @parametrize
    def test_method_object_with_array_of_objects_with_all_params(self, client: Sink) -> None:
        body_param = client.body_params.object_with_array_of_objects(
            array_prop=[{"kind": "VIRTUAL"}],
        )
        assert body_param is None

    @parametrize
    def test_raw_response_object_with_array_of_objects(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.object_with_array_of_objects()

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    def test_streaming_response_object_with_array_of_objects(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.object_with_array_of_objects() as response:
            assert not response.is_closed

            body_param = response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_object_with_union_properties(self, client: Sink) -> None:
        body_param = client.body_params.object_with_union_properties(
            bar={"bar": 0},
            foo=0,
        )
        assert body_param is None

    @parametrize
    def test_method_object_with_union_properties_with_all_params(self, client: Sink) -> None:
        body_param = client.body_params.object_with_union_properties(
            bar={"bar": 0},
            foo=0,
        )
        assert body_param is None

    @parametrize
    def test_raw_response_object_with_union_properties(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.object_with_union_properties(
            bar={"bar": 0},
            foo=0,
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    def test_streaming_response_object_with_union_properties(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.object_with_union_properties(
            bar={"bar": 0},
            foo=0,
        ) as response:
            assert not response.is_closed

            body_param = response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_only_read_only_properties(self, client: Sink) -> None:
        body_param = client.body_params.only_read_only_properties()
        assert body_param is None

    @parametrize
    def test_raw_response_only_read_only_properties(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.only_read_only_properties()

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    def test_streaming_response_only_read_only_properties(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.only_read_only_properties() as response:
            assert not response.is_closed

            body_param = response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_param_in_model_name_ref(self, client: Sink) -> None:
        body_param = client.body_params.param_in_model_name_ref(
            model_ref={"foo": "string"},
            name="name",
        )
        assert body_param is None

    @parametrize
    def test_raw_response_param_in_model_name_ref(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.param_in_model_name_ref(
            model_ref={"foo": "string"},
            name="name",
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    def test_streaming_response_param_in_model_name_ref(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.param_in_model_name_ref(
            model_ref={"foo": "string"},
            name="name",
        ) as response:
            assert not response.is_closed

            body_param = response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_property_model_ref(self, client: Sink) -> None:
        body_param = client.body_params.property_model_ref(
            model_ref={},
            name="name",
        )
        assert body_param is None

    @parametrize
    def test_method_property_model_ref_with_all_params(self, client: Sink) -> None:
        body_param = client.body_params.property_model_ref(
            model_ref={
                "id": "id",
                "bar": True,
            },
            name="name",
        )
        assert body_param is None

    @parametrize
    def test_raw_response_property_model_ref(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.property_model_ref(
            model_ref={},
            name="name",
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    def test_streaming_response_property_model_ref(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.property_model_ref(
            model_ref={},
            name="name",
        ) as response:
            assert not response.is_closed

            body_param = response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_property_with_complex_union(self, client: Sink) -> None:
        body_param = client.body_params.property_with_complex_union(
            name="name",
            unions={},
        )
        assert body_param is None

    @parametrize
    def test_method_property_with_complex_union_with_all_params(self, client: Sink) -> None:
        body_param = client.body_params.property_with_complex_union(
            name="name",
            unions={"in_both": True},
        )
        assert body_param is None

    @parametrize
    def test_raw_response_property_with_complex_union(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.property_with_complex_union(
            name="name",
            unions={},
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    def test_streaming_response_property_with_complex_union(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.property_with_complex_union(
            name="name",
            unions={},
        ) as response:
            assert not response.is_closed

            body_param = response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_read_only_properties(self, client: Sink) -> None:
        body_param = client.body_params.read_only_properties()
        assert body_param is None

    @parametrize
    def test_method_read_only_properties_with_all_params(self, client: Sink) -> None:
        body_param = client.body_params.read_only_properties(
            in_both=True,
        )
        assert body_param is None

    @parametrize
    def test_raw_response_read_only_properties(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.read_only_properties()

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    def test_streaming_response_read_only_properties(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.read_only_properties() as response:
            assert not response.is_closed

            body_param = response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_string_map_model_ref(self, client: Sink) -> None:
        body_param = client.body_params.string_map_model_ref(
            model_ref={"foo": "string"},
            name="name",
        )
        assert body_param is None

    @parametrize
    def test_raw_response_string_map_model_ref(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.string_map_model_ref(
            model_ref={"foo": "string"},
            name="name",
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    def test_streaming_response_string_map_model_ref(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.string_map_model_ref(
            model_ref={"foo": "string"},
            name="name",
        ) as response:
            assert not response.is_closed

            body_param = response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_top_level_all_of(self, client: Sink) -> None:
        body_param = client.body_params.top_level_all_of(
            is_foo=True,
            kind="VIRTUAL",
        )
        assert_matches_type(BodyParamTopLevelAllOfResponse, body_param, path=["response"])

    @parametrize
    def test_raw_response_top_level_all_of(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.top_level_all_of(
            is_foo=True,
            kind="VIRTUAL",
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert_matches_type(BodyParamTopLevelAllOfResponse, body_param, path=["response"])

    @parametrize
    def test_streaming_response_top_level_all_of(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.top_level_all_of(
            is_foo=True,
            kind="VIRTUAL",
        ) as response:
            assert not response.is_closed

            body_param = response.parse()
            assert_matches_type(BodyParamTopLevelAllOfResponse, body_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_top_level_all_of_nested_object(self, client: Sink) -> None:
        body_param = client.body_params.top_level_all_of_nested_object(
            kind="VIRTUAL",
        )
        assert body_param is None

    @parametrize
    def test_method_top_level_all_of_nested_object_with_all_params(self, client: Sink) -> None:
        body_param = client.body_params.top_level_all_of_nested_object(
            kind="VIRTUAL",
            nested_obj={"is_foo": True},
        )
        assert body_param is None

    @parametrize
    def test_raw_response_top_level_all_of_nested_object(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.top_level_all_of_nested_object(
            kind="VIRTUAL",
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    def test_streaming_response_top_level_all_of_nested_object(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.top_level_all_of_nested_object(
            kind="VIRTUAL",
        ) as response:
            assert not response.is_closed

            body_param = response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_top_level_any_of_overload_1(self, client: Sink) -> None:
        body_param = client.body_params.top_level_any_of(
            kind="VIRTUAL",
        )
        assert_matches_type(BodyParamTopLevelAnyOfResponse, body_param, path=["response"])

    @parametrize
    def test_raw_response_top_level_any_of_overload_1(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.top_level_any_of(
            kind="VIRTUAL",
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert_matches_type(BodyParamTopLevelAnyOfResponse, body_param, path=["response"])

    @parametrize
    def test_streaming_response_top_level_any_of_overload_1(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.top_level_any_of(
            kind="VIRTUAL",
        ) as response:
            assert not response.is_closed

            body_param = response.parse()
            assert_matches_type(BodyParamTopLevelAnyOfResponse, body_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_top_level_any_of_overload_2(self, client: Sink) -> None:
        body_param = client.body_params.top_level_any_of(
            is_foo=True,
        )
        assert_matches_type(BodyParamTopLevelAnyOfResponse, body_param, path=["response"])

    @parametrize
    def test_raw_response_top_level_any_of_overload_2(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.top_level_any_of(
            is_foo=True,
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert_matches_type(BodyParamTopLevelAnyOfResponse, body_param, path=["response"])

    @parametrize
    def test_streaming_response_top_level_any_of_overload_2(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.top_level_any_of(
            is_foo=True,
        ) as response:
            assert not response.is_closed

            body_param = response.parse()
            assert_matches_type(BodyParamTopLevelAnyOfResponse, body_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_top_level_any_of_with_ref_overload_1(self, client: Sink) -> None:
        body_param = client.body_params.top_level_any_of_with_ref(
            kind="VIRTUAL",
        )
        assert_matches_type(BasicSharedModelObject, body_param, path=["response"])

    @parametrize
    def test_raw_response_top_level_any_of_with_ref_overload_1(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.top_level_any_of_with_ref(
            kind="VIRTUAL",
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert_matches_type(BasicSharedModelObject, body_param, path=["response"])

    @parametrize
    def test_streaming_response_top_level_any_of_with_ref_overload_1(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.top_level_any_of_with_ref(
            kind="VIRTUAL",
        ) as response:
            assert not response.is_closed

            body_param = response.parse()
            assert_matches_type(BasicSharedModelObject, body_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_top_level_any_of_with_ref_overload_2(self, client: Sink) -> None:
        body_param = client.body_params.top_level_any_of_with_ref(
            is_foo=True,
        )
        assert_matches_type(BasicSharedModelObject, body_param, path=["response"])

    @parametrize
    def test_raw_response_top_level_any_of_with_ref_overload_2(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.top_level_any_of_with_ref(
            is_foo=True,
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert_matches_type(BasicSharedModelObject, body_param, path=["response"])

    @parametrize
    def test_streaming_response_top_level_any_of_with_ref_overload_2(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.top_level_any_of_with_ref(
            is_foo=True,
        ) as response:
            assert not response.is_closed

            body_param = response.parse()
            assert_matches_type(BasicSharedModelObject, body_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_top_level_array(self, client: Sink) -> None:
        body_param = client.body_params.top_level_array(
            items=[
                {
                    "bar": "bar",
                    "foo": "foo",
                }
            ],
        )
        assert body_param is None

    @parametrize
    def test_raw_response_top_level_array(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.top_level_array(
            items=[
                {
                    "bar": "bar",
                    "foo": "foo",
                }
            ],
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    def test_streaming_response_top_level_array(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.top_level_array(
            items=[
                {
                    "bar": "bar",
                    "foo": "foo",
                }
            ],
        ) as response:
            assert not response.is_closed

            body_param = response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_top_level_array_with_children(self, client: Sink) -> None:
        body_param = client.body_params.top_level_array_with_children(
            items=[{"id": "id"}],
        )
        assert body_param is None

    @parametrize
    def test_raw_response_top_level_array_with_children(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.top_level_array_with_children(
            items=[{"id": "id"}],
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    def test_streaming_response_top_level_array_with_children(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.top_level_array_with_children(
            items=[{"id": "id"}],
        ) as response:
            assert not response.is_closed

            body_param = response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_top_level_array_with_other_params(self, client: Sink) -> None:
        body_param = client.body_params.top_level_array_with_other_params(
            id="id",
            items=[
                {
                    "bar": "bar",
                    "foo": "foo",
                }
            ],
        )
        assert body_param is None

    @parametrize
    def test_raw_response_top_level_array_with_other_params(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.top_level_array_with_other_params(
            id="id",
            items=[
                {
                    "bar": "bar",
                    "foo": "foo",
                }
            ],
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    def test_streaming_response_top_level_array_with_other_params(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.top_level_array_with_other_params(
            id="id",
            items=[
                {
                    "bar": "bar",
                    "foo": "foo",
                }
            ],
        ) as response:
            assert not response.is_closed

            body_param = response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_top_level_one_of_overload_1(self, client: Sink) -> None:
        body_param = client.body_params.top_level_one_of(
            kind="VIRTUAL",
        )
        assert_matches_type(BodyParamTopLevelOneOfResponse, body_param, path=["response"])

    @parametrize
    def test_raw_response_top_level_one_of_overload_1(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.top_level_one_of(
            kind="VIRTUAL",
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert_matches_type(BodyParamTopLevelOneOfResponse, body_param, path=["response"])

    @parametrize
    def test_streaming_response_top_level_one_of_overload_1(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.top_level_one_of(
            kind="VIRTUAL",
        ) as response:
            assert not response.is_closed

            body_param = response.parse()
            assert_matches_type(BodyParamTopLevelOneOfResponse, body_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_top_level_one_of_overload_2(self, client: Sink) -> None:
        body_param = client.body_params.top_level_one_of(
            is_foo=True,
        )
        assert_matches_type(BodyParamTopLevelOneOfResponse, body_param, path=["response"])

    @parametrize
    def test_raw_response_top_level_one_of_overload_2(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.top_level_one_of(
            is_foo=True,
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert_matches_type(BodyParamTopLevelOneOfResponse, body_param, path=["response"])

    @parametrize
    def test_streaming_response_top_level_one_of_overload_2(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.top_level_one_of(
            is_foo=True,
        ) as response:
            assert not response.is_closed

            body_param = response.parse()
            assert_matches_type(BodyParamTopLevelOneOfResponse, body_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_top_level_one_of_one_entry(self, client: Sink) -> None:
        body_param = client.body_params.top_level_one_of_one_entry(
            kind="VIRTUAL",
        )
        assert body_param is None

    @parametrize
    def test_raw_response_top_level_one_of_one_entry(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.top_level_one_of_one_entry(
            kind="VIRTUAL",
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    def test_streaming_response_top_level_one_of_one_entry(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.top_level_one_of_one_entry(
            kind="VIRTUAL",
        ) as response:
            assert not response.is_closed

            body_param = response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_top_level_shared_type(self, client: Sink) -> None:
        body_param = client.body_params.top_level_shared_type()
        assert body_param is None

    @parametrize
    def test_method_top_level_shared_type_with_all_params(self, client: Sink) -> None:
        body_param = client.body_params.top_level_shared_type(
            bar={"bar": 0},
            foo="foo",
        )
        assert body_param is None

    @parametrize
    def test_raw_response_top_level_shared_type(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.top_level_shared_type()

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    def test_streaming_response_top_level_shared_type(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.top_level_shared_type() as response:
            assert not response.is_closed

            body_param = response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_union_overlapping_prop_overload_1(self, client: Sink) -> None:
        body_param = client.body_params.union_overlapping_prop(
            foo="foo",
        )
        assert_matches_type(BodyParamUnionOverlappingPropResponse, body_param, path=["response"])

    @parametrize
    def test_raw_response_union_overlapping_prop_overload_1(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.union_overlapping_prop(
            foo="foo",
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert_matches_type(BodyParamUnionOverlappingPropResponse, body_param, path=["response"])

    @parametrize
    def test_streaming_response_union_overlapping_prop_overload_1(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.union_overlapping_prop(
            foo="foo",
        ) as response:
            assert not response.is_closed

            body_param = response.parse()
            assert_matches_type(BodyParamUnionOverlappingPropResponse, body_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_union_overlapping_prop_overload_2(self, client: Sink) -> None:
        body_param = client.body_params.union_overlapping_prop()
        assert_matches_type(BodyParamUnionOverlappingPropResponse, body_param, path=["response"])

    @parametrize
    def test_method_union_overlapping_prop_with_all_params_overload_2(self, client: Sink) -> None:
        body_param = client.body_params.union_overlapping_prop(
            foo=True,
        )
        assert_matches_type(BodyParamUnionOverlappingPropResponse, body_param, path=["response"])

    @parametrize
    def test_raw_response_union_overlapping_prop_overload_2(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.union_overlapping_prop()

        assert response.is_closed is True
        body_param = response.parse()
        assert_matches_type(BodyParamUnionOverlappingPropResponse, body_param, path=["response"])

    @parametrize
    def test_streaming_response_union_overlapping_prop_overload_2(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.union_overlapping_prop() as response:
            assert not response.is_closed

            body_param = response.parse()
            assert_matches_type(BodyParamUnionOverlappingPropResponse, body_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_unknown_object(self, client: Sink) -> None:
        body_param = client.body_params.unknown_object(
            name="name",
            unknown_object_prop={},
        )
        assert body_param is None

    @parametrize
    def test_raw_response_unknown_object(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.unknown_object(
            name="name",
            unknown_object_prop={},
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    def test_streaming_response_unknown_object(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.unknown_object(
            name="name",
            unknown_object_prop={},
        ) as response:
            assert not response.is_closed

            body_param = response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_with_default_body_param_optional(self, client: Sink) -> None:
        body_param = client.body_params.with_default_body_param_optional()
        assert body_param is None

    @parametrize
    def test_method_with_default_body_param_optional_with_all_params(self, client: Sink) -> None:
        body_param = client.body_params.with_default_body_param_optional(
            my_version_body_param="my_version_body_param",
            normal_param=True,
        )
        assert body_param is None

    @parametrize
    def test_raw_response_with_default_body_param_optional(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.with_default_body_param_optional()

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    def test_streaming_response_with_default_body_param_optional(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.with_default_body_param_optional() as response:
            assert not response.is_closed

            body_param = response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_with_default_body_param_required(self, client: Sink) -> None:
        body_param = client.body_params.with_default_body_param_required(
            normal_param=True,
        )
        assert body_param is None

    @parametrize
    def test_raw_response_with_default_body_param_required(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.with_default_body_param_required(
            normal_param=True,
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    def test_streaming_response_with_default_body_param_required(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.with_default_body_param_required(
            normal_param=True,
        ) as response:
            assert not response.is_closed

            body_param = response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_with_model_property(self, client: Sink) -> None:
        body_param = client.body_params.with_model_property()
        assert body_param is None

    @parametrize
    def test_method_with_model_property_with_all_params(self, client: Sink) -> None:
        body_param = client.body_params.with_model_property(
            foo="foo",
            my_model={
                "id": "id",
                "bar": True,
            },
        )
        assert body_param is None

    @parametrize
    def test_raw_response_with_model_property(self, client: Sink) -> None:
        response = client.body_params.with_raw_response.with_model_property()

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    def test_streaming_response_with_model_property(self, client: Sink) -> None:
        with client.body_params.with_streaming_response.with_model_property() as response:
            assert not response.is_closed

            body_param = response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True


class TestAsyncBodyParams:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_duplicate_subproperty(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.duplicate_subproperty()
        assert_matches_type(ModelWithNestedModel, body_param, path=["response"])

    @parametrize
    async def test_method_duplicate_subproperty_with_all_params(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.duplicate_subproperty(
            baz={"bar": {"hello": "hello"}},
            foo={"bar": {"hello": "hello"}},
            foo_bar={"hello": "hello"},
            mapping={"hello": "hello"},
            mappings=[{"hello": "hello"}],
        )
        assert_matches_type(ModelWithNestedModel, body_param, path=["response"])

    @parametrize
    async def test_raw_response_duplicate_subproperty(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.duplicate_subproperty()

        assert response.is_closed is True
        body_param = response.parse()
        assert_matches_type(ModelWithNestedModel, body_param, path=["response"])

    @parametrize
    async def test_streaming_response_duplicate_subproperty(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.duplicate_subproperty() as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert_matches_type(ModelWithNestedModel, body_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_enum_properties(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.enum_properties()
        assert body_param is None

    @parametrize
    async def test_method_enum_properties_with_all_params(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.enum_properties(
            code=1,
            enabled=True,
            kind="failed",
        )
        assert body_param is None

    @parametrize
    async def test_raw_response_enum_properties(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.enum_properties()

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    async def test_streaming_response_enum_properties(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.enum_properties() as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_nested_request_models(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.nested_request_models()
        assert_matches_type(ModelWithNestedModel, body_param, path=["response"])

    @parametrize
    async def test_method_nested_request_models_with_all_params(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.nested_request_models(
            data={"foo": {"bar": {"baz": {"hello": "hello"}}}},
        )
        assert_matches_type(ModelWithNestedModel, body_param, path=["response"])

    @parametrize
    async def test_raw_response_nested_request_models(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.nested_request_models()

        assert response.is_closed is True
        body_param = response.parse()
        assert_matches_type(ModelWithNestedModel, body_param, path=["response"])

    @parametrize
    async def test_streaming_response_nested_request_models(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.nested_request_models() as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert_matches_type(ModelWithNestedModel, body_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_object_map_model_ref(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.object_map_model_ref(
            model_ref={"foo": {}},
            name="name",
        )
        assert body_param is None

    @parametrize
    async def test_raw_response_object_map_model_ref(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.object_map_model_ref(
            model_ref={"foo": {}},
            name="name",
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    async def test_streaming_response_object_map_model_ref(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.object_map_model_ref(
            model_ref={"foo": {}},
            name="name",
        ) as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_object_with_array_of_objects(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.object_with_array_of_objects()
        assert body_param is None

    @parametrize
    async def test_method_object_with_array_of_objects_with_all_params(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.object_with_array_of_objects(
            array_prop=[{"kind": "VIRTUAL"}],
        )
        assert body_param is None

    @parametrize
    async def test_raw_response_object_with_array_of_objects(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.object_with_array_of_objects()

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    async def test_streaming_response_object_with_array_of_objects(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.object_with_array_of_objects() as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_object_with_union_properties(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.object_with_union_properties(
            bar={"bar": 0},
            foo=0,
        )
        assert body_param is None

    @parametrize
    async def test_method_object_with_union_properties_with_all_params(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.object_with_union_properties(
            bar={"bar": 0},
            foo=0,
        )
        assert body_param is None

    @parametrize
    async def test_raw_response_object_with_union_properties(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.object_with_union_properties(
            bar={"bar": 0},
            foo=0,
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    async def test_streaming_response_object_with_union_properties(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.object_with_union_properties(
            bar={"bar": 0},
            foo=0,
        ) as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_only_read_only_properties(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.only_read_only_properties()
        assert body_param is None

    @parametrize
    async def test_raw_response_only_read_only_properties(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.only_read_only_properties()

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    async def test_streaming_response_only_read_only_properties(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.only_read_only_properties() as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_param_in_model_name_ref(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.param_in_model_name_ref(
            model_ref={"foo": "string"},
            name="name",
        )
        assert body_param is None

    @parametrize
    async def test_raw_response_param_in_model_name_ref(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.param_in_model_name_ref(
            model_ref={"foo": "string"},
            name="name",
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    async def test_streaming_response_param_in_model_name_ref(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.param_in_model_name_ref(
            model_ref={"foo": "string"},
            name="name",
        ) as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_property_model_ref(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.property_model_ref(
            model_ref={},
            name="name",
        )
        assert body_param is None

    @parametrize
    async def test_method_property_model_ref_with_all_params(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.property_model_ref(
            model_ref={
                "id": "id",
                "bar": True,
            },
            name="name",
        )
        assert body_param is None

    @parametrize
    async def test_raw_response_property_model_ref(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.property_model_ref(
            model_ref={},
            name="name",
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    async def test_streaming_response_property_model_ref(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.property_model_ref(
            model_ref={},
            name="name",
        ) as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_property_with_complex_union(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.property_with_complex_union(
            name="name",
            unions={},
        )
        assert body_param is None

    @parametrize
    async def test_method_property_with_complex_union_with_all_params(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.property_with_complex_union(
            name="name",
            unions={"in_both": True},
        )
        assert body_param is None

    @parametrize
    async def test_raw_response_property_with_complex_union(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.property_with_complex_union(
            name="name",
            unions={},
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    async def test_streaming_response_property_with_complex_union(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.property_with_complex_union(
            name="name",
            unions={},
        ) as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_read_only_properties(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.read_only_properties()
        assert body_param is None

    @parametrize
    async def test_method_read_only_properties_with_all_params(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.read_only_properties(
            in_both=True,
        )
        assert body_param is None

    @parametrize
    async def test_raw_response_read_only_properties(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.read_only_properties()

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    async def test_streaming_response_read_only_properties(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.read_only_properties() as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_string_map_model_ref(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.string_map_model_ref(
            model_ref={"foo": "string"},
            name="name",
        )
        assert body_param is None

    @parametrize
    async def test_raw_response_string_map_model_ref(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.string_map_model_ref(
            model_ref={"foo": "string"},
            name="name",
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    async def test_streaming_response_string_map_model_ref(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.string_map_model_ref(
            model_ref={"foo": "string"},
            name="name",
        ) as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_top_level_all_of(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.top_level_all_of(
            is_foo=True,
            kind="VIRTUAL",
        )
        assert_matches_type(BodyParamTopLevelAllOfResponse, body_param, path=["response"])

    @parametrize
    async def test_raw_response_top_level_all_of(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.top_level_all_of(
            is_foo=True,
            kind="VIRTUAL",
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert_matches_type(BodyParamTopLevelAllOfResponse, body_param, path=["response"])

    @parametrize
    async def test_streaming_response_top_level_all_of(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.top_level_all_of(
            is_foo=True,
            kind="VIRTUAL",
        ) as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert_matches_type(BodyParamTopLevelAllOfResponse, body_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_top_level_all_of_nested_object(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.top_level_all_of_nested_object(
            kind="VIRTUAL",
        )
        assert body_param is None

    @parametrize
    async def test_method_top_level_all_of_nested_object_with_all_params(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.top_level_all_of_nested_object(
            kind="VIRTUAL",
            nested_obj={"is_foo": True},
        )
        assert body_param is None

    @parametrize
    async def test_raw_response_top_level_all_of_nested_object(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.top_level_all_of_nested_object(
            kind="VIRTUAL",
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    async def test_streaming_response_top_level_all_of_nested_object(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.top_level_all_of_nested_object(
            kind="VIRTUAL",
        ) as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_top_level_any_of_overload_1(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.top_level_any_of(
            kind="VIRTUAL",
        )
        assert_matches_type(BodyParamTopLevelAnyOfResponse, body_param, path=["response"])

    @parametrize
    async def test_raw_response_top_level_any_of_overload_1(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.top_level_any_of(
            kind="VIRTUAL",
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert_matches_type(BodyParamTopLevelAnyOfResponse, body_param, path=["response"])

    @parametrize
    async def test_streaming_response_top_level_any_of_overload_1(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.top_level_any_of(
            kind="VIRTUAL",
        ) as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert_matches_type(BodyParamTopLevelAnyOfResponse, body_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_top_level_any_of_overload_2(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.top_level_any_of(
            is_foo=True,
        )
        assert_matches_type(BodyParamTopLevelAnyOfResponse, body_param, path=["response"])

    @parametrize
    async def test_raw_response_top_level_any_of_overload_2(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.top_level_any_of(
            is_foo=True,
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert_matches_type(BodyParamTopLevelAnyOfResponse, body_param, path=["response"])

    @parametrize
    async def test_streaming_response_top_level_any_of_overload_2(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.top_level_any_of(
            is_foo=True,
        ) as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert_matches_type(BodyParamTopLevelAnyOfResponse, body_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_top_level_any_of_with_ref_overload_1(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.top_level_any_of_with_ref(
            kind="VIRTUAL",
        )
        assert_matches_type(BasicSharedModelObject, body_param, path=["response"])

    @parametrize
    async def test_raw_response_top_level_any_of_with_ref_overload_1(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.top_level_any_of_with_ref(
            kind="VIRTUAL",
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert_matches_type(BasicSharedModelObject, body_param, path=["response"])

    @parametrize
    async def test_streaming_response_top_level_any_of_with_ref_overload_1(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.top_level_any_of_with_ref(
            kind="VIRTUAL",
        ) as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert_matches_type(BasicSharedModelObject, body_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_top_level_any_of_with_ref_overload_2(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.top_level_any_of_with_ref(
            is_foo=True,
        )
        assert_matches_type(BasicSharedModelObject, body_param, path=["response"])

    @parametrize
    async def test_raw_response_top_level_any_of_with_ref_overload_2(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.top_level_any_of_with_ref(
            is_foo=True,
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert_matches_type(BasicSharedModelObject, body_param, path=["response"])

    @parametrize
    async def test_streaming_response_top_level_any_of_with_ref_overload_2(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.top_level_any_of_with_ref(
            is_foo=True,
        ) as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert_matches_type(BasicSharedModelObject, body_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_top_level_array(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.top_level_array(
            items=[
                {
                    "bar": "bar",
                    "foo": "foo",
                }
            ],
        )
        assert body_param is None

    @parametrize
    async def test_raw_response_top_level_array(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.top_level_array(
            items=[
                {
                    "bar": "bar",
                    "foo": "foo",
                }
            ],
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    async def test_streaming_response_top_level_array(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.top_level_array(
            items=[
                {
                    "bar": "bar",
                    "foo": "foo",
                }
            ],
        ) as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_top_level_array_with_children(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.top_level_array_with_children(
            items=[{"id": "id"}],
        )
        assert body_param is None

    @parametrize
    async def test_raw_response_top_level_array_with_children(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.top_level_array_with_children(
            items=[{"id": "id"}],
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    async def test_streaming_response_top_level_array_with_children(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.top_level_array_with_children(
            items=[{"id": "id"}],
        ) as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_top_level_array_with_other_params(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.top_level_array_with_other_params(
            id="id",
            items=[
                {
                    "bar": "bar",
                    "foo": "foo",
                }
            ],
        )
        assert body_param is None

    @parametrize
    async def test_raw_response_top_level_array_with_other_params(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.top_level_array_with_other_params(
            id="id",
            items=[
                {
                    "bar": "bar",
                    "foo": "foo",
                }
            ],
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    async def test_streaming_response_top_level_array_with_other_params(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.top_level_array_with_other_params(
            id="id",
            items=[
                {
                    "bar": "bar",
                    "foo": "foo",
                }
            ],
        ) as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_top_level_one_of_overload_1(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.top_level_one_of(
            kind="VIRTUAL",
        )
        assert_matches_type(BodyParamTopLevelOneOfResponse, body_param, path=["response"])

    @parametrize
    async def test_raw_response_top_level_one_of_overload_1(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.top_level_one_of(
            kind="VIRTUAL",
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert_matches_type(BodyParamTopLevelOneOfResponse, body_param, path=["response"])

    @parametrize
    async def test_streaming_response_top_level_one_of_overload_1(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.top_level_one_of(
            kind="VIRTUAL",
        ) as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert_matches_type(BodyParamTopLevelOneOfResponse, body_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_top_level_one_of_overload_2(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.top_level_one_of(
            is_foo=True,
        )
        assert_matches_type(BodyParamTopLevelOneOfResponse, body_param, path=["response"])

    @parametrize
    async def test_raw_response_top_level_one_of_overload_2(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.top_level_one_of(
            is_foo=True,
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert_matches_type(BodyParamTopLevelOneOfResponse, body_param, path=["response"])

    @parametrize
    async def test_streaming_response_top_level_one_of_overload_2(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.top_level_one_of(
            is_foo=True,
        ) as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert_matches_type(BodyParamTopLevelOneOfResponse, body_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_top_level_one_of_one_entry(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.top_level_one_of_one_entry(
            kind="VIRTUAL",
        )
        assert body_param is None

    @parametrize
    async def test_raw_response_top_level_one_of_one_entry(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.top_level_one_of_one_entry(
            kind="VIRTUAL",
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    async def test_streaming_response_top_level_one_of_one_entry(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.top_level_one_of_one_entry(
            kind="VIRTUAL",
        ) as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_top_level_shared_type(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.top_level_shared_type()
        assert body_param is None

    @parametrize
    async def test_method_top_level_shared_type_with_all_params(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.top_level_shared_type(
            bar={"bar": 0},
            foo="foo",
        )
        assert body_param is None

    @parametrize
    async def test_raw_response_top_level_shared_type(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.top_level_shared_type()

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    async def test_streaming_response_top_level_shared_type(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.top_level_shared_type() as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_union_overlapping_prop_overload_1(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.union_overlapping_prop(
            foo="foo",
        )
        assert_matches_type(BodyParamUnionOverlappingPropResponse, body_param, path=["response"])

    @parametrize
    async def test_raw_response_union_overlapping_prop_overload_1(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.union_overlapping_prop(
            foo="foo",
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert_matches_type(BodyParamUnionOverlappingPropResponse, body_param, path=["response"])

    @parametrize
    async def test_streaming_response_union_overlapping_prop_overload_1(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.union_overlapping_prop(
            foo="foo",
        ) as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert_matches_type(BodyParamUnionOverlappingPropResponse, body_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_union_overlapping_prop_overload_2(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.union_overlapping_prop()
        assert_matches_type(BodyParamUnionOverlappingPropResponse, body_param, path=["response"])

    @parametrize
    async def test_method_union_overlapping_prop_with_all_params_overload_2(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.union_overlapping_prop(
            foo=True,
        )
        assert_matches_type(BodyParamUnionOverlappingPropResponse, body_param, path=["response"])

    @parametrize
    async def test_raw_response_union_overlapping_prop_overload_2(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.union_overlapping_prop()

        assert response.is_closed is True
        body_param = response.parse()
        assert_matches_type(BodyParamUnionOverlappingPropResponse, body_param, path=["response"])

    @parametrize
    async def test_streaming_response_union_overlapping_prop_overload_2(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.union_overlapping_prop() as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert_matches_type(BodyParamUnionOverlappingPropResponse, body_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_unknown_object(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.unknown_object(
            name="name",
            unknown_object_prop={},
        )
        assert body_param is None

    @parametrize
    async def test_raw_response_unknown_object(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.unknown_object(
            name="name",
            unknown_object_prop={},
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    async def test_streaming_response_unknown_object(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.unknown_object(
            name="name",
            unknown_object_prop={},
        ) as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_with_default_body_param_optional(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.with_default_body_param_optional()
        assert body_param is None

    @parametrize
    async def test_method_with_default_body_param_optional_with_all_params(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.with_default_body_param_optional(
            my_version_body_param="my_version_body_param",
            normal_param=True,
        )
        assert body_param is None

    @parametrize
    async def test_raw_response_with_default_body_param_optional(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.with_default_body_param_optional()

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    async def test_streaming_response_with_default_body_param_optional(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.with_default_body_param_optional() as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_with_default_body_param_required(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.with_default_body_param_required(
            normal_param=True,
        )
        assert body_param is None

    @parametrize
    async def test_raw_response_with_default_body_param_required(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.with_default_body_param_required(
            normal_param=True,
        )

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    async def test_streaming_response_with_default_body_param_required(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.with_default_body_param_required(
            normal_param=True,
        ) as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_with_model_property(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.with_model_property()
        assert body_param is None

    @parametrize
    async def test_method_with_model_property_with_all_params(self, async_client: AsyncSink) -> None:
        body_param = await async_client.body_params.with_model_property(
            foo="foo",
            my_model={
                "id": "id",
                "bar": True,
            },
        )
        assert body_param is None

    @parametrize
    async def test_raw_response_with_model_property(self, async_client: AsyncSink) -> None:
        response = await async_client.body_params.with_raw_response.with_model_property()

        assert response.is_closed is True
        body_param = response.parse()
        assert body_param is None

    @parametrize
    async def test_streaming_response_with_model_property(self, async_client: AsyncSink) -> None:
        async with async_client.body_params.with_streaming_response.with_model_property() as response:
            assert not response.is_closed

            body_param = await response.parse()
            assert body_param is None

        assert cast(Any, response.is_closed) is True
