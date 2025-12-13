# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ... import _legacy_response
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ...pagination import SyncPageCursor, AsyncPageCursor
from ..._base_client import AsyncPaginator, make_request_options
from ...types.my_model import MyModel
from ...types.pagination_tests import schema_type_allofs_params, schema_type_unions_params

__all__ = ["SchemaTypesResource", "AsyncSchemaTypesResource"]


class SchemaTypesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SchemaTypesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return SchemaTypesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SchemaTypesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return SchemaTypesResourceWithStreamingResponse(self)

    def allofs(
        self,
        *,
        cursor: Optional[str] | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[MyModel]:
        """
        Test case for a cursor endpoint that defines properties using allOf

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/schema_types/allofs",
            page=SyncPageCursor[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "limit": limit,
                    },
                    schema_type_allofs_params.SchemaTypeAllofsParams,
                ),
            ),
            model=MyModel,
        )

    def unions(
        self,
        *,
        cursor: Optional[str] | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[MyModel]:
        """
        Test case for a cursor endpoint that returns an anyOf

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/schema_types/unions",
            page=SyncPageCursor[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "limit": limit,
                    },
                    schema_type_unions_params.SchemaTypeUnionsParams,
                ),
            ),
            model=MyModel,
        )


class AsyncSchemaTypesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSchemaTypesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncSchemaTypesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSchemaTypesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncSchemaTypesResourceWithStreamingResponse(self)

    def allofs(
        self,
        *,
        cursor: Optional[str] | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[MyModel, AsyncPageCursor[MyModel]]:
        """
        Test case for a cursor endpoint that defines properties using allOf

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/schema_types/allofs",
            page=AsyncPageCursor[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "limit": limit,
                    },
                    schema_type_allofs_params.SchemaTypeAllofsParams,
                ),
            ),
            model=MyModel,
        )

    def unions(
        self,
        *,
        cursor: Optional[str] | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[MyModel, AsyncPageCursor[MyModel]]:
        """
        Test case for a cursor endpoint that returns an anyOf

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/paginated/schema_types/unions",
            page=AsyncPageCursor[MyModel],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "limit": limit,
                    },
                    schema_type_unions_params.SchemaTypeUnionsParams,
                ),
            ),
            model=MyModel,
        )


class SchemaTypesResourceWithRawResponse:
    def __init__(self, schema_types: SchemaTypesResource) -> None:
        self._schema_types = schema_types

        self.allofs = _legacy_response.to_raw_response_wrapper(
            schema_types.allofs,
        )
        self.unions = _legacy_response.to_raw_response_wrapper(
            schema_types.unions,
        )


class AsyncSchemaTypesResourceWithRawResponse:
    def __init__(self, schema_types: AsyncSchemaTypesResource) -> None:
        self._schema_types = schema_types

        self.allofs = _legacy_response.async_to_raw_response_wrapper(
            schema_types.allofs,
        )
        self.unions = _legacy_response.async_to_raw_response_wrapper(
            schema_types.unions,
        )


class SchemaTypesResourceWithStreamingResponse:
    def __init__(self, schema_types: SchemaTypesResource) -> None:
        self._schema_types = schema_types

        self.allofs = to_streamed_response_wrapper(
            schema_types.allofs,
        )
        self.unions = to_streamed_response_wrapper(
            schema_types.unions,
        )


class AsyncSchemaTypesResourceWithStreamingResponse:
    def __init__(self, schema_types: AsyncSchemaTypesResource) -> None:
        self._schema_types = schema_types

        self.allofs = async_to_streamed_response_wrapper(
            schema_types.allofs,
        )
        self.unions = async_to_streamed_response_wrapper(
            schema_types.unions,
        )
