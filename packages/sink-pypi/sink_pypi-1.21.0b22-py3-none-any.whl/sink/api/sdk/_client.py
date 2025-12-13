# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Dict, Mapping, cast
from typing_extensions import Self, Literal, override

import httpx

from . import _constants, _exceptions, _legacy_response
from ._qs import Querystring
from ._types import (
    Body,
    Omit,
    Query,
    Headers,
    Timeout,
    NoneType,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
    not_given,
)
from ._utils import is_given, get_async_library, maybe_coerce_float, maybe_coerce_boolean, maybe_coerce_integer
from ._compat import cached_property
from ._version import __version__
from ._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import SinkError, APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
    make_request_options,
)
from .types.api_status import APIStatus

if TYPE_CHECKING:
    from .resources import (
        cards,
        files,
        names,
        tests,
        tools,
        types,
        casing,
        parent,
        clients,
        company,
        testing,
        widgets,
        binaries,
        envelopes,
        recursion,
        resources,
        responses,
        streaming,
        docstrings,
        empty_body,
        body_params,
        path_params,
        config_tools,
        mixed_params,
        query_params,
        client_params,
        deeply_nested,
        header_params,
        method_config,
        resource_refs,
        complex_queries,
        decorator_tests,
        invalid_schemas,
        openapi_formats,
        pagination_tests,
        positional_params,
        version_1_30_names,
        default_req_options,
        shared_query_params,
        undocumented_resource,
        make_ambiguous_schemas_looser,
        make_ambiguous_schemas_explicit,
        model_referenced_in_parent_and_child,
    )
    from .resources.cards import CardsResource, AsyncCardsResource
    from .resources.files import FilesResource, AsyncFilesResource
    from .resources.tests import TestsResource, AsyncTestsResource
    from .resources.tools import ToolsResource, AsyncToolsResource
    from .resources.clients import ClientsResource, AsyncClientsResource
    from .resources.testing import TestingResource, AsyncTestingResource
    from .resources.widgets import WidgetsResource, AsyncWidgetsResource
    from .resources.binaries import BinariesResource, AsyncBinariesResource
    from .resources.webhooks import WebhooksResource, AsyncWebhooksResource
    from .resources.envelopes import EnvelopesResource, AsyncEnvelopesResource
    from .resources.resources import ResourcesResource, AsyncResourcesResource
    from .resources.streaming import StreamingResource, AsyncStreamingResource
    from .resources.docstrings import DocstringsResource, AsyncDocstringsResource
    from .resources.empty_body import EmptyBodyResource, AsyncEmptyBodyResource
    from .resources.names.names import NamesResource, AsyncNamesResource
    from .resources.path_params import PathParamsResource, AsyncPathParamsResource
    from .resources.types.types import TypesResource, AsyncTypesResource
    from .resources.config_tools import ConfigToolsResource, AsyncConfigToolsResource
    from .resources.query_params import QueryParamsResource, AsyncQueryParamsResource
    from .resources.casing.casing import CasingResource, AsyncCasingResource
    from .resources.client_params import ClientParamsResource, AsyncClientParamsResource
    from .resources.header_params import HeaderParamsResource, AsyncHeaderParamsResource
    from .resources.method_config import MethodConfigResource, AsyncMethodConfigResource
    from .resources.parent.parent import ParentResource, AsyncParentResource
    from .resources.company.company import CompanyResource, AsyncCompanyResource
    from .resources.complex_queries import ComplexQueriesResource, AsyncComplexQueriesResource
    from .resources.openapi_formats import OpenAPIFormatsResource, AsyncOpenAPIFormatsResource
    from .resources.positional_params import PositionalParamsResource, AsyncPositionalParamsResource
    from .resources.version_1_30_names import Version1_30NamesResource, AsyncVersion1_30NamesResource
    from .resources.recursion.recursion import RecursionResource, AsyncRecursionResource
    from .resources.responses.responses import ResponsesResource, AsyncResponsesResource
    from .resources.shared_query_params import SharedQueryParamsResource, AsyncSharedQueryParamsResource
    from .resources.undocumented_resource import UndocumentedResourceResource, AsyncUndocumentedResourceResource
    from .resources.body_params.body_params import BodyParamsResource, AsyncBodyParamsResource
    from .resources.mixed_params.mixed_params import MixedParamsResource, AsyncMixedParamsResource
    from .resources.deeply_nested.deeply_nested import DeeplyNestedResource, AsyncDeeplyNestedResource
    from .resources.resource_refs.resource_refs import ResourceRefsResource, AsyncResourceRefsResource
    from .resources.make_ambiguous_schemas_looser import (
        MakeAmbiguousSchemasLooserResource,
        AsyncMakeAmbiguousSchemasLooserResource,
    )
    from .resources.decorator_tests.decorator_tests import DecoratorTestsResource, AsyncDecoratorTestsResource
    from .resources.invalid_schemas.invalid_schemas import InvalidSchemasResource, AsyncInvalidSchemasResource
    from .resources.make_ambiguous_schemas_explicit import (
        MakeAmbiguousSchemasExplicitResource,
        AsyncMakeAmbiguousSchemasExplicitResource,
    )
    from .resources.pagination_tests.pagination_tests import PaginationTestsResource, AsyncPaginationTestsResource
    from .resources.default_req_options.default_req_options import (
        DefaultReqOptionsResource,
        AsyncDefaultReqOptionsResource,
    )
    from .resources.model_referenced_in_parent_and_child.model_referenced_in_parent_and_child import (
        ModelReferencedInParentAndChildResource,
        AsyncModelReferencedInParentAndChildResource,
    )

__all__ = [
    "ENVIRONMENTS",
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "Sink",
    "AsyncSink",
    "Client",
    "AsyncClient",
]

ENVIRONMENTS: Dict[str, str] = {
    "production": "https://demo.stainlessapi.com/",
    "sandbox": "https://demo-sanbox.stainlessapi.com/",
}


