# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .arrays import (
    ArraysResource,
    AsyncArraysResource,
    ArraysResourceWithRawResponse,
    AsyncArraysResourceWithRawResponse,
    ArraysResourceWithStreamingResponse,
    AsyncArraysResourceWithStreamingResponse,
)
from .objects import (
    ObjectsResource,
    AsyncObjectsResource,
    ObjectsResourceWithRawResponse,
    AsyncObjectsResourceWithRawResponse,
    ObjectsResourceWithStreamingResponse,
    AsyncObjectsResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["InvalidSchemasResource", "AsyncInvalidSchemasResource"]


class InvalidSchemasResource(SyncAPIResource):
    @cached_property
    def arrays(self) -> ArraysResource:
        return ArraysResource(self._client)

    @cached_property
    def objects(self) -> ObjectsResource:
        return ObjectsResource(self._client)

    @cached_property
    def with_raw_response(self) -> InvalidSchemasResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return InvalidSchemasResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> InvalidSchemasResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return InvalidSchemasResourceWithStreamingResponse(self)


class AsyncInvalidSchemasResource(AsyncAPIResource):
    @cached_property
    def arrays(self) -> AsyncArraysResource:
        return AsyncArraysResource(self._client)

    @cached_property
    def objects(self) -> AsyncObjectsResource:
        return AsyncObjectsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncInvalidSchemasResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncInvalidSchemasResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncInvalidSchemasResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncInvalidSchemasResourceWithStreamingResponse(self)


class InvalidSchemasResourceWithRawResponse:
    def __init__(self, invalid_schemas: InvalidSchemasResource) -> None:
        self._invalid_schemas = invalid_schemas

    @cached_property
    def arrays(self) -> ArraysResourceWithRawResponse:
        return ArraysResourceWithRawResponse(self._invalid_schemas.arrays)

    @cached_property
    def objects(self) -> ObjectsResourceWithRawResponse:
        return ObjectsResourceWithRawResponse(self._invalid_schemas.objects)


class AsyncInvalidSchemasResourceWithRawResponse:
    def __init__(self, invalid_schemas: AsyncInvalidSchemasResource) -> None:
        self._invalid_schemas = invalid_schemas

    @cached_property
    def arrays(self) -> AsyncArraysResourceWithRawResponse:
        return AsyncArraysResourceWithRawResponse(self._invalid_schemas.arrays)

    @cached_property
    def objects(self) -> AsyncObjectsResourceWithRawResponse:
        return AsyncObjectsResourceWithRawResponse(self._invalid_schemas.objects)


class InvalidSchemasResourceWithStreamingResponse:
    def __init__(self, invalid_schemas: InvalidSchemasResource) -> None:
        self._invalid_schemas = invalid_schemas

    @cached_property
    def arrays(self) -> ArraysResourceWithStreamingResponse:
        return ArraysResourceWithStreamingResponse(self._invalid_schemas.arrays)

    @cached_property
    def objects(self) -> ObjectsResourceWithStreamingResponse:
        return ObjectsResourceWithStreamingResponse(self._invalid_schemas.objects)


class AsyncInvalidSchemasResourceWithStreamingResponse:
    def __init__(self, invalid_schemas: AsyncInvalidSchemasResource) -> None:
        self._invalid_schemas = invalid_schemas

    @cached_property
    def arrays(self) -> AsyncArraysResourceWithStreamingResponse:
        return AsyncArraysResourceWithStreamingResponse(self._invalid_schemas.arrays)

    @cached_property
    def objects(self) -> AsyncObjectsResourceWithStreamingResponse:
        return AsyncObjectsResourceWithStreamingResponse(self._invalid_schemas.objects)
