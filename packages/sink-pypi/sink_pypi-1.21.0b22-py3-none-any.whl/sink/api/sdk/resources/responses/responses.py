# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ... import _legacy_response
from ..._types import Body, Query, Headers, NoneType, NotGiven, not_given
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from .union_types import (
    UnionTypesResource,
    AsyncUnionTypesResource,
    UnionTypesResourceWithRawResponse,
    AsyncUnionTypesResourceWithRawResponse,
    UnionTypesResourceWithStreamingResponse,
    AsyncUnionTypesResourceWithStreamingResponse,
)
from ..._base_client import make_request_options
from ...types.shared.simple_object import SimpleObject
from ...types.model_with_nested_model import ModelWithNestedModel
from ...types.response_allof_simple_response import ResponseAllofSimpleResponse
from ...types.response_nested_array_response import ResponseNestedArrayResponse
from ...types.object_with_any_of_null_property import ObjectWithAnyOfNullProperty
from ...types.object_with_one_of_null_property import ObjectWithOneOfNullProperty
from ...types.response_array_response_response import ResponseArrayResponseResponse
from ...types.response_missing_required_response import ResponseMissingRequiredResponse
from ...types.response_allof_cross_resource_response import ResponseAllofCrossResourceResponse
from ...types.response_object_no_properties_response import ResponseObjectNoPropertiesResponse
from ...types.response_additional_properties_response import ResponseAdditionalPropertiesResponse
from ...types.response_object_all_properties_response import ResponseObjectAllPropertiesResponse
from ...types.response_only_read_only_properties_response import ResponseOnlyReadOnlyPropertiesResponse
from ...types.response_array_object_with_union_properties_response import ResponseArrayObjectWithUnionPropertiesResponse
from ...types.response_object_with_additional_properties_prop_response import (
    ResponseObjectWithAdditionalPropertiesPropResponse,
)
from ...types.response_additional_properties_nested_model_reference_response import (
    ResponseAdditionalPropertiesNestedModelReferenceResponse,
)

__all__ = ["ResponsesResource", "AsyncResponsesResource"]


