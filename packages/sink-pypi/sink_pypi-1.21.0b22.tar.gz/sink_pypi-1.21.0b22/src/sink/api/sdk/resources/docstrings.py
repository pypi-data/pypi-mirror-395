# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .. import _legacy_response
from .._types import Body, Query, Headers, NotGiven, not_given
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from .._base_client import make_request_options
from ..types.shared.basic_shared_model_object import BasicSharedModelObject
from ..types.docstring_leading_double_quote_response import DocstringLeadingDoubleQuoteResponse
from ..types.docstring_trailing_double_quote_response import DocstringTrailingDoubleQuoteResponse

__all__ = ["DocstringsResource", "AsyncDocstringsResource"]


class DocstringsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DocstringsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return DocstringsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DocstringsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return DocstringsResourceWithStreamingResponse(self)

    def description_contains_js_doc(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BasicSharedModelObject:
        """
        This is the method description.

        Hello _/ console.log('evil code') /_ Goodbye \"\"\" \"\"\"" \"\"\""" \"\"\"\"\"\"
        console.log('more evil code'); \"\"\" \\

        these need stay (valid escapes)

        \'\"\\  \\ \n\r\t\b\f\v\x63\ufe63\U0000fe63\N{HYPHEN}\1\12\123\1234a

        these need be escaped in python (invalid escapes)

        \a\\gg\\**\\((\\&&\\@@\\x2z\\u11z1\\U1111z111\\N{HYPHEN#}

        \\
        Other text
        """
        return self._get(
            "/docstrings/description_contains_comments",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BasicSharedModelObject,
        )

    def description_contains_js_doc_end(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BasicSharedModelObject:
        """
        This is the method description.

        In the middle it contains a \\**\\**/ Or ```

        Other text
        """
        return self._get(
            "/docstrings/description_contains_comment_enders",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BasicSharedModelObject,
        )

    def leading_double_quote(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DocstringLeadingDoubleQuoteResponse:
        return self._get(
            "/docstrings/property_leading_double_quote",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocstringLeadingDoubleQuoteResponse,
        )

    def trailing_double_quote(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DocstringTrailingDoubleQuoteResponse:
        return self._get(
            "/docstrings/property_trailing_double_quote",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocstringTrailingDoubleQuoteResponse,
        )


class AsyncDocstringsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDocstringsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#accessing-raw-response-data-eg-headers
        """
        return AsyncDocstringsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDocstringsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/sink-python-public#with_streaming_response
        """
        return AsyncDocstringsResourceWithStreamingResponse(self)

    async def description_contains_js_doc(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BasicSharedModelObject:
        """
        This is the method description.

        Hello _/ console.log('evil code') /_ Goodbye \"\"\" \"\"\"" \"\"\""" \"\"\"\"\"\"
        console.log('more evil code'); \"\"\" \\

        these need stay (valid escapes)

        \'\"\\  \\ \n\r\t\b\f\v\x63\ufe63\U0000fe63\N{HYPHEN}\1\12\123\1234a

        these need be escaped in python (invalid escapes)

        \a\\gg\\**\\((\\&&\\@@\\x2z\\u11z1\\U1111z111\\N{HYPHEN#}

        \\
        Other text
        """
        return await self._get(
            "/docstrings/description_contains_comments",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BasicSharedModelObject,
        )

    async def description_contains_js_doc_end(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BasicSharedModelObject:
        """
        This is the method description.

        In the middle it contains a \\**\\**/ Or ```

        Other text
        """
        return await self._get(
            "/docstrings/description_contains_comment_enders",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BasicSharedModelObject,
        )

    async def leading_double_quote(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DocstringLeadingDoubleQuoteResponse:
        return await self._get(
            "/docstrings/property_leading_double_quote",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocstringLeadingDoubleQuoteResponse,
        )

    async def trailing_double_quote(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DocstringTrailingDoubleQuoteResponse:
        return await self._get(
            "/docstrings/property_trailing_double_quote",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocstringTrailingDoubleQuoteResponse,
        )


class DocstringsResourceWithRawResponse:
    def __init__(self, docstrings: DocstringsResource) -> None:
        self._docstrings = docstrings

        self.description_contains_js_doc = _legacy_response.to_raw_response_wrapper(
            docstrings.description_contains_js_doc,
        )
        self.description_contains_js_doc_end = _legacy_response.to_raw_response_wrapper(
            docstrings.description_contains_js_doc_end,
        )
        self.leading_double_quote = _legacy_response.to_raw_response_wrapper(
            docstrings.leading_double_quote,
        )
        self.trailing_double_quote = _legacy_response.to_raw_response_wrapper(
            docstrings.trailing_double_quote,
        )


class AsyncDocstringsResourceWithRawResponse:
    def __init__(self, docstrings: AsyncDocstringsResource) -> None:
        self._docstrings = docstrings

        self.description_contains_js_doc = _legacy_response.async_to_raw_response_wrapper(
            docstrings.description_contains_js_doc,
        )
        self.description_contains_js_doc_end = _legacy_response.async_to_raw_response_wrapper(
            docstrings.description_contains_js_doc_end,
        )
        self.leading_double_quote = _legacy_response.async_to_raw_response_wrapper(
            docstrings.leading_double_quote,
        )
        self.trailing_double_quote = _legacy_response.async_to_raw_response_wrapper(
            docstrings.trailing_double_quote,
        )


class DocstringsResourceWithStreamingResponse:
    def __init__(self, docstrings: DocstringsResource) -> None:
        self._docstrings = docstrings

        self.description_contains_js_doc = to_streamed_response_wrapper(
            docstrings.description_contains_js_doc,
        )
        self.description_contains_js_doc_end = to_streamed_response_wrapper(
            docstrings.description_contains_js_doc_end,
        )
        self.leading_double_quote = to_streamed_response_wrapper(
            docstrings.leading_double_quote,
        )
        self.trailing_double_quote = to_streamed_response_wrapper(
            docstrings.trailing_double_quote,
        )


class AsyncDocstringsResourceWithStreamingResponse:
    def __init__(self, docstrings: AsyncDocstringsResource) -> None:
        self._docstrings = docstrings

        self.description_contains_js_doc = async_to_streamed_response_wrapper(
            docstrings.description_contains_js_doc,
        )
        self.description_contains_js_doc_end = async_to_streamed_response_wrapper(
            docstrings.description_contains_js_doc_end,
        )
        self.leading_double_quote = async_to_streamed_response_wrapper(
            docstrings.leading_double_quote,
        )
        self.trailing_double_quote = async_to_streamed_response_wrapper(
            docstrings.trailing_double_quote,
        )
