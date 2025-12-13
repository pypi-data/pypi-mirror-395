# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = ["BodyParamObjectWithArrayOfObjectsParams", "ArrayProp"]


class BodyParamObjectWithArrayOfObjectsParams(TypedDict, total=False):
    array_prop: Iterable[ArrayProp]


class ArrayProp(TypedDict, total=False):
    """This is an object with required enum values"""

    kind: Required[Literal["VIRTUAL", "PHYSICAL"]]