class Sink(SyncAPIClient):
    # client options
    user_token: str | None
    api_key_header: str | None
    api_key_query: str | None
    username: str
    client_id: str | None
    client_secret: str | None
    some_boolean_arg: bool | None
    some_integer_arg: int | None
    some_number_arg: float | None
    some_number_arg_required: float
    some_number_arg_required_no_default: float
    some_number_arg_required_no_default_no_env: float
    required_arg_no_env: str
    required_arg_no_env_with_default: str
    client_path_param: str | None
    camel_case_path: str | None
    client_query_param: str | None
    client_path_or_query_param: str | None

    # constants
    CONSTANT_WITH_NEWLINES = _constants.CONSTANT_WITH_NEWLINES

    _environment: Literal["production", "sandbox"] | NotGiven

    def __init__(
        self,
        *,
        user_token: str | None = None,
        api_key_header: str | None = None,
        api_key_query: str | None = None,
        username: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        some_boolean_arg: bool | None = None,
        some_integer_arg: int | None = None,
        some_number_arg: float | None = None,
        some_number_arg_required: float | None = None,
        some_number_arg_required_no_default: float | None = None,
        some_number_arg_required_no_default_no_env: float,
        required_arg_no_env: str,
        required_arg_no_env_with_default: str | None = "hi!",
        client_path_param: str | None = None,
        camel_case_path: str | None = None,
        client_query_param: str | None = None,
        client_path_or_query_param: str | None = None,
        environment: Literal["production", "sandbox"] | NotGiven = not_given,
        base_url: str | httpx.URL | None | NotGiven = not_given,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous Sink client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `user_token` from `SINK_CUSTOM_API_KEY_ENV`
        - `api_key_header` from `SINK_CUSTOM_API_KEY_HEADER_ENV`
        - `api_key_query` from `SINK_CUSTOM_API_KEY_QUERY_ENV`
        - `username` from `SINK_USER`
        - `client_id` from `SINK_CLIENT_ID`
        - `client_secret` from `SINK_CLIENT_SECRET`
        - `some_boolean_arg` from `SINK_SOME_BOOLEAN_ARG`
        - `some_integer_arg` from `SINK_SOME_INTEGER_ARG`
        - `some_number_arg` from `SINK_SOME_NUMBER_ARG`
        - `some_number_arg_required` from `SINK_SOME_NUMBER_ARG`
        - `some_number_arg_required_no_default` from `SINK_SOME_NUMBER_ARG`
        """
        if user_token is None:
            user_token = os.environ.get("SINK_CUSTOM_API_KEY_ENV")
        self.user_token = user_token

        if api_key_header is None:
            api_key_header = os.environ.get("SINK_CUSTOM_API_KEY_HEADER_ENV")
        self.api_key_header = api_key_header

        if api_key_query is None:
            api_key_query = os.environ.get("SINK_CUSTOM_API_KEY_QUERY_ENV")
        self.api_key_query = api_key_query

        if username is None:
            username = os.environ.get("SINK_USER")
        if username is None:
            raise SinkError(
                "The username client option must be set either by passing username to the client or by setting the SINK_USER environment variable"
            )
        self.username = username

        if client_id is None:
            client_id = os.environ.get("SINK_CLIENT_ID")
        self.client_id = client_id

        if client_secret is None:
            client_secret = os.environ.get("SINK_CLIENT_SECRET") or "hellosecret"
        self.client_secret = client_secret

        if some_boolean_arg is None:
            some_boolean_arg = maybe_coerce_boolean(os.environ.get("SINK_SOME_BOOLEAN_ARG")) or True
        self.some_boolean_arg = some_boolean_arg

        if some_integer_arg is None:
            some_integer_arg = maybe_coerce_integer(os.environ.get("SINK_SOME_INTEGER_ARG")) or 123
        self.some_integer_arg = some_integer_arg

        if some_number_arg is None:
            some_number_arg = maybe_coerce_float(os.environ.get("SINK_SOME_NUMBER_ARG")) or 1.2
        self.some_number_arg = some_number_arg

        if some_number_arg_required is None:
            some_number_arg_required = maybe_coerce_float(os.environ.get("SINK_SOME_NUMBER_ARG")) or 1.2
        self.some_number_arg_required = some_number_arg_required

        if some_number_arg_required_no_default is None:
            some_number_arg_required_no_default = maybe_coerce_float(os.environ.get("SINK_SOME_NUMBER_ARG"))
        if some_number_arg_required_no_default is None:
            raise SinkError(
                "The some_number_arg_required_no_default client option must be set either by passing some_number_arg_required_no_default to the client or by setting the SINK_SOME_NUMBER_ARG environment variable"
            )
        self.some_number_arg_required_no_default = some_number_arg_required_no_default

        self.some_number_arg_required_no_default_no_env = some_number_arg_required_no_default_no_env

        self.required_arg_no_env = required_arg_no_env

        if required_arg_no_env_with_default is None:
            required_arg_no_env_with_default = "hi!"
        self.required_arg_no_env_with_default = required_arg_no_env_with_default

        self.client_path_param = client_path_param

        self.camel_case_path = camel_case_path

        self.client_query_param = client_query_param

        self.client_path_or_query_param = client_path_or_query_param

        self._environment = environment

        base_url_env = os.environ.get("ACME_BASE_URL")
        if is_given(base_url) and base_url is not None:
            # cast required because mypy doesn't understand the type narrowing
            base_url = cast("str | httpx.URL", base_url)  # pyright: ignore[reportUnnecessaryCast]
        elif is_given(environment):
            if base_url_env and base_url is not None:
                raise ValueError(
                    "Ambiguous URL; The `ACME_BASE_URL` env var and the `environment` argument are given. If you want to use the environment, you must pass base_url=None",
                )

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc
        elif base_url_env is not None:
            base_url = base_url_env
        else:
            self._environment = environment = "production"

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self._idempotency_header = "Idempotency-Key"

        self._default_stream_cls = Stream

    @cached_property
    def testing(self) -> TestingResource:
        from .resources.testing import TestingResource

        return TestingResource(self)

    @cached_property
    def complex_queries(self) -> ComplexQueriesResource:
        from .resources.complex_queries import ComplexQueriesResource

        return ComplexQueriesResource(self)

    @cached_property
    def casing(self) -> CasingResource:
        from .resources.casing import CasingResource

        return CasingResource(self)

    @cached_property
    def default_req_options(self) -> DefaultReqOptionsResource:
        from .resources.default_req_options import DefaultReqOptionsResource

        return DefaultReqOptionsResource(self)

    @cached_property
    def tools(self) -> ToolsResource:
        from .resources.tools import ToolsResource

        return ToolsResource(self)

    @cached_property
    def undocumented_resource(self) -> UndocumentedResourceResource:
        from .resources.undocumented_resource import UndocumentedResourceResource

        return UndocumentedResourceResource(self)

    @cached_property
    def method_config(self) -> MethodConfigResource:
        from .resources.method_config import MethodConfigResource

        return MethodConfigResource(self)

    @cached_property
    def streaming(self) -> StreamingResource:
        from .resources.streaming import StreamingResource

        return StreamingResource(self)

    @cached_property
    def pagination_tests(self) -> PaginationTestsResource:
        from .resources.pagination_tests import PaginationTestsResource

        return PaginationTestsResource(self)

    @cached_property
    def docstrings(self) -> DocstringsResource:
        from .resources.docstrings import DocstringsResource

        return DocstringsResource(self)

    @cached_property
    def invalid_schemas(self) -> InvalidSchemasResource:
        from .resources.invalid_schemas import InvalidSchemasResource

        return InvalidSchemasResource(self)

    @cached_property
    def resource_refs(self) -> ResourceRefsResource:
        from .resources.resource_refs import ResourceRefsResource

        return ResourceRefsResource(self)

    @cached_property
    def cards(self) -> CardsResource:
        from .resources.cards import CardsResource

        return CardsResource(self)

    @cached_property
    def files(self) -> FilesResource:
        from .resources.files import FilesResource

        return FilesResource(self)

    @cached_property
    def binaries(self) -> BinariesResource:
        from .resources.binaries import BinariesResource

        return BinariesResource(self)

    @cached_property
    def resources(self) -> ResourcesResource:
        from .resources.resources import ResourcesResource

        return ResourcesResource(self)

    @cached_property
    def config_tools(self) -> ConfigToolsResource:
        from .resources.config_tools import ConfigToolsResource

        return ConfigToolsResource(self)

    @cached_property
    def company(self) -> CompanyResource:
        """Stainless API company"""
        from .resources.company import CompanyResource

        return CompanyResource(self)

    @cached_property
    def openapi_formats(self) -> OpenAPIFormatsResource:
        from .resources.openapi_formats import OpenAPIFormatsResource

        return OpenAPIFormatsResource(self)

    @cached_property
    def parent(self) -> ParentResource:
        from .resources.parent import ParentResource

        return ParentResource(self)

    @cached_property
    def envelopes(self) -> EnvelopesResource:
        from .resources.envelopes import EnvelopesResource

        return EnvelopesResource(self)

    @cached_property
    def types(self) -> TypesResource:
        from .resources.types import TypesResource

        return TypesResource(self)

    @cached_property
    def clients(self) -> ClientsResource:
        from .resources.clients import ClientsResource

        return ClientsResource(self)

    @cached_property
    def names(self) -> NamesResource:
        from .resources.names import NamesResource

        return NamesResource(self)

    @cached_property
    def widgets(self) -> WidgetsResource:
        """
        Widget is love
        Widget is life
        """
        from .resources.widgets import WidgetsResource

        return WidgetsResource(self)

    @cached_property
    def webhooks(self) -> WebhooksResource:
        from .resources.webhooks import WebhooksResource

        return WebhooksResource(self)

    @cached_property
    def client_params(self) -> ClientParamsResource:
        from .resources.client_params import ClientParamsResource

        return ClientParamsResource(self)

    @cached_property
    def responses(self) -> ResponsesResource:
        from .resources.responses import ResponsesResource

        return ResponsesResource(self)

    @cached_property
    def path_params(self) -> PathParamsResource:
        from .resources.path_params import PathParamsResource

        return PathParamsResource(self)

    @cached_property
    def positional_params(self) -> PositionalParamsResource:
        from .resources.positional_params import PositionalParamsResource

        return PositionalParamsResource(self)

    @cached_property
    def empty_body(self) -> EmptyBodyResource:
        from .resources.empty_body import EmptyBodyResource

        return EmptyBodyResource(self)

    @cached_property
    def query_params(self) -> QueryParamsResource:
        from .resources.query_params import QueryParamsResource

        return QueryParamsResource(self)

    @cached_property
    def body_params(self) -> BodyParamsResource:
        from .resources.body_params import BodyParamsResource

        return BodyParamsResource(self)

    @cached_property
    def header_params(self) -> HeaderParamsResource:
        from .resources.header_params import HeaderParamsResource

        return HeaderParamsResource(self)

    @cached_property
    def mixed_params(self) -> MixedParamsResource:
        from .resources.mixed_params import MixedParamsResource

        return MixedParamsResource(self)

    @cached_property
    def make_ambiguous_schemas_looser(self) -> MakeAmbiguousSchemasLooserResource:
        from .resources.make_ambiguous_schemas_looser import MakeAmbiguousSchemasLooserResource

        return MakeAmbiguousSchemasLooserResource(self)

    @cached_property
    def make_ambiguous_schemas_explicit(self) -> MakeAmbiguousSchemasExplicitResource:
        from .resources.make_ambiguous_schemas_explicit import MakeAmbiguousSchemasExplicitResource

        return MakeAmbiguousSchemasExplicitResource(self)

    @cached_property
    def decorator_tests(self) -> DecoratorTestsResource:
        from .resources.decorator_tests import DecoratorTestsResource

        return DecoratorTestsResource(self)

    @cached_property
    def tests(self) -> TestsResource:
        from .resources.tests import TestsResource

        return TestsResource(self)

    @cached_property
    def deeply_nested(self) -> DeeplyNestedResource:
        from .resources.deeply_nested import DeeplyNestedResource

        return DeeplyNestedResource(self)

    @cached_property
    def version_1_30_names(self) -> Version1_30NamesResource:
        from .resources.version_1_30_names import Version1_30NamesResource

        return Version1_30NamesResource(self)

    @cached_property
    def recursion(self) -> RecursionResource:
        from .resources.recursion import RecursionResource

        return RecursionResource(self)

    @cached_property
    def shared_query_params(self) -> SharedQueryParamsResource:
        from .resources.shared_query_params import SharedQueryParamsResource

        return SharedQueryParamsResource(self)

    @cached_property
    def model_referenced_in_parent_and_child(self) -> ModelReferencedInParentAndChildResource:
        from .resources.model_referenced_in_parent_and_child import ModelReferencedInParentAndChildResource

        return ModelReferencedInParentAndChildResource(self)

    @cached_property
    def with_raw_response(self) -> SinkWithRawResponse:
        return SinkWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SinkWithStreamedResponse:
        return SinkWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        return {**self._bearer_auth, **self._api_key_auth}

    @property
    def _bearer_auth(self) -> dict[str, str]:
        user_token = self.user_token
        if user_token is None:
            return {}
        return {"Authorization": f"Bearer {user_token}"}

    @property
    def _api_key_auth(self) -> dict[str, str]:
        api_key_header = self.api_key_header
        if api_key_header is None:
            return {}
        return {"X-STL-APIKEY": api_key_header}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            "My-Api-Version": "11",
            "X-Enable-Metrics": "1",
            "X-Client-UserName": self.username,
            "X-Client-Secret": self.client_secret if self.client_secret is not None else Omit(),
            "X-Integer": str(self.some_integer_arg) if self.some_integer_arg is not None else Omit(),
            **self._custom_headers,
        }

    @property
    @override
    def default_query(self) -> dict[str, object]:
        return {
            **super().default_query,
            "stl-api-key": self.api_key_query if self.api_key_query is not None else Omit(),
            **self._custom_query,
        }

    def copy(
        self,
        *,
        user_token: str | None = None,
        api_key_header: str | None = None,
        api_key_query: str | None = None,
        username: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        some_boolean_arg: bool | None = None,
        some_integer_arg: int | None = None,
        some_number_arg: float | None = None,
        some_number_arg_required: float | None = None,
        some_number_arg_required_no_default: float | None = None,
        some_number_arg_required_no_default_no_env: float | None = None,
        required_arg_no_env: str | None = None,
        required_arg_no_env_with_default: str | None = None,
        client_path_param: str | None = None,
        camel_case_path: str | None = None,
        client_query_param: str | None = None,
        client_path_or_query_param: str | None = None,
        environment: Literal["production", "sandbox"] | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            user_token=user_token or self.user_token,
            api_key_header=api_key_header or self.api_key_header,
            api_key_query=api_key_query or self.api_key_query,
            username=username or self.username,
            client_id=client_id or self.client_id,
            client_secret=client_secret or self.client_secret,
            some_boolean_arg=some_boolean_arg or self.some_boolean_arg,
            some_integer_arg=some_integer_arg or self.some_integer_arg,
            some_number_arg=some_number_arg or self.some_number_arg,
            some_number_arg_required=some_number_arg_required or self.some_number_arg_required,
            some_number_arg_required_no_default=some_number_arg_required_no_default
            or self.some_number_arg_required_no_default,
            some_number_arg_required_no_default_no_env=some_number_arg_required_no_default_no_env
            or self.some_number_arg_required_no_default_no_env,
            required_arg_no_env=required_arg_no_env or self.required_arg_no_env,
            required_arg_no_env_with_default=required_arg_no_env_with_default or self.required_arg_no_env_with_default,
            client_path_param=client_path_param or self.client_path_param,
            camel_case_path=camel_case_path or self.camel_case_path,
            client_query_param=client_query_param or self.client_query_param,
            client_path_or_query_param=client_path_or_query_param or self.client_path_or_query_param,
            base_url=base_url or self.base_url,
            environment=environment or self._environment,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    def api_status(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> APIStatus:
        """API status check"""
        return self.get(
            "/status",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIStatus,
        )

    api_status_alias = api_status

    def create_no_response(
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
        """Endpoint returning no response"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self.post(
            "/no_response",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def _get_client_path_param_path_param(self) -> str:
        from_client = self.client_path_param
        if from_client is not None:
            return from_client

        raise ValueError(
            "Missing client_path_param argument; Please provide it at the client level, e.g. Sink(client_path_param='abcd') or per method."
        )

    def _get_camel_case_path_path_param(self) -> str:
        from_client = self.camel_case_path
        if from_client is not None:
            return from_client

        raise ValueError(
            "Missing camel_case_path argument; Please provide it at the client level, e.g. Sink(camel_case_path='abcd') or per method."
        )

    def _get_client_path_or_query_param_path_param(self) -> str:
        from_client = self.client_path_or_query_param
        if from_client is not None:
            return from_client

        raise ValueError(
            "Missing client_path_or_query_param argument; Please provide it at the client level, e.g. Sink(client_path_or_query_param='abcd') or per method."
        )

    def _get_client_query_param_query_param(self) -> str | None:
        return self.client_query_param

    def _get_client_path_or_query_param_query_param(self) -> str | None:
        return self.client_path_or_query_param

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncSink(AsyncAPIClient):
    # client options
    user_token: str | None
    api_key_header: str | None
    api_key_query: str | None
    username: str
    client_id: str | None
    client_secret: str | None
    some_boolean_arg: bool | None
    some_integer_arg: int | None
    some_number_arg: float | None
    some_number_arg_required: float
    some_number_arg_required_no_default: float
    some_number_arg_required_no_default_no_env: float
    required_arg_no_env: str
    required_arg_no_env_with_default: str
    client_path_param: str | None
    camel_case_path: str | None
    client_query_param: str | None
    client_path_or_query_param: str | None

    # constants
    CONSTANT_WITH_NEWLINES = _constants.CONSTANT_WITH_NEWLINES

    _environment: Literal["production", "sandbox"] | NotGiven

    def __init__(
        self,
        *,
        user_token: str | None = None,
        api_key_header: str | None = None,
        api_key_query: str | None = None,
        username: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        some_boolean_arg: bool | None = None,
        some_integer_arg: int | None = None,
        some_number_arg: float | None = None,
        some_number_arg_required: float | None = None,
        some_number_arg_required_no_default: float | None = None,
        some_number_arg_required_no_default_no_env: float,
        required_arg_no_env: str,
        required_arg_no_env_with_default: str | None = "hi!",
        client_path_param: str | None = None,
        camel_case_path: str | None = None,
        client_query_param: str | None = None,
        client_path_or_query_param: str | None = None,
        environment: Literal["production", "sandbox"] | NotGiven = not_given,
        base_url: str | httpx.URL | None | NotGiven = not_given,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncSink client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `user_token` from `SINK_CUSTOM_API_KEY_ENV`
        - `api_key_header` from `SINK_CUSTOM_API_KEY_HEADER_ENV`
        - `api_key_query` from `SINK_CUSTOM_API_KEY_QUERY_ENV`
        - `username` from `SINK_USER`
        - `client_id` from `SINK_CLIENT_ID`
        - `client_secret` from `SINK_CLIENT_SECRET`
        - `some_boolean_arg` from `SINK_SOME_BOOLEAN_ARG`
        - `some_integer_arg` from `SINK_SOME_INTEGER_ARG`
        - `some_number_arg` from `SINK_SOME_NUMBER_ARG`
        - `some_number_arg_required` from `SINK_SOME_NUMBER_ARG`
        - `some_number_arg_required_no_default` from `SINK_SOME_NUMBER_ARG`
        """
        if user_token is None:
            user_token = os.environ.get("SINK_CUSTOM_API_KEY_ENV")
        self.user_token = user_token

        if api_key_header is None:
            api_key_header = os.environ.get("SINK_CUSTOM_API_KEY_HEADER_ENV")
        self.api_key_header = api_key_header

        if api_key_query is None:
            api_key_query = os.environ.get("SINK_CUSTOM_API_KEY_QUERY_ENV")
        self.api_key_query = api_key_query

        if username is None:
            username = os.environ.get("SINK_USER")
        if username is None:
            raise SinkError(
                "The username client option must be set either by passing username to the client or by setting the SINK_USER environment variable"
            )
        self.username = username

        if client_id is None:
            client_id = os.environ.get("SINK_CLIENT_ID")
        self.client_id = client_id

        if client_secret is None:
            client_secret = os.environ.get("SINK_CLIENT_SECRET") or "hellosecret"
        self.client_secret = client_secret

        if some_boolean_arg is None:
            some_boolean_arg = maybe_coerce_boolean(os.environ.get("SINK_SOME_BOOLEAN_ARG")) or True
        self.some_boolean_arg = some_boolean_arg

        if some_integer_arg is None:
            some_integer_arg = maybe_coerce_integer(os.environ.get("SINK_SOME_INTEGER_ARG")) or 123
        self.some_integer_arg = some_integer_arg

        if some_number_arg is None:
            some_number_arg = maybe_coerce_float(os.environ.get("SINK_SOME_NUMBER_ARG")) or 1.2
        self.some_number_arg = some_number_arg

        if some_number_arg_required is None:
            some_number_arg_required = maybe_coerce_float(os.environ.get("SINK_SOME_NUMBER_ARG")) or 1.2
        self.some_number_arg_required = some_number_arg_required

        if some_number_arg_required_no_default is None:
            some_number_arg_required_no_default = maybe_coerce_float(os.environ.get("SINK_SOME_NUMBER_ARG"))
        if some_number_arg_required_no_default is None:
            raise SinkError(
                "The some_number_arg_required_no_default client option must be set either by passing some_number_arg_required_no_default to the client or by setting the SINK_SOME_NUMBER_ARG environment variable"
            )
        self.some_number_arg_required_no_default = some_number_arg_required_no_default

        self.some_number_arg_required_no_default_no_env = some_number_arg_required_no_default_no_env

        self.required_arg_no_env = required_arg_no_env

        if required_arg_no_env_with_default is None:
            required_arg_no_env_with_default = "hi!"
        self.required_arg_no_env_with_default = required_arg_no_env_with_default

        self.client_path_param = client_path_param

        self.camel_case_path = camel_case_path

        self.client_query_param = client_query_param

        self.client_path_or_query_param = client_path_or_query_param

        self._environment = environment

        base_url_env = os.environ.get("ACME_BASE_URL")
        if is_given(base_url) and base_url is not None:
            # cast required because mypy doesn't understand the type narrowing
            base_url = cast("str | httpx.URL", base_url)  # pyright: ignore[reportUnnecessaryCast]
        elif is_given(environment):
            if base_url_env and base_url is not None:
                raise ValueError(
                    "Ambiguous URL; The `ACME_BASE_URL` env var and the `environment` argument are given. If you want to use the environment, you must pass base_url=None",
                )

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc
        elif base_url_env is not None:
            base_url = base_url_env
        else:
            self._environment = environment = "production"

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self._idempotency_header = "Idempotency-Key"

        self._default_stream_cls = AsyncStream

    @cached_property
    def testing(self) -> AsyncTestingResource:
        from .resources.testing import AsyncTestingResource

        return AsyncTestingResource(self)

    @cached_property
    def complex_queries(self) -> AsyncComplexQueriesResource:
        from .resources.complex_queries import AsyncComplexQueriesResource

        return AsyncComplexQueriesResource(self)

    @cached_property
    def casing(self) -> AsyncCasingResource:
        from .resources.casing import AsyncCasingResource

        return AsyncCasingResource(self)

    @cached_property
    def default_req_options(self) -> AsyncDefaultReqOptionsResource:
        from .resources.default_req_options import AsyncDefaultReqOptionsResource

        return AsyncDefaultReqOptionsResource(self)

    @cached_property
    def tools(self) -> AsyncToolsResource:
        from .resources.tools import AsyncToolsResource

        return AsyncToolsResource(self)

    @cached_property
    def undocumented_resource(self) -> AsyncUndocumentedResourceResource:
        from .resources.undocumented_resource import AsyncUndocumentedResourceResource

        return AsyncUndocumentedResourceResource(self)

    @cached_property
    def method_config(self) -> AsyncMethodConfigResource:
        from .resources.method_config import AsyncMethodConfigResource

        return AsyncMethodConfigResource(self)

    @cached_property
    def streaming(self) -> AsyncStreamingResource:
        from .resources.streaming import AsyncStreamingResource

        return AsyncStreamingResource(self)

    @cached_property
    def pagination_tests(self) -> AsyncPaginationTestsResource:
        from .resources.pagination_tests import AsyncPaginationTestsResource

        return AsyncPaginationTestsResource(self)

    @cached_property
    def docstrings(self) -> AsyncDocstringsResource:
        from .resources.docstrings import AsyncDocstringsResource

        return AsyncDocstringsResource(self)

    @cached_property
    def invalid_schemas(self) -> AsyncInvalidSchemasResource:
        from .resources.invalid_schemas import AsyncInvalidSchemasResource

        return AsyncInvalidSchemasResource(self)

    @cached_property
    def resource_refs(self) -> AsyncResourceRefsResource:
        from .resources.resource_refs import AsyncResourceRefsResource

        return AsyncResourceRefsResource(self)

    @cached_property
    def cards(self) -> AsyncCardsResource:
        from .resources.cards import AsyncCardsResource

        return AsyncCardsResource(self)

    @cached_property
    def files(self) -> AsyncFilesResource:
        from .resources.files import AsyncFilesResource

        return AsyncFilesResource(self)

    @cached_property
    def binaries(self) -> AsyncBinariesResource:
        from .resources.binaries import AsyncBinariesResource

        return AsyncBinariesResource(self)

    @cached_property
    def resources(self) -> AsyncResourcesResource:
        from .resources.resources import AsyncResourcesResource

        return AsyncResourcesResource(self)

    @cached_property
    def config_tools(self) -> AsyncConfigToolsResource:
        from .resources.config_tools import AsyncConfigToolsResource

        return AsyncConfigToolsResource(self)

    @cached_property
    def company(self) -> AsyncCompanyResource:
        """Stainless API company"""
        from .resources.company import AsyncCompanyResource

        return AsyncCompanyResource(self)

    @cached_property
    def openapi_formats(self) -> AsyncOpenAPIFormatsResource:
        from .resources.openapi_formats import AsyncOpenAPIFormatsResource

        return AsyncOpenAPIFormatsResource(self)

    @cached_property
    def parent(self) -> AsyncParentResource:
        from .resources.parent import AsyncParentResource

        return AsyncParentResource(self)

    @cached_property
    def envelopes(self) -> AsyncEnvelopesResource:
        from .resources.envelopes import AsyncEnvelopesResource

        return AsyncEnvelopesResource(self)

    @cached_property
    def types(self) -> AsyncTypesResource:
        from .resources.types import AsyncTypesResource

        return AsyncTypesResource(self)

    @cached_property
    def clients(self) -> AsyncClientsResource:
        from .resources.clients import AsyncClientsResource

        return AsyncClientsResource(self)

    @cached_property
    def names(self) -> AsyncNamesResource:
        from .resources.names import AsyncNamesResource

        return AsyncNamesResource(self)

    @cached_property
    def widgets(self) -> AsyncWidgetsResource:
        """
        Widget is love
        Widget is life
        """
        from .resources.widgets import AsyncWidgetsResource

        return AsyncWidgetsResource(self)

    @cached_property
    def webhooks(self) -> AsyncWebhooksResource:
        from .resources.webhooks import AsyncWebhooksResource

        return AsyncWebhooksResource(self)

    @cached_property
    def client_params(self) -> AsyncClientParamsResource:
        from .resources.client_params import AsyncClientParamsResource

        return AsyncClientParamsResource(self)

    @cached_property
    def responses(self) -> AsyncResponsesResource:
        from .resources.responses import AsyncResponsesResource

        return AsyncResponsesResource(self)

    @cached_property
    def path_params(self) -> AsyncPathParamsResource:
        from .resources.path_params import AsyncPathParamsResource

        return AsyncPathParamsResource(self)

    @cached_property
    def positional_params(self) -> AsyncPositionalParamsResource:
        from .resources.positional_params import AsyncPositionalParamsResource

        return AsyncPositionalParamsResource(self)

    @cached_property
    def empty_body(self) -> AsyncEmptyBodyResource:
        from .resources.empty_body import AsyncEmptyBodyResource

        return AsyncEmptyBodyResource(self)

    @cached_property
    def query_params(self) -> AsyncQueryParamsResource:
        from .resources.query_params import AsyncQueryParamsResource

        return AsyncQueryParamsResource(self)

    @cached_property
    def body_params(self) -> AsyncBodyParamsResource:
        from .resources.body_params import AsyncBodyParamsResource

        return AsyncBodyParamsResource(self)

    @cached_property
    def header_params(self) -> AsyncHeaderParamsResource:
        from .resources.header_params import AsyncHeaderParamsResource

        return AsyncHeaderParamsResource(self)

    @cached_property
    def mixed_params(self) -> AsyncMixedParamsResource:
        from .resources.mixed_params import AsyncMixedParamsResource

        return AsyncMixedParamsResource(self)

    @cached_property
    def make_ambiguous_schemas_looser(self) -> AsyncMakeAmbiguousSchemasLooserResource:
        from .resources.make_ambiguous_schemas_looser import AsyncMakeAmbiguousSchemasLooserResource

        return AsyncMakeAmbiguousSchemasLooserResource(self)

    @cached_property
    def make_ambiguous_schemas_explicit(self) -> AsyncMakeAmbiguousSchemasExplicitResource:
        from .resources.make_ambiguous_schemas_explicit import AsyncMakeAmbiguousSchemasExplicitResource

        return AsyncMakeAmbiguousSchemasExplicitResource(self)

    @cached_property
    def decorator_tests(self) -> AsyncDecoratorTestsResource:
        from .resources.decorator_tests import AsyncDecoratorTestsResource

        return AsyncDecoratorTestsResource(self)

    @cached_property
    def tests(self) -> AsyncTestsResource:
        from .resources.tests import AsyncTestsResource

        return AsyncTestsResource(self)

    @cached_property
    def deeply_nested(self) -> AsyncDeeplyNestedResource:
        from .resources.deeply_nested import AsyncDeeplyNestedResource

        return AsyncDeeplyNestedResource(self)

    @cached_property
    def version_1_30_names(self) -> AsyncVersion1_30NamesResource:
        from .resources.version_1_30_names import AsyncVersion1_30NamesResource

        return AsyncVersion1_30NamesResource(self)

    @cached_property
    def recursion(self) -> AsyncRecursionResource:
        from .resources.recursion import AsyncRecursionResource

        return AsyncRecursionResource(self)

    @cached_property
    def shared_query_params(self) -> AsyncSharedQueryParamsResource:
        from .resources.shared_query_params import AsyncSharedQueryParamsResource

        return AsyncSharedQueryParamsResource(self)

    @cached_property
    def model_referenced_in_parent_and_child(self) -> AsyncModelReferencedInParentAndChildResource:
        from .resources.model_referenced_in_parent_and_child import AsyncModelReferencedInParentAndChildResource

        return AsyncModelReferencedInParentAndChildResource(self)

    @cached_property
    def with_raw_response(self) -> AsyncSinkWithRawResponse:
        return AsyncSinkWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSinkWithStreamedResponse:
        return AsyncSinkWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        return {**self._bearer_auth, **self._api_key_auth}

    @property
    def _bearer_auth(self) -> dict[str, str]:
        user_token = self.user_token
        if user_token is None:
            return {}
        return {"Authorization": f"Bearer {user_token}"}

    @property
    def _api_key_auth(self) -> dict[str, str]:
        api_key_header = self.api_key_header
        if api_key_header is None:
            return {}
        return {"X-STL-APIKEY": api_key_header}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            "My-Api-Version": "11",
            "X-Enable-Metrics": "1",
            "X-Client-UserName": self.username,
            "X-Client-Secret": self.client_secret if self.client_secret is not None else Omit(),
            "X-Integer": str(self.some_integer_arg) if self.some_integer_arg is not None else Omit(),
            **self._custom_headers,
        }

    @property
    @override
    def default_query(self) -> dict[str, object]:
        return {
            **super().default_query,
            "stl-api-key": self.api_key_query if self.api_key_query is not None else Omit(),
            **self._custom_query,
        }

    def copy(
        self,
        *,
        user_token: str | None = None,
        api_key_header: str | None = None,
        api_key_query: str | None = None,
        username: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        some_boolean_arg: bool | None = None,
        some_integer_arg: int | None = None,
        some_number_arg: float | None = None,
        some_number_arg_required: float | None = None,
        some_number_arg_required_no_default: float | None = None,
        some_number_arg_required_no_default_no_env: float | None = None,
        required_arg_no_env: str | None = None,
        required_arg_no_env_with_default: str | None = None,
        client_path_param: str | None = None,
        camel_case_path: str | None = None,
        client_query_param: str | None = None,
        client_path_or_query_param: str | None = None,
        environment: Literal["production", "sandbox"] | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            user_token=user_token or self.user_token,
            api_key_header=api_key_header or self.api_key_header,
            api_key_query=api_key_query or self.api_key_query,
            username=username or self.username,
            client_id=client_id or self.client_id,
            client_secret=client_secret or self.client_secret,
            some_boolean_arg=some_boolean_arg or self.some_boolean_arg,
            some_integer_arg=some_integer_arg or self.some_integer_arg,
            some_number_arg=some_number_arg or self.some_number_arg,
            some_number_arg_required=some_number_arg_required or self.some_number_arg_required,
            some_number_arg_required_no_default=some_number_arg_required_no_default
            or self.some_number_arg_required_no_default,
            some_number_arg_required_no_default_no_env=some_number_arg_required_no_default_no_env
            or self.some_number_arg_required_no_default_no_env,
            required_arg_no_env=required_arg_no_env or self.required_arg_no_env,
            required_arg_no_env_with_default=required_arg_no_env_with_default or self.required_arg_no_env_with_default,
            client_path_param=client_path_param or self.client_path_param,
            camel_case_path=camel_case_path or self.camel_case_path,
            client_query_param=client_query_param or self.client_query_param,
            client_path_or_query_param=client_path_or_query_param or self.client_path_or_query_param,
            base_url=base_url or self.base_url,
            environment=environment or self._environment,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    async def api_status(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> APIStatus:
        """API status check"""
        return await self.get(
            "/status",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIStatus,
        )

    api_status_alias = api_status

    async def create_no_response(
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
        """Endpoint returning no response"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self.post(
            "/no_response",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )

    def _get_client_path_param_path_param(self) -> str:
        from_client = self.client_path_param
        if from_client is not None:
            return from_client

        raise ValueError(
            "Missing client_path_param argument; Please provide it at the client level, e.g. AsyncSink(client_path_param='abcd') or per method."
        )

    def _get_camel_case_path_path_param(self) -> str:
        from_client = self.camel_case_path
        if from_client is not None:
            return from_client

        raise ValueError(
            "Missing camel_case_path argument; Please provide it at the client level, e.g. AsyncSink(camel_case_path='abcd') or per method."
        )

    def _get_client_path_or_query_param_path_param(self) -> str:
        from_client = self.client_path_or_query_param
        if from_client is not None:
            return from_client

        raise ValueError(
            "Missing client_path_or_query_param argument; Please provide it at the client level, e.g. AsyncSink(client_path_or_query_param='abcd') or per method."
        )

    def _get_client_query_param_query_param(self) -> str | None:
        return self.client_query_param

    def _get_client_path_or_query_param_query_param(self) -> str | None:
        return self.client_path_or_query_param

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class SinkWithRawResponse:
    _client: Sink

    def __init__(self, client: Sink) -> None:
        self._client = client

        self.api_status = _legacy_response.to_raw_response_wrapper(
            client.api_status,
        )
        self.api_status_alias = _legacy_response.to_raw_response_wrapper(
            client.api_status_alias,
        )
        self.create_no_response = _legacy_response.to_raw_response_wrapper(
            client.create_no_response,
        )

    @cached_property
    def testing(self) -> testing.TestingResourceWithRawResponse:
        from .resources.testing import TestingResourceWithRawResponse

        return TestingResourceWithRawResponse(self._client.testing)

    @cached_property
    def complex_queries(self) -> complex_queries.ComplexQueriesResourceWithRawResponse:
        from .resources.complex_queries import ComplexQueriesResourceWithRawResponse

        return ComplexQueriesResourceWithRawResponse(self._client.complex_queries)

    @cached_property
    def casing(self) -> casing.CasingResourceWithRawResponse:
        from .resources.casing import CasingResourceWithRawResponse

        return CasingResourceWithRawResponse(self._client.casing)

    @cached_property
    def default_req_options(self) -> default_req_options.DefaultReqOptionsResourceWithRawResponse:
        from .resources.default_req_options import DefaultReqOptionsResourceWithRawResponse

        return DefaultReqOptionsResourceWithRawResponse(self._client.default_req_options)

    @cached_property
    def tools(self) -> tools.ToolsResourceWithRawResponse:
        from .resources.tools import ToolsResourceWithRawResponse

        return ToolsResourceWithRawResponse(self._client.tools)

    @cached_property
    def undocumented_resource(self) -> undocumented_resource.UndocumentedResourceResourceWithRawResponse:
        from .resources.undocumented_resource import UndocumentedResourceResourceWithRawResponse

        return UndocumentedResourceResourceWithRawResponse(self._client.undocumented_resource)

    @cached_property
    def method_config(self) -> method_config.MethodConfigResourceWithRawResponse:
        from .resources.method_config import MethodConfigResourceWithRawResponse

        return MethodConfigResourceWithRawResponse(self._client.method_config)

    @cached_property
    def streaming(self) -> streaming.StreamingResourceWithRawResponse:
        from .resources.streaming import StreamingResourceWithRawResponse

        return StreamingResourceWithRawResponse(self._client.streaming)

    @cached_property
    def pagination_tests(self) -> pagination_tests.PaginationTestsResourceWithRawResponse:
        from .resources.pagination_tests import PaginationTestsResourceWithRawResponse

        return PaginationTestsResourceWithRawResponse(self._client.pagination_tests)

    @cached_property
    def docstrings(self) -> docstrings.DocstringsResourceWithRawResponse:
        from .resources.docstrings import DocstringsResourceWithRawResponse

        return DocstringsResourceWithRawResponse(self._client.docstrings)

    @cached_property
    def invalid_schemas(self) -> invalid_schemas.InvalidSchemasResourceWithRawResponse:
        from .resources.invalid_schemas import InvalidSchemasResourceWithRawResponse

        return InvalidSchemasResourceWithRawResponse(self._client.invalid_schemas)

    @cached_property
    def resource_refs(self) -> resource_refs.ResourceRefsResourceWithRawResponse:
        from .resources.resource_refs import ResourceRefsResourceWithRawResponse

        return ResourceRefsResourceWithRawResponse(self._client.resource_refs)

    @cached_property
    def cards(self) -> cards.CardsResourceWithRawResponse:
        from .resources.cards import CardsResourceWithRawResponse

        return CardsResourceWithRawResponse(self._client.cards)

    @cached_property
    def files(self) -> files.FilesResourceWithRawResponse:
        from .resources.files import FilesResourceWithRawResponse

        return FilesResourceWithRawResponse(self._client.files)

    @cached_property
    def binaries(self) -> binaries.BinariesResourceWithRawResponse:
        from .resources.binaries import BinariesResourceWithRawResponse

        return BinariesResourceWithRawResponse(self._client.binaries)

    @cached_property
    def resources(self) -> resources.ResourcesResourceWithRawResponse:
        from .resources.resources import ResourcesResourceWithRawResponse

        return ResourcesResourceWithRawResponse(self._client.resources)

    @cached_property
    def config_tools(self) -> config_tools.ConfigToolsResourceWithRawResponse:
        from .resources.config_tools import ConfigToolsResourceWithRawResponse

        return ConfigToolsResourceWithRawResponse(self._client.config_tools)

    @cached_property
    def company(self) -> company.CompanyResourceWithRawResponse:
        """Stainless API company"""
        from .resources.company import CompanyResourceWithRawResponse

        return CompanyResourceWithRawResponse(self._client.company)

    @cached_property
    def openapi_formats(self) -> openapi_formats.OpenAPIFormatsResourceWithRawResponse:
        from .resources.openapi_formats import OpenAPIFormatsResourceWithRawResponse

        return OpenAPIFormatsResourceWithRawResponse(self._client.openapi_formats)

    @cached_property
    def parent(self) -> parent.ParentResourceWithRawResponse:
        from .resources.parent import ParentResourceWithRawResponse

        return ParentResourceWithRawResponse(self._client.parent)

    @cached_property
    def envelopes(self) -> envelopes.EnvelopesResourceWithRawResponse:
        from .resources.envelopes import EnvelopesResourceWithRawResponse

        return EnvelopesResourceWithRawResponse(self._client.envelopes)

    @cached_property
    def types(self) -> types.TypesResourceWithRawResponse:
        from .resources.types import TypesResourceWithRawResponse

        return TypesResourceWithRawResponse(self._client.types)

    @cached_property
    def clients(self) -> clients.ClientsResourceWithRawResponse:
        from .resources.clients import ClientsResourceWithRawResponse

        return ClientsResourceWithRawResponse(self._client.clients)

    @cached_property
    def names(self) -> names.NamesResourceWithRawResponse:
        from .resources.names import NamesResourceWithRawResponse

        return NamesResourceWithRawResponse(self._client.names)

    @cached_property
    def widgets(self) -> widgets.WidgetsResourceWithRawResponse:
        """
        Widget is love
        Widget is life
        """
        from .resources.widgets import WidgetsResourceWithRawResponse

        return WidgetsResourceWithRawResponse(self._client.widgets)

    @cached_property
    def client_params(self) -> client_params.ClientParamsResourceWithRawResponse:
        from .resources.client_params import ClientParamsResourceWithRawResponse

        return ClientParamsResourceWithRawResponse(self._client.client_params)

    @cached_property
    def responses(self) -> responses.ResponsesResourceWithRawResponse:
        from .resources.responses import ResponsesResourceWithRawResponse

        return ResponsesResourceWithRawResponse(self._client.responses)

    @cached_property
    def path_params(self) -> path_params.PathParamsResourceWithRawResponse:
        from .resources.path_params import PathParamsResourceWithRawResponse

        return PathParamsResourceWithRawResponse(self._client.path_params)

    @cached_property
    def positional_params(self) -> positional_params.PositionalParamsResourceWithRawResponse:
        from .resources.positional_params import PositionalParamsResourceWithRawResponse

        return PositionalParamsResourceWithRawResponse(self._client.positional_params)

    @cached_property
    def empty_body(self) -> empty_body.EmptyBodyResourceWithRawResponse:
        from .resources.empty_body import EmptyBodyResourceWithRawResponse

        return EmptyBodyResourceWithRawResponse(self._client.empty_body)

    @cached_property
    def query_params(self) -> query_params.QueryParamsResourceWithRawResponse:
        from .resources.query_params import QueryParamsResourceWithRawResponse

        return QueryParamsResourceWithRawResponse(self._client.query_params)

    @cached_property
    def body_params(self) -> body_params.BodyParamsResourceWithRawResponse:
        from .resources.body_params import BodyParamsResourceWithRawResponse

        return BodyParamsResourceWithRawResponse(self._client.body_params)

    @cached_property
    def header_params(self) -> header_params.HeaderParamsResourceWithRawResponse:
        from .resources.header_params import HeaderParamsResourceWithRawResponse

        return HeaderParamsResourceWithRawResponse(self._client.header_params)

    @cached_property
    def mixed_params(self) -> mixed_params.MixedParamsResourceWithRawResponse:
        from .resources.mixed_params import MixedParamsResourceWithRawResponse

        return MixedParamsResourceWithRawResponse(self._client.mixed_params)

    @cached_property
    def make_ambiguous_schemas_looser(
        self,
    ) -> make_ambiguous_schemas_looser.MakeAmbiguousSchemasLooserResourceWithRawResponse:
        from .resources.make_ambiguous_schemas_looser import MakeAmbiguousSchemasLooserResourceWithRawResponse

        return MakeAmbiguousSchemasLooserResourceWithRawResponse(self._client.make_ambiguous_schemas_looser)

    @cached_property
    def make_ambiguous_schemas_explicit(
        self,
    ) -> make_ambiguous_schemas_explicit.MakeAmbiguousSchemasExplicitResourceWithRawResponse:
        from .resources.make_ambiguous_schemas_explicit import MakeAmbiguousSchemasExplicitResourceWithRawResponse

        return MakeAmbiguousSchemasExplicitResourceWithRawResponse(self._client.make_ambiguous_schemas_explicit)

    @cached_property
    def decorator_tests(self) -> decorator_tests.DecoratorTestsResourceWithRawResponse:
        from .resources.decorator_tests import DecoratorTestsResourceWithRawResponse

        return DecoratorTestsResourceWithRawResponse(self._client.decorator_tests)

    @cached_property
    def tests(self) -> tests.TestsResourceWithRawResponse:
        from .resources.tests import TestsResourceWithRawResponse

        return TestsResourceWithRawResponse(self._client.tests)

    @cached_property
    def deeply_nested(self) -> deeply_nested.DeeplyNestedResourceWithRawResponse:
        from .resources.deeply_nested import DeeplyNestedResourceWithRawResponse

        return DeeplyNestedResourceWithRawResponse(self._client.deeply_nested)

    @cached_property
    def version_1_30_names(self) -> version_1_30_names.Version1_30NamesResourceWithRawResponse:
        from .resources.version_1_30_names import Version1_30NamesResourceWithRawResponse

        return Version1_30NamesResourceWithRawResponse(self._client.version_1_30_names)

    @cached_property
    def recursion(self) -> recursion.RecursionResourceWithRawResponse:
        from .resources.recursion import RecursionResourceWithRawResponse

        return RecursionResourceWithRawResponse(self._client.recursion)

    @cached_property
    def shared_query_params(self) -> shared_query_params.SharedQueryParamsResourceWithRawResponse:
        from .resources.shared_query_params import SharedQueryParamsResourceWithRawResponse

        return SharedQueryParamsResourceWithRawResponse(self._client.shared_query_params)

    @cached_property
    def model_referenced_in_parent_and_child(
        self,
    ) -> model_referenced_in_parent_and_child.ModelReferencedInParentAndChildResourceWithRawResponse:
        from .resources.model_referenced_in_parent_and_child import (
            ModelReferencedInParentAndChildResourceWithRawResponse,
        )

        return ModelReferencedInParentAndChildResourceWithRawResponse(self._client.model_referenced_in_parent_and_child)


class AsyncSinkWithRawResponse:
    _client: AsyncSink

    def __init__(self, client: AsyncSink) -> None:
        self._client = client

        self.api_status = _legacy_response.async_to_raw_response_wrapper(
            client.api_status,
        )
        self.api_status_alias = _legacy_response.async_to_raw_response_wrapper(
            client.api_status_alias,
        )
        self.create_no_response = _legacy_response.async_to_raw_response_wrapper(
            client.create_no_response,
        )

    @cached_property
    def testing(self) -> testing.AsyncTestingResourceWithRawResponse:
        from .resources.testing import AsyncTestingResourceWithRawResponse

        return AsyncTestingResourceWithRawResponse(self._client.testing)

    @cached_property
    def complex_queries(self) -> complex_queries.AsyncComplexQueriesResourceWithRawResponse:
        from .resources.complex_queries import AsyncComplexQueriesResourceWithRawResponse

        return AsyncComplexQueriesResourceWithRawResponse(self._client.complex_queries)

    @cached_property
    def casing(self) -> casing.AsyncCasingResourceWithRawResponse:
        from .resources.casing import AsyncCasingResourceWithRawResponse

        return AsyncCasingResourceWithRawResponse(self._client.casing)

    @cached_property
    def default_req_options(self) -> default_req_options.AsyncDefaultReqOptionsResourceWithRawResponse:
        from .resources.default_req_options import AsyncDefaultReqOptionsResourceWithRawResponse

        return AsyncDefaultReqOptionsResourceWithRawResponse(self._client.default_req_options)

    @cached_property
    def tools(self) -> tools.AsyncToolsResourceWithRawResponse:
        from .resources.tools import AsyncToolsResourceWithRawResponse

        return AsyncToolsResourceWithRawResponse(self._client.tools)

    @cached_property
    def undocumented_resource(self) -> undocumented_resource.AsyncUndocumentedResourceResourceWithRawResponse:
        from .resources.undocumented_resource import AsyncUndocumentedResourceResourceWithRawResponse

        return AsyncUndocumentedResourceResourceWithRawResponse(self._client.undocumented_resource)

    @cached_property
    def method_config(self) -> method_config.AsyncMethodConfigResourceWithRawResponse:
        from .resources.method_config import AsyncMethodConfigResourceWithRawResponse

        return AsyncMethodConfigResourceWithRawResponse(self._client.method_config)

    @cached_property
    def streaming(self) -> streaming.AsyncStreamingResourceWithRawResponse:
        from .resources.streaming import AsyncStreamingResourceWithRawResponse

        return AsyncStreamingResourceWithRawResponse(self._client.streaming)

    @cached_property
    def pagination_tests(self) -> pagination_tests.AsyncPaginationTestsResourceWithRawResponse:
        from .resources.pagination_tests import AsyncPaginationTestsResourceWithRawResponse

        return AsyncPaginationTestsResourceWithRawResponse(self._client.pagination_tests)

    @cached_property
    def docstrings(self) -> docstrings.AsyncDocstringsResourceWithRawResponse:
        from .resources.docstrings import AsyncDocstringsResourceWithRawResponse

        return AsyncDocstringsResourceWithRawResponse(self._client.docstrings)

    @cached_property
    def invalid_schemas(self) -> invalid_schemas.AsyncInvalidSchemasResourceWithRawResponse:
        from .resources.invalid_schemas import AsyncInvalidSchemasResourceWithRawResponse

        return AsyncInvalidSchemasResourceWithRawResponse(self._client.invalid_schemas)

    @cached_property
    def resource_refs(self) -> resource_refs.AsyncResourceRefsResourceWithRawResponse:
        from .resources.resource_refs import AsyncResourceRefsResourceWithRawResponse

        return AsyncResourceRefsResourceWithRawResponse(self._client.resource_refs)

    @cached_property
    def cards(self) -> cards.AsyncCardsResourceWithRawResponse:
        from .resources.cards import AsyncCardsResourceWithRawResponse

        return AsyncCardsResourceWithRawResponse(self._client.cards)

    @cached_property
    def files(self) -> files.AsyncFilesResourceWithRawResponse:
        from .resources.files import AsyncFilesResourceWithRawResponse

        return AsyncFilesResourceWithRawResponse(self._client.files)

    @cached_property
    def binaries(self) -> binaries.AsyncBinariesResourceWithRawResponse:
        from .resources.binaries import AsyncBinariesResourceWithRawResponse

        return AsyncBinariesResourceWithRawResponse(self._client.binaries)

    @cached_property
    def resources(self) -> resources.AsyncResourcesResourceWithRawResponse:
        from .resources.resources import AsyncResourcesResourceWithRawResponse

        return AsyncResourcesResourceWithRawResponse(self._client.resources)

    @cached_property
    def config_tools(self) -> config_tools.AsyncConfigToolsResourceWithRawResponse:
        from .resources.config_tools import AsyncConfigToolsResourceWithRawResponse

        return AsyncConfigToolsResourceWithRawResponse(self._client.config_tools)

    @cached_property
    def company(self) -> company.AsyncCompanyResourceWithRawResponse:
        """Stainless API company"""
        from .resources.company import AsyncCompanyResourceWithRawResponse

        return AsyncCompanyResourceWithRawResponse(self._client.company)

    @cached_property
    def openapi_formats(self) -> openapi_formats.AsyncOpenAPIFormatsResourceWithRawResponse:
        from .resources.openapi_formats import AsyncOpenAPIFormatsResourceWithRawResponse

        return AsyncOpenAPIFormatsResourceWithRawResponse(self._client.openapi_formats)

    @cached_property
    def parent(self) -> parent.AsyncParentResourceWithRawResponse:
        from .resources.parent import AsyncParentResourceWithRawResponse

        return AsyncParentResourceWithRawResponse(self._client.parent)

    @cached_property
    def envelopes(self) -> envelopes.AsyncEnvelopesResourceWithRawResponse:
        from .resources.envelopes import AsyncEnvelopesResourceWithRawResponse

        return AsyncEnvelopesResourceWithRawResponse(self._client.envelopes)

    @cached_property
    def types(self) -> types.AsyncTypesResourceWithRawResponse:
        from .resources.types import AsyncTypesResourceWithRawResponse

        return AsyncTypesResourceWithRawResponse(self._client.types)

    @cached_property
    def clients(self) -> clients.AsyncClientsResourceWithRawResponse:
        from .resources.clients import AsyncClientsResourceWithRawResponse

        return AsyncClientsResourceWithRawResponse(self._client.clients)

    @cached_property
    def names(self) -> names.AsyncNamesResourceWithRawResponse:
        from .resources.names import AsyncNamesResourceWithRawResponse

        return AsyncNamesResourceWithRawResponse(self._client.names)

    @cached_property
    def widgets(self) -> widgets.AsyncWidgetsResourceWithRawResponse:
        """
        Widget is love
        Widget is life
        """
        from .resources.widgets import AsyncWidgetsResourceWithRawResponse

        return AsyncWidgetsResourceWithRawResponse(self._client.widgets)

    @cached_property
    def client_params(self) -> client_params.AsyncClientParamsResourceWithRawResponse:
        from .resources.client_params import AsyncClientParamsResourceWithRawResponse

        return AsyncClientParamsResourceWithRawResponse(self._client.client_params)

    @cached_property
    def responses(self) -> responses.AsyncResponsesResourceWithRawResponse:
        from .resources.responses import AsyncResponsesResourceWithRawResponse

        return AsyncResponsesResourceWithRawResponse(self._client.responses)

    @cached_property
    def path_params(self) -> path_params.AsyncPathParamsResourceWithRawResponse:
        from .resources.path_params import AsyncPathParamsResourceWithRawResponse

        return AsyncPathParamsResourceWithRawResponse(self._client.path_params)

    @cached_property
    def positional_params(self) -> positional_params.AsyncPositionalParamsResourceWithRawResponse:
        from .resources.positional_params import AsyncPositionalParamsResourceWithRawResponse

        return AsyncPositionalParamsResourceWithRawResponse(self._client.positional_params)

    @cached_property
    def empty_body(self) -> empty_body.AsyncEmptyBodyResourceWithRawResponse:
        from .resources.empty_body import AsyncEmptyBodyResourceWithRawResponse

        return AsyncEmptyBodyResourceWithRawResponse(self._client.empty_body)

    @cached_property
    def query_params(self) -> query_params.AsyncQueryParamsResourceWithRawResponse:
        from .resources.query_params import AsyncQueryParamsResourceWithRawResponse

        return AsyncQueryParamsResourceWithRawResponse(self._client.query_params)

    @cached_property
    def body_params(self) -> body_params.AsyncBodyParamsResourceWithRawResponse:
        from .resources.body_params import AsyncBodyParamsResourceWithRawResponse

        return AsyncBodyParamsResourceWithRawResponse(self._client.body_params)

    @cached_property
    def header_params(self) -> header_params.AsyncHeaderParamsResourceWithRawResponse:
        from .resources.header_params import AsyncHeaderParamsResourceWithRawResponse

        return AsyncHeaderParamsResourceWithRawResponse(self._client.header_params)

    @cached_property
    def mixed_params(self) -> mixed_params.AsyncMixedParamsResourceWithRawResponse:
        from .resources.mixed_params import AsyncMixedParamsResourceWithRawResponse

        return AsyncMixedParamsResourceWithRawResponse(self._client.mixed_params)

    @cached_property
    def make_ambiguous_schemas_looser(
        self,
    ) -> make_ambiguous_schemas_looser.AsyncMakeAmbiguousSchemasLooserResourceWithRawResponse:
        from .resources.make_ambiguous_schemas_looser import AsyncMakeAmbiguousSchemasLooserResourceWithRawResponse

        return AsyncMakeAmbiguousSchemasLooserResourceWithRawResponse(self._client.make_ambiguous_schemas_looser)

    @cached_property
    def make_ambiguous_schemas_explicit(
        self,
    ) -> make_ambiguous_schemas_explicit.AsyncMakeAmbiguousSchemasExplicitResourceWithRawResponse:
        from .resources.make_ambiguous_schemas_explicit import AsyncMakeAmbiguousSchemasExplicitResourceWithRawResponse

        return AsyncMakeAmbiguousSchemasExplicitResourceWithRawResponse(self._client.make_ambiguous_schemas_explicit)

    @cached_property
    def decorator_tests(self) -> decorator_tests.AsyncDecoratorTestsResourceWithRawResponse:
        from .resources.decorator_tests import AsyncDecoratorTestsResourceWithRawResponse

        return AsyncDecoratorTestsResourceWithRawResponse(self._client.decorator_tests)

    @cached_property
    def tests(self) -> tests.AsyncTestsResourceWithRawResponse:
        from .resources.tests import AsyncTestsResourceWithRawResponse

        return AsyncTestsResourceWithRawResponse(self._client.tests)

    @cached_property
    def deeply_nested(self) -> deeply_nested.AsyncDeeplyNestedResourceWithRawResponse:
        from .resources.deeply_nested import AsyncDeeplyNestedResourceWithRawResponse

        return AsyncDeeplyNestedResourceWithRawResponse(self._client.deeply_nested)

    @cached_property
    def version_1_30_names(self) -> version_1_30_names.AsyncVersion1_30NamesResourceWithRawResponse:
        from .resources.version_1_30_names import AsyncVersion1_30NamesResourceWithRawResponse

        return AsyncVersion1_30NamesResourceWithRawResponse(self._client.version_1_30_names)

    @cached_property
    def recursion(self) -> recursion.AsyncRecursionResourceWithRawResponse:
        from .resources.recursion import AsyncRecursionResourceWithRawResponse

        return AsyncRecursionResourceWithRawResponse(self._client.recursion)

    @cached_property
    def shared_query_params(self) -> shared_query_params.AsyncSharedQueryParamsResourceWithRawResponse:
        from .resources.shared_query_params import AsyncSharedQueryParamsResourceWithRawResponse

        return AsyncSharedQueryParamsResourceWithRawResponse(self._client.shared_query_params)

    @cached_property
    def model_referenced_in_parent_and_child(
        self,
    ) -> model_referenced_in_parent_and_child.AsyncModelReferencedInParentAndChildResourceWithRawResponse:
        from .resources.model_referenced_in_parent_and_child import (
            AsyncModelReferencedInParentAndChildResourceWithRawResponse,
        )

        return AsyncModelReferencedInParentAndChildResourceWithRawResponse(
            self._client.model_referenced_in_parent_and_child
        )


class SinkWithStreamedResponse:
    _client: Sink

    def __init__(self, client: Sink) -> None:
        self._client = client

        self.api_status = to_streamed_response_wrapper(
            client.api_status,
        )
        self.api_status_alias = to_streamed_response_wrapper(
            client.api_status_alias,
        )
        self.create_no_response = to_streamed_response_wrapper(
            client.create_no_response,
        )

    @cached_property
    def testing(self) -> testing.TestingResourceWithStreamingResponse:
        from .resources.testing import TestingResourceWithStreamingResponse

        return TestingResourceWithStreamingResponse(self._client.testing)

    @cached_property
    def complex_queries(self) -> complex_queries.ComplexQueriesResourceWithStreamingResponse:
        from .resources.complex_queries import ComplexQueriesResourceWithStreamingResponse

        return ComplexQueriesResourceWithStreamingResponse(self._client.complex_queries)

    @cached_property
    def casing(self) -> casing.CasingResourceWithStreamingResponse:
        from .resources.casing import CasingResourceWithStreamingResponse

        return CasingResourceWithStreamingResponse(self._client.casing)

    @cached_property
    def default_req_options(self) -> default_req_options.DefaultReqOptionsResourceWithStreamingResponse:
        from .resources.default_req_options import DefaultReqOptionsResourceWithStreamingResponse

        return DefaultReqOptionsResourceWithStreamingResponse(self._client.default_req_options)

    @cached_property
    def tools(self) -> tools.ToolsResourceWithStreamingResponse:
        from .resources.tools import ToolsResourceWithStreamingResponse

        return ToolsResourceWithStreamingResponse(self._client.tools)

    @cached_property
    def undocumented_resource(self) -> undocumented_resource.UndocumentedResourceResourceWithStreamingResponse:
        from .resources.undocumented_resource import UndocumentedResourceResourceWithStreamingResponse

        return UndocumentedResourceResourceWithStreamingResponse(self._client.undocumented_resource)

    @cached_property
    def method_config(self) -> method_config.MethodConfigResourceWithStreamingResponse:
        from .resources.method_config import MethodConfigResourceWithStreamingResponse

        return MethodConfigResourceWithStreamingResponse(self._client.method_config)

    @cached_property
    def streaming(self) -> streaming.StreamingResourceWithStreamingResponse:
        from .resources.streaming import StreamingResourceWithStreamingResponse

        return StreamingResourceWithStreamingResponse(self._client.streaming)

    @cached_property
    def pagination_tests(self) -> pagination_tests.PaginationTestsResourceWithStreamingResponse:
        from .resources.pagination_tests import PaginationTestsResourceWithStreamingResponse

        return PaginationTestsResourceWithStreamingResponse(self._client.pagination_tests)

    @cached_property
    def docstrings(self) -> docstrings.DocstringsResourceWithStreamingResponse:
        from .resources.docstrings import DocstringsResourceWithStreamingResponse

        return DocstringsResourceWithStreamingResponse(self._client.docstrings)

    @cached_property
    def invalid_schemas(self) -> invalid_schemas.InvalidSchemasResourceWithStreamingResponse:
        from .resources.invalid_schemas import InvalidSchemasResourceWithStreamingResponse

        return InvalidSchemasResourceWithStreamingResponse(self._client.invalid_schemas)

    @cached_property
    def resource_refs(self) -> resource_refs.ResourceRefsResourceWithStreamingResponse:
        from .resources.resource_refs import ResourceRefsResourceWithStreamingResponse

        return ResourceRefsResourceWithStreamingResponse(self._client.resource_refs)

    @cached_property
    def cards(self) -> cards.CardsResourceWithStreamingResponse:
        from .resources.cards import CardsResourceWithStreamingResponse

        return CardsResourceWithStreamingResponse(self._client.cards)

    @cached_property
    def files(self) -> files.FilesResourceWithStreamingResponse:
        from .resources.files import FilesResourceWithStreamingResponse

        return FilesResourceWithStreamingResponse(self._client.files)

    @cached_property
    def binaries(self) -> binaries.BinariesResourceWithStreamingResponse:
        from .resources.binaries import BinariesResourceWithStreamingResponse

        return BinariesResourceWithStreamingResponse(self._client.binaries)

    @cached_property
    def resources(self) -> resources.ResourcesResourceWithStreamingResponse:
        from .resources.resources import ResourcesResourceWithStreamingResponse

        return ResourcesResourceWithStreamingResponse(self._client.resources)

    @cached_property
    def config_tools(self) -> config_tools.ConfigToolsResourceWithStreamingResponse:
        from .resources.config_tools import ConfigToolsResourceWithStreamingResponse

        return ConfigToolsResourceWithStreamingResponse(self._client.config_tools)

    @cached_property
    def company(self) -> company.CompanyResourceWithStreamingResponse:
        """Stainless API company"""
        from .resources.company import CompanyResourceWithStreamingResponse

        return CompanyResourceWithStreamingResponse(self._client.company)

    @cached_property
    def openapi_formats(self) -> openapi_formats.OpenAPIFormatsResourceWithStreamingResponse:
        from .resources.openapi_formats import OpenAPIFormatsResourceWithStreamingResponse

        return OpenAPIFormatsResourceWithStreamingResponse(self._client.openapi_formats)

    @cached_property
    def parent(self) -> parent.ParentResourceWithStreamingResponse:
        from .resources.parent import ParentResourceWithStreamingResponse

        return ParentResourceWithStreamingResponse(self._client.parent)

    @cached_property
    def envelopes(self) -> envelopes.EnvelopesResourceWithStreamingResponse:
        from .resources.envelopes import EnvelopesResourceWithStreamingResponse

        return EnvelopesResourceWithStreamingResponse(self._client.envelopes)

    @cached_property
    def types(self) -> types.TypesResourceWithStreamingResponse:
        from .resources.types import TypesResourceWithStreamingResponse

        return TypesResourceWithStreamingResponse(self._client.types)

    @cached_property
    def clients(self) -> clients.ClientsResourceWithStreamingResponse:
        from .resources.clients import ClientsResourceWithStreamingResponse

        return ClientsResourceWithStreamingResponse(self._client.clients)

    @cached_property
    def names(self) -> names.NamesResourceWithStreamingResponse:
        from .resources.names import NamesResourceWithStreamingResponse

        return NamesResourceWithStreamingResponse(self._client.names)

    @cached_property
    def widgets(self) -> widgets.WidgetsResourceWithStreamingResponse:
        """
        Widget is love
        Widget is life
        """
        from .resources.widgets import WidgetsResourceWithStreamingResponse

        return WidgetsResourceWithStreamingResponse(self._client.widgets)

    @cached_property
    def client_params(self) -> client_params.ClientParamsResourceWithStreamingResponse:
        from .resources.client_params import ClientParamsResourceWithStreamingResponse

        return ClientParamsResourceWithStreamingResponse(self._client.client_params)

    @cached_property
    def responses(self) -> responses.ResponsesResourceWithStreamingResponse:
        from .resources.responses import ResponsesResourceWithStreamingResponse

        return ResponsesResourceWithStreamingResponse(self._client.responses)

    @cached_property
    def path_params(self) -> path_params.PathParamsResourceWithStreamingResponse:
        from .resources.path_params import PathParamsResourceWithStreamingResponse

        return PathParamsResourceWithStreamingResponse(self._client.path_params)

    @cached_property
    def positional_params(self) -> positional_params.PositionalParamsResourceWithStreamingResponse:
        from .resources.positional_params import PositionalParamsResourceWithStreamingResponse

        return PositionalParamsResourceWithStreamingResponse(self._client.positional_params)

    @cached_property
    def empty_body(self) -> empty_body.EmptyBodyResourceWithStreamingResponse:
        from .resources.empty_body import EmptyBodyResourceWithStreamingResponse

        return EmptyBodyResourceWithStreamingResponse(self._client.empty_body)

    @cached_property
    def query_params(self) -> query_params.QueryParamsResourceWithStreamingResponse:
        from .resources.query_params import QueryParamsResourceWithStreamingResponse

        return QueryParamsResourceWithStreamingResponse(self._client.query_params)

    @cached_property
    def body_params(self) -> body_params.BodyParamsResourceWithStreamingResponse:
        from .resources.body_params import BodyParamsResourceWithStreamingResponse

        return BodyParamsResourceWithStreamingResponse(self._client.body_params)

    @cached_property
    def header_params(self) -> header_params.HeaderParamsResourceWithStreamingResponse:
        from .resources.header_params import HeaderParamsResourceWithStreamingResponse

        return HeaderParamsResourceWithStreamingResponse(self._client.header_params)

    @cached_property
    def mixed_params(self) -> mixed_params.MixedParamsResourceWithStreamingResponse:
        from .resources.mixed_params import MixedParamsResourceWithStreamingResponse

        return MixedParamsResourceWithStreamingResponse(self._client.mixed_params)

    @cached_property
    def make_ambiguous_schemas_looser(
        self,
    ) -> make_ambiguous_schemas_looser.MakeAmbiguousSchemasLooserResourceWithStreamingResponse:
        from .resources.make_ambiguous_schemas_looser import MakeAmbiguousSchemasLooserResourceWithStreamingResponse

        return MakeAmbiguousSchemasLooserResourceWithStreamingResponse(self._client.make_ambiguous_schemas_looser)

    @cached_property
    def make_ambiguous_schemas_explicit(
        self,
    ) -> make_ambiguous_schemas_explicit.MakeAmbiguousSchemasExplicitResourceWithStreamingResponse:
        from .resources.make_ambiguous_schemas_explicit import MakeAmbiguousSchemasExplicitResourceWithStreamingResponse

        return MakeAmbiguousSchemasExplicitResourceWithStreamingResponse(self._client.make_ambiguous_schemas_explicit)

    @cached_property
    def decorator_tests(self) -> decorator_tests.DecoratorTestsResourceWithStreamingResponse:
        from .resources.decorator_tests import DecoratorTestsResourceWithStreamingResponse

        return DecoratorTestsResourceWithStreamingResponse(self._client.decorator_tests)

    @cached_property
    def tests(self) -> tests.TestsResourceWithStreamingResponse:
        from .resources.tests import TestsResourceWithStreamingResponse

        return TestsResourceWithStreamingResponse(self._client.tests)

    @cached_property
    def deeply_nested(self) -> deeply_nested.DeeplyNestedResourceWithStreamingResponse:
        from .resources.deeply_nested import DeeplyNestedResourceWithStreamingResponse

        return DeeplyNestedResourceWithStreamingResponse(self._client.deeply_nested)

    @cached_property
    def version_1_30_names(self) -> version_1_30_names.Version1_30NamesResourceWithStreamingResponse:
        from .resources.version_1_30_names import Version1_30NamesResourceWithStreamingResponse

        return Version1_30NamesResourceWithStreamingResponse(self._client.version_1_30_names)

    @cached_property
    def recursion(self) -> recursion.RecursionResourceWithStreamingResponse:
        from .resources.recursion import RecursionResourceWithStreamingResponse

        return RecursionResourceWithStreamingResponse(self._client.recursion)

    @cached_property
    def shared_query_params(self) -> shared_query_params.SharedQueryParamsResourceWithStreamingResponse:
        from .resources.shared_query_params import SharedQueryParamsResourceWithStreamingResponse

        return SharedQueryParamsResourceWithStreamingResponse(self._client.shared_query_params)

    @cached_property
    def model_referenced_in_parent_and_child(
        self,
    ) -> model_referenced_in_parent_and_child.ModelReferencedInParentAndChildResourceWithStreamingResponse:
        from .resources.model_referenced_in_parent_and_child import (
            ModelReferencedInParentAndChildResourceWithStreamingResponse,
        )

        return ModelReferencedInParentAndChildResourceWithStreamingResponse(
            self._client.model_referenced_in_parent_and_child
        )


class AsyncSinkWithStreamedResponse:
    _client: AsyncSink

    def __init__(self, client: AsyncSink) -> None:
        self._client = client

        self.api_status = async_to_streamed_response_wrapper(
            client.api_status,
        )
        self.api_status_alias = async_to_streamed_response_wrapper(
            client.api_status_alias,
        )
        self.create_no_response = async_to_streamed_response_wrapper(
            client.create_no_response,
        )

    @cached_property
    def testing(self) -> testing.AsyncTestingResourceWithStreamingResponse:
        from .resources.testing import AsyncTestingResourceWithStreamingResponse

        return AsyncTestingResourceWithStreamingResponse(self._client.testing)

    @cached_property
    def complex_queries(self) -> complex_queries.AsyncComplexQueriesResourceWithStreamingResponse:
        from .resources.complex_queries import AsyncComplexQueriesResourceWithStreamingResponse

        return AsyncComplexQueriesResourceWithStreamingResponse(self._client.complex_queries)

    @cached_property
    def casing(self) -> casing.AsyncCasingResourceWithStreamingResponse:
        from .resources.casing import AsyncCasingResourceWithStreamingResponse

        return AsyncCasingResourceWithStreamingResponse(self._client.casing)

    @cached_property
    def default_req_options(self) -> default_req_options.AsyncDefaultReqOptionsResourceWithStreamingResponse:
        from .resources.default_req_options import AsyncDefaultReqOptionsResourceWithStreamingResponse

        return AsyncDefaultReqOptionsResourceWithStreamingResponse(self._client.default_req_options)

    @cached_property
    def tools(self) -> tools.AsyncToolsResourceWithStreamingResponse:
        from .resources.tools import AsyncToolsResourceWithStreamingResponse

        return AsyncToolsResourceWithStreamingResponse(self._client.tools)

    @cached_property
    def undocumented_resource(self) -> undocumented_resource.AsyncUndocumentedResourceResourceWithStreamingResponse:
        from .resources.undocumented_resource import AsyncUndocumentedResourceResourceWithStreamingResponse

        return AsyncUndocumentedResourceResourceWithStreamingResponse(self._client.undocumented_resource)

    @cached_property
    def method_config(self) -> method_config.AsyncMethodConfigResourceWithStreamingResponse:
        from .resources.method_config import AsyncMethodConfigResourceWithStreamingResponse

        return AsyncMethodConfigResourceWithStreamingResponse(self._client.method_config)

    @cached_property
    def streaming(self) -> streaming.AsyncStreamingResourceWithStreamingResponse:
        from .resources.streaming import AsyncStreamingResourceWithStreamingResponse

        return AsyncStreamingResourceWithStreamingResponse(self._client.streaming)

    @cached_property
    def pagination_tests(self) -> pagination_tests.AsyncPaginationTestsResourceWithStreamingResponse:
        from .resources.pagination_tests import AsyncPaginationTestsResourceWithStreamingResponse

        return AsyncPaginationTestsResourceWithStreamingResponse(self._client.pagination_tests)

    @cached_property
    def docstrings(self) -> docstrings.AsyncDocstringsResourceWithStreamingResponse:
        from .resources.docstrings import AsyncDocstringsResourceWithStreamingResponse

        return AsyncDocstringsResourceWithStreamingResponse(self._client.docstrings)

    @cached_property
    def invalid_schemas(self) -> invalid_schemas.AsyncInvalidSchemasResourceWithStreamingResponse:
        from .resources.invalid_schemas import AsyncInvalidSchemasResourceWithStreamingResponse

        return AsyncInvalidSchemasResourceWithStreamingResponse(self._client.invalid_schemas)

    @cached_property
    def resource_refs(self) -> resource_refs.AsyncResourceRefsResourceWithStreamingResponse:
        from .resources.resource_refs import AsyncResourceRefsResourceWithStreamingResponse

        return AsyncResourceRefsResourceWithStreamingResponse(self._client.resource_refs)

    @cached_property
    def cards(self) -> cards.AsyncCardsResourceWithStreamingResponse:
        from .resources.cards import AsyncCardsResourceWithStreamingResponse

        return AsyncCardsResourceWithStreamingResponse(self._client.cards)

    @cached_property
    def files(self) -> files.AsyncFilesResourceWithStreamingResponse:
        from .resources.files import AsyncFilesResourceWithStreamingResponse

        return AsyncFilesResourceWithStreamingResponse(self._client.files)

    @cached_property
    def binaries(self) -> binaries.AsyncBinariesResourceWithStreamingResponse:
        from .resources.binaries import AsyncBinariesResourceWithStreamingResponse

        return AsyncBinariesResourceWithStreamingResponse(self._client.binaries)

    @cached_property
    def resources(self) -> resources.AsyncResourcesResourceWithStreamingResponse:
        from .resources.resources import AsyncResourcesResourceWithStreamingResponse

        return AsyncResourcesResourceWithStreamingResponse(self._client.resources)

    @cached_property
    def config_tools(self) -> config_tools.AsyncConfigToolsResourceWithStreamingResponse:
        from .resources.config_tools import AsyncConfigToolsResourceWithStreamingResponse

        return AsyncConfigToolsResourceWithStreamingResponse(self._client.config_tools)

    @cached_property
    def company(self) -> company.AsyncCompanyResourceWithStreamingResponse:
        """Stainless API company"""
        from .resources.company import AsyncCompanyResourceWithStreamingResponse

        return AsyncCompanyResourceWithStreamingResponse(self._client.company)

    @cached_property
    def openapi_formats(self) -> openapi_formats.AsyncOpenAPIFormatsResourceWithStreamingResponse:
        from .resources.openapi_formats import AsyncOpenAPIFormatsResourceWithStreamingResponse

        return AsyncOpenAPIFormatsResourceWithStreamingResponse(self._client.openapi_formats)

    @cached_property
    def parent(self) -> parent.AsyncParentResourceWithStreamingResponse:
        from .resources.parent import AsyncParentResourceWithStreamingResponse

        return AsyncParentResourceWithStreamingResponse(self._client.parent)

    @cached_property
    def envelopes(self) -> envelopes.AsyncEnvelopesResourceWithStreamingResponse:
        from .resources.envelopes import AsyncEnvelopesResourceWithStreamingResponse

        return AsyncEnvelopesResourceWithStreamingResponse(self._client.envelopes)

    @cached_property
    def types(self) -> types.AsyncTypesResourceWithStreamingResponse:
        from .resources.types import AsyncTypesResourceWithStreamingResponse

        return AsyncTypesResourceWithStreamingResponse(self._client.types)

    @cached_property
    def clients(self) -> clients.AsyncClientsResourceWithStreamingResponse:
        from .resources.clients import AsyncClientsResourceWithStreamingResponse

        return AsyncClientsResourceWithStreamingResponse(self._client.clients)

    @cached_property
    def names(self) -> names.AsyncNamesResourceWithStreamingResponse:
        from .resources.names import AsyncNamesResourceWithStreamingResponse

        return AsyncNamesResourceWithStreamingResponse(self._client.names)

    @cached_property
    def widgets(self) -> widgets.AsyncWidgetsResourceWithStreamingResponse:
        """
        Widget is love
        Widget is life
        """
        from .resources.widgets import AsyncWidgetsResourceWithStreamingResponse

        return AsyncWidgetsResourceWithStreamingResponse(self._client.widgets)

    @cached_property
    def client_params(self) -> client_params.AsyncClientParamsResourceWithStreamingResponse:
        from .resources.client_params import AsyncClientParamsResourceWithStreamingResponse

        return AsyncClientParamsResourceWithStreamingResponse(self._client.client_params)

    @cached_property
    def responses(self) -> responses.AsyncResponsesResourceWithStreamingResponse:
        from .resources.responses import AsyncResponsesResourceWithStreamingResponse

        return AsyncResponsesResourceWithStreamingResponse(self._client.responses)

    @cached_property
    def path_params(self) -> path_params.AsyncPathParamsResourceWithStreamingResponse:
        from .resources.path_params import AsyncPathParamsResourceWithStreamingResponse

        return AsyncPathParamsResourceWithStreamingResponse(self._client.path_params)

    @cached_property
    def positional_params(self) -> positional_params.AsyncPositionalParamsResourceWithStreamingResponse:
        from .resources.positional_params import AsyncPositionalParamsResourceWithStreamingResponse

        return AsyncPositionalParamsResourceWithStreamingResponse(self._client.positional_params)

    @cached_property
    def empty_body(self) -> empty_body.AsyncEmptyBodyResourceWithStreamingResponse:
        from .resources.empty_body import AsyncEmptyBodyResourceWithStreamingResponse

        return AsyncEmptyBodyResourceWithStreamingResponse(self._client.empty_body)

    @cached_property
    def query_params(self) -> query_params.AsyncQueryParamsResourceWithStreamingResponse:
        from .resources.query_params import AsyncQueryParamsResourceWithStreamingResponse

        return AsyncQueryParamsResourceWithStreamingResponse(self._client.query_params)

    @cached_property
    def body_params(self) -> body_params.AsyncBodyParamsResourceWithStreamingResponse:
        from .resources.body_params import AsyncBodyParamsResourceWithStreamingResponse

        return AsyncBodyParamsResourceWithStreamingResponse(self._client.body_params)

    @cached_property
    def header_params(self) -> header_params.AsyncHeaderParamsResourceWithStreamingResponse:
        from .resources.header_params import AsyncHeaderParamsResourceWithStreamingResponse

        return AsyncHeaderParamsResourceWithStreamingResponse(self._client.header_params)

    @cached_property
    def mixed_params(self) -> mixed_params.AsyncMixedParamsResourceWithStreamingResponse:
        from .resources.mixed_params import AsyncMixedParamsResourceWithStreamingResponse

        return AsyncMixedParamsResourceWithStreamingResponse(self._client.mixed_params)

    @cached_property
    def make_ambiguous_schemas_looser(
        self,
    ) -> make_ambiguous_schemas_looser.AsyncMakeAmbiguousSchemasLooserResourceWithStreamingResponse:
        from .resources.make_ambiguous_schemas_looser import (
            AsyncMakeAmbiguousSchemasLooserResourceWithStreamingResponse,
        )

        return AsyncMakeAmbiguousSchemasLooserResourceWithStreamingResponse(self._client.make_ambiguous_schemas_looser)

    @cached_property
    def make_ambiguous_schemas_explicit(
        self,
    ) -> make_ambiguous_schemas_explicit.AsyncMakeAmbiguousSchemasExplicitResourceWithStreamingResponse:
        from .resources.make_ambiguous_schemas_explicit import (
            AsyncMakeAmbiguousSchemasExplicitResourceWithStreamingResponse,
        )

        return AsyncMakeAmbiguousSchemasExplicitResourceWithStreamingResponse(
            self._client.make_ambiguous_schemas_explicit
        )

    @cached_property
    def decorator_tests(self) -> decorator_tests.AsyncDecoratorTestsResourceWithStreamingResponse:
        from .resources.decorator_tests import AsyncDecoratorTestsResourceWithStreamingResponse

        return AsyncDecoratorTestsResourceWithStreamingResponse(self._client.decorator_tests)

    @cached_property
    def tests(self) -> tests.AsyncTestsResourceWithStreamingResponse:
        from .resources.tests import AsyncTestsResourceWithStreamingResponse

        return AsyncTestsResourceWithStreamingResponse(self._client.tests)

    @cached_property
    def deeply_nested(self) -> deeply_nested.AsyncDeeplyNestedResourceWithStreamingResponse:
        from .resources.deeply_nested import AsyncDeeplyNestedResourceWithStreamingResponse

        return AsyncDeeplyNestedResourceWithStreamingResponse(self._client.deeply_nested)

    @cached_property
    def version_1_30_names(self) -> version_1_30_names.AsyncVersion1_30NamesResourceWithStreamingResponse:
        from .resources.version_1_30_names import AsyncVersion1_30NamesResourceWithStreamingResponse

        return AsyncVersion1_30NamesResourceWithStreamingResponse(self._client.version_1_30_names)

    @cached_property
    def recursion(self) -> recursion.AsyncRecursionResourceWithStreamingResponse:
        from .resources.recursion import AsyncRecursionResourceWithStreamingResponse

        return AsyncRecursionResourceWithStreamingResponse(self._client.recursion)

    @cached_property
    def shared_query_params(self) -> shared_query_params.AsyncSharedQueryParamsResourceWithStreamingResponse:
        from .resources.shared_query_params import AsyncSharedQueryParamsResourceWithStreamingResponse

        return AsyncSharedQueryParamsResourceWithStreamingResponse(self._client.shared_query_params)

    @cached_property
    def model_referenced_in_parent_and_child(
        self,
    ) -> model_referenced_in_parent_and_child.AsyncModelReferencedInParentAndChildResourceWithStreamingResponse:
        from .resources.model_referenced_in_parent_and_child import (
            AsyncModelReferencedInParentAndChildResourceWithStreamingResponse,
        )

        return AsyncModelReferencedInParentAndChildResourceWithStreamingResponse(
            self._client.model_referenced_in_parent_and_child
        )


Client = Sink

AsyncClient = AsyncSink
