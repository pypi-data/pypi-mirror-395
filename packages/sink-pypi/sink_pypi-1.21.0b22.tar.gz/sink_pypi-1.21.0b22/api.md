# Shared Types

```python
from sink.api.sdk.types import (
    BasicSharedModelObject,
    Currency,
    ErrorData,
    ObjectWithChildRef,
    PageCursorSharedRefPagination,
    SharedCursorNestedResponsePropMeta,
    SharedSelfRecursion,
    ShippingAddress,
    SimpleObject,
    SimpleObjectAlias,
)
```

# Sink

Types:

```python
from sink.api.sdk.types import APIStatus, CustomAPIStatusMessage, APIStatusAlias
```

Methods:

- <code title="get /status">client.<a href="./src/sink/api/sdk/_client.py">api_status</a>() -> <a href="./src/sink/api/sdk/types/api_status.py">APIStatus</a></code>
- <code title="post /no_response">client.<a href="./src/sink/api/sdk/_client.py">create_no_response</a>() -> None</code>

# Testing

Types:

```python
from sink.api.sdk.types import RootResponse
```

Methods:

- <code title="get /">client.testing.<a href="./src/sink/api/sdk/resources/testing.py">root</a>() -> <a href="./src/sink/api/sdk/types/root_response.py">RootResponse</a></code>

# ComplexQueries

Types:

```python
from sink.api.sdk.types import (
    ComplexQueryArrayQueryResponse,
    ComplexQueryObjectQueryResponse,
    ComplexQueryUnionQueryResponse,
)
```

Methods:

- <code title="get /array_query">client.complex_queries.<a href="./src/sink/api/sdk/resources/complex_queries.py">array_query</a>(\*\*<a href="src/sink/api/sdk/types/complex_query_array_query_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/complex_query_array_query_response.py">ComplexQueryArrayQueryResponse</a></code>
- <code title="get /object_query">client.complex_queries.<a href="./src/sink/api/sdk/resources/complex_queries.py">object_query</a>(\*\*<a href="src/sink/api/sdk/types/complex_query_object_query_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/complex_query_object_query_response.py">ComplexQueryObjectQueryResponse</a></code>
- <code title="get /union_query">client.complex_queries.<a href="./src/sink/api/sdk/resources/complex_queries.py">union_query</a>(\*\*<a href="src/sink/api/sdk/types/complex_query_union_query_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/complex_query_union_query_response.py">ComplexQueryUnionQueryResponse</a></code>

# Casing

## EEOC

Types:

```python
from sink.api.sdk.types.casing import EEOC
```

Methods:

- <code title="get /casing/eeoc">client.casing.eeoc.<a href="./src/sink/api/sdk/resources/casing/eeoc.py">list</a>(\*\*<a href="src/sink/api/sdk/types/casing/eeoc_list_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/casing/eeoc.py">SyncPageCursor[EEOC]</a></code>

# DefaultReqOptions

Methods:

- <code title="get /default_req_options">client.default_req_options.<a href="./src/sink/api/sdk/resources/default_req_options/default_req_options.py">example_method</a>() -> <a href="./src/sink/api/sdk/types/shared/basic_shared_model_object.py">BasicSharedModelObject</a></code>
- <code title="get /default_req_options/with_param_override">client.default_req_options.<a href="./src/sink/api/sdk/resources/default_req_options/default_req_options.py">with_param_override</a>() -> <a href="./src/sink/api/sdk/types/shared/basic_shared_model_object.py">BasicSharedModelObject</a></code>

## Child

Methods:

- <code title="get /default_req_options">client.default_req_options.child.<a href="./src/sink/api/sdk/resources/default_req_options/child.py">example_method</a>() -> <a href="./src/sink/api/sdk/types/shared/basic_shared_model_object.py">BasicSharedModelObject</a></code>

# Tools

Types:

```python
from sink.api.sdk.types import ObjectSkippedProps
```

Methods:

- <code title="post /tools/skipped_params">client.tools.<a href="./src/sink/api/sdk/resources/tools.py">skipped_params</a>(\*\*<a href="src/sink/api/sdk/types/tool_skipped_params_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/object_skipped_props.py">ObjectSkippedProps</a></code>

# MethodConfig

Types:

```python
from sink.api.sdk.types import (
    MethodConfigSkippedTestsAllResponse,
    MethodConfigSkippedTestsGoResponse,
    MethodConfigSkippedTestsJavaResponse,
    MethodConfigSkippedTestsKotlinResponse,
    MethodConfigSkippedTestsNodeResponse,
    MethodConfigSkippedTestsNodeAndPythonResponse,
    MethodConfigSkippedTestsPythonResponse,
    MethodConfigSkippedTestsRubyResponse,
)
```

Methods:

- <code title="get /method_config/skipped_tests/{id}">client.method_config.<a href="./src/sink/api/sdk/resources/method_config.py">skipped_tests_all</a>(id) -> <a href="./src/sink/api/sdk/types/method_config_skipped_tests_all_response.py">MethodConfigSkippedTestsAllResponse</a></code>
- <code title="get /method_config/skipped_tests/{id}">client.method_config.<a href="./src/sink/api/sdk/resources/method_config.py">skipped_tests_go</a>(id) -> <a href="./src/sink/api/sdk/types/method_config_skipped_tests_go_response.py">MethodConfigSkippedTestsGoResponse</a></code>
- <code title="get /method_config/skipped_tests/{id}">client.method_config.<a href="./src/sink/api/sdk/resources/method_config.py">skipped_tests_java</a>(id) -> <a href="./src/sink/api/sdk/types/method_config_skipped_tests_java_response.py">MethodConfigSkippedTestsJavaResponse</a></code>
- <code title="get /method_config/skipped_tests/{id}">client.method_config.<a href="./src/sink/api/sdk/resources/method_config.py">skipped_tests_kotlin</a>(id) -> <a href="./src/sink/api/sdk/types/method_config_skipped_tests_kotlin_response.py">MethodConfigSkippedTestsKotlinResponse</a></code>
- <code title="get /method_config/skipped_tests/{id}">client.method_config.<a href="./src/sink/api/sdk/resources/method_config.py">skipped_tests_node</a>(id) -> <a href="./src/sink/api/sdk/types/method_config_skipped_tests_node_response.py">MethodConfigSkippedTestsNodeResponse</a></code>
- <code title="get /method_config/skipped_tests/{id}">client.method_config.<a href="./src/sink/api/sdk/resources/method_config.py">skipped_tests_node_and_python</a>(id) -> <a href="./src/sink/api/sdk/types/method_config_skipped_tests_node_and_python_response.py">MethodConfigSkippedTestsNodeAndPythonResponse</a></code>
- <code title="get /method_config/skipped_tests/{id}">client.method_config.<a href="./src/sink/api/sdk/resources/method_config.py">skipped_tests_python</a>(id) -> <a href="./src/sink/api/sdk/types/method_config_skipped_tests_python_response.py">MethodConfigSkippedTestsPythonResponse</a></code>
- <code title="get /method_config/skipped_tests/{id}">client.method_config.<a href="./src/sink/api/sdk/resources/method_config.py">skipped_tests_ruby</a>(id) -> <a href="./src/sink/api/sdk/types/method_config_skipped_tests_ruby_response.py">MethodConfigSkippedTestsRubyResponse</a></code>

# Streaming

Types:

```python
from sink.api.sdk.types import (
    StreamingBasicResponse,
    StreamingNestedParamsResponse,
    StreamingNoDiscriminatorResponse,
    StreamingQueryParamDiscriminatorResponse,
    StreamingWithUnrelatedDefaultParamResponse,
)
```

Methods:

- <code title="post /streaming/basic">client.streaming.<a href="./src/sink/api/sdk/resources/streaming.py">basic</a>(\*\*<a href="src/sink/api/sdk/types/streaming_basic_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/streaming_basic_response.py">StreamingBasicResponse</a></code>
- <code title="post /streaming/nested_params">client.streaming.<a href="./src/sink/api/sdk/resources/streaming.py">nested_params</a>(\*\*<a href="src/sink/api/sdk/types/streaming_nested_params_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/streaming_nested_params_response.py">StreamingNestedParamsResponse</a></code>
- <code title="post /streaming/no_discriminator">client.streaming.<a href="./src/sink/api/sdk/resources/streaming.py">no_discriminator</a>(\*\*<a href="src/sink/api/sdk/types/streaming_no_discriminator_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/streaming_no_discriminator_response.py">StreamingNoDiscriminatorResponse</a></code>
- <code title="get /streaming/query_param_discriminator">client.streaming.<a href="./src/sink/api/sdk/resources/streaming.py">query_param_discriminator</a>(\*\*<a href="src/sink/api/sdk/types/streaming_query_param_discriminator_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/streaming_query_param_discriminator_response.py">StreamingQueryParamDiscriminatorResponse</a></code>
- <code title="post /streaming/with_unrelated_default_param">client.streaming.<a href="./src/sink/api/sdk/resources/streaming.py">with_unrelated_default_param</a>(\*\*<a href="src/sink/api/sdk/types/streaming_with_unrelated_default_param_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/streaming_with_unrelated_default_param_response.py">StreamingWithUnrelatedDefaultParamResponse</a></code>

# PaginationTests

## SchemaTypes

Methods:

- <code title="get /paginated/schema_types/allofs">client.pagination_tests.schema_types.<a href="./src/sink/api/sdk/resources/pagination_tests/schema_types.py">allofs</a>(\*\*<a href="src/sink/api/sdk/types/pagination_tests/schema_type_allofs_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/my_model.py">SyncPageCursor[MyModel]</a></code>
- <code title="get /paginated/schema_types/unions">client.pagination_tests.schema_types.<a href="./src/sink/api/sdk/resources/pagination_tests/schema_types.py">unions</a>(\*\*<a href="src/sink/api/sdk/types/pagination_tests/schema_type_unions_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/my_model.py">SyncPageCursor[MyModel]</a></code>

## ItemsTypes

Methods:

- <code title="get /paginated/items_types/unknown">client.pagination_tests.items_types.<a href="./src/sink/api/sdk/resources/pagination_tests/items_types.py">list_unknown</a>(\*\*<a href="src/sink/api/sdk/types/pagination_tests/items_type_list_unknown_params.py">params</a>) -> SyncPagePageNumber[object]</code>

## PageNumber

Methods:

- <code title="get /paginated/page_number">client.pagination_tests.page_number.<a href="./src/sink/api/sdk/resources/pagination_tests/page_number.py">list</a>(\*\*<a href="src/sink/api/sdk/types/pagination_tests/page_number_list_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/my_model.py">SyncPagePageNumber[MyModel]</a></code>
- <code title="get /paginated/page_number">client.pagination_tests.page_number.<a href="./src/sink/api/sdk/resources/pagination_tests/page_number.py">list_without_current_page_response</a>(\*\*<a href="src/sink/api/sdk/types/pagination_tests/page_number_list_without_current_page_response_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/my_model.py">SyncPagePageNumber[MyModel]</a></code>

## PageNumberWithoutCurrentPageResponse

Methods:

- <code title="get /paginated/page_number">client.pagination_tests.page_number_without_current_page_response.<a href="./src/sink/api/sdk/resources/pagination_tests/page_number_without_current_page_response.py">list</a>(\*\*<a href="src/sink/api/sdk/types/pagination_tests/page_number_without_current_page_response_list_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/my_model.py">SyncPagePageNumber[MyModel]</a></code>
- <code title="get /paginated/page_number_without_current_page_response">client.pagination_tests.page_number_without_current_page_response.<a href="./src/sink/api/sdk/resources/pagination_tests/page_number_without_current_page_response.py">list_without_current_page_response</a>(\*\*<a href="src/sink/api/sdk/types/pagination_tests/page_number_without_current_page_response_list_without_current_page_response_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/my_model.py">SyncPagePageNumberWithoutCurrentPageResponse[MyModel]</a></code>

## Refs

Methods:

- <code title="get /paginated/nested_object_ref">client.pagination_tests.refs.<a href="./src/sink/api/sdk/resources/pagination_tests/refs.py">nested_object_ref</a>(\*\*<a href="src/sink/api/sdk/types/pagination_tests/ref_nested_object_ref_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/my_model.py">SyncPageCursorNestedObjectRef[MyModel]</a></code>
- <code title="get /paginated/with_shared_model_ref">client.pagination_tests.refs.<a href="./src/sink/api/sdk/resources/pagination_tests/refs.py">with_shared_model_ref</a>(\*\*<a href="src/sink/api/sdk/types/pagination_tests/ref_with_shared_model_ref_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/my_model.py">SyncPageCursorSharedRef[MyModel]</a></code>

## ResponseHeaders

Methods:

- <code title="get /paginated/response_headers/basic_cursor">client.pagination_tests.response_headers.<a href="./src/sink/api/sdk/resources/pagination_tests/response_headers.py">basic_cursor</a>(\*\*<a href="src/sink/api/sdk/types/pagination_tests/response_header_basic_cursor_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/my_model.py">SyncPageCursorFromHeaders[MyModel]</a></code>

## TopLevelArrays

Methods:

- <code title="get /paginated/top_level_arrays/basic_cursor">client.pagination_tests.top_level_arrays.<a href="./src/sink/api/sdk/resources/pagination_tests/top_level_arrays.py">basic_cursor</a>(\*\*<a href="src/sink/api/sdk/types/pagination_tests/top_level_array_basic_cursor_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/my_model.py">SyncPageCursorTopLevelArray[MyModel]</a></code>

## Cursor

Methods:

- <code title="get /paginated/cursor">client.pagination_tests.cursor.<a href="./src/sink/api/sdk/resources/pagination_tests/cursor.py">list</a>(\*\*<a href="src/sink/api/sdk/types/pagination_tests/cursor_list_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/my_model.py">SyncPageCursor[MyModel]</a></code>
- <code title="get /paginated/cursor_with_has_more">client.pagination_tests.cursor.<a href="./src/sink/api/sdk/resources/pagination_tests/cursor.py">list_has_more</a>(\*\*<a href="src/sink/api/sdk/types/pagination_tests/cursor_list_has_more_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/my_model.py">SyncPageCursorWithHasMore[MyModel]</a></code>
- <code title="get /paginated/cursor_with_nested_has_more">client.pagination_tests.cursor.<a href="./src/sink/api/sdk/resources/pagination_tests/cursor.py">list_nested_has_more</a>(\*\*<a href="src/sink/api/sdk/types/pagination_tests/cursor_list_nested_has_more_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/my_model.py">SyncPageCursorWithNestedHasMore[MyModel]</a></code>
- <code title="get /paginated/cursor_with_reverse">client.pagination_tests.cursor.<a href="./src/sink/api/sdk/resources/pagination_tests/cursor.py">list_reverse</a>(\*\*<a href="src/sink/api/sdk/types/pagination_tests/cursor_list_reverse_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/my_model.py">SyncPageCursorWithReverse[MyModel]</a></code>

## CursorID

Methods:

- <code title="get /paginated/cursor_id">client.pagination_tests.cursor_id.<a href="./src/sink/api/sdk/resources/pagination_tests/cursor_id.py">list</a>(\*\*<a href="src/sink/api/sdk/types/pagination_tests/cursor_id_list_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/my_model.py">SyncPageCursorID[MyModel]</a></code>

## Offset

Methods:

- <code title="get /paginated/offset">client.pagination_tests.offset.<a href="./src/sink/api/sdk/resources/pagination_tests/offset.py">list</a>(\*\*<a href="src/sink/api/sdk/types/pagination_tests/offset_list_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/my_model.py">SyncPageOffset[MyModel]</a></code>
- <code title="get /paginated/offset/no_start_field">client.pagination_tests.offset.<a href="./src/sink/api/sdk/resources/pagination_tests/offset.py">list_no_start_field</a>(\*\*<a href="src/sink/api/sdk/types/pagination_tests/offset_list_no_start_field_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/my_model.py">SyncPageOffsetNoStartField[MyModel]</a></code>
- <code title="get /paginated/offset/with_total_count">client.pagination_tests.offset.<a href="./src/sink/api/sdk/resources/pagination_tests/offset.py">with_total_count</a>(\*\*<a href="src/sink/api/sdk/types/pagination_tests/offset_with_total_count_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/my_model.py">SyncPageOffsetTotalCount[MyModel]</a></code>

## FakePages

Methods:

- <code title="get /paginated/fake_page">client.pagination_tests.fake_pages.<a href="./src/sink/api/sdk/resources/pagination_tests/fake_pages.py">list</a>(\*\*<a href="src/sink/api/sdk/types/pagination_tests/fake_page_list_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/shared/simple_object.py">SyncFakePage[SimpleObject]</a></code>

## NestedItems

Methods:

- <code title="get /paginated/nested_items">client.pagination_tests.nested_items.<a href="./src/sink/api/sdk/resources/pagination_tests/nested_items.py">list</a>(\*\*<a href="src/sink/api/sdk/types/pagination_tests/nested_item_list_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/my_model.py">SyncPageCursorNestedItems[MyModel]</a></code>

# Docstrings

Types:

```python
from sink.api.sdk.types import (
    DocstringLeadingDoubleQuoteResponse,
    DocstringTrailingDoubleQuoteResponse,
)
```

Methods:

- <code title="get /docstrings/description_contains_comments">client.docstrings.<a href="./src/sink/api/sdk/resources/docstrings.py">description_contains_js_doc</a>() -> <a href="./src/sink/api/sdk/types/shared/basic_shared_model_object.py">BasicSharedModelObject</a></code>
- <code title="get /docstrings/description_contains_comment_enders">client.docstrings.<a href="./src/sink/api/sdk/resources/docstrings.py">description_contains_js_doc_end</a>() -> <a href="./src/sink/api/sdk/types/shared/basic_shared_model_object.py">BasicSharedModelObject</a></code>
- <code title="get /docstrings/property_leading_double_quote">client.docstrings.<a href="./src/sink/api/sdk/resources/docstrings.py">leading_double_quote</a>() -> <a href="./src/sink/api/sdk/types/docstring_leading_double_quote_response.py">DocstringLeadingDoubleQuoteResponse</a></code>
- <code title="get /docstrings/property_trailing_double_quote">client.docstrings.<a href="./src/sink/api/sdk/resources/docstrings.py">trailing_double_quote</a>() -> <a href="./src/sink/api/sdk/types/docstring_trailing_double_quote_response.py">DocstringTrailingDoubleQuoteResponse</a></code>

# InvalidSchemas

## Arrays

Types:

```python
from sink.api.sdk.types.invalid_schemas import ArrayMissingItemsResponse
```

Methods:

- <code title="get /invalid_schemas/arrays/missing_items">client.invalid_schemas.arrays.<a href="./src/sink/api/sdk/resources/invalid_schemas/arrays.py">missing_items</a>() -> <a href="./src/sink/api/sdk/types/invalid_schemas/array_missing_items_response.py">ArrayMissingItemsResponse</a></code>

## Objects

Methods:

- <code title="get /invalid_schemas/objects/property_missing_def">client.invalid_schemas.objects.<a href="./src/sink/api/sdk/resources/invalid_schemas/objects.py">missing_items</a>() -> object</code>

# ResourceRefs

## Parent

Types:

```python
from sink.api.sdk.types.resource_refs import ParentModelWithChildRef
```

Methods:

- <code title="get /resource_refs/parent_with_child_ref">client.resource_refs.parent.<a href="./src/sink/api/sdk/resources/resource_refs/parent/parent.py">returns_parent_model_with_child_ref</a>() -> <a href="./src/sink/api/sdk/types/resource_refs/parent_model_with_child_ref.py">ParentModelWithChildRef</a></code>

### Child

Types:

```python
from sink.api.sdk.types.resource_refs.parent import ChildModel
```

Methods:

- <code title="get /resource_refs/child">client.resource_refs.parent.child.<a href="./src/sink/api/sdk/resources/resource_refs/parent/child.py">returns_child_model</a>() -> <a href="./src/sink/api/sdk/types/resource_refs/parent/child_model.py">ChildModel</a></code>

## EscapedRef

Types:

```python
from sink.api.sdk.types.resource_refs import ModelWithEscapedName
```

Methods:

- <code title="get /resource_refs/escaped_ref">client.resource_refs.escaped_ref.<a href="./src/sink/api/sdk/resources/resource_refs/escaped_ref.py">get</a>() -> <a href="./src/sink/api/sdk/types/resource_refs/model_with_escaped_name.py">ModelWithEscapedName</a></code>

# Cards

Types:

```python
from sink.api.sdk.types import (
    Card,
    FundingAccount,
    CardListResponse,
    CardProvisionFooResponse,
    CardAlias,
    SharedObjectAlias,
)
```

Methods:

- <code title="post /cards">client.cards.<a href="./src/sink/api/sdk/resources/cards.py">create</a>(\*\*<a href="src/sink/api/sdk/types/card_create_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/card.py">Card</a></code>
- <code title="get /cards/{card_token}">client.cards.<a href="./src/sink/api/sdk/resources/cards.py">retrieve</a>(card_token) -> <a href="./src/sink/api/sdk/types/card.py">Card</a></code>
- <code title="patch /cards/{card_token}">client.cards.<a href="./src/sink/api/sdk/resources/cards.py">update</a>(card_token, \*\*<a href="src/sink/api/sdk/types/card_update_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/card.py">Card</a></code>
- <code title="get /cards">client.cards.<a href="./src/sink/api/sdk/resources/cards.py">list</a>(\*\*<a href="src/sink/api/sdk/types/card_list_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/card_list_response.py">CardListResponse</a></code>
- <code title="post /deprecations/method_all_but_go_diff_message">client.cards.<a href="./src/sink/api/sdk/resources/cards.py">deprecated_all_but_go_diff_message</a>() -> None</code>
- <code title="post /deprecations/method_all_but_go_diff_message">client.cards.<a href="./src/sink/api/sdk/resources/cards.py">deprecated_all_diff_message</a>() -> None</code>
- <code title="post /deprecations/method">client.cards.<a href="./src/sink/api/sdk/resources/cards.py">deprecated_method</a>() -> None</code>
- <code title="post /deprecations/method_only_go">client.cards.<a href="./src/sink/api/sdk/resources/cards.py">deprecated_only_go</a>() -> None</code>
- <code title="get /cards/{card_token}">client.cards.<a href="./src/sink/api/sdk/resources/cards.py">list_not_paginated</a>(card_token) -> <a href="./src/sink/api/sdk/types/card.py">Card</a></code>
- <code title="post /cards/{card_token}/provision">client.cards.<a href="./src/sink/api/sdk/resources/cards.py">provision_foo</a>(card_token, \*\*<a href="src/sink/api/sdk/types/card_provision_foo_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/card_provision_foo_response.py">CardProvisionFooResponse</a></code>
- <code title="post /cards/{card_token}/reissue">client.cards.<a href="./src/sink/api/sdk/resources/cards.py">reissue</a>(card_token, \*\*<a href="src/sink/api/sdk/types/card_reissue_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/card.py">Card</a></code>

# Files

Types:

```python
from sink.api.sdk.types import (
    FileCreateBase64Response,
    FileCreateMultipartResponse,
    FileEverythingMultipartResponse,
    FileNoFileMultipartResponse,
    FileWithOptionalParamResponse,
)
```

Methods:

- <code title="post /files/base64">client.files.<a href="./src/sink/api/sdk/resources/files.py">create_base64</a>(\*\*<a href="src/sink/api/sdk/types/file_create_base64_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/file_create_base64_response.py">FileCreateBase64Response</a></code>
- <code title="post /files/multipart">client.files.<a href="./src/sink/api/sdk/resources/files.py">create_multipart</a>(\*\*<a href="src/sink/api/sdk/types/file_create_multipart_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/file_create_multipart_response.py">FileCreateMultipartResponse</a></code>
- <code title="post /files/multipart_everything">client.files.<a href="./src/sink/api/sdk/resources/files.py">everything_multipart</a>(\*\*<a href="src/sink/api/sdk/types/file_everything_multipart_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/file_everything_multipart_response.py">FileEverythingMultipartResponse</a></code>
- <code title="post /files/no_file_multipart">client.files.<a href="./src/sink/api/sdk/resources/files.py">no_file_multipart</a>(\*\*<a href="src/sink/api/sdk/types/file_no_file_multipart_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/file_no_file_multipart_response.py">FileNoFileMultipartResponse</a></code>
- <code title="post /files/with_optional_param">client.files.<a href="./src/sink/api/sdk/resources/files.py">with_optional_param</a>(\*\*<a href="src/sink/api/sdk/types/file_with_optional_param_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/file_with_optional_param_response.py">FileWithOptionalParamResponse</a></code>

# Binaries

Methods:

- <code title="get /binaries/return_binary">client.binaries.<a href="./src/sink/api/sdk/resources/binaries.py">return_binary</a>() -> BinaryAPIResponse</code>
- <code title="post /binaries/with_path_and_body_param/{id}">client.binaries.<a href="./src/sink/api/sdk/resources/binaries.py">with_path_and_body_param</a>(id, \*\*<a href="src/sink/api/sdk/types/binary_with_path_and_body_param_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /binaries/with_path_param/{id}">client.binaries.<a href="./src/sink/api/sdk/resources/binaries.py">with_path_param</a>(id) -> BinaryAPIResponse</code>

# Resources

Methods:

- <code title="post /no_response">client.resources.<a href="./src/sink/api/sdk/resources/resources.py">foo</a>() -> None</code>

# ConfigTools

Types:

```python
from sink.api.sdk.types import (
    ModelFromNestedResponseBodyRef,
    ModelFromSchemasRef,
    ModelFromSchemasRefOpenAPIUri,
    ModelFromSchemasRefOpenAPIUriJmespath,
    ModelFromSchemasRefOpenAPIUriJsonpath,
    ConfigToolModelRefFromNestedResponseBodyResponse,
)
```

Methods:

- <code title="get /config_tools/model_refs/from_nested_response">client.config_tools.<a href="./src/sink/api/sdk/resources/config_tools.py">model_ref_from_nested_response_body</a>() -> <a href="./src/sink/api/sdk/types/config_tool_model_ref_from_nested_response_body_response.py">ConfigToolModelRefFromNestedResponseBodyResponse</a></code>
- <code title="get /config_tools/model_refs/from_schemas">client.config_tools.<a href="./src/sink/api/sdk/resources/config_tools.py">model_ref_from_schemas</a>() -> <a href="./src/sink/api/sdk/types/model_from_schemas_ref.py">ModelFromSchemasRef</a></code>

# Company

Types:

```python
from sink.api.sdk.types import Company
```

## Payments

Types:

```python
from sink.api.sdk.types.company import CompanyPayment
```

Methods:

- <code title="get /company/payments/{payment_id}">client.company.payments.<a href="./src/sink/api/sdk/resources/company/payments.py">retrieve</a>(payment_id) -> <a href="./src/sink/api/sdk/types/company/company_payment.py">CompanyPayment</a></code>

# OpenAPIFormats

Types:

```python
from sink.api.sdk.types import (
    OpenAPIFormatArrayTypeOneEntryResponse,
    OpenAPIFormatArrayTypeOneEntryWithNullResponse,
)
```

Methods:

- <code title="post /openapi_formats/array_type_one_entry">client.openapi_formats.<a href="./src/sink/api/sdk/resources/openapi_formats.py">array_type_one_entry</a>(\*\*<a href="src/sink/api/sdk/types/openapi_format_array_type_one_entry_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/openapi_format_array_type_one_entry_response.py">OpenAPIFormatArrayTypeOneEntryResponse</a></code>
- <code title="post /openapi_formats/array_type_one_entry_with_null">client.openapi_formats.<a href="./src/sink/api/sdk/resources/openapi_formats.py">array_type_one_entry_with_null</a>(\*\*<a href="src/sink/api/sdk/types/openapi_format_array_type_one_entry_with_null_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/openapi_format_array_type_one_entry_with_null_response.py">Optional[OpenAPIFormatArrayTypeOneEntryWithNullResponse]</a></code>

# Parent

## Child

Types:

```python
from sink.api.sdk.types.parent import ChildInlinedResponseResponse
```

Methods:

- <code title="get /inlined_response">client.parent.child.<a href="./src/sink/api/sdk/resources/parent/child.py">inlined_response</a>() -> <a href="./src/sink/api/sdk/types/parent/child_inlined_response_response.py">ChildInlinedResponseResponse</a></code>

# Envelopes

Types:

```python
from sink.api.sdk.types import Address, EnvelopeInlineResponseResponse, EnvelopeWrappedArrayResponse
```

Methods:

- <code title="get /envelopes/data">client.envelopes.<a href="./src/sink/api/sdk/resources/envelopes.py">explicit</a>() -> <a href="./src/sink/api/sdk/types/address.py">Address</a></code>
- <code title="get /envelopes/items">client.envelopes.<a href="./src/sink/api/sdk/resources/envelopes.py">implicit</a>() -> <a href="./src/sink/api/sdk/types/address.py">Address</a></code>
- <code title="get /envelopes/items/inline_response">client.envelopes.<a href="./src/sink/api/sdk/resources/envelopes.py">inline_response</a>() -> <a href="./src/sink/api/sdk/types/envelope_inline_response_response.py">EnvelopeInlineResponseResponse</a></code>
- <code title="get /envelopes/items/wrapped_array">client.envelopes.<a href="./src/sink/api/sdk/resources/envelopes.py">wrapped_array</a>() -> <a href="./src/sink/api/sdk/types/envelope_wrapped_array_response.py">EnvelopeWrappedArrayResponse</a></code>

# Types

Types:

```python
from sink.api.sdk.types import TypeDatesResponse, TypeDatetimesResponse
```

Methods:

- <code title="post /types/dates">client.types.<a href="./src/sink/api/sdk/resources/types/types.py">dates</a>(\*\*<a href="src/sink/api/sdk/types/type_dates_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/type_dates_response.py">TypeDatesResponse</a></code>
- <code title="post /types/datetimes">client.types.<a href="./src/sink/api/sdk/resources/types/types.py">datetimes</a>(\*\*<a href="src/sink/api/sdk/types/type_datetimes_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/type_datetimes_response.py">TypeDatetimesResponse</a></code>

## Primitives

Types:

```python
from sink.api.sdk.types.types import ModelString, PrimitiveStringsResponse
```

Methods:

- <code title="post /types/primitives/strings">client.types.primitives.<a href="./src/sink/api/sdk/resources/types/primitives.py">strings</a>(\*\*<a href="src/sink/api/sdk/types/types/primitive_strings_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/types/primitive_strings_response.py">PrimitiveStringsResponse</a></code>

## ReadOnlyParams

Types:

```python
from sink.api.sdk.types.types import ReadOnlyParamSimpleResponse
```

Methods:

- <code title="post /types/read_only_params/simple">client.types.read_only_params.<a href="./src/sink/api/sdk/resources/types/read_only_params.py">simple</a>(\*\*<a href="src/sink/api/sdk/types/types/read_only_param_simple_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/types/read_only_param_simple_response.py">ReadOnlyParamSimpleResponse</a></code>

## WriteOnlyResponses

Types:

```python
from sink.api.sdk.types.types import WriteOnlyResponseSimpleResponse
```

Methods:

- <code title="get /types/write_only_responses/simple">client.types.write_only_responses.<a href="./src/sink/api/sdk/resources/types/write_only_responses.py">simple</a>() -> <a href="./src/sink/api/sdk/types/types/write_only_response_simple_response.py">WriteOnlyResponseSimpleResponse</a></code>

## Maps

Types:

```python
from sink.api.sdk.types.types import MapUnknownItemsResponse
```

Methods:

- <code title="post /types/map/unknown_items">client.types.maps.<a href="./src/sink/api/sdk/resources/types/maps.py">unknown_items</a>(\*\*<a href="src/sink/api/sdk/types/types/map_unknown_items_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/types/map_unknown_items_response.py">MapUnknownItemsResponse</a></code>

## Enums

Types:

```python
from sink.api.sdk.types.types import EnumBasicResponse
```

Methods:

- <code title="post /types/enum_tests_array_unique_values">client.types.enums.<a href="./src/sink/api/sdk/resources/types/enums.py">array_unique_values</a>(\*\*<a href="src/sink/api/sdk/types/types/enum_array_unique_values_params.py">params</a>) -> None</code>
- <code title="post /types/enum_tests_array_unique_values_2_values">client.types.enums.<a href="./src/sink/api/sdk/resources/types/enums.py">array_unique_values_2_values</a>(\*\*<a href="src/sink/api/sdk/types/types/enum_array_unique_values_2_values_params.py">params</a>) -> None</code>
- <code title="post /types/enum_tests_array_unique_values_numbers">client.types.enums.<a href="./src/sink/api/sdk/resources/types/enums.py">array_unique_values_numbers</a>(\*\*<a href="src/sink/api/sdk/types/types/enum_array_unique_values_numbers_params.py">params</a>) -> None</code>
- <code title="post /types/enums">client.types.enums.<a href="./src/sink/api/sdk/resources/types/enums.py">basic</a>(\*\*<a href="src/sink/api/sdk/types/types/enum_basic_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/types/enum_basic_response.py">EnumBasicResponse</a></code>

## Allofs

Types:

```python
from sink.api.sdk.types.types import AllofBaseParent, AllofMultipleInlineEntries
```

## Unions

Types:

```python
from sink.api.sdk.types.types import (
    UnionDiscriminatedVariantA,
    UnionDiscriminatedVariantB,
    UnionArrayParamDiscriminatedByPropertyNameResponse,
    UnionArrayParamDiscriminatedWithBasicMappingResponse,
    UnionParamDiscriminatedByPropertyNameResponse,
    UnionParamDiscriminatedWithBasicMappingResponse,
    UnionResponseDiscriminatedByPropertyNameResponse,
    UnionResponseDiscriminatedWithBasicMappingResponse,
)
```

Methods:

- <code title="post /types/unions/array_param_discriminated_by_property_name">client.types.unions.<a href="./src/sink/api/sdk/resources/types/unions.py">array_param_discriminated_by_property_name</a>(\*\*<a href="src/sink/api/sdk/types/types/union_array_param_discriminated_by_property_name_params.py">params</a>) -> str</code>
- <code title="post /types/unions/array_param_discriminated_with_basic_mapping">client.types.unions.<a href="./src/sink/api/sdk/resources/types/unions.py">array_param_discriminated_with_basic_mapping</a>(\*\*<a href="src/sink/api/sdk/types/types/union_array_param_discriminated_with_basic_mapping_params.py">params</a>) -> str</code>
- <code title="post /types/unions/param_discriminated_by_property_name">client.types.unions.<a href="./src/sink/api/sdk/resources/types/unions.py">param_discriminated_by_property_name</a>(\*\*<a href="src/sink/api/sdk/types/types/union_param_discriminated_by_property_name_params.py">params</a>) -> str</code>
- <code title="post /types/unions/param_discriminated_with_basic_mapping">client.types.unions.<a href="./src/sink/api/sdk/resources/types/unions.py">param_discriminated_with_basic_mapping</a>(\*\*<a href="src/sink/api/sdk/types/types/union_param_discriminated_with_basic_mapping_params.py">params</a>) -> str</code>
- <code title="get /types/unions/response_discriminated_by_property_name">client.types.unions.<a href="./src/sink/api/sdk/resources/types/unions.py">response_discriminated_by_property_name</a>() -> <a href="./src/sink/api/sdk/types/types/union_response_discriminated_by_property_name_response.py">UnionResponseDiscriminatedByPropertyNameResponse</a></code>
- <code title="get /types/unions/response_discriminated_with_basic_mapping">client.types.unions.<a href="./src/sink/api/sdk/resources/types/unions.py">response_discriminated_with_basic_mapping</a>() -> <a href="./src/sink/api/sdk/types/types/union_response_discriminated_with_basic_mapping_response.py">UnionResponseDiscriminatedWithBasicMappingResponse</a></code>

## Objects

Types:

```python
from sink.api.sdk.types.types import (
    UnknownObjectType,
    ObjectMixedKnownAndUnknownResponse,
    ObjectMultipleArrayPropertiesSameRefResponse,
    ObjectMultiplePropertiesSameModelResponse,
    ObjectMultiplePropertiesSameRefResponse,
    ObjectTwoDimensionalArrayPrimitivePropertyResponse,
)
```

Methods:

- <code title="get /types/object/mixed_known_and_unknown">client.types.objects.<a href="./src/sink/api/sdk/resources/types/objects.py">mixed_known_and_unknown</a>() -> <a href="./src/sink/api/sdk/types/types/object_mixed_known_and_unknown_response.py">ObjectMixedKnownAndUnknownResponse</a></code>
- <code title="get /types/object/multiple_array_properties_same_ref">client.types.objects.<a href="./src/sink/api/sdk/resources/types/objects.py">multiple_array_properties_same_ref</a>() -> <a href="./src/sink/api/sdk/types/types/object_multiple_array_properties_same_ref_response.py">ObjectMultipleArrayPropertiesSameRefResponse</a></code>
- <code title="get /types/object/multiple_properties_same_model">client.types.objects.<a href="./src/sink/api/sdk/resources/types/objects.py">multiple_properties_same_model</a>() -> <a href="./src/sink/api/sdk/types/types/object_multiple_properties_same_model_response.py">ObjectMultiplePropertiesSameModelResponse</a></code>
- <code title="get /types/object/multiple_properties_same_ref">client.types.objects.<a href="./src/sink/api/sdk/resources/types/objects.py">multiple_properties_same_ref</a>() -> <a href="./src/sink/api/sdk/types/types/object_multiple_properties_same_ref_response.py">ObjectMultiplePropertiesSameRefResponse</a></code>
- <code title="get /types/object/2d_array_primitive_properties">client.types.objects.<a href="./src/sink/api/sdk/resources/types/objects.py">two_dimensional_array_primitive_property</a>() -> <a href="./src/sink/api/sdk/types/types/object_two_dimensional_array_primitive_property_response.py">ObjectTwoDimensionalArrayPrimitivePropertyResponse</a></code>
- <code title="get /types/object/unknown_object">client.types.objects.<a href="./src/sink/api/sdk/resources/types/objects.py">unknown_object</a>() -> <a href="./src/sink/api/sdk/types/types/unknown_object_type.py">object</a></code>

## Arrays

Types:

```python
from sink.api.sdk.types.types import (
    ArrayObjectItems,
    ArrayFloatItemsResponse,
    ArrayObjectItemsResponse,
)
```

Methods:

- <code title="get /types/array/float_items">client.types.arrays.<a href="./src/sink/api/sdk/resources/types/arrays.py">float_items</a>() -> <a href="./src/sink/api/sdk/types/types/array_float_items_response.py">ArrayFloatItemsResponse</a></code>
- <code title="post /types/array/model_nested_in_params">client.types.arrays.<a href="./src/sink/api/sdk/resources/types/arrays.py">nested_in_params</a>() -> None</code>
- <code title="get /types/array/object_items">client.types.arrays.<a href="./src/sink/api/sdk/resources/types/arrays.py">object_items</a>() -> <a href="./src/sink/api/sdk/types/types/array_object_items_response.py">ArrayObjectItemsResponse</a></code>

# Clients

Types:

```python
from sink.api.sdk.types import Client
```

Methods:

- <code title="post /clients">client.clients.<a href="./src/sink/api/sdk/resources/clients.py">create</a>(\*\*<a href="src/sink/api/sdk/types/client_create_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/client.py">Client</a></code>

# Names

Types:

```python
from sink.api.sdk.types import (
    Balance,
    NameChildPropImportClashResponse,
    NamePropertiesCommonConflictsResponse,
    NamePropertiesIllegalGoIdentifiersResponse,
    NamePropertiesIllegalJavascriptIdentifiersResponse,
    NameResponsePropertyClashesModelImportResponse,
    NameResponseShadowsPydanticResponse,
)
```

Methods:

- <code title="post /names/child_prop_import_clash">client.names.<a href="./src/sink/api/sdk/resources/names/names.py">child_prop_import_clash</a>() -> <a href="./src/sink/api/sdk/types/name_child_prop_import_clash_response.py">NameChildPropImportClashResponse</a></code>
- <code title="get /names/method_name_get">client.names.<a href="./src/sink/api/sdk/resources/names/names.py">get</a>() -> <a href="./src/sink/api/sdk/types/shared/basic_shared_model_object.py">BasicSharedModelObject</a></code>
- <code title="post /names/properties_common_conflicts">client.names.<a href="./src/sink/api/sdk/resources/names/names.py">properties_common_conflicts</a>(\*\*<a href="src/sink/api/sdk/types/name_properties_common_conflicts_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/name_properties_common_conflicts_response.py">NamePropertiesCommonConflictsResponse</a></code>
- <code title="post /names/properties_illegal_go_identifiers/{type}">client.names.<a href="./src/sink/api/sdk/resources/names/names.py">properties_illegal_go_identifiers</a>(type, \*\*<a href="src/sink/api/sdk/types/name_properties_illegal_go_identifiers_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/name_properties_illegal_go_identifiers_response.py">NamePropertiesIllegalGoIdentifiersResponse</a></code>
- <code title="post /names/properties_illegal_javascript_identifiers">client.names.<a href="./src/sink/api/sdk/resources/names/names.py">properties_illegal_javascript_identifiers</a>(\*\*<a href="src/sink/api/sdk/types/name_properties_illegal_javascript_identifiers_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/name_properties_illegal_javascript_identifiers_response.py">NamePropertiesIllegalJavascriptIdentifiersResponse</a></code>
- <code title="get /names/response_property_clashes_model_import">client.names.<a href="./src/sink/api/sdk/resources/names/names.py">response_property_clashes_model_import</a>() -> <a href="./src/sink/api/sdk/types/name_response_property_clashes_model_import_response.py">NameResponsePropertyClashesModelImportResponse</a></code>
- <code title="get /names/response_property_shadows_pydantic">client.names.<a href="./src/sink/api/sdk/resources/names/names.py">response_shadows_pydantic</a>() -> <a href="./src/sink/api/sdk/types/name_response_shadows_pydantic_response.py">NameResponseShadowsPydanticResponse</a></code>

## Unions

Types:

```python
from sink.api.sdk.types.names import DiscriminatedUnion, VariantsSinglePropObjects
```

Methods:

- <code title="get /names/unions/discriminated_union">client.names.unions.<a href="./src/sink/api/sdk/resources/names/unions.py">discriminated</a>() -> <a href="./src/sink/api/sdk/types/names/discriminated_union.py">DiscriminatedUnion</a></code>
- <code title="get /names/unions/variants_object_with_union_properties">client.names.unions.<a href="./src/sink/api/sdk/resources/names/unions.py">variants_object_with_union_properties</a>() -> <a href="./src/sink/api/sdk/types/object_with_union_properties.py">ObjectWithUnionProperties</a></code>
- <code title="get /names/unions/variants_single_prop_objects">client.names.unions.<a href="./src/sink/api/sdk/resources/names/unions.py">variants_single_prop_objects</a>() -> <a href="./src/sink/api/sdk/types/names/variants_single_prop_objects.py">VariantsSinglePropObjects</a></code>

## Renaming

Types:

```python
from sink.api.sdk.types.names import RenamingExplicitResponsePropertyResponse
```

Methods:

- <code title="get /names/renaming/explicit_response_property">client.names.renaming.<a href="./src/sink/api/sdk/resources/names/renaming.py">explicit_response_property</a>() -> <a href="./src/sink/api/sdk/types/names/renaming_explicit_response_property_response.py">RenamingExplicitResponsePropertyResponse</a></code>

## Documents

Types:

```python
from sink.api.sdk.types.names import Documents
```

Methods:

- <code title="post /names/model_import_clash_with_resource">client.names.documents.<a href="./src/sink/api/sdk/resources/names/documents.py">retrieve2</a>() -> <a href="./src/sink/api/sdk/types/names/documents.py">Documents</a></code>

## ReservedNames

Methods:

- <code title="post /names/reserved_names/common_reserved_params">client.names.reserved_names.<a href="./src/sink/api/sdk/resources/names/reserved_names/reserved_names.py">common_reserved_params</a>(\*\*<a href="src/sink/api/sdk/types/names/reserved_name_common_reserved_params_params.py">params</a>) -> None</code>

### Public

Types:

```python
from sink.api.sdk.types.names.reserved_names import Public
```

Methods:

- <code title="get /names/reserved_names/public">client.names.reserved_names.public.<a href="./src/sink/api/sdk/resources/names/reserved_names/public/public.py">public</a>() -> <a href="./src/sink/api/sdk/types/names/reserved_names/public/public.py">Public</a></code>

#### Private

Types:

```python
from sink.api.sdk.types.names.reserved_names.public import Private
```

Methods:

- <code title="get /names/reserved_names/public/private">client.names.reserved_names.public.private.<a href="./src/sink/api/sdk/resources/names/reserved_names/public/private.py">private</a>() -> <a href="./src/sink/api/sdk/types/names/reserved_names/public/private.py">Private</a></code>

#### Interface

Types:

```python
from sink.api.sdk.types.names.reserved_names.public import Interface
```

Methods:

- <code title="get /names/reserved_names/public/interface">client.names.reserved_names.public.interface.<a href="./src/sink/api/sdk/resources/names/reserved_names/public/interface.py">interface</a>() -> <a href="./src/sink/api/sdk/types/names/reserved_names/public/interface.py">Interface</a></code>

#### Class

Types:

```python
from sink.api.sdk.types.names.reserved_names.public import Class
```

Methods:

- <code title="get /names/reserved_names/public/class">client.names.reserved*names.public.class*.<a href="./src/sink/api/sdk/resources/names/reserved_names/public/class_.py">class*</a>() -> <a href="./src/sink/api/sdk/types/names/reserved_names/public/class*.py">Class</a></code>

### Import

Types:

```python
from sink.api.sdk.types.names.reserved_names import Import
```

Methods:

- <code title="get /names/reserved_names/import">client.names.reserved*names.import*.<a href="./src/sink/api/sdk/resources/names/reserved_names/import_.py">import*</a>() -> <a href="./src/sink/api/sdk/types/names/reserved_names/import*.py">Import</a></code>

### Methods

Types:

```python
from sink.api.sdk.types.names.reserved_names import Export, Return
```

Methods:

- <code title="post /names/reserved_names/methods/export/{class}">client.names.reserved*names.methods.<a href="./src/sink/api/sdk/resources/names/reserved_names/methods.py">export</a>(class*, \*\*<a href="src/sink/api/sdk/types/names/reserved_names/method_export_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/names/reserved_names/export.py">Export</a></code>

## Params

Methods:

- <code title="post /names/body_params/options">client.names.params.<a href="./src/sink/api/sdk/resources/names/params.py">options_param</a>(\*\*<a href="src/sink/api/sdk/types/names/param_options_param_params.py">params</a>) -> None</code>
- <code title="post /names/body_params/timeout">client.names.params.<a href="./src/sink/api/sdk/resources/names/params.py">timeout_param</a>(\*\*<a href="src/sink/api/sdk/types/names/param_timeout_param_params.py">params</a>) -> None</code>

## CanCauseClashes

### EmploymentData

Types:

```python
from sink.api.sdk.types.names.can_cause_clashes import EmploymentData
```

### Response

Methods:

- <code title="get /binaries/return_binary">client.names.can_cause_clashes.response.<a href="./src/sink/api/sdk/resources/names/can_cause_clashes/response.py">binary_return</a>() -> BinaryAPIResponse</code>

## OpenAPISpecials

Types:

```python
from sink.api.sdk.types.names import OpenAPISpecialUsedUsedAsPropertyNameResponse
```

Methods:

- <code title="get /names/openapi_specials/used_used_as_property_name">client.names.openapi_specials.<a href="./src/sink/api/sdk/resources/names/openapi_specials.py">used_used_as_property_name</a>() -> <a href="./src/sink/api/sdk/types/names/openapi_special_used_used_as_property_name_response.py">OpenAPISpecialUsedUsedAsPropertyNameResponse</a></code>

# Widgets

Types:

```python
from sink.api.sdk.types import Widget
```

Methods:

- <code title="get /widgets/{widgetId}/filter/{filterType}">client.widgets.<a href="./src/sink/api/sdk/resources/widgets.py">retrieve_with_filter</a>(filter_type, \*, widget_id) -> <a href="./src/sink/api/sdk/types/widget.py">Widget</a></code>

# Webhooks

Types:

```python
from sink.api.sdk.types import (
    CardCreatedWebhookEvent,
    CardReadyWebhookEvent,
    CardErroredWebhookEvent,
    CardUpdatedWebhookEvent,
    CardDeletedWebhookEvent,
    UnwrapWebhookEvent,
)
```

# ClientParams

Types:

```python
from sink.api.sdk.types import (
    ClientParamWithPathParamResponse,
    ClientParamWithPathParamAndStandardResponse,
    ClientParamWithQueryParamResponse,
)
```

Methods:

- <code title="post /client_params/path_params/{client_path_param}/{client_path_or_query_param}">client.client_params.<a href="./src/sink/api/sdk/resources/client_params.py">with_path_param</a>(\*, client_path_param, client_path_or_query_param) -> <a href="./src/sink/api/sdk/types/client_param_with_path_param_response.py">ClientParamWithPathParamResponse</a></code>
- <code title="post /client_params/path_params/{camelCasedPath}/{id}">client.client_params.<a href="./src/sink/api/sdk/resources/client_params.py">with_path_param_and_standard</a>(id, \*, camel_cased_path) -> <a href="./src/sink/api/sdk/types/client_param_with_path_param_and_standard_response.py">ClientParamWithPathParamAndStandardResponse</a></code>
- <code title="post /client_params/query_params">client.client_params.<a href="./src/sink/api/sdk/resources/client_params.py">with_query_param</a>(\*\*<a href="src/sink/api/sdk/types/client_param_with_query_param_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/client_param_with_query_param_response.py">ClientParamWithQueryParamResponse</a></code>

# Responses

Types:

```python
from sink.api.sdk.types import (
    ModelFromNestedPath,
    ModelWithNestedModel,
    ObjectWithAnyOfNullProperty,
    ObjectWithOneOfNullProperty,
    ObjectWithUnionProperties,
    ResponsesAllofCrossObject,
    SimpleAllof,
    UnknownObject,
    ResponseAdditionalPropertiesResponse,
    ResponseAdditionalPropertiesNestedModelReferenceResponse,
    ResponseAllofCrossResourceResponse,
    ResponseAllofSimpleResponse,
    ResponseArrayObjectWithUnionPropertiesResponse,
    ResponseArrayResponseResponse,
    ResponseMissingRequiredResponse,
    ResponseNestedArrayResponse,
    ResponseObjectAllPropertiesResponse,
    ResponseObjectNoPropertiesResponse,
    ResponseObjectWithAdditionalPropertiesPropResponse,
    ResponseOnlyReadOnlyPropertiesResponse,
    ResponseStringResponseResponse,
)
```

Methods:

- <code title="post /responses/additional_properties">client.responses.<a href="./src/sink/api/sdk/resources/responses/responses.py">additional_properties</a>() -> <a href="./src/sink/api/sdk/types/response_additional_properties_response.py">ResponseAdditionalPropertiesResponse</a></code>
- <code title="post /responses/additional_properties_nested_model_reference">client.responses.<a href="./src/sink/api/sdk/resources/responses/responses.py">additional_properties_nested_model_reference</a>() -> <a href="./src/sink/api/sdk/types/response_additional_properties_nested_model_reference_response.py">ResponseAdditionalPropertiesNestedModelReferenceResponse</a></code>
- <code title="get /responses/allof/cross">client.responses.<a href="./src/sink/api/sdk/resources/responses/responses.py">allof_cross_resource</a>() -> <a href="./src/sink/api/sdk/types/response_allof_cross_resource_response.py">ResponseAllofCrossResourceResponse</a></code>
- <code title="get /responses/allof/simple">client.responses.<a href="./src/sink/api/sdk/resources/responses/responses.py">allof_simple</a>() -> <a href="./src/sink/api/sdk/types/response_allof_simple_response.py">ResponseAllofSimpleResponse</a></code>
- <code title="get /responses/anyof_null">client.responses.<a href="./src/sink/api/sdk/resources/responses/responses.py">anyof_null</a>() -> <a href="./src/sink/api/sdk/types/object_with_any_of_null_property.py">ObjectWithAnyOfNullProperty</a></code>
- <code title="get /responses/array/object_with_union_properties">client.responses.<a href="./src/sink/api/sdk/resources/responses/responses.py">array_object_with_union_properties</a>() -> <a href="./src/sink/api/sdk/types/response_array_object_with_union_properties_response.py">ResponseArrayObjectWithUnionPropertiesResponse</a></code>
- <code title="get /responses/array">client.responses.<a href="./src/sink/api/sdk/resources/responses/responses.py">array_response</a>() -> <a href="./src/sink/api/sdk/types/response_array_response_response.py">ResponseArrayResponseResponse</a></code>
- <code title="post /responses/empty">client.responses.<a href="./src/sink/api/sdk/resources/responses/responses.py">empty_response</a>() -> None</code>
- <code title="get /responses/missing_required">client.responses.<a href="./src/sink/api/sdk/resources/responses/responses.py">missing_required</a>() -> <a href="./src/sink/api/sdk/types/response_missing_required_response.py">ResponseMissingRequiredResponse</a></code>
- <code title="get /responses/array/nested">client.responses.<a href="./src/sink/api/sdk/resources/responses/responses.py">nested_array</a>() -> <a href="./src/sink/api/sdk/types/response_nested_array_response.py">ResponseNestedArrayResponse</a></code>
- <code title="get /responses/object/everything">client.responses.<a href="./src/sink/api/sdk/resources/responses/responses.py">object_all_properties</a>() -> <a href="./src/sink/api/sdk/types/response_object_all_properties_response.py">ResponseObjectAllPropertiesResponse</a></code>
- <code title="post /responses/object_no_properties">client.responses.<a href="./src/sink/api/sdk/resources/responses/responses.py">object_no_properties</a>() -> <a href="./src/sink/api/sdk/types/response_object_no_properties_response.py">ResponseObjectNoPropertiesResponse</a></code>
- <code title="post /responses/object_with_additional_properties_prop">client.responses.<a href="./src/sink/api/sdk/resources/responses/responses.py">object_with_additional_properties_prop</a>() -> <a href="./src/sink/api/sdk/types/response_object_with_additional_properties_prop_response.py">ResponseObjectWithAdditionalPropertiesPropResponse</a></code>
- <code title="get /responses/oneof_null">client.responses.<a href="./src/sink/api/sdk/resources/responses/responses.py">oneof_null</a>() -> <a href="./src/sink/api/sdk/types/object_with_one_of_null_property.py">ObjectWithOneOfNullProperty</a></code>
- <code title="get /responses/only_read_only_properties">client.responses.<a href="./src/sink/api/sdk/resources/responses/responses.py">only_read_only_properties</a>() -> <a href="./src/sink/api/sdk/types/response_only_read_only_properties_response.py">ResponseOnlyReadOnlyPropertiesResponse</a></code>
- <code title="get /responses/shared_simple_object">client.responses.<a href="./src/sink/api/sdk/resources/responses/responses.py">shared_simple_object</a>() -> <a href="./src/sink/api/sdk/types/shared/simple_object.py">SimpleObject</a></code>
- <code title="post /responses/string">client.responses.<a href="./src/sink/api/sdk/resources/responses/responses.py">string_response</a>() -> str</code>
- <code title="post /responses/unknown_object">client.responses.<a href="./src/sink/api/sdk/resources/responses/responses.py">unknown_object</a>() -> <a href="./src/sink/api/sdk/types/unknown_object.py">object</a></code>
- <code title="get /responses/with_model_in_nested_path">client.responses.<a href="./src/sink/api/sdk/resources/responses/responses.py">with_model_in_nested_path</a>() -> <a href="./src/sink/api/sdk/types/model_with_nested_model.py">ModelWithNestedModel</a></code>

## UnionTypes

Types:

```python
from sink.api.sdk.types.responses import (
    UnionTypeMixedTypesResponse,
    UnionTypeNullableUnionResponse,
    UnionTypeNumbersResponse,
    UnionTypeObjectsResponse,
    UnionTypeSuperMixedTypesResponse,
    UnionTypeUnknownVariantResponse,
)
```

Methods:

- <code title="post /responses/unions/mixed_types">client.responses.union_types.<a href="./src/sink/api/sdk/resources/responses/union_types.py">mixed_types</a>() -> <a href="./src/sink/api/sdk/types/responses/union_type_mixed_types_response.py">UnionTypeMixedTypesResponse</a></code>
- <code title="post /responses/unions/nullable">client.responses.union_types.<a href="./src/sink/api/sdk/resources/responses/union_types.py">nullable_union</a>() -> <a href="./src/sink/api/sdk/types/responses/union_type_nullable_union_response.py">Optional[UnionTypeNullableUnionResponse]</a></code>
- <code title="post /responses/unions/numbers">client.responses.union_types.<a href="./src/sink/api/sdk/resources/responses/union_types.py">numbers</a>() -> <a href="./src/sink/api/sdk/types/responses/union_type_numbers_response.py">UnionTypeNumbersResponse</a></code>
- <code title="post /responses/unions/objects">client.responses.union_types.<a href="./src/sink/api/sdk/resources/responses/union_types.py">objects</a>() -> <a href="./src/sink/api/sdk/types/responses/union_type_objects_response.py">UnionTypeObjectsResponse</a></code>
- <code title="post /responses/unions/super_mixed_types">client.responses.union_types.<a href="./src/sink/api/sdk/resources/responses/union_types.py">super_mixed_types</a>() -> <a href="./src/sink/api/sdk/types/responses/union_type_super_mixed_types_response.py">UnionTypeSuperMixedTypesResponse</a></code>
- <code title="post /responses/unions/unknown_variant">client.responses.union_types.<a href="./src/sink/api/sdk/resources/responses/union_types.py">unknown_variant</a>() -> <a href="./src/sink/api/sdk/types/responses/union_type_unknown_variant_response.py">UnionTypeUnknownVariantResponse</a></code>

# PathParams

Types:

```python
from sink.api.sdk.types import (
    PathParamColonSuffixResponse,
    PathParamFileExtensionResponse,
    PathParamMultipleResponse,
    PathParamQueryParamResponse,
    PathParamSingularResponse,
)
```

Methods:

- <code title="post /path_params/{with_verb}:initiate">client.path_params.<a href="./src/sink/api/sdk/resources/path_params.py">colon_suffix</a>(with_verb) -> <a href="./src/sink/api/sdk/types/path_param_colon_suffix_response.py">PathParamColonSuffixResponse</a></code>
- <code title="post /path_params/{dashed-param}">client.path_params.<a href="./src/sink/api/sdk/resources/path_params.py">dashed_param</a>(dashed_param) -> <a href="./src/sink/api/sdk/types/shared/basic_shared_model_object.py">BasicSharedModelObject</a></code>
- <code title="post /path_params/dates/{date_param}">client.path_params.<a href="./src/sink/api/sdk/resources/path_params.py">date_param</a>(date_param) -> <a href="./src/sink/api/sdk/types/shared/basic_shared_model_object.py">BasicSharedModelObject</a></code>
- <code title="post /path_params/date_times/{datetime_param}">client.path_params.<a href="./src/sink/api/sdk/resources/path_params.py">datetime_param</a>(datetime_param) -> <a href="./src/sink/api/sdk/types/shared/basic_shared_model_object.py">BasicSharedModelObject</a></code>
- <code title="post /path_params/enums/{enum_param}">client.path_params.<a href="./src/sink/api/sdk/resources/path_params.py">enum_param</a>(enum_param) -> <a href="./src/sink/api/sdk/types/shared/basic_shared_model_object.py">BasicSharedModelObject</a></code>
- <code title="post /path_params/{with_file_extension}.json">client.path_params.<a href="./src/sink/api/sdk/resources/path_params.py">file_extension</a>(with_file_extension) -> <a href="./src/sink/api/sdk/types/path_param_file_extension_response.py">PathParamFileExtensionResponse</a></code>
- <code title="post /path_params/{integer_param}">client.path_params.<a href="./src/sink/api/sdk/resources/path_params.py">integer_param</a>(integer_param) -> <a href="./src/sink/api/sdk/types/shared/basic_shared_model_object.py">BasicSharedModelObject</a></code>
- <code title="post /path_params/{first}/{second}/{last}">client.path_params.<a href="./src/sink/api/sdk/resources/path_params.py">multiple</a>(last, \*, first, second) -> <a href="./src/sink/api/sdk/types/path_param_multiple_response.py">PathParamMultipleResponse</a></code>
- <code title="post /path_params/nullable/{nullable_param_1}/{nullable_param_2}/{nullable_param_3}">client.path_params.<a href="./src/sink/api/sdk/resources/path_params.py">nullable_params</a>(nullable_param_3, \*, nullable_param_1, nullable_param_2, \*\*<a href="src/sink/api/sdk/types/path_param_nullable_params_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/shared/basic_shared_model_object.py">BasicSharedModelObject</a></code>
- <code title="post /path_params/mixed/{integer_param}/{string_param}">client.path_params.<a href="./src/sink/api/sdk/resources/path_params.py">params_mixed_types</a>(string_param, \*, integer_param) -> <a href="./src/sink/api/sdk/types/shared/basic_shared_model_object.py">BasicSharedModelObject</a></code>
- <code title="post /path_params/{with_query_param}?beta=true">client.path_params.<a href="./src/sink/api/sdk/resources/path_params.py">query_param</a>(with_query_param) -> <a href="./src/sink/api/sdk/types/path_param_query_param_response.py">PathParamQueryParamResponse</a></code>
- <code title="post /path_params/{singular}">client.path_params.<a href="./src/sink/api/sdk/resources/path_params.py">singular</a>(singular) -> <a href="./src/sink/api/sdk/types/path_param_singular_response.py">PathParamSingularResponse</a></code>

# PositionalParams

Methods:

- <code title="post /positional_params/basic_body">client.positional_params.<a href="./src/sink/api/sdk/resources/positional_params.py">basic_body</a>(\*\*<a href="src/sink/api/sdk/types/positional_param_basic_body_params.py">params</a>) -> None</code>
- <code title="get /positional_params/basic_query">client.positional_params.<a href="./src/sink/api/sdk/resources/positional_params.py">basic_query</a>(\*\*<a href="src/sink/api/sdk/types/positional_param_basic_query_params.py">params</a>) -> None</code>
- <code title="post /positional_params/body">client.positional_params.<a href="./src/sink/api/sdk/resources/positional_params.py">body</a>(\*\*<a href="src/sink/api/sdk/types/positional_param_body_params.py">params</a>) -> None</code>
- <code title="post /positional_params/body_extra_param">client.positional_params.<a href="./src/sink/api/sdk/resources/positional_params.py">body_extra_param</a>(\*\*<a href="src/sink/api/sdk/types/positional_param_body_extra_param_params.py">params</a>) -> None</code>
- <code title="post /positional_params/query/{id}/kitchen_sink/{key}">client.positional_params.<a href="./src/sink/api/sdk/resources/positional_params.py">kitchen_sink</a>(id, \*, key, \*\*<a href="src/sink/api/sdk/types/positional_param_kitchen_sink_params.py">params</a>) -> None</code>
- <code title="post /positional_params/{first}/{second}/{last}">client.positional_params.<a href="./src/sink/api/sdk/resources/positional_params.py">multiple_path_params</a>(second, \*, first, last, \*\*<a href="src/sink/api/sdk/types/positional_param_multiple_path_params_params.py">params</a>) -> None</code>
- <code title="get /positional_params/query">client.positional_params.<a href="./src/sink/api/sdk/resources/positional_params.py">query</a>(\*\*<a href="src/sink/api/sdk/types/positional_param_query_params.py">params</a>) -> None</code>
- <code title="post /positional_params/query/{id}">client.positional_params.<a href="./src/sink/api/sdk/resources/positional_params.py">query_and_path</a>(id, \*\*<a href="src/sink/api/sdk/types/positional_param_query_and_path_params.py">params</a>) -> None</code>
- <code title="get /positional_params/query_multiple">client.positional_params.<a href="./src/sink/api/sdk/resources/positional_params.py">query_multiple</a>(\*\*<a href="src/sink/api/sdk/types/positional_param_query_multiple_params.py">params</a>) -> None</code>
- <code title="get /positional_params/{single}">client.positional_params.<a href="./src/sink/api/sdk/resources/positional_params.py">single</a>(single) -> None</code>
- <code title="post /positional_params/body/union/{id}">client.positional_params.<a href="./src/sink/api/sdk/resources/positional_params.py">union_body_and_path</a>(id, \*\*<a href="src/sink/api/sdk/types/positional_param_union_body_and_path_params.py">params</a>) -> None</code>

# EmptyBody

Methods:

- <code title="post /mixed_params/with_empty_body/{path_param}/x_stainless_empty_object">client.empty_body.<a href="./src/sink/api/sdk/resources/empty_body.py">stainless_empty_object</a>(path_param, \*\*<a href="src/sink/api/sdk/types/empty_body_stainless_empty_object_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/shared/basic_shared_model_object.py">BasicSharedModelObject</a></code>
- <code title="post /mixed_params/with_empty_body/{path_param}">client.empty_body.<a href="./src/sink/api/sdk/resources/empty_body.py">typed_params</a>(path_param, \*\*<a href="src/sink/api/sdk/types/empty_body_typed_params_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/shared/basic_shared_model_object.py">BasicSharedModelObject</a></code>

# QueryParams

Methods:

- <code title="get /query_params/allOf">client.query_params.<a href="./src/sink/api/sdk/resources/query_params.py">all_of</a>(\*\*<a href="src/sink/api/sdk/types/query_param_all_of_params.py">params</a>) -> None</code>
- <code title="get /query_params/anyOf">client.query_params.<a href="./src/sink/api/sdk/resources/query_params.py">any_of</a>(\*\*<a href="src/sink/api/sdk/types/query_param_any_of_params.py">params</a>) -> None</code>
- <code title="get /query_params/anyOfStringOrArray">client.query_params.<a href="./src/sink/api/sdk/resources/query_params.py">any_of_string_or_array</a>(\*\*<a href="src/sink/api/sdk/types/query_param_any_of_string_or_array_params.py">params</a>) -> None</code>
- <code title="get /query_params/array">client.query_params.<a href="./src/sink/api/sdk/resources/query_params.py">array</a>(\*\*<a href="src/sink/api/sdk/types/query_param_array_params.py">params</a>) -> None</code>
- <code title="get /query_params/enum">client.query_params.<a href="./src/sink/api/sdk/resources/query_params.py">enum</a>(\*\*<a href="src/sink/api/sdk/types/query_param_enum_params.py">params</a>) -> None</code>
- <code title="get /query_params/object">client.query_params.<a href="./src/sink/api/sdk/resources/query_params.py">object</a>(\*\*<a href="src/sink/api/sdk/types/query_param_object_params.py">params</a>) -> None</code>
- <code title="get /query_params/oneOf">client.query_params.<a href="./src/sink/api/sdk/resources/query_params.py">one_of</a>(\*\*<a href="src/sink/api/sdk/types/query_param_one_of_params.py">params</a>) -> None</code>
- <code title="get /query_params/primitives">client.query_params.<a href="./src/sink/api/sdk/resources/query_params.py">primitives</a>(\*\*<a href="src/sink/api/sdk/types/query_param_primitives_params.py">params</a>) -> None</code>

# BodyParams

Types:

```python
from sink.api.sdk.types import (
    ModelWithParamInName,
    MyModel,
    NestedRequestModelA,
    NestedRequestModelB,
    NestedRequestModelC,
    ObjectMapModel,
    StringMapModel,
    UnknownObjectModel,
    BodyParamTopLevelAllOfResponse,
    BodyParamTopLevelAnyOfResponse,
    BodyParamTopLevelOneOfResponse,
    BodyParamUnionOverlappingPropResponse,
)
```

Methods:

- <code title="post /body_params/with_duplicate_subproperty">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">duplicate_subproperty</a>(\*\*<a href="src/sink/api/sdk/types/body_param_duplicate_subproperty_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/model_with_nested_model.py">ModelWithNestedModel</a></code>
- <code title="post /body_params/enum_properties">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">enum_properties</a>(\*\*<a href="src/sink/api/sdk/types/body_param_enum_properties_params.py">params</a>) -> None</code>
- <code title="post /body_params/with_nested_models">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">nested_request_models</a>(\*\*<a href="src/sink/api/sdk/types/body_param_nested_request_models_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/model_with_nested_model.py">ModelWithNestedModel</a></code>
- <code title="post /body_params/object_map_model_ref">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">object_map_model_ref</a>(\*\*<a href="src/sink/api/sdk/types/body_param_object_map_model_ref_params.py">params</a>) -> None</code>
- <code title="post /body_params/object_with_array_of_objects">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">object_with_array_of_objects</a>(\*\*<a href="src/sink/api/sdk/types/body_param_object_with_array_of_objects_params.py">params</a>) -> None</code>
- <code title="post /body_params/object_with_union_properties">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">object_with_union_properties</a>(\*\*<a href="src/sink/api/sdk/types/body_param_object_with_union_properties_params.py">params</a>) -> None</code>
- <code title="patch /body_params/only_read_only_properties">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">only_read_only_properties</a>() -> None</code>
- <code title="post /body_params/param_in_model_name_ref">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">param_in_model_name_ref</a>(\*\*<a href="src/sink/api/sdk/types/body_param_param_in_model_name_ref_params.py">params</a>) -> None</code>
- <code title="post /body_params/property_model_ref">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">property_model_ref</a>(\*\*<a href="src/sink/api/sdk/types/body_param_property_model_ref_params.py">params</a>) -> None</code>
- <code title="post /body_params/property_with_complex_union">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">property_with_complex_union</a>(\*\*<a href="src/sink/api/sdk/types/body_param_property_with_complex_union_params.py">params</a>) -> None</code>
- <code title="post /body_params/read_only_properties">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">read_only_properties</a>(\*\*<a href="src/sink/api/sdk/types/body_param_read_only_properties_params.py">params</a>) -> None</code>
- <code title="post /body_params/string_map_model_ref">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">string_map_model_ref</a>(\*\*<a href="src/sink/api/sdk/types/body_param_string_map_model_ref_params.py">params</a>) -> None</code>
- <code title="post /body_params/top_level_allOf">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">top_level_all_of</a>(\*\*<a href="src/sink/api/sdk/types/body_param_top_level_all_of_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/body_param_top_level_all_of_response.py">BodyParamTopLevelAllOfResponse</a></code>
- <code title="post /body_params/top_level_allOf_nested_object">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">top_level_all_of_nested_object</a>(\*\*<a href="src/sink/api/sdk/types/body_param_top_level_all_of_nested_object_params.py">params</a>) -> None</code>
- <code title="post /body_params/top_level_anyOf">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">top_level_any_of</a>(\*\*<a href="src/sink/api/sdk/types/body_param_top_level_any_of_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/body_param_top_level_any_of_response.py">BodyParamTopLevelAnyOfResponse</a></code>
- <code title="post /body_params/top_level_anyOf_with_ref">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">top_level_any_of_with_ref</a>(\*\*<a href="src/sink/api/sdk/types/body_param_top_level_any_of_with_ref_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/shared/basic_shared_model_object.py">BasicSharedModelObject</a></code>
- <code title="post /body_params/top_level_array">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">top_level_array</a>(\*\*<a href="src/sink/api/sdk/types/body_param_top_level_array_params.py">params</a>) -> None</code>
- <code title="post /body_params/top_level_array_with_children">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">top_level_array_with_children</a>(\*\*<a href="src/sink/api/sdk/types/body_param_top_level_array_with_children_params.py">params</a>) -> None</code>
- <code title="post /body_params/top_level_array_with_other_params">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">top_level_array_with_other_params</a>(\*\*<a href="src/sink/api/sdk/types/body_param_top_level_array_with_other_params_params.py">params</a>) -> None</code>
- <code title="post /body_params/top_level_oneOf">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">top_level_one_of</a>(\*\*<a href="src/sink/api/sdk/types/body_param_top_level_one_of_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/body_param_top_level_one_of_response.py">BodyParamTopLevelOneOfResponse</a></code>
- <code title="post /body_params/top_level_oneOf_one_entry">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">top_level_one_of_one_entry</a>(\*\*<a href="src/sink/api/sdk/types/body_param_top_level_one_of_one_entry_params.py">params</a>) -> None</code>
- <code title="post /body_params/top_level_shared_type">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">top_level_shared_type</a>(\*\*<a href="src/sink/api/sdk/types/body_param_top_level_shared_type_params.py">params</a>) -> None</code>
- <code title="post /body_params/top_level_anyOf_overlapping_property">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">union_overlapping_prop</a>(\*\*<a href="src/sink/api/sdk/types/body_param_union_overlapping_prop_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/body_param_union_overlapping_prop_response.py">BodyParamUnionOverlappingPropResponse</a></code>
- <code title="post /body_params/unknown_object">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">unknown_object</a>(\*\*<a href="src/sink/api/sdk/types/body_param_unknown_object_params.py">params</a>) -> None</code>
- <code title="post /body_params/with_default_body_param_optional">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">with_default_body_param_optional</a>(\*\*<a href="src/sink/api/sdk/types/body_param_with_default_body_param_optional_params.py">params</a>) -> None</code>
- <code title="post /body_params/with_default_body_param_required">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">with_default_body_param_required</a>(\*\*<a href="src/sink/api/sdk/types/body_param_with_default_body_param_required_params.py">params</a>) -> None</code>
- <code title="post /body_params/with_model_property">client.body_params.<a href="./src/sink/api/sdk/resources/body_params/body_params.py">with_model_property</a>(\*\*<a href="src/sink/api/sdk/types/body_param_with_model_property_params.py">params</a>) -> None</code>

## Objects

Methods:

- <code title="post /body_params/objects/mixed_known_and_unknown">client.body_params.objects.<a href="./src/sink/api/sdk/resources/body_params/objects.py">mixed_known_and_unknown</a>(\*\*<a href="src/sink/api/sdk/types/body_params/object_mixed_known_and_unknown_params.py">params</a>) -> None</code>

## Unions

Types:

```python
from sink.api.sdk.types.body_params import ModelNewTypeString
```

Methods:

- <code title="post /body_params/unions/param_union_enum_new_type">client.body_params.unions.<a href="./src/sink/api/sdk/resources/body_params/unions.py">param_union_enum_new_type</a>(\*\*<a href="src/sink/api/sdk/types/body_params/union_param_union_enum_new_type_params.py">params</a>) -> None</code>

# HeaderParams

Methods:

- <code title="post /header_params/all_types">client.header_params.<a href="./src/sink/api/sdk/resources/header_params.py">all_types</a>(\*\*<a href="src/sink/api/sdk/types/header_param_all_types_params.py">params</a>) -> None</code>
- <code title="post /header_params/arrays">client.header_params.<a href="./src/sink/api/sdk/resources/header_params.py">arrays</a>(\*\*<a href="src/sink/api/sdk/types/header_param_arrays_params.py">params</a>) -> None</code>
- <code title="post /header_params/client_argument">client.header_params.<a href="./src/sink/api/sdk/resources/header_params.py">client_argument</a>(\*\*<a href="src/sink/api/sdk/types/header_param_client_argument_params.py">params</a>) -> None</code>
- <code title="post /header_params/invalid_name">client.header_params.<a href="./src/sink/api/sdk/resources/header_params.py">invalid_name</a>(\*\*<a href="src/sink/api/sdk/types/header_param_invalid_name_params.py">params</a>) -> None</code>
- <code title="post /header_params/nullable_type">client.header_params.<a href="./src/sink/api/sdk/resources/header_params.py">nullable_type</a>(\*\*<a href="src/sink/api/sdk/types/header_param_nullable_type_params.py">params</a>) -> None</code>

# MixedParams

Methods:

- <code title="post /mixed_params/body_with_top_level_one_of_and_path/{path_param}">client.mixed_params.<a href="./src/sink/api/sdk/resources/mixed_params/mixed_params.py">body_with_top_level_one_of_and_path</a>(path_param, \*\*<a href="src/sink/api/sdk/types/mixed_param_body_with_top_level_one_of_and_path_params.py">params</a>) -> None</code>
- <code title="post /mixed_params/query_and_body">client.mixed_params.<a href="./src/sink/api/sdk/resources/mixed_params/mixed_params.py">query_and_body</a>(\*\*<a href="src/sink/api/sdk/types/mixed_param_query_and_body_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/shared/basic_shared_model_object.py">BasicSharedModelObject</a></code>
- <code title="post /mixed_params/query_body_and_path/{path_param}">client.mixed_params.<a href="./src/sink/api/sdk/resources/mixed_params/mixed_params.py">query_body_and_path</a>(path_param, \*\*<a href="src/sink/api/sdk/types/mixed_param_query_body_and_path_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/shared/basic_shared_model_object.py">BasicSharedModelObject</a></code>

## Duplicates

Methods:

- <code title="post /mixed_params/duplicates/body_and_path/{id}">client.mixed_params.duplicates.<a href="./src/sink/api/sdk/resources/mixed_params/duplicates.py">body_and_path</a>(path_id, \*\*<a href="src/sink/api/sdk/types/mixed_params/duplicate_body_and_path_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/shared/basic_shared_model_object.py">BasicSharedModelObject</a></code>
- <code title="post /mixed_params/duplicates/query_and_body">client.mixed_params.duplicates.<a href="./src/sink/api/sdk/resources/mixed_params/duplicates.py">query_and_body</a>(\*\*<a href="src/sink/api/sdk/types/mixed_params/duplicate_query_and_body_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/shared/basic_shared_model_object.py">BasicSharedModelObject</a></code>
- <code title="post /mixed_params/duplicates/query_and_body_different_casing">client.mixed_params.duplicates.<a href="./src/sink/api/sdk/resources/mixed_params/duplicates.py">query_and_body_different_casing</a>(\*\*<a href="src/sink/api/sdk/types/mixed_params/duplicate_query_and_body_different_casing_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/shared/basic_shared_model_object.py">BasicSharedModelObject</a></code>
- <code title="post /mixed_params/duplicates/query_and_path/{id}">client.mixed_params.duplicates.<a href="./src/sink/api/sdk/resources/mixed_params/duplicates.py">query_and_path</a>(path_id, \*\*<a href="src/sink/api/sdk/types/mixed_params/duplicate_query_and_path_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/shared/basic_shared_model_object.py">BasicSharedModelObject</a></code>

# MakeAmbiguousSchemasLooser

Types:

```python
from sink.api.sdk.types import MakeAmbiguousSchemasLooserMakeAmbiguousSchemasLooserResponse
```

Methods:

- <code title="get /make-ambiguous-schemas-looser">client.make_ambiguous_schemas_looser.<a href="./src/sink/api/sdk/resources/make_ambiguous_schemas_looser.py">make_ambiguous_schemas_looser</a>() -> <a href="./src/sink/api/sdk/types/make_ambiguous_schemas_looser_make_ambiguous_schemas_looser_response.py">MakeAmbiguousSchemasLooserMakeAmbiguousSchemasLooserResponse</a></code>

# MakeAmbiguousSchemasExplicit

Types:

```python
from sink.api.sdk.types import MakeAmbiguousSchemasExplicitMakeAmbiguousSchemasExplicitResponse
```

Methods:

- <code title="get /make-ambiguous-schemas-explicit">client.make_ambiguous_schemas_explicit.<a href="./src/sink/api/sdk/resources/make_ambiguous_schemas_explicit.py">make_ambiguous_schemas_explicit</a>() -> <a href="./src/sink/api/sdk/types/make_ambiguous_schemas_explicit_make_ambiguous_schemas_explicit_response.py">MakeAmbiguousSchemasExplicitMakeAmbiguousSchemasExplicitResponse</a></code>

# DecoratorTests

Types:

```python
from sink.api.sdk.types import DecoratorTestKeepMeResponse
```

Methods:

- <code title="get /decorator_tests/keep/me">client.decorator_tests.<a href="./src/sink/api/sdk/resources/decorator_tests/decorator_tests.py">keep_me</a>() -> <a href="./src/sink/api/sdk/types/decorator_test_keep_me_response.py">DecoratorTestKeepMeResponse</a></code>

## Languages

Methods:

- <code title="get /responses/shared_simple_object">client.decorator_tests.languages.<a href="./src/sink/api/sdk/resources/decorator_tests/languages.py">skipped_for_node</a>() -> <a href="./src/sink/api/sdk/types/shared/simple_object.py">SimpleObject</a></code>

## KeepThisResource

Types:

```python
from sink.api.sdk.types.decorator_tests import KeepThisResourceKeepThisMethodResponse
```

Methods:

- <code title="get /decorator_tests/nested/keep/this/method">client.decorator_tests.keep_this_resource.<a href="./src/sink/api/sdk/resources/decorator_tests/keep_this_resource.py">keep_this_method</a>() -> <a href="./src/sink/api/sdk/types/decorator_tests/keep_this_resource_keep_this_method_response.py">KeepThisResourceKeepThisMethodResponse</a></code>

## SkipThisResource

Types:

```python
from sink.api.sdk.types.decorator_tests import SkipThisResourceINeverAppearResponse
```

Methods:

- <code title="get /decorator_tests/nested/i/never/appear">client.decorator_tests.skip_this_resource.<a href="./src/sink/api/sdk/resources/decorator_tests/skip_this_resource.py">i_never_appear</a>() -> <a href="./src/sink/api/sdk/types/decorator_tests/skip_this_resource_i_never_appear_response.py">SkipThisResourceINeverAppearResponse</a></code>

# Tests

Methods:

- <code title="get /tests/run_codegen">client.tests.<a href="./src/sink/api/sdk/resources/tests.py">run_codegen</a>() -> None</code>

# DeeplyNested

## LevelOne

Types:

```python
from sink.api.sdk.types.deeply_nested import ModelLevel1
```

Methods:

- <code title="get /cards/{card_token}">client.deeply_nested.level_one.<a href="./src/sink/api/sdk/resources/deeply_nested/level_one/level_one.py">method_level_1</a>(card_token) -> <a href="./src/sink/api/sdk/types/card.py">Card</a></code>

### LevelTwo

Types:

```python
from sink.api.sdk.types.deeply_nested.level_one import ModelLevel2
```

Methods:

- <code title="get /cards/{card_token}">client.deeply_nested.level_one.level_two.<a href="./src/sink/api/sdk/resources/deeply_nested/level_one/level_two/level_two.py">method_level_2</a>(card_token) -> <a href="./src/sink/api/sdk/types/card.py">Card</a></code>

#### LevelThree

Types:

```python
from sink.api.sdk.types.deeply_nested.level_one.level_two import ModelLevel3
```

Methods:

- <code title="get /cards/{card_token}">client.deeply_nested.level_one.level_two.level_three.<a href="./src/sink/api/sdk/resources/deeply_nested/level_one/level_two/level_three.py">method_level_3</a>(card_token) -> <a href="./src/sink/api/sdk/types/card.py">Card</a></code>

# Version1_30Names

Types:

```python
from sink.api.sdk.types import Version1_30NameCreateResponse
```

Methods:

- <code title="post /version_1_30_names/query/{version_1_15}">client.version_1_30_names.<a href="./src/sink/api/sdk/resources/version_1_30_names.py">create</a>(version_1_15, \*\*<a href="src/sink/api/sdk/types/version_1_30_name_create_params.py">params</a>) -> <a href="./src/sink/api/sdk/types/version_1_30_name_create_response.py">Version1_30NameCreateResponse</a></code>

# Recursion

Types:

```python
from sink.api.sdk.types import ArrayRecursion, SelfRecursion
```

## SharedResponses

Methods:

- <code title="post /recursion/shared/responses/self">client.recursion.shared_responses.<a href="./src/sink/api/sdk/resources/recursion/shared_responses.py">create_self</a>() -> <a href="./src/sink/api/sdk/types/shared/shared_self_recursion.py">SharedSelfRecursion</a></code>

# SharedQueryParams

Types:

```python
from sink.api.sdk.types import SharedQueryParamRetrieveResponse, SharedQueryParamDelResponse
```

Methods:

- <code title="get /shared-query-params">client.shared_query_params.<a href="./src/sink/api/sdk/resources/shared_query_params.py">retrieve</a>(\*\*<a href="src/sink/api/sdk/types/shared_query_param_retrieve_params.py">params</a>) -> str</code>
- <code title="delete /shared-query-params">client.shared_query_params.<a href="./src/sink/api/sdk/resources/shared_query_params.py">delete</a>(\*\*<a href="src/sink/api/sdk/types/shared_query_param_delete_params.py">params</a>) -> str</code>

# ModelReferencedInParentAndChild

Types:

```python
from sink.api.sdk.types import ModelReferencedInParentAndChild
```

Methods:

- <code title="get /model_referenced_in_parent_and_child">client.model_referenced_in_parent_and_child.<a href="./src/sink/api/sdk/resources/model_referenced_in_parent_and_child/model_referenced_in_parent_and_child.py">retrieve</a>() -> <a href="./src/sink/api/sdk/types/model_referenced_in_parent_and_child/model_referenced_in_parent_and_child.py">ModelReferencedInParentAndChild</a></code>

## Child

Methods:

- <code title="get /model_referenced_in_parent_and_child/child">client.model_referenced_in_parent_and_child.child.<a href="./src/sink/api/sdk/resources/model_referenced_in_parent_and_child/child.py">retrieve</a>() -> <a href="./src/sink/api/sdk/types/model_referenced_in_parent_and_child/model_referenced_in_parent_and_child.py">ModelReferencedInParentAndChild</a></code>
