# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sink.api.sdk import Sink, AsyncSink

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPositionalParams:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_basic_body(self, client: Sink) -> None:
        positional_param = client.positional_params.basic_body(
            key1="key1",
        )
        assert positional_param is None

    @parametrize
    def test_method_basic_body_with_all_params(self, client: Sink) -> None:
        positional_param = client.positional_params.basic_body(
            key1="key1",
            options="options",
        )
        assert positional_param is None

    @parametrize
    def test_raw_response_basic_body(self, client: Sink) -> None:
        response = client.positional_params.with_raw_response.basic_body(
            key1="key1",
        )

        assert response.is_closed is True
        positional_param = response.parse()
        assert positional_param is None

    @parametrize
    def test_streaming_response_basic_body(self, client: Sink) -> None:
        with client.positional_params.with_streaming_response.basic_body(
            key1="key1",
        ) as response:
            assert not response.is_closed

            positional_param = response.parse()
            assert positional_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_basic_query(self, client: Sink) -> None:
        positional_param = client.positional_params.basic_query(
            key1="key1",
        )
        assert positional_param is None

    @parametrize
    def test_raw_response_basic_query(self, client: Sink) -> None:
        response = client.positional_params.with_raw_response.basic_query(
            key1="key1",
        )

        assert response.is_closed is True
        positional_param = response.parse()
        assert positional_param is None

    @parametrize
    def test_streaming_response_basic_query(self, client: Sink) -> None:
        with client.positional_params.with_streaming_response.basic_query(
            key1="key1",
        ) as response:
            assert not response.is_closed

            positional_param = response.parse()
            assert positional_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_body(self, client: Sink) -> None:
        positional_param = client.positional_params.body()
        assert positional_param is None

    @parametrize
    def test_method_body_with_all_params(self, client: Sink) -> None:
        positional_param = client.positional_params.body(
            foo="foo",
        )
        assert positional_param is None

    @parametrize
    def test_raw_response_body(self, client: Sink) -> None:
        response = client.positional_params.with_raw_response.body()

        assert response.is_closed is True
        positional_param = response.parse()
        assert positional_param is None

    @parametrize
    def test_streaming_response_body(self, client: Sink) -> None:
        with client.positional_params.with_streaming_response.body() as response:
            assert not response.is_closed

            positional_param = response.parse()
            assert positional_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_body_extra_param(self, client: Sink) -> None:
        positional_param = client.positional_params.body_extra_param(
            extra_key="extra_key",
        )
        assert positional_param is None

    @parametrize
    def test_method_body_extra_param_with_all_params(self, client: Sink) -> None:
        positional_param = client.positional_params.body_extra_param(
            extra_key="extra_key",
            foo="foo",
        )
        assert positional_param is None

    @parametrize
    def test_raw_response_body_extra_param(self, client: Sink) -> None:
        response = client.positional_params.with_raw_response.body_extra_param(
            extra_key="extra_key",
        )

        assert response.is_closed is True
        positional_param = response.parse()
        assert positional_param is None

    @parametrize
    def test_streaming_response_body_extra_param(self, client: Sink) -> None:
        with client.positional_params.with_streaming_response.body_extra_param(
            extra_key="extra_key",
        ) as response:
            assert not response.is_closed

            positional_param = response.parse()
            assert positional_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_kitchen_sink(self, client: Sink) -> None:
        positional_param = client.positional_params.kitchen_sink(
            id="id",
            key="key",
            im_a_camel="imACamel",
            option1=True,
            camel_case="camel_case",
        )
        assert positional_param is None

    @parametrize
    def test_method_kitchen_sink_with_all_params(self, client: Sink) -> None:
        positional_param = client.positional_params.kitchen_sink(
            id="id",
            key="key",
            im_a_camel="imACamel",
            option1=True,
            camel_case="camel_case",
            option2="option2",
            really_cool_snake="really_cool_snake",
            bar=0,
            options="options",
            x_custom_header="X-Custom-Header",
        )
        assert positional_param is None

    @parametrize
    def test_raw_response_kitchen_sink(self, client: Sink) -> None:
        response = client.positional_params.with_raw_response.kitchen_sink(
            id="id",
            key="key",
            im_a_camel="imACamel",
            option1=True,
            camel_case="camel_case",
        )

        assert response.is_closed is True
        positional_param = response.parse()
        assert positional_param is None

    @parametrize
    def test_streaming_response_kitchen_sink(self, client: Sink) -> None:
        with client.positional_params.with_streaming_response.kitchen_sink(
            id="id",
            key="key",
            im_a_camel="imACamel",
            option1=True,
            camel_case="camel_case",
        ) as response:
            assert not response.is_closed

            positional_param = response.parse()
            assert positional_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_kitchen_sink(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.positional_params.with_raw_response.kitchen_sink(
                id="",
                key="key",
                im_a_camel="imACamel",
                option1=True,
                camel_case="camel_case",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `key` but received ''"):
            client.positional_params.with_raw_response.kitchen_sink(
                id="id",
                key="",
                im_a_camel="imACamel",
                option1=True,
                camel_case="camel_case",
            )

    @parametrize
    def test_method_multiple_path_params(self, client: Sink) -> None:
        positional_param = client.positional_params.multiple_path_params(
            second="second",
            first="first",
            last="last",
            name="name",
        )
        assert positional_param is None

    @parametrize
    def test_method_multiple_path_params_with_all_params(self, client: Sink) -> None:
        positional_param = client.positional_params.multiple_path_params(
            second="second",
            first="first",
            last="last",
            name="name",
            options="options",
        )
        assert positional_param is None

    @parametrize
    def test_raw_response_multiple_path_params(self, client: Sink) -> None:
        response = client.positional_params.with_raw_response.multiple_path_params(
            second="second",
            first="first",
            last="last",
            name="name",
        )

        assert response.is_closed is True
        positional_param = response.parse()
        assert positional_param is None

    @parametrize
    def test_streaming_response_multiple_path_params(self, client: Sink) -> None:
        with client.positional_params.with_streaming_response.multiple_path_params(
            second="second",
            first="first",
            last="last",
            name="name",
        ) as response:
            assert not response.is_closed

            positional_param = response.parse()
            assert positional_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_multiple_path_params(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `first` but received ''"):
            client.positional_params.with_raw_response.multiple_path_params(
                second="second",
                first="",
                last="last",
                name="name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `second` but received ''"):
            client.positional_params.with_raw_response.multiple_path_params(
                second="",
                first="first",
                last="last",
                name="name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `last` but received ''"):
            client.positional_params.with_raw_response.multiple_path_params(
                second="second",
                first="first",
                last="",
                name="name",
            )

    @parametrize
    def test_method_query(self, client: Sink) -> None:
        positional_param = client.positional_params.query(
            foo="foo",
        )
        assert positional_param is None

    @parametrize
    def test_raw_response_query(self, client: Sink) -> None:
        response = client.positional_params.with_raw_response.query(
            foo="foo",
        )

        assert response.is_closed is True
        positional_param = response.parse()
        assert positional_param is None

    @parametrize
    def test_streaming_response_query(self, client: Sink) -> None:
        with client.positional_params.with_streaming_response.query(
            foo="foo",
        ) as response:
            assert not response.is_closed

            positional_param = response.parse()
            assert positional_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_query_and_path(self, client: Sink) -> None:
        positional_param = client.positional_params.query_and_path(
            id="id",
            bar=0,
        )
        assert positional_param is None

    @parametrize
    def test_raw_response_query_and_path(self, client: Sink) -> None:
        response = client.positional_params.with_raw_response.query_and_path(
            id="id",
            bar=0,
        )

        assert response.is_closed is True
        positional_param = response.parse()
        assert positional_param is None

    @parametrize
    def test_streaming_response_query_and_path(self, client: Sink) -> None:
        with client.positional_params.with_streaming_response.query_and_path(
            id="id",
            bar=0,
        ) as response:
            assert not response.is_closed

            positional_param = response.parse()
            assert positional_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_query_and_path(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.positional_params.with_raw_response.query_and_path(
                id="",
                bar=0,
            )

    @parametrize
    def test_method_query_multiple(self, client: Sink) -> None:
        positional_param = client.positional_params.query_multiple(
            bar="bar",
            foo="foo",
        )
        assert positional_param is None

    @parametrize
    def test_raw_response_query_multiple(self, client: Sink) -> None:
        response = client.positional_params.with_raw_response.query_multiple(
            bar="bar",
            foo="foo",
        )

        assert response.is_closed is True
        positional_param = response.parse()
        assert positional_param is None

    @parametrize
    def test_streaming_response_query_multiple(self, client: Sink) -> None:
        with client.positional_params.with_streaming_response.query_multiple(
            bar="bar",
            foo="foo",
        ) as response:
            assert not response.is_closed

            positional_param = response.parse()
            assert positional_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_single(self, client: Sink) -> None:
        positional_param = client.positional_params.single(
            "single",
        )
        assert positional_param is None

    @parametrize
    def test_raw_response_single(self, client: Sink) -> None:
        response = client.positional_params.with_raw_response.single(
            "single",
        )

        assert response.is_closed is True
        positional_param = response.parse()
        assert positional_param is None

    @parametrize
    def test_streaming_response_single(self, client: Sink) -> None:
        with client.positional_params.with_streaming_response.single(
            "single",
        ) as response:
            assert not response.is_closed

            positional_param = response.parse()
            assert positional_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_single(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `single` but received ''"):
            client.positional_params.with_raw_response.single(
                "",
            )

    @parametrize
    def test_method_union_body_and_path(self, client: Sink) -> None:
        positional_param = client.positional_params.union_body_and_path(
            id="id",
            kind="VIRTUAL",
        )
        assert positional_param is None

    @parametrize
    def test_raw_response_union_body_and_path(self, client: Sink) -> None:
        response = client.positional_params.with_raw_response.union_body_and_path(
            id="id",
            kind="VIRTUAL",
        )

        assert response.is_closed is True
        positional_param = response.parse()
        assert positional_param is None

    @parametrize
    def test_streaming_response_union_body_and_path(self, client: Sink) -> None:
        with client.positional_params.with_streaming_response.union_body_and_path(
            id="id",
            kind="VIRTUAL",
        ) as response:
            assert not response.is_closed

            positional_param = response.parse()
            assert positional_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_union_body_and_path(self, client: Sink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.positional_params.with_raw_response.union_body_and_path(
                id="",
                kind="VIRTUAL",
            )


class TestAsyncPositionalParams:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_basic_body(self, async_client: AsyncSink) -> None:
        positional_param = await async_client.positional_params.basic_body(
            key1="key1",
        )
        assert positional_param is None

    @parametrize
    async def test_method_basic_body_with_all_params(self, async_client: AsyncSink) -> None:
        positional_param = await async_client.positional_params.basic_body(
            key1="key1",
            options="options",
        )
        assert positional_param is None

    @parametrize
    async def test_raw_response_basic_body(self, async_client: AsyncSink) -> None:
        response = await async_client.positional_params.with_raw_response.basic_body(
            key1="key1",
        )

        assert response.is_closed is True
        positional_param = response.parse()
        assert positional_param is None

    @parametrize
    async def test_streaming_response_basic_body(self, async_client: AsyncSink) -> None:
        async with async_client.positional_params.with_streaming_response.basic_body(
            key1="key1",
        ) as response:
            assert not response.is_closed

            positional_param = await response.parse()
            assert positional_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_basic_query(self, async_client: AsyncSink) -> None:
        positional_param = await async_client.positional_params.basic_query(
            key1="key1",
        )
        assert positional_param is None

    @parametrize
    async def test_raw_response_basic_query(self, async_client: AsyncSink) -> None:
        response = await async_client.positional_params.with_raw_response.basic_query(
            key1="key1",
        )

        assert response.is_closed is True
        positional_param = response.parse()
        assert positional_param is None

    @parametrize
    async def test_streaming_response_basic_query(self, async_client: AsyncSink) -> None:
        async with async_client.positional_params.with_streaming_response.basic_query(
            key1="key1",
        ) as response:
            assert not response.is_closed

            positional_param = await response.parse()
            assert positional_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_body(self, async_client: AsyncSink) -> None:
        positional_param = await async_client.positional_params.body()
        assert positional_param is None

    @parametrize
    async def test_method_body_with_all_params(self, async_client: AsyncSink) -> None:
        positional_param = await async_client.positional_params.body(
            foo="foo",
        )
        assert positional_param is None

    @parametrize
    async def test_raw_response_body(self, async_client: AsyncSink) -> None:
        response = await async_client.positional_params.with_raw_response.body()

        assert response.is_closed is True
        positional_param = response.parse()
        assert positional_param is None

    @parametrize
    async def test_streaming_response_body(self, async_client: AsyncSink) -> None:
        async with async_client.positional_params.with_streaming_response.body() as response:
            assert not response.is_closed

            positional_param = await response.parse()
            assert positional_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_body_extra_param(self, async_client: AsyncSink) -> None:
        positional_param = await async_client.positional_params.body_extra_param(
            extra_key="extra_key",
        )
        assert positional_param is None

    @parametrize
    async def test_method_body_extra_param_with_all_params(self, async_client: AsyncSink) -> None:
        positional_param = await async_client.positional_params.body_extra_param(
            extra_key="extra_key",
            foo="foo",
        )
        assert positional_param is None

    @parametrize
    async def test_raw_response_body_extra_param(self, async_client: AsyncSink) -> None:
        response = await async_client.positional_params.with_raw_response.body_extra_param(
            extra_key="extra_key",
        )

        assert response.is_closed is True
        positional_param = response.parse()
        assert positional_param is None

    @parametrize
    async def test_streaming_response_body_extra_param(self, async_client: AsyncSink) -> None:
        async with async_client.positional_params.with_streaming_response.body_extra_param(
            extra_key="extra_key",
        ) as response:
            assert not response.is_closed

            positional_param = await response.parse()
            assert positional_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_kitchen_sink(self, async_client: AsyncSink) -> None:
        positional_param = await async_client.positional_params.kitchen_sink(
            id="id",
            key="key",
            im_a_camel="imACamel",
            option1=True,
            camel_case="camel_case",
        )
        assert positional_param is None

    @parametrize
    async def test_method_kitchen_sink_with_all_params(self, async_client: AsyncSink) -> None:
        positional_param = await async_client.positional_params.kitchen_sink(
            id="id",
            key="key",
            im_a_camel="imACamel",
            option1=True,
            camel_case="camel_case",
            option2="option2",
            really_cool_snake="really_cool_snake",
            bar=0,
            options="options",
            x_custom_header="X-Custom-Header",
        )
        assert positional_param is None

    @parametrize
    async def test_raw_response_kitchen_sink(self, async_client: AsyncSink) -> None:
        response = await async_client.positional_params.with_raw_response.kitchen_sink(
            id="id",
            key="key",
            im_a_camel="imACamel",
            option1=True,
            camel_case="camel_case",
        )

        assert response.is_closed is True
        positional_param = response.parse()
        assert positional_param is None

    @parametrize
    async def test_streaming_response_kitchen_sink(self, async_client: AsyncSink) -> None:
        async with async_client.positional_params.with_streaming_response.kitchen_sink(
            id="id",
            key="key",
            im_a_camel="imACamel",
            option1=True,
            camel_case="camel_case",
        ) as response:
            assert not response.is_closed

            positional_param = await response.parse()
            assert positional_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_kitchen_sink(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.positional_params.with_raw_response.kitchen_sink(
                id="",
                key="key",
                im_a_camel="imACamel",
                option1=True,
                camel_case="camel_case",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `key` but received ''"):
            await async_client.positional_params.with_raw_response.kitchen_sink(
                id="id",
                key="",
                im_a_camel="imACamel",
                option1=True,
                camel_case="camel_case",
            )

    @parametrize
    async def test_method_multiple_path_params(self, async_client: AsyncSink) -> None:
        positional_param = await async_client.positional_params.multiple_path_params(
            second="second",
            first="first",
            last="last",
            name="name",
        )
        assert positional_param is None

    @parametrize
    async def test_method_multiple_path_params_with_all_params(self, async_client: AsyncSink) -> None:
        positional_param = await async_client.positional_params.multiple_path_params(
            second="second",
            first="first",
            last="last",
            name="name",
            options="options",
        )
        assert positional_param is None

    @parametrize
    async def test_raw_response_multiple_path_params(self, async_client: AsyncSink) -> None:
        response = await async_client.positional_params.with_raw_response.multiple_path_params(
            second="second",
            first="first",
            last="last",
            name="name",
        )

        assert response.is_closed is True
        positional_param = response.parse()
        assert positional_param is None

    @parametrize
    async def test_streaming_response_multiple_path_params(self, async_client: AsyncSink) -> None:
        async with async_client.positional_params.with_streaming_response.multiple_path_params(
            second="second",
            first="first",
            last="last",
            name="name",
        ) as response:
            assert not response.is_closed

            positional_param = await response.parse()
            assert positional_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_multiple_path_params(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `first` but received ''"):
            await async_client.positional_params.with_raw_response.multiple_path_params(
                second="second",
                first="",
                last="last",
                name="name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `second` but received ''"):
            await async_client.positional_params.with_raw_response.multiple_path_params(
                second="",
                first="first",
                last="last",
                name="name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `last` but received ''"):
            await async_client.positional_params.with_raw_response.multiple_path_params(
                second="second",
                first="first",
                last="",
                name="name",
            )

    @parametrize
    async def test_method_query(self, async_client: AsyncSink) -> None:
        positional_param = await async_client.positional_params.query(
            foo="foo",
        )
        assert positional_param is None

    @parametrize
    async def test_raw_response_query(self, async_client: AsyncSink) -> None:
        response = await async_client.positional_params.with_raw_response.query(
            foo="foo",
        )

        assert response.is_closed is True
        positional_param = response.parse()
        assert positional_param is None

    @parametrize
    async def test_streaming_response_query(self, async_client: AsyncSink) -> None:
        async with async_client.positional_params.with_streaming_response.query(
            foo="foo",
        ) as response:
            assert not response.is_closed

            positional_param = await response.parse()
            assert positional_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_query_and_path(self, async_client: AsyncSink) -> None:
        positional_param = await async_client.positional_params.query_and_path(
            id="id",
            bar=0,
        )
        assert positional_param is None

    @parametrize
    async def test_raw_response_query_and_path(self, async_client: AsyncSink) -> None:
        response = await async_client.positional_params.with_raw_response.query_and_path(
            id="id",
            bar=0,
        )

        assert response.is_closed is True
        positional_param = response.parse()
        assert positional_param is None

    @parametrize
    async def test_streaming_response_query_and_path(self, async_client: AsyncSink) -> None:
        async with async_client.positional_params.with_streaming_response.query_and_path(
            id="id",
            bar=0,
        ) as response:
            assert not response.is_closed

            positional_param = await response.parse()
            assert positional_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_query_and_path(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.positional_params.with_raw_response.query_and_path(
                id="",
                bar=0,
            )

    @parametrize
    async def test_method_query_multiple(self, async_client: AsyncSink) -> None:
        positional_param = await async_client.positional_params.query_multiple(
            bar="bar",
            foo="foo",
        )
        assert positional_param is None

    @parametrize
    async def test_raw_response_query_multiple(self, async_client: AsyncSink) -> None:
        response = await async_client.positional_params.with_raw_response.query_multiple(
            bar="bar",
            foo="foo",
        )

        assert response.is_closed is True
        positional_param = response.parse()
        assert positional_param is None

    @parametrize
    async def test_streaming_response_query_multiple(self, async_client: AsyncSink) -> None:
        async with async_client.positional_params.with_streaming_response.query_multiple(
            bar="bar",
            foo="foo",
        ) as response:
            assert not response.is_closed

            positional_param = await response.parse()
            assert positional_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_single(self, async_client: AsyncSink) -> None:
        positional_param = await async_client.positional_params.single(
            "single",
        )
        assert positional_param is None

    @parametrize
    async def test_raw_response_single(self, async_client: AsyncSink) -> None:
        response = await async_client.positional_params.with_raw_response.single(
            "single",
        )

        assert response.is_closed is True
        positional_param = response.parse()
        assert positional_param is None

    @parametrize
    async def test_streaming_response_single(self, async_client: AsyncSink) -> None:
        async with async_client.positional_params.with_streaming_response.single(
            "single",
        ) as response:
            assert not response.is_closed

            positional_param = await response.parse()
            assert positional_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_single(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `single` but received ''"):
            await async_client.positional_params.with_raw_response.single(
                "",
            )

    @parametrize
    async def test_method_union_body_and_path(self, async_client: AsyncSink) -> None:
        positional_param = await async_client.positional_params.union_body_and_path(
            id="id",
            kind="VIRTUAL",
        )
        assert positional_param is None

    @parametrize
    async def test_raw_response_union_body_and_path(self, async_client: AsyncSink) -> None:
        response = await async_client.positional_params.with_raw_response.union_body_and_path(
            id="id",
            kind="VIRTUAL",
        )

        assert response.is_closed is True
        positional_param = response.parse()
        assert positional_param is None

    @parametrize
    async def test_streaming_response_union_body_and_path(self, async_client: AsyncSink) -> None:
        async with async_client.positional_params.with_streaming_response.union_body_and_path(
            id="id",
            kind="VIRTUAL",
        ) as response:
            assert not response.is_closed

            positional_param = await response.parse()
            assert positional_param is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_union_body_and_path(self, async_client: AsyncSink) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.positional_params.with_raw_response.union_body_and_path(
                id="",
                kind="VIRTUAL",
            )
