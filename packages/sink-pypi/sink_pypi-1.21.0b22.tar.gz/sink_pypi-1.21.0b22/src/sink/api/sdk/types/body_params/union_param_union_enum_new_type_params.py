# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, TypedDict

from .model_new_type_string import ModelNewTypeString

__all__ = ["UnionParamUnionEnumNewTypeParams"]


class UnionParamUnionEnumNewTypeParams(TypedDict, total=False):
    model: Union[ModelNewTypeString, Literal["gpt-4", "gpt-3"]]
