# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Union, Iterable, cast
from typing_extensions import Literal, overload

import httpx

from ... import _legacy_response
from .unions import (
    UnionsResource,
    AsyncUnionsResource,
    UnionsResourceWithRawResponse,
    AsyncUnionsResourceWithRawResponse,
    UnionsResourceWithStreamingResponse,
    AsyncUnionsResourceWithStreamingResponse,
)
from ...types import (
    body_param_unknown_object_params,
    body_param_enum_properties_params,
    body_param_top_level_all_of_params,
    body_param_top_level_any_of_params,
    body_param_top_level_one_of_params,
    body_param_property_model_ref_params,
    body_param_with_model_property_params,
    body_param_object_map_model_ref_params,
    body_param_read_only_properties_params,
    body_param_string_map_model_ref_params,
    body_param_duplicate_subproperty_params,
    body_param_nested_request_models_params,
    body_param_top_level_shared_type_params,
    body_param_union_overlapping_prop_params,
    body_param_param_in_model_name_ref_params,
    body_param_top_level_any_of_with_ref_params,
    body_param_top_level_one_of_one_entry_params,
    body_param_property_with_complex_union_params,
    body_param_object_with_array_of_objects_params,
    body_param_object_with_union_properties_params,
    body_param_top_level_array_with_children_params,
    body_param_top_level_all_of_nested_object_params,
    body_param_with_default_body_param_optional_params,
    body_param_with_default_body_param_required_params,
    body_param_top_level_array_with_other_params_params,
)
from .objects import (
    ObjectsResource,
    AsyncObjectsResource,
    ObjectsResourceWithRawResponse,
    AsyncObjectsResourceWithRawResponse,
    ObjectsResourceWithStreamingResponse,
    AsyncObjectsResourceWithStreamingResponse,
)
from ..._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, not_given
from ..._utils import required_args, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ..._base_client import make_request_options
from ...types.my_model_param import MyModelParam
from ...types.object_map_model_param import ObjectMapModelParam
from ...types.string_map_model_param import StringMapModelParam
from ...types.model_with_nested_model import ModelWithNestedModel
from ...types.unknown_object_model_param import UnknownObjectModelParam
from ...types.shared_params.simple_object import SimpleObject
from ...types.nested_request_model_a_param import NestedRequestModelAParam
from ...types.model_with_param_in_name_param import ModelWithParamInNameParam
from ...types.shared.basic_shared_model_object import BasicSharedModelObject as SharedBasicSharedModelObject
from ...types.body_param_top_level_all_of_response import BodyParamTopLevelAllOfResponse
from ...types.body_param_top_level_any_of_response import BodyParamTopLevelAnyOfResponse
from ...types.body_param_top_level_one_of_response import BodyParamTopLevelOneOfResponse
from ...types.shared_params.basic_shared_model_object import (
    BasicSharedModelObject as SharedParamsBasicSharedModelObject,
)
from ...types.body_param_union_overlapping_prop_response import BodyParamUnionOverlappingPropResponse

__all__ = ["BodyParamsResource", "AsyncBodyParamsResource"]


