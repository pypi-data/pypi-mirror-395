# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .. import _legacy_response
from .._types import Body, Query, Headers, NotGiven, not_given
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from .._base_client import make_request_options
from ..types.model_from_schemas_ref import ModelFromSchemasRef
from ..types.config_tool_model_ref_from_nested_response_body_response import (
    ConfigToolModelRefFromNestedResponseBodyResponse,
)

__all__ = ["ConfigToolsResource", "AsyncConfigToolsResource"]


class ConfigToolsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ConfigToolsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return ConfigToolsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConfigToolsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return ConfigToolsResourceWithStreamingResponse(self)

    def model_ref_from_nested_response_body(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ConfigToolModelRefFromNestedResponseBodyResponse:
        return self._get(
            "/config_tools/model_refs/from_nested_response",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConfigToolModelRefFromNestedResponseBodyResponse,
        )

    def model_ref_from_schemas(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelFromSchemasRef:
        return self._get(
            "/config_tools/model_refs/from_schemas",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelFromSchemasRef,
        )


class AsyncConfigToolsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncConfigToolsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncConfigToolsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConfigToolsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncConfigToolsResourceWithStreamingResponse(self)

    async def model_ref_from_nested_response_body(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ConfigToolModelRefFromNestedResponseBodyResponse:
        return await self._get(
            "/config_tools/model_refs/from_nested_response",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConfigToolModelRefFromNestedResponseBodyResponse,
        )

    async def model_ref_from_schemas(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelFromSchemasRef:
        return await self._get(
            "/config_tools/model_refs/from_schemas",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelFromSchemasRef,
        )


class ConfigToolsResourceWithRawResponse:
    def __init__(self, config_tools: ConfigToolsResource) -> None:
        self._config_tools = config_tools

        self.model_ref_from_nested_response_body = _legacy_response.to_raw_response_wrapper(
            config_tools.model_ref_from_nested_response_body,
        )
        self.model_ref_from_schemas = _legacy_response.to_raw_response_wrapper(
            config_tools.model_ref_from_schemas,
        )


class AsyncConfigToolsResourceWithRawResponse:
    def __init__(self, config_tools: AsyncConfigToolsResource) -> None:
        self._config_tools = config_tools

        self.model_ref_from_nested_response_body = _legacy_response.async_to_raw_response_wrapper(
            config_tools.model_ref_from_nested_response_body,
        )
        self.model_ref_from_schemas = _legacy_response.async_to_raw_response_wrapper(
            config_tools.model_ref_from_schemas,
        )


class ConfigToolsResourceWithStreamingResponse:
    def __init__(self, config_tools: ConfigToolsResource) -> None:
        self._config_tools = config_tools

        self.model_ref_from_nested_response_body = to_streamed_response_wrapper(
            config_tools.model_ref_from_nested_response_body,
        )
        self.model_ref_from_schemas = to_streamed_response_wrapper(
            config_tools.model_ref_from_schemas,
        )


class AsyncConfigToolsResourceWithStreamingResponse:
    def __init__(self, config_tools: AsyncConfigToolsResource) -> None:
        self._config_tools = config_tools

        self.model_ref_from_nested_response_body = async_to_streamed_response_wrapper(
            config_tools.model_ref_from_nested_response_body,
        )
        self.model_ref_from_schemas = async_to_streamed_response_wrapper(
            config_tools.model_ref_from_schemas,
        )
