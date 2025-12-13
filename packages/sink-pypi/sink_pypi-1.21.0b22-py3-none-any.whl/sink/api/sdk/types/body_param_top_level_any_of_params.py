# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = ["BodyParamTopLevelAnyOfParams", "ObjectWithRequiredEnum", "SimpleObjectWithRequiredProperty"]


class ObjectWithRequiredEnum(TypedDict, total=False):
    kind: Required[Literal["VIRTUAL", "PHYSICAL"]]


class SimpleObjectWithRequiredProperty(TypedDict, total=False):
    is_foo: Required[bool]


BodyParamTopLevelAnyOfParams: TypeAlias = Union[ObjectWithRequiredEnum, SimpleObjectWithRequiredProperty]