class ResponsesResource(SyncAPIResource):
    @cached_property
    def union_types(self) -> UnionTypesResource:
        return UnionTypesResource(self._client)

    @cached_property
    def with_raw_response(self) -> ResponsesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return ResponsesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ResponsesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return ResponsesResourceWithStreamingResponse(self)

    def additional_properties(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ResponseAdditionalPropertiesResponse:
        """Endpoint with a top level additionalProperties response."""
        return self._post(
            "/responses/additional_properties",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ResponseAdditionalPropertiesResponse,
        )

    def additional_properties_nested_model_reference(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ResponseAdditionalPropertiesNestedModelReferenceResponse:
        """
        Endpoint with a top level additionalProperties response where the items type
        points to an object defined as a model in the config.
        """
        return self._post(
            "/responses/additional_properties_nested_model_reference",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ResponseAdditionalPropertiesNestedModelReferenceResponse,
        )

    def allof_cross_resource(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ResponseAllofCrossResourceResponse:
        """
        Method with a response object defined using allOf and two models, one from
        another resource and one from this resource, as well as a nested allOf.
        """
        return self._get(
            "/responses/allof/cross",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResponseAllofCrossResourceResponse,
        )

    def allof_simple(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ResponseAllofSimpleResponse:
        """
        Method with a response object defined using allOf and inline schema definitions.
        """
        return self._get(
            "/responses/allof/simple",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResponseAllofSimpleResponse,
        )

    def anyof_null(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ObjectWithAnyOfNullProperty:
        """Method with a response object that uses anyOf to indicate nullability."""
        return self._get(
            "/responses/anyof_null",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectWithAnyOfNullProperty,
        )

    def array_object_with_union_properties(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ResponseArrayObjectWithUnionPropertiesResponse:
        """Endpoint that returns an array of objects with union properties."""
        return self._get(
            "/responses/array/object_with_union_properties",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResponseArrayObjectWithUnionPropertiesResponse,
        )

    def array_response(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ResponseArrayResponseResponse:
        """Endpoint that returns a top-level array."""
        return self._get(
            "/responses/array",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResponseArrayResponseResponse,
        )

    def empty_response(
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
        """Endpoint with an empty response."""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/responses/empty",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def missing_required(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ResponseMissingRequiredResponse:
        """Endpoint with a response schema that doesn't set the `required` property."""
        return self._get(
            "/responses/missing_required",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResponseMissingRequiredResponse,
        )

    def nested_array(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ResponseNestedArrayResponse:
        """Endpoint that returns a nested array."""
        return self._get(
            "/responses/array/nested",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResponseNestedArrayResponse,
        )

    def object_all_properties(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ResponseObjectAllPropertiesResponse:
        """
        Method with a response object with a different property for each supported type.
        """
        return self._get(
            "/responses/object/everything",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResponseObjectAllPropertiesResponse,
        )

    def object_no_properties(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ResponseObjectNoPropertiesResponse:
        """Endpoint with an empty response."""
        return self._post(
            "/responses/object_no_properties",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ResponseObjectNoPropertiesResponse,
        )

    def object_with_additional_properties_prop(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ResponseObjectWithAdditionalPropertiesPropResponse:
        """
        Endpoint with an object response that contains an `additionalProperties`
        property with a nested schema.
        """
        return self._post(
            "/responses/object_with_additional_properties_prop",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ResponseObjectWithAdditionalPropertiesPropResponse,
        )

    def oneof_null(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ObjectWithOneOfNullProperty:
        """Method with a response object that uses oneOf to indicate nullability."""
        return self._get(
            "/responses/oneof_null",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectWithOneOfNullProperty,
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
    ) -> ResponseOnlyReadOnlyPropertiesResponse:
        """Endpoint with a response that only has `readOnly` properties"""
        return self._get(
            "/responses/only_read_only_properties",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResponseOnlyReadOnlyPropertiesResponse,
        )

    def shared_simple_object(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SimpleObject:
        """Endpoint that returns a $ref to SimpleObject.

        This is used to test shared
        response models.
        """
        return self._get(
            "/responses/shared_simple_object",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SimpleObject,
        )

    def string_response(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> str:
        """Endpoint with a top level string response."""
        return self._post(
            "/responses/string",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=str,
        )

    def unknown_object(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> object:
        """
        Should not generate a named return type for object without defined properties;
        instead, it should simply use an `unknown` type or equivalent. In Java and Go,
        where we have fancier accessors for raw json stuff, we should generate a named
        type, but it should basically just have untyped additional properties. See
        https://linear.app/stainless/issue/STA-563/no-type-should-be-generated-for-endpoints-returning-type-object-schema.
        """
        return self._post(
            "/responses/unknown_object",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=object,
        )

    def with_model_in_nested_path(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelWithNestedModel:
        """
        Should return a ModelWithNestedModel object with a `properties` field that we
        can rename in the Stainless config to a prettier name.
        """
        return self._get(
            "/responses/with_model_in_nested_path",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelWithNestedModel,
        )


class AsyncResponsesResource(AsyncAPIResource):
    @cached_property
    def union_types(self) -> AsyncUnionTypesResource:
        return AsyncUnionTypesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncResponsesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncResponsesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncResponsesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncResponsesResourceWithStreamingResponse(self)

    async def additional_properties(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ResponseAdditionalPropertiesResponse:
        """Endpoint with a top level additionalProperties response."""
        return await self._post(
            "/responses/additional_properties",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ResponseAdditionalPropertiesResponse,
        )

    async def additional_properties_nested_model_reference(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ResponseAdditionalPropertiesNestedModelReferenceResponse:
        """
        Endpoint with a top level additionalProperties response where the items type
        points to an object defined as a model in the config.
        """
        return await self._post(
            "/responses/additional_properties_nested_model_reference",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ResponseAdditionalPropertiesNestedModelReferenceResponse,
        )

    async def allof_cross_resource(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ResponseAllofCrossResourceResponse:
        """
        Method with a response object defined using allOf and two models, one from
        another resource and one from this resource, as well as a nested allOf.
        """
        return await self._get(
            "/responses/allof/cross",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResponseAllofCrossResourceResponse,
        )

    async def allof_simple(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ResponseAllofSimpleResponse:
        """
        Method with a response object defined using allOf and inline schema definitions.
        """
        return await self._get(
            "/responses/allof/simple",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResponseAllofSimpleResponse,
        )

    async def anyof_null(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ObjectWithAnyOfNullProperty:
        """Method with a response object that uses anyOf to indicate nullability."""
        return await self._get(
            "/responses/anyof_null",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectWithAnyOfNullProperty,
        )

    async def array_object_with_union_properties(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ResponseArrayObjectWithUnionPropertiesResponse:
        """Endpoint that returns an array of objects with union properties."""
        return await self._get(
            "/responses/array/object_with_union_properties",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResponseArrayObjectWithUnionPropertiesResponse,
        )

    async def array_response(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ResponseArrayResponseResponse:
        """Endpoint that returns a top-level array."""
        return await self._get(
            "/responses/array",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResponseArrayResponseResponse,
        )

    async def empty_response(
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
        """Endpoint with an empty response."""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/responses/empty",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    async def missing_required(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ResponseMissingRequiredResponse:
        """Endpoint with a response schema that doesn't set the `required` property."""
        return await self._get(
            "/responses/missing_required",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResponseMissingRequiredResponse,
        )

    async def nested_array(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ResponseNestedArrayResponse:
        """Endpoint that returns a nested array."""
        return await self._get(
            "/responses/array/nested",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResponseNestedArrayResponse,
        )

    async def object_all_properties(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ResponseObjectAllPropertiesResponse:
        """
        Method with a response object with a different property for each supported type.
        """
        return await self._get(
            "/responses/object/everything",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResponseObjectAllPropertiesResponse,
        )

    async def object_no_properties(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ResponseObjectNoPropertiesResponse:
        """Endpoint with an empty response."""
        return await self._post(
            "/responses/object_no_properties",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ResponseObjectNoPropertiesResponse,
        )

    async def object_with_additional_properties_prop(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ResponseObjectWithAdditionalPropertiesPropResponse:
        """
        Endpoint with an object response that contains an `additionalProperties`
        property with a nested schema.
        """
        return await self._post(
            "/responses/object_with_additional_properties_prop",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ResponseObjectWithAdditionalPropertiesPropResponse,
        )

    async def oneof_null(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ObjectWithOneOfNullProperty:
        """Method with a response object that uses oneOf to indicate nullability."""
        return await self._get(
            "/responses/oneof_null",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectWithOneOfNullProperty,
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
    ) -> ResponseOnlyReadOnlyPropertiesResponse:
        """Endpoint with a response that only has `readOnly` properties"""
        return await self._get(
            "/responses/only_read_only_properties",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResponseOnlyReadOnlyPropertiesResponse,
        )

    async def shared_simple_object(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SimpleObject:
        """Endpoint that returns a $ref to SimpleObject.

        This is used to test shared
        response models.
        """
        return await self._get(
            "/responses/shared_simple_object",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SimpleObject,
        )

    async def string_response(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> str:
        """Endpoint with a top level string response."""
        return await self._post(
            "/responses/string",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=str,
        )

    async def unknown_object(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> object:
        """
        Should not generate a named return type for object without defined properties;
        instead, it should simply use an `unknown` type or equivalent. In Java and Go,
        where we have fancier accessors for raw json stuff, we should generate a named
        type, but it should basically just have untyped additional properties. See
        https://linear.app/stainless/issue/STA-563/no-type-should-be-generated-for-endpoints-returning-type-object-schema.
        """
        return await self._post(
            "/responses/unknown_object",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=object,
        )

    async def with_model_in_nested_path(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelWithNestedModel:
        """
        Should return a ModelWithNestedModel object with a `properties` field that we
        can rename in the Stainless config to a prettier name.
        """
        return await self._get(
            "/responses/with_model_in_nested_path",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelWithNestedModel,
        )


class ResponsesResourceWithRawResponse:
    def __init__(self, responses: ResponsesResource) -> None:
        self._responses = responses

        self.additional_properties = _legacy_response.to_raw_response_wrapper(
            responses.additional_properties,
        )
        self.additional_properties_nested_model_reference = _legacy_response.to_raw_response_wrapper(
            responses.additional_properties_nested_model_reference,
        )
        self.allof_cross_resource = _legacy_response.to_raw_response_wrapper(
            responses.allof_cross_resource,
        )
        self.allof_simple = _legacy_response.to_raw_response_wrapper(
            responses.allof_simple,
        )
        self.anyof_null = _legacy_response.to_raw_response_wrapper(
            responses.anyof_null,
        )
        self.array_object_with_union_properties = _legacy_response.to_raw_response_wrapper(
            responses.array_object_with_union_properties,
        )
        self.array_response = _legacy_response.to_raw_response_wrapper(
            responses.array_response,
        )
        self.empty_response = _legacy_response.to_raw_response_wrapper(
            responses.empty_response,
        )
        self.missing_required = _legacy_response.to_raw_response_wrapper(
            responses.missing_required,
        )
        self.nested_array = _legacy_response.to_raw_response_wrapper(
            responses.nested_array,
        )
        self.object_all_properties = _legacy_response.to_raw_response_wrapper(
            responses.object_all_properties,
        )
        self.object_no_properties = _legacy_response.to_raw_response_wrapper(
            responses.object_no_properties,
        )
        self.object_with_additional_properties_prop = _legacy_response.to_raw_response_wrapper(
            responses.object_with_additional_properties_prop,
        )
        self.oneof_null = _legacy_response.to_raw_response_wrapper(
            responses.oneof_null,
        )
        self.only_read_only_properties = _legacy_response.to_raw_response_wrapper(
            responses.only_read_only_properties,
        )
        self.shared_simple_object = _legacy_response.to_raw_response_wrapper(
            responses.shared_simple_object,
        )
        self.string_response = _legacy_response.to_raw_response_wrapper(
            responses.string_response,
        )
        self.unknown_object = _legacy_response.to_raw_response_wrapper(
            responses.unknown_object,
        )
        self.with_model_in_nested_path = _legacy_response.to_raw_response_wrapper(
            responses.with_model_in_nested_path,
        )

    @cached_property
    def union_types(self) -> UnionTypesResourceWithRawResponse:
        return UnionTypesResourceWithRawResponse(self._responses.union_types)


class AsyncResponsesResourceWithRawResponse:
    def __init__(self, responses: AsyncResponsesResource) -> None:
        self._responses = responses

        self.additional_properties = _legacy_response.async_to_raw_response_wrapper(
            responses.additional_properties,
        )
        self.additional_properties_nested_model_reference = _legacy_response.async_to_raw_response_wrapper(
            responses.additional_properties_nested_model_reference,
        )
        self.allof_cross_resource = _legacy_response.async_to_raw_response_wrapper(
            responses.allof_cross_resource,
        )
        self.allof_simple = _legacy_response.async_to_raw_response_wrapper(
            responses.allof_simple,
        )
        self.anyof_null = _legacy_response.async_to_raw_response_wrapper(
            responses.anyof_null,
        )
        self.array_object_with_union_properties = _legacy_response.async_to_raw_response_wrapper(
            responses.array_object_with_union_properties,
        )
        self.array_response = _legacy_response.async_to_raw_response_wrapper(
            responses.array_response,
        )
        self.empty_response = _legacy_response.async_to_raw_response_wrapper(
            responses.empty_response,
        )
        self.missing_required = _legacy_response.async_to_raw_response_wrapper(
            responses.missing_required,
        )
        self.nested_array = _legacy_response.async_to_raw_response_wrapper(
            responses.nested_array,
        )
        self.object_all_properties = _legacy_response.async_to_raw_response_wrapper(
            responses.object_all_properties,
        )
        self.object_no_properties = _legacy_response.async_to_raw_response_wrapper(
            responses.object_no_properties,
        )
        self.object_with_additional_properties_prop = _legacy_response.async_to_raw_response_wrapper(
            responses.object_with_additional_properties_prop,
        )
        self.oneof_null = _legacy_response.async_to_raw_response_wrapper(
            responses.oneof_null,
        )
        self.only_read_only_properties = _legacy_response.async_to_raw_response_wrapper(
            responses.only_read_only_properties,
        )
        self.shared_simple_object = _legacy_response.async_to_raw_response_wrapper(
            responses.shared_simple_object,
        )
        self.string_response = _legacy_response.async_to_raw_response_wrapper(
            responses.string_response,
        )
        self.unknown_object = _legacy_response.async_to_raw_response_wrapper(
            responses.unknown_object,
        )
        self.with_model_in_nested_path = _legacy_response.async_to_raw_response_wrapper(
            responses.with_model_in_nested_path,
        )

    @cached_property
    def union_types(self) -> AsyncUnionTypesResourceWithRawResponse:
        return AsyncUnionTypesResourceWithRawResponse(self._responses.union_types)


class ResponsesResourceWithStreamingResponse:
    def __init__(self, responses: ResponsesResource) -> None:
        self._responses = responses

        self.additional_properties = to_streamed_response_wrapper(
            responses.additional_properties,
        )
        self.additional_properties_nested_model_reference = to_streamed_response_wrapper(
            responses.additional_properties_nested_model_reference,
        )
        self.allof_cross_resource = to_streamed_response_wrapper(
            responses.allof_cross_resource,
        )
        self.allof_simple = to_streamed_response_wrapper(
            responses.allof_simple,
        )
        self.anyof_null = to_streamed_response_wrapper(
            responses.anyof_null,
        )
        self.array_object_with_union_properties = to_streamed_response_wrapper(
            responses.array_object_with_union_properties,
        )
        self.array_response = to_streamed_response_wrapper(
            responses.array_response,
        )
        self.empty_response = to_streamed_response_wrapper(
            responses.empty_response,
        )
        self.missing_required = to_streamed_response_wrapper(
            responses.missing_required,
        )
        self.nested_array = to_streamed_response_wrapper(
            responses.nested_array,
        )
        self.object_all_properties = to_streamed_response_wrapper(
            responses.object_all_properties,
        )
        self.object_no_properties = to_streamed_response_wrapper(
            responses.object_no_properties,
        )
        self.object_with_additional_properties_prop = to_streamed_response_wrapper(
            responses.object_with_additional_properties_prop,
        )
        self.oneof_null = to_streamed_response_wrapper(
            responses.oneof_null,
        )
        self.only_read_only_properties = to_streamed_response_wrapper(
            responses.only_read_only_properties,
        )
        self.shared_simple_object = to_streamed_response_wrapper(
            responses.shared_simple_object,
        )
        self.string_response = to_streamed_response_wrapper(
            responses.string_response,
        )
        self.unknown_object = to_streamed_response_wrapper(
            responses.unknown_object,
        )
        self.with_model_in_nested_path = to_streamed_response_wrapper(
            responses.with_model_in_nested_path,
        )

    @cached_property
    def union_types(self) -> UnionTypesResourceWithStreamingResponse:
        return UnionTypesResourceWithStreamingResponse(self._responses.union_types)


class AsyncResponsesResourceWithStreamingResponse:
    def __init__(self, responses: AsyncResponsesResource) -> None:
        self._responses = responses

        self.additional_properties = async_to_streamed_response_wrapper(
            responses.additional_properties,
        )
        self.additional_properties_nested_model_reference = async_to_streamed_response_wrapper(
            responses.additional_properties_nested_model_reference,
        )
        self.allof_cross_resource = async_to_streamed_response_wrapper(
            responses.allof_cross_resource,
        )
        self.allof_simple = async_to_streamed_response_wrapper(
            responses.allof_simple,
        )
        self.anyof_null = async_to_streamed_response_wrapper(
            responses.anyof_null,
        )
        self.array_object_with_union_properties = async_to_streamed_response_wrapper(
            responses.array_object_with_union_properties,
        )
        self.array_response = async_to_streamed_response_wrapper(
            responses.array_response,
        )
        self.empty_response = async_to_streamed_response_wrapper(
            responses.empty_response,
        )
        self.missing_required = async_to_streamed_response_wrapper(
            responses.missing_required,
        )
        self.nested_array = async_to_streamed_response_wrapper(
            responses.nested_array,
        )
        self.object_all_properties = async_to_streamed_response_wrapper(
            responses.object_all_properties,
        )
        self.object_no_properties = async_to_streamed_response_wrapper(
            responses.object_no_properties,
        )
        self.object_with_additional_properties_prop = async_to_streamed_response_wrapper(
            responses.object_with_additional_properties_prop,
        )
        self.oneof_null = async_to_streamed_response_wrapper(
            responses.oneof_null,
        )
        self.only_read_only_properties = async_to_streamed_response_wrapper(
            responses.only_read_only_properties,
        )
        self.shared_simple_object = async_to_streamed_response_wrapper(
            responses.shared_simple_object,
        )
        self.string_response = async_to_streamed_response_wrapper(
            responses.string_response,
        )
        self.unknown_object = async_to_streamed_response_wrapper(
            responses.unknown_object,
        )
        self.with_model_in_nested_path = async_to_streamed_response_wrapper(
            responses.with_model_in_nested_path,
        )

    @cached_property
    def union_types(self) -> AsyncUnionTypesResourceWithStreamingResponse:
        return AsyncUnionTypesResourceWithStreamingResponse(self._responses.union_types)
