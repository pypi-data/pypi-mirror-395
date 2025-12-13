# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import (
    NameChildPropImportClashResponse,
    NameResponseShadowsPydanticResponse,
    NamePropertiesCommonConflictsResponse,
    NamePropertiesIllegalGoIdentifiersResponse,
    NameResponsePropertyClashesModelImportResponse,
    NamePropertiesIllegalJavascriptIdentifiersResponse,
)
from sink.api.sdk._utils import parse_date
from sink.api.sdk.types.shared import BasicSharedModelObject

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestNames:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_child_prop_import_clash(self, client: Sink) -> None:
        name = client.names.child_prop_import_clash()
        assert_matches_type(NameChildPropImportClashResponse, name, path=["response"])

    @parametrize
    def test_raw_response_child_prop_import_clash(self, client: Sink) -> None:
        response = client.names.with_raw_response.child_prop_import_clash()

        assert response.is_closed is True
        name = response.parse()
        assert_matches_type(NameChildPropImportClashResponse, name, path=["response"])

    @parametrize
    def test_streaming_response_child_prop_import_clash(self, client: Sink) -> None:
        with client.names.with_streaming_response.child_prop_import_clash() as response:
            assert not response.is_closed

            name = response.parse()
            assert_matches_type(NameChildPropImportClashResponse, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_get(self, client: Sink) -> None:
        name = client.names.get()
        assert_matches_type(BasicSharedModelObject, name, path=["response"])

    @parametrize
    def test_raw_response_get(self, client: Sink) -> None:
        response = client.names.with_raw_response.get()

        assert response.is_closed is True
        name = response.parse()
        assert_matches_type(BasicSharedModelObject, name, path=["response"])

    @parametrize
    def test_streaming_response_get(self, client: Sink) -> None:
        with client.names.with_streaming_response.get() as response:
            assert not response.is_closed

            name = response.parse()
            assert_matches_type(BasicSharedModelObject, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_properties_common_conflicts(self, client: Sink) -> None:
        name = client.names.properties_common_conflicts(
            _1_digit_leading_underscore="_1_digit_leading_underscore",
            _leading_underscore="_leading_underscore",
            _leading_underscore_mixed_case="_leading_underscore_MixedCase",
            bool=True,
            bool_2=True,
            date=parse_date("2019-12-27"),
            date_2=parse_date("2019-12-27"),
            float=0,
            float_2=0,
            int=0,
            int_2=0,
        )
        assert_matches_type(NamePropertiesCommonConflictsResponse, name, path=["response"])

    @parametrize
    def test_raw_response_properties_common_conflicts(self, client: Sink) -> None:
        response = client.names.with_raw_response.properties_common_conflicts(
            _1_digit_leading_underscore="_1_digit_leading_underscore",
            _leading_underscore="_leading_underscore",
            _leading_underscore_mixed_case="_leading_underscore_MixedCase",
            bool=True,
            bool_2=True,
            date=parse_date("2019-12-27"),
            date_2=parse_date("2019-12-27"),
            float=0,
            float_2=0,
            int=0,
            int_2=0,
        )

        assert response.is_closed is True
        name = response.parse()
        assert_matches_type(NamePropertiesCommonConflictsResponse, name, path=["response"])

    @parametrize
    def test_streaming_response_properties_common_conflicts(self, client: Sink) -> None:
        with client.names.with_streaming_response.properties_common_conflicts(
            _1_digit_leading_underscore="_1_digit_leading_underscore",
            _leading_underscore="_leading_underscore",
            _leading_underscore_mixed_case="_leading_underscore_MixedCase",
            bool=True,
            bool_2=True,
            date=parse_date("2019-12-27"),
            date_2=parse_date("2019-12-27"),
            float=0,
            float_2=0,
            int=0,
            int_2=0,
        ) as response:
            assert not response.is_closed

            name = response.parse()
            assert_matches_type(NamePropertiesCommonConflictsResponse, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_properties_illegal_go_identifiers(self, client: Sink) -> None:
        name = client.names.properties_illegal_go_identifiers(
            type="type",
        )
        assert_matches_type(NamePropertiesIllegalGoIdentifiersResponse, name, path=["response"])

    @parametrize
    def test_method_properties_illegal_go_identifiers_with_all_params(self, client: Sink) -> None:
        name = client.names.properties_illegal_go_identifiers(
            type="type",
            defer="defer",
        )
        assert_matches_type(NamePropertiesIllegalGoIdentifiersResponse, name, path=["response"])

    @parametrize
    def test_raw_response_properties_illegal_go_identifiers(self, client: Sink) -> None:
        response = client.names.with_raw_response.properties_illegal_go_identifiers(
            type="type",
        )

        assert response.is_closed is True
        name = response.parse()
        assert_matches_type(NamePropertiesIllegalGoIdentifiersResponse, name, path=["response"])

    @parametrize
    def test_streaming_response_properties_illegal_go_identifiers(self, client: Sink) -> None:
        with client.names.with_streaming_response.properties_illegal_go_identifiers(
            type="type",
        ) as response:
            assert not response.is_closed

            name = response.parse()
            assert_matches_type(NamePropertiesIllegalGoIdentifiersResponse, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_properties_illegal_go_identifiers(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `type` but received ''"):
            client.names.with_raw_response.properties_illegal_go_identifiers(
                type="",
            )

    @parametrize
    def test_method_properties_illegal_javascript_identifiers_overload_1(self, client: Sink) -> None:
        name = client.names.properties_illegal_javascript_identifiers()
        assert_matches_type(NamePropertiesIllegalJavascriptIdentifiersResponse, name, path=["response"])

    @parametrize
    def test_method_properties_illegal_javascript_identifiers_with_all_params_overload_1(self, client: Sink) -> None:
        name = client.names.properties_illegal_javascript_identifiers(
            irrelevant=0,
        )
        assert_matches_type(NamePropertiesIllegalJavascriptIdentifiersResponse, name, path=["response"])

    @parametrize
    def test_raw_response_properties_illegal_javascript_identifiers_overload_1(self, client: Sink) -> None:
        response = client.names.with_raw_response.properties_illegal_javascript_identifiers()

        assert response.is_closed is True
        name = response.parse()
        assert_matches_type(NamePropertiesIllegalJavascriptIdentifiersResponse, name, path=["response"])

    @parametrize
    def test_streaming_response_properties_illegal_javascript_identifiers_overload_1(self, client: Sink) -> None:
        with client.names.with_streaming_response.properties_illegal_javascript_identifiers() as response:
            assert not response.is_closed

            name = response.parse()
            assert_matches_type(NamePropertiesIllegalJavascriptIdentifiersResponse, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_properties_illegal_javascript_identifiers_overload_2(self, client: Sink) -> None:
        name = client.names.properties_illegal_javascript_identifiers(
            body=0,
        )
        assert_matches_type(NamePropertiesIllegalJavascriptIdentifiersResponse, name, path=["response"])

    @parametrize
    def test_raw_response_properties_illegal_javascript_identifiers_overload_2(self, client: Sink) -> None:
        response = client.names.with_raw_response.properties_illegal_javascript_identifiers(
            body=0,
        )

        assert response.is_closed is True
        name = response.parse()
        assert_matches_type(NamePropertiesIllegalJavascriptIdentifiersResponse, name, path=["response"])

    @parametrize
    def test_streaming_response_properties_illegal_javascript_identifiers_overload_2(self, client: Sink) -> None:
        with client.names.with_streaming_response.properties_illegal_javascript_identifiers(
            body=0,
        ) as response:
            assert not response.is_closed

            name = response.parse()
            assert_matches_type(NamePropertiesIllegalJavascriptIdentifiersResponse, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_response_property_clashes_model_import(self, client: Sink) -> None:
        name = client.names.response_property_clashes_model_import()
        assert_matches_type(NameResponsePropertyClashesModelImportResponse, name, path=["response"])

    @parametrize
    def test_raw_response_response_property_clashes_model_import(self, client: Sink) -> None:
        response = client.names.with_raw_response.response_property_clashes_model_import()

        assert response.is_closed is True
        name = response.parse()
        assert_matches_type(NameResponsePropertyClashesModelImportResponse, name, path=["response"])

    @parametrize
    def test_streaming_response_response_property_clashes_model_import(self, client: Sink) -> None:
        with client.names.with_streaming_response.response_property_clashes_model_import() as response:
            assert not response.is_closed

            name = response.parse()
            assert_matches_type(NameResponsePropertyClashesModelImportResponse, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_response_shadows_pydantic(self, client: Sink) -> None:
        name = client.names.response_shadows_pydantic()
        assert_matches_type(NameResponseShadowsPydanticResponse, name, path=["response"])

    @parametrize
    def test_raw_response_response_shadows_pydantic(self, client: Sink) -> None:
        response = client.names.with_raw_response.response_shadows_pydantic()

        assert response.is_closed is True
        name = response.parse()
        assert_matches_type(NameResponseShadowsPydanticResponse, name, path=["response"])

    @parametrize
    def test_streaming_response_response_shadows_pydantic(self, client: Sink) -> None:
        with client.names.with_streaming_response.response_shadows_pydantic() as response:
            assert not response.is_closed

            name = response.parse()
            assert_matches_type(NameResponseShadowsPydanticResponse, name, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncNames:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_child_prop_import_clash(self, async_client: AsyncSink) -> None:
        name = await async_client.names.child_prop_import_clash()
        assert_matches_type(NameChildPropImportClashResponse, name, path=["response"])

    @parametrize
    async def test_raw_response_child_prop_import_clash(self, async_client: AsyncSink) -> None:
        response = await async_client.names.with_raw_response.child_prop_import_clash()

        assert response.is_closed is True
        name = response.parse()
        assert_matches_type(NameChildPropImportClashResponse, name, path=["response"])

    @parametrize
    async def test_streaming_response_child_prop_import_clash(self, async_client: AsyncSink) -> None:
        async with async_client.names.with_streaming_response.child_prop_import_clash() as response:
            assert not response.is_closed

            name = await response.parse()
            assert_matches_type(NameChildPropImportClashResponse, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_get(self, async_client: AsyncSink) -> None:
        name = await async_client.names.get()
        assert_matches_type(BasicSharedModelObject, name, path=["response"])

    @parametrize
    async def test_raw_response_get(self, async_client: AsyncSink) -> None:
        response = await async_client.names.with_raw_response.get()

        assert response.is_closed is True
        name = response.parse()
        assert_matches_type(BasicSharedModelObject, name, path=["response"])

    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncSink) -> None:
        async with async_client.names.with_streaming_response.get() as response:
            assert not response.is_closed

            name = await response.parse()
            assert_matches_type(BasicSharedModelObject, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_properties_common_conflicts(self, async_client: AsyncSink) -> None:
        name = await async_client.names.properties_common_conflicts(
            _1_digit_leading_underscore="_1_digit_leading_underscore",
            _leading_underscore="_leading_underscore",
            _leading_underscore_mixed_case="_leading_underscore_MixedCase",
            bool=True,
            bool_2=True,
            date=parse_date("2019-12-27"),
            date_2=parse_date("2019-12-27"),
            float=0,
            float_2=0,
            int=0,
            int_2=0,
        )
        assert_matches_type(NamePropertiesCommonConflictsResponse, name, path=["response"])

    @parametrize
    async def test_raw_response_properties_common_conflicts(self, async_client: AsyncSink) -> None:
        response = await async_client.names.with_raw_response.properties_common_conflicts(
            _1_digit_leading_underscore="_1_digit_leading_underscore",
            _leading_underscore="_leading_underscore",
            _leading_underscore_mixed_case="_leading_underscore_MixedCase",
            bool=True,
            bool_2=True,
            date=parse_date("2019-12-27"),
            date_2=parse_date("2019-12-27"),
            float=0,
            float_2=0,
            int=0,
            int_2=0,
        )

        assert response.is_closed is True
        name = response.parse()
        assert_matches_type(NamePropertiesCommonConflictsResponse, name, path=["response"])

    @parametrize
    async def test_streaming_response_properties_common_conflicts(self, async_client: AsyncSink) -> None:
        async with async_client.names.with_streaming_response.properties_common_conflicts(
            _1_digit_leading_underscore="_1_digit_leading_underscore",
            _leading_underscore="_leading_underscore",
            _leading_underscore_mixed_case="_leading_underscore_MixedCase",
            bool=True,
            bool_2=True,
            date=parse_date("2019-12-27"),
            date_2=parse_date("2019-12-27"),
            float=0,
            float_2=0,
            int=0,
            int_2=0,
        ) as response:
            assert not response.is_closed

            name = await response.parse()
            assert_matches_type(NamePropertiesCommonConflictsResponse, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_properties_illegal_go_identifiers(self, async_client: AsyncSink) -> None:
        name = await async_client.names.properties_illegal_go_identifiers(
            type="type",
        )
        assert_matches_type(NamePropertiesIllegalGoIdentifiersResponse, name, path=["response"])

    @parametrize
    async def test_method_properties_illegal_go_identifiers_with_all_params(self, async_client: AsyncSink) -> None:
        name = await async_client.names.properties_illegal_go_identifiers(
            type="type",
            defer="defer",
        )
        assert_matches_type(NamePropertiesIllegalGoIdentifiersResponse, name, path=["response"])

    @parametrize
    async def test_raw_response_properties_illegal_go_identifiers(self, async_client: AsyncSink) -> None:
        response = await async_client.names.with_raw_response.properties_illegal_go_identifiers(
            type="type",
        )

        assert response.is_closed is True
        name = response.parse()
        assert_matches_type(NamePropertiesIllegalGoIdentifiersResponse, name, path=["response"])

    @parametrize
    async def test_streaming_response_properties_illegal_go_identifiers(self, async_client: AsyncSink) -> None:
        async with async_client.names.with_streaming_response.properties_illegal_go_identifiers(
            type="type",
        ) as response:
            assert not response.is_closed

            name = await response.parse()
            assert_matches_type(NamePropertiesIllegalGoIdentifiersResponse, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_properties_illegal_go_identifiers(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `type` but received ''"):
            await async_client.names.with_raw_response.properties_illegal_go_identifiers(
                type="",
            )

    @parametrize
    async def test_method_properties_illegal_javascript_identifiers_overload_1(self, async_client: AsyncSink) -> None:
        name = await async_client.names.properties_illegal_javascript_identifiers()
        assert_matches_type(NamePropertiesIllegalJavascriptIdentifiersResponse, name, path=["response"])

    @parametrize
    async def test_method_properties_illegal_javascript_identifiers_with_all_params_overload_1(
        self, async_client: AsyncSink
    ) -> None:
        name = await async_client.names.properties_illegal_javascript_identifiers(
            irrelevant=0,
        )
        assert_matches_type(NamePropertiesIllegalJavascriptIdentifiersResponse, name, path=["response"])

    @parametrize
    async def test_raw_response_properties_illegal_javascript_identifiers_overload_1(
        self, async_client: AsyncSink
    ) -> None:
        response = await async_client.names.with_raw_response.properties_illegal_javascript_identifiers()

        assert response.is_closed is True
        name = response.parse()
        assert_matches_type(NamePropertiesIllegalJavascriptIdentifiersResponse, name, path=["response"])

    @parametrize
    async def test_streaming_response_properties_illegal_javascript_identifiers_overload_1(
        self, async_client: AsyncSink
    ) -> None:
        async with async_client.names.with_streaming_response.properties_illegal_javascript_identifiers() as response:
            assert not response.is_closed

            name = await response.parse()
            assert_matches_type(NamePropertiesIllegalJavascriptIdentifiersResponse, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_properties_illegal_javascript_identifiers_overload_2(self, async_client: AsyncSink) -> None:
        name = await async_client.names.properties_illegal_javascript_identifiers(
            body=0,
        )
        assert_matches_type(NamePropertiesIllegalJavascriptIdentifiersResponse, name, path=["response"])

    @parametrize
    async def test_raw_response_properties_illegal_javascript_identifiers_overload_2(
        self, async_client: AsyncSink
    ) -> None:
        response = await async_client.names.with_raw_response.properties_illegal_javascript_identifiers(
            body=0,
        )

        assert response.is_closed is True
        name = response.parse()
        assert_matches_type(NamePropertiesIllegalJavascriptIdentifiersResponse, name, path=["response"])

    @parametrize
    async def test_streaming_response_properties_illegal_javascript_identifiers_overload_2(
        self, async_client: AsyncSink
    ) -> None:
        async with async_client.names.with_streaming_response.properties_illegal_javascript_identifiers(
            body=0,
        ) as response:
            assert not response.is_closed

            name = await response.parse()
            assert_matches_type(NamePropertiesIllegalJavascriptIdentifiersResponse, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_response_property_clashes_model_import(self, async_client: AsyncSink) -> None:
        name = await async_client.names.response_property_clashes_model_import()
        assert_matches_type(NameResponsePropertyClashesModelImportResponse, name, path=["response"])

    @parametrize
    async def test_raw_response_response_property_clashes_model_import(self, async_client: AsyncSink) -> None:
        response = await async_client.names.with_raw_response.response_property_clashes_model_import()

        assert response.is_closed is True
        name = response.parse()
        assert_matches_type(NameResponsePropertyClashesModelImportResponse, name, path=["response"])

    @parametrize
    async def test_streaming_response_response_property_clashes_model_import(self, async_client: AsyncSink) -> None:
        async with async_client.names.with_streaming_response.response_property_clashes_model_import() as response:
            assert not response.is_closed

            name = await response.parse()
            assert_matches_type(NameResponsePropertyClashesModelImportResponse, name, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_response_shadows_pydantic(self, async_client: AsyncSink) -> None:
        name = await async_client.names.response_shadows_pydantic()
        assert_matches_type(NameResponseShadowsPydanticResponse, name, path=["response"])

    @parametrize
    async def test_raw_response_response_shadows_pydantic(self, async_client: AsyncSink) -> None:
        response = await async_client.names.with_raw_response.response_shadows_pydantic()

        assert response.is_closed is True
        name = response.parse()
        assert_matches_type(NameResponseShadowsPydanticResponse, name, path=["response"])

    @parametrize
    async def test_streaming_response_response_shadows_pydantic(self, async_client: AsyncSink) -> None:
        async with async_client.names.with_streaming_response.response_shadows_pydantic() as response:
            assert not response.is_closed

            name = await response.parse()
            assert_matches_type(NameResponseShadowsPydanticResponse, name, path=["response"])

        assert cast(Any, response.is_closed) is True
