# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = ["MixedParamBodyWithTopLevelOneOfAndPathParams", "ObjectWithRequiredEnum", "BasicSharedModelObject"]


class ObjectWithRequiredEnum(TypedDict, total=False):
    kind: Required[Literal["VIRTUAL", "PHYSICAL"]]


class BasicSharedModelObject(TypedDict, total=False):
    bar: Required[str]

    foo: Required[str]


MixedParamBodyWithTopLevelOneOfAndPathParams: TypeAlias = Union[ObjectWithRequiredEnum, BasicSharedModelObject]
