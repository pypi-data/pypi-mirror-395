# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["QueryParamAllOfParams", "FooAndBar"]


class QueryParamAllOfParams(TypedDict, total=False):
    foo_and_bar: FooAndBar


class FooAndBar(TypedDict, total=False):
    bar: int

    foo: str