class BodyParamsResource(SyncAPIResource):
    @cached_property
    def objects(self) -> ObjectsResource:
        return ObjectsResource(self._client)

    @cached_property
    def unions(self) -> UnionsResource:
        return UnionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> BodyParamsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return BodyParamsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BodyParamsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return BodyParamsResourceWithStreamingResponse(self)

    def duplicate_subproperty(
        self,
        *,
        baz: body_param_duplicate_subproperty_params.Baz | Omit = omit,
        foo: body_param_duplicate_subproperty_params.Foo | Omit = omit,
        foo_bar: body_param_duplicate_subproperty_params.FooBar | Omit = omit,
        mapping: body_param_duplicate_subproperty_params.Mapping | Omit = omit,
        mappings: Iterable[body_param_duplicate_subproperty_params.Mapping] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ModelWithNestedModel:
        """
        An edge case where there are nested sub-properties of the same name with
        possible clashes.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/body_params/with_duplicate_subproperty",
            body=maybe_transform(
                {
                    "baz": baz,
                    "foo": foo,
                    "foo_bar": foo_bar,
                    "mapping": mapping,
                    "mappings": mappings,
                },
                body_param_duplicate_subproperty_params.BodyParamDuplicateSubpropertyParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ModelWithNestedModel,
        )

    def enum_properties(
        self,
        *,
        code: Literal[1, 2] | Omit = omit,
        enabled: Literal[True] | Omit = omit,
        kind: Literal["failed", "success"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` with various enums properties

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/body_params/enum_properties",
            body=maybe_transform(
                {
                    "code": code,
                    "enabled": enabled,
                    "kind": kind,
                },
                body_param_enum_properties_params.BodyParamEnumPropertiesParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def nested_request_models(
        self,
        *,
        data: NestedRequestModelAParam | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ModelWithNestedModel:
        """
        Should return a ModelWithNestedModel object with a `properties` field that we
        can rename in the Stainless config to a prettier name.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/body_params/with_nested_models",
            body=maybe_transform(
                {"data": data}, body_param_nested_request_models_params.BodyParamNestedRequestModelsParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ModelWithNestedModel,
        )

    def object_map_model_ref(
        self,
        *,
        model_ref: ObjectMapModelParam,
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that has an `additionalProperties` object schema
        that is defined as a model in the config.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/body_params/object_map_model_ref",
            body=maybe_transform(
                {
                    "model_ref": model_ref,
                    "name": name,
                },
                body_param_object_map_model_ref_params.BodyParamObjectMapModelRefParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def object_with_array_of_objects(
        self,
        *,
        array_prop: Iterable[body_param_object_with_array_of_objects_params.ArrayProp] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with an object `requestBody` that has an array property with `object`
        items.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/body_params/object_with_array_of_objects",
            body=maybe_transform(
                {"array_prop": array_prop},
                body_param_object_with_array_of_objects_params.BodyParamObjectWithArrayOfObjectsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def object_with_union_properties(
        self,
        *,
        bar: body_param_object_with_union_properties_params.Bar,
        foo: Union[float, str, bool, object],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with an object `requestBody` that has properties with union types.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/body_params/object_with_union_properties",
            body=maybe_transform(
                {
                    "bar": bar,
                    "foo": foo,
                },
                body_param_object_with_union_properties_params.BodyParamObjectWithUnionPropertiesParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def only_read_only_properties(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """Endpoint with a `requestBody` that only has `readOnly` properties"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._patch(
            "/body_params/only_read_only_properties",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def param_in_model_name_ref(
        self,
        *,
        model_ref: ModelWithParamInNameParam,
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that has a schema that is defined as a model in
        the config with "param" in the name.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/body_params/param_in_model_name_ref",
            body=maybe_transform(
                {
                    "model_ref": model_ref,
                    "name": name,
                },
                body_param_param_in_model_name_ref_params.BodyParamParamInModelNameRefParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def property_model_ref(
        self,
        *,
        model_ref: MyModelParam,
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that has a property that is defined as a model in
        the config.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/body_params/property_model_ref",
            body=maybe_transform(
                {
                    "model_ref": model_ref,
                    "name": name,
                },
                body_param_property_model_ref_params.BodyParamPropertyModelRefParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def property_with_complex_union(
        self,
        *,
        name: str,
        unions: body_param_property_with_complex_union_params.Unions,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that has a property that is a union type of
        complex types.

        Args:
          unions: This is an object with required properties

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/body_params/property_with_complex_union",
            body=maybe_transform(
                {
                    "name": name,
                    "unions": unions,
                },
                body_param_property_with_complex_union_params.BodyParamPropertyWithComplexUnionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def read_only_properties(
        self,
        *,
        in_both: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that sets `readOnly` to `true` on top level
        properties

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/body_params/read_only_properties",
            body=maybe_transform(
                {"in_both": in_both}, body_param_read_only_properties_params.BodyParamReadOnlyPropertiesParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def string_map_model_ref(
        self,
        *,
        model_ref: StringMapModelParam,
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that has an `additionalProperties` string schema
        that is defined as a model in the config.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/body_params/string_map_model_ref",
            body=maybe_transform(
                {
                    "model_ref": model_ref,
                    "name": name,
                },
                body_param_string_map_model_ref_params.BodyParamStringMapModelRefParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def top_level_all_of(
        self,
        *,
        is_foo: bool,
        kind: Literal["VIRTUAL", "PHYSICAL"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelAllOfResponse:
        """
        Endpoint with a `requestBody` making use of allOf.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/body_params/top_level_allOf",
            body=maybe_transform(
                {
                    "is_foo": is_foo,
                    "kind": kind,
                },
                body_param_top_level_all_of_params.BodyParamTopLevelAllOfParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BodyParamTopLevelAllOfResponse,
        )

    def top_level_all_of_nested_object(
        self,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"],
        nested_obj: body_param_top_level_all_of_nested_object_params.NestedObj | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` making use of allOf where one of the properties is
        an object type.

        Args:
          nested_obj: This is an object with required properties

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/body_params/top_level_allOf_nested_object",
            body=maybe_transform(
                {
                    "kind": kind,
                    "nested_obj": nested_obj,
                },
                body_param_top_level_all_of_nested_object_params.BodyParamTopLevelAllOfNestedObjectParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    @overload
    def top_level_any_of(
        self,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelAnyOfResponse:
        """
        Endpoint with a `requestBody` making use of anyOf.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    def top_level_any_of(
        self,
        *,
        is_foo: bool,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelAnyOfResponse:
        """
        Endpoint with a `requestBody` making use of anyOf.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["kind"], ["is_foo"])
    def top_level_any_of(
        self,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"] | Omit = omit,
        is_foo: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelAnyOfResponse:
        return cast(
            BodyParamTopLevelAnyOfResponse,
            self._post(
                "/body_params/top_level_anyOf",
                body=maybe_transform(
                    {
                        "kind": kind,
                        "is_foo": is_foo,
                    },
                    body_param_top_level_any_of_params.BodyParamTopLevelAnyOfParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    idempotency_key=idempotency_key,
                ),
                cast_to=cast(
                    Any, BodyParamTopLevelAnyOfResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    @overload
    def top_level_any_of_with_ref(
        self,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> SharedBasicSharedModelObject:
        """
        Endpoint with a `requestBody` pointing to a $ref'd schema that is an `anyOf`.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    def top_level_any_of_with_ref(
        self,
        *,
        is_foo: bool,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> SharedBasicSharedModelObject:
        """
        Endpoint with a `requestBody` pointing to a $ref'd schema that is an `anyOf`.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["kind"], ["is_foo"])
    def top_level_any_of_with_ref(
        self,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"] | Omit = omit,
        is_foo: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> SharedBasicSharedModelObject:
        return self._post(
            "/body_params/top_level_anyOf_with_ref",
            body=maybe_transform(
                {
                    "kind": kind,
                    "is_foo": is_foo,
                },
                body_param_top_level_any_of_with_ref_params.BodyParamTopLevelAnyOfWithRefParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=SharedBasicSharedModelObject,
        )

    def top_level_array(
        self,
        *,
        items: Iterable[SharedParamsBasicSharedModelObject],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that is an `array` type.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/body_params/top_level_array",
            body=maybe_transform(items, Iterable[SharedParamsBasicSharedModelObject]),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def top_level_array_with_children(
        self,
        *,
        items: Iterable[body_param_top_level_array_with_children_params.Item],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that is an `array` type with non-model children.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/body_params/top_level_array_with_children",
            body=maybe_transform(items, Iterable[body_param_top_level_array_with_children_params.Item]),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def top_level_array_with_other_params(
        self,
        *,
        id: str,
        items: Iterable[SharedParamsBasicSharedModelObject],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that is an `array` type.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/body_params/top_level_array_with_other_params",
            body=maybe_transform(items, Iterable[SharedParamsBasicSharedModelObject]),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
                query=maybe_transform(
                    {"id": id},
                    body_param_top_level_array_with_other_params_params.BodyParamTopLevelArrayWithOtherParamsParams,
                ),
            ),
            cast_to=NoneType,
        )

    @overload
    def top_level_one_of(
        self,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelOneOfResponse:
        """
        Endpoint with a `requestBody` making use of oneOf.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    def top_level_one_of(
        self,
        *,
        is_foo: bool,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelOneOfResponse:
        """
        Endpoint with a `requestBody` making use of oneOf.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["kind"], ["is_foo"])
    def top_level_one_of(
        self,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"] | Omit = omit,
        is_foo: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelOneOfResponse:
        return cast(
            BodyParamTopLevelOneOfResponse,
            self._post(
                "/body_params/top_level_oneOf",
                body=maybe_transform(
                    {
                        "kind": kind,
                        "is_foo": is_foo,
                    },
                    body_param_top_level_one_of_params.BodyParamTopLevelOneOfParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    idempotency_key=idempotency_key,
                ),
                cast_to=cast(
                    Any, BodyParamTopLevelOneOfResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def top_level_one_of_one_entry(
        self,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` making use of oneOf but only contains one entry in
        the union.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/body_params/top_level_oneOf_one_entry",
            body=maybe_transform(
                {"kind": kind}, body_param_top_level_one_of_one_entry_params.BodyParamTopLevelOneOfOneEntryParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def top_level_shared_type(
        self,
        *,
        bar: SimpleObject | Omit = omit,
        foo: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        The request body being set to a $ref that is a shared type in the stainless
        config correctly references it.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/body_params/top_level_shared_type",
            body=maybe_transform(
                {
                    "bar": bar,
                    "foo": foo,
                },
                body_param_top_level_shared_type_params.BodyParamTopLevelSharedTypeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    @overload
    def union_overlapping_prop(
        self,
        *,
        foo: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BodyParamUnionOverlappingPropResponse:
        """
        Endpoint with a `requestBody` making use of anyOf where the same property is
        defined in both variants.

        Args:
          foo: FOO 1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    def union_overlapping_prop(
        self,
        *,
        foo: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BodyParamUnionOverlappingPropResponse:
        """
        Endpoint with a `requestBody` making use of anyOf where the same property is
        defined in both variants.

        Args:
          foo: FOO 2

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    def union_overlapping_prop(
        self,
        *,
        foo: str | bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BodyParamUnionOverlappingPropResponse:
        return self._post(
            "/body_params/top_level_anyOf_overlapping_property",
            body=maybe_transform(
                {"foo": foo}, body_param_union_overlapping_prop_params.BodyParamUnionOverlappingPropParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BodyParamUnionOverlappingPropResponse,
        )

    def unknown_object(
        self,
        *,
        name: str,
        unknown_object_prop: UnknownObjectModelParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that has an untyped object schema that is defined
        as a model in the config.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/body_params/unknown_object",
            body=maybe_transform(
                {
                    "name": name,
                    "unknown_object_prop": unknown_object_prop,
                },
                body_param_unknown_object_params.BodyParamUnknownObjectParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def with_default_body_param_optional(
        self,
        *,
        my_version_body_param: str = "v1.4",
        normal_param: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with an optional request property that has a default value set.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/body_params/with_default_body_param_optional",
            body=maybe_transform(
                {
                    "my_version_body_param": my_version_body_param,
                    "normal_param": normal_param,
                },
                body_param_with_default_body_param_optional_params.BodyParamWithDefaultBodyParamOptionalParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def with_default_body_param_required(
        self,
        *,
        my_version_body_param: str = "v1.4",
        normal_param: bool,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a required request property that has a default value set.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/body_params/with_default_body_param_required",
            body=maybe_transform(
                {
                    "my_version_body_param": my_version_body_param,
                    "normal_param": normal_param,
                },
                body_param_with_default_body_param_required_params.BodyParamWithDefaultBodyParamRequiredParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def with_model_property(
        self,
        *,
        foo: str | Omit = omit,
        my_model: MyModelParam | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a request body that contains a property that points to a model
        reference.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/body_params/with_model_property",
            body=maybe_transform(
                {
                    "foo": foo,
                    "my_model": my_model,
                },
                body_param_with_model_property_params.BodyParamWithModelPropertyParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )


class AsyncBodyParamsResource(AsyncAPIResource):
    @cached_property
    def objects(self) -> AsyncObjectsResource:
        return AsyncObjectsResource(self._client)

    @cached_property
    def unions(self) -> AsyncUnionsResource:
        return AsyncUnionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncBodyParamsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncBodyParamsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBodyParamsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncBodyParamsResourceWithStreamingResponse(self)

    async def duplicate_subproperty(
        self,
        *,
        baz: body_param_duplicate_subproperty_params.Baz | Omit = omit,
        foo: body_param_duplicate_subproperty_params.Foo | Omit = omit,
        foo_bar: body_param_duplicate_subproperty_params.FooBar | Omit = omit,
        mapping: body_param_duplicate_subproperty_params.Mapping | Omit = omit,
        mappings: Iterable[body_param_duplicate_subproperty_params.Mapping] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ModelWithNestedModel:
        """
        An edge case where there are nested sub-properties of the same name with
        possible clashes.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/body_params/with_duplicate_subproperty",
            body=await async_maybe_transform(
                {
                    "baz": baz,
                    "foo": foo,
                    "foo_bar": foo_bar,
                    "mapping": mapping,
                    "mappings": mappings,
                },
                body_param_duplicate_subproperty_params.BodyParamDuplicateSubpropertyParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ModelWithNestedModel,
        )

    async def enum_properties(
        self,
        *,
        code: Literal[1, 2] | Omit = omit,
        enabled: Literal[True] | Omit = omit,
        kind: Literal["failed", "success"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` with various enums properties

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/body_params/enum_properties",
            body=await async_maybe_transform(
                {
                    "code": code,
                    "enabled": enabled,
                    "kind": kind,
                },
                body_param_enum_properties_params.BodyParamEnumPropertiesParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    async def nested_request_models(
        self,
        *,
        data: NestedRequestModelAParam | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ModelWithNestedModel:
        """
        Should return a ModelWithNestedModel object with a `properties` field that we
        can rename in the Stainless config to a prettier name.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/body_params/with_nested_models",
            body=await async_maybe_transform(
                {"data": data}, body_param_nested_request_models_params.BodyParamNestedRequestModelsParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ModelWithNestedModel,
        )

    async def object_map_model_ref(
        self,
        *,
        model_ref: ObjectMapModelParam,
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that has an `additionalProperties` object schema
        that is defined as a model in the config.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/body_params/object_map_model_ref",
            body=await async_maybe_transform(
                {
                    "model_ref": model_ref,
                    "name": name,
                },
                body_param_object_map_model_ref_params.BodyParamObjectMapModelRefParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    async def object_with_array_of_objects(
        self,
        *,
        array_prop: Iterable[body_param_object_with_array_of_objects_params.ArrayProp] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with an object `requestBody` that has an array property with `object`
        items.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/body_params/object_with_array_of_objects",
            body=await async_maybe_transform(
                {"array_prop": array_prop},
                body_param_object_with_array_of_objects_params.BodyParamObjectWithArrayOfObjectsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    async def object_with_union_properties(
        self,
        *,
        bar: body_param_object_with_union_properties_params.Bar,
        foo: Union[float, str, bool, object],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with an object `requestBody` that has properties with union types.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/body_params/object_with_union_properties",
            body=await async_maybe_transform(
                {
                    "bar": bar,
                    "foo": foo,
                },
                body_param_object_with_union_properties_params.BodyParamObjectWithUnionPropertiesParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    async def only_read_only_properties(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """Endpoint with a `requestBody` that only has `readOnly` properties"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._patch(
            "/body_params/only_read_only_properties",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    async def param_in_model_name_ref(
        self,
        *,
        model_ref: ModelWithParamInNameParam,
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that has a schema that is defined as a model in
        the config with "param" in the name.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/body_params/param_in_model_name_ref",
            body=await async_maybe_transform(
                {
                    "model_ref": model_ref,
                    "name": name,
                },
                body_param_param_in_model_name_ref_params.BodyParamParamInModelNameRefParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    async def property_model_ref(
        self,
        *,
        model_ref: MyModelParam,
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that has a property that is defined as a model in
        the config.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/body_params/property_model_ref",
            body=await async_maybe_transform(
                {
                    "model_ref": model_ref,
                    "name": name,
                },
                body_param_property_model_ref_params.BodyParamPropertyModelRefParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    async def property_with_complex_union(
        self,
        *,
        name: str,
        unions: body_param_property_with_complex_union_params.Unions,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that has a property that is a union type of
        complex types.

        Args:
          unions: This is an object with required properties

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/body_params/property_with_complex_union",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "unions": unions,
                },
                body_param_property_with_complex_union_params.BodyParamPropertyWithComplexUnionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    async def read_only_properties(
        self,
        *,
        in_both: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that sets `readOnly` to `true` on top level
        properties

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/body_params/read_only_properties",
            body=await async_maybe_transform(
                {"in_both": in_both}, body_param_read_only_properties_params.BodyParamReadOnlyPropertiesParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    async def string_map_model_ref(
        self,
        *,
        model_ref: StringMapModelParam,
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that has an `additionalProperties` string schema
        that is defined as a model in the config.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/body_params/string_map_model_ref",
            body=await async_maybe_transform(
                {
                    "model_ref": model_ref,
                    "name": name,
                },
                body_param_string_map_model_ref_params.BodyParamStringMapModelRefParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    async def top_level_all_of(
        self,
        *,
        is_foo: bool,
        kind: Literal["VIRTUAL", "PHYSICAL"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelAllOfResponse:
        """
        Endpoint with a `requestBody` making use of allOf.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/body_params/top_level_allOf",
            body=await async_maybe_transform(
                {
                    "is_foo": is_foo,
                    "kind": kind,
                },
                body_param_top_level_all_of_params.BodyParamTopLevelAllOfParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BodyParamTopLevelAllOfResponse,
        )

    async def top_level_all_of_nested_object(
        self,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"],
        nested_obj: body_param_top_level_all_of_nested_object_params.NestedObj | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` making use of allOf where one of the properties is
        an object type.

        Args:
          nested_obj: This is an object with required properties

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/body_params/top_level_allOf_nested_object",
            body=await async_maybe_transform(
                {
                    "kind": kind,
                    "nested_obj": nested_obj,
                },
                body_param_top_level_all_of_nested_object_params.BodyParamTopLevelAllOfNestedObjectParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    @overload
    async def top_level_any_of(
        self,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelAnyOfResponse:
        """
        Endpoint with a `requestBody` making use of anyOf.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    async def top_level_any_of(
        self,
        *,
        is_foo: bool,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelAnyOfResponse:
        """
        Endpoint with a `requestBody` making use of anyOf.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["kind"], ["is_foo"])
    async def top_level_any_of(
        self,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"] | Omit = omit,
        is_foo: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelAnyOfResponse:
        return cast(
            BodyParamTopLevelAnyOfResponse,
            await self._post(
                "/body_params/top_level_anyOf",
                body=await async_maybe_transform(
                    {
                        "kind": kind,
                        "is_foo": is_foo,
                    },
                    body_param_top_level_any_of_params.BodyParamTopLevelAnyOfParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    idempotency_key=idempotency_key,
                ),
                cast_to=cast(
                    Any, BodyParamTopLevelAnyOfResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    @overload
    async def top_level_any_of_with_ref(
        self,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> SharedBasicSharedModelObject:
        """
        Endpoint with a `requestBody` pointing to a $ref'd schema that is an `anyOf`.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    async def top_level_any_of_with_ref(
        self,
        *,
        is_foo: bool,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> SharedBasicSharedModelObject:
        """
        Endpoint with a `requestBody` pointing to a $ref'd schema that is an `anyOf`.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["kind"], ["is_foo"])
    async def top_level_any_of_with_ref(
        self,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"] | Omit = omit,
        is_foo: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> SharedBasicSharedModelObject:
        return await self._post(
            "/body_params/top_level_anyOf_with_ref",
            body=await async_maybe_transform(
                {
                    "kind": kind,
                    "is_foo": is_foo,
                },
                body_param_top_level_any_of_with_ref_params.BodyParamTopLevelAnyOfWithRefParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=SharedBasicSharedModelObject,
        )

    async def top_level_array(
        self,
        *,
        items: Iterable[SharedParamsBasicSharedModelObject],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that is an `array` type.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/body_params/top_level_array",
            body=await async_maybe_transform(items, Iterable[SharedParamsBasicSharedModelObject]),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    async def top_level_array_with_children(
        self,
        *,
        items: Iterable[body_param_top_level_array_with_children_params.Item],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that is an `array` type with non-model children.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/body_params/top_level_array_with_children",
            body=await async_maybe_transform(items, Iterable[body_param_top_level_array_with_children_params.Item]),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    async def top_level_array_with_other_params(
        self,
        *,
        id: str,
        items: Iterable[SharedParamsBasicSharedModelObject],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that is an `array` type.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/body_params/top_level_array_with_other_params",
            body=await async_maybe_transform(items, Iterable[SharedParamsBasicSharedModelObject]),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
                query=await async_maybe_transform(
                    {"id": id},
                    body_param_top_level_array_with_other_params_params.BodyParamTopLevelArrayWithOtherParamsParams,
                ),
            ),
            cast_to=NoneType,
        )

    @overload
    async def top_level_one_of(
        self,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelOneOfResponse:
        """
        Endpoint with a `requestBody` making use of oneOf.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    async def top_level_one_of(
        self,
        *,
        is_foo: bool,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelOneOfResponse:
        """
        Endpoint with a `requestBody` making use of oneOf.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["kind"], ["is_foo"])
    async def top_level_one_of(
        self,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"] | Omit = omit,
        is_foo: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BodyParamTopLevelOneOfResponse:
        return cast(
            BodyParamTopLevelOneOfResponse,
            await self._post(
                "/body_params/top_level_oneOf",
                body=await async_maybe_transform(
                    {
                        "kind": kind,
                        "is_foo": is_foo,
                    },
                    body_param_top_level_one_of_params.BodyParamTopLevelOneOfParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    idempotency_key=idempotency_key,
                ),
                cast_to=cast(
                    Any, BodyParamTopLevelOneOfResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def top_level_one_of_one_entry(
        self,
        *,
        kind: Literal["VIRTUAL", "PHYSICAL"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` making use of oneOf but only contains one entry in
        the union.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/body_params/top_level_oneOf_one_entry",
            body=await async_maybe_transform(
                {"kind": kind}, body_param_top_level_one_of_one_entry_params.BodyParamTopLevelOneOfOneEntryParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    async def top_level_shared_type(
        self,
        *,
        bar: SimpleObject | Omit = omit,
        foo: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        The request body being set to a $ref that is a shared type in the stainless
        config correctly references it.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/body_params/top_level_shared_type",
            body=await async_maybe_transform(
                {
                    "bar": bar,
                    "foo": foo,
                },
                body_param_top_level_shared_type_params.BodyParamTopLevelSharedTypeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    @overload
    async def union_overlapping_prop(
        self,
        *,
        foo: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BodyParamUnionOverlappingPropResponse:
        """
        Endpoint with a `requestBody` making use of anyOf where the same property is
        defined in both variants.

        Args:
          foo: FOO 1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    async def union_overlapping_prop(
        self,
        *,
        foo: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BodyParamUnionOverlappingPropResponse:
        """
        Endpoint with a `requestBody` making use of anyOf where the same property is
        defined in both variants.

        Args:
          foo: FOO 2

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    async def union_overlapping_prop(
        self,
        *,
        foo: str | bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BodyParamUnionOverlappingPropResponse:
        return await self._post(
            "/body_params/top_level_anyOf_overlapping_property",
            body=await async_maybe_transform(
                {"foo": foo}, body_param_union_overlapping_prop_params.BodyParamUnionOverlappingPropParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BodyParamUnionOverlappingPropResponse,
        )

    async def unknown_object(
        self,
        *,
        name: str,
        unknown_object_prop: UnknownObjectModelParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that has an untyped object schema that is defined
        as a model in the config.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/body_params/unknown_object",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "unknown_object_prop": unknown_object_prop,
                },
                body_param_unknown_object_params.BodyParamUnknownObjectParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    async def with_default_body_param_optional(
        self,
        *,
        my_version_body_param: str = "v1.4",
        normal_param: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with an optional request property that has a default value set.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/body_params/with_default_body_param_optional",
            body=await async_maybe_transform(
                {
                    "my_version_body_param": my_version_body_param,
                    "normal_param": normal_param,
                },
                body_param_with_default_body_param_optional_params.BodyParamWithDefaultBodyParamOptionalParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    async def with_default_body_param_required(
        self,
        *,
        my_version_body_param: str = "v1.4",
        normal_param: bool,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a required request property that has a default value set.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/body_params/with_default_body_param_required",
            body=await async_maybe_transform(
                {
                    "my_version_body_param": my_version_body_param,
                    "normal_param": normal_param,
                },
                body_param_with_default_body_param_required_params.BodyParamWithDefaultBodyParamRequiredParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    async def with_model_property(
        self,
        *,
        foo: str | Omit = omit,
        my_model: MyModelParam | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a request body that contains a property that points to a model
        reference.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/body_params/with_model_property",
            body=await async_maybe_transform(
                {
                    "foo": foo,
                    "my_model": my_model,
                },
                body_param_with_model_property_params.BodyParamWithModelPropertyParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )


class BodyParamsResourceWithRawResponse:
    def __init__(self, body_params: BodyParamsResource) -> None:
        self._body_params = body_params

        self.duplicate_subproperty = _legacy_response.to_raw_response_wrapper(
            body_params.duplicate_subproperty,
        )
        self.enum_properties = _legacy_response.to_raw_response_wrapper(
            body_params.enum_properties,
        )
        self.nested_request_models = _legacy_response.to_raw_response_wrapper(
            body_params.nested_request_models,
        )
        self.object_map_model_ref = _legacy_response.to_raw_response_wrapper(
            body_params.object_map_model_ref,
        )
        self.object_with_array_of_objects = _legacy_response.to_raw_response_wrapper(
            body_params.object_with_array_of_objects,
        )
        self.object_with_union_properties = _legacy_response.to_raw_response_wrapper(
            body_params.object_with_union_properties,
        )
        self.only_read_only_properties = _legacy_response.to_raw_response_wrapper(
            body_params.only_read_only_properties,
        )
        self.param_in_model_name_ref = _legacy_response.to_raw_response_wrapper(
            body_params.param_in_model_name_ref,
        )
        self.property_model_ref = _legacy_response.to_raw_response_wrapper(
            body_params.property_model_ref,
        )
        self.property_with_complex_union = _legacy_response.to_raw_response_wrapper(
            body_params.property_with_complex_union,
        )
        self.read_only_properties = _legacy_response.to_raw_response_wrapper(
            body_params.read_only_properties,
        )
        self.string_map_model_ref = _legacy_response.to_raw_response_wrapper(
            body_params.string_map_model_ref,
        )
        self.top_level_all_of = _legacy_response.to_raw_response_wrapper(
            body_params.top_level_all_of,
        )
        self.top_level_all_of_nested_object = _legacy_response.to_raw_response_wrapper(
            body_params.top_level_all_of_nested_object,
        )
        self.top_level_any_of = _legacy_response.to_raw_response_wrapper(
            body_params.top_level_any_of,
        )
        self.top_level_any_of_with_ref = _legacy_response.to_raw_response_wrapper(
            body_params.top_level_any_of_with_ref,
        )
        self.top_level_array = _legacy_response.to_raw_response_wrapper(
            body_params.top_level_array,
        )
        self.top_level_array_with_children = _legacy_response.to_raw_response_wrapper(
            body_params.top_level_array_with_children,
        )
        self.top_level_array_with_other_params = _legacy_response.to_raw_response_wrapper(
            body_params.top_level_array_with_other_params,
        )
        self.top_level_one_of = _legacy_response.to_raw_response_wrapper(
            body_params.top_level_one_of,
        )
        self.top_level_one_of_one_entry = _legacy_response.to_raw_response_wrapper(
            body_params.top_level_one_of_one_entry,
        )
        self.top_level_shared_type = _legacy_response.to_raw_response_wrapper(
            body_params.top_level_shared_type,
        )
        self.union_overlapping_prop = _legacy_response.to_raw_response_wrapper(
            body_params.union_overlapping_prop,
        )
        self.unknown_object = _legacy_response.to_raw_response_wrapper(
            body_params.unknown_object,
        )
        self.with_default_body_param_optional = _legacy_response.to_raw_response_wrapper(
            body_params.with_default_body_param_optional,
        )
        self.with_default_body_param_required = _legacy_response.to_raw_response_wrapper(
            body_params.with_default_body_param_required,
        )
        self.with_model_property = _legacy_response.to_raw_response_wrapper(
            body_params.with_model_property,
        )

    @cached_property
    def objects(self) -> ObjectsResourceWithRawResponse:
        return ObjectsResourceWithRawResponse(self._body_params.objects)

    @cached_property
    def unions(self) -> UnionsResourceWithRawResponse:
        return UnionsResourceWithRawResponse(self._body_params.unions)


class AsyncBodyParamsResourceWithRawResponse:
    def __init__(self, body_params: AsyncBodyParamsResource) -> None:
        self._body_params = body_params

        self.duplicate_subproperty = _legacy_response.async_to_raw_response_wrapper(
            body_params.duplicate_subproperty,
        )
        self.enum_properties = _legacy_response.async_to_raw_response_wrapper(
            body_params.enum_properties,
        )
        self.nested_request_models = _legacy_response.async_to_raw_response_wrapper(
            body_params.nested_request_models,
        )
        self.object_map_model_ref = _legacy_response.async_to_raw_response_wrapper(
            body_params.object_map_model_ref,
        )
        self.object_with_array_of_objects = _legacy_response.async_to_raw_response_wrapper(
            body_params.object_with_array_of_objects,
        )
        self.object_with_union_properties = _legacy_response.async_to_raw_response_wrapper(
            body_params.object_with_union_properties,
        )
        self.only_read_only_properties = _legacy_response.async_to_raw_response_wrapper(
            body_params.only_read_only_properties,
        )
        self.param_in_model_name_ref = _legacy_response.async_to_raw_response_wrapper(
            body_params.param_in_model_name_ref,
        )
        self.property_model_ref = _legacy_response.async_to_raw_response_wrapper(
            body_params.property_model_ref,
        )
        self.property_with_complex_union = _legacy_response.async_to_raw_response_wrapper(
            body_params.property_with_complex_union,
        )
        self.read_only_properties = _legacy_response.async_to_raw_response_wrapper(
            body_params.read_only_properties,
        )
        self.string_map_model_ref = _legacy_response.async_to_raw_response_wrapper(
            body_params.string_map_model_ref,
        )
        self.top_level_all_of = _legacy_response.async_to_raw_response_wrapper(
            body_params.top_level_all_of,
        )
        self.top_level_all_of_nested_object = _legacy_response.async_to_raw_response_wrapper(
            body_params.top_level_all_of_nested_object,
        )
        self.top_level_any_of = _legacy_response.async_to_raw_response_wrapper(
            body_params.top_level_any_of,
        )
        self.top_level_any_of_with_ref = _legacy_response.async_to_raw_response_wrapper(
            body_params.top_level_any_of_with_ref,
        )
        self.top_level_array = _legacy_response.async_to_raw_response_wrapper(
            body_params.top_level_array,
        )
        self.top_level_array_with_children = _legacy_response.async_to_raw_response_wrapper(
            body_params.top_level_array_with_children,
        )
        self.top_level_array_with_other_params = _legacy_response.async_to_raw_response_wrapper(
            body_params.top_level_array_with_other_params,
        )
        self.top_level_one_of = _legacy_response.async_to_raw_response_wrapper(
            body_params.top_level_one_of,
        )
        self.top_level_one_of_one_entry = _legacy_response.async_to_raw_response_wrapper(
            body_params.top_level_one_of_one_entry,
        )
        self.top_level_shared_type = _legacy_response.async_to_raw_response_wrapper(
            body_params.top_level_shared_type,
        )
        self.union_overlapping_prop = _legacy_response.async_to_raw_response_wrapper(
            body_params.union_overlapping_prop,
        )
        self.unknown_object = _legacy_response.async_to_raw_response_wrapper(
            body_params.unknown_object,
        )
        self.with_default_body_param_optional = _legacy_response.async_to_raw_response_wrapper(
            body_params.with_default_body_param_optional,
        )
        self.with_default_body_param_required = _legacy_response.async_to_raw_response_wrapper(
            body_params.with_default_body_param_required,
        )
        self.with_model_property = _legacy_response.async_to_raw_response_wrapper(
            body_params.with_model_property,
        )

    @cached_property
    def objects(self) -> AsyncObjectsResourceWithRawResponse:
        return AsyncObjectsResourceWithRawResponse(self._body_params.objects)

    @cached_property
    def unions(self) -> AsyncUnionsResourceWithRawResponse:
        return AsyncUnionsResourceWithRawResponse(self._body_params.unions)


class BodyParamsResourceWithStreamingResponse:
    def __init__(self, body_params: BodyParamsResource) -> None:
        self._body_params = body_params

        self.duplicate_subproperty = to_streamed_response_wrapper(
            body_params.duplicate_subproperty,
        )
        self.enum_properties = to_streamed_response_wrapper(
            body_params.enum_properties,
        )
        self.nested_request_models = to_streamed_response_wrapper(
            body_params.nested_request_models,
        )
        self.object_map_model_ref = to_streamed_response_wrapper(
            body_params.object_map_model_ref,
        )
        self.object_with_array_of_objects = to_streamed_response_wrapper(
            body_params.object_with_array_of_objects,
        )
        self.object_with_union_properties = to_streamed_response_wrapper(
            body_params.object_with_union_properties,
        )
        self.only_read_only_properties = to_streamed_response_wrapper(
            body_params.only_read_only_properties,
        )
        self.param_in_model_name_ref = to_streamed_response_wrapper(
            body_params.param_in_model_name_ref,
        )
        self.property_model_ref = to_streamed_response_wrapper(
            body_params.property_model_ref,
        )
        self.property_with_complex_union = to_streamed_response_wrapper(
            body_params.property_with_complex_union,
        )
        self.read_only_properties = to_streamed_response_wrapper(
            body_params.read_only_properties,
        )
        self.string_map_model_ref = to_streamed_response_wrapper(
            body_params.string_map_model_ref,
        )
        self.top_level_all_of = to_streamed_response_wrapper(
            body_params.top_level_all_of,
        )
        self.top_level_all_of_nested_object = to_streamed_response_wrapper(
            body_params.top_level_all_of_nested_object,
        )
        self.top_level_any_of = to_streamed_response_wrapper(
            body_params.top_level_any_of,
        )
        self.top_level_any_of_with_ref = to_streamed_response_wrapper(
            body_params.top_level_any_of_with_ref,
        )
        self.top_level_array = to_streamed_response_wrapper(
            body_params.top_level_array,
        )
        self.top_level_array_with_children = to_streamed_response_wrapper(
            body_params.top_level_array_with_children,
        )
        self.top_level_array_with_other_params = to_streamed_response_wrapper(
            body_params.top_level_array_with_other_params,
        )
        self.top_level_one_of = to_streamed_response_wrapper(
            body_params.top_level_one_of,
        )
        self.top_level_one_of_one_entry = to_streamed_response_wrapper(
            body_params.top_level_one_of_one_entry,
        )
        self.top_level_shared_type = to_streamed_response_wrapper(
            body_params.top_level_shared_type,
        )
        self.union_overlapping_prop = to_streamed_response_wrapper(
            body_params.union_overlapping_prop,
        )
        self.unknown_object = to_streamed_response_wrapper(
            body_params.unknown_object,
        )
        self.with_default_body_param_optional = to_streamed_response_wrapper(
            body_params.with_default_body_param_optional,
        )
        self.with_default_body_param_required = to_streamed_response_wrapper(
            body_params.with_default_body_param_required,
        )
        self.with_model_property = to_streamed_response_wrapper(
            body_params.with_model_property,
        )

    @cached_property
    def objects(self) -> ObjectsResourceWithStreamingResponse:
        return ObjectsResourceWithStreamingResponse(self._body_params.objects)

    @cached_property
    def unions(self) -> UnionsResourceWithStreamingResponse:
        return UnionsResourceWithStreamingResponse(self._body_params.unions)


class AsyncBodyParamsResourceWithStreamingResponse:
    def __init__(self, body_params: AsyncBodyParamsResource) -> None:
        self._body_params = body_params

        self.duplicate_subproperty = async_to_streamed_response_wrapper(
            body_params.duplicate_subproperty,
        )
        self.enum_properties = async_to_streamed_response_wrapper(
            body_params.enum_properties,
        )
        self.nested_request_models = async_to_streamed_response_wrapper(
            body_params.nested_request_models,
        )
        self.object_map_model_ref = async_to_streamed_response_wrapper(
            body_params.object_map_model_ref,
        )
        self.object_with_array_of_objects = async_to_streamed_response_wrapper(
            body_params.object_with_array_of_objects,
        )
        self.object_with_union_properties = async_to_streamed_response_wrapper(
            body_params.object_with_union_properties,
        )
        self.only_read_only_properties = async_to_streamed_response_wrapper(
            body_params.only_read_only_properties,
        )
        self.param_in_model_name_ref = async_to_streamed_response_wrapper(
            body_params.param_in_model_name_ref,
        )
        self.property_model_ref = async_to_streamed_response_wrapper(
            body_params.property_model_ref,
        )
        self.property_with_complex_union = async_to_streamed_response_wrapper(
            body_params.property_with_complex_union,
        )
        self.read_only_properties = async_to_streamed_response_wrapper(
            body_params.read_only_properties,
        )
        self.string_map_model_ref = async_to_streamed_response_wrapper(
            body_params.string_map_model_ref,
        )
        self.top_level_all_of = async_to_streamed_response_wrapper(
            body_params.top_level_all_of,
        )
        self.top_level_all_of_nested_object = async_to_streamed_response_wrapper(
            body_params.top_level_all_of_nested_object,
        )
        self.top_level_any_of = async_to_streamed_response_wrapper(
            body_params.top_level_any_of,
        )
        self.top_level_any_of_with_ref = async_to_streamed_response_wrapper(
            body_params.top_level_any_of_with_ref,
        )
        self.top_level_array = async_to_streamed_response_wrapper(
            body_params.top_level_array,
        )
        self.top_level_array_with_children = async_to_streamed_response_wrapper(
            body_params.top_level_array_with_children,
        )
        self.top_level_array_with_other_params = async_to_streamed_response_wrapper(
            body_params.top_level_array_with_other_params,
        )
        self.top_level_one_of = async_to_streamed_response_wrapper(
            body_params.top_level_one_of,
        )
        self.top_level_one_of_one_entry = async_to_streamed_response_wrapper(
            body_params.top_level_one_of_one_entry,
        )
        self.top_level_shared_type = async_to_streamed_response_wrapper(
            body_params.top_level_shared_type,
        )
        self.union_overlapping_prop = async_to_streamed_response_wrapper(
            body_params.union_overlapping_prop,
        )
        self.unknown_object = async_to_streamed_response_wrapper(
            body_params.unknown_object,
        )
        self.with_default_body_param_optional = async_to_streamed_response_wrapper(
            body_params.with_default_body_param_optional,
        )
        self.with_default_body_param_required = async_to_streamed_response_wrapper(
            body_params.with_default_body_param_required,
        )
        self.with_model_property = async_to_streamed_response_wrapper(
            body_params.with_model_property,
        )

    @cached_property
    def objects(self) -> AsyncObjectsResourceWithStreamingResponse:
        return AsyncObjectsResourceWithStreamingResponse(self._body_params.objects)

    @cached_property
    def unions(self) -> AsyncUnionsResourceWithStreamingResponse:
        return AsyncUnionsResourceWithStreamingResponse(self._body_params.unions)
