# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, TypeAlias, TypedDict

__all__ = [
    "BodyParamPropertyWithComplexUnionParams",
    "Unions",
    "UnionsObjectWithReadOnlyProperty",
    "UnionsSimpleObjectWithRequiredProperty",
]


class BodyParamPropertyWithComplexUnionParams(TypedDict, total=False):
    name: Required[str]

    unions: Required[Unions]
    """This is an object with required properties"""


class UnionsObjectWithReadOnlyProperty(TypedDict, total=False):
    in_both: bool


class UnionsSimpleObjectWithRequiredProperty(TypedDict, total=False):
    """This is an object with required properties"""

    is_foo: Required[bool]


Unions: TypeAlias = Union[UnionsObjectWithReadOnlyProperty, UnionsSimpleObjectWithRequiredProperty]
