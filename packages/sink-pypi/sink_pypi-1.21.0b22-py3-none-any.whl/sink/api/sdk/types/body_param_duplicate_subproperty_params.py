# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import TypedDict

__all__ = ["BodyParamDuplicateSubpropertyParams", "Baz", "BazBar", "Foo", "FooBar", "Mapping"]


class BodyParamDuplicateSubpropertyParams(TypedDict, total=False):
    baz: Baz

    foo: Foo

    foo_bar: FooBar

    mapping: Mapping

    mappings: Iterable[Mapping]


class BazBar(TypedDict, total=False):
    hello: str


class Baz(TypedDict, total=False):
    bar: BazBar


class FooBar(TypedDict, total=False):
    hello: str


class Foo(TypedDict, total=False):
    bar: FooBar


class Mapping(TypedDict, total=False):
    hello: str
