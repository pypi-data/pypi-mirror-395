# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Union, cast
from datetime import date
from typing_extensions import overload

import httpx

from ... import _legacy_response
from .params import (
    ParamsResource,
    AsyncParamsResource,
    ParamsResourceWithRawResponse,
    AsyncParamsResourceWithRawResponse,
    ParamsResourceWithStreamingResponse,
    AsyncParamsResourceWithStreamingResponse,
)
from .unions import (
    UnionsResource,
    AsyncUnionsResource,
    UnionsResourceWithRawResponse,
    AsyncUnionsResourceWithRawResponse,
    UnionsResourceWithStreamingResponse,
    AsyncUnionsResourceWithStreamingResponse,
)
from ...types import (
    name_properties_common_conflicts_params,
    name_properties_illegal_go_identifiers_params,
    name_properties_illegal_javascript_identifiers_params,
)
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from .renaming import (
    RenamingResource,
    AsyncRenamingResource,
    RenamingResourceWithRawResponse,
    AsyncRenamingResourceWithRawResponse,
    RenamingResourceWithStreamingResponse,
    AsyncRenamingResourceWithStreamingResponse,
)
from ..._compat import cached_property
from .documents import (
    DocumentsResource,
    AsyncDocumentsResource,
    DocumentsResourceWithRawResponse,
    AsyncDocumentsResourceWithRawResponse,
    DocumentsResourceWithStreamingResponse,
    AsyncDocumentsResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ..._base_client import make_request_options
from .openapi_specials import (
    OpenAPISpecialsResource,
    AsyncOpenAPISpecialsResource,
    OpenAPISpecialsResourceWithRawResponse,
    AsyncOpenAPISpecialsResourceWithRawResponse,
    OpenAPISpecialsResourceWithStreamingResponse,
    AsyncOpenAPISpecialsResourceWithStreamingResponse,
)
from .reserved_names.reserved_names import (
    ReservedNamesResource,
    AsyncReservedNamesResource,
    ReservedNamesResourceWithRawResponse,
    AsyncReservedNamesResourceWithRawResponse,
    ReservedNamesResourceWithStreamingResponse,
    AsyncReservedNamesResourceWithStreamingResponse,
)
from .can_cause_clashes.can_cause_clashes import (
    CanCauseClashesResource,
    AsyncCanCauseClashesResource,
    CanCauseClashesResourceWithRawResponse,
    AsyncCanCauseClashesResourceWithRawResponse,
    CanCauseClashesResourceWithStreamingResponse,
    AsyncCanCauseClashesResourceWithStreamingResponse,
)
from ...types.shared.basic_shared_model_object import BasicSharedModelObject
from ...types.name_child_prop_import_clash_response import NameChildPropImportClashResponse
from ...types.name_response_shadows_pydantic_response import NameResponseShadowsPydanticResponse
from ...types.name_properties_common_conflicts_response import NamePropertiesCommonConflictsResponse
from ...types.name_properties_illegal_go_identifiers_response import NamePropertiesIllegalGoIdentifiersResponse
from ...types.name_response_property_clashes_model_import_response import NameResponsePropertyClashesModelImportResponse
from ...types.name_properties_illegal_javascript_identifiers_response import (
    NamePropertiesIllegalJavascriptIdentifiersResponse,
)

__all__ = ["NamesResource", "AsyncNamesResource"]


class NamesResource(SyncAPIResource):
    @cached_property
    def unions(self) -> UnionsResource:
        return UnionsResource(self._client)

    @cached_property
    def renaming(self) -> RenamingResource:
        return RenamingResource(self._client)

    @cached_property
    def documents(self) -> DocumentsResource:
        return DocumentsResource(self._client)

    @cached_property
    def reserved_names(self) -> ReservedNamesResource:
        return ReservedNamesResource(self._client)

    @cached_property
    def params(self) -> ParamsResource:
        return ParamsResource(self._client)

    @cached_property
    def can_cause_clashes(self) -> CanCauseClashesResource:
        return CanCauseClashesResource(self._client)

    @cached_property
    def openapi_specials(self) -> OpenAPISpecialsResource:
        return OpenAPISpecialsResource(self._client)

    @cached_property
    def with_raw_response(self) -> NamesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return NamesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> NamesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return NamesResourceWithStreamingResponse(self)

    def child_prop_import_clash(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> NameChildPropImportClashResponse:
        """
        Endpoint with request & response properties that could cause clashes due to
        imports.
        """
        return self._post(
            "/names/child_prop_import_clash",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NameChildPropImportClashResponse,
        )

    def get(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BasicSharedModelObject:
        """Endpoint with the name `get` in the config."""
        return self._get(
            "/names/method_name_get",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BasicSharedModelObject,
        )

    def properties_common_conflicts(
        self,
        *,
        _1_digit_leading_underscore: str,
        _leading_underscore: str,
        _leading_underscore_mixed_case: str,
        bool: bool,
        bool_2: bool,
        date: Union[str, date],
        date_2: Union[str, date],
        float: float,
        float_2: float,
        int: int,
        int_2: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> NamePropertiesCommonConflictsResponse:
        """
        Endpoint with request & response properties that are likely to cause name
        conflicts.

        Args:
          _1_digit_leading_underscore: In certain languages the leading underscore in combination with this property
              name may cause issues

          _leading_underscore: In certain languages the leading underscore in this property name may cause
              issues

          _leading_underscore_mixed_case: In certain languages the leading underscore in this property name may cause
              issues alongside a case change

          bool_2: In certain languages the type declaration for this prop can shadow the `bool`
              property declaration.

          date: This shadows the stdlib `datetime.date` type in Python & causes type errors.

          date_2: In certain languages the type declaration for this prop can shadow the `date`
              property declaration.

          float_2: In certain languages the type declaration for this prop can shadow the `float`
              property declaration.

          int_2: In certain languages the type declaration for this prop can shadow the `int`
              property declaration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/names/properties_common_conflicts",
            body=maybe_transform(
                {
                    "_1_digit_leading_underscore": _1_digit_leading_underscore,
                    "_leading_underscore": _leading_underscore,
                    "_leading_underscore_mixed_case": _leading_underscore_mixed_case,
                    "bool": bool,
                    "bool_2": bool_2,
                    "date": date,
                    "date_2": date_2,
                    "float": float,
                    "float_2": float_2,
                    "int": int,
                    "int_2": int_2,
                },
                name_properties_common_conflicts_params.NamePropertiesCommonConflictsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NamePropertiesCommonConflictsResponse,
        )

    def properties_illegal_go_identifiers(
        self,
        type: str,
        *,
        defer: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> NamePropertiesIllegalGoIdentifiersResponse:
        """
        Endpoint with request & response properties with names that aren't legal go
        identifiers.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not type:
            raise ValueError(f"Expected a non-empty value for `type` but received {type!r}")
        return self._post(
            f"/names/properties_illegal_go_identifiers/{type}",
            body=maybe_transform(
                {"defer": defer}, name_properties_illegal_go_identifiers_params.NamePropertiesIllegalGoIdentifiersParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NamePropertiesIllegalGoIdentifiersResponse,
        )

    @overload
    def properties_illegal_javascript_identifiers(
        self,
        *,
        irrelevant: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> NamePropertiesIllegalJavascriptIdentifiersResponse:
        """
        Endpoint with request & response properties with names that aren't legal
        javascript identifiers.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    def properties_illegal_javascript_identifiers(
        self,
        *,
        body: float,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> NamePropertiesIllegalJavascriptIdentifiersResponse:
        """
        Endpoint with request & response properties with names that aren't legal
        javascript identifiers.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    def properties_illegal_javascript_identifiers(
        self,
        *,
        irrelevant: float | Omit = omit,
        body: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> NamePropertiesIllegalJavascriptIdentifiersResponse:
        return cast(
            NamePropertiesIllegalJavascriptIdentifiersResponse,
            self._post(
                "/names/properties_illegal_javascript_identifiers",
                body=maybe_transform(
                    {
                        "irrelevant": irrelevant,
                        "body": body,
                    },
                    name_properties_illegal_javascript_identifiers_params.NamePropertiesIllegalJavascriptIdentifiersParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    idempotency_key=idempotency_key,
                ),
                cast_to=cast(
                    Any, NamePropertiesIllegalJavascriptIdentifiersResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def response_property_clashes_model_import(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> NameResponsePropertyClashesModelImportResponse:
        """
        Endpoint with a response model property that can cause clashes with a model
        import.
        """
        return self._get(
            "/names/response_property_clashes_model_import",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NameResponsePropertyClashesModelImportResponse,
        )

    def response_shadows_pydantic(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> NameResponseShadowsPydanticResponse:
        """Endpoint with a response model property that would clash with pydantic."""
        return self._get(
            "/names/response_property_shadows_pydantic",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NameResponseShadowsPydanticResponse,
        )


class AsyncNamesResource(AsyncAPIResource):
    @cached_property
    def unions(self) -> AsyncUnionsResource:
        return AsyncUnionsResource(self._client)

    @cached_property
    def renaming(self) -> AsyncRenamingResource:
        return AsyncRenamingResource(self._client)

    @cached_property
    def documents(self) -> AsyncDocumentsResource:
        return AsyncDocumentsResource(self._client)

    @cached_property
    def reserved_names(self) -> AsyncReservedNamesResource:
        return AsyncReservedNamesResource(self._client)

    @cached_property
    def params(self) -> AsyncParamsResource:
        return AsyncParamsResource(self._client)

    @cached_property
    def can_cause_clashes(self) -> AsyncCanCauseClashesResource:
        return AsyncCanCauseClashesResource(self._client)

    @cached_property
    def openapi_specials(self) -> AsyncOpenAPISpecialsResource:
        return AsyncOpenAPISpecialsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncNamesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncNamesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncNamesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncNamesResourceWithStreamingResponse(self)

    async def child_prop_import_clash(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> NameChildPropImportClashResponse:
        """
        Endpoint with request & response properties that could cause clashes due to
        imports.
        """
        return await self._post(
            "/names/child_prop_import_clash",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NameChildPropImportClashResponse,
        )

    async def get(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BasicSharedModelObject:
        """Endpoint with the name `get` in the config."""
        return await self._get(
            "/names/method_name_get",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BasicSharedModelObject,
        )

    async def properties_common_conflicts(
        self,
        *,
        _1_digit_leading_underscore: str,
        _leading_underscore: str,
        _leading_underscore_mixed_case: str,
        bool: bool,
        bool_2: bool,
        date: Union[str, date],
        date_2: Union[str, date],
        float: float,
        float_2: float,
        int: int,
        int_2: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> NamePropertiesCommonConflictsResponse:
        """
        Endpoint with request & response properties that are likely to cause name
        conflicts.

        Args:
          _1_digit_leading_underscore: In certain languages the leading underscore in combination with this property
              name may cause issues

          _leading_underscore: In certain languages the leading underscore in this property name may cause
              issues

          _leading_underscore_mixed_case: In certain languages the leading underscore in this property name may cause
              issues alongside a case change

          bool_2: In certain languages the type declaration for this prop can shadow the `bool`
              property declaration.

          date: This shadows the stdlib `datetime.date` type in Python & causes type errors.

          date_2: In certain languages the type declaration for this prop can shadow the `date`
              property declaration.

          float_2: In certain languages the type declaration for this prop can shadow the `float`
              property declaration.

          int_2: In certain languages the type declaration for this prop can shadow the `int`
              property declaration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/names/properties_common_conflicts",
            body=await async_maybe_transform(
                {
                    "_1_digit_leading_underscore": _1_digit_leading_underscore,
                    "_leading_underscore": _leading_underscore,
                    "_leading_underscore_mixed_case": _leading_underscore_mixed_case,
                    "bool": bool,
                    "bool_2": bool_2,
                    "date": date,
                    "date_2": date_2,
                    "float": float,
                    "float_2": float_2,
                    "int": int,
                    "int_2": int_2,
                },
                name_properties_common_conflicts_params.NamePropertiesCommonConflictsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NamePropertiesCommonConflictsResponse,
        )

    async def properties_illegal_go_identifiers(
        self,
        type: str,
        *,
        defer: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> NamePropertiesIllegalGoIdentifiersResponse:
        """
        Endpoint with request & response properties with names that aren't legal go
        identifiers.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not type:
            raise ValueError(f"Expected a non-empty value for `type` but received {type!r}")
        return await self._post(
            f"/names/properties_illegal_go_identifiers/{type}",
            body=await async_maybe_transform(
                {"defer": defer}, name_properties_illegal_go_identifiers_params.NamePropertiesIllegalGoIdentifiersParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NamePropertiesIllegalGoIdentifiersResponse,
        )

    @overload
    async def properties_illegal_javascript_identifiers(
        self,
        *,
        irrelevant: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> NamePropertiesIllegalJavascriptIdentifiersResponse:
        """
        Endpoint with request & response properties with names that aren't legal
        javascript identifiers.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    async def properties_illegal_javascript_identifiers(
        self,
        *,
        body: float,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> NamePropertiesIllegalJavascriptIdentifiersResponse:
        """
        Endpoint with request & response properties with names that aren't legal
        javascript identifiers.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    async def properties_illegal_javascript_identifiers(
        self,
        *,
        irrelevant: float | Omit = omit,
        body: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> NamePropertiesIllegalJavascriptIdentifiersResponse:
        return cast(
            NamePropertiesIllegalJavascriptIdentifiersResponse,
            await self._post(
                "/names/properties_illegal_javascript_identifiers",
                body=await async_maybe_transform(
                    {
                        "irrelevant": irrelevant,
                        "body": body,
                    },
                    name_properties_illegal_javascript_identifiers_params.NamePropertiesIllegalJavascriptIdentifiersParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    idempotency_key=idempotency_key,
                ),
                cast_to=cast(
                    Any, NamePropertiesIllegalJavascriptIdentifiersResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def response_property_clashes_model_import(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> NameResponsePropertyClashesModelImportResponse:
        """
        Endpoint with a response model property that can cause clashes with a model
        import.
        """
        return await self._get(
            "/names/response_property_clashes_model_import",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NameResponsePropertyClashesModelImportResponse,
        )

    async def response_shadows_pydantic(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> NameResponseShadowsPydanticResponse:
        """Endpoint with a response model property that would clash with pydantic."""
        return await self._get(
            "/names/response_property_shadows_pydantic",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NameResponseShadowsPydanticResponse,
        )


class NamesResourceWithRawResponse:
    def __init__(self, names: NamesResource) -> None:
        self._names = names

        self.child_prop_import_clash = _legacy_response.to_raw_response_wrapper(
            names.child_prop_import_clash,
        )
        self.get = _legacy_response.to_raw_response_wrapper(
            names.get,
        )
        self.properties_common_conflicts = _legacy_response.to_raw_response_wrapper(
            names.properties_common_conflicts,
        )
        self.properties_illegal_go_identifiers = _legacy_response.to_raw_response_wrapper(
            names.properties_illegal_go_identifiers,
        )
        self.properties_illegal_javascript_identifiers = _legacy_response.to_raw_response_wrapper(
            names.properties_illegal_javascript_identifiers,
        )
        self.response_property_clashes_model_import = _legacy_response.to_raw_response_wrapper(
            names.response_property_clashes_model_import,
        )
        self.response_shadows_pydantic = _legacy_response.to_raw_response_wrapper(
            names.response_shadows_pydantic,
        )

    @cached_property
    def unions(self) -> UnionsResourceWithRawResponse:
        return UnionsResourceWithRawResponse(self._names.unions)

    @cached_property
    def renaming(self) -> RenamingResourceWithRawResponse:
        return RenamingResourceWithRawResponse(self._names.renaming)

    @cached_property
    def documents(self) -> DocumentsResourceWithRawResponse:
        return DocumentsResourceWithRawResponse(self._names.documents)

    @cached_property
    def reserved_names(self) -> ReservedNamesResourceWithRawResponse:
        return ReservedNamesResourceWithRawResponse(self._names.reserved_names)

    @cached_property
    def params(self) -> ParamsResourceWithRawResponse:
        return ParamsResourceWithRawResponse(self._names.params)

    @cached_property
    def can_cause_clashes(self) -> CanCauseClashesResourceWithRawResponse:
        return CanCauseClashesResourceWithRawResponse(self._names.can_cause_clashes)

    @cached_property
    def openapi_specials(self) -> OpenAPISpecialsResourceWithRawResponse:
        return OpenAPISpecialsResourceWithRawResponse(self._names.openapi_specials)


class AsyncNamesResourceWithRawResponse:
    def __init__(self, names: AsyncNamesResource) -> None:
        self._names = names

        self.child_prop_import_clash = _legacy_response.async_to_raw_response_wrapper(
            names.child_prop_import_clash,
        )
        self.get = _legacy_response.async_to_raw_response_wrapper(
            names.get,
        )
        self.properties_common_conflicts = _legacy_response.async_to_raw_response_wrapper(
            names.properties_common_conflicts,
        )
        self.properties_illegal_go_identifiers = _legacy_response.async_to_raw_response_wrapper(
            names.properties_illegal_go_identifiers,
        )
        self.properties_illegal_javascript_identifiers = _legacy_response.async_to_raw_response_wrapper(
            names.properties_illegal_javascript_identifiers,
        )
        self.response_property_clashes_model_import = _legacy_response.async_to_raw_response_wrapper(
            names.response_property_clashes_model_import,
        )
        self.response_shadows_pydantic = _legacy_response.async_to_raw_response_wrapper(
            names.response_shadows_pydantic,
        )

    @cached_property
    def unions(self) -> AsyncUnionsResourceWithRawResponse:
        return AsyncUnionsResourceWithRawResponse(self._names.unions)

    @cached_property
    def renaming(self) -> AsyncRenamingResourceWithRawResponse:
        return AsyncRenamingResourceWithRawResponse(self._names.renaming)

    @cached_property
    def documents(self) -> AsyncDocumentsResourceWithRawResponse:
        return AsyncDocumentsResourceWithRawResponse(self._names.documents)

    @cached_property
    def reserved_names(self) -> AsyncReservedNamesResourceWithRawResponse:
        return AsyncReservedNamesResourceWithRawResponse(self._names.reserved_names)

    @cached_property
    def params(self) -> AsyncParamsResourceWithRawResponse:
        return AsyncParamsResourceWithRawResponse(self._names.params)

    @cached_property
    def can_cause_clashes(self) -> AsyncCanCauseClashesResourceWithRawResponse:
        return AsyncCanCauseClashesResourceWithRawResponse(self._names.can_cause_clashes)

    @cached_property
    def openapi_specials(self) -> AsyncOpenAPISpecialsResourceWithRawResponse:
        return AsyncOpenAPISpecialsResourceWithRawResponse(self._names.openapi_specials)


class NamesResourceWithStreamingResponse:
    def __init__(self, names: NamesResource) -> None:
        self._names = names

        self.child_prop_import_clash = to_streamed_response_wrapper(
            names.child_prop_import_clash,
        )
        self.get = to_streamed_response_wrapper(
            names.get,
        )
        self.properties_common_conflicts = to_streamed_response_wrapper(
            names.properties_common_conflicts,
        )
        self.properties_illegal_go_identifiers = to_streamed_response_wrapper(
            names.properties_illegal_go_identifiers,
        )
        self.properties_illegal_javascript_identifiers = to_streamed_response_wrapper(
            names.properties_illegal_javascript_identifiers,
        )
        self.response_property_clashes_model_import = to_streamed_response_wrapper(
            names.response_property_clashes_model_import,
        )
        self.response_shadows_pydantic = to_streamed_response_wrapper(
            names.response_shadows_pydantic,
        )

    @cached_property
    def unions(self) -> UnionsResourceWithStreamingResponse:
        return UnionsResourceWithStreamingResponse(self._names.unions)

    @cached_property
    def renaming(self) -> RenamingResourceWithStreamingResponse:
        return RenamingResourceWithStreamingResponse(self._names.renaming)

    @cached_property
    def documents(self) -> DocumentsResourceWithStreamingResponse:
        return DocumentsResourceWithStreamingResponse(self._names.documents)

    @cached_property
    def reserved_names(self) -> ReservedNamesResourceWithStreamingResponse:
        return ReservedNamesResourceWithStreamingResponse(self._names.reserved_names)

    @cached_property
    def params(self) -> ParamsResourceWithStreamingResponse:
        return ParamsResourceWithStreamingResponse(self._names.params)

    @cached_property
    def can_cause_clashes(self) -> CanCauseClashesResourceWithStreamingResponse:
        return CanCauseClashesResourceWithStreamingResponse(self._names.can_cause_clashes)

    @cached_property
    def openapi_specials(self) -> OpenAPISpecialsResourceWithStreamingResponse:
        return OpenAPISpecialsResourceWithStreamingResponse(self._names.openapi_specials)


class AsyncNamesResourceWithStreamingResponse:
    def __init__(self, names: AsyncNamesResource) -> None:
        self._names = names

        self.child_prop_import_clash = async_to_streamed_response_wrapper(
            names.child_prop_import_clash,
        )
        self.get = async_to_streamed_response_wrapper(
            names.get,
        )
        self.properties_common_conflicts = async_to_streamed_response_wrapper(
            names.properties_common_conflicts,
        )
        self.properties_illegal_go_identifiers = async_to_streamed_response_wrapper(
            names.properties_illegal_go_identifiers,
        )
        self.properties_illegal_javascript_identifiers = async_to_streamed_response_wrapper(
            names.properties_illegal_javascript_identifiers,
        )
        self.response_property_clashes_model_import = async_to_streamed_response_wrapper(
            names.response_property_clashes_model_import,
        )
        self.response_shadows_pydantic = async_to_streamed_response_wrapper(
            names.response_shadows_pydantic,
        )

    @cached_property
    def unions(self) -> AsyncUnionsResourceWithStreamingResponse:
        return AsyncUnionsResourceWithStreamingResponse(self._names.unions)

    @cached_property
    def renaming(self) -> AsyncRenamingResourceWithStreamingResponse:
        return AsyncRenamingResourceWithStreamingResponse(self._names.renaming)

    @cached_property
    def documents(self) -> AsyncDocumentsResourceWithStreamingResponse:
        return AsyncDocumentsResourceWithStreamingResponse(self._names.documents)

    @cached_property
    def reserved_names(self) -> AsyncReservedNamesResourceWithStreamingResponse:
        return AsyncReservedNamesResourceWithStreamingResponse(self._names.reserved_names)

    @cached_property
    def params(self) -> AsyncParamsResourceWithStreamingResponse:
        return AsyncParamsResourceWithStreamingResponse(self._names.params)

    @cached_property
    def can_cause_clashes(self) -> AsyncCanCauseClashesResourceWithStreamingResponse:
        return AsyncCanCauseClashesResourceWithStreamingResponse(self._names.can_cause_clashes)

    @cached_property
    def openapi_specials(self) -> AsyncOpenAPISpecialsResourceWithStreamingResponse:
        return AsyncOpenAPISpecialsResourceWithStreamingResponse(self._names.openapi_specials)
