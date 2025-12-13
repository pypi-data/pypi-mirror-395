# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BodyParamTopLevelAllOfParams"]


class BodyParamTopLevelAllOfParams(TypedDict, total=False):
    is_foo: Required[bool]

    kind: Required[Literal["VIRTUAL", "PHYSICAL"]]
