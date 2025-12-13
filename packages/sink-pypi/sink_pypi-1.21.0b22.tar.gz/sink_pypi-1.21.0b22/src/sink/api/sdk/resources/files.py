# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Mapping, cast
from typing_extensions import Literal

import httpx

from .. import _legacy_response
from ..types import (
    file_create_base64_params,
    file_create_multipart_params,
    file_no_file_multipart_params,
    file_with_optional_param_params,
    file_everything_multipart_params,
)
from .._types import (
    Body,
    Omit,
    Query,
    Headers,
    NotGiven,
    FileTypes,
    Base64FileInput,
    omit,
    not_given,
)
from .._utils import extract_files, maybe_transform, deepcopy_minimal, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from .._base_client import make_request_options
from ..types.file_create_base64_response import FileCreateBase64Response
from ..types.file_create_multipart_response import FileCreateMultipartResponse
from ..types.file_no_file_multipart_response import FileNoFileMultipartResponse
from ..types.file_with_optional_param_response import FileWithOptionalParamResponse
from ..types.file_everything_multipart_response import FileEverythingMultipartResponse

__all__ = ["FilesResource", "AsyncFilesResource"]


class FilesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FilesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return FilesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FilesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return FilesResourceWithStreamingResponse(self)

    def create_base64(
        self,
        *,
        file: Union[str, Base64FileInput],
        purpose: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> FileCreateBase64Response:
        """
        Endpoint for testing file uploads that use base64 format

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/files/base64",
            body=maybe_transform(
                {
                    "file": file,
                    "purpose": purpose,
                },
                file_create_base64_params.FileCreateBase64Params,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=FileCreateBase64Response,
        )

    def create_multipart(
        self,
        *,
        file: FileTypes,
        purpose: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> FileCreateMultipartResponse:
        """
        Endpoint for testing file uploads

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        body = deepcopy_minimal(
            {
                "file": file,
                "purpose": purpose,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/files/multipart",
            body=maybe_transform(body, file_create_multipart_params.FileCreateMultipartParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=FileCreateMultipartResponse,
        )

    def everything_multipart(
        self,
        *,
        b: bool,
        e: Literal["a", "b", "c"],
        f: float,
        file: FileTypes,
        i: int,
        purpose: str,
        s: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> FileEverythingMultipartResponse:
        """
        Endpoint for testing file uploads with all kinds of properties

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        body = deepcopy_minimal(
            {
                "b": b,
                "e": e,
                "f": f,
                "file": file,
                "i": i,
                "purpose": purpose,
                "s": s,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/files/multipart_everything",
            body=maybe_transform(body, file_everything_multipart_params.FileEverythingMultipartParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=FileEverythingMultipartResponse,
        )

    def no_file_multipart(
        self,
        *,
        purpose: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> FileNoFileMultipartResponse:
        """
        Endpoint for multipart requests without a file parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/files/no_file_multipart",
            body=maybe_transform({"purpose": purpose}, file_no_file_multipart_params.FileNoFileMultipartParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=FileNoFileMultipartResponse,
        )

    def with_optional_param(
        self,
        *,
        image: FileTypes,
        prompt: str,
        mask: FileTypes | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> FileWithOptionalParamResponse:
        """
        Multipart request with a required and an optional file request param.

        Args:
          image: The image to edit. Must be a valid PNG file, less than 4MB, and square. If mask
              is not provided, image must have transparency, which will be used as the mask.

          prompt: A text description of the desired image(s). The maximum length is 1000
              characters.

          mask: An additional image whose fully transparent areas (e.g. where alpha is zero)
              indicate where `image` should be edited. Must be a valid PNG file, less than
              4MB, and have the same dimensions as `image`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        body = deepcopy_minimal(
            {
                "image": image,
                "prompt": prompt,
                "mask": mask,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["image"], ["mask"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/files/with_optional_param",
            body=maybe_transform(body, file_with_optional_param_params.FileWithOptionalParamParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=FileWithOptionalParamResponse,
        )


class AsyncFilesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFilesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncFilesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFilesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncFilesResourceWithStreamingResponse(self)

    async def create_base64(
        self,
        *,
        file: Union[str, Base64FileInput],
        purpose: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> FileCreateBase64Response:
        """
        Endpoint for testing file uploads that use base64 format

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/files/base64",
            body=await async_maybe_transform(
                {
                    "file": file,
                    "purpose": purpose,
                },
                file_create_base64_params.FileCreateBase64Params,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=FileCreateBase64Response,
        )

    async def create_multipart(
        self,
        *,
        file: FileTypes,
        purpose: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> FileCreateMultipartResponse:
        """
        Endpoint for testing file uploads

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        body = deepcopy_minimal(
            {
                "file": file,
                "purpose": purpose,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            "/files/multipart",
            body=await async_maybe_transform(body, file_create_multipart_params.FileCreateMultipartParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=FileCreateMultipartResponse,
        )

    async def everything_multipart(
        self,
        *,
        b: bool,
        e: Literal["a", "b", "c"],
        f: float,
        file: FileTypes,
        i: int,
        purpose: str,
        s: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> FileEverythingMultipartResponse:
        """
        Endpoint for testing file uploads with all kinds of properties

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        body = deepcopy_minimal(
            {
                "b": b,
                "e": e,
                "f": f,
                "file": file,
                "i": i,
                "purpose": purpose,
                "s": s,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            "/files/multipart_everything",
            body=await async_maybe_transform(body, file_everything_multipart_params.FileEverythingMultipartParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=FileEverythingMultipartResponse,
        )

    async def no_file_multipart(
        self,
        *,
        purpose: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> FileNoFileMultipartResponse:
        """
        Endpoint for multipart requests without a file parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            "/files/no_file_multipart",
            body=await async_maybe_transform(
                {"purpose": purpose}, file_no_file_multipart_params.FileNoFileMultipartParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=FileNoFileMultipartResponse,
        )

    async def with_optional_param(
        self,
        *,
        image: FileTypes,
        prompt: str,
        mask: FileTypes | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> FileWithOptionalParamResponse:
        """
        Multipart request with a required and an optional file request param.

        Args:
          image: The image to edit. Must be a valid PNG file, less than 4MB, and square. If mask
              is not provided, image must have transparency, which will be used as the mask.

          prompt: A text description of the desired image(s). The maximum length is 1000
              characters.

          mask: An additional image whose fully transparent areas (e.g. where alpha is zero)
              indicate where `image` should be edited. Must be a valid PNG file, less than
              4MB, and have the same dimensions as `image`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        body = deepcopy_minimal(
            {
                "image": image,
                "prompt": prompt,
                "mask": mask,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["image"], ["mask"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            "/files/with_optional_param",
            body=await async_maybe_transform(body, file_with_optional_param_params.FileWithOptionalParamParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=FileWithOptionalParamResponse,
        )


class FilesResourceWithRawResponse:
    def __init__(self, files: FilesResource) -> None:
        self._files = files

        self.create_base64 = _legacy_response.to_raw_response_wrapper(
            files.create_base64,
        )
        self.create_multipart = _legacy_response.to_raw_response_wrapper(
            files.create_multipart,
        )
        self.everything_multipart = _legacy_response.to_raw_response_wrapper(
            files.everything_multipart,
        )
        self.no_file_multipart = _legacy_response.to_raw_response_wrapper(
            files.no_file_multipart,
        )
        self.with_optional_param = _legacy_response.to_raw_response_wrapper(
            files.with_optional_param,
        )


class AsyncFilesResourceWithRawResponse:
    def __init__(self, files: AsyncFilesResource) -> None:
        self._files = files

        self.create_base64 = _legacy_response.async_to_raw_response_wrapper(
            files.create_base64,
        )
        self.create_multipart = _legacy_response.async_to_raw_response_wrapper(
            files.create_multipart,
        )
        self.everything_multipart = _legacy_response.async_to_raw_response_wrapper(
            files.everything_multipart,
        )
        self.no_file_multipart = _legacy_response.async_to_raw_response_wrapper(
            files.no_file_multipart,
        )
        self.with_optional_param = _legacy_response.async_to_raw_response_wrapper(
            files.with_optional_param,
        )


class FilesResourceWithStreamingResponse:
    def __init__(self, files: FilesResource) -> None:
        self._files = files

        self.create_base64 = to_streamed_response_wrapper(
            files.create_base64,
        )
        self.create_multipart = to_streamed_response_wrapper(
            files.create_multipart,
        )
        self.everything_multipart = to_streamed_response_wrapper(
            files.everything_multipart,
        )
        self.no_file_multipart = to_streamed_response_wrapper(
            files.no_file_multipart,
        )
        self.with_optional_param = to_streamed_response_wrapper(
            files.with_optional_param,
        )


class AsyncFilesResourceWithStreamingResponse:
    def __init__(self, files: AsyncFilesResource) -> None:
        self._files = files

        self.create_base64 = async_to_streamed_response_wrapper(
            files.create_base64,
        )
        self.create_multipart = async_to_streamed_response_wrapper(
            files.create_multipart,
        )
        self.everything_multipart = async_to_streamed_response_wrapper(
            files.everything_multipart,
        )
        self.no_file_multipart = async_to_streamed_response_wrapper(
            files.no_file_multipart,
        )
        self.with_optional_param = async_to_streamed_response_wrapper(
            files.with_optional_param,
        )
