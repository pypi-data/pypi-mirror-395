# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from sink.api.sdk import Sink, AsyncSink
from sink.api.sdk.types import (
    PathParamMultipleResponse,
    PathParamSingularResponse,
    PathParamQueryParamResponse,
    PathParamColonSuffixResponse,
    PathParamFileExtensionResponse,
)
from sink.api.sdk._utils import parse_date, parse_datetime
from sink.api.sdk.types.shared import BasicSharedModelObject

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPathParams:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_colon_suffix(self, client: Sink) -> None:
        path_param = client.path_params.colon_suffix(
            0,
        )
        assert_matches_type(PathParamColonSuffixResponse, path_param, path=["response"])

    @parametrize
    def test_raw_response_colon_suffix(self, client: Sink) -> None:
        response = client.path_params.with_raw_response.colon_suffix(
            0,
        )

        assert response.is_closed is True
        path_param = response.parse()
        assert_matches_type(PathParamColonSuffixResponse, path_param, path=["response"])

    @parametrize
    def test_streaming_response_colon_suffix(self, client: Sink) -> None:
        with client.path_params.with_streaming_response.colon_suffix(
            0,
        ) as response:
            assert not response.is_closed

            path_param = response.parse()
            assert_matches_type(PathParamColonSuffixResponse, path_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism is broken")
    @parametrize
    def test_method_dashed_param(self, client: Sink) -> None:
        path_param = client.path_params.dashed_param(
            "dashed-param",
        )
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @pytest.mark.skip(reason="prism is broken")
    @parametrize
    def test_raw_response_dashed_param(self, client: Sink) -> None:
        response = client.path_params.with_raw_response.dashed_param(
            "dashed-param",
        )

        assert response.is_closed is True
        path_param = response.parse()
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @pytest.mark.skip(reason="prism is broken")
    @parametrize
    def test_streaming_response_dashed_param(self, client: Sink) -> None:
        with client.path_params.with_streaming_response.dashed_param(
            "dashed-param",
        ) as response:
            assert not response.is_closed

            path_param = response.parse()
            assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism is broken")
    @parametrize
    def test_path_params_dashed_param(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dashed_param` but received ''"):
            client.path_params.with_raw_response.dashed_param(
                "",
            )

    @parametrize
    def test_method_date_param(self, client: Sink) -> None:
        path_param = client.path_params.date_param(
            parse_date("2023-09-01"),
        )
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @parametrize
    def test_raw_response_date_param(self, client: Sink) -> None:
        response = client.path_params.with_raw_response.date_param(
            parse_date("2023-09-01"),
        )

        assert response.is_closed is True
        path_param = response.parse()
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @parametrize
    def test_streaming_response_date_param(self, client: Sink) -> None:
        with client.path_params.with_streaming_response.date_param(
            parse_date("2023-09-01"),
        ) as response:
            assert not response.is_closed

            path_param = response.parse()
            assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_date_param(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `date_param` but received ''"):
            client.path_params.with_raw_response.date_param(
                "",
            )

    @parametrize
    def test_method_datetime_param(self, client: Sink) -> None:
        path_param = client.path_params.datetime_param(
            parse_datetime("2021-06-28T22:53:15Z"),
        )
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @parametrize
    def test_raw_response_datetime_param(self, client: Sink) -> None:
        response = client.path_params.with_raw_response.datetime_param(
            parse_datetime("2021-06-28T22:53:15Z"),
        )

        assert response.is_closed is True
        path_param = response.parse()
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @parametrize
    def test_streaming_response_datetime_param(self, client: Sink) -> None:
        with client.path_params.with_streaming_response.datetime_param(
            parse_datetime("2021-06-28T22:53:15Z"),
        ) as response:
            assert not response.is_closed

            path_param = response.parse()
            assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_datetime_param(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `datetime_param` but received ''"):
            client.path_params.with_raw_response.datetime_param(
                "",
            )

    @parametrize
    def test_method_enum_param(self, client: Sink) -> None:
        path_param = client.path_params.enum_param(
            "A",
        )
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @parametrize
    def test_raw_response_enum_param(self, client: Sink) -> None:
        response = client.path_params.with_raw_response.enum_param(
            "A",
        )

        assert response.is_closed is True
        path_param = response.parse()
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @parametrize
    def test_streaming_response_enum_param(self, client: Sink) -> None:
        with client.path_params.with_streaming_response.enum_param(
            "A",
        ) as response:
            assert not response.is_closed

            path_param = response.parse()
            assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_file_extension(self, client: Sink) -> None:
        path_param = client.path_params.file_extension(
            0,
        )
        assert_matches_type(PathParamFileExtensionResponse, path_param, path=["response"])

    @parametrize
    def test_raw_response_file_extension(self, client: Sink) -> None:
        response = client.path_params.with_raw_response.file_extension(
            0,
        )

        assert response.is_closed is True
        path_param = response.parse()
        assert_matches_type(PathParamFileExtensionResponse, path_param, path=["response"])

    @parametrize
    def test_streaming_response_file_extension(self, client: Sink) -> None:
        with client.path_params.with_streaming_response.file_extension(
            0,
        ) as response:
            assert not response.is_closed

            path_param = response.parse()
            assert_matches_type(PathParamFileExtensionResponse, path_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism is broken")
    @parametrize
    def test_method_integer_param(self, client: Sink) -> None:
        path_param = client.path_params.integer_param(
            0,
        )
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @pytest.mark.skip(reason="prism is broken")
    @parametrize
    def test_raw_response_integer_param(self, client: Sink) -> None:
        response = client.path_params.with_raw_response.integer_param(
            0,
        )

        assert response.is_closed is True
        path_param = response.parse()
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @pytest.mark.skip(reason="prism is broken")
    @parametrize
    def test_streaming_response_integer_param(self, client: Sink) -> None:
        with client.path_params.with_streaming_response.integer_param(
            0,
        ) as response:
            assert not response.is_closed

            path_param = response.parse()
            assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_multiple(self, client: Sink) -> None:
        path_param = client.path_params.multiple(
            last="last",
            first="first",
            second="second",
        )
        assert_matches_type(PathParamMultipleResponse, path_param, path=["response"])

    @parametrize
    def test_raw_response_multiple(self, client: Sink) -> None:
        response = client.path_params.with_raw_response.multiple(
            last="last",
            first="first",
            second="second",
        )

        assert response.is_closed is True
        path_param = response.parse()
        assert_matches_type(PathParamMultipleResponse, path_param, path=["response"])

    @parametrize
    def test_streaming_response_multiple(self, client: Sink) -> None:
        with client.path_params.with_streaming_response.multiple(
            last="last",
            first="first",
            second="second",
        ) as response:
            assert not response.is_closed

            path_param = response.parse()
            assert_matches_type(PathParamMultipleResponse, path_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_multiple(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `first` but received ''"):
            client.path_params.with_raw_response.multiple(
                last="last",
                first="",
                second="second",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `second` but received ''"):
            client.path_params.with_raw_response.multiple(
                last="last",
                first="first",
                second="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `last` but received ''"):
            client.path_params.with_raw_response.multiple(
                last="",
                first="first",
                second="second",
            )

    @parametrize
    def test_method_nullable_params(self, client: Sink) -> None:
        path_param = client.path_params.nullable_params(
            nullable_param_3="foo",
            nullable_param_1="nullable_param_1",
            nullable_param_2="nullable_param_2",
        )
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @parametrize
    def test_method_nullable_params_with_all_params(self, client: Sink) -> None:
        path_param = client.path_params.nullable_params(
            nullable_param_3="foo",
            nullable_param_1="nullable_param_1",
            nullable_param_2="nullable_param_2",
            foo="foo",
        )
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @parametrize
    def test_raw_response_nullable_params(self, client: Sink) -> None:
        response = client.path_params.with_raw_response.nullable_params(
            nullable_param_3="foo",
            nullable_param_1="nullable_param_1",
            nullable_param_2="nullable_param_2",
        )

        assert response.is_closed is True
        path_param = response.parse()
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @parametrize
    def test_streaming_response_nullable_params(self, client: Sink) -> None:
        with client.path_params.with_streaming_response.nullable_params(
            nullable_param_3="foo",
            nullable_param_1="nullable_param_1",
            nullable_param_2="nullable_param_2",
        ) as response:
            assert not response.is_closed

            path_param = response.parse()
            assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_nullable_params(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `nullable_param_1` but received ''"):
            client.path_params.with_raw_response.nullable_params(
                nullable_param_3="foo",
                nullable_param_1="",
                nullable_param_2="nullable_param_2",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `nullable_param_2` but received ''"):
            client.path_params.with_raw_response.nullable_params(
                nullable_param_3="foo",
                nullable_param_1="nullable_param_1",
                nullable_param_2="",
            )

    @parametrize
    def test_method_params_mixed_types(self, client: Sink) -> None:
        path_param = client.path_params.params_mixed_types(
            string_param="string_param",
            integer_param=0,
        )
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @parametrize
    def test_raw_response_params_mixed_types(self, client: Sink) -> None:
        response = client.path_params.with_raw_response.params_mixed_types(
            string_param="string_param",
            integer_param=0,
        )

        assert response.is_closed is True
        path_param = response.parse()
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @parametrize
    def test_streaming_response_params_mixed_types(self, client: Sink) -> None:
        with client.path_params.with_streaming_response.params_mixed_types(
            string_param="string_param",
            integer_param=0,
        ) as response:
            assert not response.is_closed

            path_param = response.parse()
            assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_params_mixed_types(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `string_param` but received ''"):
            client.path_params.with_raw_response.params_mixed_types(
                string_param="",
                integer_param=0,
            )

    @parametrize
    def test_method_query_param(self, client: Sink) -> None:
        path_param = client.path_params.query_param(
            0,
        )
        assert_matches_type(PathParamQueryParamResponse, path_param, path=["response"])

    @parametrize
    def test_raw_response_query_param(self, client: Sink) -> None:
        response = client.path_params.with_raw_response.query_param(
            0,
        )

        assert response.is_closed is True
        path_param = response.parse()
        assert_matches_type(PathParamQueryParamResponse, path_param, path=["response"])

    @parametrize
    def test_streaming_response_query_param(self, client: Sink) -> None:
        with client.path_params.with_streaming_response.query_param(
            0,
        ) as response:
            assert not response.is_closed

            path_param = response.parse()
            assert_matches_type(PathParamQueryParamResponse, path_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_singular(self, client: Sink) -> None:
        path_param = client.path_params.singular(
            "singular",
        )
        assert_matches_type(PathParamSingularResponse, path_param, path=["response"])

    @parametrize
    def test_raw_response_singular(self, client: Sink) -> None:
        response = client.path_params.with_raw_response.singular(
            "singular",
        )

        assert response.is_closed is True
        path_param = response.parse()
        assert_matches_type(PathParamSingularResponse, path_param, path=["response"])

    @parametrize
    def test_streaming_response_singular(self, client: Sink) -> None:
        with client.path_params.with_streaming_response.singular(
            "singular",
        ) as response:
            assert not response.is_closed

            path_param = response.parse()
            assert_matches_type(PathParamSingularResponse, path_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_singular(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `singular` but received ''"):
            client.path_params.with_raw_response.singular(
                "",
            )


class TestAsyncPathParams:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_colon_suffix(self, async_client: AsyncSink) -> None:
        path_param = await async_client.path_params.colon_suffix(
            0,
        )
        assert_matches_type(PathParamColonSuffixResponse, path_param, path=["response"])

    @parametrize
    async def test_raw_response_colon_suffix(self, async_client: AsyncSink) -> None:
        response = await async_client.path_params.with_raw_response.colon_suffix(
            0,
        )

        assert response.is_closed is True
        path_param = response.parse()
        assert_matches_type(PathParamColonSuffixResponse, path_param, path=["response"])

    @parametrize
    async def test_streaming_response_colon_suffix(self, async_client: AsyncSink) -> None:
        async with async_client.path_params.with_streaming_response.colon_suffix(
            0,
        ) as response:
            assert not response.is_closed

            path_param = await response.parse()
            assert_matches_type(PathParamColonSuffixResponse, path_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism is broken")
    @parametrize
    async def test_method_dashed_param(self, async_client: AsyncSink) -> None:
        path_param = await async_client.path_params.dashed_param(
            "dashed-param",
        )
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @pytest.mark.skip(reason="prism is broken")
    @parametrize
    async def test_raw_response_dashed_param(self, async_client: AsyncSink) -> None:
        response = await async_client.path_params.with_raw_response.dashed_param(
            "dashed-param",
        )

        assert response.is_closed is True
        path_param = response.parse()
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @pytest.mark.skip(reason="prism is broken")
    @parametrize
    async def test_streaming_response_dashed_param(self, async_client: AsyncSink) -> None:
        async with async_client.path_params.with_streaming_response.dashed_param(
            "dashed-param",
        ) as response:
            assert not response.is_closed

            path_param = await response.parse()
            assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism is broken")
    @parametrize
    async def test_path_params_dashed_param(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dashed_param` but received ''"):
            await async_client.path_params.with_raw_response.dashed_param(
                "",
            )

    @parametrize
    async def test_method_date_param(self, async_client: AsyncSink) -> None:
        path_param = await async_client.path_params.date_param(
            parse_date("2023-09-01"),
        )
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @parametrize
    async def test_raw_response_date_param(self, async_client: AsyncSink) -> None:
        response = await async_client.path_params.with_raw_response.date_param(
            parse_date("2023-09-01"),
        )

        assert response.is_closed is True
        path_param = response.parse()
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @parametrize
    async def test_streaming_response_date_param(self, async_client: AsyncSink) -> None:
        async with async_client.path_params.with_streaming_response.date_param(
            parse_date("2023-09-01"),
        ) as response:
            assert not response.is_closed

            path_param = await response.parse()
            assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_date_param(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `date_param` but received ''"):
            await async_client.path_params.with_raw_response.date_param(
                "",
            )

    @parametrize
    async def test_method_datetime_param(self, async_client: AsyncSink) -> None:
        path_param = await async_client.path_params.datetime_param(
            parse_datetime("2021-06-28T22:53:15Z"),
        )
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @parametrize
    async def test_raw_response_datetime_param(self, async_client: AsyncSink) -> None:
        response = await async_client.path_params.with_raw_response.datetime_param(
            parse_datetime("2021-06-28T22:53:15Z"),
        )

        assert response.is_closed is True
        path_param = response.parse()
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @parametrize
    async def test_streaming_response_datetime_param(self, async_client: AsyncSink) -> None:
        async with async_client.path_params.with_streaming_response.datetime_param(
            parse_datetime("2021-06-28T22:53:15Z"),
        ) as response:
            assert not response.is_closed

            path_param = await response.parse()
            assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_datetime_param(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `datetime_param` but received ''"):
            await async_client.path_params.with_raw_response.datetime_param(
                "",
            )

    @parametrize
    async def test_method_enum_param(self, async_client: AsyncSink) -> None:
        path_param = await async_client.path_params.enum_param(
            "A",
        )
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @parametrize
    async def test_raw_response_enum_param(self, async_client: AsyncSink) -> None:
        response = await async_client.path_params.with_raw_response.enum_param(
            "A",
        )

        assert response.is_closed is True
        path_param = response.parse()
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @parametrize
    async def test_streaming_response_enum_param(self, async_client: AsyncSink) -> None:
        async with async_client.path_params.with_streaming_response.enum_param(
            "A",
        ) as response:
            assert not response.is_closed

            path_param = await response.parse()
            assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_file_extension(self, async_client: AsyncSink) -> None:
        path_param = await async_client.path_params.file_extension(
            0,
        )
        assert_matches_type(PathParamFileExtensionResponse, path_param, path=["response"])

    @parametrize
    async def test_raw_response_file_extension(self, async_client: AsyncSink) -> None:
        response = await async_client.path_params.with_raw_response.file_extension(
            0,
        )

        assert response.is_closed is True
        path_param = response.parse()
        assert_matches_type(PathParamFileExtensionResponse, path_param, path=["response"])

    @parametrize
    async def test_streaming_response_file_extension(self, async_client: AsyncSink) -> None:
        async with async_client.path_params.with_streaming_response.file_extension(
            0,
        ) as response:
            assert not response.is_closed

            path_param = await response.parse()
            assert_matches_type(PathParamFileExtensionResponse, path_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism is broken")
    @parametrize
    async def test_method_integer_param(self, async_client: AsyncSink) -> None:
        path_param = await async_client.path_params.integer_param(
            0,
        )
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @pytest.mark.skip(reason="prism is broken")
    @parametrize
    async def test_raw_response_integer_param(self, async_client: AsyncSink) -> None:
        response = await async_client.path_params.with_raw_response.integer_param(
            0,
        )

        assert response.is_closed is True
        path_param = response.parse()
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @pytest.mark.skip(reason="prism is broken")
    @parametrize
    async def test_streaming_response_integer_param(self, async_client: AsyncSink) -> None:
        async with async_client.path_params.with_streaming_response.integer_param(
            0,
        ) as response:
            assert not response.is_closed

            path_param = await response.parse()
            assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_multiple(self, async_client: AsyncSink) -> None:
        path_param = await async_client.path_params.multiple(
            last="last",
            first="first",
            second="second",
        )
        assert_matches_type(PathParamMultipleResponse, path_param, path=["response"])

    @parametrize
    async def test_raw_response_multiple(self, async_client: AsyncSink) -> None:
        response = await async_client.path_params.with_raw_response.multiple(
            last="last",
            first="first",
            second="second",
        )

        assert response.is_closed is True
        path_param = response.parse()
        assert_matches_type(PathParamMultipleResponse, path_param, path=["response"])

    @parametrize
    async def test_streaming_response_multiple(self, async_client: AsyncSink) -> None:
        async with async_client.path_params.with_streaming_response.multiple(
            last="last",
            first="first",
            second="second",
        ) as response:
            assert not response.is_closed

            path_param = await response.parse()
            assert_matches_type(PathParamMultipleResponse, path_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_multiple(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `first` but received ''"):
            await async_client.path_params.with_raw_response.multiple(
                last="last",
                first="",
                second="second",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `second` but received ''"):
            await async_client.path_params.with_raw_response.multiple(
                last="last",
                first="first",
                second="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `last` but received ''"):
            await async_client.path_params.with_raw_response.multiple(
                last="",
                first="first",
                second="second",
            )

    @parametrize
    async def test_method_nullable_params(self, async_client: AsyncSink) -> None:
        path_param = await async_client.path_params.nullable_params(
            nullable_param_3="foo",
            nullable_param_1="nullable_param_1",
            nullable_param_2="nullable_param_2",
        )
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @parametrize
    async def test_method_nullable_params_with_all_params(self, async_client: AsyncSink) -> None:
        path_param = await async_client.path_params.nullable_params(
            nullable_param_3="foo",
            nullable_param_1="nullable_param_1",
            nullable_param_2="nullable_param_2",
            foo="foo",
        )
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @parametrize
    async def test_raw_response_nullable_params(self, async_client: AsyncSink) -> None:
        response = await async_client.path_params.with_raw_response.nullable_params(
            nullable_param_3="foo",
            nullable_param_1="nullable_param_1",
            nullable_param_2="nullable_param_2",
        )

        assert response.is_closed is True
        path_param = response.parse()
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @parametrize
    async def test_streaming_response_nullable_params(self, async_client: AsyncSink) -> None:
        async with async_client.path_params.with_streaming_response.nullable_params(
            nullable_param_3="foo",
            nullable_param_1="nullable_param_1",
            nullable_param_2="nullable_param_2",
        ) as response:
            assert not response.is_closed

            path_param = await response.parse()
            assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_nullable_params(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `nullable_param_1` but received ''"):
            await async_client.path_params.with_raw_response.nullable_params(
                nullable_param_3="foo",
                nullable_param_1="",
                nullable_param_2="nullable_param_2",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `nullable_param_2` but received ''"):
            await async_client.path_params.with_raw_response.nullable_params(
                nullable_param_3="foo",
                nullable_param_1="nullable_param_1",
                nullable_param_2="",
            )

    @parametrize
    async def test_method_params_mixed_types(self, async_client: AsyncSink) -> None:
        path_param = await async_client.path_params.params_mixed_types(
            string_param="string_param",
            integer_param=0,
        )
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @parametrize
    async def test_raw_response_params_mixed_types(self, async_client: AsyncSink) -> None:
        response = await async_client.path_params.with_raw_response.params_mixed_types(
            string_param="string_param",
            integer_param=0,
        )

        assert response.is_closed is True
        path_param = response.parse()
        assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

    @parametrize
    async def test_streaming_response_params_mixed_types(self, async_client: AsyncSink) -> None:
        async with async_client.path_params.with_streaming_response.params_mixed_types(
            string_param="string_param",
            integer_param=0,
        ) as response:
            assert not response.is_closed

            path_param = await response.parse()
            assert_matches_type(BasicSharedModelObject, path_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_params_mixed_types(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `string_param` but received ''"):
            await async_client.path_params.with_raw_response.params_mixed_types(
                string_param="",
                integer_param=0,
            )

    @parametrize
    async def test_method_query_param(self, async_client: AsyncSink) -> None:
        path_param = await async_client.path_params.query_param(
            0,
        )
        assert_matches_type(PathParamQueryParamResponse, path_param, path=["response"])

    @parametrize
    async def test_raw_response_query_param(self, async_client: AsyncSink) -> None:
        response = await async_client.path_params.with_raw_response.query_param(
            0,
        )

        assert response.is_closed is True
        path_param = response.parse()
        assert_matches_type(PathParamQueryParamResponse, path_param, path=["response"])

    @parametrize
    async def test_streaming_response_query_param(self, async_client: AsyncSink) -> None:
        async with async_client.path_params.with_streaming_response.query_param(
            0,
        ) as response:
            assert not response.is_closed

            path_param = await response.parse()
            assert_matches_type(PathParamQueryParamResponse, path_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_singular(self, async_client: AsyncSink) -> None:
        path_param = await async_client.path_params.singular(
            "singular",
        )
        assert_matches_type(PathParamSingularResponse, path_param, path=["response"])

    @parametrize
    async def test_raw_response_singular(self, async_client: AsyncSink) -> None:
        response = await async_client.path_params.with_raw_response.singular(
            "singular",
        )

        assert response.is_closed is True
        path_param = response.parse()
        assert_matches_type(PathParamSingularResponse, path_param, path=["response"])

    @parametrize
    async def test_streaming_response_singular(self, async_client: AsyncSink) -> None:
        async with async_client.path_params.with_streaming_response.singular(
            "singular",
        ) as response:
            assert not response.is_closed

            path_param = await response.parse()
            assert_matches_type(PathParamSingularResponse, path_param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_singular(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `singular` but received ''"):
            await async_client.path_params.with_raw_response.singular(
                "",
            )
