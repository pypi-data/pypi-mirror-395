# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BodyParamTopLevelAllOfNestedObjectParams", "NestedObj"]


class BodyParamTopLevelAllOfNestedObjectParams(TypedDict, total=False):
    kind: Required[Literal["VIRTUAL", "PHYSICAL"]]

    nested_obj: NestedObj
    """This is an object with required properties"""


class NestedObj(TypedDict, total=False):
    """This is an object with required properties"""

    is_foo: Required[bool]
